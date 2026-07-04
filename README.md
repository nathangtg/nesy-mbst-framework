# NeSy-MBST

### *The Machine Proposes. The Proof Disposes.*
**Neuro-Symbolic Synthesis of Formally Verified Markov Usage Models from Natural Language Requirements**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![IEEE](https://img.shields.io/badge/venue-IEEE_submission-blue.svg)]()
[![DOI](https://img.shields.io/badge/DOI-pending-lightgrey.svg)]()

**Authors:** Nathan G.¹² · Jordan Chay¹ · Jaeden Ting YiYong¹ · Wai Phyo Hein¹  
¹ School of Computing and Artificial Intelligence, Sunway University, Subang Jaya, Malaysia  
² Mercedes-Benz Tech Innovation  

---

## Overview

**Model-Based Statistical Testing (MBST)** derives statistically optimal test suites from Markov chain usage models — directed graphs where transition probabilities encode real-world operational usage. Tests generated from these models systematically exercise fault-revealing paths in proportion to how frequently users take them, giving MBST a 25–40% fault-detection advantage over unstructured script-based testing. The barrier to adoption: constructing usage models manually requires weeks of formal-methods expertise.

**NeSy-MBST eliminates that barrier.** It reads your natural-language requirements document and outputs a complete, mathematically verified Markov chain usage model — automatically. It then generates a full test suite from that model in under six minutes.

| Metric | Value |
|---|:---:|
| System-level extraction F1 | **0.9125** (threshold: 0.90) |
| Transition coverage vs. pure-neural | **85.7%** vs 50.0% (+35.7 pp) |
| Jensen–Shannon divergence | **0.012** |
| Model generation time (42 states) | **< 6 minutes** |
| Improvement over best GPT-4o baseline | **+39.1%** |

---

## Research Questions

This repository is the reference implementation for a paper submitted to IEEE TSE. The paper addresses four research questions:

- **RQ1 — Structural fidelity:** Can automated neuro-symbolic construction achieve F1 ≥ 0.90 for safety-critical test generation without manual effort?
- **RQ2 — Fault-detection coverage:** Does a NeSy-MBST model produce higher transition coverage than a purely neural baseline?
- **RQ3 — Probabilistic calibration:** Does symbolic constraint optimization preserve operationally weighted test allocation?
- **RQ4 — Component necessity:** Which components (symbolic loop, convex optimizer, closed-loop feedback) are individually necessary?

---

## Repository Structure

```
llm-mbst-research/
│
├── README.md                        ← You are here
├── SLIDES.md                        ← 15-minute presentation outline
├── pyproject.toml                   ← Project metadata and dependencies
├── uv.lock                          ← Locked dependency tree (uv)
│
├── run_demo.py                      ← Full pipeline demo (AV CPS case study)
├── run_evaluation.py                ← Reproduces paper Tables II–IV
├── run_ablation.py                  ← Reproduces Table V (ablation study, seed=42)
├── run_v2_evaluation.py             ← Extended v2 evaluation
├── generate_figures.py              ← Generates all 5 publication figures (PDF+PNG)
│
├── nesy_mbst/                       ← Core Python package
│   ├── agent/                       ← LLM integration layer
│   │   ├── base_llm.py              ← BaseAgent abstract class (Azure OpenAI)
│   │   ├── llm_adapter.py           ← callable(str)→str adapter
│   │   └── system_prompts.py        ← Oracle and extractor prompts
│   ├── core/                        ← Foundational data structures
│   │   ├── state_machine.py         ← DFA and MarkovChain classes
│   │   └── observation_table.py     ← L* observation table
│   ├── learning/                    ← Active automata learning
│   │   ├── lstar.py                 ← L* learner (Angluin 1987)
│   │   └── hierarchical.py          ← Higher-order Markov chain model
│   ├── learning_v2/                 ← Extended learning components
│   │   ├── active_query.py          ← Multi-step oracle querying
│   │   └── probabilistic_induction.py
│   ├── neural/                      ← Neural layer
│   │   ├── llm_oracle.py            ← Grammar-constrained oracle {Yes, No, Unsure}
│   │   └── constraint_extractor.py  ← NL→constraint extraction
│   ├── neural_v2/                   ← Enhanced neural components
│   │   ├── calibrated_oracle.py     ← Calibrated multi-step oracle
│   │   └── attention_constraint_extractor.py
│   ├── symbolic/                    ← Symbolic layer
│   │   ├── feasibility_checker.py   ← Rule-based transition validation
│   │   ├── constraint_solver.py     ← SLSQP max-entropy convex solver
│   │   └── closed_loop.py           ← Telemetry-driven recalibration
│   ├── symbolic_v2/                 ← Extended symbolic components
│   │   ├── differentiable_logic.py
│   │   └── continual_adapter.py
│   ├── testing/                     ← Test generation and metrics
│   │   ├── test_generator.py        ← Statistical test suite generator
│   │   └── metrics.py               ← F1, JSD, Frobenius, coverage
│   ├── testing_v2/
│   │   └── counterfactual_generator.py
│   ├── demo/                        ← Benchmark case studies
│   │   ├── autonomous_vehicle.py    ← AV CPS (9 states, 13 transitions)
│   │   ├── ecommerce.py             ← E-commerce User + Admin models
│   │   └── visualize.py             ← Matplotlib figure generation
│   └── tests/                       ← Test suite (9 modules)
│       ├── test_core.py
│       ├── test_lstar.py
│       ├── test_oracle.py
│       ├── test_solver.py
│       ├── test_closed_loop.py
│       ├── test_hierarchical.py
│       ├── test_metrics.py
│       ├── test_base_llm.py
│       ├── test_integration.py
│       └── test_v2_modules.py
│
├── latex/                           ← IEEE paper source (IEEEtran)
│   ├── main.tex                     ← Root document
│   ├── references.bib               ← 55 verified entries (CrossRef/arXiv)
│   ├── Makefile                     ← pdflatex + bibtex build
│   └── sections/
│       ├── abstract.tex
│       ├── introduction.tex         ← Includes RQ1–RQ4
│       ├── literature_review.tex    ← 20 papers + fault-detection subsection
│       ├── related_work.tex
│       ├── bottlenecks.tex
│       ├── framework.tex
│       ├── mathematical_formulations.tex
│       ├── evaluation.tex           ← Tables II–IV + fault-detection analysis
│       ├── ablation.tex             ← Table V (conditions A–D)
│       ├── threats.tex              ← Threats to validity
│       └── conclusion.tex           ← Adoption guidelines + future work
│
└── output/                          ← Generated artefacts (not committed)
    ├── figures/                     ← Publication figures (PDF + PNG)
    │   ├── fig1_f1_comparison.*
    │   ├── fig2_ablation_f1.*
    │   ├── fig3_divergence.*
    │   ├── fig4_coverage.*
    │   └── fig5_radar.*
    └── autonomous_vehicle_cps_*/    ← AV demo output reports
```

---

## Installation

**Prerequisites:** Python ≥ 3.12 · Azure OpenAI API access (optional — simulator available)

### With `uv` (recommended)

```bash
git clone https://github.com/nathangtg/llm-mbst-research
cd llm-mbst-research
uv sync
```

### With `pip`

```bash
pip install -e .
```

### Configure credentials

```bash
cp nesy_mbst/.env.example nesy_mbst/.env
```

Edit `nesy_mbst/.env`:

```env
AZURE_OPEN_AI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_API_KEY=your-api-key
AZURE_DEPLOYMENT=gpt-4.1-mini
```

> **No API key?** All scripts fall back to a rule-based simulator — results are representative but use regex extraction rather than a live LLM.

---

## Reproducing Paper Results

### Figure generation (all 5 paper figures)

```bash
python generate_figures.py
# → output/figures/fig1_f1_comparison.pdf  (Table II bar chart)
# → output/figures/fig2_ablation_f1.pdf    (ablation F1)
# → output/figures/fig3_divergence.pdf     (JSD + Frobenius)
# → output/figures/fig4_coverage.pdf       (coverage by condition)
# → output/figures/fig5_radar.pdf          (multi-dimensional radar)
```

### Tables II–IV (evaluation section)

```bash
python run_evaluation.py
```

### Table V (ablation study, RQ4)

```bash
python run_ablation.py
# Fixed seed=42, Azure OpenAI backend (falls back to simulator)
# Reports: Sys.F1, JSD, Frobenius, coverage for conditions A–D
```

### Full pipeline demo

```bash
python run_demo.py
# Autonomous Vehicle CPS case study: 9 states, 13 transitions
# Generates figures and a Markdown report in output/
```

### Test suite

```bash
python -m pytest nesy_mbst/tests/ -v
```

---

## Framework Architecture

NeSy-MBST separates concerns by computational capability: neural inference handles ambiguous language; symbolic computation handles formal correctness.

```
Natural Language Requirements
           │
           ▼
  ┌─────────────────────┐
  │  Neural Layer       │  LLM reads requirements, extracts candidate
  │  (LLM Oracle)       │  states/transitions, answers membership queries
  └────────┬────────────┘
           │  {Yes / No / Unsure}
           ▼
  ┌─────────────────────┐
  │  L* Active Learning │  Systematically explores state space via
  │  Engine             │  membership + equivalence queries
  └────────┬────────────┘
           │  hypothesis automaton
           ▼
  ┌─────────────────────┐
  │  Symbolic Feasibility│  Rejects transitions violating invariants,
  │  Checker            │  preconditions, and guard conditions
  └────────┬────────────┘
           │  verified topology
           ▼
  ┌─────────────────────┐
  │  Convex Optimizer   │  Assigns transition probabilities via SLSQP
  │  (SLSQP)            │  under row-stochastic + domain constraints
  └────────┬────────────┘
           │  calibrated matrix P*
           ▼
  ┌─────────────────────┐
  │  Markov Chain       │  Complete usage model → statistical test
  │  Usage Model        │  suite generation
  └────────┬────────────┘
           │
           ▼  (runtime telemetry)
  ┌─────────────────────┐
  │  Closed-Loop        │  Detects model drift, recalibrates
  │  Adapter            │  transition probabilities continuously
  └─────────────────────┘
```

### Key component map

| Component | File | Role |
|---|---|---|
| Grammar-Constrained Oracle | `neural/llm_oracle.py` | Restricts LLM to `{Yes, No, Unsure}` |
| L\* Learner | `learning/lstar.py` | Systematic DFA inference (Angluin 1987) |
| Feasibility Checker | `symbolic/feasibility_checker.py` | Rule-based structural validation |
| Convex Solver | `symbolic/constraint_solver.py` | scipy SLSQP, max-entropy objective |
| Hierarchical Model | `learning/hierarchical.py` | Higher-order tree + first-order fallback |
| Closed-Loop Adapter | `symbolic/closed_loop.py` | Telemetry-driven recalibration |
| Metrics | `testing/metrics.py` | F1, JSD, Frobenius, coverage |

---

## Ablation Study Results

Four cumulative conditions on the Autonomous Vehicle CPS benchmark (seed=42):

| Condition | Sys. F1 | Trans. Coverage | JSD | Frobenius |
|---|:---:|:---:|:---:|:---:|
| A — Pure-Neural | 0.9036 | 50.0% | 0.157 | 0.163 |
| B — +Symbolic Loop | **0.9818** | **85.7%** | 0.012 | 0.084 |
| C — +Convex Optimizer | 0.9818 | 85.7% | 0.012 | 0.084 |
| D — Full NeSy-MBST | 0.9818 | 85.7% | **0.012** | **0.084** |

**Symbolic loop** → primary driver of structural correctness and coverage (+35.7 pp).  
**Convex optimizer** → primary driver of probabilistic calibration (JSD: 0.157 → 0.012).  
**Closed-loop** → continuous fidelity maintenance over extended test campaigns.

---

## Threats to Validity

| Threat | Nature | Mitigation |
|---|---|---|
| Benchmark scope | 2 domains, max 42 states | Industrial case studies planned (see Future Work) |
| Ground-truth annotation | Single-author | AV benchmark from formal spec; e-commerce tautological (disclosed in paper) |
| Oracle consistency | Not formally proven | Empirically: 0% Unsure rate on AV benchmark; 94% direct / 6% SUT-escalated |
| Statistical validity | Single seed (42) | Fully reproducible; multi-seed study in future work |
| LLM provider | Azure GPT-4.1-mini only | Simulator fallback available; provider sensitivity in future work |

---

## Citation

```bibtex
@article{nesy_mbst_2026,
  author       = {Nathan G. and Jordan Chay and Jaeden Ting YiYong
                  and Wai Phyo Hein},
  title        = {The Machine Proposes. The Proof Disposes.:
                  Neuro-Symbolic Synthesis of Formally Verified
                  {Markov} Usage Models from Natural Language Requirements},
  journal      = {IEEE Transactions on Software Engineering},
  year         = {2026},
  note         = {Under review. Preprint: \url{https://github.com/nathangtg/llm-mbst-research}}
}
```

---

## Future Work

1. **Fault-seeding experiments** — directly measure defect-detection rates against planted fault corpora; validate the transition-coverage proxy against actual bug catch rates
2. **Industrial case studies** — deploy on real codebases in automotive (ISO 26262), medical devices, and telecommunications
3. **Multi-annotator validation** — replace single-author ground truth with inter-rater reliability protocol
4. **Domain generalisation** — evaluate on informally-written requirements (agile user stories, verbal specs)
5. **Oracle sensitivity** — characterise how LLM provider, version, and temperature affect convergence and F1

---

## License

Released under the MIT License. See `LICENSE` for details.
