#!/usr/bin/env python3
"""Generate N3.5: Gillespie paths coloured by eventual terminal fate.

The direct-method simulation uses the fixed seed ``N3_5_SEED = 3505``.  Each
realisation is continued to absorption so its colour records an actual fate,
while the displayed segment is restricted to 0 <= t <= 20.  The catastrophe
state H is represented only by the terminal drop to the plotting baseline; it
is not treated as the count state zero.  The bold overlay is the exact
unconditional mean J(t), to which both absorbed path classes contribute zero.
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

import matplotlib.patheffects as path_effects  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.ticker import MaxNLocator  # noqa: E402


LAMBDA = 1.0
MU = 0.2
DELTA = 0.05
X0 = 1
T_END = 20.0
N_PATHS = 180
N3_5_SEED = 3505
MAX_EVENTS = 200_000

EXTINCTION_COLOUR = "#768692"
CATASTROPHE_COLOUR = "#c0392b"
MEAN_COLOUR = "#162a44"
ANNOTATION_PURPLE = "#6b4c9a"

WORK_DIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORK_DIR.parents[2]
PDF_PATH = CHAPTER_DIR / "figures/N3_5_fate_coloured_paths.pdf"
PNG_PATH = WORK_DIR / "preview.png"


@dataclass(frozen=True)
class Trajectory:
    """One exact path continued until internal extinction or catastrophe."""

    times: np.ndarray
    values: np.ndarray
    fate: str
    absorption_time: float
    pre_absorption_count: int


def quadratic_roots() -> tuple[float, float]:
    """Return a > 1 > b for the chapter's characteristic quadratic."""

    eta = (LAMBDA + MU + DELTA) / (2.0 * LAMBDA)
    radical = np.sqrt(eta**2 - MU / LAMBDA)
    return float(eta + radical), float(eta - radical)


def exact_mean(t: np.ndarray | float) -> np.ndarray:
    """Stable evaluation of J(t) from Theorem 3's closed form."""

    a, b = quadratic_roots()
    A = a - 1.0
    B = 1.0 - b
    theta = LAMBDA * (a - b)
    z = np.exp(-theta * np.asarray(t, dtype=float))
    return (a - b) ** 2 * z / (B * z + A) ** 2


def simulate_path(rng: np.random.Generator) -> Trajectory:
    """Simulate one BDC path by the exact Gillespie direct method."""

    t = 0.0
    n = X0
    times = [0.0]
    values = [X0]
    event_count = 0

    while n > 0:
        event_count += 1
        assert event_count <= MAX_EVENTS, "path did not absorb within safety bound"

        total_rate = (LAMBDA + MU + DELTA) * n
        assert total_rate > 0.0
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
            # H has no numeric count.  Zero is solely the endpoint baseline used
            # to make the terminal catastrophe jump visible in the plot.
            times.append(t)
            values.append(0)
            return Trajectory(
                times=np.asarray(times, dtype=float),
                values=np.asarray(values, dtype=int),
                fate="catastrophe",
                absorption_time=t,
                pre_absorption_count=pre_event_n,
            )

    raise AssertionError("unreachable simulation state")


def simulate_ensemble() -> list[Trajectory]:
    rng = np.random.default_rng(N3_5_SEED)
    return [simulate_path(rng) for _ in range(N_PATHS)]


def path_values_at(path: Trajectory, grid: np.ndarray) -> np.ndarray:
    """Evaluate the count contribution of a path, with zero after absorption."""

    indices = np.searchsorted(path.times, grid, side="right") - 1
    indices = np.clip(indices, 0, len(path.values) - 1)
    return path.values[indices].astype(float)


def displayed_path(path: Trajectory) -> tuple[np.ndarray, np.ndarray]:
    """Clip one step path at the common plotting horizon without extrapolation."""

    if path.absorption_time <= T_END:
        mask = path.times <= T_END
        return path.times[mask], path.values[mask]

    event_mask = path.times < T_END
    times = path.times[event_mask]
    values = path.values[event_mask]
    assert times.size >= 1
    return (
        np.append(times, T_END),
        np.append(values, values[-1]),
    )


def run_asserts(paths: list[Trajectory]) -> dict[str, float | int]:
    """Check exact-path structure and the required fate-frequency agreement."""

    assert len(paths) == N_PATHS
    assert exact_mean(0.0) == np.asarray(1.0)

    for path in paths:
        assert path.fate in {"extinction", "catastrophe"}
        assert path.times.shape == path.values.shape
        assert path.times[0] == 0.0 and path.values[0] == X0
        assert np.all(np.diff(path.times) > 0.0)
        assert np.all(path.values >= 0)
        assert np.all(path.values == np.floor(path.values))
        assert path.values[-1] == 0
        assert np.isclose(path.times[-1], path.absorption_time)
        assert path.pre_absorption_count >= 1
        if path.fate == "extinction":
            assert path.pre_absorption_count == 1
            assert path.values[-2] == 1
        else:
            assert path.values[-2] == path.pre_absorption_count

        display_t, display_x = displayed_path(path)
        assert display_t[0] == 0.0
        assert display_t[-1] <= T_END
        assert np.all(np.diff(display_t) > 0.0)
        assert display_t.shape == display_x.shape
        if path.absorption_time > T_END:
            assert np.isclose(display_t[-1], T_END)
            assert display_x[-1] >= 1

    a, b = quadratic_roots()
    catastrophe_probability = 1.0 - b
    catastrophe_count = sum(path.fate == "catastrophe" for path in paths)
    extinction_count = N_PATHS - catastrophe_count
    empirical_catastrophe = catastrophe_count / N_PATHS
    monte_carlo_se = np.sqrt(
        catastrophe_probability * (1.0 - catastrophe_probability) / N_PATHS
    )
    assert abs(empirical_catastrophe - catastrophe_probability) <= 3.5 * monte_carlo_se

    grid = np.linspace(0.0, T_END, 401)
    sample_matrix = np.vstack([path_values_at(path, grid) for path in paths])
    sample_mean = np.mean(sample_matrix, axis=0)
    assert np.all(np.isfinite(sample_matrix))
    assert sample_mean[0] == X0
    for check_time in (1.0, 2.5, 5.0):
        idx = int(np.argmin(np.abs(grid - check_time)))
        standard_error = float(np.std(sample_matrix[:, idx], ddof=1) / np.sqrt(N_PATHS))
        discrepancy = abs(float(sample_mean[idx] - exact_mean(grid[idx])))
        assert discrepancy <= 4.0 * standard_error + 0.03

    censored_count = sum(path.absorption_time > T_END for path in paths)
    return {
        "a": a,
        "b": b,
        "catastrophe_count": catastrophe_count,
        "extinction_count": extinction_count,
        "empirical_catastrophe": empirical_catastrophe,
        "exact_catastrophe": catastrophe_probability,
        "monte_carlo_se": monte_carlo_se,
        "censored_at_t20": censored_count,
        "max_count": max(int(np.max(path.values)) for path in paths),
    }


def _representative(paths: list[Trajectory], fate: str) -> Trajectory:
    """Choose a central, early endpoint for a short unobtrusive annotation."""

    candidates = [
        path
        for path in paths
        if path.fate == fate and 0.45 <= path.absorption_time <= 8.0
    ]
    assert candidates
    if fate == "catastrophe":
        candidates.sort(
            key=lambda path: (
                abs(path.absorption_time - 6.4),
                abs(path.pre_absorption_count - 8),
            )
        )
    else:
        candidates.sort(key=lambda path: abs(path.absorption_time - 2.2))
    return candidates[0]


def make_figure(paths: list[Trajectory], diagnostics: dict[str, float | int]) -> None:
    """Render the single-panel fate-resolved ensemble and exact mean."""

    fig, ax = plt.subplots(figsize=(7.25, 4.65))

    # Catastrophe paths are more numerous, so draw them first and slightly more
    # transparently; extinction paths remain visible as a separate path class.
    ordered_paths = sorted(paths, key=lambda path: path.fate == "extinction")
    for path in ordered_paths:
        times, values = displayed_path(path)
        is_catastrophe = path.fate == "catastrophe"
        colour = CATASTROPHE_COLOUR if is_catastrophe else EXTINCTION_COLOUR
        alpha = 0.145 if is_catastrophe else 0.32
        linewidth = 0.60 if is_catastrophe else 0.74
        ax.step(
            times,
            values,
            where="post",
            color=colour,
            alpha=alpha,
            linewidth=linewidth,
            solid_capstyle="butt",
            zorder=1,
        )

        if path.absorption_time <= T_END:
            if is_catastrophe:
                ax.plot(
                    path.absorption_time,
                    0.0,
                    marker="o",
                    markersize=2.2,
                    markerfacecolor=CATASTROPHE_COLOUR,
                    markeredgecolor="white",
                    markeredgewidth=0.25,
                    alpha=0.58,
                    linestyle="none",
                    zorder=2,
                )
            else:
                ax.plot(
                    path.absorption_time,
                    0.0,
                    marker="x",
                    markersize=3.1,
                    markeredgewidth=0.75,
                    color=EXTINCTION_COLOUR,
                    alpha=0.78,
                    linestyle="none",
                    zorder=2,
                )

    t = np.linspace(0.0, T_END, 2001)
    mean_line = ax.plot(
        t,
        exact_mean(t),
        color=MEAN_COLOUR,
        linewidth=2.75,
        label=r"exact mean $J(t)=\mathbb{E}[X_t]$",
        zorder=6,
    )[0]
    mean_line.set_path_effects(
        [
            path_effects.Stroke(linewidth=4.8, foreground="white", alpha=0.88),
            path_effects.Normal(),
        ]
    )

    max_count = int(diagnostics["max_count"])
    y_limit = max(22.0, 1.06 * max_count)
    latest_absorption = max(path.absorption_time for path in paths)
    if latest_absorption < T_END:
        ax.axvspan(
            latest_absorption,
            T_END,
            color="#dfe3e6",
            alpha=0.26,
            linewidth=0.0,
            zorder=0,
        )
        ax.text(
            0.5 * (latest_absorption + T_END),
            0.56 * y_limit,
            rf"all {N_PATHS} paths absorbed"
            + "\n"
            + rf"by $t={latest_absorption:.1f}$",
            color="#616a70",
            fontsize=9,
            ha="center",
            va="center",
            linespacing=1.35,
            zorder=3,
        )

    # A direct label names the conceptual punchline without turning the figure
    # into a dashboard or duplicating the parameter-rich caption.
    peak_index = int(np.argmax(exact_mean(t)))
    peak_t = float(t[peak_index])
    peak_j = float(exact_mean(t)[peak_index])
    ax.annotate(
        r"$J(t)$ mixes both fates;" + "\n" + "it is not a typical path",
        xy=(peak_t, peak_j),
        xytext=(4.9, 0.24 * y_limit),
        arrowprops={
            "arrowstyle": "->",
            "color": ANNOTATION_PURPLE,
            "linewidth": 0.9,
            "shrinkA": 2,
            "shrinkB": 3,
        },
        color=ANNOTATION_PURPLE,
        fontsize=9,
        ha="left",
        va="bottom",
        zorder=8,
    )

    extinction_path = _representative(paths, "extinction")
    catastrophe_path = _representative(paths, "catastrophe")
    ax.annotate(
        r"internal extinction at $0$",
        xy=(extinction_path.absorption_time, 0.0),
        xytext=(0.9, 0.18 * y_limit),
        arrowprops={
            "arrowstyle": "->",
            "color": EXTINCTION_COLOUR,
            "linewidth": 0.8,
        },
        color="#53636f",
        fontsize=8.7,
        ha="left",
        va="bottom",
        zorder=7,
    )
    ax.annotate(
        r"catastrophe: terminal jump to $H$",
        xy=(catastrophe_path.absorption_time, 0.0),
        xytext=(7.0, 0.34 * y_limit),
        arrowprops={
            "arrowstyle": "->",
            "color": CATASTROPHE_COLOUR,
            "linewidth": 0.8,
        },
        color="#982f25",
        fontsize=8.7,
        ha="left",
        va="bottom",
        zorder=7,
    )

    extinction_count = int(diagnostics["extinction_count"])
    catastrophe_count = int(diagnostics["catastrophe_count"])
    legend_handles = [
        Line2D(
            [0],
            [0],
            color=EXTINCTION_COLOUR,
            linewidth=1.6,
            marker="x",
            markersize=5.2,
            markeredgewidth=1.0,
            label=rf"internal extinction  ($n={extinction_count}$)",
        ),
        Line2D(
            [0],
            [0],
            color=CATASTROPHE_COLOUR,
            linewidth=1.6,
            marker="o",
            markerfacecolor=CATASTROPHE_COLOUR,
            markeredgecolor="white",
            markersize=5.2,
            label=rf"catastrophe  ($n={catastrophe_count}$)",
        ),
        Line2D(
            [0],
            [0],
            color=MEAN_COLOUR,
            linewidth=2.75,
            label=r"exact mean $J(t)$",
        ),
    ]

    # The fixed ensemble has a moderate maximum.  A fully linear count axis
    # keeps the terminal steps and the magnitude of individual paths honest.
    ax.set_xlim(0.0, T_END)
    ax.set_ylim(0.0, y_limit)
    ax.set_xticks(np.arange(0.0, T_END + 0.1, 4.0))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=7, integer=True))
    ax.set_xlabel(r"time $t$")
    ax.set_ylabel(r"intracellular count $X_t$")
    ax.set_title("Two terminal path classes sit beneath one ensemble mean", pad=10)
    ax.legend(
        handles=legend_handles,
        loc="upper right",
        ncol=1,
        handlelength=2.8,
        borderpad=0.55,
        labelspacing=0.45,
    )

    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)

    assert PDF_PATH.exists() and PDF_PATH.stat().st_size > 2_000
    assert PNG_PATH.exists() and PNG_PATH.stat().st_size > 10_000


def main() -> None:
    paths = simulate_ensemble()
    diagnostics = run_asserts(paths)
    make_figure(paths, diagnostics)
    print("N3.5 asserts passed")
    for name, value in diagnostics.items():
        print(f"{name}={value}")
    print(f"seed={N3_5_SEED}")
    print(f"wrote {PDF_PATH}")
    print(f"wrote {PNG_PATH}")


if __name__ == "__main__":
    main()
