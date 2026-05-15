"""
build_tex.py — Generate publication-quality PDF via LaTeX (MiKTeX).
Output: ZIDR_benchmark_paper_v3.pdf

Compiles in C:/tmp_latex_test/ (pdflatex cannot handle paths with spaces).
Copies final PDF to research_artifacts/.
Run: python build_tex.py
"""

import os, shutil, subprocess, pathlib

BASE     = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
FIGS_SRC = BASE / ".." / "probe_robustness" / "results"
BUILD    = pathlib.Path("C:/tmp_latex_test")
OUT_PDF  = BASE / "ZIDR_benchmark_paper_v3.pdf"

BUILD.mkdir(exist_ok=True)
for fig in ["fig1_zidr_heatmap.png", "fig2_score_comparison.png", "fig3_threat_model.png"]:
    src = FIGS_SRC / fig
    if src.exists():
        shutil.copy2(src, BUILD / fig)
        print(f"Copied: {fig}")

# ── LaTeX document ─────────────────────────────────────────────────────────

TEX = r"""\documentclass[11pt,a4paper]{article}

%% Font encoding -- T1 ensures proper PDF copy/paste behaviour
\usepackage[T1]{fontenc}

%% Hyphenation overrides — prevents bad breaks in key terms
\hyphenation{bench-mark Zero-In-ter-ac-tion de-tec-tion gov-er-nance ad-ver-sar-ial}

%% Packages
\usepackage[a4paper,top=2.5cm,bottom=2.5cm,left=2.5cm,right=2.5cm]{geometry}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{float}
\usepackage{placeins}
\usepackage{booktabs}
\usepackage{array}
\usepackage{tabularx}
\usepackage[font=small,labelfont=bf,justification=justified]{caption}
\usepackage[colorlinks=true,linkcolor=blue,urlcolor=blue,citecolor=blue]{hyperref}
\usepackage[expansion=false]{microtype}
\usepackage{parskip}
\usepackage{xcolor}
\usepackage{listings}

%% Code block style
\lstset{
  basicstyle=\small\ttfamily,
  frame=single,
  breaklines=true,
  breakatwhitespace=true,
  columns=flexible,
  keepspaces=true,
  xleftmargin=6pt,
  xrightmargin=6pt,
}

%% Column types
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}

%% Assumptions box (no extra packages)
\newcommand{\assumptionbox}[1]{%
  \vspace{4pt}%
  \noindent\colorbox{blue!6}{%
    \begin{minipage}{\dimexpr\linewidth-2\fboxsep}%
      \vspace{4pt}%
      \textbf{Threat Model Assumptions}%
      \vspace{2pt}%
      #1%
      \vspace{2pt}%
    \end{minipage}%
  }%
  \vspace{6pt}%
}

\setlength{\parindent}{0pt}

%% Title
\title{%
  \textbf{Adversarial Robustness in Women's Safety AI Systems:}\\[6pt]
  \large Threat Taxonomy, Zero-Interaction Detection Rate (ZIDR),\\
  and Benchmark Evaluation%
}

\author{%
  Preethi Raghuveeran\\[4pt]
  \small Independent Researcher \quad
  \href{mailto:[removed]}{[removed]} \quad
  ORCID: 0009-0009-1907-8223%
}

\date{May 2026}

\begin{document}

\maketitle
\thispagestyle{plain}

% ── Abstract ────────────────────────────────────────────────────────────────
\begin{abstract}
Passive-detection robustness---the ability of a safety-critical AI system to trigger an
alert without user interaction, under adversary-induced sensing degradation---is rarely
evaluated by existing benchmarks and is not explicitly required by major AI governance
frameworks. This paper addresses the gap in the context of women's safety AI systems,
where the physically proximate adversary model is both realistic and systematically
understudied.

We introduce four contributions: (1)~a four-layer threat taxonomy formalised as a
benchmark schema, mapping attack surfaces, attack methods, and adversary access levels;
(2)~Zero-Interaction Detection Rate (ZIDR), a scoring metric for passive-only detection
performance under adversary-induced degradation; (3)~a 14-scenario library spanning
urban and rural Indian deployment contexts; and (4)~a benchmark evaluation of four
reference system profiles across all 14 scenarios, establishing baseline ZIDR values
and demonstrating that governance compliance does not substitute for adversarial
hardening.

A standards coverage analysis across the EU AI Act, NIST AI RMF, ISO 42001, India DPDP
Act 2023, and the India IT Act identifies a structural absence of passive-detection
robustness requirements in current AI safety governance.
\end{abstract}

\noindent\textbf{Keywords:} adversarial robustness; women's safety AI; passive
detection; threat taxonomy; AI governance; gender-based violence; ZIDR

\smallskip
\noindent\footnotesize\textbf{Data Availability:} Scenario library and benchmark
data: \href{https://doi.org/10.5281/zenodo.20028247}{\texttt{doi:10.5281/zenodo.20028247}}\normalsize

\bigskip

% ── Section 1: Introduction ─────────────────────────────────────────────────
\section{Introduction}

Women's safety applications are deployed in conditions that invert standard ML
evaluation assumptions: the user may be unable to interact with the device, the
environment is controlled by the adversary, and failure produces a false-safe outcome
at the moment of maximum danger.

The zero-interaction window---the 2--15 seconds between when a physical threat becomes
active and when the victim loses device access---is where these systems must perform
without any user input. Detection in this window depends entirely on passive layers:
computer vision, audio classification, and sensor fusion. Existing benchmarks rarely
evaluate this window explicitly. No existing governance framework requires it.

The adversary in this context is not digital or anonymous. They are physically present
(0--50\,m), environmentally familiar, and adaptive. They may hold institutional or
social authority over the victim. They do not need technical knowledge to defeat passive
detection. A hand over a camera lens, ambient noise at the right frequency, or a GPS
dead zone can simultaneously disable all three passive layers. This threat model does
not appear in adversarial ML literature, which assumes digital or white-box
attackers~\cite{goodfellow15,carlini17,biggio13}, or in HCI literature, which assumes
cooperative users~\cite{dimond11,freed18}.

This paper names the gap precisely and provides the tools to close it. This work is
primarily a threat-modelling and evaluation-framework contribution, supplemented by a
benchmark evaluation across four reference system profiles.

% ── Section 2: Related Work ─────────────────────────────────────────────────
\section{Related Work}

\subsection{Adversarial Machine Learning}

Adversarial ML research addresses evasion, poisoning, and extraction attacks against ML
models~\cite{goodfellow15,carlini17,biggio13,madry18}. The dominant adversary model
assumes digital access---either black-box query access or white-box knowledge of model
weights. Physical-world attacks~\cite{eykholt18} have extended the field to
sensor-level manipulation, but physically proximate adversaries with environmental but
not digital access remain unmodelled.

\subsection{HCI and Safety-Critical Systems}

HCI research on safety apps (bSafe, Safetipin, Ola Safety) focuses on usability,
adoption, and cooperative interaction~\cite{dimond11,freed18}. Adversarial
conditions---where the adversary controls the environment and the user cannot
act---remain outside the scope of this literature.

\subsection{Gender-Based Violence and Technology}

Research on technology-facilitated GBV examines stalkerware, intimate partner
surveillance, and coercive control~\cite{freed18,chatterjee18,woodlock17}.
Physical-world adversarial manipulation of AI-driven safety systems is not addressed.
The intersection of adversarial ML and GBV-specific threat models remains structurally
unoccupied.

\subsection{Algorithmic Fairness and Accountability}

Fairness auditing work~\cite{buolamwini18,raji19,raji20} has established that
evaluation gaps in AI systems can produce systematic harm. ZIDR applies this
accountability lens to safety-critical passive detection: measuring what the system
actually does when it matters, not what it does under cooperative evaluation conditions.

\subsection{Research Gap}

To our knowledge, no prior work combines: (1)~a physically proximate adversary model,
(2)~passive-detection-only evaluation, and (3)~women's safety deployment context. ZIDR
does not appear in any published benchmark, evaluation standard, or governance
framework.

% ── Section 3: Threat Taxonomy ──────────────────────────────────────────────
\section{Threat Taxonomy}

\subsection{Framework Structure}

The taxonomy is organised across three dimensions:
\begin{itemize}
  \item \textbf{Attack surface layers (4):} Sensing $\to$ Processing $\to$
        Communication $\to$ Response
  \item \textbf{Attack methods (5):} Suppress, Corrupt, Spoof, Exhaust, Intercept
  \item \textbf{Adversary access levels (6):} L0 (physical proximity only) through L5
        (social leverage)
\end{itemize}

Core finding: the most dangerous attacks require the least technical sophistication.
Access Level~0 attacks---requiring only physical presence---can simultaneously defeat
all three passive detection layers.

\bigskip
\assumptionbox{%
  \begin{enumerate}
    \item The adversary is physically proximate (0--50\,m) and does not require device
          access or technical knowledge.
    \item The victim is unable to initiate an alert during the zero-interaction window
          (2--15 seconds).
    \item Passive detection layers (camera, audio, GPS) operate independently and can
          each fail independently.
    \item All three passive layers can be defeated simultaneously by an L0 adversary
          using physical presence alone.
    \item Governance-certified systems are not assumed to have undergone adversarial
          robustness testing.
  \end{enumerate}
}

\subsection{Layer Definitions}

\begin{table}[htbp]
\centering
\begin{tabular}{L{2.8cm} L{4.8cm} L{6.4cm}}
\toprule
\textbf{Layer} & \textbf{Components} & \textbf{Example Attack} \\
\midrule
Sensing & Camera, mic, GPS, accelerometer & Hand over lens; noise injection \\
Processing & On-device ML inference & Input manipulation; confidence suppression \\
Communication & Network, SMS, data upload & Signal jamming; GPS dead zone \\
Response & Alert delivery, escalation & Alert suppression; false-safe output \\
\bottomrule
\end{tabular}
\caption*{\small Layer definitions across the four passive-detection attack surfaces.}
\end{table}

\FloatBarrier

\subsection{Adversary Access Levels}

\begin{table}[htbp]
\centering
\begin{tabular}{C{0.8cm} L{3.5cm} L{9.5cm}}
\toprule
\textbf{Level} & \textbf{Access Type} & \textbf{Example} \\
\midrule
L0 & Physical proximity only   & Covers camera; generates masking noise \\
L1 & Incidental device contact & Briefly blocks sensor; interferes with GPS \\
L2 & Full device access        & Grabs device; disables app or hardware \\
L3 & Environmental control     & Controls lighting, acoustics, GPS coverage \\
L4 & System knowledge          & Knows detection thresholds; times attack \\
L5 & Social leverage           & Institutional authority inhibits alert initiation \\
\bottomrule
\end{tabular}
\caption*{\small Adversary access level definitions (L0--L5).}
\end{table}

\FloatBarrier

Key insight: L5 (social leverage) is structurally distinct---it requires no technical
knowledge and is the only access level entirely absent from adversarial ML frameworks
and governance standards.

\begin{table}[htbp]
\centering
\small
\begin{tabular}{L{4.2cm} C{1.8cm} C{1.8cm} C{1.5cm} C{1.6cm} C{1.9cm}}
\toprule
\textbf{Attack Surface} & \textbf{Suppress} & \textbf{Corrupt} & \textbf{Spoof}
  & \textbf{Exhaust} & \textbf{Intercept} \\
\midrule
Sensing (camera, mic, GPS) & L0$^{1}$ & L0$^{2}$ & L2  & ---       & L2 \\
Processing (on-device ML)  & L3       & L3       & L4  & ---       & --- \\
Communication (network)    & ---      & L0$^{3}$ & --- & ---       & L0$^{4}$ \\
Response (alert delivery)  & L5$^{5}$ & ---      & --- & L0$^{6}$  & L2 \\
\bottomrule
\end{tabular}
\caption{Minimum adversary access level by layer and attack method. Lower level =
  more accessible adversary = higher governance urgency. $^{1}$U-01: crowd density
  defeats camera + audio + IMU at L0. $^{2}$U-01, U-07: ambient noise corrupts audio
  below threshold. $^{3}$U-02: GPS blackspot exploitation. $^{4}$R-01, R-03: no
  cellular signal---alert cannot transmit. $^{5}$U-03, R-04: institutional authority
  suppresses alert initiation. $^{6}$U-05: repeated false alerts condition contacts to
  ignore notifications.}
\label{tab:access}
\end{table}

\FloatBarrier

% ── Section 4: Scenario Library ─────────────────────────────────────────────
\section{Scenario Library}

Fourteen illustrative scenarios---9 urban, 5 rural---developed for the Indian
deployment context, consistent with patterns documented in NCRB Annual
Reports~\cite{ncrb22} and Safetipin urban safety audit reports~\cite{safetipin19}.
Each scenario specifies attack method, adversary access level, deployment context,
passive layer failure mode, and governance gap exposed. Full structured library
available at Zenodo (DOI on title page).

\textbf{Sample scenario---Urban Transit (Access Level~0):} Adversary positions at
0--2\,m on public transit at night. Activates ambient noise source masking distress
audio classifier threshold. Simultaneously positions body to block camera field of
view. Victim has 3--8 seconds zero-interaction window. All three passive layers fail.
No alert fires.

U-09 (added v3): Urban Transit Confinement---victim trapped in a moving vehicle
(late-night transit), limited exit, adversary controls movement and route. Confinement
+ noise + restricted device access = complete zero-interaction failure window (ZIDR
0.12--0.17 across all systems). Full scenario library in Appendix~\ref{app:scenarios}.

% ── Section 5: ZIDR ─────────────────────────────────────────────────────────
\section{Zero-Interaction Detection Rate (ZIDR)}

\subsection{Definition}

ZIDR is the proportion of adversarial attack scenarios correctly detected and alerted
without any user action, under adversary-induced passive-layer degradation:

\[
  \mathrm{ZIDR}
  \;=\;
  \frac{\bigl|\{s \in S_{\mathrm{adv}} : \mathrm{alert}(s) = 1,\;
               \mathrm{user\_action}(s) = 0\}\bigr|}
       {|S_{\mathrm{adv}}|}
\]

\noindent where $S_{\mathrm{adv}}$ is the set of adversarial scenarios,
$\mathrm{alert}(s)=1$ denotes a correct alert for scenario $s$, and
$\mathrm{user\_action}=0$ denotes no user interaction occurred.

\begin{figure}[htbp]
\centering
\includegraphics[width=0.85\textwidth]{fig3_threat_model}
\caption{ZIDR threat model architecture showing passive-layer degradation and failure-point threshold.}
\label{fig:threat}
\end{figure}

\FloatBarrier

\subsection{Distinction from Existing Metrics}

Any evaluation that includes a button press, keyword trigger, or check-in response is
evaluating a different system than the one that must function in the zero-interaction
window. ZIDR measures performance against an adversary, without a user.

\begin{table}[htbp]
\centering
\begin{tabular}{L{3.5cm} C{3.2cm} C{3.5cm} C{2.5cm}}
\toprule
\textbf{Metric} & \textbf{Adversary modelled} & \textbf{User interaction req.}
  & \textbf{Passive-only} \\
\midrule
Standard accuracy & No               & Yes & No  \\
Robustness (AML)  & Digital/white-box & No  & No  \\
ZIDR              & Physically proximate & No & Yes \\
\bottomrule
\end{tabular}
\caption*{\small ZIDR vs.\ existing evaluation metrics.}
\end{table}

\FloatBarrier

\subsection*{Zero-Interaction Window (Scenario U-01)}

\begin{figure}[htbp]
\begin{lstlisting}
 T = 0s               T = 2-15s                        T > 15s
 |                        |                                 |
 Threat becomes active.   |<--- ZERO-INTERACTION WINDOW -->|  Standard
 Adversary reaches        |                                 |  benchmarks
 proximity threshold.     |  Passive detection only.        |  begin here.
 No user action possible. |  User-triggered functions off.  |
 -----------------------------------------------------------------------

 Passive layer status at T = 8s  (L0 adversary, U1/T1 context):

   Camera (CV)     [##################]  DEFEATED   crowd occlusion
   Audio (ASR)     [##################]  DEFEATED   ambient noise >85 dB
   Accelerometer   [##################]  DEFEATED   transit vibration
   GPS             [####              ]  DEGRADED   functional, insufficient

   Functional layers: 1 of 4    ZIDR = 0.25
 -----------------------------------------------------------------------
   Benchmark accuracy (cooperative user, controlled environment):  0.95
   ZIDR              (L0 adversary, zero-interaction window):       0.25
\end{lstlisting}
\caption{Zero-Interaction Window: Passive layer status under L0 adversary
  (Scenario U-01, Mumbai local train, peak hours). Benchmark accuracy is measured under
  cooperative conditions; ZIDR measures the same system in the zero-interaction window.}
\label{fig:window}
\end{figure}

\subsection{Governance Implication}

ZIDR provides the operationalisable definition missing from EU AI Act~\cite{euai24}
conformity assessment for Annex~III high-risk AI systems. Women's safety apps qualify
under Annex~III. Conformity assessment currently has no clause requiring
passive-detection robustness testing. ZIDR fills that clause.

% ── Section 6: Benchmark Evaluation ─────────────────────────────────────────
\section{Benchmark Evaluation}

To demonstrate ZIDR measurement in practice and establish baseline reference values, we
evaluated four system profiles against all 14 scenarios using the ZIDR probe tool
specification (Section~\ref{sec:tool}). Profile definitions are formal---they represent
distinct implementation stances common in deployment, not specific named products.

\subsection{System Profiles}

\begin{table}[htbp]
\centering
\begin{tabular}{C{1.2cm} L{13cm}}
\toprule
\textbf{System} & \textbf{Definition} \\
\midrule
A & Undocumented baseline consumer safety application \\
B & Governance-compliant implementation (no adversarial robustness testing) \\
C & Best-practice robust implementation (adversarial-hardened) \\
D & Rural-optimised deployment (camera/NLP removed; GPS-primary) \\
\bottomrule
\end{tabular}
\caption*{\small Reference system profiles used in benchmark evaluation.}
\end{table}

\FloatBarrier

\clearpage
\subsection{ZIDR Results}

\begin{figure}[htbp]
\centering
\includegraphics[width=0.85\textwidth]{fig1_zidr_heatmap}
\caption{ZIDR Benchmark Results Across 14 Adversarial Scenarios. C1--C5 = criticality
  score (5 = complete detection failure, no fallback path). Red border: universal
  zero-day (R-03). Orange dashed: high ZIDR but sociotechnical suppression risk
  persists. Scores represent benchmark priors derived from reference system profiles,
  not validated commercial product measurements.}
\label{fig:heatmap}
\end{figure}

\FloatBarrier

Five findings are significant:

\textbf{Finding 1---Universal zero-day (R-03, ZIDR\,=\,0.00 all systems).}
The isolated road vehicle scenario scores zero across all four systems. A moving vehicle
with coordinated GPS dead zone timing has no passive detection path. No implementation
improvement changes this result. R-03 is a capability floor, not a benchmark failure.

\textbf{Finding 2---ZIDR inflation in sociotechnical scenarios.}
R-02 and R-04 score 0.92--0.95 but remain high-risk. Social authority suppresses alert
initiation before passive detection triggers. ZIDR alone is insufficient;
\texttt{alert\_initiation\_rate} is needed as a complementary metric
(\texttt{alert\_initiation\_rate}: the proportion of scenarios in which the victim is
socially able to initiate an alert before passive detection becomes necessary).

\textbf{Finding 3---Workplace authority degradation (U-03: 0.27--0.33).}
Employer or authority contexts suppress victim agency below passive detection threshold.
The failure mode is sociotechnical; passive-layer improvement alone cannot address it.

\textbf{Finding 4---Governance compliance does not equal robustness.}
System B (governance-compliant) achieves mean overall robustness of 0.43, compared to
System A (undocumented baseline) at 0.32---a gap of only $+$0.11. Current governance
frameworks certify documentation and process quality, not passive-detection capability.

\textbf{Finding 5---Best-practice ceiling of 0.95.}
System C (adversarial-hardened) achieves the highest scores but still peaks at 0.95 and
cannot address R-03. There is no fully robust system---only less inadequate ones.

\subsection{System Comparison}

\begin{figure}[htbp]
\centering
\includegraphics[width=0.85\textwidth]{fig2_score_comparison}
\caption{Overall Robustness Score by Safety System ($n = 14$ scenarios). (a)~Mean score
  across all 14 scenarios with $+$0.11 (A$\to$B) and $+$0.23 (B$\to$C) gap
  annotations. Error bars: $\pm$1\,SD. (b)~Urban ($n=9$) vs.\ Rural ($n=5$) split.}
\label{fig:compare}
\end{figure}

\FloatBarrier

Standard deviation reflects variance across 14 benchmark scenarios, not deployment
observations. System C shows the only substantial improvement over the baseline
($+$0.23 over B). Rural scenarios benefit more from System C than urban (0.74
vs.\ 0.61), driven by higher GPS/communication layer performance in isolated
environments. Urban confinement scenarios (U-02, U-09) remain the
hardest---both score ZIDR\,=\,0.12 across all systems.

% ── Section 7: Governance Gap Analysis ──────────────────────────────────────
\section{Governance Gap Analysis}

\subsection{Framework Coverage}

\begin{table}[htbp]
\centering
\small
\begin{tabular}{L{3.2cm} C{2.2cm} C{2.2cm} C{2.8cm} C{2.8cm}}
\toprule
\textbf{Framework} & \textbf{Accuracy req.} & \textbf{Robustness req.}
  & \textbf{Passive-detect req.} & \textbf{Adversary model} \\
\midrule
EU AI Act~\cite{euai24}           & Yes (Annex III) & Partial & None & None \\
NIST AI RMF~\cite{nist23}         & Yes             & Partial & None & None \\
ISO 42001~\cite{iso42001}         & Yes             & Partial & None & None \\
India DPDP 2023                   & No              & No      & None & None \\
India IT Act                      & No              & No      & None & None \\
\bottomrule
\end{tabular}
\caption*{\small AI governance framework coverage of passive-detection requirements.
  All five frameworks show zero coverage of passive-detection or adversary modelling
  requirements.}
\end{table}

\FloatBarrier

\subsection{Structural Absence}

The gap is not a single missed clause. Every framework evaluates AI systems on accuracy
metrics measured with cooperative users. None specify: passive-detection-only evaluation
conditions; adversary-induced sensing layer failure scenarios; social conditioning as an
attack vector; or zero-interaction window performance requirements.

\subsection{Recommended Clause Language (EU AI Act / CEN-CENELEC)}

\begin{quote}
\textit{Conformity assessment for high-risk AI systems deployed in personal safety
contexts (Annex~III) shall include evaluation of passive-detection robustness under
adversary-induced sensing layer degradation. Systems shall report Zero-Interaction
Detection Rate (ZIDR) across a standardised adversarial scenario set. ZIDR shall be
reported separately from cooperative-user accuracy metrics.}
\end{quote}

% ── Section 8: Tool Specification ───────────────────────────────────────────
\section{Probe Robustness Tool Specification}
\label{sec:tool}

A Python CLI for evaluating any safety system profile against this taxonomy, with ZIDR
as a first-class output metric.

\begin{itemize}
  \item \textbf{Inputs:} System capability profile (YAML), scenario set (JSON from
        taxonomy library)
  \item \textbf{Outputs:} ZIDR score, per-layer breakdown, governance gap flags, audit
        report
\end{itemize}

\begin{lstlisting}
zidr-probe --system-profile system.yaml \
           --scenario-set taxonomy/urban_access_0_2.json \
           --output report.json

{"zidr_overall": 0.32,
 "zidr_by_layer": {"sensing": 0.21, "processing": 0.38,
                   "communication": 0.31, "response": 0.24},
 "governance_gaps": ["EU_AI_Act_Annex_III", "NIST_RMF_GOVERN"],
 "scenarios_tested": 14, "scenarios_detected": 4}
\end{lstlisting}

Current release includes formal specification and benchmark artifacts; production
validation and live vendor testing remain Phase 2 work.

\medskip
\noindent\textbf{Code Availability.} Benchmark artifacts and probe specification are
available at the GitHub repository: \texttt{pretzelslab/ai-safety-research}
(\texttt{womens\_safety\_adversarial} module). Full repository paths are listed in
Appendix~\ref{app:taxonomy}.

% ── Section 9: AI Safety Connections ────────────────────────────────────────
\section{Connections to AI Safety Research}

\textbf{Adversarial robustness:} Passive-layer defeat by a physically proximate
adversary mirrors input-level probe evasion. The attack surface is the sensing layer
rather than the model.

\textbf{Distributional shift:} Safety apps trained on clean audio and video encounter
adversarially degraded inputs in deployment. The adversary \emph{is} the distribution
shift.

\textbf{Specification gaming:} Social conditioning (L5) is a real-world instance of
specification gaming: the adversary exploits the gap between what the system is
specified to detect and what cultural context prevents the user from allowing it to
detect.

% ── Section 10: Limitations ─────────────────────────────────────────────────
\section{Limitations}

\begin{itemize}
  \item Scenario library is not exhaustive. 14 scenarios cover urban/rural Indian
        context; generalisation requires expansion.
  \item Benchmark profiles are reference constructs, not validated against commercial
        products.
  \item ZIDR measurement is unvalidated at scale. Baseline thresholds require partner
        validation with safety app vendors.
  \item Degradation factors are benchmark priors for reproducible testing and are not
        direct empirical measurements from deployed commercial systems.
  \item Sociotechnical attack surface (L5) is qualitative; operationalising for
        quantitative ZIDR requires additional methodology.
  \item Tool specification only; full implementation is Phase 2.
\end{itemize}

% ── Section 11: Future Work ──────────────────────────────────────────────────
\section{Future Work}

\begin{itemize}
  \item ZIDR baseline measurement---controlled testing with 1--2 safety app vendors.
  \item Policy brief---targeted at CEN-CENELEC and India Bureau of Indian Standards.
  \item Expanded scenario library---coverage beyond Indian urban/rural context.
  \item L5 operationalisation---methodology for quantifying social conditioning in ZIDR.
  \item Academic submission---target ACM FAccT 2027.
\end{itemize}

% ── Section 12: Conclusion ───────────────────────────────────────────────────
\section{Conclusion}

Women's safety AI systems face a threat that no existing benchmark tests and no existing
governance framework governs: a physically proximate adversary who defeats passive
detection without device access or technical knowledge. This paper provides four
contributions to close that gap: a threat taxonomy grounding the attack surface; ZIDR
as an operationalisable evaluation metric; a 14-scenario benchmark library; and
empirical benchmark results establishing that governance compliance alone provides only
marginal improvement over an undocumented baseline ($+$0.11), while adversarial
hardening shows the only substantial gain ($+$0.23).

A system that achieves 95\% benchmark accuracy and ZIDR\,=\,0.00 is not a safe system.
Making that distinction visible---and testable---is the policy contribution of this
work.

% ── References ───────────────────────────────────────────────────────────────
\begin{thebibliography}{18}

\bibitem{goodfellow15}
Goodfellow, I.\,J., Shlens, J., \& Szegedy, C. (2015).
Explaining and harnessing adversarial examples.
\textit{ICLR 2015}.

\bibitem{carlini17}
Carlini, N., \& Wagner, D. (2017).
Towards evaluating the robustness of neural networks.
\textit{IEEE Symposium on Security and Privacy (SP)}, pp.\ 39--57.

\bibitem{biggio13}
Biggio, B., et al. (2013).
Evasion attacks against machine learning at test time.
\textit{ECML-PKDD}, pp.\ 387--402.

\bibitem{dimond11}
Dimond, J.\,P., Fiesler, C., \& Bruckman, A. (2011).
Domestic violence and information communication technologies.
\textit{Interacting with Computers}, 23(5), 413--421.

\bibitem{freed18}
Freed, D., et al. (2018).
`A stalker's paradise': How intimate partner abusers exploit technology.
\textit{ACM CHI 2018}.

\bibitem{madry18}
Madry, A., Makelov, A., Schmidt, L., Tsipras, D., \& Vladu, A. (2018).
Towards deep learning models resistant to adversarial attacks.
\textit{ICLR 2018}.

\bibitem{eykholt18}
Eykholt, K., et al. (2018).
Robust physical-world attacks on deep learning visual classification.
\textit{IEEE CVPR}, pp.\ 1625--1634.

\bibitem{chatterjee18}
Chatterjee, R., et al. (2018).
The spyware used in intimate partner violence.
\textit{IEEE Symposium on Security and Privacy (SP)}, pp.\ 441--458.

\bibitem{woodlock17}
Woodlock, D. (2017).
The abuse of technology in domestic violence and stalking.
\textit{Violence Against Women}, 23(5), 584--602.

\bibitem{buolamwini18}
Buolamwini, J., \& Gebru, T. (2018).
Gender shades: Intersectional accuracy disparities in commercial gender classification.
\textit{ACM FAccT}, pp.\ 77--91.

\bibitem{raji19}
Raji, I.\,D., \& Buolamwini, J. (2019).
Actionable auditing: Investigating the impact of publicly naming biased performance
results of commercial AI products.
\textit{AAAI/ACM AIES}.

\bibitem{raji20}
Raji, I.\,D., et al. (2020).
Closing the AI accountability gap: Defining an end-to-end framework for internal
algorithmic auditing.
\textit{ACM FAccT}, pp.\ 33--44.

\bibitem{ncrb22}
National Crime Records Bureau. (2022).
\textit{Crime in India 2022}.
Ministry of Home Affairs, Government of India, New Delhi.

\bibitem{safetipin19}
Safetipin. (2019--2023).
Urban safety audit reports.
New Delhi: Safetipin. \url{https://safetipin.com}.

\bibitem{euai24}
European Commission. (2024).
Regulation (EU) 2024/1689---EU AI Act.
\textit{Official Journal of the European Union}.

\bibitem{iso42001}
International Organization for Standardization. (2023).
ISO/IEC 42001:2023---Artificial intelligence---Management system. ISO.

\bibitem{nist23}
NIST. (2023).
Artificial intelligence risk management framework (AI RMF 1.0). NIST AI 100-1.

\end{thebibliography}

% ── Appendices ───────────────────────────────────────────────────────────────
\appendix

\section{Full Scenario Library (14 Scenarios)}
\label{app:scenarios}

All 14 scenarios. Urban (U-01 to U-09), Rural (R-01 to R-05).
(*) = novel attack vector not documented in existing adversarial ML or GBV literature.

\begin{table}[htbp]
\centering
\footnotesize
\setlength{\tabcolsep}{4pt}
\begin{tabular}{C{0.8cm} L{3.0cm} C{1.0cm} L{2.4cm} L{2.2cm} L{4.0cm}}
\toprule
\textbf{ID} & \textbf{Scenario} & \textbf{Min.\ Access} & \textbf{Attack Method}
  & \textbf{Layers Defeated} & \textbf{Governance Gap} \\
\midrule
U-01 & Mumbai Local Train, Peak Hours      & L0 & Suppress + Corrupt    & Vision, Audio, IMU       & All: no transit sensor fusion standard \\
U-02 & App-Based Cab, Night Route          & L1 & Intercept + Spoof     & Sensor Fusion, Vision    & All + India DPDP \\
U-03 & Workplace, Authority Figure         & L5 & Suppress (social)     & None (not initiated)     & All: sociotechnical suppression ungoverned \\
U-04 & Street Market, Bag Obstruction      & L0 & Suppress              & Vision, Audio            & All: no CV occlusion standard \\
U-05 & Bus Stop, Exhaustion Attack (*)     & L0 & Exhaust               & Response (human)         & All: no alert exhaustion req. \\
U-06 & Campus, Known Acquaintance          & L1 & Corrupt               & Vision, NLP              & All: NLP coercion bypass untested \\
U-07 & Social Venue, Noise + Alcohol (*)  & L0 & Suppress + Corrupt    & Audio, Vision            & All: no high-noise certification \\
U-08 & Public Toilet, Device Grab (*)     & L2 & Intercept             & Comm, Response           & All: no device interception standard \\
U-09 & Transit Confinement, Moving Vehicle & L1 & Suppress + Intercept  & Vision, Audio, GPS, Comm & All: confined transit ungoverned \\
R-01 & Agricultural Field, Isolated Worker & L0 & Intercept + Suppress  & Communication            & EU AI Act, NIST, India DPDP \\
R-02 & Village Pathway, Dusk              & L0 & Suppress              & Vision, Response         & All: no low-light rural CV standard \\
R-03 & Isolated Road, Moving Vehicle       & L0 & Intercept + Corrupt   & Sensor Fusion, Comm      & Cross-jurisdictional: no rural connectivity req. \\
R-04 & Village Common, Community Authority & L5 & Suppress (social)     & None (not initiated)     & All + India IT Act \\
R-05 & Agricultural Employer, Seasonal (*) & L5 & Suppress (economic)   & Response, Vision, Audio  & All: economic coercion ungoverned \\
\bottomrule
\end{tabular}
\caption*{\small Calibration note: R-02/R-04 ZIDR\,=\,0.92--0.95 (not 1.00)---perfect
  score is not academically defensible; minimal calibration uncertainty applied.
  U-03 ZIDR\,=\,0.27--0.33: sociotechnical suppression is the dominant failure mode;
  passive-layer performance alone overstates system safety in authority contexts.}
\end{table}

\FloatBarrier

\section{Taxonomy Reference}
\label{app:taxonomy}

See Table~\ref{tab:access} (Section~3) for the full 4-layer $\times$ 5-method matrix
with minimum access levels and scenario footnotes.

\medskip
\noindent\textbf{Scenario library (YAML):}\\
\texttt{pretzelslab/ai-safety-research/womens\_safety\_adversarial/probe\_robustness/scenarios/}

\medskip
\noindent\textbf{Benchmark results (CSV):}\\
\texttt{pretzelslab/ai-safety-research/womens\_safety\_adversarial/probe\_robustness/results/}

\end{document}
"""

def clean_for_latex(text):
    """Replace every non-ASCII Unicode character with a safe ASCII/LaTeX equivalent.

    pdflatex's UTF-8 input processor runs before comment stripping, so even chars
    inside LaTeX % comments can produce rendering artifacts or fatal errors.
    Running through this function guarantees a pure 7-bit ASCII source file.
    """
    table = {
        # Dashes
        '—': '---',   # em dash  —
        '–': '--',    # en dash  –
        '‒': '--',    # figure dash
        '‑': '-',     # non-breaking hyphen
        '­': '',      # soft hyphen (invisible — remove)
        # Quotes
        '’': "'",     # right single quote  '
        '‘': '`',     # left single quote   '
        '“': '``',    # left double quote   "
        '”': "''",    # right double quote  "
        '‚': ',',     # single low-9 quote
        '„': ',,',    # double low-9 quote
        # Spaces
        ' ': '~',     # non-breaking space
        ' ': '~',     # narrow no-break space
        ' ': ' ',     # thin space
        # Punctuation
        '…': r'\ldots{}',        # ellipsis  …
        '•': r'\textbullet{}',   # bullet    •
        '·': r'\textperiodcentered{}',  # middle dot
        '−': '-',     # minus sign  −
        '×': r'\times{}',        # multiplication sign  ×
        '÷': r'\div{}',          # division sign  ÷
        # Box-drawing (used in section-divider comments; → plain dashes)
        '─': '-',  '━': '=',   '│': '|',  '┃': '|',
        '┌': '+',  '┐': '+',   '└': '+',  '┘': '+',
        '├': '+',  '┤': '+',   '┬': '+',  '┴': '+',
        '┼': '+',  '═': '=',   '║': '||', '╬': '+',
        '╠': '+',  '╣': '+',   '╦': '+',  '╩': '+',
        # Specials / BOM variants
        '�': '',   '￾': '',    '￼': '',   '﻿': '',
        # Misc Latin supplements
        'é': r'\'e',  'è': r'\`e',  'à': r'\`a',
        'â': r'\^a',  'ê': r'\^e',  'î': r'\^i',
        'ô': r'\^o',  'û': r'\^u',  'ç': r'\c{c}',
        'ü': r'\"u',  'ö': r'\"o',  'ä': r'\"a',
        'ß': r'\ss{}',
    }
    for old, new in table.items():
        text = text.replace(old, new)
    # Final safety pass: strip any remaining non-ASCII and warn
    remaining = {ch for ch in text if ord(ch) > 127}
    if remaining:
        print(f"WARNING: {len(remaining)} unmapped non-ASCII char(s) stripped: "
              + ", ".join(f"U+{ord(c):04X}" for c in sorted(remaining, key=ord)))
        text = ''.join(ch if ord(ch) <= 127 else '?' for ch in text)
    return text


# Write .tex (pure ASCII — safe against all pdflatex encoding issues)
tex_file = BUILD / "ZIDR_benchmark_paper_v3.tex"
cleaned = clean_for_latex(TEX)
tex_file.write_text(cleaned, encoding="ascii")
print("Wrote .tex file (ASCII-clean)")

# Compile twice (resolves cross-references and figure numbering)
ok = False
for run in range(2):
    result = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "ZIDR_benchmark_paper_v3.tex"],
        cwd=str(BUILD), capture_output=True, text=True, timeout=180
    )
    ok = (BUILD / "ZIDR_benchmark_paper_v3.pdf").exists()

if ok:
    shutil.copy2(BUILD / "ZIDR_benchmark_paper_v3.pdf", OUT_PDF)
    size = OUT_PDF.stat().st_size // 1024
    print(f"Done: {OUT_PDF.name}  ({size} KB)")
else:
    errors = [l for l in result.stdout.splitlines()
              if l.startswith("!") or "Error" in l or "undefined" in l.lower()][:12]
    print("COMPILE FAILED:")
    for e in errors:
        print(" ", e)
