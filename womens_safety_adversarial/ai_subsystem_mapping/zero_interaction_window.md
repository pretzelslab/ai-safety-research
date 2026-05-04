# Cross-Cutting Finding — The Zero-Interaction Window

## The Core Problem

In the most dangerous scenarios, a woman under attack has seconds — not minutes. She cannot type. She cannot speak a code word. She cannot respond to a check-in prompt. She cannot press a button.

This means: **in the extreme case, the entire system must detect and alert without any user action.**

The burden falls entirely on passive detection — vision, audio, and sensor fusion operating continuously in the background. If any of these fail, there is no fallback. The language/NLP layer, which requires conscious user input, is functionally unavailable.

This is the **zero-interaction window**: the period between when a threat becomes physical and when the victim loses the ability to interact with the device.

Estimated duration in high-risk scenarios: **2–15 seconds.**

---

## The Cascade Failure

Each Phase 3 subsystem file documents independent failure modes. In the zero-interaction window, they compound:

| Layer | Failure Mode (Phase 3) | Effect in Zero-Interaction Window |
|---|---|---|
| Vision / CV | Occlusion suppression; lighting corruption | Camera blocked or angle defeated — first passive layer fails |
| Audio | Ambient noise suppression; mic covered | Distress signal masked — second passive layer fails |
| Sensor Fusion | Transit vibration; GPS dead zone; network loss | IMU/GPS ambiguous or unavailable — third passive layer fails |
| Language / NLP | Requires conscious user input | **Unavailable by definition** — user cannot interact |

When all three passive layers fail simultaneously — which is trivially achievable in high-risk contexts (crowded transit, isolated vehicle, rural dead zone) — no detection fires. No alert is sent. The system produces a false-safe outcome at the exact moment of maximum danger.

**This is not a marginal edge case. It is the primary attack scenario.**

---

## Why This Is a Governance Gap, Not Just a Design Problem

Every governance framework reviewed (EU AI Act, NIST AI RMF, ISO 42001, India DPDP Act) evaluates AI systems on accuracy metrics — precision, recall, F1 — measured under controlled conditions with cooperative users.

None of them:
- Require testing under zero-user-action conditions
- Define a "passive detection only" operational mode for extreme scenarios
- Mandate that passive detection achieves minimum accuracy independently of any user interaction
- Address the compound failure of multiple passive layers under adversary-induced conditions

**The result:** a safety app can achieve 95% accuracy on benchmark datasets and 0% effective detection in the zero-interaction window of a real attack.

---

## Implications for Robustness Testing

Any robustness evaluation that includes user-initiated triggers (keyword, button, check-in response) is evaluating a different system than the one that must function in the extreme case. Robustness metrics must be computed on passive-detection-only test runs.

Proposed addition to evaluation criteria (Phase 5):

**Zero-Interaction Detection Rate (ZIDR)** — the proportion of attack scenarios correctly detected and alerted without any user action, under adversary-induced passive-layer degradation conditions. Minimum acceptable ZIDR: TBD (requires baseline from real system testing). Any system with ZIDR < 0.5 cannot be considered fit for high-risk deployment.

---

## Connections

- **Phase 3 subsystem files:** every failure mode documented there becomes critical rather than severe in the zero-interaction window
- **Phase 4 governance analysis:** each framework file should be evaluated against whether it requires zero-interaction testing — none currently do
- **Phase 5 probe robustness tool:** ZIDR should be a first-class output metric
- **Phase 6 research artifacts:** zero-interaction window framing is the strongest hook for the Anthropic Fellows brief and the one-pager — it makes the stakes concrete and the governance gap undeniable

---

## Novel Contribution

The zero-interaction window as a defined evaluation criterion for women's safety AI systems is not documented in existing adversarial ML literature. Existing work assumes either a cooperative user (HCI / usability research) or a digital attacker (adversarial ML). Neither maps onto a physical proximity attack where the victim loses agency within seconds.

**This framing is original to this research. Flag it as a novel contribution in all research artifacts.**
