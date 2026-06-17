import numpy as np
from nesy_mbst.testing.metrics import Metrics
from nesy_mbst.core.state_machine import MarkovChain


class TestMetrics:
    def test_f1_perfect(self):
        states = {"A", "B"}
        trans = {("A", "B"), ("B", "A")}
        f1 = Metrics.f1_score(states, states, trans, trans)
        assert f1["state_f1"] == 1.0
        assert f1["transition_f1"] == 1.0

    def test_f1_no_match(self):
        f1 = Metrics.f1_score(set(), {"A"}, set(), {("A", "B")})
        assert f1["state_f1"] == 0.0
        assert f1["transition_f1"] == 0.0

    def test_js_divergence_identical(self):
        P = np.array([[0.5, 0.5], [0.3, 0.7]])
        jsd = Metrics.js_divergence(P, P)
        assert abs(jsd) < 1e-10

    def test_js_divergence_marginals(self):
        mc1 = MarkovChain()
        mc1.build(["A", "B"])
        mc1.P = np.array([[0.9, 0.1], [0.2, 0.8]])
        mc2 = MarkovChain()
        mc2.build(["A", "B"])
        mc2.P = np.array([[0.5, 0.5], [0.5, 0.5]])
        jsd = Metrics.js_divergence_marginals(mc1, mc2)
        assert jsd >= 0

    def test_normalized_frobenius_identical(self):
        mc1 = MarkovChain()
        mc1.build(["A", "B"])
        mc1.P = np.array([[0.5, 0.5], [0.5, 0.5]])
        mc2 = MarkovChain()
        mc2.build(["A", "B"])
        mc2.P = np.array([[0.5, 0.5], [0.5, 0.5]])
        d = Metrics.normalized_frobenius(mc1, mc2)
        assert abs(d) < 1e-10
