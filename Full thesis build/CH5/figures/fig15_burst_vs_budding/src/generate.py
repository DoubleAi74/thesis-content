#!/usr/bin/env python3
"""Generate N4a.3: matched-mean BDC and budding release laws."""

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
FIGSTEM = "fig15"

style_rc.apply()

import matplotlib.pyplot as plt  # noqa: E402


LAMBDA = 1.0
MU = 0.2
DELTA = 0.05
WORKDIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORKDIR.parents[2]
PDF_PATH = FIGDIR / (FIGSTEM + ".pdf")
PNG_PATH = FIGDIR / (FIGSTEM + ".png")
BDC_COLOUR = style_rc.VERMILLION
BUD_COLOUR = style_rc.BLUE


def roots() -> tuple[float, float]:
    eta = (LAMBDA + MU + DELTA) / (2.0 * LAMBDA)
    discriminant = eta**2 - MU / LAMBDA
    assert discriminant > 0.0
    a = eta + math.sqrt(discriminant)
    b = eta - math.sqrt(discriminant)
    return a, b


def laws(k: np.ndarray, a: float, matched_mean: float) -> tuple[np.ndarray, np.ndarray]:
    """Conditional BDC law on positive integers and budding law on nonnegative integers."""
    bdc = np.where(k >= 1, (a - 1.0) * a ** (-k), 0.0)
    q_bud = matched_mean / (matched_mean + 1.0)
    budding = (1.0 - q_bud) * q_bud**k
    return bdc, budding


def run_asserts() -> dict[str, float]:
    a, b = roots()
    assert b < 1.0 < a
    assert abs((a - 1.0) * (1.0 - b) - DELTA / LAMBDA) < 1e-13
    matched_mean = a / (a - 1.0)
    q_bud = matched_mean / (matched_mean + 1.0)

    k_check = np.arange(0, 20_001)
    bdc, budding = laws(k_check, a, matched_mean)
    assert abs(float(bdc.sum()) - 1.0) < 1e-10
    assert abs(float(budding.sum()) - 1.0) < 1e-10
    bdc_mean = float(np.dot(k_check, bdc))
    bud_mean = float(np.dot(k_check, budding))
    assert abs(bdc_mean - matched_mean) < 1e-8
    assert abs(bud_mean - matched_mean) < 1e-8
    assert bdc[0] == 0.0 and budding[0] > 0.0
    assert np.max(np.abs(bdc - budding)) > 1e-3
    return {
        "a": a,
        "b": b,
        "mean": matched_mean,
        "q_bud": q_bud,
        "bud_zero": float(budding[0]),
    }


def make_figure() -> None:
    checked = run_asserts()
    a = checked["a"]
    matched_mean = checked["mean"]
    q_bud = checked["q_bud"]

    k = np.arange(0, 66)
    bdc, budding = laws(k, a, matched_mean)
    k_tail = np.arange(1, 66)
    q_bdc = 1.0 / a
    bdc_tail = q_bdc ** (k_tail - 1)
    bud_tail = q_bud**k_tail
    tail_crossing = math.log(q_bdc) / (math.log(q_bdc) - math.log(q_bud))
    crossing_height = q_bdc ** (tail_crossing - 1.0)

    fig, ax_pmf = plt.subplots(figsize=(5.41, 3.59))

    ax_pmf.bar(
        k,
        bdc,
        width=0.80,
        color=BDC_COLOUR,
        alpha=0.42,
        edgecolor=BDC_COLOUR,
        linewidth=0.65,
        label=r"BDC conditional: $(a-1)a^{-k}$",
        zorder=2,
    )
    ax_pmf.plot(
        k,
        budding,
        color=BUD_COLOUR,
        linestyle="--",
        marker="s",
        markersize=3.2,
        markevery=4,
        linewidth=2.0,
        label=r"budding: $(1-q)q^k$",
        zorder=3,
    )
    ax_pmf.scatter(
        [0],
        [0],
        s=32,
        facecolor="white",
        edgecolor=BDC_COLOUR,
        linewidth=1.4,
        zorder=4,
    )
    ax_pmf.annotate(
        r"budding can release zero:"
        "\n"
        rf"$\Pr(\mathcal{{K}}_{{\rm bud}}=0)={checked['bud_zero']:.3f}$; BDC mass $=0$",
        xy=(0.0, checked["bud_zero"]),
        xytext=(4.0, 0.070),
        arrowprops={"arrowstyle": "->", "color": style_rc.INK, "linewidth": 0.85},
        fontsize=9,
        ha="left",
        va="center",
    )
    ax_pmf.set_xlim(-0.8, 65.5)
    ax_pmf.set_ylim(0.0, 0.078)
    ax_pmf.set_xlabel(r"released particles $k$")
    ax_pmf.set_ylabel("probability")
    ax_pmf.set_title(
        r"(a) same mean, different support",
        loc="left",
    )
    ax_pmf.legend(loc="upper right", bbox_to_anchor=(1.0, 0.84))


    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)


if __name__ == "__main__":
    results = run_asserts()
    make_figure()
    print(
        "asserts: pass; "
        f"matched mean={results['mean']:.12f}; "
        f"budding zero mass={results['bud_zero']:.12f}"
    )
    print(f"wrote {PDF_PATH} and {PNG_PATH}")
