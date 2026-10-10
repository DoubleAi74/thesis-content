#!/usr/bin/env bash
# ---------------------------------------------------------------------
# Rebuild fig_bio_intracellular_map — biological reading of the two-type
# model (companion to Table 1 of sections/07_biological_application.tex).
#
# Requirements:
#   * pdflatex (TeX Live) with the TikZ/PGF bundle  -> vector PDF
#   * Ghostscript (gs)                              -> raster PNG
#   * dvisvgm (TeX Live)                            -> vector SVG
#
# Usage:  bash build.sh
# Writes: ../fig_bio_intracellular_map.pdf  (vector, for \includegraphics)
#         ../fig_bio_intracellular_map.png  (~3600 px wide)
#         ../fig_bio_intracellular_map.svg  (vector, web/editing)
# ---------------------------------------------------------------------
set -euo pipefail
cd "$(dirname "$0")"

STEM="fig_bio_intracellular_map"
DPI="${DPI:-500}"   # 500 dpi -> ~3600 px wide (full-width journal quality)

# 1. Compile the standalone TikZ figure -> tight-cropped vector PDF.
pdflatex -interaction=nonstopmode -halt-on-error "${STEM}.tex"

# 2. Publish the vector PDF to the figure root.
cp "${STEM}.pdf" "../${STEM}.pdf"

# 3. Rasterise an opaque (white-background) PNG.
gs -q -dBATCH -dNOPAUSE -sDEVICE=png16m -r"$DPI" \
   -dTextAlphaBits=4 -dGraphicsAlphaBits=4 \
   -sOutputFile="../${STEM}.png" "${STEM}.pdf"

# 4. Vector SVG, via the DVI route (dvisvgm cannot read PDFs produced for
#    Ghostscript >= 10.01 without mutool, but reads DVI + PS specials fine).
#    Text is converted to paths so the file is self-contained.
#    LIBGS lets dvisvgm find a Homebrew/manual Ghostscript build.
if [ -z "${LIBGS:-}" ]; then
  for cand in /opt/homebrew/lib/libgs.dylib /usr/local/lib/libgs.dylib \
              /usr/lib/libgs.so /usr/lib/x86_64-linux-gnu/libgs.so; do
    [ -e "$cand" ] && { export LIBGS="$cand"; break; }
  done
fi
latex -interaction=nonstopmode -halt-on-error "${STEM}.tex" >/dev/null
dvisvgm --no-fonts --exact-bbox --output="../${STEM}.svg" "${STEM}.dvi"

# 5. Tidy LaTeX build artefacts (keep src/ source-only).
rm -f "${STEM}.aux" "${STEM}.log" "${STEM}.pdf" "${STEM}.dvi"

echo "Wrote ../${STEM}.pdf, ../${STEM}.png (${DPI} dpi) and ../${STEM}.svg"
