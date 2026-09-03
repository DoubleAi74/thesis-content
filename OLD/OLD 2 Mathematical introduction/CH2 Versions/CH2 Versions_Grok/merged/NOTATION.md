# Notation freeze (pass-1 merge)

| Object | Symbol |
|---|---|
| Discrete population | \(Z_n\) |
| Survival probability | \(S_n\) |
| Kolmogorov constant | \(A(p)\) |
| Continuous analogue | \(A_{\mathrm{c}}(p)\) (macro `\Ac`) |
| Near-critical gap | \(\varepsilon = 1-2p\) |
| Logistic multiplier | \(r = 2p\) |
| Koenigs function | \(\psi_r\) |

## Label prefixes

- Chapter M: `m:` e.g. `\label{m:sec:gw}`, `\label{m:eq:SnIter}`
- Chapter A: `a:` e.g. `\label{a:prop:series}`, `\label{a:thm:ht}`

## Cross-chapter macros

In each preamble:

- `\ChM` → `Chapter~[Mathematical introduction]`
- `\ChA` → `Chapter~[The constant \(A(p)\)]`

Thesis integration will replace these with numbered chapter refs.
