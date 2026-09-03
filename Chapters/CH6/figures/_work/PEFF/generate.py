#!/usr/bin/env python3
"""Generate peff_dr_curves: the effective-parameter map over its full range.

Written from scratch in Phase C: the original figure had no generation script
anywhere in the tree, and was placed at 43% of its native size.

Two changes of substance over the figure it replaces.  It is drawn over the
whole admissible range r > -theta rather than only r >= 0, because r = 0 is an
interior point of the map, not an end: negative r is a decaying infection, and
the chapter's own overlay scenarios include one.  And it marks the third
endpoint, the old-cell limit

    p_eff(r) -> delta * E_QS[X^2] = delta a(a+1)/(a-1)^2   as r -> -theta,

which pairs with the young-cell limit delta and fixes the full dynamic range of
a fitted release rate at exactly E_QS[X^2].
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/bdc_odes_peff_mplconfig")

import numpy as np

WORKDIR = Path(__file__).resolve().parent
sys.path.insert(0, str(WORKDIR.parent))
sys.path.insert(0, str(WORKDIR.parents[1] / "_style"))
import style_rc  # noqa: E402
import _renewal as RN  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402

PDF_PATH = WORKDIR.parents[1] / "peff_dr_curves.pdf"
PNG_PATH = WORKDIR / "preview.png"

SETS = [((1.0, 0.0, 0.1), style_rc.BLUE, "-"),
        ((1.0, 0.2, 0.05), style_rc.PURPLE, "--"),
        ((1.0, 0.9, 0.1), style_rc.VERMILLION, "-.")]

R_MAX = 3.0


def run_asserts():
    """The three endpoints, checked against their closed forms."""
    out = []
    for (l, m, d), _, _ in SETS:
        R = RN.Rates(l, m, d)
        old = RN.p_eff_old_cell(R)
        # g/S at large age must equal the old-cell limit
        Ifix, g = RN.kernels(R, np.array([80.0 / R.theta]))
        assert abs(g[0] / Ifix[0] - old) / old < 1e-9, (l, m, d)
        # r = 0 endpoint is lifetime yield over lifetime
        p0 = RN.p_eff(R, 0.0)
        assert abs(p0 - RN.V_inf(R) / RN.T_prod(R)) / p0 < 1e-9
        # young-cell endpoint
        assert abs(RN.p_eff(R, 600.0) - d) / d < 2e-2
        assert abs(RN.d_eff(R, 600.0) - (m + d)) / (m + d) < 2e-2
        out.append(dict(rates=(l, m, d), theta=R.theta, old=old, p0=p0,
                        d0=RN.d_eff(R, 0.0), young_p=d, young_d=m + d,
                        span=old / d))
    return out


def make_figure(checked):
    fig, (ax_p, ax_d) = plt.subplots(1, 2, figsize=(5.89, 2.6))

    for ((l, m, d), colour, ls), info in zip(SETS, checked):
        R = RN.Rates(l, m, d)
        th = R.theta
        # sample densely near the left edge, where the map turns over fastest
        left = -th * (1.0 - np.geomspace(3e-5, 1.0, 140))
        right = np.linspace(1e-6, R_MAX, 90)
        rs = np.concatenate([left[:-1], right])
        pe = np.array([RN.p_eff(R, r) for r in rs])
        de = np.array([RN.d_eff(R, r) for r in rs])
        lab = rf"$({l:g},{m:g},{d:g})$"

        ax_p.plot(rs, pe, color=colour, linestyle=ls, linewidth=1.9, label=lab)
        ax_d.plot(rs, de, color=colour, linestyle=ls, linewidth=1.9, label=lab)

        # Asymptotes as short segments at the edge each curve runs toward,
        # rather than six full-width rules across the panel.
        ax_p.plot([-1.25, -th + 0.10], [info["old"]] * 2, color=colour,
                  linewidth=0.9, linestyle=":", alpha=0.9)
        ax_p.plot([2.0, R_MAX], [d] * 2, color=colour,
                  linewidth=0.9, linestyle=":", alpha=0.9)
        ax_d.plot([2.0, R_MAX], [m + d] * 2, color=colour,
                  linewidth=0.9, linestyle=":", alpha=0.9)
        ax_p.plot([0.0], [info["p0"]], marker="o", ms=4.2, mfc="white",
                  mec=colour, mew=1.3, zorder=6)
        ax_d.plot([0.0], [info["d0"]], marker="o", ms=4.2, mfc="white",
                  mec=colour, mew=1.3, zorder=6)

    for ax in (ax_p, ax_d):
        ax.axvline(0.0, color=style_rc.INK, linewidth=0.8, alpha=0.45)
        ax.set_xlim(-1.25, R_MAX)
        ax.set_xlabel(r"epidemic growth rate $r$")

    ax_p.set_yscale("log")
    ax_p.set_ylabel(r"effective release rate $p_{\rm eff}(r)$")
    ax_p.set_ylim(0.017, 260.0)
    ax_d.set_ylabel(r"effective removal rate $d_{\mathcal{I},\rm eff}(r)$")
    ax_d.set_ylim(0.0, 1.35)

    ax_p.text(-1.13, 190.0, "old-cell limit", fontsize=8.0,
              color=style_rc.SOFT, ha="left", va="center")
    ax_p.text(R_MAX - 0.06, 0.026, "young-cell limit", fontsize=8.0,
              color=style_rc.SOFT, ha="right", va="center")
    ax_p.annotate(r"$r=0$", xy=(0.0, 0.20), xytext=(5, 0),
                  textcoords="offset points", fontsize=8.0,
                  color=style_rc.SOFT, ha="left", va="bottom")

    ax_p.legend(loc="upper right", fontsize=8.0, handlelength=2.4,
                title=r"$(\lambda,\mu,\delta)$", title_fontsize=8.0)
    style_rc.panel_label(ax_p, "(a)")
    style_rc.panel_label(ax_d, "(b)")
    fig.tight_layout(pad=1.0, w_pad=1.8)
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)


def main():
    checked = run_asserts()
    make_figure(checked)
    for info in checked:
        print(f"  {info['rates']}: theta={info['theta']:.4f}  "
              f"p_eff: old {info['old']:.4f} -> r=0 {info['p0']:.4f} -> young {info['young_p']:.4f}"
              f"   dynamic range x{info['span']:.1f}")
    print(f"wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
