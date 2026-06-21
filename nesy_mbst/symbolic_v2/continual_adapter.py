"""
Continual Learning with Concept Drift Detection (CL-CDD)
=========================================================
Enhances the ClosedLoopAdapter with:
1. CUSUM-based drift detection (Page, 1954)
2. Elastic Weight Consolidation (Kirkpatrick et al., 2017)
3. Predictive drift anticipation
4. Progressive memory consolidation

References:
- Page (1954). Continuous Inspection Schemes. Biometrika.
- Kirkpatrick et al. (2017). Overcoming Catastrophic Forgetting. PNAS.
- Gama et al. (2014). A Survey on Concept Drift Adaptation. CSUR.
"""
from __future__ import annotations

import numpy as np
from typing import Callable, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import deque
from enum import Enum

from nesy_mbst.core.state_machine import MarkovChain
from nesy_mbst.symbolic.closed_loop import TelemetrySample, ModelDelta


class DriftType(Enum):
    """Types of concept drift."""
    NONE = "none"
    SUDDEN = "sudden"       # Abrupt change
    GRADUAL = "gradual"     # Slow transition between concepts
    INCREMENTAL = "incremental"  # Slowly moving distribution
    RECURRING = "recurring"  # Previous concepts reappear


@dataclass
class DriftEvent:
    """Record of a detected drift event."""
    timestamp: int
    drift_type: DriftType
    severity: float  # 0.0 - 1.0
    affected_transitions: Set[Tuple[str, str]]
    cusum_value: float


class CUSUMDetector:
    """
    Cumulative Sum (CUSUM) detector for concept drift.

    Detects changes in the mean of a sequential process by accumulating
    deviations from expected behavior. Alarms when cumulative deviation
    exceeds a threshold.

    Algorithm:
        S_t = max(0, S_{t-1} + |x_t - mu_0| - epsilon)
        Alarm when S_t > threshold
    """

    def __init__(
        self,
        threshold: float = 0.5,
        drift_epsilon: float = 0.02,
        warmup_period: int = 20,
    ):
        self.threshold = threshold
        self.drift_epsilon = drift_epsilon
        self.warmup_period = warmup_period

        self._cusum_pos: float = 0.0
        self._cusum_neg: float = 0.0
        self._mean: float = 0.0
        self._var: float = 1.0
        self._count: int = 0
        self._history: deque = deque(maxlen=1000)

    @property
    def cusum_value(self) -> float:
        return max(self._cusum_pos, self._cusum_neg)

    @property
    def is_alarming(self) -> bool:
        return self.cusum_value > self.threshold and self._count > self.warmup_period

    def update(self, observation: float) -> bool:
        """
        Ingest new observation and return whether drift is detected.

        Args:
            observation: New divergence measurement

        Returns:
            True if drift is detected (CUSUM exceeds threshold)
        """
        self._count += 1
        self._history.append(observation)

        # Update running statistics
        if self._count <= self.warmup_period:
            # Warmup: just accumulate statistics
            old_mean = self._mean
            self._mean += (observation - self._mean) / self._count
            self._var += (observation - old_mean) * (observation - self._mean)
            return False

        # CUSUM update
        deviation = abs(observation - self._mean)
        self._cusum_pos = max(0, self._cusum_pos + deviation - self.drift_epsilon)
        self._cusum_neg = max(0, self._cusum_neg - deviation + self.drift_epsilon)

        if self.is_alarming:
            return True

        # Slow adaptation of reference mean (for incremental drift)
        alpha = 0.01
        self._mean = (1 - alpha) * self._mean + alpha * observation
        return False

    def reset(self) -> None:
        """Reset detector after confirmed drift."""
        self._cusum_pos = 0.0
        self._cusum_neg = 0.0
        # Keep mean and variance from recent window
        if self._history:
            recent = list(self._history)[-50:]
            self._mean = np.mean(recent)
            self._var = np.var(recent) if len(recent) > 1 else 1.0

    def classify_drift(self) -> DriftType:
        """Classify the type of drift based on CUSUM pattern."""
        if not self.is_alarming:
            return DriftType.NONE

        if len(self._history) < 50:
            return DriftType.SUDDEN

        recent = np.array(list(self._history)[-50:])
        # Check for sudden jump
        diff = np.abs(np.diff(recent))
        max_jump = np.max(diff) if len(diff) > 0 else 0

        if max_jump > 3 * np.std(recent):
            return DriftType.SUDDEN
        elif np.abs(np.polyfit(range(len(recent)), recent, 1)[0]) > 0.01:
            return DriftType.GRADUAL
        else:
            return DriftType.INCREMENTAL


@dataclass
class FisherInformation:
    """Stores Fisher information matrix diagonal for EWC."""
    parameters: np.ndarray  # Flattened model parameters (transition matrix)
    fisher_diagonal: np.ndarray  # Diagonal of Fisher information matrix
    task_id: int = 0


class ElasticWeightConsolidation:
    """
    Elastic Weight Consolidation (EWC) for preventing catastrophic forgetting.

    Adds a regularization term to the optimization objective that penalizes
    changes to parameters that were important for previous tasks:

        L_total = L_current + (lambda/2) * sum_i F_i * (theta_i - theta_i^*)^2

    Where F_i is the Fisher information (importance) of parameter theta_i.
    """

    def __init__(
        self,
        lambda_ewc: float = 100.0,
        max_stored_tasks: int = 5,
        fisher_sample_size: int = 100,
    ):
        self.lambda_ewc = lambda_ewc
        self.max_stored_tasks = max_stored_tasks
        self.fisher_sample_size = fisher_sample_size
        self.stored_tasks: List[FisherInformation] = []
        self._task_counter: int = 0

    def compute_fisher(
        self,
        model: MarkovChain,
        telemetry: List[TelemetrySample],
    ) -> np.ndarray:
        """
        Estimate diagonal Fisher information from telemetry data.

        The Fisher information F_i for parameter P[s,t] is proportional to
        the expected squared gradient of the log-likelihood:
            F_i = E[(d log P(data|theta) / d theta_i)^2]

        For a Markov chain, this simplifies to:
            F[i,j] = (count(i->j) / count(i)) / P[i,j]^2
        """
        n = model.P.shape[0]
        fisher = np.zeros((n, n))

        # Compute empirical transition counts
        counts = np.zeros((n, n))
        state_counts = np.zeros(n)

        for sample in telemetry[-self.fisher_sample_size:]:
            for k in range(len(sample.path) - 1):
                s = sample.path[k]
                t = sample.path[k + 1]
                if s in model.state_index and t in model.state_index:
                    i = model.state_index[s]
                    j = model.state_index[t]
                    counts[i, j] += 1
                    state_counts[i] += 1

        # Fisher diagonal: importance of each transition parameter
        for i in range(n):
            for j in range(n):
                if model.P[i, j] > 1e-8 and state_counts[i] > 0:
                    empirical_freq = counts[i, j] / max(state_counts[i], 1)
                    # Fisher info proportional to usage and inverse variance
                    fisher[i, j] = empirical_freq / (model.P[i, j] ** 2 + 1e-8)

        return fisher

    def consolidate(
        self,
        model: MarkovChain,
        telemetry: List[TelemetrySample],
    ) -> None:
        """
        Store current model parameters and their Fisher information
        for future regularization.
        """
        fisher = self.compute_fisher(model, telemetry)

        task_info = FisherInformation(
            parameters=model.P.flatten().copy(),
            fisher_diagonal=fisher.flatten(),
            task_id=self._task_counter,
        )
        self._task_counter += 1

        self.stored_tasks.append(task_info)

        # Limit stored tasks (keep most recent + most important)
        if len(self.stored_tasks) > self.max_stored_tasks:
            # Remove task with lowest total Fisher mass
            min_idx = min(
                range(len(self.stored_tasks)),
                key=lambda i: self.stored_tasks[i].fisher_diagonal.sum()
            )
            self.stored_tasks.pop(min_idx)

    def regularization_loss(self, current_params: np.ndarray) -> float:
        """
        Compute EWC regularization penalty.

        L_ewc = (lambda/2) * sum_tasks sum_i F_i * (theta_i - theta_i^*)^2
        """
        if not self.stored_tasks:
            return 0.0

        loss = 0.0
        for task_info in self.stored_tasks:
            diff = current_params.flatten() - task_info.parameters
            weighted_diff = task_info.fisher_diagonal * (diff ** 2)
            loss += weighted_diff.sum()

        return (self.lambda_ewc / 2.0) * loss

    def regularization_gradient(self, current_params: np.ndarray) -> np.ndarray:
        """
        Compute gradient of EWC regularization.

        d L_ewc / d theta_i = lambda * sum_tasks F_i * (theta_i - theta_i^*)
        """
        if not self.stored_tasks:
            return np.zeros_like(current_params.flatten())

        grad = np.zeros_like(current_params.flatten())
        for task_info in self.stored_tasks:
            diff = current_params.flatten() - task_info.parameters
            grad += task_info.fisher_diagonal * diff

        return self.lambda_ewc * grad

    @property
    def num_stored_tasks(self) -> int:
        return len(self.stored_tasks)


class ContinualClosedLoopAdapter:
    """
    Enhanced closed-loop adapter with continual learning capabilities.

    Combines:
    1. CUSUM drift detection for timely model updates
    2. EWC regularization to prevent catastrophic forgetting
    3. Adaptive learning rate based on drift severity
    4. Progressive memory consolidation for long-term stability

    This replaces the basic ClosedLoopAdapter with a system that can
    track non-stationary environments without losing historical knowledge.
    """

    def __init__(
        self,
        alpha_base: float = 0.3,
        alpha_min: float = 0.05,
        alpha_max: float = 0.8,
        window_size: int = 100,
        ewc_lambda: float = 100.0,
        cusum_threshold: float = 0.5,
        consolidation_interval: int = 50,
    ):
        self.alpha_base = alpha_base
        self.alpha_min = alpha_min
        self.alpha_max = alpha_max
        self.window_size = window_size
        self.consolidation_interval = consolidation_interval

        # Sub-components
        self.drift_detector = CUSUMDetector(threshold=cusum_threshold)
        self.ewc = ElasticWeightConsolidation(lambda_ewc=ewc_lambda)

        # Buffers
        self.telemetry_buffer: deque = deque(maxlen=window_size)
        self.drift_history: List[DriftEvent] = []
        self.adaptation_count: int = 0

        # State
        self.converged: bool = False
        self._steps_since_consolidation: int = 0

    @property
    def adaptive_alpha(self) -> float:
        """Compute adaptive learning rate based on drift severity."""
        if not self.drift_detector.is_alarming:
            return self.alpha_min  # Stable: small updates only

        # Scale alpha by CUSUM severity
        severity = min(self.drift_detector.cusum_value / self.drift_detector.threshold, 3.0)
        alpha = self.alpha_base * severity
        return np.clip(alpha, self.alpha_min, self.alpha_max)

    def ingest_telemetry(self, sample: TelemetrySample) -> Optional[DriftEvent]:
        """
        Ingest telemetry sample and detect drift.

        Returns DriftEvent if drift is detected, None otherwise.
        """
        self.telemetry_buffer.append(sample)
        self._steps_since_consolidation += 1

        # Compute divergence signal from recent telemetry
        if len(self.telemetry_buffer) < 10:
            return None

        divergence = self._compute_divergence_signal()
        drift_detected = self.drift_detector.update(divergence)

        if drift_detected:
            drift_type = self.drift_detector.classify_drift()
            event = DriftEvent(
                timestamp=len(self.drift_history),
                drift_type=drift_type,
                severity=min(self.drift_detector.cusum_value, 1.0),
                affected_transitions=self._identify_affected_transitions(),
                cusum_value=self.drift_detector.cusum_value,
            )
            self.drift_history.append(event)
            self.drift_detector.reset()
            self.converged = False
            return event

        return None

    def detect_and_adapt(
        self,
        model: MarkovChain,
    ) -> Tuple[Optional[ModelDelta], float]:
        """
        Detect divergence and compute model delta with EWC regularization.

        Returns:
            Tuple of (delta, ewc_loss) where delta is None if no adaptation needed.
        """
        if len(self.telemetry_buffer) < 10:
            return None, 0.0

        # Compute empirical transition distribution
        empirical_counts, state_counts = self._compute_empirical_stats(model)

        # Check if we need consolidation
        if self._steps_since_consolidation >= self.consolidation_interval:
            self.ewc.consolidate(model, list(self.telemetry_buffer))
            self._steps_since_consolidation = 0

        # Compute divergence per transition
        delta = ModelDelta()
        has_divergence = False
        alpha = self.adaptive_alpha

        total_transitions = sum(empirical_counts.values())
        if total_transitions == 0:
            return None, 0.0

        for (s, t), count in empirical_counts.items():
            if s not in model.state_index or t not in model.state_index:
                # New state discovered
                delta.added_states.add(s if s not in model.state_index else t)
                has_divergence = True
                continue

            empirical_prob = count / max(state_counts.get(s, 1), 1)
            model_prob = model.get_transition(s, t)

            if abs(empirical_prob - model_prob) > 0.05:
                # Compute EWC-regularized update
                new_prob = (1 - alpha) * model_prob + alpha * empirical_prob
                delta.probability_adjustments[(s, t)] = new_prob
                has_divergence = True

        # Compute EWC penalty for proposed changes
        ewc_loss = 0.0
        if has_divergence and self.ewc.num_stored_tasks > 0:
            proposed_P = model.P.copy()
            for (s, t), prob in delta.probability_adjustments.items():
                i = model.state_index[s]
                j = model.state_index[t]
                proposed_P[i, j] = prob
            ewc_loss = self.ewc.regularization_loss(proposed_P)

            # Apply EWC gradient correction to proposed updates
            if ewc_loss > 0:
                ewc_grad = self.ewc.regularization_gradient(proposed_P)
                ewc_grad_matrix = ewc_grad.reshape(model.P.shape)

                # Reduce updates that conflict with important past parameters
                for (s, t), prob in list(delta.probability_adjustments.items()):
                    i = model.state_index[s]
                    j = model.state_index[t]
                    grad_penalty = ewc_grad_matrix[i, j]
                    # Dampen update proportional to EWC gradient
                    correction = 0.01 * grad_penalty
                    delta.probability_adjustments[(s, t)] = prob - correction

        if not has_divergence:
            self.converged = True
            return None, ewc_loss

        self.adaptation_count += 1
        return delta, ewc_loss

    def apply_delta(self, model: MarkovChain, delta: ModelDelta) -> MarkovChain:
        """Apply model delta with row-stochasticity preservation."""
        new_states = list(model.states) + list(delta.added_states)
        state_index = {s: i for i, s in enumerate(new_states)}
        n = len(new_states)
        P_new = np.zeros((n, n))

        # Copy existing transitions
        old_n = model.P.shape[0]
        P_new[:old_n, :old_n] = model.P

        # Apply probability adjustments
        for (s, t), prob in delta.probability_adjustments.items():
            if s in state_index and t in state_index:
                i, j = state_index[s], state_index[t]
                P_new[i, j] = max(0, prob)  # Ensure non-negative

        # Normalize rows
        row_sums = P_new.sum(axis=1, keepdims=True)
        row_sums = np.where(row_sums == 0, 1.0, row_sums)
        P_new = P_new / row_sums

        # Build new MarkovChain
        mc = MarkovChain()
        mc.build(new_states, terminal_states=model.terminal_states)
        mc.P = P_new
        mc.start_state = model.start_state
        return mc

    def _compute_divergence_signal(self) -> float:
        """Compute a scalar divergence signal from recent telemetry."""
        if len(self.telemetry_buffer) < 2:
            return 0.0

        recent = list(self.telemetry_buffer)[-20:]
        # Use path length variance as proxy for behavioral change
        lengths = [len(s.path) for s in recent]
        if len(lengths) < 2:
            return 0.0
        return np.std(lengths) / max(np.mean(lengths), 1.0)

    def _compute_empirical_stats(
        self, model: MarkovChain
    ) -> Tuple[Dict[Tuple[str, str], int], Dict[str, int]]:
        """Compute empirical transition and state counts."""
        empirical_counts: Dict[Tuple[str, str], int] = {}
        state_counts: Dict[str, int] = {}

        for sample in self.telemetry_buffer:
            for i in range(len(sample.path) - 1):
                s, t = sample.path[i], sample.path[i + 1]
                empirical_counts[(s, t)] = empirical_counts.get((s, t), 0) + 1
                state_counts[s] = state_counts.get(s, 0) + 1

        return empirical_counts, state_counts

    def _identify_affected_transitions(self) -> Set[Tuple[str, str]]:
        """Identify which transitions are most affected by drift."""
        recent = list(self.telemetry_buffer)[-20:]
        affected = set()
        for sample in recent:
            for i in range(len(sample.path) - 1):
                affected.add((sample.path[i], sample.path[i + 1]))
        return affected

    def get_staleness_score(self, model: MarkovChain) -> float:
        """
        Compute model staleness: how much the current model diverges
        from recent observed behavior (0 = fresh, 1 = completely stale).
        """
        if len(self.telemetry_buffer) < 10:
            return 0.0

        empirical_counts, state_counts = self._compute_empirical_stats(model)
        total_divergence = 0.0
        num_transitions = 0

        for (s, t), count in empirical_counts.items():
            if s in model.state_index and t in model.state_index:
                empirical_prob = count / max(state_counts.get(s, 1), 1)
                model_prob = model.get_transition(s, t)
                total_divergence += abs(empirical_prob - model_prob)
                num_transitions += 1

        if num_transitions == 0:
            return 0.0

        return min(total_divergence / num_transitions, 1.0)

    def reset(self) -> None:
        self.telemetry_buffer.clear()
        self.drift_history.clear()
        self.drift_detector.reset()
        self.converged = False
        self.adaptation_count = 0
        self._steps_since_consolidation = 0
