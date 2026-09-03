# Agent instructions: produce the best merged Chapters M and A

**Role.** You are an implementation agent. Your job is to produce **one** best-of-breed pair of standalone LaTeX chapter projects by merging existing versions, following the frozen policy below. Do not invent a new architecture. Do not re-survey all sources from scratch. Execute the graft plan, compile both PDFs cleanly, and leave a provenance log.

**Governing conversation decision (frozen).**

- **Base:** `CH2 Versions_claude/merged/` (structure, methods spine, Chapter A narrative, house prose style).
- **Primary donor:** `CH2 Versions_Qwen/merged/` (early textbook texture, selected framework blocks, selected appendices, selected figures).
- **Secondary figure donors:** `CH2 Versions_Grok/merged/` and `CH2 Versions_codex/merged/` (figures only, when clearly better or missing).
- **Not bases:** Codex and Grok chapter prose (too thin / too stubby). Use them only for figures or as hygiene checks.

**Workspace root (this directory):**

```text
…/2 Mathematical introduction/CH2 Versions/
```

All relative paths below are from that root.

---

## 0. Deliverables and output layout

Create a **new** folder at the workspace root:

```text
CH2_best/
  MERGE_LOG.md
  NOTATION.md
  chapter_M_math_intro/
    main.tex
    chapter.tex          # or equivalent Claude-style wrapper if present
    preamble.tex         # or ch_preamble.tex — keep one consistent name
    references.bib
    sections/            # final Pass-2 section files only
    figures/             # all local figures used by M
    main.pdf             # must compile clean
  chapter_A_constant_Ap/
    main.tex
    chapter.tex          # if Claude uses it
    preamble.tex
    references.bib
    sections/
    figures/
    main.pdf             # must compile clean
```

**Do not** edit in place inside `CH2 Versions_claude/`, `_Qwen/`, `_codex/`, or `_Grok/`. Copy Claude into `CH2_best/` first, then modify only under `CH2_best/`.

**Optional but recommended:**

```text
CH2_best/
  sections_pass1_archive/   # only if you need a safety copy; otherwise leave Claude’s sections_pass1 uncopied
  FIGURE_SOURCES.md         # short list of which figure came from which version
```

---

## 1. Non-negotiable policy

### 1.1 Base and graft rule

| Asset | Policy |
|---|---|
| Chapter M **architecture** | Claude (objects → methods → appendices) |
| Chapter M **prose standard** | Claude continuous academic voice |
| Chapter M **methods ladder** | Claude (do not replace with Qwen’s file split) |
| Chapter A **entire project** | Claude almost unchanged; only micro-grafts if clearly better |
| Early M **definitional texture** | Graft from Qwen into Claude files |
| Logistic speciation + full coupled instance | Import from Qwen, rewrite into Claude voice (default fill policy, §1.3) |
| Appendix bulk Claude thinned | Recover selectively from Qwen if missing and useful |
| Figures | Claude core set + cherry-pick Qwen/Grok/Codex |

### 1.2 Interface contract (M ↔ A) — do not break

**Chapter M may contain:**

- Binary GW notation, survival recursion \(S_{n+1}=2pS_n-p S_n^2\).
- Light definition \(A(p)=\lim_n S_n/(2p)^n\) and \(\mathbb E[Z_n\mid Z_n>0]\to 1/A(p)\).
- Full derivation of continuous-time \(\Ac(p)=(1-2p)/(1-p)\) and competing-clocks match.
- Forward references to Chapter A for product, series, bounds, near-critical theory, closed-form search, Koenigs identity, hypertranscendence, PSLQ.

**Chapter M must not contain:** full product/series/Koenigs/Becker–Bergweiler/PSLQ development.

**Chapter A** owns all deep \(A(p)\) theory. Setup recap stays short (~1–3 pages). No re-proof of full GW extinction theory or full conditional-variance derivation already proved in M.

**Label prefixes:** `m:` in M, `a:` in A. Cross-chapter macros `\ChM`, `\ChA` (or Claude equivalents) preserved.

**Claim hygiene (A):**

- Proved: for each fixed \(r\in(0,1)\), \(z\mapsto\psi_r(z)\) is hypertranscendental (BB route).
- Not proved: irrationality/transcendence of any value \(A(p_0)\).
- Not proved: non-elementarity / DA of the parameter map \(p\mapsto A(p)\).
- PSLQ = finite-height negative evidence only.

### 1.3 Default fill policy for source gaps (frozen)

| Block | Default |
|---|---|
| Time-inhomogeneous framework | Keep Claude’s general setup; enrich with Qwen’s cleaner exposition if useful |
| Logistic speciation | **Import Qwen’s full treatment**, rewrite into Claude prose. Label mean-field surrogate steps as modelling approximations, not identities. Keep Qwen’s figure `logspec_mean.pdf` if it matches the text |
| Coupled ODE–CTMC general framework | Prefer Claude’s three-coupling taxonomy + generator; merge any clearer Qwen PDMP wording |
| Concrete coupled / rupture schematic | **Import Qwen’s schematic**, rewrite into Claude prose; keep as schematic unless text already claims it is a later-chapter model. Prefer Claude’s trajectory figure if both exist; consider also Qwen `rupture_sawtooth.pdf` if caption-true |
| Random walk / Poisson / BD objects | Claude base; absorb Qwen textbook clarity and selected figures (§4) |

Do **not** leave raw `TODO`, `Placeholder — source material required`, or “reviewed sources contain no…” remarks in the final PDFs unless a genuine author decision is still impossible. Under this default policy those stubs should be resolved by the Qwen imports + Claude rewrite.

### 1.4 Voice and register

- Abstract mathematical voice (no host/pathogen application bleed).
- Prefer Claude’s continuous argument style: name threads, bridge examples forward to methods, mark heuristics explicitly.
- When grafting Qwen, **rewrite** into that style. Do not leave adjacent paragraphs in two different AI registers.
- Do not add first-person chatty asides, emoji, or meta “as an AI / as merged from…” language in the chapter body.
- Provenance belongs in `MERGE_LOG.md`, not in the thesis prose.

### 1.5 Notation freeze

Copy Claude’s `merged/NOTATION.md` into `CH2_best/NOTATION.md` and obey it. In particular:

- \(Z_n\), \(S_n\), \(A(p)\), \(\Ac(p)\) or `A_{\mathrm c}(p)`, \(\varepsilon=1-2p\), \(r=2p\), \(\psi_r\).
- Macro names from Claude preambles (`\Ac`, `\ex`, `\pr`, theorem environments, etc.) unless a rename is required for compile consistency — if so, document it.
- One consistent preamble style under `CH2_best` (prefer Claude’s `preamble.tex` pattern for both chapters).

---

## 2. Source map (what lives where)

### 2.1 Bases

```text
CH2 Versions_claude/merged/chapter_M_math_intro/   → base for M
CH2 Versions_claude/merged/chapter_A_constant_Ap/  → base for A
CH2 Versions_claude/merged/NOTATION.md
CH2 Versions_claude/merged/MERGE_LOG.md            → read for provenance; do not treat as final
```

Claude M Pass-2 section files (expected):

```text
sections/01_overview.tex
sections/02_markov_chains.tex
sections/03_methods.tex
sections/04_method_of_characteristics.tex
sections/app_a_critical_gw.tex
sections/app_b_absorption_models.tex
sections/app_c_hypergeometric_identity.tex
sections/app_d_coefficient_extraction.tex
```

Claude A section files (expected): full `01`–`12` + two apps.

### 2.2 Primary donor (Qwen)

```text
CH2 Versions_Qwen/merged/chapter_M_math_intro/
CH2 Versions_Qwen/merged/chapter_A_constant_Ap/   # micro-grafts only
```

Useful Qwen M files:

| Qwen file | Use |
|---|---|
| `sections/01_overview.tex` | Donor phrases only; **do not replace** Claude overview wholesale |
| `sections/02_discrete_markov.tex` | Textbook DTMC + random-walk binomial law + figure cues |
| `sections/03_continuous_markov.tex` | Textbook CTMC pacing; compare clocks/generator wording |
| `sections/04_time_inhomogeneous.tex` | **Import** logistic + time-dependent BD material |
| `sections/05_coupled_ode_ctmc.tex` | **Import** schematic coupled/rupture material |
| `sections/06_methods_discrete.tex` | Optional one-liners only; Claude methods win |
| `sections/07_methods_continuous.tex` | Optional supplements only |
| `sections/08_method_of_characteristics.tex` | Optional; Claude MoC wins |
| `sections/09`–`14` apps | Selective appendix recovery (§5) |
| `figures/rw_transition.pdf` | Import if used |
| `figures/logspec_mean.pdf` | Import if logistic kept |
| `figures/rupture_sawtooth.pdf` | Import if coupled schematic uses it |
| `figures/ruin_prob.pdf` | Import if gambler’s-ruin / hitting discussion benefits |

### 2.3 Secondary figure donors

```text
CH2 Versions_Grok/merged/chapter_M_math_intro/figures/tikz_gen/
  bd_conditional_mean.pdf
  bd_mean_regimes.pdf
  bd_mean_survival_panel.pdf
  bd_survival_regimes.pdf
  poisson_path.pdf
  ruin_hitting.pdf

CH2 Versions_codex/merged/chapter_M_math_intro/figures/generated/
  founder_cohort_survival.pdf
  gw_regime_diagnostics.pdf
```

Import only if a final captioned figure actually uses them. Do not dump unused assets.

### 2.4 Do not re-harvest as masters

These were already merged into Claude/Qwen and must not re-open as competing masters:

- `7source_*`, `codex_1/`, `A_Koenigs_Chapter/`, `Koenigs_details/`, `Grok_planned_no_koen/`, `CC_C2_short_A/`

Exception: if a figure path is broken and the only clean binary is still under a source tree, copy the binary — not the prose.

---

## 3. Execution phases (do in order)

### Phase 0 — Setup

1. Create `CH2_best/`.
2. Copy recursively:
   - `CH2 Versions_claude/merged/chapter_M_math_intro/` → `CH2_best/chapter_M_math_intro/`
   - `CH2 Versions_claude/merged/chapter_A_constant_Ap/` → `CH2_best/chapter_A_constant_Ap/`
   - `CH2 Versions_claude/merged/NOTATION.md` → `CH2_best/NOTATION.md`
3. Remove build junk if desired (`*.aux`, `*.log`, `*.fls`, `*.fdb_latexmk`, `*.out`, `*.toc`, `*.bbl`, `*.blg`) — or leave and recompile cleanly later.
4. Confirm both projects still compile **before** edits:

```sh
cd "CH2_best/chapter_M_math_intro" && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cd "../chapter_A_constant_Ap" && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

If the Claude base does not compile, fix that first; do not start grafting.

5. Start `CH2_best/MERGE_LOG.md` with date, base commit/path, and phase checklist.

---

### Phase 1 — Chapter A (minimal work; do first to lock scope)

**Policy:** Claude A is the master. Goal is a clean standalone A under `CH2_best`, not a second merge.

1. Keep Claude section order and content.
2. Allowed micro-grafts only if they improve clarity without changing claims:
   - A short scope sentence from Qwen A intro if Claude’s is weaker at that single point.
   - A figure from Qwen A only if Claude is missing an asset the text already expects (e.g. numerical Koenigs / conjugacy / Mandelbrot consistency check).
3. Verify claim hygiene still matches §1.2.
4. Compile A; resolve undefined refs/cites; fix broken figure paths to local `figures/`.
5. Log any A change (even one sentence) in `MERGE_LOG.md`.

**Do not** restructure A into Codex’s fewer-section layout.  
**Do not** import Qwen A as a base.

---

### Phase 2 — Chapter M overview (Claude base, light Qwen polish)

File: `chapter_M_math_intro/sections/01_overview.tex`

1. Keep Claude’s overview as master (three threads: conditioning, near-critical, absorption; objects-then-methods; originality claim limited to ABD closed form + hypergeometric identity if that is Claude’s claim).
2. Optionally absorb **short** Qwen clarifying sentences about distributional vs absorption questions **only if** they improve the opening and do not duplicate Claude’s three threads into a fourth parallel taxonomy.
3. Update the roadmap sentences so they match the **final** section inventory after Phases 3–5 (no dangling “stub” promises; no promise of appendices you drop).
4. Remove any meta language about drafts/sources.

---

### Phase 3 — Markov objects: textbook texture graft (core of the M upgrade)

File: `chapter_M_math_intro/sections/02_markov_chains.tex` (Claude monolithic structure — keep it monolithic; do **not** split into Qwen’s many files unless compile structure already requires it).

#### 3.1 Discrete-time / random walk

From Qwen `02_discrete_markov.tex`, graft into Claude’s random-walk subsection:

- Exact \(n\)-step binomial law on the lattice (if Claude lacks it).
- Clean textbook pacing of definition → moments → law.
- Figure `rw_transition.pdf` **or** keep Claude `random_walk.pdf` if it already shows paths + ruin; best outcome is **either** one strong combined figure set **or** Claude paths/ruin + Qwen transition-law figure if not redundant.

**Preserve from Claude (do not drop):**

- Embedded jump-chain bridge to birth–death (\(q=\lambda/(\lambda+\mu)\)).
- Gambler’s-ruin solution and link to first-step methods.
- Forward pointers into methods.

#### 3.2 Galton–Watson object

- Keep Claude’s compressed GW object treatment.
- Do not re-expand full critical theory into the main body; that belongs in appendices (§5).

#### 3.3 Continuous-time clocks / generator / Poisson / BD / BDC

- Claude remains master.
- From Qwen `03_continuous_markov.tex`, borrow only clearer definitional sentences or ordering if Claude is denser than necessary.
- Preserve Claude’s competing-clocks proposition/proof and Gillespie remark if present.
- Preserve Claude figures: `poisson_process.pdf`, `birth_death_paths.pdf`, etc.

#### 3.4 Time-inhomogeneous + logistic (resolve stubs)

1. Keep Claude’s general time-inhomogeneous framework (two-time kernels / time-ordered product remarks) if present.
2. **Replace** Claude’s logistic placeholder remark with a rewritten import of Qwen `04_time_inhomogeneous.tex`:
   - time-dependent linear BD mean + Riccati extinction setup;
   - logistic speciation mean-field surrogate;
   - explicit warning that replacing random diversity by \(\bar N(t)\) is a modelling step.
3. Copy `logspec_mean.pdf` (and any required plot scripts only if needed later — scripts optional).
4. Rewrite all imported prose into Claude voice; unify notation to NOTATION.md (`\lambda(t)`, `\mu(t)`, etc.).
5. Ensure citations used by the logistic block exist in M’s `references.bib` (copy missing entries from Qwen’s bib).

#### 3.5 Coupled ODE–CTMC (resolve stubs)

1. Prefer Claude’s three coupling modes + joint generator.
2. Merge Qwen’s PDMP framing / rupture-into-medium schematic where it adds a concrete picture Claude only stubbed.
3. Figures:
   - Keep Claude `coupled_ode_ctmc.pdf` if it illustrates two-way coupling well.
   - Add Qwen `rupture_sawtooth.pdf` only with an accurate caption.
4. Rewrite into Claude voice; no “TODO” remarks left.
5. If the schematic is not a named later-chapter model, say so once (schematic / framework example), then move on — do not apologize repeatedly.

#### 3.6 Voice pass on `02_markov_chains.tex`

After grafts, read the whole file top-to-bottom and eliminate:

- duplicated definitions,
- contradictory notation,
- stub residue,
- Qwen/Claude register seams,
- broken `\cref` targets.

---

### Phase 4 — Methods + MoC (Claude master; almost no structural change)

Files:

- `sections/03_methods.tex`
- `sections/04_method_of_characteristics.tex`

1. **Do not** replace Claude methods with Qwen’s split methods files.
2. Allowed grafts:
   - a missing elementary identity,
   - a clearer one-paragraph motivation,
   - a figure from Grok/Codex that illustrates mean/survival regimes if Claude’s conditional-mean section would benefit **and** the figure is caption-true.
3. Preserve Claude’s discrete-time “where the methods run out → forward to Chapter A / Koenigs” bridge.
4. Preserve full CT ladder (backward equations, means, variances, hitting, extinction, conditional means, \(\Ac\), light \(A(p)\)).
5. Preserve MoC worked example (absorption–death) and “what the example shows.”
6. Ensure every method subsection’s examples still match the objects section after Phase 3 renumbering/labels.

---

### Phase 5 — Appendices (Claude architecture + selective Qwen recovery)

Claude appendix targets:

| Claude file | Role |
|---|---|
| `app_a_critical_gw.tex` | Critical GW / small populations bulk |
| `app_b_absorption_models.tex` | Full absorption ladder beyond worked example |
| `app_c_hypergeometric_identity.tex` | Integral identity |
| `app_d_coefficient_extraction.tex` | Coefficient extraction |

Qwen appendix donors:

| Qwen file | Recover if Claude lacks comparable content |
|---|---|
| `10_app_critical.tex` | Critical branching detail |
| `11_app_cohorts.tex` | Founding cohorts / early survival |
| `12_app_variance.tex` | QSD variance derivation |
| `13_app_dbdc.tex` | Discrete BDC + killed chain |
| `14_app_moc_catalogue.tex` | Further absorption models / regular representation |
| `09_app_moc_support.tex` | Only if hypergeo / extraction richer than Claude C/D |

**Rules:**

1. Prefer Claude appendix text when both cover the same theorem.
2. If Qwen has a lemma/figure Claude omitted (cohorts, variance, discrete BDC detail), **merge into the appropriate Claude appendix** rather than adding a sixth appendix unless the material truly does not fit.
3. If adding an appendix becomes necessary, update `main.tex` / `chapter.tex` inputs and overview roadmap.
4. Do not move deep \(A(p)\) product/Koenigs material into M appendices.
5. Keep appendix numbering working (Claude’s Alph appendix setup). Fix any `Alph0` / broken appendix numbers if they appear in the TOC.

Codex figures `founder_cohort_survival.pdf` and `gw_regime_diagnostics.pdf` may support App A if you recover cohort/critical material and the figures match the text.

---

### Phase 6 — Figures and bibliography

1. Maintain a single local `figures/` per chapter. No `../` escapes to other version trees.
2. After all text decisions, delete unused figure binaries only if you are sure nothing includes them (safer: leave unused files but do not reference them).
3. Write `CH2_best/FIGURE_SOURCES.md` listing each **used** figure and source version.
4. Merge bibliographies as needed:
   - Start from Claude `references.bib`.
   - Add any keys required by Qwen grafts (e.g. logistic speciation citation).
   - Deduplicate keys; every `\cite` must resolve.
5. Prefer `\graphicspath{{figures/}}` already used by Claude; keep paths consistent.

Suggested figure default set for M:

| Keep from Claude | Consider from Qwen | Optional from Grok/Codex |
|---|---|---|
| `random_walk.pdf` | `rw_transition.pdf` | `ruin_hitting.pdf` |
| `poisson_process.pdf` | `logspec_mean.pdf` | `poisson_path.pdf` |
| `birth_death_paths.pdf` | `rupture_sawtooth.pdf` | BD regime panels |
| `coupled_ode_ctmc.pdf` | `ruin_prob.pdf` | `founder_cohort_survival.pdf` |
| `extinction_and_law.pdf` | | `gw_regime_diagnostics.pdf` |
| `conditionalMean.pdf`, `dtctA.png` | | |
| GW / kvals / power_law / abs1 / abs2 | | |

Do not include all optional figures. Each must earn a caption and a textual purpose.

---

### Phase 7 — Global prose continuity pass (both chapters, M especially)

After structural grafts compile:

1. Read M PDF (or linearised section order) as a reader, not a merger.
2. Fix:
   - repeated definitions of the same object,
   - roadmap mismatches,
   - “in this chapter we will stub…” residue,
   - inconsistent terms (catastrophe vs rupture — pick Claude’s convention and stick to it),
   - double explanations of \(A(p)\) beyond the light interface,
   - orphan figures / orphan labels.
3. Light length control: if M exceeds ~50 pages with obvious duplication, cut duplication first, not original results or claim-hygiene sections.
4. A gets only a light continuity read unless Phase 1 changed it.

Optional skill alignment (if available in the agent environment): a single academic flow pass is allowed **after** content is frozen — not instead of the graft plan.

---

### Phase 8 — Build, QA, log

#### 8.1 Build commands

```sh
cd "CH2_best/chapter_M_math_intro"
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

cd "../chapter_A_constant_Ap"
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Both must succeed with `-halt-on-error`.

#### 8.2 Quality gates (all required)

| Gate | Requirement |
|---|---|
| G1 | Both PDFs compile with `latexmk -pdf -halt-on-error` |
| G2 | M has overview, Markov objects (incl. time-inhomogeneous + coupled), methods, MoC, appendices |
| G3 | M has **no** full product/series/Koenigs/BB/PSLQ development |
| G4 | M derives \(\Ac(p)\) and only lightly defines discrete \(A(p)\) with forward ref to A |
| G5 | A retains product, series, bounds, near-critical, compare, search, Koenigs, HT, scope, PSLQ prose, practical, conclusion, elementary-cases app |
| G6 | Claim hygiene intact (§1.2) |
| G7 | Abstract mathematical voice; no host/pathogen bleed; no merge-meta in body |
| G8 | No verification/PSLQ scripts required in the shipped chapters |
| G9 | Notation freeze respected; labels `m:` / `a:` |
| G10 | `MERGE_LOG.md` records base, grafts, omissions, figure sources, page counts |
| G11 | No unresolved `\ref`/`\cite`; no missing figures |
| G12 | No remaining `TODO` / `Placeholder — source material` in final section files |

#### 8.3 Log contents (`CH2_best/MERGE_LOG.md`)

Must include:

1. Date and agent identity note (“best merge from Claude base + Qwen grafts”).
2. Exact base paths and donor paths.
3. Section-by-section graft table for M (what was taken from Qwen/Grok/Codex).
4. Complete list of A changes (ideally short).
5. Figure source table.
6. Bibliography keys added.
7. Final page counts for M and A.
8. Known issues / residual risks (if any).
9. Explicit statement that Codex/Grok prose was not used as base.

---

## 4. Section-level keep / graft / drop map (M)

Use this as the operational checklist.

| Region | Keep (Claude) | Graft (Qwen unless noted) | Drop / avoid |
|---|---|---|---|
| Overview | Three threads; objects/methods split; originality honesty | Optional distributional-vs-absorption clarity | Qwen overview as wholesale replacement; Codex chapter-map unless you truly want it |
| DTMC defs | Claude definition + absorption language | Qwen textbook matrix/Chapman–Kolmogorov clarity | Codex “source gap” random-walk refusal |
| Random walk | Embedded chain + ruin + method pointer | Binomial law; `rw_transition` if non-redundant | Multiple redundant RW figures without purpose |
| GW object | Claude compressed object | — | Full critical theory in main body |
| CTMC clocks/generator | Claude proofs + Gillespie | Minor clarity only | Rewriting proofs into weaker form |
| Poisson / BD / BDC | Claude rates + figures | Minor clarity | Host/pathogen framing |
| Time-inhomogeneous | Claude general framework | Qwen full logistic + TI-BD | Leaving Claude logistic TODO |
| Coupled ODE–CTMC | Claude 3-mode + generator | Qwen schematic + optional sawtooth figure | Leaving concrete-instance TODO; inventing a fake “thesis theorem” about the schematic |
| Discrete methods | Claude first-step + GF + “methods run out” | Tiny supplements only | Qwen methods as master |
| CT methods | Full Claude ladder + \(\Ac\) + light \(A(p)\) | Optional Grok regime figures | Deep \(A(p)\) theory |
| MoC | Claude abs–death worked example | — | Moving ABD closed form out of appendix without reason |
| Apps | Claude A–D spine | Cohorts / variance / discrete BDC / extra MoC detail from Qwen as needed | Product/Koenigs apps; unused bulk that bloats past usefulness |

---

## 5. Chapter A keep / graft / drop map

| Region | Action |
|---|---|
| All Claude A sections `01`–`12` + apps | **Keep as base** |
| Qwen A intro claim-hygiene sentences | Optional micro-graft only |
| Qwen A figures not already in Claude | Import only if text needs them |
| Codex A compression / fewer sections | **Do not adopt** |
| Grok A | Figures only if missing asset |
| Soft BB / Mandelbrot-as-proof language | Must not re-enter; Claude/Koenigs_details structural route stays |

---

## 6. Prose rewrite rules when grafting Qwen → Claude

When importing a Qwen block:

1. Paste into the Claude section at the correct structural point.
2. Immediately rewrite:
   - macros/notation → Claude/`NOTATION.md`,
   - labels → `m:…` unique names (grep for collisions),
   - cross-refs → existing Claude labels where possible,
   - voice → continuous Claude academic prose,
   - claims → no stronger than sources support.
3. Delete the Qwen wording that duplicates a Claude paragraph already present.
4. If Qwen and Claude prove the same result differently, keep Claude’s proof unless Qwen’s is strictly richer **and** still correct; then prefer Qwen’s richness rewritten in Claude voice.
5. Never leave “In the Qwen version…” or “Draft notes say…”.

---

## 7. What “done” looks like

You are finished only when all of the following are true:

1. `CH2_best/chapter_M_math_intro/main.pdf` and `…/chapter_A_constant_Ap/main.pdf` both exist and were produced by a clean `latexmk -halt-on-error` run.
2. M contains resolved logistic + coupled sections (no placeholder remarks).
3. M methods/MoC remain Claude-structured and strong.
4. A is essentially Claude, compile-clean, claim-hygienic.
5. `CH2_best/MERGE_LOG.md` and `NOTATION.md` exist; figure provenance is recorded.
6. A reader opening M then A experiences **one** voice and **one** architecture, not a collage.

---

## 8. Suggested work order (checklist)

Copy this into the log and tick as you go:

- [ ] Phase 0: create `CH2_best/`, copy Claude bases, baseline compile
- [ ] Phase 1: Chapter A micro-grafts (if any) + compile
- [ ] Phase 3.1–3.3: early objects textbook graft (RW/CTMC)
- [ ] Phase 3.4: logistic import + rewrite + figure
- [ ] Phase 3.5: coupled import + rewrite + figures
- [ ] Phase 3.6: voice pass on objects section
- [ ] Phase 4: methods/MoC audit (minimal grafts)
- [ ] Phase 5: appendix recovery from Qwen
- [ ] Phase 6: figures + bib
- [ ] Phase 7: global continuity pass
- [ ] Phase 8: final compiles + quality gates G1–G12
- [ ] Final `MERGE_LOG.md` complete

---

## 9. Explicit anti-patterns (do not do these)

1. **Do not** take Qwen as the filesystem base and “Claude-ify” all 48 pages.
2. **Do not** re-split Claude M into Qwen’s 14-file layout unless forced by a technical constraint (you are not).
3. **Do not** reintroduce full \(A(p)\) theory into M.
4. **Do not** keep `TODO` stubs after choosing the default fill policy in §1.3.
5. **Do not** invent numerical results, digit counts, or PSLQ outcomes not already in Claude/Qwen A.
6. **Do not** copy host/pathogen or applied narrative from short drafts.
7. **Do not** edit the four source version trees; only `CH2_best/`.
8. **Do not** stop at “files copied.” The job is a **compiled, continuous, single-voice pair of chapters**.

---

## 10. If time or complexity forces triage

If you must cut scope, cut in this order (never reverse):

1. Optional Grok/Codex figures.
2. Extra appendix recovery beyond critical GW + absorption ladder + hypergeo + coefficient extraction.
3. Second coupled figure.
4. Micro-grafts into Chapter A.

**Never triage away:** Claude methods spine, Claude A obstruction/claim hygiene, M/A interface contract, clean compile.

---

## 11. One-sentence mission

**Copy Claude’s two chapters into `CH2_best/`, graft Qwen’s textbook early-object clarity and filled logistic/coupled frameworks (rewritten into Claude’s voice), recover only the appendix/figure value that earns its place, compile both PDFs clean, and leave a provenance log — producing one best version, not a fourth parallel draft.**
