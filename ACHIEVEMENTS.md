# llm-mbst-research

**Neuro-Symbolic Model-Based Statistical Testing Framework**

A research framework that closes the loop between large language models and formal verification — using LLMs as semantic oracles, symbolic reasoning for constraint validation, and convex optimization to synthesize statistically faithful Markov chain models from natural language requirements.

---

## Overview

`llm-mbst-research` implements a full neuro-symbolic pipeline for model-based statistical testing (MBST). Given a set of natural language system requirements, the framework:

1. **Extracts** the state space and transition structure using an LLM oracle
2. **Validates** the extracted model symbolically against formal constraints
3. **Synthesizes** a Markov chain whose steady-state distribution matches the reference via convex optimization
4. **Generates** test sequences that exercise the model
5. **Visualizes** results for paper-ready figures and demos

The design treats LLMs not as black-box generators but as structured semantic reasoners, grounded at every step by symbolic checks and statistical guarantees.

---

## Results

### State Space Recovery

| Metric | Score |
|--------|-------|
| State Recall | **100%** |
| System F1 | **0.98** |
| State Coverage (test gen) | 88.9% |
| Transition Coverage (test gen) | 85.7% |
| Transition Precision | 0.93 |

The pipeline correctly recovers the full state space from natural language requirements. An F1 of 0.98 reflects near-perfect precision and recall on the symbolic extraction step.

### Statistical Fidelity

| Metric | Value |
|--------|-------|
| Jensen–Shannon Divergence (JSD) | **0.012** |

A JSD of 0.012 between the synthesized Markov chain's steady-state distribution and the reference distribution confirms that the convex optimization step produces a statistically faithful model — not just a structurally plausible one.

### End-to-End Pipeline

The full neuro-symbolic loop runs end-to-end:

```
NL Requirements → LLM Oracle → Symbolic Validation → Convex Optimization → Test Generation → Visualization
```

All stages are integrated and produce reproducible outputs, with visualizations suitable for papers and demos.

---

## Known Limitations & Future Work

**Test coverage saturation.** Transition coverage of 85.7% and state coverage of 88.9% are solid but not saturated. The test generator should converge to 100% with longer or more sequences; increasing `max_sequences` or verifying generator convergence is recommended before final evaluation.

**One false-positive transition.** Transition precision of 0.93 reflects a single spurious transition introduced by the feasibility-preserving heuristic in the symbolic layer. The feasibility memory occasionally adds transitions absent from the ground truth; tightening the constraint budget should eliminate this.

**Single-symbol LLM queries.** The current oracle evaluation uses 10 queries on individual symbols. Querying multi-step paths (e.g., sequences of 3–5 states) would constitute a stronger proof of oracle fidelity and is planned for the next evaluation round.

---

## Installation

Requires **Python ≥ 3.12**.

```bash
pip install -e .
```

### Dependencies

| Package | Version |
|---------|---------|
| python-dotenv | ≥ 1.0.0 |
| langchain | ≥ 1.3.9 |
| langchain-openai | ≥ 1.3.2 |
| numpy | ≥ 2.4.6 |
| scipy | ≥ 1.17.1 |
| matplotlib | ≥ 3.8.0 |

---

## Project Structure

```
llm-mbst-research/
├── README.md
└── ...          # source modules for each pipeline stage
```

---

## Version

`0.1.0` — initial research prototype.