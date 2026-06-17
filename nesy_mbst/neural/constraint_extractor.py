from __future__ import annotations
import re
from typing import Callable, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field


@dataclass
class OperationalConstraint:
    constraint_type: str
    from_state: Optional[str]
    to_state: Optional[str]
    target_state: Optional[str]
    operator: str
    value: float
    source_text: str


@dataclass
class ConstraintSystem:
    equalities: List[Tuple[str, str, float]] = field(default_factory=list)
    inequalities: List[Tuple[str, str, str, float]] = field(default_factory=list)
    bounds: List[Tuple[str, float, float]] = field(default_factory=list)
    occupancy_upper: Dict[str, float] = field(default_factory=dict)
    occupancy_lower: Dict[str, float] = field(default_factory=dict)
    max_passage_time: Optional[float] = None

    def add_equality(self, var1: str, var2: str, coefficient: float = 1.0):
        self.equalities.append((var1, var2, coefficient))

    def add_inequality(self, var1: str, var2: str, operator: str, value: float):
        self.inequalities.append((var1, var2, operator, value))


class ConstraintExtractor:
    def __init__(
        self,
        llm_backend: Optional[Callable[[str], str]] = None,
    ):
        self.llm_backend = llm_backend

    def extract(self, requirements: str) -> ConstraintSystem:
        cs = ConstraintSystem()
        raw_constraints = self._query_llm(requirements) if self.llm_backend else ""
        if raw_constraints:
            parsed = self._parse_llm_output(raw_constraints)
        else:
            parsed = self._rule_based_extract(requirements)
        for c in parsed:
            self._add_constraint(cs, c)
        return cs

    def _query_llm(self, requirements: str) -> str:
        prompt = (
            f"Extract comparative relationships and operational constraints "
            f"from the following requirements. Output as structured constraints:\n"
            f"{requirements}\n"
            f"Format: TYPE from_state to_state operator value"
        )
        return self.llm_backend(prompt)

    def _rule_based_extract(self, requirements: str) -> List[OperationalConstraint]:
        constraints = []
        lower_req = requirements.lower()
        patterns = [
            (r"(\w+)\s+is\s+twice\s+as\s+likely\s+as\s+(\w+)", "proportional", 2.0),
            (r"(\w+)\s+is\s+more\s+common\s+than\s+(\w+)", "inequality", None),
            (r"typically\s+(\w+)\s+rather\s+than\s+(\w+)", "inequality", None),
            (r"usually\s+(\w+)\s+after\s+(\w+)", "frequent", None),
            (r"rarely\s+(\w+)", "rare", None),
        ]
        for pattern, ctype, val in patterns:
            for match in re.finditer(pattern, lower_req):
                groups = match.groups()
                if ctype == "proportional" and len(groups) >= 2:
                    constraints.append(OperationalConstraint(
                        constraint_type="proportional",
                        from_state=None,
                        to_state=groups[0],
                        target_state=groups[1],
                        operator="=",
                        value=val,
                        source_text=match.group(0),
                    ))
                elif ctype == "inequality" and len(groups) >= 2:
                    constraints.append(OperationalConstraint(
                        constraint_type="inequality",
                        from_state=None,
                        to_state=groups[0],
                        target_state=groups[1],
                        operator=">",
                        value=1.0,
                        source_text=match.group(0),
                    ))
        return constraints

    def _parse_llm_output(self, output: str) -> List[OperationalConstraint]:
        return []

    def _add_constraint(
        self, cs: ConstraintSystem, c: OperationalConstraint
    ) -> None:
        if c.constraint_type == "proportional":
            cs.add_equality(c.to_state, c.target_state, c.value)
        elif c.constraint_type == "inequality":
            cs.add_inequality(c.to_state, c.target_state, ">", 1.0)
