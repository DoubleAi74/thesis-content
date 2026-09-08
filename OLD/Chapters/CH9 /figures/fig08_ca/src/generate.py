#!/usr/bin/env python3
"""The founder species of the multiplicative-dissipation automaton, followed
from its first cell to the burst that ends it.

Data comes from src/founder.js, which drives the model's own simulation core
(src/sim.js, lifted verbatim from the page) headless at seed 20260903.
Symbols follow the chapter, not the page: energy V_i, cost per sub-species c,
inflow per cell phi.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "figures" / "_style"))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent

SEED = 20260903
PHI, C = 0.0316, 0.2884   # per-cell inflow, cost per sub-species


def main() -> None:
    d = np.genfromtxt(HERE / "founder.dat", names=True)
    t, V, X, N, balance = d["t"], d["alpha"], d["X"], d["N"], d["balance"]
    t_burst = float(t[-1])
    i_peak = int(np.argmax(V))

    fig, (ax0, ax1) = plt.subplots(
        2, 1, figsize=(5.6, 4.0), sharex=True, layout="constrained",
        gridspec_kw={"hspace": 0.08},
    )

    ax0.plot(t, V, color=style_rc.BLUE, lw=1.4)
    ax0.set_ylabel(r"energy $V_i$")
    ax0.set_ylim(0, 850)

    ax1.plot(t, balance, color=style_rc.SOFT, lw=1.1, ls="--",
             label=r"$\varphi N_i/c$")
    ax1.plot(t, X, color=style_rc.VERMILLION, lw=1.4, label=r"$X_i$")
    ax1.set_ylabel("sub-species")
    ax1.set_xlabel(r"time $t$ (sweeps)")
    ax1.set_xlim(0, t_burst)
    ax1.set_ylim(0, 1100)
    ax1.legend(loc="upper left")

    for ax in (ax0, ax1):
        ax.axvline(t_burst, color=style_rc.CATA, lw=1.0, ls=":")

    style_rc.save_figure(fig, OUT / "fig08.pdf", OUT / "fig08.png")
    plt.close(fig)

    (OUT / "meta.json").write_text(json.dumps({
        "id": "fig08_ca",
        "simulation": True,
        "seed": SEED,
        "lattice": 256,
        "frame_events": 80000,
        "parameters": {"phi": PHI, "c": C, "defaults": "page defaults"},
        "burst_time": t_burst,
        "peak_energy": float(V[i_peak]),
        "peak_time": float(t[i_peak]),
        "final": {"V": float(V[-1]), "X": float(X[-1]), "N": float(N[-1])},
    }, indent=2) + "\n")
    print(f"burst t={t_burst}  peak V={V[i_peak]:.0f} at t={t[i_peak]:.0f}  "
          f"final X={X[-1]:.0f} N={N[-1]:.0f}")


if __name__ == "__main__":
    main()
