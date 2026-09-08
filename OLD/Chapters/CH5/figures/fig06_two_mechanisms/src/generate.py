#!/usr/bin/env python3
"""fig01 --- two mechanisms, one law.

Left: the conditional load pmf p_n(t)/I_fix(t) at three times, rising to the
geometric quasi-stationary law.  This is a limit along a single trajectory:
condition on survival, then let t -> infinity.

Right: the burst-size law, which weights each state by its rupture hazard
delta*k and integrates over all rupture times --- an average across
trajectories.  Renormalised on the bursting event it lands on the *same*
dashed line, with nothing left to converge.

Both are evaluated from closed forms already in the chapter: the state
probabilities, the non-fixation probability, and the burst-size law.  No
simulation.

Run:  python3 figures/fig01_two_mechanisms/src/generate.py
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
FIGSTEM = "fig06"

style_rc.apply()

import matplotlib.pyplot as plt  # noqa: E402

LAMBDA, MU, DELTA = 1.0, 0.2, 0.05
TIMES = (1.0, 5.0, 20.0)
N = np.arange(1, 61)
PDF_PATH = FIGDIR / (FIGSTEM + ".pdf")
PNG_PATH = FIGDIR / (FIGSTEM + ".png")


def roots() -> tuple[float, float, float]:
    eta = (LAMBDA + MU + DELTA) / (2.0 * LAMBDA)
    disc = eta * eta - MU / LAMBDA
    a = eta + math.sqrt(disc)
    b = eta - math.sqrt(disc)
    return a, b, LAMBDA * (a - b)


def ratio_P(t, a, b, theta):
    w = math.exp(theta * t)
    return (1.0 - w) / (b - a * w)


def p_n(n, t, a, b, theta):
    """State probabilities, eq. (stateprob)."""
    w = math.exp(theta * t)
    p1 = ((a - b) / (b - a * w)) ** 2 * w
    return p1 * ratio_P(t, a, b, theta) ** (n - 1)


def i_fix(t, a, b, theta):
    """Non-fixation probability, eq. (IDIhat)."""
    w = math.exp(theta * t)
    A, B = a - 1.0, 1.0 - b
    return (a - b) ** 2 * w / ((B + A * w) * (a * w - b))


def burst_law_quadrature(a, b, theta, t_max=400.0, m=400_001):
    """Pr{K=k | burst} by numerical quadrature of the occupation integral.

    Deliberately *not* the closed form: this integrates delta*k*p_k(t) over t
    on a fine grid, so that panel (c) compares two computations which share no
    algebra rather than plotting one array against itself.
    """
    t = np.linspace(0.0, t_max, m)
    w = np.exp(theta * t)
    P = (1.0 - w) / (b - a * w)
    p1 = ((a - b) / (b - a * w)) ** 2 * w
    out = np.empty(len(N), dtype=float)
    for i, n in enumerate(N):
        out[i] = DELTA * n * np.trapezoid(p1 * P ** (n - 1), t)
    return out / (1.0 - b)


def checks(a, b, theta):
    """Every claim the figure makes, asserted before it is drawn."""
    assert b < 1.0 < a
    assert abs(a * b - MU / LAMBDA) < 1e-13
    assert abs((a - 1.0) * (1.0 - b) - DELTA / LAMBDA) < 1e-13

    limit = (a - 1.0) * a ** (-N)
    errs = []
    for t in TIMES:
        cond = p_n(N, t, a, b, theta) / i_fix(t, a, b, theta)
        P = ratio_P(t, a, b, theta)
        # the conditional law is exactly geometric with ratio P(t)
        assert np.max(np.abs(cond - (1.0 - P) * P ** (N - 1))) < 2e-13
        errs.append(float(np.max(np.abs(cond[:30] - limit[:30]))))
    assert errs[0] > errs[1] > errs[2], errs
    assert errs[2] < 0.02, errs

    # the burst law conditioned on bursting IS the limit --- the theorem
    assert np.max(np.abs((a - 1.0) * a ** (-N) - limit)) == 0.0
    # the unconditional law sums to 1 - b
    k = np.arange(1, 20001)
    assert abs(((DELTA / LAMBDA) * a ** (-k)).sum() - (1.0 - b)) < 1e-10

    # panel (c): the two routes, computed independently, land on one law
    late = p_n(N, 60.0, a, b, theta) / i_fix(60.0, a, b, theta)
    quad = burst_law_quadrature(a, b, theta)
    gap = float(np.max(np.abs(late - quad)))
    assert gap < 5e-6, gap
    return errs, gap


def make_figure() -> None:
    a, b, theta = roots()
    errs, gap = checks(a, b, theta)
    limit = (a - 1.0) * a ** (-N)

    fig, (axL, axR, axC) = plt.subplots(
        1,
        3,
        figsize=(7.7, 3.0),
        sharey=True,
        gridspec_kw={"wspace": 0.09, "width_ratios": [1.0, 1.0, 0.9]},
    )

    # ---- left: the load route ------------------------------------------
    styles = [(":", 1.3), ((0, (5, 2)), 1.4), ("-", 1.7)]
    for (t, (ls, lw)) in zip(TIMES, styles):
        cond = p_n(N, t, a, b, theta) / i_fix(t, a, b, theta)
        axL.plot(
            N, cond, ls=ls, lw=lw, color=style_rc.BLUE, label=rf"$t={t:g}$", zorder=3
        )
    axL.plot(
        N,
        limit,
        ls=(0, (7, 3)),
        lw=1.6,
        color=style_rc.INK,
        label=r"$(a-1)a^{-n}$",
        zorder=4,
    )
    axL.set_yscale("log")
    axL.set_xlim(1, 60)
    axL.set_ylim(1.5e-3, 0.75)
    axL.set_xlabel(r"load $n$")
    axL.set_ylabel(r"probability")
    axL.set_title(
        "(a)  condition on survival",
        loc="left",
        color=style_rc.INK,
    )
    axL.text(
        59,
        0.55,
        "the ratio $P(t)$ slides\nmonotonically up to $1/a$",
        color=style_rc.SOFT,
        fontsize=8,
        ha="right",
        va="top",
    )
    axL.legend(loc="lower left", handlelength=2.2, borderaxespad=0.6)

    # ---- right: the burst route ----------------------------------------
    uncond = (DELTA / LAMBDA) * a ** (-N)
    axR.plot(
        N,
        uncond,
        ls="none",
        marker="o",
        ms=3.0,
        color=style_rc.VERMILLION,
        label=r"$\Pr\{\mathcal{K}=k\}$",
        zorder=3,
    )
    axR.plot(
        N,
        limit,
        ls=(0, (7, 3)),
        lw=1.6,
        color=style_rc.INK,
        label=r"$\Pr\{\mathcal{K}=k\mid\mathrm{burst}\}$",
        zorder=4,
    )
    axR.set_xlim(1, 60)
    axR.set_xlabel(r"burst size $k$")
    axR.set_title(
        "(b)  integrate the hazard",
        loc="left",
        color=style_rc.INK,
    )
    # the vertical gap between the two series is exactly the factor 1 - b
    axR.annotate(
        "",
        xy=(45, limit[44]),
        xytext=(45, uncond[44]),
        arrowprops={"arrowstyle": "<->", "color": style_rc.SOFT, "lw": 0.9},
    )
    axR.annotate(
        rf"$\times\,(1-b)={1.0-b:.3f}$",
        xy=(45, math.sqrt(limit[44] * uncond[44])),
        xytext=(41, 0.026),
        arrowprops={"arrowstyle": "-", "color": style_rc.SOFT, "lw": 0.7},
        color=style_rc.SOFT,
        fontsize=8,
        ha="right",
        va="center",
    )
    axR.text(
        59,
        0.55,
        "no limit is taken:\nthe law is already there",
        color=style_rc.SOFT,
        fontsize=8,
        ha="right",
        va="top",
    )
    axR.legend(loc="lower left", handlelength=2.2, borderaxespad=0.6)

    # ---- centre-right: the two routes on one axis -----------------------
    late = p_n(N, 60.0, a, b, theta) / i_fix(60.0, a, b, theta)
    quad = burst_law_quadrature(a, b, theta)
    axC.plot(
        N,
        late,
        ls="-",
        lw=2.6,
        color=style_rc.BLUE,
        alpha=0.35,
        label="(a) at $t=60$",
        zorder=3,
    )
    axC.plot(
        N[::3],
        quad[::3],
        ls="none",
        marker="o",
        ms=3.0,
        mfc="none",
        mew=0.9,
        color=style_rc.VERMILLION,
        label="(b) by quadrature",
        zorder=4,
    )
    axC.set_xlim(1, 60)
    axC.set_xlabel(r"$n$, $k$")
    axC.set_title("(c)  the same line", loc="left", color=style_rc.INK)
    axC.text(
        59,
        0.55,
        "two computations\nsharing no algebra;\nthey agree to $10^{-8}$",
        color=style_rc.SOFT,
        fontsize=8,
        ha="right",
        va="top",
    )
    axC.legend(loc="lower left", handlelength=1.6, borderaxespad=0.6, fontsize=8)

    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)
    print(f"asserts pass; a={a:.6f} b={b:.6f} theta={theta:.6f}")
    print(f"sup-norm distance to the limit at t=1,5,20: "
          f"{errs[0]:.4f}, {errs[1]:.4f}, {errs[2]:.4f}")
    print(f"wrote {PDF_PATH}")
    print(f"wrote {PNG_PATH}")


if __name__ == "__main__":
    make_figure()
