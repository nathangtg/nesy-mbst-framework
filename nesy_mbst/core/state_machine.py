from __future__ import annotations
import numpy as np
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field


@dataclass
class DFA:
    states: Set[str] = field(default_factory=set)
    alphabet: Set[str] = field(default_factory=set)
    transition: Dict[Tuple[str, str], str] = field(default_factory=dict)
    start_state: Optional[str] = None
    accept_states: Set[str] = field(default_factory=set)

    def add_state(self, state: str, is_accept: bool = False) -> None:
        self.states.add(state)
        if is_accept:
            self.accept_states.add(state)

    def add_transition(self, from_state: str, symbol: str, to_state: str) -> None:
        self.states.add(from_state)
        self.states.add(to_state)
        self.alphabet.add(symbol)
        self.transition[(from_state, symbol)] = to_state

    def run(self, word: str) -> str:
        state = self.start_state
        for sym in word:
            state = self.transition.get((state, sym))
            if state is None:
                return None
        return state

    def accepts(self, word: str) -> bool:
        final = self.run(word)
        return final is not None and final in self.accept_states

    def is_complete(self) -> bool:
        for s in self.states:
            for a in self.alphabet:
                if (s, a) not in self.transition:
                    return False
        return True

    @property
    def num_states(self) -> int:
        return len(self.states)

    @property
    def num_transitions(self) -> int:
        return len(self.transition)


@dataclass
class MarkovChain:
    states: List[str] = field(default_factory=list)
    state_index: Dict[str, int] = field(default_factory=dict)
    P: np.ndarray = None
    start_state: str = None
    terminal_states: Set[str] = field(default_factory=set)

    def __post_init__(self):
        if self.states and self.state_index is None or not self.state_index:
            self.state_index = {s: i for i, s in enumerate(self.states)}
        if isinstance(self.P, list):
            self.P = np.array(self.P, dtype=float)

    def build(self, states: List[str], terminal_states: Set[str] = None):
        self.states = list(states)
        self.state_index = {s: i for i, s in enumerate(self.states)}
        n = len(states)
        self.P = np.zeros((n, n))
        self.terminal_states = terminal_states or set()
        return self

    def set_transition(self, from_state: str, to_state: str, prob: float) -> None:
        i = self.state_index[from_state]
        j = self.state_index[to_state]
        self.P[i, j] = prob

    def get_transition(self, from_state: str, to_state: str) -> float:
        if from_state not in self.state_index or to_state not in self.state_index:
            return 0.0
        i = self.state_index[from_state]
        j = self.state_index[to_state]
        return float(self.P[i, j])

    def validate_row_stochastic(self, tol: float = 1e-10) -> bool:
        row_sums = self.P.sum(axis=1)
        return bool(np.all(np.abs(row_sums - 1.0) < tol))

    def steady_state(self) -> np.ndarray:
        n = self.P.shape[0]
        eigvals, eigvecs = np.linalg.eig(self.P.T)
        idx = np.argmin(np.abs(eigvals - 1.0))
        pi = np.real(eigvecs[:, idx])
        pi = pi / pi.sum()
        return pi

    def mean_first_passage(self, target: str) -> np.ndarray:
        n = self.P.shape[0]
        j = self.state_index[target]
        P_minus = np.delete(np.delete(self.P, j, axis=0), j, axis=1)
        Q = P_minus
        I = np.eye(n - 1)
        m = np.linalg.solve(I - Q, np.ones(n - 1))
        full = np.zeros(n)
        idx = [i for i in range(n) if i != j]
        for k, v in zip(idx, m):
            full[k] = v
        return full

    def sample_path(self, length: int = 100, rng: np.random.Generator = None) -> List[str]:
        if rng is None:
            rng = np.random.default_rng()
        path = []
        state = self.start_state
        for _ in range(length):
            if state in self.terminal_states:
                break
            path.append(state)
            i = self.state_index[state]
            probs = self.P[i]
            if probs.sum() == 0:
                break
            next_idx = rng.choice(len(self.states), p=probs)
            state = self.states[next_idx]
        if state not in self.terminal_states:
            path.append(state)
        return path

    @property
    def num_states(self) -> int:
        return len(self.states)

    @property
    def num_transitions(self) -> int:
        return int(np.count_nonzero(self.P))
