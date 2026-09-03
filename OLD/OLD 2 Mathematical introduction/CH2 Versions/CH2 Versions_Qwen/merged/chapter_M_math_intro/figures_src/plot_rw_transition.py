#!/usr/bin/env python3
"""Position distribution of the simple random walk at time n=40.

Exact binomial law from eq:rwlaw in Chapter M, section 2.2.1:
    Pr(X_n = X_0 + 2r - n) = C(n, r) p^r (1-p)^{n-r}.
Three drifts p = 0.4, 0.5, 0.6; means and variances annotated.

Output: ../figures/rw_transition.pdf
"""
from math import lgamma

import numpy as np
import matplotlib
matplotlib.use("pdf")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "font.size": 9,
    "axes.linewidth": 0.8,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "pdf.fonttype": 42,
})

BLUE, GREEN, ORANGE = "#1d4ed8", "#166534", "#b45309"


def walk_pmf(n, p):
    """Exact Pr(X_n - X_0 = 2r - n) for r = 0..n."""
    r = np.arange(0, n + 1)
    q = 1.0 - p
    logpmf = np.vectorize(lgamma)(n + 1) \
        - np.vectorize(lgamma)(r + 1) \
        - np.vectorize(lgamma)(n - r + 1) \
        + r * np.log(p) + (n - r) * np.log(q)
    return 2 * r - n, np.exp(logpmf)


n = 40
fig, ax = plt.subplots(figsize=(5.4, 3.4))

cases = [
    (0.6, ORANGE, "--"),
    (0.5, BLUE, "-"),
    (0.4, GREEN, ":"),
]
for p, col, style in cases:
    x, pmf = walk_pmf(n, p)
    mean = (2 * p - 1) * n
    ax.plot(x, pmf, style, color=col, lw=1.6)
    ax.annotate(f"$p={p:.1f}$",
                xy=(mean, pmf.max()),
                xytext=(mean + (10 if p == 0.6 else (-11 if p == 0.4 else 4)),
                        pmf.max() * (1.05 if p != 0.4 else 0.88)),
                color=col, fontsize=9)
    ax.axvline(mean, color=col, lw=0.7, ls=(0, (1, 3)))

ax.set_xlabel("$X_n - X_0$")
ax.set_ylabel("$\\Pr(X_n - X_0)$")
ax.set_xlim(-22, 22)
ax.set_ylim(0, 0.145)
ax.annotate("means $(p-q)n$\nvariances $4pqn$",
            xy=(0.40, 0.97), xycoords="axes fraction", va="top", ha="left",
            fontsize=8)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(__file__.rsplit("/", 1)[0] + "/../figures/rw_transition.pdf")
print("wrote rw_transition.pdf")
