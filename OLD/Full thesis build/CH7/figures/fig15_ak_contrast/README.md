# Figure 15 — Antal–Krapivsky observable contrast

Conceptual process comparison between Antal–Krapivsky and this paper.

## Deliverables

| File | Description |
|---|---|
| `fig15.png` | Primary raster export (≥2400 px wide) |
| `fig15.pdf` | Vector PDF (preferred for journal) |
| `src/fig15_ak_contrast.tex` | TikZ source |
| `caption.md` | Paper-style caption |
| `README.md` | This file |
| `meta.json` | Machine-readable metadata |

## Regenerate

```bash
cd figures/fig15_ak_contrast/src
bash rebuild.sh
```

Or manually:

```bash
cd figures/fig15_ak_contrast/src
pdflatex -interaction=nonstopmode fig15_ak_contrast.tex
cp fig15_ak_contrast.pdf ../fig15.pdf

gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=png16m -r450 \
   -dTextAlphaBits=4 -dGraphicsAlphaBits=4 \
   -sOutputFile=../fig15.png ../fig15.pdf
```

### Dependencies

- TeX Live with `pdflatex`, `tikz`, `amsmath`, `standalone`
- Ghostscript (`gs`) for PNG export

### Optional cleanup

```bash
rm -f src/fig15_ak_contrast.{aux,log}
```

## Design notes

- Palette: type 1 `#0072B2`, type 2 `#D55E00`, catastrophe `#9a2820`, ink `#1a1c1f`.
- Side-by-side contrast: Antal–Krapivsky count process vs this paper’s catastrophe-survival process.
- Pure vector TikZ — AI image generation reserved slot **not** used (structure and labels are text-exact).

## Panel description

1. **Left (AK).** Type 1 and Type 2 count states with one-way conversion.
2. **Right (this paper).** The two-type process with a catastrophe sink.
