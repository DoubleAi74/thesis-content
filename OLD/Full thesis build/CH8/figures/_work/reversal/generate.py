#!/usr/bin/env python3
"""R6 --- flooding criterion reverses. Writes flooding_reversal.pdf."""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_style"))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402

LAM, MU = 1.0, 0.5
THETAS = (1, 3, 10)


def roots(lam, mu, delta):
    eta = (lam + mu + delta) / (2.0 * lam)
    disc = np.sqrt(eta ** 2 - mu / lam)
    return eta + disc, eta - disc


def parts(lam, mu, delta):
    a, b = roots(lam, mu, delta)
    L = a * (1.0 - b)
    v = L / (a - 1.0)
    return a, b, L, v


def r_burst(lam, mu, delta, theta):
    a, _, _, v = parts(lam, mu, delta)
    return v * a ** (-float(theta))


def r_bud(lam, mu, delta, theta):
    _, _, _, v = parts(lam, mu, delta)
    sigma = v / (1.0 + v)
    return v * sigma ** float(theta)


if __name__ == "__main__":
    delta = np.linspace(0.05, 2.0, 601)
    dstar = LAM * MU / (LAM + MU)
    fig, ax = plt.subplots(figsize=(5.8, 3.0))
    for th, col in ((1, style_rc.BLUE), (3, style_rc.TEAL), (10, style_rc.CATA)):
        gap = r_burst(LAM, MU, delta, th) - r_bud(LAM, MU, delta, th)
        ax.plot(delta, gap, color=col, lw=1.5, label=rf"$\vartheta={th}$")
    ax.axhline(0.0, color=style_rc.INK, lw=0.6)
    ax.axvline(dstar, color=style_rc.SOFT, lw=0.8, ls=(0, (3, 2)))
    ax.text(dstar + 0.04, 0.82, r"$\delta_*=\lambda\mu/(\lambda+\mu)$",
            fontsize=8.5, color=style_rc.SOFT, rotation=90, va="top")
    ax.set_xlim(0, 2.0)
    ax.set_ylim(-0.45, 0.95)
    ax.set_xlabel(r"catastrophe rate $\delta$")
    ax.set_ylabel(r"$\mathcal{R}_{\mathrm{burst}}-\mathcal{R}_{\mathrm{bud}}$")
    ax.legend(loc="lower right")
    fig.savefig("flooding_reversal.pdf")
    plt.close(fig)
    print("wrote flooding_reversal.pdf")
    print(f"  delta_* = {dstar:.9f}; "
          f"gap at delta_* (vartheta=3) = "
          f"{r_burst(LAM, MU, dstar, 3) - r_bud(LAM, MU, dstar, 3):.3e}")
    print("  table check (lam, mu, delta, vartheta) -> L, R_burst, R_bud:")
    for lam, mu, d, th in ((1, 0, 0.1, 5), (1, 0.5, 1 / 3, 5),
                           (1, 0.9, 0.1, 5), (1, 0.2, 0.05, 10),
                           (1, 0.9, 0.02, 5), (1, 0.95, 0.5, 3)):
        _, _, L, _ = parts(lam, mu, d)
        print(f"    ({lam}, {mu}, {d:.5f}, {th:2d}) -> L={L:.3f}  "
              f"R_burst={r_burst(lam, mu, d, th):.8f}  "
              f"R_bud={r_bud(lam, mu, d, th):.8f}")
