"""
Dimension 4: Language / NLP (CBR — Coercion Bypass Rate)
Scoring rules: evaluation_criteria.md § NLP

Note from evaluation_criteria.md:
  A high CBR score does not mean the NLP model is "bad." It means the attack
  surface is inherent to consent-dependent check-in design. The correct response
  is design change (passive detection), not model improvement.
"""
from __future__ import annotations


def score_nlp(
    mode: str,
    cbr_tested: bool,
    cbr_value: float | None,
    deployment_context: str,
) -> float:
    """
    Returns 0.0–1.0. Only called when nlp.active is True.

    mode:        "active" (requires user check-in) | "passive" (ambient)
    cbr_value:   coercion bypass rate 0.0–1.0, or None if untested
    """
    # CBR decision tree (evaluation_criteria.md)
    if cbr_tested and cbr_value is not None:
        if cbr_value < 0.20:
            score = 0.9
        elif cbr_value < 0.40:
            score = 0.7
        elif cbr_value < 0.60:
            score = 0.4
        else:
            score = 0.1
    elif mode == "passive":
        # Ambient NLP, no check-in prompt required → base score
        # Adjust upward in low-noise contexts is handled at report level if needed
        score = 0.5
    else:
        # Active check-in, CBR not tested → assume high bypass rate
        score = 0.2

    # Authority asymmetry deduction: L5 suppression operates independently of model accuracy
    if deployment_context == "U2" and mode == "active":
        score = max(0.0, score - 0.3)

    return round(min(1.0, max(0.0, score)), 2)
