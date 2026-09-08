#!/usr/bin/env python3
"""Closed-form geometric law of S_infty and the two-group contour.

The content is Candidate 2's logspec_limit figure, redrawn in this chapter's
house palette. No simulation: S_infty is geometric with mean
(K/N_0)^{sigma K / rho}.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "figures" / "_style"))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parents[1]


def main():
    fig, axes = plt.subplots(1, 2, figsize=style_rc.FIGSIZE_DOUBLE)

    ax = axes[0]
    for (room, cap), col in zip(
        [(10, 1.0), (50, 1.0), (10, 2.0)],
        [style_rc.BLUE, style_rc.VERMILLION, style_rc.TEAL],
    ):
        mean = room ** cap
        p = 1.0 / mean
        n = np.arange(1, 61)
        ax.plot(
            n,
            p * (1 - p) ** (n - 1),
            color=col,
            lw=1.5,
            label=rf"$K/N_0={room}$, $\sigma K/\varrho={cap:g}$",
        )
    ax.set_title(r"Law of $S_\infty$")
    ax.set_xlabel(r"$n$")
    ax.set_ylabel(r"$\mathbb{P}(S_\infty=n)$")
    ax.set_xlim(1, 60)
    ax.set_ylim(0, None)
    ax.legend(loc="upper right", fontsize=8)

    ax = axes[1]
    room = np.linspace(2, 60, 200)
    cap = np.linspace(0.2, 2.0, 200)
    R, C = np.meshgrid(room, cap)
    Z = R ** C
    cs = ax.contour(
        R,
        C,
        np.log10(Z),
        levels=[0.5, 1, 1.5, 2, 2.5, 3],
        colors=[style_rc.BLUE],
        linewidths=0.9,
    )
    ax.clabel(cs, fmt=lambda v: rf"$10^{{{v:g}}}$", fontsize=8)
    ax.set_title(r"$\mathbb{E}(S_\infty)$")
    ax.set_xlabel(r"$K/N_0$")
    ax.set_ylabel(r"$\sigma K/\varrho$")

    fig.tight_layout()
    style_rc.save_figure(fig, OUT / "fig02b.pdf", OUT / "fig02b.png")
    print("wrote", OUT / "fig02b.pdf")


if __name__ == "__main__":
    main()
