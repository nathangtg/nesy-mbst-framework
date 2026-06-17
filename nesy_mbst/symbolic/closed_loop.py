from __future__ import annotations
import numpy as np
from typing import Callable, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from nesy_mbst.core.state_machine import MarkovChain


@dataclass
class TelemetrySample:
    path: List[str]
    duration: float
    outcome: str


@dataclass
class ModelDelta:
    added_states: Set[str] = field(default_factory=set)
    removed_states: Set[str] = field(default_factory=set)
    added_transitions: Set[Tuple[str, str]] = field(default_factory=set)
    removed_transitions: Set[Tuple[str, str]] = field(default_factory=set)
    probability_adjustments: Dict[Tuple[str, str], float] = field(default_factory=dict)


class ClosedLoopAdapter:
    def __init__(
        self,
        convergence_threshold: float = 0.05,
        window_size: int = 100,
        alpha: float = 0.3,
        llm_analyzer: Optional[Callable[[str], str]] = None,
    ):
        self.convergence_threshold = convergence_threshold
        self.window_size = window_size
        self.alpha = alpha
        self.llm_analyzer = llm_analyzer
        self.telemetry_buffer: List[TelemetrySample] = []
        self.adaptation_history: List[ModelDelta] = []
        self.converged: bool = False

    def ingest_telemetry(self, sample: TelemetrySample) -> None:
        self.telemetry_buffer.append(sample)
        if len(self.telemetry_buffer) > self.window_size:
            self.telemetry_buffer.pop(0)

    def detect_divergence(self, model: MarkovChain) -> Optional[ModelDelta]:
        if len(self.telemetry_buffer) < 10:
            return None
        delta = ModelDelta()
        empirical_counts: Dict[Tuple[str, str], int] = {}
        state_counts: Dict[str, int] = {}
        for sample in self.telemetry_buffer:
            for i in range(len(sample.path) - 1):
                s, t = sample.path[i], sample.path[i + 1]
                empirical_counts[(s, t)] = empirical_counts.get((s, t), 0) + 1
                state_counts[s] = state_counts.get(s, 0) + 1
        total_transitions = sum(empirical_counts.values())
        if total_transitions == 0:
            return None
        has_divergence = False
        for (s, t), count in empirical_counts.items():
            empirical_prob = count / total_transitions
            if s in model.state_index and t in model.state_index:
                model_prob = model.get_transition(s, t)
                if abs(empirical_prob - model_prob) > self.convergence_threshold:
                    delta.probability_adjustments[(s, t)] = (
                        (1 - self.alpha) * model_prob + self.alpha * empirical_prob
                    )
                    has_divergence = True
        active_states = set(state_counts.keys())
        for s in model.states:
            if s not in active_states and s not in model.terminal_states:
                pass
        for s in active_states:
            if s not in model.state_index:
                delta.added_states.add(s)
                has_divergence = True
        if not has_divergence:
            self.converged = True
            return None
        self.adaptation_history.append(delta)
        return delta

    def apply_delta(self, model: MarkovChain, delta: ModelDelta) -> MarkovChain:
        new_states = list(model.states) + list(delta.added_states)
        state_index = {s: i for i, s in enumerate(new_states)}
        n = len(new_states)
        P_new = np.zeros((n, n))
        old_n = model.P.shape[0]
        P_new[:old_n, :old_n] = model.P
        for (s, t), prob in delta.probability_adjustments.items():
            if s in state_index and t in state_index:
                i, j = state_index[s], state_index[t]
                P_new[i, j] = prob
        P_new = P_new / P_new.sum(axis=1, keepdims=True).clip(min=1e-10)
        mc = MarkovChain()
        mc.build(new_states, terminal_states=model.terminal_states)
        mc.P = P_new
        mc.start_state = model.start_state
        return mc

    def reset(self) -> None:
        self.telemetry_buffer.clear()
        self.adaptation_history.clear()
        self.converged = False
