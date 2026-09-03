#!/usr/bin/env python3
"""
fig_precatastrophe_moments

Expected pre-catastrophe counts E[X_{tau_c-}] and E[Y_{tau_c-}] over the
(delta_1, delta_2) plane, at three conversion rates nu.

No simulation enters the figure. Each grid point is one deterministic
integration of the moment hierarchy obtained by differentiating the killed
generating-function system at (x,y) = (1,1); the two running integrals give
the time-integrated flux, and dividing by 1 - h gives the conditional means.

Notation follows the paper:
    S, G                 no-catastrophe probabilities  F_i(1,1,t)
    A1 = d_x F_1         B1 = d_y F_1        B2 = d_y F_2
    P1 = d_xx F_1        Q1 = d_xy F_1       R1 = d_yy F_1     R2 = d_yy F_2
    theta_i              linearisation exponent of the type-i Riccati flow

Birth and death are held equal across the two types and fixed throughout,
with birth above death, so that the only demographic parameter varying
between columns is the conversion rate nu.

Runtime: roughly 15 minutes for the default grid; --quick for a preview.
"""
import argparse
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, LogNorm
from matplotlib.ticker import FuncFormatter, NullLocator

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, ".."))

# birth and death: equal across types, fixed, birth above death
LAM1 = LAM2 = 1.2
MU1 = MU2 = 0.8
NU_VALUES = (0.1, 0.4, 1.0)     # 0.4 = lam - mu is exactly type-1 criticality

D1_LO, D1_HI = 0.0, 0.5
D2_LO, D2_HI = 0.02, 0.5        # delta_2 = 0 is singular; see module docstring


def solve_hierarchy(d1, d2, nu, T, nsteps, lam1=LAM1, mu1=MU1,
                    lam2=LAM2, mu2=MU2, tail_frac=0.05):
    """Vectorised fixed-step RK4 over flat arrays d1, d2, nu of equal length.

    Returns (EX, EY, h, tail); tail is the fraction of each running integral
    accumulated in the final tail_frac of [0, T] -- a horizon self-check that
    should be ~0 when T is long enough.
    """
    k1 = lam1 + mu1 + nu + d1          # kappa_1
    k2 = lam2 + mu2 + d2               # kappa_2
    n = d1.size

    u = np.stack([
        np.ones(n), np.ones(n),                                # S, G
        np.ones(n), np.zeros(n), np.ones(n),                   # A1, B1, B2
        np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n),    # P1,Q1,R1,R2
        np.zeros(n), np.zeros(n),                              # running ints
    ])

    def rhs(u):
        S, G, A1, B1, B2, P1, Q1, R1, R2, _, _ = u
        th1 = 2 * lam1 * S - k1
        th2 = 2 * lam2 * G - k2
        return np.stack([
            lam1 * S * S - k1 * S + mu1 + nu * G,
            lam2 * G * G - k2 * G + mu2,
            th1 * A1,
            th1 * B1 + nu * B2,
            th2 * B2,
            th1 * P1 + 2 * lam1 * A1 * A1,
            th1 * Q1 + 2 * lam1 * A1 * B1,
            th1 * R1 + 2 * lam1 * B1 * B1 + nu * R2,
            th2 * R2 + 2 * lam2 * B2 * B2,
            d1 * (A1 + P1) + d2 * Q1,
            d1 * Q1 + d2 * (B1 + R1),
        ])

    dt = T / nsteps
    mark = int((1 - tail_frac) * nsteps)
    IX_m = IY_m = None
    for i in range(nsteps):
        a = rhs(u); b = rhs(u + dt / 2 * a)
        c = rhs(u + dt / 2 * b); e = rhs(u + dt * c)
        u = u + dt / 6 * (a + 2 * b + 2 * c + e)
        if i == mark:
            IX_m, IY_m = u[9].copy(), u[10].copy()

    h = u[0]
    EX, EY = u[9] / (1 - h), u[10] / (1 - h)
    tail = np.maximum(np.abs(u[9] - IX_m) / np.maximum(np.abs(u[9]), 1e-30),
                      np.abs(u[10] - IY_m) / np.maximum(np.abs(u[10]), 1e-30))
    return EX, EY, h, tail


def singular_edge_threshold(nu, lam1=LAM1, mu1=MU1, lam2=LAM2, mu2=MU2):
    """On delta_2 = 0 one has G == 1, so theta_2 = lam2 - mu2 > 0 and
    E[Y_{tau-}] diverges whenever theta_1(inf) + (lam2 - mu2) > 0.
    Returns the largest delta_1 for which the edge is still divergent
    (0.0 if the edge is regular for every delta_1 >= 0)."""
    g2 = lam2 - mu2

    def excess(d1):
        k1 = lam1 + mu1 + nu + d1
        disc = k1 ** 2 - 4 * lam1 * (mu1 + nu)
        return -np.sqrt(max(disc, 0.0)) + g2

    if excess(0.0) <= 0:
        return 0.0
    lo, hi = 0.0, 10.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if excess(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


BLUE = ["#eaf2fd", "#cde2fb", "#9ec5f4", "#6da7ec",
        "#3987e5", "#256abf", "#184f95", "#0d366b"]
VERM = ["#fdeee6", "#fbd3c0", "#f8b191", "#f28c62",
        "#eb6834", "#c04d22", "#8a3414", "#5c210c"]

CONTOURS = [0.3, 0.5, 1, 2, 3, 5, 10, 20, 30]
CBAR_TICKS = [0.3, 1, 3, 10, 30]


def render(d1_ax, d2_ax, EXs, EYs, usetex=True):
    plt.rcParams.update({
        "text.usetex": usetex,
        "text.latex.preamble": r"\usepackage{lmodern}\usepackage[T1]{fontenc}"
                               r"\usepackage{amsmath,amssymb}",
        "font.family": "serif",
        "font.size": 8.5,
        "axes.linewidth": 0.6,
        "xtick.major.width": 0.6, "ytick.major.width": 0.6,
        "xtick.major.size": 2.3, "ytick.major.size": 2.3,
        "xtick.direction": "out", "ytick.direction": "out",
    })
    cmapX = LinearSegmentedColormap.from_list("bl", BLUE)
    cmapY = LinearSegmentedColormap.from_list("vm", VERM)

    # one shared normalisation across all six panels, so every panel is
    # directly comparable both across nu and between the two types
    allZ = np.concatenate([Z.ravel() for Z in list(EXs) + list(EYs)])
    norm = LogNorm(vmin=allZ.min(), vmax=allZ.max())

    fig, axes = plt.subplots(2, 3, figsize=(7.2, 4.35),
                             constrained_layout=True)

    for row, (Zs, cmap, rowlab) in enumerate([
            (EXs, cmapX, r"$\mathbb{E}\!\left[X_{\tau_c-}\right]$"),
            (EYs, cmapY, r"$\mathbb{E}\!\left[Y_{\tau_c-}\right]$")]):
        for col, (Z, nu) in enumerate(zip(Zs, NU_VALUES)):
            ax = axes[row, col]
            im = ax.pcolormesh(d1_ax, d2_ax, Z, cmap=cmap, norm=norm,
                               shading="gouraud", rasterized=True)
            lv = [l for l in CONTOURS if Z.min() < l < Z.max()]
            if lv:
                cs = ax.contour(d1_ax, d2_ax, Z, levels=lv,
                                colors="#00000077", linewidths=0.45)
                # Label only contours that cross the panel interior. A level
                # sitting in the extreme tail of the panel's value range hugs a
                # corner, and its inline label gets clipped by the axes edge.
                lab = [l for l in lv if 0.06 < float((Z < l).mean()) < 0.94]
                if lab:
                    ax.clabel(cs, levels=lab, inline=True, fontsize=5.4,
                              fmt="%g", inline_spacing=2)

            ax.set_xlim(D1_LO, D1_HI); ax.set_ylim(D2_LO, D2_HI)
            ax.set_xticks([0, 0.25, 0.5]); ax.set_yticks([0.1, 0.3, 0.5])
            for s in ax.spines.values():
                s.set_color("#5a5a5a")
            if row == 0:
                ax.set_title(rf"$\nu={nu:.1f}$", fontsize=8.5, pad=4)
            if row == 1:
                ax.set_xlabel(r"type-1 catastrophe rate $\delta_1$",
                              fontsize=8.0)
            if col == 0:
                ax.set_ylabel(r"type-2 rate $\delta_2$", fontsize=8.0)
            else:
                ax.tick_params(labelleft=False)

        cb = fig.colorbar(im, ax=axes[row, :].tolist(), pad=0.015, aspect=17)
        cb.set_label(rowlab, fontsize=8.5)
        cb.set_ticks(CBAR_TICKS)
        cb.ax.yaxis.set_minor_locator(NullLocator())
        cb.ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
        cb.ax.tick_params(labelsize=6.6, width=0.6, length=2.1)
        cb.outline.set_linewidth(0.5); cb.outline.set_edgecolor("#5a5a5a")

    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(OUT, f"fig_precatastrophe_moments.{ext}"),
                    dpi=220, bbox_inches="tight")
    return fig


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--no-usetex", action="store_true")
    ap.add_argument("--replot", action="store_true",
                    help="re-render from cached griddata.npz; no recomputation")
    args = ap.parse_args()

    if args.replot:
        d = np.load(os.path.join(OUT, "griddata.npz"))
        render(d["d1_ax"], d["d2_ax"], list(d["EX"]), list(d["EY"]),
               usetex=not args.no_usetex)
        print("re-rendered from cache")
        return

    N = 41 if args.quick else 111
    T, nsteps = (120.0, 20_000) if args.quick else (120.0, 60_000)

    d1_ax = np.linspace(D1_LO, D1_HI, N)
    d2_ax = np.linspace(D2_LO, D2_HI, N)
    D1, D2 = np.meshgrid(d1_ax, d2_ax, indexing="xy")

    # solve all three nu blocks in a single vectorised pass
    d1f = np.tile(D1.ravel(), len(NU_VALUES))
    d2f = np.tile(D2.ravel(), len(NU_VALUES))
    nuf = np.repeat(np.array(NU_VALUES), D1.size)
    EX, EY, h, tail = solve_hierarchy(d1f, d2f, nuf, T, nsteps)

    EXs = [EX[i * D1.size:(i + 1) * D1.size].reshape(N, N)
           for i in range(len(NU_VALUES))]
    EYs = [EY[i * D1.size:(i + 1) * D1.size].reshape(N, N)
           for i in range(len(NU_VALUES))]

    checks = {
        "max_tail_fraction": float(tail.max()),
        "per_nu": {f"{nu:g}": {"EX_range": [float(x.min()), float(x.max())],
                               "EY_range": [float(y.min()), float(y.max())]}
                   for nu, x, y in zip(NU_VALUES, EXs, EYs)},
        "singular_edge_delta1_threshold": {
            f"{nu:g}": float(singular_edge_threshold(nu)) for nu in NU_VALUES},
    }

    # step-halving on a spread of points including the awkward corner
    p1 = np.array([0.0, 0.0, 0.5, 0.5, 0.25, 0.02])
    p2 = np.array([0.02, 0.5, 0.02, 0.5, 0.25, 0.05])
    for nu in NU_VALUES:
        nuv = np.full(p1.size, nu)
        a1, b1, _, _ = solve_hierarchy(p1, p2, nuv, T, nsteps)
        a2, b2, _, _ = solve_hierarchy(p1, p2, nuv, T, 2 * nsteps)
        checks.setdefault("step_halving_max_abs_change", {})[f"{nu:g}"] = [
            float(np.abs(a2 - a1).max()), float(np.abs(b2 - b1).max())]

    print(json.dumps(checks, indent=2))
    np.savez(os.path.join(OUT, "griddata.npz"), d1_ax=d1_ax, d2_ax=d2_ax,
             nu=np.array(NU_VALUES), EX=np.array(EXs), EY=np.array(EYs))
    render(d1_ax, d2_ax, EXs, EYs, usetex=not args.no_usetex)
    print("wrote fig_precatastrophe_moments.{pdf,png}")


if __name__ == "__main__":
    main()
