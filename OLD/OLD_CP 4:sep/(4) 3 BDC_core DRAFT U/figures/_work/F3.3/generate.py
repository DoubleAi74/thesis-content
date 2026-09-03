#!/usr/bin/env python3
"""Generate F3.3: the three fixation functions from their closed forms."""

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
PDF_PATH = CHAPTER_DIR / "figures/F3_3_fixation.pdf"
PNG_PATH = WORKDIR / "preview.png"

LAMBDA = 1.0
MU = 0.2
DELTA = 0.05


def roots(lam: float, mu: float, delta: float) -> tuple[float, float]:
    """Return the ordered roots a > 1 > b of the BDC quadratic."""
    eta = (lam + mu + delta) / (2.0 * lam)
    radical = np.sqrt(eta**2 - mu / lam)
    return eta + radical, eta - radical


def quantities(
    t: np.ndarray | float, lam: float, mu: float, delta: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float, float]:
    """Evaluate I, D and I_fix using the closed forms in the brief."""
    a, b = roots(lam, mu, delta)
    A = a - 1.0
    B = 1.0 - b
    w = np.exp(lam * (a - b) * np.asarray(t))
    I = (a * B + b * A * w) / (B + A * w)
    D = a * b * (w - 1.0) / (a * w - b)
    I_fix = (a - b) ** 2 * w / ((B + A * w) * (a * w - b))
    return I, D, I_fix, a, b


def run_asserts() -> dict[str, float]:
    """Check identities, limiting values, positivity, and the initial slope."""
    t = np.linspace(0.0, 15.0, 2001)
    I, D, I_fix, a, b = quantities(t, LAMBDA, MU, DELTA)
    I_late, D_late, I_fix_late, _, _ = quantities(
        np.array([100.0]), LAMBDA, MU, DELTA
    )

    assert a > 1.0 > b > 0.0
    assert np.allclose(I - D, I_fix, atol=2e-14, rtol=2e-14)
    assert abs(float(I_late[0]) - b) < 1e-3
    assert abs(float(D_late[0]) - b) < 1e-3
    assert float(I_fix_late[0]) < 1e-6
    assert np.all(I_fix >= -1e-14)
    assert np.all(np.diff(I) <= 1e-12)
    assert np.all(np.diff(D) >= -1e-12)

    h = 1e-6
    fix_plus = quantities(h, LAMBDA, MU, DELTA)[2]
    fix_minus = quantities(-h, LAMBDA, MU, DELTA)[2]
    slope = float((fix_plus - fix_minus) / (2.0 * h))
    assert abs(slope + 0.25) < 1e-3

    return {
        "a": a,
        "b": b,
        "I_late": float(I_late[0]),
        "D_late": float(D_late[0]),
        "I_fix_late": float(I_fix_late[0]),
        "I_fix_slope_0": slope,
    }


def make_figure() -> None:
    t = np.linspace(0.0, 15.0, 1001)
    I, D, I_fix, _, b = quantities(t, LAMBDA, MU, DELTA)

    fig, ax = plt.subplots(figsize=(6.7, 4.2))
    ax.plot(t, I, color="tab:blue", label=r"$I(t)$")
    ax.plot(t, D, color="tab:orange", label=r"$D(t)$")
    ax.plot(t, I_fix, color="tab:green", label=r"$I_{\mathrm{fix}}(t)$")
    style_rc.asymptote_hline(ax, b, label=rf"$b={b:.3f}$")
    ax.axhline(
        0.0,
        color=style_rc.GRAY_REF,
        linestyle="--",
        linewidth=1.0,
        zorder=3,
        clip_on=False,
    )
    arrow_t = 0.65
    arrow_y = float(quantities(arrow_t, LAMBDA, MU, DELTA)[2])
    ax.annotate(
        r"$I_{\mathrm{fix}}'(0)=-(\mu+\delta)=-0.25$",
        xy=(arrow_t, arrow_y),
        xytext=(2.05, 0.83),
        arrowprops={"arrowstyle": "->", "color": "black", "lw": 0.8},
        fontsize=9,
        ha="left",
    )
    ax.set(xlim=(0.0, 15.0), ylim=(0.0, 1.0), xlabel=r"$t$", ylabel="Probability")
    ax.set_xticks(np.arange(0.0, 15.1, 3.0))
    ax.legend(loc="upper right")
    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)


if __name__ == "__main__":
    diagnostics = run_asserts()
    make_figure()
    for name, value in diagnostics.items():
        print(f"{name}={value:.12g}")
    print(f"wrote {PDF_PATH}")
    print(f"wrote {PNG_PATH}")

