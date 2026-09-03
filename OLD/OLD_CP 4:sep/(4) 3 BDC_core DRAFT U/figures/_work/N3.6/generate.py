#!/usr/bin/env python3
"""Generate N3.6: the parametric load-release trajectory (J(t), V(t))."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

STYLE_DIR = Path(
    "/Users/adamaldridge/Desktop/Thesis content 🎓 /4 BDC additional and BMVR/Figures run/style"
)
sys.path.insert(0, str(STYLE_DIR))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402


WORKDIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORKDIR.parents[2]
PDF_PATH = CHAPTER_DIR / "figures/N3_6_JV_parametric.pdf"
PNG_PATH = WORKDIR / "preview.png"

LAMBDA = 1.0
MU = 0.2
DELTA = 0.05
MARKER_TIMES = np.array([0.0, 1.0, 2.0, 5.0, 10.0])


def roots(lam: float, mu: float, delta: float) -> tuple[float, float]:
    eta = (lam + mu + delta) / (2.0 * lam)
    radical = np.sqrt(eta**2 - mu / lam)
    return eta + radical, eta - radical


def means(
    t: np.ndarray | float,
    lam: float = LAMBDA,
    mu: float = MU,
    delta: float = DELTA,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Evaluate I, J, and V with a stable late-time parametrisation."""
    a, b = roots(lam, mu, delta)
    A = a - 1.0
    B = 1.0 - b
    theta = lam * (a - b)
    z = np.exp(-theta * np.asarray(t, dtype=float))
    I = (a * B * z + b * A) / (B * z + A)
    J = (a - b) ** 2 * z / (B * z + A) ** 2
    V = (1.0 - I) * (1.0 + (lam / delta) * (1.0 - I))
    return I, J, V


def run_asserts() -> dict[str, float]:
    """Check the exact start, asymptotic end, and monotone release coordinate."""
    _, b = roots(LAMBDA, MU, DELTA)
    t = np.linspace(0.0, 25.0, 5001)
    _, J, V = means(t)
    v_inf = (1.0 - b) * (1.0 + (LAMBDA / DELTA) * (1.0 - b))
    _, J_late, V_late = means(100.0)

    assert abs(float(J[0]) - 1.0) < 2e-13
    assert abs(float(V[0])) < 2e-13
    assert np.all(np.isfinite([J, V]))
    assert np.all(np.diff(V) >= -2e-12)
    assert int(np.argmax(J)) not in (0, J.size - 1)
    assert float(J_late) < 1e-30
    assert abs(float(V_late) - v_inf) < 1e-11

    return {
        "J_start": float(J[0]),
        "V_start": float(V[0]),
        "J_peak": float(np.max(J)),
        "t_at_J_peak": float(t[int(np.argmax(J))]),
        "J_late": float(J_late),
        "V_late": float(V_late),
        "V_inf": v_inf,
    }


def make_figure() -> None:
    _, b = roots(LAMBDA, MU, DELTA)
    t = np.linspace(0.0, 20.0, 2401)
    _, J, V = means(t)
    v_inf = (1.0 - b) * (1.0 + (LAMBDA / DELTA) * (1.0 - b))

    # Append the analytic endpoint so the visible trajectory lands exactly at
    # (0, V_inf), rather than at a merely large finite time.
    J_curve = np.append(J, 0.0)
    V_curve = np.append(V, v_inf)
    _, J_mark, V_mark = means(MARKER_TIMES)

    fig, ax = plt.subplots(figsize=(6.75, 5.05))
    ax.plot(J_curve, V_curve, color="tab:blue", linewidth=2.45, zorder=2)
    ax.scatter(
        J_mark,
        V_mark,
        s=40,
        facecolors="white",
        edgecolors="tab:blue",
        linewidths=1.45,
        zorder=4,
    )
    ax.scatter(
        [0.0],
        [v_inf],
        s=46,
        marker="o",
        color="tab:orange",
        edgecolor="white",
        linewidth=0.8,
        zorder=5,
        clip_on=False,
    )

    label_offsets = {
        0.0: (-6, 11),
        1.0: (8, 14),
        2.0: (8, -2),
        5.0: (9, 5),
        10.0: (12, -22),
    }
    for marker_t, x, y in zip(MARKER_TIMES, J_mark, V_mark, strict=True):
        ax.annotate(
            rf"$t={marker_t:g}$",
            xy=(float(x), float(y)),
            xytext=label_offsets[float(marker_t)],
            textcoords="offset points",
            fontsize=9,
            ha="left",
            va="center",
        )
    ax.annotate(
        r"$t\to\infty$",
        xy=(0.0, v_inf),
        xytext=(15, 9),
        textcoords="offset points",
        fontsize=9,
        color="tab:orange",
        ha="left",
        va="bottom",
    )

    _, j_from, v_from = means(3.45)
    _, j_to, v_to = means(4.15)
    ax.annotate(
        "increasing time",
        xy=(float(j_to), float(v_to)),
        xytext=(3.72, 8.75),
        arrowprops={"arrowstyle": "-|>", "color": "#6b4c9a", "lw": 1.0},
        color="#6b4c9a",
        fontsize=9,
        ha="right",
    )
    ax.axhline(
        v_inf,
        color=style_rc.GRAY_REF,
        linestyle=(0, (4, 3)),
        linewidth=1.0,
        zorder=0,
    )
    ax.text(
        3.98,
        v_inf + 0.18,
        rf"$V_\infty={v_inf:.2f}$",
        color="#666666",
        fontsize=9,
        ha="right",
        va="bottom",
    )

    ax.set_xlim(-0.12, 4.08)
    ax.set_ylim(-0.55, 15.15)
    ax.set_xlabel(r"mean intracellular load $J(t)$")
    ax.set_ylabel(r"mean released count $V(t)$")
    ax.set_title("Load rises and falls while release accumulates")

    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)


if __name__ == "__main__":
    diagnostics = run_asserts()
    make_figure()
    for name, value in diagnostics.items():
        print(f"{name}={value:.12g}")
    print(f"wrote {PDF_PATH}")
    print(f"wrote {PNG_PATH}")
