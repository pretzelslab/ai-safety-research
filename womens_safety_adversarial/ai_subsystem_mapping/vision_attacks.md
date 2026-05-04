# AI Subsystem Mapping — Vision / Computer Vision

## What This Subsystem Does

**Plain language:** The camera on the victim's phone (or a wearable) feeds live video to a model that looks for signs of danger. It might detect a person moving unusually close, sudden body language changes (raised arm, grabbing motion), or a face that matches a known perpetrator. Some apps use it passively; others activate it when the user presses a button or when another sensor (accelerometer) fires.

**Technical components:**
- Object detection (person proximity, intruder detection)
- Pose estimation (gesture classification — raised arm, grabbing motion)
- Face recognition (optional; rare in consumer safety apps)
- Scene classification (lighting conditions, indoors vs. outdoors)

---

## Attack Surface Map

| Attack Method | How It Works Against CV | Min Access | Deployment Contexts |
|---|---|---|---|
| **Suppress** | Block camera angle — adversary positions body, bag, or object to eliminate line of sight before detection fires | L0 | U1, U2, T1 |
| **Corrupt** | Partial occlusion at edge of detection confidence; dim lighting or motion blur during movement degrades model accuracy | L0 | U1, U2, T1, R1 |
| **Spoof** | Present non-threatening posture (open palms, relaxed stance) while maneuvering into attack position | L0 | U2 |
| **Exhaust** | Move into and out of proximity detection range repeatedly in safe contexts to train contacts to ignore alerts | L0 | U1 |
| **Intercept** | Physically cover, flip, or disable device camera before detection window closes | L1–L2 | U1, U2 |

---

## Evasion Mechanisms — Detail

### 1. Angle Suppression (trivially achievable, L0)

The field of view of a rear phone camera is approximately 75–90°. A person approaching from a perpendicular angle or from behind the device exits the detection zone entirely. In crowded environments (Mumbai local train, market), other bodies fill the frame and prevent proximity detection. No adversary system knowledge required.

### 2. Confidence Corruption via Occlusion

Object detection models (YOLO, MobileNet-SSD, MediaPipe) assign bounding-box confidence scores. Partial occlusion — a bag strap, arm, or pillar — degrades the intersection-over-union score below threshold. In a crowded scene, fragmentation of the adversary's bounding box is routine, not anomalous.

**Critical finding:** Most real-time mobile CV models operate at confidence threshold ≥ 0.7 for triggering alerts. A partially occluded adversary will routinely score 0.4–0.6 — below alert threshold, but above false-negative recognition. The model "sees" something but does not fire. **This is the corruption sweet spot — achievable at L0, no system knowledge required.**

### 3. Lighting Corruption (L0, environmental)

Low-light scenes degrade detection accuracy sharply. Standard consumer safety apps do not apply adaptive brightness correction pre-inference. A transit vehicle switching between a lit station and a dark tunnel creates a 200–400ms blind window — enough for a rapid approach. **[CITATION NEEDED: mobile CV model accuracy under low-light conditions — see Zhu et al. 2022 or equivalent benchmark]**

### 4. Posture Spoofing

Pose estimation models classify keypoint sequences (e.g., raised arm = aggression signal). An adversary who understands the gesture trigger can maintain an open-palm, non-aggressive keypoint sequence until the moment of contact. Requires L4 system knowledge for the precise version; naive version (don't raise arm) is L0.

### 5. Camera Block / Intercept (L1)

A phone placed in a pocket, face-down, or in a bag eliminates CV entirely. This is not an adversarial technique — it is routine phone carry. Safety apps that rely on camera activation during normal carry are nonfunctional as a primary detection modality in real-world use.

---

## Highest-Risk Scenarios (cross-reference: threat_taxonomy/scenario_library/)

| Scenario | Attack | Why CV Fails | Governance Flag |
|---|---|---|---|
| U-01 (Mumbai Local Train) | Suppress + Corrupt | Crowd density, phone orientation, transit vibration | No transit-context robustness standard |
| U-04 (Street Market) | Suppress | Bag occlusion, crowd bodies in frame | No occlusion robustness requirement |
| U-07 (Social Venue) | Corrupt | Dim lighting, motion blur | No low-light CV certification |
| U-08 (Device Grab) | Intercept | Camera covered or disabled | No physical intercept failure mode addressed |

---

## Robustness Test Design

**Goal:** Quantify at what occlusion percentage and lighting level CV-based proximity detection falls below the 0.7 confidence trigger threshold.

**Test protocol:**
1. Baseline: measure detection accuracy for approaching person at 0–5 metres, full frame, 300 lux
2. Occlusion test: introduce 10% / 25% / 50% / 75% frame occlusion (bag, body, arm) — record threshold dropout at each level
3. Lighting test: reduce lux from 300 → 100 → 50 → 10 — record accuracy at each level
4. Motion test: simulate camera at transit vibration frequencies (2–8 Hz) — record blur impact on detection
5. Adversarial posture: replace "raised arm" gesture with open-palm approach — measure false-negative rate

**Output metric:** Occlusion Evasion Threshold (OET) — the occlusion percentage at which alert confidence drops below trigger threshold for a given system. Lower OET = worse real-world robustness.

---

## Governance Coverage

| Framework | Relevant Clause | What It Covers | What It Misses |
|---|---|---|---|
| EU AI Act | Annex III, Art. 10 | High-risk CV systems must document accuracy benchmarks | Does not specify real-world occlusion or transit-vibration test conditions |
| NIST AI RMF | MEASURE 2.5 | Accuracy metrics across operational contexts | Does not mandate adversarial proximity testing |
| India DPDP Act | Data minimisation | Limits biometric data retention | Does not address attack robustness or false-negative testing |
| ISO 42001 | Clause 9.1 | Performance monitoring | Does not define CV attack surfaces or evasion test conditions |

**Core gap:** No framework requires CV robustness testing under physical proximity attack conditions. All accuracy benchmarks are evaluated on static datasets in controlled lighting — not on deployed safety apps in real-world attack scenarios. **Novel finding — not documented in existing adversarial ML literature for women's safety context.**
