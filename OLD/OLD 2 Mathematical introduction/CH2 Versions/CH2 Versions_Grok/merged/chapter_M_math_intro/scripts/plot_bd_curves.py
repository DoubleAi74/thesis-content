#!/usr/bin/env python3
"""Linear birth--death mean and survival curves for Chapter M figures."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parents[1] / "figures" / "tikz_gen"
OUT.mkdir(parents=True, exist_ok=True)

# Thesis-friendly style
plt.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 12,
        "legend.fontsize": 9.5,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.dpi": 160,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "mathtext.fontset": "cm",
    }
)

BLUE = "#1f77b4"
ORANGE = "#ff7f0e"
GREEN = "#2ca02c"
RED = "#d62728"
PURPLE = "#9467bd"


def survival_N1(t, lam, mu):
    """S(t) = 1 - p_0(t) for N=1 linear BD (Kendall)."""
    t = np.asarray(t, dtype=float)
    if np.isclose(lam, mu):
        return 1.0 / (1.0 + lam * t)
    # S(t) = (lam - mu) / (lam - mu * exp((mu-lam)t))
    return (lam - mu) / (lam - mu * np.exp((mu - lam) * t))


def mean_N1(t, lam, mu):
    return np.exp((lam - mu) * t)


def main():
    t = np.linspace(0, 8, 400)

    # --- Figure 1: mean trajectories, three regimes ---
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    regimes = [
        (0.6, 1.0, "subcritical $\\lambda<\\mu$", BLUE),
        (1.0, 1.0, "critical $\\lambda=\\mu$", ORANGE),
        (1.4, 1.0, "supercritical $\\lambda>\\mu$", GREEN),
    ]
    for lam, mu, lab, col in regimes:
        ax.plot(t, mean_N1(t, lam, mu), color=col, lw=2.0, label=lab)
    ax.axhline(1.0, color="#888888", lw=0.8, ls=":", alpha=0.8)
    ax.set_xlabel("$t$")
    ax.set_ylabel(r"$\mathbb{E}[X_t\mid X_0=1]$")
    ax.set_ylim(0, 4.2)
    ax.set_xlim(0, 8)
    ax.legend(frameon=False, loc="upper left")
    ax.set_title("Linear birth--death: mean size")
    fig.savefig(OUT / "bd_mean_regimes.pdf")
    fig.savefig(OUT / "bd_mean_regimes.png")
    plt.close(fig)

    # --- Figure 2: survival probability, three regimes ---
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    for lam, mu, lab, col in regimes:
        ax.plot(t, survival_N1(t, lam, mu), color=col, lw=2.0, label=lab)
    # Ultimate extinction lines
    ax.axhline(0.0, color=BLUE, lw=0.9, ls="--", alpha=0.45)
    ax.axhline(1 - 1.0 / 1.4, color=GREEN, lw=0.9, ls="--", alpha=0.55)
    ax.text(
        7.6,
        1 - 1.0 / 1.4 + 0.03,
        r"$1-\mu/\lambda$",
        color=GREEN,
        ha="right",
        va="bottom",
        fontsize=9,
    )
    ax.set_xlabel("$t$")
    ax.set_ylabel(r"$S(t)=\mathbb{P}(X_t>0\mid X_0=1)$")
    ax.set_ylim(0, 1.05)
    ax.set_xlim(0, 8)
    ax.legend(frameon=False, loc="upper right")
    ax.set_title("Linear birth--death: survival probability")
    fig.savefig(OUT / "bd_survival_regimes.pdf")
    fig.savefig(OUT / "bd_survival_regimes.png")
    plt.close(fig)

    # --- Figure 3: combined panel (for optional single inclusion) ---
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.35))
    for lam, mu, lab, col in regimes:
        axes[0].plot(t, mean_N1(t, lam, mu), color=col, lw=2.0, label=lab)
        axes[1].plot(t, survival_N1(t, lam, mu), color=col, lw=2.0, label=lab)
    axes[0].axhline(1.0, color="#888888", lw=0.8, ls=":", alpha=0.8)
    axes[0].set_xlabel("$t$")
    axes[0].set_ylabel(r"$\mathbb{E}[X_t\mid X_0=1]$")
    axes[0].set_ylim(0, 4.2)
    axes[0].set_xlim(0, 8)
    axes[0].set_title("Mean population size")
    axes[0].legend(frameon=False, fontsize=8.5, loc="upper left")

    axes[1].axhline(1 - 1.0 / 1.4, color=GREEN, lw=0.9, ls="--", alpha=0.55)
    axes[1].set_xlabel("$t$")
    axes[1].set_ylabel(r"$S(t)=\mathbb{P}(X_t>0)$")
    axes[1].set_ylim(0, 1.05)
    axes[1].set_xlim(0, 8)
    axes[1].set_title("Survival probability")
    axes[1].legend(frameon=False, fontsize=8.5, loc="upper right")

    fig.tight_layout()
    fig.savefig(OUT / "bd_mean_survival_panel.pdf")
    fig.savefig(OUT / "bd_mean_survival_panel.png")
    plt.close(fig)

    # --- Figure 4: conditional mean approach (subcritical) ---
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    lam, mu = 0.6, 1.0
    S = survival_N1(t, lam, mu)
    m = mean_N1(t, lam, mu)
    cond = m / S
    limit = mu / (mu - lam)
    ax.plot(t, cond, color=PURPLE, lw=2.2, label=r"$\mathbb{E}[X_t\mid X_t>0]$")
    ax.axhline(
        limit,
        color=RED,
        lw=1.4,
        ls="--",
        label=rf"limit $1/A_{{\mathrm{{c}}}}=\mu/(\mu-\lambda)={limit:.2f}$",
    )
    ax.set_xlabel("$t$")
    ax.set_ylabel("conditional mean")
    ax.set_xlim(0, 8)
    ax.set_ylim(0, limit * 1.15)
    ax.legend(frameon=False, loc="lower right")
    ax.set_title(r"Subcritical BD: conditional mean ($\lambda=0.6$, $\mu=1$)")
    fig.savefig(OUT / "bd_conditional_mean.pdf")
    fig.savefig(OUT / "bd_conditional_mean.png")
    plt.close(fig)

    print(f"Wrote figures to {OUT}")


if __name__ == "__main__":
    main()
