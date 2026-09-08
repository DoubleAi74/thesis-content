#!/usr/bin/env python3
"""Regenerate unconditional ultimate-release figures (lattice killed master equations).

Matches the construction in Appendix E.4 / TT_bdc_release_visualiser:
  P(0,0) = residual no-catastrophe mass at large T  (~ sigma_infty)
  P(m,n) = integrated catastrophe flux for m+n >= 1
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Defaults used in the paper draft captions (type-1 start).
RATES = dict(
    lambda1=1.0,
    mu1=0.5,
    nu=0.3,
    delta1=0.25,
    lambda2=1.2,
    mu2=0.4,
    delta2=0.15,
)
START = 1  # 1 -> (1,0), 2 -> (0,1)
M = 24
T = 28.0
OUT = Path(__file__).resolve().parent
BLUE, VERM = "#0072B2", "#D55E00"


def integrate(p: dict, start: int, M: int, T: float):
    l1, mu1, nu, d1 = p["lambda1"], p["mu1"], p["nu"], p["delta1"]
    l2, mu2, d2 = p["lambda2"], p["mu2"], p["delta2"]
    m_idx = np.arange(M + 1)
    n_idx = np.arange(M + 1)
    mm, nn = np.meshgrid(m_idx, n_idx, indexing="ij")
    b1, d1r, cv = l1 * mm, mu1 * mm, nu * mm
    b2, d2r, cat = l2 * nn, mu2 * nn, d1 * mm + d2 * nn
    leave = b1 + d1r + cv + b2 + d2r + cat
    rate_scale = float((l1 + mu1 + nu + d1 + l2 + mu2 + d2) * M + 1e-9)
    dt = max(2e-4, min(0.01, 0.25 / rate_scale))

    def rhs(P):
        out = -leave * P
        out[1:, :] += b1[:-1, :] * P[:-1, :]
        out[:-1, :] += d1r[1:, :] * P[1:, :]
        out[:-1, 1:] += cv[1:, :-1] * P[1:, :-1]
        out[:, 1:] += b2[:, :-1] * P[:, :-1]
        out[:, :-1] += d2r[:, 1:] * P[:, 1:]
        leak = float(
            np.sum(b1[M, :] * P[M, :])
            + np.sum(b2[:, M] * P[:, M])
            + np.sum(cv[1:, M] * P[1:, M])
        )
        return out, leak

    P = np.zeros((M + 1, M + 1))
    if start == 1:
        P[1, 0] = 1.0
    else:
        P[0, 1] = 1.0
    flux = np.zeros_like(P)
    leak_tot = 0.0
    t = 0.0
    while t < T - 0.5 * dt:
        h = min(dt, T - t)
        k1, a = rhs(P)
        k2, b = rhs(P + 0.5 * h * k1)
        k3, c = rhs(P + 0.5 * h * k2)
        k4, d = rhs(P + h * k3)
        f0 = cat * P
        P = np.maximum(P + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4), 0.0)
        flux += 0.5 * h * (f0 + cat * P)
        leak_tot += (h / 6.0) * (a + 2 * b + 2 * c + d)
        t += h

    residual = float(P.sum())
    joint = flux.copy()
    joint[0, 0] = residual
    joint /= joint.sum()
    return {
        "joint": joint,
        "margX": joint.sum(axis=1),
        "margY": joint.sum(axis=0),
        "p00": float(joint[0, 0]),
        "leak": leak_tot,
        "residual_active": residual - float(P[0, 0]),
        "M": M,
        "T": t,
    }


def main():
    res = integrate(RATES, START, M, T)
    print(
        f"p00={res['p00']:.6f} leak={res['leak']:.3e} "
        f"res_act={res['residual_active']:.3e}"
    )

    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 10,
            "axes.labelsize": 11,
            "axes.titlesize": 11,
            "figure.dpi": 160,
            "savefig.dpi": 220,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )

    joint = res["joint"]
    Z = joint.T
    pos = Z[Z > 0]
    zmax = max(float(np.percentile(pos, 99)), joint[0, 0] * 0.35, 1e-4)
    cmap = LinearSegmentedColormap.from_list(
        "rel", ["#f7f8fa", "#c6d8e8", "#6fa3c7", "#2b6a9e", "#0b3d66"]
    )
    view = 14
    fig, ax = plt.subplots(figsize=(5.2, 4.6))
    im = ax.imshow(
        Z,
        origin="lower",
        aspect="equal",
        extent=(-0.5, M + 0.5, -0.5, M + 0.5),
        cmap=cmap,
        vmin=0,
        vmax=zmax,
        interpolation="nearest",
    )
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04).set_label(
        r"$P(X_{\mathrm{rel}}=m,\,Y_{\mathrm{rel}}=n)$"
    )
    ax.set_xlabel(r"$m$  (type 1, $X_{\mathrm{rel}}$)")
    ax.set_ylabel(r"$n$  (type 2, $Y_{\mathrm{rel}}$)")
    ax.set_title(r"Joint release law (unconditional)")
    ax.plot(
        [0],
        [0],
        marker="o",
        markersize=5,
        markerfacecolor="none",
        markeredgecolor="#b06a00",
        markeredgewidth=1.2,
    )
    ax.set_xlim(-0.5, view + 0.5)
    ax.set_ylim(-0.5, view + 0.5)
    fig.tight_layout()
    fig.savefig(OUT / "fig_release_joint.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)

    margX, margY = res["margX"], res["margY"]
    mass = margX + margY
    nz = np.where(mass > 1e-4)[0]
    cut = min(M, max(12, int(nz.max()) + 2 if nz.size else 12))
    kk = np.arange(cut + 1)
    w = 0.4
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.bar(
        kk - w / 2,
        margX[: cut + 1],
        width=w,
        color=BLUE,
        alpha=0.9,
        label=r"$P(X_{\mathrm{rel}}=k)$",
    )
    ax.bar(
        kk + w / 2,
        margY[: cut + 1],
        width=w,
        color=VERM,
        alpha=0.9,
        label=r"$P(Y_{\mathrm{rel}}=k)$",
    )
    ax.set_xlabel(r"$k$")
    ax.set_ylabel("probability")
    ax.set_title(r"Marginal release laws (unconditional)")
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(
        OUT / "fig_release_marginals.png", bbox_inches="tight", facecolor="white"
    )
    plt.close(fig)

    (OUT / "meta.txt").write_text(
        f"start={'type1' if START == 1 else 'type2'} M={M} T={res['T']:.3f}\n"
        f"p00={res['p00']:.6f} leak={res['leak']:.4e} "
        f"res_act={res['residual_active']:.3e}\n"
        f"rates={RATES}\n"
    )
    print("wrote", OUT / "fig_release_joint.png")
    print("wrote", OUT / "fig_release_marginals.png")


if __name__ == "__main__":
    main()
