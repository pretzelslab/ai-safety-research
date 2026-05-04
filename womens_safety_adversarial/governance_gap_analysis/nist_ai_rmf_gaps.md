# Governance Gap Analysis — NIST AI Risk Management Framework

## Framework Overview

The NIST AI Risk Management Framework (AI RMF 1.0, January 2023) is a voluntary US framework for managing AI-related risks. It is structured around four functions — GOVERN, MAP, MEASURE, MANAGE — and associated subcategories. Unlike the EU AI Act, it is non-binding but widely adopted as a de facto standard by US federal agencies, contractors, and international organisations.

**Why it matters for this research:** The NIST AI RMF is the most operationally detailed governance framework reviewed. Its MEASURE function includes specific guidance on accuracy, robustness, and evaluation methodology — making it the most directly applicable framework for assessing what robustness testing is currently expected vs. what is actually needed for women's safety AI.

---

## Current Coverage for Women's Safety AI

The NIST AI RMF does not classify AI systems by application type. It applies uniformly across all AI systems. Key relevant subcategories:

| Function | Subcategory | What It Requires |
|---|---|---|
| GOVERN 1.1 | Policies and processes for risk management | Organisation must have documented AI risk policies |
| GOVERN 6.1 | Policies for AI risk that includes sociotechnical concerns | Acknowledges sociotechnical risks; no specific test requirements |
| MAP 1.5 | Organisational risk tolerance | Requires contextual risk assessment |
| MAP 2.3 | AI system context and operational environment | Requires deployment context documentation |
| MEASURE 2.2 | AI system performance | Accuracy measurement required — no adversarial conditions specified |
| MEASURE 2.5 | Risks related to data quality and model performance | Performance monitoring required — no real-world attack scenario testing |
| MEASURE 2.6 | Bias testing | Fairness and bias evaluation across groups |
| MANAGE 2.2 | Mechanisms to respond to AI risks | Incident response planning required |

---

## Gap Analysis

| Attack Surface | Current NIST AI RMF Guidance | Specific Gap | Recommended Action |
|---|---|---|---|
| CV occlusion / lighting failure | MEASURE 2.5: performance monitoring — no occlusion conditions | No physical proximity attack test protocol | Add adversarial proximity test protocol to MEASURE 2.5 implementing guidance |
| Audio ambient noise failure | MAP 2.3: deployment context — no noise floor specification | Deployment context documentation does not require ambient noise calibration | Add noise calibration requirement to MAP 2.3 for audio-dependent safety systems |
| Sensor fusion dead zone | MAP 2.3: operational environment — connectivity not specified | Rural dead zone compound failure not addressed | Require minimum connectivity disclosure and fallback mode documentation under MAP 2.3 |
| NLP coercion bypass | GOVERN 6.1: sociotechnical — acknowledged but not operationalised | No test protocol for coerced-neutral-response or non-cooperative user state | Operationalise GOVERN 6.1 with specific coercion-scenario test requirements for safety-critical NLP |
| Zero-interaction window | Not addressed anywhere in AI RMF 1.0 | No passive-only detection accuracy requirement | Add ZIDR as a MEASURE 2.5 metric for safety-critical systems with passive detection modes |
| Exhaustion attacks on response layer | MANAGE 2.2: incident response — alert exhaustion not modelled | Contact response degradation over time not recognised as a failure mode | Add exhaustion-resistance testing to MANAGE 2.2 for safety notification systems |

---

## Key Findings

### Finding 1 — Sociotechnical Risk Is Acknowledged, Not Operationalised
GOVERN 6.1 explicitly acknowledges that "AI risks and benefits can be impacted by sociotechnical factors." This is the most forward-looking provision in any framework reviewed. However, GOVERN 6.1 stops at acknowledgement — it provides no test protocol, no minimum requirement, no definition of what "assessing sociotechnical risk" requires in practice.

For women's safety AI, sociotechnical suppression (social coercion preventing alert trigger, authority asymmetry, cultural hesitation) is the most common and most dangerous failure mode. GOVERN 6.1 names the problem and leaves it entirely unresolved. **The gap is not conceptual — it is operational.**

### Finding 2 — MEASURE Function Assumes Cooperative Users
All MEASURE subcategories evaluate model performance on test datasets or in monitored production conditions. None specify evaluation under adversarial physical conditions or non-cooperative user states. MEASURE 2.5 (risks related to data quality) and MEASURE 2.2 (AI system performance) both measure accuracy — but accuracy against benchmark datasets tells us nothing about performance in the zero-interaction window.

**A system that scores 0.93 F1 on a benchmark can score 0.0 ZIDR in a real attack. The NIST AI RMF has no mechanism to detect or prevent this.**

### Finding 3 — MAP Function Does Not Require Adversarial Deployment Context Modelling
MAP 2.3 requires documentation of "AI system context and operational environment." In practice, this means recording what environment the system is designed for — not what adversarial conditions it must withstand in that environment. A deployment context of "urban public spaces" does not trigger any requirement to test against crowded-transit sensor fusion failure or outdoor ambient noise suppression.

### Finding 4 — MANAGE Function Does Not Model Alert System Degradation
MANAGE 2.2 requires mechanisms to respond to AI risks — typically meaning incident response for model failures or drift. Alert exhaustion (the cry wolf effect, documented in threat_taxonomy/) is a form of system degradation over time that the MANAGE function does not recognise. As contacts become conditioned to dismiss alerts, the effective performance of the safety system degrades even as the model continues to function correctly.

---

## Recommended Actions

1. **MEASURE 2.5 addendum:** Issue sector-specific guidance requiring adversarial test protocols for personal safety AI — including passive-detection-only test runs (ZIDR), ambient noise floor testing (ANEF), and occlusion evasion threshold (OET) measurement.

2. **GOVERN 6.1 operationalisation:** Publish implementing guidance that translates sociotechnical risk acknowledgement into specific test requirements — at minimum, coerced-neutral-response NLP tests and authority-asymmetry scenario modelling for safety check-in systems.

3. **MAP 2.3 adversarial context requirement:** Require that deployment context documentation includes not just the operational environment but the adversarial conditions present in that environment — ambient noise levels, network reliability, GPS availability, and relevant physical proximity attack vectors.

4. **MANAGE 2.2 exhaustion resistance:** Add alert exhaustion and contact response degradation as recognised AI failure modes under the MANAGE function, with monitoring requirements for systems where repeated false alerts are a plausible adversary strategy.

---

## Connection to Zero-Interaction Window

The NIST AI RMF is the only framework reviewed that explicitly acknowledges sociotechnical risk (GOVERN 6.1). This makes it the best candidate framework for incorporating the zero-interaction window as a formal evaluation requirement. 

Proposed NIST AI RMF addition:

> **MEASURE 2.5.1 (proposed):** For AI systems with passive detection modes intended to operate without user action, organisations should evaluate Zero-Interaction Detection Rate (ZIDR) — the proportion of threat scenarios detected and alerted without user input, under adversary-induced sensor degradation conditions representative of the deployment context.

This addition would not require a full revision of AI RMF 1.0 — it could be issued as a sector profile for personal safety AI systems, consistent with the framework's existing sector-profile mechanism.
