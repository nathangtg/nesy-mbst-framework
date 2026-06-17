import numpy as np
from nesy_mbst.neural.llm_oracle import GrammarConstrainedOracle
from nesy_mbst.neural.constraint_extractor import ConstraintExtractor
from nesy_mbst.symbolic.feasibility_checker import SymbolicFeasibilityMemory
from nesy_mbst.symbolic.constraint_solver import ConstraintSolver, SolverConfig
from nesy_mbst.learning.hierarchical import HierarchicalModel
from nesy_mbst.testing.test_generator import StatisticalTestGenerator
from nesy_mbst.testing.metrics import Metrics
from nesy_mbst.core.state_machine import MarkovChain


class TestIntegration:
    def test_end_to_end_pipeline(self):
        states = ["A", "B", "C"]
        edges = {("A", "B"), ("A", "C"), ("B", "A"), ("C", "A")}
        terminal = {"C"}

        solver = ConstraintSolver(SolverConfig(max_entropy=True))
        mc = solver.solve(states, edges, terminal_states=terminal)
        mc.start_state = "A"
        assert mc.validate_row_stochastic()

        hierarchical = HierarchicalModel(order=2)
        hierarchical.build([["A", "B", "A", "C"]], mc)

        generator = StatisticalTestGenerator(mc, max_path_length=50)
        suite = generator.generate_coverage_suite(target_coverage=1.0)
        assert len(suite) > 0

        stats = StatisticalTestGenerator.coverage_statistics(suite, mc)
        assert stats["state_coverage"] > 0

        extractor = ConstraintExtractor()
        constraints = extractor.extract("A is twice as likely as B")
        assert len(constraints.equalities) > 0 or len(constraints.inequalities) > 0

    def test_f1_and_jsd(self):
        predicted_states = {"A", "B", "C"}
        true_states = {"A", "B", "C", "D"}
        predicted_transitions = {("A", "B"), ("B", "C")}
        true_transitions = {("A", "B"), ("B", "C"), ("C", "D")}
        f1 = Metrics.f1_score(
            predicted_states, true_states,
            predicted_transitions, true_transitions,
        )
        assert 0 < f1["system_f1"] < 1

        mc1 = MarkovChain()
        mc1.build(["A", "B"])
        mc1.P = np.array([[0.8, 0.2], [0.3, 0.7]])
        mc2 = MarkovChain()
        mc2.build(["A", "B"])
        mc2.P = np.array([[0.5, 0.5], [0.5, 0.5]])
        jsd = Metrics.js_divergence_marginals(mc1, mc2)
        assert jsd >= 0

    def test_constraint_solver_with_constraints(self):
        from nesy_mbst.neural.constraint_extractor import ConstraintSystem
        solver = ConstraintSolver(SolverConfig(max_entropy=True))
        states = ["Checkout", "Browse", "Payment"]
        edges = {
            ("Checkout", "Payment"), ("Checkout", "Browse"),
            ("Browse", "Checkout"), ("Browse", "Browse"),
            ("Payment", "Checkout"),
        }
        cs = ConstraintSystem()
        cs.add_inequality("Payment", "Browse", ">", 1.0)
        mc = solver.solve(states, edges, constraints=cs)
        assert mc.validate_row_stochastic()
