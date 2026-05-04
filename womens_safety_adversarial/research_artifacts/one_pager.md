# When the App Fails First
## Adversarial Robustness Gaps in Women's Safety AI Systems

**Preethi Raghuveeran | Independent AI Safety Researcher | May 2026**

---

## The Claim Every Safety App Makes

AI-enabled women's safety apps — used by millions across India, Europe, and Southeast Asia — promise automatic detection. No button needed. The system detects proximity threats, distress sounds, and sudden movement, and alerts help without the user doing anything.

This claim is tested in controlled conditions with cooperative users.

It has never been tested against an adversary.

---

## The Zero-Interaction Window

In the most dangerous scenarios, a woman under attack has 2–15 seconds before she loses the ability to interact with her device. She cannot type. She cannot speak a code word. She cannot press a button.

During this window, detection depends entirely on passive systems: computer vision, audio classification, and sensor fusion running in the background. If these fail — or are made to fail — no alert fires. There is no fallback.

**A safety app can achieve 95% accuracy on benchmark datasets and 0% effective detection in the zero-interaction window of a real attack.**

This gap has a name: the **Zero-Interaction Detection Rate (ZIDR)**. ZIDR measures what a system actually detects when a physically proximate adversary is actively working to suppress passive detection — with no button presses, no code words, no user input of any kind.

No existing evaluation standard measures ZIDR. No current governance framework requires it.

---

## The Adversary This Research Studies

Existing adversarial machine learning assumes anonymous digital attackers, or researchers with full access to model weights. Neither describes the real threat to a woman using a safety app.

The adversary in this research is:
- **Physically present** — 0–50 metres away
- **Environmentally familiar** — knows the space, the victim's patterns, the timing
- **Adaptive** — modifies behaviour in real time based on what the system appears to detect
- **Low-tech** — requires no hacking, no code, no device access

A hand over a camera lens. Ambient noise at the right frequency. A crowded transit environment with a GPS dead zone. These are not sophisticated attacks. They require no technical knowledge.

No existing research studies this adversary. Confirmed across nine published sources.

---

## What This Research Produces

1. **Threat taxonomy** — a 4-layer attack surface framework × 5 attack methods × 6 adversary access levels; the lowest level requires only physical proximity
2. **Scenario library** — 13 grounded scenarios (8 urban, 5 rural) anchored in Indian incident data, each mapped to an attack method and a governance gap
3. **Governance gap analysis** — specific ungoverned attack surfaces identified in EU AI Act, NIST AI RMF, ISO 42001, and India's Digital Personal Data Protection Act 2023
4. **ZIDR** — a proposed evaluation metric: the proportion of attack scenarios correctly detected and alerted without any user action, under adversary-induced conditions
5. **Probe robustness tool specification** — open methodology for evaluating any safety system profile against this taxonomy

---

## The Governance Gap

Every framework reviewed evaluates AI systems on accuracy metrics measured with cooperative users. None require:
- Testing under zero-user-action conditions
- Passive-detection-only evaluation as a distinct test mode
- A minimum ZIDR threshold for high-risk deployment certification

The EU AI Act classifies women's safety systems as high-risk AI (Annex III). Conformity assessment is required. But conformity assessment standards do not yet define what robustness means for passive detection under adversarial physical conditions.

**This research names that gap. Closing it is the policy contribution of this work.**

---

## Contact

**Preethi Raghuveeran**
Independent AI Safety Researcher
preeti.raghuveer@gmail.com | github.com/pretzelslab

**Cite this work:**
Raghuveeran, P. (2026). Adversarial Robustness in Women's Safety AI Systems: Threat Taxonomy, ZIDR Metric, and Governance Gap Analysis. Zenodo. https://doi.org/10.5281/zenodo.20028247

**Related work:**
Raghuveeran, P. (2026). Carbon-Aware Inference Routing for Large Language Models: A Real-Time Framework for Sustainable AI Serving. Zenodo. https://doi.org/10.5281/zenodo.19934621
