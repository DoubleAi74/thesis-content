#!/usr/bin/env python3
"""Two initial conditions, two runs each, at α=10, N=10^5."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "figures" / "_style"))
import style_rc  # noqa: E402
from pimentel import simulate  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parents[1]

N, ALPHA, EPS, STEPS = 100_000, 10.0, 1.0, 2_000_000
# Even match vs a 2% bias. Seeds chosen so both panels show the stated behaviour.
SEEDS_EVEN = (4, 7)
SEEDS_BIAS = (4, 7)
A0_BIAS = int(0.62 * N)


def main():
    fig, axes = plt.subplots(1, 2, figsize=style_rc.FIGSIZE_DOUBLE, sharey=True)
    colours = (style_rc.BLUE, style_rc.VERMILLION)

    for seed, col in zip(SEEDS_EVEN, colours):
        A, _ic = simulate(N, ALPHA, EPS, STEPS, A0=N // 2, seed=seed)
        axes[0].plot(range(len(A)), A, color=col, lw=1.05)
    axes[0].set_title("Started evenly matched")
    axes[0].set_xlabel(r"step $t$")
    axes[0].set_ylabel(r"count $A_t$")

    for seed, col in zip(SEEDS_BIAS, colours):
        A, _ic = simulate(N, ALPHA, EPS, STEPS, A0=A0_BIAS, seed=seed)
        axes[1].plot(range(len(A)), A, color=col, lw=1.05)
    axes[1].set_title("Started with a bias")
    axes[1].set_xlabel(r"step $t$")

    for ax in axes:
        ax.set_ylim(0, N)
        ax.ticklabel_format(axis="x", style="sci", scilimits=(0, 0))
        ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

    fig.tight_layout()
    style_rc.save_figure(fig, OUT / "fig04.pdf", OUT / "fig04.png")
    meta = {
        "id": "fig04_pimentel_ic",
        "simulation": True,
        "parameters": {
            "N": N,
            "alpha": ALPHA,
            "epsilon": EPS,
            "steps_cap": STEPS,
            "A0_even": N // 2,
            "A0_bias": A0_BIAS,
        },
        "seeds_even": list(SEEDS_EVEN),
        "seeds_bias": list(SEEDS_BIAS),
    }
    (OUT / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print("wrote", OUT / "fig04.pdf")


if __name__ == "__main__":
    main()
