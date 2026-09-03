#!/usr/bin/env python3
"""Mean load and release: time courses and the parametric (J, V) path."""

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
PDF_PATH = WORKDIR.parents[2] / "figures/F4_JV_parametric.pdf"
PNG_PATH = WORKDIR / "preview.png"

LAMBDA, MU, DELTA = 1.0, 0.2, 0.05
MARKER_TIMES = np.array([0.0, 1.0, 2.0, 5.0, 10.0])


def roots(lam, mu, delta):
    eta = (lam + mu + delta) / (2.0 * lam)
    radical = np.sqrt(eta**2 - mu / lam)
    return eta + radical, eta - radical


def means(t, lam=LAMBDA, mu=MU, delta=DELTA):
    a, b = roots(lam, mu, delta)
    A, B = a - 1.0, 1.0 - b
    z = np.exp(-lam * (a - b) * np.asarray(t, dtype=float))
    I = (a * B * z + b * A) / (B * z + A)
    J = (a - b) ** 2 * z / (B * z + A) ** 2
    V = (1.0 - I) * (1.0 + (lam / delta) * (1.0 - I))
    return I, J, V


def main() -> None:
    _, b = roots(LAMBDA, MU, DELTA)
    t = np.linspace(0.0, 25.0, 3001)
    _, J, V = means(t)
    v_inf = (1.0 - b) * (1.0 + (LAMBDA / DELTA) * (1.0 - b))
    _, J_mark, V_mark = means(MARKER_TIMES)
    assert abs(float(J[0]) - 1.0) < 1e-12
    assert abs(float(V[0])) < 1e-12

    fig, (ax_time, ax_phase) = plt.subplots(1, 2, figsize=(7.4, 3.3))
    ax_time.plot(t, J, color=style_rc.BLUE, linewidth=1.5, label=r"$J(t)$")
    ax_time.plot(t, V, color=style_rc.VERMILLION, linewidth=1.5, label=r"$V(t)$")
    style_rc.asymptote_hline(ax_time, v_inf, label=rf"$V_\infty={v_inf:.2f}$")
    ax_time.set_xlim(0.0, 25.0)
    ax_time.set_ylim(0.0, 15.3)
    ax_time.set_xlabel(r"$t$")
    ax_time.set_ylabel("expected count")
    ax_time.legend(loc="center right")
    ax_time.text(0.04, 0.92, r"(a)", transform=ax_time.transAxes)
    style_rc.tidy(ax_time)

    ax_phase.plot(np.append(J, 0.0), np.append(V, v_inf),
                  color=style_rc.INK, linewidth=1.5, zorder=2)
    ax_phase.scatter(J_mark, V_mark, s=22, facecolors="white",
                     edgecolors=style_rc.INK, linewidths=1.0, zorder=3)
    offsets = {0.0: (-6, 10), 1.0: (6, 8), 2.0: (6, -8), 5.0: (6, 6), 10.0: (8, -12)}
    for marker_t, x, y in zip(MARKER_TIMES, J_mark, V_mark, strict=True):
        ax_phase.annotate(
            rf"$t={marker_t:g}$", xy=(float(x), float(y)),
            xytext=offsets[float(marker_t)], textcoords="offset points",
            fontsize=7.5, ha="left", va="center",
        )
    ax_phase.set_xlim(-0.13, 4.08)
    ax_phase.set_ylim(0.0, 15.3)
    ax_phase.set_xlabel(r"$J(t)$")
    ax_phase.set_ylabel(r"$V(t)$")
    ax_phase.text(0.04, 0.92, r"(b)", transform=ax_phase.transAxes)
    style_rc.tidy(ax_phase)

    fig.tight_layout(w_pad=1.8)
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)
    print(f"V_inf={v_inf:.4f}; wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
