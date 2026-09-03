#!/usr/bin/env python3
"""Rate landscapes of b and V_infinity at lambda = 1."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

STYLE_DIR = Path(__file__).resolve().parents[2] / "_style"
sys.path.insert(0, str(STYLE_DIR))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.colors as mcolors  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FixedLocator, FuncFormatter, NullFormatter  # noqa: E402

HERE = Path(__file__).resolve().parent
PDF_PATH = HERE.parents[2] / "figures" / "F4_b_Vinf_landscape.pdf"
PNG_PATH = HERE / "preview.png"

LAMBDA = 1.0
POINTS = {"working": (0.2, 0.05), "no_death": (0.0, 0.1)}


def quantities(mu, delta):
    mu_arr = np.asarray(mu, dtype=float)
    delta_arr = np.asarray(delta, dtype=float)
    eta = (LAMBDA + mu_arr + delta_arr) / (2.0 * LAMBDA)
    b = eta - np.sqrt(eta**2 - mu_arr / LAMBDA)
    V_inf = (LAMBDA - mu_arr) * (1.0 - b) / delta_arr + 1.0
    return b, V_inf


def add_contours(ax, X, Y, Z, levels, fmt):
    ax.contour(X, Y, Z, levels=levels, colors="white", linewidths=1.4, alpha=0.85)
    contours = ax.contour(X, Y, Z, levels=levels, colors="#252525", linewidths=0.55)
    labels = ax.clabel(contours, inline=True, inline_spacing=3, fontsize=7, fmt=fmt)
    for label in labels:
        label.set_bbox(dict(facecolor="white", edgecolor="none", alpha=0.7, pad=0.1))


def mark_points(ax):
    mu_w, delta_w = POINTS["working"]
    mu_0, delta_0 = POINTS["no_death"]
    ax.scatter([mu_w], [delta_w], marker="*", s=90, facecolor=style_rc.VERMILLION,
               edgecolor="white", linewidth=0.8, zorder=8, clip_on=False)
    ax.scatter([mu_0], [delta_0], marker="D", s=36, facecolor=style_rc.BLUE,
               edgecolor="white", linewidth=0.8, zorder=8, clip_on=False)


def main() -> None:
    mu = np.linspace(0.0, 1.0, 121)
    delta = np.geomspace(0.01, 1.0, 121)
    MU, DELTA = np.meshgrid(mu, delta)
    b_grid, V_grid = quantities(MU, DELTA)
    b_w, V_w = quantities(*POINTS["working"])
    b_0, V_0 = quantities(*POINTS["no_death"])
    assert abs(float(b_0)) < 1e-12
    assert abs(float(V_0) - 11.0) < 1e-12

    fig, (ax_b, ax_v) = plt.subplots(1, 2, figsize=(7.6, 3.5))
    mesh_b = ax_b.contourf(
        MU, DELTA, b_grid, levels=np.linspace(0.0, 1.0, 41),
        cmap="cividis", vmin=0.0, vmax=1.0, antialiased=False,
    )
    add_contours(ax_b, MU, DELTA, b_grid, [0.1, 0.2, 0.4, 0.6, 0.8], "%.1f")
    cbar_b = fig.colorbar(mesh_b, ax=ax_b, pad=0.025, fraction=0.052)
    cbar_b.set_label(r"$b$")
    cbar_b.set_ticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])

    mesh_v = ax_v.contourf(
        MU, DELTA, V_grid, levels=np.geomspace(1.0, 101.0, 41),
        cmap="magma", norm=mcolors.LogNorm(vmin=1.0, vmax=101.0), antialiased=False,
    )
    add_contours(ax_v, MU, DELTA, V_grid, [2.0, 5.0, 10.0, 20.0, 50.0, 100.0], "%g")
    cbar_v = fig.colorbar(mesh_v, ax=ax_v, pad=0.025, fraction=0.052)
    cbar_v.set_label(r"$V_\infty$")
    cbar_v.set_ticks([1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0])
    cbar_v.ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:g}"))
    cbar_v.ax.yaxis.set_minor_formatter(NullFormatter())

    mark_points(ax_b)
    mark_points(ax_v)
    ax_b.text(0.04, 1.04, r"(a)", transform=ax_b.transAxes)
    ax_v.text(0.04, 1.04, r"(b)", transform=ax_v.transAxes)

    delta_ticks = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]
    for ax in (ax_b, ax_v):
        ax.set_yscale("log")
        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(0.01, 1.0)
        ax.set_xlabel(r"death rate $\mu$")
        ax.set_ylabel(r"catastrophe rate $\delta$")
        ax.yaxis.set_major_locator(FixedLocator(delta_ticks))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:g}"))
        ax.yaxis.set_minor_formatter(NullFormatter())
        ax.grid(False)

    fig.tight_layout(w_pad=1.4)
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)
    print(f"working b={float(b_w):.4f}, V_inf={float(V_w):.2f}; wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
