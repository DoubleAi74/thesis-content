# fig_bio_mapping — Intracellular biological reading

Orientation figure for §5 of *Type-specific catastrophe rates in a two-type
branching process: an exact hypergeometric formula*. It places the two-type
birth–death–conversion process with type-specific catastrophe rates inside a
single macrophage-associated compartment, matching the mapping of
`tab:bio-mapping` without privileging any of the four later regimes
(EQ, MAT, GATE, EARLY).

## Contents

| File | Description |
|---|---|
| `fig_bio_mapping.png` | Primary raster (~4310 × 2980 px at 670 dpi). White background. |
| `fig_bio_mapping.pdf` | Vector schematic (pdfLaTeX + TikZ). Preferred for typesetting. |
| `fig_bio_mapping.svg` | Vector SVG (latex + dvisvgm with Ghostscript). Optional. |
| `caption.md` | Journal-style caption in the paper's voice. |
| `src/fig_bio_mapping.tex` | Full TikZ source (self-contained `standalone` document). |
| `src/build.sh` | One-command rebuild script. |
| `meta.json` | Machine-readable metadata (tool, palette, notation source). |

## Regenerate

```bash
cd src
bash build.sh          # writes ../fig_bio_mapping.{pdf,png,svg}
```

To change the raster resolution:

```bash
DPI=900 bash build.sh
```

## Dependencies

- TeX Live (tested with 2024) — `standalone`, `tikz` (libraries
  `arrows.meta`, `positioning`, `calc`, `backgrounds`, `fit`), `amsmath`,
  `amssymb`, `mathtools`, `lmodern`, `xcolor`.
- Ghostscript (tested with 10.05) for PDF → PNG and for dvisvgm PS specials.
- `dvisvgm` (optional) for SVG; requires `libgs` (Homebrew Ghostscript).

No Python, no seed, no numerical simulation: the figure is purely symbolic.
Notation follows `sections/07_biological_application.tex` and
`sections/02_model.tex`. Rates shown:
$\lambda_1,\mu_1,\nu,\lambda_2,\mu_2,\delta_1,\delta_2$, and absorbing time
$\tau_c$.

## Design notes

- **Colour rule:** type-1 events blue (`#0072B2`), type-2 events vermillion
  (`#D55E00`), shared containment-failure sink soft red (`#9A2820`) — same
  palette as `fig01_process_schematic`.
- Type-2 rods carry a soft halo and sparse surface marks only as a schematic
  cue of the later temperature-conditioned phenotype; they are **not** labelled
  as T3SS, F1, or capsule, and are not drawn as the engine of release.
- Both $\delta_1$ and $\delta_2$ feed a single junction for $\tau_c$, so the
  figure remains compatible with EQ, MAT, GATE, and EARLY.
- Extracellular aftermath is pale and explicitly tagged “outside this model”.
