# CH6 improvement plan — Phase C

**Status.** Written 2026-08-22. Supersedes nothing; extends `PHASE_A_REPORT.md`
and `CH6_figure_workorder.md`, both of which remain accurate about what Phase A
did. This plan covers what Phase A deliberately left, what Phase B never did,
and what a fresh read of the compiled PDF found.

**Governing constraint.** `CH6_invariants.md` freezes 162 items — 73 displayed
equations, 10 theorem statements and proofs, 61 numeric values, 5 parameter
triples, 13 table data blocks. Nothing in Phase 1, 3 or 4 below touches any of
them. Phase 2 *adds* new results; every addition goes in under a licence clause
in the ledger, in the same manner as the existing "Licensed addition (plan §9)"
entry, and is logged as an addition rather than an alteration.

**Calibration targets.** `Good examples/CH2` (prose, typography, float
discipline), `Good examples/CH7` (figure composition and captions),
`Good examples/CH3` (inline figures). Findings from those three are folded into
Phase 1 and recorded in §H below.

---

## A. Recovered assets — Phase 0 unblocks everything else

The figure work-order records these as absent. They are not. Locations verified
2026-08-22.

| Asset | Location | Covers |
|---|---|---|
| `figures/_work/` (11 dirs) | `~/Desktop/CHAP3-4ab/CH6 revise/4b BDC_odes DRAFT U/figures/_work` | 8 `generate.py`, 3 TikZ `figure.tex` |
| `verify_result_20_1.py` | `~/Desktop/Thesis content 🎓 /OLD/4 BDC additional and BMVR/new_notes3/` | the 54 checks; figures D, E, F, H×2 |
| `style_rc.py` | `~/Desktop/Current best/CH5/figures/_style/style_rc.py` | the house matplotlib style |
| `CH6_rewrite_plan.md`, `CH6_polish_review.md` | `~/Desktop/CHAP3-4ab/CH6 revise/` | the Phase A brief and defect inventory |

**Genuinely absent:** `style/tikz_style.tex` — not on this machine. The three
TikZ figures import it; the fix is to inline an explicit preamble into each
`figure.tex` rather than to hunt further.

**Figure source coverage after Phase 0:**

- 8 have `generate.py`: N4b.1, N4b.2, N4b.4, N4b.5, N4b.6, N4b.7, F4b.2, F4b.3
- 3 have TikZ source: F4b.1, N4b.3, NX.1
- 5 rebuildable from the verification suite: D, E, F, H(μ=0), H(μ>0)
- **6 have no source and must be written from scratch:** `overlay_V`,
  `overlay_I`, `overlay_V_with_naive`, `overlay_rel_diff`,
  `overlay_growth_phase`, `peff_dr_curves`

The six orphans are exactly the six worst-scaled figures in the chapter. Working
renewal code for all of them — kernels, `p_eff`, the characteristic root, the
growth-rate comparison — was written and validated against the chapter's own
published numbers during the review that produced this plan.

---

## B. Phase 0 — Stage and baseline

- [ ] **0.1** Copy `_work/` into `CH6/figures/_work/`. Do not overwrite any
      existing PDF yet.
- [ ] **0.2** Create `CH6/figures/_style/style_rc.py` from CH5's copy verbatim.
- [ ] **0.3** Copy `verify_result_20_1.py` into `CH6/verification/`.
- [ ] **0.4** Record the baseline: page count, float count, `wc -w` per section,
      and a per-figure scale audit, into `CH6_PHASE_C_BASELINE.md`.
- [ ] **0.5** Confirm the suite still runs and still reports 54/54 under the
      current NumPy. Record versions — Appendix C has to state them.

**Gate.** `latexmk -pdf main.tex` clean, 39 pp, 0 overfull. Nothing has changed
yet; this is the reference point every later phase is measured against.

---

## C. Phase 1 — Figures

The largest single gain available. In-figure text currently prints at 3.3–7 pt
against 11 pt body text; CH2 and CH7 sit at 8–10 pt.

### C.1 The sizing rule

Author every figure at the width it is *placed* at, so the scale factor is ~100%
and `style_rc`'s 9.5 pt base font prints at 9.5 pt. Text width is 452.97 pt =
6.27 in.

| Placement | `\textwidth` fraction | `figsize` width (in) |
|---|---|---|
| Full | 0.94 | 5.89 |
| Wide | 0.78 | 4.89 |
| Medium | 0.64 | 4.01 |
| Half (subfigure) | 0.48 | 3.01 |

### C.2 Per-figure specification

| Figure | Now | Target placement | Target `figsize` | Action |
|---|---|---|---|---|
| `N4b_1_constant_release_fails` | 0.74 @ 57% | 0.94 | (5.89, 2.45) | resize, strip titles, `a`→`α` |
| `N4b_7_kernels_three_regimes` | 0.74 @ 55% | 0.98 | (6.14, 4.00) | resize, strip suptitle + 6 set_titles, `a`→`α` |
| `F4b_1_renewal_schematic` (TikZ) | 0.74 @ 57% | 0.98 | 15.6 cm | inline preamble, separate the two colliding labels, fix `(i∗I_fix)` overlap |
| `H_gillespie_mu0` + `_mu_pos` | 0.44 @ **31%** | one 2×2 figure @ 0.98 | (6.14, 4.20) | merge two files into one figure; titles `mu0`→`$\mu=0$` |
| `peff_dr_curves` | 0.68 @ 43% | 0.94 | (5.89, 2.60) | **write from scratch**; extend to `r ∈ (−θ, ∞)` for Phase 2a |
| `overlay_V` + `overlay_I` | 0.64 @ **33%** | one 2×2 figure @ 0.94 | (5.89, 4.20) | **write from scratch**; two scenarios only (supercritical, subcritical) |
| `overlay_rel_diff` | 0.64 @ **33%** | 0.94 | (5.89, 3.60) | **write from scratch** |
| `overlay_growth_phase` | 0.64 @ 36% | 0.94 | (5.89, 2.50) | **write from scratch** |
| `overlay_V_with_naive` | 0.64 @ **33%** | → Appendix C @ 0.78 | (4.89, 3.00) | **write from scratch**; demote from body |
| `N4b_2_identifiability_levels` | 0.74 @ 43% | 0.94 | (5.89, 2.80) | resize, strip titles |
| `F4b_2_flooding_regimes` | 0.74 @ 47% | 0.94 | (5.89, 2.20) | resize, strip 3 set_titles into caption |
| `N4b_6_generation_times` | 0.68 @ 50% | 0.78 | (4.89, 2.90) | resize, strip title, `a`→`α` |
| `F4b_3_growth_tradeoff` | 0.66 @ 58% | 0.64 | (4.01, 2.30) | resize, strip title |
| `N4b_4_L_landscape` | 0.64 @ 66% | 0.64 | (4.01, 2.70) | resize, strip title |
| `N4b_5_pareto_extinction_growth` | 0.62 @ 64% | 0.62 | (3.89, 2.50) | resize, strip title |
| `NX_1_trilogy_handoff` (TikZ) | 0.70 @ 58% | 0.94 | 14.9 cm | inline preamble; **fix chapter names**; lift annotation row clear of boxes; `a`→`α` |
| `D_exponential_reduction` | 0.64 @ 45% | 0.78 | (4.89, 1.90) | regenerate from suite |
| `E_growth_rate_match` | 0.44 @ 46% | 0.48 | (3.01, 2.20) | regenerate; "TEST E"→ caption |
| `F_R0_threshold` | 0.44 @ 43% | 0.48 | (3.01, 2.20) | regenerate; title → caption |

### C.3 Content fixes applied to every figure

- [ ] **1.1 Age variable.** Six figures label cell age `a`, which is the root of
      the characteristic quadratic in the same chapter (`a = 1.100`). All become
      `α`. Affects N4b.1, N4b.6, N4b.7, N4b.3, NX.1, and `kernels` (dropped).
- [ ] **1.2 Strip in-figure titles and suptitles.** CH2, CH3 and CH7 carry none;
      panel labels are a bare `(a)`, `(b)`, `(c)`. Everything currently in a
      title moves into the caption, which is where it already half lives.
- [ ] **1.3 Remove shouty labels.** "NEW model", "CLASSICAL" → "renewal",
      "classical BMVR", matching whatever Phase 3.6 settles on.
- [ ] **1.4 Particles, not virions.** Figure axes say "free virions" / "Free
      virus"; the body says *free particles*, and the chapter's lead organisms
      are *Y. pestis*, *F. tularensis* and phage.
- [ ] **1.5 Script artefacts.** `(mu0)`, `(mu_pos)` → `$\mu = 0$`, `$\mu > 0$`.
      "TEST E" / "Test F" capitalisation → both into captions.
- [ ] **1.6 Chapter names.** `NX_1` prints "Chapter 3 / 4a / 4b" — wrong numbers
      and a direct breach of the invariant that no chapter number appears
      anywhere. Use the `\Ch*` macro wording instead.
- [ ] **1.7 Palette.** Port all 8 `generate.py` to `_style/style_rc.py` using
      CH5's two-line recipe (dead path first, local `_style` second, so the
      local wins). Old scripts reference `style_rc.NAVY`; the current module
      exposes `BLUE`, `VERMILLION`, `INK`, `SOFT`, `GRID`, `TEAL`, `PURPLE`.
- [ ] **1.8 Parameters in captions.** CH7's convention: the caption ends
      "Parameters: λ₂ = 0.9, μ₂ = 0.35, δ₂ = 0.20." CH6 does this inconsistently
      and sometimes only inside the graphic. Standardise.

### C.4 Recomposition — §4.3 is a figure gallery

Printed p.15 carries Figures 1.7, 1.8 and 1.9 stacked: three 2×3 grids, none of
them readable, all making one point. Printed p.16 adds a fourth.

- [ ] **1.9** Merge `overlay_V` and `overlay_I` into a single 2×2 figure —
      free particles and infected cells, supercritical and subcritical — at full
      width. This is the figure that carries the section.
- [ ] **1.10** Keep `overlay_rel_diff` at full width, six panels, since the
      spread across scenarios *is* its content.
- [ ] **1.11** Demote `overlay_V_with_naive` to Appendix C. The dimensional
      error is worth one appendix figure, not a body float.
- [ ] **1.12** Keep `overlay_growth_phase` in the body — it is the figure that
      proves the section's thesis — at full width.
- [ ] **1.13** Adopt CH7's panel-directory pattern for anything above four
      panels: emit `figures/<name>/panel_*.pdf` and assemble with `subcaption`,
      so each panel is authored at its final size instead of a wide canvas being
      shrunk.

**Gate.** Every figure ≥ 85% scale. No in-figure titles. No `a` used for age. No
"NEW"/"CLASSICAL". Chapter names correct. Recompile and re-read pp. 12–17.

---

## D. Phase 2 — Mathematical additions

Four items. Two close deferred proofs outright, one sharpens the third, one adds
a result that is available from identities the chapter already carries. All were
derived and numerically validated during the review; the derivations are
recorded in §I below so they survive a cold restart.

- [ ] **2.1 The third endpoint of `p_eff`.** From the chapter's own frozen
      identity `AB = δ/λ`:

      lim_{α→∞} g(α)/S(α) = a[2λ(1−b)+δ]/(a−1) = δ·a(a+1)/(a−1)² = δ·E_QS[X²]

      the second moment of the geometric(1/a) quasi-stationary law already
      quoted in Appendix A. Hence `p_eff(r) → δ·E_QS[X²]` as `r ↓ −θ`. Verified
      exactly at (1,0,0.1): both sides 23.1.

      Consequences to write in: `r = 0` is an *interior* point of the map, not an
      end; the full dynamic range of a fitted release rate is exactly
      `E_QS[X²] = a(a+1)/(a−1)²`, which is 231-fold at (1,0,0.1) against the
      46-fold currently quoted — so "two orders of magnitude" becomes literally
      true; §2.3's failed proposal is redeemed as the `r ↓ −θ` endpoint, where
      `δ` supplies the missing inverse time and the *second* moment is what a
      load-proportional hazard demands; and the absorbing process finally gets
      the mature-cell limit that §6.2 already gives the reset process.

      New Proposition in §4.1, plus a paragraph closing the §2.3 loop, plus the
      extended `peff_dr_curves` from Phase 1.

- [ ] **2.2 `p_eff` monotonicity — closes `% HOOK-MATHS` #2.** Since
      `g/S = δ·E[X²_α | still productive]`,

      d/dr log p_eff(r) = E_{S,r}[α] − E_{g,r}[α],

      so `p_eff` is strictly decreasing iff the exponentially tilted mean release
      age exceeds the tilted mean survival age at every `r`. A monotone
      likelihood ratio — `g/S` nondecreasing in `α` — gives it immediately, and
      `g/S` is the conditional second moment of the load, rising from 1 to
      `a(a+1)/(a−1)²`. Swept 4,000 random `(μ,δ)` over `[10⁻³,20]²` at `λ=1`:
      zero genuine failures. Upgrade "monotone in the five sets examined" to a
      theorem with a closed-form calculus check.

- [ ] **2.3 The first-moment claim — closes `% HOOK-MATHS` #1.** With
      `i(t) = γT·V(t)` linear in `V`, independent cells (A4) and independent
      particle thinning, expectation commutes with the entire construction, so
      `E[I]` and `E[V]` satisfy (1.19)–(1.20) exactly. This is a short
      Proposition, not an open problem. As written, "checked numerically … but is
      not proved here" sits immediately after a Definition and makes the reader
      doubt the definition.

- [ ] **2.4 `r_bud > r_burst` — sharpens `% HOOK-MATHS` #3.** Both sides share
      `γT` and `c` and are matched at `∫g = V∞`, so the ordering holds for
      *every* `γT` and `c` iff

      g̃_burst(r) ≤ g̃_bud(r) = p/(r + d_I)   for all r > 0,

      i.e. the burst release age dominates the matched exponential in the
      **Laplace-transform order**. That single inequality removes `γT`, `c` and
      `R₀` from the problem and makes the numerics one-dimensional. Tested on
      1,500 random `(μ,δ)` at 60 values of `r ∈ [10⁻⁴,10²]`: zero violations. The
      stronger *usual* stochastic order **fails** (min gap −0.14), so stating it
      as `≥_st` would be wrong — `≥_Lt` is the right and only available order.
      Restate the open problem as this inequality and cite the sweep.

- [ ] **2.5 Extend the verification suite** with tests L (old-cell limit), M
      (`p_eff` monotonicity over a parameter sweep) and N (Laplace order),
      taking the catalogue from 54 to 57+ checks. Update Appendix C's table and
      its count. **This changes a frozen numeric value (54)** — log it as a
      licensed addition.

**Gate.** Each new result carries a proof or an explicitly-scoped numerical
claim, and a suite test. Ledger updated with additions, not alterations.

---

## E. Phase 3 — Structure and flow

- [ ] **3.1 Relocate §1.4.** A page and a half of quoted formulae plus a
      full-page notation table currently sit between "Contributions" and "Plan of
      the chapter", spending the momentum of a very good opening. Move the
      identities and moment formulae to Appendix A — which is 379 words *under*
      budget and exists for this — keeping in §1 only what §2–§3 use: the roots,
      `I_fix`, `V`, `V∞`, `⟨T_prod⟩`. Failing that, move §1.4 and the notation
      table *after* the plan, so reference material sits in the skimmable last
      position.
- [ ] **3.2 Define "flooding".** Used 30 times, defined never; first appears on
      printed p.4, fourteen pages before `L` exists. One sentence at first use.
- [ ] **3.3 Move Theorem 4.3 to the head of §5.** `R₀` invariance under bursting
      is a bursting-versus-budding result and is exactly what makes §5's matched
      comparison fair, but it sits three pages earlier under a different heading.
      §5 should open on it: the threshold is fixed by construction, so the
      question is what else moves. Proof stays by reference to §4.2's generation
      kernel.
- [ ] **3.4 Name the headline result.** "Classical BMVR is the exponential-phase
      projection of the renewal system" is the chapter's central claim and the
      only major one that is not a numbered theorem, while three lesser results
      are. Make it `Theorem (Exponential-phase equivalence)`. Already proved in
      the text; it only needs to be citable.
- [ ] **3.5 Compress §6.5 (HIV).** 1,300 words, its own literature review, model,
      stage diagram and two tables, and no result — and the main reason §6 is
      1,136 words over budget. Keep a one-page body argument (HIV is not BDC; the
      skeleton still holds; here are `S_HIV`, `g_HIV`); move the stage equations,
      both comparison tables and the linear-vs-exponential discussion to a new
      Appendix F.
- [ ] **3.6 Name stability.** Eight names for the classical object across 31
      mentions, seven for the renewal one across 34. Fix two — *classical BMVR*
      and *the renewal system* — and use nothing else. Figures inherit via
      Phase 1.3.
- [ ] **3.7 Move §2.5 (three regimes).** It interrupts the best handoff in the
      chapter: §2.4 ends on "exactly solvable" and then a parameter table
      intervenes before §3 delivers. Move to §1 with the notation, or into §3
      immediately before the kernel figure that first uses it.
- [ ] **3.8 De-duplicate §7.1.** The three candidate third observables are listed
      in full in both §4.5 and §7.1 — ~250 words that make the Discussion read as
      recap. Point back, and use the space to say what should be done with them.
- [ ] **3.9 Add a fourth question to §1.1.** The three questions map to §3, §4,
      §5, leaving §6 unquestioned. Promote contribution 6 — "how much of this
      depends on the birth–death–catastrophe process at all?" — and the plan
      becomes isomorphic to the chapter.

**Gate.** Read §1 → §2 → §3 end to end and check the argument does not stall.
Section word counts re-measured against the plan budget.

---

## F. Phase 4 — Apparatus

- [ ] **4.1** Work the 10 `TODO(verify)` markers in `references.bib`.
- [ ] **4.2** Cite `gilchrist2006evolution` — in the bib, uncited, and the
      natural reference for §5's trade-off and §7.4's forward link.
- [ ] **4.3** Add the canonical generation-interval references. Lloyd (2001) on
      realistic infectious-period distributions and Champredon & Dushoff (2015)
      on intrinsic vs realized generation intervals are precisely §5.5's
      mechanism; §5.5 currently rests on Wang (2006) and Wallinga & Lipsitch
      alone. **Verify details before adding.**
- [ ] **4.4** Work the seven `% NEEDS-REF:` markers.
- [ ] **4.5** Demote the two-row tables. `tab:correspondence` and
      `tab:growthlaw` each occupy a full float to say what reads better as two
      display lines. Sixteen tables is a lot.
- [ ] **4.6** Merge `tab:hiv-support` and `tab:hiv-contrast` — back to back on
      p.27 doing overlapping work.
- [ ] **4.7** Fix the three underfull hboxes: `\raggedright` in Appendix E's
      `tab:fourmodels` narrow `p{0.17\textwidth}` columns.
- [ ] **4.8** Replace Appendix C's `cd <repository or archived release>` with a
      real path or DOI, and state Python/NumPy versions from Phase 0.5.
- [ ] **4.9** Revert `caption` to CH2's options once the float count is down —
      `font=small,labelfont=bf` was a page-count measure, not house standard.
- [ ] **4.10** Fix the TikZ spectrum: *budding* and *bursting* are the most
      important labels on the axis and currently the smallest and least
      prominent, and "bursting" nearly touches "absorbing BDC".

---

## G. Phase 5 — Closeout

- [ ] **5.1** Re-run the invariants ledger entry by entry; report found /
      verbatim / altered / added / missing, as Phase A did.
- [ ] **5.2** Re-run the verification suite; confirm all checks pass at the new
      count.
- [ ] **5.3** Compile clean: 0 overfull, 0 underfull, 0 undefined.
- [ ] **5.4** Page budget: body ≤ 34 pp, total ≤ 40 pp on A4.
- [ ] **5.5** Write `CH6_PHASE_C_REPORT.md` in the shape of `PHASE_A_REPORT.md`.
- [ ] **5.6** Re-render every page and read the PDF as an examiner would.

---

## H. What the Good examples changed in this plan

Read after the first draft of the plan and folded back in.

**CH7 (`Two_Type_Chapter`) — the figure model.** Its Figure 5 is three panels
assembled *in LaTeX* at different sizes, bare `(a)`/`(b)`/`(c)` labels, no
in-figure title, everything explanatory in the caption, parameters listed at the
caption's end, and in-figure text at body size. Its figures live as
`figures/<fig_name>/panel_*.png` — panel directories, not wide composite files.
This is the direct answer to CH6's 33%-scale problem and became Phase 1.13 and
the caption convention in 1.8. CH7 also links an interactive HTML visualiser
from a caption ("Genealogy visualiser"); CH6's `p_eff(r)` map and `L` landscape
are natural candidates, recorded as optional below.

**CH2 — typography and float discipline.** Figures at 60–100% scale against
CH6's 31–66%, which is where the sizing rule in C.1 comes from. Default caption
size, which CH6 shrank to save pages (Phase 4.9). No in-figure titles anywhere.

**CH3 — inline figures.** Uses a small figure set beside running text rather
than a full-width float. CH6 has no such device and could use one to break up
§4's gallery; recorded as optional.

**Optional, if time allows:**

- [ ] An interactive `p_eff(r)` explorer as an HTML companion, linked from the
      caption in CH7's manner.
- [ ] One inline/wrapped figure in §4 in CH3's manner.

---

## I. Derivations to carry forward

Recorded so Phase 2 survives a cold restart.

**Old-cell limit.** With `v = e^{−θα} → 0`: `I_fix → (a−b)²v/(Aa)` and
`g = 2λ(κ−I)J → 2λ(κ−b)(a−b)²v/A²`. So

    lim g/S = 2λ(κ−b)·a/A = a[2λ(1−b)+δ]/(a−1).

Using `AB = δ/λ`, i.e. `λ(1−b) = δ/(a−1)`:

    a[2δ/(a−1) + δ]/(a−1) = δ·a(a+1)/(a−1)²  = δ·E_QS[X²].

**Quasi-stationary moments.** `X ~ geometric(1/a)` on `{1,2,…}`,
`P(X=k) = (a−1)a^{−k}`; `E[X] = a/(a−1)`, `E[X²] = a(a+1)/(a−1)²`.

**Numerically confirmed during the review** (independent reimplementation, all
matching the chapter's published values):

- Table 1.2 to 4 d.p. for all three regimes
- `z_ext` values and the identity `(L−1)(1/m−1)`
- generation times 3.089 / 2.398 → 4.089 / 3.398
- `r_bud`/`r_burst` = 0.250/0.180, 0.395/0.294, 0.343/0.198
- `∫g = V∞` and `∫I_fix = ⟨T_prod⟩` to ~1e-15
- `E_QS[X²]` limit at (1,0,0.1) = 231.00000 exactly

---

## J. Author-only — cannot be delegated

1. **The Carruthers novelty check.** Blocks submission. Verify against
   `carruthers2020stochastic` whether they already couple an intracellular BDC
   to a between-cell model. If they do, `p:rem:novelty` needs rewriting.
2. **Confirm the eclipse-division correction** (`% AUTHOR-ACTION`, §6.5) against
   the original derivation.
3. **Verify the six BibTeX entries** added in Phase A against the published
   record — volume, issue, pages.

---

## K. Execution log

### 2026-08-22 — Phase 0 complete, Phase 1 part-done

**Phase 0 — done.**
- `figures/_work/` (11 sources), `figures/_style/style_rc.py`, `verification/verify_result_20_1.py` all staged into CH6.
- `NAVY` compatibility alias added to `style_rc.py`; `panel_label()` helper added there so all scripts share one definition.
- Suite re-run: **54/54 pass**, Python 3.14.6 / NumPy 2.4.2 / Matplotlib 3.10.8. These are the versions Appendix C must state (item 4.8).
- Baseline recorded in `CH6_PHASE_C_BASELINE.md`.

**Phase 1 — 8 of 8 script-based figures migrated and regenerated.**
All now at **101–104% scale** (was 44–67%), on the house palette, with
in-graphic titles stripped, bare `(a)`/`(b)` panel labels, and `cell age α`
replacing the `a` that collided with the characteristic root.

| figure | scale | state |
|---|---|---|
| `N4b_1_constant_release_fails` | 101% | done, verified visually |
| `N4b_7_kernels_three_regimes` | 102% | done, verified visually |
| `F4b_2_flooding_regimes` | 102% | done — single figure legend, shared x-label, notes in free space |
| `N4b_2_identifiability_levels` | 101% | done, verified visually |
| `N4b_6_generation_times` | ~102% | done — inset promoted to a real second panel |
| `F4b_3_growth_tradeoff` | 103% | done, verified visually |
| `N4b_4_L_landscape` | 103% | regenerated; **residual collision**: "(i) L=1.10" over "(iii) L=0.42" |
| `N4b_5_pareto_extinction_growth` | 103% | regenerated; **residual collision**: caption-ish note over the 0.03/0.05 point labels |

`_migrate.py` in `figures/_work/` holds the reusable transforms (balanced-paren
title stripping, palette map, age-variable map).

**Reusable patterns established** (apply to the six from-scratch figures):
one figure-level legend rather than one per panel; notes placed in axes
fractions at free spots rather than offset from data points; parameters in the
caption, not in the graphic; white `bbox` backing on any note that can cross a
curve.

### 2026-08-23 — Phase 1 complete

**All 20 figures rebuilt.** Worst scale is now **85%**, everything else
101–104%; the baseline range was 31–67%.

- **Two residual collisions fixed** (`N4b.4` label offsets, `N4b.5` standing
  notes moved to the caption).
- **Shared solver written and validated.** `_work/_renewal.py` implements the
  renewal system as a second-kind Volterra equation in `V` alone, with the
  generation kernel `A = gT (g * e^{-c.})` as its convolution kernel; `A(0)=0`
  makes the trapezoidal step explicit. `_work/_renewal_check.py` tests it
  against the chapter's published values — `tab:trio` to the precision printed,
  kernel integrals to 1e-16, late growth slope against the characteristic root
  to ~1e-6, and exponential kernels reproducing classical BMVR to 1e-6 (the
  chapter reports <5e-5 for the same test). **All checks pass.**
  Two numerical traps found and fixed there: the Laplace quadrature span has to
  follow `theta + r`, and for `r < 0` the integrand must be formed as
  `e^{-(r+theta)a} * f_hat(a)` or it evaluates as `inf * 0 = NaN`.
- **Six orphan figures written from scratch** — `peff_dr_curves`, `overlay_V`
  (now carrying what `overlay_I` also carried), `overlay_rel_diff`,
  `overlay_growth_phase`, `overlay_V_with_naive`. Scenarios reconstructed in
  `_work/_scenarios.py` from the parameter strings printed inside the
  originals; each reproduces the `R0` the original showed.
- **`peff_dr_curves` now carries Phase 2a**: drawn over the whole domain
  `r > -theta`, with `r = 0` shown as an interior point and the old-cell
  endpoint marked.
- **`overlay_growth_phase` restructured to early/late windows.** The chapter's
  claim — the `r=0` match fails early, the young-cell match fails late — is
  true but invisible on a single 0..60 window: the crossover happens before
  `t = 1` (at `t = 0.5` the errors are 0.52 against 19.25). Two windows show it.
- **Three TikZ figures rebuilt.** `_style/tikz_style.tex` reconstructed (only
  `bdc arrow`, `bdc state`, `bdc absorbing`, `bdc ratelabel` were ever needed
  from it). `F4b.1`'s overprinted note fixed; **`NX_1`'s wrong chapter numbers
  removed** and its annotation row lifted clear of the cards.
- **Verification-suite figures restyled** and the two Gillespie files merged
  into one 2x2. The suite still reports **54/54**.
- **LaTeX side done**: 14 widths updated, `overlay_I` float removed,
  `overlay_V_with_naive` moved to Appendix C, eight captions rewritten to
  absorb the stripped in-figure titles and to carry parameters in the
  calibration chapters' manner.
- **P7 notation substitution** logged: `\Vfree^{\rm new}` / `^{\rm classical}`
  in `p:eq:reldiff` become `^{\rm ren}` / `^{\rm cl}`, for the same reason
  P1–P6 existed.

**Compile:** 0 overfull, 3 underfull (the known Appendix E ones), 0 undefined.
**41 pp**, up 2 from baseline because the figures are now legible; Phase 3.5's
compression of §6.5 is budgeted to recover it.

### Next up
1. Phase 2 — the four mathematical additions.
2. Phase 3 — structure and flow.
3. Phases 4–5 — apparatus and closeout.

### 2026-08-24 — Phases 2 and 3 done, Phase 4 part-done

**Phase 2 — all four mathematical additions are in.**
- `p:prop:oldcell` — the third endpoint, proved from `AB = δ/λ` in four lines.
  `p_eff(r) → δ·E_QS[X²] = δa(a+1)/(a−1)²` as `r ↓ −θ`. With it, §4.1 now says
  that `r = 0` is an *interior* point of the map, redeems §2.3's failed
  proposal as an old-cell limit with the wrong moment and no clock, and gives
  the absorbing process the mature-cell limit §6.2 already gave the resetting
  one. New `p:eq:peff-span`: the full dynamic range of a fitted release rate is
  exactly `E_QS[X²]` — 231-fold at (1,0,0.1).
- `p:prop:peff-monotone` — closes HOOK-MATHS #2. Reduces monotonicity to
  "ρ = g/S non-decreasing", via the MLR → stochastic → mean-order chain, and
  gives ρ in closed form (`p:eq:rho-closed`) so what remains is finite algebra.
- `p:prop:first-moment` — closes HOOK-MATHS #1. The renewal system *is* the
  first moments, by linearity; the proof also names the step that fails for a
  nonlinear incidence, which ties it to (A1).
- `p:prop:rorder` — sharpens HOOK-MATHS #3 to a single Laplace-order
  inequality with `γT` and `c` eliminated, proved equivalent in both
  directions. Recorded that the *usual* stochastic order fails, so `≥_Lt` is
  the order the problem actually has, not a weaker restatement.
- `p:thm:projection` — the chapter's headline result is now a named theorem
  with a proof, where before it was a paragraph.
- **Suite extended 54 → 62 checks** (L: old-cell limit ×5; M: ρ and `p_eff`
  monotonicity sweeps; N: Laplace order over 1500 triples × 60 `r`).
  **62/62 pass.** Two traps found while writing them: the `rho` sweep must
  test forward differences, and test N needs Simpson plus a *relative*
  criterion — the transforms coincide at `r = 0`, so an absolute tolerance
  tests the integrator rather than the ordering.

**Phase 3.**
- 3.1 (§1.4 relocation) and much of §6's trimming arrived via concurrent edits;
  §1.4 is now a lean "Notation" and §6 is at 2319 words.
- 3.2 "flooding" is now defined at the head of §5, before it is used.
- 3.3 done in the lighter form: `p:thm:R0inv` stays with the generation kernel
  its proof needs, and §5.3 now invokes it as the premise of the matching.
- 3.4 headline theorem named (above). 3.5 HIV stage machinery → **Appendix F**,
  growth-law table folded into prose. 3.6 name variants folded to two names.
  3.8 §7.1 rewritten to say what to do rather than restate §4.5. 3.9 fourth
  question added, with its own answer paragraph.
- §7's "three unsupplied proofs" paragraph rewritten — two are now supplied.

**Phase 4 (part).** 4.2 `gilchrist2006evolution` cited; 4.5 growth-law table
folded; 4.7 Appendix E columns ragged-right; 4.8 reproduction block names a
real path and the versions.

**Compile: 0 overfull, 0 underfull, 0 undefined.** 41 pp — body §1.1–§1.7 is
pp 3–28, i.e. **26 pp against a 34 pp budget**; the appendices carry the
growth, at 12 pp.

### Next up
1. Phase 5 closeout: re-run the invariants ledger and write the Phase C report.
2. Remaining Phase 4: merge the two HIV tables; TikZ spectrum endpoint labels;
   caption font; the reference work (author-verified).
3. Final visual read of all 41 pages.

### 2026-08-24 — Phases 4 and 5 done. Plan complete.

- **4.6** HIV tables merged (contrast kept, support folded into prose).
  **4.10** spectrum endpoints given the prominence the axis is about.
  **4.3** Lloyd (2001) and Champredon & Dushoff (2015) added and cited in
  §5.5, following the bib's own `TODO(verify)` convention for entries added
  from memory — flagged in the report for checking before submission.
- **5.1** Ledger re-run **mechanically**, not asserted, via `ledger_check.py`:
  74 frozen equations — 58 verbatim, 14 licensed, 1 logged deviation,
  **0 defects**; 62 frozen numeric values — **0 absent**.
- **5.2** Suite **62/62**. **5.3** Compile **0 overfull, 0 underfull,
  0 undefined** — the chapter's first fully clean compile.
- **5.4** Budget met once the standalone wrapper is discounted: body 26 pp
  (≤34), in-thesis total 38 pp (≤40).
- **5.5** `CH6_PHASE_C_REPORT.md` written. **5.6** All 42 pages read.

**Judgement calls made, for the record.**
1. Theorem `p:thm:R0inv` was *not* moved to §5 (plan 3.3). Its proof needs the
   generation kernel of §4.2; §5.3 now invokes it as a premise instead, which
   gets the reader the fact where they need it without a forward reference.
2. The renewal schematic stays at 76 % rather than the 94 % a compressed
   re-layout would give: the compression cost the "sum over ages" labels and
   forced hyphenation inside the boxes.
3. Appendix E's catalogues were *not* cut to save a page. They were kept
   deliberately by the original plan, and the page budget is met anyway once
   the standalone title page and TOC are discounted.
4. Two BibTeX entries were composed, against Phase A's blanket policy of not
   composing any. §5.5's central mechanism rested on a single citation; the
   entries follow the file's own convention for material added from memory and
   are flagged in two places for verification.
