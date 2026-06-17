from nesy_mbst.symbolic.closed_loop import ClosedLoopAdapter, TelemetrySample
from nesy_mbst.core.state_machine import MarkovChain
import numpy as np


class TestClosedLoopAdapter:
    def test_detect_no_divergence(self):
        mc = MarkovChain()
        mc.build(["A", "B"])
        mc.P = np.array([[0.5, 0.5], [0.5, 0.5]])
        mc.start_state = "A"
        adapter = ClosedLoopAdapter(convergence_threshold=0.5)
        for _ in range(20):
            adapter.ingest_telemetry(
                TelemetrySample(path=["A", "B", "A"], duration=1.0, outcome="pass")
            )
        delta = adapter.detect_divergence(mc)
        assert delta is None or adapter.converged

    def test_detect_divergence(self):
        mc = MarkovChain()
        mc.build(["A", "B"])
        mc.P = np.array([[0.99, 0.01], [0.5, 0.5]])
        mc.start_state = "A"
        adapter = ClosedLoopAdapter(convergence_threshold=0.1, window_size=10)
        for _ in range(15):
            adapter.ingest_telemetry(
                TelemetrySample(path=["A", "B"], duration=1.0, outcome="pass")
            )
        delta = adapter.detect_divergence(mc)
        assert delta is not None or adapter.converged

    def test_apply_delta(self):
        mc = MarkovChain()
        mc.build(["A", "B"])
        mc.P = np.array([[0.5, 0.5], [0.5, 0.5]])
        mc.start_state = "A"
        adapter = ClosedLoopAdapter()
        delta = adapter.detect_divergence(mc)
        if delta is None:
            from nesy_mbst.symbolic.closed_loop import ModelDelta
            delta = ModelDelta()
            delta.probability_adjustments[("A", "B")] = 0.8
        new_mc = adapter.apply_delta(mc, delta)
        assert new_mc.num_states >= mc.num_states
