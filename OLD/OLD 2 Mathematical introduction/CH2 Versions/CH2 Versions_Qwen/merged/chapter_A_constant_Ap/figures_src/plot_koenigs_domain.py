#!/usr/bin/env python3
"""The Koenigs function psi_r for r=0.7: germ versus basin (A rem:basin).

Solid curve: the basin value psi_r(z) = lim_{n->inf} r^{-n} f^{circ n}(z),
computed by direct orbit iteration (N=120, error O(r^N)).
Dashed curves: Taylor partial sums of orders 3, 6, 10 about the origin,
whose coefficients are obtained by iterating the functional equation
psi(f(z)) = r psi(z) on truncated polynomials.
Vertical line: the guaranteed disc radius (1-r)/r of the germ.

Output: ../figures/koenigs_domain.pdf
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

BLUE, GREEN, ORANGE, ROSE, GRAY = (
    "#1d4ed8", "#166534", "#b45309", "#be123c", "#4b5563")

r = 0.7
D = 18


def koenigs_coeffs(r, D, iters=600):
    """Coefficients of psi_r up to degree D via g <- (g o f)/r, f = rz - rz^2."""
    g = np.zeros(D + 1)
    g[1] = 1.0
    f = np.zeros(D + 1)
    f[1], f[2] = r, -r
    for _ in range(iters):
        # powers F_k = f^k (truncated)
        powers = [np.array([1.0] + [0.0] * D)]
        for _ in range(D):
            conv = np.convolve(powers[-1], f)[: D + 1]
            powers.append(np.pad(conv, (0, D + 1 - len(conv))))
        comp = np.zeros(D + 1)
        for k in range(D + 1):
            comp += g[k] * powers[k]
        g = comp / r
    return g


# ---- basin values by orbit iteration ----------------------------------------
z = np.linspace(0.0, 0.99, 220)
orb = z.copy()
for _ in range(120):
    orb = r * orb * (1.0 - orb)
psi_basin = orb / r ** 120

# ---- Taylor partial sums -----------------------------------------------------
c = koenigs_coeffs(r, D)
zz = np.linspace(0.0, 0.99, 220)
partials = {}
for m in (3, 6, 10):
    partials[m] = np.polyval(c[: m + 1][::-1], zz)

fig, ax = plt.subplots(figsize=(5.6, 3.6))

ax.plot(z, psi_basin, "-", color=BLUE, lw=1.9)
ax.plot(zz, partials[3], "--", color=ORANGE, lw=1.3)
ax.plot(zz, partials[6], "-.", color=GREEN, lw=1.3)
ax.plot(zz, partials[10], ":", color=ROSE, lw=1.5)

rad = (1.0 - r) / r
ax.axvline(rad, color=GRAY, lw=0.9, ls=(0, (4, 3)))
ax.annotate("radius $(1-r)/r$", xy=(rad, 1.95), xytext=(0.52, 1.80),
            color=GRAY, fontsize=8.5,
            arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.6))

ax.annotate("basin value $\\psi_r(z)=\\lim r^{-n}f^{\\circ n}(z)$",
            xy=(0.62, np.interp(0.62, z, psi_basin)),
            xytext=(0.40, 1.45), color=BLUE, fontsize=8.3,
            arrowprops=dict(arrowstyle="-", color=BLUE, lw=0.6))
ax.annotate("orders 3, 6, 10", xy=(0.33, np.interp(0.33, zz, partials[6])),
            xytext=(0.10, 0.75), color=GREEN, fontsize=8.3,
            arrowprops=dict(arrowstyle="-", color=GREEN, lw=0.6))

ax.set_xlabel("$z$")
ax.set_ylabel("$\\psi_{0.7}(z)$")
ax.set_xlim(0, 1.0)
ax.set_ylim(-0.4, 2.1)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(__file__.rsplit("/", 1)[0] + "/../figures/koenigs_domain.pdf")
print("wrote koenigs_domain.pdf")
