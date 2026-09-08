#!/usr/bin/env bash
# ---------------------------------------------------------------------
# Rebuild fig08 — derivation pipeline (roadmap of the Section 4 solution).
#
# Requirements:
#   * pdflatex (TeX Live) with the TikZ/PGF bundle   -> vector fig08.pdf
#   * Ghostscript (gs)                               -> raster fig08.png
#
# Usage:  bash build.sh
# Writes: ../fig08.pdf  (vector)  and  ../fig08.png  (~3800 px wide)
# ---------------------------------------------------------------------
set -euo pipefail
cd "$(dirname "$0")"

DPI="${DPI:-600}"   # 600 dpi -> ~3800 px wide (full-width journal quality)

pdflatex -interaction=nonstopmode -halt-on-error fig08.tex

cp fig08.pdf ../fig08.pdf

gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r"$DPI" \
   -dTextAlphaBits=4 -dGraphicsAlphaBits=4 \
   -sOutputFile=../fig08.png fig08.pdf

# tidy LaTeX by-products (keep src/ source-only; deliverables live in ../)
rm -f fig08.aux fig08.log fig08.pdf

echo "Wrote ../fig08.pdf and ../fig08.png at ${DPI} dpi"
