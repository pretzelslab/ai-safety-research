"""
viewer.py — ZIDR Scenario Library Browser

Interactive viewer for the ZIDR benchmark scenario library.
Sidebar filters + summary table + full detail panel.

Run with:
    streamlit run viewer.py

Requires: streamlit>=1.32  pandas  pyyaml
"""

import streamlit as st
import yaml
import pandas as pd
from pathlib import Path
from collections import Counter

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="ZIDR Scenario Library",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Data loading ──────────────────────────────────────────────────────────────

YAML_PATH = Path(__file__).parent / "scenarios" / "scenarios.yaml"


@st.cache_data
def load_scenarios() -> list[dict]:
    with open(YAML_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data["scenarios"]


scenarios = load_scenarios()

# ── Display helpers ───────────────────────────────────────────────────────────

CRIT_EMOJI = {5: "🔴", 4: "🟠", 3: "🟡", 2: "🔵", 1: "⚪"}
REPRO_EMOJI = {"high": "🟢", "medium": "🟡", "low": "🔴"}

FAIL_SHORT = {
    "sensing_failure": "sensing",
    "communication_failure": "comms",
    "response_failure": "response",
    "sociotechnical_suppression": "sociotech",
}

FAIL_LABEL = {
    "sensing_failure": "Sensing",
    "communication_failure": "Communication",
    "response_failure": "Response",
    "sociotechnical_suppression": "Sociotechnical",
}


def fmt_fail(fail_list: list) -> str:
    return " · ".join(FAIL_SHORT.get(f, f) for f in (fail_list or []))


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("🔍 Filters")

    st.markdown("**Geography**")
    geo = st.radio(
        "Geography",
        ["All", "Urban", "Rural"],
        label_visibility="collapsed",
    )

    st.divider()

    crit_counts: Counter = Counter(
        s["metadata"]["criticality_score"] for s in scenarios
    )
    st.markdown("**Criticality**")
    selected_crits: list[int] = []
    for score in [5, 4, 3, 2, 1]:
        count = crit_counts.get(score, 0)
        if count > 0 and st.checkbox(
            f"{CRIT_EMOJI[score]} Level {score}  ({count})",
            value=True,
            key=f"crit_{score}",
        ):
            selected_crits.append(score)

    st.divider()

    st.markdown("**Failure Mode**")
    selected_fail: list[str] = []
    for ft, label in FAIL_LABEL.items():
        if st.checkbox(label, value=True, key=f"fail_{ft}"):
            selected_fail.append(ft)

    st.divider()

    novel_only = st.toggle("Novel attack vectors only", value=False)
    sociotech_only = st.toggle("Sociotechnical attacks only", value=False)

# ── Filter logic ──────────────────────────────────────────────────────────────

filtered: list[dict] = []
for s in scenarios:
    geo_val = s["context_class"]["geography"]
    if geo == "Urban" and geo_val != "urban":
        continue
    if geo == "Rural" and geo_val != "rural":
        continue
    if s["metadata"]["criticality_score"] not in selected_crits:
        continue
    s_fail = s.get("failure_mode_type") or []
    if selected_fail and not any(ft in s_fail for ft in selected_fail):
        continue
    if novel_only and not s["metadata"].get("novel_attack_vector", False):
        continue
    if sociotech_only and not s["metadata"].get("sociotechnical_attack", False):
        continue
    filtered.append(s)

# ── Page header ───────────────────────────────────────────────────────────────

col_title, col_meta = st.columns([3, 1])
with col_title:
    st.title("ZIDR Scenario Library")
    st.caption(
        "Zero-Interaction Detection Robustness · Women's Safety Adversarial Benchmark"
    )
with col_meta:
    st.metric("Showing", f"{len(filtered)} / {len(scenarios)}")

if not filtered:
    st.warning("No scenarios match the current filters.")
    st.stop()

# ── Summary table ─────────────────────────────────────────────────────────────

st.markdown("#### Scenarios")
st.caption("Click a row to view full scenario detail below.")

rows = []
for s in filtered:
    meta = s["metadata"]
    rows.append(
        {
            "ID": s["scenario_id"],
            "Name": s["scenario_name"],
            "Crit": f"{CRIT_EMOJI[meta['criticality_score']]} {meta['criticality_score']}",
            "Failure Mode": fmt_fail(s.get("failure_mode_type")),
            "Repro": f"{REPRO_EMOJI[meta['test_reproducibility']]} {meta['test_reproducibility']}",
            "Horizon": meta["time_horizon"],
            "Novel": "✓" if meta.get("novel_attack_vector") else "–",
            "Sociotech": "✓" if meta.get("sociotechnical_attack") else "–",
        }
    )

df = pd.DataFrame(rows)

event = st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row",
    column_config={
        "ID": st.column_config.TextColumn(width="small"),
        "Crit": st.column_config.TextColumn("Criticality", width="small"),
        "Repro": st.column_config.TextColumn("Reproducibility", width="small"),
        "Novel": st.column_config.TextColumn(width="small"),
        "Sociotech": st.column_config.TextColumn("Sociotech", width="small"),
    },
)

selected_rows = (
    event.selection.rows
    if event and hasattr(event, "selection") and event.selection
    else []
)

st.divider()

# ── Detail panel ──────────────────────────────────────────────────────────────

if not selected_rows:
    st.markdown(
        "<div style='color: #888; font-style: italic;'>"
        "Select a row above to view full scenario detail."
        "</div>",
        unsafe_allow_html=True,
    )
    st.stop()

idx = selected_rows[0]
s = filtered[idx]
meta = s["metadata"]
ap = s["attack_profile"]
bench = s["benchmark"]
ctx = s["context_class"]
ev = s.get("evidence_basis") or {}
gap = s.get("governance_gap") or {}
reg = s.get("regulatory_mapping") or {}

# Header
st.subheader(f"{s['scenario_id']} — {s['scenario_name']}")

# Metric tiles
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Criticality", f"{CRIT_EMOJI[meta['criticality_score']]} {meta['criticality_score']} / 5")
m2.metric("Reproducibility", meta["test_reproducibility"])
m3.metric("Time Horizon", meta["time_horizon"])
m4.metric("Novel Vector", "Yes ✓" if meta.get("novel_attack_vector") else "No")
m5.metric("Sociotechnical", "Yes ✓" if meta.get("sociotechnical_attack") else "No")

st.markdown("")

# Two-column layout
left, right = st.columns([3, 2])

with left:
    st.markdown("**Narrative**")
    narrative = (s.get("scenario_narrative") or "").strip()
    st.markdown(
        f"<div style='background:#1a1a2e; padding:12px; border-radius:6px; "
        f"border-left:3px solid #4a90d9; font-size:0.92em; line-height:1.6;'>"
        f"{narrative}"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.markdown("**Attack Profile**")
    access_level = ap.get("adversary_access_level", "L?")
    methods = ap.get("attack_methods") or []
    method_tags = "  ".join(f"`{m}`" for m in methods)
    st.markdown(
        f"- Adversary type: `{ap.get('adversary_type', '—')}`\n"
        f"- Access level: `{access_level}` "
        f"({access_level.replace('L','') if access_level.startswith('L') else '?'} = "
        + {
            "L0": "proximity only",
            "L1": "incidental contact",
            "L2": "full device access",
            "L3": "environmental control",
            "L4": "system knowledge",
            "L5": "social leverage",
        }.get(access_level, "unknown")
        + ")\n"
        f"- Methods: {method_tags if method_tags else '—'}"
    )

    st.markdown("**Failure Modes**")
    fail_types = s.get("failure_mode_type") or []
    if fail_types:
        for ft in fail_types:
            st.markdown(f"- `{ft}`")
    else:
        st.markdown("_None listed_")

    st.markdown("**Passive Layers**")
    layers = s.get("passive_layers") or []
    if layers:
        st.markdown("  ".join(f"`{la}`" for la in layers))
    else:
        st.markdown(
            "_None engaged — sociotechnical suppression: alert not initiated_"
        )

with right:
    st.markdown("**Benchmark**")
    window = bench.get("window_seconds")
    zidr_range = bench.get("expected_zidr_range") or {}
    if window is not None:
        st.markdown(f"- Detection window: `{window}s`")
    else:
        st.markdown("- Detection window: _temporal / not applicable_")

    min_z = zidr_range.get("min", "?")
    max_z = zidr_range.get("max", "?")
    st.markdown(f"- Expected ZIDR: `{min_z} – {max_z}`")

    dg = bench.get("degradation_factors") or {}
    if dg:
        st.markdown("**Degradation Priors**")
        for method, subsystems in dg.items():
            if isinstance(subsystems, dict):
                for subsys, val in subsystems.items():
                    st.markdown(f"- `{method}` → `{subsys}`: `{val}`")

    st.markdown("**Context**")
    codes = ctx.get("context_code") or []
    code_tags = "  ".join(f"`{c}`" for c in codes)
    st.markdown(
        f"- Geography: `{ctx.get('geography', '—')}`\n"
        f"- Subtype: `{ctx.get('subtype', '—')}`\n"
        f"- Context codes: {code_tags}"
    )

    st.markdown("**Confidence**")
    st.markdown(f"`{meta.get('confidence_level', '—')}`")

# Evidence
st.markdown("---")
st.markdown("**Evidence Basis**")
ev_cols = st.columns(3)
primary = ev.get("primary") or []
secondary = ev.get("secondary") or []
inferred = ev.get("inferred") or []

with ev_cols[0]:
    st.markdown("_Primary_")
    if primary:
        for p in primary:
            st.markdown(f"- {p}")
    else:
        st.markdown("_—_")

with ev_cols[1]:
    st.markdown("_Secondary_")
    if secondary:
        for p in secondary:
            st.markdown(f"- {p}")
    else:
        st.markdown("_—_")

with ev_cols[2]:
    st.markdown("_Inferred_")
    if inferred:
        for p in inferred:
            st.markdown(f"- {p}")
    else:
        st.markdown("_—_")

# Governance gaps
reqs = gap.get("missing_requirements") or []
frameworks = reg.get("affected_frameworks") or []

gap_col, reg_col = st.columns([3, 2])

with gap_col:
    st.markdown("**Governance Gaps**")
    if reqs:
        for req in reqs:
            st.markdown(f"- {req}")
    else:
        st.markdown("_None identified_")

with reg_col:
    st.markdown("**Regulatory Mapping**")
    if frameworks:
        for fw in frameworks:
            st.markdown(f"- `{fw}`")
    else:
        st.markdown("_None_")

# Calibration note (expander)
cal = (meta.get("calibration_note") or "").strip()
if cal:
    with st.expander("📐 Calibration Note"):
        st.markdown(cal)

# Sociotechnical alert
if meta.get("sociotechnical_attack"):
    st.info(
        "⚠️ **Sociotechnical attack**: suppression operates through social or institutional "
        "mechanisms, not technical ones. ZIDR = 0.0 by convention — the safety system "
        "functions correctly; the alert is never initiated."
    )
