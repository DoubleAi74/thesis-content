#!/usr/bin/env python3
"""Conditional mean loads: no-death check and the working point."""

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
PDF_PATH = WORKDIR.parents[2] / "figures/F4_conditional_mean.pdf"
PNG_PATH = WORKDIR / "preview.png"


def roots(lam, mu, delta):
    eta = (lam + mu + delta) / (2.0 * lam)
    radical = np.sqrt(eta**2 - mu / lam)
    return eta + radical, eta - radical


def quantities(t, lam, mu, delta):
    a, b = roots(lam, mu, delta)
    A, B = a - 1.0, 1.0 - b
    w = np.exp(lam * (a - b) * np.asarray(t))
    I = (a * B + b * A * w) / (B + A * w)
    D = a * b * (w - 1.0) / (a * w - b)
    I_fix = I - D
    J = (a - b) ** 2 * w / (B + A * w) ** 2
    V = (1.0 - I) * (1.0 + (lam / delta) * (1.0 - I))
    return I, I_fix, J, V, a, b


def main() -> None:
    t = np.linspace(0.0, 15.0, 1001)
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.3))

    I, _, J, V, _, _ = quantities(t, 1.0, 0.0, 0.1)
    axes[0].plot(t, J / I, color=style_rc.BLUE, label=r"$J(t)/I(t)$")
    axes[0].plot(t, V, color=style_rc.VERMILLION, label=r"$V(t)$")
    style_rc.asymptote_hline(axes[0], 11.0, label=r"$1+\lambda/\delta=11$")
    axes[0].set_title(r"$\mu=0$, $\lambda=1$, $\delta=0.1$")
    axes[0].set(xlim=(0.0, 15.0), ylim=(0.0, 12.0), xlabel=r"$t$", ylabel="Mean value")
    axes[0].legend(loc="lower right")
    axes[0].text(0.04, 0.92, r"(a)", transform=axes[0].transAxes)

    I, I_fix, J, _, a, _ = quantities(t, 1.0, 0.2, 0.05)
    target_b = a / (a - 1.0)
    axes[1].plot(t, J / I_fix, color=style_rc.BLUE, label=r"$J(t)/I_{\mathrm{fix}}(t)$")
    axes[1].plot(t, J / I, color=style_rc.VERMILLION, label=r"$J(t)/I(t)$")
    style_rc.asymptote_hline(axes[1], target_b, label=rf"$a/(a-1)={target_b:.2f}$")
    axes[1].set_title(r"$\lambda=1$, $\mu=0.2$, $\delta=0.05$")
    axes[1].set(xlim=(0.0, 15.0), ylim=(0.0, 19.0), xlabel=r"$t$")
    axes[1].legend(loc="center right")
    axes[1].text(0.04, 0.92, r"(b)", transform=axes[1].transAxes)

    for ax in axes:
        style_rc.tidy(ax)

    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)
    print(f"wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
