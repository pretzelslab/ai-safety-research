# Attack Method Matrix

Cross-reference: attack method × AI subsystem × evasion mechanism

## How to Read This

Each cell answers: "If an adversary uses [method] against [subsystem], what does the evasion look like and what access does it need?"

## Matrix

| Attack Method | Vision/CV | Audio Classification | Sensor Fusion | NLP/Language | Min Access |
|---|---|---|---|---|---|
| **Suppress** | Block camera angle (bag, body position, lighting) | Create ambient noise above distress threshold (crowd, traffic, music) | Move outside GPS fix zone; disable accelerometer context | Prevent distress phrase from being spoken or heard | L0 |
| **Corrupt** | Partial occlusion — stay at edge of detection confidence | Speak calmly or below voice stress threshold until last moment | Intermittent signal — move in/out of detection range | Couch threat in neutral language the NLP model won't flag | L0 |
| **Spoof** | Present non-threatening body language while in attack posture | Play background audio that normalises the scene | Fake GPS location via signal injection | Dictate a cover narrative to victim's check-in prompt | L1–L3 |
| **Exhaust** | Trigger proximity alerts repeatedly in safe contexts | Trigger noise alerts repeatedly until contacts disable notifications | Repeated false accelerometer events (bumps, falls) | Repeated false check-in triggers until system ignored | L0 |
| **Intercept** | — | — | Block SMS/data transmission (Faraday, signal dead zone) | Grab device before alert message is sent | L1–L2 |

## Highest-Risk Combinations

| Combination | Why Dangerous | Governance Gap |
|---|---|---|
| Suppress × Audio × U2 (semi-private) | Adversary controls ambient noise in venue | No framework requires audio robustness testing under adversary-controlled noise |
| Corrupt × Vision × T1 (transit) | Crowded moving vehicle, partial occlusion trivially achievable | No certification standard for CV in moving/crowded transit context |
| Intercept × Communication × R2 (rural isolated) | No network = no alert regardless of trigger | No framework addresses dead-zone failure in rural deployment |
| Exhaust × Response × any | Trains contacts to ignore alerts over time | No framework requires exhaustion resistance testing |
| Suppress × Social (L5) × U2 | Authority figure prevents trigger at source — no technical defeat needed | No framework governs sociotechnical suppression |
