#!/usr/bin/env python3
"""One Pimentel realisation with the moving critical state overlaid."""

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

N, ALPHA, EPS, STEPS, SEED = 10_000, 3.0, 1.0, 400_000, 3


def main():
    A, ic = simulate(N, ALPHA, EPS, STEPS, seed=SEED)
    t = range(len(A))
    fig, ax = plt.subplots(figsize=style_rc.FIGSIZE_SINGLE)
    ax.plot(t, A, color=style_rc.BLUE, lw=1.3, label=r"$A_t$")
    ax.plot(t, ic, color=style_rc.CATA, lw=1.2, label=r"$i_{c,t}$")
    ax.set_xlabel(r"step $t$")
    ax.set_ylabel(r"count")
    ax.set_ylim(0, N)
    ax.legend(loc="best")
    fig.tight_layout()
    style_rc.save_figure(fig, OUT / "fig05.pdf", OUT / "fig05.png")
    meta = {
        "id": "fig05_pimentel_icrit",
        "simulation": True,
        "parameters": {"N": N, "alpha": ALPHA, "epsilon": EPS, "steps_cap": STEPS},
        "seed": SEED,
        "length": int(len(A) - 1),
    }
    (OUT / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print("wrote", OUT / "fig05.pdf", "length", len(A) - 1)


if __name__ == "__main__":
    main()
