#!/usr/bin/env python3
"""Generate overlay_V_with_naive: what the dimensional error looks like.

Written from scratch in Phase C, and demoted to the verification appendix: the
naive proposal p = <X>_QS is worth one appendix figure, not a body float."""
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

PDF_PATH = WORKDIR.parents[1] / "overlay_V_with_naive.pdf"
PNG_PATH = WORKDIR / "preview.png"

RENEWAL = dict(color=style_rc.BLUE, linewidth=1.9, linestyle="-")
CLASSIC = dict(color=style_rc.VERMILLION, linewidth=1.8, linestyle="--")
NAIVE = dict(color=style_rc.TEAL, linewidth=1.6, linestyle=":")
LBL_R = "renewal"
LBL_C = r"classical BMVR, matched at $r=0$"


TAGS = ["a", "b"]


def run_asserts():
    out = []
    for tag in TAGS:
        s = SC.BY_TAG[tag]
        R = s.rates
        t, (I, V), (Ic, Vc) = s.solve()
        # the naive proposal: the quasi-stationary mean load, a pure count,
        # substituted for a rate
        p_naive = R.a / (R.a - 1.0)
        _, In, Vn = RN.solve_classical(p_naive, 1.0 / RN.T_prod(R), s.gT, s.c,
                                       s.t_max, I0=s.I0, V0=s.V0)
        assert np.all(np.isfinite(Vn))
        out.append((s, t, V, Vc, Vn, p_naive))
    return out


def make_figure(rows):
    fig, axes = plt.subplots(1, 2, figsize=(4.89, 2.4))
    for ax, (s, t, V, Vc, Vn, p_naive) in zip(axes, rows):
        ax.plot(t, V, label=LBL_R, **RENEWAL)
        ax.plot(t, Vc, label=LBL_C, **CLASSIC)
        ax.plot(t, Vn, label=r"classical, $p=\langle X\rangle_{\rm QS}$", **NAIVE)
        ax.set_yscale("log")
        ax.set_xlabel(r"time $t$")
        ax.set_xlim(0.0, s.t_max)
        ax.set_ylim(1e-3, max(V.max(), Vn.max()) * 5)
        style_rc.panel_label(ax, f"({s.tag})")
        ax.text(0.03, 0.97, s.title, transform=ax.transAxes, ha="left",
                va="top", fontsize=8.0, color=style_rc.SOFT)
    axes[0].set_ylabel(r"free particles $\mathcal{V}(t)$")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2,
               bbox_to_anchor=(0.5, 1.005), columnspacing=1.8, fontsize=8.3)
    fig.tight_layout(pad=1.0, w_pad=1.8, rect=(0, 0, 1, 0.84))
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)


def main():
    rows = run_asserts()
    make_figure(rows)
    for s, t, V, Vc, Vn, p_naive in rows:
        print(f"  ({s.tag}) naive p = <X>_QS = {p_naive:.4f} against "
              f"p_eff(0) = {s.matched[0]:.4f}")
    print(f"wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
