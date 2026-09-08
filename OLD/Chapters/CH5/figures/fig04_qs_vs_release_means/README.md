# fig04 — qs vs release means

Shipped as **Figure 5.4**, `dist:fig:qsmeans`, included from `sections/05_quasi_stationary.tex`.

## Regenerate

```sh
cd figures/fig04_qs_vs_release_means/src && python3 generate.py
```

## Dependencies

`numpy`, `matplotlib`. Style comes from `figures/_style/style_rc.py`, which fixes the palette (#0072B2 blue, #D55E00 vermillion, #009E73 teal, #6B4C9A purple), DejaVu Serif with Computer Modern mathtext, open axes, and unframed legends.

## Provenance

Restyled to the chapter's house standard in the review pass of 2026-08-23; the generator itself predates it except where noted in `meta.json`.
