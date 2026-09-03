#!/usr/bin/env python3
"""Generate N3.2: the algebraic I-economy for J, V, and K."""

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
PDF_PATH = CHAPTER_DIR / "figures/N3_2_I_economy.pdf"
PNG_PATH = WORKDIR / "preview.png"

LAMBDA = 1.0
MU = 0.2
DELTA = 0.05


def roots(lam: float, mu: float, delta: float) -> tuple[float, float]:
    eta = (lam + mu + delta) / (2.0 * lam)
    radical = np.sqrt(eta**2 - mu / lam)
    return eta + radical, eta - radical


def moments_from_I(
    I: np.ndarray | float,
    lam: float = LAMBDA,
    mu: float = MU,
    delta: float = DELTA,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Evaluate the three chapter moments as algebraic functions of I."""
    a, b = roots(lam, mu, delta)
    values = np.asarray(I, dtype=float)
    J = -(lam / delta) * (values - a) * (values - b)
    V = (1.0 - values) * (1.0 + (lam / delta) * (1.0 - values))
    K = (1.0 + (2.0 * lam / delta) * (1.0 - values)) * J
    return J, V, K


def run_asserts() -> dict[str, float]:
    """Check endpoints and the monotone/one-turn path structure."""
    a, b = roots(LAMBDA, MU, DELTA)
    I_path = np.linspace(1.0, b, 5001)
    J, V, K = moments_from_I(I_path)
    v_inf = (1.0 - b) * (1.0 + (LAMBDA / DELTA) * (1.0 - b))

    assert a > 1.0 > b > 0.0
    assert np.all(np.diff(I_path) < 0.0)
    assert np.all(np.isfinite([J, V, K]))
    assert abs(float(J[0]) - 1.0) < 2e-13
    assert abs(float(V[0])) < 2e-13
    assert abs(float(K[0]) - 1.0) < 2e-13
    assert abs(float(J[-1])) < 2e-13
    assert abs(float(K[-1])) < 2e-13
    assert abs(float(V[-1]) - v_inf) < 2e-13
    assert np.all(np.diff(V) >= -2e-12)

    for curve in (J, K):
        peak = int(np.argmax(curve))
        assert 0 < peak < curve.size - 1
        assert np.all(np.diff(curve[: peak + 1]) >= -2e-10)
        assert np.all(np.diff(curve[peak:]) <= 2e-10)

    return {
        "a": a,
        "b": b,
        "J_at_I_1": float(J[0]),
        "V_at_I_1": float(V[0]),
        "J_at_I_b": float(J[-1]),
        "V_at_I_b": float(V[-1]),
        "V_inf": v_inf,
        "K_max": float(np.max(K)),
    }


def make_figure() -> None:
    _, b = roots(LAMBDA, MU, DELTA)
    I = np.linspace(1.0, b, 2001)
    J, V, K = moments_from_I(I)
    v_inf = float(V[-1])

    fig, ax = plt.subplots(figsize=(7.25, 4.9))
    ax.plot(I, J, color="tab:blue", linewidth=2.3, label=r"mean load $J(I)$")
    ax.plot(
        I,
        V,
        color="tab:orange",
        linewidth=2.3,
        linestyle=(0, (6, 2.5)),
        label=r"mean release $V(I)$",
    )
    ax.plot(
        I,
        K,
        color="#6b4c9a",
        linewidth=2.3,
        linestyle=(0, (5, 2, 1.3, 2)),
        label=r"second moment $K(I)$",
    )

    # A symmetric-log ordinate retains the raw moment values while keeping the
    # lower-order J and V curves legible beneath the much larger K peak.
    ax.set_yscale("symlog", linthresh=1.0, linscale=0.9, base=10)
    ax.set_yticks([0.0, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0])
    ax.set_yticklabels(["0", "1", "2", "5", "10", "20", "50"])
    ax.set_xlim(1.0, b)
    ax.set_ylim(0.0, 95.0)
    ax.set_xlabel(r"non-catastrophe probability $I$ (decreases with time)")
    ax.set_ylabel("moment value (symlog scale)")
    ax.set_title("One probability coordinate carries all three moments")

    ax.scatter(
        [1.0, 1.0],
        [1.0, 0.0],
        s=34,
        facecolors="white",
        edgecolors=["tab:blue", "tab:orange"],
        linewidths=1.35,
        zorder=5,
        clip_on=False,
    )
    ax.scatter(
        [b, b],
        [0.0, v_inf],
        s=36,
        facecolors="white",
        edgecolors=["#6b4c9a", "tab:orange"],
        linewidths=1.35,
        zorder=5,
        clip_on=False,
    )

    ax.annotate(
        r"start: $I=1$" + "\n" + r"$J=K=1,\ V=0$",
        xy=(1.0, 1.0),
        xytext=(0.955, 3.0),
        arrowprops={"arrowstyle": "->", "color": "#555555", "lw": 0.8},
        fontsize=9,
        ha="left",
    )
    ax.annotate(
        rf"limit: $I=b={b:.3f}$" + "\n" + rf"$J=K=0,\ V_\infty={v_inf:.2f}$",
        xy=(b, v_inf),
        xytext=(b + 0.16, 27.0),
        arrowprops={"arrowstyle": "->", "color": "#555555", "lw": 0.8},
        fontsize=9,
        ha="right",
    )
    ax.annotate(
        "time increases",
        xy=(0.66, 0.935),
        xytext=(0.34, 0.935),
        xycoords="axes fraction",
        textcoords="axes fraction",
        ha="center",
        va="center",
        fontsize=9,
        color="#444444",
        arrowprops={"arrowstyle": "-|>", "color": "#444444", "lw": 0.9},
    )
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.14),
        ncol=3,
        borderaxespad=0.0,
    )

    fig.tight_layout(rect=(0.0, 0.06, 1.0, 1.0))
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)


if __name__ == "__main__":
    diagnostics = run_asserts()
    make_figure()
    for name, value in diagnostics.items():
        print(f"{name}={value:.12g}")
    print(f"wrote {PDF_PATH}")
    print(f"wrote {PNG_PATH}")
