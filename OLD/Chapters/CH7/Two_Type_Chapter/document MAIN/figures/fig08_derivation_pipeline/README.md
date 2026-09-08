# fig08 — Derivation pipeline (roadmap of the Section 4 solution)

A serpentine flowchart that gives multi-field readers the *logic* of the exact
solution before the algebra. Eight large stages carry the two coupled backward
equations to the boxed closed form for the finite-time no-catastrophe
probability $S(t)$. One vermillion stage marks the type-2 input (Section 3);
the seven blue stages are the type-1 reduction (Section 4); the final stage —
the exact result of the main theorem — is highlighted.

## The eight stages

| # | Stage | Key object |
|---|---|---|
| 1 | Autonomous type-2 solve *(input)* | $\widehat G\to r_{2,-}$; $z_2=z_{2,0}e^{\hat q_2\hat t}$ |
| 2 | Substitute into type 1 | non-autonomous Riccati for $\widehat S$ |
| 3 | Shift by long-time root | $\widehat S=X+h$, lower root $h$ |
| 4 | Linearise | $X=-Z'/Z$ → linear ODE for $Z$ |
| 5 | Change of variable | $\hat t\to z_2$, $Z=\Phi(z_2)$ |
| 6 | Gauss equation | ${}_2F_1$ basis $U,V$; params $A,B,C$ |
| 7 | Initial condition | Wronskian coefficients $K_U,K_V$ |
| 8 | Exact $S(t)$ *(output)* | $\widehat S=h-\hat q_2 z_2\,(K_UU'+K_VV')/(K_UU+K_VV)$ |

## Contents

| File | Description |
|---|---|
| `fig08.png` | Primary raster, 4603 × 3032 px (Ghostscript, 600 dpi). White background. |
| `fig08.pdf` | Vector schematic (pdfLaTeX + TikZ). Preferred for typesetting. |
| `caption.md` | Journal-style caption in the paper's voice. |
| `src/fig08.tex` | Full TikZ source (self-contained `standalone` document). |
| `src/build.sh` | One-command rebuild script. |
| `meta.json` | Machine-readable metadata (tool, palette, notation source). |

## Regenerate

From a clean shell, with TeX Live (providing `pdflatex` + TikZ) and Ghostscript
(`gs`) on the `PATH`:

```bash
cd src
bash build.sh          # writes ../fig08.pdf and ../fig08.png
```

To change the raster resolution, set `DPI`:

```bash
DPI=900 bash build.sh  # larger PNG
```

Or build by hand:

```bash
cd src
pdflatex fig08.tex
gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r600 \
   -dTextAlphaBits=4 -dGraphicsAlphaBits=4 \
   -sOutputFile=../fig08.png fig08.pdf
```

## Dependencies

- TeX Live (tested with 2024) — `standalone`, `tikz` (libraries
  `arrows.meta`, `positioning`, `calc`, `backgrounds`, `fit`), `amsmath`,
  `amssymb`, `mathtools`, `lmodern`, `xcolor`.
- Ghostscript (tested with 10.05) for PDF → PNG.

No Python, no seed, no numerical simulation: the figure is a purely symbolic,
label-driven roadmap. Notation is taken from `sections/03_autonomous.tex` and
`sections/04_main_result.tex`; the numbered stages mirror the introduction's
derivation bullet list (`sections/01_introduction.tex`).

## Design notes

- **Serpentine layout:** the top row reads left→right (stages 1–4), turns down
  on the right, and the bottom row reads right→left (stages 5–8). This keeps all
  arrows short and directional — no long backward jumps — and ends the flow at
  the highlighted output box on the lower left.
- **Colour rule:** vermillion is reserved for the single external input (the
  autonomous type-2 solve of Section 3); the type-1 reduction of Section 4 is
  uniformly blue; the exact-result stage is emphasised with a green halo, a
  heavier frame, an inner boxed formula (echoing the boxed equation in the
  paper), and a "Thm" ribbon.
- **Short phrases + key symbols:** transformation stages show only the operation
  and the object it produces; the single full equation is the boxed final
  result. This follows the figure brief ("not full equations in 8-point type").
- Palette and typography follow `Prompts/SHARED_CONVENTIONS.md`.
