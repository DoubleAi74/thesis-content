#!/usr/bin/env python3
"""Generate F4a.8: conditional rupture time versus burst size."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

STYLE_DIR = Path(
    "/Users/adamaldridge/Desktop/Thesis content 🎓 /4 BDC additional and BMVR/"
    "Figures run/style"
)
sys.path.insert(0, str(STYLE_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_style"))
import style_rc  # noqa: E402

FIGDIR = Path(__file__).resolve().parents[1]
FIGSTEM = "fig10"

style_rc.apply()

import matplotlib.pyplot as plt  # noqa: E402


LAMBDA = 1.0
DELTA = 0.1
THETA = LAMBDA + DELTA
BUDDING_SCALE = 8.0
N = np.arange(1, 41)
EULER_GAMMA = float(np.euler_gamma)
WORKDIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORKDIR.parents[2]
PDF_PATH = FIGDIR / (FIGSTEM + ".pdf")
PNG_PATH = FIGDIR / (FIGSTEM + ".png")


def harmonic_numbers(n: np.ndarray) -> np.ndarray:
    assert n.ndim == 1 and np.all(n >= 1)
    return np.cumsum(1.0 / np.arange(1, int(n.max()) + 1))[n - 1]


def exact_conditional_means(n: np.ndarray) -> np.ndarray:
    return harmonic_numbers(n) / THETA


def harmonic_approximation(n: np.ndarray) -> np.ndarray:
    return (np.log(n) + EULER_GAMMA) / THETA


def budding_conditional_means(n: np.ndarray) -> np.ndarray:
    return (n + 1.0) / BUDDING_SCALE


def run_asserts() -> tuple[float, float]:
    exact = exact_conditional_means(N)
    independently_summed = np.array(
        [math.fsum(1.0 / k for k in range(1, int(n) + 1)) / THETA for n in N]
    )
    assert np.max(np.abs(exact - independently_summed)) < 1e-12
    assert np.all(np.diff(exact) > 0.0)

    approximation = harmonic_approximation(N)
    large_n_error = float(abs(exact[-1] - approximation[-1]))
    assert large_n_error < 0.02
    assert abs(exact[0] - 1.0 / THETA) < 1e-14

    budding = budding_conditional_means(N)
    assert np.allclose(np.diff(budding), 1.0 / BUDDING_SCALE)
    assert budding[-1] > exact[-1]
    return float(exact[-1]), large_n_error


def make_figure() -> None:
    run_asserts()
    exact = exact_conditional_means(N)
    approximation = harmonic_approximation(N)
    budding = budding_conditional_means(N)

    fig, ax = plt.subplots(figsize=(5.25, 3.17))
    ax.scatter(
        N,
        exact,
        s=22,
        color=style_rc.BLUE,
        edgecolor="white",
        linewidth=0.35,
        label="exact harmonic mean",
        zorder=4,
    )
    ax.plot(
        N[1:],
        approximation[1:],
        color=style_rc.INK,
        linestyle=":",
        linewidth=2.0,
        label=r"$(\log n+\gamma)/\theta$",
        zorder=3,
    )
    ax.plot(
        N,
        budding,
        color=style_rc.VERMILLION,
        linestyle="--",
        linewidth=1.8,
        label=r"budding $(n+1)/(d_I+p)$",
        zorder=2,
    )

    ax.set_xlim(1.0, 40.0)
    ax.set_ylim(0.0, 5.5)
    ax.set_xlabel(r"burst size $n$")
    ax.set_ylabel(r"conditional mean rupture time $\mathbb{E}[\tau\mid\mathcal{K}=n]$")
    ax.legend(loc="upper left")
    ax.text(
        0.98,
        0.05,
        r"$\theta=\lambda+\delta=1.1$" "\n" r"$d_I+p=8$",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9},
    )

    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)


if __name__ == "__main__":
    checked_mean, checked_error = run_asserts()
    make_figure()
    print(
        "asserts: pass; "
        f"mean(n=40)={checked_mean:.6f}; approximation error={checked_error:.6f}"
    )
    print(f"wrote {PDF_PATH} and {PNG_PATH}")
