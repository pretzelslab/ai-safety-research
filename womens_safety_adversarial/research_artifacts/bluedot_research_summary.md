# Research Summary — Frontier AI Governance

**Researcher:** Preethi Raghuveeran
**Research Title:** Adversarial Robustness in Women's Safety AI: Where Safety Certification Fails
**Program context:** BlueDot Impact — Frontier AI Governance
**Date:** May 2026

---

## The Research Question

Women's safety apps — AI systems that automatically detect proximity threats, distress sounds, and sudden movement — are deployed at scale across India, Europe, and Southeast Asia. They are classified as high-risk AI under the EU AI Act. Conformity assessment is required before deployment.

This research asks: what does conformity assessment miss, and what happens when it misses it?

---

## The Gap This Research Documents

**Standard evaluation assumes a cooperative user.**

Every accuracy metric — precision, recall, F1 score — is measured under conditions where the user is available to interact with the device: press a button, speak a keyword, respond to a check-in. Even passive detection benchmarks are run without an active adversary.

**Real attacks do not include cooperative users.**

The zero-interaction window is the 2–15 second period between when a physical threat becomes active and when the victim loses the ability to interact with her device. During this window, only passive systems are available: computer vision, audio classification, and sensor fusion. A physically proximate adversary can suppress all three simultaneously — no technical knowledge required, no device access needed.

When this happens, no alert fires. The system is certified as safe. It fails at the moment it is needed most.

This gap is what the **Zero-Interaction Detection Rate (ZIDR)** measures: the proportion of attack scenarios correctly detected and alerted without any user action, under adversary-induced passive-layer degradation conditions.

No current evaluation standard measures ZIDR. No current governance framework requires it.

---

## Governance Findings

**EU AI Act**

Women's safety systems qualify as high-risk AI under Annex III (biometric identification and categorisation systems). Conformity assessment is mandatory. However, the harmonised standards being developed by CEN-CENELEC do not define robustness requirements for passive-detection-only operational modes. A system with a ZIDR of 0% passes conformity assessment if its aggregate accuracy meets the threshold.

**NIST AI RMF**

The Govern, Map, Measure, and Manage functions provide a comprehensive risk framework. But robustness measurement — the Measure function — assumes testable accuracy under standard operating conditions. Adversary-induced passive-layer degradation is not a defined test scenario in any NIST guidance reviewed.

**ISO 42001**

The AI management system standard requires risk assessment and ongoing monitoring. It does not require adversarial robustness testing. Physical proximity adversary scenarios are not a defined risk category under any ISO 42001 annex reviewed.

**India DPDP Act 2023 and IT Act**

India's data protection and digital safety provisions address data handling and online harm respectively. Neither addresses AI system robustness under adversarial physical conditions. Women's safety AI is not specifically governed under either framework.

**Cross-jurisdictional gap**

No coordination mechanism exists between EU, US, and Indian standards bodies on adversarial robustness requirements for safety-critical AI. A system certified under EU AI Act conformity assessment is not required to meet any equivalent Indian standard — because no equivalent Indian standard exists. Regulatory arbitrage is possible and currently ungoverned.

---

## The Policy Contribution

**A new evaluation metric:** Zero-Interaction Detection Rate (ZIDR) — proposed for inclusion in EU AI Act conformity assessment standards (Article 15 implementing guidance) and NIST AI RMF measurement guidance. Definition: the proportion of attack scenarios correctly detected and alerted without any user action, under adversary-induced passive-layer degradation conditions.

**Clause language recommendation:** CEN-CENELEC harmonised standards for high-risk AI robustness should include a mandatory ZIDR measurement requirement for any safety-critical system with passive detection capability. Minimum acceptable threshold: to be established by ZIDR baseline measurement (proposed next phase).

**International coordination gap:** No standards body currently owns the problem of cross-jurisdictional alignment on passive-detection robustness for safety-critical AI. A joint working group between CEN-CENELEC, NIST, and India's Bureau of Indian Standards is the appropriate structure. This research is a proposed input to that process.

---

## Connection to Frontier AI Governance Themes

This research connects directly to three challenges at the centre of the Frontier AI Governance curriculum:

**Standards lag behind deployment.** Women's safety AI is already deployed at scale in high-risk conditions. The standards that should govern it — particularly on adversarial robustness for passive detection — do not yet exist in the form needed. This is not a future problem. It is a current one.

**High-risk AI in under-resourced contexts.** The users most dependent on these systems — women in rural India with limited network connectivity, women in contexts where triggering an alert carries social risk — are the least represented in standards development processes. Governance that does not account for constrained deployment environments will fail precisely where it is most needed.

**Multi-stakeholder coordination failure.** Closing the ZIDR gap requires vendors to expose systems for adversarial testing, standards bodies to define what constitutes acceptable passive-detection robustness, civil society to represent affected users, and researchers to produce the measurement methodology. Currently, none of these actors share a common framework. This research is an attempt to provide one.

---

## What I'm Looking For from the Cohort

- **Governance review:** peer feedback on the clause language recommendations for CEN-CENELEC and NIST — are they technically precise enough to be actionable?
- **Stakeholder introductions:** connections to EU AI Act standards working groups, India DPDP delegated acts process, or NIST AI RMF development teams
- **Publication venue guidance:** which policy-facing journals or outlets most effectively reach standards bodies and regulators?

---

## Researcher Background

Preethi Raghuveeran is an independent AI safety researcher with a portfolio of adversarial robustness and AI fairness tools, all published openly:

- LLM safety evaluation framework — multi-vendor, 5 harm categories, open-source
- Fairness-under-quantization research — 14.4 percentage point false positive rate disparity between Black and Other defendants is invariant to quantization (FP32, INT8, INT4); bias encoded in quantization-stable high-magnitude neurons
- Agent goal drift detection system — real-time monitoring for autonomous agents
- Carbon-aware inference router — safety-constrained routing; Zenodo preprint DOI: 10.5281/zenodo.19934621

**Published research:**

Raghuveeran, P. (2026). Adversarial Robustness in Women's Safety AI Systems: Threat Taxonomy, ZIDR Metric, and Governance Gap Analysis. Zenodo. https://doi.org/10.5281/zenodo.20028247

Raghuveeran, P. (2026). Carbon-Aware Inference Routing for Large Language Models: A Real-Time Framework for Sustainable AI Serving. Zenodo. https://doi.org/10.5281/zenodo.19934621

**Repository:** github.com/pretzelslab/ai-safety-research/tree/main/womens_safety_adversarial  
**GitHub:** github.com/pretzelslab  
**Email:** rangchampak@gmail.com
