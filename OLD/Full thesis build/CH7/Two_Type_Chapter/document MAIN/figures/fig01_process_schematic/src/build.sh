#!/usr/bin/env bash
# ---------------------------------------------------------------------
# Rebuild fig01 — process & global-catastrophe schematic.
#
# Requirements:
#   * pdflatex (TeX Live) with the TikZ/PGF bundle   -> vector fig01.pdf
#   * Ghostscript (gs)                               -> raster fig01.png
#
# Usage:  bash build.sh
# Writes: ../fig01.pdf  (vector)  and  ../fig01.png  (~3650 px wide)
# ---------------------------------------------------------------------
set -euo pipefail
cd "$(dirname "$0")"

DPI="${DPI:-670}"   # 670 dpi -> ~3650 px wide (full-width journal quality)

pdflatex -interaction=nonstopmode -halt-on-error fig01.tex

cp fig01.pdf ../fig01.pdf

gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r"$DPI" \
   -dTextAlphaBits=4 -dGraphicsAlphaBits=4 \
   -sOutputFile=../fig01.png fig01.pdf

# tidy LaTeX by-products (keep src/ source-only; deliverables live in ../)
rm -f fig01.aux fig01.log fig01.pdf

echo "Wrote ../fig01.pdf and ../fig01.png at ${DPI} dpi"
