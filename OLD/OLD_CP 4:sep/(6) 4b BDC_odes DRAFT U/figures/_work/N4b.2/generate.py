#!/usr/bin/env python3
"""Generate N4b.2: non-identifiability from R0 and growth-rate level sets."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/bdc_odes_n4b2_mplconfig")

import numpy as np
from numpy.polynomial.legendre import leggauss

sys.path.insert(
    0,
    "/Users/adamaldridge/Desktop/Thesis content 🎓 /4 BDC additional and BMVR/Figures run/style",
)
import style_rc  # noqa: E402

style_rc.apply()

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.ticker import FixedLocator, FuncFormatter, NullFormatter  # noqa: E402


WORKDIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORKDIR.parents[2]
PDF_PATH = CHAPTER_DIR / "figures" / "N4b_2_identifiability_levels.pdf"
PNG_PATH = WORKDIR / "preview.png"

CLEARANCE_RATE = 1.0
R0_TARGET = 2.0
PURPLE = "#6b4c9a"
BLUE = "#1f77b4"
RED = "#8b1e1e"

_NODES, _WEIGHTS = leggauss(280)
_X = 0.5 * (_NODES + 1.0)
_WEIGHTS = 0.5 * _WEIGHTS


@dataclass(frozen=True)
class Triple:
    lam: float
    mu: float
    delta: float


# The L=1 flooding row is deliberately used as the reference: unlike the
# no-death row, it lies in the interior of the fixed-lambda slice.
REFERENCE = Triple(1.0, 0.5, 1.0 / 3.0)


def roots(
    lam: float | np.ndarray,
    mu: float | np.ndarray,
    delta: float | np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Return the ordered roots a > 1 > b of the BDC quadratic."""
    lam_arr = np.asarray(lam, dtype=float)
    mu_arr = np.asarray(mu, dtype=float)
    delta_arr = np.asarray(delta, dtype=float)
    eta = (lam_arr + mu_arr + delta_arr) / (2.0 * lam_arr)
    discriminant = eta**2 - mu_arr / lam_arr
    assert np.all(discriminant >= 0.0)
    radical = np.sqrt(discriminant)
    return eta + radical, eta - radical


def mean_yield(
    lam: float | np.ndarray,
    mu: float | np.ndarray,
    delta: float | np.ndarray,
) -> np.ndarray:
    """Return V_infinity from the closed form in the chapter."""
    a, b = roots(lam, mu, delta)
    return a * (1.0 - b) / (a - 1.0)


V_REFERENCE = float(mean_yield(REFERENCE.lam, REFERENCE.mu, REFERENCE.delta))
INFECTION_FACTOR = R0_TARGET * CLEARANCE_RATE / V_REFERENCE


def release_transform(
    growth_rate: float,
    lam: float,
    mu: float | np.ndarray,
    delta: float | np.ndarray,
) -> np.ndarray:
    """Evaluate delta times the Laplace transform of K.

    The substitution x=exp(-theta*t) maps t in [0,infinity) to x in [0,1]
    and remains stable for the weak-catastrophe edge of the plotted slice.
    """
    mu_arr = np.asarray(mu, dtype=float)
    delta_arr = np.asarray(delta, dtype=float)
    a, b = roots(lam, mu_arr, delta_arr)
    cap_a = a - 1.0
    cap_b = 1.0 - b
    theta = lam * (a - b)

    x = _X.reshape((-1,) + (1,) * mu_arr.ndim)
    weights = _WEIGHTS.reshape((-1,) + (1,) * mu_arr.ndim)
    a_b = a - b
    fixation_i = (a * cap_b * x + b * cap_a) / (cap_b * x + cap_a)
    first_moment_j = a_b**2 * x / (cap_b * x + cap_a) ** 2
    second_moment_k = (
        1.0 + 2.0 * lam / delta_arr * (1.0 - fixation_i)
    ) * first_moment_j
    integrand = second_moment_k * x ** (growth_rate / theta - 1.0)
    return delta_arr / theta * np.sum(weights * integrand, axis=0)


def characteristic_residual(growth_rate: float, triple: Triple) -> float:
    transform = float(
        release_transform(growth_rate, triple.lam, triple.mu, triple.delta)
    )
    return growth_rate + CLEARANCE_RATE - INFECTION_FACTOR * transform


def growth_rate(triple: Triple) -> float:
    """Solve the renewal characteristic equation by safeguarded bisection."""
    lower, upper = 0.0, 1.0
    assert characteristic_residual(lower, triple) < 0.0
    while characteristic_residual(upper, triple) <= 0.0:
        upper *= 2.0
        assert upper < 64.0
    for _ in range(72):
        midpoint = 0.5 * (lower + upper)
        if characteristic_residual(midpoint, triple) > 0.0:
            upper = midpoint
        else:
            lower = midpoint
    result = 0.5 * (lower + upper)
    assert abs(characteristic_residual(result, triple)) < 2e-11
    return result


R_REFERENCE = growth_rate(REFERENCE)


def delta_ratio_for_yield(mu_ratio: float, target: float = V_REFERENCE) -> float:
    """Solve V_infinity(1, mu/lambda, delta/lambda)=target."""
    lower, upper = 1e-7, 4.0
    assert float(mean_yield(1.0, mu_ratio, lower)) > target
    assert float(mean_yield(1.0, mu_ratio, upper)) < target
    for _ in range(80):
        midpoint = 0.5 * (lower + upper)
        if float(mean_yield(1.0, mu_ratio, midpoint)) > target:
            lower = midpoint
        else:
            upper = midpoint
    return 0.5 * (lower + upper)


def simultaneous_family(mu_ratios: np.ndarray) -> list[Triple]:
    """Trace triples that share both the reference R0 and reference r."""
    required_transform = (R_REFERENCE + CLEARANCE_RATE) / INFECTION_FACTOR
    family: list[Triple] = []
    for mu_ratio in mu_ratios:
        delta_ratio = delta_ratio_for_yield(float(mu_ratio))

        lower, upper = 1e-8, 4.0
        transform_lower = float(
            release_transform(lower, 1.0, float(mu_ratio), delta_ratio)
        )
        transform_upper = float(
            release_transform(upper, 1.0, float(mu_ratio), delta_ratio)
        )
        assert transform_lower > required_transform > transform_upper
        for _ in range(72):
            midpoint = 0.5 * (lower + upper)
            value = float(
                release_transform(midpoint, 1.0, float(mu_ratio), delta_ratio)
            )
            if value > required_transform:
                lower = midpoint
            else:
                upper = midpoint
        scaled_growth = 0.5 * (lower + upper)
        lam = R_REFERENCE / scaled_growth
        family.append(Triple(lam, float(mu_ratio) * lam, delta_ratio * lam))
    return family


def run_asserts(family: list[Triple]) -> dict[str, float]:
    """Check both level sets and the simultaneous non-identifiable family."""
    r0_reference = INFECTION_FACTOR * V_REFERENCE / CLEARANCE_RATE
    assert abs(r0_reference - R0_TARGET) < 1e-13
    assert abs(characteristic_residual(R_REFERENCE, REFERENCE)) < 2e-11

    fixed_slice_points = [
        Triple(1.0, mu, delta_ratio_for_yield(mu)) for mu in (0.15, 0.5, 0.78)
    ]
    for point in fixed_slice_points:
        r0_value = (
            INFECTION_FACTOR
            * float(mean_yield(point.lam, point.mu, point.delta))
            / CLEARANCE_RATE
        )
        assert abs(r0_value - R0_TARGET) < 2e-10
    separation = np.hypot(
        fixed_slice_points[-1].mu - fixed_slice_points[0].mu,
        fixed_slice_points[-1].delta - fixed_slice_points[0].delta,
    )
    assert separation > 0.5

    family_r0_errors = []
    family_r_errors = []
    for point in family:
        family_r0_errors.append(
            abs(
                INFECTION_FACTOR
                * float(mean_yield(point.lam, point.mu, point.delta))
                / CLEARANCE_RATE
                - R0_TARGET
            )
        )
        family_r_errors.append(abs(characteristic_residual(R_REFERENCE, point)))
    assert max(family_r0_errors) < 2e-9
    assert max(family_r_errors) < 5e-10
    assert np.hypot(
        family[-1].mu - family[0].mu,
        family[-1].delta - family[0].delta,
    ) > 1.5
    return {
        "r_reference": R_REFERENCE,
        "fixed_slice_separation": float(separation),
        "max_family_r0_error": float(max(family_r0_errors)),
        "max_family_r_error": float(max(family_r_errors)),
    }


def fixed_slice_fields(
    mu_values: np.ndarray, delta_values: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Evaluate R0 and the r=r_reference contour residual on a mesh."""
    mu_grid, delta_grid = np.meshgrid(mu_values, delta_values)
    r0_grid = INFECTION_FACTOR * mean_yield(1.0, mu_grid, delta_grid)
    residual_grid = np.empty_like(r0_grid)
    for row, delta in enumerate(delta_values):
        transforms = release_transform(
            R_REFERENCE,
            1.0,
            mu_values,
            np.full_like(mu_values, delta),
        )
        residual_grid[row, :] = (
            R_REFERENCE + CLEARANCE_RATE - INFECTION_FACTOR * transforms
        )
    assert np.all(np.isfinite(r0_grid))
    assert np.all(np.isfinite(residual_grid))
    return mu_grid, delta_grid, r0_grid, residual_grid


def annotate_family_point(
    ax: plt.Axes,
    point: Triple,
    label: str,
    offset: tuple[float, float],
) -> None:
    ax.scatter(
        [point.mu],
        [point.delta],
        s=28,
        facecolor="white",
        edgecolor=PURPLE,
        linewidth=1.2,
        zorder=7,
    )
    ax.annotate(
        label + "\n" + rf"$({point.lam:.2f},{point.mu:.2f},{point.delta:.2f})$",
        xy=(point.mu, point.delta),
        xytext=offset,
        textcoords="offset points",
        arrowprops=dict(arrowstyle="-", color=PURPLE, linewidth=0.8),
        fontsize=7.8,
        ha="left" if offset[0] >= 0 else "right",
        va="bottom" if offset[1] >= 0 else "top",
        color="#4f3973",
    )


def make_figure(family: list[Triple]) -> None:
    mu_values = np.linspace(0.0, 0.9, 181)
    delta_values = np.geomspace(0.018, 1.35, 181)
    mu_grid, delta_grid, r0_grid, residual_grid = fixed_slice_fields(
        mu_values, delta_values
    )

    fig, (ax_slice, ax_family) = plt.subplots(1, 2, figsize=(10.8, 4.55))

    r0_contour = ax_slice.contour(
        mu_grid,
        delta_grid,
        r0_grid,
        levels=[R0_TARGET],
        colors=[BLUE],
        linewidths=2.4,
    )
    r_contour = ax_slice.contour(
        mu_grid,
        delta_grid,
        residual_grid,
        levels=[0.0],
        colors=[PURPLE],
        linewidths=2.2,
        linestyles="--",
    )
    assert len(r0_contour.allsegs[0]) >= 1
    assert len(r_contour.allsegs[0]) >= 1

    slice_points = [
        Triple(1.0, mu, delta_ratio_for_yield(mu)) for mu in (0.15, 0.5, 0.78)
    ]
    for label, point, offset in zip(
        ("A", "reference", "C"),
        slice_points,
        ((7, 7), (8, -8), (-7, 8)),
    ):
        if label == "reference":
            ax_slice.scatter(
                [point.mu],
                [point.delta],
                marker="*",
                s=145,
                facecolor=RED,
                edgecolor="white",
                linewidth=0.9,
                zorder=8,
            )
        else:
            ax_slice.scatter(
                [point.mu],
                [point.delta],
                s=40,
                facecolor="white",
                edgecolor=BLUE,
                linewidth=1.4,
                zorder=8,
            )
        ax_slice.annotate(
            label,
            xy=(point.mu, point.delta),
            xytext=offset,
            textcoords="offset points",
            fontsize=8.2,
            ha="left" if offset[0] > 0 else "right",
            va="bottom" if offset[1] > 0 else "top",
            color=RED if label == "reference" else "#155987",
        )

    ax_slice.text(
        0.04,
        0.055,
        r"A and C share $R_0=2$ with the reference" "\n" r"but have different growth rates",
        transform=ax_slice.transAxes,
        fontsize=8.3,
        color="#444444",
        va="bottom",
    )
    ax_slice.set_yscale("log")
    ax_slice.set_xlim(0.0, 0.9)
    ax_slice.set_ylim(delta_values[0], delta_values[-1])
    ax_slice.set_xlabel(r"death rate $\mu$ at fixed $\lambda=1$")
    ax_slice.set_ylabel(r"catastrophe rate $\delta$")
    ax_slice.set_title(
        "(a) One population observable leaves a level curve",
        loc="left",
        fontweight="bold",
        pad=8,
    )
    ax_slice.yaxis.set_major_locator(
        FixedLocator([0.02, 0.05, 0.1, 0.2, 0.5, 1.0])
    )
    ax_slice.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:g}"))
    ax_slice.yaxis.set_minor_formatter(NullFormatter())
    ax_slice.legend(
        handles=[
            Line2D([0], [0], color=BLUE, linewidth=2.4, label=r"$R_0=2$"),
            Line2D(
                [0],
                [0],
                color=PURPLE,
                linewidth=2.2,
                linestyle="--",
                label=rf"$r=r_\star={R_REFERENCE:.3f}$",
            ),
        ],
        loc="upper right",
    )

    family_mu = np.array([point.mu for point in family])
    family_delta = np.array([point.delta for point in family])
    ax_family.plot(
        family_mu,
        family_delta,
        color=PURPLE,
        linewidth=2.5,
        zorder=3,
    )
    ax_family.scatter(
        family_mu[::10],
        family_delta[::10],
        s=18,
        facecolor="white",
        edgecolor=PURPLE,
        linewidth=0.9,
        zorder=4,
    )

    reference_index = int(
        np.argmin(
            [
                abs(point.lam - REFERENCE.lam)
                + abs(point.mu - REFERENCE.mu)
                + abs(point.delta - REFERENCE.delta)
                for point in family
            ]
        )
    )
    reference_family_point = family[reference_index]
    assert (
        abs(reference_family_point.lam - REFERENCE.lam)
        + abs(reference_family_point.mu - REFERENCE.mu)
        + abs(reference_family_point.delta - REFERENCE.delta)
        < 1e-8
    )
    ax_family.scatter(
        [REFERENCE.mu],
        [REFERENCE.delta],
        marker="*",
        s=155,
        facecolor=RED,
        edgecolor="white",
        linewidth=0.9,
        zorder=8,
        label="reference triple",
    )

    for index, label, offset in (
        (12, "D", (10, 10)),
        (reference_index, "reference", (12, -13)),
        (-8, "F", (10, -15)),
    ):
        point = family[index]
        if label == "reference":
            ax_family.annotate(
                "reference\n" + r"$(1.00,0.50,0.33)$",
                xy=(point.mu, point.delta),
                xytext=offset,
                textcoords="offset points",
                arrowprops=dict(arrowstyle="-", color=RED, linewidth=0.8),
                fontsize=7.8,
                color="#681616",
                ha="left",
                va="top",
            )
        else:
            annotate_family_point(ax_family, point, label, offset)

    ax_family.annotate(
        r"every point: $R_0=2$ and $r=0.294$" "\n" r"$\lambda$ varies along the curve",
        xy=(family_mu[len(family) // 3], family_delta[len(family) // 3]),
        xytext=(0.97, 0.95),
        textcoords="axes fraction",
        arrowprops=dict(arrowstyle="->", color=PURPLE, linewidth=0.9),
        ha="right",
        va="top",
        fontsize=8.6,
        color="#4f3973",
    )
    ax_family.set_xlim(-0.05, family_mu.max() * 1.08)
    ax_family.set_ylim(max(0.0, family_delta.min() - 0.03), family_delta.max() + 0.055)
    ax_family.set_xlabel(r"death rate $\mu$")
    ax_family.set_ylabel(r"catastrophe rate $\delta$")
    ax_family.set_title(
        r"(b) Even $R_0$ and $r$ leave a one-parameter family",
        loc="left",
        fontweight="bold",
        pad=8,
    )

    fig.tight_layout(w_pad=2.2, pad=1.2)
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)


def main() -> None:
    mu_ratios = np.unique(np.r_[np.linspace(0.0, 0.82, 83), 0.5])
    family = simultaneous_family(mu_ratios)
    checked = run_asserts(family)
    make_figure(family)
    print(
        "asserts: pass; "
        f"reference r={checked['r_reference']:.12f}; "
        f"R0-contour separation={checked['fixed_slice_separation']:.6f}; "
        f"family max errors R0={checked['max_family_r0_error']:.3e}, "
        f"r={checked['max_family_r_error']:.3e}"
    )
    print(f"wrote {PDF_PATH} and {PNG_PATH}")


if __name__ == "__main__":
    main()
