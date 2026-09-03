#!/usr/bin/env python3
"""Generate F3.5: geometric burst-size preview for the mu=0 case."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

STYLE_DIR = Path(
    "/Users/adamaldridge/Desktop/Thesis content 🎓 /4 BDC additional and BMVR/Figures run/style"
)
sys.path.insert(0, str(STYLE_DIR))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402


WORKDIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORKDIR.parents[2]
PDF_PATH = CHAPTER_DIR / "figures/F3_5_burst_size_preview.pdf"
PNG_PATH = WORKDIR / "preview.png"

LAM = 1.0
MU = 0.0
DELTA = 0.1
A = (LAM + DELTA) / LAM
K = np.arange(1, 31)


def burst_probabilities(k: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return the analytic burst law and geometric law with ratio 1/a."""
    ratio = 1.0 / A
    burst = (DELTA / LAM) * A ** (-k)
    geometric = (1.0 - ratio) * ratio ** (k - 1)
    return burst, geometric


def run_asserts() -> dict[str, float]:
    """Verify coincidence, normalization, and zero mass at the origin."""
    burst, geometric = burst_probabilities(K)
    max_difference = float(np.max(np.abs(burst - geometric)))
    infinite_sum = float((DELTA / LAM) / (A - 1.0))
    displayed_sum = float(burst.sum())
    remaining_tail = float((1.0 / A) ** K[-1])
    mass_at_zero = 0.0  # b=mu/lambda root in this mu=0 parameter set.

    assert MU == 0.0
    assert abs(A - 1.1) < 1e-14
    assert max_difference < 1e-12
    assert abs(infinite_sum - 1.0) < 1e-12
    assert abs(displayed_sum + remaining_tail - 1.0) < 1e-12
    assert mass_at_zero == 0.0
    assert np.all(burst > 0.0)
    assert np.all(np.diff(burst) < 0.0)

    return {
        "max_bar_curve_difference": max_difference,
        "infinite_probability_sum": infinite_sum,
        "displayed_probability_sum": displayed_sum,
        "tail_beyond_k30": remaining_tail,
        "mass_at_zero": mass_at_zero,
    }


def make_figure() -> None:
    burst, geometric = burst_probabilities(K)

    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.bar(
        K,
        burst,
        width=0.76,
        color="tab:blue",
        edgecolor="tab:blue",
        linewidth=0.7,
        alpha=0.62,
        label=r"$\Pr\{\mathcal{K}=k\}$",
        zorder=2,
    )
    ax.plot(
        K,
        geometric,
        color="tab:orange",
        marker="o",
        markersize=3.2,
        markerfacecolor="white",
        markeredgewidth=0.9,
        linewidth=1.8,
        label=r"geometric$(1/a)$",
        zorder=3,
    )

    ax.annotate(
        r"$\Pr\{\mathcal{K}=0\}=b=0$",
        xy=(0.0, 0.0),
        xytext=(5.2, 0.061),
        arrowprops={"arrowstyle": "->", "color": "black", "linewidth": 0.8},
        ha="left",
        va="center",
        fontsize=9,
    )
    ax.set(
        xlim=(-0.5, 30.5),
        ylim=(0.0, 0.1),
        xlabel=r"Burst size $k$",
        ylabel="Probability",
    )
    ax.set_xticks(np.arange(0, 31, 5))
    ax.legend(loc="upper right")

    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)


if __name__ == "__main__":
    diagnostics = run_asserts()
    make_figure()
    for name, value in diagnostics.items():
        print(f"{name}={value:.12g}")
    print(f"wrote {PDF_PATH}")
    print(f"wrote {PNG_PATH}")
