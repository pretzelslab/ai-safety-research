# Governance Gap Analysis — EU AI Act

## Framework Overview

The EU AI Act (Regulation 2024/1689, in force August 2024) is the world's first comprehensive binding AI regulation. It classifies AI systems by risk tier and applies conformity requirements accordingly. The highest-risk systems (Annex III) must undergo mandatory conformity assessment, maintain technical documentation, implement risk management systems, and meet robustness and accuracy requirements before market entry.

**Why it matters for this research:** The EU AI Act is the global governance benchmark. Its risk classification determines whether women's safety AI systems face any mandatory robustness requirements at all. If they are not classified as high-risk, most binding requirements do not apply.

---

## Current Classification of Women's Safety AI

**Women's safety apps are not explicitly listed in Annex III.**

The closest Annex III categories are:
- **8(a):** AI systems intended to be used by law enforcement authorities for assessing the risk of an individual becoming a victim of criminal offences
- **6(a):** AI systems used for biometric categorisation of natural persons

Neither covers a privately deployed women's safety application (Safetipin, Himmat, Shake2Safety, generic SOS apps). These apps are used by civilians, not law enforcement, and typically do not perform biometric categorisation.

**Result:** Under the EU AI Act as written, most women's safety AI systems fall into the **limited-risk or minimal-risk tier** — requiring only transparency obligations (Art. 50), not conformity assessment, accuracy benchmarks, or robustness testing.

---

## Gap Analysis

| Attack Surface | Ungoverned by EU AI Act | Specific Clause Gap | Recommended Fix |
|---|---|---|---|
| CV proximity detection under occlusion | Not required to test under real-world occlusion conditions | Art. 15: accuracy/robustness — no physical proximity test condition specified | Amend Art. 15 to require adversarial physical proximity testing for safety-critical CV |
| Audio classification in high-ambient-noise environments | No ambient noise floor testing requirement | Art. 10: data governance — no deployment-context noise calibration | Require audio models to document operational noise floor limits and ambient calibration data |
| Sensor fusion in GPS dead zones | No offline-mode or minimum coverage requirement | Art. 9: risk management — dead-zone compound failure not addressed | Mandate fallback alert modes (stored-and-forward, Bluetooth mesh) for safety-critical apps |
| NLP under social coercion | Assumes cooperative user; coerced-neutral-response not tested | Art. 13: transparency — no adversarial user-state scenario | Require robustness testing under non-cooperative / coerced user conditions |
| Zero-interaction window | No passive-detection-only test requirement | Art. 15: accuracy — all benchmarks assume user-initiated input | Mandate Zero-Interaction Detection Rate (ZIDR) as a required accuracy metric for safety apps |
| Sociotechnical suppression (L5) | Not recognised as an attack surface anywhere in the Act | No clause addresses social/cultural suppression mechanisms | Add sociotechnical risk categories to Annex III assessment criteria |

---

## Key Findings

### Finding 1 — Classification Gap (Most Critical)
Women's safety AI does not meet the Annex III threshold for mandatory high-risk designation under current text. This means Art. 9 (risk management), Art. 10 (data governance), Art. 13 (transparency), Art. 15 (accuracy and robustness), and Art. 43 (conformity assessment) **do not apply** to most women's safety apps deployed in the EU market.

A company can deploy a women's safety app in the EU that fails in the zero-interaction window 100% of the time and be fully compliant with the EU AI Act.

### Finding 2 — Robustness Requirements Are Benchmark-Only
Art. 15 requires that high-risk AI systems achieve "appropriate levels of accuracy, robustness, and cybersecurity." The operative word is "appropriate" — defined against benchmark performance, not real-world adversarial conditions. Even for systems that do fall under Annex III, robustness is not tested under physical proximity attack, ambient noise, or zero-interaction conditions.

### Finding 3 — No Sociotechnical Attack Surface Recognition
The EU AI Act addresses technical robustness (Art. 15) and data quality (Art. 10) but has no framework for sociotechnical attack surfaces — specifically, the use of social, cultural, or institutional pressure to suppress user engagement with a safety system. This is not a gap that can be filled by amending a single article; it requires adding a new category of adversarial risk to the Act's assessment framework.

### Finding 4 — Rural / Network Dead Zone Blindspot
Art. 9 requires risk management systems but does not specify operational context requirements. Safety apps deployed in rural contexts with unreliable network coverage are not required to disclose minimum connectivity requirements or implement offline fallback modes. The compound GPS + network failure mode documented in sensor_attacks.md is entirely unaddressed.

---

## Recommended Amendments

1. **Annex III expansion:** Add "AI systems used in consumer personal safety applications intended to detect physical threat, trigger emergency alerts, or support personal safety decision-making" as a high-risk category — bringing these systems under the full conformity assessment regime.

2. **Art. 15 amendment:** Require robustness testing under adversarial physical proximity conditions, ambient noise levels representative of real-world deployment contexts, and zero-user-action passive-detection-only scenarios.

3. **Art. 9 amendment:** Mandate disclosure of minimum operational conditions (network coverage, GPS fix quality, ambient noise ceiling) in risk management documentation. Require fallback alert modes for deployments in low-connectivity contexts.

4. **New guidance on sociotechnical attack surfaces:** Issue implementing guidance under Art. 9 that explicitly includes sociotechnical suppression mechanisms (social leverage, authority asymmetry, cultural hesitation) as risk categories requiring assessment.

---

## Connection to Zero-Interaction Window

The zero-interaction window finding makes Finding 1 more severe. Not only is women's safety AI unclassified as high-risk — but even if it were, the robustness requirements in Art. 15 would not require testing for the scenario that matters most: passive detection without user action during the seconds of a physical attack.

**No amendment to Art. 15 alone can fix this. The zero-interaction window requires a new evaluation paradigm — ZIDR — that does not exist anywhere in current EU AI Act text or implementing guidance.**
