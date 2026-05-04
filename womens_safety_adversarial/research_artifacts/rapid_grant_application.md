# Grant Application
## Adversarial Robustness in Women's Safety AI: ZIDR Measurement and Policy Translation

**Applicant:** Preethi Raghuveeran, Independent AI Safety Researcher
**Date:** May 2026
**Relevant funders:** Long-Term Future Fund · Survival and Flourishing Fund · Longview Philanthropy

---

## Research Question

How can a physically proximate adversary with environmental familiarity defeat AI-enabled women's safety systems — and what specific changes to AI governance standards would close this gap?

---

## Why This Matters

Women's safety AI systems — apps that automatically detect threat proximity, distress sounds, and sudden movement — are deployed at scale across India, Europe, and Southeast Asia. They are classified as high-risk AI under the EU AI Act, requiring conformity assessment. Millions of users rely on them in the highest-stakes conditions.

These systems have never been evaluated against a physically proximate adversary.

**The zero-interaction window** is the 2–15 second period between when a physical threat becomes active and when the victim loses the ability to interact with her device. During this window, detection depends entirely on passive systems: computer vision, audio classification, and sensor fusion. The layer that requires user input — typing, speaking, pressing a button — is unavailable by definition.

When a proximate adversary occludes the camera, generates ambient noise, or positions the encounter in a GPS dead zone, all three passive layers can fail simultaneously. No alert fires.

A system can achieve 95% accuracy in benchmark testing and 0% effective detection in this window. This gap is what the Zero-Interaction Detection Rate (ZIDR) measures. No existing evaluation standard measures ZIDR. No current governance framework requires it.

---

## What Has Already Been Built (No Funding Required)

This research is substantially complete. The following have been produced as independent, unfunded work:

- **Threat taxonomy** — 4-layer attack surface classification × 5 attack methods × 6 adversary access levels; Access Level 0 requires only physical proximity, no device contact, no technical knowledge
- **Scenario library** — 13 grounded scenarios (8 urban, 5 rural) anchored in Indian context, drawing on NCRB Annual Reports for incident patterns
- **AI subsystem mapping** — failure modes documented for computer vision, audio classification, sensor fusion, and language/NLP layers
- **Governance gap analysis** — specific ungoverned attack surfaces identified across EU AI Act, NIST AI RMF, ISO 42001, and India DPDP Act 2023
- **ZIDR metric** — novel evaluation criterion defined, documented, and connected to the governance gap
- **Probe robustness tool specification** — Python CLI design for evaluating safety system profiles against this taxonomy

This application requests funding for the next phase only: empirical ZIDR measurement and policy translation.

---

## What Funding Would Enable

### Output 1 — ZIDR Baseline Measurement

Work with 1–2 existing women's safety app vendors to conduct the first empirical measurement of ZIDR under adversary-induced passive-layer degradation conditions. Specifically:

- Structured access to a controlled test environment
- Execution of scenarios from the established threat taxonomy
- Baseline ZIDR measurement across 4 attack surface layers
- A replicable measurement protocol, published openly

This is not a full academic study. It establishes whether ZIDR can be measured, what a plausible minimum acceptable threshold looks like, and what protocol allows others to replicate it.

### Output 2 — Policy Brief

A 10–15 page policy brief targeted at CEN-CENELEC (the EU technical standards body responsible for AI Act implementing standards) and India's Bureau of Indian Standards. The brief will:

- Define ZIDR with precision sufficient for inclusion in a conformity assessment standard
- Recommend specific clause language for the EU AI Act implementing regulation on high-risk AI robustness (Article 15)
- Propose a minimum acceptable ZIDR threshold for safety-critical passive-detection systems

### Output 3 — Public Research Artifact

Full research brief published to Zenodo with an open DOI, freely accessible and citable. Submitted to a relevant academic venue — target: FAccT 2027 or IEEE S&P.

---

## Timeline

| Month | Activity |
|---|---|
| 1–2 | Vendor outreach and test environment setup |
| 3–4 | ZIDR baseline measurement (2 vendors) |
| 5 | Analysis, measurement protocol write-up, policy brief drafting |
| 6 | Publication and academic submission |

---

## Researcher Background

Preethi Raghuveeran is an independent AI safety researcher with a portfolio of adversarial robustness and fairness tools, all built and published openly:

- **LLM Safety Evaluation Framework** — multi-dimensional safety evaluation across 5 harm categories; multi-vendor adapter design covering major frontier models
- **Fairness-under-quantization research** — 14.4 percentage point false positive rate disparity between Black and Other defendants persists invariantly across FP32, INT8, and INT4 precision levels; bias encoded in high-magnitude, quantization-stable neurons; published to Zenodo
- **Agent goal drift detection system** — real-time monitoring for autonomous agent goal drift; all 3 evaluation scenarios passing
- **Carbon-aware inference router** — safety-constrained model routing achieving 45.5% carbon reduction; Zenodo preprint DOI: 10.5281/zenodo.19934621

**Published research:**

Raghuveeran, P. (2026). Adversarial Robustness in Women's Safety AI Systems: Threat Taxonomy, ZIDR Metric, and Governance Gap Analysis. Zenodo. https://doi.org/10.5281/zenodo.20028247

Raghuveeran, P. (2026). Carbon-Aware Inference Routing for Large Language Models: A Real-Time Framework for Sustainable AI Serving. Zenodo. https://doi.org/10.5281/zenodo.19934621

**Repository:** github.com/pretzelslab/ai-safety-research/tree/main/womens_safety_adversarial  
**Target programs:** Anthropic Fellows Program · BlueDot Impact Frontier AI Governance  
**GitHub:** github.com/pretzelslab  
**Email:** preeti.raghuveer@gmail.com
