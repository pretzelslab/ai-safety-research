# Governance Gap Analysis — ISO 42001

## Framework Overview

ISO/IEC 42001:2023 is the first international standard for AI Management Systems (AIMS). Published December 2023, it provides requirements for establishing, implementing, maintaining, and continually improving an AI management system within an organisation. It follows the high-level structure (HLS) of other ISO management system standards (ISO 9001, ISO 27001), making it integrable with existing quality and security frameworks.

**Why it matters for this research:** ISO 42001 is positioned to become the global operational standard for AI governance in organisations — equivalent to ISO 27001 for information security. Unlike the EU AI Act (regulatory) or NIST AI RMF (advisory), ISO 42001 certification is auditable and increasingly expected by enterprise procurement, insurance, and government contracting. Understanding its gaps determines what a certified women's safety AI developer is and is not required to do.

**Scope note:** ISO 42001 governs the management system of an AI-deploying organisation — not the AI model itself. It does not mandate specific accuracy thresholds or adversarial test protocols. It requires that the organisation have a documented, implemented, and auditable process for managing AI risks.

---

## Current Coverage for Women's Safety AI

| Clause | Title | What It Requires | Applicability |
|---|---|---|---|
| 4.1 | Understanding the organisation | Identify internal/external context relevant to AI | Requires identifying deployment context — not adversarial conditions |
| 4.2 | Understanding needs of interested parties | Identify stakeholder requirements | Could require identifying end-user safety needs — not operationalised |
| 6.1 | Actions to address risks and opportunities | Risk identification and treatment | Requires documented risk assessment — no adversarial AI attack surface requirement |
| 6.2 | AI objectives | Set measurable AI performance objectives | Requires objectives — no minimum robustness level defined |
| 8.4 | AI system lifecycle | Manage AI system through lifecycle | Covers development, deployment, operation — no adversarial testing phase required |
| 9.1 | Monitoring, measurement, analysis, evaluation | Performance monitoring | Requires ongoing monitoring — no adversarial probe or ZIDR measurement |
| 10.2 | Nonconformity and corrective action | Respond to failures | Requires corrective action for identified failures — no proactive failure discovery |

---

## Gap Analysis

| Attack Surface | ISO 42001 Coverage | Specific Gap | Recommended Addition |
|---|---|---|---|
| CV occlusion / proximity failure | Clause 6.1: risk identified if documented — not required | No requirement to identify physical proximity as a risk category | Annex A control: adversarial physical environment testing required for safety-critical CV |
| Audio ambient noise failure | Clause 8.4: lifecycle management — test conditions not specified | No deployment-context noise calibration in lifecycle requirements | Require ambient noise calibration data as a lifecycle artifact for audio-dependent AI |
| Sensor fusion dead zone | Clause 4.1: external context — connectivity not explicitly required | Rural connectivity gap not recognised as an external context factor | Require minimum operational connectivity to be documented and disclosed under Clause 4.1 |
| NLP coercion bypass | Clause 4.2: stakeholder needs — victim coercion not modelled | Stakeholder analysis assumes cooperative end users | Add adversarial-user-state scenario to Clause 4.2 stakeholder requirements for safety AI |
| Zero-interaction window | Not addressed — no passive-detection evaluation requirement | No clause requires testing without user action | New Annex A control for passive-detection-only evaluation (ZIDR) |
| Exhaustion attack on response layer | Clause 9.1: monitoring — alert degradation not a recognised metric | Contact response rate degradation not a monitored performance indicator | Add exhaustion-resistance monitoring to Clause 9.1 for safety notification systems |

---

## Key Findings

### Finding 1 — Process Compliance ≠ Safety Performance
ISO 42001's fundamental structure is process-based, not outcome-based. An organisation can achieve full ISO 42001 certification by documenting its risk management processes, setting AI objectives, monitoring performance, and responding to identified failures — without ever testing whether its women's safety AI detects a threat in the zero-interaction window.

**ISO 42001 certification does not mean the AI works. It means the organisation has documented processes for managing the AI.** For women's safety applications, this distinction is life-safety critical.

### Finding 2 — Risk Identification Is Self-Directed
Clause 6.1 requires organisations to identify AI risks and opportunities. The standard does not specify what risks must be identified — it is left to the organisation. An organisation developing a women's safety app can complete a Clause 6.1 risk assessment that omits CV occlusion, audio noise suppression, GPS dead zones, and sociotechnical coercion — and be fully ISO 42001 compliant. The standard has no minimum risk category requirement for safety-critical AI applications.

### Finding 3 — Annex A Controls Are Voluntary
ISO 42001 includes an Annex A with a set of AI-specific controls (similar to ISO 27001 Annex A for security). These controls address fairness, transparency, data quality, and related concerns — but include no controls for physical-world adversarial robustness, passive detection performance, or zero-interaction window testing. Annex A controls are voluntary — organisations apply them "as applicable" based on their own risk assessment.

### Finding 4 — Lifecycle Requirements Do Not Specify Adversarial Testing Phase
Clause 8.4 governs the AI system lifecycle (design, development, testing, deployment, monitoring, decommission). It does not require an adversarial testing phase. A women's safety AI can complete the ISO 42001 lifecycle process — designed, tested, deployed, monitored — with all testing conducted on benchmark datasets under cooperative conditions. The standard has no mechanism to require the kind of physical proximity, ambient noise, or coercion-scenario testing documented in this research.

---

## Recommended Additions

1. **New Annex A control — Adversarial deployment context testing:** For AI systems deployed in personal safety applications, add a control requiring adversarial test protocols covering the deployment context's physical conditions (ambient noise, occlusion, network reliability, GPS availability).

2. **Clause 6.1 minimum risk categories for safety-critical AI:** Issue sector guidance specifying minimum risk categories that must be assessed for personal safety AI — including physical proximity attack surfaces, passive-detection failure modes, sociotechnical suppression, and rural connectivity gaps.

3. **Clause 8.4 adversarial testing phase:** Add an adversarial testing phase to the lifecycle requirements for high-risk personal safety applications — requiring testing under real-world conditions representative of the deployment context.

4. **Clause 9.1 ZIDR monitoring:** Add Zero-Interaction Detection Rate as a required performance metric for safety-critical AI systems with passive detection modes.

5. **Clause 4.2 adversarial stakeholder model:** Require that stakeholder analysis for safety AI includes not only the cooperative end user but also the adversarial scenarios — victim under coercion, non-cooperative user state — as part of understanding stakeholder needs.

---

## Connection to Zero-Interaction Window

ISO 42001's process-based structure makes it the most tractable framework for incorporating the zero-interaction window as a systematic requirement — because it governs the organisation's entire AI management process, not just specific model metrics.

Specifically: adding ZIDR to Clause 9.1 monitoring requirements would mean any ISO 42001-certified women's safety AI developer must measure, document, and respond to passive-detection-only performance. This would create a continuous improvement obligation around the zero-interaction window — not just a one-time test.

**Of all frameworks reviewed, ISO 42001 has the most potential to operationalise zero-interaction window testing at scale — because it embeds the requirement in the ongoing management system, not just a conformity assessment point-in-time.**
