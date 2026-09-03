#!/usr/bin/env python3
"""Generate overlay_rel_diff: relative free-particle discrepancy.

Written from scratch in Phase C; the original had no generation script and was
placed at 33% of native size.  Six scenarios kept, because the spread across
scenarios is this figure's content."""
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

PDF_PATH = WORKDIR.parents[1] / "overlay_rel_diff.pdf"
PNG_PATH = WORKDIR / "preview.png"

RENEWAL = dict(color=style_rc.BLUE, linewidth=1.9, linestyle="-")
CLASSIC = dict(color=style_rc.VERMILLION, linewidth=1.8, linestyle="--")
NAIVE = dict(color=style_rc.TEAL, linewidth=1.6, linestyle=":")
LBL_R = "renewal"
LBL_C = r"classical BMVR, matched at $r=0$"


def run_asserts():
    out = []
    for s in SC.SCENARIOS:
        t, (I, V), (Ic, Vc) = s.solve()
        rel = np.abs(V - Vc) / np.max(V)
        assert np.all(np.isfinite(rel)) and rel[0] < 1e-9
        out.append((s, t, rel))
    return out


def make_figure(rows):
    fig, axes = plt.subplots(2, 3, figsize=(5.89, 3.45))
    for ax, (s, t, rel) in zip(axes.flat, rows):
        ax.plot(t, rel, color=style_rc.BLUE, linewidth=1.8)
        ax.fill_between(t, 0.0, rel, color=style_rc.BLUE, alpha=0.13, linewidth=0.0)
        ax.set_xlim(0.0, s.t_max)
        ax.set_ylim(0.0, max(rel.max() * 1.18, 1e-3))
        style_rc.panel_label(ax, f"({s.tag})")
        ax.text(0.97, 0.95, s.title + "\n" + rf"$R_0={s.R0:.2f}$",
                transform=ax.transAxes, ha="right", va="top",
                fontsize=8.0, color=style_rc.SOFT, linespacing=1.3)
    for ax in axes[1, :]:
        ax.set_xlabel(r"time $t$")
    for ax in axes[:, 0]:
        ax.set_ylabel("relative discrepancy")
    fig.tight_layout(pad=1.0, w_pad=1.6, h_pad=1.2)
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)


def main():
    rows = run_asserts()
    make_figure(rows)
    for s, t, rel in rows:
        print(f"  ({s.tag}) max relative discrepancy {rel.max():.3f}   R0={s.R0:.2f}")
    print(f"wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
