#!/usr/bin/env python3
"""The three cell-fate probabilities I, D and I_fix from their closed forms."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

STYLE_DIR = Path(__file__).resolve().parents[2] / "_style"
sys.path.insert(0, str(STYLE_DIR))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402

WORKDIR = Path(__file__).resolve().parent
PDF_PATH = WORKDIR.parents[2] / "figures/F4_fate_probabilities.pdf"
PNG_PATH = WORKDIR / "preview.png"

LAMBDA, MU, DELTA = 1.0, 0.2, 0.05


def roots(lam, mu, delta):
    eta = (lam + mu + delta) / (2.0 * lam)
    radical = np.sqrt(eta**2 - mu / lam)
    return eta + radical, eta - radical


def quantities(t, lam, mu, delta):
    a, b = roots(lam, mu, delta)
    A, B = a - 1.0, 1.0 - b
    w = np.exp(lam * (a - b) * np.asarray(t))
    I = (a * B + b * A * w) / (B + A * w)
    D = a * b * (w - 1.0) / (a * w - b)
    I_fix = (a - b) ** 2 * w / ((B + A * w) * (a * w - b))
    return I, D, I_fix, a, b


def main() -> None:
    t = np.linspace(0.0, 15.0, 2001)
    I, D, I_fix, a, b = quantities(t, LAMBDA, MU, DELTA)
    assert a > 1.0 > b > 0.0
    assert np.allclose(I - D, I_fix, atol=2e-14)

    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    ax.plot(t, I, color=style_rc.BLUE, label=r"$I(t)$")
    ax.plot(t, D, color=style_rc.VERMILLION, label=r"$D(t)$")
    ax.plot(t, I_fix, color=style_rc.INK, label=r"$I_{\mathrm{fix}}(t)$")
    style_rc.asymptote_hline(ax, b, label=rf"$b={b:.3f}$")
    ax.set(xlim=(0.0, 15.0), ylim=(0.0, 1.0), xlabel=r"$t$", ylabel="Probability")
    ax.legend(loc="upper right")
    style_rc.tidy(ax)
    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)
    print(f"wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
