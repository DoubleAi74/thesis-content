#!/usr/bin/env python3
"""Gambler's ruin hitting probabilities, exact formula eq:ruinprob.

h_i = probability the walk reaches b before 0, started at i:
    h_i = ((q/p)^i - 1) / ((q/p)^b - 1)   for p != q,
    h_i = i/b                              for p = q.
Shown for p = 0.4, 0.5, 0.6 with b = 20.

Output: ../figures/ruin_prob.pdf
"""
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

b = 20
i = np.arange(0, b + 1)

fig, ax = plt.subplots(figsize=(5.4, 3.4))

cases = [
    (0.6, ORANGE, "--", 4, "$p=0.6$"),
    (0.5, BLUE, "-", 12, "$p=\\frac{1}{2}$"),
    (0.4, GREEN, ":", 16, "$p=0.4$"),
]
for p, col, style, ilab, lab in cases:
    q = 1.0 - p
    if p == 0.5:
        h = i / b
    else:
        ratio = q / p
        h = (ratio ** i - 1) / (ratio ** b - 1)
    ax.plot(i, h, style, color=col, lw=1.7)
    ax.annotate(lab, xy=(ilab, h[ilab]),
                xytext=(ilab + 1.2, h[ilab] + 0.06),
                color=col, fontsize=8.5)

ax.set_xlabel("starting position $i$")
ax.set_ylabel("$h_i = \\Pr(\\,$reach $b$ before $0\\,)$")
ax.set_xlim(0, b)
ax.set_ylim(0, 1.18)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(__file__.rsplit("/", 1)[0] + "/../figures/ruin_prob.pdf")
print("wrote ruin_prob.pdf")
