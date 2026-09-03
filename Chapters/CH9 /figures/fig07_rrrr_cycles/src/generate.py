#!/usr/bin/env python3
"""RRRR realisations: two single paths and one overlaid ensemble."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "figures" / "_style"))
import style_rc  # noqa: E402
from rrrr import simulate  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parents[1]

# Rates chosen so several cycles fit a moderate horizon, with visible amplitude.
PHI, C, LAM, DELTA, OMEGA = 4.0, 0.8, 0.5, 0.25, 0.15
TMAX = 80.0
V0, X0 = 20.0, 1
SEEDS_SINGLE = (3, 11)
SEEDS_ENS = (3, 5, 8, 11, 17)


def _plot_one(ax, t, X, V):
    ax.plot(t, X, color=style_rc.BLUE, lw=1.25, label=r"$X_t$")
    ax.plot(t, V, color=style_rc.VERMILLION, lw=1.25, label=r"$V(t)$")
    ax.set_xlabel(r"time $t$")


def main():
    fig, axes = plt.subplots(1, 2, figsize=style_rc.FIGSIZE_DOUBLE, sharey=False)
    for ax, seed in zip(axes, SEEDS_SINGLE):
        t, X, V = simulate(PHI, C, LAM, DELTA, OMEGA, TMAX, X0=X0, V0=V0, seed=seed)
        _plot_one(ax, t, X, V)
        ax.set_xlim(0, TMAX)
    axes[0].set_ylabel("count / potential")
    axes[0].legend(loc="upper right")
    fig.tight_layout()
    style_rc.save_figure(fig, OUT / "fig07a.pdf", OUT / "fig07a.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=style_rc.FIGSIZE_SINGLE)
    for i, seed in enumerate(SEEDS_ENS):
        t, X, V = simulate(PHI, C, LAM, DELTA, OMEGA, 40.0, X0=X0, V0=V0, seed=seed)
        ax.plot(t, X, color=style_rc.BLUE, lw=1.0, alpha=0.45 + 0.1 * (i == 0))
        ax.plot(t, V, color=style_rc.VERMILLION, lw=1.0, alpha=0.45 + 0.1 * (i == 0))
    ax.set_xlabel(r"time $t$")
    ax.set_ylabel("count / potential")
    ax.set_xlim(0, 40)
    fig.tight_layout()
    style_rc.save_figure(fig, OUT / "fig07b.pdf", OUT / "fig07b.png")
    plt.close(fig)

    # Combined shipping figure: two singles on top, ensemble below — actually
    # the chapter uses two floats. Emit a 2+1 panel page as fig07.pdf as well.
    fig = plt.figure(figsize=(7.6, 6.4))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.15], hspace=0.38, wspace=0.28)
    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])
    ax2 = fig.add_subplot(gs[1, :])
    for ax, seed in zip((ax0, ax1), SEEDS_SINGLE):
        t, X, V = simulate(PHI, C, LAM, DELTA, OMEGA, TMAX, X0=X0, V0=V0, seed=seed)
        _plot_one(ax, t, X, V)
        ax.set_xlim(0, TMAX)
    ax0.set_ylabel("count / potential")
    ax0.legend(loc="upper right")
    for i, seed in enumerate(SEEDS_ENS):
        t, X, V = simulate(PHI, C, LAM, DELTA, OMEGA, 40.0, X0=X0, V0=V0, seed=seed)
        ax2.plot(t, X, color=style_rc.BLUE, lw=1.0, alpha=0.5)
        ax2.plot(t, V, color=style_rc.VERMILLION, lw=1.0, alpha=0.5)
    ax2.set_xlabel(r"time $t$")
    ax2.set_ylabel("count / potential")
    ax2.set_xlim(0, 40)
    style_rc.save_figure(fig, OUT / "fig07.pdf", OUT / "fig07.png")
    meta = {
        "id": "fig07_rrrr_cycles",
        "simulation": True,
        "parameters": {
            "phi": PHI,
            "c": C,
            "lambda": LAM,
            "delta": DELTA,
            "omega": OMEGA,
            "t_max": TMAX,
            "X0": X0,
            "V0": V0,
        },
        "seeds_single": list(SEEDS_SINGLE),
        "seeds_ensemble": list(SEEDS_ENS),
    }
    (OUT / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print("wrote", OUT / "fig07.pdf")


if __name__ == "__main__":
    main()
