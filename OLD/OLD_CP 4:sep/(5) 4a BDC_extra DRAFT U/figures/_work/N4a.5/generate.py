#!/usr/bin/env python3
"""Generate N4a.5: exact joint law of burst time and burst size."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(
    0,
    "/Users/adamaldridge/Desktop/Thesis content 🎓 /4 BDC additional and BMVR/"
    "Figures run/style",
)
import style_rc  # noqa: E402

style_rc.apply()

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LogNorm  # noqa: E402


LAMBDA = 1.0
MU = 0.0
DELTA = 0.1
THETA = LAMBDA + DELTA
A = DELTA / LAMBDA
WORKDIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORKDIR.parents[2]
PDF_PATH = CHAPTER_DIR / "figures" / "N4a_5_joint_tau_K.pdf"
PNG_PATH = WORKDIR / "preview.png"


def no_burst_probability(t: np.ndarray) -> np.ndarray:
    """Exact I(t) for mu=0, with a=1+delta/lambda and b=0."""
    t_arr = np.asarray(t, dtype=float)
    a = 1.0 + A
    return a / (1.0 + A * np.exp(THETA * t_arr))


def state_probabilities(t: np.ndarray, k: np.ndarray) -> np.ndarray:
    """Transient p_k(t), returned with shape (len(k), len(t))."""
    t_arr = np.asarray(t, dtype=float)
    k_arr = np.asarray(k, dtype=int)
    decay = np.exp(-THETA * t_arr)
    q = (1.0 - decay) / (1.0 + DELTA / LAMBDA)
    return decay[None, :] * q[None, :] ** (k_arr[:, None] - 1)


def conditional_mean_closed(t: np.ndarray) -> np.ndarray:
    return 1.0 + 2.0 * LAMBDA / DELTA * (1.0 - no_burst_probability(t))


def run_asserts() -> dict[str, float]:
    assert MU == 0.0
    assert abs(no_burst_probability(np.array([0.0]))[0] - 1.0) < 1e-14

    check_t = np.array([0.25, 1.0, 2.5, 5.0])
    check_k = np.arange(1, 1_001)
    p = state_probabilities(check_t, check_k)
    joint = DELTA * check_k[:, None] * p
    numeric_mean = (check_k[:, None] * joint).sum(axis=0) / joint.sum(axis=0)
    closed_mean = conditional_mean_closed(check_t)
    mean_error = float(np.max(np.abs(numeric_mean - closed_mean)))
    assert mean_error < 1e-10, mean_error
    assert np.all(np.diff(closed_mean) > 0.0)

    # The defective density delta*J integrates to one when mu=0: every cell bursts.
    t_integral = np.linspace(0.0, 30.0, 30_001)
    w = np.exp(THETA * t_integral)
    mean_load = (1.0 + A) ** 2 * w / (1.0 + A * w) ** 2
    burst_mass = float(np.trapezoid(DELTA * mean_load, t_integral))
    assert abs(burst_mass - 1.0) < 2e-6, burst_mass
    assert float(no_burst_probability(t_integral[-1:])[0]) < 1e-12

    late_limit = 1.0 + 2.0 * LAMBDA / DELTA
    assert abs(late_limit - 21.0) < 1e-13
    return {
        "conditional_mean_max_error": mean_error,
        "burst_mass": burst_mass,
        "late_limit": late_limit,
    }


def make_figure() -> None:
    run_asserts()
    t = np.linspace(0.0, 6.0, 1_301)
    k = np.arange(1, 56)
    p = state_probabilities(t, k)
    joint_density = DELTA * k[:, None] * p
    conditional_mean = conditional_mean_closed(t)

    fig, ax = plt.subplots(figsize=(7.5, 4.65))
    cmap = plt.get_cmap("Blues").copy()
    cmap.set_under("#f7fbff")
    mesh = ax.pcolormesh(
        t,
        k,
        joint_density,
        shading="auto",
        cmap=cmap,
        norm=LogNorm(vmin=1e-6, vmax=float(joint_density.max())),
        # Rasterise only the dense heat field; text, axes, mean curve, and
        # annotations remain vector in the production PDF. This avoids PDF
        # viewer seams between adjacent analytic mesh cells.
        rasterized=True,
        antialiased=False,
        edgecolors="none",
        linewidth=0.0,
        snap=True,
    )
    ax.grid(False)

    # A white under-stroke keeps the analytic mean legible throughout the heat field.
    ax.plot(t, conditional_mean, color="white", linewidth=5.2, zorder=4)
    ax.plot(
        t,
        conditional_mean,
        color="#6b4c9a",
        linewidth=2.6,
        label=r"conditional mean $\mathbb{E}[\mathcal{K}\mid\tau=t]$",
        zorder=5,
    )
    sample_t = np.array([0.8, 2.4, 5.0])
    ax.scatter(
        sample_t,
        conditional_mean_closed(sample_t),
        s=34,
        facecolor="white",
        edgecolor="#6b4c9a",
        linewidth=1.3,
        zorder=6,
    )
    ax.annotate(
        "later rupture selects\nlarger loads",
        xy=(4.6, float(conditional_mean_closed(np.array([4.6]))[0])),
        xytext=(3.05, 32.5),
        arrowprops={"arrowstyle": "->", "color": "#333333", "linewidth": 0.85},
        fontsize=9,
        color="#333333",
        ha="left",
        va="center",
        zorder=7,
    )
    ax.text(
        0.98,
        0.97,
        r"$\lambda=1$, $\mu=0$, $\delta=0.1$",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9,
        color="#222222",
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.86, "pad": 2.0},
        zorder=8,
    )
    ax.set_xlim(0.0, 6.0)
    ax.set_ylim(0.5, 55.5)
    ax.set_yticks([1, 10, 20, 30, 40, 50])
    ax.set_xlabel(r"burst time $\tau$")
    ax.set_ylabel(r"burst size $\mathcal{K}$")
    ax.set_title(
        "Late bursts shift towards larger release sizes",
        loc="left",
        fontweight="bold",
    )
    ax.legend(loc="upper left", bbox_to_anchor=(0.015, 0.89))

    cbar = fig.colorbar(mesh, ax=ax, pad=0.025, fraction=0.055)
    cbar.set_label(r"joint density $f_{\tau,\mathcal{K}}(t,k)$")
    cbar.ax.tick_params(labelsize=8)

    fig.tight_layout()
    fig.savefig(PDF_PATH, format="pdf", bbox_inches="tight", dpi=300)
    fig.savefig(PNG_PATH, format="png", bbox_inches="tight", dpi=240)
    plt.close(fig)


if __name__ == "__main__":
    checked = run_asserts()
    make_figure()
    print(
        "asserts: pass; conditional-mean max error="
        f"{checked['conditional_mean_max_error']:.3e}; "
        f"integrated burst mass={checked['burst_mass']:.9f}; "
        f"late mean={checked['late_limit']:.2f}"
    )
    print(f"wrote {PDF_PATH} and {PNG_PATH}")
