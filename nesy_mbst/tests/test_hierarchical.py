import numpy as np
from nesy_mbst.learning.hierarchical import HierarchicalModel
from nesy_mbst.core.state_machine import MarkovChain


class TestHierarchicalModel:
    def test_build_and_query(self):
        mc = MarkovChain()
        mc.build(["A", "B", "C"])
        mc.P = np.array([[0.5, 0.3, 0.2], [0.4, 0.4, 0.2], [0.3, 0.3, 0.4]])
        hierarchical = HierarchicalModel(order=2)
        sequences = [
            ["A", "B", "C"],
            ["A", "B", "A"],
            ["A", "A", "B"],
            ["B", "C", "A"],
        ]
        hierarchical.build(sequences, mc)
        prob = hierarchical.get_probability(("A", "B"), "C")
        assert prob >= 0

    def test_fallback_to_first_order(self):
        mc = MarkovChain()
        mc.build(["A", "B"])
        mc.P = np.array([[0.5, 0.5], [0.5, 0.5]])
        hierarchical = HierarchicalModel(order=2)
        hierarchical.build([], mc)
        prob = hierarchical.get_probability(("X", "Y"), "A")
        assert prob == 0.0

    def test_sample_path(self):
        mc = MarkovChain()
        mc.build(["A", "B"], terminal_states={"B"})
        mc.P = np.array([[0.7, 0.3], [0.0, 1.0]])
        mc.start_state = "A"
        hierarchical = HierarchicalModel(order=2)
        hierarchical.build([["A", "A", "B"]], mc)
        path = hierarchical.sample_path(length=100, rng=np.random.default_rng(42))
        assert len(path) >= 1
