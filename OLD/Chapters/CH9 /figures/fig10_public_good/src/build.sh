#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
DPI="${DPI:-400}"
pdflatex -interaction=nonstopmode -halt-on-error fig10.tex >/dev/null
cp fig10.pdf ../fig10.pdf
gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r"$DPI" \
   -dTextAlphaBits=4 -dGraphicsAlphaBits=4 \
   -sOutputFile=../fig10.png fig10.pdf
rm -f fig10.aux fig10.log fig10.pdf
echo "Wrote ../fig10.pdf and ../fig10.png"
