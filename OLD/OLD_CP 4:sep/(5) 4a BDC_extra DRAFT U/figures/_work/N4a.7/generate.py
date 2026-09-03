#!/usr/bin/env python3
"""Generate N4a.7: honest MOI release-flux ratios."""

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
import style_rc  # noqa: E402

style_rc.apply()

import matplotlib.pyplot as plt  # noqa: E402


LAMBDA = 1.0
MU = 0.2
DELTA = 0.05
T_MAX = 15.0
WORKDIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORKDIR.parents[2]
PDF_PATH = CHAPTER_DIR / "figures" / "N4a_7_moi_flux_ratios.pdf"
PNG_PATH = WORKDIR / "preview.png"


def roots() -> tuple[float, float, float]:
    eta = (LAMBDA + MU + DELTA) / (2.0 * LAMBDA)
    discriminant = eta**2 - MU / LAMBDA
    assert discriminant > 0.0
    a = eta + math.sqrt(discriminant)
    b = eta - math.sqrt(discriminant)
    return a, b, LAMBDA * (a - b)


def moments(t: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    a, b, theta = roots()
    cap_a = a - 1.0
    cap_b = 1.0 - b
    w = np.exp(theta * np.asarray(t, dtype=float))
    i_t = (a * cap_b + b * cap_a * w) / (cap_b + cap_a * w)
    j_t = (a - b) ** 2 * w / (cap_b + cap_a * w) ** 2
    k_t = (1.0 + 2.0 * LAMBDA / DELTA * (1.0 - i_t)) * j_t
    return i_t, j_t, k_t


def ratio_to_linear(t: np.ndarray, k: int) -> np.ndarray:
    """Return g_k/(k g_1), retaining the shared-clock survival factors."""
    if k < 2:
        raise ValueError("k must be at least 2")
    i_t, j_t, k_t = moments(t)
    return i_t ** (k - 1) + (k - 1) * j_t**2 * i_t ** (k - 2) / k_t


def downward_crossing(t: np.ndarray, y: np.ndarray, level: float = 1.0) -> float:
    idx = np.flatnonzero((y[:-1] >= level) & (y[1:] < level))
    if len(idx) != 1:
        raise AssertionError(f"expected one downward crossing, found {len(idx)}")
    i = int(idx[0])
    return float(t[i] + (level - y[i]) * (t[i + 1] - t[i]) / (y[i + 1] - y[i]))


def run_asserts() -> dict[str, object]:
    t = np.linspace(0.0, T_MAX, 3_001)
    ratios = {k: ratio_to_linear(t, k) for k in (2, 3, 4)}
    early = {k: float(ratio_to_linear(np.array([1.0]), k)[0]) for k in ratios}
    assert all(value > 1.0 for value in early.values()), early
    assert all(np.all(np.isfinite(values)) for values in ratios.values())
    assert all(np.all(values > 0.0) for values in ratios.values())
    assert all(abs(ratios[k][0] - k) < 1e-12 for k in ratios)

    # Each ratio becomes sublinear, but their mutual order is not fixed in age.
    crossings = {k: downward_crossing(t, values) for k, values in ratios.items()}
    assert all(ratios[k][-1] < 1.0 for k in ratios)
    assert np.any(ratios[4] > ratios[3]) and np.any(ratios[4] < ratios[3])
    a, b, _ = roots()
    del a
    assert abs(ratios[2][-1] - b) < 5e-5
    return {"early": early, "crossings": crossings, "b": b}


def make_figure() -> None:
    checked = run_asserts()
    t = np.linspace(0.0, T_MAX, 3_001)
    styles = {
        2: ("tab:blue", "-"),
        3: ("tab:orange", "--"),
        4: ("#6b4c9a", "-."),
    }

    fig, ax = plt.subplots(figsize=(7.4, 4.55))
    ax.axhspan(1.0, 4.25, color="tab:blue", alpha=0.055, zorder=0)
    ax.axhline(1.0, color="#555555", linestyle="--", linewidth=1.35, zorder=1)
    for k, (color, linestyle) in styles.items():
        ratio = ratio_to_linear(t, k)
        ax.plot(
            t,
            ratio,
            color=color,
            linestyle=linestyle,
            linewidth=2.25,
            label=rf"$k={k}$",
            zorder=3,
        )
        ax.scatter(
            [1.0],
            [checked["early"][k]],
            s=34,
            facecolor="white",
            edgecolor=color,
            linewidth=1.25,
            zorder=5,
        )

    ax.axvline(1.0, color="#999999", linestyle=":", linewidth=0.9, zorder=1)
    ax.text(
        0.68,
        3.45,
        r"at $t=1$: all ratios exceed $1$",
        fontsize=9,
        color="#333333",
        ha="left",
        va="center",
    )
    ax.text(
        10.55,
        1.12,
        "linear scaling",
        fontsize=9,
        color="#555555",
        ha="left",
        va="bottom",
    )
    ax.annotate(
        "curve crossings: no global\npointwise order in $k$",
        xy=(1.95, float(ratio_to_linear(np.array([1.95]), 4)[0])),
        xytext=(4.0, 2.45),
        arrowprops={"arrowstyle": "->", "color": "#333333", "linewidth": 0.85},
        fontsize=9,
        color="#333333",
        ha="left",
        va="center",
    )
    ax.text(
        0.98,
        0.96,
        r"$\lambda=1$, $\mu=0.2$, $\delta=0.05$",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9,
        color="#222222",
    )
    ax.text(
        0.98,
        0.07,
        "shared-clock survival tempers late flux",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=9,
        color="#555555",
    )

    ax.set_xlim(0.0, T_MAX)
    ax.set_ylim(0.0, 4.25)
    ax.set_xlabel(r"infection age $t$")
    ax.set_ylabel(r"flux ratio $g_k(t)/(k g_1(t))$")
    ax.set_title(
        "MOI enhancement is strong early and fades with age",
        loc="left",
        fontweight="bold",
    )
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.86), ncol=3)

    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)


if __name__ == "__main__":
    checked = run_asserts()
    make_figure()
    early = checked["early"]
    crossings = checked["crossings"]
    print(
        "asserts: pass; ratios at t=1="
        + ", ".join(f"k={k}: {early[k]:.6f}" for k in (2, 3, 4))
        + "; crossings of 1="
        + ", ".join(f"k={k}: t={crossings[k]:.4f}" for k in (2, 3, 4))
    )
    print(f"wrote {PDF_PATH} and {PNG_PATH}")
