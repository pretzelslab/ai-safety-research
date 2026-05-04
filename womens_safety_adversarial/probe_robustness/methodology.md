# Probe Robustness Tool — Methodology

## Purpose

The probe robustness tool evaluates how well a women's safety AI system withstands adversarial attack under real-world deployment conditions. It does not test whether the AI model is accurate on benchmark datasets — it tests whether the system detects a threat when an adversary is actively working to prevent it.

**Plain language:** Imagine a structured test where someone simulates being an attacker — blocking the camera, making noise, moving to a dead zone — and we measure how often the safety app still fires an alert. The tool formalises that test so it can be run consistently, scored, and compared across different safety apps.

---

## Core Evaluation Philosophy

### What existing evaluations measure
Standard AI evaluation measures accuracy on held-out test sets: precision, recall, F1. The adversary is absent. The user is cooperative. The environment is controlled. These metrics are necessary but not sufficient for safety-critical personal AI.

### What this tool measures
This tool measures **adversarial robustness under physical proximity attack** — specifically:
- How much adversary-induced degradation (occlusion, noise, GPS loss, coercion) a system can absorb before detection fails
- Whether passive detection holds up when an adversary has suppressed victim agency (the zero-interaction window)
- Which attack surfaces are most exploitable for a given system profile

### Evaluation stance
The tool adopts the adversary's perspective: given a specific safety AI system, what is the minimum effort required to defeat it? Lower minimum effort = worse robustness = higher risk to the user.

---

## What the Tool Takes As Input

A safety AI system is characterised by a **system profile** (YAML file) describing:
1. Which sensing modalities are active (camera, microphone, GPS, accelerometer)
2. Whether detection is active (user-triggered) or passive (continuous background)
3. Known accuracy metrics per modality (from developer documentation or independent test)
4. Deployment context(s) the system is marketed for (U1, U2, R1, R2, T1)
5. Alert transmission method (data, SMS, offline capable or not)
6. Any published robustness testing results (or absence thereof)

An **attack scenario ID** from the scenario library (e.g., U-01, R-02) specifies which real-world context to evaluate against.

---

## Evaluation Dimensions

The tool evaluates four attack surfaces, each corresponding to one Phase 3 subsystem file, plus one cross-cutting measure:

| Dimension | What It Probes | Key Metric |
|---|---|---|
| Vision | Occlusion tolerance under proximity attack | OET — Occlusion Evasion Threshold |
| Audio | Ambient noise tolerance at Indian urban/rural levels | ANEF — Audio Noise Evasion Floor |
| Sensor Fusion | GPS + network compound failure in deployment context | SFES — Sensor Fusion Evasion Score |
| Language / NLP | Coercion bypass — adversary suppresses victim agency over check-in | CBR — NLP Coercion Bypass Rate |
| Zero-Interaction | Passive detection rate when adversary has removed victim agency | ZIDR — Zero-Interaction Detection Rate (adversary-induced) |

ZIDR is computed from the four subsystem scores — it is the cross-cutting measure of whether the system functions when an adversary has suppressed victim agency across all modalities simultaneously.

---

## Evaluation Approach

The tool does not require access to the AI model internals. It is a **black-box evaluation**: inputs are the system profile (declared capabilities and deployment context) and the attack scenario; outputs are robustness scores derived from:

1. **Declared capability vs. deployment context gap analysis** — does the system claim robustness to conditions it will actually face?
2. **Attack surface applicability scoring** — which of the five attack methods (suppress, corrupt, spoof, exhaust, intercept) apply to the system's active modalities in the given scenario?
3. **Minimum access requirement check** — what is the lowest adversary access level (L0–L5) at which the system can be defeated?
4. **Governance gap flagging** — which governance requirements (EU AI Act, NIST AI RMF, ISO 42001, India regulatory) are absent for the identified attack surfaces?

This approach makes the tool usable without model access — it works from published documentation, marketing claims, and deployment context — while still producing actionable, differentiated robustness scores.

---

## Scoring Logic

Each dimension produces a score from 0.0 to 1.0:
- **1.0** = adversary cannot defeat this surface at the required access level for the scenario
- **0.5** = adversary can defeat this surface with moderate effort or higher access level
- **0.0** = adversary can defeat this surface trivially (L0, no system knowledge)

Scores are derived from a decision tree per attack surface — documented in `evaluation_criteria.md`.

**Overall robustness score** = weighted average across the five dimensions, with weights reflecting the scenario's primary threat type (groping vs. assault vs. abduction vs. surveillance).

**ZIDR (adversary-induced)** = computed as: proportion of active sensing modalities that remain functional at L0 adversary access in the given deployment context. A system with camera, audio, and GPS active that loses all three at L0 in a T1 (transit) scenario has ZIDR = 0.0.

---

## Limitations

**This tool is a specification-based probe, not a live system test.** It evaluates based on declared system capabilities and known adversarial conditions — not by instrumenting the actual AI model. Live testing (physically running the attack against a real safety app) would produce more precise metrics but is out of scope for v1.0.

**Scores are relative, not absolute.** A score of 0.7 means "meaningfully harder to defeat than 0.3" — not "70% safe." The tool surfaces comparative weaknesses and governance gaps, not certified safety levels.

**The tool does not evaluate response layer effectiveness** (whether emergency contacts actually respond, whether authorities act). It evaluates detection and alert transmission only — up to and including successful alert delivery.
