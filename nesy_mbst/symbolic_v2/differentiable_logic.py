"""
Differentiable Logic Integration (DLI)
=======================================
Replaces discrete Boolean feasibility checking with continuous relaxations
using fuzzy logic t-norms, enabling gradient flow through the full pipeline.

Key contributions:
- Product, Lukasiewicz, and Godel t-norm implementations
- Adaptive temperature annealing (loss-dependent)
- End-to-end differentiable constraint satisfaction
- Hard-constraint guarantee recovery via projection

References:
- van Krieken et al. (2022). Analyzing Differentiable Fuzzy Logic Operators. AIJ.
- Xu et al. (2018). A Semantic Loss Function for Deep Learning with Symbolic Knowledge. ICML.
"""
from __future__ import annotations

import numpy as np
from typing import Callable, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum

from nesy_mbst.core.state_machine import MarkovChain


class TNormType(Enum):
    """Fuzzy logic t-norm types for differentiable conjunction."""
    PRODUCT = "product"
    LUKASIEWICZ = "lukasiewicz"
    GODEL = "godel"


@dataclass
class TemperatureScheduler:
    """
    Adaptive temperature annealing for smooth -> hard logic transition.

    As training progresses, temperature decreases, making soft logic
    gates approach hard Boolean behavior while maintaining differentiability.
    """
    initial_temp: float = 5.0
    min_temp: float = 0.1
    schedule: str = "adaptive"  # "linear", "exponential", "cosine", "adaptive"
    decay_rate: float = 0.95
    _current_temp: float = field(init=False, default=5.0)
    _step: int = field(init=False, default=0)
    _initial_loss: Optional[float] = field(init=False, default=None)

    def __post_init__(self):
        self._current_temp = self.initial_temp

    @property
    def temperature(self) -> float:
        return self._current_temp

    def step(self, loss: Optional[float] = None) -> float:
        """Advance scheduler by one step, return new temperature."""
        self._step += 1

        if self.schedule == "linear":
            self._current_temp = max(
                self.min_temp,
                self.initial_temp - (self.initial_temp - self.min_temp) * self._step / 1000
            )
        elif self.schedule == "exponential":
            self._current_temp = max(
                self.min_temp,
                self.initial_temp * (self.decay_rate ** self._step)
            )
        elif self.schedule == "cosine":
            # Cosine annealing with warm restarts
            period = 100
            progress = (self._step % period) / period
            self._current_temp = self.min_temp + \
                (self.initial_temp - self.min_temp) * 0.5 * (1 + np.cos(np.pi * progress))
        elif self.schedule == "adaptive":
            # Loss-dependent: anneal faster when loss is low
            if loss is not None:
                if self._initial_loss is None:
                    self._initial_loss = loss
                ratio = loss / max(self._initial_loss, 1e-8)
                # Temperature proportional to remaining loss
                self._current_temp = max(
                    self.min_temp,
                    self.min_temp + (self.initial_temp - self.min_temp) * ratio
                )
            else:
                # Fallback to exponential if no loss provided
                self._current_temp = max(
                    self.min_temp,
                    self.initial_temp * (self.decay_rate ** self._step)
                )

        return self._current_temp

    def reset(self) -> None:
        self._current_temp = self.initial_temp
        self._step = 0
        self._initial_loss = None


class DifferentiableLogicGate:
    """
    Differentiable logic gate that replaces hard Boolean feasibility checks.

    Instead of binary {0, 1} outputs, produces continuous values in [0, 1]
    with well-defined gradients everywhere. Temperature annealing recovers
    hard logic at convergence.
    """

    def __init__(
        self,
        t_norm: TNormType = TNormType.PRODUCT,
        temperature: float = 1.0,
    ):
        self.t_norm = t_norm
        self.temperature = temperature

    def sigmoid(self, x: float) -> float:
        """Temperature-scaled sigmoid activation."""
        z = x / max(self.temperature, 1e-8)
        # Numerically stable sigmoid
        if z >= 0:
            return 1.0 / (1.0 + np.exp(-z))
        else:
            ez = np.exp(z)
            return ez / (1.0 + ez)

    def sigmoid_grad(self, x: float) -> float:
        """Gradient of temperature-scaled sigmoid."""
        s = self.sigmoid(x)
        return s * (1 - s) / max(self.temperature, 1e-8)

    def conjunction(self, a: float, b: float) -> float:
        """Differentiable AND (t-norm)."""
        if self.t_norm == TNormType.PRODUCT:
            return a * b
        elif self.t_norm == TNormType.LUKASIEWICZ:
            return max(0.0, a + b - 1.0)
        elif self.t_norm == TNormType.GODEL:
            return min(a, b)
        return a * b

    def disjunction(self, a: float, b: float) -> float:
        """Differentiable OR (t-conorm)."""
        if self.t_norm == TNormType.PRODUCT:
            return a + b - a * b
        elif self.t_norm == TNormType.LUKASIEWICZ:
            return min(1.0, a + b)
        elif self.t_norm == TNormType.GODEL:
            return max(a, b)
        return a + b - a * b

    def negation(self, a: float) -> float:
        """Differentiable NOT (standard negation)."""
        return 1.0 - a

    def implication(self, a: float, b: float) -> float:
        """Differentiable implication: a -> b = NOT(a) OR b."""
        return self.disjunction(self.negation(a), b)

    def evaluate_constraint(
        self,
        logit: float,
        threshold: float = 0.0,
    ) -> float:
        """
        Evaluate a single constraint as a soft truth value.

        Args:
            logit: Raw constraint score (positive = satisfied, negative = violated)
            threshold: Decision boundary

        Returns:
            Soft truth value in [0, 1]
        """
        return self.sigmoid(logit - threshold)

    def batch_conjunction(self, values: List[float]) -> float:
        """Apply conjunction over multiple soft truth values."""
        if not values:
            return 1.0
        result = values[0]
        for v in values[1:]:
            result = self.conjunction(result, v)
        return result


class DLIFeasibilityChecker:
    """
    Differentiable feasibility checker that replaces SymbolicFeasibilityMemory.

    Instead of returning Boolean feasible/infeasible, returns continuous
    feasibility scores in [0, 1] that:
    1. Enable gradient flow to upstream components
    2. Gracefully degrade near constraint boundaries
    3. Converge to hard Boolean at low temperature
    """

    def __init__(
        self,
        t_norm: TNormType = TNormType.PRODUCT,
        scheduler: Optional[TemperatureScheduler] = None,
    ):
        self.scheduler = scheduler or TemperatureScheduler()
        self.gate = DifferentiableLogicGate(
            t_norm=t_norm,
            temperature=self.scheduler.temperature
        )
        self.blocked_transitions: Set[Tuple[str, str]] = set()
        self.soft_constraints: List[Callable[[str, str], float]] = []
        self.constraint_weights: List[float] = []
        self._feasibility_cache: Dict[Tuple[str, str], float] = {}

    def add_blocked_transition(self, from_state: str, to_state: str) -> None:
        """Hard block a transition (score = 0 regardless of temperature)."""
        self.blocked_transitions.add((from_state, to_state))

    def add_soft_constraint(
        self,
        constraint_fn: Callable[[str, str], float],
        weight: float = 1.0,
    ) -> None:
        """
        Add a soft constraint function.

        The function takes (from_state, to_state) and returns a logit
        (positive = more feasible, negative = less feasible).
        """
        self.soft_constraints.append(constraint_fn)
        self.constraint_weights.append(weight)

    def feasibility_score(
        self,
        from_state: str,
        to_state: str,
        context: Optional[Dict[str, float]] = None,
    ) -> float:
        """
        Compute differentiable feasibility score for a transition.

        Returns:
            Score in [0, 1] where 1.0 = fully feasible, 0.0 = infeasible
        """
        # Hard blocks always return 0
        if (from_state, to_state) in self.blocked_transitions:
            return 0.0

        # Check cache
        cache_key = (from_state, to_state)
        if cache_key in self._feasibility_cache:
            return self._feasibility_cache[cache_key]

        # Update gate temperature
        self.gate.temperature = self.scheduler.temperature

        # Evaluate all soft constraints
        scores = []
        for i, constraint_fn in enumerate(self.soft_constraints):
            logit = constraint_fn(from_state, to_state)
            weight = self.constraint_weights[i]
            soft_truth = self.gate.evaluate_constraint(logit * weight)
            scores.append(soft_truth)

        # If no constraints, default feasible
        if not scores:
            result = 1.0
        else:
            # Combine via t-norm (all constraints must be satisfied)
            result = self.gate.batch_conjunction(scores)

        self._feasibility_cache[cache_key] = result
        return result

    def validate_transition_matrix(
        self,
        states: List[str],
        P: np.ndarray,
        context: Optional[Dict[str, float]] = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Apply differentiable feasibility checking to transition matrix.

        Returns:
            Tuple of (validated_P, feasibility_mask) where:
            - validated_P: probability matrix scaled by feasibility scores
            - feasibility_mask: matrix of feasibility scores for each transition
        """
        n = len(states)
        mask = np.ones((n, n))

        for i, s_i in enumerate(states):
            for j, s_j in enumerate(states):
                mask[i, j] = self.feasibility_score(s_i, s_j, context)

        # Scale probabilities by feasibility (differentiable masking)
        validated = P * mask

        # Re-normalize rows (maintain stochasticity)
        row_sums = validated.sum(axis=1, keepdims=True)
        row_sums = np.where(row_sums == 0, 1.0, row_sums)
        validated = validated / row_sums

        return validated, mask

    def compute_loss(
        self,
        states: List[str],
        P: np.ndarray,
        target_constraints: Optional[Dict[Tuple[str, str], float]] = None,
    ) -> float:
        """
        Compute differentiable constraint satisfaction loss.

        This loss can be backpropagated through the pipeline to
        optimize upstream components (oracle, learner, solver).
        """
        n = len(states)
        loss = 0.0

        # Penalty for probability mass on infeasible transitions
        for i, s_i in enumerate(states):
            for j, s_j in enumerate(states):
                if P[i, j] > 1e-8:
                    feasibility = self.feasibility_score(s_i, s_j)
                    # Loss proportional to probability * infeasibility
                    loss += P[i, j] * (1.0 - feasibility)

        # Target constraint matching loss
        if target_constraints:
            for (s_i, s_j), target_score in target_constraints.items():
                actual_score = self.feasibility_score(s_i, s_j)
                loss += (actual_score - target_score) ** 2

        return loss

    def step(self, loss: Optional[float] = None) -> float:
        """
        Advance temperature schedule and clear cache.

        Returns new temperature.
        """
        self._feasibility_cache.clear()
        return self.scheduler.step(loss)

    def project_to_hard(self, threshold: float = 0.5) -> Set[Tuple[str, str]]:
        """
        Project current soft feasibility to hard Boolean decisions.

        Used at the end of training to recover discrete guarantees.
        """
        hard_blocked = set(self.blocked_transitions)

        for (s_i, s_j), score in self._feasibility_cache.items():
            if score < threshold:
                hard_blocked.add((s_i, s_j))

        return hard_blocked

    def reset(self) -> None:
        self._feasibility_cache.clear()
        self.scheduler.reset()
        self.gate.temperature = self.scheduler.temperature
