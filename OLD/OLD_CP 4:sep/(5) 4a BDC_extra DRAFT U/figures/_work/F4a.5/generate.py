#!/usr/bin/env python3
"""Generate F4a.5: burst-size laws and the mean size of a late burst."""

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
K = np.arange(1, 41)
WORKDIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORKDIR.parents[2]
PDF_PATH = CHAPTER_DIR / "figures" / "F4a_5_burst_size_late.pdf"
PNG_PATH = WORKDIR / "preview.png"


def roots() -> tuple[float, float, float]:
    eta = (LAMBDA + MU + DELTA) / (2.0 * LAMBDA)
    discriminant = eta**2 - MU / LAMBDA
    assert discriminant > 0.0
    a = eta + math.sqrt(discriminant)
    b = eta - math.sqrt(discriminant)
    theta = LAMBDA * (a - b)
    return a, b, theta


def no_burst_probability(t: np.ndarray, a: float, b: float, theta: float) -> np.ndarray:
    cap_a = a - 1.0
    cap_b = 1.0 - b
    w = np.exp(theta * t)
    return (a * cap_b + b * cap_a * w) / (cap_b + cap_a * w)


def burst_laws(k: np.ndarray, a: float) -> tuple[np.ndarray, np.ndarray]:
    unconditional = (DELTA / LAMBDA) * a ** (-k)
    conditional = (a - 1.0) * a ** (-k)
    return unconditional, conditional


def late_burst_mean(t: np.ndarray, a: float, b: float, theta: float) -> np.ndarray:
    i_t = no_burst_probability(t, a, b, theta)
    return 1.0 + (2.0 * LAMBDA / DELTA) * (1.0 - i_t)


def run_asserts() -> tuple[float, float, float, float]:
    a, b, theta = roots()
    assert b < 1.0 < a
    assert abs(a * b - MU / LAMBDA) < 1e-13
    assert abs((a - 1.0) * (1.0 - b) - DELTA / LAMBDA) < 1e-13

    check_k = np.arange(1, 10_001)
    unconditional, conditional = burst_laws(check_k, a)
    unconditional_total = float(unconditional.sum())
    conditional_total = float(conditional.sum())
    assert abs(unconditional_total - (1.0 - b)) < 1e-10
    assert abs(conditional_total - 1.0) < 1e-10
    assert abs(b + unconditional_total - 1.0) < 1e-10

    asymptote = (a + 1.0) / (a - 1.0)
    t = np.linspace(0.0, 25.0, 501)
    mean = late_burst_mean(t, a, b, theta)
    assert abs(mean[0] - 1.0) < 1e-13
    assert np.all(np.diff(mean) > 0.0)
    assert abs(mean[-1] - asymptote) < 0.5
    assert abs(asymptote - 33.5) < 0.1
    return a, b, theta, asymptote


def make_figure() -> None:
    a, b, theta, asymptote = run_asserts()
    unconditional, conditional = burst_laws(K, a)
    t = np.linspace(0.0, 25.0, 700)
    mean = late_burst_mean(t, a, b, theta)

    fig, (ax_law, ax_mean) = plt.subplots(1, 2, figsize=(9.6, 4.25))

    ax_law.bar(
        K,
        unconditional,
        width=0.82,
        color="tab:blue",
        alpha=0.78,
        label=r"unconditional $(\delta/\lambda)a^{-k}$",
        zorder=2,
    )
    ax_law.plot(
        K,
        conditional,
        color="tab:orange",
        marker="o",
        markersize=3.0,
        markevery=2,
        label=r"conditional $(a-1)a^{-k}$",
        zorder=3,
    )
    ax_law.bar(
        [0],
        [b],
        width=0.82,
        color="white",
        edgecolor="#666666",
        hatch="///",
        linewidth=0.9,
        label=rf"no-burst mass $b={b:.3f}$",
        zorder=2,
    )
    ax_law.annotate(
        rf"$b={b:.3f}$",
        xy=(0.0, b),
        xytext=(3.2, b * 0.9),
        arrowprops={"arrowstyle": "->", "color": "black", "linewidth": 0.8},
        va="center",
        fontsize=9,
    )
    ax_law.set_xlim(-0.75, 40.75)
    ax_law.set_ylim(0.0, 0.215)
    ax_law.set_xlabel(r"Burst size $k$")
    ax_law.set_ylabel("Probability")
    ax_law.set_title(r"(a) Burst-size distribution", loc="left", fontweight="bold")
    ax_law.legend(loc="upper right")

    ax_mean.plot(
        t,
        mean,
        color="tab:blue",
        label=r"$\mathbb{E}[\mathcal{K}\mid\tau=t]$",
    )
    ax_mean.axhline(
        asymptote,
        color="#777777",
        linestyle="--",
        linewidth=1.2,
        label=rf"late-burst limit $={asymptote:.2f}$",
        zorder=1,
    )
    ax_mean.annotate(
        rf"$(a+1)/(a-1)={asymptote:.2f}$",
        xy=(17.5, asymptote),
        xytext=(9.4, asymptote - 6.0),
        arrowprops={"arrowstyle": "->", "color": "black", "linewidth": 0.8},
        fontsize=9,
    )
    ax_mean.set_xlim(0.0, 25.0)
    ax_mean.set_ylim(0.0, 36.0)
    ax_mean.set_xlabel(r"Time $t$")
    ax_mean.set_ylabel(r"Conditional mean $\mathbb{E}[\mathcal{K}\mid\tau=t]$")
    ax_mean.set_title(r"(b) Size of a late burst", loc="left", fontweight="bold")
    ax_mean.legend(loc="lower right")

    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)


if __name__ == "__main__":
    _, checked_b, _, checked_asymptote = run_asserts()
    make_figure()
    print(
        "asserts: pass; "
        f"b={checked_b:.6f}; late-burst limit={checked_asymptote:.6f}"
    )
    print(f"wrote {PDF_PATH} and {PNG_PATH}")
