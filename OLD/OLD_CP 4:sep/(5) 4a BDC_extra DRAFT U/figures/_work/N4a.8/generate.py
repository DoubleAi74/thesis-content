#!/usr/bin/env python3
"""Generate N4a.8: yield sub-extensivity with founding multiplicity."""

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
PDF_PATH = CHAPTER_DIR / "figures" / "N4a_8_yield_subextensive.pdf"
PNG_PATH = WORKDIR / "preview.png"


def roots() -> tuple[float, float]:
    eta = (LAMBDA + MU + DELTA) / (2.0 * LAMBDA)
    discriminant = eta**2 - MU / LAMBDA
    assert discriminant > 0.0
    root = math.sqrt(discriminant)
    return eta + root, eta - root


def lifetime_yield(k: int) -> float:
    """Closed expression in Eq. (Vk), including its k=1 specialization."""
    if k < 1:
        raise ValueError("k must be positive")
    a, b = roots()
    first = (1.0 - b**k) + 2.0 * LAMBDA / DELTA * (
        1.0 / (k + 1) - b**k + k * b ** (k + 1) / (k + 1)
    )
    if k == 1:
        return first
    integral = (
        (b ** (k + 1) - 1.0) / (k + 1)
        - (a + b) * (b**k - 1.0) / k
        + a * b * (b ** (k - 1) - 1.0) / (k - 1)
    )
    return first + k * (k - 1) * LAMBDA / DELTA * integral


def run_asserts() -> dict[str, object]:
    a, b = roots()
    v_inf = a * (1.0 - b) / (a - 1.0)
    k = np.arange(1, 9)
    true_yield = np.array([lifetime_yield(int(value)) for value in k])
    naive_yield = k * v_inf
    assert abs(true_yield[0] - v_inf) < 1e-12
    assert abs(true_yield[1] - 17.43) < 0.05
    assert np.all(true_yield[1:] < naive_yield[1:])
    assert np.all(np.diff(true_yield) > 0.0)
    return {
        "k": k,
        "true": true_yield,
        "naive": naive_yield,
        "v_inf": v_inf,
    }


def make_figure() -> None:
    checked = run_asserts()
    k = checked["k"]
    true_yield = checked["true"]
    naive_yield = checked["naive"]

    fig, ax = plt.subplots(figsize=(7.25, 4.55))
    ax.fill_between(
        k,
        true_yield,
        naive_yield,
        color="#6b4c9a",
        alpha=0.10,
        linewidth=0.0,
        zorder=1,
    )
    ax.plot(
        k,
        true_yield,
        color="tab:blue",
        marker="o",
        markersize=6.0,
        markerfacecolor="white",
        markeredgewidth=1.35,
        linewidth=2.35,
        label=r"shared-cell yield $V_\infty^{(k)}$",
        zorder=4,
    )
    ax.plot(
        k,
        naive_yield,
        color="tab:orange",
        linestyle="--",
        marker="^",
        markersize=5.2,
        linewidth=2.1,
        label=r"naive independent-cell line $kV_\infty$",
        zorder=3,
    )

    x_bracket = 2.15
    y_true_2 = float(true_yield[1])
    y_naive_2 = float(naive_yield[1])
    ax.annotate(
        "",
        xy=(x_bracket, y_naive_2),
        xytext=(x_bracket, y_true_2),
        arrowprops={
            "arrowstyle": "<->",
            "color": "#444444",
            "linewidth": 1.0,
            "shrinkA": 1,
            "shrinkB": 1,
        },
        zorder=5,
    )
    ax.text(
        2.28,
        0.5 * (y_true_2 + y_naive_2),
        r"$17.43$ vs $27.97$",
        fontsize=9,
        color="#333333",
        ha="left",
        va="center",
    )
    ax.text(
        5.15,
        59.0,
        "gap from counting one cell\nas if it could rupture repeatedly",
        fontsize=9,
        color="#555555",
        ha="center",
        va="center",
    )
    ax.text(
        0.98,
        0.96,
        r"$\lambda=1$, $\mu=0.2$, $\delta=0.05$",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9,
        color="#222222",
    )

    ax.set_xlim(0.75, 8.25)
    ax.set_ylim(0.0, 118.0)
    ax.set_xticks(k)
    ax.set_xlabel(r"founding multiplicity $k$")
    ax.set_ylabel(r"unconditional mean yield")
    ax.set_title(
        "One shared catastrophe prevents $k$-fold yield scaling",
        loc="left",
        fontweight="bold",
    )
    ax.legend(loc="upper left")

    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)


if __name__ == "__main__":
    checked = run_asserts()
    make_figure()
    print(
        "asserts: pass; V_inf="
        f"{checked['v_inf']:.12f}; V_inf^(2)={checked['true'][1]:.12f}; "
        "sub-extensive for k=2,...,8"
    )
    print(f"wrote {PDF_PATH} and {PNG_PATH}")
