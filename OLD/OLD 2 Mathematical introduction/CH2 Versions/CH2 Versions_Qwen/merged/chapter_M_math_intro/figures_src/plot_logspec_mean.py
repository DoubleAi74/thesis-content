#!/usr/bin/env python3
"""Mean diversity of the logistic speciation surrogate, eq:logspecmean.

E[X_t] = N* / (1 + B e^{-rt}),  B = N*/N_0 - 1,
with the chapter's parameters mu/lambda_0 = 0.1, K = 10, so
r = 0.9 lambda_0 and N* = K(1 - mu/lambda_0) = 9.
Curves for N_0 = 1, 3, 6, all relaxing to N*.

Output: ../figures/logspec_mean.pdf
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

Nstar = 9.0
rt = np.linspace(0, 6, 400)

fig, ax = plt.subplots(figsize=(5.4, 3.4))

for N0, col, style in [(1, BLUE, "-"), (3, GREEN, "--"), (6, ORANGE, ":")]:
    B = Nstar / N0 - 1.0
    mean = Nstar / (1.0 + B * np.exp(-rt))
    ax.plot(rt, mean, style, color=col, lw=1.7)
    ax.annotate(f"$N_0={N0}$", xy=(rt[8], mean[8]),
                xytext=(rt[8] + 0.15, mean[8] - 1.1),
                color=col, fontsize=9)

ax.axhline(Nstar, color="#4b5563", lw=0.9, ls=(0, (4, 3)))
ax.annotate("$N_\\ast = K(1-\\mu/\\lambda_0)$", xy=(6.0, Nstar),
            xytext=(3.6, Nstar + 0.35), fontsize=8.5, color="#4b5563")

ax.set_xlabel("rescaled time $rt$, $\\;r=\\lambda_0-\\mu$")
ax.set_ylabel("mean diversity $\\mathrm{E}[X_t]$")
ax.set_xlim(0, 6)
ax.set_ylim(0, 10.6)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(__file__.rsplit("/", 1)[0] + "/../figures/logspec_mean.pdf")
print("wrote logspec_mean.pdf")
