# Governance Gap Analysis — India Regulatory Landscape

## Framework Overview

India does not have a comprehensive AI regulation equivalent to the EU AI Act. The regulatory landscape for AI-enabled women's safety systems is fragmented across three instruments:

1. **Digital Personal Data Protection Act 2023 (DPDP Act)** — data protection legislation, enacted August 2023, rules under development
2. **Information Technology Act 2000 (IT Act)** — baseline digital safety and cybercrime legislation
3. **MeitY AI Advisory (February 2023)** — advisory (non-binding) requiring approval for "unreliable or untested" AI with potential harm to citizens

Women's safety AI in India is additionally shaped by:
- **BIS IS 2061** and related standards — applicable to electronic safety devices, not AI systems
- **National Commission for Women (NCW)** — oversight of women's safety policy, no AI certification mandate
- **Safe City projects** — government-funded CV/AI deployments in 8 cities (Delhi, Mumbai, Lucknow, Kolkata, Chennai, Ahmedabad, Bengaluru, Hyderabad) under Nirbhaya Fund; no published AI quality standard

**Why it matters for this research:** India is the primary deployment context for this research. Women's safety AI deployed in India faces the highest real-world risk (documented incident rates, infrastructure limitations, rural-urban gap) and the least regulatory requirement for robustness.

---

## Current Coverage for Women's Safety AI

### DPDP Act 2023

| Provision | What It Covers | Applicability to Safety AI |
|---|---|---|
| Section 4 — Consent | Lawful basis for personal data processing | Safety apps processing location, audio, video must obtain consent |
| Section 8 — Data Fiduciary obligations | Accuracy, completeness, data quality | Requires data accuracy — not model accuracy or adversarial robustness |
| Section 9 — Children's data | Special protection for data of minors | Relevant if safety app used by minors |
| Section 16 — Data Protection Board | Enforcement and complaints | Provides grievance mechanism — not proactive robustness oversight |

**Critical gap:** DPDP Act governs what happens to data collected by the safety app. It does not govern whether the safety app's AI models work correctly, robustly, or at all under adversarial conditions. A safety app can collect biometric data lawfully and still produce zero effective detections in the zero-interaction window — fully DPDP compliant.

### IT Act 2000

| Provision | What It Covers | Applicability to Safety AI |
|---|---|---|
| Section 43A — Compensation for failure to protect data | Liability for negligent data protection | Could apply if safety app data breach occurs |
| Section 66C — Identity theft | Offence for fraudulent use of identity | Relevant if adversary spoofs victim's device identity |
| Section 66E — Violation of privacy | Offence for capturing private images | Could apply to adversary using victim's camera access |

**Critical gap:** IT Act provisions address offences after the fact. They do not establish proactive quality requirements for AI safety systems. There is no provision governing adversarial robustness, operational failure modes, or minimum detection performance.

### MeitY AI Advisory (February 2023)

The advisory requires platforms with "significant risk of harm to citizens" to obtain government approval before deploying "unreliable or untested" AI. This is:
- Non-binding
- Not operationalised (no definition of "reliable" or "tested" for safety AI)
- Not enforced

---

## Gap Analysis

| Attack Surface | Current India Regulatory Coverage | Specific Gap | Recommended Action |
|---|---|---|---|
| CV failure in crowded transit | None — no AI quality standard | No robustness requirement of any kind | MeitY to issue sector standard for safety-critical AI: mandatory OET measurement |
| Audio failure at Indian urban noise levels | None | Indian-calibrated ambient noise baselines not required | Require ANEF testing calibrated to Indian urban noise data (CPCB benchmarks) |
| Sensor fusion dead zone (rural R2) | None | Rural coverage gap compound failure not addressed by any instrument | Mandate offline fallback mode disclosure for safety apps deployed in rural areas |
| NLP coercion bypass | None | No requirement of any kind for NLP safety check-in robustness | MeitY/NCW joint guidance on sociotechnical attack surfaces in safety AI |
| Zero-interaction window | None | Not addressed anywhere in Indian regulatory landscape | Add ZIDR to any future AI safety standard for personal safety apps |
| Safe City AI deployments | Nirbhaya Fund project criteria — procurement-only, no post-deployment quality standard | Government-funded CV deployments have no mandatory robustness standard | Establish post-deployment audit requirement for Nirbhaya Fund AI procurement |

---

## Key Findings

### Finding 1 — No AI Quality Standard Exists in India for Women's Safety Applications
Neither DPDP Act, IT Act, MeitY advisory, nor any BIS standard imposes a minimum quality, robustness, or adversarial-resilience requirement on AI systems marketed for women's personal safety. Any app can be sold as an AI-powered women's safety product in India with zero tested detection capability.

### Finding 2 — The Rural Deployment Gap Is the Most Severe Unaddressed Risk
Rural contexts (R2) combine the highest adversarial risk (isolated, no bystanders, weak institutional response) with the worst infrastructure conditions (no network, no GPS, no fallback). India has approximately 833,000 villages, many with intermittent or absent mobile coverage. **[CITATION NEEDED: TRAI 2023 rural connectivity data]**. No Indian regulation requires safety apps to disclose whether they function in low-connectivity rural deployments or mandate offline fallback capability. This is the largest absolute safety gap in the Indian regulatory landscape.

### Finding 3 — Safe City Deployments Are Unaudited Post-Procurement
The Nirbhaya Fund has allocated approximately ₹2,919 crore to Safe City projects deploying AI-enabled surveillance and safety infrastructure across 8 cities. **[CITATION NEEDED: MHA/MoWCD Safe City project allocation data]**. Procurement criteria govern vendor selection — but no post-deployment audit standard requires ongoing robustness verification. These are government-operated CV systems in high-population urban contexts with no published accuracy benchmark, no adversarial test requirement, and no published failure mode documentation.

### Finding 4 — Data Protection ≠ Operational Safety
The DPDP Act is a sophisticated data protection instrument. It does not govern operational AI quality. The distinction matters: an app that collects location data with lawful consent, stores it securely, and processes it lawfully can still fail to detect a threat during a physical attack. Data protection compliance tells us nothing about detection performance.

### Finding 5 — No Cross-State Coordination Mechanism
Women's safety incidents in India frequently cross state boundaries (transit harassment on intercity routes, cross-state abduction scenarios). No regulatory mechanism coordinates AI safety quality standards across state jurisdictions. A safety app certified (hypothetically) by one state has no mutual recognition in another.

---

## Recommended Actions

1. **MeitY AI safety sector standard:** Issue a binding standard for AI systems marketed as personal safety tools — requiring minimum robustness documentation, adversarial test results, and deployment context limitations disclosure. Priority: CV (OET), Audio (ANEF), Sensor Fusion (SFES), and ZIDR as mandatory outputs.

2. **Rural deployment disclosure mandate:** Require any safety app sold or deployed in India to disclose explicitly: minimum network coverage required, GPS availability requirement, and whether offline fallback mode exists. Enforce under Consumer Protection Act 2019 (misleading claims about product capabilities).

3. **Nirbhaya Fund post-deployment audit:** Establish an independent technical audit requirement for all Nirbhaya Fund AI deployments — annual robustness verification against published attack surface framework (this research can serve as the basis).

4. **NCW / MeitY joint sociotechnical guidance:** Issue guidance recognising sociotechnical suppression (social coercion, authority asymmetry, cultural hesitation) as an AI safety failure mode requiring design attention — not just technical robustness.

5. **Rural connectivity minimum standard:** In coordination with TRAI and DoT, establish a minimum connectivity SLA for geographic areas designated for women's safety AI deployment under government programmes.

---

## Connection to Zero-Interaction Window

India presents the most severe zero-interaction window risk of any jurisdiction covered in this research:
- Highest ambient noise in urban deployments (passive audio detection severely degraded)
- Largest rural dead zone coverage gap (passive sensor fusion and alert transmission both fail)
- No regulatory requirement of any kind for passive detection performance

A woman in a rural Indian context using a government-recommended safety app may have zero effective protection during a physical attack — with no regulator aware this is the case, no standard that would reveal it, and no enforcement mechanism that could address it.

**This is the central policy finding of this research: the countries and contexts with the greatest need for effective women's safety AI have the least regulatory capacity to ensure it works.**
