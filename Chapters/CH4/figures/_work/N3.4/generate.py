#!/usr/bin/env python3
"""Characteristic quadratic and its two roots at the working point."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

STYLE_DIR = Path(__file__).resolve().parents[2] / "_style"
sys.path.insert(0, str(STYLE_DIR))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
CHAPTER = HERE.parents[2]
PDF_PATH = CHAPTER / "figures" / "F4_quadratic_roots.pdf"
PNG_PATH = HERE / "preview.png"

LAMBDA, MU, DELTA = 1.0, 0.2, 0.05


def roots(lam, mu, delta):
    eta = (lam + mu + delta) / (2.0 * lam)
    spread = np.sqrt(eta**2 - mu / lam)
    return float(eta + spread), float(eta - spread)


def main() -> None:
    a, b = roots(LAMBDA, MU, DELTA)
    assert b < 1.0 < a
    assert abs(a * b - MU / LAMBDA) < 1e-10
    assert np.isclose((a - 1.0) * (1.0 - b), DELTA / LAMBDA, atol=1e-12)
    A, B = a - 1.0, 1.0 - b

    f = np.linspace(-0.02, 1.24, 1600)
    q = LAMBDA * f**2 - (LAMBDA + MU + DELTA) * f + MU

    fig, ax = plt.subplots(figsize=(5.8, 3.5))
    ax.axhline(0.0, color=style_rc.INK, linewidth=0.7, zorder=1)
    ax.axvline(1.0, color=style_rc.GREY, linestyle="--", linewidth=0.8, zorder=1)
    ax.plot(f, q, color=style_rc.VERMILLION, linewidth=1.6, zorder=3)
    ax.plot(b, 0.0, marker="o", markersize=6, color=style_rc.BLUE, zorder=5)
    ax.plot(a, 0.0, marker="o", markersize=6, markerfacecolor="white",
            markeredgecolor=style_rc.VERMILLION, markeredgewidth=1.4, zorder=5)
    ax.plot(1.0, -DELTA, marker="x", color=style_rc.GREY, markersize=6, zorder=5)

    ax.annotate(rf"$b={b:.3f}$", xy=(b, 0.0), xytext=(0.08, 0.09),
                arrowprops=dict(arrowstyle="->", color=style_rc.BLUE, lw=0.8),
                color=style_rc.BLUE, fontsize=8)
    ax.annotate(rf"$a={a:.3f}$", xy=(a, 0.0), xytext=(1.08, 0.09),
                arrowprops=dict(arrowstyle="->", color=style_rc.VERMILLION, lw=0.8),
                color=style_rc.VERMILLION, fontsize=8)
    ax.annotate(r"$q(1)=-\delta$", xy=(1.0, -DELTA), xytext=(0.72, -0.12),
                arrowprops=dict(arrowstyle="->", color=style_rc.GREY, lw=0.8),
                color=style_rc.SOFT, fontsize=8, ha="center")
    ax.text((b + 1.0) / 2.0, -0.20, rf"$B={B:.3f}$", color=style_rc.BLUE,
            ha="center", fontsize=8)
    ax.text((1.0 + a) / 2.0, -0.20, rf"$A={A:.3f}$", color=style_rc.VERMILLION,
            ha="center", fontsize=8)

    ax.set_xlabel(r"candidate probability $f$")
    ax.set_ylabel(r"$q(f)$")
    ax.set_xlim(-0.02, 1.24)
    ax.set_ylim(-0.27, 0.22)
    style_rc.tidy(ax)
    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)
    print(f"roots b={b:.6f}, a={a:.6f}; wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
