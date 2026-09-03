#!/usr/bin/env python3
"""Generate N4b.5: extinction-growth trade-off as delta varies."""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/bdc_odes_n4b5_mplconfig")

import numpy as np
from numpy.polynomial.legendre import leggauss

STYLE_DIR = Path(
    "/Users/adamaldridge/Desktop/Thesis content 🎓 "
    "/4 BDC additional and BMVR/Figures run/style"
)
sys.path.insert(0, str(STYLE_DIR))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402


LAMBDA = 1.0
MU = 0.0
CLEARANCE = 1.0
R0 = 2.0
DELTA_MIN = 0.03
DELTA_MAX = 0.80
MARKER_DELTAS = np.asarray([0.03, 0.05, 0.10, 0.20, 0.40, 0.80])

_NODES, _WEIGHTS = leggauss(420)
_X = 0.5 * (_NODES + 1.0)
_WEIGHTS = 0.5 * _WEIGHTS


def derived_parameters(delta: float) -> tuple[float, float, float, float]:
    eta = (LAMBDA + MU + delta) / (2.0 * LAMBDA)
    radical = np.sqrt(eta**2 - MU / LAMBDA)
    a = eta + radical
    b = eta - radical
    flooding = a * (1.0 - b)
    v_inf = flooding / (a - 1.0)
    theta = LAMBDA * (a - b)
    return a, b, v_inf, theta


def release_transform(growth_rate: float, delta: float) -> float:
    """Evaluate delta times the Laplace transform of K."""
    a, b, _, theta = derived_parameters(delta)
    A, B = a - 1.0, 1.0 - b
    fixation_i = (a * B * _X + b * A) / (B * _X + A)
    first_moment_j = (a - b) ** 2 * _X / (B * _X + A) ** 2
    second_moment_k = (
        1.0 + 2.0 * LAMBDA / delta * (1.0 - fixation_i)
    ) * first_moment_j
    integrand = second_moment_k * _X ** (growth_rate / theta - 1.0)
    return float(delta / theta * np.sum(_WEIGHTS * integrand))


def matched_quantities(delta: float) -> tuple[float, float, float, float]:
    a, b, v_inf, _ = derived_parameters(delta)
    coupling = R0 * CLEARANCE / v_inf
    q = coupling / (coupling + CLEARANCE)
    offspring_mean = q * v_inf
    assert offspring_mean > 1.0
    flooding = a * (1.0 - b)
    z_ext = (a - 1.0) / q + 1.0 - flooding

    def characteristic(growth_rate: float) -> float:
        return (
            growth_rate
            + CLEARANCE
            - coupling * release_transform(growth_rate, delta)
        )

    lower, upper = 0.0, 1.0
    assert characteristic(lower) < 0.0
    while characteristic(upper) <= 0.0:
        upper *= 2.0
        assert upper < 64.0
    for _ in range(70):
        midpoint = 0.5 * (lower + upper)
        if characteristic(midpoint) > 0.0:
            upper = midpoint
        else:
            lower = midpoint
    growth_rate = 0.5 * (lower + upper)
    assert abs(characteristic(growth_rate)) < 2e-11
    return growth_rate, z_ext, q, v_inf


def calculate_curve() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    deltas = np.geomspace(DELTA_MIN, DELTA_MAX, 181)
    quantities = np.asarray([matched_quantities(delta) for delta in deltas])
    return deltas, quantities[:, 0], quantities[:, 1]


def run_asserts(
    deltas: np.ndarray, growth_rates: np.ndarray, extinction: np.ndarray
) -> None:
    assert np.all(np.diff(deltas) > 0.0)
    assert np.all(np.diff(growth_rates) > 0.0)
    assert np.all(np.diff(extinction) > 0.0)
    assert np.all((extinction > 0.0) & (extinction < 1.0))

    closed_form_extinction = 0.5 * (1.0 + deltas)
    assert np.max(np.abs(extinction - closed_form_extinction)) < 2e-12
    assert abs(extinction[0] - 0.515) < 1e-12
    assert abs(extinction[-1] - 0.900) < 1e-12
    assert abs(growth_rates[0] - 0.133097) < 1e-3
    assert abs(growth_rates[-1] - 0.393636) < 1e-3

    for delta in (DELTA_MIN, 0.10, DELTA_MAX):
        _, _, _, v_inf = matched_quantities(delta)
        assert abs(release_transform(0.0, delta) - v_inf) < 2e-8


def make_figure(
    deltas: np.ndarray, growth_rates: np.ndarray, extinction: np.ndarray
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(6.15, 4.05))
    ax.tick_params(labelsize=10)
    ax.plot(
        growth_rates,
        extinction,
        color="#6b4c9a",
        linewidth=2.5,
        zorder=2,
    )

    marker_growth = []
    marker_extinction = []
    for delta in MARKER_DELTAS:
        growth_rate, z_ext, _, _ = matched_quantities(float(delta))
        marker_growth.append(growth_rate)
        marker_extinction.append(z_ext)
    marker_growth = np.asarray(marker_growth)
    marker_extinction = np.asarray(marker_extinction)
    ax.scatter(
        marker_growth,
        marker_extinction,
        s=46,
        facecolor="white",
        edgecolor="#6b4c9a",
        linewidth=1.5,
        zorder=4,
        label=r"selected $\delta$ values",
    )

    label_offsets = ((8, 8), (8, 8), (8, 8), (8, 12), (-10, 10), (-8, -18))
    for delta, x_value, y_value, offset in zip(
        MARKER_DELTAS, marker_growth, marker_extinction, label_offsets
    ):
        ax.annotate(
            rf"${delta:g}$",
            xy=(x_value, y_value),
            xytext=offset,
            textcoords="offset points",
            ha="left" if offset[0] >= 0 else "right",
            va="bottom" if offset[1] >= 0 else "top",
            fontsize=9.5,
            color="#3d2d58",
        )

    arrow_start = 94
    arrow_end = 121
    ax.annotate(
        "",
        xy=(growth_rates[arrow_end], extinction[arrow_end]),
        xytext=(growth_rates[arrow_start], extinction[arrow_start]),
        arrowprops=dict(
            arrowstyle="-|>",
            color="tab:orange",
            linewidth=1.7,
            shrinkA=3,
            shrinkB=3,
        ),
    )
    midpoint_x = 0.5 * (growth_rates[arrow_start] + growth_rates[arrow_end])
    midpoint_y = 0.5 * (extinction[arrow_start] + extinction[arrow_end])
    ax.text(
        midpoint_x - 0.005,
        midpoint_y + 0.032,
        r"increasing $\delta$",
        ha="center",
        va="bottom",
        fontsize=9.8,
        color="#a94f00",
    )

    ax.text(
        0.03,
        0.96,
        r"$\lambda=1$, $\mu=0$, $c=1$, $R_0=2$",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9.4,
        color="#444444",
    )
    ax.text(
        0.97,
        0.07,
        r"coupling reset along the curve to keep $R_0=2$",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=9.4,
        color="#444444",
    )
    ax.set(
        xlabel=r"exponential growth rate $r$",
        ylabel=r"extinction probability $z_{\mathrm{ext}}$",
        title=r"Tuning $\delta$ traces a strict extinction–growth trade-off",
    )
    x_margin = 0.045 * (growth_rates[-1] - growth_rates[0])
    y_margin = 0.075 * (extinction[-1] - extinction[0])
    ax.set_xlim(growth_rates[0] - x_margin, growth_rates[-1] + x_margin)
    ax.set_ylim(extinction[0] - y_margin, extinction[-1] + y_margin)
    fig.tight_layout()
    return fig


def main() -> None:
    deltas, growth_rates, extinction = calculate_curve()
    run_asserts(deltas, growth_rates, extinction)
    workdir = Path(__file__).resolve().parent
    figures_dir = workdir.parents[1]
    production_pdf = figures_dir / "N4b_5_pareto_extinction_growth.pdf"
    preview_png = workdir / "preview.png"
    fig = make_figure(deltas, growth_rates, extinction)
    style_rc.save_figure(fig, production_pdf, preview_png, dpi=240)
    plt.close(fig)
    print(
        "asserts: pass; endpoints "
        f"delta={deltas[0]:.3f}: (r,z)=({growth_rates[0]:.6f},{extinction[0]:.6f}); "
        f"delta={deltas[-1]:.3f}: (r,z)=({growth_rates[-1]:.6f},{extinction[-1]:.6f})"
    )
    print(f"wrote {production_pdf} and {preview_png}")


if __name__ == "__main__":
    main()
