#!/usr/bin/env python3
"""Mean species count of the basic logistic speciation model (Yule slaved
to deterministic logistic abundance). Writes logspec_yule_mean.pdf.

    E[Y_t] = exp(σ K t) * ((ξ + 1) / (ξ + exp(r t)))^(σ K / r)
    ξ = K / N_0 - 1
    lim t→∞ E[Y_t] = (K / N_0)^{σ K / r}
"""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent

mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman"],
    "mathtext.fontset": "dejavuserif",
    "font.size": 9,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "axes.linewidth": 0.7,
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
    "pdf.fonttype": 42,
})

BLUE, GREEN, ORANGE, GRAY = "#1d4ed8", "#166534", "#b45309", "#4b5563"


def mean_y(t, N0, K, r, sigma):
    xi = K / N0 - 1.0
    expo = sigma * K / r
    return np.exp(sigma * K * t) * ((xi + 1.0) / (xi + np.exp(r * t))) ** expo


def main():
    K, r, sigma = 10.0, 1.0, 0.08
    expo = sigma * K / r
    t = np.linspace(0.0, 8.0, 500)

    fig, ax = plt.subplots(figsize=(5.4, 3.3))
    for N0, col, style in [(1, BLUE, "-"), (2, GREEN, "--"), (5, ORANGE, ":")]:
        m = mean_y(t, N0, K, r, sigma)
        lim = (K / N0) ** expo
        ax.plot(t, m, style, color=col, lw=1.7)
        ax.axhline(lim, color=col, lw=0.6, ls=(0, (3, 2)), alpha=0.45)
        ax.annotate(rf"$N_0={N0}$", xy=(t[12], m[12]),
                    xytext=(t[12] + 0.2, m[12] + 0.35),
                    color=col, fontsize=9)

    ax.set_xlabel(r"time $t$")
    ax.set_ylabel(r"mean species count $\mathbb{E}(Y_t)$")
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8.2)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    dest = OUT / "logspec_yule_mean.pdf"
    fig.savefig(dest)
    print("wrote", dest)


if __name__ == "__main__":
    main()
