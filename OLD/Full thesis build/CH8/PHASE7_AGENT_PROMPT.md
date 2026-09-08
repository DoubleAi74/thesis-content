# Fresh-agent prompt — CH8 Phase 7 only

Copy everything below the line into a new agent. Do not paste the conversation history.

---

You are executing **Phase 7 only** of a thesis-chapter visual pass. Phases 0–6 are already in the tree. Do **not** rewrite the chapter, reopen science, restyle screenshots, or re-run earlier phases.

## Workspace

`/Users/adamaldridge/Desktop/Current best/CH8/`

Standalone compile: `cd "/Users/adamaldridge/Desktop/Current best/CH8" && latexmk -pdf -interaction=nonstopmode main.tex`

Live plan (same content as this brief, with rationale): session `plan.md` for CH8, or ignore it and follow this prompt.

## What this pass is

Make CH8’s **vector schematics and float specifiers** match the bound Good-example pages:

- **CH2** (state-space as a chain): `/Users/adamaldridge/Desktop/Current best/Good examples/CH2/`
  - PDF: `main.pdf`, pages **8–10** (printed). Fig 1.4 = three-regime birth–death paths, labels on the figure. Fig 1.5 / Def 1.4 = rate diagram.
  - TikZ source to copy *grammar* from: `Good examples/CH2/sections/02_markov_chains.tex` around the figure labelled `m:fig:ratediagram` (styles `st` = drawn circle, `ab` = double-circle absorbing, rates on arrows, `0.92\textwidth`, specifier `[!htbp]`).
- **CH7** (process as a mechanism): `/Users/adamaldridge/Desktop/Current best/Good examples/CH7/Two_Type_Chapter/document MAIN/`
  - PDF: `two_type.pdf`, page **4**. Definition, then a designed schematic: large nodes, rates on arrows, Okabe–Ito, absorbing catastrophe as a **filled card**, legend on the figure.
  - TikZ source: `figures/fig01_process_schematic/src/fig01.tex`.
- **CH3** is **not** a visual model. Its only lesson (already applied): do not add routing scaffolding. Do not copy visualiser stills.

Rasterise those Good-example pages **before** you edit, and keep them in view while drawing.

A 2-D count pair cannot be CH7’s two-node cartoon. It **can** be a CH2 rate diagram on a grid: open circles for transient states, double circles (or CH7 filled cards) for the absorbing row and column, and \(\lambda i\), \(\varsigma ij\) written on one representative pair of arrows.

## Frozen — do not touch

**Science.** Claims, numbers, symbols, equation meaning, proofs, table values. Do not rename \(\varsigma\), \(\vartheta\), \(\pi_{i,j}\), \(Q_t\), \(\mathcal{R}\), \(V_\infty\).

**Screenshots — files and printed widths.** Do not crop, recolour, upscale, replace, or drop:

- `figures/basic1.png` … `basic4.png`
- `figures/RS1.png`, `RS2.png`
- `figures/big1.png` … `big3.png`, `small1.png` … `small3.png`
- `figures/QT1.png`, `QT2.png`

Printed widths stay `0.40\textwidth` (two-up) and `0.31\textwidth` (three-up). You **may** change only the float specifier (`[tbp]` → `[!htbp]`) on those figure environments.

**Near-verbatim prose** (typos/macros only if you must; otherwise leave the sentences):

1. `sections/02_schedule_alone.tex` — opening through “broad propagation dynamics would remain identical.”
2. Same file, §2.1 — Brownian-drift / macrophage-motility / *Y. pestis* absorption / “environment of play.”
3. `sections/04_extracellular_depletion.tex` — the leading-edge sentence: “Those at the leading edge, as it were, clearing the way for their comrades in the rear.”

**Comments.** All `% NEEDS-BIOLOGY` blocks stay in the `.tex`. Do not invent biological claims or new citations.

**Do not edit:** `sections/01_introduction.tex`, `sections/06_discussion.tex`, `references.bib`, `chapter.tex`, sibling chapters, screenshot PNGs. Do not fill the flooding coiner. Do not put a code listing back in Appendix B.

**Standalone `??`.** Cross-references whose labels begin `m:`, `bdc:`, `dist:`, or `p:` are other chapters and stay undefined. That is expected. Do not add dummy labels.

**Palette** (already in `preamble.tex`; use it):

- birth / cool `na1` `#0072B2`
- suppression / vermillion `mut1` `#D55E00`
- extinction / catastrophe `Rup2` `#9A2820`
- spent store / certain `Rec2` `#009E73`
- contested yellow `nb1` `#F0E442`
- ink `#1A1C1F`, `inksoft` `#565B62`
- fills `na1fill`, `Rec2fill`, `Rup2fill`

Do not switch to CH2’s muted pair (`#8c1d18` / `#1f4e79`).

## Already done — do not redo

§1 rewrite; flooding used plainly; house-style matplotlib (`vinf`, `ratio`, `reversal`, \(N=20\) maps); TikZ palette; Def 1.1 packed with Fig 1.3; Prop 1.3 interior proof; memoryless \(\mathcal{R}\) leading §4.3; two flooding arguments; spectrum axis; *Y. pestis* as a reading; no `_parked` / `_work/` in print; 28-page compile, 0 overfull.

## Tasks (do in this order)

### 7.1 State-space schematic — the main job

File: `sections/03_intracellular_depletion.tex`, figure `path:fig:statespace` (currently `\begin{figure}[!h]` immediately after `\end{definition}` of `path:def:rs`).

Replace the grey-dot lattice with CH2 node language:

- Transient states \((i,j)\) with \(i\ge 1\), \(j\ge 1\): **drawn circles** (CH2 `st` style: `circle,draw,thick`, light or white fill), not `\fill[gray1] ... circle`.
- Column \(X_t=0\): absorbing, **double circles** (CH2 `ab` style) or a CH7 filled card, colour `Rup2`. This is extinction.
- Row \(Q_t=0\), \(i\ge 1\): absorbing, double circles or a distinct card, colour `Rec2`. This is spent store. The two absorbing sets must not look like two colours of the same dot.
- Birth arrows (right, `na1`) and suppression arrows (down-left, `mut1`) stay. On **one** representative birth arrow write \(\lambda i\); on **one** representative suppression arrow write \(\varsigma ij\).
- Keep the on-figure legend, axis titles (\(X_t\) replicators, \(Q_t\) granules), and the existing caption. Geometry of the lattice (counts 0…7, births right, suppressions down-left) stays.
- Specifier `[!htbp]`. Keep the figure **immediately after** `\end{definition}` of `path:def:rs`. Keep `\Needspace{16\baselineskip}` before the definition and `\FloatBarrier` after the figure.

Fail if a reader could still describe it as “a homework grid of grey dots.”

### 7.2 Fate and level diagrams

Same file.

**`path:fig:fate`.** Keep the three coloured regions (certain \(i>j\), contested \(1\le i\le j\), extinct \(i=0\)) and the on-figure legend. Change the dots to the same circle/card language as 7.1. No overflow past the axes. Specifier `[!htbp]`. Caption stays.

**`path:fig:levels`.** Replace the cramped top row `$j-i=0$` `$1$` `$2$` … `$5$` with **readable** callouts: either one label per diagonal sitting in a clear gap, or a small on-figure legend “level \(j-i\)”. Same node language as 7.1. Specifier `[!htbp]`. Caption stays. Lattice geometry stays.

### 7.3 House float specifier

CH2/CH7 use `[!htbp]`, not `[tbp]` and not `[H]`.

Change remaining `[tbp]` / `[bp]` / `[!h]` on **vector** figures to `[!htbp]`:

- TikZ: statespace, fate, levels, `path:fig:tollspectrum` in `sections/05_selection.tex`
- PDFs: `repsupp_N20`, `repsupp_N10`, `vinf_delta`, `ratio_removal`, `flooding_reversal`, and any other included `.pdf`

Screenshot figure environments **may** take `[!htbp]` as well; printed widths must not change. `[!h]` is allowed only as a local fix if `[!htbp]` splits a definition or a remark.

After the change, these must still hold:

- Definition 1.1 is not split by Fig 1.3 (definition complete, schematic under it or immediately after, not interrupted mid-definition).
- Proposition 1.7’s proof is not interrupted by `vinf` / `ratio`.
- Remark 1.13 is not cut by Fig 1.15 (`path:fig:tollspectrum`).

`\FloatBarrier` at section ends stays. `\Needspace` before Def 1.1 stays.

### 7.4 Drop cell numbers on \(N=10\)

File: `figures/_work/repsupp/generate.py`.

`_panel(..., numbers)` currently writes `ax.text` in every tile when `numbers` is true. `main` calls `numbers=(N <= 10)`, so \(N=10\) is a number dump.

- Stop annotating tiles at \(N=10\). Simplest: pass `numbers=False` for both \(N=10\) and \(N=20\) in `draw_strip` / `draw_single` calls (or only for \(N=10\); \(N=20\) already skips dense labels via `step=2` but still should not print numbers).
- Do **not** restyle \(N=20\) otherwise (figsize, cmap, titles, colourbar, dashed diagonal all stay).
- Run from `figures/_work/repsupp/`: `python3 generate.py`
- Closed-form print `worst |pi_jj - closed form|` must still appear and stay on the order of `1e-16`.
- Copy `repsupp_N10.pdf` (and `repsupp_N10_s*.pdf` if the chapter includes them — it includes the strip `repsupp_N10.pdf`) into `figures/`.

### 7.5 Optional mapping table — skip if it costs a page

Only if the compile after 7.1–7.4 is still **28 pages**. If it is already 29, **skip**.

In `sections/05_selection.tex` §1.5.4 (`path:sec:ypestis`), after the sentence “The formulae themselves do not depend on that reading,” a compact CH7-style table of **already-named** objects, for example:

| Model | Reading |
| replicators \(X_t\) | intracellular pathogen in one macrophage |
| granules \(Q_t\) | remaining oxidative store |
| \(\varsigma\) | suppression per replicator–granule pair |
| burst size \(r\) | load at rupture |
| budget \(\vartheta\) | killer cells removed per delivery |
| \(\mathcal{R}(\vartheta)\) | expected surviving release |

No new citations. Do not fill `% NEEDS-BIOLOGY`. Do not add a second copy of Table 1.1. If the table pushes the chapter to 29 pages, delete it.

### 7.6 Compile and visual check (mandatory)

```bash
cd "/Users/adamaldridge/Desktop/Current best/CH8"
latexmk -pdf -interaction=nonstopmode main.tex
```

Must hold:

- Pages ≤ 30 (body+appendices target ~28; ceiling 30).
- 0 overfull boxes, 0 underfull `\hbox` if possible, 0 multiply-defined labels, 0 undefined **local** `path:` references.
- Foreign `??` remain.
- Grep `sections/` for `_parked`, `_work/`, `PLACEHOLDER` — none in printed text.

Then rasterise and look:

```bash
pdftoppm -png -r 140 -f 8 -l 12 main.pdf /tmp/ch8p7/ch8
pdftoppm -png -r 140 -f 16 -l 21 main.pdf /tmp/ch8p7/ch8
```

Stand CH8 Def 1.1 + Fig 1.3, fate, levels, \(N=20\) maps, ratio/reversal next to CH2 pp. 8–10 and CH7 p. 4.

**Fail the pass if:** the lattice is still grey dots; \(N=10\) still prints a number in every cell; Def 1.1 is split; vinf sits on the proof; a screenshot file changed.

If a float regresses, fix the specifier / `\Needspace` / `\FloatBarrier` — do not shrink mathematics or captions as the first resort.

## Non-goals

- Do not rewrite §1, §2, §4.3’s closed form, §5’s reversal, or the discussion.
- Do not restyle matplotlib beyond 7.4.
- Do not recrop screenshots.
- Do not add dummy labels for other chapters.
- Do not copy CH7’s title page or CH3’s explorer stills.

## Done when

A knowledgeable reader can bind a vector-figure page of CH8 next to CH2 pp. 8–10 without a change of node language, and next to CH7 p. 4 without thinking CH8’s absorbing states are just coloured dots. The freeze list is intact. `main.pdf` is ≤ 30 pages and compiles clean locally.

Report: files changed, page count, overfull count, whether 7.5 was taken, and one sentence on the visual check against CH2/CH7.
