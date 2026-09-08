#!/usr/bin/env python3
"""R1 --- replicator-suppressor survival maps.

Writes combined strips repsupp_N20.pdf and repsupp_N10.pdf, and the six
individual panels. Quantity: 1 - pi_{i,j}.
"""

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_style"))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1 import make_axes_locatable

LAM = 1.0
SIGS = (0.1, 0.2, 0.3)
CMAP = style_rc.survival_cmap()
NORM = Normalize(vmin=0.0, vmax=1.0)


def solve_pi(N, sig, lam=LAM):
    idx = {}
    for j in range(1, N + 1):
        for i in range(1, j + 1):
            idx[(i, j)] = len(idx)
    n = len(idx)
    A = np.zeros((n, n))
    c = np.zeros(n)
    for (i, j), k in idx.items():
        ahat = lam / (lam + sig * j)
        bhat = sig * j / (lam + sig * j)
        if i + 1 <= j:
            A[k, idx[(i + 1, j)]] = ahat
        if i - 1 >= 1:
            A[k, idx[(i - 1, j - 1)]] = bhat
        else:
            c[k] = bhat
    sol = np.linalg.solve(np.eye(n) - A, c)
    pi = np.zeros((N + 1, N + 1))
    pi[0, :] = 1.0
    for (i, j), k in idx.items():
        pi[i, j] = sol[k]
    return pi


def diagonal_closed_form(N, sig, lam=LAM):
    nu = lam / sig
    out = np.ones(N + 1)
    for j in range(1, N + 1):
        out[j] = math.exp(math.lgamma(j + 1) + math.lgamma(nu + 1)
                          - math.lgamma(j + nu + 1))
    return out


def _panel(ax_bar, ax, surv, N, sig, numbers):
    ax_bar.bar(np.arange(N + 1), surv[:, N], width=0.8,
               color=style_rc.BLUE, linewidth=0)
    ax_bar.set_xlim(-0.6, N + 0.6)
    ax_bar.set_ylim(0, 1.05)
    ax_bar.set_yticks([0.0, 1.0])
    ax_bar.set_xticks([])
    ax_bar.set_title(rf"$N={N}$, $\varsigma={sig}$", fontsize=9)
    im = ax.imshow(
        surv.T, origin="lower", cmap=CMAP, norm=NORM,
        extent=(-0.5, N + 0.5, -0.5, N + 0.5), aspect="equal",
        interpolation="nearest",
    )
    if numbers:
        step = 1 if N <= 10 else 2
        for i in range(0, N + 1, step):
            for j in range(0, N + 1, step):
                val = surv[i, j]
                ax.text(i, j, f"{val:.1f}", ha="center", va="center",
                        fontsize=5.0 if N <= 10 else 3.6,
                        color="white" if val < 0.45 or val > 0.85 else style_rc.INK)
    ax.plot([-0.5, N + 0.5], [-0.5, N + 0.5],
            color=style_rc.INK, lw=0.7, ls=(0, (3, 2)))
    ax.set_xticks(range(0, N + 1, 2))
    ax.set_yticks(range(0, N + 1, 2))
    ax.set_xlabel(r"incident replicators $X_0=i$")
    ax.set_ylabel(r"granule store $Q_0=j$")
    return im


def draw_strip(N, survs, path, numbers):
    fig = plt.figure(figsize=(7.6, 3.7))
    gs = fig.add_gridspec(2, 3, height_ratios=[1, 3.6], hspace=0.08, wspace=0.28)
    im = None
    for col, (sig, surv) in enumerate(zip(SIGS, survs)):
        ax_bar = fig.add_subplot(gs[0, col])
        ax = fig.add_subplot(gs[1, col])
        im = _panel(ax_bar, ax, surv, N, sig, numbers=numbers)
        if col > 0:
            ax.set_ylabel("")
    cax = fig.add_axes([0.92, 0.12, 0.015, 0.58])
    cb = fig.colorbar(im, cax=cax)
    cb.set_label("survival probability", fontsize=8.5)
    cb.set_ticks([0.0, 0.5, 1.0])
    fig.subplots_adjust(left=0.06, right=0.90, top=0.92, bottom=0.12)
    fig.savefig(path)
    plt.close(fig)


def draw_single(N, sig, surv, path, numbers):
    fig = plt.figure(figsize=(3.2, 4.0))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 3.4], hspace=0.14)
    ax_bar = fig.add_subplot(gs[0])
    ax = fig.add_subplot(gs[1])
    im = _panel(ax_bar, ax, surv, N, sig, numbers=numbers)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="6%", pad=0.08)
    cb = fig.colorbar(im, cax=cax)
    cb.set_ticks([0.0, 0.5, 1.0])
    fig.savefig(path)
    plt.close(fig)


if __name__ == "__main__":
    worst = 0.0
    for N in (10, 20):
        survs = []
        for sig in SIGS:
            pi = solve_pi(N, sig)
            exact = diagonal_closed_form(N, sig)
            worst = max(worst, float(np.max(np.abs(np.diag(pi) - exact))))
            surv = 1.0 - pi
            survs.append(surv)
            name = f"repsupp_N{N}_s{sig}.pdf"
            draw_single(N, sig, surv, name, numbers=False)
            print(f"wrote {name}")
        strip = f"repsupp_N{N}.pdf"
        draw_strip(N, survs, strip, numbers=False)
        print(f"wrote {strip}")
    print(f"worst |pi_jj - closed form| = {worst:.3e}")
