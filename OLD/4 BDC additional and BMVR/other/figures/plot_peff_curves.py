#!/usr/bin/env python3
"""
Effective-parameter curves p_eff(r), d_eff(r) for the burst-aware renewal
BMVR, for three representative intracellular parameter sets.

  p_eff(r) = delta*~K(r)/~Ihat(r),   d_eff(r) = 1/~Ihat(r) - r,
  limits:  p_eff(0) = V_inf/E[T_prod],  p_eff(inf) = delta,
           d_eff(0) = 1/E[T_prod],      d_eff(inf) = mu + delta.

Writes peff_dr_curves.pdf into this directory.
"""
from __future__ import annotations

import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUTDIR = os.path.dirname(os.path.abspath(__file__))

SETS = [
    (1.0, 0.0, 0.1),
    (1.0, 0.2, 0.05),
    (1.0, 0.9, 0.1),
]
COLORS = ["tab:blue", "tab:orange", "tab:green"]


def roots(beta: float, mu: float, delta: float):
    eta = (beta + mu + delta) / (2.0 * beta)
    disc = np.sqrt(eta**2 - mu / beta)
    a = eta + disc
    b = eta - disc
    return a, b, beta * (a - b)


def kernels_on_grid(t: np.ndarray, beta: float, mu: float, delta: float):
    a, b, th = roots(beta, mu, delta)
    A, B = a - 1.0, 1.0 - b
    q = np.exp(-th * t)
    I = (a * B * q + b * A) / (B * q + A)
    Ihat = (a - b) ** 2 * q / ((B * q + A) * (a - b * q))
    Ihat = np.where(t == 0.0, 1.0, Ihat)
    J = (a - b) ** 2 * q / (B * q + A) ** 2
    K = (1.0 + (2.0 * beta / delta) * (1.0 - I)) * J
    return Ihat, K, a, b, A, B


def main() -> None:
    t = np.linspace(0.0, 300.0, 30001)
    r_grid = np.linspace(0.0, 3.0, 61)

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.9))

    for (beta, mu, delta), col in zip(SETS, COLORS):
        Ihat, K, a, b, A, B = kernels_on_grid(t, beta, mu, delta)
        V_inf = a * B / A
        E_Tprod = np.log(a / (a - 1)) / beta
        p_eff = np.empty_like(r_grid)
        d_eff = np.empty_like(r_grid)
        for i, r in enumerate(r_grid):
            w = np.exp(-r * t)
            LI = np.trapezoid(w * Ihat, t)
            LK = np.trapezoid(w * K, t)
            p_eff[i] = delta * LK / LI
            d_eff[i] = 1.0 / LI - r
        label = rf"$(\beta,\mu,\delta)=({beta:g},{mu:g},{delta:g})$"
        axes[0].plot(r_grid, p_eff, color=col, lw=1.8, label=label)
        axes[1].plot(r_grid, d_eff, color=col, lw=1.8, label=label)
        # asymptotes
        axes[0].axhline(V_inf / E_Tprod, color=col, ls=":", lw=1.0, alpha=0.6)
        axes[0].axhline(delta, color=col, ls="--", lw=1.0, alpha=0.6)
        axes[1].axhline(1.0 / E_Tprod, color=col, ls=":", lw=1.0, alpha=0.6)
        axes[1].axhline(mu + delta, color=col, ls="--", lw=1.0, alpha=0.6)

    axes[0].set_yscale("log")
    axes[0].set_xlabel(r"epidemic growth rate $r$")
    axes[0].set_ylabel(r"$p_{\rm eff}(r)$")
    axes[0].set_title("Effective release rate")
    axes[1].set_xlabel(r"epidemic growth rate $r$")
    axes[1].set_ylabel(r"$d_{\mathcal{I},{\rm eff}}(r)$")
    axes[1].set_title("Effective removal rate")
    for ax in axes:
        ax.legend(fontsize=8)
        ax.grid(alpha=0.25)
    fig.suptitle(
        "Effective BMVR parameters vs growth rate "
        r"(dotted: $r=0$ limit; dashed: $r\to\infty$ limit)",
        fontsize=10,
    )
    fig.tight_layout()
    out = os.path.join(OUTDIR, "peff_dr_curves.pdf")
    fig.savefig(out)
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
