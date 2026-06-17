import numpy as np
from nesy_mbst.symbolic.constraint_solver import ConstraintSolver, SolverConfig
from nesy_mbst.symbolic.feasibility_checker import SymbolicFeasibilityMemory
from nesy_mbst.neural.constraint_extractor import ConstraintSystem


class TestConstraintSolver:
    def test_simple_two_state(self):
        solver = ConstraintSolver(SolverConfig(max_entropy=True))
        states = ["A", "B"]
        edges = {("A", "A"), ("A", "B"), ("B", "A"), ("B", "B")}
        mc = solver.solve(states, edges)
        assert mc.validate_row_stochastic() is True
        assert mc.num_states == 2

    def test_structural_zeros(self):
        solver = ConstraintSolver(SolverConfig(max_entropy=True))
        states = ["A", "B", "C"]
        edges = {("A", "B"), ("B", "C"), ("C", "A")}
        mc = solver.solve(states, edges)
        assert mc.P[0, 2] == 0.0
        assert mc.validate_row_stochastic() is True


class TestSymbolicFeasibilityMemory:
    def test_blocked_transition(self):
        mem = SymbolicFeasibilityMemory()
        mem.block_transition("A", "B")
        assert mem.is_feasible("A", "B") is False
        assert mem.is_feasible("A", "C") is True

    def test_precondition(self):
        mem = SymbolicFeasibilityMemory()
        mem.add_precondition("Checkout", "cart_not_empty")
        assert mem.is_feasible("Checkout", "Payment", {"cart_not_empty": True})
        assert mem.is_feasible("Checkout", "Payment", {"cart_not_empty": False}) is False
