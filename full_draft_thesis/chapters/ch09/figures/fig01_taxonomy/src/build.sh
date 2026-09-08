#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
DPI="${DPI:-400}"
pdflatex -interaction=nonstopmode -halt-on-error fig01.tex >/dev/null
cp fig01.pdf ../fig01.pdf
gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r"$DPI" \
   -dTextAlphaBits=4 -dGraphicsAlphaBits=4 \
   -sOutputFile=../fig01.png fig01.pdf
rm -f fig01.aux fig01.log fig01.pdf
echo "Wrote ../fig01.pdf and ../fig01.png"
