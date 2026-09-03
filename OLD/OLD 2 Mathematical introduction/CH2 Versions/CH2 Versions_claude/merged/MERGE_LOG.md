# MERGE_LOG

Builder record for the two merged chapter projects under `merged/`. Governing
documents: `MERGE_MAP_TWO_CHAPTERS.md` (content inventory) and
`IMPLEMENTATION_PLAN_TWO_CHAPTERS.md` (execution). Notation freeze:
`merged/NOTATION.md`.

**Workspace note.** The workspace was split into three parallel copies
(`CH2 Versions_CL`, `CH2 Versions_codex`, `CH2 Versions_Grok`) with identical source
contents; this build was performed in the `_CL` copy. Those three copies were later
gathered under a parent directory, so the current path of this project is
`Desktop/CH2 Versions/CH2 Versions_CL/merged/`. If the tree is moved again, nothing
inside it needs changing: all figure paths are local via `\graphicspath{{figures/}}`
and there are no absolute references.

---

## Pass 1 — content merge

### Deliverables

| Path | State |
|---|---|
| `merged/chapter_M_math_intro/main.pdf` | compiles, `latexmk -pdf -halt-on-error`, 42 pp, zero LaTeX warnings (superseded by the pass-2 restructure below, which brings it to 40 pp) |
| `merged/chapter_A_constant_Ap/main.pdf` | compiles, `latexmk -pdf -halt-on-error`, 28 pp, zero LaTeX warnings |
| `merged/NOTATION.md` | written |
| `merged/MERGE_LOG.md` | this file |

Both projects are standalone (`main.tex` → `chapter.tex` → `sections/`), carry local
`figures/` copies and their own `references.bib`, and use `report` with `\chapter`
so each is a thesis-ready fragment. Every `\cite` resolves; no `\ref` is undefined.

### 1. Source file → destination map

#### Chapter M — mathematical introduction

| Destination | Primary source | Merged-in upgrades |
|---|---|---|
| `sections/01_introduction.tex` | `7source_claude_1/sections/01_introduction.tex` | Roadmap rewritten for the two-chapter split: the two threads are kept, but the near-critical *amplitude theory* is explicitly assigned to Chapter A. The claim that §`06_constant_A` results "are placed here" was removed; the only originality claim left in M is the absorption–birth–death closed form and the hypergeometric identity. |
| `sections/02_preliminaries.tex` | `7source_claude_1/sections/02_preliminaries.tex` | Backward-equation sentence added to the CTMC subsection. **New subsection `First-step analysis`** built from `7source_grok_1/sections/01_preliminaries.tex` (Prop. first-step principle) plus the framing of `7source_grok_2/sections/02_preliminaries.tex` §first-step; mean-hitting-time companion system added. Multi-type PGF kept as a one-sentence pointer only (per map: pointer, not development), phrasing after `7source_codex_2`. Closing paragraph of `linbd` now ties the extinction threshold back to first-step analysis. |
| `sections/03_galton_watson.tex` | `7source_claude_1/sections/03_galton_watson.tex` | **Upgrade:** the heuristic continuum derivation of $S_n\sim2/n$ is replaced as the primary argument by `7source_codex_1/sections/03_galton_watson.tex` Prop. *Critical survival probability* (Stolz–Cesàro on reciprocal increments); the continuum route is retained as a marked remark. Added from the same source: exact extinction-time decrement $\Pr(T=n+1)=\tfrac12S_n^2$, and the **Catalan total-progeny law** $\Pr(\mathcal T=2k+1)=C_kp^k(1-p)^{k+1}$ with its $k^{-3/2}$ critical asymptotic. **New closing subsection** "What is elementary here, and what is not" — the one-paragraph pointer to Chapter A required by the map. |
| `sections/04_conditioning.tex` | `7source_claude_1/sections/04_quasi_stationarity.tex` | Retitled from "The limiting conditional distribution". **Added:** formal Definition of quasi-stationary and Yaglom laws from `7source_codex_1/sections/04_quasi_stationarity.tex`, with that source's careful attribution paragraph (existence cited to Yaglom, not re-proved; two converged moments ≠ full distributional convergence). Mean and full second-moment/variance derivation kept in body per map. **New subsection `m:sec:Apinterface`** implements the interface policy: states the two facts about $A(p)$ that M uses, then enumerates everything deferred to Chapter A. Riccati subsection retained and its closing sentence re-pointed at Chapter A. |
| `sections/05_small_populations.tex` | `7source_claude_1/sections/05_small_populations.tex` | **Reordered per the interface policy** so the continuous-time constant is developed first and in detail. Added: ultimate establishment probability for a $k$-cohort (`7source_codex_1` small pops); exact exposure identity $\Pr(\text{no rupture})=\E[(1-\kappa)^{H_n}]$ and $\E[H_n]$ (`7source_codex_1` §discrete rupture) which turns claude_1's Jensen remark into a stated identity plus a bound; **`m:rem:notmeanfield`** ("a state-dependent catastrophe is not a mean-field hazard") built from `codex_1/sections/03_survivability_of_small_populations.tex` §catastrophe-caution, including the joint-survival caveat and the coupling-after-trigger point. `m:sec:cts` substantially expanded: the closed form for $\Ac(p)$ is now derived with the amplitude exhibited outright as the prefactor $(\mu-\lambda)/\mu$, the competing-clocks parametrisation is given its own subsection, and a "discrete against continuous" subsection states the comparison and hands the proof to Chapter A. **New subsection `m:sec:killedchain`** from `7source_codex_1/sections/05_small_populations.tex` §bdc-setup: killed subgenerator, survival-loss balance, QSD left-eigenvector relation and decay rate, constant-vs-state-dependent catastrophe clock. |
| `sections/06_method_of_characteristics.tex` | `7source_claude_1/sections/07_method_of_characteristics.tex` | Full three-model ladder kept. **Added from `7source_codex_1/sections/07_characteristics.tex`:** §*A parameter-regular representation* (interior backward equation, the $\beta=\mu$ critical case, the absorption-time convolution $g=\ee^{-\alpha t}y+\alpha\ee^{-\alpha t}\int_0^t\ee^{\alpha v}F\,\dd v$, and the observation that it fixes which continuation of the special-function form is meant); domain remark strengthened with the coordinate-singularity point at $x=x_-$; resonance remark strengthened with the explicit cancelling combination and secular factor; **new §*Recovering state probabilities*** with the exterior/interior coefficient separation $p_{i,j}=\binom Nj\ee^{-\alpha tj}[x^i]h^{N-j}$. Voice filter applied: codex's "transfer" language mapped onto claude's "absorption"; no host/pathogen wording imported. |
| `sections/07_synthesis.tex` | `7source_claude_1/sections/08_summary.tex` + `7source_claude_2/sections/08_outlook.tex` | Four-strand summary (apparatus / method / quasi-stationary picture / reserved definitions). The "working method" strand is claude_2's. **Open questions section** takes claude_2's M-scope questions — QSD under neither extinction nor rupture, tightness of the Jensen bound — and explicitly *hands the third* (elementarity of $p\mapsto A(p)$) to Chapter A rather than answering it. |
| `sections/08_appendices.tex` | `7source_claude_1/sections/09_appendices.tex` | Both appendices kept in full. **Added from `7source_codex_1/appendices/C_coefficient_extraction.tex`:** the bivariate Cauchy-integral form of the coefficient, noted as the robust route when derivatives of a special-function representation are unwieldy. Closing paragraph re-pointed at the ABD separation formula. `7source_codex_1/appendices/B_hypergeometric_integral.tex` was compared against claude_1's App. A and is not strictly richer, so claude_1's proof was kept unchanged. |

Figures copied to `chapter_M_math_intro/figures/`: `simpleGWvis.png`,
`subGWvis.png`, `power_law_fixed.pdf`, `conditionalMean.pdf`, `kvals.png`,
`kvals505.png`, `kvals495.png`, `dtctA.png`, `abs1.pdf`, `abs2.pdf`. All
`figures/IMG_ch3/` paths flattened; `\graphicspath{{figures/}}` set locally.

#### Chapter A — the constant $A(p)$

| Destination | Primary source | Merged-in upgrades |
|---|---|---|
| `sections/01_introduction.tex` | new framing | Remit and section-by-section roadmap; opens by stating the four-reading scope problem so that the honesty of §`10` is set up rather than sprung. Tone after the `Koenigs_details` abstract. |
| `sections/02_setup_recap.tex` | `7source_claude_1/sections/04_quasi_stationarity.tex` (compressed) + `Koenigs_details` §limiting conditional mean | Deliberately short (≈2 pp): binary GW, $S_{n+1}=2pS_n-pS_n^2$, standing range $0\le p<\tfrac12$, $\varepsilon$ and $r$, definition of $A(p)$, the two inherited consequences $1/A$ and the conditional variance **quoted not re-derived**, $\Ac(p)$ quoted with the competing-clocks matching **cited to Chapter M, not re-proved**, and the endpoint convention $A(0):=\lim_{p\downarrow0}A(p)=\tfrac12$. |
| `sections/03_product.tex` | `7source_claude_1/sections/06_constant_A.tex` §product | Logistic substitution, telescoping, convergence. **Upgrade:** the result is promoted to a numbered Proposition (as in `7source_codex_1` §A-product) so that existence of the limit has a citable home, since Chapter M defers existence here. **Added:** `7source_codex_1` certified tail bracket $A_N(1-w_{N+1}/(1-r))\le A\le A_N$ as its own subsection. "Is this an advance?" kept. |
| `sections/04_series_bounds.tex` | `7source_claude_1` §series/bounds | Series proposition, two-sided bounds, $A>\tfrac12\Ac$, parity bound, and `tab:Avals`. Iteration counts in the table are claude_1's (they correspond to claude_1's convergence criterion; codex_1's table gives smaller counts under a different criterion — claude_1's were kept for consistency with §practical). |
| `sections/05_near_critical.tex` | **`7source_codex_1/sections/06_constant_A.tex` Thm. near-critical** | **This is the main theorem upgrade.** claude_1 had only a heuristic $A\sim2\varepsilon$; the codex source has a full proof of $A=2\varepsilon[1+O(\varepsilon\log(1/\varepsilon))]$ and it has been imported *with* its proof, made self-contained (the monotone comparison $S_n(p)\le S_n(\tfrac12)$ and the bound $S_n(\tfrac12)\le2/(n+2)$ are now derived inline rather than cross-referenced to codex's GW section). claude_1's heuristic version is retained afterwards as exposition. The critical-gradient diagnostic ($-4$) and the empirical $c\approx0.78$ fit are kept, the latter explicitly flagged as empirical and unused. |
| `sections/06_discrete_vs_continuous.tex` | `7source_claude_1` §compare | Ratio limits, both endpoint interpretations, and the figure. **Added:** the next-order comparison — $\Ac$ has an elementary $\varepsilon$-expansion whereas the discrete correction carries $\log(1/\varepsilon)$ — and a closing "where the closed form went" subsection that states the structural difference and forward-points to §`09`. |
| `sections/07_closed_form_search.tex` | `7source_claude_1` §GA | Continuum route, GA narrative, $\hat A_1$, $\hat A_3$, $\hat A_4$, the $-4$-gradient kill criterion, and the "curve fitting cannot distinguish" punchline. Endpoint-constrained framing and the "no inferential status" disclaimer taken from `7source_codex_1/appendices/A_closed_form_search.tex`. |
| `sections/08_koenigs_identity.tex` | `7source_claude_1` §koenigs + **`Koenigs_details` §4** | **Claim-hygiene upgrade.** claude_1 proved $A(p)=2\psi_r(\tfrac12)$ without addressing that $\tfrac12$ leaves the Koenigs germ once $p\ge\tfrac13$ (germ radius $(1-r)/r$). The `Koenigs_details` treatment is used instead: local $\psi_r$, explicit **basin extension** $\Psi_r(w)=\lim r^{-n}f_r^{\circ n}(w)$, identity stated as $A(p)=2\Psi_r(\tfrac12)$, and `a:rem:basin` recording that hypertranscendence of germ and basin extension are equivalent so nothing is lost. `figure3_numerical_koenigs.png` imported from `Koenigs_details/figures/`. |
| `sections/09_hypertranscendence.tex` | **`Koenigs_details` §§5.1–5.3** | **The obstruction core, replacing claude_1's argument entirely.** Definitions of differentially algebraic / hypertranscendental; Lemma elementary ⇒ DA (Rubel); Lemma closure under compositional inversion (Moore; Boshernitzan–Rubel) with the $\psi$ vs $\varphi$ convention warning; Becker–Bergweiler stated precisely in the Fernandes restatement; lineage remark (Ritt 1926, Aschenbrenner–Bergweiler, Di Vizio–Fernandes); **Theorem: for every $r\in(0,1)$, $\psi_r$ is hypertranscendental**, proved via BB(i) *repelling*, not via parameter-plane avoidance. `a:rem:empty` records that the earlier parameter-plane argument is superfluous and why. The Mandelbrot/cardioid material is retained but demoted in its own subsection and captioned as a pedagogical consistency check, twice stated not to be part of the proof. |
| `sections/10_scope_and_pslq.tex` | **`Koenigs_details` §§5.4–5.6** | Four-reading taxonomy (V)/(E)/(D)/(S); the **value gap** with the 1993 Becker–Bergweiler non-transfer argued on both formal (degree mismatch) and structural (Mahler-method exponent) grounds, and the explicit statement that irrationality is unproved for every rational $p_0$; the **parameter gap** with the Hardouin–Singer non-applicability reason ($\partial_r$ does not commute with a $\sigma$ that moves with $r$); the PSLQ battery as prose (eleven parameters, dual routes, ≥1150 digits agreeing to ≥1192, five test families, 123 null tests, all terminating on internal norm bounds) with the scope disclaimer; the working claim quoted as a display. |
| `sections/11_practical.tex` | `7source_claude_1` §practical + `Koenigs_details` §practical | Hybrid product/asymptotic scheme with crossover selection justified by the proved remainder. **Added:** three practical points — prefer the product over the raw ratio, stop on the certificate rather than on apparent convergence (a real failure mode near criticality), and compute $1/A$ from the series directly when that is what is wanted. The certificate is `7source_codex_1`'s tail bracket. |
| `sections/12_conclusion.tex` | `Koenigs_details` conclusion + `7source_claude_2` outlook (A-scope question) | What is established, what is not, and two numbered open problems (the value problem; the parameter problem) stated as such. |
| `sections/app_elementary_cases.tex` | **`Koenigs_details` App. A** | $r=2$ (logarithmic) and $r=4$ (inverse-trigonometric) derivations with verifications; affine conjugacy lemma $c=(2r-r^2)/4$; and the placement of both worked examples inside the BB classification (exponential and cosine families, both over repelling fixed points). |
| `sections/app_closed_form_catalogue.tex` | `7source_codex_1/appendices/A_closed_form_search.tex` | Quarantine appendix. Holds $\hat A_2$ (the long nested-trigonometric output, which appears in no other merged location), the constrained rational candidate restated with its slope defect, and the splice discussion pointing back at the certified scheme. |

Figures copied to `chapter_A_constant_Ap/figures/`: `period_double.png`,
`A3_hat_plot.pdf`, `figure1_parameter_conjugacy.pdf`,
`figure2_koenigs_linearization.png`, `figure4_mandelbrot_context.png`,
`dtctA.png`, `conditionalMean.pdf` (copied, currently unused — retained for a
possible conditional-mean plot in A), and `figure3_numerical_koenigs.png` from
`Koenigs_details/figures/`.

### 2. Interface between the two chapters

Chapter M hands over: $Z_n$, $p$, $\phi(z)=pz^2+(1-p)$, $S_n$ and its recursion,
the definition of $A(p)$, $\E[Z_n\mid Z_n>0]\to1/A(p)$ and the conditional
variance, $\Ac(p)=(1-2p)/(1-p)$ derived in full, and the competing-clocks
identification $p=\lambda/(\lambda+\mu)$ proved once (`m:prop:race`) and cited
rather than re-proved in A.

Chapter M states $A(p)$'s existence and the bound $0<A(p)\le\tfrac12$ **as facts
proved in Chapter A** (`m:sec:Apinterface`), and develops nothing else about it.
`06_constant_A.tex` was never `\input` into M.

Chapter A's recap (`02_setup_recap.tex`) is ~2 pages and re-derives nothing that M
proves.

### 3. Content deliberately omitted

| Omitted | Reason |
|---|---|
| `7source_codex_1/scripts/` (`verify_algebra.py`, `verify_pgf.py`, `reproduce_numerics.py`, `extract_coefficients.py`, `run_checks.sh`) | User lock: prose only this phase. Gate G8. The claims those scripts underwrite are stated as reported numerical checks. |
| PSLQ pipelines, logs, 1150-digit value files | Same lock. The evidence is reported as prose with an explicit "archived with the project sources" footnote, per the map's A.10 fallback. |
| `Grok_planned_no_koen` Path A/B/C scaffolding, TODO markers, "pending verification" stance | Draft meta, explicitly excluded by the map. The one usable idea — a mid-chapter toolkit checkpoint — was judged redundant against the synthesis section and dropped; see "known issues" below. |
| `CC_C2_short_A` as a master | Seed kernel with applied (host/pathogen) bleed and no preliminaries. Nothing in it was found missing from claude_1. |
| `A_Koenigs_Chapter` claim language | Superseded by `Koenigs_details`; importing it would reintroduce the softer NCF phrasing the plan requires be removed. |
| claude_1's "parameter avoids $c\in\{0,-2\}$" as the *main* obstruction argument | Replaced wholesale by the BB(i)-repelling route. The parameter-plane observation survives only as a consistency check, explicitly labelled as such in three places. |
| codex_1's alternative hypergeometric-integral appendix (`B_*`) | Compared against claude_1's App. A; not strictly richer. claude_1's version kept per the "only if strictly richer" rule. |
| Host/pathogen framing throughout | Voice filter, gate G7. codex "transfer" terminology mapped to "absorption"; grok MoC framing not used. |
| codex_2 figure paths `../Ch2_seed/...` | Would break the local-figures rule. |
| Multi-type GW sketch (codex_2) | Listed as optional stretch only. A one-sentence multivariate-PGF pointer is in M's PGF subsection; the sketch itself was not imported. |

### 4. Tier-1 items placed, with nothing unaccounted for

Every Tier-1 row of `MERGE_MAP_TWO_CHAPTERS.md` §1 has a destination above. No
formula present in a Tier-1 source was left unplaced. The two items closest to
being dropped were codex's $\hat A_2$ (now in `app_closed_form_catalogue.tex`) and
codex's killed-chain eigenrelation (now `m:sec:killedchain`).

### 5. Quality gates

| Gate | Status |
|---|---|
| G1 both PDFs compile with `latexmk -halt-on-error` | pass (42 pp / 28 pp, zero warnings, no undefined refs or cites) |
| G2 M contains prelims, GW, conditioning, small pops, CT BDC def, full MoC ladder, synthesis, apps | pass |
| G3 M contains no product/series/Koenigs/BB/PSLQ development | pass — grep confirms the only occurrences of those terms in M are forward pointers |
| G4 M develops $\Ac(p)$ in detail and forward-refs discrete $A(p)$ theory | pass (`m:sec:cts`, `m:sec:Apinterface`) |
| G5 A contains product, series, bounds, near-crit, discrete/continuous, search, Koenigs identity, HT theorem, scope, PSLQ prose, practical, conclusion, elementary-cases app | pass |
| G6 claim hygiene | pass: no claim that $p\mapsto A(p)$ is non-elementary; no claim of transcendence or irrationality of $A(p_0)$; hypertranscendence of $z\mapsto\psi_r(z)$ claimed with BB attribution; PSLQ stated as finite-height negative evidence |
| G7 abstract mathematical voice | pass |
| G8 no verification scripts shipped | pass |
| G9 notation freeze respected | pass — `\Ac` throughout, $\varepsilon=1-2p$, $r=2p$, `m:`/`a:` label prefixes with no bare labels surviving |
| G10 MERGE_LOG complete | this file |

### 6. Known issues for a later phase (not fixed now)

1. `chapter_A_constant_Ap/figures/conditionalMean.pdf` is copied but unused. The
   map allows the conditional-mean plot to appear lightly in A as well as M; it
   currently appears only in M.
2. The iteration counts in `a:tab:Avals` come from claude_1 and reflect its
   convergence criterion. `7source_codex_1` reports smaller counts for the same
   parameters under a different criterion. Neither is wrong; if the table is ever
   regenerated, the criterion should be stated in the caption.
3. The empirical constant $c\approx0.78$ in `a:rem:rate` is unverified in this
   build and is flagged in the text as empirical and unused.
4. The optional mid-chapter "toolkit checkpoint" for M (map §7, ½ page) was not
   written; the synthesis section covers the same ground at the end instead.
5. Cross-chapter references are routed through `\ChM` / `\ChA` macros. Thesis
   integration means redefining those two macros to emit real chapter numbers, and
   redefining `\fwd` to carry chapter references to the later modelling chapters.
6. `Koenigs_details` front-matter typos (e.g. "centuary") were not carried in,
   because none of those paragraphs were used.

---

## Pass 2 — Chapter M restructure

Governing document: `SECOND_PASS_CHAPTER_M_OUTLINE.md` §1. **Chapter A was not
modified**, and no product/series/bounds/Koenigs/hypertranscendence/PSLQ material
was moved back into M.

### Preconditions checked

| Requirement | State before pass 2 |
|---|---|
| `merged/chapter_M_math_intro/` exists and compiles | yes, 42 pp |
| `merged/chapter_A_constant_Ap/` exists and compiles | yes, 28 pp |
| `merged/MERGE_LOG.md` exists | yes (Pass 1 section above) |

### Result

`merged/chapter_M_math_intro/main.pdf` — 40 pp, `latexmk -pdf -halt-on-error`,
zero LaTeX warnings, no undefined or multiply-defined labels, all twelve `\cite`
keys resolved. `merged/chapter_A_constant_Ap/main.pdf` rebuilt unchanged, 28 pp,
zero warnings.

Pass-1 section files are preserved verbatim in
`chapter_M_math_intro/sections_pass1/` (including the old `chapter.tex`) and are no
longer `\input`. Nothing was deleted without a copy.

Final file list and donor map: `chapter_M_math_intro/OUTLINE_PASS2.md`.

### Structure delivered

```
1   Overview
2   Markov chains
2.1   Discrete-time Markov chains        (simple random walks; Galton--Watson, brief)
2.2   Continuous-time Markov chains      (exponential clocks; Poisson; birth--death;
                                          birth--death--catastrophe)
2.3   Time-inhomogeneous processes       (logistic speciation model — STUB)
2.4   Coupled ODE--CTMC systems          (framework complete; instance — STUB)
3   Methods for Markov chains
3.1   Discrete-time methods              (first-step; generating functions; functional
                                          iteration; hand-off to Chapter A/Koenigs)
3.2   Continuous-time methods            (forward/backward equations; mean; variance and
                                          higher moments; hitting probabilities;
                                          extinction probabilities; conditional means)
3.3   The method of characteristics      (the idea; one worked example; what it shows)
A   Critical behaviour and small populations
B   The absorption models in full
C   An integral identity for the hypergeometric function
D   Extracting state probabilities from a generating function
```

### Compression applied

| Pass-1 block | Pass-2 fate |
|---|---|
| Full binary GW section (critical theory, phase portraits, power laws) | §2.1 keeps definition, offspring PGF, mean recursion and survival recursion only. Fixed-point/extinction analysis moved to §3.1 as an instance of functional iteration, where the phase-portrait figure now sits. All critical theory — $S_n\sim2/n$ with its Stolz–Cesàro proof, the harmonic-series divergence, $\Pr(T=n+1)\sim2/n^2$, the Catalan total-progeny law, the power-law figure — moved intact to **App. A**. |
| Quasi-stationarity section | Recast as §3.2 *Conditional means*, one method among several rather than a section of its own. Definition of quasi-stationary/Yaglom laws kept; the mean derivation kept; the full second-moment derivation compressed to its result \cref{m:eq:condvar} with the method indicated (App. A carries no replacement — the derivation is the one place where pass-1 detail was genuinely cut rather than moved, and it is recoverable from `sections_pass1/04_conditioning.tex`). |
| Riccati continuum view | Moved to **App. A** alongside the critical-case continuum remark, where the two heuristic substitutions can be compared directly. |
| Small-populations section (early $S_n$, $k$-cohort, push of the past) | Moved wholesale to **App. A**. |
| Discrete BDC calculation | The conceptual content — the exact exposure identity, the Jensen direction, the three cautions — is now `m:rem:notmeanfield` in §2.2. The arithmetic ($2^n-1$ exposure, $(1-\kappa)^{2^n-1}$, $\E[H_n]$) moved to **App. A**. |
| Full MoC three-model ladder | §3.3 presents the method generically and carries **one** worked example (absorption–death), chosen because an independent answer exists to check against. Absorption-only and absorption–birth–death, with the parameter-regular representation, hypergeometric form, domain, resonance and coefficient recovery, moved to **App. B**. |
| Synthesis / outlook | Folded into §1 Overview and into the closing paragraphs of §3.2; the two M-scope open questions survive in place (Jensen tightness at the end of App. A; QSD under neither mechanism at the end of §3.2). |
| Hypergeometric identity and coefficient extraction appendices | Unchanged, now **App. C** and **App. D**, supporting §3.3 via App. B. |

### Genuinely new material, and how it was sourced

The outline requires four blocks absent from every pass-1 draft. A repository-wide
search (`grep` over all `.tex`, `.md`, `.txt` in `CH2 Versions_CL`) found **no**
source material for any of them. They were handled differently according to whether
writing them requires inventing anything:

| Block | Treatment | Justification |
|---|---|---|
| §2.1 simple random walks | **Written in full** (~1 p): transition probabilities, mean and variance, the embedded-jump-chain identification $q=\lambda/(\lambda+\mu)$, gambler's ruin | Standard textbook material already covered by the bibliography (`Norris1997`, `KarlinTaylor1975`); nothing is invented, and the embedded-chain link makes it load-bearing for §3.2 hitting probabilities rather than decorative |
| §2.2 Poisson process | **Written in full** (~1 p): rates, holding-time construction, the law, mean $=$ variance, independent increments, thinning, and the link to pure birth | Same; thinning is used again in App. B |
| §3.2 mean, variance, higher moments | **Written in full**: moment ODEs derived from the master equation, closed-form variance, the moment hierarchy and why it closes for linear rates | Derived from `m:eq:bdmaster`, which pass 1 already had; no new model or citation |
| §3.2 hitting probabilities | **Written in full**: `m:eq:bdruin` from the embedded walk, with the consistency check against the extinction probability | Same |
| §2.3.1 logistic speciation model | **STUB**, `m:rem:speciationstub` | Writing it would mean inventing rate functions and a citation. The remark states plainly that it is a placeholder and lists exactly what is needed: state space, speciation/extinction rate functions and their time dependence, where the logistic term enters, initial condition, and the source reference. |
| §2.4 coupled ODE–CTMC | **Framework written in full; instance STUB**, `m:rem:coupledstub` | The general theory — the three coupling directions, and the joint generator `m:eq:coupledgenerator` with its transport plus jump terms — requires no source material and is written properly. The thesis's own concrete system is not identified anywhere, so it is not fabricated. A plausible candidate is noted explicitly *as a conjecture about intent, not a statement about the model*. |

### TODO — blocked on user input

1. **Logistic speciation model (§2.3.1).** Needs the model definition and reference.
   Until then §2.3 has its general time-inhomogeneous theory but no worked instance.
2. **Coupled ODE–CTMC instance (§2.4).** Needs identification of the thesis model
   and which of the three couplings it exhibits.
3. Open questions §7 of the outline were answered by default, the user being
   unavailable: GW detail lives in App. A of M plus Chapter A (Q1); stubs for Q2 and
   Q3; absorption–death as the MoC worked example (Q4); hitting probabilities via
   BD/absorption examples only (Q5); full critical GW theory and the full ABD closed
   form both to M appendices (Q6); titles only, no thesis chapter numbers (Q7).
   Any of these can be revisited without touching the rest.

### Interface preserved

- $\Ac(p)$ retains its detailed treatment, now in §3.2 *Conditional means*, where
  the amplitude $(\mu-\lambda)/\mu$ is exhibited directly from the exact survival
  probability and the reason a closed form exists is stated.
- Discrete $A(p)$ is defined lightly (`m:eq:Apdef`) at the point where the
  discrete-time methods run out, §3.1.4, and used as a named object thereafter.
- Forward references to Chapter A appear in §1, §3.1.4 and §3.2, and name what is
  deferred: product and series representations, bounds, near-critical asymptotics,
  the Koenigs identification, and hypertranscendence.
- Chapter A's back-references (`\ChM`) remain accurate: the competing-clocks
  proposition, the conditional-mean and conditional-variance derivations, and
  $\Ac(p)$ are all still in M and still proved there.
- Gate G3 re-checked after restructuring: the only occurrences in M of "Koenigs",
  "Schröder", "hypertranscendental", "product", "series" in the Chapter-A sense are
  forward pointers in §1, §3.1.4, §3.2 and App. A.

### Not done, by instruction

No final literary rewrite or humanizer pass; no cut for length; no new mathematics
beyond what the sources contain; Chapter A untouched.

---

## Pass 3 — aa-flow-lucid prose pass (user-requested, supersedes a phase lock)

Run after Pass 2 at explicit user request. Both `IMPLEMENTATION_PLAN_TWO_CHAPTERS.md`
§9 and the Pass 2 brief defer a literary rewrite; that instruction was superseded by
the request, and this section records the departure so the provenance stays honest.

**Scope.** Both chapters, edited in place at paragraph grain, light-to-moderate
aggression. **This means the Pass 2 statement that Chapter A was "rebuilt unchanged"
is true of Pass 2 only — Chapter A prose was subsequently edited here.** No
structural change to either chapter; the Pass 2 section map and
`OUTLINE_PASS2.md` remain accurate.

**Science frozen.** No claim, number, symbol, equation, citation or attribution was
altered in either chapter. Chapter A's claim hygiene is unchanged: hypertranscendence
of $\psi_r$ claimed with Becker–Bergweiler attribution; the value and parameter
questions still stated as open; PSLQ still finite-height negative evidence.

**Changes made.**

| Location | Change |
|---|---|
| Chapter M, §1 / §2.1 / §3.1.4 | *Amplitude* was used four times before its defining occurrence. It now debuts once, at `m:sec:dtlimit` where $A(p)$ is introduced, and the earlier uses were reworded to plain English. |
| Chapter M, §1 overview | The two-part division was asserted as "deliberate" without a reason; it now gives one, and prepares the two paragraphs that follow. |
| Chapter M, `m:rem:notmeanfield` | Landed on machinery with an afterthought trailing; now lands on a bridge to `m:app:discreterupture`. |
| Chapter M, App. D | Opening sentence split its subject from its verb across a display equation; recast. "More robustly" → "more stably in floating point" (the sense meant). |
| Chapter A, §1 introduction | A ten-rung roadmap enumerating the table of contents replaced by two paragraphs following the actual line of argument. All cross-references preserved. |
| Both | Two near-verbatim repetitions introduced by the above edits were caught and differentiated. |

**Checks.** British spelling verified across both chapters (only `-iz-` hits are the
`itemize` environment and the on-disk filename `figure2_koenigs_linearization.png`,
neither of which may change). No prestige-sludge phrases, slogan landings, or
assert-then-fence patterns. Every section landing inspected individually: all end on
an implication, a limit, or a handoff.

**Build after pass.** Chapter M 40 pp, Chapter A 28 pp, both `latexmk -pdf
-halt-on-error`, zero LaTeX warnings, no undefined or multiply-defined labels.

---

## Pass 4 — figures for Chapter M (user-requested)

Five figures added to the mathematical introduction, all in sections that the pass-2
restructure created and left without one. Chapter A was not touched. No prose was
rewritten beyond the one sentence per figure that introduces it, and no scientific
content changed: every figure plots a quantity the chapter already derives.

| Figure | Section | Made with | What it shows |
|---|---|---|---|
| `m:fig:randomwalk` | §2.1.1 Simple random walks | Python (`random_walk.pdf`) | (a) seven realisations at $q=0.45$ against the drift line and one-sd envelope of `m:eq:rwmoments`; (b) the gambler's-ruin probability `m:eq:gamblersruin` for five values of $\theta$, showing that only the ratio enters — which is what lets `m:eq:bdruin` read it off the embedded jump chain |
| `m:fig:poisson` | §2.2.2 The Poisson process | Python (`poisson_process.pdf`) | (a) a realisation of the counting process with the $\mathrm{Exp}(\alpha)$ holding times marked along the axis and the mean $\alpha t$ dashed; (b) the law `m:eq:poissonlaw` at three times, showing mean $=$ variance $=\alpha t$ |
| `m:fig:ratediagram` | §2.2.4 Birth–death–catastrophe | TikZ (inline) | Transition-rate diagrams for the birth–death and birth–death–catastrophe chains side by side. Makes visible the structural asymmetry recorded in `m:eq:bdcsurvivalloss`: the first can only be absorbed through state 1, the second is removed from any state at once |
| `m:fig:coupled` | §2.4 Coupled ODE–CTMC systems | Python (`coupled_ode_ctmc.pdf`) | A trajectory of the two-way coupling `m:eq:coupledthree`, with the state-2 intervals shaded and the chain shown beneath. The visits to state 2 cluster where $y$ is large, which is the $y$-dependence of the switching rate made visible |
| `m:fig:characteristics` | §3.3.1 The method of characteristics | pgfplots (inline) | The characteristic family of `m:eq:ch13` foliating the $(x,t)$ plane, with one curve highlighted and traced back from an evaluation point to its foot $\sigma$ on the initial surface |

### Honesty constraints observed

- **The coupled ODE–CTMC figure is generic.** Its parameters were chosen only to
  display the mechanism. Both the surrounding prose and the caption say so
  explicitly, so it does not quietly fill the gap that `m:rem:coupledstub` reports.
  The stub stands: the thesis's own coupled model is still unidentified.
- **Nothing was invented.** Every figure plots an equation already in the chapter.
  The random-walk and Poisson figures illustrate standard results already cited to
  the existing bibliography; no new citation was added.
- No figure was added to the logistic speciation subsection, since there is still no
  model to draw.

### Note on the shipped script

`chapter_M_math_intro/figures/make_figures.py` generates the three simulated PDFs
from fixed seeds, so the figures are reproducible. **This is a figure generator, not
a verification script**, so it is not what gate G8 and the "prose only" lock were
aimed at — but that lock did say "no scripts directory in this phase", so the
decision is flagged here rather than made silently. Deleting the file costs only the
ability to regenerate the three PDFs; the PDFs themselves are self-contained and the
chapter compiles without it.

### Second batch (three further figures)

| Figure | Section | Made with | What it shows |
|---|---|---|---|
| `m:fig:bdpaths` | §2.2.3 Birth–death processes | Python (`birth_death_paths.pdf`) | Nine Gillespie realisations from $X_0=5$ in the subcritical, critical and supercritical regimes, with the mean `m:eq:bdmean` overlaid and extinction times marked. The middle panel carries the chapter's opening argument: at criticality the mean is exactly constant while some paths are already extinct and others have grown fourfold |
| `m:fig:extinction` | §3.2.5 Extinction probabilities | Python (`extinction_and_law.pdf`) | (a) $p_0(t)$ from `m:eq:p0t` for three rate ratios and two founding cohort sizes, with the supercritical limit $(\mu/\lambda)^N$ marked; (b) the exact critical law on the positive states at three times, log scale, showing mass accumulating at zero while the tail flattens — with the mean equal to $1$ at all three |
| `m:fig:compartment` | §3.3.2 Worked example | TikZ (inline) | Schematic of the single-compartment absorption geometry: exterior medium, compartment, and the three channels $\alpha$, $\lambda$, $\mu$. The absorption models were previously described only in prose, leaving the reader to picture $X_t$ and $Y_t$ unaided |

The birth–death figure is the only one of the eight that required simulation
(Gillespie, per `m:rem:gillespie`); everything else is an exact formula already in
the chapter. The critical law in panel (b) of `m:fig:extinction` is
$p_n(t)=(\lambda t)^{n-1}/(1+\lambda t)^{n+1}$ for $n\ge1$ with
$p_0=\lambda t/(1+\lambda t)$, obtained from the $\lambda=\mu$ limit of
`m:eq:bdsolution`; it is exact, not sampled.

One LaTeX trap worth recording: a TikZ style named `cap` silently collides with the
built-in line-cap key and aborts the build. The style in `m:fig:compartment` is
named `note` for that reason.

### Build after pass

Chapter M 44 pp (up from 40 before any figures), Chapter A 28 pp unchanged, both
`latexmk -pdf -halt-on-error`, zero LaTeX warnings, no undefined or
multiply-defined labels. `preamble.tex` gained one line,
`\usetikzlibrary{arrows.meta,positioning,calc}`, required by the rate diagram.
