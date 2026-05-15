# Scenario YAML Schema

Each scenario in `scenarios.yaml` has 12 top-level fields. This document
defines every field, its type, and its allowed values.

---

## Top-Level Structure

```yaml
- scenario_id:       string        # e.g. "U-01"
  scenario_name:     string        # Human-readable name
  context_class:     object        # Where the threat occurs
  scenario_narrative: string       # Plain-English description of the threat event
  attack_profile:    object        # Who the adversary is and what they do
  failure_mode_type: list[string]  # Which system layers fail
  passive_layers:    list[string]  # Which passive modalities are engaged
  benchmark:         object        # Evaluation parameters
  metadata:          object        # Scoring metadata
  evidence_basis:    object        # Empirical grounding
  governance_gap:    object        # Missing regulatory requirements
  regulatory_mapping: object       # Which frameworks are implicated
```

---

## Field Reference

### 1. `scenario_id`
**Type:** string  
**Format:** `U-NN` (urban) or `R-NN` (rural), zero-padded two digits.  
**Examples:** `"U-01"`, `"R-03"`

Stable identifier used by the probe tool (`--scenario U-01`) and all benchmark outputs.

---

### 2. `scenario_name`
**Type:** string  
**Example:** `"Mumbai Local Train, Peak Hours"`

Short descriptive name used in tables and the Streamlit viewer.

---

### 3. `context_class`
**Type:** object

```yaml
context_class:
  geography: urban | rural
  subtype: string          # internal routing key for threat-type mapping
  context_code: list[str]  # one or more context tags
```

**`context_code` values:**

| Code | Meaning |
|------|---------|
| U1 | Urban public space |
| U2 | Urban semi-private (workplace, campus, venue) |
| U3 | Urban isolated confinement (cab, toilet) |
| R1 | Rural public space |
| R2 | Rural isolated location |
| T1 | Transit (any moving vehicle) |

Scenarios can carry multiple codes (e.g. U-01 is both `U1` and `T1`). The ZIDR
scorer uses worst-case modality status across all codes.

---

### 4. `scenario_narrative`
**Type:** string (YAML block scalar `>`)

Plain-English description of the threat event: who is present, what happens,
and which sensing layers are degraded. Written to be readable without technical
context.

---

### 5. `attack_profile`
**Type:** object

```yaml
attack_profile:
  adversary_type: opportunistic | adaptive | informed
  adversary_access_level: L0 | L1 | L2 | L3 | L4 | L5
  attack_methods: list[string]
```

**`adversary_type`:**
- `opportunistic` — no pre-planning; exploits ambient environment
- `adaptive` — adjusts to victim's behaviour in real time
- `informed` — knows the system's detection thresholds or architecture

**`adversary_access_level`:** See access level table in `README.md`.

**`attack_methods`:**
- `suppress` — reduce signal quality (crowd, noise, obstruction)
- `corrupt` — inject false signal (vibration, spoofed GPS)
- `spoof` — impersonate a legitimate signal source
- `exhaust` — trigger false positives to condition contacts or victim
- `intercept` — take over the communication or response layer

---

### 6. `failure_mode_type`
**Type:** list[string]  
**Allowed values:**
- `sensing_failure` — passive modalities (camera, audio, IMU, GPS) are degraded
- `communication_failure` — alert cannot be transmitted (no signal, intercepted)
- `response_failure` — alert is transmitted but the response layer is suppressed
- `sociotechnical_suppression` — alert is never initiated due to social/institutional pressure

A scenario can have multiple failure modes (e.g. both `sensing_failure` and
`communication_failure`). Sociotechnical suppression is always listed alone —
it precedes the technical layers.

---

### 7. `passive_layers`
**Type:** list[string]  
**Allowed values:** `vision`, `audio`, `sensor_fusion`, `gps`, `nlp`

The passive AI modalities that are engaged in this scenario. `nlp` in active
(check-in) mode requires user action and is therefore excluded from ZIDR scoring
even when listed here. For sociotechnical scenarios, this field is empty (the
system never reaches the passive detection stage).

---

### 8. `benchmark`
**Type:** object

```yaml
benchmark:
  window_seconds: int | null       # Zero-interaction detection window duration
  degradation_factors:             # Initial benchmark priors (see NOTICE below)
    {attack_method}:
      {modality}: float            # 0.0–1.0, higher = more degraded
  expected_zidr_range:
    min: float
    max: float
```

**`window_seconds`:** Duration of the zero-interaction window in seconds. `null`
for sociotechnical scenarios (no temporal window applies).

**`degradation_factors`:** Principled estimates for how much each attack method
degrades each modality in this context. Used by the benchmark runner to compute
weighted scores. **These are initial benchmark priors, not empirically measured
values.** They are intended to enable consistent, comparable evaluation runs
and are expected to be revised as empirical data becomes available.

**`expected_zidr_range`:** Expected ZIDR interval for an unspecified system
evaluated against this scenario. Used by the probe tool to flag anomalous scores.

---

### 9. `metadata`
**Type:** object

```yaml
metadata:
  criticality_score: 3 | 4 | 5
  criticality_definition: string
  confidence_level: high | medium | low
  calibration_note: string
  test_reproducibility: high | medium | low
  time_horizon: immediate | long-term
  novel_attack_vector: bool
  sociotechnical_attack: bool
```

**`criticality_score`:**
- `5` = Complete alert failure, no fallback path. Death or severe harm possible.
- `4` = Alert fails or is suppressed; partial fallback exists.
- `3` = Alert is degraded but not fully suppressed; some fallback exists.

**`confidence_level`:** How well-supported the scenario and priors are by
available evidence.

**`test_reproducibility`:** How reliably the scenario conditions can be
reproduced in a controlled test environment.

**`time_horizon`:**
- `immediate` — threat is active in the zero-interaction window
- `long-term` — attack unfolds over time (e.g. exhaustion/conditioning attacks)

**`novel_attack_vector`:** `true` if the primary attack method is not covered
by existing safety certification frameworks.

**`sociotechnical_attack`:** `true` if the primary failure mode is
`sociotechnical_suppression`.

---

### 10. `evidence_basis`
**Type:** object with three sub-lists

```yaml
evidence_basis:
  primary:   list[string]   # Direct empirical sources
  secondary: list[string]   # Corroborating data
  inferred:  list[string]   # Logical extrapolation with stated basis
```

Evidence is cited at the scenario level, not the field level. Primary sources are
preferred; inferred entries document the reasoning chain explicitly.

---

### 11. `governance_gap`
**Type:** object

```yaml
governance_gap:
  missing_requirements: list[string]
```

Specific regulatory or certification requirements that are absent from all five
frameworks reviewed (EU AI Act, NIST AI RMF, ISO 42001, India DPDP Act 2023,
India IT Act) and that would be needed to surface this failure mode under
conformity assessment.

---

### 12. `regulatory_mapping`
**Type:** object

```yaml
regulatory_mapping:
  affected_frameworks: list[string]
```

Which regulatory frameworks are implicated by this scenario's governance gap.
Standard codes used: `EU-AIA`, `NIST-RMF`, `ISO-42001`, `IN-DPDP`, `IN-ITA`.

---

## Adding a New Scenario

1. Copy an existing scenario block from `scenarios.yaml` as a template.
2. Assign the next sequential ID (`U-10` or `R-06`).
3. Fill all 12 fields. Required fields: `scenario_id`, `scenario_name`,
   `context_class`, `scenario_narrative`, `attack_profile`, `failure_mode_type`,
   `passive_layers`, `benchmark`, `metadata`.
4. Run the regression check:
   ```bash
   python scenarios/scenario_loader.py  # or: python probe_tool/probe.py --list-scenarios
   ```
5. Update scenario counts in `README.md` and `VERSION.md`.
