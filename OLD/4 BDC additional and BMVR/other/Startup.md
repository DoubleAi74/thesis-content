# Startup — Three-Chapter BDC Build

**Read this document first, then `Project_specification.md`, then `Progress.md`.**
Those three files are your complete brief. This file tells you where the project
stands; the specification tells you exactly what to build; `Progress.md` is the
living document in which you track and record the work — keep it updated
continuously, because if you are interrupted, another agent resumes from it.

---

## 1. The mission

Build three polished, standalone, publication-quality thesis chapters from
existing source material:

| Build folder (create) | Chapter | Working title |
|---|---|---|
| `BDC_core/` | Chapter 3 | The birth–death–catastrophe process: definition and main results |
| `BDC_extra/` | Chapter 4a | The birth–death–catastrophe process: distribution theory, quasi-stationarity, and burst statistics |
| `BDC_odes/` | Chapter 4b | From one cell to a population: burst-aware renewal dynamics and the bursting–budding comparison |

All three builds live at the root of the current directory
(`/Users/adamaldridge/Desktop/Thesis content 🎓 /4 BDC additional and BMVR/`).
Each build has its own `main.tex`, `sections/`, `figures/`, `references.bib`,
and compiles standalone with `latexmk -pdf main.tex`.

The chapters must form a strong sequence with overlapping material: Chapter 3
defines the process and its main results and sets up the other two; Chapter 4a
completes the single-cell theory; Chapter 4b builds the population-level
renewal theory. Each chapter stands alone (short boxed "what we need from
earlier chapters" opening, its own discussion, cross-references by chapter
number only).

**Prose standard:** everything must read as a final-draft chapter of a rigorous
interdisciplinary applied-mathematics PhD thesis, in the register prescribed by
the `/aa-flow-lucid` skill (continuous academic flow, laddered explanation,
stable notation, located uncertainty, model conclusions separated from
biological claims, British English). The co-authored paper `Grant_paper.pdf`
is the second stylistic reference: polished prose and mathematical sentences on
exactly this material. Match its clarity and precision, then expand to thesis
density — the chapters are naturally more expansive than the succinct paper
(more motivation, connective tissue, and step-by-step exposition), never
looser. Invoke `/aa-flow-lucid` at the start of the writing phases and apply
it end to end. There are no pilots or stylistic approval gates: work
continuously until done.

**Figures:** you do **not** generate new figures (this is deliberate, to save
tokens for writing). You **do**: (i) copy the existing figures into the builds
and keep their references; (ii) keep the two existing TikZ figures already in
the 4b source (they compile as-is); (iii) insert **figure flags** — visible,
compile-rendered boxes at the locations where figures belong, each containing a
detailed generation specification sufficient for a later figure-agent to produce
the figure with no further context. Flag format and seed lists are in the
specification (§7).

---

## 2. What has already been done (do not redo)

1. **The Chapter 4 draft is complete and verified.** In `document MAIN/` there
   is a finished 59-page draft of everything that becomes Chapters 4a and 4b:
   17 section files + 3 appendix files, compiling cleanly (0 errors, 0
   undefined references, 0 overfulls). The mathematics in it has been checked
   numerically; you are **restructuring, converting notation, and polishing
   prose** — not re-deriving. Any formula change beyond symbol renaming is a
   formula-level change (see guardrails).
2. **Two verification suites exist and pass:**
   - `new_notes3/verify_result_20_1.py` — renewal BMVR suite, 54 checks, all
     PASS (report: `new_notes3/verify_result_20_1_report.txt`).
   - `N=2 Immediate Transfer content/verify_chained_transfer.py` — chained
     immediate-transfer suite, 28 checks, all PASS (report alongside).
   Re-run them (unmodified) at the milestones specified in `Progress.md` and
   after any formula-level change.
3. **`CHAPTER4_PLAN.md`** (folder root) records how the Chapter 4 draft was
   built, phase by phase, with the errata sign-off. Useful background; not
   binding on this project where the specification differs (the specification
   wins).
4. **The corrected mathematics is authoritative in two places:** the draft
   itself, and `new_notes3/Comprehensive_Corrected_Notes.tex` (the corrected
   master notes). Where this brief and the specification give a formula, that
   formula has already been verified.
5. **`Grant_paper.pdf` is a first-class source file** for the build:
   Aldridge, Whaler, López-García, Molina-París, Gillard & Lythe, "Release of
   virus and bacteria from infected cells: models of budding and bursting"
   (dated 1 April 2026). It serves three purposes: (i) a reference for quality
   and tone of prose and mathematical sentences, alongside `/aa-flow-lucid`
   (the chapters will be naturally more expansive than the paper, but never
   less precise); (ii) a source of additional material to be *fluidly
   incorporated* into the chapters — conditional rupture-time laws, the
   budding single-cell picture, the budding-vs-bursting comparison, real
   parameter estimates for *F. tularensis* and *B. anthracis* — woven into
   the relevant sections, not bolted on; (iii) a register model for the
   target exposition. **Its notation is not the unified regime and must be
   translated into it** (the chapters' notation is canonical — e.g. δ stays
   the catastrophe rate): see specification §2.7 before quoting anything.

---

## 3. The source material (read-only unless stated)

| Path | What it is | Use |
|---|---|---|
| `3 BDC core/document MAIN/` | Chapter 3 source (LaTeX, 11 section files, 20-page PDF) | Source for `BDC_core`. See specification §3 for the per-file survey (errors, duplicates, typos — all documented there). |
| `document MAIN/` | The completed Chapter 4 draft (17 sections + 3 appendices) | Source for `BDC_extra` (§§1–10) and `BDC_odes` (§§11–17). |
| `new_notes3/Comprehensive_Corrected_Notes.tex` | Corrected master notes; authoritative for all formulas | Reference while writing; **never edit**. |
| `new_notes/BMVR_extension_notes.tex`, `new_notes2/Core_Publishable_Work_Summary.tex` | Earlier note generations; full-detail spectrum/HIV material already folded into the draft | Reference only; never edit. |
| `N=2 Immediate Transfer content/` | Chained-transfer source + verification suite | Reference; suite re-run only. |
| `figures/` | BMVR overlay + peff figures + plotting scripts | Copy figures into `BDC_odes/figures/`; scripts are reference for figure-flag specs. |
| `document MAIN/figures/` | QSmean plots (chapter 4a), all copied overlay/verification figures | Copy into the builds as specified. |
| `3 BDC core/document MAIN/figures/` | Chapter 3's six figures | Copy into `BDC_core/figures/`. |
| `paper.pdf` | Hataye et al. 2019 (HIV contrast reference) | Citation source for `BDC_odes`. |
| `Grant_paper.pdf` | Co-authored paper on the same work (budding vs bursting) | **First-class source**: stylistic reference alongside `/aa-flow-lucid`; additional material to incorporate fluidly (see specification §§4.1, 5.1); notation translated per specification §2.7. |
| `CHAPTER4_PLAN.md` | History of the Chapter 4 build | Background reading. |

**Nothing in these folders is to be edited, moved, or deleted.** The three new
build folders are the only places you write.

---

## 4. What you are going to do (rough summary)

- **Phase 0 — Setup.** Create `BDC_core/`, `BDC_extra/`, `BDC_odes/`; copy the
  relevant sources into each; write each `main.tex` (title, unified macros,
  the figure-flag macro, theorem environments); write each `references.bib`;
  get a skeleton compile of each.
- **Phase 1 — Chapter 3 (`BDC_core`).** Upgrade in the sense of the
  specification §3: fix the documented mathematical errors in place, merge the
  duplicated section pairs (preserving all unique content), unify notation,
  polish prose, add the forward-looking setup section, copy figures, insert
  figure flags with detailed specs, add the Brockwell reference. Nothing
  removed without record.
- **Phase 2 — Chapter 4a (`BDC_extra`).** Take draft §§1–10, convert notation
  (β→λ, R→H, Î→I_fix, per §4 of the specification), delete the
  "Chapter 3 was wrong" correction remarks, write the chapter-level
  introduction and the "what we need from Chapter 3" opening, split the
  discussion as specified (assay predictions + single-cell open problems close
  this chapter), assemble the single-cell appendices (formula table, chained
  verification record, technical derivations), copy figures, insert figure
  flags.
- **Phase 3 — Chapter 4b (`BDC_odes`).** Same for draft §§11–17: notation
  conversion, correction-remark removal, "what we need from Chapters 3 and 4a"
  opening, closing discussion (fitting consequences, forward connections,
  population open problems), population appendices (formula table, renewal
  verification record, hypergeometric transforms), copy the 12 existing
  figures, keep the two existing TikZ figures, insert figure flags.
- **Phase 4 — Prose pass.** End-to-end `/aa-flow-lucid` pass over all three
  chapters.
- **Phase 5 — Final QA.** Clean compiles (0 errors / 0 undefined refs / 0
  overfulls; figure flags are intentional and allowed), both verification
  suites re-run and recorded, cross-reference sweep, figure-flag registry
  complete in `Progress.md`, all logs final.

The detailed task breakdown, acceptance criteria, and the notation conversion
table are in `Project_specification.md`. Track everything in `Progress.md`.

---

## 5. Guardrails (binding)

1. **Write only inside** `BDC_core/`, `BDC_extra/`, `BDC_odes/`, and the three
   handoff documents (`Startup.md`, `Project_specification.md`, `Progress.md`).
2. **Never edit** `new_notes*/`, the two verification suites, `document MAIN/`,
   `3 BDC core/`, `figures/`, `N=2 Immediate Transfer content/`, or
   `CHAPTER4_PLAN.md`. Suites are re-run, never modified.
3. **No deletions without record.** Anything removed from the chapter sources
   during the builds (merged-away duplicates, orphaned lines, dead macros) is
   listed in `Progress.md` with its former location.
4. **Formula discipline.** The draft's formulas are verified. Symbol renaming
   (β→λ etc.) is expected and is not a formula change. Anything that alters a
   formula's *content* requires: re-running both verification suites, recording
   the change and the suite results in `Progress.md`.
5. **No new figure generation.** Copy existing figures; keep the two existing
   TikZ figures; write figure flags with full generation specs for everything
   else (specification §7).
6. **Out of scope:** Chapters 1, 5, 6, 7 of the thesis and their errata; the
   stale `3 BDC core/` duplicate question; web verification of bibliography
   entries (leave `TODO(verify)` notes as they are and list them in
   `Progress.md`).
7. **Continuous execution.** No pilots, no interim approval gates. Save at
   every logical milestone; update `Progress.md` continuously (completed work,
   current work, next actions, decisions, formula changes, figure/build
   status, verification results). Stop only for a genuine blocker requiring
   user input — and record the blocker in `Progress.md` when it occurs.

---

## 6. Environment facts

- macOS; TeX Live 2024 with `latexmk`, `pdflatex`, `bibtex`
  (`/usr/local/texlive/2024/bin/universal-darwin/`).
- Python 3.14 with `numpy` and `matplotlib` (Agg backend fine). **No scipy,
  no mpmath** — never introduce a dependency on them. (The suites already
  avoid them; the chained suite's ₂F₁ series-vs-closed-form line may report
  "scipy unavailable" — that is expected, and the acceptance criterion is
  the overall 28/28 PASS.)
- Build command per chapter: `latexmk -pdf main.tex` inside the build folder.
- The chapter sources use `$$...$$` displays, the macro families listed in the
  specification §2, `unsrt` bibliography style, `article` class at 11pt.

---

## 7. Definition of done

All of the following, recorded in `Progress.md`:

1. `BDC_core/`, `BDC_extra/`, `BDC_odes/` each compile with `latexmk -pdf` to
   a clean PDF (0 errors, 0 undefined references, 0 overfull boxes outside
   figure-flag boxes — overfulls inside flag boxes are exempt, and
   underfulls are allowed; figure flags intentional).
2. One unified notation regime across all three chapters (specification §2),
   applied to prose, formulas, captions, and figure-flag text.
3. Chapter 3's documented errors fixed, duplicates merged with all unique
   content preserved, and the chapter ends by setting up Chapters 4a and 4b.
4. Chapters 4a and 4b each open with a boxed "what we need" subsection and
   close with their own discussion; no "Chapter 3 was wrong" remarks remain
   anywhere in the builds; cross-references are by chapter number only.
5. Figure flags with detailed generation specifications at every location
   listed in specification §7 (plus any you add), visible in the compiled
   PDFs, and a complete flag registry in `Progress.md` (Log C).
6. Both verification suites re-run at final QA: renewal 54 checks, chained 28
   checks, results recorded.
7. Prose at final-draft standard per `/aa-flow-lucid`, British English,
   throughout all three chapters.
8. `Progress.md` fully updated: all phases checked off, logs complete, nothing
   silently assumed.
