#!/usr/bin/env python3
"""Generate N4b.6: generation-time mechanism for budding versus bursting."""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/bdc_odes_n4b6_mplconfig")

import numpy as np
from numpy.polynomial.legendre import leggauss

sys.path.insert(
    0,
    "/Users/adamaldridge/Desktop/Thesis content 🎓 /4 BDC additional and BMVR/Figures run/style",
)
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_style"))
import style_rc  # noqa: E402

style_rc.apply()

import matplotlib.pyplot as plt  # noqa: E402


WORKDIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORKDIR.parents[2]
PDF_PATH = CHAPTER_DIR / "figures" / "N4b_6_generation_times.pdf"
PNG_PATH = WORKDIR / "preview.png"

LAMBDA = 1.0
MU = 0.0
DELTA = 0.1
CLEARANCE_RATE = 1.0
R0_TARGET = 2.0
BLUE = "#1f77b4"
ORANGE = "#e66101"
PURPLE = "#6b4c9a"

_NODES, _WEIGHTS = leggauss(500)
_X = 0.5 * (_NODES + 1.0)
_WEIGHTS = 0.5 * _WEIGHTS


def derived() -> tuple[float, float, float, float, float, float]:
    eta = (LAMBDA + MU + DELTA) / (2.0 * LAMBDA)
    radical = np.sqrt(eta**2 - MU / LAMBDA)
    a = float(eta + radical)
    b = float(eta - radical)
    theta = LAMBDA * (a - b)
    v_inf = a * (1.0 - b) / (a - 1.0)
    productive_lifetime = np.log(a / (a - 1.0)) / LAMBDA
    matched_death_rate = 1.0 / productive_lifetime
    return a, b, theta, v_inf, productive_lifetime, matched_death_rate


A_ROOT, B_ROOT, THETA, V_INF, PRODUCTIVE_LIFETIME, D_I = derived()
INFECTION_FACTOR = R0_TARGET * CLEARANCE_RATE / V_INF
MATCHED_RELEASE_RATE = V_INF * D_I


def intracellular_functions(t: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return productive survival, K, and the release kernel g=delta*K."""
    t_arr = np.asarray(t, dtype=float)
    cap_a = A_ROOT - 1.0
    cap_b = 1.0 - B_ROOT
    w = np.exp(THETA * t_arr)
    fixation_i = (A_ROOT * cap_b + B_ROOT * cap_a * w) / (cap_b + cap_a * w)
    first_moment_j = (A_ROOT - B_ROOT) ** 2 * w / (cap_b + cap_a * w) ** 2
    second_moment_k = (
        1.0 + 2.0 * LAMBDA / DELTA * (1.0 - fixation_i)
    ) * first_moment_j
    productive_survival = (
        (A_ROOT - B_ROOT) ** 2
        * w
        / ((cap_b + cap_a * w) * (A_ROOT * w - B_ROOT))
    )
    return productive_survival, second_moment_k, DELTA * second_moment_k


def cumulative_trapezoid(values: np.ndarray, t: np.ndarray) -> np.ndarray:
    """Cumulative trapezoidal integral with a zero initial value."""
    result = np.zeros_like(values)
    increments = 0.5 * (values[1:] + values[:-1]) * np.diff(t)
    result[1:] = np.cumsum(increments)
    return result


def generation_densities(t: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return normalized infection-generation densities for both models.

    Eliminating free virus gives the renewal kernel g * exp(-c t).  After
    normalization by R0 this is the convolution of the release-age density
    with the common extracellular density c exp(-c t).
    """
    _, _, burst_release = intracellular_functions(t)
    weighted = burst_release * np.exp(CLEARANCE_RATE * t)
    burst_convolution = np.exp(-CLEARANCE_RATE * t) * cumulative_trapezoid(
        weighted, t
    )
    burst_density = CLEARANCE_RATE * burst_convolution / V_INF

    if abs(CLEARANCE_RATE - D_I) < 1e-12:
        bud_density = D_I**2 * t * np.exp(-D_I * t)
    else:
        bud_density = (
            CLEARANCE_RATE
            * D_I
            / (CLEARANCE_RATE - D_I)
            * (np.exp(-D_I * t) - np.exp(-CLEARANCE_RATE * t))
        )
    return bud_density, burst_density


def release_transform(growth_rate: float) -> float:
    """Evaluate delta times the Laplace transform of K by quadrature."""
    cap_a = A_ROOT - 1.0
    cap_b = 1.0 - B_ROOT
    x = _X
    fixation_i = (A_ROOT * cap_b * x + B_ROOT * cap_a) / (cap_b * x + cap_a)
    first_moment_j = (A_ROOT - B_ROOT) ** 2 * x / (cap_b * x + cap_a) ** 2
    second_moment_k = (
        1.0 + 2.0 * LAMBDA / DELTA * (1.0 - fixation_i)
    ) * first_moment_j
    integrand = second_moment_k * x ** (growth_rate / THETA - 1.0)
    return float(DELTA / THETA * np.sum(_WEIGHTS * integrand))


def burst_release_mean() -> float:
    """Return the mean release age under g/V_infinity."""
    # Direct time integration converges much faster for the first moment
    # than Gauss--Legendre quadrature after x=exp(-theta*t), whose logarithm
    # produces a weak endpoint singularity at x=0.
    t = np.linspace(0.0, 60.0, 240_001)
    _, _, release_kernel = intracellular_functions(t)
    return float(np.trapezoid(t * release_kernel, t) / V_INF)


def growth_rates() -> tuple[float, float]:
    discriminant = (D_I - CLEARANCE_RATE) ** 2 + 4.0 * INFECTION_FACTOR * MATCHED_RELEASE_RATE
    r_bud = 0.5 * (-(D_I + CLEARANCE_RATE) + np.sqrt(discriminant))

    def residual(growth_rate: float) -> float:
        return (
            growth_rate
            + CLEARANCE_RATE
            - INFECTION_FACTOR * release_transform(growth_rate)
        )

    lower, upper = 0.0, 1.0
    assert residual(lower) < 0.0 < residual(upper)
    for _ in range(72):
        midpoint = 0.5 * (lower + upper)
        if residual(midpoint) > 0.0:
            upper = midpoint
        else:
            lower = midpoint
    r_burst = 0.5 * (lower + upper)
    assert abs(residual(r_burst)) < 2e-11
    return float(r_bud), float(r_burst)


def run_asserts() -> dict[str, float]:
    assert abs(A_ROOT - 1.1) < 1e-13
    assert abs(B_ROOT) < 1e-13
    assert abs(V_INF - 11.0) < 2e-12
    assert abs(INFECTION_FACTOR * V_INF / CLEARANCE_RATE - R0_TARGET) < 1e-13
    assert abs(release_transform(0.0) - V_INF) < 5e-10

    mean_release_burst = burst_release_mean()
    mean_release_bud = 1.0 / D_I
    mean_generation_bud = mean_release_bud + 1.0 / CLEARANCE_RATE
    mean_generation_burst = mean_release_burst + 1.0 / CLEARANCE_RATE
    assert mean_generation_bud < mean_generation_burst

    r_bud, r_burst = growth_rates()
    assert r_bud > r_burst
    assert abs(r_bud - 0.250) < 0.002
    assert abs(r_burst - 0.180) < 0.002

    t_check = np.linspace(0.0, 55.0, 110_001)
    bud_density, burst_density = generation_densities(t_check)
    bud_mass = float(np.trapezoid(bud_density, t_check))
    burst_mass = float(np.trapezoid(burst_density, t_check))
    bud_mean_numeric = float(np.trapezoid(t_check * bud_density, t_check))
    burst_mean_numeric = float(np.trapezoid(t_check * burst_density, t_check))
    assert abs(bud_mass - 1.0) < 2e-7
    assert abs(burst_mass - 1.0) < 3e-7
    assert abs(bud_mean_numeric - mean_generation_bud) < 2e-6
    assert abs(burst_mean_numeric - mean_generation_burst) < 2e-6
    return {
        "mean_bud": mean_generation_bud,
        "mean_burst": mean_generation_burst,
        "r_bud": r_bud,
        "r_burst": r_burst,
        "bud_mass": bud_mass,
        "burst_mass": burst_mass,
    }


def make_figure(checked: dict[str, float]) -> None:
    t = np.linspace(0.0, 14.0, 4_000)
    bud_density, burst_density = generation_densities(t)
    _, _, burst_release = intracellular_functions(t)
    bud_release_density = D_I * np.exp(-D_I * t)
    burst_release_density = burst_release / V_INF

    fig, (ax, ax_rel) = plt.subplots(
        1, 2, figsize=(5.89, 2.65), gridspec_kw={"width_ratios": (1.5, 1.0)}
    )
    ax.fill_between(
        t,
        0.0,
        burst_density,
        color=BLUE,
        alpha=0.12,
        linewidth=0.0,
        zorder=1,
    )
    ax.fill_between(
        t,
        0.0,
        bud_density,
        color=ORANGE,
        alpha=0.09,
        linewidth=0.0,
        zorder=1,
    )
    ax.plot(
        t,
        burst_density,
        color=BLUE,
        linewidth=2.5,
        label="bursting",
        zorder=3,
    )
    ax.plot(
        t,
        bud_density,
        color=ORANGE,
        linewidth=2.4,
        linestyle="--",
        label="matched budding",
        zorder=3,
    )

    mean_bud = checked["mean_bud"]
    mean_burst = checked["mean_burst"]
    ax.axvline(mean_bud, color=ORANGE, linestyle="--", linewidth=1.15, alpha=0.9)
    ax.axvline(mean_burst, color=BLUE, linestyle=":", linewidth=1.35, alpha=0.95)
    ax.scatter(
        [mean_bud, mean_burst],
        [0.0, 0.0],
        marker="^",
        s=38,
        c=[ORANGE, BLUE],
        edgecolor="white",
        linewidth=0.6,
        clip_on=False,
        zorder=5,
    )
    ax.annotate(
        rf"bud mean $={mean_bud:.2f}$",
        xy=(mean_bud, 0.0),
        xytext=(mean_bud - 0.18, 0.115),
        ha="right",
        va="bottom",
        fontsize=8.5,
        color="#9a3e00",
        bbox=dict(boxstyle="round,pad=0.12", facecolor="white", edgecolor="none", alpha=0.85),
        arrowprops=dict(arrowstyle="-", color=ORANGE, linewidth=0.8),
    )
    ax.annotate(
        rf"burst mean $={mean_burst:.2f}$",
        xy=(mean_burst, 0.0),
        xytext=(mean_burst + 0.32, 0.062),
        ha="left",
        va="bottom",
        fontsize=8.5,
        color="#155987",
        bbox=dict(boxstyle="round,pad=0.12", facecolor="white", edgecolor="none", alpha=0.85),
        arrowprops=dict(arrowstyle="-", color=BLUE, linewidth=0.8),
    )
    ax.annotate(
        "",
        xy=(mean_burst, 0.011),
        xytext=(mean_bud, 0.011),
        arrowprops=dict(arrowstyle="<->", color=PURPLE, linewidth=1.0),
    )
    ax.text(
        0.5 * (mean_bud + mean_burst),
        0.020,
        "later generations",
        ha="center",
        va="bottom",
        fontsize=8.0,
        color=PURPLE,
    )

    ax.text(
        0.985,
        0.985,
        rf"$r_{{\rm bud}}={checked['r_bud']:.3f}"
        rf">r_{{\rm burst}}={checked['r_burst']:.3f}$",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9.2,
        color="#4f3973",
        bbox=dict(boxstyle="round,pad=0.22", facecolor="white", edgecolor="none", alpha=0.88),
    )
    inset = ax_rel
    inset.plot(
        t,
        burst_release_density,
        color=BLUE,
        linewidth=1.8,
    )
    inset.plot(
        t,
        bud_release_density,
        color=ORANGE,
        linestyle="--",
        linewidth=1.7,
    )
    inset.scatter([0.0], [D_I], s=22, color=ORANGE, edgecolor="white", linewidth=0.5, zorder=5)
    inset.annotate(
        "release available\nat age zero",
        xy=(0.0, D_I),
        xytext=(1.15, 0.50),
        arrowprops=dict(arrowstyle="->", color=ORANGE, linewidth=0.75),
        fontsize=8.0,
        ha="left",
        va="center",
        color="#9a3e00",
    )
    inset.set_xlim(0.0, 4.0)
    inset.set_ylim(0.0, 0.62)
    inset.set_xticks([0, 1, 2, 3, 4])
    inset.set_yticks([0.0, 0.2, 0.4, 0.6])
    inset.set_xlabel(r"cell age $\alpha$")
    inset.set_ylabel(r"release-age density")

    ax.set_xlim(0.0, 12.0)
    ax.set_ylim(0.0, max(bud_density.max(), burst_density.max()) * 1.17)
    ax.set_xlabel(r"infection generation interval $\tau$")
    ax.set_ylabel(r"generation-time density $w(\tau)$")
    ax.legend(loc="upper left")

    style_rc.panel_label(ax, "(a)")
    style_rc.panel_label(inset, "(b)")
    fig.tight_layout(pad=1.05, w_pad=1.6)
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)


def main() -> None:
    checked = run_asserts()
    make_figure(checked)
    print(
        "asserts: pass; "
        f"generation means bud={checked['mean_bud']:.9f}, "
        f"burst={checked['mean_burst']:.9f}; "
        f"growth rates bud={checked['r_bud']:.9f}, "
        f"burst={checked['r_burst']:.9f}; "
        f"density masses={checked['bud_mass']:.9f}/{checked['burst_mass']:.9f}"
    )
    print(f"wrote {PDF_PATH} and {PNG_PATH}")


if __name__ == "__main__":
    main()
