# OUTLINE_PASS2 — frozen target structure for Chapter M (pass 2)

Frozen 2026-08-07 per `SECOND_PASS_CHAPTER_M_OUTLINE.md` §5 (phase S1) and the
following user decisions:

- Displaced pass-1 bulk (GW critical theory, QSD variance, discrete-BDC
  calculation, full MoC ladder) → **M appendices** (not dropped).
- New blocks (§2.1 random walk, §2.2 Poisson, §2.3 logistic speciation,
  §2.4 coupled ODE–CTMC) → **written fully** in this pass (standard
  textbook-level constructions; no thesis-specific claims invented).
- MoC worked example in body → **absorption–death**; abs-only and ABD catalogue
  to appendix.
- Thesis numbering → standalone builds set to **M = Chapter 2, A = Chapter 3**.

## Section layout and donors

| New file | Section | Donors (pass-1 M unless noted) |
|---|---|---|
| `01_overview.tex` | §2.1 Overview | pass-1 intro + synthesis, rewritten as framework/methods map |
| `02_discrete_markov.tex` | §2.2 DTMC: random walk (**new**); GW compressed | pass-1 §3 (definition/PGF/mean only); depth → App 2.C and Chapter A |
| `03_continuous_markov.tex` | §2.3 CTMC: clocks/races; Poisson (**new**); BD; BDC | pass-1 prelims (exp, CTMC, BD) + §5 (BDC def) |
| `04_time_inhomogeneous.tex` | §2.4 Time-inhomogeneous + logistic speciation (**new**) | none in drafts; standard construction |
| `05_coupled_ode_ctmc.tex` | §2.5 Coupled ODE–CTMC (**new**) | none in drafts; conceptual framework + schematic rupture example |
| `06_methods_discrete.tex` | §3.1 Discrete-time methods (brief) | pass-1 §3 iteration + first-step; pointer to Chapter A / Koenigs |
| `07_methods_continuous.tex` | §3.2 CT methods via BD: backward eqs, mean, variance, hitting, extinction, conditional means | pass-1 prelims BD + §4 mean + §5 CT BD (Ac compressed); variance → App 2.E |
| `08_method_of_characteristics.tex` | §3.3 MoC accessible + worked example (absorption–death) | pass-1 §6 (recipe abstracted; abs-death worked example kept) |
| `09_app_moc_support.tex` | App 2.A integral identity; App 2.B coefficient extraction | pass-1 apps (unchanged) |
| `10_app_critical.tex` | App 2.C Critical branching in detail | pass-1 §3.2–3.4 (extinction, critical power law, reciprocal increments, total progeny, figures) |
| `11_app_cohorts.tex` | App 2.D Founding cohorts and early survival | pass-1 §5 (early-S_n arithmetic, k-cohort, push of the past, figures) |
| `12_app_variance.tex` | App 2.E Quasi-stationary variance derivation | pass-1 §4.3 |
| `13_app_dbdc.tex` | App 2.F Discrete BDC + killed chain | pass-1 §5.3 + killed-chain subsubsection |
| `14_app_moc_catalogue.tex` | App 2.G Further absorption models (abs-only; ABD closed form + regular rep + hypergeometric) | pass-1 §6 (remainder) |

## Rules applied

- Notation/label freeze of `NOTATION.md` preserved; all labels keep `m:` prefix.
- No Chapter A theory re-absorbed: product/series/bounds/asymptotic/Koenigs/HT
  stay in Chapter A; M carries the $A(p)$ *definition*, the quasi-stationary mean
  $1/A(p)$, the elementary $\Ac(p)$ sketch, and pointers.
- Abstract voice; no scripts; `\fwd{}` forward references retained for later
  thesis chapters.
