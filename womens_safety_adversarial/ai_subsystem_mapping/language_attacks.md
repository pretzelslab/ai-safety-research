# AI Subsystem Mapping — Language / NLP

## What This Subsystem Does

**Plain language:** Some safety apps use language AI to check in with the user — asking "Are you safe?" at intervals and classifying the reply. Others let the user describe a threatening situation in text or voice, and the AI judges whether it's dangerous. A third variant is a chatbot that helps users report an incident or request help. The language model reads what the user (or the adversary) writes or says and decides what to do next.

**Technical components:**
- Check-in prompt + response classification ("safe" vs. "distress" signal)
- Free-text situation description → threat classification
- Natural language understanding (intent detection, sentiment analysis)
- Named entity extraction (location, person names)
- Conversational AI / chatbot for safety reporting
- Code word / phrase detection (user-defined distress triggers)

---

## Attack Surface Map

| Attack Method | How It Works Against NLP | Min Access | Deployment Contexts |
|---|---|---|---|
| **Suppress** | Prevent the victim from typing, speaking, or engaging with the check-in prompt — explicit or implicit threat of consequences if the device is used | L0–L5 | U2, R1, R2 |
| **Corrupt** | Coerce victim to respond "I'm fine" to check-in; dictate neutral language the model won't flag as distress | L0–L5 | U2 |
| **Spoof** | Intercept device and respond to check-in prompt on victim's behalf ("All good, heading home") | L1–L2 | U2 |
| **Exhaust** | Trigger repeated false check-in alerts until contacts stop responding; condition victim to dismiss alerts habitually | L0 | U1, U2 |
| **Intercept** | Read or delete check-in notifications before victim sees them; disable the app or silence notifications | L1–L2 | U2 |

---

## Evasion Mechanisms — Detail

### 1. Neutral Language Coercion (L0, Highest Risk)

NLP threat classification relies on distress markers: urgent phrasing, explicit threats, high-emotion vocabulary, help-seeking language. An adversary with social proximity can coerce the victim to respond in neutral language — "I'm fine", "just out for a walk", "heading home" — that the model correctly classifies as safe.

**This is a sociotechnical attack, not a model evasion.** The model is functioning correctly — the input is genuinely neutral. The adversary has defeated the system by removing the distress signal at source, not by bypassing the classifier.

**Critical distinction from audio:** Unlike voice stress detection, which has involuntary prosodic biomarkers (F0 spike, jitter) that exist below conscious control, text and spoken check-in responses are fully under conscious control. Any adversary with social leverage (L1+) can force a non-distress response. No NLP model can detect a threat the victim has been coerced into not reporting. **This is a fundamental design-level limitation of consent-dependent check-in systems, not a modelling failure.**

### 2. Prompt Interception / Device Response Spoofing (L1–L2)

If the adversary has the device (L2) or can see the screen (L1), they can respond to check-in prompts directly. "Are you safe?" → adversary types "Yes, all good" on victim's behalf. The NLP model receives a genuine "safe" response with no anomalies to detect.

**Mitigation direction (out of scope v1.0):** biometric authentication on check-in response (fingerprint, typing cadence, face) would partially address this — but each adds friction that reduces adoption and creates new attack surfaces. **[CITATION NEEDED: no existing literature on biometric-gated safety check-ins — novel gap, flag as such]**

### 3. Semantic Evasion by Informed Adversary (L4)

If the adversary understands the NLP model's classification features — through direct knowledge, prior research, or learning over time from observed system responses — they can coach the victim to describe a threatening situation in semantically neutral language that scores as low-risk. For example, instead of "he's following me and I'm scared," the coerced response becomes "I think I know where I'm going, I have company."

**Requires L4 system knowledge for the precise version.** The naive version (coerce "I'm fine") is simpler and available at L0. The L4 version is relevant for intimate-partner and workplace contexts where the adversary has observed system responses over multiple incidents.

### 4. Social Hesitation — The Non-Technical Failure (L5)

The most common NLP system failure in women's safety apps is that the victim does not initiate the interaction at all. In semi-private, authority-asymmetric contexts (U2, U3), the perceived cost of triggering a distress signal is high:
- Fear of not being believed
- Fear of professional or social retaliation (workplace or institutional authority)
- Cultural pressure to de-escalate or "handle it"
- Prior false alarm experience reducing willingness to trigger again (exhaustion carryover from U-05)

**This is a design failure, not a model failure.** Passive triggering systems (ambient audio, CV) partially address it — but introduce the attack surfaces documented in audio_attacks.md and vision_attacks.md. No combination of passive and active sensing eliminates the underlying sociotechnical suppression dynamic.

**[CITATION NEEDED: user friction in safety app adoption — iCall / iHuman research or equivalent Indian helpline literature]**

### 5. Check-In Exhaustion (L0)

Repeated false check-in triggers — from location events, time intervals, motion events — train both emergency contacts and the victim to treat alerts as noise. Contacts become slower to respond or dismiss without confirming. The victim begins ignoring or silencing the app. This is the cry wolf failure applied specifically to the NLP check-in loop, compounding over time across all other subsystems.

---

## Highest-Risk Scenarios (cross-reference: threat_taxonomy/scenario_library/)

| Scenario | Attack | Why NLP Fails | Governance Flag |
|---|---|---|---|
| U-03 (Office Authority) | Suppress + Social L5 | Victim cannot initiate check-in; institutional authority prevents device use | No framework governs check-in suppression via authority asymmetry |
| U-06 (Campus Acquaintance) | Corrupt | Victim describes threat in neutral language under social pressure from known person | NLP not tested for adversary-coerced neutral response scenario |
| U-02 (App Cab) | Spoof | Adversary responds to check-in on victim's behalf | No authentication requirement on check-in response |
| U-05 (Bus Stop — Exhaustion) | Exhaust | Repeated triggers → contacts stop responding; victim stops triggering | No exhaustion-resistance or contact response degradation testing in any framework |

---

## Robustness Test Design

**Goal:** Quantify the NLP threat classification failure rate under coerced-neutral-response and social suppression conditions.

**Test protocol:**
1. Baseline: measure classification accuracy on distress vs. safe text pairs (standard benchmark using existing safety app NLP)
2. Coerced neutral test: rewrite distress scenarios in neutral language as a socially-pressured victim might — measure false-negative rate
3. Semantic evasion test: adversarially rewrite distress descriptions to avoid known distress markers — measure classification evasion rate at L4 access
4. Spoofed check-in: inject neutral "safe" responses at check-in prompts simulating adversary device access — measure proportion of undetected adversary-controlled responses
5. Exhaustion simulation: send repeated false triggers over N sessions — measure contact response rate degradation across sessions

**Output metric:** NLP Coercion Bypass Rate (CBR) — proportion of adversarially-coerced or neutral-language responses that the model classifies as "safe" when ground-truth threat is present. Higher CBR indicates the model is accurate on cooperative users but fails entirely under social coercion.

---

## Governance Coverage

| Framework | Relevant Clause | What It Covers | What It Misses |
|---|---|---|---|
| EU AI Act | Art. 13 (transparency), Annex III | High-risk AI transparency and accuracy | No coerced-neutral-response testing; no check-in authentication requirement |
| NIST AI RMF | GOVERN 6.1, MEASURE 2.2 | Sociotechnical risk assessment | Sociotechnical suppression not operationalised in test protocol |
| India DPDP Act | Consent requirements | User data consent framework | Coerced consent scenario not addressed |
| ISO 42001 | Clause 9.1 | Performance monitoring | NLP-specific adversarial conditions not defined |

**Core gap:** No framework requires NLP-based safety check-ins to be tested under conditions of social coercion, authority asymmetry, or user hesitation. All NLP accuracy benchmarks assume a freely cooperating user. **This is the most fundamental design-level governance gap in the subsystem mapping: the adversarial attack requires no technical knowledge — only social proximity — and is entirely invisible to the model.**
