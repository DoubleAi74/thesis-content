#!/usr/bin/env python3
"""Generate N4a.6: quasi-stationary and release means across death rates."""

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
FIGSTEM = "fig04"

style_rc.apply()

import matplotlib.pyplot as plt  # noqa: E402


LAMBDA = 1.0
DELTA = 0.05
WORKDIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORKDIR.parents[2]
PDF_PATH = FIGDIR / (FIGSTEM + ".pdf")
PNG_PATH = FIGDIR / (FIGSTEM + ".png")


def roots(mu: float | np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mu_arr = np.asarray(mu, dtype=float)
    eta = (LAMBDA + mu_arr + DELTA) / (2.0 * LAMBDA)
    discriminant = eta**2 - mu_arr / LAMBDA
    if np.any(discriminant < 0.0):
        raise ValueError("negative root discriminant")
    root = np.sqrt(discriminant)
    return eta + root, eta - root


def release_means(mu: float | np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    a, b = roots(mu)
    qs_mean = a / (a - 1.0)
    unconditional = (1.0 - b) * qs_mean
    conditional = unconditional / (1.0 - b)
    return unconditional, conditional, b


def run_asserts() -> dict[str, float]:
    v0_arr, conditional0_arr, b0_arr = release_means(0.0)
    a0_arr, _ = roots(0.0)
    v0 = float(v0_arr)
    conditional0 = float(conditional0_arr)
    qs0 = float(a0_arr / (a0_arr - 1.0))
    b0 = float(b0_arr)
    assert abs(b0) < 1e-15
    assert abs(v0 - conditional0) < 1e-13
    assert abs(v0 - qs0) < 1e-13
    assert abs(v0 - 21.0) < 1e-12

    v_work_arr, conditional_work_arr, b_work_arr = release_means(0.2)
    v_work = float(v_work_arr)
    conditional_work = float(conditional_work_arr)
    b_work = float(b_work_arr)
    assert abs(v_work - 13.985699678629192) < 1e-12
    assert abs(conditional_work - 17.23212459828649) < 1e-12
    assert v_work < conditional_work
    assert abs((conditional_work - v_work) - b_work * conditional_work) < 1e-12

    mu_grid = np.linspace(0.0, 0.9, 901)
    v_grid, conditional_grid, _ = release_means(mu_grid)
    assert abs(float(v_grid[0] - conditional_grid[0])) < 1e-13
    assert np.all(v_grid[1:] < conditional_grid[1:])
    return {
        "v0": v0,
        "v_work": v_work,
        "conditional_work": conditional_work,
        "b_work": b_work,
    }


def make_figure() -> None:
    checked = run_asserts()
    mu = np.linspace(0.0, 0.9, 1_001)
    unconditional, conditional, _ = release_means(mu)

    fig, ax = plt.subplots(figsize=(5.39, 3.32))
    ax.fill_between(
        mu,
        unconditional,
        conditional,
        color=style_rc.PURPLE,
        alpha=0.10,
        linewidth=0.0,
        zorder=1,
    )
    ax.plot(
        mu,
        unconditional,
        color=style_rc.BLUE,
        linewidth=2.2,
        label=r"unconditional release $V_\infty$",
        zorder=3,
    )
    ax.plot(
        mu,
        conditional,
        color=style_rc.PURPLE,
        linewidth=2.3,
        label=r"$\langle X\rangle_{\rm QS}=V_\infty/(1-b)$",
        zorder=3,
    )
    ax.scatter(
        [0.0],
        [checked["v0"]],
        s=62,
        facecolor="white",
        edgecolor=style_rc.INK,
        linewidth=1.2,
        zorder=5,
        clip_on=False,
    )
    ax.annotate(
        r"$\mu=0$: $b=0$, all three coincide",
        xy=(0.0, checked["v0"]),
        xytext=(0.15, 21.8),
        arrowprops={"arrowstyle": "->", "color": style_rc.INK, "linewidth": 0.85},
        fontsize=9,
        ha="left",
        va="center",
    )

    mu_work = 0.2
    v_work = checked["v_work"]
    conditional_work = checked["conditional_work"]
    ax.scatter(
        [mu_work, mu_work],
        [v_work, conditional_work],
        s=34,
        color=(style_rc.BLUE, style_rc.PURPLE),
        edgecolor="white",
        linewidth=0.65,
        zorder=5,
    )
    ax.annotate(
        "",
        xy=(mu_work, conditional_work),
        xytext=(mu_work, v_work),
        arrowprops={
            "arrowstyle": "<->",
            "color": style_rc.SOFT,
            "linewidth": 0.9,
            "shrinkA": 4,
            "shrinkB": 4,
        },
    )
    ax.text(
        0.66,
        12.0,
        "internal-clearance realisations\ncontribute zero release",
        ha="center",
        va="center",
        fontsize=9,
        color=style_rc.SOFT,
    )
    ax.text(
        0.98,
        0.95,
        r"$\lambda=1$, $\delta=0.05$",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9,
    )

    ax.set_xlim(0.0, 0.9)
    ax.set_ylim(0.0, 23.0)
    ax.set_xlabel(r"internal death rate $\mu$")
    ax.set_ylabel("mean particle count")
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.84))

    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)


if __name__ == "__main__":
    results = run_asserts()
    make_figure()
    print(
        "asserts: pass; at mu=0 all means="
        f"{results['v0']:.12f}; at mu=0.2 V_inf={results['v_work']:.12f}, "
        f"conditional/QS={results['conditional_work']:.12f}"
    )
    print(f"wrote {PDF_PATH} and {PNG_PATH}")
