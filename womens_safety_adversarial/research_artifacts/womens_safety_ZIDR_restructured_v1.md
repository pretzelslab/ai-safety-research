# Adversarial Robustness in Women's Safety AI Systems: Threat Taxonomy, ZIDR Metric, and Governance Gap Analysis

**Preethi Raghuveeran** · Independent Researcher  
[removed] · ORCID: 0009-0009-1907-8223  
Scenario library & data: Zenodo DOI https://doi.org/10.5281/zenodo.20028247

---

## Abstract

Women's safety AI systems — deployed for proximity alerting, distress sound classification, and movement-triggered detection — are evaluated exclusively on benchmark accuracy with cooperative users. This paper demonstrates that a system achieving 95% benchmark accuracy can achieve 0% effective detection in the zero-interaction window of a real attack. We introduce three contributions: (1) a 4-layer threat taxonomy mapping attack surfaces × attack methods × adversary access levels for physically proximate adversaries; (2) Zero-Interaction Detection Rate (ZIDR), a novel evaluation metric capturing passive-only detection under adversary-induced degradation; and (3) a governance gap analysis across five frameworks (EU AI Act, NIST AI RMF, ISO 42001, India DPDP Act 2023, India IT Act) confirming a structural absence of passive-detection robustness requirements. A Python CLI specification for ZIDR-based system profiling is included. This work provides the missing definition and metric needed to make passive robustness requirements testable by standards bodies.

**Keywords:** adversarial robustness, women's safety AI, passive detection, threat taxonomy, AI governance, gender-based violence, ZIDR

---

## 1. Introduction

Women's safety applications are deployed in conditions that invert standard ML evaluation assumptions: the user may be unable to interact with the device, the environment is controlled by the adversary, and failure produces a false-safe outcome at the moment of maximum danger.

The zero-interaction window — the 2–15 seconds between when a physical threat becomes active and when the victim loses device access — is where these systems must perform without any user input. Detection in this window depends entirely on passive layers: computer vision, audio classification, and sensor fusion. No existing benchmark evaluates this window. No existing governance framework requires it.

The adversary in this context is not digital or anonymous. They are physically present (0–50m), environmentally familiar, and adaptive. They may hold institutional or social authority over the victim. They do not need technical knowledge to defeat passive detection. A hand over a camera lens, ambient noise at the right frequency, or a GPS dead zone can simultaneously disable all three passive layers. This threat model does not appear in adversarial ML literature, which assumes digital or white-box attackers, or in HCI literature, which assumes cooperative users.

This paper names the gap precisely and provides the tools to close it.

---

## 2. Related Work

### 2.1 Adversarial Machine Learning

Adversarial ML research addresses evasion, poisoning, and extraction attacks against ML models [Goodfellow et al., 2015; Carlini & Wagner, 2017]. The dominant adversary model assumes digital access — either black-box query access or white-box knowledge of model weights. Physically proximate adversaries with environmental but not digital access are not modelled. The failure modes documented here — passive-layer degradation without device contact — are structurally analogous to input-level probe evasion but occur at the sensing layer rather than the model layer.

### 2.2 HCI and Safety-Critical Systems

HCI research on safety apps (e.g., bSafe, Safetipin, Ola Safety) focuses on usability, adoption, cooperative interaction, and technology-mediated support systems for survivors of abuse [Dimond et al., 2011; Freed et al., 2018]. Existing evaluation protocols assume the user can intentionally activate or interact with the system. Adversarial conditions — where the adversary controls the environment and the user cannot act — remain outside the scope of this literature.

### 2.3 Gender-Based Violence and Technology

Research on technology-facilitated gender-based violence (TFGBV) examines stalkerware, intimate partner surveillance, NCII, doxxing, coercive control, and online harassment [Freed et al., 2018; Chatterjee et al., 2018; Woodlock, 2017]. This literature demonstrates that adversaries increasingly exploit digital systems to extend coercive control into victims’ physical and social environments. However, physical-world adversarial manipulation of AI-driven safety systems — including passive sensing layer degradation — is not addressed. The intersection of adversarial ML and GBV-specific threat models therefore remains structurally unoccupied.

### 2.4 AI Safety Governance

Major AI governance frameworks — EU AI Act, NIST AI RMF, ISO 42001, India DPDP Act 2023 — specify accuracy, fairness, and transparency requirements. Evaluation protocols in all five frameworks assume cooperative users and standard benchmark datasets. None require passive-detection-only testing. None address adversary-induced sensing layer failure.

### 2.5 Research Gap

No existing work combines: (1) a physically proximate adversary model, (2) passive-detection-only evaluation, and (3) women's safety deployment context. Confirmed across nine sources prior to this research. ZIDR does not appear in any published benchmark, evaluation standard, or governance framework.

---

## 3. Threat Taxonomy

### 3.1 Framework Structure

The taxonomy is organized across three dimensions:

- **Attack surface layers (4):** Sensing → Processing → Communication → Response
- **Attack methods (5):** Suppress, Corrupt, Spoof, Exhaust, Intercept
- **Adversary access levels (6):** Access Level 0 (physical proximity only) through Access Level 5 (full device access)

The core finding: the most dangerous attacks require the least technical sophistication. Access Level 0 attacks — requiring only physical presence — can simultaneously defeat all three passive detection layers.

### 3.2 Layer Definitions

| Layer | Components | Example Attack |
|---|---|---|
| Sensing | Camera, microphone, GPS, accelerometer | Hand over lens; ambient noise injection |
| Processing | On-device ML inference | Model confidence suppression via input manipulation |
| Communication | Network, SMS, data upload | Signal jamming; GPS dead zone exploitation |
| Response | Alert delivery, escalation | Alert suppression; false-safe output |

### 3.3 Adversary Access Levels

| Level | Access Type | Example |
|---|---|---|
| 0 | Physical proximity only | Covers camera; generates masking noise |
| 1 | Incidental device contact | Briefly blocks sensor; interferes with GPS receiver |
| 2 | Full device access | Grabs device; disables app or hardware |
| 3 | Environmental control | Controls lighting, acoustics, GPS coverage |
| 4 | System knowledge | Knows detection thresholds; times attack to exploit them |
| 5 | Social leverage | Institutional or economic authority inhibits victim from triggering alert |

**Key insight:** L5 (social leverage) is structurally distinct — it requires no technical knowledge and is the only access level entirely absent from adversarial ML frameworks and governance standards.

---

**Figure 1 — Threat Taxonomy Heatmap: Minimum Adversary Access Level by Layer and Attack Method**

*Each cell shows the lowest access level at which the attack was observed across 14 grounded scenarios. Lower = more accessible adversary = higher governance urgency.*

| Attack Surface Layer | Suppress | Corrupt | Spoof | Exhaust | Intercept |
|---|---|---|---|---|---|
| **Sensing** (camera, mic, IMU, GPS) | 🔴 L0¹ | 🔴 L0² | 🟠 L2 | — | 🟠 L2 |
| **Processing** (on-device inference) | 🟡 L3 | 🟡 L3 | 🟡 L4 | — | — |
| **Communication** (network, SMS) | — | 🔴 L0³ | — | — | 🔴 L0⁴ |
| **Response** (alert delivery) | 🟡 L5⁵ | — | — | 🔴 L0⁶ | 🟠 L2 |

**Shading key:** 🔴 L0–L1 (proximity only — highest risk) · 🟠 L2–L3 (device/environmental access) · 🟡 L4–L5 (system knowledge or social leverage) · — not observed in current scenario library

¹ **U-01 (Mumbai local train, peak hours):** Crowd density + transit vibration + ambient noise simultaneously defeat camera, audio, and IMU at L0 — physical proximity alone. No device contact required.  
² **U-01, U-07 (Transit / social venue):** Ambient noise corrupts audio classifier below detection threshold; crowded or dim environment corrupts vision proximity detection. Achieved at L0 in high-density environments.  
³ **U-02 (App-based cab, night route):** Driver exploits known GPS blackspots; sensor fusion degrades below alert threshold with only environmental knowledge.  
⁴ **R-01, R-03 (Agricultural field / isolated road):** No cellular signal — alert cannot transmit even if correctly triggered. Network interception requires only knowledge of dead zone locations; no device access.  
⁵ **U-03, R-04 (Workplace / village authority):** Institutional or community authority suppresses victim agency — alert never initiated. Social leverage (L5) requires no device contact or technical knowledge; it is the only access level structurally absent from adversarial ML frameworks.  
⁶ **U-05 (Bus stop, late night):** Repeated false proximity alerts over weeks condition emergency contacts to ignore notifications. Achieved at L0 over time — the only cross-layer attack requiring zero technical access.

---

## 4. Scenario Library

Fourteen illustrative scenarios — 9 urban, 5 rural — developed for the Indian deployment context and consistent with patterns documented in NCRB Annual Reports (2019–2023) and Safetipin urban safety audit reports. Scenarios are designed to demonstrate the threat taxonomy; individual citation gaps are flagged in the extended scenario library (Appendix A; Zenodo DOI above).

Each scenario specifies:
- Attack method and adversary access level
- Deployment context (transit, workplace, rural road, domestic)
- Passive layer failure mode triggered
- Governance gap exposed

**Sample scenario — Urban Transit (Access Level 0):**  
Adversary positions themselves at 0–2m on public transit at night. Activates ambient noise source at frequency masking distress audio classifier threshold. Simultaneously positions body to block camera field of view. Victim has 3–8 seconds of zero-interaction window. All three passive layers fail. No alert fires.

---

## 5. Zero-Interaction Detection Rate (ZIDR)

### 5.1 Definition

**ZIDR** is the proportion of adversarial attack scenarios correctly detected and alerted without any user action, under adversary-induced passive-layer degradation conditions.

$$\text{ZIDR} = \frac{|\{s \in S_{\text{adv}} : \text{alert}(s) = 1, \text{user\_action}(s) = 0\}|}{|S_{\text{adv}}|}$$

Where:
- $S_{\text{adv}}$ = set of adversarial attack scenarios from the taxonomy
- $\text{alert}(s) = 1$ = correct alert fired for scenario $s$
- $\text{user\_action}(s) = 0$ = no user interaction occurred

### 5.2 Distinction from Existing Metrics

Any evaluation that includes a button press, keyword trigger, or check-in response is evaluating a *different system* than the one that must function in the zero-interaction window. Existing accuracy benchmarks measure performance with cooperative users. ZIDR measures performance *against* an adversary, *without* a user. These are not the same test.

| Metric | Adversary modelled | User interaction required | Passive-only |
|---|---|---|---|
| Standard accuracy | No | Yes | No |
| Robustness (AML) | Digital/white-box | No | No |
| ZIDR | Physically proximate | No | Yes |

### 5.3 Measurement Protocol

1. Select scenario set from taxonomy (minimum: all Access Level 0–2 scenarios)
2. Simulate adversary-induced passive layer degradation per scenario specification
3. Run system under test with user interaction disabled
4. Record alert fired (1) or not (0)
5. Compute ZIDR across scenario set
6. Report: overall ZIDR, ZIDR by attack layer, ZIDR by adversary access level

---

**Figure 2 — Zero-Interaction Window: Passive Layer Status Under L0 Adversary**

*Scenario: U-01 (Mumbai local train, peak hours). Adversary access level: L0 (proximity only).*

```
 T = 0s                 T = 2–15s                           T > 15s
 |                           |                                   |
 Threat becomes active.      |<---- ZERO-INTERACTION WINDOW ---->|   Standard
 Adversary reaches           |                                   |   benchmarks
 proximity threshold.        |  Passive detection only.          |   begin here.
 No user action possible.    |  User-triggered functions off.    |
 ─────────────────────────────────────────────────────────────────────────────

 Passive layer status at T = 8s (L0 adversary, U1/T1 context):

   Camera (CV)        [██████████████████]  DEFEATED  crowd occlusion — L0
   Audio (ASR)        [██████████████████]  DEFEATED  ambient noise > 85 dB — L0
   Accelerometer      [██████████████████]  DEFEATED  indistinct from transit vibration — L0
   GPS                [████              ]  DEGRADED  functional but insufficient alone

   Functional layers: 1 of 4    ZIDR = 0.25

 ─────────────────────────────────────────────────────────────────────────────
   Benchmark accuracy (cooperative user, controlled environment):   0.95
   ZIDR              (L0 adversary, zero-interaction window):        0.25
   A system that passes benchmark testing can fail entirely in the
   window that determines whether an alert fires.
 ─────────────────────────────────────────────────────────────────────────────
```

---

### 5.4 Governance Implication

ZIDR provides the operationalisable definition missing from EU AI Act conformity assessment for Annex III high-risk AI systems. Women's safety apps qualify under Annex III. Conformity assessment currently has no clause requiring passive-detection robustness testing. ZIDR fills that clause.

---

## 6. Governance Gap Analysis

### 6.1 Framework Coverage

Five frameworks reviewed: EU AI Act, NIST AI RMF, ISO 42001, India DPDP Act 2023, India IT Act.

| Framework | Accuracy req. | Robustness req. | Passive-detection req. | Adversary model |
|---|---|---|---|---|
| EU AI Act | Yes (Annex III) | Partial | None | None |
| NIST AI RMF | Yes | Partial | None | None |
| ISO 42001 | Yes | Partial | None | None |
| India DPDP 2023 | No | No | None | None |
| India IT Act | No | No | None | None |

### 6.2 Structural Absence

The gap is not a single missed clause. Every framework evaluates AI systems on accuracy metrics measured with cooperative users. None specify:
- Passive-detection-only evaluation conditions
- Adversary-induced sensing layer failure scenarios
- Social conditioning as an attack vector
- Zero-interaction window performance requirements

### 6.3 Recommended Clause Language (EU AI Act / CEN-CENELEC)

> *Conformity assessment for high-risk AI systems deployed in personal safety contexts (Annex III) shall include evaluation of passive-detection robustness under adversary-induced sensing layer degradation. Systems shall report Zero-Interaction Detection Rate (ZIDR) across a standardised adversarial scenario set. ZIDR shall be reported separately from cooperative-user accuracy metrics.*

---

## 7. Probe Robustness Tool Specification

A Python CLI for evaluating any safety system profile against this taxonomy, with ZIDR as a first-class output metric.

**Inputs:** System capability profile (YAML), scenario set (JSON from taxonomy library)  
**Outputs:** ZIDR score, per-layer breakdown, governance gap flags, audit report

**CLI interface (specification):**
```bash
zidr-probe --system-profile system.yaml \
           --scenario-set taxonomy/urban_access_0_2.json \
           --output report.json
```

**Output schema:**
```json
{
  "zidr_overall": 0.23,
  "zidr_by_layer": {
    "sensing": 0.15,
    "processing": 0.31,
    "communication": 0.28,
    "response": 0.18
  },
  "governance_gaps": ["EU_AI_Act_Annex_III", "NIST_RMF_GOVERN"],
  "scenarios_tested": 14,
  "scenarios_detected": 3
}
```

Implementation is Phase 2. Specification and scenario library available at: github.com/pretzelslab/ai-safety-research/tree/main/womens_safety_adversarial

---

## 8. Connections to AI Safety Research

**Adversarial robustness:** Passive-layer defeat by a physically proximate adversary mirrors input-level probe evasion. The underlying problem — robustness under adversarial conditions outside training distribution — is the same. The attack surface is the sensing layer rather than the model.

**Distributional shift:** Safety apps trained on clean audio and video datasets encounter adversarially degraded inputs in deployment. This is a controlled, intentional distributional shift — the adversary *is* the distribution shift.

**Specification gaming:** Social conditioning as an attack vector (Level 2) is a real-world instance of specification gaming: the adversary exploits the gap between what the system is specified to detect and what cultural context prevents the user from allowing it to detect.

**High-stakes deployment:** Women's safety AI is already deployed at scale in resource-constrained, high-noise, adversarially demanding environments without robustness standards. It is an urgent real-world test case for safety-critical AI governance.

---

## 9. Limitations

- **Scenario library is not exhaustive.** 14 scenarios cover urban/rural Indian context; generalization to other geographies requires expansion.
- **ZIDR measurement is unvalidated empirically.** Baseline ZIDR values, minimum acceptable thresholds, and protocol replication standards require partner validation with safety app vendors.
- **Sociotechnical attack surface is underspecified.** Level 2 (social conditioning) scenarios are qualitative; operationalizing them for quantitative ZIDR measurement requires additional methodology.
- **Tool specification only; implementation pending.** The Probe Robustness Tool is a design specification. Phase 2 implementation is planned.

---

## 10. Future Work

- **ZIDR baseline measurement** — Controlled testing with 1–2 safety app vendors; establish minimum plausible ZIDR thresholds and replicable protocol.
- **Policy brief** — Targeted at CEN-CENELEC and India Bureau of Indian Standards; recommended clause language for conformity assessment standards.
- **Expanded scenario library** — Coverage beyond Indian urban/rural context; additional geographies and deployment environments.
- **Level 2 operationalization** — Methodology for quantifying social conditioning as an attack surface in ZIDR measurement.
- **Academic submission** — Target ACM FAccT 2027; contribution: first threat taxonomy and evaluation metric for women's safety AI adversarial robustness.

---

## 11. Conclusion

Women's safety AI systems face a threat that no existing benchmark tests and no existing governance framework governs: a physically proximate adversary who defeats passive detection without device access or technical knowledge. This paper provides three contributions to close that gap: a threat taxonomy grounding the attack surface, ZIDR as an operationalisable evaluation metric, and governance gap analysis with recommended clause language for standards bodies. A system that achieves 95% benchmark accuracy and 0% ZIDR is not a safe system. Making that distinction visible — and testable — is the policy contribution of this work.

---

## References

Dimond, J. P., Fiesler, C., & Bruckman, A. (2011). Domestic violence and information communication technologies. *Interacting with Computers*, 23(5), 413–421.

Freed, D., Palmer, J., Minchala, D., Levy, K., Dell, N., & Ristenpart, T. (2018). “A Stalker’s Paradise”: How Intimate Partner Abusers Exploit Technology. In *Proceedings of the 2018 CHI Conference on Human Factors in Computing Systems* (CHI ’18).

Chatterjee, R., Doerfler, P., Orgad, H., Havron, S., Palmer, J., Freed, D., Levy, K., Dell, N., McCoy, D., & Ristenpart, T. (2018). The Spyware Used in Intimate Partner Violence. In *Proceedings of the 2018 IEEE Symposium on Security and Privacy (SP)*, 441–458.

Woodlock, D. (2017). The Abuse of Technology in Domestic Violence and Stalking. *Violence Against Women*, 23(5), 584–602.

---

## Appendix A: Full Scenario Library

*14 grounded scenarios. Urban (U-01–U-08) and rural (R-01–R-05). All scenarios confirmed 2026-05-05. ⚠ = novel attack vector not documented in existing adversarial ML or GBV literature.*

| ID | Scenario | Context | Adv. Type | Min. Access | Attack Method(s) | Passive Layer(s) Defeated | Governance Gap |
|---|---|---|---|---|---|---|---|
| U-01 | Mumbai Local Train, Peak Hours | U1, T1 | Opportunistic | L0 | Suppress + Corrupt | Vision · Audio · Sensor Fusion | All — no transit sensor fusion standard |
| U-02 | App-Based Cab, Night Route | U1→R2 | Adaptive | L1 | Intercept + Spoof | Sensor Fusion · Vision · Audio | All + India DPDP — no location-spoofing resistance |
| U-03 | Office / Workplace, Authority Figure | U2 | Informed | L5 | Suppress (social) | None (alert not triggered) | All — sociotechnical suppression ungoverned |
| U-04 | Street Market, Shoulder Bag Obstruction | U1 | Opportunistic | L0 | Suppress | Vision · Audio | All — no CV occlusion robustness standard |
| U-05 | Bus Stop, Late Night — Exhaustion Attack | U1 | Adaptive | L0 | Exhaust | Response (human layer) | All — no alert exhaustion testing req. ⚠ |
| U-06 | College Campus, Known Acquaintance | U2 | Adaptive | L1 | Corrupt | Vision · NLP | All — NLP coercion bypass untested |
| U-07 | Social Venue / Party, Noise + Alcohol | U2 | Opportunistic | L0 | Suppress + Corrupt | Audio · Vision | All — no high-noise certification ⚠ |
| U-08 | Public Toilet / Changing Area, Device Grab | U1, U2 | Opportunistic | L2 | Intercept | Communication · Response | All — no device interception standard ⚠ |
| R-01 | Agricultural Field, Isolated Worker | R2 | Adaptive | L0 | Intercept + Suppress | Communication | EU AI Act · NIST AI RMF · India DPDP |
| R-02 | Village Pathway, Dusk | R1 | Adaptive | L0 | Suppress | Vision · Response | All — no low-light rural CV standard |
| R-03 | Isolated Road, Moving Vehicle | R2, T1 | Informed | L0 | Intercept + Corrupt | Sensor Fusion · Communication | Cross-jurisdictional — no rural connectivity req. |
| R-04 | Village Common, Community Authority | R1 | Informed | L5 | Suppress (social) | None (alert not triggered) | All + India IT Act — social suppression |
| R-05 | Agricultural Employer, Seasonal Labour | R1, R2 | Informed | L5 | Suppress (economic) | Response · Vision · Audio | All — economic coercion vector ⚠ |

**Context codes:** U1 = urban public · U2 = urban semi-private · R1 = rural public · R2 = rural isolated · T1 = transit  
**Min. Access** = lowest adversary access level at which attack was observed (see Section 3.3 + Figure 1).

---

## Appendix B: Taxonomy Reference Table

See **Figure 1** (Section 3.3) for the full 4-layer × 5-method heatmap with minimum access levels and scenario footnotes. For the per-scenario breakdown of all layer × method combinations, see Appendix A above.

The full structured scenario library (YAML format, machine-readable for probe tool input) is available at:  
`github.com/pretzelslab/ai-safety-research/tree/main/womens_safety_adversarial/probe_robustness/scenarios/`

---

