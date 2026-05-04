# Adversarial Robustness in Women's Safety AI Systems

**Researcher:** Preethi Raghuveeran | Independent AI Safety Researcher  
**Status:** Complete ✅ — All 6 phases built and published  
**Zenodo DOI:** [10.5281/zenodo.20028247](https://doi.org/10.5281/zenodo.20028247)  
**Primary artifact for:** Anthropic Fellows Program · BlueDot Impact Frontier AI Governance

---

## Research Question

How can a physically proximate adversary with environmental familiarity defeat AI-enabled women's safety systems — and what governance frameworks fail to prevent this?

## Why This Gap Exists

Adversarial ML literature assumes anonymous digital attackers or white-box model access. Neither maps onto the real-world threat landscape for women's safety AI, where the adversary is frequently:
- Physically present (0–50 metres)
- Environmentally familiar — knows the space, victim patterns, timing
- Known but non-intimate (acquaintance, colleague, authority figure)
- Capable of adaptive behavior based on observed system responses in real time

No existing research systematically examines this threat model. Confirmed across 9 sources. This is the gap.

## Repository Structure

```
threat_taxonomy/        — attack surfaces, adversary profiles, scenario library
ai_subsystem_mapping/   — vision / audio / sensor / language attack analysis
governance_gap_analysis/— EU AI Act, NIST AI RMF, India DPDP, ISO 42001, cross-jurisdictional
probe_robustness/       — evaluation methodology and tool specification
research_artifacts/     — Fellows brief, grant application, one-pager
data/                   — incident patterns, existing systems reviewed
```

## Research Principles

- Accuracy over completeness
- Grounded in Indian urban + rural context
- Sociotechnical, not just technical — social conditioning is an attack surface
- Every attack surface connects to at least one governance gap
- No fabricated citations — `[CITATION NEEDED: source]` where unknown

## Citation Sources
- NCRB Annual Reports (ncrb.gov.in) — crime against women statistics, state/district breakdowns
- iCall / iHuman NGO — psychosocial helpline incident patterns (Mumbai / urban India)
- Safetipin — street-level safety audit data, Indian cities
