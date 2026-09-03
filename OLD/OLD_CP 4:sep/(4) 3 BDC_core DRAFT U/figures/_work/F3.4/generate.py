#!/usr/bin/env python3
"""Generate F3.4: two closed-form conditional-mean convergence panels."""

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
PDF_PATH = CHAPTER_DIR / "figures/F3_4_conditional_mean.pdf"
PNG_PATH = WORKDIR / "preview.png"


def roots(lam: float, mu: float, delta: float) -> tuple[float, float]:
    eta = (lam + mu + delta) / (2.0 * lam)
    radical = np.sqrt(eta**2 - mu / lam)
    return eta + radical, eta - radical


def quantities(
    t: np.ndarray | float, lam: float, mu: float, delta: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, float, float]:
    """Evaluate I, I_fix, J, and V using the brief's closed forms."""
    a, b = roots(lam, mu, delta)
    A = a - 1.0
    B = 1.0 - b
    w = np.exp(lam * (a - b) * np.asarray(t))
    I = (a * B + b * A * w) / (B + A * w)
    D = a * b * (w - 1.0) / (a * w - b)
    I_fix = I - D
    J = (a - b) ** 2 * w / (B + A * w) ** 2
    V = (1.0 - I) * (1.0 + (lam / delta) * (1.0 - I))
    return I, I_fix, J, V, a, b


def run_asserts() -> dict[str, float]:
    """Check the three late-time statements specified in the brief."""
    t_late = np.array([15.0])

    I_a, I_fix_a, J_a, V_a, a_a, b_a = quantities(t_late, 1.0, 0.0, 0.1)
    ratio_a = float((J_a / I_a)[0])
    V_a_late = float(V_a[0])
    target_a = 1.0 + 1.0 / 0.1
    assert abs(b_a) < 1e-14
    assert np.allclose(I_a, I_fix_a)
    assert abs(ratio_a - target_a) < 0.05
    assert abs(V_a_late - target_a) < 0.05

    I_b, I_fix_b, J_b, _, a_b, b_b = quantities(t_late, 1.0, 0.2, 0.05)
    ratio_fix_b = float((J_b / I_fix_b)[0])
    ratio_I_b = float((J_b / I_b)[0])
    target_b = a_b / (a_b - 1.0)
    assert a_b > 1.0 > b_b > 0.0
    assert abs(ratio_fix_b - target_b) < 0.05
    assert ratio_I_b < 0.1

    # Guard the displayed ranges against poles, negative probabilities, or NaNs.
    t = np.linspace(0.0, 15.0, 2001)
    for params in ((1.0, 0.0, 0.1), (1.0, 0.2, 0.05)):
        I, I_fix, J, V, _, _ = quantities(t, *params)
        assert np.all(np.isfinite([I, I_fix, J, V]))
        assert np.all(I > 0.0)
        assert np.all(I_fix > 0.0)
        assert np.all(J > 0.0)
        assert np.all(V >= -1e-14)

    return {
        "panel_a_J_over_I_t15": ratio_a,
        "panel_a_V_t15": V_a_late,
        "panel_a_target": target_a,
        "panel_b_J_over_Ifix_t15": ratio_fix_b,
        "panel_b_J_over_I_t15": ratio_I_b,
        "panel_b_target": target_b,
    }


def make_figure() -> None:
    t = np.linspace(0.0, 15.0, 1001)
    fig, axes = plt.subplots(1, 2, figsize=(10.0, 4.25))

    I, _, J, V, _, _ = quantities(t, 1.0, 0.0, 0.1)
    target_a = 11.0
    axes[0].plot(t, J / I, color="tab:blue", label=r"$J(t)/I(t)$")
    axes[0].plot(t, V, color="tab:orange", label=r"$V(t)$")
    style_rc.asymptote_hline(
        axes[0], target_a, label=r"$1+\lambda/\delta=11$"
    )
    axes[0].set_title(r"(a) $\mu=0$, $\lambda=1$, $\delta=0.1$")
    axes[0].set(xlim=(0.0, 15.0), ylim=(0.0, 12.0), xlabel=r"$t$", ylabel="Mean value")
    axes[0].set_xticks(np.arange(0.0, 15.1, 3.0))
    axes[0].legend(loc="lower right")

    I, I_fix, J, _, a, _ = quantities(t, 1.0, 0.2, 0.05)
    target_b = a / (a - 1.0)
    axes[1].plot(t, J / I_fix, color="tab:blue", label=r"$J(t)/I_{\mathrm{fix}}(t)$")
    axes[1].plot(t, J / I, color="tab:orange", label=r"$J(t)/I(t)$")
    style_rc.asymptote_hline(
        axes[1], target_b, label=rf"$a/(a-1)={target_b:.2f}$"
    )
    axes[1].axhline(
        0.0,
        color=style_rc.GRAY_REF,
        linestyle="--",
        linewidth=1.0,
        zorder=3,
        clip_on=False,
    )
    axes[1].set_title(r"(b) $\mu=0.2$, $\lambda=1$, $\delta=0.05$")
    axes[1].set(xlim=(0.0, 15.0), ylim=(0.0, 19.0), xlabel=r"$t$")
    axes[1].set_xticks(np.arange(0.0, 15.1, 3.0))
    axes[1].legend(loc="center right")

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

