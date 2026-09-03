# Notation and label freeze (Pass 1 merge)

Frozen 2026-08-07. Both chapters must respect this freeze. Source: MERGE_MAP_TWO_CHAPTERS.md §6, IMPLEMENTATION_PLAN_TWO_CHAPTERS.md §4.

## Symbols

| Object | Symbol | Notes |
|---|---|---|
| Discrete population | $Z_n$ | binary Galton–Watson, $Z_0=1$ unless stated |
| Offspring law | $L$, $\Pr(L=2)=p$, $\Pr(L=0)=1-p$ | mean $2p$ |
| Offspring PGF | $\phi(z)=pz^2+(1-p)$ | |
| Extinction by generation $n$ | $u_n$ | $u_{n+1}=\phi(u_n)$, $u_0=0$ |
| Survival probability | $S_n=1-u_n=\Pr(Z_n>0)$ | $S_{n+1}=2pS_n-pS_n^2$, $S_0=1$ |
| Kolmogorov constant | $A(p)=\lim_{n\to\infty}S_n/(2p)^n$ | $p\in[0,\tfrac12)$; endpoint convention $A(0):=\tfrac12$ (continuous extension) |
| Continuous analogue | $A_{\mathrm{c}}(p)=\dfrac{1-2p}{1-p}$ | macro `\Ac`; **use this form everywhere** |
| Near-critical gap | $\varepsilon=1-2p$ | not overloaded with $r$ |
| Logistic multiplier | $r=2p$ | logistic map $w\mapsto rw(1-w)$, $S_n=2w_n$ |
| Koenigs function | $\psi_r$ | normalised $\psi_r(0)=0$, $\psi_r'(0)=1$; basin extension $\Psi_r$ where needed |
| Quasi-stationary mean | $1/A(p)$ (discrete), $1/\Ac(p)$ (continuous) | |
| Catastrophe probability (discrete) | $\kappa$ | per individual per step |
| CT BDC rates | $\lambda$ (birth), $\mu$ (death), $\rho$ (per-capita catastrophe) | as in Definition of M |
| Absorption models | $\alpha$ (absorption), $\lambda$ (interior birth), $\mu$ (interior death) | counts $X_t$ interior, $Y_t$ exterior |

## Label prefixes

- Chapter M: `m:` — e.g. `\label{m:sec:gw}`, `\label{m:eq:SnIter}`.
- Chapter A: `a:` — e.g. `\label{a:prop:series}`, `\label{a:thm:ht}`.
- No bare labels; no label reused across chapters.

## Cross-chapter references (standalone builds)

- Standalone builds are numbered for the expected thesis order: M = Chapter 2,
  A = Chapter 3 (`\setcounter{chapter}` in each `main.tex`).
- In M: `\ChA` expands to `Chapter 3 (The constant A(p))`.
- In A: `\ChM` expands to `Chapter 2 (Mathematical introduction)`.
- Thesis integration will redefine these macros to numbered `\ref` targets.

## Heading conventions

- Use “the constant $A(p)$” (claude_1) in headings; “amplitude” may appear at most once as a synonym per chapter.
