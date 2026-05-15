# probe_robustness/ — Deprecated

This directory is no longer in use.

All code was moved in v2.0.0 (2026-05-14) to maintain a clean repository
structure. The new locations are:

| Was in probe_robustness/ | Now in |
|--------------------------|--------|
| `probe.py` | `probe_tool/probe.py` |
| `viewer.py` | `probe_tool/viewer.py` |
| `scorer/` | `probe_tool/scorer/` |
| `weights/` | `probe_tool/weights/` |
| `governance/` | `probe_tool/governance/` |
| `scenarios/` | `scenarios/` (repo root) |
| `benchmark_runner.py` | `benchmark/benchmark_runner.py` |
| `calibrate_data.py` | `benchmark/calibrate_data.py` |
| `charts.py` | `benchmark/charts.py` |
| `profiles/` | `benchmark/profiles/` |

CLI usage is unchanged — paths are the only thing that moved:

```bash
# Before (v1):
python probe_robustness/probe.py --profile ... --scenario U-01

# After (v2):
python probe_tool/probe.py --profile ... --scenario U-01
```

See `probe_tool/README.md` for the full CLI reference.
