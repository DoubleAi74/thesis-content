#!/usr/bin/env python3
"""Schematic simulation of the coupled ODE--CTMC rupture system (M section 2.2.4).

Compartment contents X_t evolve as a birth--death--catastrophe process
(rates lambda X, mu X, rho X); the shared medium obeys dy/dt = -delta y
between events and receives y -> y + c X_{tau-} at each rupture tau.
For illustration the compartment is re-seeded with N0 individuals after
each rupture (the true process of def:bdc is absorbing post-catastrophe).

Exact event-driven (Gillespie) simulation; the ODE is integrated exactly
between events. Fixed seed for reproducibility.

Output: ../figures/rupture_sawtooth.pdf
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

BLUE, ORANGE, GRAY = "#1d4ed8", "#b45309", "#4b5563"

lam, mu, rho = 0.55, 0.25, 0.08
N0, delta, cin = 5, 0.30, 0.4
rng = np.random.default_rng(7)

t, X, y = 0.0, N0, 0.0
segs_X = [(0.0, N0)]          # (time, value held from this time)
events_y = [(0.0, 0.0)]       # (time, y just after event)
ruptures = []

while len(ruptures) < 6 and t < 60.0:
    R = (lam + mu + rho) * X
    t += rng.exponential(1.0 / R)
    u = rng.random() * R
    if u < lam * X:
        X += 1
    elif u < (lam + mu) * X:
        X -= 1
        if X == 0:
            X = N0  # re-seed for illustration
    else:
        ruptures.append(t)
        events_y.append((t, y))
        y += cin * X
        events_y.append((t, y))
        X = N0  # re-seed for illustration
    segs_X.append((t, X))

t_end = t

# reconstruct y(t) exactly on a fine grid
grid = np.linspace(0.0, t_end, 4000)
yv = np.empty_like(grid)
ev = sorted(events_y)
j = 0
for k, tg in enumerate(grid):
    while j + 1 < len(ev) and ev[j + 1][0] <= tg:
        j += 1
    t0, y0 = ev[j]
    yv[k] = y0 * np.exp(-delta * (tg - t0))

fig, (ax1, ax2) = plt.subplots(
    2, 1, figsize=(5.6, 4.4), sharex=True, layout="constrained",
    gridspec_kw={"height_ratios": [1.0, 1.0], "hspace": 0.14})

ts = [s[0] for s in segs_X] + [t_end]
xs = [s[1] for s in segs_X] + [segs_X[-1][1]]
ax1.step(ts, xs, where="post", color=BLUE, lw=1.2)
ax1.set_ylabel("compartment $X_t$")
ax1.set_ylim(0, max(xs) * 1.12)

ax2.plot(grid, yv, color=ORANGE, lw=1.3)
ax2.set_ylabel("medium $y(t)$")
ax2.set_xlabel("time $t$")
ax2.set_xlim(0, t_end)

for ax in (ax1, ax2):
    for tr in ruptures:
        ax.axvline(tr, color=GRAY, lw=0.6, ls=(0, (2, 3)))
    ax.spines[["top", "right"]].set_visible(False)
    ax.annotate("rupture", xy=(ruptures[0], 1.0), xycoords=("data", "axes fraction"),
                xytext=(ruptures[0] + 0.6, 0.88), fontsize=8, color=GRAY)

fig.savefig(__file__.rsplit("/", 1)[0] + "/../figures/rupture_sawtooth.pdf")
print(f"wrote rupture_sawtooth.pdf  ({len(ruptures)} ruptures, t_end={t_end:.2f})")
