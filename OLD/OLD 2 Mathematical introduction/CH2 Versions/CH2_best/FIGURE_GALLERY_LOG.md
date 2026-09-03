# Figure candidate gallery — build log

**Date:** 9 August 2026
**Follows:** `AGENT_INSTRUCTIONS_FIGURE_GALLERY.md`
**Purpose:** stage every figure binary from the four base merges, plus the current
`CH2_best` production assets, and display all of them in temporary gallery appendices so
that a human can compare variants and choose winners.

**Nothing was curated.** No candidate was dropped for redundancy, for duplication, or for
quality. Byte-identical files appear in the gallery several times over, under different
source prefixes, because the instruction is completeness rather than taste. Where the
same binary appears under several names, the inventory's "Byte-identical sets" tables say
so, so the selector can tell a real comparison from an apparent one — but every copy is
still staged and still shown.

---

## 1. What happened

| | Before | After |
|---|---|---|
| Chapter M | 50 pages, 2.0 MB | **72 pages, 10.3 MB** |
| Chapter A | 28 pages, 1.6 MB | **49 pages, 13.2 MB** |

Both were compiling cleanly before the gallery was added, and both still are. The
baseline was re-checked before any file was copied.

| | M | A |
|---|---|---|
| candidates staged | **85** | **68** |
| comparison groups | 32 (24 multi-variant, 8 one-offs) | 19 (11 multi-variant, 8 one-offs) |
| `best` (current production) | 18 | 8 |
| `claude` | 15 | 8 |
| `qwen` | 13 | 10 |
| `grok` | 22 | 17 |
| `codex` | 17 | 25 |
| failed the integrity check | 0 | 0 |
| candidate directory size | 9.1 MB | 14 MB |

153 candidates in total.

---

## 2. Commands

Everything is done by one re-runnable script, which lives inside `CH2_best/` and writes
only inside `CH2_best/`:

```sh
cd CH2_best
python3 scripts/build_figure_galleries.py

cd chapter_M_math_intro  && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cd ../chapter_A_constant_Ap && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The script wipes and rebuilds `figures/candidates/` in both projects, regenerates
`sections/app_figure_gallery.tex` in both, and rewrites
`FIGURE_CANDIDATE_INVENTORY.md`, `FIGURE_SELECTION_CHECKLIST.md` and
`scripts/last_run_notes.txt`. Running it twice gives the same result; it is safe to
delete `candidates/` and re-run.

What it harvests, per chapter:

- `CH2_best/<chapter>/figures/*` — top level only, tagged `best`; `candidates/` itself is
  excluded, so re-running never stages a candidate of a candidate.
- `CH2 Versions_{claude,Qwen,Grok,codex}/merged/<chapter>/figures/**` — recursive, so
  `IMG_ch3/`, `tikz_gen/` and `generated/` are all picked up, and both the `.pdf` and the
  `.png` of a stem are taken where both exist.
- Extensions `.pdf .png .jpg .jpeg .eps`. Scripts, data and TeX sources are skipped.

Naming is `{source}__{relative path with / as __}`, so
`grok/figures/tikz_gen/bd_mean_regimes.pdf` becomes
`grok__tikz_gen__bd_mean_regimes.pdf`.

---

## 3. Renames, collisions, corrupt files

**None of any kind.** `scripts/last_run_notes.txt` records the run and reads:

```text
no collisions, no symlinks, no integrity failures
```

No `__dupN` suffix was needed: the source prefix plus the relative path made every one of
the 153 names unique on the first pass. No symlinks were encountered. Every staged file
passed its format check — `%PDF` header plus a successful `pdfinfo` parse for PDFs, and
signature checks for PNG and JPEG — so the "Candidates that failed the integrity check"
section at the end of each gallery is empty and every candidate is displayed as an image.
Had any file failed, it would have been shown as a framed placeholder panel and listed by
name and reason rather than silently dropped.

---

## 4. One fix that was needed

The last real appendix in each chapter (`app_d_coefficient_extraction.tex` in M,
`app_closed_form_catalogue.tex` in A) ends with

```latex
\renewcommand{\thesection}{\thechapter.\arabic{section}}
```

to hand section numbering back to the chapters that follow. A gallery appended after that
therefore numbered itself `1.5` and `2.3` instead of `1.E` and `2.C`. The generated
gallery now re-enters appendix numbering at its own head and restores arabic numbering at
its foot, so the appendix lettering is correct and the restore those files perform is
left exactly as it was. This is the only LaTeX change outside the gallery files and the
two `\input` lines.

---

## 5. Verification

Run after the final build:

- Image files counted directly in each source tree and compared with the staged count:
  M expected 85 and has 85; A expected 68 and has 68.
- Every staged filename was grepped for in the corresponding
  `app_figure_gallery.tex`: 85 of 85 and 68 of 68 appear.
- Every `\includegraphics{candidates/…}` target in the generated TeX was checked to exist
  on disk: no misses.
- Both projects compile with `latexmk -pdf -halt-on-error`, exit 0, with no undefined
  references or citations in the final pass.
- The narrative's own `\includegraphics` calls were listed and confirmed unchanged: M
  still uses its 18 production filenames and A its 7, all resolved through
  `\graphicspath{{figures/}}` at the top level. Nothing was rewired to a candidate.
- Appendix lettering checked in `main.toc`: M ends `1.D`, `1.E`; A ends `2.B`, `2.C`.

---

## 6. Source trees

**Unmodified.** `git status --porcelain` reports no modified tracked files; the only
untracked entry is `CH2_best/` itself. The script reads from
`CH2 Versions_claude/`, `CH2 Versions_Qwen/`, `CH2 Versions_Grok/` and
`CH2 Versions_codex/` and never opens a file there for writing.

---

## 7. What the human does next

1. Open `chapter_M_math_intro/main.pdf` at appendix **1.E** and
   `chapter_A_constant_Ap/main.pdf` at appendix **2.C**. Each opens with an index of
   groups whose figure references are hyperlinks.
2. Compare variants within a group — they sit on the same page, or on consecutive pages
   for groups larger than four.
3. Fill in `FIGURE_SELECTION_CHECKLIST.md`. Groups the narrative currently uses are
   marked `(production)`; the rest are unused candidates that would need a figure
   environment and a caption written for them before they could enter the text.
4. A later pass then rewires the body `\includegraphics` calls to the winners, deletes
   `figures/candidates/` and `sections/app_figure_gallery.tex`, removes the two `\input`
   lines from the `chapter.tex` files, and recompiles. That pass is out of scope here and
   no selection has been made.

---

## 8. Notes for the selector

Three observations that fell out of the staging and may save time. They are observations,
not recommendations, and nothing was acted on.

- **Most cross-source "variants" are the same file.** Of M's 24 multi-variant groups, 15
  are byte-identical throughout: `abs1`, `abs2`, `birth_death_paths`, `conditionalMean`,
  `coupled_ode_ctmc`, `dtctA`, `extinction_and_law`, `kvals`, `kvals495`, `kvals505`,
  `poisson_process`, `power_law_fixed`, `random_walk`, `simpleGWvis`, `subGWvis`. Of A's
  11, 10 are: `conditionalMean`, `dtctA`, `figure1_parameter_conjugacy`,
  `figure2_koenigs_linearization`, `figure3_numerical_koenigs`,
  `figure4_mandelbrot_context`, `period_double`, `power_law_fixed`, `simpleGWvis`,
  `subGWvis`. Those groups need no looking at.
- **Only ten groups across both chapters contain files that actually differ.** In M:
  `logspec_mean`, `rupture_sawtooth` and `rw_transition`, where the `best` panel is the
  version regenerated during the merge and the `qwen` panel is the original; and the six
  Grok `tikz_gen` stems, which differ only because Grok ships each plot as both a PDF and
  a PNG. In A, only `a3_hat_plot`, again a PDF/PNG split. So the substantive comparisons
  are three, and the rest of the gallery is a completeness record.
- **The one-offs are where genuinely unseen material sits.** M's eight are
  `a3_hat_plot`, `figure1_parameter_conjugacy`, `figure2_koenigs_linearization` and
  `figure4_mandelbrot_context` (Codex A-topic assets found in M's `IMG_ch3/`),
  `period_double`, Qwen's `ruin_prob`, and Codex's two `generated` figures
  `founder_cohort_survival` and `gw_regime_diagnostics`. A's eight are `abs1`, `abs2`,
  `kvals`, `kvals495`, `kvals505` (M-topic assets found in A's trees) and Qwen's
  `ap_bounds_ratio`, `ap_nearcrit` and `koenigs_domain`. Nothing in either list is used
  by the narrative today, so promoting any of them means writing a figure environment and
  a caption for it.
- **Chapter A's trees carry M-topic assets.** Codex A and Grok A both contain
  `IMG_ch3/` directories holding `abs1`, `abs2`, `kvals*`, `simpleGWvis`, `subGWvis` and
  so on. Per the instruction these are staged in **A's** gallery, because that is where
  they were found; they are not cross-copied into M. The inventory's "Group keys present
  in both chapters" section lists every stem this affects.
