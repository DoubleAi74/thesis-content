# Chapter 6 rewrite — Phase A closeout

**Scope.** Structure, content, mathematics, notation, labels, citations, LaTeX
hygiene. Executed against `CH6 revise/CH6_rewrite_plan.md` (authoritative),
`CH6_polish_review.md` (defect inventory) and `Chapter numbers/CH2/` (house
standard).

**Phase B has not run.** This document is the handover; Phase B starts cold and
sees nothing else from Phase A.

---

## 1. Files written — `Chapter numbers/CH6_REWRITE/`

```
preamble.tex          packages + macros; merges into the thesis preamble
chapter.tex           thesis-ready fragment: \chapter + \input's + appendix guard
main.tex              standalone report-class wrapper (a4paper)
references.bib        original + the six entries of plan §8.3, verbatim
figures/              23 PDFs, verbatim copies, none created/edited/repointed
sections/01_introduction.tex .. 07_discussion.tex
sections/A_quoted_results.tex .. E_release_catalogue.tex
CH6_invariants.md     the ledger, built before any prose, + the verification table
CH6_figure_workorder.md
PHASE_A_REPORT.md     this file
```

Seven body sections, five appendices, CH2's three-file architecture,
`report` class, real `\chapter`, appendix hyperref guard copied verbatim.

---

## 2. Compile

`latexmk -pdf main.tex`, A4:

```
undefined citations 0
undefined references 0   (Chapter 2 m:… targets: none are referenced)
multiply defined     0
overfull boxes       0
underfull            3
page size            595.276 x 841.89 pts (A4)
```

## 3. Pages

| | | budget |
|---|---|---|
| front matter (titlepage + 2-page TOC) | pp 1–3 | — |
| **body §1–§7** | **pp 4–30 = 27 pp** | ≤34 ✓ |
| appendices A–E | pp 31–38 = 8 pp | — |
| bibliography | p 39 | — |
| **total** | **39 pp** | ≤40 ✓ |

Down from the draft's 42.

At US Letter the same source compiled to 41 pp — 1 over budget, entirely in
front matter: CH2's `main.tex` uses a full titlepage where the draft used
`\maketitle`, and at CH2's `tocdepth=2` a chapter with 12 sections and ~35
subsections needs two TOC pages. Adding `a4paper` (Leeds requirement) recovered
2 pp. **No content was recut to reach the number.**

## 4. Word counts against plan §4 budget

Raw `wc -w`, which is the measure the plan's own table uses.

| § | actual | budget | Δ |
|---|---|---|---|
| §1 Introduction | 1412 | 900 | **+512** |
| §2 The comparator and the obstruction | 1243 | 1100 | +143 |
| §3 Burst-aware renewal dynamics | 1162 | 1300 | −138 |
| §4 The classical model as a projection | 1848 | 1600 | +248 |
| §5 Bursting versus budding | 1594 | 1800 | −206 |
| §6 The reach of the construction | 3336 | 2200 | **+1136** |
| §7 Discussion | 1098 | 900 | +198 |
| App A Quoted results | 371 | 750 | −379 |
| App B Formula table | 333 | 320 | +13 |
| App C Verification record | 593 | 450 | +143 |
| App D Technical derivations | 337 | 300 | +37 |
| App E Release catalogue | 1098 | 650 | **+448** |
| **total** | **14425** | 12270 | +2155 |

**§6 missed its budget by 1,136 words** (5217 → 3336, target 2200). About 900 of
the residual is markup rather than prose: the section carries 21 displayed
equations, two inline TikZ diagrams and six tables, all of which the plan
requires kept. Prose only (`texcount`) it is 2,411.

**§1 is over by 512** because it absorbs two things the plan routes into it — the
chapter notation table (§6 of the plan) and the quoted roots, identities,
fixation functions and moments (the Appendix A note in §5 of the plan) — on top
of its 900-word argument. Appendix A is correspondingly 379 words under.

**App E is over by 448**: the three catalogue tables are large.

---

## 5. Ledger check

Full entry-by-entry table in `CH6_invariants.md` §I. Summary:

| Class | Entries | Found | Verbatim | Altered (permitted) | Missing |
|---|---|---|---|---|---|
| Displayed equations | 73 | 73 | 60 | 13 | **0** |
| Theorem / proposition statements and proofs | 10 | 10 | 5 | 5 | **0** |
| Numeric values | 61 | 61 | 61 | 0 | **0** |
| Parameter triples | 5 | 5 | 5 | 0 | **0** |
| Table data blocks | 13 | 13 | 8 | 5 | **0** |
| **Total** | **162** | **162** | **139** | **23** | **0** |

Every alteration is one of:

- a plan §6 notation substitution — **P1** cell age `a`→`α`, **P2** eclipse
  conversion `α`→`ω`, **P3** geometric parameter `r`→`ϱ` inside the `prop:L1`
  proof, **P4** Model 10 intensity `r`→`ψ`, **P5** mean load `m`→`x̄`,
  **P6** Dirac source restated as an initial condition;
- the plan §10.1 **licensed correction** to the eclipse-division equations, whose
  `ρ_div` terms cancelled identically as printed;
- plan §7.3's `\eqref{eq:X}` → `\cref{p:eq:X}`.

Nothing else changed. One entry (EQ-036) initially differed by terminal
punctuation alone; it was restored to verbatim rather than logged as altered.

### §15 checklist — verified mechanically, not asserted

`[H]` floats 0 · `\eqref` 0 · `Figure~\ref` / `\S\ref` / `Appendix~\ref` 0 ·
`\Figref`/`\Eqref`/`\Tabref`/`\Chapref` 0 · `\figureflag` 0 · dead macros 0 ·
bare `tabular` outside a `table` float 0 · labels not `p:`-prefixed 0 ·
chapter numbers in body prose 0 (two grep hits are provenance comments, which
plan §12.3 keeps) · `\includegraphics` with a `figures/` prefix 0 ·
`Result~\ref` 0 · `$$` display delimiters 0 · *honest* 0 · *Headline* 0 ·
confidence ratings 0 · "the recommendation" / "the practical ranking" 0 ·
"not to be confused" 0.

Bibliography: exactly six entries added, all six copied verbatim from plan §8.3,
all six cited. The four plan §8.2 entries (`hawkes1971spectra`, `van2011quasi`,
`stehfest1970algorithm`, `gaver1965observations`) are now cited. **No BibTeX
entry was composed.** The chapter cites 19 works against the draft's 10.

Source integrity: `diff -rq "Chapter numbers/CH6" "CH6 revise/4b BDC_odes DRAFT U"`
is clean but for Finder's `.DS_Store`, which already differed before this run.

---

## 6. Deviations from the plan — all seven accepted by the author

1. **The generation kernel is written `\mathcal A(α)`, not `A(α)`.** Plan §9
   specifies `A(α)`, but `A = a−1` is a *frozen* derived constant (EQ-002)
   appearing in EQ-003, EQ-023, EQ-075 and EQ-077. A bare `A` would reintroduce
   exactly the collision plan §6 exists to remove. `\mathcal A` is consistent
   with the calligraphic population objects `\Icell`, `\Vfree`, `\Kb`.

2. **`p:tab:trio` prints two derived values that are not in the source** —
   `p_eff(0)` = 1.82 and 0.92 for the second and third regimes. Plan §4.2
   commissions that column and states the values are "already in the source";
   they are not. They are exact evaluations of frozen closed forms at frozen
   parameter triples. Every other cell reproduces a source number exactly
   (0.417 / 0.910 / 0.701, and L, V∞, E[T_prod]).

3. **Plan §11.1's figure premise is factually wrong.** `NX.1`, `N4b.3` and
   `F4b.1` each carry a complete standalone TikZ `figure.tex`, not "only a
   README". All three are blocked on one absent shared file,
   `style/tikz_style.tex`, which exists nowhere in the tree. Recovering that one
   file restores the source of two of the four visibly broken figures. Recorded
   in `CH6_figure_workorder.md` §1 and §3 (A2).

4. **Two citations rescued.** Deleting open problem 5 (plan §10.3) would have
   orphaned `pearson2011stochastic` and `carruthers2020stochastic`. Both are in
   the original `references.bib`, so plan §8.1 permits them: Pearson is placed at
   §5's burst-versus-continuous-production comparison, Carruthers at the
   *F. tularensis* estimate in §7.4.

5. **The `\boxed{}` frames were dropped** from the eleven quoted single-cell
   results. The mathematics inside each is byte-identical; the boxes were a
   device of the reference card that §1.4 and Appendix A replace.

6. **Appendix A is 379 words under budget.** Plan §4.1 and the Appendix A note
   in plan §5 between them route the roots, identities, fixation functions and
   moments into §1.4; they are not duplicated in the appendix.

7. **`caption` loaded with `font=small`, and `\arraystretch` reduced
   throughout.** Page-count measures, not house-standard changes.

Two further mechanical notes, made after the author's acceptance and within the
same envelope:

- **`$$…$$` → `\[…\]`** in the proof of `prop:L1` (3 displays) and Appendix D
  (2 displays). Delimiter-only; display contents verified byte-identical. No
  `$$` remained inside TikZ or anywhere else.
- **`a4paper` added** to the `geometry` options in `main.tex`. The narrower text
  block put standing assumption **(A4)** 7.6 pt overfull; it was reworded to the
  plan's own phrasing (`MOI-$k$ kernels are available … but are not used`,
  plan §4.1), which fixes the box and is closer to the specification than what
  it replaced. Zero overfull boxes.

---

## 7. Not done — deliberately out of Phase A scope

### 7.1 Three deferred proofs — `% HOOK-MATHS:` markers only

| Marker | Claim | Review §|
|---|---|---|
| §3.2, after `p:def:renewal-system` | that the renewal system gives the first moments of the underlying stochastic process **exactly** | `CH6_polish_review.md` §4.3 |
| §4.1, at the monotonicity sentence | that `p_eff` is **monotone decreasing** in `r` | §4.2 |
| §5.5, at `p:eq:rorder` | that `r_bud > r_burst` **in general** | §4.4 |

The chapter now states each honestly where it occurs — as a numerical check
(test H), as a claim over the five named parameter sets of Appendix C, and as a
claim over the three named regimes of `p:tab:trio` — and §7.4 records all three
together. Theorem 3.1 of the draft, which asserted nothing and proved nothing,
is now `\begin{definition}` "The burst-aware renewal system", per plan §4.3.

`p:thm:R0inv` **has acquired its one-line proof** from the generation kernel
(plan §4.4); it had none in the draft.

### 7.2 Seven `% NEEDS-REF:` markers

| Where | Topic |
|---|---|
| §4.2 | Crump–Mode–Jagers general branching processes |
| §5.5 | optimal lysis timing beyond Wang (Abedon; Bull) |
| §6.5 | Allee effects and stochastic establishment theory |
| §6.5 | Erlang-eclipse within-host models; the Rong–Feng–Perelson line |
| §7.3 | *Y. pestis* macrophage residence, YCV maturation, and the YopJ / pyroptosis / necroptosis exit literature |
| App D | a standard Volterra-quadrature reference |

### 7.3 Two `% AUTHOR-ACTION` markers

- **§6.5** — confirm the eclipse-division correction (plan §10.1). The draft
  printed `dE_j/dt = αE_{j−1} + ρ_div E_j − (μ_E + ρ_div + ω)E_j`, in which the
  `ρ_div` terms cancel identically, so eclipse proliferation had no effect at
  all — contradicting the surrounding text. Corrected to
  `dE_j/dt = ωE_{j−1} + ρ_div E_j − (μ_E + ω)E_j`, with the Dirac source
  replaced by the initial condition `E_1(0) = α_A L_0`.
- **App C** — the reproduction block reads `cd <repository or archived release>`.
  Replace with a repository URL or archived DOI and state the
  Python / NumPy / SciPy versions. `verify_result_20_1.py` is absent from the
  whole tree.

### 7.4 The Carruthers check — **blocks submission**

Plan §10.3 deletes the draft's open problem 5, which read: *"Verify whether
Carruthers et al. already couple an intracellular BDC to a between-cell model —
the novelty claim of §3 depends on the answer."* A to-do note saying in the
author's own words that the central novelty claim is unverified cannot go to an
examiner, so the item is gone from the chapter. **The check itself has not been
done and cannot be done by an agent.**

Verify against `carruthers2020stochastic` and the surrounding literature. If
they do couple an intracellular birth–death–catastrophe process to a
between-cell model, `p:rem:novelty` in §3.2 needs rewriting. As it stands the
remark claims novelty only for the *derivation of the kernels in closed form
from a mechanistic intracellular process* — the narrower and more defensible
claim — and engages `nelson2004agestructured` head-on per plan §8.4.

### 7.5 Also out of scope, per plan §16

Regenerating or editing any figure (the two inline TikZ repairs of plan §11.4
were made); running or modifying the verification suite; composing BibTeX
entries; touching `Chapter numbers/CH6/` or the `DRAFT U` folder; editing
Chapters 4, 5 or 7.

---

## 8. For Phase B

Phase B runs `/aa-flow-lucid` over this output, bound by the same ledger.
The plan's §14 brief applies in full. The points that matter most here:

- **Read `Chapter numbers/CH2/sections/01_overview.tex` first** and calibrate
  against it, not against this output.
- **`CH6_invariants.md` binds Phase B exactly as it bound Phase A.** Equations,
  theorem statements, proofs, numbers and table data are untouchable, and the
  ledger check must be re-run and reported in full afterwards.
- **Proofs are not restyled.**
- **Name stability matters unusually much**, because §6 of the plan fixed a
  notation catastrophe. Do not introduce synonyms for `S`, `g`, `α`, `L` or
  `p_eff`, and do not revert `\mathcal A` to `A`.
- **Do not touch** `% HOOK-MATHS:`, `% NEEDS-REF:` or `% AUTHOR-ACTION`
  comments.
- Do not change structure, and do not chase page count.
