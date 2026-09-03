#!/usr/bin/env bash
# Regenerate fig05 — first-event contribution map.
# Requires: pdflatex (TeX Live, with TikZ) and Ghostscript (gs).
set -euo pipefail
cd "$(dirname "$0")"

# 1. Compile the standalone TikZ figure -> tight-cropped vector PDF.
pdflatex -interaction=nonstopmode -halt-on-error fig05.tex

# 2. Publish the vector PDF to the figure root.
cp fig05.pdf ../fig05.pdf

# 3. Rasterise an opaque (white-background) PNG at 600 dpi
#    (~4380 px wide -> comfortably above the 3600 px full-width target).
gs -q -dBATCH -dNOPAUSE -sDEVICE=png16m -r600 \
   -dTextAlphaBits=4 -dGraphicsAlphaBits=4 \
   -sOutputFile=../fig05.png fig05.pdf

# 4. Tidy LaTeX build artefacts.
rm -f fig05.aux fig05.log

echo "Wrote ../fig05.pdf and ../fig05.png"
