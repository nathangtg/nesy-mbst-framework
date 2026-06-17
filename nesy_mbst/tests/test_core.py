import numpy as np
from nesy_mbst.core.state_machine import DFA, MarkovChain
from nesy_mbst.core.observation_table import ObservationTable


class TestDFA:
    def test_basic_dfa(self):
        dfa = DFA(start_state="q0")
        dfa.add_state("q0", is_accept=False)
        dfa.add_state("q1", is_accept=True)
        dfa.add_transition("q0", "a", "q1")
        dfa.add_transition("q1", "b", "q0")
        assert dfa.accepts("a") is True
        assert dfa.accepts("") is False
        assert dfa.num_states == 2
        assert dfa.num_transitions == 2

    def test_dfa_rejection(self):
        dfa = DFA(start_state="q0")
        dfa.add_state("q0", is_accept=True)
        dfa.add_transition("q0", "a", "q0")
        assert dfa.accepts("a") is True
        assert dfa.accepts("b") is False


class TestMarkovChain:
    def test_build_and_validate(self):
        mc = MarkovChain()
        mc.build(["A", "B", "C"])
        mc.set_transition("A", "B", 0.7)
        mc.set_transition("A", "C", 0.3)
        mc.set_transition("B", "A", 1.0)
        mc.set_transition("C", "A", 1.0)
        mc.start_state = "A"
        assert mc.validate_row_stochastic() is True
        assert abs(mc.get_transition("A", "B") - 0.7) < 1e-10

    def test_steady_state(self):
        mc = MarkovChain()
        mc.build(["A", "B"])
        mc.P = np.array([[0.5, 0.5], [0.5, 0.5]])
        pi = mc.steady_state()
        assert len(pi) == 2
        assert abs(pi.sum() - 1.0) < 1e-10

    def test_sample_path(self):
        mc = MarkovChain()
        mc.build(["A", "B"], terminal_states={"B"})
        mc.P = np.array([[0.9, 0.1], [0.0, 1.0]])
        mc.start_state = "A"
        path = mc.sample_path(length=1000, rng=np.random.default_rng(42))
        assert path[0] == "A"
        assert len(path) >= 2


class TestObservationTable:
    def test_basic_table(self):
        table = ObservationTable(alphabet={"a", "b"})
        table.add_prefix("")
        table.add_suffix("")
        table.set_cell("", "", True)
        assert table.row("") == (True,)
        assert table.get_cell("", "") is True
