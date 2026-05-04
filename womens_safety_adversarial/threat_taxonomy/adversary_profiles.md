# Adversary Profiles

## Core Framing

This research deliberately departs from the intimate partner violence (IPV) framing dominant in existing literature. The adversary is frequently NOT an intimate partner. Restricting the model to IPV understates the real threat surface and excludes the majority of harassment and assault contexts.

## Primary Adversary Profile

| Dimension | Range |
|---|---|
| **Proximity** | 0–50 metres, physically present |
| **Environmental familiarity** | Knows the space, victim's patterns, timing, bystander likelihood |
| **Relationship to victim** | Acquaintance · colleague · authority figure · stranger with local knowledge |
| **Relationship NOT assumed** | Intimate partner (separate, well-covered literature) |
| **Adaptability** | Modifies behavior based on observed system responses in real time |
| **Device access** | Ranges: none → incidental contact → full grab |
| **System knowledge** | Ranges: naive → partial → fully informed |
| **Social leverage** | May hold cultural authority, employer status, or institutional position that reduces victim's willingness to trigger alert |

## Adversary Subtypes

### Opportunistic
No technical knowledge of the safety system. Uses proximity, timing, and environmental positioning to suppress detection. Relies on the gap between what the system can detect and what actually happens at close range. Hardest to govern because no system knowledge is required — L0 access is enough.

### Adaptive
Has observed the system respond (or fail to respond) before. Learns detection thresholds through repeated interaction. Can train the victim's contacts to dismiss alerts over time (exhaustion). Represents the transition from one-off threat to sustained threat actor.

### Informed
Has working knowledge of how AI safety systems function — detection windows, trigger thresholds, network dependency. May hold institutional authority over the victim (employer, supervisor, family authority figure in a semi-private setting). Can exploit social dynamics to prevent alert being triggered at source before any technical attack is needed.

### Environmental Controller
Controls the physical conditions of the space — lighting, ambient noise, network availability. Venue owner, employer, or building manager. Can systematically defeat the sensing layer without touching the device. Most dangerous in R2 (rural isolated) and U2 (urban semi-private) contexts.

## What Makes This Adversary Different from Standard Adversarial ML

| Assumption | Standard Adversarial ML | This Research |
|---|---|---|
| Adversary location | Remote / digital | Physically present |
| Model access | White-box or black-box API | None — behavioral observation only |
| Attack timing | Asynchronous | Real-time, seconds-level |
| Victim agency | Not modeled | Central — victim hesitation is an attack surface |
| Context knowledge | Limited | Deep environmental familiarity |
| Governance coverage | OWASP, MITRE ATLAS | Not covered by any existing framework |

## Sociotechnical Attack Surfaces

The adversary does not need to defeat the AI system if the victim does not trigger it.

Key sociotechnical vectors:
- **Authority suppression** — victim does not trigger alert because adversary holds employer, family, or cultural authority
- **Social conditioning** — repeated false alarm exhaustion trains victim to doubt whether triggering is warranted
- **Bystander diffusion** — in crowded contexts, victim assumes someone else will act; adversary exploits this passivity
- **Shame / stigma** — cultural context makes triggering a public safety alert feel more costly than the threat

These vectors are absent from every governance framework reviewed. They require no technical capability — only social proximity and context knowledge (L5 access).
