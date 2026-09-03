#!/usr/bin/env python3
"""Generate F4a.2: the geometric slide of the positive state probabilities."""

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
TIMES = np.array([0.5, 1.0, 2.0, 5.0, 15.0])
N = np.arange(1, 61)
WORKDIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORKDIR.parents[2]
PDF_PATH = CHAPTER_DIR / "figures" / "F4a_2_geometric_slide.pdf"
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


def run_asserts() -> tuple[float, float, float]:
    a, b, theta = roots()
    assert b < 1.0 < a
    assert abs(a * b - MU / LAMBDA) < 1e-13
    assert abs((a - 1.0) * (1.0 - b) - DELTA / LAMBDA) < 1e-13

    ratios = np.array([ratio_p(t, a, b, theta) for t in TIMES])
    # The brief's word "decreases" is a direction typo: P(0)=0 and the
    # displayed closed form increases monotonically to 1/a.
    assert np.all(np.diff(ratios) > 0.0)
    assert np.all((ratios > 0.0) & (ratios < 1.0 / a))
    assert abs(ratios[-1] - 1.0 / a) < 1e-2

    for t, ratio in zip(TIMES, ratios):
        pn = p_positive(N, float(t), a, b, theta)
        total = i_fix(float(t), a, b, theta)
        assert np.all(np.isfinite(pn)) and np.all(pn > 0.0)
        # Infinite geometric sum agrees with the independent I_fix formula.
        assert abs(pn[0] / (1.0 - ratio) - total) < 2e-13
        # The plotted range contains at least 97% of the positive-state mass.
        assert pn.sum() / total > 0.97
        expected_truncation = total * (1.0 - ratio ** len(N))
        assert abs(pn.sum() - expected_truncation) < 2e-13
    return a, b, theta


def make_figure() -> None:
    a, b, theta = run_asserts()
    fig, ax = plt.subplots(figsize=(7.4, 4.4))

    for t in TIMES:
        ratio = ratio_p(float(t), a, b, theta)
        pn = p_positive(N, float(t), a, b, theta)
        time_text = f"{t:g}"
        ax.semilogy(
            N,
            pn,
            label=rf"$t={time_text}$, $P(t)={ratio:.3f}$",
        )

    ax.set_xlim(1, 60)
    ax.set_ylim(1e-10, 1.0)
    ax.set_xlabel(r"State $n$")
    ax.set_ylabel(r"State probability $p_n(t)$")
    ax.set_xticks(np.arange(1, 61, 10))
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), borderaxespad=0.0)

    inset = ax.inset_axes([0.57, 0.56, 0.39, 0.39])
    dense_times = np.linspace(0.0, 15.0, 400)
    dense_ratios = np.array([ratio_p(float(t), a, b, theta) for t in dense_times])
    inset.plot(dense_times, dense_ratios, color="tab:blue", linewidth=1.5)
    inset.scatter(
        TIMES,
        [ratio_p(float(t), a, b, theta) for t in TIMES],
        color="tab:blue",
        s=11,
        zorder=3,
    )
    inset.axhline(1.0 / a, color="#777777", linestyle="--", linewidth=1.0)
    inset.text(
        14.7,
        1.0 / a - 0.055,
        r"$1/a$",
        ha="right",
        va="top",
        fontsize=8,
        color="#666666",
    )
    inset.set_xlim(0.0, 15.0)
    inset.set_ylim(0.0, 1.02)
    inset.set_xlabel(r"$t$", fontsize=8, labelpad=0)
    inset.set_ylabel(r"$P(t)$", fontsize=8, labelpad=1)
    inset.tick_params(labelsize=7)
    inset.grid(True, alpha=0.25, linewidth=0.5)

    fig.tight_layout(rect=(0.0, 0.0, 0.79, 1.0))
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)


if __name__ == "__main__":
    make_figure()
    print(f"asserts: pass; wrote {PDF_PATH} and {PNG_PATH}")
