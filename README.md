# AI Safety Research

Independent research and evaluation frameworks for responsible AI deployment.

Built by [Preethi Raghuveeran](https://preetibuilds-33d6f6da.vercel.app) — AI governance practitioner focused on operationalising fairness, safety, and compliance in production AI systems.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20028247.svg)](https://doi.org/10.5281/zenodo.20028247) — Women's Safety Adversarial Robustness  
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19934621.svg)](https://doi.org/10.5281/zenodo.19934621) — Carbon-Aware Inference Router

---

## Projects

### [Women's Safety Adversarial Robustness](./womens_safety_adversarial/)

Research into how physically proximate adversaries defeat AI-enabled women's safety systems — and which governance frameworks fail to prevent this.

Produces a 4-layer threat taxonomy × 5 attack methods × 6 adversary access levels, a scenario library of 13 grounded Indian-context scenarios, governance gap analysis across EU AI Act / NIST AI RMF / ISO 42001 / India DPDP, and a novel evaluation metric: **Zero-Interaction Detection Rate (ZIDR)**.

**Finding:** No existing governance framework requires passive-detection-only robustness testing. Every framework evaluates AI systems against cooperative users. ZIDR names and measures the gap.

Primary artifact for Anthropic Fellows Program application.  
**Zenodo DOI:** [10.5281/zenodo.20028247](https://doi.org/10.5281/zenodo.20028247)

---

### [FT9: Proxy Discrimination Under Quantization](./FT9_Proxy_Discrimination_Under_Quantization.md)

Investigates whether model quantization disproportionately harms already-disadvantaged groups in high-stakes prediction.

Trained RecidivismNet (740 parameters) on the COMPAS dataset and measured racial fairness at FP32, INT8, and INT4 precision. Conducted neuron-level attribution to identify the mechanism.

**Finding:** The 14.4 percentage point false positive rate disparity between Black and Other defendants is invariant to quantization — it persists at all three precision levels. Bias is encoded in high-magnitude neurons, which are inherently more quantization-stable. Making a model smaller does not make it fairer.

---

### [SA1: Carbon-Aware Inference Router (CAIR)](./sa1-carbon-inference-router/)

A safety-constrained routing system that selects the smallest model capable of handling each query — reducing carbon cost without degrading output quality below threshold.

**Eval results (50 test cases, 2026-05-02):** 45.5% carbon reduction vs always-large baseline · routing precision 100%/90%/100% across complexity tiers · P95 latency 0.09ms · 100% fallback reliability.

Zenodo preprint DOI: [10.5281/zenodo.19934621](https://doi.org/10.5281/zenodo.19934621)

---

### [AC1: Rogue Agent & Goal Drift Detector](./ac1-agent-drift-detector/)

Real-time monitoring system for autonomous agent goal drift. Scores each agent step against the original task intent using semantic similarity; flags DRIFTING (score 0.62–0.77) and ROGUE (score < 0.62) states with human-in-the-loop escalation.

**Eval results:** All 3 evaluation scenarios passing — safe task, goal-drifting task, and rogue exfiltration task correctly classified.

---

### [AC4: Agent Goal Hijacking Demo](./ac4-agent-hijacking/)

Demonstration of adversarial goal hijacking in a multi-step autonomous agent pipeline. Shows how an injected secondary objective (exfiltrate records, write cover report) can be introduced mid-task without triggering standard output filters.

Includes Phase 2 detection layer and human-in-the-loop review workflow.

---

### [COMPAS Safety Evaluation Runbook](./COMPAS_Safety_Eval_Runbook.md)

A structured deployment evaluation framework for the COMPAS recidivism risk scoring tool, used in bail, sentencing, and parole decisions across the US.

**Finding:** COMPAS is deployment-blocked under EU AI Act, NIST AI RMF, and US 4/5ths rule — 4 critical threshold breaches including a Disparate Impact Ratio of 1.92× against a 1.25× legal limit. Replicates and extends ProPublica's 2016 investigation within 2–3% of original findings.

---

### [Credit Scoring Safety Evaluation Runbook](./Credit_Scoring_Safety_Eval_Runbook.md)

Applies the same structured evaluation framework to AI-based credit scoring systems. Covers fairness metrics, regulatory pass/fail thresholds (EU AI Act, ECOA), escalation paths, and monitoring cadence for high-risk consumer lending decisions.

---

## Standards Referenced

- EU AI Act (2024) — Annex III high-risk classification, Art. 10, Art. 12
- NIST AI Risk Management Framework — GOVERN 1.1, MAP 1.5, MEASURE 2.5
- ISO 42001 — AI management system requirements
- US EEOC 4/5ths Rule — 29 CFR Part 1607
- India Digital Personal Data Protection Act 2023

---

## Related Work (Portfolio)

- [Algorithmic Fairness Auditor](https://preetibuilds-33d6f6da.vercel.app/algorithmic-fairness) — interactive tool: quantization bias + COMPAS + credit scoring audit
- [LLM Safety Evaluation Framework](https://preetibuilds-33d6f6da.vercel.app/safety-eval) — multi-vendor safety benchmark across 5 harm categories
- [Carbon-Fairness Efficiency Frontier](https://preetibuilds-33d6f6da.vercel.app/carbon-fairness) — quantifies the carbon cost of fairness decisions
- [AI Governance Tracker](https://preetibuilds-33d6f6da.vercel.app/ai-governance) — EU AI Act, NIST RMF, ISO 42001 clause-level compliance tracker
