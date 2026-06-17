from __future__ import annotations
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from nesy_mbst.core.state_machine import DFA


@dataclass
class FeasibilityRule:
    precondition: Dict[str, bool]
    guard: Optional[str] = None
    description: str = ""


class SymbolicFeasibilityMemory:
    def __init__(self):
        self.invariants: Dict[str, FeasibilityRule] = {}
        self.state_preconditions: Dict[str, Set[str]] = {}
        self.blocked_transitions: Set[Tuple[str, str]] = set()

    def add_invariant(self, state: str, rule: FeasibilityRule) -> None:
        self.invariants[state] = rule

    def add_precondition(self, state: str, required_flag: str) -> None:
        if state not in self.state_preconditions:
            self.state_preconditions[state] = set()
        self.state_preconditions[state].add(required_flag)

    def block_transition(self, from_state: str, to_state: str) -> None:
        self.blocked_transitions.add((from_state, to_state))

    def is_feasible(
        self,
        from_state: str,
        to_state: str,
        context: Optional[Dict[str, bool]] = None,
    ) -> bool:
        if (from_state, to_state) in self.blocked_transitions:
            return False
        if context and from_state in self.state_preconditions:
            preconditions = self.state_preconditions[from_state]
            for flag in preconditions:
                if not context.get(flag, False):
                    return False
        return True

    def validate_dfa(self, dfa: DFA, context: Dict[str, bool]) -> DFA:
        validated = DFA(
            states=set(dfa.states),
            alphabet=set(dfa.alphabet),
            start_state=dfa.start_state,
            accept_states=set(dfa.accept_states),
        )
        for (s, a), t in dfa.transition.items():
            if self.is_feasible(s, t, context):
                validated.add_transition(s, a, t)
        return validated

    def validate_transition_matrix(
        self, states: List[str], P: "np.ndarray", context: Dict[str, bool]
    ) -> "np.ndarray":
        import numpy as np
        validated = P.copy()
        for i, s_i in enumerate(states):
            for j, s_j in enumerate(states):
                if not self.is_feasible(s_i, s_j, context):
                    validated[i, j] = 0.0
        row_sums = validated.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1.0
        validated = validated / row_sums
        return validated
