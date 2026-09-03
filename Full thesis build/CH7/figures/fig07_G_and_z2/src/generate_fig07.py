#!/usr/bin/env python3
"""Generate Figure 7: the exact type-2 solution and moving coordinate z_2."""

from __future__ import annotations

import json
import math
import platform
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
OUT_DIR = HERE.parent

# Physical rates from the figure brief. Scaled quantities are formed explicitly
# below, even though lambda_1=1 makes their numerical values coincide here.
LAMBDA1 = 1.00
LAMBDA2 = 0.85
MU2 = 0.40
DELTA2 = 0.18

T_MAX = 15.0
RK4_STEP = 0.001

VERMILLION = "#D55E00"
TEAL = "#009E73"
INK = "#1a1c1f"
SOFT_INK = "#565b62"
GRID = "#e3e6ea"
SOFT_FILL = "#fafafa"
VERMILLION_FILL = "#fff3ec"
TEAL_FILL = "#edf8f4"


def scaled_constants() -> dict[str, float]:
    """Implement the paper's scaled definitions for the type-2 solution."""
    hat_lambda2 = LAMBDA2 / LAMBDA1
    hat_mu2 = MU2 / LAMBDA1
    hat_delta2 = DELTA2 / LAMBDA1
    hat_delta = math.sqrt(
        (hat_lambda2 + hat_mu2 + hat_delta2) ** 2
        - 4.0 * hat_lambda2 * hat_mu2
    )
    r_plus = (
        hat_lambda2 + hat_mu2 + hat_delta2 + hat_delta
    ) / (2.0 * hat_lambda2)
    r_minus = (
        hat_lambda2 + hat_mu2 + hat_delta2 - hat_delta
    ) / (2.0 * hat_lambda2)
    alpha2 = r_plus - r_minus
    hat_q2 = -hat_lambda2 * alpha2
    z20 = (r_minus - 1.0) / (r_plus - 1.0)
    return {
        "hat_lambda2": hat_lambda2,
        "hat_mu2": hat_mu2,
        "hat_delta2": hat_delta2,
        "hat_Delta2": hat_delta,
        "r2_plus": r_plus,
        "r2_minus": r_minus,
        "alpha2": alpha2,
        "hat_q2": hat_q2,
        "z2_0": z20,
    }


def z2_physical(t: np.ndarray | float, constants: dict[str, float]) -> np.ndarray | float:
    """Return z_2(lambda_1 t), expressed on the physical-time axis."""
    return constants["z2_0"] * np.exp(constants["hat_q2"] * LAMBDA1 * t)


def g_closed_form(t: np.ndarray | float, constants: dict[str, float]) -> np.ndarray | float:
    """Evaluate G(t)=G-hat(lambda_1 t) using the moving coordinate."""
    z = z2_physical(t, constants)
    return constants["r2_minus"] - constants["alpha2"] * z / (1.0 - z)


def unscaled_rhs(g: float) -> float:
    """Unscaled physical-time type-2 backward equation."""
    return LAMBDA2 * g * g - (LAMBDA2 + MU2 + DELTA2) * g + MU2


def integrate_rk4(t_end: float, step: float) -> tuple[np.ndarray, np.ndarray]:
    """Classical fixed-step RK4 for the unscaled type-2 ODE."""
    n_steps = int(round(t_end / step))
    if not math.isclose(n_steps * step, t_end, rel_tol=0.0, abs_tol=1e-13):
        raise ValueError("t_end must be an integer multiple of step")

    times = np.linspace(0.0, t_end, n_steps + 1)
    values = np.empty(n_steps + 1)
    values[0] = 1.0
    for i in range(n_steps):
        g = float(values[i])
        k1 = unscaled_rhs(g)
        k2 = unscaled_rhs(g + 0.5 * step * k1)
        k3 = unscaled_rhs(g + 0.5 * step * k2)
        k4 = unscaled_rhs(g + step * k3)
        values[i + 1] = g + step * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
    return times, values


def configure_matplotlib() -> None:
    matplotlib.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
            "mathtext.fontset": "cm",
            "font.size": 17.25,
            "axes.titlesize": 19.5,
            "axes.labelsize": 17.7,
            "xtick.labelsize": 15.3,
            "ytick.labelsize": 15.3,
            "legend.fontsize": 14.4,
            "axes.linewidth": 0.8,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def style_axis(ax: plt.Axes) -> None:
    ax.set_facecolor("white")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(INK)
    ax.spines["bottom"].set_color(INK)
    ax.tick_params(colors=INK, length=3.5, width=0.8)
    ax.grid(axis="y", color=GRID, linewidth=0.75, zorder=0)
    ax.set_axisbelow(True)


def panel_label(ax: plt.Axes, label: str) -> None:
    ax.text(
        -0.13,
        1.10,
        label,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=20.25,
        fontweight="bold",
        color=INK,
    )


def main() -> None:
    configure_matplotlib()
    c = scaled_constants()

    if not (0.0 <= c["r2_minus"] < 1.0 < c["r2_plus"]):
        raise AssertionError("The computed roots do not have the paper's probability ordering")
    if not c["z2_0"] < 0.0 or not c["hat_q2"] < 0.0:
        raise AssertionError("Expected z2_0<0 and hat_q2<0")
    if not math.isclose(c["hat_q2"], -c["hat_Delta2"], abs_tol=1e-14):
        raise AssertionError("hat q2 must equal -hat Delta2")

    rk_t, rk_g = integrate_rk4(T_MAX, RK4_STEP)
    cf_on_rk_grid = np.asarray(g_closed_form(rk_t, c))
    max_abs_error = float(np.max(np.abs(cf_on_rk_grid - rk_g)))
    if max_abs_error >= 1e-9:
        raise AssertionError(f"Closed form/RK4 discrepancy too large: {max_abs_error:.3e}")

    t = np.linspace(0.0, T_MAX, 1400)
    z = np.asarray(z2_physical(t, c))
    g = np.asarray(g_closed_form(t, c))
    if not np.all(np.diff(g) < 0.0):
        raise AssertionError("G(t) must decrease on the plotted interval")
    if not np.all(np.diff(z) > 0.0) or not np.all(z < 0.0):
        raise AssertionError("z2 must remain negative and increase monotonically towards zero")
    if not math.isclose(float(g[0]), 1.0, abs_tol=1e-14):
        raise AssertionError("The closed form must satisfy G(0)=1")

    fig, axes = plt.subplots(1, 3, figsize=(16.5, 6.2), constrained_layout=False)
    fig.patch.set_facecolor("white")
    plt.subplots_adjust(left=0.07, right=0.985, bottom=0.22, top=0.88, wspace=0.40)

    # (a) Exact physical-time probability and independent RK4 check.
    ax = axes[0]
    style_axis(ax)
    panel_label(ax, "(a)")
    ax.axhspan(c["r2_minus"], 1.0, color=VERMILLION_FILL, alpha=0.70, zorder=-2)
    ax.plot(t, g, color=VERMILLION, linewidth=3.0, zorder=3)
    ax.axhline(
        c["r2_minus"],
        color=SOFT_INK,
        linewidth=1.25,
        linestyle=(0, (5, 3)),
        zorder=2,
    )
    ax.scatter([0.0], [1.0], s=42, color=VERMILLION, edgecolor="white", linewidth=0.9, zorder=5)
    ax.annotate(
        r"$G(0)=1$",
        xy=(0.0, 1.0),
        xytext=(1.45, 0.935),
        arrowprops=dict(arrowstyle="->", color=SOFT_INK, lw=0.9),
        color=INK,
        fontsize=15.3,
    )
    ax.text(
        14.7,
        c["r2_minus"] + 0.025,
        rf"$r_{{2,-}}={c['r2_minus']:.3f}$",
        ha="right",
        va="bottom",
        color=SOFT_INK,
        fontsize=15.3,
    )
    ax.set_xlim(0.0, T_MAX)
    ax.set_ylim(0.30, 1.04)
    ax.set_xticks([0, 3, 6, 9, 12, 15])
    ax.set_yticks([0.4, 0.6, 0.8, 1.0])
    ax.set_xlabel(r"Physical time, $t$")
    ax.set_ylabel(r"No-catastrophe probability, $G(t)$")
    ax.set_title("Exact decay to the stable limit", loc="left", pad=14, color=INK, fontweight="bold")

    # (b) The moving coordinate on the same physical-time interval.
    ax = axes[1]
    style_axis(ax)
    panel_label(ax, "(b)")
    ax.axhspan(c["z2_0"], 0.0, color=TEAL_FILL, alpha=0.85, zorder=-2)
    ax.plot(t, z, color=TEAL, linewidth=3.0, zorder=3)
    ax.axhline(0.0, color=SOFT_INK, linewidth=1.25, linestyle=(0, (5, 3)), zorder=2)
    ax.scatter([0.0], [c["z2_0"]], s=42, color=TEAL, edgecolor="white", linewidth=0.9, zorder=5)
    ax.text(
        14.65,
        -0.10,
        r"$z_2(\lambda_1t)\to0^{-}$",
        ha="right",
        va="top",
        color=TEAL,
        fontsize=15.6,
        fontweight="bold",
    )
    ax.text(
        0.965,
        0.16,
        r"$z_2(\lambda_1t)=z_{2,0}e^{\hat q_2\lambda_1t}$",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        color=INK,
        fontsize=16.5,
        bbox=dict(boxstyle="round,pad=0.32", facecolor="white", edgecolor=GRID, linewidth=0.8),
    )
    ax.set_xlim(0.0, T_MAX)
    ax.set_ylim(-2.08, 0.12)
    ax.set_xticks([0, 3, 6, 9, 12, 15])
    ax.set_yticks([-2.0, -1.5, -1.0, -0.5, 0.0])
    ax.set_xlabel(r"Physical time, $t$")
    ax.set_ylabel(r"Moving coordinate, $z_2(\lambda_1t)$")
    ax.set_title("Exponential motion towards zero", loc="left", pad=14, color=INK, fontweight="bold")

    # (c) Parametric view: all time dependence becomes a rational function of z_2.
    ax = axes[2]
    style_axis(ax)
    panel_label(ax, "(c)")
    ax.set_facecolor(SOFT_FILL)
    ax.plot(z, g, color=VERMILLION, linewidth=3.0, zorder=3)
    time_marks = np.array([0.0, 1.0, 2.0, 4.0, 8.0, 15.0])
    mark_z = np.asarray(z2_physical(time_marks, c))
    mark_g = np.asarray(g_closed_form(time_marks, c))
    ax.scatter(
        mark_z,
        mark_g,
        s=42,
        facecolor="white",
        edgecolor=VERMILLION,
        linewidth=1.1,
        zorder=4,
    )
    for time_value, zz, gg in zip(time_marks[:4], mark_z[:4], mark_g[:4]):
        ax.annotate(
            rf"$t={time_value:g}$",
            xy=(zz, gg),
            xytext=(5, 7),
            textcoords="offset points",
            color=SOFT_INK,
            fontsize=13.35,
        )
    # Direction arrow evaluated at two nearby times along the parametric curve.
    arrow_t0, arrow_t1 = 2.45, 3.15
    ax.annotate(
        "",
        xy=(float(z2_physical(arrow_t1, c)), float(g_closed_form(arrow_t1, c))),
        xytext=(float(z2_physical(arrow_t0, c)), float(g_closed_form(arrow_t0, c))),
        arrowprops=dict(arrowstyle="-|>", color=VERMILLION, lw=2.0, mutation_scale=13),
        zorder=5,
    )
    ax.scatter([0.0], [c["r2_minus"]], s=48, color=SOFT_INK, edgecolor="white", linewidth=0.9, zorder=5)
    ax.text(
        -0.22,
        c["r2_minus"] + 0.035,
        rf"$(0,r_{{2,-}})$",
        ha="right",
        va="bottom",
        color=SOFT_INK,
        fontsize=15.0,
    )
    ax.text(
        0.96,
        0.93,
        r"$G=r_{2,-}-\alpha_2\,\dfrac{z_2}{1-z_2}$",
        transform=ax.transAxes,
        ha="right",
        va="top",
        color=INK,
        fontsize=16.8,
        bbox=dict(boxstyle="round,pad=0.34", facecolor="white", edgecolor=GRID, linewidth=0.8),
    )
    ax.set_xlim(-2.08, 0.10)
    ax.set_ylim(0.30, 1.04)
    ax.set_xticks([-2.0, -1.5, -1.0, -0.5, 0.0])
    ax.set_yticks([0.4, 0.6, 0.8, 1.0])
    ax.set_xlabel(r"Coordinate, $z_2$")
    ax.set_ylabel(r"Probability, $G$")
    ax.set_title("Time becomes a rational coordinate", loc="left", pad=14, color=INK, fontweight="bold")

    png_path = OUT_DIR / "fig07.png"
    pdf_path = OUT_DIR / "fig07.pdf"
    fig.savefig(png_path, dpi=400, facecolor="white", bbox_inches="tight", pad_inches=0.08)
    fig.savefig(pdf_path, facecolor="white", bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)

    meta = {
        "figure": "fig07_G_and_z2",
        "parameters": {
            "lambda1": LAMBDA1,
            "lambda2": LAMBDA2,
            "mu2": MU2,
            "delta2": DELTA2,
        },
        "scaled_parameters": {
            "hat_lambda2": c["hat_lambda2"],
            "hat_mu2": c["hat_mu2"],
            "hat_delta2": c["hat_delta2"],
        },
        "derived": {
            "hat_Delta2": c["hat_Delta2"],
            "r2_minus": c["r2_minus"],
            "r2_plus": c["r2_plus"],
            "alpha2": c["alpha2"],
            "hat_q2": c["hat_q2"],
            "z2_0": c["z2_0"],
            "G_at_tmax": float(g[-1]),
            "z2_at_tmax": float(z[-1]),
            "G_gap_at_tmax": float(g[-1] - c["r2_minus"]),
        },
        "validation": {
            "max_abs_closed_form_vs_rk4": max_abs_error,
            "integration_method": "fixed-step classical RK4 on the unscaled physical-time ODE",
            "rk4_step": RK4_STEP,
            "plotted_time_interval": [0.0, T_MAX],
            "time_axis": "physical t; internal closed form evaluated at hat_t=lambda1*t",
            "checks": {
                "G0_equals_1": True,
                "G_strictly_decreasing": True,
                "z2_negative": True,
                "z2_strictly_increasing_to_zero": True,
                "hat_q2_equals_minus_hat_Delta2": True,
            },
        },
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "matplotlib": matplotlib.__version__,
        },
        "random_seed": None,
        "ai_generated_content": False,
    }
    with (OUT_DIR / "meta.json").open("w", encoding="utf-8") as handle:
        json.dump(meta, handle, indent=2)
        handle.write("\n")

    print(f"Wrote {png_path}")
    print(f"Wrote {pdf_path}")
    print(
        f"r2_minus={c['r2_minus']:.12f}, r2_plus={c['r2_plus']:.12f}, "
        f"z2_0={c['z2_0']:.12f}"
    )
    print(f"max |G_closed_form - G_RK4|={max_abs_error:.3e}")


if __name__ == "__main__":
    main()
