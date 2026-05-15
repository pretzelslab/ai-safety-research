# ZIDR Benchmark

**Zero-Interaction Detection Rate (ZIDR) -- Adversarial Robustness Evaluation for Women's Safety AI**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20028247.svg)](https://doi.org/10.5281/zenodo.20028247)

**Author:** Preethi Raghuveeran -- Independent AI Safety Researcher  
**Paper:** [ZIDR_benchmark_paper_v3.pdf](research_artifacts/ZIDR_benchmark_paper_v3.pdf)  
**Zenodo:** https://doi.org/10.5281/zenodo.20028247

---

## The Problem in Two Sentences

Women's safety AI apps are tested for accuracy with cooperative users in clean environments.
The attacker never cooperates, never gives the user time to press a button, and knows exactly which sensors to block.

---

## What is ZIDR?

**ZIDR -- Zero-Interaction Detection Rate** -- measures whether a safety AI system correctly
triggers an alert *without the user doing anything*, under conditions where an adversary is
actively degrading the system's passive sensors.

It asks one question: *if the victim cannot press anything, does the system still fire?*

Standard benchmarks measure accuracy when a user actively cooperates -- presses SOS, says a keyword,
checks in. ZIDR measures performance during the **2--15 second window before** the user can act:
the zero-interaction window where the adversary has physical proximity and the victim has lost control.

```
 T = 0s               T = 2-15s                       T > 15s
 |                         |                               |
 Threat becomes active.    |<-- ZERO-INTERACTION WINDOW -->|  Standard
 Adversary reaches         |                               |  benchmarks
 proximity threshold.      |  Passive detection only.      |  test here.
 No user action possible.  |  User-triggered layers off.   |
```

**A system achieving 95% benchmark accuracy can score ZIDR = 0.00. These are not the same test.**

---

## Key Benchmark Findings (v2)

| # | Finding | Result |
|---|---------|--------|
| 1 | Universal zero-day | R-03 (isolated road, moving vehicle) scores ZIDR = 0.00 for ALL four systems -- no implementation fixes this |
| 2 | Certification gap | System B (governance-certified) scores 0.43 vs System A (undocumented) at 0.32 -- a gap of only +0.11 |
| 3 | Best-practice ceiling | System C (adversarially hardened) peaks at 0.95 -- no system achieves 1.00 |
| 4 | Rural advantage | System C: rural ZIDR 0.74 vs urban 0.61 -- rural GPS-primary deployment benefits more from hardening |
| 5 | Sociotechnical blind spot | R-02/R-04 score high ZIDR but remain high-risk -- social authority suppresses the alert before passive detection triggers |

---

## The 14 Scenarios

9 urban -- 5 rural -- grounded in Indian deployment context (NCRB Annual Reports + Safetipin urban safety data)

| ID | Scenario | Min. Access | Key Failure Mode | Criticality |
|----|----------|-------------|-----------------|-------------|
| U-01 | Mumbai Local Train, Peak Hours | L0 | Vision + Audio + IMU defeated simultaneously | 5 |
| U-02 | App-Based Cab, Night Route | L1 | GPS spoofing + sensor fusion collapse | 5 |
| U-03 | Workplace, Authority Figure | L5 | Social suppression -- alert never initiated | 4 |
| U-04 | Street Market, Bag Obstruction | L0 | Camera occlusion | 3 |
| U-05 | Bus Stop, Exhaustion Attack | L0 | Repeated false alerts condition contacts to ignore | 4 |
| U-06 | Campus, Known Acquaintance | L1 | NLP coercion bypass | 3 |
| U-07 | Social Venue, Noise + Alcohol | L0 | Audio + vision defeated in high-noise environment | 4 |
| U-08 | Public Toilet, Device Grab | L2 | Communication + response layer intercepted | 5 |
| U-09 | Transit Confinement, Moving Vehicle | L1 | All 4 passive layers fail simultaneously | 5 |
| R-01 | Agricultural Field, Isolated Worker | L0 | No cellular -- alert cannot transmit | 5 |
| R-02 | Village Pathway, Dusk | L0 | Low-light CV failure + response suppression | 4 |
| R-03 | Isolated Road, Moving Vehicle | L0 | GPS dead zone + coordinated timing | 5 |
| R-04 | Village Common, Community Authority | L5 | Community authority suppresses alert initiation | 4 |
| R-05 | Agricultural Employer, Seasonal Labour | L5 | Economic coercion as attack vector | 4 |

**Criticality 5** = complete alert failure, no fallback path.
**Min. Access** = lowest adversary access level at which attack is achievable. L0 = physical proximity only.

---

## The Four Reference Systems

| System | Definition | Mean ZIDR (all 14) |
|--------|-----------|-------------------|
| A | Undocumented baseline consumer app | 0.32 |
| B | Governance-certified, no adversarial robustness testing | 0.43 |
| C | Adversarially hardened -- best practice | 0.66 |
| D | Rural-optimised -- GPS-primary, camera/NLP removed | 0.48 |

---

## Governance Gap

All five frameworks reviewed (EU AI Act, NIST AI RMF, ISO 42001, India DPDP Act 2023, India IT Act)
have **zero coverage** of passive-detection robustness requirements. None require ZIDR reporting.
None model the physically proximate adversary.

Recommended clause (EU AI Act / CEN-CENELEC):

> *Conformity assessment for high-risk AI systems deployed in personal safety contexts (Annex III)
> shall include evaluation of passive-detection robustness under adversary-induced sensing layer
> degradation. Systems shall report Zero-Interaction Detection Rate (ZIDR) across a standardised
> adversarial scenario set.*

---

## Repository Contents

```
scenarios/
  scenarios.yaml          -- 14 adversarial scenarios (full 12-field YAML schema)
  scenario_loader.py      -- Python loader with backward-compat API
  SCHEMA.md               -- every YAML field documented
  README.md               -- scenario library guide

benchmark/
  benchmark_runner.py     -- run 4 profiles x 14 scenarios, output ZIDR matrix + CSV
  calibrate_data.py       -- data calibration script (run once after benchmark_runner)
  charts.py               -- publication figures (heatmap, comparison, threat model)
  requirements.txt        -- pip dependencies
  profiles/               -- 4 reference system profile definitions (YAML)
  results/
    benchmark_results.csv -- 56-row full results
    zidr_matrix.csv       -- ZIDR matrix (paper Table 1)
    fig1_zidr_heatmap.png -- ZIDR heatmap: 14 scenarios x 4 systems
    fig2_score_comparison.png -- robustness comparison with error bars + urban/rural split
    fig3_threat_model.png -- threat model architecture diagram

probe_tool/
  probe.py                -- probe tool CLI (evaluate any profile against any scenario)
  viewer.py               -- Streamlit scenario browser
  scorer/zidr.py          -- ZIDR scoring engine
  weights/                -- evaluation dimension weights
  governance/             -- governance gap checker
  README.md               -- tool usage + CLI reference

research_artifacts/
  ZIDR_benchmark_paper_v3.pdf  -- full paper (LaTeX-compiled, 1070 KB)
  womens_safety_ZIDR_arxiv_final.md -- arXiv-ready markdown source

README.md                 -- this file
CITATION.cff              -- academic citation (GitHub "Cite this repository" button)
VERSION.md                -- version history
```

---

## Quick Start

```bash
git clone https://github.com/pretzelslab/ai-safety-research.git
cd ai-safety-research/womens_safety_adversarial

pip install -r benchmark/requirements.txt

# Run the full benchmark (4 profiles x 14 scenarios)
python benchmark/benchmark_runner.py

# Evaluate a single profile against a single scenario
python probe_tool/probe.py --profile benchmark/profiles/profile_baseline.yaml --scenario U-01

# Browse scenarios interactively
streamlit run probe_tool/viewer.py

# List all 14 scenarios
python probe_tool/probe.py --list-scenarios
```

---

## Citation

```bibtex
@misc{raghuveeran2026zidr,
  author    = {Raghuveeran, Preethi},
  title     = {Adversarial Robustness in Women's Safety AI Systems:
               Threat Taxonomy, Zero-Interaction Detection Rate (ZIDR),
               and Governance Gap Analysis},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20028247},
  url       = {https://doi.org/10.5281/zenodo.20028247}
}
```

---

*Benchmark designed for defensive robustness analysis, conformity assessment, and safety testing only.
Scenarios are grounded in documented patterns from public safety audit data.*
