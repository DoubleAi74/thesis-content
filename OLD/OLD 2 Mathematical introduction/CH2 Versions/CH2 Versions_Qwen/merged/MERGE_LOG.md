# MERGE_LOG — Pass 1 merge into `chapter_M_math_intro/` and `chapter_A_constant_Ap/`

Date: 2026-08-07.
Governing documents: `MERGE_MAP_TWO_CHAPTERS.md` (content inventory), `IMPLEMENTATION_PLAN_TWO_CHAPTERS.md` (execution order, phases 0–8), both locked by the user decisions of 2026-08-06. Copies of both are included beside this log for self-containment.
Notation/label freeze: `NOTATION.md`.

---

## 1. Source file → destination map

### 1.1 `7source_claude_1/` (primary base)

| Source file | Destination | Notes |
|---|---|---|
| `ch2_preamble.tex` | both `ch_preamble.tex` files | packages, macros, theorem environments, `\cref` equation format, `ch2plotstyle` (M), `\fwd` (M); `\ChA`/`\ChM` cross-chapter macros added |
| `main.tex` / `chapter2.tex` | both `main.tex` / `chapter_M.tex`, `chapter_A.tex` | report-class wrapper pattern kept; `\setcounter{chapter}{1}` removed (fresh numbering in standalone builds) |
| `sections/01_introduction.tex` | M `sections/01_introduction.tex` | rewritten for two-chapter role: deep $A(p)$ now attributed to Chapter A via `\ChA`; roadmap and original-results remark adjusted; opening paragraphs and two-threads framing kept |
| `sections/02_preliminaries.tex` | M `sections/02_preliminaries.tex` | kept in full (clocks + competing-clocks proof, CTMC/generator/master, PGF, linear BD + Kendall solution + $p_0(t)$); labels renamed `m:` |
| `sections/03_galton_watson.tex` | M `sections/03_galton_watson.tex` | kept in full (figures, phase portrait, critical heuristic derivation); rigorous reciprocal-increment derivation of $S_n\sim2/n$ and Catalan total-progeny law added from codex_1 (see §1.3); pointer sentence to Chapter A replaces the `\cref{sec:Ap}` reference |
| `sections/04_quasi_stationarity.tex` | M `sections/04_conditioning.tex` | mean/variance development kept in body; product-existence and bounds references converted to forward references to Chapter A; Yaglom definition + existence-cited-not-overclaimed paragraph added from codex_1 (see §1.3); `\cref{sec:practical}` in figure caption replaced by "iteration of the recursion" phrasing |
| `sections/05_small_populations.tex` | M `sections/05_small_populations.tex` | early-$S_n$ arithmetic, $k$-cohort, push-of-the-past, discrete BDC, CT BD with full $\Ac(p)$ derivation, CT BDC definition all kept; `\cref{sec:Ap}/sec:GA/sec:compare` references converted to `\ChA` forward refs; upgrades added from codex_1/codex_2 (see §1.3, §1.5) |
| `sections/06_constant_A.tex` | **Chapter A only** (deliberately NOT input into M, per interface policy) | split across A `03_product`, `04_series_bounds`, `05_near_critical` (motivation + continuum-route comparison + rate remark), `06_discrete_vs_continuous`, `07_closed_form_search`, `08_koenigs_identity` (Koenigs definition prose, identity proof skeleton), `11_practical`; soft Becker–Bergweiler/"parameter avoids $\{0,-2\}$" argument and Mandelbrot-as-proof paragraphs **removed** and replaced by the Koenigs_details pipeline (§1.6) |
| `sections/07_method_of_characteristics.tex` | M `sections/06_method_of_characteristics.tex` | all three models, MoC test calculation, ABD closed form kept; equal-rates degeneracy, parameter-regular representation, strengthened domain/resonance remarks and recovering-state-probabilities subsection added from codex_1 (§1.3); Sharp acknowledgement footnote preserved |
| `sections/08_summary.tex` | M `sections/07_synthesis.tex` | rewritten as "What carries forward": toolkit summary, quasi-stationary picture with pointer to Chapter A for the $A(p)$ stack, MoC; M-scoped open questions from claude_2 added (§1.2); A-scoped open question excluded |
| `sections/09_appendices.tex` | M `sections/08_appendices.tex` | both appendices kept; hypergeometric identity enriched with continuation/resonance note (codex_1 App B); coefficient extraction enriched with bivariate Cauchy form, equal-rate limit and ABD extraction via $h(x,t)$ + convolution + marginal check (codex_1 App C) |
| `references.bib` | both `references.bib` files, split by actual citation | Becker1995 verification note preserved; Becker1993 entry added from Koenigs_details bibliography for A |
| `figures/IMG_ch3/*` | copied locally | M: `simpleGWvis`, `subGWvis`, `power_law_fixed`, `conditionalMean`, `kvals`, `kvals505`, `kvals495`, `dtctA`, `abs1`, `abs2`. A: `period_double`, `dtctA`, `A3_hat_plot`, `figure1_parameter_conjugacy`, `figure2_koenigs_linearization`, `figure4_mandelbrot_context`. Paths in `\includegraphics` updated to `figures/` |

### 1.2 `7source_claude_2/` (prose/outlook donor)

| Source | Destination | Notes |
|---|---|---|
| `sections/01_introduction.tex` | M intro (phrasing level only) | "working method" language and honesty remark echoed; claude_1 kept as structural master per the map |
| `sections/05_small_populations.tex` | consulted | claude_1 early-$S_n$ presentation retained (map: only if better; not clearly better) |
| `sections/08_outlook.tex` | M `07_synthesis.tex`; A `12_conclusion.tex` | M-scoped questions (QSD under neither extinction nor rupture; Jensen-bound tightness) placed in M synthesis; value/parameter-transcendence question placed in A conclusion/scope. Split per merge map M.6 |

### 1.3 `7source_codex_1/` (theorem/MoC/BDC upgrades)

| Source | Destination | Notes |
|---|---|---|
| `sections/03_galton_watson.tex` | M `03_galton_watson.tex` | rigorous critical-decay proposition (reciprocal increments + Stolz–Cesàro) added after claude's heuristic; extinction-time tail $2/n^2$; Catalan total progeny exact law + $n^{-3/2}$ asymptotic. Voice neutralised (codex used $\xi$, $\Prob$, $\E$; rewritten in claude macros) |
| `sections/04_quasi_stationarity.tex` | M `04_conditioning.tex` | formal QSD/Yaglom definition; "moments $\neq$ full convergence" caveat; Yaglom-attribution phrasing |
| `sections/05_small_populations.tex` | M `05_small_populations.tex` | exact identity $\Pr(\text{no rupture})=\ex{c^{H_n}}$ with Jensen lower bound and explicit $\ex{H_n}$; non-rupture vs joint-survival distinction; killed-chain subgenerator, survival-loss balance, QSD eigenrelation $\nu K=-\theta\nu$ with decay-rate formula, constant- vs state-dependent-catastrophe semigroup remark. Rates renamed to claude conventions ($\kappa_i$ general, $\rho$ for linear BDC) |
| `sections/06_constant_A.tex` | A `03_product`, `04_series_bounds`, `05_near_critical`, `11_practical` | product tail bracket / certified interval `a:eq:tailbound`; near-critical theorem with remainder $O(\varepsilon\ln(1/\varepsilon))$ and full proof (series decomposition + logarithmic remainder bound); $A(0):=1/2$ convention with motivation; ratio monotonicity marked descriptive; certified-bracket stopping criterion in practical section. Script references in codex captions dropped (prose-only lock) |
| `sections/07_characteristics.tex` | M `06_method_of_characteristics.tex` | equal-rates $p_{1,0}=\alpha t\ee^{-\alpha t}$; parameter-regular (transfer-time convolution) representation with checks; hypergeometric domain/branch-cut discussion and coordinate-singularity note; resonance cancellation $\to t\ee^{-\alpha t}$; recovering-state-probabilities subsection. $\beta\to\lambda$, $\rho\to x_-$ renames applied for notation freeze |
| `appendices/A_closed_form_search.tex` | A `app_closed_form_catalogue.tex` (quarantine) + `07_closed_form_search.tex` (narrative) | $\hat A_1$ slope-kill kept in body; $\hat A_2,\hat A_3,\hat A_4$ and the $A_3$ plot quarantined to appendix; quadratic-conjugacy subsection dropped from the appendix (now main text §08). Autobiographical asides already absent in codex |
| `appendices/B_hypergeometric_integral.tex` | M `08_appendices.tex` App A | continuation clause in statement; resonant-case closing sentence; claude's $\sigma,\eta$-based remark kept as base |
| `appendices/C_coefficient_extraction.tex` | M `08_appendices.tex` App B | Cauchy integral form; ABD $y$-linear extraction $p_{i,j}=\binom Nj\ee^{-\alpha tj}[x^i]h^{N-j}$; finite-convolution note; exterior-binomial marginal check |

### 1.4 `7source_codex_2/` (condensed alternate; selective)

| Source | Destination | Notes |
|---|---|---|
| `sections/05_small_populations.tex` | M `05_small_populations.tex` | hazard-vs-exact-time distinction ($h_n$ conditional hazard, $S_nh_n$ mass function) in discrete BDC; "catastrophe is not mean-field hazard" caution; weighted PGF exact recursion $F_{n+1}=c\phi(F_n)$ with $F_n(1)$, $F_n(1)-F_n(0)$ interpretations. Host/pathogen framing not present in the harvested passages |
| `sections/02_framework.tex` | consulted | multi-type PGF pointer added to M §preliminaries from grok_2's cleaner one-equation form (see §1.7) |

### 1.5 `7source_grok_2/`

| Source | Destination | Notes |
|---|---|---|
| `sections/02_preliminaries.tex` | M `02_preliminaries.tex` | first-step analysis subsection (abstract, short); multi-type PGF pointer equation. Gillespie remark kept short per map |

### 1.6 `Koenigs_details/Galton_Watson_A.tex` (obstruction authority)

| Source block | Destination | Notes |
|---|---|---|
| Abstract | A `01_introduction.tex` | remit/honesty tone carried into the chapter introduction |
| §2 (limiting conditional mean) | A `02_setup_recap.tex` | condensed to the standing-setup role (leans on M); asymptotic-vs-identity caution kept |
| §4 (Koenigs relationship) | A `08_koenigs_identity.tex` | Koenigs definition with $r^{-n}f^{\circ n}$ limit form; basin value $\Psi_r$ and the "shorthand, not naive evaluation" wording; identity proof. GW front matter of D2 §§1–3 **not harvested** (claude_1 is master for shared front; D2 typos/"centuary" moot) |
| §5.1 (definitions) | A `09_hypertranscendence.tex` | DA/HT definition; elementary$\Rightarrow$DA lemma (Rubel); inversion lemma (Moore, Boshernitzan–Rubel); $\psi$/$\varphi$ convention warning |
| §5.2 (BB theorem) | A `09_hypertranscendence.tex` | precise BB statement via Fernandes' survey; lineage remark (Ritt, Aschenbrenner–Bergweiler, Di Vizio–Fernandes) |
| §5.3 (main theorem) | A `09_hypertranscendence.tex` | theorem "no exceptional parameters in $(0,1)$" with proof; remark that the exceptional set inside the window is empty, not merely avoided (supersedes claude_1's soft parameter-plane argument); germ-vs-basin remark |
| §5.4 (scope) | A `10_scope_and_pslq.tex` | (V)/(E)/(D)/(S) taxonomy; value gap with BB 1993 non-transfer (formal + structural reasons); parameter gap with Hardouin–Singer non-applicability; working claim |
| §5.5 (PSLQ) | A `10_scope_and_pslq.tex` | eleven rationals, dual routes (product vs Koenigs-series pullback), 123-test battery, digit/height figures preserved exactly as stated, "evidence not proof" scope statement; mpmath footnote kept; no scripts shipped |
| §6 (practical) | A `11_practical.tex` | hybrid product/asymptotic recipe merged with claude_1's version |
| §7 (conclusion) | A `12_conclusion.tex` | base for the conclusion |
| Appendix A (integrable cases) | A `app_elementary_cases.tex` | $r=2$, $r=4$ derivations; affine-conjugacy lemma promoted to main text §08 (`a:lem:affine`) since rem:empty and the conjugacy figure refer to it; placement inside BB classification |
| Figures | A `figures/` | `figure3_numerical_koenigs.png` copied; figure1/2/4 taken from claude_1 copies (identical assets). Mandelbrot figure recaptioned as consistency check, not proof |
| Bibliography | A `references.bib` | all obstruction-cluster entries transferred; Becker1993 pages/volume taken verbatim from D2 |

### 1.7 Other sources consulted

| Source | Disposition |
|---|---|
| `7source_grok_1/` | consulted for formal density; superseded by claude_1/codex_1 harvests; no passage required beyond what codex_1 provided |
| `codex_1/`, `codex_2/` (short twins) | consulted; early-survival figure material already present in claude_1 with equal quality; nothing harvested |
| `Grok_planned_no_koen/` | architecture only: checkpoint-style toolkit recap folded into M synthesis as ½-page "working method" summary; all Path A/B/C meta, TODOs and pending-verification stance dropped |

---

## 2. Content deliberately omitted

| Omitted | Source | Reason |
|---|---|---|
| `06_constant_A.tex` from Chapter M | claude_1 | user-locked interface policy: M defines $A(p)$ lightly, develops $\Ac(p)$ in detail, forward-refs the deep theory to Chapter A |
| Soft BB claim language ("results of Becker–Bergweiler imply… parameter avoids $c\in\{0,-2\}$" as the *main* argument; Mandelbrot-fractal-domain argument as evidence of non-closed-form) | claude_1 §6 | replaced by the Koenigs_details structural pipeline (D2); Mandelbrot figure retained as pedagogical consistency check only |
| Verification scripts (`scripts/reproduce_numerics.py`, `scripts/extract_coefficients.py`) and their caption references | codex_1 | prose-only lock for this phase; scripts stay with source drafts and are described, not shipped |
| Path A/B/C scaffolding, checkpoint TODOs, "pending MoC verification" stance | Grok_planned_no_koen | draft meta, not thesis prose |
| Host/pathogen-led MoC framing | CC_C2_short_A, grok drafts | abstract-voice lock; compartment/particle language used throughout |
| `CC_C2_short_A/`, `A_Koenigs_Chapter/` as masters | — | map §2: seed kernel / superseded intermediate; nothing needed from them that the primary sources did not supply better |
| D1 (`A_Koenigs_Chapter`) claim language | — | map: do not import; NCF claims superseded by D2 |
| D2 GW front matter (tutorial §§1–3: expectation tower, harmonic-sermon figures, wrapfigure phase diagrams) | Koenigs_details | duplicates M content in a weaker register (typos, first person); claude_1 versions kept |
| codex_2 multi-type GW development beyond a pointer | codex_2 | map: pointer only in M (stretch item satisfied by the pointer equation) |
| Visualiser-kit footnotes / HTML kit paths | CC_C2_short_A | not thesis content |

**Tier-1 residue check:** every Tier-1 item of MERGE_MAP §1 has a home above. The only inventory item placed by reference rather than inclusion is the runnable PSLQ pipeline (user lock: prose only); its numerical content is preserved verbatim in A §10.

---

## 3. Interface contract (MERGE_MAP §3) — status

- M hands to A: binary GW notation ($Z_n$, $\phi(z)=pz^2+(1-p)$), survival recursion, $A(p)$ definition + existence statement, $\ex{Z_n\mid Z_n>0}\to1/A(p)$, $\Ac(p)$ stated and derived, competing-clocks proof of $p=\lambda/(\lambda+\mu)$ — all present in M with `m:` labels.
- A assumes from M only those items; A's setup recap (`a:sec:setup`) is ~2 pages and points to \ChM{} for conditional-law variance and competing-clocks proof. A is readable standalone: every M-dependent claim used in A is either re-stated or explicitly attributed to \ChM.
- Label namespaces `m:`/`a:` enforced; no bare-label collisions (both projects build with zero undefined references).
- Cross-chapter macros: `\ChA` in M, `\ChM` in A, each carrying a thesis-integration comment.

---

## 4. Claim-hygiene checklist (plan §9) — verified in compiled A

- [x] No theorem claimed for non-elementarity of $p\mapsto A(p)$ (explicitly open in `a:sec:scope`, `a:sec:conclusion`).
- [x] No transcendence/irrationality of $A(p_0)$ claimed as proved (boxed denial in the value gap).
- [x] Hypertranscendence of $z\mapsto\psi_r(z)$ claimed for each fixed $r\in(0,1)$ with BB attribution (`a:thm:mainht` via `a:thm:BB`).
- [x] PSLQ stated as finite-height negative evidence only (digit counts and 123-test total preserved from D2).

---

## 5. Builds

- `chapter_M_math_intro/main.pdf`: `latexmk -pdf -halt-on-error` clean from scratch (39 pages; 0 undefined references/citations).
- `chapter_A_constant_Ap/main.pdf`: `latexmk -pdf -halt-on-error` clean from scratch (25 pages; 0 undefined references/citations).
- Figures: all `\includegraphics` resolve against local `figures/` directories; no external paths.

---

## 6. Known issues for the next refinement phase

1. **Pass-2 redesign of Chapter M** — done 2026-08-07; see §7 below.
2. Thesis integration: `\ChA`/`\ChM` macros and `\fwd{...}` forward references need `\ref` targets once chapters are assembled; macros currently hard-code the agreed numbering M = Chapter 2, A = Chapter 3.
3. `conditionalMean.pdf` caption values (2.825, …) are quoted from claude_1 without an in-repo recomputation (prose-only phase).
4. Overfull boxes: none catastrophic; no microtype pass performed (per plan §11).
5. PSLQ reproducibility assets (scripts, 1150-digit values, per-test log) remain with the original project archive, referenced only in the A footnote.
6. Standalone chapter numbering — fixed in pass 2: builds now render Chapter 2 / Chapter 3.

---

## 7. Pass 2 — Chapter M redesign (executed 2026-08-07)

Restructured `chapter_M_math_intro/` per `SECOND_PASS_CHAPTER_M_OUTLINE.md` §1. Frozen decisions (user answers to outline §7): displaced bulk → **M appendices**; new blocks → **written fully**; MoC worked example → **absorption–death**; thesis numbering → **M = 2, A = 3**. Donor map frozen in `chapter_M_math_intro/OUTLINE_PASS2.md`.

### 7.1 New structure (compiled TOC)

- §2.1 Overview (new; framework + methods map; two-questions framing)
- §2.2 Markov chains
  - 2.2.1 DTMC: definition + Chapman–Kolmogorov; **simple random walk (new)** with $n$-step law, drift/diffusion, gambler's-ruin teaser; GW compressed to definition + one-step structure + binary specialization + pointer
  - 2.2.2 CTMC: exponential clocks + competing-clocks proof; generator/master; **Poisson process (new)** with inductive law, thinning/superposition; birth–death (rates, PGF PDE, Kendall solution, $p_0(t)$, threshold, density-dependent pointer); BDC definition + PGF equation
  - 2.2.3 **Time-inhomogeneous (new)**: general setup (no semigroup, holding-time survival function); time-inhomogeneous linear BD (mean explicit, extinction Riccati); **logistic speciation model (new, fully worked)**: state-dependent speciation $\lambda_0(1-n/K)$, mean-field closure to logistic ODE with equilibrium $N_\ast=K(1-\mu/\lambda_0)$, closed intensity integral and explicit mean relaxing to $N_\ast$, figure
  - 2.2.4 **Coupled ODE–CTMC (new)**: two-directional definition (ODE flow between jumps, $Y$-dependent generator), PDMP character (Davis 1993), event-driven simulation with time-dependent race, mean-field closures, rupture-feeds-medium schematic example
- §2.3 Methods for Markov chains
  - 2.3.1 Discrete-time (brief): PGFs/composition, functional iteration + smallest-fixed-point argument, first-step analysis with gambler's ruin solved; pointer to Chapter A / Koenigs (no Koenigs development)
  - 2.3.2 Continuous-time (main weight): backward equations with BD extinction Riccati worked; mean; variance + higher-moment triangular closure with explicit BD variance; hitting probabilities (BD gambler's-ruin analogue, embedded-jump-chain correspondence); extinction probabilities (both routes); conditional means: QSD/Yaglom definition, BD quasi-stationary mean, critical $1+\lambda t$, $\Ac(p)$ derivation, discrete $A(p)$ definition + quasi-stationary mean $1/A(p)$ + forward refs to Chapter A, conditional-mean figure
  - 2.3.3 MoC: four-step recipe; worked example = absorption–death (full characteristic calculation + independence check + state-probability figure); pointers to appendix models and support appendices
- Appendices 2.A–2.G:
  - 2.A hypergeometric integral identity (unchanged from pass 1)
  - 2.B coefficient extraction (unchanged except ABD part → pointer to 2.G)
  - 2.C critical branching in detail (pass-1 §3: fixed points + cobweb figure, critical power law with heuristic and rigorous reciprocal-increment proof, harmonic and power-law figures, Catalan total progeny)
  - 2.D founding cohorts and early survival (pass-1 §5: early-$S_n$ arithmetic, $k$-cohort, push of the past, figures)
  - 2.E quasi-stationary variance derivation (pass-1 §4.3)
  - 2.F discrete BDC + killed chain (pass-1 §5.3 + killed-chain subsubsection)
  - 2.G further absorption models (pass-1 §6 remainder: absorption-only with independence route; full ABD closed form, parameter-regular representation, hypergeometric/domain/resonance, state-probability recovery; Sharp acknowledgement footnote moved here)

### 7.2 Housekeeping performed

- Pass-1 section files preserved under `chapter_M_math_intro/pass1_archive/` (not in the build path).
- Labels: all `m:`-prefixed and stable across the move; new labels for new blocks (`m:sec:rw`, `m:sec:poisson`, `m:sec:inhomog`/`logspec`, `m:sec:coupled`, `m:sec:methdisc`/`methct`/`backward`/`hittingct`, `m:app:critical`/`cohorts`/`variance`/`dbdc`/`moc`). One pass-1 label renamed for hygiene: `m:eq:pgfDef` → `m:eq:pgfbiv` (bivariate PGF), to avoid collision with the univariate `m:eq:pgfdef` of §2.3.1.
- Numbering: `\setcounter{chapter}{1}` in M `main.tex` (renders Chapter 2), `\setcounter{chapter}{2}` in A `main.tex` (renders Chapter 3); appendix letters render 2.A–2.G and 3.A–3.B respectively.
- Cross-chapter macros now hard-code the agreed numbering: `\ChA` = “Chapter 3 (*The constant $A(p)$*)”, `\ChM` = “Chapter 2 (*Mathematical introduction*)”, with thesis-integration comments.
- `references.bib` (M): added `Davis1993` (PDMPs).
- Figures: `dtctA.png` removed from M (discrete-vs-continuous comparison is Chapter A's property); all other figures retained and re-homed with their sections.
- NOTATION.md cross-reference block updated for the numbering.

### 7.3 New content provenance and caveats

- Random walk, Poisson, time-inhomogeneous framework, logistic speciation and coupled ODE–CTMC subsections are new writing (no donor in the source drafts), at textbook level; the logistic-speciation intensity integral and mean were derived and checked during writing (first draft carried an inconsistent carrying point, corrected before freeze). The mean-field step in logistic speciation is explicitly flagged as modelling, not identity.
- No thesis-specific claims invented in the new blocks; the coupled-system schematic example points at later chapters via `\fwd`.

### 7.4 Builds

- `chapter_M_math_intro/main.pdf`: 48 pages (after §7.6 figures), `latexmk -pdf -halt-on-error` clean, 0 undefined references/citations.
- `chapter_A_constant_Ap/main.pdf`: 27 pages (after §7.6 figures), clean, 0 undefined references/citations.

### 7.5 Stop conditions (outline §5) — status

- [x] Structure matches outline §1 (verified against compiled TOC)
- [x] New process classes present at agreed depth (written fully, per user)
- [x] MoC accessible + one worked example (absorption–death) in body; remaining models in appendix 2.G
- [x] Chapter A still owns deep $A(p)$ (M carries only definition, mean, $\Ac$ derivation and pointers — grep-verified: no Koenigs/BB/PSLQ in M)
- [x] Not a final literary rewrite

### 7.6 Figures added (2026-08-08)

Eight new publishable figures, generated from reproducible scripts stored in
each project's `figures_src/` (Python 3 + numpy + matplotlib, serif/CM math
styling, validated palette with dash-style + direct-label secondary encoding;
one TikZ schematic). All embedded with informative captions; both PDFs rebuild
clean.

Chapter M:
- `figures/rw_transition.pdf` (§2.2.1): exact binomial position law at $n=40$, three drifts, means/variances annotated.
- `figures/ruin_prob.pdf` (§2.3.1): gambler's-ruin hitting probabilities, $p=0.4,\tfrac12,0.6$, $b=20$.
- `figures/logspec_mean.pdf` (§2.2.3): mean diversity of the logistic speciation surrogate, $N_0=1,3,6$, relaxing to $N_\ast$.
- `figures/rupture_sawtooth.pdf` (§2.2.4): exact event-driven simulation of the coupled rupture system; compartment staircase + medium sawtooth with aligned rupture times (re-seeding flagged in caption).
- TikZ feedback schematic `m:fig:coupled` (§2.2.4): CTMC ⇄ ODE coupling.

Chapter A:
- `figures/Ap_bounds_ratio.pdf` (§04): $A(p)$ between its two-sided bounds plus ratio $A/\Ac$ with endpoint limits, from the exact series.
- `figures/Ap_nearcrit.pdf` (§05): deficit $1-A/2\varepsilon$ over five decades of $\varepsilon$, slope-1 guide and empirical $\varepsilon(\ln(1/\varepsilon)+0.78)$ fit.
- `figures/koenigs_domain.pdf` (§09): basin value vs Taylor truncations at $r=0.7$ with the $(1-r)/r$ radius line (germ/basin distinction).

Script fixes made during visual QA: mathtext substitutions (`\tfrac`→`\frac`, `\bigl`→parens), panel-(b) ratio denominator corrected to $\Ac=2\varepsilon/(1+\varepsilon)$, $\varepsilon$-grid orientation corrected, deficit sign corrected to $1-A/2\varepsilon$, label placements adjusted.
