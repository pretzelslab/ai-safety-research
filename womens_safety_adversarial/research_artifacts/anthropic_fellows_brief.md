# Anthropic Fellows Program — Research Brief

**Applicant:** Preethi Raghuveeran
**Research Title:** Adversarial Robustness in Women's Safety AI Systems: Threat Taxonomy, ZIDR Metric, and Governance Gap Analysis
**Date:** May 2026

---

## Opening

A safety app can achieve 95% accuracy on benchmark datasets and 0% effective detection in the zero-interaction window of a real attack.

This research names that gap. Closing it is the policy contribution of this work.

---

## The Problem

Women's safety apps are deployed in the highest-stakes conditions imaginable — public transit at night, isolated rural roads, workplaces where the adversary has institutional authority over the victim. They promise automatic detection: proximity alerts, distress sound classification, movement-triggered alerts. No button needed.

This promise has never been tested against an adversary.

Adversarial machine learning research assumes digital, anonymous attackers — or white-box access to model weights. Neither describes the real threat. The adversary in a women's safety context is physically present (0–50 metres), environmentally familiar (knows the space, the timing, the victim's patterns, the device she carries), and adaptive. She may know him. He may have cultural or institutional authority over her. He does not need to hack anything.

**The zero-interaction window** is where this matters most. In the 2–15 seconds between when a physical threat becomes active and when the victim loses the ability to interact with her device, detection depends entirely on passive systems: computer vision, audio classification, and sensor fusion. The layer that requires user input — typing, speaking, pressing a button — is unavailable by definition.

When a proximate adversary places a hand over a camera, generates ambient noise at the right frequency, or positions the encounter in a GPS dead zone, all three passive layers can fail simultaneously. No alert fires. The system produces a false-safe outcome at the exact moment of maximum danger.

No existing research studies this. Confirmed across nine sources. No existing governance framework governs it. Confirmed across five frameworks.

---

## The Research

This project has produced five concrete outputs:

**1. Threat Taxonomy**

A 4-layer attack surface framework (sensing → processing → communication → response) × 5 attack methods (suppress, corrupt, spoof, exhaust, intercept) × 6 adversary access levels.

Access Level 0 requires only physical proximity. No device contact. No technical knowledge. A structured hand over a camera lens qualifies. The taxonomy establishes that the most dangerous attacks require the least technical sophistication.

**2. Scenario Library**

13 grounded scenarios — 8 urban, 5 rural — anchored in Indian context. Each scenario maps to an attack method, an adversary access level, a deployment context, and a specific governance gap. Sources include NCRB Annual Reports (crime against women, state and district breakdowns) and Safetipin (urban street-level safety audit data, Indian cities).

**3. Governance Gap Analysis**

Five frameworks reviewed: EU AI Act, NIST AI RMF, ISO 42001, India Digital Personal Data Protection Act 2023, India IT Act.

Finding, consistent across all five: every framework evaluates AI systems on accuracy metrics measured with cooperative users. None require passive-detection-only testing. None address adversary-induced passive layer failures. None coordinate internationally on robustness standards for safety-critical AI. The gap is not a single missed clause — it is a structural absence.

**4. Zero-Interaction Detection Rate (ZIDR)**

A novel evaluation metric: the proportion of attack scenarios correctly detected and alerted without any user action, under adversary-induced passive-layer degradation conditions.

ZIDR is not in any existing benchmark, evaluation standard, or governance framework. It fills the gap between what systems are tested for and what they must do in real attacks. Any evaluation that includes a button press, a keyword, or a check-in response is testing a different system than the one that must function in the zero-interaction window.

**5. Probe Robustness Tool Specification**

A Python CLI design for evaluating any safety system profile against this taxonomy, with ZIDR as a first-class output metric. Specification complete; implementation is the next phase.

---

## Why This Is Novel

Three things make this contribution original:

**The adversary model.** Physically proximate, environmentally familiar, non-intimate, adaptive. This does not exist in adversarial machine learning literature, which assumes digital or white-box adversaries. It does not exist in human-computer interaction literature, which assumes cooperative users. The gap was confirmed across nine sources before this project began.

**ZIDR as a distinct evaluation criterion.** Existing robustness evaluations allow user-initiated triggers. Any evaluation that includes a button press, a keyword, or a check-in response is evaluating a different system than the one that must function in the extreme case. ZIDR forces the distinction. It does not exist in any published benchmark or standard.

**The sociotechnical attack surface.** Social conditioning — the cultural hesitation to trigger an alert against a known person, a colleague, or an authority figure — is an attack surface. An adversary with institutional or social authority over the victim does not need to disable the device. He can rely on the victim not triggering it. This is absent from every governance framework reviewed, and it is not a technical problem. It is a specification problem.

---

## Connection to Anthropic's Mission

Anthropic's work on AI safety focuses on ensuring that AI systems behave as intended — and do not cause harm when they fail. This research extends that framing into the physical deployment layer.

**Adversarial robustness.** The failure modes documented here are structurally analogous to model-level probe evasion. A physically proximate adversary defeating a passive detection system mirrors an input that causes a model to suppress its own safety signal. The underlying challenge — building systems that remain robust under adversarial conditions outside the training distribution — is the same.

**High-stakes deployment.** Safety-critical AI deployed in resource-constrained, high-noise, adversarial environments is exactly the context where specification gaps and distributional shift are most dangerous. Women's safety AI is already deployed in these conditions, at scale, without adversarial robustness standards.

**Policy contribution.** The EU AI Act requires conformity assessment for high-risk AI. Women's safety systems qualify under Annex III. But conformity assessment standards do not yet define what robustness means for passive detection under adversarial physical conditions. This research provides the missing definition, and the metric that makes it testable.

---

## Why I'm Building This

I came to AI safety research through product work and AI governance. For years, I built tools that used AI without systematically asking whether the AI was safe — or safe for whom. That question became urgent not abstractly, but when I started documenting what AI systems actually do in high-stakes deployments and who bears the cost when they fail.

Women's safety AI compresses the problem. It is AI deployed in the highest-stakes context, used by the most resource-constrained users, in the most adversarially demanding real-world conditions — and it is evaluated as if none of those conditions exist. The benchmark doesn't include the adversary. The certification doesn't require passive-only testing. The governance framework doesn't recognise the zero-interaction window.

I built this research because no one else had, and because I could see exactly where the gap was. The threat taxonomy, the scenario library, the governance analysis, the ZIDR metric — all of that is done. What the Fellows program enables is what independent research cannot sustain alone: ZIDR baseline measurement with real vendors, a policy brief that reaches the people writing EU AI Act implementing standards, and the time to take this to an academic venue.

---

## What Comes Next (with Fellows Support)

**ZIDR baseline measurement** — partner with 1–2 safety app vendors for controlled testing; establish whether ZIDR can be measured, what a plausible minimum threshold looks like, and what protocol others can replicate

**Policy brief** — targeted at CEN-CENELEC (EU AI Act technical standards body) and India's Bureau of Indian Standards; recommended clause language for conformity assessment standards governing passive-detection robustness

**Academic submission** — target FAccT 2027 or IEEE S&P; contribution: first threat taxonomy and novel evaluation metric for women's safety AI adversarial robustness

---

## Portfolio Context

This research is part of a broader body of work in adversarial robustness and AI fairness:

- **LLM Safety Evaluation Framework** — multi-dimensional safety benchmark across 5 harm categories; multi-vendor adapter design covering major frontier models; open-source
- **Fairness-under-quantization research** — 14.4 percentage point false positive rate disparity between Black and Other defendants in recidivism prediction is invariant to quantization: persists at FP32, INT8, and INT4 precision; bias is encoded in high-magnitude, quantization-stable neurons — making it resistant to post-training precision interventions; documents a safety-fairness tradeoff invisible to standard quantization benchmarks
- **Agent goal drift detection system** — real-time monitoring for autonomous agent goal drift; all 3 evaluation scenarios passing; open-source
- **Carbon-aware inference router** — safety-constrained routing with 45.5% carbon reduction and 100% fallback coverage; Zenodo preprint DOI: 10.5281/zenodo.19934621

**Published research:**

Raghuveeran, P. (2026). Adversarial Robustness in Women's Safety AI Systems: Threat Taxonomy, ZIDR Metric, and Governance Gap Analysis. Zenodo. https://doi.org/10.5281/zenodo.20028247

Raghuveeran, P. (2026). Carbon-Aware Inference Routing for Large Language Models: A Real-Time Framework for Sustainable AI Serving. Zenodo. https://doi.org/10.5281/zenodo.19934621

**Repository:** github.com/pretzelslab/ai-safety-research/tree/main/womens_safety_adversarial  
**GitHub:** github.com/pretzelslab  
**Email:** preeti.raghuveer@gmail.com
