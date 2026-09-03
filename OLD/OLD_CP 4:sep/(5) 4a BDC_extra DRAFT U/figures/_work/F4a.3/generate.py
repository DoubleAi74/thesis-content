#!/usr/bin/env python3
"""Generate F4a.3: convergence of the conditional pmf to the QSD."""

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
import style_rc  # noqa: E402

style_rc.apply()

import matplotlib.pyplot as plt  # noqa: E402


LAMBDA = 1.0
MU = 0.2
DELTA = 0.05
TIMES = np.array([1.0, 5.0, 20.0])
N = np.arange(1, 61)
WORKDIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORKDIR.parents[2]
PDF_PATH = CHAPTER_DIR / "figures" / "F4a_3_qsd_convergence.pdf"
PNG_PATH = WORKDIR / "preview.png"


def roots() -> tuple[float, float, float]:
    eta = (LAMBDA + MU + DELTA) / (2.0 * LAMBDA)
    discriminant = eta**2 - MU / LAMBDA
    assert discriminant > 0.0
    a = eta + math.sqrt(discriminant)
    b = eta - math.sqrt(discriminant)
    theta = LAMBDA * (a - b)
    return a, b, theta


def ratio_p(t: float, a: float, b: float, theta: float) -> float:
    w = math.exp(theta * t)
    return (1.0 - w) / (b - a * w)


def p_positive(
    n: np.ndarray, t: float, a: float, b: float, theta: float
) -> np.ndarray:
    w = math.exp(theta * t)
    p1 = ((a - b) / (b - a * w)) ** 2 * w
    return p1 * ratio_p(t, a, b, theta) ** (n - 1)


def i_fix(t: float, a: float, b: float, theta: float) -> float:
    w = math.exp(theta * t)
    cap_a = a - 1.0
    cap_b = 1.0 - b
    return (a - b) ** 2 * w / ((cap_b + cap_a * w) * (a * w - b))


def conditional_pmf(
    n: np.ndarray, t: float, a: float, b: float, theta: float
) -> np.ndarray:
    return p_positive(n, t, a, b, theta) / i_fix(t, a, b, theta)


def qsd(n: np.ndarray, a: float) -> np.ndarray:
    return (a - 1.0) * a ** (-n)


def run_asserts() -> tuple[float, float, float]:
    a, b, theta = roots()
    assert b < 1.0 < a
    assert abs(a * b - MU / LAMBDA) < 1e-13

    limit = qsd(N, a)
    assert np.all(limit > 0.0)
    assert abs(limit.sum() - (1.0 - a ** (-len(N)))) < 2e-13
    assert limit.sum() > 0.97

    errors = []
    for t in TIMES:
        ratio = ratio_p(float(t), a, b, theta)
        cond = conditional_pmf(N, float(t), a, b, theta)
        closed_cond = (1.0 - ratio) * ratio ** (N - 1)
        assert np.all(cond > 0.0) and np.all(np.isfinite(cond))
        assert np.max(np.abs(cond - closed_cond)) < 2e-13
        assert abs(cond.sum() - (1.0 - ratio ** len(N))) < 2e-13
        assert cond.sum() > 0.97
        errors.append(float(np.max(np.abs(cond[:30] - limit[:30]))))

    assert errors[2] < 0.02
    assert errors[0] > errors[1] > errors[2]
    return a, b, theta


def make_figure() -> None:
    a, b, theta = run_asserts()
    fig, ax = plt.subplots(figsize=(7.2, 4.25))

    for index, t in enumerate(TIMES):
        cond = conditional_pmf(N, float(t), a, b, theta)
        ax.plot(
            N,
            cond,
            marker="o" if index == 2 else None,
            markevery=5,
            markersize=3.5,
            label=rf"$t={t:g}$",
            zorder=2,
        )

    ax.plot(
        N,
        qsd(N, a),
        color="#666666",
        linestyle="--",
        linewidth=1.6,
        label=r"limit $(a-1)a^{-n}$",
        zorder=3,
    )
    ax.set_xlim(1, 60)
    ax.set_ylim(0.0, 0.44)
    ax.set_xlabel(r"State $n$")
    ax.set_ylabel(r"Conditional probability $p_n(t)/I_{\mathrm{fix}}(t)$")
    ax.set_xticks(np.arange(1, 61, 10))
    ax.legend(loc="upper right")

    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)


if __name__ == "__main__":
    make_figure()
    print(f"asserts: pass; wrote {PDF_PATH} and {PNG_PATH}")
