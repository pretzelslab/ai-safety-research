# AI Subsystem Mapping — Audio Classification

## What This Subsystem Does

**Plain language:** The phone's microphone listens continuously (or on activation) for sounds that signal danger. This includes the victim's own voice stress or shouting, loud threatening speech from nearby, sounds of a physical altercation (impact, breaking objects), crowd aggression noise, or a specific code word or phrase the victim has set up. Some apps let the victim raise her voice and the model detects it; others wait for a specific keyword.

**Technical components:**
- Voice stress analysis (fundamental frequency spike, jitter, shimmer)
- Sound event detection (scream, impact, glass break, crowd aggression)
- Keyword / phrase detection ("help", user-defined code words)
- Speaker diarisation (who is speaking — victim or adversary)
- Ambient noise baseline estimation

---

## Attack Surface Map

| Attack Method | How It Works Against Audio | Min Access | Deployment Contexts |
|---|---|---|---|
| **Suppress** | Generate ambient noise above the distress detection threshold — crowd, music, traffic — before the victim vocalises | L0 (environmental) | U1, U2, T1 |
| **Corrupt** | Speak calmly to victim; keep scene audio below stress threshold; restrict victim's ability to vocalise | L0 | U2, R1 |
| **Spoof** | Play background audio that normalises scene classification; instruct victim to "speak normally" on threat of escalation | L0–L1 | U2 |
| **Exhaust** | Trigger noise events (music, voice) repeatedly in safe contexts until contacts silence notifications | L0 | U1, U2 |
| **Intercept** | Cover microphone (finger, case); move victim to location where ambient noise drowns any vocalisation | L1, L3 | U1, U2 |

---

## Evasion Mechanisms — Detail

### 1. Ambient Noise Suppression (L0, highest risk)

Safety apps that detect distress audio compute Signal-to-Noise Ratio (SNR) or compare against a trained ambient baseline. In environments with noise above approximately 70 dB, the distress signal is suppressed before the model can classify it.

**Real-world noise levels (Indian contexts):**
- Mumbai local train platform: ~85 dB [CITATION NEEDED: CPCB noise pollution reports, Indian Railways]
- Crowded market: ~75–80 dB
- Social venue (party, bar): ~80–90 dB
- Rural road with vehicle traffic: ~70–75 dB

At these levels, a scream at ~90 dB must exceed ambient by only 5–20 dB to be detectable. Panic, social suppression, and adversary proximity all reduce peak vocal output.

**Novel finding:** Urban Indian soundscapes have higher baseline noise than the Western environments used to calibrate most safety app audio models. Standard Western-calibrated models will have higher false-negative rates in Indian urban deployments. **[CITATION NEEDED: no direct citation — novel claim requiring empirical validation]**

### 2. Voice Stress Threshold Corruption (L0)

Voice stress analysis uses prosodic features: fundamental frequency (F0) spike, increased jitter and shimmer, shorter utterance duration, higher energy variation. An adversary can corrupt this without any system knowledge:
- Speaking to the victim in a calm, controlled tone (reduces victim's stress vocal response)
- Restricting the victim's ability to vocalise (physical proximity, hand near face)
- Applying social leverage to suppress visible distress (L5: "stay calm or this gets worse")

**Adversary does not need to know the model features. Calm environmental control is sufficient at L0.**

### 3. Keyword Suppression (Sociotechnical, L0–L5)

Keyword detection requires the victim to vocalise in the adversary's presence. This is a sociotechnical attack surface: the adversary's presence, authority, or implicit threat suppresses the victim's willingness to trigger the alert. This is especially acute when:
- Adversary is a figure of institutional authority (L5: employer, senior colleague)
- Victim is in a semi-private space where shouting would cause social harm (U2)
- Victim has been conditioned over time not to trigger alerts (cry wolf effect from U-05)

**No audio model can defend against suppression at the human layer. This is a governance gap, not a technical one.**

### 4. Microphone Intercept / Physical Cover (L1)

Placing a hand, object, or case cover over the microphone reduces audio capture by 10–30 dB. A phone face-down in a pocket or closed in a bag effectively eliminates audio detection. This is not a sophisticated adversarial technique — it is a routine carry state. Safety apps that require an unobstructed microphone in a pocketed device are nonfunctional in real-world carry conditions.

---

## Highest-Risk Scenarios (cross-reference: threat_taxonomy/scenario_library/)

| Scenario | Attack | Why Audio Fails | Governance Flag |
|---|---|---|---|
| U-01 (Mumbai Local Train) | Suppress | ~85 dB ambient eliminates distress SNR | No ambient noise calibration standard for transit deployment |
| U-03 (Office Authority) | Suppress + Social L5 | Victim cannot vocalise; authority suppresses trigger intent | No framework governs sociotechnical suppression |
| U-07 (Social Venue) | Suppress + Corrupt | Party noise exceeds distress threshold; calm coercion keeps stress markers below detection | No high-noise venue certification |
| R-01 (Rural Road) | Suppress | No bystanders; vehicle traffic noise; victim alone and unobserved | No rural noise-floor calibration requirement |

---

## Robustness Test Design

**Goal:** Identify the ambient noise floor at which audio-based distress detection becomes nonfunctional, calibrated to Indian deployment conditions.

**Test protocol:**
1. Baseline: scream detection at 0 dB ambient — establish detection rate ceiling for the safety app under test
2. Noise floor sweep: inject ambient noise at 60 / 70 / 75 / 80 / 85 / 90 dB — record detection rate at each level
3. Stress suppression test: use calm-speech audio at adversary-control scenarios — measure false-negative rate for stress detection
4. Keyword test: play code-word audio at progressively reduced volume (social suppression) — measure minimum effective volume for trigger
5. Mic intercept: simulate phone in pocket and in bag — measure audio capture degradation in dB loss

**Output metric:** Audio Noise Evasion Floor (ANEF) — the ambient dB level at which detection rate falls below 0.5. Lower ANEF = worse robustness in real-world Indian deployments.

---

## Governance Coverage

| Framework | Relevant Clause | What It Covers | What It Misses |
|---|---|---|---|
| EU AI Act | Art. 13 (transparency), Annex III | Accuracy benchmarks for high-risk AI applications | No ambient-noise robustness requirement; no real-world noise condition specified |
| NIST AI RMF | MEASURE 2.5, 2.6 | Operational accuracy monitoring | No adversarial noise floor testing protocol |
| India DPDP Act | Data minimisation (audio as biometric) | Audio retention limits | No robustness or attack-surface requirement |
| ISO 42001 | Clause 9.1 | Performance monitoring | No audio-specific test conditions defined |

**Core gap:** No framework requires audio models to be tested at real-world ambient noise levels representative of Indian urban deployments. All accuracy benchmarks assume quiet-to-moderate environments. **Novel finding for Indian safety app governance — the noise baseline mismatch between Western calibration and Indian deployment is undocumented in existing governance literature.**
