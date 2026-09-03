# CH6 figure work-order

What must be regenerated, by whom, and what is blocking it. Written by Phase A
(plan §11.5). **No PDF in `figures/` was created, edited or repointed** — the
directory is a verbatim copy of the source chapter's, minus nothing.

Two figures were **dropped** as floats per plan §11.2; their PDFs remain in
`figures/` in case the decision is reversed.

---

## 1. Regeneration sources — corrected audit

Plan §11.1 states that `NX.1` and `N4b.3` "have only a `README.md` build record
with no TikZ source". **That is not what is in the tree.** Both, and `F4b.1`,
carry a complete standalone TikZ `figure.tex`:

```
figures/_work/NX.1/figure.tex     137 lines
figures/_work/N4b.3/figure.tex    148 lines
figures/_work/F4b.1/figure.tex
```

All three open with

```latex
\input{../../../../style/tikz_style.tex}
```

which resolves to `CH6 revise/style/tikz_style.tex`. **That file is absent from
this tree**, and a search of `~/Desktop/CHAP3-4ab` finds no copy anywhere. So
the three TikZ figures are not unrecoverable — they are blocked on one small
shared style file. Recovering it restores the source of two of the four
visibly broken figures.

`verify_result_20_1.py`, the suite behind Appendix C's 54 checks, is likewise
absent from the whole tree.

---

## 2. Per-figure status

| Figure | File | Source in `_work/` | Where it lands | Defect | Action |
|---|---|---|---|---|---|
| Trilogy handoff | `NX_1_trilogy_handoff.pdf` | `figure.tex` (blocked) | App A | **Text overlap.** The grey annotation strip runs underneath and through the box contents; several phrases illegible. First impression of the old §1. | Recover `style/tikz_style.tex`, rebuild, separate the annotation row from the boxes |
| Constant release fails | `N4b_1_constant_release_fails.pdf` | `generate.py` | §2.2 | In-figure title; caption vocabulary was "producer units" | Caption rewritten to body vocabulary. Optional: strip the in-figure suptitle |
| Kernels (4 sets) | `kernels.pdf` | **none** | — | **Three title lines stacked and unreadable.** | **Dropped** (plan §11.2); superseded by `N4b_7`. No action |
| Kernels, three regimes | `N4b_7_kernels_three_regimes.pdf` | `generate.py` | §3.1 | none | none |
| Renewal schematic | `F4b_1_renewal_schematic.pdf` | `figure.tex` (blocked) | §3.2 | Mild: "each marker starts a cohort" overrun by "cohort born at $t-\alpha$" | Recover style file, rebuild, nudge the two labels apart |
| Gillespie ($\mu=0$, $\mu>0$) | `H_gillespie_mu0.pdf`, `H_gillespie_mu_pos.pdf` | **none** | §3.4 | none | none, unless the suite is recovered |
| $p_{\rm eff}$, $d_{\rm eff}$ curves | `peff_dr_curves.pdf` | **none** | §4.1 | none | none |
| Overlay $\Vfree$ | `overlay_V.pdf` | **none** | §4.3 | Caption said "constant-production surrogate" | Caption rewritten |
| Overlay $\Icell$ | `overlay_I.pdf` | **none** | §4.3 | as above | Caption rewritten |
| Overlay with naive $p$ | `overlay_V_with_naive.pdf` | **none** | §4.3 | as above | Caption rewritten |
| Overlay relative difference | `overlay_rel_diff.pdf` | **none** | §4.3 | none | none |
| Overlay growth phase | `overlay_growth_phase.pdf` | **none** | §4.3 | none | none |
| Identifiability level sets | `N4b_2_identifiability_levels.pdf` | `generate.py` | §4.5 | none | none |
| Exponential reduction (test D) | `D_exponential_reduction.pdf` | **none** | **App C** | none | Relocated from body per plan §11.2 |
| Growth-rate match (test E) | `E_growth_rate_match.pdf` | **none** | **App C** | none | Relocated |
| $R_0$ threshold (test F) | `F_R0_threshold.pdf` | **none** | **App C** | none | Relocated |
| $L$ landscape | `N4b_4_L_landscape.pdf` | `generate.py` | §5.3 | none | none |
| Flooding regimes | `F4b_2_flooding_regimes.pdf` | `generate.py` | §5.3 | none | none |
| Growth trade-off | `F4b_3_growth_tradeoff.pdf` | `generate.py` | §5.5 | none | none |
| Generation times | `N4b_6_generation_times.pdf` | `generate.py` | §5.5 | Caption wrote $\mathbb E[T]$, $d$, $p$ | Caption harmonised to $\mathbb E[T_{\rm prod}]$, $d_{\Icell}$, $p_{\rm eff}(0)$ |
| Pareto extinction/growth | `N4b_5_pareto_extinction_growth.pdf` | `generate.py` | §5.5 | Caption said "constant-production comparator" | Caption rewritten |
| Spectrum (TikZ, inline) | inline in §6 | in the chapter source | §6 | **Endpoint labels collided with tick labels.** | **Repaired in source** (plan §11.4): "budding"/"bursting" moved to their own row at `below=1.4cm` |
| Release spectrum (raster) | `N4b_3_release_spectrum.pdf` | `figure.tex` (blocked) | — | **Severe collisions**: red dashed HIV box overlaps the stage box; "shared stage language only" prints over box text; top annotation row clipped to fragments | **Dropped** (plan §11.2); the TikZ spectrum is kept instead. No action unless reinstated |
| HIV stages (TikZ, inline) | inline in §6.5 | in the chapter source | §6.5 | sound as drawn | Symbols updated: Erlang step rate $\alpha\to\omega$ (plan §6) |

**Counts.** 20 figure floats survive — 17 in the body, 3 in the appendices —
which is exactly plan §11.2's target. Twelve included PDFs have no regeneration
source anywhere in this tree: `kernels` (dropped), all five `overlay_*`,
`peff_dr_curves`, and the four D/E/F/H verification figures (`H` is two files).

---

## 3. Author actions

Ordered by consequence.

### A1 — The Carruthers novelty check. **Blocks submission.**

The draft's open problem 5 read:

> *Verify whether Carruthers et al. already couple an intracellular BDC to a
> between-cell model — the novelty claim of §3 depends on the answer.*

Per plan §10.3 that item has been **deleted from the chapter**: a to-do note
stating in the author's own words that the central novelty claim is unverified
cannot go to an examiner. The check itself has not been done and cannot be done
by an agent.

Verify it against `carruthers2020stochastic` and the surrounding literature. If
they do couple an intracellular birth–death–catastrophe process to a
between-cell model, Remark `p:rem:novelty` in §3.2 needs rewriting — it
currently claims novelty for the *derivation of the kernels from a mechanistic
intracellular process*, which is the narrower and more defensible claim, but it
would still need to engage them directly.

### A2 — Recover `style/tikz_style.tex`

One file unblocks three TikZ figures, two of which are among the four with
visible text-overlap defects (`NX.1`, `N4b.3`) and one of which has a mild one
(`F4b.1`). It lived at `CH6 revise/style/tikz_style.tex` relative to the
`figure.tex` files. Check the `new_notes3` folder if it can be located.

### A3 — Recover `verify_result_20_1.py` and archive it

Appendix C cites 54 checks that no longer have a runnable suite in this tree.
The reproduction block now reads `cd <repository or archived release>` with an
`% AUTHOR-ACTION` marker: replace with a repository URL or an archived DOI
(Zenodo), and state the Python/NumPy/SciPy versions. Recovering the suite also
restores the source of the four D/E/F/H verification figures.

### A4 — Confirm the eclipse-division correction

Plan §10.1. The draft's HIV stage equations (`07_hiv_contrast.tex:205–211`)
printed

$$\frac{\mathrm dE_j}{\mathrm dt}=\alpha E_{j-1}+\rho_{\rm div}E_j-(\mu_E+\rho_{\rm div}+\alpha)E_j$$

in which the $\rho_{\rm div}$ terms **cancel identically**, so eclipse
proliferation had no effect at all — contradicting the surrounding text, which
stresses that sustained detection *is* proliferation in eclipse. §6.5 now
prints

$$\frac{\mathrm dE_j}{\mathrm dt}=\omega E_{j-1}+\rho_{\rm div}E_j-(\mu_E+\omega)E_j$$

with the Dirac source replaced by the initial condition $E_1(0)=\alpha_AL_0$.
An `% AUTHOR-ACTION` comment marks the spot. Please confirm against the original
derivation.

### A5 — Verify the six new BibTeX entries

`wallinga2007generation`, `diekmann1990definition`, `nelson2004agestructured`,
`miao2011identifiability`, `wang2006lysis`, `metz1986dynamics` were copied
verbatim from plan §8.3, which supplies them so that an agent copies rather than
composes. **Volume, issue and page numbers must be checked against the published
record before submission.** The pre-existing `TODO(verify)` markers in
`references.bib` are also still outstanding.

### A6 — Work the `% NEEDS-REF:` markers

Seven, all in the chapter source:

| Where | Topic |
|---|---|
| §4.2 | Crump–Mode–Jagers general branching processes |
| §5.5 | optimal lysis timing beyond Wang (Abedon; Bull) |
| §6.5 | Allee effects and stochastic establishment theory |
| §6.5 | Erlang-eclipse within-host models; the Rong–Feng–Perelson line |
| §7.3 | *Y. pestis* macrophage residence, YCV maturation, and the YopJ / pyroptosis / necroptosis exit literature |
| App D | a standard Volterra-quadrature reference |

### A7 — The three deferred proofs

`% HOOK-MATHS:` markers only, per plan §16. Each names its section in
`CH6_polish_review.md`:

| Marker | Claim | Review |
|---|---|---|
| §3.2 | that the renewal system gives the first moments of the underlying stochastic process exactly | §4.3 |
| §4.1 | that $p_{\rm eff}$ is monotone decreasing in $r$ | §4.2 |
| §5.5 | that $r_{\rm bud}>r_{\rm burst}$ in general | §4.4 |

The chapter now states each honestly where it occurs — as a numerical check, as
a claim over five named parameter sets, and as a claim over three named regimes
— and §7.4 records all three together.

### A8 — Optional figure work, if sources are recovered

- Strip in-figure titles and suptitles throughout; thesis convention is
  caption-only, and several N-series figures carry a bold title inside the
  graphic in a non-document font.
- Remove shouty capitals from any in-figure text ("the **NEW** (renewal) BMVR",
  "the **CLASSICAL** model"). All *captions* have already been rewritten to the
  body's vocabulary; the in-graphic text has not, and cannot be without sources.
- If `kernels.pdf` becomes rebuildable it is still not needed: `N4b_7` is the
  better figure and now carries the job.
