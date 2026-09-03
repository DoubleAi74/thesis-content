#!/usr/bin/env python3
"""fig02 --- the size of a late burst.

A single-panel regeneration of the source chapter's F4a.5.  Panel (a) of that
figure --- the burst-size law --- is now carried by fig01, whose right-hand
panel is exactly it; only panel (b), the size-biased conditional mean, is
retained here, and its content is unchanged.

Run:  python3 figures/fig02_late_burst_mean/src/generate.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
FIGDIR = HERE.parent
sys.path.insert(0, str(FIGDIR.parent / "_style"))
import style_rc  # noqa: E402

FIGDIR = Path(__file__).resolve().parents[1]
FIGSTEM = "fig07"

style_rc.apply()

import matplotlib.pyplot as plt  # noqa: E402

LAMBDA, MU, DELTA = 1.0, 0.2, 0.05
PDF_PATH = FIGDIR / (FIGSTEM + ".pdf")
PNG_PATH = FIGDIR / (FIGSTEM + ".png")


def roots():
    eta = (LAMBDA + MU + DELTA) / (2.0 * LAMBDA)
    disc = eta * eta - MU / LAMBDA
    a = eta + math.sqrt(disc)
    b = eta - math.sqrt(disc)
    return a, b, LAMBDA * (a - b)


def no_burst(t, a, b, theta):
    A, B = a - 1.0, 1.0 - b
    w = np.exp(theta * t)
    return (a * B + b * A * w) / (B + A * w)


def late_mean(t, a, b, theta):
    """E[K | tau = t] = K(t)/J(t) = 1 + (2 lambda/delta)(1 - I(t))."""
    return 1.0 + (2.0 * LAMBDA / DELTA) * (1.0 - no_burst(t, a, b, theta))


def make_figure() -> None:
    a, b, theta = roots()
    assert b < 1.0 < a
    assert abs((a - 1.0) * (1.0 - b) - DELTA / LAMBDA) < 1e-13
    asymptote = (a + 1.0) / (a - 1.0)
    qs_mean = a / (a - 1.0)
    assert abs(asymptote - 33.4642) < 5e-4, asymptote
    assert abs(qs_mean - 17.2321) < 5e-4, qs_mean

    t = np.linspace(0.0, 25.0, 800)
    mean = late_mean(t, a, b, theta)
    assert abs(mean[0] - 1.0) < 1e-13
    assert np.all(np.diff(mean) > 0.0)
    assert abs(late_mean(np.array([400.0]), a, b, theta)[0] - asymptote) < 1e-9

    fig, ax = plt.subplots(figsize=(5.4, 3.5))
    ax.plot(
        t,
        mean,
        color=style_rc.BLUE,
        lw=1.8,
        label=r"$\mathbb{E}[\mathcal{K}\mid\tau=t]=K(t)/J(t)$",
        zorder=3,
    )
    ax.axhline(
        asymptote,
        color=style_rc.INK,
        ls=(0, (7, 3)),
        lw=1.4,
        label=rf"$(a+1)/(a-1)={asymptote:.2f}$",
        zorder=2,
    )
    ax.axhline(
        qs_mean,
        color=style_rc.VERMILLION,
        ls=(0, (2, 2)),
        lw=1.3,
        label=rf"$a/(a-1)={qs_mean:.2f}$",
        zorder=2,
    )
    ax.set_xlim(0.0, 25.0)
    ax.set_ylim(0.0, 37.0)
    ax.set_xlabel(r"burst time $t$")
    ax.set_ylabel(r"mean burst size given rupture at $t$")
    ax.legend(loc="lower right", handlelength=2.2)
    ax.annotate(
        "size-biasing:\nthe factor is exactly\n"
        r"$\langle X^2\rangle_{\mathrm{QS}}/\langle X\rangle_{\mathrm{QS}}$",
        xy=(6.0, 26.0),
        color=style_rc.SOFT,
        fontsize=8,
        ha="left",
        va="center",
    )
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)
    print(f"asserts pass; a={a:.6f} b={b:.6f}")
    print(f"late-burst limit (a+1)/(a-1) = {asymptote:.4f}; "
          f"QS mean a/(a-1) = {qs_mean:.4f}")
    print(f"wrote {PDF_PATH}\nwrote {PNG_PATH}")


if __name__ == "__main__":
    make_figure()
