#!/usr/bin/env python3
"""Generate N3.4: the characteristic quadratic and its two roots."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(
    0,
    "/Users/adamaldridge/Desktop/Thesis content 🎓 /4 BDC additional and BMVR/Figures run/style",
)
import style_rc  # noqa: E402

style_rc.apply()

import matplotlib.pyplot as plt  # noqa: E402


HERE = Path(__file__).resolve().parent
CHAPTER = HERE.parents[2]
PDF_PATH = CHAPTER / "figures" / "N3_4_quadratic_roots.pdf"
PNG_PATH = HERE / "preview.png"

LAMBDA = 1.0
MU = 0.2
DELTA = 0.05


def roots(lam: float, mu: float, delta: float) -> tuple[float, float]:
    eta = (lam + mu + delta) / (2.0 * lam)
    spread = np.sqrt(eta**2 - mu / lam)
    return float(eta + spread), float(eta - spread)


def validate(a: float, b: float) -> None:
    assert abs(a * b - MU / LAMBDA) < 1e-10
    assert abs(a + b - (LAMBDA + MU + DELTA) / LAMBDA) < 1e-10
    assert b < 1.0 < a
    assert np.isclose((a - 1.0) * (1.0 - b), DELTA / LAMBDA, atol=1e-12)


def build() -> tuple[float, float]:
    a, b = roots(LAMBDA, MU, DELTA)
    validate(a, b)
    A, B = a - 1.0, 1.0 - b

    f = np.linspace(-0.02, 1.24, 1600)
    q = LAMBDA * f**2 - (LAMBDA + MU + DELTA) * f + MU

    fig, ax = plt.subplots(figsize=(8.25, 4.95))
    ax.axvspan(0.0, 1.0, color="#1f77b4", alpha=0.07, zorder=0)
    ax.axhline(0.0, color="#242424", linewidth=1.0, zorder=1)
    ax.axvline(1.0, color="#888888", linestyle="--", linewidth=1.2, zorder=1)
    ax.plot(f, q, color="#e05a00", linewidth=2.6, zorder=3)

    ax.plot(
        b,
        0.0,
        marker="o",
        markersize=9,
        markerfacecolor="#1f77b4",
        markeredgecolor="white",
        markeredgewidth=1.5,
        zorder=5,
    )
    ax.plot(
        a,
        0.0,
        marker="o",
        markersize=9,
        markerfacecolor="white",
        markeredgecolor="#e05a00",
        markeredgewidth=2.2,
        zorder=5,
    )
    ax.plot(1.0, -DELTA, marker="x", color="#555555", markersize=7, markeredgewidth=1.5, zorder=5)

    ax.annotate(
        rf"stable root  $b={b:.3f}$",
        xy=(b, 0.0),
        xytext=(0.055, 0.095),
        arrowprops=dict(arrowstyle="->", color="#1f77b4", linewidth=1.1),
        color="#175886",
        ha="left",
    )
    ax.annotate(
        rf"unstable root  $a={a:.3f}$",
        xy=(a, 0.0),
        xytext=(1.205, 0.105),
        arrowprops=dict(arrowstyle="->", color="#e05a00", linewidth=1.1),
        color="#b84900",
        ha="right",
    )
    ax.annotate(
        r"$q(1)=-\delta=-0.050$",
        xy=(1.0, -DELTA),
        xytext=(0.82, -0.105),
        arrowprops=dict(arrowstyle="->", color="#666666", linewidth=1.0),
        color="#555555",
        ha="center",
    )

    distance_y = -0.245
    ax.annotate(
        "",
        xy=(1.0, distance_y),
        xytext=(b, distance_y),
        arrowprops=dict(arrowstyle="<->", color="#1f4e79", linewidth=1.2),
    )
    ax.text((b + 1.0) / 2.0, distance_y + 0.012, rf"$B=1-b={B:.3f}$", color="#1f4e79", ha="center", va="bottom")
    ax.annotate(
        "",
        xy=(a, distance_y),
        xytext=(1.0, distance_y),
        arrowprops=dict(arrowstyle="<->", color="#8b1e1e", linewidth=1.2),
    )
    ax.text(1.035, distance_y + 0.012, rf"$A=a-1={A:.3f}$", color="#8b1e1e", ha="center", va="bottom", fontsize=9)

    ax.text(
        0.02,
        0.96,
        r"$q(f)=\lambda f^2-(\lambda+\mu+\delta)f+\mu=\lambda(f-a)(f-b)$",
        transform=ax.transAxes,
        ha="left",
        va="top",
        color="#333333",
    )
    ax.text(
        0.48,
        0.87,
        r"probability range  $[0,1]$",
        transform=ax.transAxes,
        ha="center",
        color="#5d6570",
        fontsize=9,
        style="italic",
    )
    ax.text(1.0, 0.205, r"unit state $f=1$", ha="right", va="top", color="#666666", fontsize=9)

    ax.set_title("The two roots organise the closed-form geometry", loc="left", pad=10)
    ax.set_xlabel(r"candidate probability $f$")
    ax.set_ylabel(r"quadratic $q(f)$")
    ax.set_xlim(-0.02, 1.24)
    ax.set_ylim(-0.27, 0.22)
    ax.set_xticks(np.arange(0.0, 1.21, 0.2))
    ax.set_yticks(np.arange(-0.2, 0.21, 0.1))
    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)
    return a, b


if __name__ == "__main__":
    root_a, root_b = build()
    print(
        "N3.4 asserts passed: "
        f"b={root_b:.12f} < 1 < a={root_a:.12f}; "
        f"ab={root_a * root_b:.12f}, a+b={root_a + root_b:.12f}"
    )

