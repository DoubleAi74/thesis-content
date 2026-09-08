#!/usr/bin/env python3
"""R4 --- lifetime yield against the catastrophe rate. Writes vinf_delta.pdf."""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_style"))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402

LAM, MU = 0.8, 0.0


def roots(lam, mu, delta):
    eta = (lam + mu + delta) / (2.0 * lam)
    disc = np.sqrt(eta ** 2 - mu / lam)
    return eta + disc, eta - disc


def v_infty(lam, mu, delta):
    a, b = roots(lam, mu, delta)
    return a * (1.0 - b) / (a - 1.0)


if __name__ == "__main__":
    delta = np.linspace(0.1, 2.5, 601)
    v = v_infty(LAM, MU, delta)
    fig, ax = plt.subplots(figsize=(5.6, 2.8))
    ax.plot(delta, v, color=style_rc.BLUE, lw=1.5,
            label=r"$V_\infty(\delta)=\mathcal{R}(0)$")
    ax.axhline(1.0, color=style_rc.SOFT, lw=0.8, ls=(0, (3, 2)))
    ax.text(2.35, 0.55, r"$y=1$", ha="right", va="top",
            fontsize=8.5, color=style_rc.SOFT)
    ax.set_xlim(0, 2.5)
    ax.set_ylim(0, 10)
    ax.set_xlabel(r"catastrophe rate $\delta$")
    ax.set_ylabel(r"expected release per cell")
    ax.legend(loc="upper right")
    fig.savefig("vinf_delta.pdf")
    plt.close(fig)
    print("wrote vinf_delta.pdf")
    for d in (0.1, 0.5, 0.8, 2.0):
        print(f"  delta={d:4.2f}  V_inf={v_infty(LAM, MU, d):.6f}"
              f"   (closed form 1+lam/delta = {1.0 + LAM / d:.6f})")
