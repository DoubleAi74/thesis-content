#!/usr/bin/env python3
"""Few-path Gillespie realisations coloured by terminal fate, with exact mean."""

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
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.ticker import MaxNLocator  # noqa: E402

LAMBDA = 1.0
MU = 0.2
DELTA = 0.05
X0 = 1
T_END = 20.0
N_PATHS = 12
SEED = 154
MAX_EVENTS = 200_000

WORK_DIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORK_DIR.parents[2]
PDF_PATH = CHAPTER_DIR / "figures/F4_fate_coloured_paths.pdf"
PNG_PATH = WORK_DIR / "preview.png"


@dataclass(frozen=True)
class Trajectory:
    times: np.ndarray
    values: np.ndarray
    fate: str
    absorption_time: float
    pre_absorption_count: int


def quadratic_roots() -> tuple[float, float]:
    eta = (LAMBDA + MU + DELTA) / (2.0 * LAMBDA)
    radical = np.sqrt(eta**2 - MU / LAMBDA)
    return float(eta + radical), float(eta - radical)


def exact_mean(t: np.ndarray | float) -> np.ndarray:
    a, b = quadratic_roots()
    A = a - 1.0
    B = 1.0 - b
    theta = LAMBDA * (a - b)
    z = np.exp(-theta * np.asarray(t, dtype=float))
    return (a - b) ** 2 * z / (B * z + A) ** 2


def simulate_path(rng: np.random.Generator) -> Trajectory:
    t = 0.0
    n = X0
    times = [0.0]
    values = [X0]
    event_count = 0
    while n > 0:
        event_count += 1
        assert event_count <= MAX_EVENTS
        total_rate = (LAMBDA + MU + DELTA) * n
        t += float(rng.exponential(1.0 / total_rate))
        pre_event_n = n
        draw = float(rng.random() * (LAMBDA + MU + DELTA))
        if draw < LAMBDA:
            n += 1
            times.append(t)
            values.append(n)
        elif draw < LAMBDA + MU:
            n -= 1
            times.append(t)
            values.append(n)
            if n == 0:
                return Trajectory(
                    times=np.asarray(times, dtype=float),
                    values=np.asarray(values, dtype=int),
                    fate="extinction",
                    absorption_time=t,
                    pre_absorption_count=pre_event_n,
                )
        else:
            times.append(t)
            values.append(0)
            return Trajectory(
                times=np.asarray(times, dtype=float),
                values=np.asarray(values, dtype=int),
                fate="catastrophe",
                absorption_time=t,
                pre_absorption_count=pre_event_n,
            )
    raise AssertionError("unreachable")


def displayed_path(path: Trajectory) -> tuple[np.ndarray, np.ndarray]:
    if path.absorption_time <= T_END:
        mask = path.times <= T_END
        return path.times[mask], path.values[mask]
    event_mask = path.times < T_END
    times = path.times[event_mask]
    values = path.values[event_mask]
    return np.append(times, T_END), np.append(values, values[-1])


def run_asserts(paths: list[Trajectory]) -> dict[str, int]:
    assert len(paths) == N_PATHS
    fates = {path.fate for path in paths}
    assert "extinction" in fates and "catastrophe" in fates
    for path in paths:
        assert path.times[0] == 0.0 and path.values[0] == X0
        assert path.values[-1] == 0
        if path.fate == "extinction":
            assert path.values[-2] == 1
        else:
            assert path.values[-2] == path.pre_absorption_count
    return {
        "catastrophe": sum(p.fate == "catastrophe" for p in paths),
        "extinction": sum(p.fate == "extinction" for p in paths),
    }


def make_figure(paths: list[Trajectory], counts: dict[str, int]) -> None:
    fig, ax = plt.subplots(figsize=(5.8, 3.6))
    for path in sorted(paths, key=lambda p: p.fate == "extinction"):
        times, values = displayed_path(path)
        is_cat = path.fate == "catastrophe"
        colour = style_rc.VERMILLION if is_cat else style_rc.GREY
        ax.step(
            times,
            values,
            where="post",
            color=colour,
            alpha=0.85,
            linewidth=1.05,
            solid_capstyle="butt",
            zorder=1,
        )
        if path.absorption_time <= T_END:
            ax.plot(
                path.absorption_time,
                0.0,
                marker="o" if is_cat else "x",
                markersize=4.0 if is_cat else 5.0,
                markerfacecolor=style_rc.VERMILLION if is_cat else "none",
                markeredgecolor=colour,
                markeredgewidth=1.0,
                linestyle="none",
                zorder=2,
            )

    t = np.linspace(0.0, T_END, 2001)
    ax.plot(t, exact_mean(t), color=style_rc.INK, linewidth=1.8, zorder=4)

    ymax = max(22.0, 1.12 * max(int(np.max(p.values)) for p in paths))
    ax.set_xlim(0.0, T_END)
    ax.set_ylim(0.0, ymax)
    ax.set_xlabel(r"$t$")
    ax.set_ylabel(r"$X_t$")
    ax.yaxis.set_major_locator(MaxNLocator(nbins=6, integer=True))
    style_rc.tidy(ax)
    ax.legend(
        handles=[
            Line2D([0], [0], color=style_rc.GREY, lw=1.4, marker="x",
                   markersize=5, label=rf"extinction ($n={counts['extinction']}$)"),
            Line2D([0], [0], color=style_rc.VERMILLION, lw=1.4, marker="o",
                   markersize=4, label=rf"catastrophe ($n={counts['catastrophe']}$)"),
            Line2D([0], [0], color=style_rc.INK, lw=1.8, label=r"exact mean $J(t)$"),
        ],
        loc="upper right",
    )
    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)


def main() -> None:
    rng = np.random.default_rng(SEED)
    paths = [simulate_path(rng) for _ in range(N_PATHS)]
    counts = run_asserts(paths)
    make_figure(paths, counts)
    print(f"fate paths: {counts}")
    print(f"wrote {PDF_PATH}")


if __name__ == "__main__":
    main()
