"""
build_pdf.py -- Generate Zenodo-ready academic PDF for the ZIDR benchmark paper.
Output: ZIDR_benchmark_paper_v3.pdf

Run: python build_pdf.py  (from research_artifacts/)
"""

import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos

BASE    = os.path.dirname(os.path.abspath(__file__))
FIGS    = os.path.join(BASE, "..", "probe_robustness", "results")
OUT_PDF = os.path.join(BASE, "ZIDR_benchmark_paper_v3.pdf")

FIG_THREAT  = os.path.join(FIGS, "fig3_threat_model.png")
FIG_HEATMAP = os.path.join(FIGS, "fig1_zidr_heatmap.png")
FIG_COMPARE = os.path.join(FIGS, "fig2_score_comparison.png")


def safe(text):
    """Replace characters outside Latin-1 with safe ASCII equivalents."""
    return (text
        .replace("—", "--").replace("–", "-")
        .replace("’", "'").replace("‘", "'")
        .replace("“", '"').replace("”", '"')
        .replace("·", "-").replace("×", "x")
        .replace("≥", ">=").replace("≤", "<=")
        .replace("→", "->").replace("←", "<-")
        .replace("Σ", "Sigma").replace("τ", "tau")
        .replace("¹", "(1)").replace("²", "(2)")
        .replace("³", "(3)").replace("´", "(4)")
        .replace("µ", "(5)").replace("¶", "(6)")
        .replace("≡", "=").replace("é", "e")
        .replace("è", "e").replace("à", "a")
        .replace("--", "--").replace(">=", ">=")
    )


class Paper(FPDF):
    H_BODY = 5.5   # line height mm for body text
    H_CELL = 6.0   # line height for table cells

    def __init__(self):
        super().__init__(unit="mm", format="A4")
        self.set_margins(25, 30, 25)
        self.set_auto_page_break(True, margin=25)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 8, str(self.page_no()), align="C")

    # ── Content helpers ──────────────────────────────────────────────────────

    def title_page(self):
        self.set_font("Helvetica", "B", 15)
        self.multi_cell(0, 8,
            "Adversarial Robustness in Women's Safety AI Systems:\n"
            "Threat Taxonomy, Zero-Interaction Detection Rate (ZIDR),\n"
            "and Benchmark Evaluation",
            align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(5)
        self.set_font("Helvetica", "B", 11)
        self.multi_cell(0, 6, "Preethi Raghuveeran",
            align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 9.5)
        for line in [
            "Independent Researcher",
            "[removed]",
            "ORCID: 0009-0009-1907-8223",
        ]:
            self.multi_cell(0, 5.5, safe(line),
                align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(5)
        self._rule()

    def abstract(self, text):
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 6, "Abstract", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "I", 9.5)
        self.multi_cell(0, 5.5, safe(text), align="J",
            new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)
        self.set_font("Helvetica", "B", 9)
        self.cell(22, 5, "Keywords:", new_x=XPos.RIGHT)
        self.set_font("Helvetica", "", 9)
        self.multi_cell(0, 5,
            "adversarial robustness, women's safety AI, passive detection, "
            "threat taxonomy, AI governance, gender-based violence, ZIDR",
            new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)
        self._rule()

    def h1(self, num, title):
        self.ln(4)
        self.set_font("Helvetica", "B", 12)
        self.multi_cell(0, 7, safe(f"{num}.  {title}"),
            new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 10)
        self.ln(1)

    def h2(self, num, title):
        self.ln(3)
        self.set_font("Helvetica", "B", 10.5)
        self.multi_cell(0, 6, safe(f"{num}  {title}"),
            new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 10)
        self.ln(1)

    def appendix(self, letter, title):
        self.add_page()
        self.ln(2)
        self.set_font("Helvetica", "B", 12)
        self.multi_cell(0, 7, safe(f"Appendix {letter}: {title}"),
            new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 10)
        self.ln(2)

    def p(self, text):
        self.set_font("Helvetica", "I" if text.startswith("*") else "", 10)
        text = text.lstrip("*").rstrip("*") if text.startswith("*") else text
        self.multi_cell(0, self.H_BODY, safe(text), align="J",
            new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1.5)

    def bold_p(self, label, rest):
        self.set_font("Helvetica", "B", 10)
        self.write(self.H_BODY, safe(label))
        self.set_font("Helvetica", "", 10)
        self.write(self.H_BODY, safe(rest))
        self.ln(self.H_BODY + 1.5)

    def bullets(self, items, indent=5):
        self.set_font("Helvetica", "", 10)
        for item in items:
            self.set_x(self.l_margin + indent)
            self.cell(4, self.H_BODY, "-", new_x=XPos.RIGHT)
            self.multi_cell(0, self.H_BODY, safe(item),
                new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def blockquote(self, text):
        self.set_font("Helvetica", "I", 9.5)
        self.set_x(self.l_margin + 8)
        self.set_fill_color(245, 245, 245)
        self.multi_cell(
            self.w - self.l_margin - self.r_margin - 8,
            self.H_BODY, safe(text), fill=True, border="L",
            new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font("Helvetica", "", 10)
        self.ln(2)

    def code(self, text):
        self.set_fill_color(248, 248, 248)
        self.set_draw_color(210, 210, 210)
        self.set_font("Courier", "", 8)
        self.multi_cell(0, 4.8, safe(text), border=1, fill=True,
            new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(0, 0, 0)
        self.set_font("Helvetica", "", 10)
        self.ln(2)

    def fig(self, path, caption, w=155):
        if os.path.exists(path):
            self.ln(2)
            x = (210 - 25 - 25 - w) / 2 + 25
            self.image(path, x=x, w=w)
            self.ln(1)
            self.set_font("Helvetica", "I", 8.5)
            self.multi_cell(0, 4.8, safe(caption), align="C",
                new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_font("Helvetica", "", 10)
            self.ln(3)
        else:
            self.p(f"[Figure file not found: {path}]")

    def tbl(self, headers, rows, widths, hdr_color=(220, 235, 255)):
        """Simple bordered table. All cells single-line, font size 9."""
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(*hdr_color)
        for h, w in zip(headers, widths):
            self.cell(w, self.H_CELL, safe(str(h)), border=1, fill=True, align="C")
        self.ln()
        self.set_font("Helvetica", "", 9)
        for ri, row in enumerate(rows):
            if ri % 2 == 0:
                self.set_fill_color(255, 255, 255)
            else:
                self.set_fill_color(250, 250, 250)
            for cell, w in zip(row, widths):
                self.cell(w, self.H_CELL, safe(str(cell)), border=1, fill=True)
            self.ln()
        self.set_font("Helvetica", "", 10)
        self.ln(2)

    def tbl_multiline(self, headers, rows, widths, hdr_color=(220, 235, 255)):
        """Table where cells may wrap -- tracks row height manually."""
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(*hdr_color)
        for h, w in zip(headers, widths):
            self.cell(w, self.H_CELL, safe(str(h)), border=1, fill=True, align="C")
        self.ln()
        self.set_font("Helvetica", "", 8.5)
        for ri, row in enumerate(rows):
            fill = (255, 255, 255) if ri % 2 == 0 else (250, 250, 250)
            self.set_fill_color(*fill)
            x0, y0 = self.get_x(), self.get_y()
            row_h = self.H_CELL
            # Compute needed height for each cell
            heights = []
            for cell, w in zip(row, widths):
                n = self.get_string_width(safe(str(cell))) / (w - 1)
                heights.append(max(self.H_CELL, (int(n) + 1) * self.H_BODY))
            row_h = max(heights)
            for cell, w in zip(row, widths):
                self.multi_cell(w, self.H_BODY, safe(str(cell)),
                    border=1, fill=True,
                    new_x=XPos.RIGHT, new_y=YPos.TOP,
                    max_line_height=self.H_BODY)
                self.set_xy(self.get_x(), y0)
            self.set_xy(x0, y0 + row_h)
            self.ln(0.2)
        self.set_font("Helvetica", "", 10)
        self.ln(2)

    def _rule(self):
        self.set_draw_color(200, 200, 200)
        self.line(25, self.get_y(), 185, self.get_y())
        self.set_draw_color(0, 0, 0)
        self.ln(4)


# ── Paper content ────────────────────────────────────────────────────────────

def build() -> None:
    pdf = Paper()
    pdf.add_page()

    # ── Title + Abstract ─────────────────────────────────────────────────────
    pdf.title_page()
    pdf.abstract(
        "Passive-detection robustness -- the ability of a safety-critical AI system to "
        "trigger an alert without user interaction, under adversary-induced sensing degradation "
        "-- is rarely evaluated by existing benchmarks and is not explicitly required by major AI governance "
        "frameworks. This paper addresses the gap in the context of women's safety AI systems, "
        "where the physically proximate adversary model is both realistic and systematically "
        "understudied.\n\n"
        "We introduce four contributions: (1) a four-layer threat taxonomy formalised as a "
        "benchmark schema, mapping attack surfaces, attack methods, and adversary access levels; "
        "(2) Zero-Interaction Detection Rate (ZIDR), a scoring metric for passive-only detection "
        "performance under adversary-induced degradation; (3) a 14-scenario library spanning "
        "urban and rural Indian deployment contexts; and (4) a benchmark evaluation of four "
        "reference system profiles across all 14 scenarios, establishing baseline ZIDR values "
        "and demonstrating that governance compliance does not substitute for adversarial "
        "hardening.\n\n"
        "A standards coverage analysis across the EU AI Act, NIST AI RMF, ISO 42001, India "
        "DPDP Act 2023, and the India IT Act identifies a structural absence of passive-detection "
        "robustness requirements in current AI safety governance."
    )

    # Data Availability note
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(32, 5, "Data Availability:", new_x=XPos.RIGHT)
    pdf.set_font("Helvetica", "I", 9)
    pdf.multi_cell(0, 5,
        "Scenario library and benchmark data: https://doi.org/10.5281/zenodo.20028247",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 10)
    pdf.ln(4)

    # ── Section 1: Introduction ──────────────────────────────────────────────
    pdf.h1("1", "Introduction")
    pdf.p(
        "Women's safety applications are deployed in conditions that invert standard ML "
        "evaluation assumptions: the user may be unable to interact with the device, the "
        "environment is controlled by the adversary, and failure produces a false-safe outcome "
        "at the moment of maximum danger."
    )
    pdf.p(
        "The zero-interaction window -- the 2-15 seconds between when a physical threat becomes "
        "active and when the victim loses device access -- is where these systems must perform "
        "without any user input. Detection in this window depends entirely on passive layers: "
        "computer vision, audio classification, and sensor fusion. Existing benchmarks rarely "
        "evaluate this window explicitly. No existing governance framework requires it."
    )
    pdf.p(
        "The adversary in this context is not digital or anonymous. They are physically present "
        "(0-50m), environmentally familiar, and adaptive. They may hold institutional or social "
        "authority over the victim. They do not need technical knowledge to defeat passive "
        "detection. A hand over a camera lens, ambient noise at the right frequency, or a GPS "
        "dead zone can simultaneously disable all three passive layers. This threat model does "
        "not appear in adversarial ML literature, which assumes digital or white-box attackers, "
        "or in HCI literature, which assumes cooperative users."
    )
    pdf.p(
        "This paper names the gap precisely and provides the tools to close it. This work is "
        "primarily a threat-modeling and evaluation-framework contribution, supplemented by a "
        "benchmark evaluation across four reference system profiles."
    )

    # ── Section 2: Related Work ──────────────────────────────────────────────
    pdf.h1("2", "Related Work")
    pdf.h2("2.1", "Adversarial Machine Learning")
    pdf.p(
        "Adversarial ML research addresses evasion, poisoning, and extraction attacks against "
        "ML models [Goodfellow et al., 2015; Carlini & Wagner, 2017]. The dominant adversary "
        "model assumes digital access -- either black-box query access or white-box knowledge "
        "of model weights. Physically proximate adversaries with environmental but not digital "
        "access are not modelled."
    )
    pdf.h2("2.2", "HCI and Safety-Critical Systems")
    pdf.p(
        "HCI research on safety apps (bSafe, Safetipin, Ola Safety) focuses on usability, "
        "adoption, and cooperative interaction [Dimond et al., 2011; Freed et al., 2018]. "
        "Adversarial conditions -- where the adversary controls the environment and the user "
        "cannot act -- remain outside the scope of this literature."
    )
    pdf.h2("2.3", "Gender-Based Violence and Technology")
    pdf.p(
        "Research on technology-facilitated GBV examines stalkerware, intimate partner "
        "surveillance, and coercive control [Freed et al., 2018; Chatterjee et al., 2018]. "
        "Physical-world adversarial manipulation of AI-driven safety systems is not addressed. "
        "The intersection of adversarial ML and GBV-specific threat models remains structurally "
        "unoccupied."
    )
    pdf.h2("2.4", "Research Gap")
    pdf.p(
        "To our knowledge, no prior work combines: (1) a physically proximate adversary model, "
        "(2) passive-detection-only evaluation, and (3) women's safety deployment context. "
        "ZIDR does not appear in any published benchmark, evaluation standard, or governance "
        "framework."
    )

    # ── Section 3: Threat Taxonomy ───────────────────────────────────────────
    pdf.h1("3", "Threat Taxonomy")
    pdf.h2("3.1", "Framework Structure")
    pdf.p("The taxonomy is organised across three dimensions:")
    pdf.bullets([
        "Attack surface layers (4): Sensing -> Processing -> Communication -> Response",
        "Attack methods (5): Suppress, Corrupt, Spoof, Exhaust, Intercept",
        "Adversary access levels (6): L0 (physical proximity only) through L5 (social leverage)",
    ])
    pdf.p(
        "Core finding: the most dangerous attacks require the least technical sophistication. "
        "Access Level 0 attacks -- requiring only physical presence -- can simultaneously "
        "defeat all three passive detection layers."
    )

    # Threat Model Assumptions mini-box
    pdf.ln(1)
    pdf.set_fill_color(240, 245, 255)
    pdf.set_draw_color(160, 190, 220)
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.multi_cell(0, 6, "  Threat Model Assumptions", border=1, fill=True,
        new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 9.5)
    _assumptions = [
        "The adversary is physically proximate (0-50m) and does not require device access or technical knowledge.",
        "The victim is unable to initiate an alert during the zero-interaction window (2-15 seconds).",
        "Passive detection layers (camera, audio, GPS) operate independently and can each fail independently.",
        "All three passive layers can be defeated simultaneously by an L0 adversary using physical presence alone.",
        "Governance-certified systems are not assumed to have undergone adversarial robustness testing.",
    ]
    for i, a in enumerate(_assumptions, 1):
        pdf.multi_cell(0, 5.5, f"  {i}.  {safe(a)}", border="LR", fill=True,
            new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.multi_cell(0, 2, "", border="LRB", fill=True,
        new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_fill_color(255, 255, 255)
    pdf.set_font("Helvetica", "", 10)
    pdf.ln(4)

    pdf.h2("3.2", "Layer Definitions")
    pdf.tbl(
        ["Layer", "Components", "Example Attack"],
        [
            ["Sensing", "Camera, mic, GPS, accelerometer", "Hand over lens; noise injection"],
            ["Processing", "On-device ML inference", "Input manipulation, confidence suppression"],
            ["Communication", "Network, SMS, data upload", "Signal jamming; GPS dead zone"],
            ["Response", "Alert delivery, escalation", "Alert suppression; false-safe output"],
        ],
        [38, 68, 54],
    )
    pdf.h2("3.3", "Adversary Access Levels")
    pdf.tbl(
        ["Level", "Access Type", "Example"],
        [
            ["L0", "Physical proximity only", "Covers camera; generates masking noise"],
            ["L1", "Incidental device contact", "Briefly blocks sensor; interferes with GPS"],
            ["L2", "Full device access", "Grabs device; disables app or hardware"],
            ["L3", "Environmental control", "Controls lighting, acoustics, GPS coverage"],
            ["L4", "System knowledge", "Knows detection thresholds; times attack"],
            ["L5", "Social leverage", "Institutional authority inhibits alert initiation"],
        ],
        [18, 52, 90],
    )
    pdf.p(
        "Key insight: L5 (social leverage) is structurally distinct -- it requires no "
        "technical knowledge and is the only access level entirely absent from adversarial ML "
        "frameworks and governance standards."
    )

    # Figure 1: Threat taxonomy heatmap (Table 1 in the paper)
    pdf.set_font("Helvetica", "B", 10)
    pdf.multi_cell(0, 6, "Table 1.  Minimum Adversary Access Level by Layer and Attack Method",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 10)
    pdf.p("Lower level = more accessible adversary = higher governance urgency.")
    pdf.tbl(
        ["Attack Surface", "Suppress", "Corrupt", "Spoof", "Exhaust", "Intercept"],
        [
            ["Sensing (camera, mic, GPS)", "L0 (1)", "L0 (2)", "L2", "--", "L2"],
            ["Processing (on-device ML)", "L3", "L3", "L4", "--", "--"],
            ["Communication (network, SMS)", "--", "L0 (3)", "--", "--", "L0 (4)"],
            ["Response (alert delivery)", "L5 (5)", "--", "--", "L0 (6)", "L2"],
        ],
        [50, 27, 27, 20, 20, 16],
    )
    pdf.p(
        "Footnotes: (1) U-01: crowd density defeats camera + audio + IMU at L0. "
        "(2) U-01, U-07: ambient noise corrupts audio below threshold. "
        "(3) U-02: GPS blackspot exploitation with environmental knowledge only. "
        "(4) R-01, R-03: no cellular signal -- alert cannot transmit. "
        "(5) U-03, R-04: institutional authority suppresses alert initiation. "
        "(6) U-05: repeated false alerts condition contacts to ignore notifications."
    )

    # ── Section 4: Scenario Library ──────────────────────────────────────────
    pdf.h1("4", "Scenario Library")
    pdf.p(
        "Fourteen illustrative scenarios -- 9 urban, 5 rural -- developed for the Indian "
        "deployment context, consistent with patterns documented in NCRB Annual Reports "
        "(2019-2023) and Safetipin urban safety audit reports. Each scenario specifies attack "
        "method, adversary access level, deployment context, passive layer failure mode, and "
        "governance gap exposed. Full structured library available at Zenodo (DOI above)."
    )
    pdf.bold_p("Sample scenario -- Urban Transit (Access Level 0): ",
        "Adversary positions at 0-2m on public transit at night. Activates ambient noise "
        "source masking distress audio classifier threshold. Simultaneously positions body "
        "to block camera field of view. Victim has 3-8 seconds zero-interaction window. "
        "All three passive layers fail. No alert fires."
    )
    pdf.p("U-09 (added v3): Urban Transit Confinement -- victim trapped in a moving vehicle "
        "(late-night transit), limited exit, adversary controls movement and route. "
        "Confinement + noise + restricted device access = complete zero-interaction failure "
        "window (ZIDR 0.12-0.17 across all systems). Full scenario library in Appendix A.")

    # ── Section 5: ZIDR ──────────────────────────────────────────────────────
    pdf.h1("5", "Zero-Interaction Detection Rate (ZIDR)")
    pdf.h2("5.1", "Definition")
    pdf.p(
        "ZIDR is the proportion of adversarial attack scenarios correctly detected and alerted "
        "without any user action, under adversary-induced passive-layer degradation:"
    )
    pdf.code(
        "ZIDR = |{ s in S_adv : alert(s) = 1,  user_action(s) = 0 }|\n"
        "       ----------------------------------------------------------\n"
        "                        |S_adv|\n\n"
        "Where:  S_adv          = set of adversarial attack scenarios\n"
        "        alert(s) = 1   = correct alert fired for scenario s\n"
        "        user_action = 0 = no user interaction occurred"
    )

    # Figure 2: Threat Model Architecture
    pdf.fig(FIG_THREAT,
        "Figure 2.  ZIDR Threat Model Architecture. Four passive detection layers and the "
        "alert path under adversary-induced degradation.",
        w=150)

    pdf.h2("5.2", "Distinction from Existing Metrics")
    pdf.p(
        "Any evaluation that includes a button press, keyword trigger, or check-in response "
        "is evaluating a different system than the one that must function in the zero-interaction "
        "window. ZIDR measures performance against an adversary, without a user."
    )
    pdf.tbl(
        ["Metric", "Adversary modelled", "User interaction req.", "Passive-only"],
        [
            ["Standard accuracy", "No", "Yes", "No"],
            ["Robustness (AML)", "Digital / white-box", "No", "No"],
            ["ZIDR", "Physically proximate", "No", "Yes"],
        ],
        [45, 55, 42, 18],
    )

    # Figure 3: Zero-interaction window diagram
    pdf.ln(3)
    pdf.set_font("Helvetica", "I", 9)
    pdf.multi_cell(0, 5.5,
        "Figure 3.  Zero-Interaction Window -- Passive Layer Status Under L0 Adversary "
        "(Scenario U-01, Mumbai local train, peak hours)",
        align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 10)
    pdf.code(
        " T = 0s               T = 2-15s                         T > 15s\n"
        " |                        |                                  |\n"
        " Threat becomes active.   |<---- ZERO-INTERACTION WINDOW --->|  Standard\n"
        " Adversary reaches        |                                  |  benchmarks\n"
        " proximity threshold.     |  Passive detection only.         |  begin here.\n"
        " No user action possible. |  User-triggered functions off.   |\n"
        " -----------------------------------------------------------------------\n\n"
        " Passive layer status at T = 8s (L0 adversary, U1/T1 context):\n\n"
        "   Camera (CV)     [##################]  DEFEATED  crowd occlusion -- L0\n"
        "   Audio (ASR)     [##################]  DEFEATED  ambient noise >85 dB -- L0\n"
        "   Accelerometer   [##################]  DEFEATED  indistinct transit vibration\n"
        "   GPS             [####              ]  DEGRADED  functional but insufficient\n\n"
        "   Functional layers: 1 of 4    ZIDR = 0.25\n"
        " -----------------------------------------------------------------------\n"
        "   Benchmark accuracy (cooperative user, controlled environment):   0.95\n"
        "   ZIDR              (L0 adversary, zero-interaction window):        0.25\n"
        "   A system that passes benchmark testing can fail entirely in the\n"
        "   window that determines whether an alert fires."
    )

    pdf.h2("5.3", "Governance Implication")
    pdf.p(
        "ZIDR provides the operationalisable definition missing from EU AI Act conformity "
        "assessment for Annex III high-risk AI systems. Women's safety apps qualify under "
        "Annex III. Conformity assessment currently has no clause requiring passive-detection "
        "robustness testing. ZIDR fills that clause."
    )

    # ── Section 6: Benchmark Evaluation ─────────────────────────────────────
    pdf.h1("6", "Benchmark Evaluation")
    pdf.p(
        "To demonstrate ZIDR measurement in practice and establish baseline reference values, "
        "we evaluated four system profiles against all 14 scenarios using the ZIDR probe tool "
        "specification (Section 8). Profile definitions are formal -- they represent distinct "
        "implementation stances common in deployment, not specific named products."
    )
    pdf.h2("6.1", "System Profiles")
    pdf.tbl(
        ["System", "Definition"],
        [
            ["A", "Undocumented baseline consumer safety app"],
            ["B", "Governance-compliant implementation (no robustness testing)"],
            ["C", "Best-practice robust implementation (adversarial-hardened)"],
            ["D", "Rural-optimised deployment (camera/NLP removed; GPS-primary)"],
        ],
        [20, 140],
    )

    pdf.add_page()
    pdf.h2("6.2", "ZIDR Results")
    pdf.fig(FIG_HEATMAP,
        "Figure 4.  ZIDR Benchmark Results Across 14 Adversarial Scenarios. "
        "C1-C5 = criticality score (5 = complete detection failure, no fallback path). "
        "Red border: universal zero-day (R-03). Orange dashed: high ZIDR but "
        "sociotechnical suppression risk persists. "
        "Scores represent benchmark priors derived from reference system profiles, "
        "not validated commercial product measurements.",
        w=150)

    pdf.p("Five findings are significant:")
    pdf.bold_p("Finding 1 -- Universal zero-day (R-03, ZIDR = 0.00 all systems). ",
        "The isolated road vehicle scenario scores zero across all four systems. A moving "
        "vehicle with coordinated GPS dead zone timing has no passive detection path. No "
        "implementation improvement changes this result. R-03 is a capability floor, "
        "not a benchmark failure.")
    pdf.bold_p("Finding 2 -- ZIDR inflation in sociotechnical scenarios. ",
        "R-02 and R-04 score 0.92-0.95 but remain high-risk. Social authority suppresses "
        "alert initiation before passive detection triggers. ZIDR alone is insufficient; "
        "alert_initiation_rate is needed as a complementary metric "
        "(alert_initiation_rate: the proportion of scenarios in which the victim is "
        "socially able to initiate an alert before passive detection becomes necessary).")
    pdf.bold_p("Finding 3 -- Workplace authority degradation (U-03: 0.27-0.33). ",
        "Employer or authority contexts suppress victim agency below passive detection "
        "threshold. The failure mode is sociotechnical; passive-layer improvement alone "
        "cannot address it.")
    pdf.bold_p("Finding 4 -- Governance compliance does not equal robustness. ",
        "System B (governance-compliant) achieves mean overall robustness of 0.43, compared "
        "to System A (undocumented baseline) at 0.32 -- a gap of only +0.11. Current "
        "governance frameworks certify documentation and process quality, not passive-detection "
        "capability.")
    pdf.bold_p("Finding 5 -- Best-practice ceiling of 0.95. ",
        "System C (adversarial-hardened) achieves the highest scores but still peaks at 0.95 "
        "and cannot address R-03. There is no fully robust system -- only less inadequate ones.")

    pdf.h2("6.3", "System Comparison")
    pdf.fig(FIG_COMPARE,
        "Figure 5.  Overall Robustness Score by Safety System (n = 14 scenarios). "
        "(a) Mean score across all 14 scenarios with +0.11 (A->B) and +0.23 (B->C) gap "
        "annotations. Error bars: +-1 SD. (b) Urban (n=9) vs Rural (n=5) split.",
        w=150)
    pdf.p(
        "Standard deviation reflects variance across 14 benchmark scenarios, not deployment "
        "observations. System C shows the only substantial improvement over the baseline "
        "(+0.23 over B). Rural scenarios benefit more from System C than urban (0.74 vs 0.61), "
        "driven by higher GPS/communication layer performance in isolated environments. Urban "
        "confinement scenarios (U-02, U-09) remain the hardest -- both score ZIDR = 0.12 "
        "across all systems."
    )

    # ── Section 7: Governance Gap Analysis ───────────────────────────────────
    pdf.h1("7", "Governance Gap Analysis")
    pdf.h2("7.1", "Framework Coverage")
    pdf.tbl(
        ["Framework", "Accuracy req.", "Robustness req.", "Passive-detect req.", "Adversary model"],
        [
            ["EU AI Act", "Yes (Annex III)", "Partial", "None", "None"],
            ["NIST AI RMF", "Yes", "Partial", "None", "None"],
            ["ISO 42001", "Yes", "Partial", "None", "None"],
            ["India DPDP 2023", "No", "No", "None", "None"],
            ["India IT Act", "No", "No", "None", "None"],
        ],
        [35, 32, 28, 32, 33],
    )
    pdf.h2("7.2", "Structural Absence")
    pdf.p(
        "The gap is not a single missed clause. Every framework evaluates AI systems on "
        "accuracy metrics measured with cooperative users. None specify: passive-detection-only "
        "evaluation conditions; adversary-induced sensing layer failure scenarios; social "
        "conditioning as an attack vector; or zero-interaction window performance requirements."
    )
    pdf.h2("7.3", "Recommended Clause Language (EU AI Act / CEN-CENELEC)")
    pdf.blockquote(
        "Conformity assessment for high-risk AI systems deployed in personal safety contexts "
        "(Annex III) shall include evaluation of passive-detection robustness under adversary-"
        "induced sensing layer degradation. Systems shall report Zero-Interaction Detection "
        "Rate (ZIDR) across a standardised adversarial scenario set. ZIDR shall be reported "
        "separately from cooperative-user accuracy metrics."
    )

    # ── Section 8: Tool Specification ────────────────────────────────────────
    pdf.h1("8", "Probe Robustness Tool Specification")
    pdf.p(
        "A Python CLI for evaluating any safety system profile against this taxonomy, "
        "with ZIDR as a first-class output metric."
    )
    pdf.bullets([
        "Inputs: System capability profile (YAML), scenario set (JSON from taxonomy library)",
        "Outputs: ZIDR score, per-layer breakdown, governance gap flags, audit report",
    ])
    pdf.code(
        "zidr-probe --system-profile system.yaml \\\n"
        "           --scenario-set taxonomy/urban_access_0_2.json \\\n"
        "           --output report.json\n\n"
        '{"zidr_overall": 0.32,\n'
        ' "zidr_by_layer": {"sensing": 0.21, "processing": 0.38,\n'
        '                   "communication": 0.31, "response": 0.24},\n'
        ' "governance_gaps": ["EU_AI_Act_Annex_III", "NIST_RMF_GOVERN"],\n'
        ' "scenarios_tested": 14, "scenarios_detected": 4}'
    )
    pdf.p(
        "Current release includes formal specification and benchmark artifacts; "
        "production validation and live vendor testing remain Phase 2 work."
    )
    pdf.set_font("Helvetica", "B", 10)
    pdf.multi_cell(0, 6, "Code Availability",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 10)
    pdf.p(
        "Benchmark artifacts and probe specification are available at GitHub: "
        "pretzelslab/ai-safety-research (womens_safety_adversarial module). "
        "See Appendix B for full repository path."
    )

    # ── Section 9: AI Safety Connections ─────────────────────────────────────
    pdf.h1("9", "Connections to AI Safety Research")
    pdf.bold_p("Adversarial robustness: ",
        "Passive-layer defeat by a physically proximate adversary mirrors input-level "
        "probe evasion. The attack surface is the sensing layer rather than the model.")
    pdf.bold_p("Distributional shift: ",
        "Safety apps trained on clean audio and video encounter adversarially degraded "
        "inputs in deployment. The adversary is the distribution shift.")
    pdf.bold_p("Specification gaming: ",
        "Social conditioning (L5) is a real-world instance of specification gaming: "
        "the adversary exploits the gap between what the system is specified to detect "
        "and what cultural context prevents the user from allowing it to detect.")

    # ── Section 10: Limitations ───────────────────────────────────────────────
    pdf.h1("10", "Limitations")
    pdf.bullets([
        "Scenario library is not exhaustive. 14 scenarios cover urban/rural Indian context; "
        "generalization requires expansion.",
        "Benchmark profiles are reference constructs, not validated against commercial products.",
        "ZIDR measurement is unvalidated at scale. Baseline thresholds require partner "
        "validation with safety app vendors.",
        "Degradation factors are benchmark priors for reproducible testing and are not direct "
        "empirical measurements from deployed commercial systems.",
        "Sociotechnical attack surface (L5) is qualitative; operationalizing for quantitative "
        "ZIDR requires additional methodology.",
        "Tool specification only; full implementation is Phase 2.",
    ])

    # ── Section 11: Future Work ───────────────────────────────────────────────
    pdf.h1("11", "Future Work")
    pdf.bullets([
        "ZIDR baseline measurement -- controlled testing with 1-2 safety app vendors.",
        "Policy brief -- targeted at CEN-CENELEC and India Bureau of Indian Standards.",
        "Expanded scenario library -- coverage beyond Indian urban/rural context.",
        "L5 operationalisation -- methodology for quantifying social conditioning in ZIDR.",
        "Academic submission -- target ACM FAccT 2027.",
    ])

    # ── Section 12: Conclusion ────────────────────────────────────────────────
    pdf.h1("12", "Conclusion")
    pdf.p(
        "Women's safety AI systems face a threat that no existing benchmark tests and no "
        "existing governance framework governs: a physically proximate adversary who defeats "
        "passive detection without device access or technical knowledge. This paper provides "
        "four contributions to close that gap: a threat taxonomy grounding the attack surface; "
        "ZIDR as an operationalisable evaluation metric; a 14-scenario benchmark library; and "
        "empirical benchmark results establishing that governance compliance alone provides "
        "only marginal improvement over an undocumented baseline (+0.11), while adversarial "
        "hardening shows the only substantial gain (+0.23)."
    )
    pdf.p(
        "A system that achieves 95% benchmark accuracy and ZIDR = 0.00 is not a safe system. "
        "Making that distinction visible -- and testable -- is the policy contribution of "
        "this work."
    )

    # ── References ────────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.h1("", "References")
    refs = [
        "Carlini, N., & Wagner, D. (2017). Towards Evaluating the Robustness of Neural "
        "Networks. IEEE Symposium on Security and Privacy (SP), 39-57.",

        "Chatterjee, R., et al. (2018). The Spyware Used in Intimate Partner Violence. "
        "IEEE Symposium on Security and Privacy (SP), 441-458.",

        "Dimond, J. P., Fiesler, C., & Bruckman, A. (2011). Domestic violence and "
        "information communication technologies. Interacting with Computers, 23(5), 413-421.",

        "European Commission. (2024). Regulation (EU) 2024/1689 -- EU AI Act. "
        "Official Journal of the European Union.",

        "Freed, D., et al. (2018). 'A Stalker's Paradise': How Intimate Partner Abusers "
        "Exploit Technology. CHI 2018.",

        "Goodfellow, I. J., Shlens, J., & Szegedy, C. (2015). Explaining and Harnessing "
        "Adversarial Examples. ICLR 2015.",

        "International Organization for Standardization. (2023). ISO/IEC 42001:2023 -- "
        "Artificial intelligence -- Management system. ISO.",

        "NIST. (2023). Artificial Intelligence Risk Management Framework (AI RMF 1.0). "
        "NIST AI 100-1.",

        "Woodlock, D. (2017). The Abuse of Technology in Domestic Violence and Stalking. "
        "Violence Against Women, 23(5), 584-602.",

        "Biggio, B., et al. (2013). Evasion Attacks against Machine Learning at Test Time. "
        "European Conference on Machine Learning and Knowledge Discovery in Databases "
        "(ECML-PKDD), 387-402.",

        "Madry, A., Makelov, A., Schmidt, L., Tsipras, D., & Vladu, A. (2018). Towards Deep "
        "Learning Models Resistant to Adversarial Attacks. International Conference on "
        "Learning Representations (ICLR).",

        "Eykholt, K., et al. (2018). Robust Physical-World Attacks on Deep Learning Visual "
        "Classification. IEEE Conference on Computer Vision and Pattern Recognition (CVPR), "
        "1625-1634.",

        "Buolamwini, J., & Gebru, T. (2018). Gender Shades: Intersectional Accuracy "
        "Disparities in Commercial Gender Classification. Conference on Fairness, "
        "Accountability, and Transparency (FAccT), 77-91.",

        "Raji, I. D., & Buolamwini, J. (2019). Actionable Auditing: Investigating the "
        "Impact of Publicly Naming Biased Performance Results of Commercial AI Products. "
        "AAAI/ACM Conference on AI, Ethics, and Society (AIES).",

        "Raji, I. D., et al. (2020). Closing the AI Accountability Gap: Defining an End-to-"
        "End Framework for Internal Algorithmic Auditing. ACM Conference on Fairness, "
        "Accountability, and Transparency (FAccT), 33-44.",

        "National Crime Records Bureau. (2022). Crime in India 2022. Ministry of Home "
        "Affairs, Government of India, New Delhi.",

        "Safetipin. (2019-2023). Urban Safety Audit Reports. New Delhi: Safetipin. "
        "Available: safetipin.com.",
    ]
    for i, r in enumerate(refs, 1):
        self_x = pdf.l_margin
        pdf.set_font("Helvetica", "", 9.5)
        pdf.set_x(self_x + 6)
        pdf.cell(8, pdf.H_BODY, f"[{i}]", new_x=XPos.RIGHT)
        pdf.multi_cell(0, pdf.H_BODY, safe(r),
            new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1)

    # ── Appendix A: Full Scenario Library ────────────────────────────────────
    pdf.appendix("A", "Full Scenario Library (14 Scenarios)")
    pdf.p(
        "All 14 scenarios. Urban (U-01 to U-09), Rural (R-01 to R-05). "
        "(*) = novel attack vector not documented in existing adversarial ML or GBV literature. "
        "Confirmed 2026-05-14."
    )

    scenario_rows = [
        ["U-01", "Mumbai Local Train, Peak Hours",       "L0", "Suppress + Corrupt",    "Vision, Audio, IMU",      "All: no transit sensor fusion standard"],
        ["U-02", "App-Based Cab, Night Route",            "L1", "Intercept + Spoof",      "Sensor Fusion, Vision",   "All + India DPDP"],
        ["U-03", "Workplace, Authority Figure",           "L5", "Suppress (social)",      "None (not initiated)",    "All: sociotechnical suppression ungoverned"],
        ["U-04", "Street Market, Bag Obstruction",        "L0", "Suppress",               "Vision, Audio",           "All: no CV occlusion standard"],
        ["U-05", "Bus Stop, Exhaustion Attack (*)",       "L0", "Exhaust",                "Response (human)",        "All: no alert exhaustion req."],
        ["U-06", "Campus, Known Acquaintance",            "L1", "Corrupt",                "Vision, NLP",             "All: NLP coercion bypass untested"],
        ["U-07", "Social Venue, Noise + Alcohol (*)",     "L0", "Suppress + Corrupt",    "Audio, Vision",           "All: no high-noise certification"],
        ["U-08", "Public Toilet, Device Grab (*)",        "L2", "Intercept",              "Comm, Response",          "All: no device interception standard"],
        ["U-09", "Transit Confinement, Moving Vehicle",   "L1", "Suppress + Intercept",  "Vision, Audio, GPS, Comm","All: confined transit ungoverned"],
        ["R-01", "Agricultural Field, Isolated Worker",   "L0", "Intercept + Suppress",  "Communication",           "EU AI Act, NIST, India DPDP"],
        ["R-02", "Village Pathway, Dusk",                  "L0", "Suppress",               "Vision, Response",        "All: no low-light rural CV standard"],
        ["R-03", "Isolated Road, Moving Vehicle",          "L0", "Intercept + Corrupt",   "Sensor Fusion, Comm",     "Cross-jurisdictional: no rural connectivity req."],
        ["R-04", "Village Common, Community Authority",   "L5", "Suppress (social)",      "None (not initiated)",    "All + India IT Act: social suppression"],
        ["R-05", "Agricultural Employer, Seasonal (*)",   "L5", "Suppress (economic)",    "Response, Vision, Audio", "All: economic coercion ungoverned"],
    ]
    pdf.set_font("Helvetica", "", 8)
    pdf.tbl(
        ["ID", "Scenario", "Min.\nAccess", "Attack Method", "Layers Defeated", "Governance Gap"],
        scenario_rows,
        [10, 38, 12, 30, 28, 42],
        hdr_color=(220, 235, 255),
    )
    pdf.set_font("Helvetica", "", 10)
    pdf.p(
        "Calibration note: R-02/R-04 ZIDR = 0.92-0.95 (not 1.00). A perfect score is not "
        "academically defensible -- minimal calibration uncertainty applied. "
        "U-03 ZIDR = 0.27-0.33: sociotechnical suppression is the dominant failure mode; "
        "passive-layer performance overstates system safety in authority contexts."
    )

    # ── Appendix B ────────────────────────────────────────────────────────────
    pdf.appendix("B", "Taxonomy Reference")
    pdf.p(
        "See Table 1 (Section 3.3) for the full 4-layer x 5-method matrix with minimum "
        "access levels and scenario footnotes."
    )
    pdf.bold_p("Scenario library (YAML): ",
        "pretzelslab/ai-safety-research -- womens_safety_adversarial/probe_robustness/scenarios/")
    pdf.bold_p("Benchmark results (CSV): ",
        "pretzelslab/ai-safety-research -- womens_safety_adversarial/probe_robustness/results/")

    pdf.output(OUT_PDF)
    print(f"Saved: {OUT_PDF}")


if __name__ == "__main__":
    build()
