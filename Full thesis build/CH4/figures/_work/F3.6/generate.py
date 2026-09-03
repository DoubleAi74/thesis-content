#!/usr/bin/env python3
"""Few-path Gillespie realisations of (X_t, W_t) at the working point."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

STYLE_DIR = Path(__file__).resolve().parents[2] / "_style"
sys.path.insert(0, str(STYLE_DIR))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import MaxNLocator  # noqa: E402

LAMBDA = 1.0
MU = 0.2
DELTA = 0.05
X0 = 1
T_END = 20.0
N_PATHS = 10
SEED = 12

WORK_DIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORK_DIR.parents[2]
PDF_PATH = CHAPTER_DIR / "figures/F4_paths_XW.pdf"
PNG_PATH = WORK_DIR / "preview.png"


@dataclass(frozen=True)
class Trajectory:
    x_times: np.ndarray
    x_display: np.ndarray
    w_times: np.ndarray
    w_values: np.ndarray
    terminal: str
    catastrophe_time: float | None
    burst_size: int | None


def simulate_path(rng: np.random.Generator) -> Trajectory:
    t = 0.0
    n = X0
    x_times = [0.0]
    x_values = [X0]
    catastrophe_time: float | None = None
    burst_size: int | None = None
    terminal = "continuing"

    while t < T_END and n > 0:
        total_rate = (LAMBDA + MU + DELTA) * n
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
        else:
            catastrophe_time = t
            burst_size = n
            terminal = "catastrophe"
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
    assert len(paths) == N_PATHS
    terminals = {path.terminal for path in paths}
    assert "extinct" in terminals
    assert "catastrophe" in terminals
    for path in paths:
        assert path.x_times[0] == 0.0
        assert np.all(path.w_values[0] == 0)
        if path.terminal == "catastrophe":
            assert path.burst_size is not None and path.burst_size >= 1
            assert path.x_display[-2] == path.burst_size
            assert path.x_display[-1] == 0
            assert path.w_values[-1] == path.burst_size
        else:
            assert path.w_values[-1] == 0
            if path.terminal == "extinct":
                assert path.x_display[-1] == 0


def make_figure(paths: list[Trajectory]) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(5.8, 5.4), sharex=True)
    ax_x, ax_w = axes

    ordered = sorted(paths, key=lambda p: p.terminal == "extinct")
    for path in ordered:
        colour = (
            style_rc.VERMILLION if path.terminal == "catastrophe" else style_rc.GREY
        )
        ax_x.step(
            path.x_times,
            path.x_display,
            where="post",
            color=colour,
            alpha=0.85,
            linewidth=1.05,
            solid_capstyle="butt",
        )
        ax_w.step(
            path.w_times,
            path.w_values,
            where="post",
            color=colour,
            alpha=0.85,
            linewidth=1.05,
            solid_capstyle="butt",
        )

    ymax_x = max(int(np.max(path.x_display)) for path in paths) * 1.12
    ymax_w = max(int(np.max(path.w_values)) for path in paths) * 1.12
    ax_x.set_ylabel(r"$X_t$")
    ax_w.set_ylabel(r"$W_t$")
    ax_w.set_xlabel(r"$t$")
    ax_x.set_ylim(0.0, ymax_x)
    ax_w.set_ylim(0.0, ymax_w)
    for ax in axes:
        ax.set_xlim(0.0, T_END)
        ax.yaxis.set_major_locator(MaxNLocator(nbins=6, integer=True))
        style_rc.tidy(ax)

    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)


def main() -> None:
    paths = simulate_ensemble()
    run_asserts(paths)
    make_figure(paths)
    n_cat = sum(path.terminal == "catastrophe" for path in paths)
    n_ext = sum(path.terminal == "extinct" for path in paths)
    print(f"F4 paths: {len(paths)} paths; {n_cat} catastrophe, {n_ext} extinct")
    print(f"wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
