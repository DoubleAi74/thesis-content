#!/usr/bin/env python3
"""Rebuild Figures 2.17 and 2.18 at their printed size, with axis labels.

The curves are the binary Galton--Watson survival probabilities. One lineage
obeys S_0 = 1 and S_{n+1} = 2 p S_n - p S_n^2, and a founding cohort of size k
survives with probability S^{(k)}_n = 1 - (1 - S_n)^k.

main.tex is A4 with 1 inch margins. Figure 2.17 is included at 0.52\\textwidth
and each panel of Figure 2.18 at 0.44\\textwidth. The PDFs are drawn at those
widths, so a point here is a point on the page.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent

# A4 width minus the two 1 inch margins in main.tex.
TEXTWIDTH_IN = (595.276 - 2 * 72) / 72
WIDTH_CRITICAL = 0.52 * TEXTWIDTH_IN
WIDTH_PANEL = 0.44 * TEXTWIDTH_IN

# Axes box of the original PNGs (pixels). Kept so the curves keep their shape.
ORIG_AX_W = 335
ORIG_AX_H = 218

LABEL_PT = 12
TICK_PT = 10
KS = (1, 10, 100, 1000)
N_MAX = 500
# Matplotlib tab10, in plot order. Later curves are drawn on top.
COLOURS = ("#1f77b4", "#ff7f0e", "#2ca02c", "#d62728")

plt.rcParams.update(
    {
        "text.usetex": True,
        "font.family": "serif",
        "text.latex.preamble": r"\usepackage{lmodern}\usepackage{amsmath}",
        "axes.linewidth": 0.8,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "xtick.major.size": 3.5,
        "ytick.major.size": 3.5,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)


def cohort_survival(p, n_max=N_MAX, ks=KS):
    s = np.empty(n_max + 1)
    s[0] = 1.0
    for n in range(n_max):
        s[n + 1] = 2 * p * s[n] - p * s[n] ** 2
    n = np.arange(n_max + 1)
    # 1 - (1-s)^k. Clip the tiny negative that float error can leave at s=1.
    base = np.clip(1.0 - s, 0.0, 1.0)
    return n, {k: 1.0 - base**k for k in ks}


def draw(path, p, printed_w):
    # Margins in inches, sized for a 12 pt label and 10 pt tick numbers.
    left, right = 0.70, 0.07
    bottom, top = 0.50, 0.07
    axes_w = printed_w - left - right
    axes_h = axes_w * ORIG_AX_H / ORIG_AX_W
    printed_h = axes_h + bottom + top

    # Marker diameter matches the original circles as a fraction of the axes.
    marker_pt = (7 / ORIG_AX_H) * axes_h * 72

    fig = plt.figure(figsize=(printed_w, printed_h))
    ax = fig.add_axes(
        [
            left / printed_w,
            bottom / printed_h,
            axes_w / printed_w,
            axes_h / printed_h,
        ]
    )

    n, curves = cohort_survival(p)
    for k, colour in zip(KS, COLOURS):
        ax.plot(
            n,
            curves[k],
            linestyle="none",
            marker="o",
            markersize=marker_pt,
            markeredgewidth=0,
            color=colour,
            clip_on=True,
        )

    # Same window as the original figures: default 5% margins on n=0..500, S in [0, 1].
    ax.set_xlim(-25, 525)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xticks([0, 100, 200, 300, 400, 500])
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter("%.1f"))

    ax.set_xlabel(r"generation $n$", fontsize=LABEL_PT, labelpad=3)
    ax.set_ylabel(r"$S^{(k)}_n$", fontsize=LABEL_PT, labelpad=6)
    ax.tick_params(axis="both", labelsize=TICK_PT)

    fig.savefig(path)
    plt.close(fig)


def main():
    draw(HERE / "kvals.pdf", 0.5, WIDTH_CRITICAL)
    draw(HERE / "kvals505.pdf", 0.505, WIDTH_PANEL)
    draw(HERE / "kvals495.pdf", 0.495, WIDTH_PANEL)


if __name__ == "__main__":
    main()
