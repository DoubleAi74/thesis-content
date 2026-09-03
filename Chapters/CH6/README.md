# CH6 — rewritten as a journal article

`chapter.tex` is a single self-contained, thesis-ready fragment (opens with
`\chapter`, no preamble of its own). Build the standalone PDF with
`latexmk -pdf main.tex`. To drop it into the thesis, merge `preamble.tex`
into the thesis preamble and `\input{chapter}`.

- 34 pages (was 42), 8 sections + 3 appendices (was 7 sections + 6 appendices).
- Compiles clean: no undefined references or citations, no overfull boxes.

## What the rewrite does

**Spine.** One construction (the BDC-forced renewal system), three
consequences (projection / identifiability / the L comparison), one scope
section. Contributions are stated as a numbered list in the introduction.

**The L analysis is the centrepiece.** `L = a(1-b)` is now a named
Definition, followed immediately by the flooding theorem, the boxed
criterion `1/δ < 1/λ + 1/μ`, the L-landscape figure and the extinction
table — all in one place. §4.4 (`Relation to existing multiscale models`)
and §6 both make the point that the L result is what the *stochastic*
intracellular model buys: it turns on the offspring distribution, so no
deterministic multiscale model can produce it.

**Ciupe & Conway (2024) is cited 10 times across 9 subsections**, as the
framing of the field in the introduction and then at load-bearing points:
nonlinear incidence, the (S,g) table, the eclipse, identifiability (twice),
antiviral mode of action, HIV incidence, fitting practice, coinfection.

## New material

- §4.4 **Relation to existing multiscale models** — positions the work
  against Nelson et al. and against the Guedj/Rong HCV multiscale model,
  which is a prior instance of the same skeleton. The novelty claim is now
  "stochastic, hence distributional", not "derived age structure".
- §5.6 — Mittler et al.'s delay-distribution insensitivity is reconciled
  with the projection theorem (it is the same statement seen from the
  fitting side), with Kakizoe et al. as the counterweight.
- §7.2 **Partial release, and antiviral mode of action** — maps the DAA
  parameters onto the kernels; `φ = 1 − ε_s` exactly. Two testable
  consequences.
- §8.1 — the HCV clearance-rate story (6.2 vs 23.3 /day) as a published
  precedent for "a fitted rate is a property of the phase".
- §4.1 — Gilmore et al. as measured evidence for age-dependent `d_I`.
- §6.5 — Lord & Bonsall as the closest published relative of the
  bursting/budding comparison.
- §8.2 — Koelle et al.'s macroparasite bookkeeping as the relative of `Q`.

## Cut

The 12-model self-excitation catalogue, the five-ODE-case ladder as a
standalone section, the HIV stage-model appendix and TikZ diagram, the
trilogy-handoff figure, the naive-overlay figure, the spectrum TikZ strip.
HIV is now one compressed subsection (§7.3). Four now-unused figure PDFs
were deleted from `figures/`.

## Author actions outstanding

1. `references.bib` — the 12 new entries in the final block were taken
   verbatim from Ciupe & Conway's reference list and should be correct.
   Pre-existing `TODO(verify)` markers (McLean 1993, Nowak & Bangham, Lloyd
   2001 realistic, Champredon, van Doorn & Pollett, and others) are
   inherited and still outstanding.
2. Appendix C carries the `% AUTHOR-ACTION` for a repository URL or DOI for
   the verification suite.
3. All displayed numbers were re-verified independently during the rewrite:
   the three-regime table, `⟨X²⟩_QS = 231 / 30.5`, the old-cell limit in all
   three regimes, every row of the flooding table against `(L-1)(1/m-1)`,
   the growth-rate table, and the generation times `3.398 / 4.089`.


---

# Appearance pass

A second pass on how the chapter looks. Twelve changes, all verified against
a clean build: **0 overfull boxes, no undefined references or citations, 40
pages.** The figures were regenerated from their own sources and the
verification suite re-run (**124 checks, 0 failures**).

## Typography

**Measure.** *Reverted at the author's request.* `main.tex` is back to the
original `margin=1in` on A4, a 453pt block measuring about 92 characters per
line. (For the record: an asymmetric 373pt block gave 77.4 characters, which
is nearer the 60-75 that reads comfortably. Restoring it is a one-line
change to the `geometry` call.)

The document is still `twoside`. That is what lets the running heads split
across the spread -- chapter on the verso, section on the recto. Set on one
side both marks land on every page and overlap, since both are long. If
one-sided output is wanted, drop `twoside,openright` from the class options
and put only `\rightmark` in the header.

**Running heads.** `fancyhdr`: chapter short title on the verso, section on
the recto, a hairline rule in the accent colour, page number centred in the
foot. Chapter-opening pages carry no rule.

**Short chapter title.** `\chapter[Burst-aware within-host dynamics]{...}`
so the running head is legible; the full title still appears on the chapter
page.

**Page breaking.** Widow, club, display-widow and broken penalties all at
10000, plus `\raggedbottom`: a slightly short page in preference to a
stranded line.

## Visual hierarchy

**Theorems are set apart.** The chapter turns on four results, and they were
previously indistinguishable from the six supporting propositions. `theorem`
now gets a tinted panel with an accent left rule (`mdframed`); propositions,
definitions and remarks stay in the ordinary run of text, so the distinction
carries information.

**Proofs are subordinated.** Set one size down in a soft grey, so a
statement reads clearly against its own argument.

**The flooding criterion is promoted.** `1/δ < 1/λ + 1/μ` now sits in a
`keyresult` panel rather than a `\boxed{}` inside a numbered display. Used
once only -- using it twice would spend the emphasis.

**One accent colour**, `#0072B2`, shared with the figures, so a rule on the
page and a curve in a panel are the same blue.

## Figures

All 15 regenerated from `figures/_work/*/generate.py` and
`verification/verify_result_20_1.py`.

**Typography now matches the document exactly.** `_style/style_rc.py` set
`font.serif: ["DejaVu Serif"]` with Computer Modern mathtext, so every panel
had its words in one family, its maths in a second, and neither matched the
Latin Modern body; three figures also fell back to STIX for `\star` and
`\mathbb{E}`. The style file now renders figure text through LaTeX itself
(`text.usetex`, `lmodern` preamble). Every figure now embeds only
LMRoman/LMMathItalic/LMMathSymbols plus MSBM -- the document's own font set,
at proper optical sizes. If LaTeX is unavailable the file falls back to the
Latin Modern OTFs shipped with TeX Live, which it registers with matplotlib
directly; `CH6_NO_USETEX=1` forces that path.

**Figure 1.10 collision fixed.** In panel (a) the budding curve ran straight
through the `L = 1.10, (1,0,0.1)` annotation. The caption block now takes
the free corner per panel, with a translucent backing box as a guard.

**Figure 1.6 regimes corrected.** `peff_dr_curves` plotted
`(1, 0.2, 0.05)` as its purple middle curve while every other figure used
`(1, 0.5, 1/3)` -- the same colour denoting different parameters one page
apart. It now uses the canonical trio of Table 1.2, with `1/3` set as a
fraction.

## Tables and equations

**Decimal alignment.** Tables 1.2, 1.5 and 1.6 use `siunitx` `S` columns, so
numeric columns align on the decimal point.

**Floats.** Every figure and table is cross-referenced from the text, and
every figure in `figures/` is used by the chapter.

**Equation numbering.** Two purely expository displays were unnumbered. The
other 17 unreferenced numbers were left alone: they are appendix reference
formulae or the content of a named result, where the number earns its place.

## New dependencies

`preamble.tex` now requires **siunitx**, **mdframed** and **needspace**;
`main.tex` additionally requires **fancyhdr** and **geometry**. All are in
TeX Live. On merging into the thesis, note that `\raggedbottom` and the
penalties live in `preamble.tex` and are document-level choices worth
reviewing; the geometry and running heads live in `main.tex` and will be
superseded by the thesis preamble.

## Rebuilding the figures

```sh
cd figures/_work
for d in N4b.1 N4b.2 N4b.4 N4b.5 N4b.6 N4b.7 F4b.2 PEFF OVL_MAIN OVL_GROWTH; do
  PYTHONPATH="../_style:." python3 "$d/generate.py"
done
cd F4b.1 && pdflatex figure.tex && cp figure.pdf ../../F4b_1_renewal_schematic.pdf
cd ../../..                      # chapter root
PYTHONPATH="figures/_style" python3 verification/verify_result_20_1.py
cp verification/verify_figures/H_gillespie.pdf figures/
```

The suite also writes `D_exponential_reduction`, `E_growth_rate_match` and
`F_R0_threshold`. Those illustrated the verification appendix and are no
longer used by the chapter, so they stay in `verification/verify_figures/`
and are not copied across.

`figures/_work/_renewal_check.py` validates the renewal solver against the
chapter's published values; run it before trusting any overlay.


---

# Later edits

**Text width reverted** to the original `margin=1in` (453pt, ~92 chars/line).
The rest of the appearance pass is unaffected.

**Appendix C (Verification record) removed.** The appendices are now
A (single-cell results), B (Laplace transforms), C (master formula table) --
relettered automatically by the `\Alph{section}` counter, so nothing else
needed changing. Repairs made where the body pointed into it:

- Section 4.5 no longer cross-references the appendix. Because it still
  claims "all 62 checks pass", one sentence was added naming the suite, the
  five parameter sets it runs over, and tests M and N, so the claim keeps
  its provenance. The `% AUTHOR-ACTION` for a repository URL or DOI moved
  there with it.
- The `(S,g)` table's first row pointed at the appendix's Figure D; it now
  points at section 4.5.
- The two numerical-sweep citations in sections 5.3 and 6.4 now read
  "test M / test N of the verification suite" rather than citing a section.
- Three figures (`D_exponential_reduction`, `E_growth_rate_match`,
  `F_R0_threshold`) had no consumer left and were removed from `figures/`.
  They are still produced by the verification suite into
  `verification/verify_figures/`.
- Assumption (A4) was rephrased to clear an overfull line that reappeared at
  the restored width.

`verification/` is kept in full: it is the provenance for the 62-check claim
and for every number in the chapter.
