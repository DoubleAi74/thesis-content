# Implementation & writing plan — two merged chapters

**Audience:** the agent that will construct the chapters in this directory.  
**Governing documents:** `MERGE_MAP_TWO_CHAPTERS.md` (content inventory + source disposition) and this plan (how to execute).  
**Do not invent new mathematics** beyond what the sources already contain. **Do not run a final literary rewrite** — that is a later phase. This phase is a **full content merge** into two unrestricted-length, compilable chapters.

---

## 1. Locked product definition

### Deliverables

```text
CH2 Versions/merged/
  chapter_M_math_intro/
    main.tex
    sections/*.tex
    figures/          # local copies of required assets
    references.bib
    main.pdf          # build before handoff
  chapter_A_constant_Ap/
    main.tex
    sections/*.tex
    figures/
    references.bib
    main.pdf
  MERGE_LOG.md        # what was taken from where; what was left behind
```

### Locked decisions (user)

1. **Chapter A leans on Chapter M** — short setup recap only in A.  
2. **In M, \(A(p)\) treatment is light and pedagogically ordered around \(A_c(p)\) first**, then forward-ref to Chapter A for discrete \(A(p)\).  
3. **Abstract mathematical voice.**  
4. **Standalone projects under `merged/`.**  
5. **Prose only** — no scripts/PSLQ pipelines in this phase.

### Chapter roles (one sentence each)

- **M — Mathematical introduction:** probabilistic and analytic toolkit for the thesis (clocks, CTMC, PGF, branching, quasi-stationarity at the level needed to *use* limiting conditional laws, small populations, absorption/MoC).  
- **A — The constant \(A(p)\):** full theory of the discrete Kolmogorov constant, closed-form search, Koenigs identification, hypertranscendence obstruction, numerical/inverse-symbolic evidence, practical evaluation.

---

## 2. Working order (do not scramble)

Execute in this order. Later steps assume earlier ones exist on disk.

| Phase | Name | Done when |
|------:|---|---|
| 0 | Scaffold | Both project trees compile empty “Hello chapter” PDFs |
| 1 | Freeze notation & labels | `merged/NOTATION.md` written; label prefixes fixed |
| 2 | Build Chapter M spine from claude_1 | M has all M sections from base, compiles |
| 3 | Upgrade M from secondary sources | MoC resonance, killed BDC, first-step, etc. merged in |
| 4 | Apply M’s \(A(p)\) interface policy | M defines lightly + \(A_c\) first + forward-ref; no bulk A theory |
| 5 | Build Chapter A spine | A has full analytic + obstruction content, compiles |
| 6 | Upgrade A obstruction core from Koenigs_details | HT theorem, scope taxonomy, PSLQ *prose* |
| 7 | Cross-links, bibliographies, figures | Both PDFs clean; no missing figures |
| 8 | Quality gates + MERGE_LOG | Checklist in §8 all green |

**Do not** polish prose globally, humanize, or restructure beyond what is needed to merge cleanly. Prefer surgical stitches over rewrite.

---

## 3. Phase 0 — Scaffold

1. Create directory tree as in §1.  
2. For each chapter, copy a minimal preamble style from `7source_claude_1` (report or article — **prefer `report` with `\chapter` for thesis-likeness**, or `article` with top-level `\section`; pick one style and use it for **both** projects).  
3. Use:
   - `amsmath,amssymb,amsthm,mathtools`
   - `graphicx`, `booktabs`, `hyperref`, `cleveref`
   - theorem environments matching claude_1  
4. `\graphicspath{{figures/}}` local to each project.  
5. Compile once each.

**Title suggestions (agent may refine):**

- M: *Mathematical introduction* — subtitle *Branching, quasi-stationarity, and absorption models*  
- A: *The constant \(A(p)\)* — subtitle *Quasi-stationary amplitude, closed forms, and the Koenigs obstruction*

---

## 4. Phase 1 — Notation & label freeze

Write `merged/NOTATION.md` with the freeze from the merge map §6. Mandatory:

| Object | Symbol |
|---|---|
| Discrete population | \(Z_n\) |
| Survival probability | \(S_n\) |
| Kolmogorov constant | \(A(p)\) |
| Continuous analogue | \(A_{\mathrm{c}}(p)\) **(use this form everywhere)** |
| Near-critical gap | \(\varepsilon = 1-2p\) |
| Logistic multiplier | \(r = 2p\) |
| Koenigs function | \(\psi_r\) |

**Label prefixes:**

- Chapter M: `m:` e.g. `\label{m:sec:gw}`, `\label{m:eq:SnIter}`  
- Chapter A: `a:` e.g. `\label{a:prop:series}`, `\label{a:thm:ht}`  

Cross-chapter refs: use textual “Chapter~\ref{...}” only within a future combined thesis; for **standalone** builds, write  
`Chapter~[Mathematical introduction]` / `Chapter~[The constant \(A(p)\)]`  
or define `\newcommand{\ChM}{Chapter~M}` / `\ChA` in each preamble with a comment that thesis integration will replace these.

---

## 5. Phase 2 — Chapter M spine (from `7source_claude_1`)

### File map (suggested)

```text
sections/
  01_introduction.tex
  02_preliminaries.tex
  03_galton_watson.tex
  04_conditioning.tex      # was quasi_stationarity; retitle OK
  05_small_populations.tex
  06_method_of_characteristics.tex
  07_synthesis.tex
  08_appendices.tex        # or subappendices
```

### Copy-then-edit procedure

For each source file below, **copy** into the new section file, then apply renames (labels → `m:`), then apply listed edits.

| New file | Source | Immediate edits |
|---|---|---|
| `01_introduction.tex` | `7source_claude_1/sections/01_introduction.tex` | Rewrite roadmap for **two-chapter** thesis: this chapter = toolkit; **next** = full \(A(p)\). Remove implication that deep \(A(p)\) lives here. Keep two threads (conditioning; near-critical) but say near-critical *amplitude theory* is Chapter A. |
| `02_preliminaries.tex` | `.../02_preliminaries.tex` | Keep competing-clocks prop + linear BD closed form. |
| `03_galton_watson.tex` | `.../03_galton_watson.tex` | Keep critical case fully. End with optional one-paragraph “elementary vs not” pointer to Chapter A. |
| `04_conditioning.tex` | `.../04_quasi_stationarity.tex` | **Apply §6 interface policy** (below). Keep mean/variance development. |
| `05_small_populations.tex` | `.../05_small_populations.tex` | Keep CT BDC definition. Reorder comparison narrative per §6. |
| `06_method_of_characteristics.tex` | `.../07_method_of_characteristics.tex` | Abstract voice only. |
| `07_synthesis.tex` | `.../08_summary.tex` + claude_2 outlook (M-only questions) | Point forward to Chapter A and later modelling chapters. |
| `08_appendices.tex` | `.../09_appendices.tex` | Keep both apps. |

Copy required figures from `7source_claude_1/figures/` into `chapter_M_math_intro/figures/`.

Compile after spine is in place.

---

## 6. Chapter M — \(A(p)\) / \(A_{\mathrm{c}}(p)\) interface policy (user-specific)

This is the **most important content rule** for M.

### Required pedagogical shape

1. **In continuous-time birth–death (small populations / BD subsection):** develop survival and the **closed form**  
   \[
   A_{\mathrm{c}}(p)=\frac{1-2p}{1-p}
   \]
   (or equivalent \(\mu/(\mu-\lambda)\) form), with enough detail that the reader sees *why* a closed form exists in continuous time.  
2. **Then** introduce the discrete constant \(A(p)\) only at the level needed for quasi-stationarity:  
   \[
   A(p)=\lim_{n\to\infty}\frac{S_n}{(2p)^n},\qquad
   \mathbb{E}[Z_n\mid Z_n>0]\to\frac1{A(p)}.
   \]  
3. **Explicit forward reference:** the product representation, series, bounds, near-critical asymptotics, closed-form search, and Koenigs/hypertranscendence theory are **the subject of the next chapter** — not developed here.  
4. **Do not** include in M: infinite-product proof, series/bounds proofs, GA catalogue, Koenigs definition/proof, Becker–Bergweiler, PSLQ, practical hybrid splice (except a one-line “computable by iteration” if needed for a figure caption).

### Placement guidance

- **Option preferred:** In `04_conditioning`, define \(A(p)\) and mean/variance; say “structure of \(A(p)\) is Chapter A.” In `05_small_populations` continuous BD, give **full** \(A_{\mathrm{c}}\) and a short discrete-vs-continuous contrast that **starts from \(A_{\mathrm{c}}\)** and notes discrete \(A(p)\) lacks an elementary form (→ Chapter A).  
- If narrative flow is better, a brief preview sentence in the introduction is allowed.

### What to strip from claude_1 § `06_constant_A` when building M

**Do not input `06_constant_A.tex` into Chapter M at all.** That file is the primary donor for Chapter A.

---

## 7. Phase 3 — Upgrade Chapter M from secondary sources

Apply **additively**. Prefer insert subsections / paragraphs over rewriting claude prose.

| Upgrade | Source | Where in M | Rule |
|---|---|---|---|
| First-step analysis vignette | `7source_grok_2` or planned prelims | Preliminaries | Short; abstract |
| Critical total progeny / Catalan (if missing) | `7source_codex_1` GW | After critical lifetime | Include if not already equivalent |
| Yaglom existence cited carefully | `7source_codex_1` QSD | Conditioning | “Existence from classical Yaglom; we compute moments via \(A(p)\)” |
| Discrete rupture + killed-chain BDC | `7source_codex_1` small pops | After discrete BDC | **Add** eigenrelation material; keep claude CT BDC def |
| Catastrophe ≠ mean-field hazard | short codex | Small pops | One clear remark |
| MoC parameter-regular form + resonance + domains | `7source_codex_1` § characteristics | MoC abs-birth-death | Merge into ABD subsection or app |
| Coefficient / hypergeometric app enrichment | codex apps B,C | M appendices | Only if strictly richer |
| Outlook open questions (M-scope) | `7source_claude_2` outlook | Synthesis | QSD under neither extinction nor rupture; Jensen tightness — **not** value transcendence of \(A(p)\) |
| Early-generations subsection / figure | `7source_claude_2` small pops | Small pops | If better than claude_1 alone |
| Checkpoint-style toolkit list | planned § checkpoint | End of small pops or start of MoC | **Strip** Path/TODO language; ½ page max |

### Voice filter (mandatory on every upgrade)

- Remove host/pathogen-led wording from short_A / grok MoC.  
- Replace with compartment / particle / population language consistent with claude_1.  
- Drop visualiser HTML footnotes and kit paths.

### Do **not** import into M

- Path A/B/C scaffolding  
- Full `06_constant_A` / Koenigs_details  
- Verification scripts  
- codex_2 figure path `../Ch2_seed/...`

Compile M after upgrades.

---

## 8. Phase 4 — Chapter A spine

### File map (suggested)

```text
sections/
  01_introduction.tex
  02_setup_recap.tex          # short; leans on M
  03_product.tex
  04_series_bounds.tex
  05_near_critical.tex
  06_discrete_vs_continuous.tex
  07_closed_form_search.tex
  08_koenigs_identity.tex
  09_hypertranscendence.tex   # from Koenigs_details
  10_scope_and_pslq.tex       # scope taxonomy + PSLQ prose
  11_practical.tex
  12_conclusion.tex
  app_elementary_cases.tex
  app_closed_form_catalogue.tex  # optional, from codex App A
```

(Agent may combine files if fewer inputs are cleaner; content blocks must all appear.)

### Primary donors

| Block | Primary source file |
|---|---|
| Product, series, bounds, parity, table, GA narrative, practical, much Koenigs identity | `7source_claude_1/sections/06_constant_A.tex` **split across A sections** |
| Near-crit with remainder | Upgrade from `7source_codex_1/sections/06_constant_A.tex` |
| HT theorem, BB precise, scope, PSLQ, working claim, elementary cases app | `Koenigs_details/Galton_Watson_A.tex` |
| Closed-form catalogue quarantine | `7source_codex_1/appendices/A_closed_form_search.tex` |

### Setup recap (`02_setup_recap.tex`) — keep short

Include only:

- Binary GW, \(S_{n+1}=2pS_n-pS_n^2\)  
- Definition of \(A(p)\) and \(\mathbb{E}[Z_n\mid Z_n>0]\to 1/A(p)\)  
- Pointer: full derivation of the conditional law and variance → Chapter M  
- Standing assumption \(0\le p<\tfrac12\), endpoint convention \(A(0):=\lim_{p\downarrow0}A(p)\) if present in sources  

**Target length:** roughly 1–3 pages, not a second GW chapter.

### Split procedure for claude_1 `06_constant_A.tex`

1. Open the file; map subsections to A.03–A.08 and A.11.  
2. Move each subsection into the corresponding new file with `a:` labels.  
3. Delete Mandelbrot/BB soft paragraphs that will be **replaced** by Koenigs_details in Phase 5 (do not leave contradictory claim language).  
4. Keep “Is this an advance?” on the product.

### Figures for A

Copy from claude_1 / Koenigs_details as needed:

- period doubling, conjugacy, Koenigs schematic, \(A_3\) hat, Mandelbrot (pedagogical only), conditional means, \(A(p)\) table data if figure-based  

Compile A spine before Phase 5 if possible.

---

## 9. Phase 5 — Obstruction core upgrade (critical)

**Replace** claude_1’s softer “results of Becker–Bergweiler imply… parameter avoids \(c\in\{0,-2\}\)” **as the main argument** with the **Koenigs_details** pipeline:

1. Definitions: differentially algebraic / hypertranscendental / elementary.  
2. Precise Becker–Bergweiler statement (DA Schröder ⇒ repelling + listed forms).  
3. Theorem: for every \(r\in(0,1)\), \(\psi_r\) is hypertranscendental over \(\mathbb{C}(z)\).  
4. Attracting vs repelling; \(r=2,4\) outside window; place elementary cases in appendix.  
5. Germ/basin remark if present in D2.  
6. **Scope section:** what is proved (conjugacy in \(z\)) vs open (values \(A(p_0)\), even irrationality; map \(p\mapsto A(p)\); DA in \(p\)). Include BB 1993 non-transfer and brief Hardouin–Singer non-applicability if in D2.  
7. **PSLQ prose only:** include the eleven rationals, dual routes, null battery description, and “evidence for the conjecture, not a proof.” **Do not** require scripts or data files in this phase. If digit counts and test counts appear in Koenigs_details, preserve them as stated in that source.  
8. Working claim / conclusion aligned with D2 abstract-level honesty.

### Claim hygiene checklist (must all hold in compiled A)

- [ ] Never claim a theorem that \(p\mapsto A(p)\) is non-elementary.  
- [ ] Never claim transcendence/irrationality of \(A(p_0)\) as proved.  
- [ ] Do claim hypertranscendence of \(z\mapsto\psi_r(z)\) for each fixed \(r\in(0,1)\), with BB attribution.  
- [ ] State PSLQ as finite-height negative evidence only.

### Near-critical upgrade

Where claude_1 has \(A\sim 2\varepsilon\), prefer `7source_codex_1` form with remainder \(O(\varepsilon\log(1/\varepsilon))\) **if** the proof/argument is fully present in that source; otherwise keep claude asymptotic and add codex remainder only as far as the source supports.

### Prose register in A

- Analytic sections (product/series): prefer claude_1 clarity.  
- Obstruction sections: prefer Koenigs_details precision; **lightly** smooth D2’s research-note density into thesis chapter register **without** weakening claims.  
- Do not import D1 (`A_Koenigs_Chapter`) claim language.  
- Fix obvious typos if copying D2 front matter (“centuary” etc.) only when those paragraphs are used.

---

## 10. Phase 6 — Bibliographies and cross-chapter consistency

1. Build `chapter_M_math_intro/references.bib` from claude_1 + any newly cited codex/QSD items actually cited in M.  
2. Build `chapter_A_constant_Ap/references.bib` from claude_1 \(A(p)\) cites + **full Koenigs_details bibliography** for obstruction cites.  
3. Deduplicate keys within each bib.  
4. Ensure every `\cite{...}` resolves.  
5. Scan both chapters for consistent \(A_{\mathrm{c}}(p)\), \(\varepsilon\), \(r=2p\).  
6. Ensure M’s forward-ref language matches A’s title.  
7. Ensure A’s back-ref language matches M’s title.

**No scripts directory** in this phase (user lock).

---

## 11. Phase 7 — Build & fix

For each chapter:

```sh
cd merged/chapter_M_math_intro && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cd merged/chapter_A_constant_Ap && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Fix:

- missing figures (copy or comment with MERGE_LOG note — prefer copy)  
- undefined refs/labels  
- multiply-defined labels  
- overfull boxes only if catastrophic; no microtype vanity pass required  

---

## 12. Phase 8 — Quality gates & MERGE_LOG

### MERGE_LOG.md must list

1. Every source file harvested → destination section.  
2. Content deliberately omitted (with reason), especially: scripts, Path meta, host/pathogen MoC, duplicate bulk.  
3. Any formula present in a Tier-1 source that could not be placed (must be empty or justified).  
4. Known issues for the *next* refinement phase (not fixed now).

### Gates (all required)

| # | Gate |
|---|---|
| G1 | Both PDFs compile with latexmk halt-on-error |
| G2 | M contains: prelims, GW, conditioning, small pops, CT BDC def, full MoC ladder, synthesis, apps |
| G3 | M does **not** contain full product/series/Koenigs/BB/PSLQ development |
| G4 | M develops \(A_{\mathrm{c}}(p)\) with basic detail and forward-refs discrete \(A(p)\) theory to A |
| G5 | A contains: product, series, bounds, near-crit, discrete vs continuous, search, Koenigs identity, HT theorem, scope, PSLQ prose, practical, conclusion, elementary-cases app |
| G6 | Obstruction claims pass claim hygiene checklist (§9) |
| G7 | Abstract mathematical voice throughout both |
| G8 | No verification scripts shipped (by design this phase) |
| G9 | Notation freeze respected |
| G10 | MERGE_LOG complete |

### Optional stretch (only if time; not required)

- Import multi-type GW *sketch* paragraph into M from codex_2.  
- Mid-chapter toolkit checkpoint in M (½ page).

---

## 13. What “done” means for this phase

The implementing agent stops when:

1. `merged/chapter_M_math_intro/main.pdf` and `merged/chapter_A_constant_Ap/main.pdf` exist and compile cleanly.  
2. Content inventory of the merge map is satisfied under the user locks.  
3. `MERGE_LOG.md` is written.  
4. **No** final rewrite, length cut, or new theorems.

**Handoff note for later phases (do not do now):**

1. **Pass 2 — Chapter M redesign** (structure + additions): see `SECOND_PASS_CHAPTER_M_OUTLINE.md`. Do **not** implement that outline in pass 1; still harvest full M bulk so pass 2 can rearrange it.  
2. Further refinements/additions; full literary rewrite; optional scripts/PSLQ reproducibility; thesis-number integration.

---

## 14. Risk register (read before editing)

| Risk | Mitigation |
|---|---|
| A becomes a second full GW chapter | Enforce 1–3 page setup recap |
| M still contains claude §6 bulk by habit | Never `\input` `06_constant_A` into M |
| Contradictory closed-form claims (soft vs D2) | Phase 5 replaces soft BB language entirely |
| Host/pathogen voice re-enters via codex/grok | Voice filter on every secondary paste |
| Figure paths break | Local `figures/` copies only |
| Label collisions | `m:` / `a:` prefixes |
| Over-merge creates inconsistency in \(\varepsilon\) vs \(r\) | Notation freeze + final scan |

---

## 15. Suggested agent checklist (copy into working notes)

```
[ ] Scaffold M and A projects
[ ] NOTATION.md + label prefixes
[ ] M spine from claude_1 (no 06_constant_A)
[ ] M interface policy (A_c first detail, A(p) light + forward ref)
[ ] M upgrades (codex MoC/BDC, etc.) + voice filter
[ ] A split from claude 06_constant_A
[ ] A near-crit upgrade from codex_1
[ ] A obstruction core from Koenigs_details
[ ] A apps (r=2,4; optional search catalogue)
[ ] Bibs + cross-title consistency
[ ] Both latexmk clean
[ ] Quality gates G1–G10
[ ] MERGE_LOG.md
```

---

## 16. Sources — quick path index

| Role | Path |
|---|---|
| Base M + A analytics | `7source_claude_1/` |
| Prose/outlook donor | `7source_claude_2/` |
| Theorem/MoC/BDC upgrades | `7source_codex_1/` |
| Obstruction authority | `Koenigs_details/Galton_Watson_A.tex` |
| Architecture ideas only | `grok first try/Grok_planned_no_koen/` |
| Do not master from | `CC_C2_short_A/`, `A_Koenigs_Chapter/`, Path meta in planned |

Governing content map: `MERGE_MAP_TWO_CHAPTERS.md`.
