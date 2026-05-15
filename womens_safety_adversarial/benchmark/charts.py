"""
charts.py — Publication figures for the ZIDR benchmark paper.

Outputs (all to results/):
  fig1_zidr_heatmap.png      — ZIDR matrix + system definitions table
  fig2_score_comparison.png  — Overall robustness by system (all / urban-rural)
  fig3_threat_model.png      — Threat model architecture diagram

Run: python charts.py
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap

# ── Paths ────────────────────────────────────────────────────────────────────
BASE       = os.path.dirname(os.path.abspath(__file__))
RESULTS    = os.path.join(BASE, "results")
MATRIX_CSV = os.path.join(RESULTS, "zidr_matrix.csv")
BENCH_CSV  = os.path.join(RESULTS, "benchmark_results.csv")
OUT_FIG1   = os.path.join(RESULTS, "fig1_zidr_heatmap.png")
OUT_FIG2   = os.path.join(RESULTS, "fig2_score_comparison.png")
OUT_FIG3   = os.path.join(RESULTS, "fig3_threat_model.png")

# ── Constants ────────────────────────────────────────────────────────────────
SCENARIO_SHORT = {
    "U-01": "U-01  Mumbai Local Train",
    "U-02": "U-02  App-Cab, Night Route",
    "U-03": "U-03  Workplace Authority",
    "U-04": "U-04  Street Market",
    "U-05": "U-05  Bus Stop, Exhaustion",
    "U-06": "U-06  Campus Acquaintance",
    "U-07": "U-07  Social Venue, Noise",
    "U-08": "U-08  Public Toilet, Device",
    "U-09": "U-09  Transit Confinement",
    "R-01": "R-01  Agricultural Field",
    "R-02": "R-02  Village Pathway",
    "R-03": "R-03  Isolated Road Vehicle",
    "R-04": "R-04  Village Community",
    "R-05": "R-05  Employer Coercion",
}

CRITICALITY = {
    "U-01": 5, "U-02": 5, "U-03": 4, "U-04": 3, "U-05": 4,
    "U-06": 3, "U-07": 4, "U-08": 5, "U-09": 5,
    "R-01": 5, "R-02": 4, "R-03": 5, "R-04": 4, "R-05": 4,
}

SCENARIO_ORDER = [
    "U-01", "U-02", "U-03", "U-04", "U-05",
    "U-06", "U-07", "U-08", "U-09",
    "R-01", "R-02", "R-03", "R-04", "R-05",
]

SYSTEM_COLS  = ["Baseline (A)", "Compliant (B)", "Best Practice (C)", "Rural-Opt (D)"]
SYSTEM_SHORT = ["A: Baseline", "B: Compliant", "C: Best Practice", "D: Rural-Opt"]
SYSTEM_CODES = ["A", "B", "C", "D"]
SYS_COLORS   = ["#ef5350", "#ff8a65", "#66bb6a", "#42a5f5"]


# ── Figure 1: ZIDR Heatmap ───────────────────────────────────────────────────
def fig1_heatmap(matrix_df: pd.DataFrame) -> None:
    df   = matrix_df.set_index("scenario_id")[SYSTEM_COLS].reindex(SCENARIO_ORDER)
    data = df.values.astype(float)

    # Red (0) → yellow (0.5) → green (1)
    cmap = LinearSegmentedColormap.from_list(
        "zidr",
        [(0.00, "#c62828"), (0.20, "#ef5350"),
         (0.40, "#fbc02d"), (0.60, "#aed581"),
         (0.80, "#66bb6a"), (1.00, "#2e7d32")],
    )

    fig, ax = plt.subplots(figsize=(9, 8))

    # ── Heatmap ──────────────────────────────────────────────────────────────
    im = ax.imshow(data, cmap=cmap, vmin=0.0, vmax=1.0, aspect="auto")

    for i, sid in enumerate(SCENARIO_ORDER):
        for j in range(4):
            val       = data[i, j]
            txt_color = "white" if (val <= 0.30 or val >= 0.82) else "#212121"
            ax.text(j, i, f"{val:.2f}",
                    ha="center", va="center",
                    fontsize=9.5, color=txt_color, fontweight="bold")

    # R-03 — thick red border (universal zero-day)
    r03 = SCENARIO_ORDER.index("R-03")
    for j in range(4):
        ax.add_patch(plt.Rectangle(
            (j - 0.49, r03 - 0.49), 0.98, 0.98,
            linewidth=2.8, edgecolor="#b71c1c", facecolor="none", zorder=5
        ))

    # R-02, R-04 — dashed orange (ZIDR high but sociotechnical risk)
    for sid in ("R-02", "R-04"):
        idx = SCENARIO_ORDER.index(sid)
        for j in range(4):
            ax.add_patch(plt.Rectangle(
                (j - 0.49, idx - 0.49), 0.98, 0.98,
                linewidth=1.8, edgecolor="#e65100",
                facecolor="none", linestyle="--", zorder=5
            ))

    # Urban/rural separator
    ax.axhline(y=8.5, color="white", linewidth=2.5, zorder=4)

    # X axis
    ax.set_xticks(range(4))
    ax.set_xticklabels(SYSTEM_SHORT, fontsize=9.5, fontweight="bold")
    ax.xaxis.set_tick_params(length=0)

    # Y axis
    ax.set_yticks(range(len(SCENARIO_ORDER)))
    ax.set_yticklabels([SCENARIO_SHORT[s] for s in SCENARIO_ORDER], fontsize=8.5)
    ax.yaxis.set_tick_params(length=0)

    fig.canvas.draw()
    for tick, sid in zip(ax.get_yticklabels(), SCENARIO_ORDER):
        tick.set_color("#1565c0" if sid.startswith("U") else "#2e7d32")

    # Right axis — criticality
    ax2 = ax.twinx()
    ax2.set_ylim(ax.get_ylim())
    ax2.set_yticks(range(len(SCENARIO_ORDER)))
    ax2.set_yticklabels(
        [f"C{CRITICALITY[s]}" for s in SCENARIO_ORDER],
        fontsize=8, color="#757575"
    )
    ax2.yaxis.set_tick_params(length=0)
    ax2.set_ylabel("Criticality", fontsize=8.5, color="#757575", labelpad=6)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_color("#e0e0e0")

    # Context block labels
    ax.annotate("URBAN", xy=(-0.5, 4), xycoords="data",
                fontsize=8, color="#1565c0", fontweight="bold",
                ha="center", va="center", rotation=90,
                xytext=(-1.0, 4), textcoords="data", annotation_clip=False)
    ax.annotate("RURAL", xy=(-0.5, 11.5), xycoords="data",
                fontsize=8, color="#2e7d32", fontweight="bold",
                ha="center", va="center", rotation=90,
                xytext=(-1.0, 11.5), textcoords="data", annotation_clip=False)

    # Colorbar
    cbar = plt.colorbar(im, ax=ax, fraction=0.025, pad=0.12)
    cbar.set_label("ZIDR Score", fontsize=9)
    cbar.set_ticks([0, 0.25, 0.50, 0.75, 1.0])
    cbar.ax.tick_params(labelsize=8)

    # Legend
    patch_zeroday = mpatches.Patch(
        facecolor="none", edgecolor="#b71c1c", linewidth=2.2,
        label="Red border: universal zero-day (R-03) — no passive detection path"
    )
    patch_warn = mpatches.Patch(
        facecolor="none", edgecolor="#e65100", linewidth=1.6, linestyle="--",
        label="Orange dashed: high ZIDR but sociotechnical suppression risk persists"
    )
    ax.legend(handles=[patch_zeroday, patch_warn],
              loc="upper right", bbox_to_anchor=(1.0, -0.03),
              fontsize=8, framealpha=0.9, ncol=1)

    ax.set_title(
        "ZIDR Benchmark Results Across 14 Adversarial Scenarios",
        fontsize=11, pad=12, fontweight="bold"
    )

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()
    fig.savefig(OUT_FIG1, dpi=300, bbox_inches="tight")
    print(f"Saved: {OUT_FIG1}")
    plt.close(fig)


# ── Figure 2: Overall Robustness Score Comparison ────────────────────────────
def fig2_comparison(bench_df: pd.DataFrame) -> None:
    bench_df = bench_df.copy()
    bench_df["context"] = bench_df["scenario_id"].apply(
        lambda x: "Urban" if x.startswith("U") else "Rural"
    )

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))
    rng = np.random.default_rng(42)

    # ── Panel (a): Mean overall score, all 14 scenarios ──────────────────────
    ax = axes[0]
    means = [bench_df[bench_df["system"] == s]["overall"].mean() for s in SYSTEM_CODES]
    stds  = [bench_df[bench_df["system"] == s]["overall"].std()  for s in SYSTEM_CODES]

    x_pos = np.arange(4)
    bars = ax.bar(x_pos, means, color=SYS_COLORS, alpha=0.82,
                  edgecolor="white", linewidth=0.8, width=0.55, zorder=2)
    ax.errorbar(x_pos, means, yerr=stds,
                fmt="none", color="#424242", capsize=5, linewidth=1.4, zorder=3)

    # Scatter individual scenario scores
    for i, s in enumerate(SYSTEM_CODES):
        vals   = bench_df[bench_df["system"] == s]["overall"].values
        jitter = rng.uniform(-0.14, 0.14, len(vals))
        ax.scatter(i + jitter, vals,
                   color=SYS_COLORS[i], alpha=0.40, s=24, zorder=4)

    ax.axhline(0.5, color="#9e9e9e", linestyle="--", linewidth=1.0, alpha=0.8, zorder=1)
    ax.text(3.65, 0.505, "0.5", fontsize=7.5, color="#9e9e9e", va="bottom")

    for bar, val in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.018,
                f"{val:.2f}", ha="center", va="bottom",
                fontsize=9.5, fontweight="bold", color="#212121")

    # A→B and B→C gap annotations
    for i, (label, color) in enumerate(
        [(f"+{means[1]-means[0]:.2f}", "#757575"),
         (f"+{means[2]-means[1]:.2f}", "#388e3c")]
    ):
        x1, x2 = i, i + 1
        y_top = max(means[x1], means[x2]) + 0.07
        ax.annotate(
            "", xy=(x2, means[x2] + 0.01), xytext=(x1, means[x1] + 0.01),
            arrowprops=dict(arrowstyle="<->", color=color, lw=1.3)
        )
        ax.text((x1 + x2) / 2, y_top, label,
                ha="center", fontsize=8.5, color=color, fontweight="bold")

    # Error bar explanation
    ax.text(0.02, 0.02, "Error bars: ±1 SD across 14 scenarios",
            transform=ax.transAxes, fontsize=7.5, color="#757575", va="bottom")

    ax.set_xticks(x_pos)
    ax.set_xticklabels(SYSTEM_SHORT, fontsize=9, rotation=12)
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("Mean Overall Robustness Score", fontsize=10)
    ax.set_title("(a)  All Scenarios  (n = 14)", fontsize=10, pad=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, alpha=0.25, zorder=0)
    ax.set_axisbelow(True)

    # ── Panel (b): Urban vs Rural split ──────────────────────────────────────
    ax = axes[1]
    ctx_colors = {"Urban": "#1565c0", "Rural": "#2e7d32"}
    bw     = 0.32
    x_pos2 = np.arange(4)

    for ci, ctx in enumerate(("Urban", "Rural")):
        ctx_df  = bench_df[bench_df["context"] == ctx]
        n_scen  = ctx_df["scenario_id"].nunique()
        c_means = [ctx_df[ctx_df["system"] == s]["overall"].mean() for s in SYSTEM_CODES]
        c_stds  = [ctx_df[ctx_df["system"] == s]["overall"].std()  for s in SYSTEM_CODES]
        offset  = (ci - 0.5) * bw * 2.2
        ax.bar(x_pos2 + offset, c_means, width=bw * 1.85,
               color=ctx_colors[ctx], alpha=0.78 if ctx == "Urban" else 0.70,
               label=f"{ctx} (n = {n_scen})", edgecolor="white", linewidth=0.6, zorder=2)
        ax.errorbar(x_pos2 + offset, c_means, yerr=c_stds,
                    fmt="none", color="#424242", capsize=4, linewidth=1.1, zorder=3)
        for xi, val in zip(x_pos2, c_means):
            ax.text(xi + offset, val + 0.015, f"{val:.2f}",
                    ha="center", va="bottom", fontsize=7.5,
                    color=ctx_colors[ctx], fontweight="bold")

    ax.axhline(0.5, color="#9e9e9e", linestyle="--", linewidth=1.0, alpha=0.8, zorder=1)

    ax.text(0.02, 0.02, "Error bars: ±1 SD",
            transform=ax.transAxes, fontsize=7.5, color="#757575", va="bottom")

    ax.set_xticks(x_pos2)
    ax.set_xticklabels(SYSTEM_SHORT, fontsize=9, rotation=12)
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("Mean Overall Robustness Score", fontsize=10)
    ax.set_title("(b)  Urban vs Rural Split", fontsize=10, pad=8)
    ax.legend(fontsize=9.5, framealpha=0.88, loc="upper left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, alpha=0.25, zorder=0)
    ax.set_axisbelow(True)

    fig.suptitle(
        "Overall Robustness Score by Safety System",
        fontsize=11.5, fontweight="bold", y=1.02
    )

    plt.tight_layout()
    fig.savefig(OUT_FIG2, dpi=300, bbox_inches="tight")
    print(f"Saved: {OUT_FIG2}")
    plt.close(fig)


# ── Figure 3: Threat Model Architecture ──────────────────────────────────────
def fig3_threat_model() -> None:
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8.5)
    ax.axis("off")

    def box(x, y, w, h, text, fc, ec, fs=9, bold=False, fc_text="black"):
        ax.add_patch(FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.12",
            facecolor=fc, edgecolor=ec, linewidth=1.6, zorder=2
        ))
        ax.text(x + w / 2, y + h / 2, text,
                ha="center", va="center", fontsize=fs,
                fontweight="bold" if bold else "normal",
                color=fc_text, multialignment="center", zorder=3,
                linespacing=1.4)

    def arrow(x1, y1, x2, y2, color="#424242", lw=1.5):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(
                        arrowstyle="-|>", color=color,
                        lw=lw, mutation_scale=14
                    ), zorder=4)

    def label(x, y, text, color="#616161", fs=8):
        ax.text(x, y, text, ha="center", va="center",
                fontsize=fs, color=color, style="italic")

    # ── Zone 1: ADVERSARY ────────────────────────────────────────────────────
    box(4.5, 7.2, 4.0, 1.0,
        "ADVERSARY\nL0–L5 Capability Spectrum",
        "#fce4ec", "#c62828", fs=10, bold=True)

    # ── Zone 2: Attack Methods ───────────────────────────────────────────────
    for (x, txt) in [(0.4, "SUPPRESS\ndisable sensor layer"),
                     (4.5, "INTERCEPT\nblock signal path"),
                     (8.6, "CORRUPT\ninject noise / spoof")]:
        box(x, 5.6, 3.6, 0.9, txt, "#fff3e0", "#e65100", fs=8.5)

    # Arrows: ADVERSARY → each attack method
    for cx in [2.2, 6.3, 10.4]:
        arrow(6.5, 7.2, cx, 6.5, color="#c62828", lw=1.2)

    label(6.5, 7.0, "executes", "#9e9e9e", fs=7.5)

    # ── Zone 3: Passive Detection Layers ─────────────────────────────────────
    layers = [
        ("Vision\n(camera / optical)", "#e3f2fd", "#1565c0"),
        ("Audio\n(mic / glass-break)", "#e8f5e9", "#2e7d32"),
        ("NLP /\nLanguage Model",       "#f3e5f5", "#7b1fa2"),
        ("GPS /\nLocation",             "#fff8e1", "#f57f17"),
        ("Comm /\nNetwork",             "#fbe9e7", "#bf360c"),
    ]
    lw_box = 2.2
    lx_start = 0.5
    for i, (txt, fc, ec) in enumerate(layers):
        box(lx_start + i * 2.4, 4.0, lw_box, 1.1, txt, fc, ec, fs=8)

    # Arrow: attack methods → layers (one representative arrow per method)
    for cx in [2.2, 6.3, 10.4]:
        arrow(cx, 5.6, cx, 5.1, color="#e65100", lw=1.1)

    label(6.5, 4.8, "degrades", "#9e9e9e", fs=7.5)

    # ── Zone 4: ZIDR Computation ──────────────────────────────────────────────
    # Arrow: layers → ZIDR
    arrow(6.5, 4.0, 6.5, 3.45, color="#424242")
    label(6.9, 3.72, "scores", "#9e9e9e", fs=7.5)

    box(1.0, 2.65, 11.0, 0.75,
        "ZIDR  =  Σ ( layer_scoreᵢ  ×  weightᵢ  ×  degradationᵢ )     "
        "[Zone Integrity Detection Rate]",
        "#e8eaf6", "#3949ab", fs=9.5, bold=False)

    # ── Zone 5: Decision fork ─────────────────────────────────────────────────
    arrow(6.5, 2.65, 6.5, 2.1, color="#424242")

    # Decision diamond
    dx, dy = 6.5, 1.65
    diamond = plt.Polygon(
        [[dx, dy + 0.44], [dx + 1.0, dy], [dx, dy - 0.44], [dx - 1.0, dy]],
        facecolor="#fff9c4", edgecolor="#f9a825", linewidth=1.8, zorder=2
    )
    ax.add_patch(diamond)
    ax.text(dx, dy, "ZIDR ≥ τ ?",
            ha="center", va="center", fontsize=9.5, fontweight="bold", zorder=3)

    # Left branch: ZIDR >= tau → ALERT
    arrow(dx - 1.0, dy, 3.0, dy, color="#2e7d32", lw=1.4)
    arrow(3.0, dy, 3.0, 0.9, color="#2e7d32", lw=1.4)
    label(4.7, dy + 0.18, "ZIDR ≥ τ", "#2e7d32", fs=8.5)
    box(0.5, 0.2, 5.0, 0.65, "ALERT SENT", "#e8f5e9", "#2e7d32", fs=10, bold=True, fc_text="#1b5e20")

    # Right branch: ZIDR < tau → failure
    arrow(dx + 1.0, dy, 10.0, dy, color="#c62828", lw=1.4)
    arrow(10.0, dy, 10.0, 0.9, color="#c62828", lw=1.4)
    label(8.3, dy + 0.18, "ZIDR < τ", "#c62828", fs=8.5)
    box(6.0, 0.2, 6.5, 0.65, "DETECTION WINDOW MISSED  →  FAILURE POINT",
        "#ffebee", "#c62828", fs=9, bold=True, fc_text="#b71c1c")

    # ── Title and caption ─────────────────────────────────────────────────────
    ax.set_title(
        "ZIDR Threat Model Architecture\n"
        "Adversary capability degrades passive detection layers; "
        "ZIDR below threshold creates an undetected high-risk window.",
        fontsize=11, fontweight="bold", pad=10
    )

    fig.savefig(OUT_FIG3, dpi=300, bbox_inches="tight")
    print(f"Saved: {OUT_FIG3}")
    plt.close(fig)


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    matrix_df = pd.read_csv(MATRIX_CSV)
    bench_df  = pd.read_csv(BENCH_CSV)

    print("Building Figure 1: ZIDR Heatmap + System Definitions...")
    fig1_heatmap(matrix_df)

    print("Building Figure 2: Score Comparison...")
    fig2_comparison(bench_df)

    print("Building Figure 3: Threat Model Architecture...")
    fig3_threat_model()

    print("\nDone.")
    print(f"  fig1: {OUT_FIG1}")
    print(f"  fig2: {OUT_FIG2}")
    print(f"  fig3: {OUT_FIG3}")
