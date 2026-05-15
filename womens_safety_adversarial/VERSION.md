# Version History

## v2.0.0 — 2026-05-14

**Benchmark artifact release.** Complete restructure from research narrative to runnable benchmark.

Changes:
- Added U-09 (Urban Transit Confinement, Moving Vehicle) — 9 urban scenarios, 14 total
- Introduced `scenarios/` — structured YAML library with 12-field schema, Python loader
- Introduced `benchmark/` — runner, 4 reference profiles, calibration script, charts, CSV outputs
- Introduced `probe_tool/` — CLI (`probe.py`), Streamlit viewer, ZIDR scorer, governance checker
- All benchmark results regenerated: 56-cell ZIDR matrix (4 systems x 14 scenarios)
- Three publication figures: ZIDR heatmap, score comparison with error bars, threat model
- Paper updated: title corrected to "...Governance Gap Analysis", pure-ASCII LaTeX source

Prior layout (`probe_robustness/`) is no longer in use. See `probe_robustness/README.md`.

---

## v1.0.0 — 2026-05-08

**Initial research artifact release.**

- 13 adversarial scenarios (8 urban, 5 rural)
- Threat taxonomy, governance gap analysis across 5 frameworks
- Probe tool specification and methodology
- ZIDR concept paper (preprint)
- Zenodo DOI: 10.5281/zenodo.20028247
