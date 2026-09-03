#!/usr/bin/env python3
"""Generate F4b.3: matched-R0 deterministic growth-rate trade-off."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/bdc_odes_mplconfig")

import numpy as np
from numpy.polynomial.legendre import leggauss

STYLE_DIR = Path(
    "/Users/adamaldridge/Desktop/Thesis content 🎓 "
    "/4 BDC additional and BMVR/Figures run/style"
)
sys.path.insert(0, str(STYLE_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_style"))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402


@dataclass(frozen=True)
class ParameterSet:
    lam: float
    mu: float
    delta: float
    display: str

    @property
    def derived(self) -> tuple[float, float, float, float, float]:
        eta = (self.lam + self.mu + self.delta) / (2.0 * self.lam)
        radical = np.sqrt(eta**2 - self.mu / self.lam)
        a = eta + radical
        b = eta - radical
        flooding_parameter = a * (1.0 - b)
        v_inf = flooding_parameter / (a - 1.0)
        theta = self.lam * (a - b)
        return a, b, flooding_parameter, v_inf, theta


PARAMETER_SETS = (
    ParameterSet(1.0, 0.0, 0.1, r"$(1,0,0.1)$"),
    ParameterSet(1.0, 0.5, 1.0 / 3.0, r"$(1,0.5,1/3)$"),
    ParameterSet(1.0, 0.9, 0.1, r"$(1,0.9,0.1)$"),
)

CLEARANCE_RATE = 1.0
R0 = 2.0
_QUADRATURE_NODES, _QUADRATURE_WEIGHTS = leggauss(600)
_QUADRATURE_X = 0.5 * (_QUADRATURE_NODES + 1.0)
_QUADRATURE_WEIGHTS = 0.5 * _QUADRATURE_WEIGHTS


def release_transform(
    growth_rate: float,
    parameters: ParameterSet,
) -> float:
    """Evaluate delta times the Laplace transform of K by quadrature.

    The substitution x=exp(-theta*t) maps the semi-infinite time domain
    to [0,1] and keeps the closed forms numerically stable at late times.
    """
    a, b, _, _, theta = parameters.derived
    A, B = a - 1.0, 1.0 - b
    x = _QUADRATURE_X
    fixation_i = (a * B * x + b * A) / (B * x + A)
    first_moment_j = (a - b) ** 2 * x / (B * x + A) ** 2
    first_moment_k = (
        1.0 + 2.0 * parameters.lam / parameters.delta * (1.0 - fixation_i)
    ) * first_moment_j
    integrand = first_moment_k * x ** (growth_rate / theta - 1.0)
    return float(parameters.delta / theta * np.sum(_QUADRATURE_WEIGHTS * integrand))


def growth_rates(parameters: ParameterSet) -> tuple[float, float, float, float]:
    """Return d_I, gamma*T, and the budding and bursting growth rates."""
    a, _, _, v_inf, _ = parameters.derived
    productive_lifetime = np.log(a / (a - 1.0)) / parameters.lam
    d_i = 1.0 / productive_lifetime
    release_rate = v_inf * d_i
    gamma_t = R0 * CLEARANCE_RATE / v_inf

    discriminant = (d_i - CLEARANCE_RATE) ** 2 + 4.0 * gamma_t * release_rate
    r_bud = 0.5 * (-(d_i + CLEARANCE_RATE) + np.sqrt(discriminant))

    def characteristic(r: float) -> float:
        return r + CLEARANCE_RATE - gamma_t * release_transform(r, parameters)

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
    r_burst = 0.5 * (lower + upper)
    assert abs(characteristic(r_burst)) < 1e-10
    return d_i, gamma_t, float(r_bud), float(r_burst)


def calculate_all() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    d_values, gamma_t_values, bud_values, burst_values = [], [], [], []
    for parameters in PARAMETER_SETS:
        d_i, gamma_t, r_bud, r_burst = growth_rates(parameters)
        d_values.append(d_i)
        gamma_t_values.append(gamma_t)
        bud_values.append(r_bud)
        burst_values.append(r_burst)
    return tuple(
        np.asarray(values, dtype=float)
        for values in (d_values, gamma_t_values, bud_values, burst_values)
    )


def run_asserts(
    d_values: np.ndarray,
    gamma_t_values: np.ndarray,
    bud_values: np.ndarray,
    burst_values: np.ndarray,
) -> None:
    expected_d = np.array([0.417, 0.910, 0.701])
    expected_bud = np.array([0.250, 0.395, 0.343])
    expected_burst = np.array([0.180, 0.294, 0.198])
    assert np.max(np.abs(d_values - expected_d)) < 1e-3
    assert np.max(np.abs(bud_values - expected_bud)) < 0.01
    assert np.max(np.abs(burst_values - expected_burst)) < 0.01
    assert np.all(bud_values > burst_values)

    for parameters, gamma_t in zip(PARAMETER_SETS, gamma_t_values):
        _, _, _, v_inf, _ = parameters.derived
        assert abs(gamma_t * v_inf / CLEARANCE_RATE - R0) < 1e-12
        assert abs(release_transform(0.0, parameters) - v_inf) < 1e-9


def make_figure(bud_values: np.ndarray, burst_values: np.ndarray) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(4.01, 2.3))
    positions = np.arange(len(PARAMETER_SETS), dtype=float)
    width = 0.32

    bud_bars = ax.bar(
        positions - width / 2,
        bud_values,
        width,
        color=style_rc.VERMILLION,
        edgecolor="black",
        linewidth=0.55,
        label="budding",
    )
    burst_bars = ax.bar(
        positions + width / 2,
        burst_values,
        width,
        color=style_rc.BLUE,
        edgecolor="black",
        linewidth=0.55,
        label="bursting",
    )

    ax.bar_label(bud_bars, fmt="%.3f", padding=3, fontsize=8.5)
    ax.bar_label(burst_bars, fmt="%.3f", padding=3, fontsize=8.5)
    for position, parameters, bud_value, burst_value in zip(
        positions, PARAMETER_SETS, bud_values, burst_values
    ):
        flooding_parameter = parameters.derived[2]
        ax.text(
            position,
            max(bud_value, burst_value) + 0.055,
            rf"$L={flooding_parameter:.2f}$",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    ax.set_xticks(positions, [parameters.display for parameters in PARAMETER_SETS])
    ax.set_xlabel(r"parameter set $(\lambda,\mu,\delta)$")
    ax.set_ylabel(r"growth rate $r$")
    ax.set_ylim(0.0, 0.49)
    ax.legend(loc="upper left")
    ax.xaxis.grid(False)
    fig.tight_layout()
    return fig


def main() -> None:
    d_values, gamma_t_values, bud_values, burst_values = calculate_all()
    run_asserts(d_values, gamma_t_values, bud_values, burst_values)
    workdir = Path(__file__).resolve().parent
    figures_dir = workdir.parents[1]
    production_pdf = figures_dir / "F4b_3_growth_tradeoff.pdf"
    preview_png = workdir / "preview.png"
    fig = make_figure(bud_values, burst_values)
    style_rc.save_figure(fig, production_pdf, preview_png)
    plt.close(fig)
    print("asserts: pass")
    for parameters, d_i, r_bud, r_burst in zip(
        PARAMETER_SETS, d_values, bud_values, burst_values
    ):
        print(
            f"{parameters.display}: d_I={d_i:.6f}, "
            f"r_bud={r_bud:.6f}, r_burst={r_burst:.6f}"
        )
    print(f"wrote {production_pdf} and {preview_png}")


if __name__ == "__main__":
    main()
