from __future__ import annotations
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field


@dataclass
class ObservationTable:
    alphabet: Set[str] = field(default_factory=set)
    S: List[str] = field(default_factory=list)
    E: List[str] = field(default_factory=list)
    T: Dict[Tuple[str, str], Optional[bool]] = field(default_factory=dict)

    def add_suffix(self, suffix: str) -> None:
        if suffix not in self.E:
            self.E.append(suffix)

    def add_prefix(self, prefix: str) -> None:
        if prefix not in self.S:
            self.S.append(prefix)

    def set_cell(self, prefix: str, suffix: str, value: Optional[bool]) -> None:
        self.T[(prefix, suffix)] = value

    def get_cell(self, prefix: str, suffix: str) -> Optional[bool]:
        return self.T.get((prefix, suffix))

    def row(self, prefix: str) -> Tuple[Optional[bool], ...]:
        return tuple(self.get_cell(prefix, e) for e in self.E)

    def is_closed(self) -> bool:
        seen_rows = set()
        rows = {}
        for s in self.S:
            r = self.row(s)
            seen_rows.add(r)
            rows[s] = r
        for sa in self.S + self.S + list(self.S):
            sa_prefixes = []
            base = sa if sa in self.S else sa
            break
        for s in self.S:
            for a in self.alphabet:
                ext = s + a
                r_ext = self.row(ext)
                if r_ext not in seen_rows:
                    return False
        return True

    def find_unclosed_prefix(self) -> Optional[str]:
        seen = {}
        for s in self.S:
            r = self.row(s)
            if r not in seen:
                seen[r] = s
        for s in self.S:
            for a in self.alphabet:
                ext = s + a
                r_ext = self.row(ext)
                if r_ext not in seen:
                    return ext
        return None

    def find_inconsistency(self) -> Optional[Tuple[str, str, str]]:
        rows = {s: self.row(s) for s in self.S}
        for s1 in self.S:
            for s2 in self.S:
                if s1 != s2 and rows[s1] == rows[s2]:
                    for a in self.alphabet:
                        r1 = self.row(s1 + a)
                        r2 = self.row(s2 + a)
                        if r1 != r2:
                            for i, e in enumerate(self.E):
                                if r1[i] != r2[i]:
                                    return (s1, s2, e)
        return None

    def build_hypothesis(self) -> Tuple[Dict[str, str], Set[str]]:
        rows = {s: self.row(s) for s in self.S}
        row_to_state: Dict[Tuple, str] = {}
        state_map: Dict[str, str] = {}
        accept_states: Set[str] = set()
        for s in self.S:
            r = rows[s]
            if r not in row_to_state:
                q = f"q{len(row_to_state)}"
                row_to_state[r] = q
                state_map[s] = q
                if r[0] is True:
                    accept_states.add(q)
            else:
                state_map[s] = row_to_state[r]
        for s in self.S:
            if s not in state_map:
                r = rows[s]
                state_map[s] = row_to_state[r]
        return state_map, accept_states
