# fig01 — joint process

Shipped as **Figure 5.1**, `dist:fig:joint`, included from `sections/02_recap.tex`.

## Regenerate

```sh
cd figures/fig01_joint_process/src && latexmk -pdf fig01.tex && cp fig01.pdf ../
```

## Dependencies

A LaTeX installation with TikZ. Styles come from `figures/_style/tikz_style.tex`, which matches the palette of `style_rc.py`.

## Provenance

Restyled to the chapter's house standard in the review pass of 2026-08-23; the generator itself predates it except where noted in `meta.json`.
