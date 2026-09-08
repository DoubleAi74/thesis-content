#!/usr/bin/env python3
"""Two birth–plague realisations at the source parameter point."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "figures" / "_style"))
import style_rc  # noqa: E402
from plague import simulate  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parents[1]

LAM, DELTA, CHI, MU = 1.0, 0.1, 0.02, 10.0
TMAX, X0, Y0 = 20.0, 80, 4
SEEDS = (2, 8)


def main():
    fig, axes = plt.subplots(1, 2, figsize=style_rc.FIGSIZE_DOUBLE, sharey=True)
    for ax, seed in zip(axes, SEEDS):
        t, X, Y = simulate(LAM, DELTA, CHI, MU, TMAX, X0=X0, Y0=Y0, seed=seed)
        ax.plot(t, X, color=style_rc.BLUE, lw=1.3, label=r"$X_t$")
        ax.plot(t, Y, color=style_rc.VERMILLION, lw=1.3, label=r"$Y_t$")
        ax.set_xlabel(r"time $t$")
        ax.set_xlim(0, TMAX)
    axes[0].set_ylabel("count")
    axes[0].legend(loc="upper left")
    fig.tight_layout()
    style_rc.save_figure(fig, OUT / "fig09.pdf", OUT / "fig09.png")
    meta = {
        "id": "fig09_plague_paths",
        "simulation": True,
        "parameters": {
            "lambda": LAM,
            "delta": DELTA,
            "chi": CHI,
            "mu": MU,
            "t_max": TMAX,
            "X0": X0,
            "Y0": Y0,
        },
        "seeds": list(SEEDS),
    }
    (OUT / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print("wrote", OUT / "fig09.pdf")


if __name__ == "__main__":
    main()
