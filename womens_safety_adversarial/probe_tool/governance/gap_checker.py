"""
Governance Gap Flag Checker
Rules source: evaluation_criteria.md § Governance Gap Flags

check_governance_gaps() is a lookup-table function — it maps
(deployment_context, score_bands, governance fields, scenario attack methods)
to a list of gap flags. No scoring logic here.
"""
from __future__ import annotations


def check_governance_gaps(profile, scenario, scores: dict) -> list[dict]:
    """
    Returns a list of triggered governance gap flags.

    Each flag dict:
      { "code": str, "description": str, "article": str }

    profile:  SystemProfile object with .governance attributes
    scenario: Scenario object with .contexts, .attack_methods
    scores:   dict of { dimension: { "score": float, ... } }
    """
    flags: list[dict] = []
    gov = profile.governance

    # GOV-EU-CLASSIFICATION: not classified high-risk → Art. 15 does not apply
    if gov.eu_ai_act_classification != "high_risk":
        flags.append({
            "code": "GOV-EU-CLASSIFICATION",
            "description": (
                "System not classified high-risk under EU AI Act Annex III. "
                "Art. 15 robustness requirements do not apply."
            ),
            "article": "EU AI Act Art. 15 / Annex III",
        })

    # GOV-EU-ROBUSTNESS: high-risk classified but no robustness evidence published
    if gov.eu_ai_act_classification == "high_risk" and not gov.robustness_testing_published:
        flags.append({
            "code": "GOV-EU-ROBUSTNESS",
            "description": (
                "System classified high-risk but no Art. 15 robustness evidence "
                "published for physical proximity adversarial conditions."
            ),
            "article": "EU AI Act Art. 15",
        })

    # GOV-NIST-SOCIOTECH: scenario involves sociotechnical suppression, NIST not aligned
    if "suppress" in scenario.attack_methods and not gov.nist_ai_rmf_aligned:
        flags.append({
            "code": "GOV-NIST-SOCIOTECH",
            "description": (
                "Scenario involves sociotechnical suppression (L4/L5) but system has "
                "no NIST AI RMF GOVERN 6.1 documentation addressing this attack surface."
            ),
            "article": "NIST AI RMF GOVERN 6.1",
        })

    # GOV-NIST-ZIDR: no ZIDR measurement documented
    if not gov.robustness_testing_published:
        flags.append({
            "code": "GOV-NIST-ZIDR",
            "description": (
                "No ZIDR measurement documented. System has not published adversarial "
                "robustness data under zero-interaction conditions."
            ),
            "article": "NIST AI RMF MEASURE 2.5",
        })

    # GOV-INDIA-NONE: no India regulatory compliance documented at all
    if gov.india_regulatory_compliant is None:
        flags.append({
            "code": "GOV-INDIA-NONE",
            "description": (
                "No India regulatory robustness requirement applies to this system. "
                "DPDP Act and IT Act cover data storage, not real-time attack surfaces."
            ),
            "article": "India DPDP Act / IT Act 2000",
        })

    # GOV-INDIA-RURAL: rural deployment with no offline alert fallback
    if (
        any(c in ("R1", "R2") for c in scenario.contexts)
        and not profile.modalities.gps.offline_fallback
    ):
        flags.append({
            "code": "GOV-INDIA-RURAL",
            "description": (
                "Deployed in rural context (R1/R2) with no offline alert fallback. "
                "Alert cannot transmit in connectivity dead zones — no framework "
                "currently requires offline fallback capability."
            ),
            "article": "India DPDP Act (gap: no rural connectivity requirement)",
        })

    # GOV-ISO-PROCESS: ISO 42001 certified but no adversarial test evidence
    if gov.iso_42001_certified and not gov.robustness_testing_published:
        flags.append({
            "code": "GOV-ISO-PROCESS",
            "description": (
                "ISO 42001 certified but no adversarial robustness test evidence published. "
                "ISO 42001 certifies management process, not system performance."
            ),
            "article": "ISO 42001:2023",
        })

    # GOV-CROSS-ARBITRAGE: no jurisdiction requires minimum robustness for this system
    no_eu = gov.eu_ai_act_classification != "high_risk"
    no_nist = not gov.nist_ai_rmf_aligned
    no_india = gov.india_regulatory_compliant is None
    if no_eu and no_nist and no_india:
        flags.append({
            "code": "GOV-CROSS-ARBITRAGE",
            "description": (
                "No jurisdiction currently requires minimum robustness standards "
                "for this system's deployment context. Regulatory gap is fully unaddressed "
                "across EU, US, and India frameworks."
            ),
            "article": "Cross-jurisdictional gap (EU AI Act / NIST AI RMF / India DPDP)",
        })

    return flags
