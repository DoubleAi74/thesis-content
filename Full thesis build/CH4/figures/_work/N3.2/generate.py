#!/usr/bin/env python3
"""J, V and K as algebraic functions of I along the Riccati trajectory."""

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
PDF_PATH = WORKDIR.parents[2] / "figures/F4_I_economy.pdf"
PNG_PATH = WORKDIR / "preview.png"

LAMBDA, MU, DELTA = 1.0, 0.2, 0.05


def roots(lam, mu, delta):
    eta = (lam + mu + delta) / (2.0 * lam)
    radical = np.sqrt(eta**2 - mu / lam)
    return eta + radical, eta - radical


def moments_from_I(I, lam=LAMBDA, mu=MU, delta=DELTA):
    a, b = roots(lam, mu, delta)
    values = np.asarray(I, dtype=float)
    J = -(lam / delta) * (values - a) * (values - b)
    V = (1.0 - values) * (1.0 + (lam / delta) * (1.0 - values))
    K = (1.0 + (2.0 * lam / delta) * (1.0 - values)) * J
    return J, V, K


def main() -> None:
    _, b = roots(LAMBDA, MU, DELTA)
    I = np.linspace(1.0, b, 2001)
    J, V, K = moments_from_I(I)
    v_inf = float(V[-1])
    assert abs(float(J[0]) - 1.0) < 2e-13
    assert abs(float(V[-1]) - v_inf) < 2e-13

    fig, ax = plt.subplots(figsize=(5.8, 3.7))
    ax.plot(I, J, color=style_rc.BLUE, linewidth=1.5, label=r"$J(I)$")
    ax.plot(I, V, color=style_rc.VERMILLION, linewidth=1.5,
            linestyle=(0, (5, 2)), label=r"$V(I)$")
    ax.plot(I, K, color=style_rc.INK, linewidth=1.5,
            linestyle=(0, (4, 2, 1.2, 2)), label=r"$K(I)$")
    ax.set_yscale("symlog", linthresh=1.0, linscale=0.9, base=10)
    ax.set_yticks([0.0, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0])
    ax.set_yticklabels(["0", "1", "2", "5", "10", "20", "50"])
    ax.set_xlim(1.0, b)
    ax.set_ylim(0.0, 95.0)
    ax.set_xlabel(r"non-catastrophe probability $I$ (decreases with time)")
    ax.set_ylabel("moment value")
    ax.scatter([1.0], [1.0], s=22, facecolors="white",
               edgecolors=style_rc.BLUE, linewidths=1.1, zorder=5, clip_on=False)
    ax.scatter([b], [v_inf], s=22, facecolors="white",
               edgecolors=style_rc.VERMILLION, linewidths=1.1, zorder=5, clip_on=False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=3)
    style_rc.tidy(ax)
    fig.tight_layout(rect=(0.0, 0.06, 1.0, 1.0))
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)
    print(f"wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
