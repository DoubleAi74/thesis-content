#!/usr/bin/env python3
"""Geometric burst-size preview for the no-death case."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

STYLE_DIR = Path(__file__).resolve().parents[2] / "_style"
sys.path.insert(0, str(STYLE_DIR))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402

WORKDIR = Path(__file__).resolve().parent
PDF_PATH = WORKDIR.parents[2] / "figures/F4_burst_size_preview.pdf"
PNG_PATH = WORKDIR / "preview.png"

LAM, MU, DELTA = 1.0, 0.0, 0.1
A = (LAM + DELTA) / LAM
K = np.arange(1, 31)


def main() -> None:
    ratio = 1.0 / A
    burst = (DELTA / LAM) * A ** (-K)
    geometric = (1.0 - ratio) * ratio ** (K - 1)
    assert MU == 0.0
    assert float(np.max(np.abs(burst - geometric))) < 1e-12

    fig, ax = plt.subplots(figsize=(5.6, 3.2))
    ax.bar(K, burst, width=0.76, color=style_rc.BLUE, edgecolor=style_rc.BLUE,
           linewidth=0.5, alpha=0.55, label=r"$\Pr\{\mathcal{K}=k\}$", zorder=2)
    ax.plot(K, geometric, color=style_rc.VERMILLION, marker="o", markersize=3.0,
            markerfacecolor="white", markeredgewidth=0.8, linewidth=1.3,
            label=r"geometric$(1/a)$", zorder=3)
    ax.set(xlim=(0.5, 30.5), ylim=(0.0, 0.1), xlabel=r"burst size $k$",
           ylabel="Probability")
    ax.legend(loc="upper right")
    style_rc.tidy(ax)
    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)
    print(f"wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
