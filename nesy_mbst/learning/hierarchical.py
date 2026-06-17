from __future__ import annotations
import numpy as np
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from nesy_mbst.core.state_machine import MarkovChain


@dataclass
class HigherOrderNode:
    history: Tuple[str, ...]
    children: Dict[str, "HigherOrderNode"] = field(default_factory=dict)
    transitions: Dict[str, float] = field(default_factory=dict)
    is_leaf: bool = False


class HierarchicalModel:
    def __init__(self, order: int = 2):
        self.order = order
        self.root = HigherOrderNode(history=())
        self.first_order: Optional[MarkovChain] = None
        self.high_freq_threshold: float = 0.05
        self.states: List[str] = []
        self.state_index: Dict[str, int] = {}

    def build(self, sequences: List[List[str]], first_order_mc: MarkovChain) -> None:
        self.first_order = first_order_mc
        self.states = first_order_mc.states
        self.state_index = first_order_mc.state_index
        for seq in sequences:
            self._add_sequence(seq)
        self._prune_tree()

    def _add_sequence(self, sequence: List[str]) -> None:
        for i in range(len(sequence)):
            for k in range(1, min(self.order, i + 1) + 1):
                history = tuple(sequence[i - k : i])
                current = sequence[i]
                self._update_transition(history, current)

    def _update_transition(self, history: Tuple[str, ...], next_state: str) -> None:
        node = self.root
        for h in history:
            if h not in node.children:
                node.children[h] = HigherOrderNode(history=node.history + (h,))
            node = node.children[h]
        node.transitions[next_state] = node.transitions.get(next_state, 0) + 1

    def _prune_tree(self) -> None:
        self._normalize_node(self.root)

    def _normalize_node(self, node: HigherOrderNode) -> None:
        total = sum(node.transitions.values())
        if total > 0:
            for s in node.transitions:
                node.transitions[s] /= total
        for child in node.children.values():
            self._normalize_node(child)

    def get_probability(self, history: Tuple[str, ...], next_state: str) -> float:
        node = self.root
        start = max(0, len(history) - self.order)
        for h in history[start:]:
            if h in node.children:
                node = node.children[h]
            else:
                break
        if node.transitions and next_state in node.transitions:
            return node.transitions[next_state]
        if self.first_order and history and history[-1] in self.first_order.state_index:
            return self.first_order.get_transition(history[-1], next_state)
        return 0.0

    def sample_path(
        self, length: int = 100, rng: np.random.Generator = None
    ) -> List[str]:
        if rng is None:
            rng = np.random.default_rng()
        path = [self.first_order.start_state] if self.first_order else []
        for _ in range(length):
            if not path:
                break
            history = tuple(path[-self.order :]) if path else ()
            probs = []
            states = self.states if self.states else []
            for s in states:
                probs.append(self.get_probability(history, s))
            probs = np.array(probs)
            if probs.sum() == 0:
                break
            probs /= probs.sum()
            next_s = rng.choice(states, p=probs)
            path.append(next_s)
            if self.first_order and next_s in self.first_order.terminal_states:
                break
        return path

    def steady_state(self) -> np.ndarray:
        if self.first_order:
            return self.first_order.steady_state()
        return np.array([])
