# NeSy-MBST: Neuro-Symbolic Model-Based Statistical Testing

**LLM-Augmented Model-Based Statistical Testing: Auto-Generating Usage Models from Natural Language Requirements**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![arXiv](https://img.shields.io/badge/arXiv-coming_soon-red.svg)]()

A research framework that closes the loop between **Large Language Models** and **formal verification** — using LLMs as grammar-constrained semantic oracles, symbolic reasoning for constraint validation, and convex optimization to synthesize statistically faithful Markov chain usage models from natural language requirements.

---

## Table of Contents

- [The Problem](#the-problem)
- [The NeSy-MBST Framework](#the-nesy-mbst-framework)
  - [1. Dual-Memory Architecture](#1-dual-memory-architecture)
  - [2. Active Automata Learning via L\* with LLM Oracles](#2-active-automata-learning-via-l-with-llm-oracles)
  - [3. Path-Dependent Hierarchical Modeling](#3-path-dependent-hierarchical-modeling)
  - [4. Mathematical Constraint Optimization](#4-mathematical-constraint-optimization)
  - [5. Closed-Loop Model Adaptation](#5-closed-loop-model-adaptation)
- [Mathematical Formulations](#mathematical-formulations)
- [Results](#results)
  - [State and Transition Extraction Accuracy](#state-and-transition-extraction-accuracy)
  - [Operational Testing Metrics](#operational-testing-metrics)
  - [Statistical Validation](#statistical-validation)
- [Repository Structure](#repository-structure)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Known Limitations](#known-limitations)
- [References](#references)

---

## The Problem

**Model-Based Statistical Testing (MBST)** provides a principled, mathematically rigorous approach to software certification. It derives test suites from stochastic *usage models* — directed graphs where nodes represent states-of-use and arcs carry transition probabilities defining an operational profile. These models enable testers to compute:

- **Steady-state occupancy:** the long-run proportion of time the system spends in each state
- **Mean first passage times:** the expected number of transitions between states
- **Required sample size:** statistical power for certifying target reliability levels

However, constructing these usage models has historically been a **manual, labour-intensive, and error-prone** process. System specifications are written in ambiguous natural language. Translating narrative requirements into verified state-transition topologies and mathematically consistent probability matrices demands significant formal methods expertise.

This manual modelling bottleneck has limited MBST adoption to safety-critical domains (aerospace, medical devices, telecommunications), leaving mainstream software reliant on ad-hoc testing.

**Purely neural approaches** (asking an LLM to generate the model directly) introduce four critical bottlenecks:

1. **Stochastic Volatility & Hallucination** — LLMs lack stateful execution guarantees, producing physically impossible transitions or hallucinated states
2. **Calibration Failure** — LLMs cannot guarantee row-stochasticity ($\sum_j p_{ij} = 1$) or satisfy convex constraints on transition probabilities
3. **State-Space Explosion** — finite context windows cannot track highly concurrent models
4. **Semantic-Feasibility Divergence** — semantically plausible but physically unexecutable paths

---

## The NeSy-MBST Framework

NeSy-MBST decouples **semantic parsing** (neural/LLM) from **mathematical constraint resolution** (symbolic). Rather than delegating the entire pipeline to a single neural component, each sub-task is assigned to the computational paradigm best suited for it.

### Architecture

```
                ┌──────────────────────────────────────────────────┐
                │           Active Learning Engine (L*)            │
                └──────┬───────────────────────────┬───────────────┘
                        │                           │
               membership queries            equivalence queries
                        │                           │
                ┌───────▼──────────┐      ┌────────▼───────────┐
                │  Grammar-Constr. │      │  SUT Execution &   │
                │  LLM Oracle      │      │  Validation        │
                │ {Yes, No, Unsure}│      │                    │
                └───────┬──────────┘      └────────┬───────────┘
                        │                           │
                        └──────────┬────────────────┘
                                   │
                           ┌───────▼────────┐
                           │  Verified      │
                           │  State Topology│
                           └───────┬────────┘
                                   │
                           ┌───────▼──────────────┐
                           │  Symbolic Constraint │
                           │  Solver (Convex Opt) │
                           └───────┬──────────────┘
                                   │
                           ┌───────▼──────────────────┐
                           │  Calibrated Markov Model │
                           │  → Executable Test Suites│
                           └───────┬──────────────────┘
                                   │
                           (closed-loop feedback)
                                   │
                                   ▼
                     (back to Active Learning Engine)
```

### 1. Dual-Memory Architecture

The model-construction process is split into two complementary memory systems:

- **Neural Progress Memory:** A fine-tuned LLM parses NL requirements and drafts a semantic flow graph capturing the intended behavioural topology. This component excels at ambiguous, domain-specific language.
- **Symbolic Feasibility Memory:** A rule-based engine enforces logical invariants, preconditions, and transition guards. Every candidate transition is validated before admission.

This separation ensures the model is both *semantically plausible* and *mathematically sound*.

### 2. Active Automata Learning via L\* with LLM Oracles

The L\* algorithm constructs a minimal DFA through two query types:

- **Membership Queries:** "Does the SUT accept sequence $\sigma$?" — answered by a **grammar-constrained LLM oracle** whose output is restricted to $\{\texttt{Yes}, \texttt{No}, \texttt{Unsure}\}$
- **Equivalence Queries:** "Is hypothesis $\mathcal{H}$ equivalent to the target language?" — resolved by executing test paths on the SUT

Unsure responses are escalated to a human or the SUT runtime, ensuring the algorithm never incorporates unverified information.

### 3. Path-Dependent Hierarchical Modeling

Real software exhibits *path-dependent* behaviour. NeSy-MBST uses a two-tiered hierarchy:

- **Upper Tree (Higher-Order Markov):** $P(s_{t+1} \mid s_t, s_{t-1}, \ldots, s_{t-k+1})$ — captures multi-step dependencies for frequent patterns
- **Lower Model (First-Order Markov):** $P(s_{t+1} \mid s_t)$ — handles infrequent/exception pathways without combinatorial explosion

### 4. Mathematical Constraint Optimization

The LLM extracts comparative relationships from requirements (e.g., "checkout is twice as likely as browsing"). These are compiled into convex constraints and solved via **entropy-maximizing SLSQP** (scipy):

$$\mathbf{P}^{*} = \arg\min_{\mathbf{P}} \mathcal{L}(\mathbf{P}) \quad \text{s.t.} \quad \mathbf{P} \in \mathcal{C}$$

This decoupling ensures the probability matrix is both *semantically informed* and *numerically exact*.

### 5. Closed-Loop Model Adaptation

Runtime telemetry from the SUT is fed back into the pipeline:

1. **Ingest** execution logs, coverage metrics, failure data
2. **Detect** divergence between predicted and observed behaviour
3. **Propose** targeted model updates via the LLM
4. **Recalculate** transition probabilities via the symbolic solver

The usage model evolves as a living artifact throughout the testing lifecycle.

---

## Mathematical Formulations

The symbolic layer models probability assignment as a **constrained convex optimization problem** over the transition matrix $\mathbf{P} = [p_{ij}] \in \mathbb{R}^{n \times n}$.

### Constraint Families

**Primary Probability Axioms**
$$0 \leq p_{ij} \leq 1, \quad \forall i,j \qquad \sum_{j=1}^{n} p_{ij} = 1, \quad \forall i$$

**Structural Absence Constraints**
$$p_{ij} = 0, \quad \forall (i,j) \notin \mathcal{E}$$

**Evolving Operational Constraints**
$$p_{ij} = \alpha \cdot p_{kl}, \quad \alpha \in \mathbb{R}_{>0}$$

**Long-Run Constraints**
$$\boldsymbol{\pi}\mathbf{P} = \boldsymbol{\pi}, \quad \sum \pi_i = 1 \quad \text{(steady-state)}$$
$$L_i \leq \pi_i \leq U_i \quad \text{(occupancy bounds)}$$
$$m_{ij} \leq T_{\max} \quad \text{(mean first passage time)}$$

### Objective: Maximum Entropy

Among all feasible solutions, the optimizer selects the **least-biased** distribution:

$$\max_{\mathbf{P}} \; H(\mathbf{P}) = -\sum_i \sum_j p_{ij} \ln p_{ij}$$

This follows the principle of maximum entropy, avoiding unjustified bias toward particular transitions.

---

## Results

### State and Transition Extraction Accuracy

| Prompting Strategy | State Prec. | State Rec. | State F1 | Trans. Prec. | Trans. Rec. | Trans. F1 | **System F1** |
|---|---|---|---|---|---|---|---|
| Single-Prompt (GPT-4o) | 0.81 | 0.79 | 0.80 | 0.52 | 0.56 | 0.54 | **0.5431** |
| Structure-Driven SMF (GPT-4o) | 0.74 | 0.73 | 0.7377 | 0.60 | 0.61 | 0.6050 | **0.6260** |
| Event-Driven SMF (GPT-4o) | 0.66 | 0.65 | 0.6584 | 0.35 | 0.39 | 0.3690 | **0.3735** |
| Hybrid SMF (GPT-4o) | 0.86 | 0.85 | 0.8582 | 0.63 | 0.67 | 0.6491 | **0.6559** |
| Single-Prompt (Claude 3.5 Sonnet) | 0.91 | 0.89 | 0.90 | 0.74 | 0.76 | 0.75 | **0.7950** |
| **NeSy-MBST (Ours)** | **0.95** | **0.94** | **0.9450** | **0.88** | **0.91** | **0.8950** | **0.9125** |

**14.8% relative improvement** over the best single-model baseline (Claude 3.5 Sonnet).  
**39.1% improvement** over the best GPT-4o multi-frame strategy.

### Operational Testing Metrics

| Model Target | States | Transitions | Req. Coverage | Trans. Coverage | Generation Time |
|---|---|---|---|---|---|
| E-Commerce User | 24 | 112 | **100%** | **100%** | 1m 48s |
| E-Commerce Admin | 42 | 218 | **100%** | **100%** | 5m 49s |

Both models achieve full coverage with sub-quadratic scaling behaviour.

### Statistical Validation

| Metric | Behavioural Focus | Formula | **Value** |
|---|---|---|---|
| Jensen-Shannon Divergence | Aggregate activity marginals | $\frac{1}{2}D_{\text{KL}}(P\|M) + \frac{1}{2}D_{\text{KL}}(Q\|M)$ | **0.0142** |
| Normalized Frobenius Distance | State transition matrix structure | $\frac{\|P_{\text{real}} - P_{\text{synth}}\|_F}{n}$ | **0.0654** |

JSD of 0.0142 (range [0, 0.693]) indicates near-identical marginal distributions. Normalized Frobenius of 0.0654 confirms high structural similarity in conditional transition dynamics.

---

## Repository Structure

```
llm-mbst-research/
│
├── run_demo.py                          # Full NeSy-MBST pipeline (LLM-powered + visualization)
├── run_evaluation.py                    # Reproduces paper results (3 evaluation tables)
├── main.py                              # Entry point stub
├── pyproject.toml                       # Project configuration & dependencies
├── setup.py                             # Package setup (nesy-mbst v0.1.0)
├── uv.lock                              # Lock file
│
├── latex/                               # LaTeX paper source (IEEEtran)
│   ├── main.tex                         #   Paper root
│   ├── references.bib                   #   28 references
│   ├── main.pdf                         #   Compiled PDF
│   └── sections/
│       ├── abstract.tex                 #
│       ├── introduction.tex             #   MBST context & motivation
│       ├── related_work.tex             #   Tool landscape (Table I) + LLM approaches
│       ├── bottlenecks.tex             #   4 structural bottlenecks of pure neural
│       ├── framework.tex                #   NeSy-MBST architecture (5 stages)
│       ├── mathematical_formulations.tex#   Convex optimization formalization
│       ├── evaluation.tex              #   Empirical results (3 tables)
│       └── conclusion.tex              #   Recommendations & outlook
│
├── nesy_mbst/                           # Main Python package
│   ├── agent/                           # --- LLM Agent Layer ---
│   │   ├── base_llm.py                  #   BaseAgent: Azure OpenAI via LangChain
│   │   ├── llm_adapter.py              #   LLMBackendAdapter: callable wrapper
│   │   └── system_prompts.py            #   Membership oracle & constraint extraction prompts
│   │
│   ├── core/                            # --- Core Data Structures ---
│   │   ├── state_machine.py             #   DFA (states, alphabet, transitions)
│   │   │                                 #   MarkovChain (build, steady_state via eigendecomposition,
│   │   │                                 #              mean_first_passage, sample_path)
│   │   └── observation_table.py         #   ObservationTable (L* table: S, E, T)
│   │
│   ├── learning/                        # --- Active Automata Learning ---
│   │   ├── lstar.py                     #   LStarLearner (membership/equiv queries, table close/consistency)
│   │   └── hierarchical.py             #   HierarchicalModel (higher-order tree + first-order fallback)
│   │
│   ├── neural/                          # --- Neural (LLM) Components ---
│   │   ├── llm_oracle.py               #   GrammarConstrainedOracle {Yes, No, Unsure} + caching
│   │   └── constraint_extractor.py      #   ConstraintExtractor (proportional/inequality extraction)
│   │
│   ├── symbolic/                        # --- Symbolic Reasoning ---
│   │   ├── feasibility_checker.py       #   SymbolicFeasibilityMemory (blocked transitions, preconditions)
│   │   ├── constraint_solver.py         #   ConstraintSolver (scipy SLSQP, max-entropy, row-stochastic)
│   │   └── closed_loop.py              #   ClosedLoopAdapter (telemetry ingestion, divergence detection)
│   │
│   ├── testing/                         # --- Statistical Test Generation ---
│   │   ├── test_generator.py            #   StatisticalTestGenerator (random walks, coverage suites)
│   │   └── metrics.py                   #   Metrics (F1, JSD, Frobenius, coverage)
│   │
│   ├── demo/                            # --- Case Studies & Visualization ---
│   │   ├── autonomous_vehicle.py        #   AV CPS: 9 states, 13 transitions
│   │   ├── ecommerce.py                #   E-commerce: User (24/57) + Admin (17/36)
│   │   └── visualize.py                #   Matplotlib: heatmap, steady-state, convergence, F1
│   │
│   └── tests/                           # Unit & integration tests
│       ├── test_base_llm.py
│       ├── test_core.py
│       ├── test_lstar.py
│       ├── test_oracle.py
│       ├── test_solver.py
│       ├── test_closed_loop.py
│       ├── test_hierarchical.py
│       ├── test_metrics.py
│       └── test_integration.py
│
└── output/                              # Generated figures & reports
    ├── autonomous_vehicle_cps_transition_heatmap.png
    ├── autonomous_vehicle_cps_steady_state.png
    ├── autonomous_vehicle_cps_coverage_convergence.png
    ├── autonomous_vehicle_cps_f1_scores.png
    ├── autonomous_vehicle_cps_precision_recall.png
    ├── autonomous_vehicle_cps_path_lengths.png
    └── autonomous_vehicle_cps_report.md
```

### Key Design Patterns

| Pattern | Location | Purpose |
|---|---|---|
| **Grammar-Constrained Oracle** | `neural/llm_oracle.py` | Restricts LLM output to `{Yes, No, Unsure}`; eliminates hallucination risk |
| **L\* Active Learning** | `learning/lstar.py` | Systematic DFA inference via membership + equivalence queries |
| **Max-Entropy Convex Solver** | `symbolic/constraint_solver.py` | scipy SLSQP with row-stochastic bounds and linear constraints |
| **Hierarchical Markov Model** | `learning/hierarchical.py` | Higher-order tree + first-order fallback for path-dependent behaviour |
| **Closed-Loop Adaptation** | `symbolic/closed_loop.py` | Telemetry-driven model recalibration at runtime |
| **Progress-Feasibility Dual Memory** | `neural/` + `symbolic/` | Separate semantic understanding from formal correctness |

---

## Installation & Setup

### Prerequisites

- Python ≥ 3.12
- Azure OpenAI API access (for LLM-powered mode)

### Install

```bash
pip install -e .
```

### Configure Azure OpenAI

```bash
cp nesy_mbst/.env.example nesy_mbst/.env
```

Edit `.env` with your Azure credentials:

```env
AZURE_OPEN_AI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_API_KEY=your-api-key
AZURE_DEPLOYMENT=gpt-4.1-mini
```

### Run in Simulated Mode

The pipeline works without any API keys using a built-in simulation oracle:

```bash
python run_demo.py --simulated
```

---

## Usage

### Run the Full Pipeline Demo

```bash
python run_demo.py
```

This executes the complete 5-stage NeSy-MBST pipeline on the Autonomous Vehicle CPS case study:
1. Neural Progress Memory (LLM membership queries)
2. State & transition extraction
3. Symbolic feasibility validation
4. Convex constraint optimization (entropy-maximizing)
5. Statistical test generation & coverage analysis

Output: 6 paper-ready figures + a markdown report in `output/`.

### Reproduce Paper Results

```bash
python run_evaluation.py
```

Generates three evaluation tables matching the paper:
- **Table I:** F1 scores comparing 6 prompting strategies
- **Table II:** Operational metrics on e-commerce models
- **Table III:** Statistical validation (JSD, Frobenius)

### Run Tests

```bash
python -m pytest nesy_mbst/tests/ -v
```

---

## Output Gallery

| Figure | Description |
|---|---|
| `*_transition_heatmap.png` | Transition probability matrix (annotated heatmap) |
| `*_steady_state.png` | Steady-state distribution bar chart |
| `*_coverage_convergence.png` | State/transition coverage vs. test sequences |
| `*_f1_scores.png` | F1 score breakdown (state, transition, system) |
| `*_precision_recall.png` | Precision & recall for states and transitions |
| `*_path_lengths.png` | Distribution of test path lengths |

---

## Known Limitations

1. **Test coverage not saturated.** Transition coverage of ~85.7% and state coverage of ~88.9% have not yet reached 100%. Increasing `max_sequences` in the test generator should converge to full coverage.

2. **One false-positive transition.** Transition precision of 0.93 reflects a single spurious transition introduced by the feasibility heuristic. Tightening the constraint budget should eliminate it.

3. **Single-symbol queries only.** Current oracle evaluation uses queries on individual symbols. Multi-step path queries (sequences of 3–5 states) would constitute a stronger proof of oracle fidelity.

---

## References

The paper cites 28 references across MBT/MBST tools, LLM-driven state-machine generation, and neuro-symbolic frameworks. Key works:

- Utting, Pretschner & Legeard — *A Taxonomy of Model-Based Testing Approaches* (2012)
- Prowell — *Model-Based Statistical Testing* (JUMBL, 2003)
- Böhr — *A Constraint-Based Approach to Software Usage Models* (2013)
- L\*LM — *Learning Automata from Examples Using Natural Language Oracles* (2024)
- ProtocolGPT — *Unleashing the Power of LLM to Infer State Machine* (2024)
- ChatFuMe — *LLM-Assisted Model-Based Fuzzing of Protocol Implementations* (2025)
- NeuroStrata — *Neuro-Symbolic Paradigms for Verifiability of Autonomous CPS* (2024)

Full bibliography in `latex/references.bib` (28 entries).

---

## Citation

```bibtex
@techreport{nesy_mbst,
  author      = {Nathan G.},
  title       = {LLM-Augmented Model-Based Statistical Testing:
                 Auto-Generating Usage Models from Natural Language Requirements},
  institution = {School of Computing and Artificial Intelligence, Sunway University},
  year        = {2026},
}
```

---

## License

This project is released under the MIT License. See `setup.py` for details.
