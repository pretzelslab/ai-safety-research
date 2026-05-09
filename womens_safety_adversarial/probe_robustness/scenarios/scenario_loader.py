"""
scenario_loader.py — Load a scenario from scenarios.yaml by ID.

Usage (from probe.py):
    from scenarios.scenario_loader import load_scenario
    scenario = load_scenario("U-01")
    print(scenario.threat_type)     # "transit_harassment"
    print(scenario.contexts)        # ["U1", "T1"]
"""

from __future__ import annotations
import yaml
from pathlib import Path
from dataclasses import dataclass, field


SCENARIOS_FILE = Path(__file__).parent / "scenarios.yaml"


@dataclass
class Scenario:
    id: str
    name: str
    contexts: list[str]
    threat_type: str
    adversary_type: str
    access_level_min: int
    access_level_max: int
    attack_methods: list[str]
    subsystems_targeted: list[str]
    evasion_mechanism: str
    governance_gap_frameworks: list[str]
    all_frameworks_gap: bool
    novel_vector: bool
    governance_gap_note: str
    citation_status: str
    citation_note: str

    # Derived convenience properties

    @property
    def primary_context(self) -> str:
        """First context in the list (used as primary for scoring)."""
        return self.contexts[0] if self.contexts else "U1"

    @property
    def is_rural(self) -> bool:
        return any(c.startswith("R") for c in self.contexts)

    @property
    def is_transit(self) -> bool:
        return "T1" in self.contexts

    @property
    def is_social_suppression(self) -> bool:
        """True when the alert is never triggered — sociotechnical suppression scenarios."""
        return not self.subsystems_targeted and "suppress" in self.attack_methods

    @property
    def access_level(self) -> int:
        """Maximum access level the adversary can reach in this scenario."""
        return self.access_level_max


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

    scenarios = data.get("scenarios", [])
    for entry in scenarios:
        if entry["id"] == scenario_id:
            return Scenario(
                id=entry["id"],
                name=entry["name"],
                contexts=entry.get("contexts", []),
                threat_type=entry["threat_type"],
                adversary_type=entry["adversary_type"],
                access_level_min=entry["access_level_min"],
                access_level_max=entry["access_level_max"],
                attack_methods=entry.get("attack_methods", []),
                subsystems_targeted=entry.get("subsystems_targeted", []),
                evasion_mechanism=entry.get("evasion_mechanism", ""),
                governance_gap_frameworks=entry.get("governance_gap_frameworks", []),
                all_frameworks_gap=entry.get("all_frameworks_gap", False),
                novel_vector=entry.get("novel_vector", False),
                governance_gap_note=entry.get("governance_gap_note", ""),
                citation_status=entry.get("citation_status", "needed"),
                citation_note=entry.get("citation_note", ""),
            )

    valid_ids = [s["id"] for s in scenarios]
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
    return [(s["id"], s["name"]) for s in data.get("scenarios", [])]
