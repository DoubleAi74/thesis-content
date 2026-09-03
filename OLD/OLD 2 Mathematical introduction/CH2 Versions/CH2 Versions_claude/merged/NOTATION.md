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
