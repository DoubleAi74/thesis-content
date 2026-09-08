#!/usr/bin/env python3
"""Logistic speciation with a constant extinction rate.

Origination follows beta_3(t) = sigma N'(t), one of the alternative rate laws
of the section; extinction is constant at mu per species, suppressed at
S_t = 1 so that a genus cannot lose its last species.  Paths are exact,
simulated by thinning against the envelope (beta_max + mu) * n.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "figures" / "_style"))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parents[1]

K, N0, RHO, SIGMA, MU = 10.0, 5.0, 0.8, 0.8, 0.4
TMAX = 15.0
NPATH = 400          # paths averaged for the mean
NSHOW = 160          # paths drawn faintly
SEED = 11
XI = K / N0 - 1.0
BETA_MAX = SIGMA * RHO * K / 4.0     # N0 = K/2, so the maximum is at t = 0


def N(t):
    return K * np.exp(RHO * t) / (XI + np.exp(RHO * t))


def beta(t):
    """sigma * dN/dt for the logistic N."""
    n = N(t)
    return SIGMA * RHO * n * (1.0 - n / K)


def path(rng):
    """One exact realisation, by thinning. Returns (times, counts)."""
    t, n = 0.0, 1
    ts, ns = [0.0], [1]
    env_rate = BETA_MAX + MU
    while t < TMAX:
        t += rng.exponential(1.0 / (env_rate * n))
        if t >= TMAX:
            break
        u = rng.random() * env_rate
        if u < beta(t):
            n += 1
        elif u < beta(t) + MU and n > 1:      # the last species cannot go
            n -= 1
        else:
            continue                           # thinned out; no event
        ts.append(t)
        ns.append(n)
    ts.append(TMAX)
    ns.append(n)
    return np.array(ts), np.array(ns)


def main() -> None:
    rng = np.random.default_rng(SEED)
    grid = np.linspace(0.0, TMAX, 900)
    paths, on_grid = [], np.empty((NPATH, grid.size))
    for i in range(NPATH):
        ts, ns = path(rng)
        # left-continuous step interpolation onto the common grid
        on_grid[i] = ns[np.searchsorted(ts, grid, side="right") - 1]
        if i < NSHOW:
            paths.append((ts, ns))
    mean = on_grid.mean(axis=0)

    fig, (ax0, ax1) = plt.subplots(
        2, 1, figsize=(5.6, 4.3), sharex=True, layout="constrained",
        gridspec_kw={"height_ratios": [3.0, 1.0], "hspace": 0.06},
    )

    for ts, ns in paths:
        ax0.step(ts, ns, where="post", color=style_rc.BLUE, lw=0.7, alpha=0.07)
    ax0.plot(grid, mean, color=style_rc.BLUE, lw=1.9)
    ax0.set_ylabel(r"$S_t$: number of species")
    ax0.set_ylim(0, 30)

    ax1.plot(grid, beta(grid), color=style_rc.VERMILLION, lw=1.4,
             label=r"origination $\beta_3(t)=\sigma N'(t)$")
    ax1.axhline(MU, color=style_rc.CATA, lw=1.4, label=r"extinction $\mu$")
    ax1.set_ylabel("rate")
    ax1.set_xlabel(r"time $t$")
    ax1.set_xlim(0, TMAX)
    ax1.set_ylim(0, 1.85)
    ax1.legend(loc="upper right")

    style_rc.save_figure(fig, OUT / "fig02c.pdf", OUT / "fig02c.png")
    plt.close(fig)

    t_cross = float(grid[np.argmin(np.abs(beta(grid) - MU))])
    t_peak = float(grid[np.argmax(mean)])
    (OUT / "meta.json").write_text(json.dumps({
        "id": "fig02c_extinction",
        "simulation": True,
        "seed": SEED,
        "paths_averaged": NPATH,
        "paths_drawn": NSHOW,
        "parameters": {"K": K, "N0": N0, "rho": RHO, "sigma": SIGMA, "mu": MU},
        "rate_crossing": t_cross,
        "mean_peak_time": t_peak,
        "mean_peak": float(mean.max()),
        "mean_final": float(mean[-1]),
        "pure_birth_limit_mean": float(np.exp(SIGMA * (K - N0))),
    }, indent=2) + "\n")
    print(f"crossing t={t_cross:.2f}  mean peaks {mean.max():.1f} at t={t_peak:.2f}  "
          f"final {mean[-1]:.2f}  pure-birth limit {np.exp(SIGMA*(K-N0)):.1f}")


if __name__ == "__main__":
    main()
