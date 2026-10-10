# Markov model extraction

Complete extraction of every stochastic model with Markovian dynamics from
the thesis **"Stochastic models of early *Yersinia pestis* infection"**
(source: `../full_draft_thesis/main.pdf`, September 2026 working draft, read
from its LaTeX chapter sources `../full_draft_thesis/chapters/ch01`–`ch10`).

## Contents

- `main.tex` — the document. **38 numbered models + 4 general frameworks**,
  each specified in a uniform sheet: class, state space, dynamics (the
  defining transition rates / probabilities / offspring laws, quoted from
  the thesis), parameters, initial conditions, principal closed forms with
  the thesis's own `label` keys, and location/connections. Deterministic
  non-Markov companions (BMVR, renewal system, projection map, mean-field
  ODEs, rate comparisons) are included and flagged **[D]**.
- `README.md` — this file.

## Compile

```sh
cd markov_model_extraction
latexmk -pdf main.tex
```

Self-contained (article class; amsmath, booktabs, longtable, hyperref
only) — no thesis macros or preamble needed. Thesis `label` keys
(e.g. `bdc:thm:I`, `dist:thm:qsd`, `tt:thm:main`) are cited throughout as
stable identifiers, since the thesis cross-references by key rather than
printed number.

## Inventory

| ID | Model | Class | Ch. | One-line spec |
|----|-------|-------|-----|----------------|
| F1 | Discrete-time Markov chain | framework | 2 | $P_{ij}$, Chapman–Kolmogorov |
| F2 | Continuous-time Markov chain | framework | 2 | generator $q_{ij}$, exponential clocks, Gillespie |
| F3 | Time-inhomogeneous CTMC | framework | 2 | $Q(t)$, forward/backward Kolmogorov |
| F4 | Coupled ODE–CTMC (PDMP) | framework | 2 | joint generator; three coupling types |
| M1 | Random walk / gambler's ruin | DTMC | 2 | $P_{i,i\pm1}$; ruin probabilities |
| M2 | Galton–Watson (binary) | DTMC branching | 1–3 | $p_2=p$; $S_n\sim A(p)(2p)^n$; Koenigs/hypertranscendence |
| M3 | Poisson process | CTMC | 2 | $q_{n,n+1}=\alpha$; thinning |
| M4 | Yule process | CTMC | 1, 2 | $q_{n,n+1}=\lambda n$; geometric law |
| M5 | Linear birth–death | CTMC | 1, 2 | $\lambda n,\mu n$; Kendall solution; $A_c$ |
| M6 | **Birth–death–catastrophe (BDC)** | CTMC | 2, 4, 5 | $\lambda n,\mu n,\delta n\to H$; the spine; full distribution theory |
| M7 | Discrete-generation catastrophe | DTMC variant | 2 | per-generation hazard $\chi$; Jensen gap |
| M8 | Inhomogeneous linear BD | CTMC $Q(t)$ | 2 | $\lambda(t),\mu(t)$; backward Riccati |
| M9 | Seasonal Lotka–Volterra | 2-pop.\ CTMC | 2 | periodic prey birth $\mathcal S^+(t)$ |
| M10 | Logistic speciation | nonhom.\ Yule | 2, 9 | $\beta(t)=\sigma(K-N(t))$; exact geometric marginal |
| M11 | Gated release | PDMP | 2 | gate opens at rate $\eta A_t$ |
| M12 | Surging gated release | PDMP | 2 | gate opens at rate $\nu$ (autonomous) |
| M13 | Absorption-only | bivariate CTMC | 2 | uptake $\alpha$; binomial |
| M14 | Absorption–death | bivariate CTMC | 2 | $+\mu$; characteristics worked example |
| M15 | Absorption–birth–death | bivariate CTMC | 2 | $+$ interior BD; **novel pgf (thesis result)** |
| M16 | Chained immediate transfer ($\mu=0$) | chained CTMC | 5, 8 | burst founds next cell; negative-binomial ruptures |
| M17 | Budding comparator cell | two-stream Poisson | 5, 6 | release $p$, death $d_I$; geometric |
| M18 | Basic model of viral replication | **[D]** ODE | 1, 6 | $\dot I=\gamma TV-d_I I$, $\dot V=pI-cV$; $R_0$ |
| M19 | Within-host population process | CTMC population | 6 | BDC cells + infect/clear; first-moment exactness |
| M20 | Burst-aware renewal system | **[D]** exact means | 6 | $I=I_0\hat I+(i*\hat I)$; $(S,g)$ skeleton |
| M21 | Effective-parameter projection | **[D]** map | 6 | $p_{\rm eff}(r)=\delta\mathcal L K/\mathcal L\hat I$ |
| M22 | Generation kernel / $R_0$ | **[D]** functional | 6 | $\mathcal A(\alpha)$; $R_0=\gamma TV_\infty/c$; invariance |
| M23 | Establishment branching (burst vs bud) | GW offspring | 6 | flooding $L=a(1-b)$; $z_{\rm ext}$ difference |
| M24 | Invasion-speed comparison | **[D]** | 6 | $r_{\rm bud}>r_{\rm burst}$; Laplace order |
| M25 | Reset process | CTMC + death | 6 | dumps to 0 at rate $\delta n$; cell death $d_I$ |
| M26 | Partial-release stock model | **[D]** mean-field | 6 | thinning $\varphi$; stock $Q$; visibility of clock |
| M27 | HIV skeleton variant | specification | 6 | Allee incidence; Erlang eclipse |
| M28 | **Two-type catastrophe process** | 2-type CTMC | 7 | $\lambda_i,\mu_i,\nu$; $\delta_1x+\delta_2y\to\mathsf R$; hypergeometric $S$ |
| M29 | Replicator–suppressor | nonlinear CTMC | 8 | birth $\lambda i$, kill $\varsigma ij$; diagonal law |
| M30 | Playing-field particle model | spatial sim. | 8 | Brownian; killers used up; $\vartheta(r)\sim\log(r+1)$ |
| M31 | Fixed-removal ratio model | functional on M6 | 8 | $\mathcal R(\vartheta)=V_\infty a^{-\vartheta}$; reversal at $L<1$ |
| M32 | Pimentel competition chain | path-dep.\ DTMC | 9 | moving unstable critical point $i_c$ |
| M33 | Pimentel+ | specification | 9 | fitness + species BD coupling ($-\gamma S$) |
| M34 | Rise–run–ruin–rejuvenation | CTMC + ODE | 9 | catastrophe $\delta X_t/V(t)$; revival $\omega$ |
| M35 | Multiplicative dissipation | stochastic CA | 9 | $256^2$ torus; fragmentation $\delta X_i/V_i$ |
| M36 | Birth–plague (+ vitality) | two-type CTMC | 9 | bilinear infection $\chi X_tY_t$ |
| M37 | Public good accumulation | CTMC + ODE | 9 | $\lambda(t)=\lambda_0+\alpha P(t)$; $K^*$; GW embedding |
| M38 | Quadrant argument | **[D]** comparison | 10 | $p_N^*=(\mu_E-\mu_M)/(\mu_N-\mu_M)$ |

Chapter 3 adds no new process beyond M2 (it is the $A(p)$/Koenigs analysis
of the Galton–Watson model); Chapter 4's and Chapter 5's theory is the
analysis of M6 and its $k$-founder / killing-convention variants, covered
inside M6's entry.
