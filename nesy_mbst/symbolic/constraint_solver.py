from __future__ import annotations
import numpy as np
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from scipy.optimize import minimize, LinearConstraint, Bounds
from nesy_mbst.core.state_machine import MarkovChain
from nesy_mbst.neural.constraint_extractor import ConstraintSystem


@dataclass
class SolverConfig:
    max_entropy: bool = True
    regularization: float = 1e-6
    max_iterations: int = 1000
    tol: float = 1e-12


class ConstraintSolver:
    def __init__(self, config: Optional[SolverConfig] = None):
        self.config = config or SolverConfig()

    def solve(
        self,
        states: List[str],
        structural_edges: Set[Tuple[str, str]],
        constraints: Optional[ConstraintSystem] = None,
        terminal_states: Optional[Set[str]] = None,
    ) -> MarkovChain:
        n = len(states)
        P0 = self._initialize_matrix(states, structural_edges)
        bounds = self._build_bounds(n, structural_edges, states)
        linear_constraints = self._build_linear_constraints(
            n, constraints, states
        )
        x0 = P0.flatten()
        result = minimize(
            self._objective,
            x0,
            method="SLSQP",
            bounds=bounds,
            constraints=linear_constraints,
            options={
                "maxiter": self.config.max_iterations,
                "ftol": self.config.tol,
            },
        )
        P_opt = result.x.reshape(n, n)
        P_opt = self._normalize_rows(P_opt)
        mc = MarkovChain()
        mc.build(states, terminal_states=terminal_states)
        mc.P = P_opt
        mc.start_state = states[0]
        return mc

    def _objective(self, x: np.ndarray) -> float:
        P = x.reshape(-1, int(np.sqrt(len(x))))
        if self.config.max_entropy:
            P_safe = np.clip(P, self.config.regularization, 1.0)
            entropy = -np.sum(P_safe * np.log(P_safe))
            return -entropy
        return np.sum(P ** 2)

    def _initialize_matrix(
        self, states: List[str], structural_edges: Set[Tuple[str, str]]
    ) -> np.ndarray:
        n = len(states)
        P = np.zeros((n, n))
        state_idx = {s: i for i, s in enumerate(states)}
        for (s, t) in structural_edges:
            i = state_idx.get(s)
            j = state_idx.get(t)
            if i is not None and j is not None:
                P[i, j] = 1.0
        return self._normalize_rows(P)

    def _normalize_rows(self, P: np.ndarray) -> np.ndarray:
        row_sums = P.sum(axis=1, keepdims=True)
        row_sums[row_sums == 0] = 1.0
        return P / row_sums

    def _build_bounds(
        self,
        n: int,
        structural_edges: Set[Tuple[str, str]],
        states: List[str],
    ) -> Bounds:
        lb = np.zeros(n * n)
        ub = np.ones(n * n)
        state_idx = {s: i for i, s in enumerate(states)}
        for i in range(n):
            for j in range(n):
                idx = i * n + j
                s_i = states[i]
                s_j = states[j]
                if (s_i, s_j) not in structural_edges:
                    ub[idx] = 0.0
        return Bounds(lb, ub)

    def _build_linear_constraints(
        self, n: int, constraints: Optional[ConstraintSystem], states: List[str]
    ) -> List[LinearConstraint]:
        cons = []
        A_row_stoch = np.zeros((n, n * n))
        for i in range(n):
            start = i * n
            end = (i + 1) * n
            A_row_stoch[i, start:end] = 1.0
        cons.append(LinearConstraint(A_row_stoch, np.ones(n), np.ones(n)))
        if constraints:
            for eq in constraints.equalities:
                var1, var2, coeff = eq
                A_eq = np.zeros((1, n * n))
                if var1 in states and var2 in states:
                    i, j = states.index(var1), states.index(var2)
                    A_eq[0, i * n + j] = 1.0
                    A_eq[0, i * n + j] = -coeff
                    cons.append(LinearConstraint(A_eq, 0, 0))
            for ineq in constraints.inequalities:
                var1, var2, op, val = ineq
                A_ineq = np.zeros((1, n * n))
                if var1 in states and var2 in states:
                    i, j = states.index(var1), states.index(var2)
                    A_ineq[0, i * n + j] = 1.0 if op == ">" else -1.0
                    A_ineq[0, i * n + j] = -1.0 if op == ">" else 1.0
                    lb = val if op == ">" else -np.inf
                    ub = np.inf if op == ">" else val
                    cons.append(LinearConstraint(A_ineq, lb, ub))
        return cons
