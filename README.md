# AI Safety Research

Independent research and evaluation frameworks for responsible AI deployment.

Built by [Preeti Raghuveer](https://preetibuilds-33d6f6da.vercel.app) — AI governance practitioner focused on operationalising fairness, safety, and compliance.

---

## Contents

### [COMPAS Safety Evaluation Runbook](./COMPAS_Safety_Eval_Runbook.md)

A structured deployment evaluation framework for the COMPAS recidivism risk scoring tool, used in bail, sentencing, and parole decisions across the US.

Covers:
- Fairness metrics and baseline findings (n=6,172 Broward County records)
- Pass/fail thresholds against EU AI Act, NIST AI RMF, and US 4/5ths rule
- Escalation path and authority matrix for threshold breaches
- Monitoring cadence and drift detection
- Success metrics for the evaluation process itself

**Finding:** COMPAS is deployment-blocked under all three regulatory frameworks — 4 critical threshold breaches including DIR of 1.92× against a 1.25× legal limit.

This runbook replicates and extends ProPublica's 2016 investigation using the same public dataset, independently verified within 2–3% of original findings.

---

## Standards referenced

- EU AI Act (2024) — Annex III high-risk classification, Art. 10, Art. 12
- NIST AI Risk Management Framework — GOVERN 1.1, MAP 1.5, MEASURE 2.5
- US EEOC 4/5ths Rule — 29 CFR Part 1607

---

## Related work

- [Algorithmic Fairness Auditor](https://preetibuilds-33d6f6da.vercel.app/algorithmic-fairness) — interactive tool for quantization bias + COMPAS audit
- [AI Ethics & Governance Tracker](https://preetibuilds-33d6f6da.vercel.app/ai-governance) — EU AI Act, NIST RMF, ISO 42001 clause-level compliance tracker
- [Carbon-Fairness Efficiency Frontier](https://preetibuilds-33d6f6da.vercel.app/carbon-fairness) — first tool to quantify the carbon cost of fairness decisions
