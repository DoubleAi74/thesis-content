# Agent instructions: figure candidate gallery for manual selection

**Role.** You are an implementation agent. Your job is **not** to rewrite the thesis chapters or re-merge prose. Your job is to gather **every figure binary** from all four base merges into `CH2_best/`, preserve them under collision-safe names, and **display them all in the compiled PDFs** in side-by-side comparison galleries so a human can pick winners and delete losers later.

**Purpose.** The human will open the PDFs, compare variants of the same conceptual figure (and unique one-offs), then manually keep the best assets and remove the rest. Completeness beats taste: **include everything**, including near-duplicates and multiple versions of the same plot.

---

## 0. Scope and non-goals

### Do

- Work **only** under `CH2_best/` (edit M and A projects there).
- Copy figure binaries from all four bases into `CH2_best`.
- Add gallery appendices (or equivalent) so **every** collected figure appears in a PDF.
- Keep existing narrative `\includegraphics` paths working (production figures stay put).
- Compile both chapter PDFs cleanly.
- Leave a clear inventory log for the human selector.

### Do not

- Do **not** delete any candidate figure.
- Do **not** “curate,” “prefer Claude,” or drop Grok/Codex assets as redundant.
- Do **not** rewrite scientific prose, methods, or claim hygiene (except minimal appendix glue text).
- Do **not** modify the four source trees:
  - `CH2 Versions_claude/`
  - `CH2 Versions_Qwen/`
  - `CH2 Versions_Grok/`
  - `CH2 Versions_codex/`
- Do **not** replace production figure filenames used by the main body unless required for a compile fix; prefer **adding** candidates beside them.
- Do **not** invent new scientific plots.

---

## 1. Paths

**Workspace root:**

```text
…/2 Mathematical introduction/CH2 Versions/
```

**Target (edit here):**

```text
CH2_best/
  chapter_M_math_intro/
  chapter_A_constant_Ap/
  FIGURE_GALLERY_LOG.md          # create/update
  FIGURE_CANDIDATE_INVENTORY.md  # create (machine- and human-readable)
```

**Figure sources (read only):**

| Tag | M figures root | A figures root |
|---|---|---|
| `claude` | `CH2 Versions_claude/merged/chapter_M_math_intro/figures/` | `CH2 Versions_claude/merged/chapter_A_constant_Ap/figures/` |
| `qwen` | `CH2 Versions_Qwen/merged/chapter_M_math_intro/figures/` | `CH2 Versions_Qwen/merged/chapter_A_constant_Ap/figures/` |
| `grok` | `CH2 Versions_Grok/merged/chapter_M_math_intro/figures/` | `CH2 Versions_Grok/merged/chapter_A_constant_Ap/figures/` |
| `codex` | `CH2 Versions_codex/merged/chapter_M_math_intro/figures/` | `CH2 Versions_codex/merged/chapter_A_constant_Ap/figures/` |
| `best` (current production) | `CH2_best/chapter_M_math_intro/figures/` | `CH2_best/chapter_A_constant_Ap/figures/` |

Also treat **current `CH2_best` production figures** as a fifth provenance tag `best` (or `best_current`) so regenerated assets (e.g. `rw_transition.pdf`, fixed `rupture_sawtooth.pdf`) appear next to original Qwen binaries.

---

## 2. What counts as a figure

Collect every file under each figures tree matching:

```text
*.pdf  *.png  *.jpg  *.jpeg  *.eps
```

**Include:**

- Nested folders: `IMG_ch3/`, `tikz_gen/`, `generated/`, etc.
- Both `.pdf` and `.png` of the same stem (e.g. Grok often has both).
- Assets present only under A even if “about” M topics, and vice versa — place each gallery in the chapter where the file was found **and** also allow a cross-list in the inventory (see §5).

**Exclude:**

- Python/shell scripts (`.py`, `.sh`)
- CSV/data (`.csv`)
- LaTeX sources, logs, aux
- Non-image files

If the same path appears twice only because of a symlink, copy once and note it.

---

## 3. Naming convention (mandatory)

Main-body production figures in `figures/` keep their **existing** names so current `\includegraphics{foo}` keeps working.

All **candidates for comparison** go under a dedicated subdirectory:

```text
chapter_M_math_intro/figures/candidates/
chapter_A_constant_Ap/figures/candidates/
```

### 3.1 Candidate filename pattern

```text
{source}__{safe_relative_stem}{ext}
```

Rules:

1. `{source}` ∈ `claude`, `qwen`, `grok`, `codex`, `best`.
2. `{safe_relative_stem}` = relative path under that version’s `figures/` root, with `/` → `__`, spaces → `_`.
   - Examples:
     - `claude/figures/conditionalMean.pdf` → `claude__conditionalMean.pdf`
     - `grok/figures/tikz_gen/bd_mean_regimes.pdf` → `grok__tikz_gen__bd_mean_regimes.pdf`
     - `codex/figures/IMG_ch3/kvals.png` → `codex__IMG_ch3__kvals.png`
     - `codex/figures/generated/founder_cohort_survival.pdf` → `codex__generated__founder_cohort_survival.pdf`
3. Keep original extension.
4. If a collision still occurs (should be rare), append `__dupN` before the extension and log it.
5. **Do not overwrite** an existing candidate file with a different source; different sources always differ in the `{source}__` prefix.

### 3.2 Also keep production copies

Leave (or restore if missing) the current production set at the top level of `figures/` used by the body text:

```text
figures/random_walk.pdf
figures/rw_transition.pdf
…
```

Optionally **also** copy each production file into `candidates/` as `best__{name}` so the gallery shows the exact asset currently in the narrative.

---

## 4. Gallery presentation (how the human sees them)

### 4.1 Add a gallery appendix to each chapter

**Chapter M**

1. Create `sections/app_figure_gallery.tex`.
2. Input it **last** in `chapter.tex` (after existing appendices).
3. Title it clearly as temporary review material, e.g.

```latex
\section{Figure candidate gallery (temporary)}
\label{m:app:figuregallery}
```

Opening paragraph (keep short):

> This appendix is a temporary asset-selection aid. It displays every figure binary collected from the Claude, Qwen, Grok, and Codex merges, plus the current production assets in \texttt{CH2\_best}. Variants are grouped by stem when possible. After manual selection, this appendix and unused candidate files will be removed.

**Chapter A**

Same pattern: `sections/app_figure_gallery.tex`, input last from A’s chapter wrapper.

### 4.2 Grouping for side-by-side comparison

Within each gallery, organise by **comparison groups**, not by source alone.

**Algorithm:**

1. For each candidate file, compute a **group key** = final path component stem, lowercased, with common noise stripped lightly if needed:
   - basename without extension
   - if stem is like `figure1_parameter_conjugacy`, keep as-is
   - do **not** merge different stems just because topics are similar (e.g. keep `random_walk` separate from `rw_transition`)
2. Sort groups alphabetically by group key.
3. Within a group, order sources: `best`, `claude`, `qwen`, `grok`, `codex`, then any leftover.
4. Within same source+stem with multiple relative paths (`IMG_ch3` vs root vs `tikz_gen`), show each as its own subentry (all of them).

**Unique one-offs** (only one source has the stem) still appear — in a final section “Unique assets (single source)” or simply as groups of size 1.

### 4.3 Layout template (use consistently)

For each group:

```latex
\subsection{Group: \texttt{conditionalMean}}
% optional one-line note: "same stem across sources"

\begin{figure}[p]
  \centering
  % For each variant in the group (repeat minipage or subfloat):
  \begin{minipage}[t]{0.48\textwidth}
    \centering
    \includegraphics[width=\linewidth,height=0.38\textheight,keepaspectratio]{candidates/claude__conditionalMean.pdf}\\[4pt]
    {\footnotesize\ttfamily claude\_\_conditionalMean.pdf}
  \end{minipage}\hfill
  \begin{minipage}[t]{0.48\textwidth}
    \centering
    \includegraphics[width=\linewidth,height=0.38\textheight,keepaspectratio]{candidates/qwen__conditionalMean.pdf}\\[4pt]
    {\footnotesize\ttfamily qwen\_\_conditionalMean.pdf}
  \end{minipage}
  \caption{Candidate group \texttt{conditionalMean}. Compare variants; pick one production asset later.}
  \label{m:fig:cand-conditionalMean}
\end{figure}
```

Rules:

- Prefer **at most 2 variants per row**, 1–2 rows per float when possible.
- If a group has many members (e.g. 6+), split across consecutive figures `…-1`, `…-2` with the same group title.
- Use `[p]` or `[htbp]` freely; float quality is secondary to completeness.
- Use `height=…\textheight,keepaspectratio` so huge plots do not overflow.
- If `\includegraphics` fails for a corrupt file, still list the filename in a table of failures (do not silently drop it).
- **Every** candidate must either render or appear in a “failed to render” table with path + error.

### 4.4 Graphic path

Ensure preambles / chapter setups can see candidates. Claude-style projects often have:

```latex
\graphicspath{{figures/}}
```

Then include as `candidates/claude__foo.pdf`. If `\graphicspath` is missing, use `figures/candidates/...` consistently — pick one scheme and stick to it.

### 4.5 Do not disturb narrative figures

Do **not** change which file the main body uses, except if a path is broken. The gallery is additive. The human will later rewire production paths after choosing winners.

---

## 5. Inventory documents

### 5.1 `CH2_best/FIGURE_CANDIDATE_INVENTORY.md`

Create a complete table:

| Chapter | Group key | Source | Candidate filename | Original path | Bytes | SHA256 (short) | Rendered in gallery? |
|---|---|---|---|---|---|---|---|

Also include summary counts:

- total candidates M / A
- per-source counts
- groups with ≥2 variants (the interesting comparison sets)
- unique one-offs

### 5.2 `CH2_best/FIGURE_GALLERY_LOG.md`

Record:

1. Date and that this follows `AGENT_INSTRUCTIONS_FIGURE_GALLERY.md`.
2. Commands used to copy files.
3. Any renames / collisions / corrupt files.
4. Final PDF page counts for M and A (will grow).
5. Confirmation that source trees were not modified.
6. Explicit note: **no candidates were dropped for redundancy.**

### 5.3 Optional helper: selection checklist

Add `CH2_best/FIGURE_SELECTION_CHECKLIST.md` with one row per group:

```text
- [ ] conditionalMean  → keep: ________  drop: ________
- [ ] random_walk      → keep: ________  drop: ________
…
```

Pre-fill group names; leave keep/drop blank for the human.

---

## 6. Source inventory checklist (must all be harvested)

Use this as a minimum coverage list. If you find additional images under those trees, include them too.

### 6.1 Claude M (flat `figures/`)

`abs1.pdf`, `abs2.pdf`, `birth_death_paths.pdf`, `conditionalMean.pdf`, `coupled_ode_ctmc.pdf`, `dtctA.png`, `extinction_and_law.pdf`, `kvals.png`, `kvals495.png`, `kvals505.png`, `poisson_process.pdf`, `power_law_fixed.pdf`, `random_walk.pdf`, `simpleGWvis.png`, `subGWvis.png`

### 6.2 Claude A

`A3_hat_plot.pdf`, `conditionalMean.pdf`, `dtctA.png`, `figure1_parameter_conjugacy.pdf`, `figure2_koenigs_linearization.png`, `figure3_numerical_koenigs.png`, `figure4_mandelbrot_context.png`, `period_double.png`

### 6.3 Qwen M

`abs1.pdf`, `abs2.pdf`, `conditionalMean.pdf`, `kvals.png`, `kvals495.png`, `kvals505.png`, `logspec_mean.pdf`, `power_law_fixed.pdf`, `ruin_prob.pdf`, `rupture_sawtooth.pdf`, `rw_transition.pdf`, `simpleGWvis.png`, `subGWvis.png`

### 6.4 Qwen A

`A3_hat_plot.pdf`, `Ap_bounds_ratio.pdf`, `Ap_nearcrit.pdf`, `dtctA.png`, `figure1_parameter_conjugacy.pdf`, `figure2_koenigs_linearization.png`, `figure3_numerical_koenigs.png`, `figure4_mandelbrot_context.png`, `koenigs_domain.pdf`, `period_double.png`

### 6.5 Grok M

- `IMG_ch3/*` (pdf/png present there)
- `tikz_gen/*` including **both** `.pdf` and `.png` where both exist:
  - `bd_conditional_mean`, `bd_mean_regimes`, `bd_mean_survival_panel`, `bd_survival_regimes`, `poisson_path`, `ruin_hitting`

### 6.6 Grok A

All image binaries under Grok A `figures/` (including nested dirs if any).

### 6.7 Codex M

- `generated/founder_cohort_survival.pdf`
- `generated/gw_regime_diagnostics.pdf`
- `IMG_ch3/*` image binaries

### 6.8 Codex A

Top-level A figures **and** `IMG_ch3/*` image binaries (even if some look like M assets — still include under A candidates if found in A’s tree).

### 6.9 Best current production

All current top-level image binaries in `CH2_best/.../figures/` (excluding `candidates/` itself), copied into `candidates/` as `best__…`.

**Especially include** regenerated best-only or best-fixed assets such as:

- `best__rw_transition.pdf`
- `best__logspec_mean.pdf`
- `best__rupture_sawtooth.pdf`
- `best__birth_death_paths.pdf`, `best__poisson_process.pdf`, `best__random_walk.pdf`, etc.

---

## 7. Execution phases

### Phase 0 — Snapshot

1. Confirm `CH2_best/chapter_M_math_intro` and `chapter_A_constant_Ap` exist and currently compile.
2. Baseline page counts in the log.
3. Do not start if `CH2_best` is missing — stop and report.

### Phase 1 — Create directories

```text
CH2_best/chapter_M_math_intro/figures/candidates/
CH2_best/chapter_A_constant_Ap/figures/candidates/
```

### Phase 2 — Copy all candidates

For each source tag and each chapter:

1. Walk the source `figures/` tree.
2. For each image file, copy to the matching chapter’s `candidates/` with the naming convention in §3.
3. If a source stores an asset only under M but A also has a copy, both chapter galleries should show the copy that lives in that chapter’s source tree (do not cross-copy unless the file exists only in one tree and is needed for completeness — default: **mirror the source chapter**).

**Cross-chapter note:** Codex A’s `IMG_ch3/` may contain M-like assets. Still place them in **A’s** `candidates/` because that is where they were found. Mention in the inventory under “found in A tree”.

### Phase 3 — Write gallery TeX

1. Generate `app_figure_gallery.tex` for M and for A (script-generated TeX is fine and preferred for completeness).
2. Group as in §4.2.
3. Wire into `chapter.tex` / main include list **last**.
4. Mark appendix in TOC (normal `\section` under appendix numbering is fine).

Suggested generation approach (agent may implement as a shell/python script **inside** `CH2_best/`, not in source trees):

```text
CH2_best/scripts/build_figure_galleries.py
```

The script should be re-runnable: deleting `candidates/` + regenerating is OK as long as the final state is complete.

### Phase 4 — Compile and fix

```sh
cd CH2_best/chapter_M_math_intro
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

cd ../chapter_A_constant_Ap
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Fix only gallery-related issues:

- missing files
- bad extensions
- overfull huge images (cap height)
- need for `\usepackage{graphicx}` already present — do not break preamble

If the PDF becomes extremely long, that is **expected and acceptable**.

### Phase 5 — Verify completeness

Automated checks the agent must run:

1. Count image files harvested from each source tree.
2. Count files in each `candidates/` directory.
3. Assert `candidates_count >= sum of source images for that chapter` (with `best` production also included).
4. Grep gallery `.tex` for each candidate basename — every candidate filename string must appear at least once in the gallery file **or** in the failure table.
5. Confirm main body still compiles and still references its original production figures (spot-check a few `\includegraphics` in `02_markov_chains.tex` etc.).

### Phase 6 — Logs

Write/update:

- `FIGURE_CANDIDATE_INVENTORY.md`
- `FIGURE_GALLERY_LOG.md`
- `FIGURE_SELECTION_CHECKLIST.md`

Update `FIGURE_SOURCES.md` only with a short pointer:

> Temporary candidate gallery added; see FIGURE_CANDIDATE_INVENTORY.md. Production figure choices unchanged pending human selection.

Do **not** rewrite the scientific merge log’s historical claims; append a short note to `MERGE_LOG.md` if desired:

```text
## Addendum — figure candidate gallery
Date: …
All figures from claude/qwen/grok/codex (+ best production) staged under figures/candidates/ and shown in app_figure_gallery.tex. No production figure selection yet.
```

---

## 8. Quality gates

| Gate | Requirement |
|---|---|
| F1 | Both M and A compile with `latexmk -pdf -halt-on-error` |
| F2 | `figures/candidates/` exists in both chapters and is non-empty |
| F3 | Every image binary from all four base merges’ M/A figure trees is present as a candidate (naming §3) |
| F4 | Current best production images also appear as `best__…` candidates |
| F5 | Gallery appendix displays every candidate (or lists render failures explicitly) |
| F6 | Main narrative figure includes are unchanged in target (no silent rewiring to a different source) |
| F7 | Source version trees unmodified |
| F8 | Inventory + gallery log + selection checklist written |
| F9 | No candidate dropped for “duplicate” or “worse quality” reasons |

---

## 9. Explicit anti-patterns

1. **Do not** keep only “the best” of each stem — that defeats the task.
2. **Do not** skip Grok `tikz_gen` pngs because pdfs exist — include both.
3. **Do not** skip Codex `IMG_ch3` copies because Claude already has the same basename.
4. **Do not** put all candidates only on disk without putting them in the PDF.
5. **Do not** replace the whole chapter with a figure dump — append a gallery.
6. **Do not** edit prose sections to “integrate” every candidate into the scientific argument.
7. **Do not** run a long literary rewrite pass.

---

## 10. Done criteria

You are finished when:

1. A human can open `CH2_best/chapter_M_math_intro/main.pdf` and `…/chapter_A_constant_Ap/main.pdf`.
2. Near the end of each PDF, a **Figure candidate gallery** shows all staged variants.
3. Groups with multiple sources place variants on the same page or consecutive pages for easy comparison.
4. `FIGURE_CANDIDATE_INVENTORY.md` lists every file with source and group key.
5. `FIGURE_SELECTION_CHECKLIST.md` is ready for human ticks.
6. Builds are clean.

---

## 11. After the human selects (out of scope for this agent)

Do **not** perform selection unless the user later asks. For reference only:

- Human marks winners in the checklist.
- A future pass rewires body `\includegraphics` to winners, deletes `candidates/`, removes gallery appendices, recompiles.

---

## 12. One-sentence mission

**Stage every figure from Claude, Qwen, Grok, Codex, and current best production into `CH2_best` candidate folders under collision-safe names, display them all in temporary gallery appendices for side-by-side human selection, leave the scientific text’s production figures alone, compile clean, and inventory everything.**
