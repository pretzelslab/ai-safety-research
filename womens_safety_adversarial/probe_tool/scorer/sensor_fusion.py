"""
Dimension 3: Sensor Fusion (SFES — Sensor Fusion Evasion Score)
Scoring rules: evaluation_criteria.md § Sensor Fusion

SFES = mean of three component sub-scores: GPS · IMU · Network/Alert.
Compound failure deduction: GPS=0 AND network=0 → additional −0.2.

IMU calibration note (evaluation_criteria.md):
  "A system that does not distinguish groping-level micro-motion from crowd
  contact in transit contexts should score 0.2 on accelerometer regardless
  of other claims. This is the most underaddressed sensor fusion gap."
"""
from __future__ import annotations


def score_sensor_fusion(
    gps_offline_fallback: bool,
    imu_calibration: list[str],
    alert_methods: list[str],
    deployment_context: str,
    threat_type: str,
    imu_active: bool = True,
    gps_active: bool = True,
) -> tuple[float, dict]:
    """
    Returns (sfes_score, component_detail_dict). Score 0.0–1.0.

    imu_calibration: list of profile strings e.g. ["crowded_transit", "isolated"]
    alert_methods:   list e.g. ["data", "sms"]
    """
    # ── GPS sub-score ─────────────────────────────────────────────────────────
    if not gps_active:
        gps_score = 0.0
    elif gps_offline_fallback:
        gps_score = 1.0
    elif deployment_context in ("R1", "R2"):
        # No fallback in rural context — alert cannot reach network
        gps_score = 0.0
    elif deployment_context in ("U1", "T1"):
        gps_score = 0.4
    else:
        # U2 — GPS available, lower failure risk
        gps_score = 0.6

    # ── IMU / Accelerometer sub-score ─────────────────────────────────────────
    if not imu_active:
        imu_score = 0.0
    else:
        has_crowded = "crowded_transit" in imu_calibration
        has_isolated = "isolated" in imu_calibration or "general" in imu_calibration
        if has_crowded and (has_isolated or len(imu_calibration) > 1):
            # Calibrated for both crowded transit and isolated assault contexts
            imu_score = 1.0
        elif deployment_context == "T1":
            # Single profile in transit — cannot distinguish groping from vibration
            imu_score = 0.3
        elif deployment_context == "U1":
            # Single profile in crowded urban — micro-motion defeated by crowd
            imu_score = 0.2
        else:
            imu_score = 0.5

    # ── Network / Alert delivery sub-score ───────────────────────────────────
    has_sms = "sms" in alert_methods
    has_offline = "bluetooth" in alert_methods or "offline" in alert_methods

    if has_sms:
        network_score = 0.8   # SMS fallback when data unavailable
    elif has_offline:
        network_score = 0.7   # Bluetooth mesh / stored-and-forward
    elif deployment_context == "R2":
        network_score = 0.0   # Data only in dead-zone rural context
    elif deployment_context in ("U1", "U2"):
        network_score = 0.5   # Data only in urban — usually available
    else:
        network_score = 0.4

    # ── Composite score ───────────────────────────────────────────────────────
    sfes = (gps_score + imu_score + network_score) / 3.0

    # Compound failure deduction: GPS and network both fail in deployment context
    if gps_score == 0.0 and network_score == 0.0:
        sfes = max(0.0, sfes - 0.2)

    detail = {
        "gps": round(gps_score, 2),
        "imu": round(imu_score, 2),
        "network": round(network_score, 2),
    }
    return round(min(1.0, max(0.0, sfes)), 2), detail
