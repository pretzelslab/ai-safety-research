# Credit Scoring Fairness Evaluation Runbook

**Tool:** Mortgage Lending Decision Model (AI-assisted underwriting)  
**Auditor:** Preeti Raghuveer  
**Standard:** EU AI Act Annex III · ECOA · Federal Reserve Regulation B · US 4/5ths Rule  
**Dataset:** CFPB HMDA 2022 — New York State, 138,665 conventional home purchase loan applications  
**Last reviewed:** April 2026

---

## Overview

AI-assisted underwriting models are now used across retail banking to predict default risk and recommend credit decisions. Under EU AI Act Annex III, credit scoring is explicitly classified as a **high-risk AI system** — it requires a mandatory conformity assessment, human oversight, and documented bias evaluation before deployment.

This runbook defines what to test, what numbers are acceptable, what happens when something fails, and how to monitor a mortgage lending model over time. It covers obligations under US law (ECOA, Reg B) and EU regulation (EU AI Act, GDPR Article 22), and is designed to be usable by a model risk team, a compliance function, or an external auditor.

This runbook was produced following an independent audit of CFPB HMDA 2022 data for New York State. Three demographic groups — Black, Hispanic, and Native American applicants — exceed the EU AI Act 1.25× DIR threshold. This triggers a mandatory conformity assessment for the entire model regardless of which group is the source of the breach.

---

## 1. What We Are Testing

### 1.1 Fairness Metrics

| Metric | Definition | Groups tested |
|--------|-----------|---------------|
| **Denial Rate** | % of applications denied per demographic group | Black, White, Hispanic, Asian, Native American |
| **Disparate Impact Ratio (DIR)** | Group denial rate ÷ White denial rate | All groups vs White baseline |
| **Approval Ratio (4/5ths)** | Group approval rate ÷ White approval rate | All groups |
| **Income-controlled DIR** | DIR computed within each income quartile | Black, Hispanic, Asian, Native American |

### 1.2 Baseline Findings (HMDA 2022 audit, n=138,665)

| Group | n | Denial Rate | DIR | Approval Ratio | Status |
|-------|---|-------------|-----|----------------|--------|
| White | 93,900 | 10.4% | 1.00× | 1.00 | Baseline |
| Black | 7,931 | 18.9% | **1.81×** | 0.91 | ❌ Critical |
| Hispanic | 11,770 | 17.9% | **1.71×** | 0.92 | ❌ Critical |
| Asian | 24,608 | 11.6% | 1.11× | 0.99 | ✅ Pass |
| Native American | 456 | 27.4% | **2.63×** | 0.81 | ❌ Double-critical (⚠ low n — treat as indicative) |

**Note on Native American finding:** n=456 sits below the 500-row threshold for full statistical confidence. The DIR of 2.63× is treated as indicative rather than definitive. However, it does not reduce severity classification — a model with an indicative DIR of 2.63× must be treated as double-critical pending a larger sample. The conformity assessment obligation is triggered by Black and Hispanic findings independently of Native American.

### 1.3 Income-Controlled Finding (Black applicants)

| Income quartile | Black denial rate | DIR vs White |
|-----------------|------------------|--------------|
| Q1 (lowest) | 25.7% | 1.55× |
| Q2 | 16.8% | 1.83× |
| Q3 | 14.0% | 1.95× |
| Q4 (highest) | 14.1% | **1.94×** |

The DIR increases as income rises, reaching 1.94× in the highest income bracket. Income does not explain the disparity — proxy discrimination via correlated features (zip code, credit history length, employment type) is the likely mechanism.

### 1.4 What Is Not Being Tested

- Individual loan officer decisions (human bias outside model scope)
- Interest rate disparities (separate fair pricing analysis required)
- Small business or commercial lending (separate HMDA classification)
- Models that do not produce a continuous probability output

---

## 2. Pass/Fail Thresholds

### 2.1 EU AI Act (Annex III — Credit Scoring)

Credit scoring is a named high-risk use case under EU AI Act Annex III. The conformity assessment and oversight obligations below apply to the **model as a whole** — they are triggered when ANY group exceeds the DIR threshold, not per group individually.

| Model-level check | Requirement | Status |
|-------------------|-------------|--------|
| DIR ≤ 1.25× for all tested groups | Mandatory | ❌ 3 groups exceed threshold — Black 1.81×, Hispanic 1.71×, Native American 2.63× |
| Conformity assessment completed | Required before deployment | ❌ Not yet initiated — **triggered by all three failing groups** |
| Human oversight mechanism in place | Automated denial must allow human review on request | ⚠ Verify — document the appeal process |
| Adverse action explainability | Each denial must be explainable at the individual level | ⚠ Verify — black-box models risk non-compliance |
| Bias monitoring post-deployment | Ongoing obligation, not one-time audit | ⚠ Monitoring cadence to be established (see Section 4) |

**Finding:** EU AI Act conformity assessment is mandatory and has not been initiated. Deployment is blocked for all applicant groups until assessment is complete and DIR findings are remediated.

### 2.2 ECOA — Equal Credit Opportunity Act (US)

| Check | Threshold | Status |
|-------|-----------|--------|
| No disparate impact — Black | DIR ≤ 1.25× | ❌ 1.81× — FLAGGED |
| No disparate impact — Hispanic | DIR ≤ 1.25× | ❌ 1.71× — FLAGGED |
| No disparate impact — Native American | DIR ≤ 1.25× | ❌ 2.63× — FLAGGED (low n, indicative) |
| No disparate impact — Asian | DIR ≤ 1.25× | ✅ 1.11× — Pass |
| No disparate treatment (intent) | No evidence of intentional use of protected characteristics | ⚠ Income-controlled data suggests proxy discrimination — warrants further investigation |

**Finding:** ECOA adverse impact triggered for Black, Hispanic, and Native American applicants. Legal exposure under CFPB enforcement. Self-disclosure assessment recommended.

### 2.3 Regulation B (Federal Reserve)

| Check | Requirement | Status |
|-------|------------|--------|
| Adverse action notice within 30 days | Must be sent to all denied applicants within 30 days | ✅ Operational requirement — verify process compliance |
| Specific denial reasons | Notice must state specific reasons, not generic "credit model output" | ⚠ Black-box models are at risk — verify explainability layer exists |
| Record retention (mortgage) | Adverse action records retained for minimum 25 months | ✅ Operational requirement — verify record-keeping process |
| No prohibited basis | Denial must not reference race, sex, national origin, or other protected characteristics | ✅ Feature audit required to confirm no direct use of protected attributes |

**Finding:** If the model cannot produce specific, individual-level reasons for each denial, Reg B compliance is at risk. An explainability audit is required independently of the fairness findings.

### 2.4 US 4/5ths Rule (EEOC Uniform Guidelines — applied to credit)

| Group | Approval Ratio | Threshold | Status |
|-------|---------------|-----------|--------|
| Black | 0.91 | ≥ 0.80 | ✅ Pass |
| Hispanic | 0.92 | ≥ 0.80 | ✅ Pass |
| Asian | 0.99 | ≥ 0.80 | ✅ Pass |
| Native American | 0.81 | ≥ 0.80 | ✅ Pass (marginal, ⚠ low n) |

**Finding:** All groups pass the 4/5ths rule. The EU AI Act 1.25× DIR threshold is more stringent and is the binding constraint in this audit. Passing the 4/5ths rule does not clear the EU AI Act or ECOA findings.

### 2.5 Internal Thresholds (Recommended)

| Check | Warning | Critical | Double-Critical |
|-------|---------|----------|-----------------|
| DIR (any group) | > 1.10× | > 1.25× | > 1.50× |
| Denial rate gap vs White | > 3 pp | > 7 pp | > 12 pp |
| Income-controlled DIR (any quartile) | > 1.25× | > 1.50× | > 1.75× |
| Sample size (minority group) | n < 1,000 | n < 300 | n < 100 |

---

## 3. Escalation Path

### 3.1 Severity Classification

| Level | Trigger | Owner | Required action |
|-------|---------|-------|-----------------|
| **Warning** | DIR 1.10–1.25× OR income-controlled DIR > 1.25× in any quartile | Model Risk | Document finding, increase monitoring frequency, no deployment block |
| **Critical** | DIR > 1.25× for any group with n ≥ 300 | Compliance + Model Risk | Deployment blocked — mandatory remediation plan within 30 days |
| **Double-critical** | DIR > 1.50× OR ECOA adverse impact triggered OR CFPB examination risk | CCO + Legal | Immediate escalation, external counsel engaged, voluntary self-disclosure assessed |

**Current status of this audit:**
- Black (n=7,931, DIR 1.81×): **Double-critical** — ECOA adverse impact triggered
- Hispanic (n=11,770, DIR 1.71×): **Double-critical** — ECOA adverse impact triggered
- Native American (n=456, DIR 2.63×): **Double-critical (indicative)** — low n but DIR is the most severe breach; treated as double-critical pending sample expansion
- Asian (n=24,608, DIR 1.11×): **Pass** — no escalation

### 3.2 Authority Matrix

| Action | Authority required |
|--------|--------------------|
| Deploy with warning-level findings | Model Risk sign-off |
| Deploy with mitigations after critical finding | Chief Compliance Officer + Legal sign-off |
| Deploy after double-critical finding | Board Risk Committee approval + documented remediation plan |
| Withdraw model from production | Chief Risk Officer |
| Voluntary CFPB disclosure | Legal counsel decision |
| EU AI Act conformity assessment initiation | Chief Compliance Officer |

### 3.3 Remediation Options (in order of preference)

1. **Threshold recalibration per group** — adjust the approval threshold separately for each demographic group to bring denial rates within DIR ≤ 1.25×. Reduces disparity immediately but does not address root cause. Carries financial risk (approving applicants who may default at higher rates). Interim measure only — must be accompanied by a plan for options 2 or 3.

2. **Feature audit and removal** — identify proxy variables carrying racial signal (zip code, credit history length, employment type, time at address). Remove or replace in the next model version. Addresses root cause. Requires careful testing — removing features may reduce predictive accuracy.

3. **Fairness-constrained retraining** — retrain the model with an explicit fairness constraint (e.g. DIR ≤ 1.25× as a regularisation term). Requires demographic labels in training data and careful cross-validation. Most complete fix.

4. **Human review overlay** — require human sign-off for all denials in flagged demographic groups. Satisfies EU AI Act human oversight requirement immediately. Does not fix the underlying model. Operationally expensive at scale.

5. **Model replacement** — if options 1–4 do not achieve and sustain compliance within 6 months of the critical finding, retire the model and replace with a compliant alternative. This is the backstop, not the first resort.

---

## 4. Monitoring Cadence

### 4.1 Scheduled Audits

| Frequency | Trigger | Scope |
|-----------|---------|-------|
| **Quarterly** | Calendar (Jan, Apr, Jul, Oct) | Full denial rate audit across all groups, income-controlled DIR |
| **Annual** | HMDA data release (Q3 each year) | External benchmark — compare model output to HMDA published data for same geography and loan type |
| **Post-retraining** | Any model update, feature change, or hyperparameter change | Full audit before re-deployment — treat as a new model |
| **Post-policy change** | CFPB rule change, EU AI Act secondary legislation, ECOA enforcement guidance | Re-evaluate all thresholds and classifications |

### 4.2 Drift Triggers (Ad Hoc Audit Required)

- DIR for any group crosses from warning to critical (> 1.25×) in any quarter
- Denial rate for any group increases by > 2 percentage points quarter-over-quarter
- Income-controlled DIR for any group exceeds 1.50× in any income quartile
- CFPB examination notice received
- Internal or external complaint alleging discriminatory lending
- Native American sample size drops below 200 in any quarterly audit period

### 4.3 Minimum Sample Sizes for Valid Audit

| Group | Minimum n | Action if below minimum |
|-------|-----------|------------------------|
| White (baseline) | 500 | Flag audit as unreliable — do not use for compliance reporting |
| Black | 300 | Flag as unreliable; use wider confidence intervals; escalate to warning regardless of DIR |
| Hispanic | 300 | Flag as unreliable |
| Asian | 200 | Flag as low confidence |
| Native American | 200 | Flag as low confidence — current audit (n=456) is borderline; target 500+ within 2 annual cycles |

---

## 5. Success Metrics

### 5.1 Compliance Outcomes (Hard Pass/Fail)

| Metric | Target | Current status |
|--------|--------|----------------|
| DIR ≤ 1.25× for all groups with n ≥ 300 | All groups pass | ❌ Black 1.81×, Hispanic 1.71× fail |
| EU AI Act conformity assessment completed | Yes | ❌ Not yet initiated |
| ECOA adverse impact cleared | No flagged groups | ❌ Black and Hispanic flagged |
| Reg B adverse action notices satisfy specificity requirement | Yes | ⚠ Explainability audit required |
| Human oversight mechanism documented and operational | Yes | ⚠ Verify |

### 5.2 Process Health Metrics

| Metric | Target |
|--------|--------|
| Quarterly audit completed on schedule | 100% of scheduled audits |
| Remediation plan produced within 30 days of critical finding | 100% |
| Income-controlled DIR included in every audit report | Yes |
| Native American sample size ≥ 500 | Within 2 annual HMDA data cycles |
| EU AI Act conformity assessment initiated | Within 60 days of this runbook |

### 5.3 Outcome Quality Metrics

| Metric | Target |
|--------|--------|
| Post-remediation DIR ≤ 1.25× sustained for 4 consecutive quarters | Yes |
| No CFPB examination findings related to fair lending | Yes |
| Default rates within 1 percentage point across demographic groups post-recalibration | Yes |
| Income-controlled DIR ≤ 1.25× in all quartiles for all groups | Yes |

---

## Appendix: Key Regulatory References

| Regulation | Scope | Key obligation for credit AI |
|-----------|-------|------------------------------|
| EU AI Act Annex III | Credit scoring = listed high-risk use case | Conformity assessment, human oversight, transparency, bias monitoring before and after deployment |
| ECOA (15 U.S.C. § 1691) | All credit transactions in the US | Prohibits disparate impact or treatment on protected classes including race, sex, national origin |
| Regulation B (12 CFR Part 202) | ECOA implementing rule | Adverse action notices with specific reasons, 25-month record retention for mortgages |
| GDPR Article 22 | EU automated individual decisions | Right to explanation, right to contest, human review available on request |
| CFPB Supervision and Examination | Fair lending enforcement | CFPB can examine, enforce, and publicise ECOA/Reg B violations |
| NIST AI RMF | US AI risk framework | Govern, Map, Measure, Manage — provides monitoring structure complementary to this runbook |

---

*Analysis built in Python · Google Colab · CFPB HMDA 2022 data*  
*Methodology consistent with COMPAS Safety Evaluation Runbook (April 2026)*  
*Part of the Algorithmic Fairness Auditor — preetibuilds portfolio*  
*GitHub: pretzelslab/ai-safety-research*
