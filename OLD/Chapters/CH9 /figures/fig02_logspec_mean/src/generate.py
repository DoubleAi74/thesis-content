#!/usr/bin/env python3
"""Mean species count of the logistic speciation model.

    E[S_t] = exp(σ K t) * ((ξ + 1) / (ξ + exp(ϱ t)))^(σ K / ϱ)
    ξ = K / N_0 - 1
    lim t→∞ E[S_t] = (K / N_0)^{σ K / ϱ}

Parameters match Good examples/CH2/figures/make_logspec_yule_mean.py,
with CH9 symbols (K, ϱ, S_t) in place of (C, r, Y_t).
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


def mean_s(t, N0, K, rho, sigma):
    xi = K / N0 - 1.0
    expo = sigma * K / rho
    return np.exp(sigma * K * t) * ((xi + 1.0) / (xi + np.exp(rho * t))) ** expo


def main():
    K, rho, sigma = 10.0, 1.0, 0.08
    expo = sigma * K / rho
    t = np.linspace(0.0, 8.0, 500)
    styles = [
        (1, style_rc.BLUE, "-"),
        (2, style_rc.TEAL, "--"),
        (5, style_rc.VERMILLION, ":"),
    ]

    fig, ax = plt.subplots(figsize=style_rc.FIGSIZE_SINGLE)
    for N0, col, ls in styles:
        m = mean_s(t, N0, K, rho, sigma)
        lim = (K / N0) ** expo
        ax.plot(t, m, ls, color=col, lw=1.7, label=rf"$N_0={N0}$")
        ax.axhline(lim, color=col, lw=0.7, ls=(0, (3, 2)), alpha=0.55)

    ax.set_xlabel(r"time $t$")
    ax.set_ylabel(r"mean species count $\mathbb{E}(S_t)$")
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8.2)
    ax.legend(loc="lower right")
    fig.tight_layout()
    style_rc.save_figure(fig, OUT / "fig02.pdf", OUT / "fig02.png")
    print("wrote", OUT / "fig02.pdf")


if __name__ == "__main__":
    main()
