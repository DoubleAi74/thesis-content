# fig02 — three readings

Shipped as **Figure 5.2**, `dist:fig:readings`, included from `sections/04_geometric.tex`.

## Regenerate

```sh
cd figures/fig02_three_readings/src && latexmk -pdf fig02.tex && cp fig02.pdf ../
```

## Dependencies

A LaTeX installation with TikZ. Styles come from `figures/_style/tikz_style.tex`, which matches the palette of `style_rc.py`.

## Provenance

Restyled to the chapter's house standard in the review pass of 2026-08-23; the generator itself predates it except where noted in `meta.json`.
