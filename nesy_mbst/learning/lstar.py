from __future__ import annotations
import logging
from typing import Callable, Dict, List, Optional, Set, Tuple
from nesy_mbst.core.state_machine import DFA
from nesy_mbst.core.observation_table import ObservationTable

logger = logging.getLogger(__name__)


class LStarLearner:
    def __init__(
        self,
        alphabet: Set[str],
        membership_oracle: Callable[[str], Optional[bool]],
        equivalence_oracle: Callable[[DFA], Optional[str]],
        max_iterations: int = 50,
    ):
        self.alphabet = alphabet
        self.membership_oracle = membership_oracle
        self.equivalence_oracle = equivalence_oracle
        self.max_iterations = max_iterations
        self.iteration = 0
        self._init_table()

    def _init_table(self) -> None:
        self.table = ObservationTable(alphabet=self.alphabet)
        self.table.add_prefix("")
        self.table.add_suffix("")
        self._update_cell("", "")

    def _update_cell(self, prefix: str, suffix: str) -> None:
        word = prefix + suffix
        result = self.membership_oracle(word)
        self.table.set_cell(prefix, suffix, result)

    def _update_row(self, prefix: str) -> None:
        for e in self.table.E:
            if self.table.get_cell(prefix, e) is None:
                self._update_cell(prefix, e)

    def _fill_table(self) -> None:
        for s in self.table.S:
            self._update_row(s)
            for a in self.alphabet:
                self._update_row(s + a)

    def _extend_alphabet_row(self, new_suffix: str) -> None:
        self.table.add_suffix(new_suffix)
        for s in self.table.S:
            self._update_cell(s, new_suffix)
            for a in self.alphabet:
                self._update_cell(s + a, new_suffix)

    def _close_table(self) -> bool:
        ext = self.table.find_unclosed_prefix()
        if ext is not None:
            self.table.S.append(ext)
            self._update_row(ext)
            for a in self.alphabet:
                self._update_row(ext + a)
            return False
        return True

    def _make_table_consistent(self) -> bool:
        inc = self.table.find_inconsistency()
        if inc is not None:
            s1, s2, suffix = inc
            for a in self.alphabet:
                new_suffix = a + suffix
                self._extend_alphabet_row(new_suffix)
            return False
        return True

    def _build_dfa(self) -> DFA:
        state_map, accept_states = self.table.build_hypothesis()
        dfa = DFA(alphabet=self.alphabet)
        row_to_q: Dict[Tuple, str] = {}
        for s in self.table.S:
            r = self.table.row(s)
            if r not in row_to_q:
                q = f"q{len(row_to_q)}"
                row_to_q[r] = q
                dfa.add_state(q, is_accept=(r[0] is True))
        for s in self.table.S:
            src_r = self.table.row(s)
            src_q = row_to_q[src_r]
            for a in self.alphabet:
                ext_r = self.table.row(s + a)
                if ext_r in row_to_q:
                    dst_q = row_to_q[ext_r]
                    dfa.add_transition(src_q, a, dst_q)
        dfa.start_state = row_to_q.get(self.table.row(""))
        return dfa

    def learn(self) -> Optional[DFA]:
        self._fill_table()
        for iteration in range(self.max_iterations):
            self.iteration = iteration
            logger.info(f"L* iteration {iteration}: |S|={len(self.table.S)}, |E|={len(self.table.E)}")
            while not self._close_table():
                pass
            while not self._make_table_consistent():
                pass
            hypothesis = self._build_dfa()
            counterexample = self.equivalence_oracle(hypothesis)
            if counterexample is None:
                logger.info(f"L* converged after {iteration} iterations")
                return hypothesis
            logger.info(f"Counterexample found: {counterexample}")
            self._process_counterexample(counterexample)
        logger.warning("L* did not converge within max iterations")
        hypothesis = self._build_dfa()
        return hypothesis

    def _process_counterexample(self, counterexample: str) -> None:
        for i in range(len(counterexample) + 1):
            prefix = counterexample[:i]
            if prefix not in self.table.S:
                self.table.S.append(prefix)
                self._update_row(prefix)
                for a in self.alphabet:
                    self._update_row(prefix + a)
            for suffix_len in range(len(counterexample) - i + 1):
                suffix = counterexample[i : i + suffix_len]
                if suffix not in self.table.E:
                    self._extend_alphabet_row(suffix)
