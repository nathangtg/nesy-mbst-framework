from nesy_mbst.neural.llm_oracle import GrammarConstrainedOracle


class TestGrammarConstrainedOracle:
    def test_grammar_constraint(self):
        oracle = GrammarConstrainedOracle()
        raw = "  YeS "
        assert oracle._apply_grammar(raw) == "yes"

    def test_grammar_unsure(self):
        oracle = GrammarConstrainedOracle()
        raw = "I am uncertain about this sequence"
        assert oracle._apply_grammar(raw) == "unsure"

    def test_no_llm_simulates(self):
        oracle = GrammarConstrainedOracle(
            escalate_unsure=lambda seq: False,
        )
        result = oracle.query_membership("a")
        assert result is not None

    def test_escalation(self):
        calls = []
        oracle = GrammarConstrainedOracle(
            escalate_unsure=lambda seq: (
                calls.append(seq) or True
            ) if calls is not None else True,
        )
        oracle._query_llm = lambda s: "unsure"
        result = oracle.query_membership("test_seq")
        assert result is not None
