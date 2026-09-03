#!/usr/bin/env python3
"""Generate overlay_V: the renewal system against classical BMVR.

Written from scratch in Phase C.  It replaces two separate six-panel figures
(overlay_V and overlay_I), each of which was placed at 33% of its native size
and was unreadable in print.  Two scenarios, both state variables, one figure:
the point the pair was making is that the discrepancy is not confined to the
release equation, and that reads more directly from a 2x2 than from twelve
illegible panels."""
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

PDF_PATH = WORKDIR.parents[1] / "overlay_V.pdf"
PNG_PATH = WORKDIR / "preview.png"

RENEWAL = dict(color=style_rc.BLUE, linewidth=1.9, linestyle="-")
CLASSIC = dict(color=style_rc.VERMILLION, linewidth=1.8, linestyle="--")
NAIVE = dict(color=style_rc.TEAL, linewidth=1.6, linestyle=":")
LBL_R = "renewal"
LBL_C = r"classical BMVR, matched at $r=0$"


COLS = ["a", "d"]          # supercritical, subcritical


def run_asserts():
    out = []
    for tag in COLS:
        s = SC.BY_TAG[tag]
        t, (I, V), (Ic, Vc) = s.solve()
        assert np.all(np.isfinite(V)) and np.all(np.isfinite(I))
        assert np.all(V >= -1e-12) and np.all(I >= -1e-12)
        # supercritical solutions must grow, subcritical must decay
        if s.R0 > 1: assert V[-1] > V[len(V)//2]
        else: assert V[-1] < V[len(V)//2]
        out.append((s, t, I, V, Ic, Vc))
    return out


def make_figure(rows):
    fig, axes = plt.subplots(2, 2, figsize=(5.89, 4.05), sharex="col")
    letters = [["a", "b"], ["c", "d"]]

    for col, (s, t, I, V, Ic, Vc) in enumerate(rows):
        for row, (new, old, name) in enumerate(
                [(V, Vc, r"free particles $\mathcal{V}(t)$"),
                 (I, Ic, r"infected cells $\mathcal{I}(t)$")]):
            ax = axes[row, col]
            ax.plot(t, new, label=LBL_R, **RENEWAL)
            ax.plot(t, old, label=LBL_C, **CLASSIC)
            if s.logV:
                ax.set_yscale("log")
                lo = max(np.min(new[new > 0]) * 0.5, np.max(new) * 1e-6)
                ax.set_ylim(lo, np.max([new.max(), old.max()]) * 3.0)
            if col == 0:
                ax.set_ylabel(name)
            style_rc.panel_label(ax, f"({letters[row][col]})")
            if row == 1:
                ax.set_xlabel(r"time $t$")
        axes[0, col].text(0.5, 1.12, s.title, transform=axes[0, col].transAxes,
                          ha="center", va="bottom", fontsize=9.0)

    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2,
               bbox_to_anchor=(0.5, 1.005), columnspacing=2.2)
    fig.tight_layout(pad=1.0, w_pad=1.9, h_pad=0.9, rect=(0, 0, 1, 0.93))
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)


def main():
    rows = run_asserts()
    make_figure(rows)
    for s, *_ in rows:
        print(f"  ({s.tag}) R0={s.R0:.3f}  {s.caption_line}")
    print(f"wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
