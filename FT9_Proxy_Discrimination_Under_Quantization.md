# FT9: Proxy Discrimination Under Quantization

**Research Type:** Frontier Experiment  
**Dataset:** COMPAS Recidivism (ProPublica, 2016)  
**Model:** RecidivismNet — 3-layer neural network, 740 parameters  
**Status:** Complete ✅

---

## Overview

This experiment investigates whether model quantization — the process of reducing numerical precision to make AI models smaller and faster — disproportionately harms already-disadvantaged groups.

We trained a neural network on the COMPAS recidivism dataset and measured racial bias (False Positive Rate gap between Black and Other defendants) at three precision levels: FP32 (full precision), INT8, and INT4. We then conducted neuron-level attribution to understand *why* the gap behaved the way it did under precision reduction.

---

## Why This Matters

Quantization is increasingly used to deploy AI models on edge devices, mobile phones, and embedded systems. Standard benchmarks measure *accuracy loss* under quantization. Nobody measures *fairness degradation*.

If quantization disproportionately distorts the weights that encode protected attributes, it could amplify existing bias at inference time — harming already-marginalised groups without any change to training data or model architecture.

---

## Model

```
RecidivismNet:
  Linear(7 → 32) → ReLU
  Linear(32 → 16) → ReLU
  Linear(16 → 1)  → Sigmoid

Parameters: ~740
Features: age, priors_count, juv_fel_count, juv_misd_count, c_charge_degree, race, sex
Target: two_year_recid (binary)
```

Trained for 200 epochs, Adam optimizer, BCE loss. Final loss: 0.6041.

---

## Experiment

Three precision levels tested:

| Precision | Method |
|-----------|--------|
| FP32 | Standard PyTorch float32 training |
| INT8 | `torch.quantization.quantize_dynamic` — dynamic INT8 on Linear layers |
| INT4 | Simulated: uniform quantization to 16 levels (min–max range, per layer) |

---

## Results — Output Level

| Precision | Black FPR | Other FPR | FPR Gap | Δ Gap |
|-----------|-----------|-----------|---------|-------|
| FP32      | 28.4%     | 14.0%     | 14.4%   | —     |
| INT8      | 29.6%     | 15.1%     | 14.5%   | +0.1% |
| INT4      | 27.2%     | 13.8%     | 13.4%   | −1.0% |

**FPR = False Positive Rate:** defendants flagged as high-risk who did not reoffend.  
Black defendants are wrongly flagged at approximately **2× the rate** of Other defendants at every precision level.

---

## Results — Neuron Attribution

Layer 1 weight matrix: shape `[32, 7]` — 32 neurons, each with one weight per feature.

**Race-encoding neurons** (defined as `|race_weight| > 0.1`):

- **24 out of 32 neurons** carry a strong race signal
- These neurons push in competing directions — some increase risk for race=1, some decrease it
- The mean race weight ≈ 0, but individual neurons range from −0.50 to +0.50

**INT4 distortion by neuron type:**

| Neuron type | Avg INT4 weight distortion | 
|-------------|---------------------------|
| Race-encoding (n=24) | 0.014509 |
| Neutral (n=8)        | 0.017871 |
| **Ratio**            | **0.81×** |

Race-encoding neurons experience **19% less distortion** under INT4 than neutral neurons.

---

## The Mechanism

Race signal is encoded in neurons with **large weights** (ranging ±0.30 to ±0.50). INT4 quantization spreads 16 discrete levels uniformly across the full weight range. Large weights near the extremes of this range are preserved more faithfully than small weights near zero — small neutral weights may experience large *relative* distortion even though their absolute change is tiny.

Example from top-5 most distorted neurons:
- Neuron 4 [**neutral**]: −0.0214 → −0.0525 (distortion: 0.031) — a 145% relative shift
- Neuron 20 [**race**]: +0.1953 → +0.2258 (distortion: 0.031) — a 16% relative shift

---

## Key Finding

> Quantization does not widen racial bias in this model — but it cannot remove it either. The 2× FPR disparity for Black defendants is invariant to precision reduction. This is not because quantization is fair: race signal is encoded in neurons with large weights, which are inherently more resistant to INT4 precision loss. The bias is baked in at training and encoded in the most quantization-stable part of the network.

---

## Implications

1. **Null result ≠ no problem.** The gap didn't widen, but it didn't narrow either. Black defendants remain wrongly flagged at 2× the rate across all precision levels.
2. **Weight magnitude protects bias.** Models that encode protected attributes in high-magnitude weights may be especially resistant to fairness interventions applied post-training.
3. **Quantization alone is not a fairness lever.** Deploying INT4 models for efficiency does not introduce new fairness harms at this scale — but it also offers no fairness benefit.
4. **Scale may matter.** This model has 740 parameters. In larger models (millions of parameters), weight distributions are more complex. The mechanism identified here warrants testing at scale.

---

## Limitations

- Small model (740 parameters) — compounding effects may differ at scale
- INT4 is simulated via uniform quantization; production INT4 (e.g. NF4 via bitsandbytes) uses non-uniform schemes
- Single dataset (COMPAS) — results may not generalise to other domains
- Race is binary-encoded (African-American vs Other) — loses within-group variation

---

## Next Steps

- **FT12:** Test whether INT4-quantized model still passes DIR ≥ 0.80 regulatory threshold while causing harm (regulatory threshold gaming)
- **Scale test:** Repeat experiment on a larger pre-trained classifier (BERT-based tabular model) to test whether weight-magnitude protection holds at scale
- **Eval framework:** Build a reusable `quantization-fairness-audit` class that accepts any PyTorch model + protected attribute column and produces this full report automatically

---

## Files

| File | Description |
|------|-------------|
| `FT9_Notebook_1_Weights.ipynb` | Data loading, model architecture, weight inspection |
| `FT9_Notebook_2_Baseline.ipynb` | 200-epoch training, FP32 fairness baseline |
| `FT9_Notebook_3_Quantization.ipynb` | INT8/INT4 quantization, neuron attribution, charts |
| `ft9_quantization_fairness.png` | FPR by group + gap across precision levels |
| `ft9_neuron_distortion.png` | Scatter + bar chart of neuron-level distortion |

---

## Stack

Python · PyTorch · pandas · scikit-learn · matplotlib

---

*Part of the Algorithmic Fairness Auditor research series.*  
*Portfolio: [preetibuilds-33d6f6da.vercel.app](https://preetibuilds-33d6f6da.vercel.app/algorithmic-fairness)*  
*GitHub: [pretzelslab/ai-safety-research](https://github.com/pretzelslab/ai-safety-research)*
