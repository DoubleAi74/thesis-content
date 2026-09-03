# Notation and label freeze (merge phase)

This file records the conventions frozen for the two merged chapter projects. It is a
builder document, not chapter content.

## Symbols

| Object | Symbol | Notes |
|---|---|---|
| Discrete-time population at generation $n$ | $Z_n$ | started from $Z_0=1$ unless stated |
| Continuous-time population at time $t$ | $X_t$ | |
| Offspring random variable | $L$ | binary law: $\Pr(L=2)=p$, $\Pr(L=0)=1-p$ |
| Offspring generating function | $\phi(z)=pz^2+(1-p)$ | |
| Survival probability | $S_n=\Pr(Z_n>0)$ | recursion $S_{n+1}=2pS_n-pS_n^2$, $S_0=1$ |
| Extinction probability by generation $n$ | $u_n=1-S_n$ | |
| Kolmogorov (discrete) constant | $A(p)$ | $A(p)=\lim_n S_n/(2p)^n$ |
| Continuous-time analogue | $A_{\mathrm c}(p)$ | macro `\Ac`; $A_{\mathrm c}(p)=(1-2p)/(1-p)$ |
| Near-critical gap | $\varepsilon=1-2p$ | never reused for anything else |
| Logistic multiplier | $r=2p$ | never reused for a rate |
| Koenigs linearising coordinate | $\psi_r$ | $\psi_r(f_r(z))=r\psi_r(z)$, $\psi_r(0)=0$, $\psi_r'(0)=1$ |
| Koenigs basin extension | $\Psi_r$ | used where the evaluation point lies outside the germ |
| Koenigs parametrisation (inverse) | $\varphi_r=\psi_r^{-1}$ | the function classified by Becker–Bergweiler |
| Birth / death / catastrophe rates | $\lambda,\mu,\rho$ | per capita |
| Absorption (uptake) rate | $\alpha$ | per exterior particle |
| Absorption-model series function | $\Psi(\zeta)$ | **Chapter M only**; distinct from the Koenigs $\Psi_r$, which appears only in Chapter A |

`\Ac` is the only permitted spelling of the continuous-time constant. "Constant $A(p)$" is
the standard phrase in headings; "amplitude" may appear once as a synonym.

## Label prefixes

- Chapter M: `m:` — e.g. `\label{m:sec:gw}`, `\label{m:eq:SnIter}`
- Chapter A: `a:` — e.g. `\label{a:prop:series}`, `\label{a:thm:ht}`

No bare label (`sec:Ap`, `eq:lateS`, …) survives from the sources; every label carries its
chapter prefix so that the two projects can be concatenated into one thesis without
collision.

## Cross-chapter references

Each preamble defines

```latex
\newcommand{\ChM}{the mathematical introduction}
\newcommand{\ChA}{the following chapter}   % in M
\newcommand{\ChA}{this chapter}            % in A, where needed
```

so that thesis integration only has to redefine these macros to emit real chapter numbers.
Forward references inside Chapter M to the deep $A(p)$ theory are all routed through `\ChA`.

## Structural conventions

- `report` class, `\chapter` at top level, so both projects are thesis-shaped fragments.
- `\graphicspath{{figures/}}`; every figure is a local copy. No `../` paths.
- Theorem environments numbered within `chapter`, shared counter across
  theorem/proposition/lemma/corollary/definition/remark.

## Symbols added in the `CH2_best` merge

These enter only with the time-inhomogeneous and coupled material of Chapter M
§1.2.3–§1.2.4. None of them displaces a frozen symbol above; each is defined at the
point of use.

| Object | Symbol | Notes |
|---|---|---|
| Time-dependent birth / death rates | $\lambda(t)$, $\mu(t)$ | **Chapter M only**; the homogeneous $\lambda,\mu$ are unchanged |
| Logistic intrinsic growth rate | $\gamma=\lambda_0-\mu$ | **Chapter M only.** The donor draft called this $r$; renamed, because $r=2p$ is frozen |
| Niche capacity / logistic equilibrium | $K$, $N_\ast=K(1-\mu/\lambda_0)$ | **Chapter M only** |
| Mean-field diversity | $\bar N(t)$ | **Chapter M only**; the bar marks the mean-field substitution as a modelling step |
| Medium concentration and clearance rate | $y(t)$, $\delta$ | **Chapter M only**, coupled schematic §1.2.4.2 |
| Material released per individual at rupture | $c$ | **Chapter M only**, coupled schematic §1.2.4.2 |

Two further conventions were adopted for the merge:

- Chapter M appendix A is titled "Critical behaviour, small populations and
  conditional moments", widened from the original title to cover the limiting
  conditional variance recovered into §1.A.4.
- No symbol $m$ is used for the offspring mean $2p$; the appendix derivations write
  $2p$ out, so that $\mu$ is unambiguously the continuous-time death rate.
