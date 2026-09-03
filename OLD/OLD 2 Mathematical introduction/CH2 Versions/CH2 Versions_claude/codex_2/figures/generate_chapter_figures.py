"""Generate the vector figures used by the mathematical-background chapter.

All Galton--Watson curves are deterministic evaluations of exact recurrences.
The Kolmogorov constant is evaluated with a rigorous bound on the omitted
log-product tail; no Monte Carlo simulation or fitted surrogate is used.
"""

from __future__ import annotations

import math
import os
from pathlib import Path
import tempfile

os.environ.setdefault(
    "MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "matplotlib-thesis-chapter")
)

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).resolve().parent

mpl.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["STIXGeneral", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "legend.fontsize": 9,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 1.0,
        "grid.color": "#D9DDE3",
        "grid.linewidth": 0.6,
        "lines.linewidth": 1.8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "savefig.bbox": "tight",
    }
)

BLUE = "#0072B2"
ORANGE = "#D55E00"
GREEN = "#009E73"
PURPLE = "#CC79A7"
SKY = "#56B4E9"
BLACK = "#222222"
COLOURS = [BLUE, ORANGE, GREEN, PURPLE, SKY, BLACK]


def survival_series(p: float, n_max: int) -> np.ndarray:
    """Return S_0,...,S_n for binary 0-or-2 offspring."""
    values = np.empty(n_max + 1, dtype=float)
    values[0] = 1.0
    for n in range(n_max):
        values[n + 1] = 2.0 * p * values[n] - p * values[n] ** 2
    return values


def conditional_mean_series(p: float, n_max: int) -> np.ndarray:
    """Return m^n/S_n without forming two small floating-point numbers."""
    survival = survival_series(p, n_max)
    means = np.empty(n_max + 1, dtype=float)
    means[0] = 1.0
    for n in range(n_max):
        means[n + 1] = means[n] / (1.0 - survival[n] / 2.0)
    return means


def kolmogorov_constant(
    p: float, *, log_tail_tolerance: float = 5e-12, max_iter: int = 5_000_000
) -> float:
    """Evaluate A(p) from its exact product with certified tail control.

    If A_N = prod_{k=0}^N (1-S_k/2), then

      0 <= log(A_N/A)
         <= S_{N+1}/(2(1-S_{N+1}/2)(1-2p)).

    The endpoint p=0 is the continuous extension, not the defining ratio.
    """
    if p == 0.0:
        return 0.5
    if not 0.0 < p < 0.5:
        raise ValueError("p must lie in [0, 1/2)")

    m = 2.0 * p
    survival = 1.0
    log_product = 0.0
    for _ in range(max_iter):
        log_product += math.log1p(-survival / 2.0)
        survival = m * survival * (1.0 - survival / 2.0)
        tail_bound = survival / (
            2.0 * (1.0 - survival / 2.0) * (1.0 - m)
        )
        if tail_bound <= log_tail_tolerance:
            return math.exp(log_product)
    raise RuntimeError(f"Kolmogorov product did not converge for p={p}")


def save(fig: plt.Figure, filename: str) -> None:
    fig.savefig(
        OUT / filename,
        metadata={
            "Title": filename.removesuffix(".pdf").replace("_", " "),
            "Author": "Adam Aldridge",
            "Creator": "generate_chapter_figures.py",
        },
    )
    plt.close(fig)


def make_survival_regimes() -> None:
    fig, ax = plt.subplots(figsize=(6.9, 3.8), constrained_layout=True)
    n = np.arange(0, 81)
    for p, colour, label in [
        (0.45, BLUE, r"$p=0.45$ (subcritical)"),
        (0.50, BLACK, r"$p=0.50$ (critical)"),
        (0.55, ORANGE, r"$p=0.55$ (supercritical)"),
    ]:
        ax.semilogy(n, survival_series(p, int(n[-1])), color=colour, label=label)
    limit = (2.0 * 0.55 - 1.0) / 0.55
    ax.axhline(
        limit,
        color=ORANGE,
        linestyle="--",
        linewidth=1.1,
        label=r"$S_\infty=(2p-1)/p$ for $p=0.55$",
    )
    ax.set(xlabel="Generation $n$", ylabel=r"Survival probability $S_n$")
    ax.set_xlim(0, 80)
    ax.set_ylim(1e-5, 1.05)
    ax.legend(frameon=False, ncol=2, loc="lower left")
    save(fig, "gw_survival_regimes.pdf")


def make_conditional_means() -> None:
    fig, ax = plt.subplots(figsize=(6.9, 3.9), constrained_layout=True)
    n = np.arange(0, 301)
    for p, colour in zip([0.30, 0.40, 0.45, 0.48, 0.49], COLOURS):
        ax.plot(
            n,
            conditional_mean_series(p, int(n[-1])),
            color=colour,
            label=fr"$p={p:.2f}$",
        )
    ax.set(
        xlabel="Generation $n$",
        ylabel=r"$\mathbb{E}[Z_n\mid Z_n>0]$",
    )
    ax.set_xlim(0, 300)
    ax.set_ylim(bottom=0)
    ax.legend(frameon=False, ncol=3, loc="upper left")
    save(fig, "gw_conditional_mean.pdf")


def make_kolmogorov_constant() -> None:
    coarse = np.linspace(0.0, 0.49, 150)
    near = np.linspace(0.4905, 0.499, 36)
    p_values = np.unique(np.concatenate([coarse, near]))
    a_values = np.array([kolmogorov_constant(float(p)) for p in p_values])

    fig, (left, right) = plt.subplots(
        1, 2, figsize=(7.25, 3.35), constrained_layout=True
    )
    left.plot(p_values, a_values, color=BLUE)
    left.scatter([0.0], [0.5], s=20, facecolor="white", edgecolor=BLUE, zorder=3)
    left.set(
        xlabel="Division probability $p$",
        ylabel=r"Kolmogorov constant $A(p)$",
        xlim=(0, 0.5),
        ylim=(0, 0.52),
    )

    right.semilogy(p_values, 1.0 / a_values, color=ORANGE)
    right.set(
        xlabel="Division probability $p$",
        ylabel=r"Yaglom mean $1/A(p)$",
        xlim=(0, 0.5),
    )
    save(fig, "kolmogorov_constant.pdf")


def cohort_survival(single_survival: np.ndarray, k: int) -> np.ndarray:
    """Stable evaluation of 1-(1-S)^k."""
    result = np.empty_like(single_survival)
    mask = single_survival < 1.0
    result[~mask] = 1.0
    result[mask] = -np.expm1(k * np.log1p(-single_survival[mask]))
    return result


def make_cohort_survival() -> None:
    fig, axes = plt.subplots(
        1, 2, figsize=(7.35, 3.45), sharex=True, sharey=True, constrained_layout=True
    )
    n = np.arange(0, 501)
    for ax, p, title in [
        (axes[0], 0.495, r"Subcritical: $p=0.495$"),
        (axes[1], 0.505, r"Supercritical: $p=0.505$"),
    ]:
        single = survival_series(p, int(n[-1]))
        for k, colour in zip([1, 10, 100, 1000], [BLUE, ORANGE, GREEN, PURPLE]):
            ax.plot(n, cohort_survival(single, k), color=colour, label=fr"$k={k}$")
        ax.set_title(title)
        ax.set_xlabel("Generation $n$")
        ax.set_xlim(0, 500)
        ax.set_ylim(0, 1.02)
    axes[0].set_ylabel(r"Cohort survival $S_n^{(k)}$")
    axes[1].legend(frameon=False, loc="center right")
    save(fig, "gw_cohort_survival.pdf")


def make_absorption_probabilities() -> None:
    alpha = 1.0
    mu = 0.4
    t = np.linspace(0.0, 7.0, 500)
    p_external = np.exp(-alpha * t)

    fig, axes = plt.subplots(
        1, 2, figsize=(7.35, 3.35), sharex=True, sharey=True, constrained_layout=True
    )

    axes[0].plot(t, p_external, color=BLUE, label="extracellular")
    axes[0].plot(t, 1.0 - p_external, color=ORANGE, label="intracellular")
    axes[0].set_title(r"Absorption only: $\alpha=1$")

    p_internal = alpha / (mu - alpha) * (
        np.exp(-alpha * t) - np.exp(-mu * t)
    )
    p_dead = 1.0 - p_external - p_internal
    axes[1].plot(t, p_external, color=BLUE, label="extracellular")
    axes[1].plot(t, p_internal, color=ORANGE, label="intracellular")
    axes[1].plot(t, p_dead, color=GREEN, label="dead")
    axes[1].set_title(r"Absorption--death: $\alpha=1,\ \mu=0.4$")

    for ax in axes:
        ax.set_xlabel("Time $t$")
        ax.set_xlim(0, 7)
        ax.set_ylim(0, 1.02)
        ax.legend(frameon=False)
    axes[0].set_ylabel("State probability")
    save(fig, "absorption_probabilities.pdf")


def self_check() -> None:
    critical = survival_series(0.5, 3)
    expected = np.array([1.0, 0.5, 0.375, 0.3046875])
    if not np.allclose(critical, expected, rtol=0.0, atol=1e-14):
        raise AssertionError("critical survival recurrence failed")
    if not math.isclose(
        kolmogorov_constant(0.4), 0.237646658969725, rel_tol=2e-10
    ):
        raise AssertionError("Kolmogorov product check failed")


def main() -> None:
    self_check()
    make_survival_regimes()
    make_conditional_means()
    make_kolmogorov_constant()
    make_cohort_survival()
    make_absorption_probabilities()
    print("Generated chapter figures in", OUT)


if __name__ == "__main__":
    main()
