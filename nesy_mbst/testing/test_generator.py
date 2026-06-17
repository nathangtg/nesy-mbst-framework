from __future__ import annotations
import numpy as np
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from nesy_mbst.core.state_machine import MarkovChain


@dataclass
class TestCase:
    path: List[str]
    transitions: List[Tuple[str, str]]
    expected_length: float
    coverage: Dict[str, Set[str]]


class StatisticalTestGenerator:
    def __init__(
        self,
        model: MarkovChain,
        rng: Optional[np.random.Generator] = None,
        max_path_length: int = 1000,
    ):
        self.model = model
        self.rng = rng or np.random.default_rng()
        self.max_path_length = max_path_length

    def generate_random_walk(self) -> TestCase:
        path = self.model.sample_path(
            length=self.max_path_length, rng=self.rng
        )
        transitions = list(zip(path[:-1], path[1:]))
        coverage = self._compute_path_coverage(path, transitions)
        return TestCase(
            path=path,
            transitions=transitions,
            expected_length=len(transitions),
            coverage=coverage,
        )

    def generate_suite(
        self, n_sequences: int = 100
    ) -> List[TestCase]:
        return [self.generate_random_walk() for _ in range(n_sequences)]

    def generate_coverage_suite(
        self, target_coverage: float = 1.0
    ) -> List[TestCase]:
        suite = []
        covered_states: Set[str] = set()
        covered_transitions: Set[Tuple[str, str]] = set()
        max_attempts = 1000
        for _ in range(max_attempts):
            tc = self.generate_random_walk()
            suite.append(tc)
            covered_states.update(tc.path)
            covered_transitions.update(tc.transitions)
            state_cov = len(covered_states) / self.model.num_states
            trans_cov = len(covered_transitions) / max(
                self.model.num_transitions, 1
            )
            if state_cov >= target_coverage and trans_cov >= target_coverage:
                break
        return suite

    def _compute_path_coverage(
        self, path: List[str], transitions: List[Tuple[str, str]]
    ) -> Dict[str, Set[str]]:
        coverage = {}
        for s in path:
            if s not in coverage:
                coverage[s] = set()
        for s, t in transitions:
            if s in coverage:
                coverage[s].add(t)
        return coverage

    @staticmethod
    def coverage_statistics(
        suite: List[TestCase], model: MarkovChain
    ) -> Dict[str, float]:
        all_states = set(model.states)
        all_transitions = set()
        for i, s in enumerate(model.states):
            for j, t in enumerate(model.states):
                if model.P[i, j] > 0:
                    all_transitions.add((s, t))
        covered_states: Set[str] = set()
        covered_transitions: Set[Tuple[str, str]] = set()
        for tc in suite:
            covered_states.update(tc.path)
            covered_transitions.update(tc.transitions)
        return {
            "state_coverage": len(covered_states) / max(len(all_states), 1),
            "transition_coverage": len(covered_transitions)
            / max(len(all_transitions), 1),
            "num_sequences": len(suite),
            "total_transitions": sum(len(tc.transitions) for tc in suite),
        }
