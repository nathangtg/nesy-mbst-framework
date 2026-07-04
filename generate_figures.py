#!/usr/bin/env python3
"""
NeSy-MBST — Publication-quality figure generator
Produces PNG + PDF figures saved to output/figures/
Uses Matplotlib + Seaborn only (no Manim dependency needed for static plots).

Figures generated:
  fig1_f1_comparison.pdf     — Grouped bar chart: F1 across all six strategies
  fig2_ablation_av.pdf       — Stacked contribution chart: ablation on AV benchmark
  fig3_jsd_frobenius.pdf     — Dual-axis bar: JSD + Frobenius across ablation conditions
  fig4_coverage_ablation.pdf — Coverage improvement across ablation conditions
  fig5_radar.pdf             — Radar / spider chart: NeSy-MBST vs best baselines
"""
from __future__ import annotations

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import seaborn as sns

OUT = os.path.join(os.path.dirname(__file__), "output", "figures")
os.makedirs(OUT, exist_ok=True)

sns.set_theme(style="whitegrid", font_scale=1.05)
plt.rcParams.update({
    "font.family": "serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": 150,
})

PALETTE = {
    "blue":   "#2C6FAC",
    "green":  "#2E8B57",
    "orange": "#D4742A",
    "red":    "#B03A2E",
    "grey":   "#8E8E8E",
    "teal":   "#1A7A7A",
    "gold":   "#C8962A",
}

# Figure 1 — F1 Comparison across six prompting strategies
def fig1_f1_comparison():
    strategies = [
        "Single-Prompt\n(GPT-4o)",
        "Structure-Driven\nSMF (GPT-4o)",
        "Event-Driven\nSMF (GPT-4o)",
        "Hybrid SMF\n(GPT-4o)",
        "Single-Prompt\n(Claude 3.5)",
        "NeSy-MBST\n(Ours)",
    ]
    state_f1  = [0.80,   0.7377, 0.6584, 0.8582, 0.90,   0.9450]
    trans_f1  = [0.54,   0.6050, 0.3690, 0.6491, 0.75,   0.8950]
    system_f1 = [0.5431, 0.6260, 0.3735, 0.6559, 0.7950, 0.9125]

    x = np.arange(len(strategies))
    width = 0.26

    fig, ax = plt.subplots(figsize=(11, 5))

    bars1 = ax.bar(x - width, state_f1,  width, label="State F1",      color=PALETTE["blue"],   alpha=0.88, zorder=3)
    bars2 = ax.bar(x,         trans_f1,  width, label="Transition F1",  color=PALETTE["orange"], alpha=0.88, zorder=3)
    bars3 = ax.bar(x + width, system_f1, width, label="System F1",      color=PALETTE["green"],  alpha=0.88, zorder=3)

    # annotate NeSy-MBST (last group) with values
    for bar in [bars1[-1], bars2[-1], bars3[-1]]:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.012,
                f"{bar.get_height():.3f}", ha="center", va="bottom",
                fontsize=8, fontweight="bold", color="#222222")

    # 0.90 safety threshold line
    ax.axhline(0.90, color=PALETTE["red"], linewidth=1.2, linestyle="--", zorder=2)
    ax.text(5.62, 0.905, "Safety threshold (0.90)", fontsize=8,
            color=PALETTE["red"], va="bottom", ha="right")

    ax.set_xticks(x)
    ax.set_xticklabels(strategies, fontsize=9)
    ax.set_ylabel("F1 Score", fontsize=11)
    ax.set_ylim(0, 1.08)
    ax.set_title("State, Transition, and System F1 Scores Across Prompting Strategies",
                 fontsize=12, fontweight="bold", pad=12)
    ax.legend(loc="upper left", fontsize=9, framealpha=0.9)
    ax.yaxis.grid(True, linewidth=0.5, alpha=0.6)

    # Highlight NeSy-MBST column
    ax.axvspan(4.55, 5.45, color=PALETTE["teal"], alpha=0.06, zorder=1)

    fig.tight_layout()
    _save(fig, "fig1_f1_comparison")


# Figure 2 — Ablation: System F1 gains on AV benchmark
def fig2_ablation_f1():
    conditions  = ["A\nPure-Neural", "B\n+Symbolic\nLoop", "C\n+Convex\nOptimizer", "D\nFull\nNeSy-MBST"]
    state_f1    = [1.0000, 1.0000, 1.0000, 1.0000]
    trans_f1    = [0.7826, 0.9630, 0.9630, 0.9630]
    system_f1   = [0.9036, 0.9818, 0.9818, 0.9818]

    x = np.arange(len(conditions))
    width = 0.26

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(x - width, state_f1,  width, label="State F1",     color=PALETTE["blue"],   alpha=0.88, zorder=3)
    ax.bar(x,         trans_f1,  width, label="Transition F1", color=PALETTE["orange"], alpha=0.88, zorder=3)
    ax.bar(x + width, system_f1, width, label="System F1",     color=PALETTE["green"],  alpha=0.88, zorder=3)

    # annotate delta on condition B
    ax.annotate("",
        xy=(1, trans_f1[1] + 0.01), xytext=(0, trans_f1[0] + 0.01),
        arrowprops=dict(arrowstyle="->", color=PALETTE["red"], lw=1.5))
    ax.text(0.5, max(trans_f1[0], trans_f1[1]) + 0.025,
            f"ΔTr.F1 = +{trans_f1[1]-trans_f1[0]:.3f}",
            ha="center", fontsize=8.5, color=PALETTE["red"])

    ax.set_xticks(x)
    ax.set_xticklabels(conditions, fontsize=9.5)
    ax.set_ylabel("F1 Score", fontsize=11)
    ax.set_ylim(0.65, 1.12)
    ax.set_title("Ablation Study: F1 Scores on AV CPS Benchmark\n(Each condition adds one NeSy-MBST component)",
                 fontsize=11, fontweight="bold", pad=10)
    ax.legend(loc="lower right", fontsize=9, framealpha=0.9)
    ax.yaxis.grid(True, linewidth=0.5, alpha=0.6)

    fig.tight_layout()
    _save(fig, "fig2_ablation_f1")


# Figure 3 — Ablation: JSD and Frobenius distance
def fig3_divergence():
    conditions = ["A — Pure-Neural", "B — +Symbolic Loop",
                  "C — +Convex Opt.", "D — Full NeSy-MBST"]
    jsd   = [0.1568, 0.0120, 0.0120, 0.0118]
    frob  = [0.1627, 0.0843, 0.0843, 0.0840]

    x = np.arange(len(conditions))
    width = 0.35

    fig, ax1 = plt.subplots(figsize=(9, 5))
    ax2 = ax1.twinx()

    b1 = ax1.bar(x - width/2, jsd,  width, label="JSD (marginals)",        color=PALETTE["blue"],   alpha=0.85, zorder=3)
    b2 = ax2.bar(x + width/2, frob, width, label="Norm. Frobenius Distance", color=PALETTE["orange"], alpha=0.85, zorder=3)

    # value labels
    for bar in b1:
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.003,
                 f"{bar.get_height():.4f}", ha="center", va="bottom", fontsize=8.5,
                 color=PALETTE["blue"])
    for bar in b2:
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.003,
                 f"{bar.get_height():.4f}", ha="center", va="bottom", fontsize=8.5,
                 color=PALETTE["orange"])

    ax1.set_ylabel("Jensen-Shannon Divergence", color=PALETTE["blue"], fontsize=10)
    ax2.set_ylabel("Normalized Frobenius Distance", color=PALETTE["orange"], fontsize=10)
    ax1.tick_params(axis="y", labelcolor=PALETTE["blue"])
    ax2.tick_params(axis="y", labelcolor=PALETTE["orange"])

    ax1.set_xticks(x)
    ax1.set_xticklabels(conditions, fontsize=9.5)
    ax1.set_ylim(0, 0.22)
    ax2.set_ylim(0, 0.22)
    ax1.set_title("Probabilistic Fidelity: JSD and Frobenius Distance by Ablation Condition\n"
                  "(lower is better — both axes on same scale for direct comparison)",
                  fontsize=11, fontweight="bold", pad=10)

    lines = [mpatches.Patch(color=PALETTE["blue"],   label="JSD (marginals)"),
             mpatches.Patch(color=PALETTE["orange"], label="Norm. Frobenius")]
    ax1.legend(handles=lines, loc="upper right", fontsize=9, framealpha=0.9)
    ax1.yaxis.grid(True, linewidth=0.5, alpha=0.5, zorder=0)

    fig.tight_layout()
    _save(fig, "fig3_divergence")


# Figure 4 — Coverage improvement across ablation conditions
def fig4_coverage():
    conditions    = ["A\nPure-Neural", "B\n+Symbolic\nLoop", "C\n+Convex\nOpt.", "D\nFull\nNeSy-MBST"]
    state_cov     = [55.6, 88.9, 88.9, 88.9]
    trans_cov     = [50.0, 85.7, 85.7, 85.7]

    x = np.arange(len(conditions))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(x - width/2, state_cov, width, label="State Coverage (%)",      color=PALETTE["teal"],  alpha=0.88, zorder=3)
    ax.bar(x + width/2, trans_cov, width, label="Transition Coverage (%)",  color=PALETTE["gold"],  alpha=0.88, zorder=3)

    # draw improvement bracket A → B
    y_top = 94
    ax.annotate("",
        xy=(1 - width/2, state_cov[1] + 1.5), xytext=(0 - width/2, state_cov[0] + 1.5),
        arrowprops=dict(arrowstyle="-|>", color=PALETTE["green"], lw=1.8))
    ax.text(0.5, y_top,
            f"+{state_cov[1]-state_cov[0]:.1f} pp\n(state)",
            ha="center", fontsize=8, color=PALETTE["green"])

    ax.set_xticks(x)
    ax.set_xticklabels(conditions, fontsize=10)
    ax.set_ylabel("Coverage (%)", fontsize=11)
    ax.set_ylim(0, 108)
    ax.set_title("Test-Suite Coverage by Ablation Condition — AV CPS Benchmark",
                 fontsize=11, fontweight="bold", pad=10)
    ax.legend(loc="lower right", fontsize=9, framealpha=0.9)
    ax.yaxis.grid(True, linewidth=0.5, alpha=0.6)

    fig.tight_layout()
    _save(fig, "fig4_coverage")


# Figure 5 — Radar chart: NeSy-MBST vs baselines
def fig5_radar():
    categories = ["State F1", "Transition F1", "System F1",
                  "State Cov.", "Trans. Cov.", "Prob. Fidelity\n(1 − JSD)"]

    # scale all metrics to [0, 1]
    systems = {
        "GPT-4o Hybrid SMF":       [0.8582, 0.6491, 0.6559, 0.556, 0.500, 1 - 0.20],
        "Claude 3.5 Single-Prompt":[0.90,   0.75,   0.7950, 0.667, 0.600, 1 - 0.18],
        "NeSy-MBST (Ours)":        [0.9450, 0.8950, 0.9125, 0.889, 0.857, 1 - 0.0118],
    }
    colors = [PALETTE["orange"], PALETTE["blue"], PALETTE["green"]]

    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]  # close the polygon

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"polar": True})

    for (name, values), color in zip(systems.items(), colors):
        vals = values + values[:1]
        ax.plot(angles, vals, linewidth=2, color=color, label=name)
        ax.fill(angles, vals, alpha=0.10, color=color)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.50, 0.75, 1.00])
    ax.set_yticklabels(["0.25", "0.50", "0.75", "1.00"], fontsize=8)
    ax.yaxis.grid(True, linewidth=0.6, alpha=0.5)
    ax.xaxis.grid(True, linewidth=0.6, alpha=0.4)

    ax.set_title("Multi-Dimensional Comparison: NeSy-MBST vs Baselines",
                 fontsize=12, fontweight="bold", pad=20)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.18),
              ncol=1, fontsize=9.5, framealpha=0.9)

    fig.tight_layout()
    _save(fig, "fig5_radar")


# Helper
def _save(fig: plt.Figure, name: str) -> None:
    for ext in ("pdf", "png"):
        path = os.path.join(OUT, f"{name}.{ext}")
        fig.savefig(path, bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"  Saved: {name}.pdf / .png")


# Entry point
def main():
    print("Generating NeSy-MBST publication figures...")
    fig1_f1_comparison()
    fig2_ablation_f1()
    fig3_divergence()
    fig4_coverage()
    fig5_radar()
    print(f"\nAll figures saved to: {OUT}")


if __name__ == "__main__":
    main()
