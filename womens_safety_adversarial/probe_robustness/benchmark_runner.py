"""
benchmark_runner.py — Controlled Benchmark: 4 System Profiles × 14 Scenarios

Runs the probe tool evaluation for every (profile, scenario) pair and outputs:
  1. Terminal: rich table matrix (ZIDR × scenarios × systems)
  2. Terminal: per-scenario governance gap count
  3. CSV: results/benchmark_results.csv (all scores)
  4. CSV: results/zidr_matrix.csv (ZIDR only — for paper Table 1)

Usage:
    python benchmark_runner.py
    python benchmark_runner.py --output-dir results/

Requires: pyyaml rich  (pip install pyyaml rich)
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

# probe.py handles the UTF-8 redirect for Windows at import time — do not duplicate
from probe import load_profile, run_evaluation

BASE_DIR = Path(__file__).parent
WEIGHTS_DEFAULT = BASE_DIR / "weights" / "default_weights.yaml"

# ── Profile registry ──────────────────────────────────────────────────────────

PROFILES: list[tuple[str, str]] = [
    ("A", str(BASE_DIR / "profiles" / "profile_baseline.yaml")),
    ("B", str(BASE_DIR / "profiles" / "profile_compliant.yaml")),
    ("C", str(BASE_DIR / "profiles" / "profile_best_practice.yaml")),
    ("D", str(BASE_DIR / "profiles" / "profile_rural_optimised.yaml")),
]

PROFILE_LABELS: dict[str, str] = {
    "A": "Baseline (A)",
    "B": "Compliant (B)",
    "C": "Best Practice (C)",
    "D": "Rural-Opt (D)",
}

# ── Risk colour ───────────────────────────────────────────────────────────────

def risk_color(score: float) -> str:
    if score >= 0.8:
        return "green"
    elif score >= 0.6:
        return "yellow"
    elif score >= 0.4:
        return "red"
    else:
        return "bold red"


def risk_icon(score: float) -> str:
    if score >= 0.8:
        return "✓"
    elif score >= 0.6:
        return "~"
    else:
        return "✗"


# ── Run benchmark ─────────────────────────────────────────────────────────────

def run_benchmark(weights_path: Path) -> list[dict]:
    """
    Returns a list of result dicts, one per (profile, scenario) pair.
    """
    from scenarios import load_scenario, list_scenarios

    scenarios = list_scenarios()
    results: list[dict] = []

    for sys_label, profile_path in PROFILES:
        profile = load_profile(Path(profile_path))
        for sid, sname in scenarios:
            scenario = load_scenario(sid)
            eval_result = run_evaluation(profile, scenario, weights_path)
            zidr = eval_result["results"].get("zidr", {}).get("score", 0.0)
            overall = eval_result["overall"]
            n_flags = len(eval_result["governance_flags"])
            results.append(
                {
                    "system": sys_label,
                    "system_name": profile.name,
                    "scenario_id": sid,
                    "scenario_name": sname,
                    "zidr": zidr,
                    "overall": overall,
                    "risk_level": eval_result["risk_level"],
                    "governance_flags": n_flags,
                    "weight_category": eval_result["weight_category"],
                }
            )

    return results


# ── Display: ZIDR matrix table ────────────────────────────────────────────────

def display_zidr_matrix(results: list[dict]) -> None:
    from rich.console import Console
    from rich.table import Table
    from rich.text import Text

    console = Console()
    scenario_ids = sorted(
        {r["scenario_id"] for r in results},
        key=lambda s: (s[0], int(s[2:])),
    )
    sys_labels = [p[0] for p in PROFILES]

    # Index results
    index: dict[tuple[str, str], dict] = {
        (r["system"], r["scenario_id"]): r for r in results
    }

    table = Table(
        title="ZIDR Matrix — Scenarios × System Archetypes",
        show_header=True,
        header_style="bold",
        border_style="dim",
    )

    table.add_column("Scenario", style="bold", width=10)
    table.add_column("Name", width=28)
    for sl in sys_labels:
        table.add_column(PROFILE_LABELS[sl], justify="center", width=14)
    table.add_column("Avg ZIDR", justify="center", width=10)

    # Group by geography
    urban_ids = [s for s in scenario_ids if s.startswith("U")]
    rural_ids = [s for s in scenario_ids if s.startswith("R")]

    def add_rows(ids: list[str]) -> None:
        for sid in ids:
            row_results = [index[(sl, sid)] for sl in sys_labels]
            zidr_scores = [r["zidr"] for r in row_results]
            avg_zidr = sum(zidr_scores) / len(zidr_scores)

            cells: list[Text] = []
            for r in row_results:
                z = r["zidr"]
                t = Text(f"{z:.2f} {risk_icon(z)}", style=risk_color(z))
                cells.append(t)

            name = row_results[0]["scenario_name"]
            if len(name) > 26:
                name = name[:24] + "…"

            avg_text = Text(f"{avg_zidr:.2f}", style=risk_color(avg_zidr))
            table.add_row(sid, name, *cells, avg_text)

    console.print()
    console.print("URBAN SCENARIOS", style="bold underline")
    add_rows(urban_ids)
    console.print()
    console.print("RURAL SCENARIOS", style="bold underline")
    add_rows(rural_ids)
    console.print(table)

    console.print()
    console.print("Score key: ✓ LOW RISK (≥0.8)  ~ MODERATE (0.6–0.8)  ✗ HIGH RISK / CRITICAL (<0.6)", style="dim")
    console.print()


# ── Display: overall score table ──────────────────────────────────────────────

def display_overall_matrix(results: list[dict]) -> None:
    from rich.console import Console
    from rich.table import Table
    from rich.text import Text

    console = Console()
    scenario_ids = sorted(
        {r["scenario_id"] for r in results},
        key=lambda s: (s[0], int(s[2:])),
    )
    sys_labels = [p[0] for p in PROFILES]
    index = {(r["system"], r["scenario_id"]): r for r in results}

    table = Table(
        title="Overall Score Matrix — Weighted Across Dimensions",
        show_header=True,
        header_style="bold",
        border_style="dim",
    )

    table.add_column("Scenario", style="bold", width=10)
    for sl in sys_labels:
        table.add_column(PROFILE_LABELS[sl], justify="center", width=14)
    table.add_column("Gov Flags (avg)", justify="center", width=16)

    for sid in scenario_ids:
        row_results = [index[(sl, sid)] for sl in sys_labels]
        cells: list[Text] = []
        for r in row_results:
            o = r["overall"]
            t = Text(f"{o:.2f}", style=risk_color(o))
            cells.append(t)
        avg_flags = sum(r["governance_flags"] for r in row_results) / len(row_results)
        table.add_row(sid, *cells, f"{avg_flags:.1f}")

    console.print(table)


# ── Display: governance gap summary ───────────────────────────────────────────

def display_governance_summary(results: list[dict]) -> None:
    from rich.console import Console
    from rich.table import Table

    console = Console()
    sys_labels = [p[0] for p in PROFILES]

    table = Table(
        title="Governance Gap Flags by System (total across all 14 scenarios)",
        show_header=True,
        header_style="bold",
        border_style="dim",
    )
    table.add_column("System", style="bold")
    table.add_column("System Name", width=32)
    table.add_column("Total Flags", justify="center")
    table.add_column("Avg Flags/Scenario", justify="center")

    for sl in sys_labels:
        sys_results = [r for r in results if r["system"] == sl]
        total = sum(r["governance_flags"] for r in sys_results)
        avg = total / len(sys_results)
        name = sys_results[0]["system_name"] if sys_results else "—"
        table.add_row(sl, name, str(total), f"{avg:.1f}")

    console.print(table)


# ── CSV export ────────────────────────────────────────────────────────────────

def export_csv(results: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    # Full results
    full_path = output_dir / "benchmark_results.csv"
    fieldnames = [
        "system", "system_name", "scenario_id", "scenario_name",
        "zidr", "overall", "risk_level", "governance_flags", "weight_category",
    ]
    with open(full_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    # ZIDR matrix (for paper Table 1)
    scenario_ids = sorted(
        {r["scenario_id"] for r in results},
        key=lambda s: (s[0], int(s[2:])),
    )
    sys_labels = [p[0] for p in PROFILES]
    index = {(r["system"], r["scenario_id"]): r for r in results}

    matrix_path = output_dir / "zidr_matrix.csv"
    with open(matrix_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        header = ["scenario_id", "scenario_name"] + [PROFILE_LABELS[sl] for sl in sys_labels] + ["avg_zidr"]
        writer.writerow(header)
        for sid in scenario_ids:
            row_results = [index[(sl, sid)] for sl in sys_labels]
            zidrs = [r["zidr"] for r in row_results]
            avg = sum(zidrs) / len(zidrs)
            name = row_results[0]["scenario_name"]
            writer.writerow([sid, name] + [f"{z:.3f}" for z in zidrs] + [f"{avg:.3f}"])

    print(f"\nCSV exports written to: {output_dir.resolve()}")
    print(f"  {full_path.name} — full results ({len(results)} rows)")
    print(f"  {matrix_path.name} — ZIDR matrix (paper Table 1)")


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run ZIDR benchmark: 4 system profiles × 14 scenarios."
    )
    parser.add_argument(
        "--output-dir", type=Path, default=BASE_DIR / "results",
        help="Directory for CSV output (default: results/)",
    )
    parser.add_argument(
        "--no-csv", action="store_true",
        help="Skip CSV export (terminal output only)",
    )
    parser.add_argument(
        "--weights", type=Path, default=WEIGHTS_DEFAULT,
        help="Custom weights YAML",
    )
    args = parser.parse_args()

    from rich.console import Console
    console = Console()

    console.print()
    console.print("=" * 70, style="bold")
    console.print("ZIDR BENCHMARK — Adversarial Robustness for Women's Safety AI", style="bold")
    console.print("4 System Archetypes × 14 Scenarios", style="dim")
    console.print("=" * 70, style="bold")
    console.print()
    console.print("Running evaluations...", style="dim")

    results = run_benchmark(args.weights)

    display_zidr_matrix(results)
    display_overall_matrix(results)
    display_governance_summary(results)

    if not args.no_csv:
        export_csv(results, args.output_dir)

    console.print()
    console.print("=" * 70, style="bold")


if __name__ == "__main__":
    main()
