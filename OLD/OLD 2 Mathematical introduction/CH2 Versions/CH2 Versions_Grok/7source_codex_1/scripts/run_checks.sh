#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

python3 "$SCRIPT_DIR/reproduce_numerics.py"
python3 "$SCRIPT_DIR/verify_algebra.py"
python3 "$SCRIPT_DIR/extract_coefficients.py"
python3 "$SCRIPT_DIR/verify_pgf.py"

echo "PASS: all reproducibility checks"
