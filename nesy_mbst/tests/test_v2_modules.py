"""
Tests for NeSy-MBST v2 enhanced modules.
Validates: DLI, PPI, AGCS, CTG, CL-CDD, CalibratedOracle.
"""
import pytest
import numpy as np

from nesy_mbst.core.state_machine import DFA, MarkovChain
from nesy_mbst.symbolic_v2.differentiable_logic import (
    DifferentiableLogicGate,
    DLIFeasibilityChecker,
    TemperatureScheduler,
    TNormType,
)
from nesy_mbst.symbolic_v2.continual_adapter import (
    CUSUMDetector,
    ElasticWeightConsolidation,
    ContinualClosedLoopAdapter,
    DriftType,
)
from nesy_mbst.symbolic.closed_loop import TelemetrySample
from nesy_mbst.learning_v2.probabilistic_induction import (
    PDFA,
    ProbabilisticObservationTable,
    ProbabilisticInductionLearner,
)
from nesy_mbst.learning_v2.active_query import InformationGainSelector, QueryStrategy
from nesy_mbst.neural_v2.attention_constraint_extractor import AttentionConstraintExtractor
from nesy_mbst.neural_v2.calibrated_oracle import CalibratedOracle, OracleCalibrator
from nesy_mbst.testing_v2.counterfactual_generator import (
    CausalGraph,
    CounterfactualTestGenerator,
    ShapleyAnalyzer,
)


# ═══════════════════════════════════════════════════════════════════════════
# DLI Tests
# ═══════════════════════════════════════════════════════════════════════════

class TestDifferentiableLogicGate:

    def test_sigmoid_range(self):
        gate = DifferentiableLogicGate(temperature=1.0)
        for x in np.linspace(-10, 10, 100):
            s = gate.sigmoid(x)
            assert 0.0 <= s <= 1.0

    def test_sigmoid_midpoint(self):
        gate = DifferentiableLogicGate(temperature=1.0)
        assert abs(gate.sigmoid(0) - 0.5) < 1e-6

    def test_conjunction_product(self):
        gate = DifferentiableLogicGate(t_norm=TNormType.PRODUCT)
        assert abs(gate.conjunction(1.0, 1.0) - 1.0) < 1e-6
        assert abs(gate.conjunction(1.0, 0.0) - 0.0) < 1e-6
        assert abs(gate.conjunction(0.5, 0.5) - 0.25) < 1e-6

    def test_conjunction_lukasiewicz(self):
        gate = DifferentiableLogicGate(t_norm=TNormType.LUKASIEWICZ)
        assert gate.conjunction(1.0, 1.0) == 1.0
        assert gate.conjunction(0.3, 0.5) == 0.0  # 0.3 + 0.5 - 1 < 0
        assert abs(gate.conjunction(0.8, 0.7) - 0.5) < 1e-6

    def test_negation(self):
        gate = DifferentiableLogicGate()
        assert gate.negation(1.0) == 0.0
        assert gate.negation(0.0) == 1.0
        assert abs(gate.negation(0.3) - 0.7) < 1e-6

    def test_temperature_effect(self):
        gate_hot = DifferentiableLogicGate(temperature=5.0)
        gate_cold = DifferentiableLogicGate(temperature=0.1)
        # High temperature -> smoother (closer to 0.5)
        assert abs(gate_hot.sigmoid(1.0) - 0.5) < abs(gate_cold.sigmoid(1.0) - 0.5)


class TestDLIFeasibilityChecker:

    def test_blocked_transition(self):
        checker = DLIFeasibilityChecker()
        checker.add_blocked_transition("A", "B")
        assert checker.feasibility_score("A", "B") == 0.0
        assert checker.feasibility_score("A", "C") == 1.0  # No constraint

    def test_soft_constraint(self):
        checker = DLIFeasibilityChecker()
        checker.add_soft_constraint(lambda s, t: 2.0 if s == "A" else -2.0)
        score_a = checker.feasibility_score("A", "X")
        score_b = checker.feasibility_score("B", "X")
        assert score_a > score_b

    def test_validate_matrix_preserves_stochasticity(self):
        checker = DLIFeasibilityChecker()
        checker.add_blocked_transition("A", "C")

        states = ["A", "B", "C"]
        P = np.array([[0.3, 0.4, 0.3], [0.2, 0.5, 0.3], [0.1, 0.6, 0.3]])
        P_validated, mask = checker.validate_transition_matrix(states, P)

        # Check stochasticity
        row_sums = P_validated.sum(axis=1)
        assert np.allclose(row_sums, 1.0, atol=1e-6)
        # Check blocked transition is zeroed
        assert P_validated[0, 2] == 0.0

    def test_temperature_annealing(self):
        scheduler = TemperatureScheduler(initial_temp=5.0, schedule="exponential")
        initial = scheduler.temperature
        scheduler.step()
        scheduler.step()
        assert scheduler.temperature < initial


class TestTemperatureScheduler:

    def test_linear_schedule(self):
        sched = TemperatureScheduler(initial_temp=5.0, min_temp=0.1, schedule="linear")
        temps = [sched.step() for _ in range(100)]
        # Should decrease
        assert temps[-1] < temps[0]
        # Should not go below min
        for _ in range(2000):
            sched.step()
        assert sched.temperature >= 0.1

    def test_adaptive_schedule(self):
        sched = TemperatureScheduler(initial_temp=5.0, schedule="adaptive")
        # High loss -> high temperature
        sched.step(loss=2.0)
        high_loss_temp = sched.temperature
        sched.step(loss=0.1)
        low_loss_temp = sched.temperature
        assert low_loss_temp < high_loss_temp


# ═══════════════════════════════════════════════════════════════════════════
# CL-CDD Tests
# ═══════════════════════════════════════════════════════════════════════════

class TestCUSUMDetector:

    def test_no_drift_normal_signal(self):
        detector = CUSUMDetector(threshold=1.0, warmup_period=10)
        rng = np.random.default_rng(42)
        # Normal signal - no drift
        for _ in range(50):
            val = rng.normal(0.5, 0.05)
            detected = detector.update(val)
        assert not detected

    def test_drift_detection(self):
        detector = CUSUMDetector(threshold=0.3, warmup_period=10)
        # Warmup
        for _ in range(15):
            detector.update(0.5)
        # Inject sudden drift
        detected = False
        for _ in range(20):
            if detector.update(2.0):
                detected = True
                break
        assert detected

    def test_reset(self):
        detector = CUSUMDetector(threshold=0.5)
        for _ in range(30):
            detector.update(1.0)
        detector.reset()
        assert detector.cusum_value == 0.0


class TestElasticWeightConsolidation:

    def test_consolidation(self):
        ewc = ElasticWeightConsolidation(lambda_ewc=100.0)
        mc = MarkovChain()
        mc.build(["A", "B", "C"])
        mc.P = np.array([[0.5, 0.3, 0.2], [0.1, 0.6, 0.3], [0.2, 0.3, 0.5]])
        mc.start_state = "A"

        telemetry = [TelemetrySample(path=["A", "B", "C"], duration=1.0, outcome="ok")]
        ewc.consolidate(mc, telemetry)
        assert ewc.num_stored_tasks == 1

    def test_regularization_loss(self):
        ewc = ElasticWeightConsolidation(lambda_ewc=100.0)
        mc = MarkovChain()
        mc.build(["A", "B"])
        mc.P = np.array([[0.6, 0.4], [0.3, 0.7]])
        mc.start_state = "A"

        telemetry = [TelemetrySample(path=["A", "B", "A"], duration=1.0, outcome="ok")]
        ewc.consolidate(mc, telemetry)

        # Same params -> zero loss
        loss_same = ewc.regularization_loss(mc.P)
        # Different params -> positive loss
        different_P = np.array([[0.1, 0.9], [0.9, 0.1]])
        loss_diff = ewc.regularization_loss(different_P)
        assert loss_diff > loss_same


class TestContinualClosedLoopAdapter:

    def test_basic_telemetry_ingestion(self):
        adapter = ContinualClosedLoopAdapter()
        sample = TelemetrySample(path=["A", "B", "C"], duration=1.0, outcome="ok")
        event = adapter.ingest_telemetry(sample)
        assert event is None  # Not enough data for drift

    def test_staleness_score(self):
        adapter = ContinualClosedLoopAdapter()
        mc = MarkovChain()
        mc.build(["A", "B", "C"])
        mc.P = np.array([[0.5, 0.3, 0.2], [0.1, 0.6, 0.3], [0.2, 0.3, 0.5]])
        mc.start_state = "A"

        # With few samples, staleness should be low or zero
        for _ in range(5):
            adapter.ingest_telemetry(TelemetrySample(path=["A", "B"], duration=1.0, outcome="ok"))

        staleness = adapter.get_staleness_score(mc)
        assert 0 <= staleness <= 1.0


# ═══════════════════════════════════════════════════════════════════════════
# PPI Tests
# ═══════════════════════════════════════════════════════════════════════════

class TestPDFA:

    def test_basic_pdfa(self):
        pdfa = PDFA(alphabet={"a", "b"})
        pdfa.add_state("q0", termination_prob=0.1)
        pdfa.add_state("q1", termination_prob=0.5)
        pdfa.add_transition("q0", "a", "q1", 0.7)
        pdfa.add_transition("q0", "b", "q0", 0.2)
        pdfa.start_state = "q0"

        assert pdfa.num_states == 2
        assert pdfa.num_transitions == 2

    def test_to_markov_chain(self):
        pdfa = PDFA(alphabet={"a", "b"})
        pdfa.add_state("q0", termination_prob=0.0)
        pdfa.add_state("q1", termination_prob=0.0)
        pdfa.add_transition("q0", "a", "q1", 0.6)
        pdfa.add_transition("q0", "b", "q0", 0.4)
        pdfa.add_transition("q1", "a", "q0", 0.5)
        pdfa.add_transition("q1", "b", "q1", 0.5)
        pdfa.start_state = "q0"

        mc = pdfa.to_markov_chain()
        assert mc.num_states == 2
        # Rows should sum to 1
        assert np.allclose(mc.P.sum(axis=1), 1.0, atol=1e-6)

    def test_to_dfa(self):
        pdfa = PDFA(alphabet={"a"})
        pdfa.add_state("q0", termination_prob=0.9)
        pdfa.add_transition("q0", "a", "q0", 0.5)
        pdfa.start_state = "q0"

        dfa = pdfa.to_dfa(threshold=0.01)
        assert dfa.num_states >= 1


class TestProbabilisticObservationTable:

    def test_bayesian_update(self):
        table = ProbabilisticObservationTable(alphabet={"a", "b"})
        table.add_prefix("")
        table.add_suffix("")

        # After True observation, mean should increase
        table.update_cell("", "", True)
        mean, var = table.get_cell("", "")
        assert mean > 0.5

        # After another True, uncertainty should decrease
        old_var = var
        table.update_cell("", "", True)
        _, new_var = table.get_cell("", "")
        assert new_var < old_var

    def test_uncertainty_for_unqueried(self):
        table = ProbabilisticObservationTable(alphabet={"a"})
        table.add_prefix("")
        table.add_suffix("")
        mean, var = table.get_cell("", "")
        assert mean == 0.5  # Maximum uncertainty
        assert var == 0.25


class TestProbabilisticInductionLearner:

    def test_basic_learning(self):
        alphabet = {"a", "b"}

        def oracle(word):
            return len(word) < 4

        ppi = ProbabilisticInductionLearner(
            alphabet=alphabet,
            membership_oracle=oracle,
            max_iterations=10,
        )
        pdfa = ppi.learn()
        assert pdfa.num_states >= 1
        assert ppi.total_queries > 0

    def test_info_efficiency(self):
        alphabet = {"a"}

        def oracle(word):
            return word == "" or word == "a"

        ppi = ProbabilisticInductionLearner(
            alphabet=alphabet,
            membership_oracle=oracle,
            max_iterations=5,
        )
        ppi.learn()
        assert ppi.information_efficiency >= 0


# ═══════════════════════════════════════════════════════════════════════════
# AGCS Tests
# ═══════════════════════════════════════════════════════════════════════════

class TestAttentionConstraintExtractor:

    def test_extract_comparative(self):
        extractor = AttentionConstraintExtractor(confidence_threshold=0.1)
        text = "Active is more common than Idle in normal operation."
        cs, candidates = extractor.extract(text)
        # Should find at least one inequality
        assert len(candidates) > 0

    def test_extract_negation(self):
        extractor = AttentionConstraintExtractor(confidence_threshold=0.1)
        text = "The system must not transition from Idle to Emergency."
        cs, candidates = extractor.extract(text)
        blocked = [c for c in candidates if c.constraint.constraint_type == "blocked"]
        assert len(blocked) > 0

    def test_state_grounding(self):
        vocab = {"Idle", "Active", "Error"}
        extractor = AttentionConstraintExtractor(
            state_vocabulary=vocab,
            confidence_threshold=0.1,
        )
        text = "idle is more common than error"
        cs, candidates = extractor.extract(text)
        # Candidates should be grounded to vocabulary
        for c in candidates:
            if c.constraint.to_state:
                assert c.constraint.to_state in vocab or c.constraint.to_state.lower() in {s.lower() for s in vocab}

    def test_multiple_constraint_types(self):
        extractor = AttentionConstraintExtractor(confidence_threshold=0.1)
        text = (
            "Never go from A to B. "
            "X is more common than Y. "
            "If in C, then must reach D."
        )
        cs, candidates = extractor.extract(text)
        types_found = {c.constraint.constraint_type for c in candidates}
        assert len(types_found) >= 2


# ═══════════════════════════════════════════════════════════════════════════
# CTG Tests
# ═══════════════════════════════════════════════════════════════════════════

class TestCausalGraph:

    def test_build_from_markov_chain(self):
        mc = MarkovChain()
        mc.build(["A", "B", "C"])
        mc.P = np.array([[0.5, 0.3, 0.2], [0.1, 0.6, 0.3], [0.2, 0.3, 0.5]])
        mc.start_state = "A"

        graph = CausalGraph.from_markov_chain(mc)
        assert len(graph.nodes) > 0
        assert len(graph.edges) > 0

    def test_parent_child_relationships(self):
        graph = CausalGraph()
        graph.add_edge("A", "B", effect_size=0.5)
        graph.add_edge("A", "C", effect_size=0.3)
        graph.add_edge("B", "D", effect_size=0.7)

        assert "B" in graph.get_children("A")
        assert "C" in graph.get_children("A")
        assert "A" in graph.get_parents("B")


class TestShapleyAnalyzer:

    def test_shapley_computation(self):
        mc = MarkovChain()
        mc.build(["A", "B", "C"], terminal_states={"C"})
        mc.P = np.array([[0.3, 0.5, 0.2], [0.1, 0.4, 0.5], [0.0, 0.0, 1.0]])
        mc.start_state = "A"

        analyzer = ShapleyAnalyzer(mc, failure_states={"C"})
        values = analyzer.compute_shapley_values(num_samples=50)
        assert len(values) > 0
        # Shapley values are bounded (marginal contributions can be negative)
        assert all(-1.0 <= v <= 1.0 for v in values.values())

    def test_critical_transitions(self):
        mc = MarkovChain()
        mc.build(["A", "B", "C"], terminal_states={"C"})
        mc.P = np.array([[0.3, 0.5, 0.2], [0.1, 0.4, 0.5], [0.0, 0.0, 1.0]])
        mc.start_state = "A"

        analyzer = ShapleyAnalyzer(mc, failure_states={"C"})
        critical = analyzer.get_critical_transitions(top_k=3)
        assert len(critical) <= 3


class TestCounterfactualTestGenerator:

    def test_generate_suite(self):
        mc = MarkovChain()
        mc.build(["A", "B", "C", "D"], terminal_states={"D"})
        mc.P = np.array([
            [0.2, 0.5, 0.2, 0.1],
            [0.1, 0.3, 0.4, 0.2],
            [0.1, 0.2, 0.3, 0.4],
            [0.0, 0.0, 0.0, 1.0],
        ])
        mc.start_state = "A"

        ctg = CounterfactualTestGenerator(
            model=mc, failure_states={"D"}, max_path_length=20
        )
        suite = ctg.generate_counterfactual_suite(n_tests=10, strategy="hybrid")
        assert len(suite) == 10
        assert all(len(tc.path) > 0 for tc in suite)

    def test_coverage_improvement(self):
        mc = MarkovChain()
        mc.build(["A", "B", "C", "D"], terminal_states={"D"})
        mc.P = np.array([
            [0.2, 0.5, 0.2, 0.1],
            [0.1, 0.3, 0.4, 0.2],
            [0.1, 0.2, 0.3, 0.4],
            [0.0, 0.0, 0.0, 1.0],
        ])
        mc.start_state = "A"

        ctg = CounterfactualTestGenerator(model=mc, failure_states={"D"})
        ctg.generate_counterfactual_suite(n_tests=30)
        stats = ctg.get_coverage_stats()
        assert stats["state_coverage"] > 0
        assert stats["transition_coverage"] > 0


# ═══════════════════════════════════════════════════════════════════════════
# Calibrated Oracle Tests
# ═══════════════════════════════════════════════════════════════════════════

class TestCalibratedOracle:

    def test_basic_query(self):
        oracle = CalibratedOracle()
        result = oracle.query_membership("")
        assert result is True  # Empty string accepted in simulation

    def test_uncertainty_estimate(self):
        oracle = CalibratedOracle(num_ensemble_queries=3)
        estimate = oracle.query_with_uncertainty("short")
        assert 0 <= estimate.confidence <= 1
        assert estimate.epistemic_uncertainty >= 0
        assert estimate.aleatoric_uncertainty >= 0

    def test_evidence_accumulation(self):
        oracle = CalibratedOracle(num_ensemble_queries=1)
        # Query same word multiple times
        est1 = oracle.query_with_uncertainty("test")
        est2 = oracle.query_with_uncertainty("test")
        # Epistemic should decrease with more evidence
        assert est2.epistemic_uncertainty <= est1.epistemic_uncertainty + 0.01

    def test_calibrator(self):
        cal = OracleCalibrator(initial_temperature=1.0)
        # Perfect confidence should stay high
        result = cal.calibrate_confidence(0.99)
        assert result > 0.9
        # Low confidence should stay low
        result = cal.calibrate_confidence(0.1)
        assert result < 0.5


# ═══════════════════════════════════════════════════════════════════════════
# Active Query Tests
# ═══════════════════════════════════════════════════════════════════════════

class TestInformationGainSelector:

    def test_select_query(self):
        selector = InformationGainSelector(
            alphabet={"a", "b"}, strategy=QueryStrategy.HYBRID
        )
        beliefs = {"a": 0.5, "b": 0.5, "aa": 0.5}
        word = selector.select_query(beliefs, max_length=5)
        assert isinstance(word, str)
        assert len(word) <= 5

    def test_diversity(self):
        selector = InformationGainSelector(
            alphabet={"a", "b"}, strategy=QueryStrategy.HYBRID
        )
        beliefs = {}
        queries = set()
        for _ in range(10):
            word = selector.select_query(beliefs, max_length=5)
            queries.add(word)
            selector.record_result(word, True)
            beliefs[word] = 1.0
        # Should generate diverse queries
        assert len(queries) >= 5
