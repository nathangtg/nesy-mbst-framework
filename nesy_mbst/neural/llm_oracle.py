from __future__ import annotations
import logging
import re
from typing import Callable, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


class GrammarConstrainedOracle:
    VALID_OUTPUTS = {"yes", "no", "unsure"}

    def __init__(
        self,
        llm_backend: Optional[Callable[[str], str]] = None,
        requirements: str = "",
        escalate_unsure: Optional[Callable[[str], Optional[bool]]] = None,
    ):
        self.llm_backend = llm_backend
        self.requirements = requirements
        self.escalate_unsure = escalate_unsure
        self.membership_cache: Dict[str, Optional[bool]] = {}
        self.query_count = 0
        self.escalation_count = 0

    def query_membership(self, sequence: str) -> Optional[bool]:
        if sequence in self.membership_cache:
            return self.membership_cache[sequence]

        self.query_count += 1
        raw_response = self._query_llm(sequence)
        constrained = self._apply_grammar(raw_response)

        if constrained == "yes":
            result = True
        elif constrained == "no":
            result = False
        else:
            self.escalation_count += 1
            if self.escalate_unsure:
                result = self.escalate_unsure(sequence)
            else:
                result = None

        self.membership_cache[sequence] = result
        return result

    def _query_llm(self, sequence: str) -> str:
        if self.llm_backend:
            prompt = self._build_prompt(sequence)
            return self.llm_backend(prompt) or "unsure"
        return self._simulate_query(sequence)

    def _build_prompt(self, sequence: str) -> str:
        return (
            f"Given the following system requirements:\n{self.requirements}\n\n"
            f"Does the sequence '{sequence}' represent a valid execution path "
            f"in the system under test? Answer only with Yes, No, or Unsure."
        )

    def _apply_grammar(self, response: str) -> str:
        cleaned = response.strip().lower()
        tokens = re.findall(r'\b(yes|no|unsure)\b', cleaned)
        if tokens:
            return tokens[0]
        return "unsure"

    def _simulate_query(self, sequence: str) -> str:
        if not sequence:
            return "yes"
        if len(sequence) > 10:
            return "no"
        if "error" in sequence.lower() or "invalid" in sequence.lower():
            return "unsure"
        return "yes"

    def reset(self) -> None:
        self.membership_cache.clear()
        self.query_count = 0
        self.escalation_count = 0

    def set_llm_backend(self, backend: Callable[[str], str]) -> None:
        self.llm_backend = backend

    def set_requirements(self, requirements: str) -> None:
        self.requirements = requirements
