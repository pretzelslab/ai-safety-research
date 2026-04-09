# COMPAS Safety Evaluation Runbook

**Tool:** COMPAS Recidivism Risk Score (Northpointe Inc.)  
**Auditor:** Preeti Raghuveer  
**Standard:** EU AI Act · NIST AI RMF · US 4/5ths Rule  
**Dataset:** Broward County, Florida — 6,172 defendant records  
**Last reviewed:** April 2026

---

## Overview

COMPAS (Correctional Offender Management Profiling for Alternative Sanctions) assigns recidivism risk scores used in bail, sentencing, and parole decisions across the United States. This runbook defines the evaluation criteria for determining whether the tool is safe and fair to deploy. It covers what to test, what numbers are acceptable, what happens when something fails, and how to monitor the tool over time.

This runbook was produced following an independent audit that replicated ProPublica's 2016 findings within 2–3% using the same Broward County dataset.

---

## 1. What We Are Testing

### 1.1 Fairness Metrics

| Metric | Definition | Groups tested |
|--------|-----------|---------------|
| **False Positive Rate (FPR)** | % of people who did NOT re-offend but were scored "high risk" | Black, White, Hispanic, Other |
| **False Negative Rate (FNR)** | % of people who DID re-offend but were scored "low risk" | Black, White, Hispanic, Other |
| **Disparate Impact Ratio (DIR)** | Rate of unfavourable decisions for group A ÷ group B | All pairwise comparisons |
| **Intersectional breakdown** | FPR/FNR split by race × gender × age band | Black female, White male, etc. |

### 1.2 Baseline findings (ProPublica replication, n=6,172)

| Group | n | Base rate | FPR | FNR | DIR |
|-------|---|-----------|-----|-----|-----|
| African-American | 3,175 | 52.3% | 42.3% | 28.5% | 1.92× |
| Caucasian | 2,103 | 39.1% | 22.0% | 49.6% | 1.00× (baseline) |
| Hispanic | 509 | 37.1% | 19.4% | 58.2% | 0.88× |
| Other | 343 | 36.2% | 12.8% | 66.1% | 0.58× |

**Dual-direction bias note:** The tool overflags African-Americans (high FPR, DIR 1.92×) while simultaneously underflaging Hispanic and Other groups (FNR 58–66%). These are not offsetting errors — they represent distinct harms to distinct populations and must each be remediated independently.

### 1.3 Data requirements

- Minimum 100 records per demographic group before conclusions are drawn
- Dataset must include: race, sex, age, charge degree, decile score, two-year recidivism outcome
- Any group with < 100 records is flagged as **insufficient coverage** and excluded from pass/fail assessment

---

## 2. Pass/Fail Thresholds

### 2.1 Regulatory thresholds

| Standard | Metric | Pass | Fail | Status (baseline) |
|----------|--------|------|------|-------------------|
| EU AI Act Art. 10 | DIR (any group pair) | ≤ 1.25× | > 1.25× | ❌ FAIL — 1.92× |
| US 4/5ths Rule | Selection rate ratio | ≥ 0.80 | < 0.80 | ❌ FAIL — 0.52 |
| NIST RMF MEASURE 2.5 | Bias documented pre-deployment | Yes | No | ✅ PASS — this document |
| NIST RMF GOVERN 1.1 | Thresholds defined and owned | Yes | No | ✅ PASS — this document |
| NIST RMF MAP 1.5 | Affected groups identified | Yes | No | ✅ PASS — Section 1.1 |

### 2.2 Internal thresholds (recommended)

These are tighter than legal minimums — intended to catch problems before they become legal violations:

| Metric | Warning | Critical |
|--------|---------|----------|
| DIR (any group pair) | > 1.10× | > 1.25× |
| FPR gap (highest minus lowest group) | > 10 percentage points | > 15 percentage points |
| FNR gap (highest minus lowest group) | > 10 percentage points | > 15 percentage points |
| Demographic coverage | < 200 records per group | < 100 records per group |

**Warning** = flag for review before deployment proceeds.  
**Critical** = automatic hold. Deployment blocked until resolved.

### 2.3 Current COMPAS status

| Check | Value | Threshold | Result |
|-------|-------|-----------|--------|
| DIR — African-American/Caucasian | 1.92× | 1.25× | ❌ Critical |
| FPR gap (AA vs Other) | 29.5 pp | 15 pp | ❌ Critical |
| FNR gap (Other vs AA) | 37.6 pp | 15 pp | ❌ Critical |
| US 4/5ths — African-American | 0.52 | ≥ 0.80 | ❌ Critical |
| Minimum group coverage | 343 (Other) | 100 min | ✅ Pass |

**Overall verdict: DEPLOYMENT BLOCKED — 4 critical threshold breaches.**

---

## 3. Escalation Path

### 3.1 Trigger conditions

| Level | Trigger | Response time |
|-------|---------|---------------|
| **Warning** | Any metric exceeds Warning threshold (Section 2.2) | Review within 5 business days |
| **Critical** | Any metric exceeds Critical threshold | Immediate hold — same business day |
| **Double critical** | 2+ metrics in Critical simultaneously | Executive escalation — 24 hours |

### 3.2 Escalation steps — Warning

1. Analyst documents the breach: metric, value, threshold, affected group
2. Analyst notifies ML lead and product owner in writing
3. Joint review scheduled within 5 business days
4. Options: remediate → re-audit → clear for deployment, OR escalate to Critical
5. Decision and rationale logged in audit trail

### 3.3 Escalation steps — Critical

1. **Deployment hold issued immediately** — no exceptions, no overrides at analyst level
2. Analyst files breach report within 4 hours:
   - Metric(s) breached
   - Affected group(s) and estimated harm scale
   - Recommended remediation path
3. Notified parties (simultaneously):
   - ML / Data Science lead
   - Product owner
   - Legal / Compliance
   - If justice system deployment: external oversight body
4. Remediation options assessed (see Section 3.4)
5. Re-audit required before hold is lifted — same analyst cannot self-clear

### 3.4 Remediation options

| Approach | What it does | When to use |
|----------|-------------|-------------|
| **Threshold recalibration** | Adjust decision threshold per group | DIR breach only |
| **Quantization-aware retraining** | Retrain with fairness constraints built in | FPR/FNR gap > 15pp |
| **Score suppression** | Remove COMPAS score from decision for flagged groups | Emergency hold only |
| **Human review overlay** | Mandatory human review for all high-risk scores | Interim measure while retraining |
| **Decommission** | Remove tool from deployment entirely | If no remediation closes breach |

### 3.5 Authority matrix

| Action | Who can authorise |
|--------|------------------|
| Issue deployment hold | Safety Analyst (unilateral) |
| Lift deployment hold | ML Lead + Legal sign-off (joint) |
| Override Critical breach | Not permitted — must remediate first |
| Approve decommission | Executive + Legal |

### 3.6 COMPAS current status

All 4 critical thresholds breached (Section 2.2).  
**Status: Deployment hold active.**  
Recommended path: threshold recalibration per group + human review overlay as interim measure. Full retraining required before permanent deployment clearance.

---

## 4. Monitoring Cadence

### 4.1 Scheduled audits

| Audit type | Frequency | Scope |
|-----------|-----------|-------|
| Full fairness audit | Quarterly | All metrics, all groups, full Section 2 threshold check |
| Lightweight spot-check | Monthly | DIR and FPR only, sample of 500 recent records |
| Third-party independent review | Annually | Full audit by external auditor, results published |
| Post-remediation re-audit | Within 30 days of any fix | Full audit, same methodology as baseline |

### 4.2 Triggered re-audits

A full unscheduled audit is mandatory when any of the following occur:

| Trigger | Action required |
|---------|----------------|
| Model retrained or updated | Full re-audit before new version deploys |
| Dataset demographic shift > 5% in any group | Full re-audit within 2 weeks |
| New jurisdiction added | Full re-audit on local data before deployment |
| External audit or press report flags concern | Full re-audit within 5 business days |
| Any individual complaint alleging bias | Spot-check within 48 hours, full audit if confirmed |
| Regulation change (e.g. new EU AI Act guidance) | Threshold review within 30 days |

### 4.3 Drift detection

| Signal | How to detect | Threshold for action |
|--------|--------------|---------------------|
| Demographic mix shift | Compare monthly group proportions vs baseline | > 5% shift in any group |
| Score distribution shift | Compare decile score histograms monthly | KS statistic > 0.1 |
| Outcome rate shift | Compare actual recidivism rates vs predicted | > 3pp divergence |
| FPR/FNR creep | Track monthly spot-checks as time series | Upward trend over 3 consecutive months |

### 4.4 Audit trail requirements

Every audit — scheduled or triggered — must produce:
- Date, analyst name, dataset version, model version
- Full metric table (Section 2.1 format)
- Pass/fail result per threshold
- If any breach: breach report filed per Section 3.3
- Signed off by ML lead before filing

All audit records retained for minimum 7 years (EU AI Act Art. 12 — high-risk system logging requirement).

---

## 5. Success Metrics

### 5.1 Process health

| Metric | Target | Measured |
|--------|--------|---------|
| Scheduled audits completed on time | 100% | Quarterly |
| Audit reports filed within 24hrs of completion | 100% | Per audit |
| Breach reports filed within 4hrs of detection | 100% | Per breach |
| Audit trail complete (all fields populated) | 100% | Per audit |
| Third-party review completed annually | 1 per year | Annually |

### 5.2 Detection effectiveness

| Metric | Target | Measured |
|--------|--------|---------|
| Drift detected before Critical threshold breach | > 80% of cases | Quarterly review |
| Mean time from drift onset to detection | < 30 days | Per incident |
| Undetected breaches (found by external party first) | 0 | Ongoing |
| False alarm rate (Warning issued, no real problem) | < 20% | Quarterly review |

### 5.3 Outcome quality

| Metric | Target | Measured |
|--------|--------|---------|
| Deployment holds that were later found unjustified | < 5% | Per hold lifted |
| Remediations that successfully closed the breach | > 90% | Per remediation |
| Re-audit pass rate after remediation | > 85% | Per re-audit |
| DIR trend (quarter over quarter) | Declining or stable | Quarterly |

### 5.4 Runbook health

| Trigger | Action |
|---------|--------|
| New regulation published | Review thresholds within 30 days |
| Remediation fails twice | Review escalation path |
| External audit finds gap | Update relevant section within 2 weeks |
| Annual cycle | Full runbook review regardless |

**Runbook owner:** Safety Evaluations Analyst  
**Approver:** ML Lead + Legal  
**Review cycle:** Annual minimum, triggered as above

---

## References

- ProPublica: [Machine Bias](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing) (2016)
- EU AI Act — Annex III (High-Risk AI Systems), Art. 10, Art. 12
- NIST AI Risk Management Framework — GOVERN 1.1, MAP 1.5, MEASURE 2.5
- US EEOC 4/5ths Rule — 29 CFR Part 1607
- Broward County dataset: public release via ProPublica GitHub

---

*This runbook was produced as part of an independent COMPAS audit. Audit code and methodology available at [github.com/pretzelslab](https://github.com/pretzelslab).*
