#!/usr/bin/env python3
"""
Generate the figures for the time-inhomogeneous and coupled sections.

Produces, in the directory containing this script:
    logspec_mean.pdf      -- section 2.4.2, the logistic speciation surrogate
    rupture_sawtooth.pdf  -- section 2.5.3, rupture into a shared medium

Notation follows NOTATION.md: gamma = lambda_0 - mu is the intrinsic growth
rate of the logistic surrogate (r is reserved for the multiplier 2p), and
delta is the clearance rate of the medium.

Run:  python3 make_inhomogeneous_figures.py
Deps: numpy, matplotlib.  The seed is fixed, so output is reproducible.
"""

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

BLUE, GREEN, ORANGE, GRAY = "#1d4ed8", "#166534", "#b45309", "#4b5563"


# ---------------------------------------------------------------------------
#  The logistic speciation surrogate: mean diversity
#     E[X_t] = N* / (1 + B e^{-gamma t}),   B = N*/N_0 - 1,
#  with mu/lambda_0 = 0.1 and K = 10, so N* = K(1 - mu/lambda_0) = 9.
# ---------------------------------------------------------------------------
def logspec_mean():
    Nstar = 9.0
    gt = np.linspace(0, 6, 400)

    fig, ax = plt.subplots(figsize=(5.4, 3.3))
    for N0, col, style in [(1, BLUE, "-"), (3, GREEN, "--"), (6, ORANGE, ":")]:
        B = Nstar / N0 - 1.0
        mean = Nstar / (1.0 + B * np.exp(-gt))
        ax.plot(gt, mean, style, color=col, lw=1.7)
        ax.annotate(rf"$N_0={N0}$", xy=(gt[8], mean[8]),
                    xytext=(gt[8] + 0.15, mean[8] - 1.1),
                    color=col, fontsize=9)

    ax.axhline(Nstar, color=GRAY, lw=0.9, ls=(0, (4, 3)))
    ax.annotate(r"$N_\ast = K(1-\mu/\lambda_0)$", xy=(6.0, Nstar),
                xytext=(3.5, Nstar + 0.35), fontsize=8.5, color=GRAY)

    ax.set_xlabel(r"rescaled time $\gamma t$,$\ \gamma = \lambda_0-\mu$")
    ax.set_ylabel(r"mean diversity $\mathbb{E}(X_t)$")
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 10.6)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "logspec_mean.pdf")
    print("wrote", OUT / "logspec_mean.pdf")


# ---------------------------------------------------------------------------
#  Rupture into a shared medium.
#
#  X_t is a birth-death-catastrophe process (rates lambda X, mu X, rho X);
#  the medium obeys dy/dt = -delta y between ruptures and receives the
#  impulsive release y -> y + c X_{tau-} at each rupture tau.  The medium is
#  decayed to the event time *before* the release is added, so the drawn
#  trajectory solves the stated flow-plus-jump system exactly.
#
#  For illustration the compartment is re-seeded with X_0 individuals after
#  each rupture; the process of Definition 2.x is absorbed there instead.
# ---------------------------------------------------------------------------
def rupture_sawtooth(seed=24, n_ruptures=5):
    lam, mu, rho = 0.55, 0.25, 0.08
    X0, delta, c = 5, 0.30, 0.4
    rng = np.random.default_rng(seed)

    t, X, y, t_last = 0.0, X0, 0.0, 0.0
    steps_X = [(0.0, X0)]        # (time, value held from this time)
    events_y = [(0.0, 0.0)]      # (time, y immediately after the event)
    ruptures = []

    while len(ruptures) < n_ruptures:
        total = (lam + mu + rho) * X
        t += rng.exponential(1.0 / total)
        u = rng.random() * total
        if u < lam * X:
            X += 1
        elif u < (lam + mu) * X:
            X -= 1
            if X == 0:
                X = X0                      # re-seed for illustration
        else:
            y *= np.exp(-delta * (t - t_last))   # clear, then release
            t_last = t
            events_y.append((t, y))
            y += c * X
            events_y.append((t, y))
            ruptures.append(t)
            X = X0                          # re-seed for illustration
        steps_X.append((t, X))

    t_end = t

    # y(t) reconstructed exactly between events
    grid = np.linspace(0.0, t_end, 4000)
    yv = np.empty_like(grid)
    j = 0
    for k, tg in enumerate(grid):
        while j + 1 < len(events_y) and events_y[j + 1][0] <= tg:
            j += 1
        t0, y0 = events_y[j]
        yv[k] = y0 * np.exp(-delta * (tg - t0))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5.6, 4.2), sharex=True,
                                   layout="constrained")

    ts = [s[0] for s in steps_X] + [t_end]
    xs = [s[1] for s in steps_X] + [steps_X[-1][1]]
    ax1.step(ts, xs, where="post", color=BLUE, lw=1.2)
    ax1.set_ylabel("compartment $X_t$")
    ax1.set_ylim(0, max(xs) * 1.15)

    ax2.plot(grid, yv, color=ORANGE, lw=1.3)
    ax2.set_ylabel("medium $y(t)$")
    ax2.set_xlabel("time $t$")
    ax2.set_xlim(0, t_end)
    ax2.set_ylim(0, max(yv) * 1.15)

    for ax in (ax1, ax2):
        for tr in ruptures:
            ax.axvline(tr, color=GRAY, lw=0.6, ls=(0, (2, 3)))
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
    ax1.annotate("rupture", xy=(ruptures[0], 1.0),
                 xycoords=("data", "axes fraction"),
                 xytext=(ruptures[0] + 0.25, 0.88), fontsize=8, color=GRAY)

    fig.savefig(OUT / "rupture_sawtooth.pdf")
    print("wrote", OUT / "rupture_sawtooth.pdf",
          f"({len(ruptures)} ruptures, t_end={t_end:.2f})")


if __name__ == "__main__":
    logspec_mean()
    rupture_sawtooth()
