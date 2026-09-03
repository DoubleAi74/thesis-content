# Figure provenance — `CH2_best`

> **Temporary candidate gallery added (9 August 2026).** Every figure from all four base
> merges is now staged under `figures/candidates/` and displayed in a gallery appendix in
> each PDF; see `FIGURE_CANDIDATE_INVENTORY.md` and `FIGURE_GALLERY_LOG.md`. Production
> figure choices are unchanged pending human selection, so the tables below still
> describe what the narrative uses.

Every figure that appears in the narrative of either PDF, with where it came from. Figures drawn inline
with TikZ/pgfplots in the section files carry no binary and are marked accordingly.
Nothing in this list is unreferenced: each entry has a caption and a sentence that sends
the reader to it.

## Chapter M

| Fig. | Asset | Kind | Source |
|---|---|---|---|
| 1.1 | `rw_transition.pdf` | binary | **Qwen**, regenerated — `figures/make_rw_transition.py`. Donor labelled the step probability $p$; redrawn with $q$, per `NOTATION.md` |
| 1.2 | `random_walk.pdf` | binary | Claude (`figures/make_figures.py`) |
| 1.3 | `simpleGWvis.png`, `subGWvis.png` | binary | Claude |
| 1.4 | `poisson_process.pdf` | binary | Claude (`figures/make_figures.py`) |
| 1.5 | `birth_death_paths.pdf` | binary | Claude (`figures/make_figures.py`) |
| 1.6 | — | inline TikZ | Claude (transition-rate diagrams, BD and BDC) |
| 1.7 | `logspec_mean.pdf` | binary | **Qwen**, regenerated — `figures/make_inhomogeneous_figures.py`. Curve unchanged; axis label $r$ → $\gamma$, since $r=2p$ is frozen |
| 1.8 | `coupled_ode_ctmc.pdf` | binary | Claude (`figures/make_figures.py`) |
| 1.9 | `rupture_sawtooth.pdf` | binary | **Qwen**, regenerated — `figures/make_inhomogeneous_figures.py`. Donor binary did not satisfy its own caption; see `MERGE_LOG.md` §5 |
| 1.10 | — | inline pgfplots | Claude (cobweb panels and the $S_\infty$ transition) |
| 1.11 | `extinction_and_law.pdf` | binary | Claude (`figures/make_figures.py`) |
| 1.12 | `conditionalMean.pdf` | binary | Claude |
| 1.13 | `dtctA.png` | binary | Claude |
| 1.14 | — | inline pgfplots | Claude (characteristic curves) |
| 1.15 | — | inline TikZ | Claude (compartment and medium schematic) |
| 1.16 | `abs2.pdf` | binary | Claude |
| 1.17 | — | inline pgfplots | Claude (harmonic series) |
| 1.18 | `power_law_fixed.pdf` | binary | Claude |
| 1.19 | — | inline TikZ | Claude (early $S_n$, three parameters) |
| 1.20 | `kvals.png` | binary | Claude |
| 1.21 | `kvals505.png`, `kvals495.png` | binary | Claude |
| 1.22 | `abs1.pdf` | binary | Claude |

## Chapter A

All figures are Claude's, unchanged: `figure1_parameter_conjugacy.pdf`,
`figure2_koenigs_linearization.png`, `figure3_numerical_koenigs.png`,
`figure4_mandelbrot_context.png`, `period_double.png`, `A3_hat_plot.pdf`, `dtctA.png`.

`figures/conditionalMean.pdf` is present in Chapter A's figure directory but referenced
by no section; it is inherited from the Claude base and left in place, unused.

## Donors declined

| Asset | Donor | Why not |
|---|---|---|
| `ruin_prob.pdf` | Qwen M | Redundant with panel (b) of `random_walk.pdf`, which plots the same gambler's-ruin curves |
| `bd_conditional_mean.pdf`, `bd_mean_regimes.pdf`, `bd_mean_survival_panel.pdf`, `bd_survival_regimes.pdf`, `poisson_path.pdf`, `ruin_hitting.pdf` | Grok M | Every one duplicates a Claude figure already carrying the point (`birth_death_paths.pdf`, `conditionalMean.pdf`, `extinction_and_law.pdf`, `poisson_process.pdf`, `random_walk.pdf`). No sentence in the merged text was waiting for any of them |
| `founder_cohort_survival.pdf`, `gw_regime_diagnostics.pdf` | Codex M | The cohort and critical-regime material they would support is already illustrated by `kvals*.png` and `power_law_fixed.pdf` |
| `Ap_bounds_ratio.pdf`, `Ap_nearcrit.pdf`, `koenigs_domain.pdf` | Qwen A | Chapter A is Claude's and its text does not expect them |

## Reproducing the binaries

```sh
cd chapter_M_math_intro/figures
python3 make_figures.py                  # Claude's set
python3 make_rw_transition.py            # fig. 1.1
python3 make_inhomogeneous_figures.py    # figs. 1.7 and 1.9
```

Requires `numpy` and `matplotlib`. Seeds are fixed, so output is reproducible.
The remaining binaries (`kvals*.png`, `simpleGWvis.png`, `subGWvis.png`, `abs1.pdf`,
`abs2.pdf`, `conditionalMean.pdf`, `dtctA.png`, `power_law_fixed.pdf`) are carried over
from the Claude base without generating scripts.
