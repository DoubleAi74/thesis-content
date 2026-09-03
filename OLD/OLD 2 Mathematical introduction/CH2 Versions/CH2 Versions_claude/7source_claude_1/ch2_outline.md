# Chapter 2 — outline as built

**Built:** 46 pages, ~13.9k words of prose (detex count; excludes display maths).
Compiles clean: no undefined references, no undefined citations, no overfull boxes
above 20pt. All 18 bibliography entries are cited.

## Files

| File | Role |
|------|------|
| `chapter2.tex` | **Thesis-ready fragment.** Opens with `\chapter`, no preamble of its own. `\input` this into `Thesis.tex`. |
| `ch2_preamble.tex` | Packages + macros the fragment needs. Merge into the thesis preamble; delete duplicates. |
| `main.tex` | Thin standalone wrapper so the chapter compiles alone. Not needed once the chapter is in the thesis. |
| `main.pdf` | The compiled chapter. |
| `sections/01…09` | Section bodies. |
| `references.bib` | 18 entries (11 carried from the seed, 7 added). |
| `figures/IMG_ch3/` | All 15 figures, copied in so the folder is self-contained. |

## Spine

| § | Title | Pages | Words | Source |
|---|-------|-------|-------|--------|
| 2.1 | Introduction | 3 | 610 | seed + new signposting |
| 2.2 | Preliminaries | 4–6 | 1,389 | index (menu only) |
| 2.2.1 | Exponential clocks | | | index |
| 2.2.2 | Continuous-time Markov chains | | | index |
| 2.2.3 | Probability generating functions | | | index |
| 2.2.4 | The linear birth–death process | | | index |
| 2.3 | The Galton–Watson process | 7–11 | 1,457 | seed |
| 2.3.1 | Death or division | | | seed |
| 2.3.2 | Certainty of extinction | | | seed |
| 2.3.3 | The critical case | | | seed |
| 2.4 | The limiting conditional distribution | 12–15 | 1,165 | seed |
| 2.4.1 | Late-time survival probability | | | seed |
| 2.4.2 | Mean | | | seed |
| 2.4.3 | Variance | | | seed |
| 2.4.4 | A continuum view of the survival recursion | | | seed |
| 2.5 | Survival of small populations | 16–21 | 2,076 | seed + new §2.5.5 |
| 2.5.1 | An initial cohort of size $k$ | | | seed |
| 2.5.2 | Conditioning and apparent early growth | | | seed, recast abstractly |
| 2.5.3 | Discrete birth–death–catastrophe | | | seed |
| 2.5.4 | Continuous-time birth–death | | | seed |
| 2.5.5 | Continuous-time birth–death–catastrophe | | | **new** (definition only) |
| 2.6 | **The constant $A(p)$** *(original work)* | 22–32 | 3,899 | seed |
| 2.6.1 | An infinite-product representation | | | seed |
| 2.6.2 | An exact series and two-sided bounds | | | seed |
| 2.6.3 | Behaviour as $p\to\frac12^-$ | | | seed |
| 2.6.4 | Why the discrete and continuous constants differ | | | seed |
| 2.6.5 | Searching for a closed form | | | seed, compressed |
| 2.6.6 | The Koenigs connection | | | seed |
| 2.6.7 | Computing $A(p)$ in practice | | | seed |
| 2.7 | Absorption models and the method of characteristics | 33–40 | 2,492 | seed |
| 2.7.1 | Absorption only | | | seed |
| 2.7.2 | Absorption–death | | | seed |
| 2.7.3 | The method of characteristics, tested | | | seed |
| 2.7.4 | Absorption–birth–death *(original)* | | | seed |
| 2.8 | Summary | 41 | 290 | **new** |
| 2.A | An integral identity for the hypergeometric function | 42 | | seed |
| 2.B | Extracting state probabilities from a generating function | 43–44 | | seed |

## Numbered results

| Label | Statement |
|-------|-----------|
| Def. 2.1 | Exponential law |
| Prop. 2.2 | Competing clocks (min is exponential; winner is a weighted choice, independent of the time) |
| Rem. 2.3 | Direct simulation (Gillespie) |
| Rem. 2.4 | $S_n\sim A(p)(2p)^n$ is an equivalence, not an identity |
| Def. 2.5 | Birth–death–catastrophe process |
| Prop. 2.6 | Series representation: $1/A(p) = 1+\sum_n (2p)^n/(2-S_n)$ |
| Prop. 2.7 | Two-sided bounds: $\varepsilon/(1+\varepsilon) < A(p) < 2\varepsilon/(1+2\varepsilon)$ |
| Prop. 2.8 | Parity bound: $A(p)\le\frac12$ |
| Rem. 2.9 | Rate of approach to the near-critical asymptotic |
| Def. 2.10 | Koenigs function / Schröder equation |
| Prop. 2.11 | $A(p) = 2\psi_r(\frac12)$ |
| Rem. 2.12 | Attracting versus repelling linearisations |
| Prop. 2.13 | Generating function for absorption–birth–death |
| Rem. 2.14 | Domain of validity of the $\Psi$ series |
| Rem. 2.15 | Resonance, $\alpha = n(\mu-\lambda)$ |
| Prop. 2.16 | Integral identity for ${}_2F_1$ |

## Notation

Bold is reserved for the vector-valued states of later multi-type chapters; every
scalar here is italic.

| Object | Symbol |
|--------|--------|
| Offspring random variable | $L$ |
| Generation size | $Z_n$ |
| Extinction / survival probability by generation $n$ | $u_n$, $S_n = 1-u_n$ |
| Survival from a cohort of $k$ | $S_n^{(k)}$ |
| Distance from criticality | $\varepsilon = 1-2p$ |
| Logistic parameter | $r = 2p$ |
| Interior / exterior particle counts | $X_t$, $Y_t$ |
| Birth, death, absorption rates | $\lambda$, $\mu$, $\alpha$ |
| Discrete rupture probability; continuous rupture rate | $\kappa$; $\rho$ |
| Characteristic coordinates | $(\sigma,\eta,\tau)$ |
| Discrete / continuous quasi-stationary constant | $A(p)$ / $A_{\mathrm c}(p)$ |

Three collisions carried by the seed were resolved rather than reproduced:

1. Bold $\mathbf X$ denoted the offspring variable, the expected population and the
   interior particle count in three different sections. Now $L$, $Z_i$ and $X_t$.
2. $r$ denoted both $1-2p$ (Riccati view) and $2p$ (logistic map). Now $\varepsilon$
   and $r$ respectively, fixed by a definition at first use.
3. The characteristic coordinate $r$ in the method-of-characteristics section
   collided with the logistic $r$. Renamed $\eta$, with $s\to\sigma$ alongside it.

Two further symbols were changed for consistency with the preliminaries: interior
birth rate $\beta\to\lambda$ (so $b_1 = \lambda-\mu$, $x_-=\mu/\lambda$), and the
appendix constants $p,q\to P,Q$, which had clashed with the replication
probability $p$.

## Forward references

All routed through one macro, `\fwd{key}{prose}`, defined in `ch2_preamble.tex` as
`\newcommand{\fwd}[2]{#2}`. Redefining that single macro is enough to make every
forward reference carry a chapter number once the thesis order is fixed.

| Key | Prose as typeset | Hook |
|-----|------------------|------|
| `inhomog` | "the later chapter on non-constant rates" | Ch. 7 |
| `bdc` | "the later chapters on birth–death–catastrophe processes" | Ch. 3–4 |
| `multitype` | "the chapter on multi-type processes" | Ch. 5 |
| `rupture` | "the chapter on compartment rupture" | Ch. 6 |

## Heuristic steps, all marked in the text

1. §2.3.3 — difference equation replaced by a differential equation to obtain
   $S_n\sim2/n$ at criticality.
2. §2.4.4 — the same replacement for the Riccati view, with the explicit note that
   the constant of integration is exactly what the approximation cannot supply.
3. §2.5.3 — the mean-population substitution in the birth–death–catastrophe
   survival probability, shown by Jensen's inequality to be a lower bound rather
   than an identity.
4. §2.6.3 — the two-scale argument for $A(p)\sim2(1-2p)$, and the asymptotic
   matching of the alternative derivation, with a note that the matching step is
   the delicate one.
5. §2.6.6 — an explicit "what this does and does not establish" passage separating
   hypertranscendence of $\psi_r$ in $z$ from any claim about $p\mapsto A(p)$.
