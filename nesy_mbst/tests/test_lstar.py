from nesy_mbst.learning.lstar import LStarLearner
from nesy_mbst.core.state_machine import DFA


class TestLStar:
    def test_learn_simple_dfa(self):
        target = DFA(alphabet={"a", "b"}, start_state="q0")
        target.add_state("q0", is_accept=True)
        target.add_state("q1", is_accept=False)
        target.add_transition("q0", "a", "q0")
        target.add_transition("q0", "b", "q1")
        target.add_transition("q1", "a", "q1")
        target.add_transition("q1", "b", "q1")
        membership = lambda w: target.accepts(w)
        equivalence = lambda hyp: None
        learner = LStarLearner(
            alphabet={"a", "b"},
            membership_oracle=membership,
            equivalence_oracle=equivalence,
            max_iterations=10,
        )
        result = learner.learn()
        assert result is not None
