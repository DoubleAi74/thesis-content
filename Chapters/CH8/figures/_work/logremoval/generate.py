#!/usr/bin/env python3
"""R2 --- the logarithmic casualty law.

The chapter draws this figure inline with pgfplots, replacing the external
standalone-TikZ build log_plot1.pdf.  This script is the reference: it
reproduces the same curve as a PDF and prints the expression the inline
\\addplot uses, so the two can be checked against one another.

Plotted quantity: the casualty count vartheta(r) = log(r+1), the number of
released agents removed by killer cells as a function of burst size r
(chapter section 4.1; source 03_fixed_removal.tex:94).  Range r in [0, 50].

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

R_MAX = 50.0

if __name__ == "__main__":
    r = np.linspace(0.0, R_MAX, 501)
    y = np.log(r + 1.0)

    fig, ax = plt.subplots(figsize=(3.6, 2.1))
    ax.plot(r, y, color="#1f4e9c", lw=1.3)
    ax.set_xlim(0, R_MAX)
    ax.set_ylim(0, np.log(R_MAX + 1.0) * 1.05)
    ax.set_xlabel(r"burst size $r$")
    ax.set_ylabel("casualties")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.savefig("log_removal_reference.pdf")
    plt.close(fig)

    print("wrote log_removal_reference.pdf")
    print(r"inline pgfplots expression:  \addplot[domain=0:50]{ln(x+1)};")
    print(f"check: vartheta(0)={np.log(1.0):.6f}, "
          f"vartheta(10)={np.log(11.0):.6f}, "
          f"vartheta(50)={np.log(51.0):.6f}")
