"""
Active Query Selection for Probabilistic Program Induction
===========================================================
Information-theoretic query selection strategies that maximize
the information gained per oracle query.

Key strategies:
- Maximum Entropy: query where model is most uncertain
- Expected Information Gain: query to maximize expected reduction in posterior entropy
- Uncertainty Sampling: query boundary regions between accept/reject

References:
- Angluin (1988). Queries and Concept Learning. Machine Learning.
- Settles (2009). Active Learning Literature Survey. CS Tech Report.
"""
from __future__ import annotations

import numpy as np
from typing import Callable, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum


class QueryStrategy(Enum):
    """Available query selection strategies."""
    RANDOM = "random"
    UNCERTAINTY = "uncertainty"
    EXPECTED_INFO_GAIN = "expected_info_gain"
    BOUNDARY = "boundary"
    HYBRID = "hybrid"


@dataclass
class QueryCandidate:
    """A candidate query with its expected utility."""
    word: str
    expected_info_gain: float
    uncertainty: float
    strategy_score: float


class InformationGainSelector:
    """
    Selects the most informative query to pose to the membership oracle.

    Instead of querying random or sequential words, selects queries that
    maximize the expected reduction in model uncertainty.

    Information gain for query x:
        IG(x) = H(A) - E_{y|x}[H(A | x, y)]

    where H(A) is the current entropy of the automaton posterior.
    """

    def __init__(
        self,
        alphabet: Set[str],
        strategy: QueryStrategy = QueryStrategy.HYBRID,
        max_candidates: int = 50,
        exploration_weight: float = 0.2,
    ):
        self.alphabet = list(sorted(alphabet))
        self.strategy = strategy
        self.max_candidates = max_candidates
        self.exploration_weight = exploration_weight

        # Track query history for diversity
        self._queried_words: Set[str] = set()
        self._query_results: Dict[str, Optional[bool]] = {}
        self._rng = np.random.default_rng(42)

    def select_query(
        self,
        current_beliefs: Dict[str, float],
        max_length: int = 10,
    ) -> str:
        """
        Select the most informative word to query.

        Args:
            current_beliefs: Dict mapping words to their current probability estimates
            max_length: Maximum word length to consider

        Returns:
            The word that should be queried next
        """
        candidates = self._generate_candidates(max_length)
        scored = self._score_candidates(candidates, current_beliefs)

        if not scored:
            # Fallback: random word
            return self._random_word(max_length)

        # Return highest scoring candidate
        scored.sort(key=lambda c: c.strategy_score, reverse=True)
        best = scored[0]
        self._queried_words.add(best.word)
        return best.word

    def record_result(self, word: str, result: Optional[bool]) -> None:
        """Record the result of a query for future reference."""
        self._query_results[word] = result

    def _generate_candidates(self, max_length: int) -> List[str]:
        """Generate candidate words for querying."""
        candidates = []

        # Strategy 1: Extensions of known prefixes
        for word in list(self._query_results.keys())[:20]:
            for a in self.alphabet:
                ext = word + a
                if ext not in self._queried_words and len(ext) <= max_length:
                    candidates.append(ext)

        # Strategy 2: Boundary exploration (words similar to both + and - examples)
        positive = [w for w, r in self._query_results.items() if r is True]
        negative = [w for w, r in self._query_results.items() if r is False]

        if positive and negative:
            # Generate words between positive and negative examples
            for p in positive[:5]:
                for length in range(1, min(len(p) + 2, max_length + 1)):
                    # Modify one character
                    if length <= len(p):
                        for pos in range(length):
                            for a in self.alphabet:
                                modified = p[:pos] + a + p[pos+1:length]
                                if modified not in self._queried_words:
                                    candidates.append(modified)

        # Strategy 3: Random diverse candidates
        for _ in range(self.max_candidates - len(candidates)):
            word = self._random_word(max_length)
            if word not in self._queried_words:
                candidates.append(word)

        # Deduplicate and limit
        seen = set()
        unique = []
        for c in candidates:
            if c not in seen and c not in self._queried_words:
                seen.add(c)
                unique.append(c)
                if len(unique) >= self.max_candidates:
                    break

        return unique

    def _score_candidates(
        self,
        candidates: List[str],
        beliefs: Dict[str, float],
    ) -> List[QueryCandidate]:
        """Score candidates according to the query strategy."""
        scored = []

        for word in candidates:
            # Current belief about this word
            belief = beliefs.get(word, 0.5)
            uncertainty = self._binary_entropy(belief)

            if self.strategy == QueryStrategy.UNCERTAINTY:
                score = uncertainty
            elif self.strategy == QueryStrategy.EXPECTED_INFO_GAIN:
                score = self._expected_info_gain(word, belief, beliefs)
            elif self.strategy == QueryStrategy.BOUNDARY:
                score = 1.0 - abs(belief - 0.5) * 2  # Higher near decision boundary
            elif self.strategy == QueryStrategy.HYBRID:
                eig = self._expected_info_gain(word, belief, beliefs)
                boundary = 1.0 - abs(belief - 0.5) * 2
                diversity = self._diversity_bonus(word)
                score = 0.4 * eig + 0.3 * boundary + 0.2 * uncertainty + 0.1 * diversity
            else:  # RANDOM
                score = self._rng.random()

            scored.append(QueryCandidate(
                word=word,
                expected_info_gain=self._expected_info_gain(word, belief, beliefs),
                uncertainty=uncertainty,
                strategy_score=score,
            ))

        return scored

    def _expected_info_gain(
        self,
        word: str,
        belief: float,
        beliefs: Dict[str, float],
    ) -> float:
        """
        Estimate expected information gain from querying a word.

        IG(x) = H(beliefs) - P(y=1|x)*H(beliefs|x,y=1) - P(y=0|x)*H(beliefs|x,y=0)

        Approximated by the uncertainty of related words.
        """
        # Current entropy of belief about this word
        current_entropy = self._binary_entropy(belief)

        # Expected entropy after observing (will be 0 for binary oracle)
        # But for noisy oracle, there's residual uncertainty
        residual_entropy = 0.05  # Small residual due to oracle noise

        # Additional info: how much does knowing this word tell us about others?
        propagation_gain = 0.0
        for prefix_len in range(1, len(word)):
            prefix = word[:prefix_len]
            if prefix in beliefs:
                # Knowing word's label constrains prefix's interpretation
                propagation_gain += 0.1 * self._binary_entropy(beliefs[prefix])

        return current_entropy - residual_entropy + propagation_gain

    def _diversity_bonus(self, word: str) -> float:
        """Bonus for querying words dissimilar to previous queries."""
        if not self._queried_words:
            return 1.0

        min_dist = float("inf")
        for queried in list(self._queried_words)[-20:]:
            dist = self._edit_distance(word, queried)
            min_dist = min(min_dist, dist)

        # Normalize: higher diversity = higher bonus
        return min(min_dist / max(len(word), 1), 1.0)

    def _edit_distance(self, a: str, b: str) -> int:
        """Simple edit distance for diversity computation."""
        if len(a) == 0:
            return len(b)
        if len(b) == 0:
            return len(a)
        # Simplified: length difference + character mismatches
        min_len = min(len(a), len(b))
        mismatches = sum(1 for i in range(min_len) if a[i] != b[i])
        return mismatches + abs(len(a) - len(b))

    def _binary_entropy(self, p: float) -> float:
        """Binary entropy H(p)."""
        p = np.clip(p, 1e-10, 1 - 1e-10)
        return float(-p * np.log2(p) - (1 - p) * np.log2(1 - p))

    def _random_word(self, max_length: int) -> str:
        """Generate a random word."""
        length = self._rng.integers(1, max_length + 1)
        return "".join(self._rng.choice(self.alphabet, size=length))

    @property
    def statistics(self) -> Dict[str, float]:
        """Return selection statistics."""
        if not self._query_results:
            return {"total_queries": 0, "avg_info_gain": 0.0}

        beliefs = {w: (1.0 if r else 0.0) if r is not None else 0.5
                   for w, r in self._query_results.items()}
        avg_entropy = np.mean([self._binary_entropy(b) for b in beliefs.values()])

        return {
            "total_queries": len(self._queried_words),
            "positive_rate": sum(1 for r in self._query_results.values() if r is True) / max(len(self._query_results), 1),
            "avg_remaining_uncertainty": avg_entropy,
        }
