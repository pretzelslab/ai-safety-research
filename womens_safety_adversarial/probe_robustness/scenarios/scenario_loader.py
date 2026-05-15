"""
scenario_loader.py — Load a scenario from scenarios.yaml by ID.

Schema: new 12-field structure (2026-05-14 redo).
Backward-compatible API preserved for probe.py.

Usage (from probe.py):
    from scenarios.scenario_loader import load_scenario
    scenario = load_scenario("U-01")
    print(scenario.threat_type)       # derived from context_class.subtype
    print(scenario.contexts)          # from context_class.context_code
    print(scenario.criticality_score) # new field
"""

from __future__ import annotations
import yaml
from pathlib import Path
from dataclasses import dataclass, field


SCENARIOS_FILE = Path(__file__).parent / "scenarios.yaml"

# Map context_class.subtype → threat_type for weights lookup
_SUBTYPE_TO_THREAT: dict[str, str] = {
    "transit_public":                "transit_harassment",
    "cab_transit":                   "cab_harassment",
    "semi_private_institutional":    "workplace_harassment",  # U-06 overridden below
    "public_market":                 "street_following",
    "public_transit_stop":           "stalking",
    "semi_private_social":           "social_venue_assault",
    "isolated_semi_private":         "device_grab",
    "isolated_confinement":          "cab_harassment",
    "agricultural_isolated":         "rural_assault",
    "public_pathway":                "pathway_assault",
    "transit_moving_rural":          "rural_transit_assault",
    "public_community":              "community_authority_harassment",
    "agricultural_employer_context": "employer_coercion",
}

# Per-ID overrides where subtype is ambiguous
_SCENARIO_THREAT_OVERRIDES: dict[str, str] = {
    "U-06": "campus_harassment",
}


@dataclass
class Scenario:
    # Core identity
    id: str
    name: str

    # Derived backward-compat fields (used by probe.py + gap_checker.py)
    contexts: list[str]
    threat_type: str
    adversary_type: str
    attack_methods: list[str]
    novel_vector: bool

    # New fields from updated schema
    criticality_score: int
    failure_mode_type: list[str]
    passive_layers: list[str]
    test_reproducibility: str
    time_horizon: str
    novel_attack_vector: bool
    sociotechnical_attack: bool
    confidence_level: str
    adversary_access_level: str          # "L0"–"L5"
    evidence_basis: dict = field(default_factory=dict)
    governance_gap_requirements: list[str] = field(default_factory=list)
    regulatory_frameworks: list[str] = field(default_factory=list)

    # Benchmark
    window_seconds: int | None = None
    expected_zidr_min: float = 0.0
    expected_zidr_max: float = 1.0
    degradation_factors: dict = field(default_factory=dict)

    # ── Backward-compat properties ────────────────────────────────────────────

    @property
    def primary_context(self) -> str:
        return self.contexts[0] if self.contexts else "U1"

    @property
    def is_rural(self) -> bool:
        return any(c.startswith("R") for c in self.contexts)

    @property
    def is_transit(self) -> bool:
        return "T1" in self.contexts

    @property
    def is_social_suppression(self) -> bool:
        return "sociotechnical_suppression" in self.failure_mode_type

    @property
    def access_level(self) -> int:
        try:
            return int(self.adversary_access_level.lstrip("L"))
        except (ValueError, AttributeError):
            return 0

    # access_level_min / access_level_max kept as properties for any callers
    @property
    def access_level_min(self) -> int:
        return self.access_level

    @property
    def access_level_max(self) -> int:
        return self.access_level

    # subsystems_targeted: derive from passive_layers (best approximation)
    @property
    def subsystems_targeted(self) -> list[str]:
        return self.passive_layers


def load_scenario(scenario_id: str) -> Scenario:
    """
    Load a single scenario by ID (e.g. "U-01", "R-02").

    Raises:
        FileNotFoundError: if scenarios.yaml cannot be found
        ValueError: if scenario_id does not exist in the library
    """
    if not SCENARIOS_FILE.exists():
        raise FileNotFoundError(
            f"Scenario library not found at {SCENARIOS_FILE}. "
            "Ensure scenarios.yaml is present in probe_robustness/scenarios/."
        )

    with open(SCENARIOS_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    for entry in data.get("scenarios", []):
        if entry["scenario_id"] == scenario_id:
            return _build_scenario(entry)

    valid_ids = [s["scenario_id"] for s in data.get("scenarios", [])]
    raise ValueError(
        f"Scenario '{scenario_id}' not found. "
        f"Available IDs: {', '.join(valid_ids)}"
    )


def list_scenarios() -> list[tuple[str, str]]:
    """Return all (id, name) pairs from the scenario library."""
    if not SCENARIOS_FILE.exists():
        return []
    with open(SCENARIOS_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return [(s["scenario_id"], s["scenario_name"]) for s in data.get("scenarios", [])]


def _build_scenario(entry: dict) -> Scenario:
    sid = entry["scenario_id"]
    ctx = entry.get("context_class", {})
    ap = entry.get("attack_profile", {})
    bench = entry.get("benchmark", {})
    meta = entry.get("metadata", {})
    ev = entry.get("evidence_basis", {})
    gap = entry.get("governance_gap", {})
    reg = entry.get("regulatory_mapping", {})

    contexts = ctx.get("context_code", [])
    subtype = ctx.get("subtype", "")
    threat_type = _SCENARIO_THREAT_OVERRIDES.get(
        sid, _SUBTYPE_TO_THREAT.get(subtype, "transit_harassment")
    )

    zidr_range = bench.get("expected_zidr_range") or {}
    dg = bench.get("degradation_factors") or {}

    return Scenario(
        id=sid,
        name=entry["scenario_name"],
        contexts=contexts,
        threat_type=threat_type,
        adversary_type=ap.get("adversary_type", "opportunistic"),
        attack_methods=ap.get("attack_methods", []),
        novel_vector=meta.get("novel_attack_vector", False),
        criticality_score=meta.get("criticality_score", 3),
        failure_mode_type=entry.get("failure_mode_type") or [],
        passive_layers=entry.get("passive_layers") or [],
        test_reproducibility=meta.get("test_reproducibility", "medium"),
        time_horizon=meta.get("time_horizon", "immediate"),
        novel_attack_vector=meta.get("novel_attack_vector", False),
        sociotechnical_attack=meta.get("sociotechnical_attack", False),
        confidence_level=meta.get("confidence_level", "medium"),
        adversary_access_level=ap.get("adversary_access_level", "L0"),
        evidence_basis=ev,
        governance_gap_requirements=gap.get("missing_requirements") or [],
        regulatory_frameworks=reg.get("affected_frameworks") or [],
        window_seconds=bench.get("window_seconds"),
        expected_zidr_min=float(zidr_range.get("min", 0.0)),
        expected_zidr_max=float(zidr_range.get("max", 1.0)),
        degradation_factors=dg,
    )
