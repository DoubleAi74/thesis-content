#!/usr/bin/env python3
"""Generate N4b.4: the flooding-parameter landscape at lambda=1."""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/bdc_odes_n4b4_mplconfig")

import numpy as np

STYLE_DIR = Path(
    "/Users/adamaldridge/Desktop/Thesis content 🎓 "
    "/4 BDC additional and BMVR/Figures run/style"
)
sys.path.insert(0, str(STYLE_DIR))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm  # noqa: E402

plt.rcParams["savefig.dpi"] = 220


LAMBDA = 1.0
WORKED_POINTS = (
    (0.0, 0.1, "(i)", 1.10),
    (0.5, 1.0 / 3.0, "(ii)", 1.00),
    (0.9, 0.1, "(iii)", 0.42),
)


def flooding_parameter(mu: np.ndarray | float, delta: np.ndarray | float):
    mu_array = np.asarray(mu, dtype=float)
    delta_array = np.asarray(delta, dtype=float)
    eta = (LAMBDA + mu_array + delta_array) / (2.0 * LAMBDA)
    a = eta + np.sqrt(eta**2 - mu_array / LAMBDA)
    return a - mu_array / LAMBDA


def critical_delta(mu: np.ndarray | float):
    mu_array = np.asarray(mu, dtype=float)
    return LAMBDA * mu_array / (LAMBDA + mu_array)


def run_asserts() -> None:
    values = np.asarray(
        [flooding_parameter(mu, delta) for mu, delta, _, _ in WORKED_POINTS]
    )
    assert values[0] > 1.0
    assert abs(values[1] - 1.0) < 1e-12
    assert values[2] < 1.0
    expected = np.asarray([point[3] for point in WORKED_POINTS])
    assert np.max(np.abs(values - expected)) < 5e-3

    test_mu = np.linspace(0.0, 1.05, 301)
    boundary_values = flooding_parameter(test_mu, critical_delta(test_mu))
    assert np.max(np.abs(boundary_values - 1.0)) < 2e-12


def make_figure() -> plt.Figure:
    mu = np.linspace(0.0, 1.05, 421)
    delta = np.linspace(0.0, 0.75, 361)
    MU, DELTA = np.meshgrid(mu, delta)
    landscape = flooding_parameter(MU, DELTA)

    cmap = LinearSegmentedColormap.from_list(
        "flooding_balance",
        ["#d95f02", "#fddbc7", "#f7f7f7", "#d1e5f0", "#2166ac"],
    )
    norm = TwoSlopeNorm(vmin=0.0, vcenter=1.0, vmax=1.75)

    fig, ax = plt.subplots(figsize=(6.15, 4.25))
    ax.tick_params(labelsize=10)
    mesh = ax.pcolormesh(
        MU,
        DELTA,
        landscape,
        shading="auto",
        cmap=cmap,
        norm=norm,
        rasterized=True,
    )
    boundary_mu = np.linspace(0.0, 1.05, 800)
    boundary_delta = critical_delta(boundary_mu)
    ax.plot(
        boundary_mu,
        boundary_delta,
        color="#222222",
        linewidth=2.0,
        label=r"exact boundary $L=1$",
    )
    ax.text(
        0.69,
        float(critical_delta(0.69)) + 0.045,
        r"$\delta_*=\lambda\mu/(\lambda+\mu)$",
        rotation=25,
        ha="center",
        va="bottom",
        fontsize=9.5,
        color="#222222",
    )

    annotation_offsets = ((28, 12), (24, 20), (-48, 14))
    for (mu_value, delta_value, tag, _), offset in zip(
        WORKED_POINTS, annotation_offsets
    ):
        value = float(flooding_parameter(mu_value, delta_value))
        ax.scatter(
            mu_value,
            delta_value,
            s=58,
            facecolor="white",
            edgecolor="#111111",
            linewidth=1.35,
            zorder=5,
            clip_on=False,
        )
        ax.annotate(
            rf"{tag} $L={value:.2f}$",
            xy=(mu_value, delta_value),
            xytext=offset,
            textcoords="offset points",
            arrowprops=dict(
                arrowstyle="-", color="#333333", linewidth=0.9
            ),
            ha="left" if offset[0] > 0 else "right",
            va="bottom",
            fontsize=9.5,
            color="#222222",
        )

    ax.text(
        0.18,
        0.61,
        r"$L>1$",
        ha="center",
        va="center",
        fontsize=12,
        color="#174a75",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.78, pad=2.5),
    )
    ax.text(
        0.84,
        0.20,
        r"$L<1$",
        ha="center",
        va="center",
        fontsize=12,
        color="#9a3e00",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.78, pad=2.5),
    )

    colorbar = fig.colorbar(mesh, ax=ax, pad=0.025, fraction=0.055)
    colorbar.set_label(r"flooding parameter $L$")
    colorbar.set_ticks([0.0, 0.5, 1.0, 1.25, 1.5, 1.75])
    colorbar.ax.tick_params(labelsize=10)

    ax.set(
        xlim=(-0.025, 1.05),
        ylim=(0.0, 0.75),
        xlabel=r"rate $\mu$",
        ylabel=r"rate $\delta$",
        title=r"The curve $L=1$ partitions the rate plane ($\lambda=1$)",
    )
    ax.set_xticks(np.linspace(0.0, 1.0, 6))
    ax.legend(loc="upper right", fontsize=9.5)
    ax.grid(False)
    fig.tight_layout()
    return fig


def main() -> None:
    run_asserts()
    workdir = Path(__file__).resolve().parent
    figures_dir = workdir.parents[1]
    production_pdf = figures_dir / "N4b_4_L_landscape.pdf"
    preview_png = workdir / "preview.png"
    fig = make_figure()
    style_rc.save_figure(fig, production_pdf, preview_png, dpi=240)
    plt.close(fig)
    values = [
        float(flooding_parameter(mu, delta))
        for mu, delta, _, _ in WORKED_POINTS
    ]
    print("asserts: pass; worked-point L values = " + ", ".join(f"{v:.6f}" for v in values))
    print(f"wrote {production_pdf} and {preview_png}")


if __name__ == "__main__":
    main()
