# fig02 — Path-dependent catastrophe exposure

Pedagogical multi-panel figure for the two-type birth–death–conversion model
with a single global catastrophe of hazard \(\lambda(t)=\delta_1X_t+\delta_2Y_t\).
It shows that the no-catastrophe probability is an **occupation-time** functional:
two histories with the *same* start \((1,0)\) and *same* terminal counts \((2,1)\)
accumulate very different type-weighted exposure and hence very different
path-wise survival weights \(\exp\{-\int_0^t\lambda\,\mathrm ds\}\).

## Panels

| Panel | Content |
|---|---|
| (a) | Path A counts \(X_t\) (type 1, blue) and \(Y_t\) (type 2, vermillion): an early boom to six, then die-back. |
| (b) | Path B counts on the same vertical scale: small for a long time, blooms late. Both paths solid-in-own-panel; Path A solid / Path B dashed elsewhere. |
| (c) | Instantaneous hazard \(\lambda(t)=\delta_1X_t+\delta_2Y_t\) for both paths (shaded). Same terminal hazard \(\lambda(10)=0.22\), but areas \(\int_0^{10}\lambda\,\mathrm dt\approx 2.7\) (A) vs \(\approx 1.1\) (B). |
| (d) | Path-wise no-catastrophe weight \(\exp\{-\int_0^t\lambda\,\mathrm ds\}\): terminal \(\approx 0.066\) (A) vs \(\approx 0.32\) (B), a \(\approx 4.9\times\) gap. |

## Regenerate

From a clean shell:

```bash
python3 src/make_fig02.py
```

Writes `fig02.png` (300 dpi, ~3995×2836 px), `fig02.pdf` (vector),
`paths.json`, and `meta.json` into this folder.

### Dependencies

- Python 3 with **numpy** and **matplotlib** (developed with numpy 2.4, matplotlib 3.10).
- Optional: a LaTeX installation (TeX Live) with `dvipng` and `ghostscript`.
  If present, the script uses `text.usetex` for authentic Computer Modern
  typography; the script prepends common TeX Live `bin` directories to `PATH`
  automatically. If LaTeX is unavailable it falls back to matplotlib `mathtext`
  with the `cm` font set (endorsed in `SHARED_CONVENTIONS.md`) — the figure still
  renders, only the typeface differs slightly. The mode used is recorded in
  `meta.json` (`"typography"`).

On this machine the matplotlib-bearing interpreter was `/opt/homebrew/bin/python3`;
substitute whichever `python3` has numpy + matplotlib.

## Parameters and seed

- Hazard weights: `DELTA1 = 0.06`, `DELTA2 = 0.10`; horizon `T = 10.0` (physical time).
  These are set at the top of `src/make_fig02.py`. See `caption.md` for why they
  are scaled down from the model section's worked pair \((0.15,0.25)\).
- **Deterministic — no seed.** The two histories are prescribed integer-valued
  step functions (`PATH_A`, `PATH_B` in the script, mirrored in `paths.json`),
  not stochastic realisations. There is no random-number generator to seed.

## Editing the paths

Each path is a list of `(t, X, Y)` breakpoints; the state is held from time `t`
until the next breakpoint, and the final row is held to `T`. Both paths are
constructed to start at `(1,0)` and end at `(2,1)`. Edit `PATH_A` / `PATH_B` and
re-run; the exposure integrals, weights, ratios, annotations, `paths.json` and
`meta.json` all update automatically from the tables.

## Validation

\(\lambda\) is piecewise constant, so the cumulative exposure
\(\Lambda(t)=\int_0^t\lambda\,\mathrm ds\) is computed in closed form. An
independent trapezoidal quadrature on a grid straddling every jump reproduces it
to a maximum absolute discrepancy of \(1.7\times10^{-8}\)
(`meta.json → validation`).

## Notes

- Palette follows `SHARED_CONVENTIONS.md`: type 1 `#0072B2`, type 2 `#D55E00`,
  ink `#1a1c1f`; the *derived* catastrophe quantities (the combined hazard and
  the survival weight, which belong to neither type) use one permitted muted
  purple `#6B4C9A`, with Path A solid and Path B dashed.
- The prompt reserves an optional AI-generated conceptual inset for this figure.
  It is intentionally **not** used — the figure stands on computational content,
  conserving the project-wide AI-image budget.
