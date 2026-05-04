# Attack Surfaces — Classification Framework

## Four Target Layers

| Layer | Components | Example Attack |
|---|---|---|
| **L1: Sensing** | Camera/CV · microphone · GPS · accelerometer · network | Block camera angle; create ambient noise above detection threshold |
| **L2: Processing** | Vision model · audio model · LLM/NLP · sensor fusion · trigger logic | Move in/out of detection range; speak calmly until last moment |
| **L3: Communication** | SMS/data · app server · emergency contact notification · authority notification | Move victim to signal dead zone; block network at critical moment |
| **L4: Response** | Emergency contact acts · authorities respond · evidence preserved | Exhaust contacts with repeated false alarms; intercept device before evidence uploads |

## Five Attack Methods

| Method | Definition | Minimum Access |
|---|---|---|
| **Suppress** | Prevent signal from being generated | L0 (proximity only) |
| **Corrupt** | Degrade signal below detection threshold | L0 |
| **Spoof** | Inject false signals to mislead system | L1 |
| **Exhaust** | Trigger repeated false alarms until ignored | L0 |
| **Intercept** | Capture alert before it reaches help | L1 |

## Adversary Access Levels

| Level | Description |
|---|---|
| **L0** | Physical proximity only — no device contact |
| **L1** | Incidental device contact |
| **L2** | Full device access (grab, disable) |
| **L3** | Environmental control (lighting, noise, network) |
| **L4** | System knowledge — knows how the safety AI works |
| **L5** | Social leverage — cultural/institutional authority over victim |

## Deployment Contexts

| Code | Context |
|---|---|
| U1 | Urban public space (street, market, public transport) |
| U2 | Urban semi-private (office, venue, restaurant, party) |
| R1 | Rural public (road, field, village common) |
| R2 | Rural isolated (no network, no bystanders) |
| T1 | Transit — moving vehicle |

## Attack Surface Matrix — Method × Layer

| | L1 Sensing | L2 Processing | L3 Communication | L4 Response |
|---|---|---|---|---|
| **Suppress** | ●● high | ● medium | ○ | ○ |
| **Corrupt** | ●● high | ●● high | ○ | ○ |
| **Spoof** | ● medium | ● medium | ● medium | ○ |
| **Exhaust** | ● medium | ● medium | ●● high | ●● high |
| **Intercept** | ○ | ○ | ●● high | ●● high |

*●● = primary attack surface · ● = secondary · ○ = not applicable*

## Key Finding

The highest-risk attack surfaces are at L1 (Sensing) for suppression/corruption and L3 (Communication) for interception/exhaustion. L2 (Processing) is the hardest to attack without system knowledge (L4 access). No governance framework reviewed addresses L0-level suppression or L3 network dead-zone failures.

*(Governance gap detail in governance_gap_analysis/ — Phase 4)*
