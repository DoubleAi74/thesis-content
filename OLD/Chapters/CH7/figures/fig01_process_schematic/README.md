# fig01 — Process & global-catastrophe schematic

Orientation figure for §1–2 of *Type-specific catastrophe hazards in a two-type
branching process: an exact hypergeometric formula*. It shows the two-type
birth–death–conversion process and the single global absorbing catastrophe
entered at total rate $\delta_1 x + \delta_2 y$, contrasting local
per-individual events with the one shared absorbing outcome.

## Contents

| File | Description |
|---|---|
| `fig01.png` | Primary raster, 3649 × 2878 px (Ghostscript, 670 dpi). White background. |
| `fig01.pdf` | Vector schematic (pdfLaTeX + TikZ). Preferred for typesetting. |
| `caption.md` | Journal-style caption in the paper's voice. |
| `src/fig01.tex` | Full TikZ source (self-contained `standalone` document). |
| `src/build.sh` | One-command rebuild script. |
| `meta.json` | Machine-readable metadata (tool, palette, notation source). |

## Regenerate

From a clean shell, with TeX Live (providing `pdflatex` + TikZ) and Ghostscript
(`gs`) on the `PATH`:

```bash
cd src
bash build.sh          # writes ../fig01.pdf and ../fig01.png
```

To change the raster resolution, set `DPI`:

```bash
DPI=900 bash build.sh  # larger PNG
```

Or build by hand:

```bash
cd src
pdflatex fig01.tex
gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r670 \
   -dTextAlphaBits=4 -dGraphicsAlphaBits=4 \
   -sOutputFile=../fig01.png fig01.pdf
```

## Dependencies

- TeX Live (tested with 2024) — `standalone`, `tikz` (libraries
  `arrows.meta`, `positioning`, `calc`, `backgrounds`, `fit`), `amsmath`,
  `amssymb`, `mathtools`, `lmodern`, `xcolor`.
- Ghostscript (tested with 10.05) for PDF → PNG.

No Python, no seed, no numerical simulation: the figure is purely symbolic and
label-driven. Notation is taken verbatim from `sections/02_model.tex`
(Definition 2.1 and Eq. (1)); the seven per-event rates shown are
$\lambda_1,\mu_1,\nu,\lambda_2,\mu_2,\delta_1,\delta_2$.

## Design notes

- **Colour rule:** an arrow's colour is the type whose per-capita rate drives
  the event (type-1 events blue, type-2 events vermillion). This makes the two
  catastrophe contributions $\delta_1,\delta_2$ read as separate, colour-coded
  routes into the same sink.
- Ordinary death sends an individual to $\varnothing$ ($-1$), whereas
  catastrophe absorbs the whole process to $(\mathsf R,\mathsf R)$.
- Palette and typography follow `Prompts/SHARED_CONVENTIONS.md`.
