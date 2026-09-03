#!/usr/bin/env python3
"""Re-render F3.6: Gillespie paths for the BDC process.

The catastrophe state H is non-numeric.  In the X plot its transition is drawn
to the plotting baseline so that the terminal jump is visible, and the plot
annotation identifies that endpoint explicitly as H.  The trajectory ends at
the jump; it is not continued as though H were the count state zero.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np


STYLE_DIR = Path(
    "/Users/adamaldridge/Desktop/Thesis content 🎓 /4 BDC additional and BMVR/"
    "Figures run/style"
)
sys.path.insert(0, str(STYLE_DIR))
import style_rc  # noqa: E402

style_rc.apply()

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import MaxNLocator  # noqa: E402


LAMBDA = 1.0
MU = 0.0
DELTA = 0.1
X0 = 1
T_END = 20.0
N_PATHS = 100
SEED = 42

WORK_DIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORK_DIR.parents[2]
FIGURE_DIR = CHAPTER_DIR / "figures"
X_PDF = FIGURE_DIR / "F3_6_gillespie_X.pdf"
W_PDF = FIGURE_DIR / "F3_6_gillespie_W.pdf"
PREVIEW_PNG = WORK_DIR / "preview.png"


@dataclass(frozen=True)
class Trajectory:
    """One exact path, with numeric display coordinates kept explicit."""

    x_times: np.ndarray
    x_display: np.ndarray
    w_times: np.ndarray
    w_values: np.ndarray
    terminal: str
    catastrophe_time: float | None
    burst_size: int | None


def simulate_path(rng: np.random.Generator) -> Trajectory:
    """Simulate (X, W) by the direct Gillespie algorithm."""

    t = 0.0
    n = X0
    x_times = [0.0]
    x_values = [X0]
    catastrophe_time: float | None = None
    burst_size: int | None = None
    terminal = "continuing"

    while t < T_END and n > 0:
        total_rate = (LAMBDA + MU + DELTA) * n
        assert total_rate > 0.0
        event_time = t + rng.exponential(1.0 / total_rate)

        if event_time > T_END:
            x_times.append(T_END)
            x_values.append(n)
            break

        t = event_time
        draw = rng.random() * (LAMBDA + MU + DELTA)
        if draw < LAMBDA:
            n += 1
            x_times.append(t)
            x_values.append(n)
        elif draw < LAMBDA + MU:
            n -= 1
            x_times.append(t)
            x_values.append(n)
            if n == 0:
                terminal = "extinct"
                x_times.append(T_END)
                x_values.append(0)
        else:
            catastrophe_time = t
            burst_size = n
            terminal = "catastrophe"
            # H has no numeric count.  Zero is used only as a display baseline,
            # and the path terminates here rather than continuing at count zero.
            x_times.append(t)
            x_values.append(0)
            break

    if catastrophe_time is None:
        w_times = [0.0, T_END]
        w_values = [0, 0]
    else:
        w_times = [0.0, catastrophe_time, T_END]
        w_values = [0, burst_size, burst_size]

    return Trajectory(
        x_times=np.asarray(x_times, dtype=float),
        x_display=np.asarray(x_values, dtype=int),
        w_times=np.asarray(w_times, dtype=float),
        w_values=np.asarray(w_values, dtype=int),
        terminal=terminal,
        catastrophe_time=catastrophe_time,
        burst_size=burst_size,
    )


def simulate_ensemble() -> list[Trajectory]:
    rng = np.random.default_rng(SEED)
    return [simulate_path(rng) for _ in range(N_PATHS)]


def run_asserts(paths: list[Trajectory]) -> None:
    """Numerical and structural checks required by the F3.6 brief."""

    assert len(paths) == N_PATHS == 100
    valid_terminal_states = {"extinct", "catastrophe", "continuing"}

    for path in paths:
        assert path.terminal in valid_terminal_states
        assert path.x_times.shape == path.x_display.shape
        assert np.all(np.diff(path.x_times) >= 0.0)
        assert path.x_times[0] == 0.0
        assert path.x_times[-1] <= T_END
        assert np.all(path.x_display >= 0)
        assert np.all(path.x_display == np.floor(path.x_display))
        assert path.w_times[0] == 0.0 and path.w_times[-1] == T_END
        assert np.all(np.diff(path.w_times) >= 0.0)
        assert np.all(path.w_values >= 0)

        if path.terminal == "catastrophe":
            assert path.catastrophe_time is not None
            assert path.burst_size is not None and path.burst_size >= 1
            assert np.isclose(path.x_times[-1], path.catastrophe_time)
            assert path.x_display[-2] == path.burst_size
            assert path.x_display[-1] == 0  # plotting coordinate for H
            assert np.count_nonzero(np.diff(path.w_values) > 0) == 1
            assert np.array_equal(
                path.w_values, np.asarray([0, path.burst_size, path.burst_size])
            )
            assert np.isclose(path.w_times[1], path.catastrophe_time)
        else:
            assert path.catastrophe_time is None and path.burst_size is None
            assert np.count_nonzero(np.diff(path.w_values)) == 0
            if path.terminal == "extinct":
                assert path.x_display[-1] == 0
            else:
                assert path.x_times[-1] == T_END
                assert path.x_display[-1] >= 1

    # With mu=0, the only absorbing event is catastrophe; X can otherwise
    # remain a valid positive count at the finite plotting horizon.
    assert MU == 0.0
    assert all(path.terminal != "extinct" for path in paths)
    assert any(path.terminal == "catastrophe" for path in paths)
    assert any(np.count_nonzero(np.diff(path.w_values) > 0) == 1 for path in paths)


def representative_burst(paths: list[Trajectory]) -> Trajectory:
    """Choose a legible, non-extreme burst for the required annotation."""

    burst_paths = [
        path
        for path in paths
        if path.catastrophe_time is not None
        and 1.0 <= path.catastrophe_time <= 0.75 * T_END
    ]
    assert burst_paths
    ordered = sorted(burst_paths, key=lambda path: (path.burst_size, path.catastrophe_time))
    return ordered[int(0.72 * (len(ordered) - 1))]


def configure_axis(ax: plt.Axes, ylabel: str, ymax: float) -> None:
    ax.set_xlim(0.0, T_END)
    ax.set_ylim(0.0, ymax)
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(ylabel)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=6, integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=7, integer=True))


def draw_x(ax: plt.Axes, paths: list[Trajectory], representative: Trajectory) -> None:
    for path in paths:
        ax.step(
            path.x_times,
            path.x_display,
            where="post",
            color="tab:blue",
            alpha=0.20,
            linewidth=0.75,
            solid_capstyle="butt",
        )

    ax.step(
        representative.x_times,
        representative.x_display,
        where="post",
        color="tab:blue",
        alpha=0.95,
        linewidth=1.35,
        solid_capstyle="butt",
        zorder=3,
    )
    tau = float(representative.catastrophe_time)
    size = int(representative.burst_size)
    ymax = max(int(np.max(path.x_display)) for path in paths) * 1.08
    configure_axis(ax, r"$X_t$ (count)", ymax)
    ax.set_title(r"100 Gillespie realisations of $X_t$")
    ax.annotate(
        r"catastrophe: $X_t=H$",
        xy=(tau, 0.03 * ymax),
        xytext=(min(tau + 2.4, 0.72 * T_END), min(size + 0.16 * ymax, 0.82 * ymax)),
        arrowprops={"arrowstyle": "->", "color": "black", "linewidth": 0.8},
        fontsize=9,
        ha="left",
        va="bottom",
        color="black",
    )


def draw_w(ax: plt.Axes, paths: list[Trajectory], representative: Trajectory) -> None:
    for path in paths:
        ax.step(
            path.w_times,
            path.w_values,
            where="post",
            color="tab:orange",
            alpha=0.20,
            linewidth=0.75,
            solid_capstyle="butt",
        )

    ax.step(
        representative.w_times,
        representative.w_values,
        where="post",
        color="tab:orange",
        alpha=1.0,
        linewidth=1.35,
        solid_capstyle="butt",
        zorder=3,
    )
    tau = float(representative.catastrophe_time)
    size = int(representative.burst_size)
    ymax = max(int(np.max(path.w_values)) for path in paths) * 1.08
    configure_axis(ax, r"$W_t$ (count)", ymax)
    ax.set_title(r"100 Gillespie realisations of $W_t$")
    ax.plot(tau, size, marker="o", markersize=3.5, color="tab:orange", zorder=4)
    ax.annotate(
        r"representative burst",
        xy=(tau, size),
        xytext=(min(tau + 2.2, 0.70 * T_END), min(size + 0.16 * ymax, 0.86 * ymax)),
        arrowprops={"arrowstyle": "->", "color": "black", "linewidth": 0.8},
        fontsize=9,
        ha="left",
        va="bottom",
        color="black",
    )


def save_figures(paths: list[Trajectory]) -> None:
    representative = representative_burst(paths)

    fig_x, ax_x = plt.subplots(figsize=(6.4, 4.15))
    draw_x(ax_x, paths, representative)
    fig_x.tight_layout()
    style_rc.save_figure(fig_x, X_PDF)
    plt.close(fig_x)

    fig_w, ax_w = plt.subplots(figsize=(6.4, 4.15))
    draw_w(ax_w, paths, representative)
    fig_w.tight_layout()
    style_rc.save_figure(fig_w, W_PDF)
    plt.close(fig_w)

    preview, axes = plt.subplots(2, 1, figsize=(7.2, 7.7))
    draw_x(axes[0], paths, representative)
    draw_w(axes[1], paths, representative)
    preview.tight_layout()
    preview.savefig(PREVIEW_PNG, format="png", dpi=200, bbox_inches="tight")
    plt.close(preview)


def main() -> None:
    paths = simulate_ensemble()
    run_asserts(paths)
    save_figures(paths)
    n_catastrophes = sum(path.terminal == "catastrophe" for path in paths)
    max_burst = max(path.burst_size or 0 for path in paths)
    print(
        f"F3.6 asserts passed: {len(paths)} paths; "
        f"{n_catastrophes} catastrophes by t={T_END:g}; max burst={max_burst}."
    )
    print(f"Wrote {X_PDF}")
    print(f"Wrote {W_PDF}")
    print(f"Wrote {PREVIEW_PNG}")


if __name__ == "__main__":
    main()
