#!/usr/bin/env python3
"""R3 --- the capped removal law.

The chapter draws this figure inline with pgfplots, replacing the external
standalone-TikZ build log_plot_square.pdf.  This script is the reference: it
reproduces the same curve as a PDF and prints the expression the inline
\\addplot uses, so the two can be checked against one another.

Plotted quantity: removal = min(r, vartheta), the number of released agents
actually killed under a fixed removal budget (chapter section 4.1; source
03_fixed_removal.tex:111-114).  Range r in [0, 20], with the plan's
vartheta = 3.5; the plateau is labelled vartheta rather than by its value,
so no non-integer budget is displayed.

Self-contained: numpy and matplotlib only, style inlined.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "font.size": 9,
    "axes.linewidth": 0.6,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
    "pdf.fonttype": 42,
})

R_MAX = 20.0
THETA = 3.5

if __name__ == "__main__":
    r = np.linspace(0.0, R_MAX, 801)
    y = np.minimum(r, THETA)

    fig, ax = plt.subplots(figsize=(3.6, 2.1))
    ax.plot(r, y, color="#1f4e9c", lw=1.3)
    ax.axhline(THETA, color="#b03030", lw=0.7, ls=(0, (3, 2)))
    ax.text(R_MAX * 0.97, THETA * 1.06, r"$\vartheta$", ha="right",
            va="bottom", color="#b03030")
    ax.set_xlim(0, R_MAX)
    ax.set_ylim(0, THETA * 1.4)
    ax.set_xlabel(r"burst size $r$")
    ax.set_ylabel("removed")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.savefig("capped_removal_reference.pdf")
    plt.close(fig)

    print("wrote capped_removal_reference.pdf")
    print(r"inline pgfplots expression:  \addplot[domain=0:20]{min(x,3.5)};")
    print(f"check: removal(2)={min(2.0, THETA)}, "
          f"removal(10)={min(10.0, THETA)}")
