# Merge map: two chapters from CH2 Versions

**Status:** merge map + user decisions locked (see §0A).  
**Base manuscript:** `7source_claude_1/`  
**Goal:** absorb *everything worth keeping* from the reviewed drafts into two unrestricted-length chapters:

1. **Chapter M — Mathematical introduction**  
2. **Chapter A — The constant \(A(p)\), Galton–Watson quasi-stationarity, and the Koenigs obstruction**

Later phases (out of scope for this map): refinements, additions, full structural rewrite to final form.

---

## 0A. User decisions (locked 2026-08-06)

| Question | Decision |
|---|---|
| Self-containment of Chapter A | **Lean on M.** Short setup recap only; full GW/QSD development lives in M. Sequential thesis reading assumed. |
| \(A(p)\) footprint in Chapter M | **Custom:** include **basic details beginning with \(A_c(p)\)** (continuous-time closed form where available), then **forward-reference** that discrete \(A(p)\) is developed in the next chapter. Do not deep-dive product/series/Koenigs in M. Still define discrete \(A(p)\) lightly where QSD needs the symbol (mean \(1/A(p)\)), without analytic development. |
| Framing voice | **Abstract mathematical** (claude_1/2 style). No host/pathogen-led narrative. |
| Packaging | **Two standalone projects** under `merged/` (each compiles alone). |
| Scripts / PSLQ reproducibility | **Prose only for now.** No verification scripts in merge phase. PSLQ/search material may appear as mathematical prose/evidence narrative from sources; do not require runnable pipelines. |

---

## 0. Design principles for the merge

1. **Base first.** Structural spine, notation hygiene, abstract voice, and most prose come from `7source_claude_1` unless a source is explicitly preferred below.
2. **No intentional loss of good content.** Prefer inclusion over compression. Optional depth goes in appendices or clearly marked advanced subsections, not the bin.
3. **Clean split.** Chapter M builds the probabilistic and analytic toolkit and uses \(A(p)\) as a *named object*. Chapter A owns all deep analysis of \(A(p)\), closed-form search, Koenigs linearisation, hypertranscendence, and inverse-symbolic evidence.
4. **Interface, not duplication of bulk.** A short bridge (definition + forward/back pointer) is required on both sides of the cut; full proofs of product/series/Koenigs/BB live only in Chapter A.
5. **Provenance is for the builder, not the reader.** Source tags below are instructions for the merging agent; the compiled chapters should read as original thesis prose, not a collage with attribution footnotes.
6. **Prefer abstract framing** from claude_1/claude_2 over host/pathogen bleed from `CC_C2_short_A` / parts of grok MoC, unless a modelling-adjacent remark is needed and marked as such.
7. **Engineering assets travel with the math they support.** Figures, tables, scripts, and verification notes are assigned with their sections.

---

## 1. Target chapter outlines (merged content inventory)

These outlines are *content maps*, not final section titles. The merging agent may renumber and retitle for flow.

### Chapter M — Mathematical introduction

| Target block | Content to include | Primary source | Merge-in / upgrades |
|---|---|---|---|
| **M.0 Front matter** | Title, abstract/opening remit, chapter roadmap | `7source_claude_1` intro rewritten for two-chapter role | Roadmap language from `7source_claude_2` intro; optional Path-style “what every reader needs” bullet from planned checkpoint (stripped of draft meta) |
| **M.1 Preliminaries / toolkit** | Exp clocks, memoryless, competing clocks **with proof**; CTMC + generator + Kolmogorov/master; uni/multi PGF; linear BD + PGF PDE + closed solution + \(p_0(t)\) derived | `7source_claude_1/sections/02_preliminaries.tex` | First-step vignette from `7source_grok_2` or planned; Gillespie remark keep short; codex compact CTMC phrasing only if clearer; multi-type PGF mention from `7source_codex_2` as *pointer only* |
| **M.2 Galton–Watson** | Binary death/division; mean \((2p)^n\); extinction certainty + phase portrait; critical \(S_n\sim 2/n\), \(\mathbb{E}[T]=\infty\), related exponents | `7source_claude_1/sections/03_galton_watson.tex` | Critical total progeny / Catalan material from `7source_codex_1` or short codex if not already present; “what is elementary vs not” punchline *one paragraph*, pointing to Chapter A |
| **M.3 Conditioning on survival (light \(A(p)\))** | Late survival scale; **definition** of \(A(p)\); limiting conditional mean \(1/A(p)\); conditional variance (second-moment derivation **in body** as in claude_1/grok_1); continuum/Riccati view; Yaglom existence **cited not overclaimed** | `7source_claude_1/sections/04_quasi_stationarity.tex` | Yaglom attribution care from `7source_codex_1`; modern QSD citations (Méléard–Villemonais; Collet–Martínez–San Martín) from claude provenance; **do not** move product/series/Koenigs proofs here — one sentence forward-ref to Chapter A |
| **M.4 Survival of small populations** | Early generations / \(S_n\) arithmetic; cohort of size \(k\); conditioning & apparent early growth (abstract ensemble framing); discrete BDC with full formulae + Jensen caveat; continuous-time BD + \(A_c(p)\); **CT BDC definition + PDE** | `7source_claude_1/sections/05_small_populations.tex` | Discrete rupture / killed-chain BDC eigenrelation from `7source_codex_1` § small pops (add, do not replace CT BDC def); “catastrophe is not mean-field hazard” caution from short codex; early-\(S_n\) figure material from claude_2 if better |
| **M.5 Absorption models & method of characteristics** | Abs-only; abs-death; MoC check on abs-death; abs-birth-death closed form; figures | `7source_claude_1/sections/07_method_of_characteristics.tex` | From `7source_codex_1/sections/07_characteristics.tex`: parameter-regular representation, hypergeometric domains/resonance, recovering state probabilities subsection; keep abstract compartment language; numerical master-equation check claim from grok_1 if still valid |
| **M.6 Synthesis / what carries forward** | What toolkit is now available; what is withheld for later modelling chapters; pointer to Chapter A for deep \(A(p)\) | `7source_claude_1` summary + `7source_claude_2` outlook open questions **that belong to M** (QSD under neither extinction nor rupture; Jensen BDC tightness) | Exclude pure value-transcendence open questions (those belong in Chapter A) |
| **M.App** | Hypergeometric integral identity; coefficient extraction for absorption models | `7source_claude_1/sections/09_appendices.tex` | Strengthen with `7source_codex_1/appendices/B_*.tex` and `C_*.tex` where fuller |

**Explicitly *not* bulk content of Chapter M:** GA closed-form catalogue, full two-sided bounds proofs for \(A\), near-critical asymptotic proof, Koenigs identity proof, Becker–Bergweiler, PSLQ, Mandelbrot cardioid deep dive, elementary \(r=2,4\) derivations (except a one-line mention if needed for curiosity).

**Minimal \(A(p)\) footprint in M (required):**
- Definition \(A(p)=\lim S_n/(2p)^n\)
- Conditional mean \(1/A(p)\)
- One numerical/plot of conditional mean vs \(p\) if already available
- Sentence: deep analysis, product/series, and non-elementarity discussion → Chapter A

---

### Chapter A — \(A(p)\), quasi-stationary amplitude, Koenigs obstruction

| Target block | Content to include | Primary source | Merge-in / upgrades |
|---|---|---|---|
| **A.0 Front matter** | Abstract-style remit; standing assumptions (\(p\in[0,1/2)\), binary GW); dependence on Chapter M (or self-contained recap — *see open questions*) | New framing; tone of `Koenigs_details` abstract + claude honesty | — |
| **A.1 Standing setup (short)** | Binary GW, \(S_{n+1}=2pS_n-pS_n^2\), definition of \(A(p)\), conditional mean \(1/A(p)\), existence of limit | Short recap from claude_1 QSD + `Koenigs_details` § limiting conditional mean | Keep short: this is not a second GW chapter |
| **A.2 Infinite product** | Logistic substitution; product formula; convergence; “is this an advance?” | `7source_claude_1/sections/06_constant_A.tex` product | Product tail bracket / certified intervals from `7source_codex_1` if stronger |
| **A.3 Series and bounds** | Exact series \(1/A=1+\sum(2p)^n/(2-S_n)\); two-sided bounds; \(A>\tfrac12 A_c\); parity bound; numerical table | claude_1 § series/bounds | Explicit \(A_c/2 < A < A_c\) packaging from codex_2 if cleaner; keep all proofs in body or app, not dropped |
| **A.4 Near-critical asymptotics** | \(A\sim 2(1-2p)\); gradient \(-4\) diagnostic; rate-of-approach remark | claude_1 § asymptotic | **Upgrade:** near-critical theorem with remainder \(O(\varepsilon\log(1/\varepsilon))\) from `7source_codex_1` |
| **A.5 Discrete vs continuous constants** | \(A\) vs \(A_c\); endpoint interpretations; competing-clocks link to \(p=\lambda/(\lambda+\mu)\) | claude_1 § compare | Competing-clocks justification already proved in M — cite, do not re-prove |
| **A.6 Closed-form search (negative evidence, informal)** | Symbolic regression / GA narrative; \(\hat A_i\) candidates; critical-slope kill criteria | claude_1 § GA | Quarantine “exploratory formulae” detail into appendix from `7source_codex_1/appendices/A_closed_form_search.tex`; drop autobiographical asides already cut in provenance note |
| **A.7 Koenigs identification** | Definition of Koenigs/Schröder function; proof \(A(p)=2\psi_r(1/2)\); logistic \(\leftrightarrow z^2+c\) conjugacy figure | claude_1 § Koenigs | Identity packaging from Koenigs_details §4; basin/germ radius remark from Koenigs_details |
| **A.8 Hypertranscendence / no elementary conjugacy** | Definitions (DA / hypertranscendence / elementarity); BB theorem precise statement; **theorem: no exceptional \(r\in(0,1)\)**; attracting vs repelling; elementary cases \(r=2,4\) located in classification | **`Koenigs_details`** §§5.1–5.3, App A.4 | Replace softer “parameter avoids \(c\in\{0,-2\}\)” sole argument from claude_1 with D2 structural proof; keep Mandelbrot figure only as pedagogical consistency check, not as proof |
| **A.9 Scope: what is and is not proved about \(A(p)\)** | Taxonomy: (function of \(z\)) / (values \(A(p_0)\)) / (map \(p\mapsto A(p)\)) / (DA in \(p\)); BB 1993 non-transfer; Hardouin–Singer non-applicability note | **`Koenigs_details`** §5.4 + working claim | Align chapter-language honesty with D2; drop overselling in first-try A_Koenigs abstract |
| **A.10 Inverse-symbolic / PSLQ evidence** | 11 rationals; dual high-precision routes; battery of null tests; explicit “evidence not proof” | **`Koenigs_details`** §5.5 | Include if scripts/logs available or describe as archived; if not reproducible in-repo, keep as reported evidence with provenance note in builder log |
| **A.11 Practical computation** | Hybrid product / near-critical splice recipe | claude_1 § practical + Koenigs_details practical | codex certified product iteration notes |
| **A.12 Conclusion** | Usable conclusions for the thesis; open problems proper to this chapter | Koenigs_details conclusion + claude_2 value-transcendence open Q | — |
| **A.App** | Elementary Koenigs at \(r=2,4\); affine conjugacy; BB classification placement; optional closed-form search catalogue; optional conjugacy/Mandelbrot extras | `Koenigs_details` App + `7source_codex_1` App A | Figures from Koenigs_details / IMG_ch3 |

**Explicitly *not* bulk content of Chapter A:** full MoC absorption ladder, CTMC toolkit, multi-compartment models (except if a sentence uses \(A(p)\) later).

---

## 2. Source-by-source disposition

| Source | Role in merge | Harvest | Deprioritise / discard as master |
|---|---|---|---|
| **`7source_claude_1`** | **Primary base for Chapter M**; primary for product/series/GA prose in A until upgraded | Almost everything except deep Koenigs claim language (upgrade from D2) | — |
| **`7source_claude_2`** | Parallel rewrite; prose & outlook donor | Intro/tools phrasing; early-generations subsection; “What carries forward” research questions (split M/A) | Do not use as structural master if it conflicts with claude_1 |
| **`7source_codex_1`** | Best engineering + some stronger theorems | Near-crit remainder; MoC resonance/regular form; killed BDC; apps B/C; verification scripts; closed-form app quarantine | Sparser prose should not overwrite claude narrative wholesale |
| **`7source_codex_2`** | Condensed alternate order | Multi-type GW *sketch*; framework-first CT Yaglom phrasing; weighted catastrophe PGF; synthesis bullets | Not self-contained; no figure path dependency in final build |
| **`7source_grok_1`** | Strong formal mid-draft | Formal def/prop density in prelims if claude is too essayistic; MoC numerical check claim | Superseded length/polish by grok_2/claude |
| **`7source_grok_2`** | Near-duplicate of short_A + prelims | First-step subsection; any clearer sentence-level polish on shared core | Host/pathogen MoC framing |
| **`CC_C2_short_A`** | Seed kernel | Only if a formula/figure is missing elsewhere | No prelims; applied bleed; visualiser kit footnote |
| **`codex_1` / `codex_2`** | Short background twins (sources ≈ identical) | Occasional clearer short explanations; generated figure ideas (`gw_survival_regimes`, etc.) if useful | Not full-depth masters; do not treat PDFs as two designs |
| **`Grok_planned_no_koen`** | Architecture donor only | Checkpoint bullet list; “exit contract” into MoC; honest scope phrasing | Path A/B/C meta, TODOs, pending MoC verification stance, thin \(A(p)\) body |
| **`Koenigs_details`** | **Primary upgrade for Chapter A obstruction core** | HT theorem pipeline; scope taxonomy; PSLQ; BB precise statement; appendix integrable cases | Informal GW front (typos, GA long form) — prefer claude for shared front where overlapping |
| **`A_Koenigs_Chapter`** | Intermediate specialist | Only if a derivation is clearer than D2 (unlikely) | Soft NCF claim language; superseded |
| **`becker_bergweiler_note.pdf`** | Builder reference | Scope checklist (A proved / B,C open) | Not chapter prose |

---

## 3. The cut between M and A (interface contract)

### What Chapter M *must* hand to Chapter A
- Binary GW notation \(Z_n\), \(p\), offspring PGF \(\phi(z)=pz^2+(1-p)\)
- Survival \(S_n=\mathbb{P}(Z_n>0)\), recursion \(S_{n+1}=2pS_n-pS_n^2\)
- Definition and existence of \(A(p)\), and \(\mathbb{E}[Z_n\mid Z_n>0]\to 1/A(p)\)
- Continuous-time comparison constant \(A_c(p)=(1-2p)/(1-p)\) *stated* (derivation may live in M small-pops or BD section)
- Competing-clocks justification of \(p=\lambda/(\lambda+\mu)\) already available by citation

### What Chapter A *must not* assume without stating
- Reader has seen product/series/Koenigs before (A develops them)
- Any result about hypertranscendence (A proves/cites carefully)
- Modelling chapters’ applied interpretation

### Cross-references (builder conventions)
- Labels: prefer namespaced labels `chM:...` and `chA:...` or thesis-global unique labels; never reuse bare `sec:Ap` in both.
- First mention of deep \(A(p)\) in M: “Chapter~\ref{ch:Ap}”.
- First setup recap in A: “as in Chapter~\ref{ch:math-intro}” (or self-contained paragraph if chapters must stand alone — *open question*).

---

## 4. Figures, tables, scripts — assignment

| Asset class | Goes to | Source locations |
|---|---|---|
| GW visualisation, phase/power-law, early \(S_n\), \(k\)-cohort, dt vs ct \(A\), abs1/abs2 | **Chapter M** | `7source_claude_1/figures/`, codex generated figures if kept |
| Conditional mean vs \(p\), \(A(p)\) table, period-double, \(A_3\) hat plot | **Chapter A** (mean plot may also appear lightly in M) | claude_1 / IMG_ch3 |
| Koenigs linearisation, parameter conjugacy, Mandelbrot context | **Chapter A** | Koenigs_details / claude figures |
| `scripts/` algebra, PGF, numerics checks | **Repo tooling for both**; document which chapter’s claims they underwrite | `7source_codex_1/scripts/` |
| Closed-form / PSLQ logs | **Chapter A** builder appendix or `artifacts/` | Koenigs_details provenance; recreate if missing |

---

## 5. Bibliography disposition

| Cluster | Chapter |
|---|---|
| Norris, Karlin–Taylor, Kendall 1948, Gillespie, Athreya–Ney, Méléard–Villemonais, Collet–Martínez–San Martín, NIST handbook | **M** (and A only if cited) |
| Koenigs 1884; Becker–Bergweiler 1993, 1995; Ritt; Fernandes; Di Vizio–Fernandes; Hardouin–Singer; Milnor; Rubel; etc. | **A** primary |
| Shared branching classics | Both if both cite |

Merge `references.bib` entries; deduplicate keys; preserve verification notes on BB hypotheses from claude provenance where still relevant — then update after D2 upgrade.

---

## 6. Notation conventions (freeze for merge)

Adopt **claude_1** cleaned notation as default:

| Object | Symbol |
|---|---|
| Population | \(Z_n\) (discrete), continuous as in claude |
| Offspring / one-step | \(L\) or as in claude (not overloaded \(\mathbf X\)) |
| Survival | \(S_n\) |
| Kolmogorov constant | \(A(p)\) |
| Continuous analogue | \(A_c(p)\) or \(A_{\mathrm{c}}(p)\) — pick one and stick |
| Near-critical gap | \(\varepsilon=1-2p\) (not overloaded \(r\)) |
| Logistic multiplier | \(r=2p\) |
| Koenigs function | \(\psi_r\) (or \(\Psi_r\)); state convention once |
| Catastrophe / absorption rates | as in claude_1 CT BDC def |

If codex uses “survival amplitude” language, prefer **constant \(A(p)\)** (claude) in headings; “amplitude” may appear once as synonym.

---

## 7. Quality gates for the merged drafts (for the implementing agent)

The merge is successful only if:

1. **No orphaned good content:** every Tier-1 item in this map appears in M or A (or a written “intentionally deferred to later refinement” log entry).
2. **No double bulk:** product/series/Koenigs/BB full development appears once (Chapter A).
3. **Interface works:** a reader of M alone can use \(1/A(p)\) and MoC; a reader of A alone understands \(A(p)\) after A.1 (depth of self-containment TBD).
4. **Claim hygiene on obstruction matches Koenigs_details**, not the softer first-try / pure parameter-plane story.
5. **Abstract voice** in M MoC and small-pops (no host-cell default).
6. **Builds:** two standalone `main.tex` (or thesis-integrable fragments) compile with local figures.
7. **Builder log:** `MERGE_LOG.md` listing every source file harvested and any content left behind with reason.

---

## 8. Suggested on-disk layout for the implementing agent

```text
CH2 Versions/
  merged/
    chapter_M_math_intro/
      main.tex
      sections/...
      figures/...
      references.bib
    chapter_A_constant_Ap/
      main.tex
      sections/...
      figures/...
      references.bib
    MERGE_LOG.md          # provenance of what went where
    MERGE_MAP_TWO_CHAPTERS.md  # this file
```

(Exact paths may change after open questions.)

---

## 9. Explicit non-goals of the merge phase

- Final literary rewrite / humanizer pass  
- Cutting for length  
- New mathematical results beyond what the sources already contain  
- Resolving open research questions listed in outlooks  
- Full thesis integration (numbering relative to other chapters) unless specified  

Those belong to later refinement and finalisation phases.

---

## 10. Quick “default decisions” if the user is silent later

Only for items not answered in Q&A; implementing agent should still prefer explicit answers.

1. Base prose: claude_1.  
2. Obstruction math: Koenigs_details.  
3. Near-crit remainder + MoC resonance: codex_1.  
4. CT BDC definition: keep in M from claude_1.  
5. Drop Path/checkpoint meta; keep a short mid-chapter toolkit recap in M if useful.  
6. Two standalone compileable projects under `merged/`.
