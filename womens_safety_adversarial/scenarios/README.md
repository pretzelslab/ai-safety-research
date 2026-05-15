# Scenario Library

14 adversarial scenarios for the ZIDR benchmark — 9 urban, 5 rural.

All scenarios are grounded in Indian deployment context using NCRB Annual Reports and
Safetipin urban safety audit data. Each scenario models a realistic threat situation
where an adversary is physically proximate and the victim has lost or is losing agency.

---

## Files

| File | Purpose |
|------|---------|
| `scenarios.yaml` | All 14 scenarios, full 12-field YAML schema |
| `scenario_loader.py` | Python loader — `load_scenario(id)` and `list_scenarios()` |
| `SCHEMA.md` | Every YAML field documented |

---

## Scenario Index

### Urban (U-01 to U-09)

| ID | Name | Criticality | Min. Access | Key Failure |
|----|------|-------------|-------------|-------------|
| U-01 | Mumbai Local Train, Peak Hours | 5 | L0 | Vision + Audio + IMU defeated simultaneously |
| U-02 | App-Based Cab, Night Route | 5 | L1 | GPS spoofing + sensor fusion collapse |
| U-03 | Workplace, Authority Figure | 4 | L5 | Social suppression — alert never initiated |
| U-04 | Street Market, Bag Obstruction | 3 | L0 | Camera occlusion |
| U-05 | Bus Stop, Exhaustion Attack | 4 | L0 | Repeated false alerts condition contacts to ignore |
| U-06 | Campus, Known Acquaintance | 3 | L1 | NLP coercion bypass |
| U-07 | Social Venue, Noise + Alcohol | 4 | L0 | Audio + vision defeated in high-noise environment |
| U-08 | Public Toilet, Device Grab | 5 | L2 | Communication + response layer intercepted |
| U-09 | Transit Confinement, Moving Vehicle | 5 | L1 | All 4 passive layers fail simultaneously |

### Rural (R-01 to R-05)

| ID | Name | Criticality | Min. Access | Key Failure |
|----|------|-------------|-------------|-------------|
| R-01 | Agricultural Field, Isolated Worker | 5 | L0 | No cellular — alert cannot transmit |
| R-02 | Village Pathway, Dusk | 4 | L0 | Low-light CV failure + response suppression |
| R-03 | Isolated Road, Moving Vehicle | 5 | L0 | GPS dead zone + coordinated timing |
| R-04 | Village Common, Community Authority | 4 | L5 | Community authority suppresses alert initiation |
| R-05 | Agricultural Employer, Seasonal Labour | 4 | L5 | Economic coercion as attack vector |

**Criticality 5** = complete alert failure, no fallback path.

---

## Adversary Access Levels

| Level | Label | What it means |
|-------|-------|---------------|
| L0 | Proximity only | No device contact; physical presence alone is sufficient |
| L1 | Incidental contact | Brief, deniable contact (bump, brush) |
| L2 | Full device access | Has the victim's phone in hand |
| L3 | Environmental control | Controls the physical environment (venue, transport) |
| L4 | System knowledge | Knows the app or its detection thresholds |
| L5 | Social leverage | Authority, economic dependency, or community power |

---

## Python API

```python
from scenarios import load_scenario, list_scenarios

# List all IDs
for sid, name in list_scenarios():
    print(sid, name)

# Load a single scenario
s = load_scenario("U-01")
print(s.criticality_score)      # 5
print(s.adversary_access_level) # "L0"
print(s.failure_mode_type)      # ["sensing_failure"]
print(s.passive_layers)         # ["vision", "audio", "sensor_fusion"]
```

The `Scenario` dataclass exposes all 12 YAML fields plus backward-compatible
properties used by the probe tool and ZIDR scorer. See `SCHEMA.md` for the
complete field reference.

---

## ZIDR Convention for Sociotechnical Scenarios

U-03, R-04, and R-05 involve L5 adversaries who suppress alerts through
social or institutional mechanisms — authority, community power, economic
coercion. The AI system functions correctly in these scenarios; the alert
is simply never initiated.

ZIDR = 0.0 by convention for these scenarios. This is not a system failure
in the technical sense — it is a governance failure. The benchmark surfaces
this as a separate failure mode (`sociotechnical_suppression`).
