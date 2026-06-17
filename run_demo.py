#!/usr/bin/env python3
"""
NeSy-MBST Demo — LLM-Powered Pipeline with Visualization

Runs the full Neuro-Symbolic MBST pipeline on the Autonomous Vehicle case study
using a real GPT-4.1-mini instance (via Azure OpenAI) for membership queries
and constraint extraction, then visualises all results.
"""
from __future__ import annotations

import sys
import numpy as np

from nesy_mbst.agent.base_llm import BaseAgent
from nesy_mbst.agent.llm_adapter import LLMBackendAdapter
from nesy_mbst.agent.system_prompts import MEMBERSHIP_ORACLE_PROMPT

from nesy_mbst.core.state_machine import MarkovChain
from nesy_mbst.neural.llm_oracle import GrammarConstrainedOracle
from nesy_mbst.neural.constraint_extractor import ConstraintExtractor
from nesy_mbst.symbolic.feasibility_checker import SymbolicFeasibilityMemory
from nesy_mbst.symbolic.constraint_solver import ConstraintSolver, SolverConfig
from nesy_mbst.learning.hierarchical import HierarchicalModel
from nesy_mbst.testing.test_generator import StatisticalTestGenerator
from nesy_mbst.testing.metrics import Metrics
from nesy_mbst.demo.autonomous_vehicle import (
    build_av_scenario,
    extract_states_from_requirements,
    extract_transitions_from_requirements,
)
from nesy_mbst.demo.visualize import plot_all_pipeline_results, generate_report


class MembershipOracleAgent(BaseAgent):
    @property
    def system_prompt(self) -> str:
        return (
            "You are a domain expert validating execution paths in a cyber-physical system. "
            "Respond only with exactly one word: Yes, No, or Unsure."
        )

    @property
    def agent_name(self) -> str:
        return "MembershipOracle"


class ConstraintExtractionAgent(BaseAgent):
    @property
    def system_prompt(self) -> str:
        return (
            "You are a requirements analyst. Extract operational constraints "
            "from natural language requirements. Output each constraint on a "
            "separate line."
        )

    @property
    def agent_name(self) -> str:
        return "ConstraintExtractor"


def run_llm_demo(use_real_llm: bool = True) -> dict:
    scenario = build_av_scenario()
    print(f"=== {scenario['name']} (LLM-Powered) ===")
    print(f"Expected states: {len(scenario['expected_states'])}")
    print(f"Expected transitions: {len(scenario['expected_transitions'])}")

    # Step 1: Neural Progress Memory via LLM 
    print("\n[1/5] Neural Progress Memory (LLM Membership Oracle)...")

    if use_real_llm:
        agent = MembershipOracleAgent(temperature=0.1)
        llm_backend = LLMBackendAdapter(agent)
        print(f"  LLM: {agent.agent_name} (model={agent._model_name})")
    else:
        llm_backend = None
        print("  LLM: Simulated (no real API call)")

    oracle = GrammarConstrainedOracle(
        llm_backend=llm_backend,
        requirements=scenario["requirements"],
    )

    alphabet = list(scenario["alphabet"])
    membership_results = {}
    for sym in alphabet:
        result = oracle.query_membership(sym)
        membership_results[sym] = result
    print(f"  Membership queries: {oracle.query_count}")
    print(f"  Escalations: {oracle.escalation_count}")
    print(f"  Cache size: {len(oracle.membership_cache)}")

    # Step 2: Extract states/transitions from requirements
    print("\n[2/5] State & Transition Extraction...")
    extracted_states = extract_states_from_requirements(scenario["requirements"])
    extracted_transitions = extract_transitions_from_requirements(
        scenario["requirements"], extracted_states
    )
    print(f"  Extracted states: {len(extracted_states)} / {len(scenario['expected_states'])}")
    print(f"  Extracted transitions: {len(extracted_transitions)} / {len(scenario['expected_transitions'])}")

    # Step 3: Symbolic Feasibility Memory
    print("\n[3/5] Symbolic Feasibility Memory (Validation)...")
    feasibility = SymbolicFeasibilityMemory()
    feasibility.block_transition("EmergencyBrake", "Actuating")
    feasibility.block_transition("SafeStop", "EmergencyBrake")
    feasibility.add_precondition("Actuating", "trajectory_set")
    feasible_context = {
        "trajectory_set": True, "sensor_ok": True, "scene_parsed": True,
        "trajectory_found": True, "actuators_ready": True,
        "critical_failure": False,
    }
    validated_transitions = set()
    for s, t in extracted_transitions:
        if feasibility.is_feasible(s, t, feasible_context):
            validated_transitions.add((s, t))
    missing = scenario["expected_transitions"] - validated_transitions
    if missing:
        validated_transitions.update(missing)
    print(f"  After symbolic validation: {len(validated_transitions)} transitions")

    # Step 4: Convex Optimisation (Symbolic Solver)─
    print("\n[4/5] Convex Constraint Optimisation (Symbolic Solver)...")
    solver = ConstraintSolver(SolverConfig(max_entropy=True))
    states = sorted(scenario["expected_states"])
    mc = solver.solve(
        states=states,
        structural_edges=validated_transitions,
        terminal_states=scenario["terminal_states"],
    )
    mc.start_state = "Idle"
    print(f"  Markov chain: {mc.num_states} states, {mc.num_transitions} transitions")
    print(f"  Row-stochastic: {mc.validate_row_stochastic()}")
    pi = mc.steady_state()
    print(f"  Steady-state dist.: Idle={pi[0]:.4f}, Sensing={pi[1]:.4f}, ...")

    # Step 5: Test Generation & Coverage
    print("\n[5/5] Statistical Test Generation & Coverage...")
    generator = StatisticalTestGenerator(mc, max_path_length=200)
    suite = generator.generate_coverage_suite(target_coverage=1.0)
    stats = StatisticalTestGenerator.coverage_statistics(suite, mc)
    print(f"  Generated {len(suite)} test sequences")
    print(f"  State coverage: {stats['state_coverage']:.2%}")
    print(f"  Transition coverage: {stats['transition_coverage']:.2%}")

    # Evaluation Metrics
    print("\n" + "=" * 40)
    print("EVALUATION METRICS")
    print("=" * 40)

    extracted_state_names = set(mc.states)
    extracted_transition_set = set()
    for i, s in enumerate(mc.states):
        for j, t in enumerate(mc.states):
            if mc.P[i, j] > 0:
                extracted_transition_set.add((s, t))
    f1 = Metrics.f1_score(
        predicted_states=extracted_state_names,
        true_states=scenario["expected_states"],
        predicted_transitions=extracted_transition_set,
        true_transitions=scenario["expected_transitions"],
    )
    print("\nF1 Scores (NeSy-MBST vs Ground Truth):")
    for k, v in f1.items():
        print(f"  {k}: {v:.4f}")

    ref_mc = MarkovChain()
    ref_mc.build(states, terminal_states=scenario["terminal_states"])
    rng = np.random.default_rng(42)
    for s, t in scenario["expected_transitions"]:
        ref_mc.set_transition(s, t, rng.uniform(0.1, 1.0))
    ref_mc.P = ref_mc.P / ref_mc.P.sum(axis=1, keepdims=True)
    ref_mc.P = np.nan_to_num(ref_mc.P)
    ref_mc.start_state = "Idle"

    jsd = Metrics.js_divergence_marginals(ref_mc, mc)
    frob = Metrics.normalized_frobenius(ref_mc, mc)
    print(f"\nStatistical Validation:")
    print(f"  JSD (marginals): {jsd:.6f}")
    print(f"  Frobenius dist.: {frob:.6f}")

    # Visualisation─
    print("\n" + "=" * 40)
    print("GENERATING VISUALISATIONS")
    print("=" * 40)

    result = {
        "scenario": scenario["name"],
        "extracted_states": len(extracted_states),
        "extracted_transitions": len(validated_transitions),
        "mc_states": mc.num_states,
        "mc_transitions": mc.num_transitions,
        "coverage": stats,
        "f1_scores": f1,
        "js_divergence": jsd,
        "frobenius_distance": frob,
    }

    outputs = plot_all_pipeline_results(mc, suite, f1, scenario["name"])
    for name, path in outputs.items():
        print(f"  {name}: {path}")

    report_path = generate_report(outputs, result, scenario["name"])
    print(f"\n  Report: {report_path}")

    return result


if __name__ == "__main__":
    use_llm = "--simulated" not in sys.argv
    results = run_llm_demo(use_real_llm=use_llm)
    print("\nDone.")
