#!/usr/bin/env python3
"""Means and one-standard-deviation envelopes for X_t and W_t."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

STYLE_DIR = Path(__file__).resolve().parents[2] / "_style"
sys.path.insert(0, str(STYLE_DIR))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402

WORKDIR = Path(__file__).resolve().parent
PDF_PATH = WORKDIR.parents[2] / "figures/F4_mean_sd_XW.pdf"
PNG_PATH = WORKDIR / "preview.png"

LAMBDA, MU, DELTA = 1.0, 0.2, 0.05


def roots(lam, mu, delta):
    eta = (lam + mu + delta) / (2.0 * lam)
    radical = np.sqrt(eta**2 - mu / lam)
    return eta + radical, eta - radical


def moments(t, lam=LAMBDA, mu=MU, delta=DELTA):
    a, b = roots(lam, mu, delta)
    A, B = a - 1.0, 1.0 - b
    z = np.exp(-lam * (a - b) * np.asarray(t, dtype=float))
    I = (a * B * z + b * A) / (B * z + A)
    J = (a - b) ** 2 * z / (B * z + A) ** 2
    V = (1.0 - I) * (1.0 + (lam / delta) * (1.0 - I))
    K = (1.0 + (2.0 * lam / delta) * (1.0 - I)) * J
    var_x = K - J**2
    second_w = (
        (2.0 * (lam - mu) / delta) * V
        - ((lam + mu) / delta) * I
        - K
        + (lam + mu) / delta
        + 1.0
    )
    var_w = second_w - V**2
    return I, J, V, K, var_x, var_w


def sd_band(ax, t, mean, sd, color, mean_label):
    lower = np.maximum(0.0, mean - sd)
    upper = mean + sd
    ax.fill_between(t, lower, upper, color=color, alpha=0.16, linewidth=0.0, zorder=1)
    ax.plot(t, upper, color=color, linestyle="--", linewidth=0.9, alpha=0.8)
    ax.plot(t, lower, color=color, linestyle="--", linewidth=0.8, alpha=0.5)
    ax.plot(t, mean, color=color, linewidth=1.5, label=mean_label, zorder=3)


def main() -> None:
    t = np.linspace(0.0, 20.0, 2001)
    _, J, V, _, var_x, var_w = moments(t)
    sd_x = np.sqrt(np.clip(var_x, 0.0, None))
    sd_w = np.sqrt(np.clip(var_w, 0.0, None))
    assert float(np.min(var_x)) > -2e-12
    assert abs(float(var_x[0])) < 2e-12

    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.3), sharex=True)
    sd_band(axes[0], t, J, sd_x, style_rc.BLUE, r"$J(t)$")
    axes[0].set_ylabel("intracellular units")
    axes[0].set_ylim(0.0, 12.4)
    axes[0].legend(loc="upper right")
    axes[0].text(0.04, 0.92, r"(a)", transform=axes[0].transAxes)

    sd_band(axes[1], t, V, sd_w, style_rc.VERMILLION, r"$V(t)$")
    axes[1].set_ylabel("released units")
    axes[1].set_ylim(0.0, 32.0)
    axes[1].legend(loc="center right")
    axes[1].text(0.04, 0.92, r"(b)", transform=axes[1].transAxes)

    for ax in axes:
        ax.set_xlim(0.0, 20.0)
        ax.set_xlabel(r"$t$")
        style_rc.tidy(ax)

    fig.tight_layout(w_pad=1.6)
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)
    print(f"wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
