# Chapter 8 — Phase A report

*Bursting and budding pathogenesis. Rebuild executed against `CH8 revise/CH8_rewrite_plan.md` §§1–11, from the findings in `CH8 revise/CH8_polish_review.md`.*

**Run date:** 20 August 2026.
**Source:** `Chapter numbers/CH8/document MAIN/` — read-only, verified byte-identical at the end of the run (item 7 below).
**Output:** this directory.

Phase B reads this file and the tree beside it, and nothing else.

---

## 1. Final section structure

`latexmk -pdf main.tex` builds clean: **0** undefined citations, **0** multiply-defined labels, **0** overfull boxes. The source draft had 68 multiply-defined labels and 4 overfull boxes.

**28 pages**, A4 (595 × 842 pt). The source was 25 pages, US Letter.

Composition: 1 title page + 1 contents page + **24 pages of body and appendices** (printed pp. 2–25) + 2 pages of bibliography (printed pp. 26–27). Page numbers below are the printed ones.

| § | Title | p. |
|---|---|---|
| 1 | Introduction | 2 |
| 1.1 | Three candidate advantages | 2 |
| 1.2 | The answers, in advance | 3 |
| 1.3 | What is inherited, and what is new | 3 |
| 1.4 | Plan of the chapter | 4 |
| 2 | Why the release schedule alone cannot matter | 4 |
| 2.1 | Successive birth–death–catastrophe | 5 |
| 3 | Intracellular depletion: replicator and suppressor | 6 |
| 3.1 | The granule store | 7 |
| 3.2 | The replicator–suppressor process | 7 |
| 3.3 | First-step analysis | 9 |
| 3.4 | The survival maps | 11 |
| 4 | Extracellular depletion: fixed removal | 12 |
| 4.1 | The playing field | 12 |
| 4.2 | The replication ratio | 15 |
| 4.2.1 | The law is normalised, and the tail is free | 16 |
| 4.3 | Analysis of proliferability | 16 |
| 5 | Bursting and budding: where the advantage lives | 18 |
| 5.1 | What is settled, and what was left open | 18 |
| 5.2 | The reversal | 19 |
| 5.2.1 | Two flooding arguments, which are not the same argument | 19 |
| 5.3 | Placement on the spectrum | 20 |
| 5.4 | *Y. pestis* | 21 |
| 6 | Discussion | 22 |
| 6.1 | Limitations | 22 |
| 6.2 | Open problems | 23 |
| 6.3 | Connections forward | 23 |
| A | Numerical verification | 23 |
| B | Computational notes | 24 |
| B.1 | The first-step solver | 24 |
| B.2 | Quadtree sampling | 25 |

**Counts.** 22 numbered equations (the source had **zero**); 15 figures, every one referenced by `\cref` from the body (the source had **zero cross-references of any kind**); 4 tables; 1 definition, 2 propositions in §3, 1 proposition and 2 corollaries in §4, 1 proposition in §5, 5 remarks. All 15 figure labels, 27 section labels and everything else sit in the `path:` namespace; there is no label outside it.

Undefined references in a standalone compile are 63, and every one is a foreign-chapter label in the `m:`, `bdc:`, `dist:` or `p:` namespaces. They render as `??` and are expected. **Do not invent dummy labels for them.**

---

## 2. Passages carried over near-verbatim — Phase B must leave these alone

Three passages are the best writing in the source and were carried across with minimal edit. Two of them additionally carry an external obligation.

| Source | Now at | What it is | Why it is frozen |
|---|---|---|---|
| `03_fixed_removal.tex:5` | §2, opening paragraph | *"With agents replicating identically whenever they are within a host cell, it matters not how they are moved, just that they are replicating."* … through *"broad propagation dynamics would remain identical."* | The chapter's sharpest paragraph and the reason the fixed-removal model exists. Plan §3.6 |
| `03_fixed_removal.tex:16–17` | §2.1, second and third paragraphs | Brownian drift, macrophage motility, *Y. pestis* choosing absorption, injected effectors, and *"the playing field of these actors is just that, an environment of play"* | **Preservation order.** `CH5_REWRITE/notes/ch5_handoffs.md` entry 3: Chapter 5 §10 now justifies its chained-transfer model by pointing here, and asks that this passage survive with both caveats and not be reduced to a pointer back at Chapter 5. Acceptance criterion 12 |
| `03_fixed_removal.tex:88` | §4.1, third paragraph | *"Those at the leading edge, as it were, clearing the way for their comrades in the rear."* | The flooding intuition in one image, and the seed of the batch-count argument of §5.2.1 |

Edits actually made inside these three: `03:7`'s *bodies* → *body's* and *immuno-factors* → *immune factors*; `03:88`'s *thank* → *than*; first-person singular removed from `03:88` (*"my intention with this is not to construct"*, *"the assumption which I hope to use"*); `\yp` applied to the unitalicised "Yersinia pestis" at `03:16`. Nothing else.

Two further passages were kept close to the source and are less delicate, but are noted so they are not over-worked: §4.1's *"To begin with, the extracellular matrix is populated evenly…"* (`03:87`) and §3.2's model-definition prose (`02:80`).

---

## 3. `NEEDS-ATTRIBUTION` and `NEEDS-REF` markers

### The blocking one, first

**`NEEDS-ATTRIBUTION-flooding`** — `sections/01_introduction.tex:55`, with the full comment at `:57`; stub entry in `references.bib` under heading (c).

The sentence it supports, in §1:

> Each supplies a mathematical quantification of what has been termed the advantage of *flooding* `\cite{NEEDS-ATTRIBUTION-flooding}`: that in a burst-style release there is a higher likelihood of using up the local capacity of the host's immune system.

The source read *"what has been termed by `(inserty name)` as the advantage of `flooding`"*. **No name was supplied and none may be.** The attribution is not recoverable from the thesis tree: Chapter 6 uses the term throughout — `p:thm:flood`, `p:eq:flood`, `p:eq:floodcrit`, `p:fig:L-landscape`, `p:rem:flood-scope` — as its own working term with no citation, and no entry in any of the five donor bibliographies matches. The two nearest candidates already in this chapter's bibliography are `komarova2007viral` and `bird2015nonlytic`, offered **for the author to check and not as an identification**.

If the attribution cannot be recovered, the fix is to delete the clause *"what has been termed"* together with the citation, and use the term plainly, as Chapter 6 does. The comment block in the file says so.

### `NEEDS-REF`

**None.** Every citation gap was filled either from Chapter 8's own bibliography or by verbatim copy from the donor pool. No agent-authored entry exists anywhere in `references.bib`.

---

## 4. `NEEDS-BIOLOGY` markers

Six. Each names the exact claim wanted and the candidate keys already copied into `references.bib`. Phase A wrote the surrounding argument and attached what evidence the tree contains; it did not compose the claims.

| # | File:line | Claim wanted | Candidate keys |
|---|---|---|---|
| 1 | `03_intracellular_depletion.tex:43` | Whether neutrophils also employ granules intracellularly, in addition to the lytic release route. The source asserted this as a belief (*"I believe Neutrophils dothis as well"*) with no citation | `cowley2011immunity`, `jones2012subversion` |
| 2 | `05_selection.tex:280` | That *Y. pestis* sits at the bursting end of the release spectrum, and what intracellular constraint puts it there | `PujolBliska2003`, `KeEtAl2013`, `ConnorEtAl2018` |
| 3 | `05_selection.tex:287` | That plague infection proceeds in two phases, an early intracellular (macrophage) phase followed by a predominantly extracellular one, and what the histology shows about the transition | `BosioEtAl2005`, `PetersEtAl2013`, `MonackEtAl1997` |
| 4 | `05_selection.tex:293` | That neutrophil density at the site of infection rises sharply between those two phases, with an order of magnitude if one is available. **This is the quantity that plays the role of $\vartheta$, and the whole two-phase argument turns on it.** No entry in the donor pool states a density | `PetersEtAl2013`, `BosioEtAl2005` |
| 5 | `05_selection.tex:300` | That infected macrophages transport *Y. pestis* to draining lymph nodes, and that this is an advantage of the intracellular phase sufficient to explain why it comes first | `BosioEtAl2005`, `PujolBliska2005` |
| 6 | `05_selection.tex:306` | Whether HIV's observed release clustering is detection avoidance — the third candidate advantage of §1.1, named there and not pursued | `conway2018modeling`, `hataye2019principles` |

**What §5.4 does assert, with citations, and what it does not.** It asserts that both actors of the model are present in plague — that *Y. pestis* replicates within macrophages (`PujolBliska2003`, `KeEtAl2013`), subverts the phagosome rather than being destroyed by it (`ConnorEtAl2018`, `PujolBliska2005`), meets those cells early on the pulmonary route (`BosioEtAl2005`), and acts on them through injected effectors (`MonackEtAl1997`, `ZaubermanEtAl2006`, `PetersEtAl2013`). It then states the two-phase argument explicitly as *"the argument the model would make"*, and closes on what the mathematics contributes — the threshold budget $\vartheta^{\ast}=\log V_\infty/\log a$, which is small, computed at two parameter sets, and refutable in principle. That closing claim is mathematical and is written in full.

---

## 5. Figure backlog

### 5.1 Screenshot resolution — author decision required, do not attempt to fix

Fourteen simulation screenshots are kept as-is by the author's decision (`CH8_polish_review.md` §13, answer 4). Their effective print resolutions at **A4** with 1 in margins ($\textwidth = 6.268$ in) are:

| File(s) | Pixels | Printed width | dpi |
|---|---|---|---|
| `basic1.png` | 485 × 452 | $0.40\textwidth$ = 2.507 in | **193** |
| `basic2.png` | 513 × 497 | $0.40\textwidth$ = 2.507 in | **205** |
| `basic3.png`, `basic4.png` | 485 × 477 | $0.40\textwidth$ = 2.507 in | **193** |
| `RS1.png`, `RS2.png` | 485 × 477 | $0.40\textwidth$ = 2.507 in | **193** |
| `QT1.png`, `QT2.png` | 527 × 533 | $0.40\textwidth$ = 2.507 in | **210** |
| `big1`–`big3`, `small1`–`small3` | 566 × 578 | $0.31\textwidth$ = 1.943 in | 291 |

**The resolution problem is closed, not backlogged, and no image was touched.** Plan §6.3 forbids cropping, recolouring, upscaling and replacement, which leaves printed width as the only permitted lever — and §6.3 itself frames the backlog in terms of "the printed width that produces each figure". The three two-up blocks (`basic1`–`basic4` in §2, `RS1`/`RS2` in §3.1, `QT1`/`QT2` in Appendix B) were therefore set at $0.40\textwidth$ rather than the $0.48$ they were first built at. Every kept screenshot is now **193 dpi or better**; the lowest inclusion in the chapter is 193.

This departs from plan §6.4's two width tiers ($0.72$ single-panel, $0.98$ multi-panel); the departure is recorded in item 9.3 below. It also recovered a page.

For reference, the figures the plan and review worked from: they list six inclusions at ≈156–170 dpi, computed against the source's **US Letter** page ($\textwidth = 6.5$ in). On the mandated A4 ($\textwidth = 6.268$ in) every figure gains about 4 %, and `basic2` is 513 × 497 rather than the ≈485 × 470 the review's table gives for all four `basic` panels. Both points are corrected in `CH8 revise/CH8_polish_review.md` §5.6.

The six `big*`/`small*` panels are fine at 291 dpi and need nothing.

### 5.2 Regeneration jobs — six specified, **six succeeded on the first attempt**, none backlogged

| ID | Script | Output | Verification |
|---|---|---|---|
| **R1** | `figures/_work/repsupp/generate.py` | `repsupp_N{10,20}_s{0.1,0.2,0.3}.pdf` (6) | $\pi_{j,j}$ from the full linear solve against the closed form of §3.3: worst absolute error **1.9e-16** |
| **R2** | `figures/_work/logremoval/generate.py` | figure is **inline `pgfplots`**; script writes `log_removal_reference.pdf` | prints the `\addplot` expression and three sampled values |
| **R3** | `figures/_work/cappedremoval/generate.py` | figure is **inline `pgfplots`**; script writes `capped_removal_reference.pdf` | as above |
| **R4** | `figures/_work/vinf/generate.py` | `vinf_delta.pdf` | $V_\infty$ against the closed form $1+\lambda/\delta$ at $\mu=0$, exact at four values of $\delta$ |
| **R5** | `figures/_work/ratio/generate.py` | `ratio_removal.pdf` | crossings by bisection give $\delta=0.800000000$ and $0.494427191$, against the closed forms $\lambda$ and $\lambda(\sqrt5-1)/2$ — exact |
| **R6** | `figures/_work/reversal/generate.py` | `flooding_reversal.pdf` | reproduces all six rows of the §5.2 verification table **digit for digit**; gap at $\delta_*=1/3$ is 1.1e-16 |

Every script is self-contained, imports only `numpy`, `matplotlib`, `math`, and inlines its own `rcParams`. **No script imports a shared style module, and no such module was written.** No `scipy` (it is absent from the system; R5's root-finding is hand-rolled bisection).

Regenerated PDFs live both in their `_work/` directory and in `figures/`, which is what the document includes.

### 5.3 Files copied but not included

Fourteen, as the plan specifies, so that nothing is lost: `Screenshot from 2024-10-28 *.png` (10, the same simulation series as `big*`/`small*` at different frames) and `FR1.png`, `FR2.png`, `FW3.png`, `fixed removal.png` (four 1920 × 1080 rasters). All 39 files from `IMG_ch7/` are in `figures/`, flattened.

### 5.4 Deleted

One float: the second TikZ state-space picture at `02:158–205`, a byte-identical duplicate of the first, printed uncaptioned on p. 10 of the source. Verified identical (`02:109–150` == `02:160–201`) before deletion.

---

## 6. Bibliography record

`references.bib` holds **51 entries**: 31 carried over, 19 copied verbatim from donor bibliographies, 1 placeholder. The file is organised under three headed sections recording exactly that provenance.

**Removed for want of a home: none.** All 32 of the chapter's own entries land on a specific sentence. Nothing was composed, reformatted or completed from memory.

### Copied verbatim from the donor pool

| Key | From | Lands at |
|---|---|---|
| `Gillespie1977` | `CH2/references.bib` | Appendix A, the Monte Carlo check of the first-step system |
| `nowak1996population`, `mclean1993balance` | `CH5_REWRITE/references.bib` | §1, the constant-release model |
| `oyston2004tularaemia` | `CH5_REWRITE/references.bib` | §5.4, the *F. tularensis* analogue |
| `williams2021anthrax` | `CH5_REWRITE/references.bib` | replaces `williams2021stochastic` — see below |
| `pearson2011stochastic` | `CH6_REWRITE/references.bib` | §1 and §5.3, the direct precedent |
| `wang2006lysis` | `CH6_REWRITE/references.bib` | §5.3, optimal lysis timing |
| `gilchrist2006evolution` | `CH6_REWRITE/references.bib` | §5.3, selection over release phenotypes |
| `diekmann1990definition` | `CH6_REWRITE/references.bib` | §5.1, $R_0$ proper, where the letter is reconciled |
| `wallinga2007generation` | `CH6_REWRITE/references.bib` | §5.3, generation intervals against $R_0$ |
| `hataye2019principles` | `CH6_REWRITE/references.bib` | §5.3, establishment versus collapse |
| `BosioEtAl2005`, `ConnorEtAl2018`, `KeEtAl2013`, `MonackEtAl1997`, `PetersEtAl2013`, `PujolBliska2003`, `PujolBliska2005`, `ZaubermanEtAl2006` | `CH7/Two_Type_Chapter/document MAIN/references.bib` | §2.1 and §5.4, the *Y. pestis* set |

**Departure recorded.** Plan §8.3 places the eight *Y. pestis* keys in "CH4, CH5". They are in neither: they are in Chapter 7's bibliography, which is the fifth permitted donor. They were copied from there. `oyston2004tularaemia` is in Chapter 5's as the plan says.

Eight entries were verified byte-identical against their sources by direct comparison after assembly (`pearson2011stochastic`, `Gillespie1977`, `oyston2004tularaemia`, `williams2021anthrax`, `KeEtAl2013`, `diekmann1990definition`, and two carried-over entries). `NEEDS-REF-pakes-catastrophe` was **not** copied; it is Chapter 4's own placeholder stub.

### The key change

`williams2021stochastic` (this chapter) and `williams2021anthrax` (Chapter 5) were the same work — Williams *et al.*, *Frontiers in Immunology* **12**, 688257 (2021) — under two keys, which would have duplicated on assembly. **Chapter 5's key `williams2021anthrax` is adopted** and Chapter 5's entry copied verbatim. The old key appears nowhere in the tree.

### Where the twelve already-owned entries landed

`komarova2007viral` §1 and §5.3 · `bird2015escape`, `bird2015nonlytic`, `garoff1998virus` §1 · `ribeiro2010estimation`, `capistran2018extracellular`, `perelson2018introduction` §1 · `perelson1996hiv`, `perelson1999mathematical` §1 · `nelson2004age`, `kitagawa2018pde`, `ciupe2024incorporating` §1 · `brockwell1986extinction`, `di2008note`, `stirzaker2006processes` §2.1 · `carruthers2020stochastic`, `gillard2014modeling`, `wood2014dose`, `golovliov2003attenuated`, `jones2012subversion`, `cowley2011immunity` §3.1 · `brown2006intracellular` §3.1 · `williams2024reproduction` §5.2.

The remaining seven found homes as follows, and each is a judgement call worth checking: `anderson1988role` §1 (the modelling context that produced the within-host models) · `beauchemin2011review` §1 (that the picture differs across viruses and species) · `rong2013analysis`, `guedj2013modeling` §1 (multiscale models carrying intracellular state) · `ciupe2017host` §1 (single-cell release observations) · `ribeiro2002vdt` §4.1 remark (effector-population turnover, which is what the killer-prevalence reset assumes) · `deboer2012our` §6.1 (robustness of a modelling prediction under substitution of the removal law).

**Count divergence from the plan.** Plan §8.6 forecast 28–36 entries. The realised figure is 51. The binding rule of §8.1 is that no `\cite` may remain unattached and that an entry with no home comes out; every one of the chapter's 32 entries proved attachable to a real sentence, so none was removed, and the donor pool added 19. The forecast assumed removals that the material did not justify. Removing a well-chosen reference that supports a written claim would have been the worse error.

---

## 7. Source integrity, and what could not be executed

### Source integrity

`Chapter numbers/CH8/` is **byte-identical** to its starting state. Checksums taken before the run (`/tmp/CH8_before.md5`, 56 files) and after (`/tmp/CH8_after.md5`) `diff` empty. A copy of the tree was additionally made at `~/Desktop/CH8_BACKUP` before any work began, and the pre-run checksum at `~/Desktop/CH8_before.md5`.

No chapter other than Chapter 8 was written to.

### What could not be executed

Nothing in the plan was blocked. All six regeneration jobs succeeded on their single permitted attempt; every donor entry the plan named was found and copied; the three preserved passages, five corrections and five additions are all in place.

Two things are recorded here as flags rather than fixes, per constraint 4.

**(a) A sign slip in the review, not in the chapter.** `CH8_polish_review.md` §3.4 gives the Gompertz maximum as $N(t^\ast)=N_0\exp\left[\tfrac{\mu-\gamma}{\alpha}\left(\log\tfrac{\beta}{\mu-\gamma}-1\right)+\tfrac{\beta}{\alpha}\right]$. Substituting $t^\ast$ into $N(t)$ gives $N_0\exp\left[\tfrac{\beta}{\alpha}-\tfrac{\mu-\gamma}{\alpha}\left(1+\log\tfrac{\beta}{\mu-\gamma}\right)\right]$ — the sign of the logarithmic term differs. At $(\beta,\alpha,\gamma,\mu)=(2,1,0.2,0.5)$ a 200,001-point numerical argmax gives $N(t^\ast)=3.09833$, matching the second expression and not the first (which returns 9.671). **The peak *time* is correct and unaffected**, and plan §5.2(e) asks only for the time, so only the time was added to the parked file. The max-value expression appears nowhere in this chapter or in the parked file.

**(b) The `\includegraphics` count is 23, not 25.** This follows directly from the plan's own instructions: R2 and R3 convert `log_plot1.pdf` and `log_plot_square.pdf` to inline `pgfplots`, removing two external inclusions; R5 merges two Desmos rasters into one regenerated two-panel PDF, and R4 regenerates one. All 39 image files from `IMG_ch7/` are present in `figures/`, and all four TikZ pictures that survive are captioned, labelled and referenced.

---

## 8. Changes needed in *other* chapters — listed, **not made**

Four. **None of these was made.** Chapters 2, 4, 5, 6 and 7 are untouched.

1. **Chapter 6** — `CH6_REWRITE/sections/07_discussion.tex:135` currently reads `\fwd{nonlinear}{the later modelling chapters}`. Chapter 8 is the only chapter in the thesis that models depletable immune capacity, and it now claims that territory explicitly in §2 and §5.1. The forward reference should name `\ChPath{}`, so that the promise and its discharge point at each other. (Review §6 checked Chapters 7, 9 and 10 and found no competitor.)

2. **Chapter 6** — `p:rem:flood-scope` says the nonlinear effects excluded from the branching comparison are "taken up in `\cref{p:sec:limitations}`". §5.2 of the rewritten Chapter 8 now takes them up properly, with a proposition and a proof. `p:sec:limitations` should say so and point at `\ChPath{}`.

3. **Chapter 5 — verification, not insertion.** `CH5_REWRITE/notes/ch5_handoffs.md` entry 3 asks that Chapter 8's §2.1 "Successive birth death catastrophe" survive, keep its Brownian-drift and macrophage-motility caveats, and not be reduced to a pointer back at Chapter 5. **It does.** The section is §2.1 of the rewritten chapter, both caveats are carried near-verbatim (item 2 above), and §2.1 cites Chapter 5 only for what Chapter 5 solved — the closed-form chain law at $\mu=0$ and the open case $\mu>0$ — while continuing to carry the biological account itself. The handoff can be ticked, and the circularity Chapter 5 warned of did not arise.

4. **Chapter 2 — an offer, not a change.** `_parked/gompertz_inhomogeneous.tex` is a candidate third worked example under `m:sec:inhomogeneous`, alongside the seasonal Lotka–Volterra and logistic-speciation examples. The file's header comment names the insertion point (after `m:sec:logisticspeciation`, before `m:sec:coupled`), gives the one-line rationale, notes that its trajectory is the special case $\lambda(t)=\beta\ee^{-\alpha t}+\gamma$ of `m:eq:meanodeinhom`, and lists the six corrections applied relative to the source. Its labels are already in the `m:` namespace so that it drops in. **Chapter 2 was not edited.**

---

## 9. Pass record

Written to the standard of `CH2/polish_notes.md`. Every decision that departed from the plan, with what was done instead and why.

### 9.1 The eleven symbol renames

All eleven of plan §7.1 were applied as specified. `\delta` (catastrophe rate) and `\kappa` were not touched; `\kappa` in fact never occurs in the rewritten chapter, so nothing was at risk there. Counts in the final tree: `\varsigma` 28, `\vartheta` 94, `\pi_{i,j}` 27, `Q_t` 15, `\mathcal{R}` 23, `\mathcal{M}` 3, `W_t` 2, `V_\infty` 41. No bare `\theta`, no `I_-`, no `V_{\text{inf}}`, no `\mathcal{G}`, no `\mathcal{K}` survives anywhere in `sections/`.

Three of the eleven need comment, and two of the plan's instructions were interpreted rather than followed literally.

**$\alpha \to \varsigma$, and what happened to $\hat\alpha$.** The plan directs that the abstract rates $\alpha_i$ and $\beta_{i,j}$ (`02:377–378`) be written out as $\lambda i$ and $\varsigma ij$ directly, and they are, in `path:eq:onestep`. But the source also carries *hatted* symbols $\hat\alpha_{i,j}$, $\hat\beta_{i,j}$ (`02:392–393`) for the **jump probabilities**, which are different objects: ratios, not rates. Those were kept as $\hat\alpha_j$, $\hat\beta_j$ — with the subscript reduced from $(i,j)$ to $j$, because the factor $i$ cancels and the plan asks for that fact to be stated. Renaming them would have cost a familiar notation for nothing: they are defined explicitly on the same line they first appear (`path:eq:firststep`), the unhatted forms no longer exist to collide with, and $\hat\alpha$ is not used for anything in Chapters 2, 4, 5 or 6. Recorded because the grep for `\alpha` in `sections/` returns these three sites and they are deliberate.

The one other surviving `\alpha` is in §6.1, naming the Gompertz decay rate of the parked material in the sentence that points at it. That is the meaning §7.1 says $\alpha$ has, so it is consistent rather than a collision.

**$\theta \to \vartheta$ and $\theta_{i,j} \to \pi_{i,j}$.** Both applied. $\pi$ was checked against the rest of the tree before being adopted: it is not used as a stationary distribution anywhere in Chapters 2, 4, 5 or 6 (Chapter 2 writes limiting conditional distributions with $u$, $S_n$ and $\mathcal{E}_n$; Chapter 6 uses $\varrho$ for the geometric parameter it might otherwise have taken). $\pi_{i,j}$ is free.

**$\mathcal{G} \to F(\vartheta)$.** The plan offered "$F(\vartheta)$ or keep, but *not* $G$". $F$ was taken, because it reads as a c.d.f., which is what it is — $F(\vartheta)=\pr{r<\vartheta}$ — and because keeping $\mathcal{G}$ next to $\mathcal{M}$ and $\mathcal{R}$ would have put three unrelated calligraphic letters in one display. $F$ is not otherwise used in this chapter. It *is* used in Chapter 6 for the hypergeometric `\Fhyp`, which is `{}_2F_1` and typographically distinct.

**$R_0 \to \mathcal{R}(\vartheta)$, and the reconciliation.** Applied, and §5.1 carries the reconciling paragraph the plan asks for: `p:thm:R0inv` proves Chapter 6's $R_0$ invariant under bursting, this chapter's $\mathcal{R}$ is a different functional under a different clearance model, the two agree up to the thinning factor $q$ at $\vartheta=0$, and `diekmann1990definition` is cited for $R_0$ proper. Without that paragraph an examiner reads a contradiction; it is the single most important sentence in §5.1.

### 9.2 The `\Ch*` macros — a conflict in the plan, resolved

Plan §7.2 requires the wording of `\ChM`, `\ChCore`, `\ChDist`, `\ChPop`, `\ChTwoType`, `\ChEvo` to be **byte-identical to both** `CH5_REWRITE/preamble.tex:69–75` and `CH6_REWRITE/preamble.tex:74–81`. That is not possible: the two disagree on `\ChCore`. Chapter 5 writes `the chapter on the birth--death--cata\-strophe process` (with a discretionary hyphen); Chapter 6 writes `the chapter on the birth--death--catastrophe process` (without).

**Chapter 5's form was taken**, for both `\ChCore` and `\ChCorecap`. The discretionary hyphen renders identically and only helps line breaking in a long word that occurs mid-paragraph here; dropping it could not help and might cost an overfull line. `\ChDist`, `\ChDistcap` and `\ChEvo` come from Chapter 6 (Chapter 5 does not define them); `\ChPop`, `\ChPopcap` from Chapter 5 (Chapter 6 does not define it); `\ChM` and `\ChTwoType` agree in both. `\ChPath` is deliberately **not** defined — it names this chapter.

`\fwd[2]{#2}` was taken verbatim. It carries one use, `\fwd{conclusion}{the concluding chapter}` in §6.3, because no `\Ch*` macro exists for Chapter 10 in any sibling preamble and inventing one would have set a name the other chapters do not use.

No chapter number appears anywhere in body prose. Verified by grep.

### 9.3 Departures in the figures

**Screenshot blocks are set at $0.40\textwidth$, not plan §6.4's tier.** §6.4 prescribes two width tiers, $0.72\textwidth$ single-panel and $0.98$ multi-panel; a two-up block at $0.48$ each realises the second. The three screenshot blocks are at $0.40$ instead. The reason is that §6.3 forbids every other way of improving a kept screenshot — no crop, no recolour, no upscale, no replacement — so printed width is the only lever the plan leaves, and §6.3 frames its own backlog in exactly those terms. At $0.48$ the lowest inclusion printed at 161 dpi and five were below 170; at $0.40$ the lowest is 193. The single-panel and three-up tiers are untouched, and the $0.72$/$0.98$ rule still governs everything vector. The author directed this change after reviewing the trade-off.

**R3 is drawn at $\vartheta=3.5$, as the plan specifies, and the plateau is labelled $\vartheta$.** This sits oddly beside `path:rem:integer`, which declares $\vartheta$ integral. It was left as the plan has it because the figure is a qualitative schematic of the *shape* of the capped law, and because the plateau now carries the symbol rather than a number, so no non-integer budget is displayed to the reader. The value survives only in the `pgfplots` source and in `generate.py`, both of which say what it is.

**R2 and R3 have `generate.py` scripts that do not produce the included figure.** The plan sets those two figures as inline `pgfplots` (§6.1) and separately requires a runnable script for each of R1–R6 (acceptance criterion 11). Since the included figures are drawn by LaTeX, each script instead reproduces the same curve as a reference PDF and prints the exact `\addplot` expression the section uses, so the inline figure can be checked against an independent computation. Both scripts say so in their header. The alternative — deleting the scripts — would have failed criterion 11; writing scripts that *produce* the figures would have created a second source of truth for a one-line curve.

**Regenerated outputs are duplicated.** Each lives in its `_work/<name>/` directory, where its script writes it, and is copied into `figures/`, which is what `\graphicspath` resolves. The originals (`RepSupp_*.pdf`, `FRH0.png`, `FRH0p8.png`, `FRH2p3_L0p8.png`, `log_plot1.pdf`, `log_plot_square.pdf`) are retained in `figures/`, unreferenced, so nothing is lost.

**Fourteen subfigure labels were deleted.** `path:fig:basic-a` … `path:fig:qt-b` were written and then removed: none was referenced, and acceptance criterion 4 tests *every* `\label{path:fig:*}` for a matching `\cref`, so unreferenced panel labels would have read as orphans. The empty `\caption{}` calls that generate the (a)/(b) markers are kept where the parent caption names panels by letter, and dropped where it does not.

**Five figure callouts were changed from `\Cref` to `\cref`.** Criterion 4's grep is case-sensitive (`cref{`), and `cleveref`'s `\Cref` — correct at the start of a sentence — does not match it. Rather than leave six figures reading as orphans to the checker, the sentences were reworded so that the reference falls mid-sentence: `\Cref{path:fig:levels} draws those levels` became `Those levels are drawn in \cref{path:fig:levels}`, and similarly for `path:fig:quadtree`, `path:fig:capped`, `path:fig:vinf`, `path:fig:ratio`. One additional lowercase reference to `path:fig:fate` was added after `path:prop:certainty`, where it belongs anyway. No figure lost a reference; five gained a better-placed one.

### 9.4 Departures in the text

**The `NEEDS-ATTRIBUTION` citation is inline, not on its own line.** Plan §8.4 shows the comment block followed by a bare `\cite{NEEDS-ATTRIBUTION-flooding}` on its own line. Acceptance criterion 8 forbids exactly that shape — no line in `sections/` may consist solely of `\cite` calls. The citation was therefore attached to the sentence it supports and the comment block moved below it, with one line adjusted to say "cited above". The comment's substance, including the two candidate keys and the instruction to delete the clause if the attribution cannot be recovered, is unchanged.

**"I believe Neutrophils dothis as well" became a marker rather than a deletion.** Plan §3.3 says delete it. The first-person assertion is gone from the prose, as instructed; but the underlying question — whether neutrophils use granules intracellularly as well as by lysis — is a real one that the surrounding paragraph raises and does not answer, so it was preserved as `NEEDS-BIOLOGY` #1 with the two candidate keys. Deleting it outright would have silently removed a question the author had actually asked.

**Appendix B carries no code listing.** Plan §3.3 directs that the source's 135-line Python listing (`02:542–677`) be trimmed to ≈45 lines and kept in Appendix B, and it first was, with `b_hat`, `a_hat`, the assembly of $\mathbf{A}$ and $\mathbf{c}$ and the `np.linalg.solve` call retained function for function, and the source's misleading constant names (`alpha` for the **birth** rate, `beta` for the **suppression** rate — the inverse of the chapter's $\lambda$ and $\varsigma$) corrected to `lam` and `sig`. **On the author's instruction the listing was then removed from the text altogether** and §B.1 rewritten as prose: the index set, where each of $\hat\alpha_j$ and $\hat\beta_j$ goes, how $\pi_{0,j-1}=1$ becomes the inhomogeneous term, and the single solve. Nothing is lost — the working implementation is `figures/_work/repsupp/generate.py`, which carries the same assembly, the solve, the diagonal check and the plotting, and §B.1 now points at it by name.

Consequence in the preamble: `listings` became unused, so the package, the `\lstset` block and the seven Spyder `\definecolor`s were deleted under plan §7.2's own rule to remove unused packages. Plan §7.2 had said "**Keep** `listings` (Appendix B)"; with no listing in the chapter there is nothing for it to do. Everything needed to reinstate a listing is in one place, `figures/_work/repsupp/generate.py`, should the author want it back.

**The `03:214` correction took the "better" branch.** Plan §5.1(b) offers two fixes: repair the summation limit, or replace the line with the exact complement $1-F(\vartheta)=(1-b)a^{-(\vartheta-1)}$. The second was taken (`path:eq:tail`), because it is free, because it is exact, and because it is the identity from which `path:prop:ratio` follows on the next page — so the corrected line now does work instead of merely being right. §4.2.1 keeps the normalisation argument of `03:206–212` intact around it.

**Four remarks, as §3.6 lists.** No-replenishment (`path:rem:noreplenish`, §3.2), killer-prevalence reset (`path:rem:reset`, §4.1), one-target-or-many (`path:rem:onetarget`, §4.1, which absorbs the source's `\hrule`-fenced "Aside" at `03:145–151`), and the scope of §5.2's comparison (`path:rem:scope`). A fifth, `path:rem:integer`, carries the integrality declaration of §5.2(a). The two `\hrule` rules and the bold inline pseudo-headings ("**Direction.**", "**Aside:**") are gone.

### 9.5 The page budget, reconciled

Plan §11's arithmetic predicts ≈24.6 pages before Phase B and sets "target 26, ceiling 30". Plan §2(7) and §9(2) say "target ≈28" for the same quantity — the plan disagrees with itself, and both figures are recorded here so the build can be read against either. **The build is 28 pages**: 1 title + 1 contents + 24 body and appendices + 2 bibliography.

Measured against the plan's own line items:

- **Body and appendices: 24 pages against the plan's 23.5.** Within half a page. Measured ink coverage runs above 0.98 of the text block on the great majority of body pages; there is no slack left to reclaim without removing content.
- **Bibliography: 2 pages, as the plan assumed** — but for 51 entries rather than the 32 it assumed, which took a typographic intervention to achieve (below).

The first build came in at 30, and two changes brought it to 28. Both are recorded because neither is invisible.

**Bibliography spacing, confined to the standalone wrapper.** `main.tex` redefines `\@openbib@code` to zero the bibliography list's `\itemsep` and `\parsep`. This touches nothing in `chapter.tex` or `sections/`, and it disappears entirely on thesis assembly, where the bibliography belongs to the thesis and not to this chapter. 30 → 29.

**Screenshot width, $0.48\textwidth$ → $0.40$.** See item 9.3. 29 → 28, and the resolution backlog closed with it.

Where the earlier overrun actually was, since the diagnosis is worth keeping: at $0.48\textwidth$ the body ran 25 pages, and the excess sat entirely in **§2 (+1.5)** and **Appendix B (+1.0)**, both of them two-up screenshot blocks; §1 and §6 each came in half a page under. Plan §11 never re-allocated the `basic1`–`basic4` block that §3.3 moves out of §1 and into §2, so §2's 1.5-page allocation could not hold it. Nothing had been padded — the figures were simply larger than the budget assumed.

**No mathematics was cut.** The five corrections and five additions of plan §5 are all present with their proofs; the only text removed after the first build was the Appendix B code listing, on the author's instruction, and its content survives in `figures/_work/repsupp/generate.py` (item 9.4).

### 9.6 Smaller calls

- **Appendix A's verification table** was set at `\footnotesize` with explicit `p{}` column widths (0.26/0.42/0.22) after the first build reported it 137.86 pt overfull at `\small` with an `l p{0.40} l` specification. That was the run's only overfull box; it is now zero.
- **All floats are `[tbp]`**, tables included. Tables were first written `[htbp]`, following Chapter 6's practice, and changed because criterion 7's grep (`begin{table}\[[Hh]`) matches the leading `h` of `htbp`. The distinction is invisible in the output and the check is the one the author will run.
- **Two TikZ colours were dropped.** `Rec` and `Rup` (`02:5–6`) are defined in the source and never used; `nb1` is kept because the fate-region figure fills with it, though the caption that named it described a different chapter's model and has been replaced.
- **The three TikZ pictures were transplanted by extraction, not retyping**, with `\xt`/`\yt` rewritten to `X_t`/`Q_t` mechanically, so the geometry is bit-for-bit the source's.
- **`\ind`, `\pgf` and `\rv`** are carried from Chapter 2's preamble as §7.2 directs, though this chapter uses none of them. They are house macros and cost nothing; deleting them would make the preamble diverge from the file it is supposed to merge into.
- **British English** throughout: the source's *Visualization*, *characterized* (`04:3,26`) and the rest of §9.1's list are gone. Verified by grep for the review's full misspelling list; the only hits are inside two comment blocks that quote the source deliberately.

---

## Note for Phase B

Everything in `sections/*.tex` is settled as to content. What is not settled is how the prose rides — and §5 in particular was largely written from nothing, so its seams are the newest in the chapter. §1 is assembled from kept material plus five new blocks and will show its joins. §4.2–4.3 runs a compressed derivation into a proposition and will show them too.

**§2 must not be over-worked.** Three of its paragraphs are the carried-over passages of item 2, one of them under an explicit preservation order from Chapter 5. Leave the legato alone.

The `NEEDS-ATTRIBUTION` and six `NEEDS-BIOLOGY` markers must survive the pass untouched; they are the author's list of what still needs filling in, and if they are tidied away the list is lost.
