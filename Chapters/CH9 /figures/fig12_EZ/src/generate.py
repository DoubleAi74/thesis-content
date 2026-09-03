#!/usr/bin/env python3
"""Host-to-host mean offspring E(Z) against the phase-1 catastrophe rate.

Closed form var:eq:EZ; no simulation.
Parameters: (λ1, μ1) = (1, 0.2), (λ2, μ2) = (1, 0.9), as on the source plot.
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


def roots(lam, mu, delta):
    eta = (lam + mu + delta) / (2.0 * lam)
    disc = eta**2 - mu / lam
    s = np.sqrt(np.maximum(disc, 0.0))
    return eta + s, eta - s


def EZ(delta, lam1=1.0, mu1=0.2, lam2=1.0, mu2=0.9):
    delta = np.asarray(delta, dtype=float)
    a, b = roots(lam1, mu1, delta)
    return 2.0 * (1.0 - b - (delta / lam1) * mu2 / (a * lam2 - mu2))


def mean_burst(delta, lam1=1.0, mu1=0.2):
    """Unconditional E(K), including mass b at zero."""
    delta = np.asarray(delta, dtype=float)
    a, _b = roots(lam1, mu1, delta)
    return (delta / lam1) * a / (a - 1.0) ** 2


def main():
    d = np.linspace(1e-4, 0.20, 400)
    y = EZ(d)
    y0 = float(EZ(np.array([1e-6]))[0])
    # Crossing of the unit line (the epidemic threshold), not an interior max:
    # on this interval E(Z) is decreasing in δ1.
    cross = float(d[np.where(y <= 1.0)[0][0]]) if np.any(y <= 1.0) else None

    fig, ax = plt.subplots(figsize=style_rc.FIGSIZE_SINGLE)
    ax.plot(d, y, color=style_rc.BLUE, lw=1.8)
    ax.axhline(1.0, color=style_rc.CATA, lw=1.0, ls="-")
    if cross is not None:
        ax.axvline(cross, color=style_rc.SOFT, lw=0.7, ls=(0, (3, 2)))
        ax.plot([cross], [1.0], "o", color=style_rc.VERMILLION, ms=5, zorder=5)
        ax.annotate(
            rf"$\mathbb{{E}}(Z)=1$ at $\delta_1\simeq{cross:.3f}$",
            xy=(cross, 1.0),
            xytext=(cross + 0.018, 1.22),
            color=style_rc.VERMILLION,
            fontsize=9,
        )
    ax.set_xlabel(r"phase-1 catastrophe rate $\delta_1$")
    ax.set_ylabel(r"host-to-host mean $\mathbb{E}(Z)$")
    ax.set_xlim(0.0, 0.20)
    ax.set_ylim(0.55, 1.85)
    fig.tight_layout()
    style_rc.save_figure(fig, OUT / "fig12.pdf", OUT / "fig12.png")

    meta = {
        "id": "fig12_EZ",
        "simulation": False,
        "parameters": {
            "lambda1": 1.0,
            "mu1": 0.2,
            "lambda2": 1.0,
            "mu2": 0.9,
        },
        "derived": {
            "EZ_delta_to_0": y0,
            "delta1_unit_crossing": cross,
            "EZ_at_0.2": float(EZ(np.array([0.2]))[0]),
        },
    }
    (OUT / "meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print("wrote", OUT / "fig12.pdf", "unit crossing", cross)


if __name__ == "__main__":
    main()
