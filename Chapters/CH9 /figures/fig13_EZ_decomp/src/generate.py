#!/usr/bin/env python3
"""Decomposition of E(Z) into mean burst size and the second-phase map."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "figures" / "_style"))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402

# Import closed forms from fig12's generator.
sys.path.insert(0, str(ROOT / "figures" / "fig12_EZ" / "src"))
from generate import EZ, mean_burst  # noqa: E402

OUT = Path(__file__).resolve().parents[1]


def main():
    d = np.linspace(1e-4, 0.20, 400)
    burst = mean_burst(d)
    ez = EZ(d)

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=style_rc.FIGSIZE_DOUBLE)

    ax0.plot(d, burst, color=style_rc.BLUE, lw=1.8)
    ax0.set_xlabel(r"catastrophe rate $\delta_1$")
    ax0.set_ylabel(r"mean burst size $\mathbb{E}(\mathcal{K})$")
    ax0.set_xlim(0.0, 0.20)
    ax0.set_yscale("log")

    ax1.plot(burst, ez, color=style_rc.BLUE, lw=1.8)
    ax1.axhline(1.0, color=style_rc.CATA, lw=1.0)
    ax1.set_xlabel(r"mean burst size $\mathbb{E}(\mathcal{K})$")
    ax1.set_ylabel(r"host-to-host mean $\mathbb{E}(Z)$")
    ax1.set_xscale("log")
    ax1.set_ylim(0.55, 1.85)

    fig.tight_layout()
    style_rc.save_figure(fig, OUT / "fig13.pdf", OUT / "fig13.png")
    print("wrote", OUT / "fig13.pdf")


if __name__ == "__main__":
    main()
