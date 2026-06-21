"""
Calibrated Oracle with Uncertainty Quantification
===================================================
Enhances the GrammarConstrainedOracle with:
1. Temperature-scaled calibration for reliable confidence estimates
2. Ensemble-based uncertainty quantification
3. Active escalation based on epistemic vs aleatoric uncertainty
4. Response caching with Bayesian evidence accumulation

References:
- Guo et al. (2017). On Calibration of Modern Neural Networks. ICML.
- Lakshminarayanan et al. (2017). Simple and Scalable Predictive Uncertainty Estimation.
"""
from __future__ import annotations

import logging
import re
import numpy as np
from typing import Callable, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class UncertaintyEstimate:
    """Decomposed uncertainty estimate for a membership query."""
    prediction: Optional[bool]  # True/False/None
    confidence: float  # Calibrated confidence [0, 1]
    epistemic_uncertainty: float  # Model uncertainty (reducible)
    aleatoric_uncertainty: float  # Data uncertainty (irreducible)
    total_uncertainty: float  # Combined uncertainty
    num_queries: int  # How many times this was queried
    evidence_for: float  # Bayesian evidence for True
    evidence_against: float  # Bayesian evidence for False


class OracleCalibrator:
    """
    Post-hoc calibration for oracle predictions using temperature scaling.

    Fits a temperature parameter T such that:
        P_calibrated(y|x) = softmax(logits / T)

    This ensures that when the oracle says "80% confident", it's actually
    correct 80% of the time (reliability diagram alignment).
    """

    def __init__(self, initial_temperature: float = 1.5):
        self.temperature = initial_temperature
        self._calibration_data: List[Tuple[float, bool]] = []
        self._ece: float = 0.0  # Expected Calibration Error

    def calibrate_confidence(self, raw_confidence: float) -> float:
        """Apply temperature scaling to raw confidence."""
        if self.temperature == 1.0:
            return raw_confidence

        # Temperature-scaled sigmoid
        logit = np.log(max(raw_confidence, 1e-10) / max(1 - raw_confidence, 1e-10))
        scaled_logit = logit / self.temperature
        calibrated = 1.0 / (1.0 + np.exp(-scaled_logit))
        return float(calibrated)

    def update(self, predicted_confidence: float, true_label: bool) -> None:
        """Update calibrator with a new data point."""
        self._calibration_data.append((predicted_confidence, true_label))

        # Periodically re-fit temperature
        if len(self._calibration_data) % 20 == 0:
            self._fit_temperature()

    def _fit_temperature(self) -> None:
        """Fit temperature to minimize Expected Calibration Error."""
        if len(self._calibration_data) < 10:
            return

        # Grid search for optimal temperature
        best_ece = float("inf")
        best_temp = self.temperature

        for temp_candidate in np.linspace(0.5, 5.0, 20):
            ece = self._compute_ece(temp_candidate)
            if ece < best_ece:
                best_ece = ece
                best_temp = temp_candidate

        self.temperature = best_temp
        self._ece = best_ece

    def _compute_ece(self, temperature: float) -> float:
        """Compute Expected Calibration Error for a given temperature."""
        n_bins = 10
        bin_boundaries = np.linspace(0, 1, n_bins + 1)
        bin_accuracies = np.zeros(n_bins)
        bin_confidences = np.zeros(n_bins)
        bin_counts = np.zeros(n_bins)

        for raw_conf, true_label in self._calibration_data:
            # Apply temperature
            logit = np.log(max(raw_conf, 1e-10) / max(1 - raw_conf, 1e-10))
            cal_conf = 1.0 / (1.0 + np.exp(-logit / temperature))

            bin_idx = min(int(cal_conf * n_bins), n_bins - 1)
            bin_accuracies[bin_idx] += float(true_label)
            bin_confidences[bin_idx] += cal_conf
            bin_counts[bin_idx] += 1

        # ECE = sum |accuracy - confidence| weighted by bin size
        ece = 0.0
        total = sum(bin_counts)
        for i in range(n_bins):
            if bin_counts[i] > 0:
                avg_acc = bin_accuracies[i] / bin_counts[i]
                avg_conf = bin_confidences[i] / bin_counts[i]
                ece += (bin_counts[i] / total) * abs(avg_acc - avg_conf)

        return ece

    @property
    def expected_calibration_error(self) -> float:
        return self._ece


class CalibratedOracle:
    """
    Enhanced membership oracle with calibrated uncertainty quantification.

    Key improvements over GrammarConstrainedOracle:
    1. Bayesian evidence accumulation (multiple queries per word)
    2. Epistemic/aleatoric uncertainty decomposition
    3. Temperature-calibrated confidence estimates
    4. Intelligent escalation based on uncertainty type
    5. Ensemble querying for robust predictions

    This enables the learning algorithm to make better decisions about
    which queries to prioritize and when to trust the oracle's answers.
    """

    VALID_OUTPUTS = {"yes", "no", "unsure"}

    def __init__(
        self,
        llm_backend: Optional[Callable[[str], str]] = None,
        requirements: str = "",
        escalate_unsure: Optional[Callable[[str], Optional[bool]]] = None,
        num_ensemble_queries: int = 1,
        confidence_threshold: float = 0.7,
        max_retries: int = 3,
    ):
        self.llm_backend = llm_backend
        self.requirements = requirements
        self.escalate_unsure = escalate_unsure
        self.num_ensemble_queries = num_ensemble_queries
        self.confidence_threshold = confidence_threshold
        self.max_retries = max_retries

        # State
        self.calibrator = OracleCalibrator()
        self._evidence_store: Dict[str, UncertaintyEstimate] = {}
        self.query_count = 0
        self.escalation_count = 0
        self._cached_results: Dict[str, Optional[bool]] = {}

    def query_membership(self, sequence: str) -> Optional[bool]:
        """
        Query membership with calibrated confidence.

        Returns True/False/None based on accumulated evidence.
        """
        estimate = self.query_with_uncertainty(sequence)
        return estimate.prediction

    def query_with_uncertainty(self, sequence: str) -> UncertaintyEstimate:
        """
        Full uncertainty-aware membership query.

        Returns detailed uncertainty decomposition alongside prediction.
        """
        # Check if we already have high-confidence evidence
        if sequence in self._evidence_store:
            existing = self._evidence_store[sequence]
            if existing.confidence >= self.confidence_threshold:
                return existing

        # Perform ensemble queries
        votes_yes = 0
        votes_no = 0
        votes_unsure = 0

        n_queries = max(self.num_ensemble_queries, 1)
        for _ in range(n_queries):
            raw_response = self._query_llm(sequence)
            constrained = self._apply_grammar(raw_response)
            self.query_count += 1

            if constrained == "yes":
                votes_yes += 1
            elif constrained == "no":
                votes_no += 1
            else:
                votes_unsure += 1

        # Bayesian evidence accumulation
        estimate = self._compute_estimate(
            sequence, votes_yes, votes_no, votes_unsure
        )

        # Store evidence
        if sequence in self._evidence_store:
            # Merge with existing evidence
            existing = self._evidence_store[sequence]
            estimate = self._merge_evidence(existing, estimate)

        self._evidence_store[sequence] = estimate

        # Escalation decision based on uncertainty type
        if estimate.prediction is None and estimate.epistemic_uncertainty > 0.3:
            self.escalation_count += 1
            if self.escalate_unsure:
                escalated_result = self.escalate_unsure(sequence)
                if escalated_result is not None:
                    # Update evidence with ground truth
                    estimate.prediction = escalated_result
                    estimate.confidence = 0.95
                    self.calibrator.update(0.5, escalated_result)

        # Cache final result
        self._cached_results[sequence] = estimate.prediction
        return estimate

    def _compute_estimate(
        self,
        sequence: str,
        votes_yes: int,
        votes_no: int,
        votes_unsure: int,
    ) -> UncertaintyEstimate:
        """Compute uncertainty estimate from vote distribution."""
        total = votes_yes + votes_no + votes_unsure

        if total == 0:
            return UncertaintyEstimate(
                prediction=None, confidence=0.0,
                epistemic_uncertainty=1.0, aleatoric_uncertainty=0.5,
                total_uncertainty=1.0, num_queries=0,
                evidence_for=0.5, evidence_against=0.5,
            )

        # Beta posterior for acceptance probability
        alpha = votes_yes + 1  # Prior: Beta(1,1) = uniform
        beta = votes_no + 1
        evidence_for = alpha / (alpha + beta)
        evidence_against = beta / (alpha + beta)

        # Raw confidence
        raw_confidence = max(evidence_for, evidence_against)

        # Calibrate
        calibrated_confidence = self.calibrator.calibrate_confidence(raw_confidence)

        # Uncertainty decomposition
        # Epistemic: uncertainty due to limited data (reducible by more queries)
        epistemic = 1.0 / (alpha + beta)  # Decreases with more evidence
        # Aleatoric: uncertainty due to ambiguous input (irreducible)
        aleatoric = votes_unsure / max(total, 1)  # Proportion of "unsure" responses

        total_uncertainty = epistemic + aleatoric

        # Make prediction
        if calibrated_confidence >= self.confidence_threshold:
            prediction = evidence_for > 0.5
        elif total_uncertainty > 0.5:
            prediction = None  # Too uncertain
        else:
            prediction = evidence_for > 0.5

        return UncertaintyEstimate(
            prediction=prediction,
            confidence=calibrated_confidence,
            epistemic_uncertainty=epistemic,
            aleatoric_uncertainty=aleatoric,
            total_uncertainty=total_uncertainty,
            num_queries=total,
            evidence_for=evidence_for,
            evidence_against=evidence_against,
        )

    def _merge_evidence(
        self,
        existing: UncertaintyEstimate,
        new: UncertaintyEstimate,
    ) -> UncertaintyEstimate:
        """Merge existing and new evidence via Bayesian update."""
        # Combine evidence counts
        total_for = (existing.evidence_for * existing.num_queries +
                     new.evidence_for * new.num_queries)
        total_against = (existing.evidence_against * existing.num_queries +
                         new.evidence_against * new.num_queries)
        total_queries = existing.num_queries + new.num_queries

        evidence_for = total_for / max(total_queries, 1)
        evidence_against = total_against / max(total_queries, 1)

        raw_confidence = max(evidence_for, evidence_against)
        calibrated = self.calibrator.calibrate_confidence(raw_confidence)

        # Epistemic decreases with more queries
        epistemic = 1.0 / (total_queries + 2)
        aleatoric = (existing.aleatoric_uncertainty + new.aleatoric_uncertainty) / 2

        prediction = None
        if calibrated >= self.confidence_threshold:
            prediction = evidence_for > 0.5

        return UncertaintyEstimate(
            prediction=prediction,
            confidence=calibrated,
            epistemic_uncertainty=epistemic,
            aleatoric_uncertainty=aleatoric,
            total_uncertainty=epistemic + aleatoric,
            num_queries=total_queries,
            evidence_for=evidence_for,
            evidence_against=evidence_against,
        )

    def _query_llm(self, sequence: str) -> str:
        """Query the LLM backend."""
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
        """Constrain response to valid grammar."""
        cleaned = response.strip().lower()
        tokens = re.findall(r'\b(yes|no|unsure)\b', cleaned)
        if tokens:
            return tokens[0]
        return "unsure"

    def _simulate_query(self, sequence: str) -> str:
        """Built-in simulation for testing."""
        if not sequence:
            return "yes"
        if len(sequence) > 10:
            return "no"
        if "error" in sequence.lower() or "invalid" in sequence.lower():
            return "unsure"
        return "yes"

    def get_uncertainty_stats(self) -> Dict[str, float]:
        """Return aggregate uncertainty statistics."""
        if not self._evidence_store:
            return {}

        estimates = list(self._evidence_store.values())
        return {
            "mean_confidence": np.mean([e.confidence for e in estimates]),
            "mean_epistemic": np.mean([e.epistemic_uncertainty for e in estimates]),
            "mean_aleatoric": np.mean([e.aleatoric_uncertainty for e in estimates]),
            "fraction_uncertain": sum(1 for e in estimates if e.prediction is None) / len(estimates),
            "total_queries": self.query_count,
            "escalation_rate": self.escalation_count / max(self.query_count, 1),
            "calibration_ece": self.calibrator.expected_calibration_error,
        }

    def reset(self) -> None:
        self._evidence_store.clear()
        self._cached_results.clear()
        self.query_count = 0
        self.escalation_count = 0
