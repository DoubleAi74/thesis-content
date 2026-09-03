#!/usr/bin/env python3
"""The constant A(p) against its two-sided bounds, and the ratio A/A_c.

Panel (a): A(p) from the exact series of Prop. a:prop:series,
    1/A(p) = 1 + sum_{n>=0} (2p)^n / (2 - S_n),
against the lower bound eps/(1+eps), the upper bound 2 eps/(1+2 eps)
and the near-critical asymptotic 2 eps, eps = 1 - 2p.
Panel (b): the ratio A(p)/A_c(p) with the endpoint limits 1/2 and 1
of eq:ratiolimits.

Output: ../figures/Ap_bounds_ratio.pdf
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

BLUE, GREEN, ORANGE, GRAY = "#1d4ed8", "#166534", "#b45309", "#4b5563"


def A_of_p(p, tol=1e-13, cap=20_000_000):
    """Exact-series evaluation of A(p), p in [0, 1/2)."""
    if p == 0.0:
        return 0.5
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


fig, (axa, axb) = plt.subplots(1, 2, figsize=(7.2, 3.2))

# ---- panel (a): A(p) between its bounds ------------------------------------
ps = np.linspace(0.001, 0.499, 160)
Av = np.array([A_of_p(p) for p in ps])
eps = 1.0 - 2.0 * ps
lower = eps / (1.0 + eps)
upper = 2.0 * eps / (1.0 + 2.0 * eps)

axa.plot(ps, Av, "-", color=BLUE, lw=1.8)
axa.plot(ps, lower, "--", color=GREEN, lw=1.4)
axa.plot(ps, upper, "--", color=ORANGE, lw=1.4)
axa.plot(ps, 2.0 * eps, ":", color=GRAY, lw=1.4)
axa.annotate("$A(p)$", xy=(0.20, A_of_p(0.20)), xytext=(0.155, 0.44),
             color=BLUE, fontsize=9)
axa.annotate(r"$\frac{\varepsilon}{1+\varepsilon}$", xy=(0.29, 0.165),
             xytext=(0.24, 0.245), color=GREEN, fontsize=9)
axa.annotate(r"$\frac{2\varepsilon}{1+2\varepsilon}$", xy=(0.315, 0.425),
             xytext=(0.21, 0.52), color=ORANGE, fontsize=9)
axa.annotate("$2\\varepsilon$", xy=(0.40, 0.20), xytext=(0.352, 0.152),
             color=GRAY, fontsize=9)
axa.annotate("sharp as $p\\to 0$", xy=(0.01, 0.49), xytext=(0.06, 0.60),
             fontsize=8, color=GREEN,
             arrowprops=dict(arrowstyle="-", color=GREEN, lw=0.6))
axa.annotate("sharp as $p\\to\\frac{1}{2}$", xy=(0.497, 0.0045),
             xytext=(0.34, 0.06), fontsize=8, color=ORANGE,
             arrowprops=dict(arrowstyle="-", color=ORANGE, lw=0.6))
axa.set_xlabel("$p$")
axa.set_ylabel("$A(p)$ and comparison curves")
axa.set_xlim(0, 0.5)
axa.set_ylim(0, 0.70)
axa.spines[["top", "right"]].set_visible(False)

# ---- panel (b): the ratio A/A_c ---------------------------------------------
eps2 = np.concatenate([np.linspace(0.999, 0.05, 60),
                       np.geomspace(0.05, 1e-4, 40)[1:]])
ps2 = (1.0 - eps2) / 2.0
ratio = np.array([A_of_p(p) for p in ps2]) / (2.0 * eps2 / (1.0 + eps2))

axb.plot(ps2, ratio, "-", color=BLUE, lw=1.8)
axb.axhline(0.5, color=GRAY, lw=0.9, ls=(0, (4, 3)))
axb.axhline(1.0, color=GRAY, lw=0.9, ls=(0, (4, 3)))
axb.annotate(r"$\frac{1}{2}$", xy=(0.002, 0.5), xytext=(0.03, 0.42),
             color=GRAY, fontsize=9)
axb.annotate(r"$1$", xy=(0.49, 1.0), xytext=(0.44, 0.93),
             color=GRAY, fontsize=9)
axb.annotate(r"$A(p)/A_{\mathrm{c}}(p)$", xy=(0.19, 0.66), xytext=(0.12, 0.73),
             color=BLUE, fontsize=9)
axb.set_xlabel("$p$")
axb.set_ylabel("ratio")
axb.set_xlim(0, 0.5)
axb.set_ylim(0.4, 1.12)
axb.spines[["top", "right"]].set_visible(False)

fig.tight_layout()
fig.savefig(__file__.rsplit("/", 1)[0] + "/../figures/Ap_bounds_ratio.pdf")
print("wrote Ap_bounds_ratio.pdf")
