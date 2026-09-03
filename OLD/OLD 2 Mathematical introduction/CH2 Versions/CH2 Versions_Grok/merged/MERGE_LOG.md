# MERGE_LOG — two-chapter merge

**Workspace:** `CH2 Versions` (Grok working copy)  
**Pass 1 completed:** 2026-08-06  
**Base manuscript:** `7source_claude_1/`

---

## Deliverables

| Path | Status |
|---|---|
| `merged/chapter_M_math_intro/main.pdf` | Compiles (latexmk -pdf -halt-on-error) |
| `merged/chapter_A_constant_Ap/main.pdf` | Compiles (latexmk -pdf -halt-on-error) |
| `merged/NOTATION.md` | Written |
| `merged/MERGE_LOG.md` | This file |

---

## 1. Source → destination (Pass 1)

### Chapter M — Mathematical introduction

| Destination | Primary source | Notes |
|---|---|---|
| `sections/01_introduction.tex` | claude_1 `01_introduction.tex` | Rewritten for two-chapter role; deep \(A(p)\) deferred to \(\ChA\) |
| `sections/02_preliminaries.tex` | claude_1 `02_preliminaries.tex` | + first-step vignette (new short subsection) |
| `sections/03_galton_watson.tex` | claude_1 `03_galton_watson.tex` | + Catalan total progeny; + elementary-vs-not remark → \(\ChA\) |
| `sections/04_conditioning.tex` | claude_1 `04_quasi_stationarity.tex` | Light \(A(p)\); product/series/practical refs stripped → \(\ChA\); Yaglom citation care |
| `sections/05_small_populations.tex` | claude_1 `05_small_populations.tex` | \(\Ac(p)\) full detail; discrete \(A(p)\) contrast → \(\ChA\); + killed-chain BDC eigenrelation + catastrophe≠mean-field remark (codex_1) |
| `sections/06_method_of_characteristics.tex` | claude_1 `07_method_of_characteristics.tex` | + parameter-regular / resonance note (codex_1) |
| `sections/07_synthesis.tex` | claude_1 `08_summary.tex` + claude_2 outlook (M-scope) | No product/Koenigs bulk; open Qs split M vs A |
| `sections/08_appendices.tex` | claude_1 `09_appendices.tex` | Hypergeometric + coefficient extraction |
| `figures/IMG_ch3/*` | claude_1 figures | GW, conditional mean, k-cohort, abs1/2, dtctA, power law |
| `references.bib` | claude_1 | Prob/branching/QSD core |

**Explicitly NOT in M:** `06_constant_A.tex` (entire file → Chapter A only).

### Chapter A — The constant \(A(p)\)

| Destination | Primary source | Notes |
|---|---|---|
| `01_introduction.tex` | New framing | Remit + honesty; cites Becker–Bergweiler for HT |
| `02_setup_recap.tex` | claude_1 QSD + short recap | 1–2 pages; leans on \(\ChM\) |
| `03_product.tex` | claude_1 `06` product subsection | Labels `a:` |
| `04_series_bounds.tex` | claude_1 `06` series/bounds | Full proofs retained |
| `05_near_critical.tex` | claude_1 asymptotic + **codex_1** remainder packaging | Theorem with \(O(\varepsilon\log(1/\varepsilon))\) |
| `06_discrete_vs_continuous.tex` | claude_1 compare | + dtct figure local copy |
| `07_closed_form_search.tex` | claude_1 GA | Soft BB claim language not used as proof |
| `08_koenigs_identity.tex` | claude_1 Koenigs identity | Soft BB “avoids \(c\in\{0,-2\}\)” **replaced** by pointer to HT section |
| `09_hypertranscendence.tex` | **Koenigs_details** §§ DA/BB/HT | Full theorem pipeline, germ/basin remark |
| `10_scope_and_pslq.tex` | **Koenigs_details** §5.4–5.5 + working claim | Scope taxonomy; PSLQ prose only (no scripts) |
| `11_practical.tex` | claude_1 practical | Hybrid product / asymptotic |
| `12_conclusion.tex` | Koenigs_details conclusion adapted | Claim hygiene aligned with D2 |
| `app_elementary_cases.tex` | Koenigs_details App \(r=2,4\) | + classification placement |
| `app_closed_form_catalogue.tex` | codex_1 `A_closed_form_search.tex` | Quarantine exploratory formulae |
| `figures/` | claude_1 IMG_ch3 + Koenigs_details | Period double, conjugacy, Koenigs, Mandelbrot, A3 hat, dtct |
| `references.bib` | claude_1 + Koenigs_details HT cites | Becker1993, Ritt, Rubel, Fernandes, Hardouin–Singer, etc. |

---

## 2. Deliberately omitted (with reason)

| Content | Reason |
|---|---|
| Verification scripts / PSLQ pipelines | User lock: prose only this phase |
| Path A/B/C scaffolding, TODOs (`Grok_planned_no_koen`) | Draft meta, not thesis prose |
| Host/pathogen-led MoC framing (`CC_C2_short_A`, parts of grok) | Voice lock: abstract mathematical |
| `A_Koenigs_Chapter` as master | Superseded claim language; D2 preferred |
| Full product/series/Koenigs/BB/PSLQ in M | Interface contract: Chapter A owns these |
| Multi-type GW full development | Pointer only; later modelling chapters |
| codex_2 figure path `../Ch2_seed/...` | Broken external dependency |

---

## 3. Formulae from Tier-1 sources not placed

None identified. Near-critical remainder, killed BDC eigenrelation, Catalan total progeny, HT theorem, scope taxonomy, and PSLQ prose are all present.

---

## 4. Quality gates (Pass 1)

| # | Gate | Status |
|---|---|---|
| G1 | Both PDFs compile latexmk halt-on-error | **Pass** |
| G2 | M has prelims, GW, conditioning, small pops, CT BDC, MoC, synthesis, apps | **Pass** |
| G3 | M has no full product/series/Koenigs/BB/PSLQ | **Pass** |
| G4 | M develops \(\Ac(p)\) in detail; light \(A(p)\) + forward ref | **Pass** |
| G5 | A has product, series, bounds, near-crit, compare, search, Koenigs id, HT, scope, PSLQ, practical, conclusion, elementary app | **Pass** |
| G6 | Claim hygiene (no false value-transcendence / map-elementarity theorems) | **Pass** |
| G7 | Abstract mathematical voice | **Pass** |
| G8 | No verification scripts shipped | **Pass** |
| G9 | Notation freeze (`\Ac`, \(\varepsilon\), \(r=2p\), labels `m:`/`a:`) | **Pass** |
| G10 | MERGE_LOG complete | **Pass** |

---

## 5. Known issues for later refinement (not fixed now)

- Minor hyperref duplicate-destination warnings in M appendices (custom Alph section renumbering).
- Pass-1 M is still claude_1-shaped (objects then applications); **Pass 2** redesign is separate (`SECOND_PASS_CHAPTER_M_OUTLINE.md`).
- No final literary rewrite / length cut.
- PSLQ evidence is prose-only; reproducibility scripts deferred.
- codex MoC resonance/domains full derivation compressed to a short note + existing rem:resonance; full catalogue remains in sources.
- Multi-type GW sketch from codex_2 not imported (optional stretch).

---

## 6. Cross-chapter interface

- M defines \(A(p)=\lim S_n/(2p)^n\), \(\ex{Z_n\mid Z_n>0}\to 1/A(p)\), develops \(\Ac(p)=(1-2p)/(1-p)\).
- M forward-refs product/series/bounds/Koenigs/HT/PSLQ to \(\ChA\).
- A setup recap is short; does not re-prove GW extinction or conditional variance.
- Macros: `\ChM`, `\ChA` in both preambles for standalone builds.

---

## Pass 2 — Chapter M redesign (2026-08-06)

**Governing doc:** `SECOND_PASS_CHAPTER_M_OUTLINE.md`  
**Scope:** restructure `merged/chapter_M_math_intro/` only; Chapter A unchanged.

### Target structure implemented

| § | Title | File |
|---|---|---|
| 1 | Overview | `sections/01_overview.tex` |
| 2 | Markov chains | `sections/02_markov_chains.tex` |
| 2.1 | DTMC: random walks (stub), GW (brief) | same |
| 2.2 | CTMC: clocks, generator, PGF, Poisson (stub), BD, BDC | same |
| 2.3 | Time-inhomogeneous / logistic speciation | **TODO stub** |
| 2.4 | Coupled ODE–CTMC | **TODO stub** (framework only) |
| 3 | Methods for Markov chains | `sections/03_methods.tex` |
| 3.1 | Discrete-time methods (first-step; pointer to Ch A / Koenigs) | same |
| 3.2 | Continuous-time methods via BD; conditional means + \(A_c\); light \(A(p)\) | same |
| 3.3 | MoC accessible + absorption–death worked example | same |
| App | Extended MoC (abs-only, ABD) + hypergeometric apps | `sections/04_appendices.tex` |

Pass-1 section files archived in `sections_pass1/` for provenance.  
Outline listing: `chapter_M_math_intro/OUTLINE_PASS2.md`.

### Compression / moves

| Pass-1 bulk | Pass-2 fate |
|---|---|
| Full GW critical theory, Catalan, phase portraits | Compressed to brief GW + remark “greater detail later”; full text in `sections_pass1/` |
| Full QSD variance derivation | Trimmed; conditional mean + \(A(p)\) light definition kept in §3.2 |
| Full MoC three-model ladder | Abs–death + MoC check in main §3.3; abs-only + ABD → appendix |
| Synthesis / outlook | Folded into §1 Overview |

### NEW blocks without repo sources (honest stubs)

| Block | Status |
|---|---|
| Simple random walks | Short definition + gambler’s-ruin teaser; `m:rem:rw-todo` |
| Poisson processes | Standard link to Exp clocks / pure birth; `m:rem:poisson-todo` |
| Logistic speciation | Structured placeholder; `m:rem:logistic-todo` |
| Coupled ODE–CTMC | Conceptual framework (i)–(iii); `m:rem:coupled-todo` |

**Do not invent models or citations** for these until notes are supplied.

### Interface preserved

- \(A_c(p)\) developed with basic detail in §3.2  
- Discrete \(A(p)\) defined lightly; deep theory remains Chapter A  
- No product/series/Koenigs/BB/PSLQ re-merged into M  
- Chapter A not modified in Pass 2  

### Compile

- `merged/chapter_M_math_intro/main.pdf` — Pass 2 structure, `latexmk -pdf -halt-on-error` clean (25 pp.; minor hyperref duplicate-destination warnings on Alph apps remain as in Pass 1)  
- `merged/chapter_A_constant_Ap/main.pdf` — unchanged role, still compiles  

### Verification (re-check after polish)

| Done criterion | Status |
|---|---|
| Structure matches SECOND_PASS §1 | **Yes** — Overview → MC (DT/CT/time-inhom/coupled) → Methods (DT brief / CT via BD / MoC + abs–death) → apps |
| Chapter compiles | **Yes** |
| Chapter A still owns deep \(A(p)\) | **Yes** — M has light \(A(p)\) + detailed \(\Ac(p)\) + forward refs only |
| MERGE_LOG Pass 2 | **Yes** (this section) |
| Honest stubs for N blocks | RW, Poisson (short defs); logistic speciation + coupled ODE–CTMC (TODO remarks) |
| No final literary humanizer pass | **Yes** |

### Small prose polish (same Pass 2 session)

- Removed builder meta from thesis body (“pass-1 source material”, “conditioning source notes”).  
- Stub remarks reworded: scope/TODO language, intentional content not fabricated.  
- Homogeneity sentence points to §2.3 instead of dangling `\fwd`.
