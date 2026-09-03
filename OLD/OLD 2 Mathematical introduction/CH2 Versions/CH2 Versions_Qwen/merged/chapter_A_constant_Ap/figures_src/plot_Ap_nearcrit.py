#!/usr/bin/env python3
"""Near-critical approach of A(p) to its leading asymptotic.

Plots A(p)/(2 eps) - 1 against eps = 1 - 2p on log-log axes, using the
exact series of Prop. a:prop:series, together with the slope-1 guide and
the empirical fit eps (ln(1/eps) + 0.78) of Remark a:rem:rate.

Output: ../figures/Ap_nearcrit.pdf
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

BLUE, GRAY, ORANGE = "#1d4ed8", "#4b5563", "#b45309"


def A_of_p(p, tol=1e-15, cap=20_000_000):
    r = 2.0 * p
    S = 1.0
    rn = 1.0
    inv = 1.0
    for _ in range(cap):
        term = rn / (2.0 - S)
        inv += term
        if term < tol:
            break
        S = r * S - p * S * S
        rn *= r
    return 1.0 / inv


eps = np.geomspace(1e-5, 10 ** -0.35, 34)
deficit = np.array([1.0 - A_of_p((1.0 - e) / 2.0) / (2.0 * e) for e in eps])

fig, ax = plt.subplots(figsize=(5.4, 3.6))

ax.loglog(eps, deficit, "o", color=BLUE, ms=3.2, mew=0,
          label=None, zorder=3)
# slope-1 guide anchored at the largest eps
i0 = -1
c1 = deficit[i0] / eps[i0]
ax.loglog(eps, c1 * eps, ":", color=GRAY, lw=1.3)
ax.annotate("slope $1$", xy=(eps[6], c1 * eps[6]),
            xytext=(eps[6] * 1.6, c1 * eps[6] * 0.55), color=GRAY, fontsize=8.5)
# empirical fit eps (ln(1/eps) + 0.78)
fit = eps * (np.log(1.0 / eps) + 0.78)
ax.loglog(eps, fit, "--", color=ORANGE, lw=1.4)
ax.annotate(r"$\varepsilon\,(\ln\frac{1}{\varepsilon}+0.78)$",
            xy=(1.2e-3, fit[eps.searchsorted(1.2e-3)]),
            xytext=(3e-3, fit[eps.searchsorted(1.2e-3)] * 1.25),
            color=ORANGE, fontsize=8.5)

ax.annotate(r"exact series for $1-\frac{A(p)}{2\varepsilon}$",
            xy=(3e-5, deficit[3]), xytext=(6e-5, deficit[3] * 1.9),
            color=BLUE, fontsize=8.5,
            arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.6))

ax.set_xlabel(r"$\varepsilon = 1-2p$")
ax.set_ylabel(r"$1-\frac{A(p)}{2\varepsilon}$")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(__file__.rsplit("/", 1)[0] + "/../figures/Ap_nearcrit.pdf")
print("wrote Ap_nearcrit.pdf")
