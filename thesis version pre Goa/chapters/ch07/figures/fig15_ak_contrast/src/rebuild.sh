#!/usr/bin/env bash
# Rebuild fig15 Antal–Krapivsky contrast schematic (PDF + high-res PNG).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

pdflatex -interaction=nonstopmode fig15_ak_contrast.tex
cp -f fig15_ak_contrast.pdf ../fig15.pdf

gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=png16m -r450 \
   -dTextAlphaBits=4 -dGraphicsAlphaBits=4 \
   -sOutputFile=../fig15.png ../fig15.pdf

if command -v sips >/dev/null 2>&1; then
  sips -g pixelWidth -g pixelHeight ../fig15.png
fi

echo "Wrote ../fig15.pdf and ../fig15.png"
