# Figures

One folder per figure, numbered in chapter order, following the project's
shared figure conventions:

```
figNN_slug/
  figNN.pdf      the figure the chapter includes
  figNN.png      raster preview (matplotlib figures only)
  caption.md     the caption as typeset, for reference
  README.md      what it shows, how to regenerate, dependencies
  meta.json      label, generator, style module, outputs
  src/           generate.py (matplotlib) or figNN.tex (TikZ)
```

`_style/` holds the two style modules both kinds share — `style_rc.py` for
matplotlib and `tikz_style.tex` for TikZ — so the palette and typography stay
in step across the set.

## Rebuild everything

```sh
cd figures
for d in fig[0-9][0-9]_*/; do
  nn=$(basename "$d" | cut -c4-5)
  if [ -f "$d/src/generate.py" ]; then
    (cd "$d/src" && python3 generate.py)
  else
    (cd "$d/src" && latexmk -pdf "fig$nn.tex" && cp "fig$nn.pdf" ../ && latexmk -c "fig$nn.tex")
  fi
done
```

Verified: deleting every `figNN.pdf` and running the loop above reproduces all
fifteen, and the chapter then builds unchanged.
