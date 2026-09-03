#!/usr/bin/env python3
"""Generate overlay_growth_phase: why no single constant pair will do.

Written from scratch in Phase C.  One renewal trajectory against two classical
parameter choices -- the r = 0 match and the young-cell limit -- showing that
each is right at one growth rate while the trajectory passes through many."""
from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/bdc_odes_ovl_mplconfig")

import numpy as np

WORKDIR = Path(__file__).resolve().parent
sys.path.insert(0, str(WORKDIR.parent))
sys.path.insert(0, str(WORKDIR.parents[1] / "_style"))
import style_rc  # noqa: E402
import _renewal as RN  # noqa: E402
import _scenarios as SC  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402

PDF_PATH = WORKDIR.parents[1] / "overlay_growth_phase.pdf"
PNG_PATH = WORKDIR / "preview.png"

RENEWAL = dict(color=style_rc.BLUE, linewidth=1.9, linestyle="-")
CLASSIC = dict(color=style_rc.VERMILLION, linewidth=1.8, linestyle="--")
NAIVE = dict(color=style_rc.TEAL, linewidth=1.6, linestyle=":")
LBL_R = "renewal"
LBL_C = r"classical BMVR, matched at $r=0$"


TRIPLE = (1.0, 0.0, 0.1)
GT, C, T_MAX = 0.025, 0.2, 60.0


def run_asserts():
    R = RN.Rates(*TRIPLE)
    R0 = GT * RN.V_inf(R) / C
    assert abs(R0 - 1.375) < 1e-9, R0
    t, I, V = RN.solve_renewal(R, GT, C, T_MAX, n=6001)
    p0, d0 = RN.V_inf(R) / RN.T_prod(R), 1.0 / RN.T_prod(R)
    _, Im, Vm = RN.solve_classical(p0, d0, GT, C, T_MAX, n=6001)
    # young-cell parameters: p -> delta, d -> mu + delta
    _, Iy, Vy = RN.solve_classical(TRIPLE[2], TRIPLE[1] + TRIPLE[2], GT, C,
                                   T_MAX, n=6001)
    for a in (V, Vm, Vy, I, Im, Iy):
        assert np.all(np.isfinite(a))
    return R, R0, t, (I, V), (Im, Vm), (Iy, Vy)


def make_figure(bundle):
    R, R0, t, (I, V), (Im, Vm), (Iy, Vy) = bundle
    fig, (ax_early, ax_late) = plt.subplots(1, 2, figsize=(5.89, 2.55))

    # The two matches fail at opposite ends, and the crossover happens inside
    # the first couple of time units -- invisible on a single 0..60 window.
    for ax, t_hi in ((ax_early, 6.0), (ax_late, T_MAX)):
        m = t <= t_hi
        ax.plot(t[m], V[m], label=LBL_R, **RENEWAL)
        ax.plot(t[m], Vm[m], label=LBL_C, **CLASSIC)
        ax.plot(t[m], Vy[m], label=r"classical, young-cell $p=\delta$",
                color=style_rc.PURPLE, linewidth=1.7, linestyle="-.")
        ax.set_yscale("log")
        ax.set_xlabel(r"time $t$")
        ax.set_xlim(0.0, t_hi)

    ax_early.set_ylim(2e-2, 30.0)
    ax_late.set_ylim(2e-3, 400.0)
    ax_early.set_ylabel(r"free particles $\mathcal{V}(t)$")
    ax_early.text(0.97, 0.05, "the $r=0$ match\novershoots here",
                  transform=ax_early.transAxes, ha="right", va="bottom",
                  fontsize=8.0, color=style_rc.SOFT, linespacing=1.3,
                 bbox=dict(boxstyle="round,pad=0.16", facecolor="white",
                            edgecolor="none", alpha=0.86))
    ax_late.text(0.97, 0.05, "the young-cell match\nhas collapsed here",
                 transform=ax_late.transAxes, ha="right", va="bottom",
                 fontsize=8.0, color=style_rc.SOFT, linespacing=1.3,
                  bbox=dict(boxstyle="round,pad=0.16", facecolor="white",
                            edgecolor="none", alpha=0.86))
    style_rc.panel_label(ax_early, "(a)")
    style_rc.panel_label(ax_late, "(b)")

    handles, labels = ax_early.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=3,
               bbox_to_anchor=(0.5, 1.005), columnspacing=1.6, fontsize=8.3)
    fig.tight_layout(pad=1.0, w_pad=1.9, rect=(0, 0, 1, 0.90))
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)


def main():
    bundle = run_asserts()
    make_figure(bundle)
    print(f"  triple={TRIPLE} gT={GT} c={C}  R0={bundle[1]:.3f}")
    print(f"wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
