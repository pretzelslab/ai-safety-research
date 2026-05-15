"""
Dimension 2: Audio (ANEF — Audio Noise Evasion Floor)
Scoring rules: evaluation_criteria.md § Audio

Indian deployment context reference levels (CPCB, to be cited):
  Urban street / market:       75–80 dB
  Mumbai local train platform: ~85 dB
  Social venue (party, bar):   80–90 dB
  Rural road with traffic:     70–75 dB
  Quiet rural area:            45–55 dB
"""
from __future__ import annotations


def score_audio(
    anef_db: float | None,
    keyword_required: bool,
    deployment_context: str,
    threat_type: str,
    is_primary_modality: bool = False,
) -> float:
    """
    Returns 0.0–1.0. Only called when audio.active is True.

    anef_db: ambient noise floor (dB) at 50% detection rate, or None if unpublished.
    is_primary_modality: True when audio is the only active threat-detection modality.
    """
    # ANEF decision tree (evaluation_criteria.md)
    if anef_db is not None:
        # Published ANEF data exists
        if anef_db >= 90:
            score = 1.0
        elif anef_db >= 80:
            score = 0.8
        elif anef_db >= 70:
            score = 0.5
        else:
            score = 0.2
    elif is_primary_modality:
        # Audio is only modality and no noise floor data → critical
        score = 0.0
    elif deployment_context in ("U1", "T1"):
        # No ANEF, deployed in high-noise urban/transit context
        score = 0.1
    else:
        # No ANEF, other contexts (U2, R1, R2)
        score = 0.3

    # Sociotechnical deduction: keyword activation in authority-asymmetric context.
    # Social suppression operates at L5 independently of acoustic performance.
    if keyword_required and deployment_context == "U2":
        score = max(0.0, score - 0.3)

    return round(min(1.0, max(0.0, score)), 2)
