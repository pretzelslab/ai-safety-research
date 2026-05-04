# Probe Robustness Tool — Evaluation Criteria

## How to Read This File

For each evaluation dimension, this file defines:
- The decision tree that produces a score (0.0–1.0)
- The threshold values that separate score bands
- What a score means in plain language
- Which attack scenarios the dimension is most relevant to

All thresholds are provisional — they require calibration against live system testing in Phase 5 implementation. Where specific values are not yet empirically grounded, they are marked `[CALIBRATE]`.

---

## Dimension 1 — Vision (OET: Occlusion Evasion Threshold)

**What it measures:** The minimum percentage of frame occlusion at which CV proximity detection drops below its alert confidence threshold (typically 0.7).

**Scoring decision tree:**

| Condition | Score |
|---|---|
| System has no camera-based detection | N/A (dimension excluded from overall score) |
| System claims robustness to ≥ 50% frame occlusion with published test data | 0.9–1.0 |
| System claims robustness to occlusion with no published test data | 0.5 (unverified claim) |
| System makes no occlusion robustness claim; deployed in U1/U2/T1 context | 0.2 |
| System relies on camera as primary detection modality with no occlusion claim | 0.0 |

**Lighting adjustment:** If deployed in low-light contexts (U2 venue, T1 night transit) without adaptive pre-processing, reduce score by 0.2.

**OET threshold guide (to be calibrated against live systems):**
- OET ≥ 50%: score 0.8+ (adversary needs to cover most of frame)
- OET 25–50%: score 0.5 (partial occlusion by bag or body defeats it)
- OET < 25%: score 0.2 (trivially defeated by body positioning)
- OET = 0% (camera blocked entirely defeats detection): score 0.0 [CALIBRATE]

**Primary scenarios:** U-01, U-04, U-07, U-08

---

## Dimension 2 — Audio (ANEF: Audio Noise Evasion Floor)

**What it measures:** The ambient noise level (dB) at which audio-based distress detection rate falls below 0.5.

**Indian deployment context reference levels:**
- Urban street / market: 75–80 dB
- Mumbai local train platform: ~85 dB [CITATION NEEDED: CPCB]
- Social venue (party, bar): 80–90 dB
- Rural road with traffic: 70–75 dB
- Quiet rural area: 45–55 dB

**Scoring decision tree:**

| Condition | Score |
|---|---|
| System has no audio detection | N/A |
| ANEF ≥ 90 dB with published test data | 1.0 |
| ANEF 80–90 dB with published test data | 0.8 |
| ANEF 70–80 dB with published test data | 0.5 |
| ANEF < 70 dB with published test data | 0.2 |
| No ANEF data published; deployed in U1/T1 context | 0.1 |
| Audio is primary detection modality; no noise floor data | 0.0 |

**Sociotechnical deduction:** If system relies on keyword/phrase activation (requires victim to vocalise willingly) and is deployed in U2 (authority-asymmetric) context, deduct 0.3 regardless of ANEF — social suppression applies independently of acoustic performance.

**Primary scenarios:** U-01, U-03, U-07, R-01

---

## Dimension 3 — Sensor Fusion (SFES: Sensor Fusion Evasion Score)

**What it measures:** Composite score across GPS reliability, accelerometer disambiguation, and network-dependent alert delivery in the deployment context.

**Component scores:**

| Component | Condition | Sub-score |
|---|---|---|
| GPS | Offline fallback mode exists and is documented | 1.0 |
| GPS | No offline fallback; deployed in R1/R2 context | 0.0 |
| GPS | No offline fallback; deployed in U1/T1 context | 0.4 |
| Accelerometer | IMU calibrated separately for crowded transit (groping) vs. isolated (assault) contexts | 1.0 |
| Accelerometer | Single calibration profile; deployed in T1 | 0.3 |
| Accelerometer | Single calibration profile; deployed in U1 (crowded transit) | 0.2 |
| Network / Alert delivery | SMS fallback when data unavailable | 0.8 |
| Network / Alert delivery | Data only; deployed in R2 context | 0.0 |
| Network / Alert delivery | Data only; deployed in U1/U2 context | 0.5 |

**SFES = mean of three component sub-scores.** [CALIBRATE weighting]

**Compound failure deduction:** If GPS sub-score = 0.0 AND network sub-score = 0.0 (both fail in deployment context), apply additional −0.2 to SFES to reflect the compound failure severity.

**Note on IMU calibration:** A system that does not distinguish groping-level micro-motion from crowd contact in transit contexts should score 0.2 on accelerometer regardless of other claims. This is the most underaddressed sensor fusion gap in current safety AI design.

**Primary scenarios:** U-01 (groping), U-02 (route deviation), R-02 (compound failure), T-01 (isolated vehicle assault)

---

## Dimension 4 — Language / NLP (CBR: NLP Coercion Bypass Rate)

**What it measures:** Proportion of adversarially-coerced or neutral-language responses that the NLP system classifies as "safe" when ground-truth threat is present.

**Scoring decision tree:**

| Condition | Score |
|---|---|
| System has no NLP / check-in component | N/A |
| CBR tested and published: < 20% bypass rate | 0.9 |
| CBR tested and published: 20–40% bypass rate | 0.7 |
| CBR tested and published: 40–60% bypass rate | 0.4 |
| CBR tested and published: > 60% bypass rate | 0.1 |
| CBR not tested; system relies on active user check-in | 0.2 (default assumed high bypass) |
| System uses ambient passive NLP (no check-in prompt required) | 0.5 base + adjust for audio score |

**Authority asymmetry deduction:** If deployed in U2 (workplace, campus, institutional) and relies on user-initiated check-in, deduct 0.3 — authority suppression operates at L5 regardless of model accuracy.

**Critical note:** A high CBR score does not mean the NLP system is "bad." It means the attack surface is inherent to consent-dependent check-in design. The correct response is design change (move toward passive detection), not model improvement.

**Primary scenarios:** U-03, U-05, U-06, U-02

---

## Dimension 5 — ZIDR (Zero-Interaction Detection Rate, Adversary-Induced)

**What it measures:** Whether the system can detect and alert a threat when an adversary has suppressed victim agency — the woman cannot interact with the device — through active environmental degradation of passive sensing layers.

**Framing:** ZIDR is adversarial, not usability. The zero-interaction condition is caused by an adversary removing agency, not by poor UX design.

**ZIDR computation:**

1. Count the number of passive sensing modalities active in the system (camera, audio, IMU, GPS — exclude NLP check-in which requires user action)
2. For each passive modality, determine whether it is functional at L0 adversary access in the given deployment scenario (using the scenario's context code)
3. ZIDR = (functional passive modalities at L0) / (total passive modalities)

**Functional at L0 criteria per modality in scenario:**

| Modality | Scenario | Functional at L0? |
|---|---|---|
| Camera | U1 (crowded public) | No — crowd occlusion trivially achieved |
| Camera | U2 (semi-private) | Marginal — depends on lighting |
| Camera | R2 (rural isolated) | Yes — open space, clear sightlines |
| Audio | U1 / T1 | No — ambient noise suppression at L0 |
| Audio | U2 (controlled venue) | No — adversary controls ambient noise |
| Audio | R2 (quiet rural) | Yes — low ambient, unless adversary vocalises |
| IMU | T1 (transit) | No — vehicle vibration corrupts baseline at L0 |
| IMU | R2 (rural, foot) | Marginal — open terrain, less vibration |
| GPS | R2 (dead zone) | No — dead zone exploitable at L0 |
| GPS | U1 (urban) | Yes — GPS typically available |

**ZIDR score interpretation:**

| ZIDR | Meaning |
|---|---|
| 0.75–1.0 | System retains meaningful passive detection under adversary-induced conditions. Acceptable for high-risk deployments. |
| 0.5–0.74 | Partial passive detection. System is vulnerable in specific adversary-induced conditions. |
| 0.25–0.49 | Most passive detection fails at L0. System depends heavily on user action to be effective. |
| 0.0–0.24 | Passive detection effectively defeated at L0 in this deployment context. System provides false assurance. |

---

## Overall Robustness Score

**Formula:**
```
Overall = (w_v × Vision) + (w_a × Audio) + (w_s × SFES) + (w_n × NLP) + (w_z × ZIDR)
```

**Default weights by scenario type:**

| Scenario Type | w_v | w_a | w_s | w_n | w_z |
|---|---|---|---|---|---|
| Crowded transit (groping) | 0.25 | 0.30 | 0.25 | 0.05 | 0.15 |
| Isolated vehicle (assault/abduction) | 0.15 | 0.20 | 0.35 | 0.10 | 0.20 |
| Semi-private / authority (workplace) | 0.15 | 0.15 | 0.15 | 0.35 | 0.20 |
| Rural isolated | 0.10 | 0.15 | 0.45 | 0.05 | 0.25 |

**Score bands:**

| Overall Score | Risk Level | Interpretation |
|---|---|---|
| 0.8–1.0 | Low | System withstands most adversarial conditions for this scenario. |
| 0.6–0.79 | Moderate | Meaningful robustness gaps exist. Adversary with L0–L1 access can partially defeat system. |
| 0.4–0.59 | High | Multiple attack surfaces exploitable at L0. System unreliable in adversarial conditions. |
| 0.0–0.39 | Critical | System provides false assurance. Most passive detection defeated at L0. Not suitable for high-risk deployment without redesign. |

---

## Governance Gap Flags

After scoring, the tool flags which governance requirements are absent:

| Gap Flag | Triggered When |
|---|---|
| `GOV-EU-CLASSIFICATION` | System not classified high-risk under EU AI Act Annex III |
| `GOV-EU-ROBUSTNESS` | No Art. 15 robustness evidence for physical proximity conditions |
| `GOV-NIST-SOCIOTECH` | Sociotechnical suppression not addressed in GOVERN 6.1 documentation |
| `GOV-NIST-ZIDR` | No ZIDR measurement in MEASURE 2.5 documentation |
| `GOV-INDIA-NONE` | No India regulatory robustness requirement applicable |
| `GOV-INDIA-RURAL` | Deployed in R1/R2 context with no offline fallback documented |
| `GOV-ISO-PROCESS` | ISO 42001 certified but no adversarial test evidence |
| `GOV-CROSS-ARBITRAGE` | No jurisdiction requires minimum robustness for this system |
