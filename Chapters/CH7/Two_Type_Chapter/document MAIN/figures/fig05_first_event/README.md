# fig05 — First-event contribution map

A clean flow / case diagram illustrating the **first-event derivation** of the
type-1 backward equation (Section 2, "First-event calculation"). For one type-1
individual over a short interval $\Delta t$ it shows the five possible fates
(nothing / birth / death / conversion / catastrophe), the probability of each over
$[0,\Delta t]$, and the no-catastrophe probability each contributes over the residual
horizon $t$. Summing rate $\times$ contribution and taking $\Delta t\downarrow 0$
rebuilds the ODE

$$\dot S=\lambda_1 S^2-(\lambda_1+\mu_1+\nu+\delta_1)S+\mu_1+\nu G.$$

A smaller companion panel repeats the argument for a type-2 individual (no conversion
out of type 2), giving $\dot G=\lambda_2 G^2-(\lambda_2+\mu_2+\delta_2)G+\mu_2$.

## Files

| File | Purpose |
|---|---|
| `fig05.pdf` | Vector figure (primary; tight-cropped `standalone`) |
| `fig05.png` | Opaque 600-dpi raster, 4377 × 3906 px (white background) |
| `caption.md` | Journal-style caption + method notes |
| `meta.json` | Machine-readable metadata |
| `src/fig05.tex` | TikZ source |
| `src/build.sh` | One-shot regeneration script |

## Regenerate

From a clean shell:

```bash
cd src
./build.sh
```

or manually:

```bash
cd src
pdflatex fig05.tex          # -> fig05.pdf (tight-cropped)
cp fig05.pdf ../fig05.pdf
gs -q -dBATCH -dNOPAUSE -sDEVICE=png16m -r600 \
   -dTextAlphaBits=4 -dGraphicsAlphaBits=4 \
   -sOutputFile=../fig05.png fig05.pdf
```

## Dependencies

- **TeX Live** (TikZ; libraries `positioning`, `calc`, `arrows.meta`,
  `shapes.geometric`, `backgrounds`; fonts `lmodern`). Built with TeX Live 2024.
- **Ghostscript** for PDF → PNG (built with `gs` 10.05.1).

No Python, no random seed, no data: the figure is a symbolic schematic and uses the
model rates as symbols only. To place it in the manuscript, prefer `fig05.pdf`
(vector) at full text width.

## Notation

Follows the paper: $S(t)$, $G(t)$; rates $\lambda_i,\mu_i,\nu,\delta_i$; absorbing
catastrophe state $\mathsf R$. Palette from `Prompts/SHARED_CONVENTIONS.md`
(type 1 `#0072B2`, type 2 `#D55E00`, catastrophe/error `#9a2820`).
