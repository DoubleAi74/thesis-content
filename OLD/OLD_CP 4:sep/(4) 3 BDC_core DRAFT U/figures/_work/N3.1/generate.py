#!/usr/bin/env python3
"""Generate N3.1: mean and one-standard-deviation envelopes for X_t and W_t."""

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
PDF_PATH = CHAPTER_DIR / "figures/N3_1_mean_sd_XW.pdf"
PNG_PATH = WORKDIR / "preview.png"

LAMBDA = 1.0
MU = 0.2
DELTA = 0.05


def roots(lam: float, mu: float, delta: float) -> tuple[float, float]:
    """Return the ordered roots a > 1 > b of the BDC quadratic."""
    eta = (lam + mu + delta) / (2.0 * lam)
    radical = np.sqrt(eta**2 - mu / lam)
    return eta + radical, eta - radical


def moments(
    t: np.ndarray | float,
    lam: float = LAMBDA,
    mu: float = MU,
    delta: float = DELTA,
) -> tuple[np.ndarray, ...]:
    """Evaluate I, J, V, K, Var(X_t), and Var(W_t) from the chapter forms."""
    a, b = roots(lam, mu, delta)
    A = a - 1.0
    B = 1.0 - b
    theta = lam * (a - b)

    # The exp(-theta*t) form is algebraically identical to the chapter form
    # and remains stable at the late-time assertion point.
    z = np.exp(-theta * np.asarray(t, dtype=float))
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


def run_asserts() -> dict[str, float]:
    """Check non-negativity, finiteness, limits, and the stated noise crossover."""
    t = np.linspace(0.0, 20.0, 4001)
    I, J, V, K, var_x, var_w = moments(t)
    a, b = roots(LAMBDA, MU, DELTA)

    arrays = (I, J, V, K, var_x, var_w)
    assert all(np.all(np.isfinite(values)) for values in arrays)
    assert float(np.min(var_x)) > -2e-12
    assert float(np.min(var_w)) > -2e-10
    assert abs(float(var_x[0])) < 2e-12
    assert abs(float(var_w[0])) < 2e-12
    assert np.all(np.diff(V) >= -2e-12)

    I_late, J_late, V_late, K_late, _, var_w_late = moments(100.0)
    v_inf = (1.0 - b) * (1.0 + (LAMBDA / DELTA) * (1.0 - b))
    assert abs(float(I_late) - b) < 1e-12
    assert float(J_late) < 1e-30
    assert float(K_late) < 1e-30
    assert abs(float(V_late) - v_inf) < 1e-11

    sd_x = np.sqrt(np.clip(var_x, 0.0, None))
    sd_w = np.sqrt(np.clip(var_w, 0.0, None))
    mid = (t >= 0.5) & (t <= 10.0)
    crossover_indices = np.flatnonzero(mid & (sd_x > J))
    assert crossover_indices.size > 0
    cross_index = int(crossover_indices[0])
    assert float(np.sqrt(max(float(var_w_late), 0.0))) > v_inf

    return {
        "a": a,
        "b": b,
        "min_var_X": float(np.min(var_x)),
        "min_var_W": float(np.min(var_w)),
        "SD_X_exceeds_J_at_t": float(t[cross_index]),
        "V_inf": v_inf,
        "SD_W_inf": float(np.sqrt(max(float(var_w_late), 0.0))),
    }


def sd_band(
    ax: plt.Axes,
    t: np.ndarray,
    mean: np.ndarray,
    sd: np.ndarray,
    color: str,
    mean_label: str,
) -> None:
    """Draw a count-respecting mean +/- SD envelope and its upper boundary."""
    lower = np.maximum(0.0, mean - sd)
    upper = mean + sd
    ax.fill_between(
        t,
        lower,
        upper,
        color=color,
        alpha=0.14,
        linewidth=0.0,
        label=r"mean $\pm$ one SD",
        zorder=1,
    )
    ax.plot(t, upper, color=color, linestyle="--", linewidth=1.35, alpha=0.82)
    ax.plot(t, lower, color=color, linestyle="--", linewidth=1.15, alpha=0.55)
    ax.plot(t, mean, color=color, linewidth=2.35, label=mean_label, zorder=3)


def make_figure() -> None:
    t = np.linspace(0.0, 20.0, 2001)
    _, J, V, _, var_x, var_w = moments(t)
    sd_x = np.sqrt(np.clip(var_x, 0.0, None))
    sd_w = np.sqrt(np.clip(var_w, 0.0, None))
    _, b = roots(LAMBDA, MU, DELTA)
    v_inf = (1.0 - b) * (1.0 + (LAMBDA / DELTA) * (1.0 - b))

    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.25), sharex=True)

    sd_band(
        axes[0],
        t,
        J,
        sd_x,
        "tab:blue",
        r"mean $J(t)=\mathbb{E}[X_t]$",
    )
    cross = int(np.flatnonzero((t >= 0.5) & (sd_x > J))[0])
    axes[0].scatter(
        [t[cross]],
        [J[cross]],
        s=26,
        facecolors="white",
        edgecolors="#6b4c9a",
        linewidths=1.3,
        zorder=5,
    )
    axes[0].annotate(
        rf"$\mathrm{{SD}}(X_t)>J(t)$ from $t\approx {t[cross]:.1f}$",
        xy=(t[cross], J[cross]),
        xytext=(4.2, 10.4),
        arrowprops={"arrowstyle": "->", "color": "#6b4c9a", "lw": 0.9},
        color="#6b4c9a",
        fontsize=9,
    )
    axes[0].set_title("(a) Load: dispersion overtakes the mean")
    axes[0].set_ylabel("intracellular units")
    axes[0].set_ylim(0.0, 12.4)
    axes[0].legend(loc="upper right")

    sd_band(
        axes[1],
        t,
        V,
        sd_w,
        "tab:orange",
        r"mean $V(t)=\mathbb{E}[W_t]$",
    )
    axes[1].axhline(
        v_inf,
        color=style_rc.GRAY_REF,
        linestyle=(0, (4, 3)),
        linewidth=1.0,
        zorder=0,
    )
    axes[1].text(
        19.5,
        v_inf + 0.5,
        rf"$V_\infty={v_inf:.2f}$",
        ha="right",
        va="bottom",
        color="#666666",
        fontsize=9,
    )
    axes[1].annotate(
        rf"late SD $\approx {sd_w[-1]:.1f}$"
        + "\n"
        + "mixture of zero release and large bursts",
        xy=(15.8, V[-1] + sd_w[-1]),
        xytext=(7.0, 25.6),
        arrowprops={"arrowstyle": "->", "color": "#6b4c9a", "lw": 0.9},
        color="#6b4c9a",
        fontsize=8.8,
        ha="left",
    )
    axes[1].set_title("(b) Release: the late mixture stays broad")
    axes[1].set_ylabel("released units")
    axes[1].set_ylim(0.0, 32.0)
    axes[1].legend(loc="center right")

    for ax in axes:
        ax.set_xlim(0.0, 20.0)
        ax.set_xticks(np.arange(0.0, 20.1, 4.0))
        ax.set_xlabel(r"time $t$")

    fig.tight_layout(w_pad=2.2)
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)


if __name__ == "__main__":
    diagnostics = run_asserts()
    make_figure()
    for name, value in diagnostics.items():
        print(f"{name}={value:.12g}")
    print(f"wrote {PDF_PATH}")
    print(f"wrote {PNG_PATH}")
