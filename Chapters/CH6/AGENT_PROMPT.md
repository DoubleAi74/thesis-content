# Prompt for a fresh agent — CH6 Good-examples layout pass

Copy everything below the line into a new agent session.

---

You are executing a finished layout plan on a thesis chapter. Do it end to end, then stop. Do not reopen earlier structural work. Do not restyle the prose. Do not add science.

## 1. Where you work

```
/Users/adamaldridge/Desktop/Current best/CH6
```

Compile from that directory:

```
latexmk -pdf main.tex
```

Do **not** edit `/Users/adamaldridge/Desktop/Current best copy`. That tree is stale.

The plan you are executing lives at:

```
/Users/adamaldridge/.grok/sessions/%2FUsers%2Fadamaldridge%2FDesktop%2FCurrent%20best%20copy/01a027c8-74ad-76d1-a47d-4cf6616ffcc2/plan.md
```

Read that plan, then this prompt, then the Good examples, then start G1. If the plan and this prompt conflict, this prompt wins on procedure; the plan wins on the list of changes.

## 2. What this chapter already is

Phases 0–6 of an earlier plan are **done**. Do not re-run them.

Already true, and must stay true:

- Intro is question → answers in advance → (A1)–(A5) → short notation table. Formula dump EQ-001–013 lives in App A.
- Body overlays are two figures: `overlay_V.pdf` and `overlay_growth_phase.pdf`. Naive overlay is App C. Bar chart `F4b_3` is not in the body.
- §6 is a coda. ODE cases and Hataye numbers are in App E.
- Figures use house palette `#0072B2` / `#D55E00` / `#1a1c1f` via `figures/_style/style_rc.py`. Cell age is \(\alpha\), birth rate \(\lambda\). No `NEW` / `CLASSICAL` / `producer`.
- App B is master table then notes. App C reproduction path is `verification/verify_result_20_1.py`.
- Last compile: 38 pages, 0 overfull, 0 missing invariant labels.

Your job is a **visual calibration** against three Gold-standard chapters, not another rewrite.

## 3. Frozen science — a defect if you touch it

Ledger: `CH6_invariants.md`. Before you edit any `.tex` that contains mathematics, skim §A and the NUM/PAR tables.

Do not change:

- Displayed equation *contents* (labels stay `p:eq:*`; boxing and line-breaks around them may change).
- Theorem / proposition / remark *statements* and existing proofs (`p:thm:R0inv`, `p:thm:flood`, `p:prop:L1`, `p:rem:novelty`, `p:rem:flood-scope`).
- NUM-* values and PAR-* triples. They must still appear somewhere in the chapter. They may move with a caption.
- Table *data cells*. Headers and captions may be rewritten.
- Comments `% HOOK-MATHS:`, `% NEEDS-REF:`, `% AUTHOR-ACTION`. Do not delete them.

Do not invent a Zenodo DOI. Do not run `/aa-flow-lucid` or `/aa-flow`. Do not restyle §§2–5 body prose. Do not add figures. Do not add HTML visualisers.

After every phase that moves or deletes a float, grep that every `p:eq:`, `p:fig:`, `p:tab:`, `p:thm:`, `p:prop:`, `p:def:`, `p:rem:` label still exists **exactly once**.

## 4. Read these before you edit anything

Open the PDFs as a reader. Do not skim the TeX first.

| File | Why |
|---|---|
| `../Good examples/CH2/main.pdf` pp. 2–8 | Float discipline, caption size, one figure then prose, annotations in the data colour |
| `../Good examples/CH7/Two_Type_Chapter/document MAIN/two_type.pdf` pp. 3–11 | Schematic as visual argument (Fig. 1, first-event tree, Fig. 5–6); caption end-clause `Parameters: …`; float-page top-align |
| `../Good examples/CH7/Two_Type_Chapter/document MAIN/figures/fig01_process_schematic/` | The drawing dialect for G3 |
| `Current best/CH5/main.pdf` opening only | Intro shape — already matched; do not reopen |
| `CH6/main.pdf` whole file, especially pp. 8–9, 14, 20, 21, 28 | Current defects you are fixing |

CH3 (`../Good examples/CH3/chapterB.pdf`) is a different genre. Do not copy its article layout, inline photos, or visualiser links. The only lesson: a figure that restates the surrounding sentence should leave.

## 5. Execute G1 → G7 in order

Do not skip ahead to the schematic. G1’s float counters change where figures land; G3 depends on that.

### G1 — Caption size and float machinery

**File:** `preamble.tex`

1. Change
   ```
   \usepackage[hypcap=false,font=small,labelfont=bf]{caption}
   ```
   to
   ```
   \usepackage[hypcap=false,labelfont=bf]{caption}
   ```
   Captions must print at body-adjacent size, like CH2/CH7. Check CH5’s preamble; if CH5 also uses `labelfont=bf`, keep it.

2. After `\usepackage{float}` (or with the other float settings), add CH7’s placement knobs, adapted for a report chapter:

   ```latex
   \setcounter{topnumber}{2}
   \setcounter{bottomnumber}{1}
   \setcounter{totalnumber}{3}
   \renewcommand{\topfraction}{0.9}
   \renewcommand{\bottomfraction}{0.5}
   \renewcommand{\textfraction}{0.1}
   \renewcommand{\floatpagefraction}{0.8}
   \makeatletter
   \setlength{\@fptop}{0pt}
   \setlength{\@fpsep}{8pt plus 2fil}
   \setlength{\@fpbot}{0pt plus 1fil}
   \makeatother
   ```

   `topnumber=2` is the anti-stacking rule. CH7 used 4 because it is an article with smaller figures. Do not copy 4.

3. Compile once. If any caption is now overfull, shorten *that caption only*, without stripping NUM values.

**Done when:** captions are not `\small`; compile still 0 overfull from this change.

### G2 — Unstack full-width figure pairs

Current stacked pages (numbers may shift after G1; find them by looking at `main.pdf`):

- `overlay_V` and `overlay_growth_phase` (were Figures 1.6 and 1.7 on p.14)
- `N4b_6_generation_times` and `N4b_5_pareto_extinction_growth` (were 1.11 and 1.12 on p.20)

If G1 did not separate them, force it with `[p]` / `[t]` on opposite floats. Do **not** shrink `\includegraphics` widths to make two figures share a page. That is how the old 33% gallery happened.

**Done when:** none of those four figures shares a page with another figure. Sharing a page with prose is correct.

### G3 — Rebuild the renewal schematic in the CH7 dialect

**Source:** `figures/_work/F4b.1/figure.tex`  
**Shipped PDF:** `figures/F4b_1_renewal_schematic.pdf`  
**Visual target:** CH7 Figure 1 (two coloured states, one distinctive absorbing block, body-size type, air around every phrase). Also look at CH7’s first-event tree on p.8 of `two_type.pdf`.

Keep the *information*: incidence \(i(s)=\gamma T\,\mathcal V(s)\) → cell age \(\alpha=t-s\) → survival weight \(I_{\mathrm{fix}}(\alpha)\) and release weight \(g(\alpha)=\delta K(\alpha)\) → \(\mathcal I(t)\), \(\mathcal V'(t)\) → feedback. Same macros already in the file (`\Ifix`, `\Icell`, `\Vfree`). Style file: `\input{../../_style/tikz_style.tex}`.

Change the *drawing*:

- Survival path: house blue `#0072B2`. Release path: vermillion `#D55E00`. Feedback / incidence loop: one distinct ink stroke (`#1a1c1f`), not another grey box identical to the rest.
- In-figure type `\small` minimum. No stacked `\footnotesize` two-line notes. If a phrase needs two lines, the box is too small or the phrase belongs in the caption (`p:fig:renewal-schematic`).
- No label within ~2 mm of another. The previous pass unstuck “each marker starts a cohort” from “cohort born at \(t-\alpha\)”; do not reintroduce that collision, and do not put convolution formulae on the arrows (the destination boxes already carry them).
- Compile standalone, then copy:
  ```
  cd "/Users/adamaldridge/Desktop/Current best/CH6/figures/_work/F4b.1"
  latexmk -pdf -interaction=nonstopmode figure.tex
  cp figure.pdf "/Users/adamaldridge/Desktop/Current best/CH6/figures/F4b_1_renewal_schematic.pdf"
  ```
- Placement: Definition `p:def:renewal-system` and Figure `p:fig:renewal-schematic` on the **same spread**. Prefer `[ht]` on the schematic. The kernels figure (`N4b_7`, `p:fig:kernels`) stays in §3.1; do not let `[t]` on the kernels float steal the definition page. Kernels and schematic are different objects.

**Done when:** a reader can parse the schematic without the caption, and it looks like the same family as CH7 Figure 1, not a dense flowchart.

### G4 — Annotation restraint (three figures only)

Do not restyle every plot.

| Figure | File | Defect | Action |
|---|---|---|---|
| `overlay_V` | `figures/_work/OVL_MAIN/generate.py` | `axes[0, col].text(..., 1.12, s.title)` is a title band above the axes | Put the phrase inside the panel at 9.5 pt as CH7 does, or into the caption. Regenerating writes `figures/overlay_V.pdf`. |
| `N4b_6_generation_times` | `figures/_work/N4b.6/generate.py` | Six annotations on panel (a) | Keep the two means and \(r_{\mathrm{bud}}>r_{\mathrm{burst}}\). Move “later generations” and extra arrows to the caption. |
| Spectrum | `sections/06_reach_of_the_construction.tex` (`p:fig:spectrum`) | Six station names tight on a ~13 cm TikZ axis | Widen or recast as one row of short labels. `\tiny` is forbidden. Keep budding / bursting ends. |

House style for generators: local `figures/_style` on `sys.path` first. Run from the `_work` script so `PDF_PATH` lands in `figures/`. After Python changes, open the shipped PDF, not only `preview.png`.

CH7 *does* allow short in-panel phrases at reading size (“Exact decay to the stable limit”). Bare `(a)` is CH2, not a CH7 absolute. The defect is the **title band above the axes**, not the words “supercritical” / “subcritical”.

### G5 — Drop NX.1 from the chapter

**File:** `sections/A_quoted_results.tex`

- Delete the `figure` environment that `\includegraphics`s `NX_1_trilogy_handoff.pdf`.
- Keep `figures/NX_1_trilogy_handoff.pdf` and `figures/_work/NX.1/` on disk.
- The appendix opening paragraph already names the three handoffs (`\ChCore`, `\ChDist`, this chapter). If a sentence exists only to `\cref{p:fig:handoff}`, delete or rewrite that sentence so it does not need the float.
- Grep `p:fig:handoff` in `sections/`. Zero remaining required refs.

**Done when:** App A still states the handoff in prose; the float is gone.

### G6 — One caption

**File:** `sections/03_renewal_construction.tex`, caption of `p:fig:gillespie`.

Shorten to: object + relative \(L^2\) of 1–2% + left column \(\mu=0\), right \(\mu>0\). The sentence that the renewal equations are not an approximation is already in the body. Do not strip the 1–2% number (NUM-016).

Do not rewrite captions that already fit (kernels, flooding regimes, L-landscape). Do not strip frozen numbers from any caption.

### G7 — Compile, ledger, visual pass

1. `latexmk -pdf main.tex` from `CH6/`. **Overfull boxes = 0.** Underfull boxes in App E tables are acceptable.
2. Ledger (run something equivalent):

   ```bash
   cd "/Users/adamaldridge/Desktop/Current best/CH6"
   # every invariant p:eq: label present exactly once
   # NUM tokens still in sections/*.tex
   # these comments still present:
   rg -n '% AUTHOR-ACTION|% HOOK-MATHS|% NEEDS-REF' sections
   # these must be absent from body tex (figure filenames N4b_/F4b_ are fine):
   rg -n 'cd <|producer|Chapter 3|Chapter 4a|Chapter 4b' sections
   ```

   Report: invariant `p:eq:` count, missing = 0, duplicate labels = 0.

3. Visual pass of `main.pdf` with CH2 and CH7 open. Walk: title → intro (do not edit) → obstruction → kernels in §3.1 → definition + schematic on one spread → two overlays on **separate** pages → flooding → short reach → discussion → App A without NX.1. Check every figure for leftover title bands, age labelled \(a\), birth labelled \(\beta\).

**Done when:** compile clean; ledger missing = 0; stacked full-width figures = 0; schematic parses without the caption.

## 6. Rebuild commands you will need

TikZ schematic: see G3.

Matplotlib (from `CH6/`):

```
python3 figures/_work/OVL_MAIN/generate.py
python3 figures/_work/N4b.6/generate.py
```

Confirm each script writes the production PDF under `figures/`, not only `preview.png`.

## 7. What you report at the end

A short completion note, not a memoir:

- Pages, overfull count, undefined refs.
- Ledger: `p:eq:` found / missing / duplicate.
- Which of G1–G7 you did, and any G1 float-counter result that made G2 unnecessary.
- Remaining author actions (do not do these): Carruthers check, eclipse-division confirm, BibTeX pages, `% NEEDS-REF:`, three `% HOOK-MATHS:` proofs.

If something in G3 or G4 is blocked (style file missing, generator path wrong), say so and ship the rest. Do not invent a second schematic dialect. Do not expand scope into §6 prose or the intro.
