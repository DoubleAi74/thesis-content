#!/usr/bin/env python3
"""Generate F4a.4: defective and conditional burst-time densities."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

STYLE_DIR = Path(
    "/Users/adamaldridge/Desktop/Thesis content 🎓 /4 BDC additional and BMVR/"
    "Figures run/style"
)
sys.path.insert(0, str(STYLE_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_style"))
import style_rc  # noqa: E402

FIGDIR = Path(__file__).resolve().parents[1]
FIGSTEM = "fig09"

style_rc.apply()

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402


PARAMETER_SETS = (
    (1.0, 0.2, 0.05, style_rc.BLUE),
    (1.0, 0.0, 0.1, style_rc.VERMILLION),
)
WORKDIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORKDIR.parents[2]
PDF_PATH = FIGDIR / (FIGSTEM + ".pdf")
PNG_PATH = FIGDIR / (FIGSTEM + ".png")


def roots(lam: float, mu: float, delta: float) -> tuple[float, float, float]:
    eta = (lam + mu + delta) / (2.0 * lam)
    discriminant = eta**2 - mu / lam
    assert discriminant >= 0.0
    a = eta + math.sqrt(discriminant)
    b = eta - math.sqrt(discriminant)
    theta = lam * (a - b)
    return a, b, theta


def mean_load(
    t: np.ndarray, lam: float, mu: float, delta: float
) -> tuple[np.ndarray, float]:
    """Return J(t) and the no-burst mass b at infinity."""
    a, b, theta = roots(lam, mu, delta)
    cap_a = a - 1.0
    cap_b = 1.0 - b
    w = np.exp(theta * t)
    j = (a - b) ** 2 * w / (cap_b + cap_a * w) ** 2
    return j, b


def run_asserts() -> dict[tuple[float, float, float], float]:
    masses: dict[tuple[float, float, float], float] = {}
    integration_t = np.linspace(0.0, 50.0, 200_001)
    for lam, mu, delta, _ in PARAMETER_SETS:
        a, b, _ = roots(lam, mu, delta)
        assert b < 1.0 < a
        assert abs(a * b - mu / lam) < 1e-13
        assert abs((a - 1.0) * (1.0 - b) - delta / lam) < 1e-13
        j, b_from_curve = mean_load(integration_t, lam, mu, delta)
        phi = delta * j
        mass = float(np.trapezoid(phi, integration_t))
        assert np.all(np.isfinite(phi)) and np.all(phi >= 0.0)
        assert abs(b_from_curve - b) < 1e-15
        assert abs(mass - (1.0 - b)) < 1e-2
        if mu == 0.0:
            assert abs(b) < 1e-15
            assert abs(mass - 1.0) < 1e-2
            assert np.max(np.abs(phi - phi / (1.0 - b))) < 1e-14
        masses[(lam, mu, delta)] = mass
    return masses


def make_figure() -> None:
    run_asserts()
    t = np.linspace(0.0, 15.0, 900)
    fig, ax = plt.subplots(figsize=(5.23, 3.16))

    for lam, mu, delta, colour in PARAMETER_SETS:
        j, b = mean_load(t, lam, mu, delta)
        phi = delta * j
        parameter_text = rf"$(\lambda,\mu,\delta)=({lam:g},{mu:g},{delta:g})$"
        if mu > 0.0:
            ax.plot(
                t,
                phi,
                color=colour,
                linestyle="-",
                label=rf"$\varphi(t)$, {parameter_text}",
            )
            ax.plot(
                t,
                phi / (1.0 - b),
                color=colour,
                linestyle="--",
                label=rf"$\varphi(t)/(1-b)$, {parameter_text}",
            )
        else:
            ax.plot(
                t,
                phi,
                color=colour,
                linestyle="-",
                label=rf"$\varphi(t)=\varphi(t)/(1-b)$, {parameter_text}",
            )

    _, b_positive = mean_load(t, 1.0, 0.2, 0.05)
    ax.text(
        0.8175,
        0.745,
        rf"point mass $b={b_positive:.4f}$" "\n"
        r"at $\tau=\infty$ ($\mu=0.2$)",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=9,
        color=style_rc.SOFT,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9, "pad": 2.0},
        zorder=5,
    )

    ax.set_xlim(0.0, 15.0)
    ax.set_ylim(bottom=0.0)
    ax.set_xlabel(r"time $t$")
    ax.set_ylabel("density")
    ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.64))
    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)


if __name__ == "__main__":
    checked_masses = run_asserts()
    make_figure()
    mass_report = ", ".join(
        f"{params}: {mass:.6f}" for params, mass in checked_masses.items()
    )
    print(f"asserts: pass; integrated masses [{mass_report}]")
    print(f"wrote {PDF_PATH} and {PNG_PATH}")
