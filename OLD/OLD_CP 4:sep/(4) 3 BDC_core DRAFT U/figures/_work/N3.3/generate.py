#!/usr/bin/env python3
"""Generate N3.3: multi-founder non-fixation probabilities.

The figure is analytic and deterministic.  It compares the branching-property
formula I(t)^k-D(t)^k with the tempting but false power [I(t)-D(t)]^k.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(
    0,
    "/Users/adamaldridge/Desktop/Thesis content 🎓 /4 BDC additional and BMVR/Figures run/style",
)
import style_rc  # noqa: E402

style_rc.apply()

import matplotlib.pyplot as plt  # noqa: E402


HERE = Path(__file__).resolve().parent
CHAPTER = HERE.parents[2]
PDF_PATH = CHAPTER / "figures" / "N3_3_multi_founder_fixation.pdf"
PNG_PATH = HERE / "preview.png"

LAMBDA = 1.0
MU = 0.2
DELTA = 0.05
KS = (1, 2, 3, 5)


def roots(lam: float, mu: float, delta: float) -> tuple[float, float]:
    eta = (lam + mu + delta) / (2.0 * lam)
    spread = np.sqrt(eta**2 - mu / lam)
    return float(eta + spread), float(eta - spread)


def single_founder_probabilities(t: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return I(t) and D(t) in forms stable at late time."""
    a, b = roots(LAMBDA, MU, DELTA)
    A, B = a - 1.0, 1.0 - b
    decay = np.exp(-LAMBDA * (a - b) * t)
    I = (a * B * decay + b * A) / (B * decay + A)
    D = a * b * (1.0 - decay) / (a - b * decay)
    return I, D


def validate(t: np.ndarray, I: np.ndarray, D: np.ndarray) -> dict[str, float]:
    Ifix = I - D
    true_k1 = I**1 - D**1
    false_k1 = Ifix**1
    assert np.allclose(true_k1, Ifix, atol=1e-13)
    assert np.allclose(false_k1, Ifix, atol=1e-13)

    all_curves = [I, D, Ifix]
    for k in KS:
        all_curves.extend((I**k, D**k, I**k - D**k, Ifix**k))
    for curve in all_curves:
        assert np.all(np.isfinite(curve))
        assert float(curve.min()) >= -1e-12
        assert float(curve.max()) <= 1.0 + 1e-12

    true_k2 = I**2 - D**2
    false_k2 = Ifix**2
    gap = true_k2 - false_k2
    gap_index = int(np.argmax(gap))
    assert float(gap[gap_index]) > 1e-2
    assert np.all(gap >= -1e-13)
    assert np.isclose(I[0], 1.0, atol=1e-13)
    assert np.isclose(D[0], 0.0, atol=1e-13)
    return {
        "max_gap": float(gap[gap_index]),
        "gap_time": float(t[gap_index]),
        "true_at_gap": float(true_k2[gap_index]),
        "false_at_gap": float(false_k2[gap_index]),
    }


def build() -> dict[str, float]:
    t = np.linspace(0.0, 15.0, 2001)
    I, D = single_founder_probabilities(t)
    Ifix = I - D
    checks = validate(t, I, D)

    colours = {
        1: "#1f77b4",
        2: "#e67e22",
        3: "#6b4c9a",
        5: "#8b1e1e",
    }
    styles = {1: "-", 2: "--", 3: "-.", 5: (0, (1.2, 1.5))}

    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.55), sharex=True, sharey=True)
    ax_a, ax_b = axes

    for k in KS:
        curve = I**k - D**k
        ax_a.plot(
            t,
            curve,
            color=colours[k],
            linestyle=styles[k],
            linewidth=2.25,
            label=rf"$k={k}$",
        )
    ax_a.set_title("(a) Founder number reshapes the non-fixation window", loc="left")
    ax_a.set_xlabel(r"time $t$")
    ax_a.set_ylabel("non-fixation probability")
    ax_a.legend(title="founders", loc="upper right", ncols=2)
    ax_a.text(
        0.97,
        0.08,
        r"$I_{\rm fix}^{(k)}=I^k-D^k$",
        transform=ax_a.transAxes,
        ha="right",
        va="bottom",
        color="#444444",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="#cccccc", alpha=0.92),
    )

    true_k2 = I**2 - D**2
    false_k2 = Ifix**2
    gap = true_k2 - false_k2
    gap_index = int(np.argmax(gap))
    ax_b.fill_between(
        t,
        false_k2,
        true_k2,
        color="#6b4c9a",
        alpha=0.15,
        label="omitted mixed fates",
        zorder=1,
    )
    ax_b.plot(
        t,
        true_k2,
        color="#1f77b4",
        linewidth=2.5,
        label=r"true: $I^2-D^2$",
        zorder=3,
    )
    ax_b.plot(
        t,
        false_k2,
        color="#e67e22",
        linestyle="--",
        linewidth=2.3,
        label=r"naive: $(I-D)^2$",
        zorder=3,
    )
    ax_b.plot(
        t[gap_index],
        true_k2[gap_index],
        marker="o",
        markersize=6.5,
        markerfacecolor="white",
        markeredgecolor="#1f77b4",
        markeredgewidth=1.7,
        zorder=4,
    )
    ax_b.annotate(
        rf"largest gap $={gap[gap_index]:.2f}$" "\n" "one lineage may die while another remains productive",
        xy=(t[gap_index], 0.5 * (true_k2[gap_index] + false_k2[gap_index])),
        xytext=(4.0, 0.44),
        arrowprops=dict(arrowstyle="->", color="#6b4c9a", linewidth=1.1),
        color="#5a3f82",
        fontsize=9,
        ha="left",
        va="center",
    )
    ax_b.set_title("(b) The naive power misses mixed lineage fates", loc="left")
    ax_b.set_xlabel(r"time $t$")
    ax_b.legend(loc="upper right")

    for ax in axes:
        ax.set_xlim(0.0, 15.0)
        ax.set_ylim(0.0, 1.035)
        ax.set_xticks(np.arange(0.0, 15.1, 3.0))
        ax.set_yticks(np.linspace(0.0, 1.0, 6))

    fig.tight_layout(w_pad=2.2)
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)
    return checks


if __name__ == "__main__":
    summary = build()
    print(
        "N3.3 asserts passed: "
        f"max true-naive gap={summary['max_gap']:.6f} "
        f"at t={summary['gap_time']:.4f}"
    )

