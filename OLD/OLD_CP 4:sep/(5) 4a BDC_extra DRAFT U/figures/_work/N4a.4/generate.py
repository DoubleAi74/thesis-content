#!/usr/bin/env python3
"""Generate N4a.4: the three distinct means called 'burst size'."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(
    0,
    "/Users/adamaldridge/Desktop/Thesis content 🎓 /4 BDC additional and BMVR/"
    "Figures run/style",
)
import style_rc  # noqa: E402

style_rc.apply()

import matplotlib.pyplot as plt  # noqa: E402


LAMBDA = 1.0
MU = 0.2
DELTA = 0.05
WORKDIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORKDIR.parents[2]
PDF_PATH = CHAPTER_DIR / "figures" / "N4a_4_three_burst_means.pdf"
PNG_PATH = WORKDIR / "preview.png"


def roots() -> tuple[float, float]:
    eta = (LAMBDA + MU + DELTA) / (2.0 * LAMBDA)
    discriminant = eta**2 - MU / LAMBDA
    assert discriminant > 0.0
    return eta + math.sqrt(discriminant), eta - math.sqrt(discriminant)


def three_means() -> tuple[float, float, float, float]:
    a, b = roots()
    unconditional = a * (1.0 - b) / (a - 1.0)
    conditional = a / (a - 1.0)
    late_size_biased = (a + 1.0) / (a - 1.0)
    return unconditional, conditional, late_size_biased, b


def run_asserts() -> dict[str, float]:
    unconditional, conditional, late_size_biased, b = three_means()
    expected = (13.985699678629192, 17.23212459828649, 33.46424919657298)
    actual = (unconditional, conditional, late_size_biased)
    assert np.allclose(actual, expected, rtol=0.0, atol=1e-12)
    assert unconditional < conditional < late_size_biased
    assert abs(conditional - unconditional / (1.0 - b)) < 1e-12
    return {
        "unconditional": unconditional,
        "conditional": conditional,
        "late": late_size_biased,
        "b": b,
    }


def make_figure() -> None:
    checked = run_asserts()
    values = np.array(
        [checked["unconditional"], checked["conditional"], checked["late"]]
    )
    positions = np.array([0.0, 1.45, 2.90])
    colours = ("tab:blue", "tab:orange", "#6b4c9a")
    labels = (
        "All cells\n" + r"$V_\infty$",
        "Cells that burst\n" + r"$V_\infty/(1-b)$",
        "Very late bursts\n" + r"$(a+1)/(a-1)$",
    )

    fig, ax = plt.subplots(figsize=(7.6, 4.65))
    bars = ax.bar(
        positions,
        values,
        width=0.86,
        color=colours,
        alpha=0.78,
        edgecolor=colours,
        linewidth=1.0,
        zorder=3,
    )
    ax.bar_label(
        bars,
        labels=[f"{value:.2f}" for value in values],
        padding=4,
        fontsize=10,
        fontweight="bold",
    )

    ax.annotate(
        "",
        xy=(1.12, 38.0),
        xytext=(0.33, 38.0),
        arrowprops={"arrowstyle": "->", "color": "#444444", "linewidth": 0.9},
    )
    ax.text(
        0.725,
        38.6,
        rf"remove no-burst mass $b={checked['b']:.3f}$",
        ha="center",
        va="bottom",
        fontsize=9,
        color="#444444",
    )
    ax.annotate(
        "",
        xy=(2.57, 41.0),
        xytext=(1.78, 41.0),
        arrowprops={"arrowstyle": "->", "color": "#444444", "linewidth": 0.9},
    )
    ax.text(
        2.175,
        41.6,
        "condition on very late bursts",
        ha="center",
        va="bottom",
        fontsize=9,
        color="#444444",
    )

    ax.text(
        0.02,
        0.96,
        r"$(\lambda,\mu,\delta)=(1,0.2,0.05)$",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
    )
    ax.set_xlim(-0.70, 3.60)
    ax.set_ylim(0.0, 45.0)
    ax.set_xticks(positions, labels)
    ax.set_ylabel("mean released particles")
    ax.set_title(
        "Conditioning changes which burst-size mean is being taken",
        loc="left",
        fontweight="bold",
    )
    ax.grid(axis="x", visible=False)

    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)


if __name__ == "__main__":
    results = run_asserts()
    make_figure()
    print(
        "asserts: pass; means="
        f"{results['unconditional']:.12f}, "
        f"{results['conditional']:.12f}, {results['late']:.12f}"
    )
    print(f"wrote {PDF_PATH} and {PNG_PATH}")
