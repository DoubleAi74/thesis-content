#!/usr/bin/env python3
"""Minimum founding cohort K* of the public-good model, vs μ − λ0."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "figures" / "_style"))
import style_rc  # noqa: E402
from public_good import kstar, survival_prob  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parents[1]
OUT.mkdir(parents=True, exist_ok=True)

LAM0, ALPHA, G, C = 0.6, 0.25, 0.15, 0.45  # c/g = 3
N_PATHS = 600
K_MAX = 28
SEED = 17
# Excess death rate μ − λ0. Without the public good, survival → 0 for all K.
DELTAS = np.array([0.15, 0.25, 0.35, 0.50, 0.70, 0.95, 1.20])


def main():
    ks, ps = [], []
    for dmu in DELTAS:
        mu = LAM0 + float(dmu)
        K, p = kstar(
            LAM0, mu, ALPHA, G, C,
            n_paths=N_PATHS, k_max=K_MAX, seed=SEED, thresh=0.5,
        )
        ks.append(K if K is not None else np.nan)
        ps.append(p if p is not None else np.nan)
        print(f"mu-lam0={dmu:.2f}  K*={K}  p={p}")

    # Survival curve at one interior point, for the caption to have a picture
    # of the threshold as well as of its movement.
    mu_mid = LAM0 + 0.50
    Kgrid = np.arange(1, 16)
    pgrid = [
        survival_prob(int(K), LAM0, mu_mid, ALPHA, G, C, n_paths=N_PATHS, seed=SEED + 100 + int(K))
        for K in Kgrid
    ]

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=style_rc.FIGSIZE_DOUBLE)

    ax0.plot(Kgrid, pgrid, "o-", color=style_rc.BLUE, lw=1.6, ms=5)
    ax0.axhline(0.5, color=style_rc.CATA, lw=1.0)
    ax0.set_xlabel(r"founding cohort $K$")
    ax0.set_ylabel(r"estimated $\lim_t\,\mathbb{P}(X_t>0\mid X_0=K)$")
    ax0.set_xlim(0.5, 15.5)
    ax0.set_ylim(-0.02, 1.02)

    ax1.plot(DELTAS, ks, "o-", color=style_rc.BLUE, lw=1.6, ms=5)
    ax1.axhline(C / G, color=style_rc.SOFT, lw=0.8, ls=(0, (3, 2)))
    ax1.set_xlabel(r"excess death $\mu-\lambda_0$")
    ax1.set_ylabel(r"minimum founding cohort $K^\ast$")
    ax1.set_xlim(0.1, 1.25)

    fig.tight_layout()
    style_rc.save_figure(fig, OUT / "fig14.pdf", OUT / "fig14.png")
    meta = {
        "id": "fig14_kstar",
        "simulation": True,
        "parameters": {
            "lambda0": LAM0,
            "alpha": ALPHA,
            "g": G,
            "c": C,
            "n_paths": N_PATHS,
            "k_max": K_MAX,
            "threshold": 0.5,
            "c_over_g": C / G,
        },
        "deltas": DELTAS.tolist(),
        "Kstar": [None if (isinstance(k, float) and np.isnan(k)) else k for k in ks],
        "p_at_Kstar": ps,
        "mu_mid": mu_mid,
        "Kgrid": Kgrid.tolist(),
        "pgrid": pgrid,
        "seed": SEED,
    }
    (OUT / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print("wrote", OUT / "fig14.pdf")


if __name__ == "__main__":
    main()
