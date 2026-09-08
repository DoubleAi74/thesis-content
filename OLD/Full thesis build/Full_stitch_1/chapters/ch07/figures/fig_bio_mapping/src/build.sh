#!/usr/bin/env bash
# ---------------------------------------------------------------------
# Rebuild fig_bio_mapping — biological reading of the intracellular model.
#
# Requirements:
#   * pdflatex (TeX Live) with the TikZ/PGF bundle   -> vector PDF
#   * Ghostscript (gs)                               -> raster PNG
#   * latex + dvisvgm + libgs (optional)              -> SVG
#
# Usage:  bash build.sh
# Writes: ../fig_bio_mapping.pdf  ../fig_bio_mapping.png  [../fig_bio_mapping.svg]
# ---------------------------------------------------------------------
set -euo pipefail
cd "$(dirname "$0")"

DPI="${DPI:-670}"   # full-width journal quality
export PATH="/opt/homebrew/bin:/usr/local/bin:${PATH:-}"

pdflatex -interaction=nonstopmode -halt-on-error fig_bio_mapping.tex
cp fig_bio_mapping.pdf ../fig_bio_mapping.pdf

gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r"$DPI" \
   -dTextAlphaBits=4 -dGraphicsAlphaBits=4 \
   -sOutputFile=../fig_bio_mapping.png fig_bio_mapping.pdf

# SVG via DVI route (PGF writes PS specials; dvisvgm needs libgs)
if command -v latex >/dev/null 2>&1 && command -v dvisvgm >/dev/null 2>&1; then
  latex -interaction=nonstopmode -halt-on-error fig_bio_mapping.tex >/dev/null
  LIBGS=""
  for cand in \
      /opt/homebrew/lib/libgs.dylib \
      /usr/local/lib/libgs.dylib \
      /opt/homebrew/lib/libgs.10.dylib; do
    if [[ -f "$cand" ]]; then LIBGS="$cand"; break; fi
  done
  if [[ -n "$LIBGS" ]]; then
    dvisvgm -n --exact --libgs="$LIBGS" -o ../fig_bio_mapping.svg fig_bio_mapping.dvi \
      && echo "Wrote ../fig_bio_mapping.svg" \
      || echo "Warning: SVG export failed (continuing with PDF/PNG)"
  else
    echo "Warning: libgs not found; skipping SVG"
  fi
  rm -f fig_bio_mapping.dvi
fi

rm -f fig_bio_mapping.aux fig_bio_mapping.log fig_bio_mapping.pdf

echo "Wrote ../fig_bio_mapping.pdf and ../fig_bio_mapping.png at ${DPI} dpi"
