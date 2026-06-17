from __future__ import annotations

import io
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import Dict, List, Optional
from nesy_mbst.core.state_machine import MarkovChain
from nesy_mbst.testing.test_generator import StatisticalTestGenerator, TestCase
from nesy_mbst.testing.metrics import Metrics

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def _save(fig: plt.Figure, name: str) -> str:
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_transition_heatmap(
    mc: MarkovChain,
    title: str = "Transition Probability Matrix",
    filename: str = "transition_heatmap.png",
) -> str:
    fig, ax = plt.subplots(figsize=(10, 8))
    n = len(mc.states)
    im = ax.imshow(mc.P, cmap="YlOrRd", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(mc.states, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(mc.states, fontsize=8)
    for i in range(n):
        for j in range(n):
            val = mc.P[i, j]
            if val > 0.01:
                ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=7, color="black" if val < 0.5 else "white")
    ax.set_title(title, fontsize=14, fontweight="bold")
    fig.colorbar(im, ax=ax, shrink=0.8, label="Transition Probability")
    fig.tight_layout()
    return _save(fig, filename)


def plot_steady_state_distribution(
    mc: MarkovChain,
    title: str = "Steady-State Distribution",
    filename: str = "steady_state.png",
) -> str:
    pi = mc.steady_state()
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(mc.states)))
    bars = ax.bar(mc.states, pi, color=colors, edgecolor="black", linewidth=0.5)
    for bar, val in zip(bars, pi):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
                f"{val:.3f}", ha="center", va="bottom", fontsize=8)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_ylabel("Steady-State Probability")
    ax.set_xlabel("State")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    return _save(fig, filename)


def plot_coverage_convergence(
    model: MarkovChain,
    max_sequences: int = 100,
    title: str = "Test Coverage Convergence",
    filename: str = "coverage_convergence.png",
) -> str:
    generator = StatisticalTestGenerator(model, max_path_length=200)
    covered_states: set = set()
    covered_transitions: set = set()
    state_covs: list[float] = []
    trans_covs: list[float] = []
    for i in range(max_sequences):
        tc = generator.generate_random_walk()
        covered_states.update(tc.path)
        covered_transitions.update(tc.transitions)
        state_covs.append(len(covered_states) / max(model.num_states, 1))
        trans_covs.append(len(covered_transitions) / max(model.num_transitions, 1))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(range(1, max_sequences + 1), state_covs, label="State Coverage", linewidth=2, color="#2E86AB")
    ax.plot(range(1, max_sequences + 1), trans_covs, label="Transition Coverage", linewidth=2, color="#A23B72")
    ax.axhline(y=1.0, color="gray", linestyle="--", alpha=0.5, label="100% Target")
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel("Number of Test Sequences")
    ax.set_ylabel("Coverage")
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 1.05)
    fig.tight_layout()
    return _save(fig, filename)


def plot_f1_comparison(
    f1_scores: Dict[str, float],
    title: str = "F1 Score Comparison (NeSy-MBST vs Ground Truth)",
    filename: str = "f1_scores.png",
) -> str:
    labels_to_plot = ["state_f1", "transition_f1", "system_f1"]
    display_labels = ["State F1", "Transition F1", "System F1"]
    values = [f1_scores.get(k, 0) for k in labels_to_plot]
    colors = ["#2E86AB", "#A23B72", "#F18F01"]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(display_labels, values, color=colors, edgecolor="black", linewidth=0.8, width=0.5)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f"{val:.4f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_ylim(0, 1.1)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_ylabel("F1 Score")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    return _save(fig, filename)


def plot_precision_recall(
    f1_scores: Dict[str, float],
    title: str = "Precision & Recall Breakdown",
    filename: str = "precision_recall.png",
) -> str:
    metrics = {
        "State\nPrecision": f1_scores.get("state_precision", 0),
        "State\nRecall": f1_scores.get("state_recall", 0),
        "Transition\nPrecision": f1_scores.get("transition_precision", 0),
        "Transition\nRecall": f1_scores.get("transition_recall", 0),
    }
    labels = list(metrics.keys())
    values = list(metrics.values())
    colors = ["#2E86AB", "#2E86AB", "#A23B72", "#A23B72"]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, values, color=colors, edgecolor="black", linewidth=0.8, width=0.5)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f"{val:.4f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_ylim(0, 1.1)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_ylabel("Score")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    return _save(fig, filename)


def plot_path_length_distribution(
    suite: List[TestCase],
    title: str = "Test Path Length Distribution",
    filename: str = "path_lengths.png",
) -> str:
    lengths = [len(tc.path) for tc in suite]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(lengths, bins=20, color="#2E86AB", edgecolor="black", alpha=0.8)
    ax.axvline(np.mean(lengths), color="#A23B72", linestyle="--", linewidth=2,
               label=f"Mean: {np.mean(lengths):.1f}")
    ax.axvline(np.median(lengths), color="#F18F01", linestyle=":", linewidth=2,
               label=f"Median: {np.median(lengths):.1f}")
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel("Path Length")
    ax.set_ylabel("Frequency")
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return _save(fig, filename)


def plot_all_pipeline_results(
    mc: MarkovChain,
    suite: List[TestCase],
    f1_scores: Dict[str, float],
    scenario_name: str,
) -> Dict[str, str]:
    safe_name = scenario_name.lower().replace(" ", "_").replace("-", "_")
    outputs = {}
    outputs["heatmap"] = plot_transition_heatmap(mc, title=f"{scenario_name} - Transition Probabilities",
                                                  filename=f"{safe_name}_transition_heatmap.png")
    outputs["steady_state"] = plot_steady_state_distribution(mc, title=f"{scenario_name} - Steady-State Distribution",
                                                              filename=f"{safe_name}_steady_state.png")
    outputs["coverage"] = plot_coverage_convergence(mc, max_sequences=50,
                                                     title=f"{scenario_name} - Coverage Convergence",
                                                     filename=f"{safe_name}_coverage_convergence.png")
    outputs["f1"] = plot_f1_comparison(f1_scores, title=f"{scenario_name} - F1 Scores",
                                        filename=f"{safe_name}_f1_scores.png")
    outputs["pr"] = plot_precision_recall(f1_scores, title=f"{scenario_name} - Precision & Recall",
                                           filename=f"{safe_name}_precision_recall.png")
    outputs["path_lengths"] = plot_path_length_distribution(suite,
                                                             title=f"{scenario_name} - Path Length Distribution",
                                                             filename=f"{safe_name}_path_lengths.png")
    return outputs


def generate_report(outputs: Dict[str, str], metrics_dict: Dict, scenario_name: str) -> str:
    lines = [
        f"# NeSy-MBST Pipeline Results: {scenario_name}",
        "",
        "## Overview",
        f"- States: {metrics_dict.get('mc_states', 'N/A')}",
        f"- Transitions: {metrics_dict.get('mc_transitions', 'N/A')}",
        f"- Test Sequences Generated: {metrics_dict.get('coverage', {}).get('num_sequences', 'N/A')}",
        f"- State Coverage: {metrics_dict.get('coverage', {}).get('state_coverage', 0):.2%}",
        f"- Transition Coverage: {metrics_dict.get('coverage', {}).get('transition_coverage', 0):.2%}",
        "",
        "## F1 Scores",
    ]
    f1 = metrics_dict.get("f1_scores", {})
    for k, v in f1.items():
        lines.append(f"- {k}: {v:.4f}")
    lines.extend([
        "",
        "## Statistical Validation",
        f"- Jensen-Shannon Divergence (marginals): {metrics_dict.get('js_divergence', 'N/A')}",
        f"- Normalized Frobenius Distance: {metrics_dict.get('frobenius_distance', 'N/A')}",
        "",
        "## Visualizations",
    ])
    for name, path in outputs.items():
        lines.append(f"![{name}]({path})")
    lines.append("")
    report_path = os.path.join(OUTPUT_DIR, f"{scenario_name.lower().replace(' ', '_')}_report.md")
    with open(report_path, "w") as f:
        f.write("\n".join(lines))
    return report_path
