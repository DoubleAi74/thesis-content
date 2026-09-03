#!/usr/bin/env python3
"""Generate N4a.2: productive lifetime over rates and its survival integral."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(
    0,
    "/Users/adamaldridge/Desktop/Thesis content 🎓 /4 BDC additional and BMVR/"
    "Figures run/style",
)
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_style"))
import style_rc  # noqa: E402

FIGDIR = Path(__file__).resolve().parents[1]
FIGSTEM = "fig05"

style_rc.apply()

import matplotlib.pyplot as plt  # noqa: E402


LAMBDA = 1.0
MU_WORK = 0.2
DELTA_WORK = 0.05
WORKDIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORKDIR.parents[2]
PDF_PATH = FIGDIR / (FIGSTEM + ".pdf")
PNG_PATH = FIGDIR / (FIGSTEM + ".png")


def roots(
    lam: float, mu: float | np.ndarray, delta: float | np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Return the ordered roots a > 1 > b of the BDC quadratic."""
    mu_arr = np.asarray(mu, dtype=float)
    delta_arr = np.asarray(delta, dtype=float)
    eta = (lam + mu_arr + delta_arr) / (2.0 * lam)
    discriminant = eta**2 - mu_arr / lam
    if np.any(discriminant < 0.0):
        raise ValueError("negative root discriminant")
    root = np.sqrt(discriminant)
    return eta + root, eta - root


def productive_lifetime(
    lam: float, mu: float | np.ndarray, delta: float | np.ndarray
) -> np.ndarray:
    a, _ = roots(lam, mu, delta)
    return np.log(a / (a - 1.0)) / lam


def productive_survival(t: np.ndarray, lam: float, mu: float, delta: float) -> np.ndarray:
    a_arr, b_arr = roots(lam, mu, delta)
    a = float(a_arr)
    b = float(b_arr)
    cap_a = a - 1.0
    cap_b = 1.0 - b
    theta = lam * (a - b)
    w = np.exp(theta * t)
    return (a - b) ** 2 * w / ((cap_b + cap_a * w) * (a * w - b))


def run_asserts() -> dict[str, float]:
    a_arr, b_arr = roots(LAMBDA, MU_WORK, DELTA_WORK)
    a = float(a_arr)
    b = float(b_arr)
    assert b < 1.0 < a
    assert abs(a * b - MU_WORK / LAMBDA) < 1e-13
    assert abs((a - 1.0) * (1.0 - b) - DELTA_WORK / LAMBDA) < 1e-13

    closed = float(productive_lifetime(LAMBDA, MU_WORK, DELTA_WORK))
    assert abs(closed - 2.8467753510219733) < 1e-12

    t_check = np.linspace(0.0, 60.0, 240_001)
    survival = productive_survival(t_check, LAMBDA, MU_WORK, DELTA_WORK)
    integral = float(np.trapezoid(survival, t_check))
    relative_error = abs(integral - closed) / closed
    assert abs(survival[0] - 1.0) < 1e-13
    assert np.all(np.diff(survival) < 0.0)
    assert survival[-1] < 1e-20
    assert relative_error < 0.01
    return {"a": a, "b": b, "closed": closed, "integral": integral}


def make_figure() -> None:
    checked = run_asserts()
    lifetime_work = checked["closed"]
    matched_death_rate = 1.0 / lifetime_work

    mu_values = np.linspace(0.0, 1.0, 241)
    delta_values = np.geomspace(0.005, 1.0, 241)
    mu_grid, delta_grid = np.meshgrid(mu_values, delta_values)
    lifetime_grid = productive_lifetime(LAMBDA, mu_grid, delta_grid)
    assert np.all(np.isfinite(lifetime_grid)) and np.all(lifetime_grid > 0.0)

    t = np.linspace(0.0, 12.0, 1_400)
    survival = productive_survival(t, LAMBDA, MU_WORK, DELTA_WORK)

    fig, (ax_map, ax_surv) = plt.subplots(
        1,
        2,
        figsize=(7.27, 3.09),
        dpi=240,
        gridspec_kw={"width_ratios": (1.06, 1.0)},
    )

    mesh = ax_map.pcolormesh(
        mu_grid,
        delta_grid,
        lifetime_grid,
        shading="auto",
        cmap="cividis",
        rasterized=True,
        antialiased=False,
    )
    contours = ax_map.contour(
        mu_grid,
        delta_grid,
        lifetime_grid,
        levels=(1.0, 2.0, 3.0, 4.0),
        colors=style_rc.INK,
        linewidths=0.75,
        alpha=0.78,
    )
    ax_map.clabel(
        contours,
        inline=True,
        fmt=lambda value: f"{value:g}",
        fontsize=8,
        manual=((0.70, 0.324), (0.70, 0.062), (0.45, 0.030), (0.20, 0.015)),
    )
    ax_map.scatter(
        [MU_WORK],
        [DELTA_WORK],
        marker="*",
        s=110,
        color=style_rc.VERMILLION,
        edgecolor="white",
        linewidth=0.9,
        label="working point",
        zorder=4,
    )
    ax_map.set_yscale("log")
    ax_map.set_xlim(0.0, 1.0)
    ax_map.set_ylim(delta_values[0], delta_values[-1])
    ax_map.set_yticks((0.01, 0.05, 0.1, 0.5, 1.0))
    ax_map.set_yticklabels(("0.01", "0.05", "0.1", "0.5", "1"))
    ax_map.set_xlabel(r"internal death rate $\mu$")
    ax_map.set_ylabel(r"rupture rate $\delta$")
    ax_map.set_title(
        r"(a) slower rupture extends productive life",
        loc="left",
    )
    ax_map.legend(loc="upper right")
    colorbar = fig.colorbar(mesh, ax=ax_map, pad=0.025)
    colorbar.set_label(r"mean lifetime $\mathbb{E}[T_{\rm prod}]$")

    ax_surv.fill_between(
        t,
        0.0,
        survival,
        color=style_rc.BLUE,
        alpha=0.14,
        linewidth=0.0,
        zorder=1,
    )
    ax_surv.plot(t, survival, color=style_rc.BLUE, linewidth=2.2, zorder=2)
    ax_surv.annotate(
        rf"shaded area $=\int_0^\infty I_{{\rm fix}}(t)\,\mathrm{{d}}t$"
        "\n"
        rf"$=\mathbb{{E}}[T_{{\rm prod}}]={lifetime_work:.3f}$",
        xy=(2.0, 0.30),
        xytext=(4.45, 0.67),
        arrowprops={"arrowstyle": "->", "color": style_rc.INK, "linewidth": 0.85},
        ha="center",
        va="center",
        fontsize=9,
    )
    ax_surv.text(
        0.97,
        0.94,
        r"$(\lambda,\mu,\delta)=(1,0.2,0.05)$",
        transform=ax_surv.transAxes,
        ha="right",
        va="top",
        fontsize=9,
    )
    ax_surv.text(
        0.97,
        0.12,
        rf"matched classical rate $d_I={matched_death_rate:.3f}$",
        transform=ax_surv.transAxes,
        ha="right",
        va="bottom",
        fontsize=9,
        color=style_rc.SOFT,
    )
    ax_surv.set_xlim(0.0, 12.0)
    ax_surv.set_ylim(0.0, 1.03)
    ax_surv.set_xlabel(r"time $t$")
    ax_surv.set_ylabel(r"productive survival $I_{\rm fix}(t)$")
    ax_surv.set_title(
        r"(b) productive survival accumulates the mean",
        loc="left",
    )

    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)


if __name__ == "__main__":
    results = run_asserts()
    make_figure()
    print(
        "asserts: pass; "
        f"closed lifetime={results['closed']:.12f}; "
        f"numerical integral={results['integral']:.12f}"
    )
    print(f"wrote {PDF_PATH} and {PNG_PATH}")
