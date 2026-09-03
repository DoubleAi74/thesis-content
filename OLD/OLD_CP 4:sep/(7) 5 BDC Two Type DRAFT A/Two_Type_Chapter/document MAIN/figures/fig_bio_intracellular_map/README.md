# fig_bio_intracellular_map — biological reading of the two-type model

> **Status: alternate.** `main.tex` currently uses `figures/fig_bio_mapping/`
> for this slot. See [`NOTE_alternate.md`](NOTE_alternate.md) for the
> side-by-side comparison and the two lines needed to swap this one in.

Companion to Table 1 (`tab:bio-mapping`) of §5.1 in *Type-specific catastrophe
rates in a two-type branching process: an exact hypergeometric formula*. It
draws the same mapping the table states in words: the two-type
birth–death–conversion process placed inside one macrophage-associated
intracellular compartment, with both catastrophe channels reaching a single
absorbing event.

Reading order is left to right: uptake → type 1 in a *Yersinia*-containing
vacuole → one-way adaptation at $\nu$ → type 2 → the shared endpoint $\tau_c$
at the break in the host-cell boundary → the pale, out-of-model extracellular
phase.

## Contents

| File | Description |
|---|---|
| `fig_bio_intracellular_map.pdf` | Vector schematic (pdfLaTeX + TikZ). Preferred for typesetting. 514 × 296 pt. |
| `fig_bio_intracellular_map.png` | Primary raster, 3640 × 2154 px (Ghostscript, 500 dpi). White background. |
| `fig_bio_intracellular_map.svg` | Vector SVG (dvisvgm, text as paths). Self-contained. |
| `caption.md` | Journal-style caption in the paper's voice, plus a shorter variant. |
| `NOTE_alternate.md` | Comparison against `fig_bio_mapping` and swap-in instructions. |
| `src/fig_bio_intracellular_map.tex` | Full TikZ source (self-contained `standalone` document). |
| `src/build.sh` | One-command rebuild script. |
| `meta.json` | Machine-readable metadata (tool, palette, caveats, departures). |

## Regenerate

From a clean shell, with TeX Live (providing `pdflatex`, `latex`, `dvisvgm`
and TikZ) and Ghostscript (`gs`) on the `PATH`:

```bash
cd src
bash build.sh          # writes ../*.pdf, ../*.png and ../*.svg
```

To change the raster resolution, set `DPI`:

```bash
DPI=670 bash build.sh  # larger PNG
```

## Dependencies

- TeX Live (tested with 2024) — `standalone`, `tikz` (libraries `arrows.meta`,
  `positioning`, `calc`, `backgrounds`, `fit`, `decorations.pathmorphing`),
  `amsmath`, `amssymb`, `mathtools`, `lmodern`, `xcolor`.
- Ghostscript (tested with 10.05.1) for PDF → PNG.
- dvisvgm (tested with 3.2.2) for SVG.

No Python, no seed, no numerical simulation: the figure is purely symbolic and
label-driven. Notation is taken verbatim from `sections/02_model.tex` and
`tab:bio-mapping`; the biology follows `flow_D.pdf`.

### SVG note

dvisvgm cannot read PDFs produced against Ghostscript ≥ 10.01 without `mutool`,
so `build.sh` takes the DVI route (`latex` → `dvisvgm`) and points `LIBGS` at a
Homebrew or system `libgs`. It probes the usual locations; override by exporting
`LIBGS=/path/to/libgs.dylib` before running.

## Design notes

- **Colour rule.** Rate symbols and event arrows keep the canonical manuscript
  accents (type-1 `#0072B2`, type-2 `#D55E00`, catastrophe `#9A2820`), so an
  arrow's colour is still the type whose per-capita rate drives the event —
  identical to `fig01`. Drawn bacterial bodies use lowered-chroma tints of the
  same two hues so the biology does not read as a state diagram.
- **Greyscale.** Type 1 is deliberately *lighter* than type 2, and type 2 also
  carries a faint halo and sparse surface hairlines, so the two states separate
  by lightness and by texture, not by hue alone. Verified with
  `gs -sDEVICE=pnggray`.
- **Event grammar reused from `fig01`.** A self-loop means birth; an arrow into
  `∅` means ordinary death of one individual; the two `δ` arrows are the only
  routes into the shared absorbing endpoint. A reader who has seen Figure 1
  maps the biology onto the mathematics without the caption.
- **No regime is privileged.** `δ₁` and `δ₂` are drawn at identical line
  weight, both originate from a population region, and both terminate on the
  same marker. The figure is therefore compatible with EQ, MAT, GATE and EARLY
  alike; the in-figure caveat line says so explicitly.
- **Restraint at the endpoint.** Containment failure is a gap in the boundary
  with a marker and a few bacteria drifting out at reduced opacity — not an
  exploding cell. The surface cue on type 2 evokes the temperature-induced
  package without naming or drawing a mechanism.
- **The conversion band** is 48 discrete colour strips rather than a true
  gradient. A PDF/PostScript shading is lost on the DVI → SVG route; strips
  render identically in both outputs. The three transitional rods inside the
  band carry the colour change even in greyscale.
- Palette and typography follow the conventions of `fig01`/`fig05`
  (`lmodern`, `standalone`, `border=6pt`).
