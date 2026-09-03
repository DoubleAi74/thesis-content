# Merge log — Pass 1 two-chapter content merge

Date: 2026-08-06  
Workspace: `/Users/adamaldridge/Desktop/CH2 Versions_codex`  
Scope: Pass 1 only. The structure in `SECOND_PASS_CHAPTER_M_OUTLINE.md` was reviewed but not implemented.

## Deliverables

- `chapter_M_math_intro/`: standalone report project for *Mathematical introduction*.
- `chapter_A_constant_Ap/`: standalone report project for *The constant A(p)*.
- `NOTATION.md`: frozen notation and label-prefix policy.
- This provenance log.

Both projects use local `sections/`, local `figures/`, a local `references.bib`, and a standalone `main.tex`. No scripts directory is shipped.

## Chapter M — harvested sources

| Source file | Destination | Material retained / adaptation |
|---|---|---|
| `7source_claude_1/sections/01_introduction.tex` | `sections/01_introduction.tex` | Base remit and roadmap, rewritten only to enforce the two-chapter division and abstract mathematical voice. |
| `7source_claude_1/sections/02_preliminaries.tex` | `sections/02_preliminaries.tex` | Exponential clocks, memorylessness, competing clocks with proof, CTMC generators, Kolmogorov/master equations, uni- and bivariate PGFs, linear birth–death PDE, closed solution, mean, and extinction probability. |
| `7source_grok_2/sections/02_preliminaries.tex` | `sections/02_preliminaries.tex` | Short first-step-analysis vignette, stripped of application-led language. |
| `7source_claude_1/sections/03_galton_watson.tex` | `sections/03_galton_watson.tex` | Full binary Galton–Watson spine: PGF iteration, mean, extinction phase portrait, critical survival and lifetime exponents, figures. |
| `7source_codex_1/sections/03_galton_watson.tex` | `sections/03_galton_watson.tex` | Exact Catalan total-progeny law and critical `3/2` asymptotic. |
| `7source_claude_1/sections/04_quasi_stationarity.tex` | `sections/04_conditioning.tex` | Late-survival scale, light definition of `A(p)`, limiting conditional mean, full second-moment/conditional-variance derivation, continuum/Riccati view, conditional-mean figure. Deep `A(p)` references were replaced by a forward reference to Chapter A. |
| `7source_codex_1/sections/04_quasi_stationarity.tex` | `sections/04_conditioning.tex` | Claim-hygiene upgrade: Yaglom existence is cited as classical; the chapter’s calculation is described as identifying moments, not as proving the full law from two moments. |
| `7source_claude_1/sections/05_small_populations.tex` | `sections/05_small_populations.tex` | Early-generation arithmetic, founding cohorts, conditional-selection caution, discrete catastrophe calculation and Jensen bound, detailed continuous-time birth–death derivation of `A_c(p)`, discrete/continuous plot, CT birth–death–catastrophe definition and PGF PDE. |
| `codex_1/sections/03_survivability_of_small_populations.tex` | `sections/05_small_populations.tex` | Explicit warning that a state-dependent catastrophe is not a mean-field hazard. |
| `7source_codex_1/sections/05_small_populations.tex` | `sections/05_small_populations.tex` | Killed-subgenerator formulation, survival-mass balance, quasi-stationary left-eigenvector relation and constant-vs-state-dependent catastrophe distinction. |
| `7source_claude_1/sections/07_method_of_characteristics.tex` | `sections/06_method_of_characteristics.tex` | Full absorption ladder: absorption only, absorption–death, MoC verification on the known case, absorption–birth–death, closed PGF, hypergeometric form, figures. |
| `7source_codex_1/sections/07_characteristics.tex` | `sections/06_method_of_characteristics.tex` | Parameter-regular convolution representation, critical/resonant interpretation, domain guidance, and explicit state-probability recovery formula. |
| `7source_claude_1/sections/08_summary.tex` | `sections/07_synthesis.tex` | Toolkit synthesis, rewritten to remove inherited deep-`A(p)` content. |
| `7source_claude_2/sections/08_outlook.tex` | `sections/07_synthesis.tex` | M-scope open questions only: joint conditioning under extinction/catastrophe and tightness of the Jensen exposure bound. Value-transcendence questions were assigned to A. |
| `7source_claude_1/sections/09_appendices.tex` | `sections/08_appendices.tex` | Hypergeometric integral identity and coefficient extraction appendices. |
| `7source_claude_1/references.bib` | `references.bib` | M bibliography, including branching, QSD, CTMC and special-function sources actually cited. |
| `7source_claude_1/figures/` | `figures/` | Local copies of all figures used by M: GW, critical powers, early cohorts, conditional means, discrete/continuous comparison, and absorption figures. |

### Chapter M interface decision

M contains only

\[
A(p)=\lim_{n\to\infty}S_n/(2p)^n,
\qquad
\mathbb E[Z_n\mid Z_n>0]\to1/A(p),
\]

plus the conditional variance needed for quasi-stationarity. In the continuous-time birth–death subsection it derives

\[
A_{\mathrm c}(p)=\frac{1-2p}{1-p}
\]

from the explicit birth–death survival probability and the competing-clock parameter match. Product, series, bounds, near-critical theorem, search, Koenigs theory, Becker–Bergweiler and PSLQ are forward-referenced to A and are not developed in M. In particular, `7source_claude_1/sections/06_constant_A.tex` is never input by M.

## Chapter A — harvested sources

| Source file | Destination | Material retained / adaptation |
|---|---|---|
| New bridge based on `7source_claude_1/sections/04_quasi_stationarity.tex` and `Koenigs_details/Galton_Watson_A.tex` | `sections/01_introduction.tex`, `sections/02_setup_recap.tex` | Short 1–3 page setup only: binary offspring law, survival recursion, definition/existence interface for `A(p)`, limiting conditional mean, notation, and `A_c(p)` benchmark. The full GW/QSD chapter is not duplicated. |
| `7source_claude_1/sections/06_constant_A.tex`, lines corresponding to the product/series/bounds blocks | `sections/03_product_series_bounds.tex` | Infinite product and convergence, “Is this an advance?”, exact series, two-sided bounds, `A>A_c/2`, parity bound, and numerical table. |
| `7source_codex_1/sections/06_constant_A.tex`, near-critical theorem block | `sections/05_near_critical_upgrade.tex` | Rigorous `A(p)=2ε[1+O(ε log(1/ε))]` theorem and proof, replacing reliance on the softer asymptotic alone. |
| `7source_claude_1/sections/06_constant_A.tex`, comparison/search block | `sections/06_comparison_search.tex` | Discrete-vs-continuous endpoint interpretation, symbolic-regression/GA negative evidence, candidate formulae, and critical-slope diagnostics. |
| `Koenigs_details/Galton_Watson_A.tex`, Koenigs section | `sections/08_koenigs_identity.tex` | Logistic substitution, local Koenigs definition, basin extension, and identity `A(p)=2ψ_r(1/2)` with the basin-value qualification. |
| `Koenigs_details/Galton_Watson_A.tex`, obstruction/scope/PSLQ section | `sections/09_obstruction_scope_pslq.tex` | DA/hypertranscendence definitions, inversion lemma, precise Becker–Bergweiler classification statement, theorem for every `r∈(0,1)`, attracting-vs-repelling structural proof, germ/basin remark, scope taxonomy, 1993 non-transfer, Hardouin–Singer non-applicability, eleven rational parameters, 123-test null battery, and explicit evidence-not-proof language. |
| `7source_claude_1/sections/06_constant_A.tex`, practical block | `sections/11_practical.tex` | Hybrid product / near-critical evaluation recipe. |
| `Koenigs_details/Galton_Watson_A.tex`, conclusion | `sections/12_conclusion.tex` | Conclusion rewritten compactly while preserving D2’s claim boundary. |
| `Koenigs_details/Galton_Watson_A.tex`, Appendix A | `sections/app_elementary_cases.tex` | Explicit elementary repelling linearisers at `r=2` and `r=4`, affine conjugacy to `z^2+c`, and their placement in the Becker–Bergweiler classification. |
| `7source_codex_1/appendices/A_closed_form_search.tex` | `sections/app_closed_form_catalogue.tex` | Quarantined exploratory formulae, quadratic conjugacy, parameter geometry and consistency-check figures. The parameter-plane picture is not used as the obstruction proof. |
| `7source_claude_1/references.bib` plus the full cited D2 obstruction cluster | `references.bib` | Deduplicated standalone bibliography. Added Becker 1993, Ritt, Moore, Boshernitzan–Rubel, Rubel, Fernandes, Di Vizio–Fernandes, Aschenbrenner–Bergweiler, Hardouin–Singer, and Nishioka entries. |
| `7source_claude_1/figures/`, `Koenigs_details/figures/`, `Koenigs_details/pictures/` | `figures/` | Local copies of product/search/Koenigs/conjugacy/Mandelbrot-context assets used by A. |

### Chapter A claim hygiene

- Proved: for every fixed `r∈(0,1)`, the dynamical-variable function `z↦ψ_r(z)` is hypertranscendental over `C(z)` and therefore not elementary.
- Not proved: irrationality or transcendence of any particular value `A(p_0)`.
- Not proved: non-elementarity or differential transcendence of the parameter map `p↦A(p)`.
- The Becker–Bergweiler 1993 values theorem is explicitly explained not to transfer to the attracting Koenigs value problem.
- The PSLQ study is reported as finite-height negative evidence only. The source record’s digit and test counts are retained, but scripts and pipelines are not shipped in this phase.

## Deliberately omitted or deferred

| Source / content | Reason |
|---|---|
| `7source_claude_1/sections/06_constant_A.tex` in Chapter M | Locked clean split: all deep discrete-constant theory belongs to Chapter A. |
| Softer Becker–Bergweiler / Mandelbrot-only proof language in the original `claude_1` Koenigs subsection | Replaced by the structural attracting-vs-repelling theorem from `Koenigs_details`. |
| Full GW/critical-lifetime front matter from `Koenigs_details/Galton_Watson_A.tex` | Chapter A leans on M; duplicating it would create a second GW chapter. |
| `A_Koenigs_Chapter/` | Superseded obstruction wording; not used as a master. |
| `CC_C2_short_A/` | Seed/short draft is dominated by the full base and contains application-led voice not wanted here. |
| `Grok_planned_no_koen/` Path A/B/C, checkpoints and TODO scaffolding | Draft metadata rather than thesis prose. |
| Host/pathogen-led passages from short/Grok drafts | Locked abstract mathematical voice. |
| `7source_codex_1/scripts/` and all verification/PSLQ pipelines | Locked prose-only Pass 1; no scripts directory shipped. |
| `7source_codex_1/appendices/B_hypergeometric_integral.tex` and `C_coefficient_extraction.tex` as separate copies | Their substantive identities are already present in M’s base appendices, with the richer parameter-regular and coefficient-recovery material merged into the MoC body. Duplicate appendices were not added. |
| Multi-type GW sketch | Optional stretch only; deferred to the later structural/multi-type context to avoid an isolated pointer. |
| Random walks, Poisson-process expansion, logistic speciation, coupled ODE–CTMC section | Pass-2-only outline additions; the repository survey found no substantive source blocks for the genuinely new models. Pass 1 does not implement them. |
| Final literary rewrite, humanizer pass, or length cut | Explicitly outside this phase. |

No Tier-1 formula from the governing merge map remains unplaced. Repeated derivations were omitted only where the same mathematical content was already retained in the owning chapter.

## Build and visual QA

Commands run in each standalone project:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Final build results:

- Chapter M: success, 36 pages, no unresolved citations/references or multiply defined labels.
- Chapter A: success, 26 pages, no unresolved citations/references or multiply defined labels.
- Final logs were scanned for unresolved references/citations, multiply defined labels and catastrophic boxes.
- Both PDFs were rendered page-by-page with Poppler. Contact-sheet inspection covered every page and found no clipped text, overlapping floats, missing glyphs, broken figures or unreadable tables.

## Quality gates G1–G10

- [x] **G1** Both standalone PDFs compile with `latexmk -pdf -halt-on-error`.
- [x] **G2** M contains preliminaries, full GW, conditioning, small populations, CT BDC definition/PDE, full MoC ladder, synthesis and appendices.
- [x] **G3** M contains no full product/series/Koenigs/BB/PSLQ development.
- [x] **G4** M derives `A_c(p)` in basic detail and forward-references discrete `A(p)` theory to A.
- [x] **G5** A contains product, series, bounds, near-critical theorem, discrete/continuous comparison, search, Koenigs identity, hypertranscendence theorem, scope taxonomy, PSLQ prose, practical computation, conclusion and elementary cases.
- [x] **G6** Obstruction claims match the `Koenigs_details` authority and preserve the function/value/parameter distinction.
- [x] **G7** Abstract mathematical voice is used throughout both chapters.
- [x] **G8** No verification scripts are shipped.
- [x] **G9** Frozen notation is respected: `Z_n`, `S_n`, `A(p)`, `A_c(p)`, `ε`, `r=2p`, `ψ_r`; labels use `m:` and `a:` prefixes.
- [x] **G10** This log records harvested, omitted and deferred content.

## Known next-phase work

Pass 2 may restructure Chapter M according to `SECOND_PASS_CHAPTER_M_OUTLINE.md`, compress the full GW/QSD/small-population/MoC bulk, and create honest stubs for genuinely missing source material. That restructuring has not been started here. Chapter A remains the sole owner of product, series, bounds, Koenigs, hypertranscendence and PSLQ content.

---

# Pass 2 — Chapter M framework-and-methods restructure

Date: 2026-08-06  
Scope: `merged/chapter_M_math_intro/` only, plus this appended provenance record. Chapter A was not edited.

## Implemented architecture

Chapter M now follows the locked Pass 2 order:

1. Overview.
2. Markov Chains.
   - Discrete-Time Markov Chains: simple-random-walk source-gap stub; compressed Galton–Watson definition, PGF iteration, mean and survival recursion.
   - Continuous-Time Markov Chains: exponential holding-time/generator setup; Poisson source-gap stub; birth–death and birth–death–catastrophe process definitions.
   - Time-Inhomogeneous Processes: logistic-speciation source-gap stub.
   - Coupled ODE–CTMC Systems: conceptual interface and source-gap stub.
3. Methods for Markov Chains.
   - Discrete-Time Methods: PGFs, first-step analysis, light `A(p)` definition and forward reference to Chapter A.
   - Continuous-Time Methods: forward/backward equations, mean, variance/higher-moment method, hitting probabilities, extinction probabilities, and a detailed conditional-mean derivation of `A_c(p)`.
   - Method of Characteristics: one accessible absorption–death worked example.
4. Appendix A: compressed absorption-only and absorption–birth–death catalogue plus coefficient extraction.

The compiled inputs are `sections/01_overview.tex`, `02_markov_chains.tex`, `03_methods.tex`, and `04_extended_absorption.tex`. `OUTLINE_PASS2.md` records these files and their Pass 1 donors. The original Pass 1 section files remain in `sections/` as an uncompiled source archive so that compressed material is recoverable.

## Disposition of Pass 1 bulk

| Pass 1 material | Pass 2 disposition |
|---|---|
| Full GW extinction phase portrait, critical lifetime and Catalan total-progeny calculations | Compressed out of the main chapter; retained in the uncompiled Pass 1 donor file. The process survey keeps only the definition, PGF iteration, mean and survival recursion. |
| Full discrete QSD mean/variance derivation and Riccati heuristic | Replaced by the method-level definition of `A(p)` and the limiting conditional mean `1/A(p)`. Deep discrete theory remains a forward reference to Chapter A. |
| Early generations, cohort-size plots, apparent early growth, and discrete catastrophe/Jensen calculation | Compressed out of the framework chapter; the CT BDC definition and the warning about population-dependent catastrophe exposure are retained. |
| Full three-model MoC ladder | Absorption–death is the sole main-text worked example. Absorption-only and absorption–birth–death are compressed into Appendix A, using the parameter-regular convolution formula for the latter. |
| Hypergeometric identity and detailed resonance/domain discussion | Not re-expanded in Pass 2; preserved in the uncompiled Pass 1 donor files. |
| Synthesis/outlook | Folded into the Overview and method hand-offs. |

## Source-gap TODOs

The repository survey found no substantive source block for the following requested additions. Each heading is present in Chapter M, but the chapter explicitly declines to fabricate a model or citation.

- **TODO M-RW:** supply author-approved notes or references for simple random walks, then add the transition law and any desired hitting/gambler’s-ruin example.
- **TODO M-POISSON:** supply an approved Poisson-process source; the current text retains only the supported exponential holding-time and competing-clock interface.
- **TODO M-LOGISTIC:** supply the logistic speciation state space, time-dependent rates, parameter definitions and citations.
- **TODO M-COUPLED:** supply a concrete thesis ODE–CTMC model, its ODEs, CTMC rate functions and coupling direction(s).
- **TODO M-CTVAR:** if an explicit closed-form continuous-time birth–death variance is desired, supply or approve a source. Pass 2 currently introduces variance and higher moments through PGF derivatives and the moment hierarchy, without inventing an unsourced formula.

## Chapter interface and ownership check

- M retains the binary notation `Z_n`, `S_n`, the recursion `S_{n+1}=2pS_n-pS_n^2`, the light definition `A(p)=lim S_n/(2p)^n`, and the limit `E[Z_n | Z_n>0] -> 1/A(p)`.
- M derives `A_c(p)=(1-2p)/(1-p)` from the exact continuous-time birth–death survival probability and the rate match `p=lambda/(lambda+mu)`.
- Product, series, bounds, near-critical theorem, Koenigs theory, hypertranscendence and PSLQ remain exclusively in Chapter A. No Chapter A file was modified.

## Pass 2 build and visual QA

- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`: **success** for Chapter M.
- Chapter M log scan: no unresolved citations/references, multiply defined labels, overfull boxes or package warnings.
- Chapter M final PDF: 14 pages. All 14 pages were rendered with Poppler and inspected; headings, equations, links, appendix numbering, margins and bibliography are legible, with no clipping, overlap or missing glyphs.
- Chapter A unchanged-build confirmation: `latexmk` reports `main.pdf` up to date; 26 pages; no warning patterns in the existing build log.
- Chapter A remained the owner of deep `A(p)` theory throughout Pass 2 and no file under `chapter_A_constant_Ap/` was modified.

---

# AA flow-lucid prose pass

Date: 2026-08-06  
Scope: all compiled Pass 2 inputs in `chapter_M_math_intro/` and all compiled section and appendix inputs in `chapter_A_constant_Ap/`. The uncompiled Pass 1 donor archive in Chapter M was left unchanged.

## Editorial treatment

- Rewrote at paragraph and section grain for continuous academic flow, laddered technical density, stable mathematical names and British English.
- Improved transitions across the process-to-methods sequence in M and the product-to-obstruction sequence in A.
- Preserved the mathematics, theorem scope, equations, citations, labels, figures, chapter ownership and explicit source-gap stubs.
- Did not add new mathematics, deepen `A(p)` theory in M, alter the Pass 2 structure, or perform a separate voice-matching/humanizer pass.

## Build and visual QA

- Chapter M: `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` succeeded; 14 pages.
- Chapter A: `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` succeeded; 26 pages.
- Final log scans found no LaTeX/package warnings, unresolved citations or references, multiply defined labels, overfull or underfull boxes, or fatal errors.
- Both PDFs were rendered page-by-page and inspected. No clipping, overlap, missing figures, missing glyphs or unreadable material was found.

---

# Chapter M figure enhancement

Date: 2026-08-06  
Scope: `merged/chapter_M_math_intro/` only.

- Added a TikZ overview diagram linking the discrete Galton--Watson and continuous-time birth--death analytical lanes to their principal methods and conditional-mean constants.
- Added a TikZ local transition diagram for the birth--death--catastrophe chain.
- Added a PGFPlots illustration of survival, the unconditional mean and the conditional mean for the already-derived example $\lambda=1$, $\mu=3/2$.
- All figures visualise equations already present in Chapter M; no new process, theorem, citation or mathematical claim was introduced.

## Additional explanatory figures

Date: 2026-08-07  
Scope: `merged/chapter_M_math_intro/` only. Chapter A was not edited.

- Added `figures/generated/gw_regime_diagnostics.pdf`, a three-panel vector
  comparison of the subcritical amplitude, critical `n S_n -> 2` scaling and
  supercritical positive survival fixed point. The curves are direct iterations
  of the existing binary survival recursion.
- Added `figures/generated/founder_cohort_survival.pdf`, a two-panel vector
  comparison of exact `k`-founder survival and the shared critical asymptotic
  `S_n^(k) ~ 2k/n`.
- Added a TikZ killed-chain schematic separating sub-probability evolution,
  absorbed mass, renormalisation and the quasi-stationary eigenrelation.
- The Python generation was a one-off build action; no plotting or verification
  script was added to the chapter project.
- Recompiled with `latexmk -pdf -halt-on-error`; the final log and all rendered
  pages were checked for float order, clipping, legibility and broken references.

---

# Chapter M content restoration after Pass 2

Date: 2026-08-07  
Scope: `merged/chapter_M_math_intro/` only, plus this provenance entry. No file
under `merged/chapter_A_constant_Ap/` was modified.

## Orphan repair

The four-file Pass 2 build had left eight Pass 1 files beside the compiled files
in `sections/`, where their uncompiled status was silent. Their usable material
was mined into the Pass 2 structure. The originals were then moved, unchanged, to
`chapter_M_math_intro/sections_pass1/`:

- `01_introduction.tex`
- `02_preliminaries.tex`
- `03_galton_watson.tex`
- `04_conditioning.tex`
- `05_small_populations.tex`
- `06_method_of_characteristics.tex`
- `07_synthesis.tex`
- `08_appendices.tex`

Every file remaining in `sections/` is now input by `main.tex`:
`01_overview.tex`, `02_markov_chains.tex`, `03_methods.tex`,
`04_extended_absorption.tex`, and the new `05_branching_details.tex`.

## Restored mathematical content

| Restored block | Compiled destination | Provenance |
|---|---|---|
| Critical binary GW survival `S_n ~ 2/n`, with reciprocal-increment proof | Main summary in `02_markov_chains.tex`; proof in `05_branching_details.tex` | Pass 1 `03_galton_watson.tex`, strengthened with the rigorous argument in `7source_codex_1/sections/03_galton_watson.tex` |
| Extinction-time mass `P(T=n+1) ~ 2/n^2` | `05_branching_details.tex` | Same critical recursion and Codex proof upgrade |
| Exact Catalan total-progeny law and `k^{-3/2}` asymptotic | `05_branching_details.tex` | `7source_codex_1/sections/03_galton_watson.tex`; existing local power-law figure retained |
| Limiting conditional variance | Main statement in `03_methods.tex`; derivation in `05_branching_details.tex` | Pass 1 `04_conditioning.tex`, based on `7source_claude_1/sections/04_quasi_stationarity.tex` with Codex claim hygiene |
| Early survival probabilities, `k`-founder cohort survival and push of the past | Main summary in `02_markov_chains.tex`; detail and TikZ cohort plot in `05_branching_details.tex` | Pass 1 `05_small_populations.tex`; `7source_claude_1/sections/05_small_populations.tex` and `7source_codex_1/sections/05_small_populations.tex` |
| Deterministic rupture, exact random-exposure calculation and Jensen lower bound | Main bridge in `02_markov_chains.tex`; full calculation in `05_branching_details.tex` | Pass 1 `05_small_populations.tex` and the corresponding Claude/Codex source blocks |

## Technical-depth restoration

- The Pass 2 top-level order remains exactly **Overview / Markov Chains /
  Methods for Markov Chains**.
- Birth--death is again the principal continuous-time example: the process block
  now includes infinitesimal transitions, generator action, independent founder
  families, embedded jump chain, PGF derivation/recovery and a TikZ state diagram;
  its analysis continues throughout the six-page continuous-time methods block.
- Continuous-time methods now span six physical PDF pages and include the
  semigroup derivation of forward/backward equations, generator observables,
  factorial moments, hitting probabilities and transforms, extinction by backward
  and characteristic methods, conditional means, `A_c(p)`, killed-semigroup
  conditioning and a method-selection table.
- The method of characteristics now spans five physical PDF pages in the main
  text. It retains one complete absorption--death example, an explicit
  characteristic workflow, a TikZ geometry diagram, coefficient/moment checks and
  an independent finite-state check. The wider absorption catalogue remains in
  Appendix A.
- Appendix B contains the restored GW, conditional-variance, small-population and
  rupture detail, keeping the main process survey compact.

## Ownership and exclusions

The Chapter M interface is unchanged. M develops `A_c(p)` in detail, defines
discrete `A(p)` only through its survival-amplitude and conditional-moment roles,
and forwards the deeper theory to Chapter A. Product and series representations,
bounds, Koenigs theory, hypertranscendence and PSLQ remain outside M. The
random-walk, Poisson, logistic-speciation and coupled ODE--CTMC source-gap stubs
remain honest stubs because no approved substantive source material was found.

## Restoration build and visual QA

- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`: **success**.
- Final Chapter M PDF: 28 pages (restored from the defective 14-page build).
- Final log scan: no LaTeX/package warnings, unresolved citations or references,
  multiply defined labels, overfull/underfull boxes, or fatal errors.
- All 28 pages were rendered with Poppler and inspected in contact sheets; the new
  birth--death, characteristic-geometry and small-founder TikZ figures and the
  retained PGFPlots/critical-law figures were also inspected at full-page scale.
  No clipping, overlap, missing glyphs, broken references or unreadable material
  was found.
