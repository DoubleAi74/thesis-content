#!/usr/bin/env python3
"""Generate N4b.1: age-dependent and constant-release cohort responses."""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/bdc_odes_n4b1_mplconfig")

import numpy as np

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
DELTA = 0.1
CLEARANCE = 1.0


def derived_parameters() -> tuple[float, float, float, float, float]:
    eta = (LAMBDA + MU + DELTA) / (2.0 * LAMBDA)
    radical = np.sqrt(eta**2 - MU / LAMBDA)
    a = eta + radical
    b = eta - radical
    theta = LAMBDA * (a - b)
    v_inf = a * (1.0 - b) / (a - 1.0)
    mean_lifetime = np.log(a / (a - 1.0)) / LAMBDA
    return a, b, theta, v_inf, mean_lifetime


def release_flux(age: np.ndarray) -> np.ndarray:
    """Return g(a)=delta K(a), evaluated in a late-age-stable form."""
    a, b, theta, _, _ = derived_parameters()
    A, B = a - 1.0, 1.0 - b
    x = np.exp(-theta * np.asarray(age, dtype=float))
    fixation_i = (a * B * x + b * A) / (B * x + A)
    first_moment_j = (a - b) ** 2 * x / (B * x + A) ** 2
    second_moment_k = (
        1.0 + 2.0 * LAMBDA / DELTA * (1.0 - fixation_i)
    ) * first_moment_j
    return DELTA * second_moment_k


def constant_source(age: np.ndarray) -> np.ndarray:
    _, _, _, v_inf, mean_lifetime = derived_parameters()
    d = 1.0 / mean_lifetime
    p = v_inf * d
    return p * np.exp(-d * np.asarray(age, dtype=float))


def cumulative_trapezoid(values: np.ndarray, grid: np.ndarray) -> np.ndarray:
    result = np.zeros_like(values, dtype=float)
    result[1:] = np.cumsum(
        0.5 * (values[:-1] + values[1:]) * np.diff(grid)
    )
    return result


def cleared_response(source: np.ndarray, time: np.ndarray) -> np.ndarray:
    weighted_source = np.exp(CLEARANCE * time) * source
    return np.exp(-CLEARANCE * time) * cumulative_trapezoid(
        weighted_source, time
    )


def calculate_plot_data() -> tuple[np.ndarray, ...]:
    age = np.linspace(0.0, 12.0, 4801)
    kernel = release_flux(age)
    comparator = constant_source(age)
    kernel_response = cleared_response(kernel, age)
    comparator_response = cleared_response(comparator, age)
    return age, kernel, comparator, kernel_response, comparator_response


def run_asserts(plot_data: tuple[np.ndarray, ...]) -> None:
    _, _, _, v_inf, mean_lifetime = derived_parameters()
    d = 1.0 / mean_lifetime
    p = v_inf * d

    integration_age = np.linspace(0.0, 70.0, 70001)
    integrated_kernel = float(
        np.trapezoid(release_flux(integration_age), integration_age)
    )
    integrated_comparator = p / d
    assert abs(integrated_kernel - v_inf) < 2e-5
    assert abs(integrated_comparator - v_inf) < 1e-12

    age, kernel, comparator, kernel_response, comparator_response = plot_data
    early = (age >= 0.05) & (age <= 1.5)
    assert np.all(comparator_response[early] > kernel_response[early])
    assert comparator[0] > 40.0 * kernel[0]
    assert age[np.argmax(kernel)] > age[np.argmax(comparator)] + 1.0
    assert abs(kernel_response[0]) < 1e-14
    assert abs(comparator_response[0]) < 1e-14


def make_figure(plot_data: tuple[np.ndarray, ...]) -> plt.Figure:
    age, kernel, comparator, kernel_response, comparator_response = plot_data

    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.4))
    ax_schedule, ax_response = axes
    for axis in axes:
        axis.tick_params(labelsize=10)

    ax_schedule.plot(
        age,
        kernel,
        color=style_rc.NAVY,
        linewidth=2.3,
        label=r"age-dependent $g(a)$",
    )
    ax_schedule.plot(
        age,
        comparator,
        color="tab:orange",
        linewidth=2.1,
        linestyle="--",
        label=r"constant $p\,\mathrm{e}^{-da}$",
    )
    kernel_peak_index = int(np.argmax(kernel))
    ax_schedule.scatter(
        age[kernel_peak_index],
        kernel[kernel_peak_index],
        s=35,
        facecolor="white",
        edgecolor=style_rc.NAVY,
        linewidth=1.3,
        zorder=4,
    )
    ax_schedule.set(
        xlim=(0.0, 12.0),
        ylim=(0.0, 5.0),
        xlabel=r"producer age $a$",
        ylabel=r"expected release flux",
        title="(a) Matched yield, different release timing",
    )
    ax_schedule.legend(loc="upper right", fontsize=9.5)

    ax_response.axvspan(0.0, 1.5, color="tab:gray", alpha=0.10, zorder=0)
    ax_response.plot(
        age,
        kernel_response,
        color=style_rc.NAVY,
        linewidth=2.3,
        label="kernel response",
    )
    ax_response.plot(
        age,
        comparator_response,
        color="tab:orange",
        linewidth=2.1,
        linestyle="--",
        label="constant response",
    )
    response_peak_index = int(np.argmax(kernel_response))
    ax_response.scatter(
        age[response_peak_index],
        kernel_response[response_peak_index],
        s=35,
        facecolor="white",
        edgecolor=style_rc.NAVY,
        linewidth=1.3,
        zorder=4,
    )
    lag_time = 1.0
    lag_index = int(np.argmin(np.abs(age - lag_time)))
    ax_response.annotate(
        "early lag",
        xy=(lag_time, kernel_response[lag_index]),
        xytext=(2.05, 2.15),
        arrowprops=dict(
            arrowstyle="->", color="#555555", linewidth=1.0
        ),
        ha="center",
        va="bottom",
        fontsize=9.5,
        color="#444444",
    )
    ax_response.set(
        xlim=(0.0, 12.0),
        ylim=(0.0, 3.35),
        xlabel=r"time $t$",
        ylabel="free count per initial producer unit",
        title="(b) Linear clearance preserves the early lag",
    )
    ax_response.legend(loc="upper right", fontsize=9.5)

    fig.tight_layout(w_pad=1.8)
    return fig


def main() -> None:
    plot_data = calculate_plot_data()
    run_asserts(plot_data)
    workdir = Path(__file__).resolve().parent
    figures_dir = workdir.parents[1]
    production_pdf = figures_dir / "N4b_1_constant_release_fails.pdf"
    preview_png = workdir / "preview.png"
    fig = make_figure(plot_data)
    style_rc.save_figure(fig, production_pdf, preview_png, dpi=240)
    plt.close(fig)

    _, _, _, v_inf, mean_lifetime = derived_parameters()
    print(
        "asserts: pass; "
        f"V_inf={v_inf:.6f}, E[T]={mean_lifetime:.6f}, c={CLEARANCE:g}"
    )
    print(f"wrote {production_pdf} and {preview_png}")


if __name__ == "__main__":
    main()
