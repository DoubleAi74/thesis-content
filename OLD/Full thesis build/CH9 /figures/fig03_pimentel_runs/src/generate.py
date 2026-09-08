#!/usr/bin/env python3
"""Two reversals of the Pimentel chain at the physical exponent α=1."""

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

N, ALPHA, EPS, STEPS = 100, 1.0, 10.0, 800
SEEDS = (19, 3)


def main():
    fig, ax = plt.subplots(figsize=style_rc.FIGSIZE_SINGLE)
    colours = (style_rc.BLUE, style_rc.VERMILLION)
    lengths = []
    for seed, col in zip(SEEDS, colours):
        A, _ic = simulate(N, ALPHA, EPS, STEPS, seed=seed)
        t = range(len(A))
        ax.plot(t, A, color=col, lw=1.4)
        lengths.append(len(A) - 1)
    ax.set_xlabel(r"step $t$")
    ax.set_ylabel(r"count $A_t$")
    ax.set_ylim(0, N)
    fig.tight_layout()
    style_rc.save_figure(fig, OUT / "fig03.pdf", OUT / "fig03.png")
    meta = {
        "id": "fig03_pimentel_runs",
        "simulation": True,
        "parameters": {"N": N, "alpha": ALPHA, "epsilon": EPS, "steps_cap": STEPS},
        "seeds": list(SEEDS),
        "absorption_times": lengths,
    }
    (OUT / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print("wrote", OUT / "fig03.pdf", "lengths", lengths)


if __name__ == "__main__":
    main()
