# Governance Gap Analysis — Cross-Jurisdictional Gaps

## Overview

Women's safety AI is deployed globally but regulated locally. The four frameworks reviewed (EU AI Act, NIST AI RMF, India DPDP Act + IT Act, ISO 42001) each address fragments of the problem. None coordinates with the others. The result is a fragmented regulatory landscape with three structural problems:

1. **Regulatory arbitrage** — developers optimise for the least demanding jurisdiction
2. **Mutual recognition gaps** — no certification in one jurisdiction is recognised in another
3. **Unaddressed cross-border attack surfaces** — the compound GPS + network failure mode in rural transnational contexts falls between every framework

This file documents the gaps that emerge specifically at the intersection of frameworks — gaps that no single framework can close alone.

---

## Framework Coverage Comparison

| Requirement | EU AI Act | NIST AI RMF | India DPDP / IT Act | ISO 42001 |
|---|---|---|---|---|
| Classifies safety AI as high-risk | ✗ (not listed in Annex III) | N/A (voluntary) | ✗ (no classification) | N/A (process standard) |
| Requires adversarial physical proximity testing | ✗ | ✗ | ✗ | ✗ |
| Requires ambient noise calibration | ✗ | ✗ | ✗ | ✗ |
| Addresses rural dead-zone compound failure | ✗ | ✗ | ✗ | ✗ |
| Addresses sociotechnical suppression | ✗ | Acknowledged only | ✗ | ✗ |
| Requires zero-interaction detection testing | ✗ | ✗ | ✗ | ✗ |
| Requires exhaustion-resistance testing | ✗ | ✗ | ✗ | ✗ |
| Provides mutual recognition of certification | N/A | N/A | N/A | Partial (ISO mutual recognition) |
| Cross-border deployment coordination | ✗ | ✗ | ✗ | ✗ |

**Every cell in the adversarial robustness rows is ✗ across all four frameworks.** This is the core finding of the governance gap analysis: the adversarial attack surfaces documented in this research are ungoverned globally, not just in one jurisdiction.

---

## Cross-Jurisdictional Gap 1 — Regulatory Arbitrage

### The problem
A women's safety app developer based in the EU faces no mandatory conformity assessment (EU AI Act does not classify safety apps as high-risk). The same developer faces no binding robustness requirement in India (no AI quality standard exists), the US (NIST AI RMF is voluntary), or under ISO 42001 (process-based, outcome-agnostic).

**There is no jurisdiction in which a women's safety app developer is required to demonstrate minimum adversarial robustness performance.** A developer seeking to minimise compliance cost faces identical regulatory demands everywhere: none.

### Regulatory arbitrage risk
If any future jurisdiction does introduce binding robustness requirements (plausible if EU AI Act is amended to include safety apps in Annex III), developers can:
- Incorporate in a jurisdiction without equivalent requirements
- Market globally from that low-compliance base
- Claim compliance with the local standard without meeting the more demanding foreign one

### No current fix exists
No mutual recognition agreement, bilateral treaty, or international coordination mechanism covers AI robustness standards for personal safety applications. The gap is structural.

---

## Cross-Jurisdictional Gap 2 — No Mutual Recognition of Certification

### The problem
ISO 42001 is the closest instrument to a globally recognised AI management certification. However:
- ISO 42001 certification is process-based (see iso_42001_gaps.md) — it does not certify robustness outcomes
- The EU AI Act's conformity assessment (where applicable) is EU-market-specific — not recognised in India or the US
- India has no AI certification scheme at all

A women's safety app certified under ISO 42001 in Europe can be marketed in India with no obligation to demonstrate equivalent performance in Indian deployment conditions (higher ambient noise, rural dead zones, different threat patterns).

### Implication
The certification that exists (ISO 42001) does not certify what matters. The certification that would matter (adversarial robustness under real-world conditions) does not exist anywhere.

---

## Cross-Jurisdictional Gap 3 — Cross-Border Attack Scenarios Are Unaddressed

### The problem
High-risk women's safety scenarios frequently cross jurisdictional boundaries:
- **Transnational transit:** intercity buses and trains cross state lines in India; international transport routes cross national borders
- **App-cab scenarios (U-02):** the deviation from safe route may cross into a different state or district jurisdiction
- **Urban-rural transition:** a scenario beginning in U1 (urban public, covered by hypothetical city-level Safe City standards) transitions through T1 (transit) to R2 (rural isolated, uncovered by any standard)

No governance framework accounts for the jurisdictional transition within a single attack scenario. A safety app that meets hypothetical urban standards fails the moment it enters a rural dead zone — with no regulatory oversight of that failure mode.

### Specific cross-border failure: India's Safe City boundary problem
Safe City AI deployments cover 8 specific cities. The perimeter of a Safe City is typically the municipal boundary. A cab journey that begins inside a Safe City perimeter and exits it is governed by no standard for the post-boundary segment — exactly the segment where route deviation and network failure are most dangerous (U-02).

---

## Cross-Jurisdictional Gap 4 — No Coordinated Incident Reporting

### The problem
When a women's safety AI system fails during an actual incident — alert not sent, detection missed, device intercepted — there is no mandatory incident reporting mechanism in any jurisdiction that:
- Requires the developer to report the failure
- Makes failure data available across jurisdictions
- Aggregates failure patterns across deployments to identify systemic weaknesses

This means every women's safety AI deployment is an isolated experiment. Systemic failure modes — such as the ambient noise suppression documented in audio_attacks.md or the rural dead zone compound failure in sensor_attacks.md — can persist undetected across millions of deployments because no mechanism aggregates incident data.

**Existing frameworks:** EU AI Act Art. 73 requires serious incident reporting for high-risk AI systems — but women's safety apps are not classified as high-risk. NIST AI RMF MANAGE 2.2 requires internal incident response — not cross-developer, cross-jurisdiction reporting.

---

## Cross-Jurisdictional Gap 5 — The Indian Context Is Unrepresented in Global Standards

### The problem
The dominant global AI governance frameworks (EU AI Act, NIST AI RMF, ISO 42001) were designed primarily in European and North American contexts. Their calibration assumptions — ambient noise levels, network reliability, GPS coverage, threat patterns — reflect Western deployment environments.

For Indian deployments, specifically:
- **Ambient noise:** Indian urban noise floors are systematically higher than Western calibration environments (see audio_attacks.md)
- **Network coverage:** Rural India has significantly lower mobile coverage than rural Europe or the US (see sensor_attacks.md)
- **Threat patterns:** The specific combination of crowded transit (groping) + isolated vehicle (assault) + rural road (abduction) is documented extensively in Indian incident data but absent from Western adversarial ML literature

**A safety app certified against EU or NIST standards is certified against conditions that do not represent India.** This is not a minor calibration difference — the ambient noise gap alone means an EU-certified audio detection system may have 40–60% lower effective detection rates in Mumbai vs. a European city.

No cross-jurisdictional mechanism exists to require India-specific calibration for safety apps sold in India.

---

## Recommendations for Cross-Jurisdictional Action

### Immediate (2–3 years)
1. **ISO 42001 sector profile for personal safety AI:** ISO TC 42 or a nominated body to develop a sector-specific profile requiring minimum adversarial robustness outcomes — creating the first globally applicable standard with teeth for women's safety AI.

2. **NIST AI RMF sector profile:** NIST to publish a personal safety AI sector profile requiring ZIDR, ANEF, OET, and SFES as MEASURE 2.5 outputs — providing a voluntary but operationally specific standard that other jurisdictions can reference.

### Medium-term (3–7 years)
3. **EU-India bilateral AI safety dialogue:** Establish a government-level dialogue on AI safety standards for women's safety applications — focused on calibrating standards to Indian deployment conditions and mutual recognition of conformity assessments.

4. **Global incident reporting for safety-critical consumer AI:** Advocate for a multilateral incident reporting requirement (through ITU, UN Women, or GPAI) for AI systems marketed as personal safety tools — aggregate failure data across jurisdictions to identify systemic weaknesses.

### Structural (7+ years)
5. **International Women's Safety AI Standard:** A dedicated ISO/IEC standard (or IEC 62443-equivalent for personal safety AI) specifying mandatory adversarial robustness requirements, deployment context calibration, zero-interaction detection performance, and cross-jurisdictional incident reporting — covering the full attack surface taxonomy documented in this research.

---

## Connection to Zero-Interaction Window

The zero-interaction window is the clearest demonstration of why cross-jurisdictional coordination matters: every woman in every deployment context — urban India, rural India, EU, US — is equally vulnerable during the 2–15 seconds when passive detection is the only layer. Yet no jurisdiction has a standard that addresses it.

**The zero-interaction window is a global governance gap, not a local one. Closing it requires the only solution that matches its scope: international coordination.**

The absence of any ✓ in the zero-interaction window row across all four frameworks is not a coincidence or oversight. It reflects a structural failure: governance frameworks were designed around AI systems that interact with cooperative users. The zero-interaction window — a physically coercive, adversarial, real-time scenario — falls entirely outside the design assumptions of every governance framework currently in operation.

**This research names that gap. Closing it is the policy contribution of this work.**
