#!/usr/bin/env python3
"""Reproduce the survival-amplitude table and conditional-mean plot data."""

from __future__ import annotations

import csv
from decimal import Decimal, getcontext
from pathlib import Path


getcontext().prec = 60
HERE = Path(__file__).resolve().parent
FIGURES = HERE.parent / "figures"


def amplitude_bracket(p_text: str, rel_tol: Decimal = Decimal("1e-14")):
    """Return a certified product bracket for A(p).

    After factors 0,...,n have been included, the remaining product is bounded
    below by 1-sum_{k>n} w_k and w_{k+1} <= r w_k.
    """
    p = Decimal(p_text)
    r = Decimal(2) * p
    if not Decimal(0) < r < Decimal(1):
        raise ValueError("p must lie in (0, 1/2)")
    w = Decimal("0.5")
    product = Decimal(1)
    factors = 0
    while True:
        product *= Decimal(1) - w
        factors += 1
        w = r * w * (Decimal(1) - w)
        tail_sum = w / (Decimal(1) - r)
        if tail_sum < rel_tol:
            lower = product * (Decimal(1) - tail_sum)
            upper = product
            return lower, upper, (lower + upper) / Decimal(2), factors


def write_conditional_means(path: Path) -> None:
    ps = [0.30, 0.40, 0.45, 0.48, 0.49]
    labels = ["p030", "p040", "p045", "p048", "p049"]
    states = {label: (1.0, 1.0) for label in labels}  # (S_n, r^n)
    rows = []
    for n in range(251):
        row = {"n": n}
        for p, label in zip(ps, labels):
            survival, mean = states[label]
            row[label] = mean / survival
            r = 2.0 * p
            states[label] = (
                p * survival * (2.0 - survival),
                mean * r,
            )
        rows.append(row)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["n", *labels])
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    write_conditional_means(FIGURES / "conditional_means.csv")

    values = [
        "0.05", "0.10", "0.20", "0.30", "0.40",
        "0.45", "0.48", "0.49", "0.499", "0.4999",
    ]
    print("p,lower,upper,midpoint,1/A,factors")
    for p_text in values:
        lower, upper, midpoint, factors = amplitude_bracket(p_text)
        reciprocal = Decimal(1) / midpoint
        print(
            f"{p_text},{lower:.12g},{upper:.12g},"
            f"{midpoint:.12g},{reciprocal:.12g},{factors}"
        )

    # Values used in the labelled near-critical diagnostic.
    print("near-critical epsilon,A/(2 epsilon)")
    for eps_text in ["2e-2", "2e-3", "2e-4", "2e-5", "2e-6"]:
        eps = Decimal(eps_text)
        p = (Decimal(1) - eps) / Decimal(2)
        _, _, midpoint, _ = amplitude_bracket(str(p), Decimal("1e-13"))
        print(f"{eps},{midpoint/(Decimal(2)*eps):.10f}")


if __name__ == "__main__":
    main()

