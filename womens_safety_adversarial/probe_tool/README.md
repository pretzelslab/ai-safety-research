# Probe Tool

Evaluate any system profile against any scenario. Three entry points:
CLI (`probe.py`), Streamlit browser (`viewer.py`), and a Python API.

---

## Quick Start

```bash
cd womens_safety_adversarial

pip install pyyaml rich streamlit pandas

# Evaluate a profile against a single scenario
python probe_tool/probe.py --profile benchmark/profiles/profile_baseline.yaml --scenario U-01

# Output as JSON
python probe_tool/probe.py --profile benchmark/profiles/profile_best_practice.yaml --scenario R-03 --output json

# List all 14 scenarios
python probe_tool/probe.py --list-scenarios

# Browse scenarios interactively
streamlit run probe_tool/viewer.py
```

---

## CLI Reference — probe.py

```
python probe_tool/probe.py [OPTIONS]

Options:
  --profile PATH       Path to system profile YAML (required unless --list-scenarios)
  --scenario ID        Scenario ID to evaluate against, e.g. U-01, R-03
  --weights PATH       Custom weights YAML (default: probe_tool/weights/default_weights.yaml)
  --output FORMAT      Output format: table (default) | json
  --list-scenarios     Print all available scenario IDs and names, then exit
```

**Example output (table mode):**
```
U-01: Mumbai Local Train, Peak Hours
Adversary: L0 (proximity only) | Window: 5s

Dimension         Score    Risk
ZIDR              0.08     CRITICAL
Vision            0.12     CRITICAL
Audio             0.10     CRITICAL
Sensor Fusion     0.20     HIGH RISK
Governance        0.45     HIGH RISK
Overall           0.19     CRITICAL

Governance flags: 3
  - No passive-detection robustness requirement
  - No adversary proximity model in certification
  - No ZIDR reporting requirement
```

---

## Streamlit Viewer — viewer.py

Interactive scenario library browser with sidebar filters.

```bash
streamlit run probe_tool/viewer.py
```

**Filters available:**
- Geography: All / Urban / Rural
- Criticality: checkboxes per level (3/4/5)
- Failure mode: Sensing / Communication / Response / Sociotechnical
- Novel attack vectors only (toggle)
- Sociotechnical attacks only (toggle)

Click any row in the summary table to expand the full scenario detail panel:
narrative, attack profile, passive layers, benchmark parameters, degradation
priors, evidence basis, governance gaps, regulatory mapping, and calibration note.

---

## Directory Structure

```
probe_tool/
  probe.py                -- CLI entry point
  viewer.py               -- Streamlit scenario browser
  scorer/
    zidr.py               -- ZIDR scoring engine
    vision.py             -- Vision dimension scorer
    audio.py              -- Audio dimension scorer
    sensor_fusion.py      -- IMU + GPS dimension scorer
    nlp.py                -- NLP dimension scorer (active check-in)
  weights/
    default_weights.yaml  -- Per-scenario-category dimension weights
  governance/
    gap_checker.py        -- Governance gap flag checker
```

---

## ZIDR Scoring

ZIDR is computed by `scorer/zidr.py`:

```
ZIDR = (functional passive modalities) / (total passive modalities)
```

For each passive modality (camera, audio, IMU, GPS), the scorer checks whether
an L0 adversary (proximity only) can defeat it in the scenario's context:

- `functional` (1.0) — adversary at L0 cannot suppress this modality here
- `marginal` (0.5) — partial — depends on specific conditions within the context
- `defeated` (0.0) — adversary at L0 trivially suppresses this modality

When a scenario spans multiple context codes (e.g. U-01 spans U1 and T1),
**worst-case context is used** for each modality.

NLP in active (check-in) mode is excluded from ZIDR: it requires the victim
to initiate, so it cannot contribute to zero-interaction detection.

**Sociotechnical scenarios** (U-03, R-04, R-05): ZIDR = 0.0 by convention.
The detection system never activates because the alert is suppressed before
any passive layer is engaged.

---

## Writing a Custom Profile

Copy `benchmark/profiles/example_profile.yaml` and fill in:

```yaml
name: My System
version: "1.0"
modalities:
  camera:
    active: true
    mode: passive
    low_light_processing: true
    published_accuracy: 0.82
  audio:
    active: true
    mode: passive
    published_accuracy: 0.76
  imu:
    active: true
  gps:
    active: true
  nlp:
    active: false          # set true if system has active NLP check-in
certifications: []         # list any governance certifications
adversarial_testing: false # true if system has been adversarially tested
```

Then run:
```bash
python probe_tool/probe.py --profile path/to/my_profile.yaml --scenario U-01
```

---

## Python API

```python
from pathlib import Path
from probe_tool.probe import load_profile, run_evaluation

profile = load_profile(Path("benchmark/profiles/profile_best_practice.yaml"))
weights = Path("probe_tool/weights/default_weights.yaml")

from scenarios import load_scenario
scenario = load_scenario("R-03")

result = run_evaluation(profile, scenario, weights)
print(result["results"]["zidr"]["score"])   # e.g. 0.00
print(result["risk_level"])                  # CRITICAL / HIGH RISK / MODERATE / LOW RISK
print(result["governance_flags"])            # list of missing requirements
```
