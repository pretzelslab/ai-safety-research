#!/usr/bin/env python3
"""
probe.py — Probe Robustness Tool CLI

Evaluates a safety AI system profile against an adversarial scenario and
produces a robustness report: per-dimension scores, ZIDR, governance gap
flags, and recommendations.

Usage:
    python probe.py --profile profiles/example_profile.yaml --scenario U-01
    python probe.py --profile profiles/himmat_plus.yaml --scenario R-02 --output json
    python probe.py --list-scenarios

Requirements: pyyaml rich  (pip install pyyaml rich)
"""

from __future__ import annotations

import argparse
import io
import json
import sys

# Force UTF-8 output on Windows (box-drawing characters require it)
if sys.platform == "win32" and hasattr(sys.stdout, "buffer"):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except AttributeError:
        pass

from dataclasses import dataclass, field
from pathlib import Path

import yaml

# ── Paths ─────────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent
WEIGHTS_DEFAULT = BASE_DIR / "weights" / "default_weights.yaml"

# ── Profile dataclasses ───────────────────────────────────────────────────────


@dataclass
class CameraModality:
    active: bool = False
    mode: str = "passive"
    claimed_occlusion_tolerance: float | None = None
    low_light_processing: bool = False
    published_accuracy: float | None = None


@dataclass
class AudioModality:
    active: bool = False
    mode: str = "passive"
    claimed_anef_db: float | None = None
    keyword_required: bool = True
    published_accuracy: float | None = None


@dataclass
class IMUModality:
    active: bool = False
    calibration_profiles: list[str] = field(default_factory=list)
    published_accuracy: float | None = None


@dataclass
class GPSModality:
    active: bool = False
    offline_fallback: bool = False
    minimum_signal_required: str | None = None


@dataclass
class NLPModality:
    active: bool = False
    mode: str = "active"
    cbr_tested: bool = False
    cbr_value: float | None = None


@dataclass
class Modalities:
    camera: CameraModality = field(default_factory=CameraModality)
    audio: AudioModality = field(default_factory=AudioModality)
    imu: IMUModality = field(default_factory=IMUModality)
    gps: GPSModality = field(default_factory=GPSModality)
    nlp: NLPModality = field(default_factory=NLPModality)


@dataclass
class AlertConfig:
    methods: list[str] = field(default_factory=list)
    delivery_verified: bool = False


@dataclass
class GovernanceConfig:
    eu_ai_act_classification: str | None = None
    iso_42001_certified: bool = False
    nist_ai_rmf_aligned: bool = False
    india_regulatory_compliant: str | None = None
    robustness_testing_published: bool = False


@dataclass
class SystemProfile:
    name: str = "Unknown System"
    version: str = "0.0"
    developer: str = "Unknown"
    markets: list[str] = field(default_factory=list)
    modalities: Modalities = field(default_factory=Modalities)
    alert: AlertConfig = field(default_factory=AlertConfig)
    deployment_contexts: list[str] = field(default_factory=list)
    governance: GovernanceConfig = field(default_factory=GovernanceConfig)


# ── Profile loader ────────────────────────────────────────────────────────────


def load_profile(path: Path) -> SystemProfile:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    sys_raw = raw.get("system", {})
    mod_raw = raw.get("modalities", {})
    cam = mod_raw.get("camera", {})
    aud = mod_raw.get("audio", {})
    imu = mod_raw.get("imu", {})
    gps = mod_raw.get("gps", {})
    nlp = mod_raw.get("nlp", {})
    gov = raw.get("governance", {})
    alt = raw.get("alert", {})

    return SystemProfile(
        name=sys_raw.get("name", "Unknown"),
        version=str(sys_raw.get("version", "0.0")),
        developer=sys_raw.get("developer", "Unknown"),
        markets=sys_raw.get("markets", []),
        modalities=Modalities(
            camera=CameraModality(
                active=cam.get("active", False),
                mode=cam.get("mode", "passive"),
                claimed_occlusion_tolerance=cam.get("claimed_occlusion_tolerance"),
                low_light_processing=cam.get("low_light_processing", False),
                published_accuracy=cam.get("published_accuracy"),
            ),
            audio=AudioModality(
                active=aud.get("active", False),
                mode=aud.get("mode", "passive"),
                claimed_anef_db=aud.get("claimed_anef_db"),
                keyword_required=aud.get("keyword_required", True),
                published_accuracy=aud.get("published_accuracy"),
            ),
            imu=IMUModality(
                active=imu.get("active", False),
                calibration_profiles=imu.get("calibration_profiles", []),
                published_accuracy=imu.get("published_accuracy"),
            ),
            gps=GPSModality(
                active=gps.get("active", False),
                offline_fallback=gps.get("offline_fallback", False),
                minimum_signal_required=gps.get("minimum_signal_required"),
            ),
            nlp=NLPModality(
                active=nlp.get("active", False),
                mode=nlp.get("mode", "active"),
                cbr_tested=nlp.get("cbr_tested", False),
                cbr_value=nlp.get("cbr_value"),
            ),
        ),
        alert=AlertConfig(
            methods=alt.get("methods", []),
            delivery_verified=alt.get("delivery_verified", False),
        ),
        deployment_contexts=raw.get("deployment_contexts", []),
        governance=GovernanceConfig(
            eu_ai_act_classification=gov.get("eu_ai_act_classification"),
            iso_42001_certified=gov.get("iso_42001_certified", False),
            nist_ai_rmf_aligned=gov.get("nist_ai_rmf_aligned", False),
            india_regulatory_compliant=gov.get("india_regulatory_compliant"),
            robustness_testing_published=gov.get("robustness_testing_published", False),
        ),
    )


# ── Weights loader ────────────────────────────────────────────────────────────


def load_weights(threat_type: str, weights_path: Path) -> tuple[str, dict[str, float]]:
    with open(weights_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    threat_map = data.get("threat_type_map", {})
    category = threat_map.get(threat_type, "crowded_transit")
    category_raw = data.get("weights", {}).get(category, {})
    # Strip non-numeric keys (e.g. "description")
    weights = {k: v for k, v in category_raw.items() if isinstance(v, (int, float))}
    return category, weights


# ── Score utilities ───────────────────────────────────────────────────────────


def score_label(score: float) -> str:
    """Map 0.0–1.0 score to risk band label."""
    if score >= 0.8:
        return "LOW RISK"
    elif score >= 0.6:
        return "MODERATE"
    elif score >= 0.4:
        return "HIGH RISK"
    else:
        return "CRITICAL"


def score_bar(score: float, width: int = 10) -> str:
    filled = min(width, round(score * width))
    return "█" * filled + "░" * (width - filled)


def risk_color(label: str) -> str:
    return {
        "LOW RISK": "green",
        "MODERATE": "yellow",
        "HIGH RISK": "red",
        "CRITICAL": "bold red",
    }.get(label, "white")


# ── Evaluation ────────────────────────────────────────────────────────────────


def run_evaluation(profile: SystemProfile, scenario, weights_path: Path) -> dict:
    from scorer import score_vision, score_audio, score_sensor_fusion, score_nlp, compute_zidr
    from governance import check_governance_gaps

    # Detection modalities determine "primary" status for vision/audio scoring
    active_detection = [
        m for m, active in [
            ("camera", profile.modalities.camera.active),
            ("audio", profile.modalities.audio.active),
            ("nlp", profile.modalities.nlp.active),
        ] if active
    ]

    ctx = scenario.primary_context
    results: dict[str, dict] = {}

    # ── Dimension 1: Vision ───────────────────────────────────────────────────
    if profile.modalities.camera.active:
        v = score_vision(
            occlusion_tolerance=profile.modalities.camera.claimed_occlusion_tolerance,
            low_light_processing=profile.modalities.camera.low_light_processing,
            deployment_context=ctx,
            published_accuracy=profile.modalities.camera.published_accuracy,
            is_primary_modality=(
                "camera" in active_detection and len(active_detection) == 1
            ),
        )
        results["vision"] = {"score": v, "detail": {}}

    # ── Dimension 2: Audio ────────────────────────────────────────────────────
    if profile.modalities.audio.active:
        a = score_audio(
            anef_db=profile.modalities.audio.claimed_anef_db,
            keyword_required=profile.modalities.audio.keyword_required,
            deployment_context=ctx,
            threat_type=scenario.threat_type,
            is_primary_modality=(
                "audio" in active_detection and len(active_detection) == 1
            ),
        )
        results["audio"] = {"score": a, "detail": {}}

    # ── Dimension 3: Sensor Fusion (always computed) ──────────────────────────
    sf, sf_detail = score_sensor_fusion(
        gps_offline_fallback=profile.modalities.gps.offline_fallback,
        imu_calibration=profile.modalities.imu.calibration_profiles,
        alert_methods=profile.alert.methods,
        deployment_context=ctx,
        threat_type=scenario.threat_type,
        imu_active=profile.modalities.imu.active,
        gps_active=profile.modalities.gps.active,
    )
    results["sensor_fusion"] = {"score": sf, "detail": sf_detail}

    # ── Dimension 4: NLP ──────────────────────────────────────────────────────
    if profile.modalities.nlp.active:
        n = score_nlp(
            mode=profile.modalities.nlp.mode,
            cbr_tested=profile.modalities.nlp.cbr_tested,
            cbr_value=profile.modalities.nlp.cbr_value,
            deployment_context=ctx,
        )
        results["nlp"] = {"score": n, "detail": {}}

    # ── Dimension 5: ZIDR ─────────────────────────────────────────────────────
    zidr, zidr_detail = compute_zidr(profile, scenario)
    results["zidr"] = {"score": zidr, "detail": zidr_detail}

    # ── Weighted overall score ─────────────────────────────────────────────────
    weight_category, weights = load_weights(scenario.threat_type, weights_path)
    total_weight = 0.0
    overall = 0.0
    for dim, w in weights.items():
        if dim in results:
            overall += results[dim]["score"] * w
            total_weight += w
    if total_weight > 0:
        # Normalise in case some dimensions are excluded (modality inactive)
        overall = overall / total_weight

    overall = round(min(1.0, max(0.0, overall)), 2)
    risk = score_label(overall)

    flags = check_governance_gaps(profile, scenario, results)
    recs = _generate_recommendations(results, profile, scenario, flags)

    return {
        "results": results,
        "overall": overall,
        "risk_level": risk,
        "weight_category": weight_category,
        "governance_flags": flags,
        "recommendations": recs,
        "zidr_detail": zidr_detail,
    }


def _generate_recommendations(
    results: dict, profile: SystemProfile, scenario, flags: list[dict]
) -> list[str]:
    recs: list[str] = []

    # Audio: no published ANEF data
    a = results.get("audio", {}).get("score")
    if a is not None and a < 0.3:
        recs.append(
            "Audio: Publish ANEF data. Calibrate to Indian urban noise levels "
            "(target ANEF ≥ 85 dB for U1/T1 contexts)."
        )

    # IMU: single calibration profile in transit
    sf_detail = results.get("sensor_fusion", {}).get("detail", {})
    if sf_detail.get("imu", 1.0) < 0.4 and scenario.is_transit:
        recs.append(
            "IMU: Add crowded-transit calibration profile to distinguish groping "
            "micro-motion from standard transit movement noise."
        )

    # Sensor fusion: GPS or network failure in deployment context
    if sf_detail.get("gps", 1.0) == 0.0 or sf_detail.get("network", 1.0) == 0.0:
        recs.append(
            "Offline fallback: Implement stored-and-forward SMS alert for "
            "network-degraded and rural dead-zone contexts."
        )

    # NLP: keyword-only in high-noise or authority-asymmetric contexts
    n = results.get("nlp", {}).get("score")
    if (
        n is not None
        and n < 0.4
        and profile.modalities.audio.keyword_required
    ):
        recs.append(
            "Passive detection: Reduce reliance on keyword activation in "
            "high-noise or authority-asymmetric deployment contexts."
        )

    # ZIDR: passive detection effectively defeated
    if results.get("zidr", {}).get("score", 1.0) < 0.25:
        recs.append(
            "ZIDR: Passive detection effectively defeated at L0 in this scenario. "
            "System provides false assurance — redesign required before high-risk deployment."
        )

    # Governance: no EU classification
    if any(f["code"] == "GOV-EU-CLASSIFICATION" for f in flags):
        recs.append(
            "Governance: Request EU AI Act high-risk classification review to "
            "ensure Art. 15 adversarial robustness requirements apply."
        )

    return recs


# ── Terminal display ──────────────────────────────────────────────────────────


def display_terminal(profile: SystemProfile, scenario, eval_result: dict) -> None:
    from rich.console import Console
    from rich.text import Text

    console = Console()

    DIM_LABELS = {
        "vision":        "Vision",
        "audio":         "Audio",
        "sensor_fusion": "Sensor Fusion",
        "nlp":           "NLP / Language",
        "zidr":          "ZIDR (adv.)",
    }

    W = 62  # report width

    # ── Header ────────────────────────────────────────────────────────────────
    console.print("═" * W, style="bold")
    console.print("PROBE ROBUSTNESS REPORT", style="bold")
    console.print(f"System:   {profile.name} v{profile.version}")
    console.print(f"Scenario: {scenario.id} — {scenario.name}")
    context_str = "/".join(scenario.contexts)
    threat_str = scenario.threat_type.replace("_", " ")
    console.print(f"Context:  {context_str} | Threat: {threat_str}")
    console.print("═" * W, style="bold")

    # ── Dimension scores ──────────────────────────────────────────────────────
    console.print()
    console.print("DIMENSION SCORES", style="bold")
    console.print("─" * 45)

    results = eval_result["results"]
    for dim in ["vision", "audio", "sensor_fusion", "nlp", "zidr"]:
        label = DIM_LABELS[dim]
        if dim not in results:
            console.print(f"{label:<16}  ──────────  {'N/A':<6}   [ {'N/A':<9} ]", style="dim")
            continue

        score = results[dim]["score"]
        band = score_label(score)
        bar = score_bar(score)
        line = Text()
        line.append(f"{label:<16}  ")
        line.append(bar, style=risk_color(band))
        line.append(f"  {score:.2f}   ")
        line.append(f"[ {band:<9} ]", style=risk_color(band))
        console.print(line)

    console.print("─" * 45)

    # ── Overall ───────────────────────────────────────────────────────────────
    overall = eval_result["overall"]
    risk = eval_result["risk_level"]
    indicator = "✓" if risk == "LOW RISK" else "⚠"
    overall_line = Text()
    overall_line.append("OVERALL SCORE   ")
    overall_line.append(score_bar(overall), style=risk_color(risk))
    overall_line.append(f"  {overall:.2f}   ")
    overall_line.append(f"{indicator} {risk}", style=risk_color(risk))
    console.print(overall_line, style="bold")
    console.print("─" * 45)

    # ── ZIDR note ─────────────────────────────────────────────────────────────
    zidr_detail = eval_result.get("zidr_detail", {})
    if zidr_detail and zidr_detail.get("total_passive_modalities", 0) > 0:
        console.print()
        console.print("ZIDR NOTE:", style="bold")
        status = zidr_detail.get("modality_status", {})
        defeated = [m for m, s in status.items() if s == "defeated"]
        functional = [m for m, s in status.items() if s == "functional"]
        marginal = [m for m, s in status.items() if s == "marginal"]
        total = zidr_detail["total_passive_modalities"]
        func_sum = zidr_detail["functional_sum"]

        # Express functional count as integer where possible
        func_display = int(func_sum) if func_sum == int(func_sum) else func_sum

        parts = [
            f"At L0 adversary access in {context_str} context, "
            f"{func_display} of {total} passive modalities remain functional.",
        ]
        if defeated:
            parts.append(f"Defeated: {', '.join(defeated)}.")
        if marginal:
            parts.append(f"Marginal: {', '.join(marginal)}.")
        if functional:
            parts.append(f"Functional: {', '.join(functional)}.")
        if func_sum < total * 0.5:
            parts.append("Victim agency suppressed; passive detection effectively unavailable.")

        console.print(" ".join(parts))

    # ── Governance gap flags ──────────────────────────────────────────────────
    if eval_result["governance_flags"]:
        console.print()
        console.print("GOVERNANCE GAP FLAGS", style="bold")
        console.print("─" * 45)
        for flag in eval_result["governance_flags"]:
            console.print(f"[{flag['code']}]", style="yellow bold")
            console.print(f"  {flag['description']}")
            console.print(f"  Ref: {flag['article']}", style="dim")

    # ── Recommendations ───────────────────────────────────────────────────────
    if eval_result["recommendations"]:
        console.print()
        console.print("RECOMMENDATIONS", style="bold")
        console.print("─" * 45)
        for i, rec in enumerate(eval_result["recommendations"], 1):
            console.print(f"{i}. {rec}")

    console.print("═" * W, style="bold")


# ── JSON display ──────────────────────────────────────────────────────────────


def display_json(profile: SystemProfile, scenario, eval_result: dict) -> None:
    output = {
        "system": f"{profile.name} v{profile.version}",
        "developer": profile.developer,
        "scenario": scenario.id,
        "scenario_name": scenario.name,
        "scenario_context": "/".join(scenario.contexts),
        "threat_type": scenario.threat_type,
        "scores": {dim: data["score"] for dim, data in eval_result["results"].items()},
        "sensor_fusion_components": eval_result["results"].get("sensor_fusion", {}).get("detail", {}),
        "overall": eval_result["overall"],
        "risk_level": eval_result["risk_level"],
        "weight_category": eval_result["weight_category"],
        "governance_flags": [f["code"] for f in eval_result["governance_flags"]],
        "governance_flag_detail": eval_result["governance_flags"],
        "zidr_detail": eval_result["zidr_detail"],
        "recommendations": eval_result["recommendations"],
    }
    print(json.dumps(output, indent=2))


# ── CLI ───────────────────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Probe Robustness Tool — evaluate a women's safety AI system "
            "against an adversarial scenario."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python probe.py --profile profiles/example_profile.yaml --scenario U-01
  python probe.py --profile profiles/example_profile.yaml --scenario R-02 --output json
  python probe.py --list-scenarios
        """,
    )
    parser.add_argument("--profile", type=Path, help="Path to system profile YAML")
    parser.add_argument("--scenario", type=str, help="Scenario ID (e.g. U-01, R-02)")
    parser.add_argument(
        "--output", choices=["terminal", "json"], default="terminal",
        help="Output format (default: terminal)"
    )
    parser.add_argument(
        "--weights", type=Path, default=WEIGHTS_DEFAULT,
        help="Custom weights YAML (default: weights/default_weights.yaml)"
    )
    parser.add_argument(
        "--list-scenarios", action="store_true",
        help="List all available scenario IDs and exit"
    )
    args = parser.parse_args()

    from scenarios import load_scenario, list_scenarios

    if args.list_scenarios:
        all_scenarios = list_scenarios()
        print("Available scenarios:")
        for sid, sname in all_scenarios:
            print(f"  {sid:<6}  {sname}")
        sys.exit(0)

    if not args.profile or not args.scenario:
        parser.error("--profile and --scenario are required (or use --list-scenarios)")

    if not args.profile.exists():
        print(f"Error: profile not found: {args.profile}", file=sys.stderr)
        sys.exit(1)

    if not args.weights.exists():
        print(f"Error: weights file not found: {args.weights}", file=sys.stderr)
        sys.exit(1)

    profile = load_profile(args.profile)
    scenario = load_scenario(args.scenario)
    eval_result = run_evaluation(profile, scenario, args.weights)

    if args.output == "json":
        display_json(profile, scenario, eval_result)
    else:
        display_terminal(profile, scenario, eval_result)


if __name__ == "__main__":
    main()
