"""
Dimension 5: ZIDR — Zero-Interaction Detection Rate (adversary-induced)
Scoring rules: evaluation_criteria.md § ZIDR

ZIDR = (functional passive modalities at L0) / (total passive modalities)

Framing: the zero-interaction condition is adversarially imposed, not a UX failure.
NLP active check-in is excluded because it requires user action by definition.

Marginal (None): modality is partially functional at L0 in this context.
Treated as 0.5 contribution (fractional ZIDR). Worst-case context is used
when a scenario spans multiple context codes (e.g. U-01 spans U1 and T1).
"""
from __future__ import annotations


# Functional at L0 per modality per context code.
# True  = functional (adversary at L0 cannot defeat this modality here)
# False = defeated   (adversary at L0 trivially suppresses this modality)
# None  = marginal   (partial — treated as 0.5 contribution)
_FUNCTIONAL_AT_L0: dict[str, dict[str, bool | None]] = {
    "camera": {
        "U1": False,  # crowd occlusion trivially achieved at L0
        "U2": None,   # depends on lighting — marginal
        "R1": True,   # open space, clear sightlines
        "R2": True,   # open space, clear sightlines
        "T1": False,  # transit crowd occlusion at L0
    },
    "audio": {
        "U1": False,  # ambient noise suppression at L0 (85 dB)
        "U2": False,  # adversary controls venue ambient noise
        "R1": True,   # low ambient — detectable unless adversary vocalises
        "R2": True,   # quiet rural
        "T1": False,  # transit noise defeats audio at L0
    },
    "imu": {
        "U1": None,   # urban crowd vibration — marginal
        "U2": None,   # venue-dependent — marginal
        "R1": True,   # open terrain, low vibration
        "R2": True,   # open terrain, low vibration
        "T1": False,  # vehicle vibration corrupts baseline at L0
    },
    "gps": {
        "U1": True,   # GPS typically available in urban
        "U2": True,   # GPS available
        "R1": True,   # available (may be weak signal)
        "R2": False,  # dead zone — exploitable at L0 with local knowledge
        "T1": True,   # typically available
    },
}

_MARGINAL_VALUE = 0.5


def compute_zidr(profile, scenario) -> tuple[float, dict]:
    """
    Returns (zidr_score, detail_dict).

    profile:  SystemProfile object with .modalities.{camera,audio,imu,gps}.active
    scenario: Scenario object with .contexts (list[str]) and .primary_context
    """
    passive_modalities: list[str] = []
    if profile.modalities.camera.active:
        passive_modalities.append("camera")
    if profile.modalities.audio.active:
        passive_modalities.append("audio")
    if profile.modalities.imu.active:
        passive_modalities.append("imu")
    if profile.modalities.gps.active:
        passive_modalities.append("gps")
    # NLP in active (check-in) mode is excluded — requires victim agency

    if not passive_modalities:
        return 0.0, {
            "total_passive_modalities": 0,
            "functional_sum": 0.0,
            "modality_status": {},
            "primary_context": scenario.primary_context,
        }

    functional_sum = 0.0
    modality_status: dict[str, str] = {}

    for mod in passive_modalities:
        ctx_map = _FUNCTIONAL_AT_L0.get(mod, {})

        # Evaluate across all scenario contexts; use worst case
        values: list[float] = []
        for c in scenario.contexts:
            v = ctx_map.get(c)
            if v is True:
                values.append(1.0)
            elif v is False:
                values.append(0.0)
            else:
                values.append(_MARGINAL_VALUE)

        worst = min(values) if values else _MARGINAL_VALUE
        functional_sum += worst

        if worst >= 1.0:
            modality_status[mod] = "functional"
        elif worst <= 0.0:
            modality_status[mod] = "defeated"
        else:
            modality_status[mod] = "marginal"

    zidr = functional_sum / len(passive_modalities)

    detail = {
        "total_passive_modalities": len(passive_modalities),
        "functional_sum": round(functional_sum, 2),
        "modality_status": modality_status,
        "primary_context": scenario.primary_context,
    }
    return round(min(1.0, max(0.0, zidr)), 2), detail
