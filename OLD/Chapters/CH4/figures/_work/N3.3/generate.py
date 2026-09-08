#!/usr/bin/env python3
"""Multi-founder non-fixation: I^k - D^k versus the naive power (I-D)^k."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

STYLE_DIR = Path(__file__).resolve().parents[2] / "_style"
sys.path.insert(0, str(STYLE_DIR))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
PDF_PATH = HERE.parents[2] / "figures" / "F4_multi_founder.pdf"
PNG_PATH = HERE / "preview.png"

LAMBDA, MU, DELTA = 1.0, 0.2, 0.05
KS = (1, 2, 3, 5)


def roots(lam, mu, delta):
    eta = (lam + mu + delta) / (2.0 * lam)
    spread = np.sqrt(eta**2 - mu / lam)
    return float(eta + spread), float(eta - spread)


def single_founder(t):
    a, b = roots(LAMBDA, MU, DELTA)
    A, B = a - 1.0, 1.0 - b
    decay = np.exp(-LAMBDA * (a - b) * t)
    I = (a * B * decay + b * A) / (B * decay + A)
    D = a * b * (1.0 - decay) / (a - b * decay)
    return I, D


def main() -> None:
    t = np.linspace(0.0, 15.0, 2001)
    I, D = single_founder(t)
    Ifix = I - D
    true_k2 = I**2 - D**2
    false_k2 = Ifix**2
    gap = true_k2 - false_k2
    assert float(gap.max()) > 1e-2

    colours = {1: style_rc.BLUE, 2: style_rc.VERMILLION, 3: "#6b4c9a", 5: style_rc.INK}
    styles = {1: "-", 2: "--", 3: "-.", 5: (0, (1.2, 1.5))}

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(7.4, 3.3), sharex=True, sharey=True)
    for k in KS:
        ax_a.plot(t, I**k - D**k, color=colours[k], linestyle=styles[k],
                  linewidth=1.4, label=rf"$k={k}$")
    ax_a.set_xlabel(r"$t$")
    ax_a.set_ylabel(r"$I_{\mathrm{fix},k}(t)$")
    ax_a.legend(title="founders", loc="upper right", ncol=2, fontsize=7.5)
    ax_a.text(0.04, 0.08, r"(a)", transform=ax_a.transAxes)

    ax_b.fill_between(t, false_k2, true_k2, color="#6b4c9a", alpha=0.15, zorder=1)
    ax_b.plot(t, true_k2, color=style_rc.BLUE, linewidth=1.5,
              label=r"$I^2-D^2$", zorder=3)
    ax_b.plot(t, false_k2, color=style_rc.VERMILLION, linestyle="--", linewidth=1.4,
              label=r"$(I-D)^2$", zorder=3)
    ax_b.set_xlabel(r"$t$")
    ax_b.legend(loc="upper right")
    ax_b.text(0.04, 0.08, r"(b)", transform=ax_b.transAxes)

    for ax in (ax_a, ax_b):
        ax.set_xlim(0.0, 15.0)
        ax.set_ylim(0.0, 1.03)
        style_rc.tidy(ax)

    fig.tight_layout(w_pad=1.6)
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)
    print(f"max gap={float(gap.max()):.4f}; wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
