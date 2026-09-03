#!/usr/bin/env python3
"""
Generate the exact displacement law of the simple random walk.

Produces, in the directory containing this script:
    rw_transition.pdf  -- section 2.1.1, eq. (m:eq:rwlaw)

The law plotted is
    Pr(X_n - X_0 = 2r - n) = C(n, r) q^r (1-q)^{n-r},
with q the probability of a +1 step, matching the chapter's notation
(p is reserved for the Galton-Watson division probability).

Run:  python3 make_rw_transition.py
Deps: numpy, matplotlib.  Output is deterministic.
"""

from math import lgamma
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent

# --- House style: match the 11pt serif body text of the chapter ------------
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

BLUE, GREEN, ORANGE = "#1d4ed8", "#166534", "#b45309"


def walk_pmf(n, q):
    """Exact Pr(X_n - X_0 = 2r - n) for r = 0..n, computed in logs."""
    r = np.arange(0, n + 1)
    lg = np.vectorize(lgamma)
    logpmf = (lg(n + 1) - lg(r + 1) - lg(n - r + 1)
              + r * np.log(q) + (n - r) * np.log(1.0 - q))
    return 2 * r - n, np.exp(logpmf)


def main():
    n = 40
    fig, ax = plt.subplots(figsize=(5.4, 3.2))

    for q, col, style, dx, dy in [(0.6, ORANGE, "--", 10, 1.05),
                                  (0.5, BLUE, "-", 4, 1.05),
                                  (0.4, GREEN, ":", -11, 0.88)]:
        x, pmf = walk_pmf(n, q)
        mean = (2 * q - 1) * n
        ax.plot(x, pmf, style, color=col, lw=1.6)
        ax.annotate(rf"$q={q:.1f}$",
                    xy=(mean, pmf.max()),
                    xytext=(mean + dx, pmf.max() * dy),
                    color=col, fontsize=9)
        ax.axvline(mean, color=col, lw=0.7, ls=(0, (1, 3)))

    ax.set_xlabel(r"$X_n - X_0$")
    ax.set_ylabel(r"$\Pr(X_n - X_0)$")
    ax.set_xlim(-22, 22)
    ax.set_ylim(0, 0.145)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "rw_transition.pdf")
    print("wrote", OUT / "rw_transition.pdf")


if __name__ == "__main__":
    main()
