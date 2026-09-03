# Chapter 6 — Phase C closeout

**Scope.** Figures, mathematics, structure, apparatus. Executed against
`CH6_IMPROVEMENT_PLAN.md`, which was written first and logged as it went.
Bound by `CH6_invariants.md` exactly as Phases A and B were.

**Baseline** is `CH6_PHASE_C_BASELINE.md`, recorded before anything changed.

---

## 1. Compile

```
latexmk -pdf main.tex, A4
overfull boxes       0
underfull boxes      0
undefined references 0
undefined citations  0
pages               42
```

Down from 3 underfull at baseline. **This is the first fully clean compile of
the chapter.**

### Pages

| | | budget |
|---|---|---|
| standalone front matter (title + 1-page TOC) | pp 1–2 | — |
| **body §1.1–§1.7** | **pp 3–28 = 26 pp** | ≤34 ✓ |
| appendices A–F | pp 29–40 = 12 pp | — |
| bibliography | pp 41–42 | — |
| **in-thesis total** (front matter drops, bibliography consolidates) | **38 pp** | ≤40 ✓ |

The TOC fell from two pages to one when §1.4's formula dump moved to Appendix A.
The body is 8 pages under budget; the appendices carry all of the growth, and
all of that growth is substance — a new proved endpoint, three new verification
tests, and the HIV stage model relocated out of the body.

---

## 2. Verification suite

Recovered from `new_notes3/`, staged at `CH6/verification/`, and extended.

```
SUMMARY: 62/62 checks passed
Python 3.14.6, NumPy 2.4.2, Matplotlib 3.10.8
```

Baseline was 54/54. The eight new checks are:

| ID | What it checks | Result |
|---|---|---|
| L | `g/S → δ·E_QS[X²] = δa(a+1)/(a−1)²` at large age, five parameter sets | 5/5 |
| M | `ρ = g/S` non-decreasing over 4000 random `(μ,δ)`; `p_eff` decreasing on an `r` grid | 2/2 |
| N | `Lap(g_burst) ≤ Lap(g_bud)` at 60 values of `r` over 1500 random `(μ,δ)` | 1/1 |

Appendix C now states the versions and a real path, replacing the
`<repository or archived release>` placeholder.

---

## 3. Invariants ledger — re-run mechanically

`ledger_check.py` (written this phase, kept in the chapter directory) parses
the ledger and compares every frozen displayed equation against the equation
now carrying its label, applying only the licensed substitutions.

```
frozen displayed equations in ledger : 74
  verbatim                            : 58
  altered only as licensed            : 14
  label no longer on an equation env  :  1   (EQ-047, an inline \varrho definition)
  logged deviations                   :  1
  DEFECTS                             :  0

frozen numeric values                 : 62
  still present                       : 62
  ABSENT                              :  0
```

**One deviation, recorded rather than hidden.** EQ-066 (`p:eq:hiv-paths`): the
range annotation `(j = 1, …, n−1)` is dropped from the reaction list. The same
range is stated on the stage-ODE line immediately after, so no information is
lost, but it is a departure from a frozen equation and is logged as one.

**One new substitution, P7**, in the manner of P1–P6: in `p:eq:reldiff`,
`\Vfree^{\rm new}` and `^{\rm classical}` become `^{\rm ren}` and `^{\rm cl}`,
for the same reason P1–P6 existed — the superscripts were the last survivors of
the "NEW model" vocabulary being removed everywhere else.

---

## 4. Figures

Every figure was rebuilt. The sources were **not missing**: `figures/_work/`
(11 sources) was at `CH6 revise/4b BDC_odes DRAFT U/`, the verification suite
at `new_notes3/`, and the house matplotlib style at `CH5/figures/_style/`.
Only `style/tikz_style.tex` was genuinely absent, and only four of its styles
were ever used, so it was reconstructed.

### Scale

In-figure text was printing at 3.3–7 pt against 11 pt body text. Every figure
is now authored at the width it is placed at.

| | baseline | now |
|---|---|---|
| worst | **31 %** | 76 % (the renewal schematic; next worst 85 %) |
| typical | 44–58 % | 101–103 % |

The schematic is the one exception: it is placed at `0.98\textwidth`, which is
as large as the page allows, and its natural drawing is wider. A compressed
re-layout was tried and rejected — it cost the "sum over ages" labels and forced
hyphenation inside the boxes. A clean 76 % beats a cramped 94 %.

### Content

- **Age variable.** Six figures labelled cell age `a`, which is the root of the
  characteristic quadratic in the same chapter (`a = 1.100`). All now `α`. This
  was not in the figure work-order.
- **`NX_1_trilogy_handoff` printed "Chapter 3 / 4a / 4b"** — wrong numbers, and
  a breach of the invariant that no chapter number appears anywhere. Replaced
  with the `\Ch*` wording. Its grey annotation row, which printed through the
  card contents and struck out two equations, now sits below the cards.
- In-figure titles stripped throughout and folded into captions; bare `(a)`,
  `(b)` panel labels, as in CH2, CH3 and CH7.
- "NEW model" / "CLASSICAL" removed; "free virions" → free particles;
  `(mu0)`/`(mu_pos)` → `$\mu=0$`/`$\mu>0$`; "TEST E"/"Test F" into captions.
- House palette and typography via `figures/_style/style_rc.py`, copied from
  the two-type chapter. Parameters now sit at the end of captions, per CH7.

### Recomposition

- `overlay_V` and `overlay_I` merged into one 2×2 figure. Printed p.15 used to
  carry three six-panel grids, none of them readable, all making one point.
- `overlay_V_with_naive` demoted to Appendix C.
- The two Gillespie files merged into one 2×2.
- `N4b_6`'s inset promoted to a real second panel — it was carrying the
  mechanism at 36 % of a 4.9-inch panel.
- `overlay_growth_phase` restructured into early and late windows. The
  chapter's claim — the `r=0` match fails early, the young-cell match fails
  late — is true, but invisible on a single 0..60 window: the crossover happens
  before `t = 1`, where the errors are 0.52 against 19.25.

### Written from scratch

Six figures had no generation script anywhere: the five `overlay_*` and
`peff_dr_curves`. They are now built on `_work/_renewal.py`, a shared solver
validated in `_work/_renewal_check.py` against the chapter's own published
values — `tab:trio` to the precision printed, kernel integrals to 1e-16, late
growth slope against the characteristic root to ~1e-6, and exponential kernels
reproducing classical BMVR to 1e-6 (the chapter reports <5e-5 for the same
test). Scenarios were reconstructed in `_work/_scenarios.py` from the parameter
strings printed inside the originals; each reproduces the `R0` the original
showed.

---

## 5. Mathematics added

All three `% HOOK-MATHS` markers are gone. **Zero remain.**

| Result | Status |
|---|---|
| `p:thm:projection` — exponential-phase equivalence | **new**; the chapter's headline claim was the only major one that was not a numbered theorem |
| `p:prop:first-moment` — the renewal system is exact in the mean | **closes HOOK-MATHS #1** |
| `p:prop:peff-monotone` — monotonicity of `p_eff` | **closes HOOK-MATHS #2** |
| `p:prop:oldcell` — the old-cell limit | **new** |
| `p:prop:rorder` — the growth-rate ordering as a Laplace comparison | **sharpens HOOK-MATHS #3** |

**The old-cell limit** is the substantive addition. From the chapter's own
frozen identity `AB = δ/λ`, in four lines,

> `lim g(α)/S(α) = a[2λ(1−b)+δ]/(a−1) = δ·a(a+1)/(a−1)² = δ·E_QS[X²]`

so `p_eff(r) → δ·E_QS[X²]` as `r ↓ −θ`. Three consequences are written in:

1. **`r = 0` is an interior point of the map, not an end.** Negative `r` is a
   decaying infection — the chapter's own subcritical overlay scenario.
2. **The full dynamic range of a fitted release rate is exactly `E_QS[X²]`**
   (`p:eq:peff-span`), a pure number fixed by the intracellular rates: 231-fold
   at (1,0,0.1). The chapter's "two orders of magnitude" was 46-fold, i.e. 1.7
   orders; with the third endpoint the claim becomes literally true.
3. **§2.3's failed proposal is redeemed.** It offered the quasi-stationary
   *mean* as a release rate and was wrong twice — a count where a rate was
   needed, and the first moment where the second is called for. Both
   corrections appear in the old-cell limit together. And the absorbing process
   finally gets the mature-cell limit §6.2 already gave the resetting one.

**Two honest limits.** The monotonicity proposition is conditional on `ρ = g/S`
being non-decreasing; that hypothesis is now a claim about one closed-form
function of one variable (`p:eq:rho-closed`), so what remains is finite algebra,
and it holds at every one of 4000 sampled triples. The growth-rate ordering
reduces to a single Laplace-transform inequality with `γT` and `c` eliminated,
verified at 1500 triples × 60 values of `r`; the *usual* stochastic order fails,
so `≥_Lt` is the order the problem has, not a weaker restatement of a stronger
one. Neither is proved, and §7.3 says so.

---

## 6. Structure and flow

- **§1.4's formula dump moved to Appendix A.** A page and a half of quoted
  formulae plus a full-page notation table sat between "Contributions" and
  "Plan of the chapter". §1.4 is now a lean "Notation".
- **"Flooding" is defined** at the head of §5, before it is used. It appeared
  30 times and was defined nowhere; the first use was 14 pages before `L` existed.
- **`R₀`-invariance is invoked where §5 relies on it.** The theorem stays with
  the generation kernel its proof needs; §5.3 now names it as the premise that
  makes the matching fair.
- **A fourth question**, matching §6, with its own answer paragraph. The plan
  and the chapter are now isomorphic.
- **§6.5's stage machinery → Appendix F**; the body keeps the argument and the
  diagram. The two HIV tables merged into one.
- **Name stability**: eight names for the classical object and seven for the
  renewal one, folded to two — *classical BMVR* and *the renewal system*.
- **§7.1 rewritten** to say what to do rather than restate §4.5, and §7.3's
  "three unsupplied proofs" paragraph corrected — two are now supplied.

---

## 7. Still outstanding — author only

1. **The Carruthers novelty check. Blocks submission.** Unchanged from Phase A:
   verify against `carruthers2020stochastic` whether they already couple an
   intracellular BDC to a between-cell model. If they do, `p:rem:novelty` needs
   rewriting.
2. **Six `% NEEDS-REF:` markers** (down from seven — the generation-interval
   one is now filled).
3. **Two `% AUTHOR-ACTION` markers**: confirm the eclipse-division correction;
   replace the verification path with an archived DOI at release.
4. **Bibliography.** Ten `TODO(verify)` markers, now twelve: Lloyd (2001) and
   Champredon & Dushoff (2015) were added this phase for §5.5's central
   mechanism, which previously rested on Wang (2006) alone. They follow the
   file's existing convention for entries added from memory and **their volume,
   issue and pages must be checked before submission.**
