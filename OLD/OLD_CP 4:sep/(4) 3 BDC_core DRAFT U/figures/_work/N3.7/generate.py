#!/usr/bin/env python3
"""Generate N3.7: rate landscapes of b and V_infinity at lambda=1."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(
    0,
    "/Users/adamaldridge/Desktop/Thesis content 🎓 /4 BDC additional and BMVR/Figures run/style",
)
import style_rc  # noqa: E402

style_rc.apply()

import matplotlib.colors as mcolors  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FixedLocator, FuncFormatter, NullFormatter  # noqa: E402


HERE = Path(__file__).resolve().parent
CHAPTER = HERE.parents[2]
PDF_PATH = CHAPTER / "figures" / "N3_7_b_Vinf_landscape.pdf"
PNG_PATH = HERE / "preview.png"

LAMBDA = 1.0
POINTS = {
    "working": (0.2, 0.05),
    "no_death": (0.0, 0.1),
}


def quantities(mu: np.ndarray | float, delta: np.ndarray | float) -> tuple[np.ndarray, np.ndarray]:
    mu_arr = np.asarray(mu, dtype=float)
    delta_arr = np.asarray(delta, dtype=float)
    eta = (LAMBDA + mu_arr + delta_arr) / (2.0 * LAMBDA)
    b = eta - np.sqrt(eta**2 - mu_arr / LAMBDA)
    V_inf = (LAMBDA - mu_arr) * (1.0 - b) / delta_arr + 1.0
    return b, V_inf


def validate(b_grid: np.ndarray, V_grid: np.ndarray) -> dict[str, tuple[float, float]]:
    assert np.all(np.isfinite(b_grid))
    assert np.all(np.isfinite(V_grid))
    assert float(b_grid.min()) >= -1e-12
    assert float(b_grid.max()) <= 1.0 + 1e-12
    assert float(V_grid.min()) >= 1.0 - 1e-12

    values: dict[str, tuple[float, float]] = {}
    for name, (mu, delta) in POINTS.items():
        b, V = quantities(mu, delta)
        values[name] = (float(b), float(V))

    b_work, V_work = values["working"]
    b_zero, V_zero = values["no_death"]
    assert abs(b_work - 0.18839377008567548) < 1e-12
    assert abs(V_work - 13.985699678629192) < 1e-11
    assert abs(b_zero) < 1e-13
    assert abs(V_zero - 11.0) < 1e-12
    return values


def add_two_tone_contours(ax: plt.Axes, X: np.ndarray, Y: np.ndarray, Z: np.ndarray, levels: list[float], fmt: str) -> None:
    ax.contour(X, Y, Z, levels=levels, colors="white", linewidths=1.65, alpha=0.9)
    contours = ax.contour(X, Y, Z, levels=levels, colors="#252525", linewidths=0.65, alpha=0.9)
    labels = ax.clabel(contours, inline=True, inline_spacing=3, fontsize=7.5, fmt=fmt)
    for label in labels:
        label.set_bbox(dict(facecolor="white", edgecolor="none", alpha=0.72, pad=0.12))


def mark_points(ax: plt.Axes, values: dict[str, tuple[float, float]], quantity_index: int) -> None:
    mu_w, delta_w = POINTS["working"]
    mu_0, delta_0 = POINTS["no_death"]
    value_w = values["working"][quantity_index]
    value_0 = values["no_death"][quantity_index]

    ax.scatter(
        [mu_w],
        [delta_w],
        marker="*",
        s=115,
        facecolor="#8b1e1e",
        edgecolor="white",
        linewidth=1.0,
        zorder=8,
        clip_on=False,
    )
    ax.scatter(
        [mu_0],
        [delta_0],
        marker="D",
        s=48,
        facecolor="#1f4e79",
        edgecolor="white",
        linewidth=1.0,
        zorder=8,
        clip_on=False,
    )

    if quantity_index == 0:
        text_w = "working point\n" + rf"$b={value_w:.3f}$"
        text_0 = "no death\n" + rf"$b={value_0:.0f}$"
    else:
        text_w = "working point\n" + rf"$V_\infty={value_w:.2f}$"
        text_0 = "no death\n" + rf"$V_\infty={value_0:.0f}$"

    ax.annotate(
        text_w,
        xy=(mu_w, delta_w),
        xytext=(0.34, 0.027),
        arrowprops=dict(arrowstyle="->", color="#8b1e1e", linewidth=1.0),
        color="#681616",
        fontsize=8.3,
        ha="left",
        va="top",
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.82),
        zorder=9,
    )
    ax.annotate(
        text_0,
        xy=(mu_0, delta_0),
        xytext=(0.095, 0.19),
        arrowprops=dict(arrowstyle="->", color="#1f4e79", linewidth=1.0),
        color="#163b5c",
        fontsize=8.3,
        ha="left",
        va="bottom",
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.82),
        zorder=9,
    )


def build() -> dict[str, tuple[float, float]]:
    # A 121 x 121 analytic mesh is visually smooth at thesis width while
    # keeping every heatmap cell as vector geometry in the production PDF.
    mu = np.linspace(0.0, 1.0, 121)
    delta = np.geomspace(0.01, 1.0, 121)
    MU, DELTA = np.meshgrid(mu, delta)
    b_grid, V_grid = quantities(MU, DELTA)
    values = validate(b_grid, V_grid)

    fig, axes = plt.subplots(1, 2, figsize=(11.7, 4.75))
    ax_b, ax_v = axes

    mesh_b = ax_b.contourf(
        MU,
        DELTA,
        b_grid,
        levels=np.linspace(0.0, 1.0, 41),
        cmap="cividis",
        vmin=0.0,
        vmax=1.0,
        antialiased=False,
    )
    add_two_tone_contours(ax_b, MU, DELTA, b_grid, [0.1, 0.2, 0.4, 0.6, 0.8], "%.1f")
    cbar_b = fig.colorbar(mesh_b, ax=ax_b, pad=0.025, fraction=0.052)
    cbar_b.set_label(r"internal-extinction probability $b$")
    cbar_b.set_ticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])

    mesh_v = ax_v.contourf(
        MU,
        DELTA,
        V_grid,
        levels=np.geomspace(1.0, 101.0, 41),
        cmap="magma",
        norm=mcolors.LogNorm(vmin=1.0, vmax=101.0),
        antialiased=False,
    )
    add_two_tone_contours(ax_v, MU, DELTA, V_grid, [2.0, 5.0, 10.0, 20.0, 50.0, 100.0], "%g")
    cbar_v = fig.colorbar(mesh_v, ax=ax_v, pad=0.025, fraction=0.052)
    cbar_v.set_label(r"mean release $V_\infty$")
    cbar_v.set_ticks([1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0])
    cbar_v.ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:g}"))
    cbar_v.ax.yaxis.set_minor_formatter(NullFormatter())

    mark_points(ax_b, values, 0)
    mark_points(ax_v, values, 1)

    ax_b.set_title("(a) Weak catastrophe exposes internal extinction", loc="left", pad=9)
    ax_v.set_title("(b) Low catastrophe creates a high-yield ridge", loc="left", pad=9)

    delta_ticks = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]
    for ax in axes:
        ax.set_yscale("log")
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(0.01, 1.0)
        ax.set_xlabel(r"death rate $\mu$")
        ax.set_ylabel(r"catastrophe rate $\delta$")
        ax.yaxis.set_major_locator(FixedLocator(delta_ticks))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:g}"))
        ax.yaxis.set_minor_formatter(NullFormatter())
        ax.grid(False)

    fig.tight_layout(w_pad=1.8, pad=1.55)
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)
    return values


if __name__ == "__main__":
    point_values = build()
    b_w, V_w = point_values["working"]
    b_0, V_0 = point_values["no_death"]
    print(
        "N3.7 asserts passed: "
        f"working b={b_w:.12f}, V_inf={V_w:.12f}; "
        f"no-death b={b_0:.12f}, V_inf={V_0:.12f}"
    )
