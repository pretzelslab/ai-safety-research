# Probe Robustness Tool — Technical Specification

## Overview

The probe robustness tool is a Python CLI script that takes a safety system profile (YAML) and an attack scenario ID, runs the evaluation criteria from `evaluation_criteria.md`, and produces a robustness report: per-dimension scores, overall score, ZIDR, and governance gap flags.

**Version:** v1.0 specification (implementation out of scope for this research phase)  
**Language:** Python 3.11+  
**Output:** terminal report + optional JSON export  
**Model access required:** No — black-box, specification-based evaluation  

---

## CLI Design

```
python probe.py --profile <system_profile.yaml> --scenario <scenario_id> [--output json]
```

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `--profile` | Yes | Path to YAML file describing the safety AI system |
| `--scenario` | Yes | Scenario ID from scenario library (e.g., U-01, R-02) |
| `--output` | No | Output format: `terminal` (default) or `json` |
| `--weights` | No | Path to custom weight YAML file (overrides defaults) |

**Example:**
```
python probe.py --profile profiles/shakealert_v2.yaml --scenario U-01
python probe.py --profile profiles/himmat_plus.yaml --scenario R-02 --output json
```

---

## Input: System Profile YAML Schema

```yaml
# system_profile.yaml
system:
  name: "Example Safety App"
  version: "2.1"
  developer: "Example Corp"
  markets: ["IN", "EU"]           # ISO 3166-1 alpha-2 country codes

# Active sensing modalities
modalities:
  camera:
    active: true
    mode: passive                  # passive | active (user-triggered)
    claimed_occlusion_tolerance: null   # percentage, or null if not documented
    low_light_processing: false    # adaptive brightness correction pre-inference
    published_accuracy: null       # F1 or precision/recall, or null
  audio:
    active: true
    mode: passive
    claimed_anef_db: null          # ambient noise floor (dB) at detection rate 0.5, or null
    keyword_required: true         # true = requires user vocalisation
    published_accuracy: null
  imu:
    active: true
    calibration_profiles:
      - crowded_transit            # "crowded_transit" | "isolated" | "general"
    published_accuracy: null
  gps:
    active: true
    offline_fallback: false        # true = stored-and-forward or Bluetooth mesh fallback
    minimum_signal_required: null  # or "any" | "strong"
  nlp:
    active: true
    mode: active                   # active = requires user input (check-in)
    cbr_tested: false              # coercion bypass rate tested and published
    cbr_value: null                # 0.0–1.0, or null

# Alert transmission
alert:
  methods: ["data", "sms"]         # "data" | "sms" | "bluetooth" | "offline"
  delivery_verified: false         # end-to-end delivery confirmation tested

# Deployment contexts marketed
deployment_contexts: ["U1", "U2"]  # U1 | U2 | R1 | R2 | T1

# Governance documentation
governance:
  eu_ai_act_classification: null   # "high_risk" | "limited_risk" | "minimal_risk" | null
  iso_42001_certified: false
  nist_ai_rmf_aligned: false
  india_regulatory_compliant: null # "dpdp" | "it_act" | null
  robustness_testing_published: false
```

---

## Processing Logic (Pseudocode)

```python
def evaluate(profile, scenario_id):
    scenario = load_scenario(scenario_id)         # loads context, threat_type, access_level
    
    scores = {}
    
    # Dimension 1: Vision
    if profile.modalities.camera.active:
        scores['vision'] = score_vision(
            occlusion_tolerance = profile.modalities.camera.claimed_occlusion_tolerance,
            low_light = profile.modalities.camera.low_light_processing,
            deployment_context = scenario.context,
            published_accuracy = profile.modalities.camera.published_accuracy
        )
    
    # Dimension 2: Audio
    if profile.modalities.audio.active:
        scores['audio'] = score_audio(
            anef_db = profile.modalities.audio.claimed_anef_db,
            keyword_required = profile.modalities.audio.keyword_required,
            deployment_context = scenario.context,
            threat_type = scenario.threat_type
        )
    
    # Dimension 3: Sensor Fusion
    scores['sensor_fusion'] = score_sensor_fusion(
        gps_offline_fallback = profile.modalities.gps.offline_fallback,
        imu_calibration = profile.modalities.imu.calibration_profiles,
        alert_methods = profile.alert.methods,
        deployment_context = scenario.context,
        threat_type = scenario.threat_type
    )
    
    # Dimension 4: NLP
    if profile.modalities.nlp.active:
        scores['nlp'] = score_nlp(
            mode = profile.modalities.nlp.mode,
            cbr_tested = profile.modalities.nlp.cbr_tested,
            cbr_value = profile.modalities.nlp.cbr_value,
            deployment_context = scenario.context
        )
    
    # Dimension 5: ZIDR (adversary-induced)
    scores['zidr'] = compute_zidr(
        profile = profile,
        scenario = scenario
    )
    
    # Overall score with scenario-appropriate weights
    weights = load_weights(scenario.threat_type)
    overall = weighted_average(scores, weights)
    
    # Governance gap flags
    flags = check_governance_gaps(profile, scenario, scores)
    
    return RobustnessReport(scores, overall, flags, scenario)
```

---

## Output: Terminal Report Format

```
══════════════════════════════════════════════════════════════
PROBE ROBUSTNESS REPORT
System:   Example Safety App v2.1
Scenario: U-01 — Mumbai Local Train, Peak Hours
Context:  U1 (urban public), T1 (transit) | Threat: Groping
══════════════════════════════════════════════════════════════

DIMENSION SCORES
─────────────────────────────────────────────
Vision          ████░░░░░░  0.40   [ MODERATE ]
Audio           ██░░░░░░░░  0.20   [ HIGH RISK ]
Sensor Fusion   ███░░░░░░░  0.30   [ HIGH RISK ]
NLP / Language  ██░░░░░░░░  0.20   [ HIGH RISK ]
ZIDR (adv.)     █░░░░░░░░░  0.10   [ CRITICAL  ]

─────────────────────────────────────────────
OVERALL SCORE   ██░░░░░░░░  0.24   ⚠ CRITICAL
─────────────────────────────────────────────

ZIDR NOTE: At L0 adversary access in U1/T1 context, 1 of 4
passive modalities (GPS) remains functional. Camera, audio,
and IMU defeated by crowd occlusion, 85 dB ambient, and
transit vibration respectively. Victim agency suppressed;
passive detection effectively unavailable.

GOVERNANCE GAP FLAGS
─────────────────────────────────────────────
[GOV-EU-CLASSIFICATION]  System not classified high-risk
                         under EU AI Act Annex III —
                         Art. 15 robustness requirements
                         do not apply.
[GOV-NIST-ZIDR]          No ZIDR measurement documented.
[GOV-INDIA-NONE]         No India robustness requirement
                         applicable to this system.
[GOV-CROSS-ARBITRAGE]    No jurisdiction requires minimum
                         robustness for this deployment.

RECOMMENDATIONS
─────────────────────────────────────────────
1. Audio: Publish ANEF data. Calibrate to Indian urban
   noise levels (target ANEF ≥ 85 dB for U1/T1).
2. IMU: Add crowded-transit calibration profile to
   distinguish groping from crowd contact.
3. Offline fallback: Implement stored-and-forward SMS
   alert for network-degraded contexts.
4. Passive detection: Reduce reliance on keyword
   activation in high-noise deployment contexts.
══════════════════════════════════════════════════════════════
```

---

## Output: JSON Format

```json
{
  "system": "Example Safety App v2.1",
  "scenario": "U-01",
  "scenario_context": "U1/T1",
  "threat_type": "groping",
  "scores": {
    "vision": 0.40,
    "audio": 0.20,
    "sensor_fusion": 0.30,
    "nlp": 0.20,
    "zidr_adversary_induced": 0.10
  },
  "overall": 0.24,
  "risk_level": "CRITICAL",
  "governance_flags": [
    "GOV-EU-CLASSIFICATION",
    "GOV-NIST-ZIDR",
    "GOV-INDIA-NONE",
    "GOV-CROSS-ARBITRAGE"
  ],
  "zidr_detail": {
    "passive_modalities_total": 4,
    "functional_at_l0": 1,
    "functional_modalities": ["gps"],
    "defeated_modalities": ["camera", "audio", "imu"]
  }
}
```

---

## File Structure

```
probe_robustness/
├── probe.py                   # main CLI entry point
├── methodology.md             # evaluation philosophy (this phase)
├── evaluation_criteria.md     # scoring decision trees (this phase)
├── tool_specification.md      # this file
├── scorer/
│   ├── vision.py              # score_vision()
│   ├── audio.py               # score_audio()
│   ├── sensor_fusion.py       # score_sensor_fusion()
│   ├── nlp.py                 # score_nlp()
│   └── zidr.py                # compute_zidr()
├── governance/
│   └── gap_checker.py         # check_governance_gaps()
├── scenarios/
│   └── scenario_loader.py     # loads scenario context from scenario_library/
├── profiles/
│   └── example_profile.yaml   # template system profile
└── weights/
    └── default_weights.yaml   # scenario-type weight tables
```

---

## Dependencies

```
python >= 3.11
pyyaml >= 6.0      # YAML profile loading
tabulate >= 0.9    # terminal table formatting
rich >= 13.0       # terminal colour output (progress bars, score bands)
```

No ML framework required. No API calls. Fully offline.

---

## Implementation Notes (for Phase 5 build)

1. **Start with `probe.py` + `scorer/sensor_fusion.py`** — the sensor fusion scorer handles the most complex logic (compound GPS + network failure, IMU calibration profile check) and is the most differentiating output.

2. **Scenario loader links to existing scenario library YAML** — scenarios should be exported from `threat_taxonomy/scenario_library/` as structured YAML (not just markdown) to enable programmatic loading. This is a Phase 5 data task.

3. **Governance gap checker is a lookup table** — `check_governance_gaps()` is not complex logic; it maps (deployment_context, score_bands, governance fields) to a list of flags. Implement as a simple rules dictionary.

4. **Calibration is the hard part** — the scoring thresholds in `evaluation_criteria.md` marked `[CALIBRATE]` require live system testing against real safety apps to establish. Version the thresholds so they can be updated as empirical data is collected.

5. **The tool is a research artifact first** — output is designed to be citation-ready (JSON for reproducibility, terminal for presentation). Prioritise interpretability of output over computational efficiency.
