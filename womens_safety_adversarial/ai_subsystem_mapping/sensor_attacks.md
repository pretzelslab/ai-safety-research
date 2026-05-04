# AI Subsystem Mapping — Sensor Fusion

## What This Subsystem Does

**Plain language:** Modern safety apps don't rely on just one sensor — they combine signals from multiple sensors to make a confident decision. GPS tells the app where you are and whether the route looks wrong. The accelerometer detects unusual movement (a fall, a struggle, sudden deceleration). Network state tells the app whether an alert can actually be sent. Sensor fusion is the logic that weighs all these signals together and decides when to trigger. No single sensor fires the alert alone — the system is looking for multiple signals to agree before acting.

**Technical components:**
- GPS location tracking (route deviation detection, geofence crossing)
- Accelerometer / IMU (fall detection, struggle detection, unusual movement patterns)
- Network state monitoring (signal strength, data availability)
- Sensor fusion engine (rule-based threshold logic or ML-based classifier combining sensor inputs)
- Automated alert logic (trigger when N sensors cross threshold simultaneously)

---

## Attack Surface Map

| Attack Method | How It Works Against Sensor Fusion | Min Access | Deployment Contexts |
|---|---|---|---|
| **Suppress** | Move victim to GPS dead zone (tunnel, basement, rural valley); disable data connection if device accessible | L0–L1 | R2, T1, U2 |
| **Corrupt** | Generate accelerometer ambiguity — in crowded transit, groping produces the same micro-motion signal as incidental contact; in moving vehicles, vibration masks struggle signatures | L0 | U1, T1 |
| **Spoof** | GPS signal injection (fake location); fake accelerometer events via device manipulation | L2–L3 | T1, R2 |
| **Exhaust** | Trigger motion events repeatedly in safe contexts until sensor-fusion confidence score is reduced or alert is disabled | L0 | U1, U2 |
| **Intercept** | Block network at the moment of alert transmission — Faraday environment, active jamming, or known rural dead zone | L2–L3 | R2, T1 |

---

## Evasion Mechanisms — Detail

### 1. GPS Dead Zone — The Rural R2 Problem (Highest Risk)

In rural isolated contexts (R2), GPS signal may be absent (valley, dense forest, building shadow, absent base station coverage) or heavily attenuated. Without GPS fix, route deviation detection fails entirely. Worse: alert transmission via SMS or data network may also fail in the same conditions.

**This is the worst compound failure mode:** in exactly the contexts where institutional response is weakest — rural, isolated, no bystanders — both sensing and communication collapse simultaneously. The safety app fails at the moment it is most needed.

**Novel finding:** No governance framework reviewed addresses the compounding failure of sensing and communication in rural dead zones. EU AI Act, NIST AI RMF, DPDP Act — none require safety apps to specify minimum operational network conditions or mandate offline-capable alert modes (Bluetooth mesh, stored-and-forward SMS). **[CITATION NEEDED: India mobile coverage gap statistics — TRAI 2023 or equivalent]**

### 2. Accelerometer Ambiguity — Two Distinct Failure Modes

The IMU failure in women's safety contexts is not uniform. The threat type and context determine which failure mode applies:

**In crowded transit (U1, T1 — local train, bus):**
Threat is typically groping or contact-based harassment — not full physical struggle. Groping produces micro-motion signals (subtle, localised, low-amplitude) that are indistinguishable from incidental contact in a crowded moving vehicle. Transit vibration, passenger jostling, and normal boarding/alighting movement form a continuous noise baseline that completely masks these signals. **No adversary action required — the environment provides full IMU camouflage at L0.**

**In isolated moving vehicles (T1 — cab, auto-rickshaw, private car):**
Threat escalates to physical assault or abduction — which does produce detectable struggle signatures (rapid, high-amplitude, multi-axis). However, vehicle motion (bumpy roads, speed changes, lane changes) corrupts the IMU baseline. An adversary can time contact to coincide with a speed bump or road irregularity, further degrading the signal-to-noise ratio. **[CITATION NEEDED: accelerometer signal characteristics under transit conditions — see fall-detection literature, e.g. Abbate et al. or equivalent]**

**Design implication:** A sensor fusion system calibrated for struggle detection in isolated settings will generate high false-positive rates in crowded transit. A system calibrated to reduce false positives in transit will miss groping entirely. This is a fundamental accuracy tradeoff with no current governance requirement to address it.

### 3. Route Deviation Defeat (L0 social / L4 technical)

Route deviation detection flags when the GPS track diverges from the expected path. Defeatable by:
- Knowing the victim's regular route and staging deviation gradually — requires L4 (system knowledge)
- Convincing the victim to disable route tracking — requires L5 (social leverage)
- Routing through a network dead zone before deviation is registered — requires L3 (environmental control)

**Critical design weakness:** route deviation detection is retrospective — it fires after the deviation is established. A fast-moving adversary can create isolation before the alert fires.

### 4. Network Interception / Dead Zone Exploitation

Once a safety app triggers, alert transmission depends on data or SMS connectivity. A cab driver (L3: environmental control) can route through a known dead zone. In urban India, mobile black spots exist in building basements, metro tunnel sections, and industrial zones.

Without offline-capable fallback, loss of network at the moment of alert = complete failure of the response chain. The alert was triggered, the sensor fusion worked, the model classified correctly — and no help arrives.

---

## Highest-Risk Scenarios (cross-reference: threat_taxonomy/scenario_library/)

| Scenario | Threat Type | Attack | Why Sensor Fusion Fails | Governance Flag |
|---|---|---|---|---|
| U-01 (Mumbai Local Train) | Groping / contact harassment | Corrupt Accelerometer | Groping micro-motion indistinguishable from crowd contact; transit vibration provides complete IMU camouflage | No standard distinguishes groping signature from incidental contact in crowded transit |
| U-02 (App Cab, Night Route) | Physical assault / abduction | Suppress GPS + Corrupt route | Route deviates through low-signal area; GPS drops before alert fires | No location-spoof resistance requirement |
| T-01 (Isolated Moving Vehicle) | Physical assault / struggle | Corrupt Accelerometer | Vehicle vibration corrupts struggle baseline; adversary times contact to road irregularity | No vibration-context IMU certification for isolated vehicle threat scenario |
| R-02 (Rural Isolated) | Physical assault | Suppress + Intercept | GPS and data both fail simultaneously; no fallback mode | No offline-mode requirement; no minimum coverage standard |

---

## Robustness Test Design

**Goal:** Quantify the sensor fusion failure rate under adversary-induced conditions, with specific attention to the groping/struggle distinction in crowded vs. isolated contexts.

**Test protocol:**
1. GPS dead zone: simulate signal drop mid-route — measure time-to-alert vs. time-to-route-deviation-flag; measure proportion of alerts lost without offline fallback
2. Accelerometer crowded transit: inject crowd-jostling + transit-vibration noise profile — measure false-negative rate for groping-level micro-motion against baseline
3. Accelerometer isolated vehicle: inject vehicle vibration (auto-rickshaw, car) — measure false-negative rate for struggle detection under vehicle motion
4. Network loss at trigger: cut data and SMS at the moment alert fires — measure proportion of undelivered alerts
5. Compound failure (R2): degrade GPS + data simultaneously — measure complete sensor fusion failure rate

**Output metric:** Sensor Fusion Evasion Score (SFES) — composite 0–1 score across GPS failure rate, accelerometer false-negative rate (groping and struggle contexts separately), and alert delivery rate under network disruption. Computed separately for urban crowded (U1), urban isolated (U2), transit (T1), and rural isolated (R2) deployment contexts.

---

## Governance Coverage

| Framework | Relevant Clause | What It Covers | What It Misses |
|---|---|---|---|
| EU AI Act | Art. 9 (risk management), Art. 15 (accuracy, robustness) | Robustness requirements in high-risk AI | No sensor fusion dead-zone, vibration, or context-specific threat-type test condition |
| NIST AI RMF | GOVERN 1.7, MEASURE 2.5 | Context-aware risk assessment | No rural dead-zone or groping vs. struggle IMU calibration requirement |
| India DPDP Act | Location data provisions | GPS data retention limits | No attack-surface or coverage gap requirement |
| ISO 42001 | Clause 8.4 | Operational planning | No sensor-specific adversarial conditions defined |

**Core gap:** No framework requires safety apps to specify minimum operational conditions (network coverage, GPS fix quality) or mandate fallback modes for coverage-absent deployment contexts. No framework distinguishes between crowded-transit (groping) and isolated-vehicle (assault) IMU calibration requirements. **Novel finding — no existing standard addresses the compound GPS + network failure mode in rural contexts, or the groping/struggle IMU calibration tradeoff in Indian transit scenarios.**
