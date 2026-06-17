from __future__ import annotations
import numpy as np
from typing import Dict, List, Optional, Set, Tuple
from nesy_mbst.core.state_machine import DFA, MarkovChain


class Metrics:

    @staticmethod
    def f1_score(
        predicted_states: Set[str],
        true_states: Set[str],
        predicted_transitions: Set[Tuple[str, str]],
        true_transitions: Set[Tuple[str, str]],
    ) -> Dict[str, float]:
        state_precision = Metrics._precision(predicted_states, true_states)
        state_recall = Metrics._recall(predicted_states, true_states)
        state_f1 = Metrics._f1(state_precision, state_recall)
        trans_precision = Metrics._precision(
            predicted_transitions, true_transitions
        )
        trans_recall = Metrics._recall(
            predicted_transitions, true_transitions
        )
        trans_f1 = Metrics._f1(trans_precision, trans_recall)
        system_f1 = Metrics._system_f1(
            state_f1, trans_f1,
            state_precision, state_recall,
            trans_precision, trans_recall,
        )
        return {
            "state_precision": state_precision,
            "state_recall": state_recall,
            "state_f1": state_f1,
            "transition_precision": trans_precision,
            "transition_recall": trans_recall,
            "transition_f1": trans_f1,
            "system_f1": system_f1,
        }

    @staticmethod
    def _precision(
        predicted: Set, true: Set
    ) -> float:
        if not predicted:
            return 0.0
        tp = len(predicted & true)
        return tp / len(predicted)

    @staticmethod
    def _recall(
        predicted: Set, true: Set
    ) -> float:
        if not true:
            return 1.0
        tp = len(predicted & true)
        return tp / len(true)

    @staticmethod
    def _f1(precision: float, recall: float) -> float:
        if precision + recall == 0:
            return 0.0
        return 2 * precision * recall / (precision + recall)

    @staticmethod
    def _system_f1(
        sf1: float, tf1: float,
        sp: float, sr: float,
        tp: float, tr: float,
    ) -> float:
        state_contrib = sf1 * (sp + sr) / 2 if (sp + sr) > 0 else 0
        trans_contrib = tf1 * (tp + tr) / 2 if (tp + tr) > 0 else 0
        total_weight = (sp + sr + tp + tr) / 2
        if total_weight == 0:
            return 0.0
        return (state_contrib + trans_contrib) / total_weight

    @staticmethod
    def js_divergence(P: np.ndarray, Q: np.ndarray) -> float:
        P_flat = P.flatten()
        Q_flat = Q.flatten()
        P_safe = P_flat + 1e-12
        Q_safe = Q_flat + 1e-12
        P_safe = P_safe / P_safe.sum()
        Q_safe = Q_safe / Q_safe.sum()
        M = 0.5 * (P_safe + Q_safe)
        def kl(a, b):
            return np.sum(a * np.log(a / b))
        jsd = 0.5 * kl(P_safe, M) + 0.5 * kl(Q_safe, M)
        return float(jsd)

    @staticmethod
    def js_divergence_marginals(
        real_model: MarkovChain, synth_model: MarkovChain
    ) -> float:
        pi_real = real_model.steady_state()
        pi_synth = synth_model.steady_state()
        M = 0.5 * (pi_real + pi_synth) + 1e-12
        def kl(a, b):
            a_safe = a + 1e-12
            a_safe = a_safe / a_safe.sum()
            b_safe = b + 1e-12
            b_safe = b_safe / b_safe.sum()
            return np.sum(a_safe * np.log(a_safe / b_safe))
        jsd = 0.5 * kl(pi_real, M) + 0.5 * kl(pi_synth, M)
        return float(jsd)

    @staticmethod
    def normalized_frobenius(
        real_model: MarkovChain, synth_model: MarkovChain
    ) -> float:
        n = real_model.P.shape[0]
        diff = real_model.P - synth_model.P
        frob = np.linalg.norm(diff, "fro")
        return float(frob / n)

    @staticmethod
    def coverage_metrics(
        model: MarkovChain,
        covered_states: Set[str],
        covered_transitions: Set[Tuple[str, str]],
    ) -> Dict[str, float]:
        total_states = model.num_states
        total_transitions = model.num_transitions
        return {
            "state_coverage": (
                len(covered_states) / total_states if total_states > 0 else 1.0
            ),
            "transition_coverage": (
                len(covered_transitions) / total_transitions
                if total_transitions > 0
                else 1.0
            ),
        }
