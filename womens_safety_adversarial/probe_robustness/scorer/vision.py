"""
Dimension 1: Vision (OET — Occlusion Evasion Threshold)
Scoring rules: evaluation_criteria.md § Vision
"""
from __future__ import annotations


def score_vision(
    occlusion_tolerance: float | None,
    low_light_processing: bool,
    deployment_context: str,
    published_accuracy: float | None,
    is_primary_modality: bool = False,
) -> float:
    """
    Returns 0.0–1.0. Only called when camera.active is True.

    is_primary_modality: True when camera is the only active threat-detection
    modality (no audio, no NLP active). Triggers the 0.0 floor score.
    """
    # OET decision tree (evaluation_criteria.md)
    if occlusion_tolerance is not None and published_accuracy is not None:
        # Claimed + published data → use OET threshold guide
        if occlusion_tolerance >= 50:
            score = 0.9
        elif occlusion_tolerance >= 25:
            score = 0.5
        elif occlusion_tolerance > 0:
            score = 0.2
        else:
            score = 0.0
    elif occlusion_tolerance is not None:
        # Unverified claim (no published accuracy)
        score = 0.5
    elif is_primary_modality:
        # Relies on camera as sole modality, no occlusion claim → critical
        score = 0.0
    elif deployment_context in ("U1", "U2", "T1"):
        # No claim, urban or transit context
        score = 0.2
    else:
        # No claim, rural context (R1/R2) — open space is less severe
        score = 0.35

    # Low-light adjustment: no adaptive pre-processing in night/indoor contexts
    if not low_light_processing and deployment_context in ("U2", "T1"):
        score = max(0.0, score - 0.2)

    return round(min(1.0, max(0.0, score)), 2)
