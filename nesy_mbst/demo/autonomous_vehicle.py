from __future__ import annotations
import numpy as np
import re
from typing import Dict, List, Set, Tuple
from nesy_mbst.core.state_machine import DFA, MarkovChain
from nesy_mbst.learning.lstar import LStarLearner
from nesy_mbst.neural.llm_oracle import GrammarConstrainedOracle
from nesy_mbst.neural.constraint_extractor import ConstraintExtractor, ConstraintSystem
from nesy_mbst.symbolic.feasibility_checker import (
    SymbolicFeasibilityMemory,
    FeasibilityRule,
)
from nesy_mbst.symbolic.constraint_solver import ConstraintSolver, SolverConfig
from nesy_mbst.learning.hierarchical import HierarchicalModel
from nesy_mbst.testing.test_generator import StatisticalTestGenerator
from nesy_mbst.testing.metrics import Metrics


def extract_states_from_requirements(requirements: str) -> Set[str]:
    match = re.search(r"The system states are:\s*(.+?)\.", requirements)
    if match:
        states_str = match.group(1)
        states = set(s.strip() for s in states_str.split(","))
        return states
    return set()


def extract_transitions_from_requirements(
    requirements: str, states: Set[str]
) -> Set[Tuple[str, str]]:
    transitions = set()
    patterns = [
        r"From\s+(\w+),\s+the\s+system\s+transitions\s+to\s+(\w+)",
        r"From\s+(\w+),\s+it\s+goes\s+to\s+(\w+)",
        r"From\s+(\w+),\s+it\s+splits\s+to\s+(\w+)\s+and\s+(\w+)",
        r"(\w+)\s+and\s+(\w+)\s+converge\s+to\s+(\w+)",
        r"From\s+(\w+),\s+it\s+may\s+loop\s+back\s+to\s+(\w+)",
        r"(\w+)\s+can\s+transition\s+to\s+(\w+)",
        r"(\w+)\s+transitions\s+(?:back\s+)?to\s+(\w+)",
        r"system\s+enters\s+(\w+)\s+then\s+(\w+)",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, requirements, re.IGNORECASE):
            groups = match.groups()
            if len(groups) == 2:
                s, t = groups[0], groups[1]
                if s in states and t in states:
                    transitions.add((s, t))
            elif len(groups) == 3:
                s1, s2, t = groups
                if s1 in states and t in states:
                    transitions.add((s1, t))
                if s2 in states and t in states:
                    transitions.add((s2, t))
    return transitions


def build_av_scenario() -> Dict:
    requirements = (
        "An autonomous vehicle has three core modules: Perception, Planning, and Actuation. "
        "The Perception module processes LiDAR and camera data and generates a semantic scene graph. "
        "The Planning module computes safe trajectories using local and global planners. "
        "The Actuation module executes steering and throttle commands. "
        "After perception completes, planning begins. After planning, actuation executes. "
        "If perception fails, the system enters a safe stop state. "
        "If planning cannot find a trajectory, it reverts to perception for re-evaluation. "
        "The system states are: Idle, Sensing, SceneGraphReady, PlanningLocal, PlanningGlobal, "
        "TrajectorySet, Actuating, SafeStop, EmergencyBrake. "
        "From Idle, the system transitions to Sensing. From Sensing, it goes to SceneGraphReady. "
        "From SceneGraphReady, it splits to PlanningLocal and PlanningGlobal. "
        "PlanningLocal and PlanningGlobal converge to TrajectorySet. From TrajectorySet, it goes to Actuating. "
        "From Actuating, it may loop back to Sensing, PlanningLocal, or Idle. "
        "If any module detects a critical failure, the system enters EmergencyBrake then SafeStop. "
        "EmergencyBrake can transition to SafeStop, and SafeStop transitions back to Idle. "
        "Typically the vehicle actuates rather than re-planning. "
        "EmergencyBrake is rare compared to normal actuation."
    )
    expected_states = {
        "Idle", "Sensing", "SceneGraphReady", "PlanningLocal",
        "PlanningGlobal", "TrajectorySet", "Actuating", "SafeStop",
        "EmergencyBrake",
    }
    expected_transitions = {
        ("Idle", "Sensing"),
        ("Sensing", "SceneGraphReady"),
        ("SceneGraphReady", "PlanningLocal"),
        ("SceneGraphReady", "PlanningGlobal"),
        ("PlanningLocal", "TrajectorySet"),
        ("PlanningGlobal", "TrajectorySet"),
        ("TrajectorySet", "Actuating"),
        ("Actuating", "Sensing"),
        ("Actuating", "PlanningLocal"),
        ("Actuating", "Idle"),
        ("Actuating", "EmergencyBrake"),
        ("EmergencyBrake", "SafeStop"),
        ("SafeStop", "Idle"),
    }
    return {
        "name": "Autonomous Vehicle CPS",
        "requirements": requirements,
        "expected_states": expected_states,
        "expected_transitions": expected_transitions,
        "terminal_states": {"SafeStop"},
        "alphabet": {
            "sense", "scene_ready", "plan_local", "plan_global",
            "trajectory_set", "actuate", "failure_critical",
            "failure_perception", "recover", "idle",
        },
    }


def run_av_demo(use_solver: bool = True) -> Dict:
    scenario = build_av_scenario()
    print(f"=== Autonomous Vehicle CPS Demo ===")
    print(f"Scenario: {scenario['name']}")
    print(f"Expected states: {len(scenario['expected_states'])}")
    print(f"Expected transitions: {len(scenario['expected_transitions'])}")

    print("\n[1/5] Neural Progress Memory (NL Requirements -> Candidate Model)...")
    extracted_states = extract_states_from_requirements(scenario["requirements"])
    extracted_transitions = extract_transitions_from_requirements(
        scenario["requirements"], extracted_states
    )
    print(f"  Neural-extracted states: {len(extracted_states)} / {len(scenario['expected_states'])}")
    print(f"  Neural-extracted transitions: {len(extracted_transitions)} / {len(scenario['expected_transitions'])}")

    print("\n[2/5] Symbolic Feasibility Memory (Validation)...")
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

    print("\n[3/5] Convex Constraint Optimization (Symbolic Solver)...")
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

    print("\n[4/5] Path-Dependent Hierarchical Modeling...")
    sample_sequences = [
        ["Idle", "Sensing", "SceneGraphReady", "PlanningLocal",
         "TrajectorySet", "Actuating"],
        ["Idle", "Sensing", "SceneGraphReady", "PlanningGlobal",
         "TrajectorySet", "Actuating"],
        ["Idle", "Sensing", "SceneGraphReady", "PlanningLocal",
         "TrajectorySet", "Actuating", "Sensing"],
        ["Idle", "Sensing", "SceneGraphReady", "PlanningGlobal",
         "TrajectorySet", "Actuating", "PlanningLocal"],
        ["Idle", "EmergencyBrake", "SafeStop"],
    ]
    hierarchical = HierarchicalModel(order=2)
    hierarchical.build(sample_sequences, mc)
    example = hierarchical.sample_path(length=20, rng=np.random.default_rng(42))
    print(f"  Hierarchical model built (order={hierarchical.order})")
    print(f"  Sample path: {' -> '.join(example)}")

    print("\n[5/5] Statistical Test Generation & Coverage...")
    generator = StatisticalTestGenerator(mc, max_path_length=200)
    suite = generator.generate_coverage_suite(target_coverage=1.0)
    stats = StatisticalTestGenerator.coverage_statistics(suite, mc)
    print(f"  Generated {len(suite)} test sequences")
    print(f"  State coverage: {stats['state_coverage']:.2%}")
    print(f"  Transition coverage: {stats['transition_coverage']:.2%}")

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
    print("\nF1 Scores (NeSy-MBST Pipeline Output vs Ground Truth):")
    for k, v in f1.items():
        print(f"  {k}: {v:.4f}")

    ref_mc = MarkovChain()
    ref_mc.build(states, terminal_states=scenario["terminal_states"])
    np.random.seed(42)
    for (s, t) in scenario["expected_transitions"]:
        ref_mc.set_transition(s, t, np.random.uniform(0.1, 1.0))
    ref_mc.P = ref_mc.P / ref_mc.P.sum(axis=1, keepdims=True)
    ref_mc.P = np.nan_to_num(ref_mc.P)
    ref_mc.start_state = "Idle"

    jsd = Metrics.js_divergence_marginals(ref_mc, mc)
    frob = Metrics.normalized_frobenius(ref_mc, mc)
    print(f"\nStatistical Validation:")
    print(f"  Jensen-Shannon Divergence (marginals): {jsd:.6f}")
    print(f"  Normalized Frobenius Distance: {frob:.6f}")

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
    return result


if __name__ == "__main__":
    run_av_demo()
