# Research Brief: Adversarial Robustness in Women's Safety AI

**Researcher:** Preethi Raghuveeran  
**Date:** May 2026  
**Target programs:** Anthropic Fellows · BlueDot Impact Frontier AI Governance

---

## The Problem in One Paragraph

Women's safety apps increasingly use AI — computer vision to detect threatening proximity, audio classification to detect distress, sensor fusion to trigger alerts automatically. These systems are deployed in high-stakes, time-critical conditions. Yet no published research examines how a physically proximate adversary can suppress, corrupt, or exhaust these systems before an alert is triggered. Existing adversarial ML assumes anonymous digital attackers or full model access. The real threat is a person standing next to the victim who knows the environment.

## Research Contribution

This project produces:
1. **Threat taxonomy** — 4-layer attack surface classification (sensing → processing → communication → response) × 5 attack methods (suppress / corrupt / spoof / exhaust / intercept) × 6 adversary access levels
2. **Scenario library** — 13+ grounded scenarios (8 urban, 5 rural) with Indian incident data, each mapped to attack method + access level + governance gap
3. **Governance gap analysis** — specific ungoverned attack surfaces across EU AI Act, NIST AI RMF, India DPDP Act 2023, India IT Act, ISO 42001
4. **Probe robustness tool specification** — Python CLI design for evaluating safety system profiles against this taxonomy

## Why Now

The EU AI Act requires conformity assessment for high-risk AI. Women's safety systems qualify under Annex III category 1 (biometric) and potentially category 6 (law enforcement-adjacent). No current standard requires adversarial robustness testing under physical proximity conditions. This research establishes what "robustness" should mean in this context.

## Novel Contribution

The physically proximate, environmentally familiar adversary model is absent from existing adversarial ML literature. The sociotechnical attack surfaces — social conditioning preventing victims from triggering alerts, cultural authority suppressing response — are absent from every governance framework reviewed.

## Connections to Existing Work

| This Research | Portfolio Link |
|---|---|
| Physical proximity attack surfaces | Extends SE1 (LLM Safety Eval, OWASP red-teaming) |
| Model failures in high-stakes settings | Connects to FT9 (proxy discrimination under quantization) |
| Cross-jurisdictional governance gaps | Connects to CCE1 (cross-jurisdictional compliance engine) |
| Longitudinal safety classifier drift | Connects to AC1 (agent goal drift detection) |
