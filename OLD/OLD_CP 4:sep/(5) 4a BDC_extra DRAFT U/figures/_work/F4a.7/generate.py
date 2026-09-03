#!/usr/bin/env python3
"""Generate F4a.7: chained-transfer rupture sizes and intervals."""

from __future__ import annotations

import sys
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


LAMBDA = 1.0
DELTA = 1.0
S = DELTA / (LAMBDA + DELTA)
RHO = LAMBDA / (LAMBDA + DELTA)
SAMPLE_SIZE = 1_000_000
SEED = 42
MAX_CHAIN = 6
DISPLAY_N = np.arange(1, 21)
WORKDIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORKDIR.parents[2]
PDF_PATH = CHAPTER_DIR / "figures" / "F4a_7_chained_transfer.pdf"
PNG_PATH = WORKDIR / "preview.png"


def rupture_pmf(founders: int, max_n: int) -> np.ndarray:
    """Stable recurrence for P(r_k=n), n=1,...,max_n."""
    pmf = np.empty(max_n, dtype=float)
    pmf[0] = S**founders
    for index in range(1, max_n):
        n = float(index)  # preceding support value: n=index
        pmf[index] = pmf[index - 1] * RHO * (n + founders - 1.0) / n
    return pmf


def fixed_founder_mean_interval(founders: int) -> float:
    m = np.arange(0, 500, dtype=float)
    terms = RHO**m / ((LAMBDA + DELTA) * (founders + m))
    return float(terms.sum())


def simulate_chain() -> tuple[np.ndarray, np.ndarray]:
    """Exact event-type simulation for six linked cells."""
    rng = np.random.default_rng(SEED)
    births = (rng.geometric(S, size=(SAMPLE_SIZE, MAX_CHAIN)) - 1).astype(
        np.int16
    )
    rupture_sizes = 1 + np.cumsum(births, axis=1, dtype=np.int32)
    interval_means = np.empty(MAX_CHAIN, dtype=float)

    for chain_index in range(MAX_CHAIN):
        if chain_index == 0:
            founding_load = np.ones(SAMPLE_SIZE, dtype=np.int32)
        else:
            founding_load = rupture_sizes[:, chain_index - 1]
        event_births = births[:, chain_index]
        intervals = np.zeros(SAMPLE_SIZE, dtype=float)
        for offset in range(int(event_births.max()) + 1):
            active = event_births >= offset
            loads = founding_load[active] + offset
            intervals[active] += rng.exponential(
                scale=1.0 / ((LAMBDA + DELTA) * loads)
            )
        interval_means[chain_index] = intervals.mean()

    return rupture_sizes, interval_means


def run_asserts(
    rupture_sizes: np.ndarray, interval_means: np.ndarray
) -> np.ndarray:
    assert abs(S - 0.5) < 1e-15 and abs(RHO - 0.5) < 1e-15
    assert rupture_sizes.shape == (SAMPLE_SIZE, MAX_CHAIN)
    assert np.all(np.diff(rupture_sizes, axis=1) >= 0)

    for founders in range(1, 5):
        pmf = rupture_pmf(founders, 500)
        assert np.all(pmf >= 0.0)
        assert abs(pmf.sum() - 1.0) < 2e-14
        expected_mean = 1.0 + founders * RHO / S
        support = np.arange(1, 501, dtype=float)
        assert abs(np.dot(support, pmf) - expected_mean) < 2e-12
        assert abs(rupture_sizes[:, founders - 1].mean() - expected_mean) < 0.02

        hist = np.bincount(
            rupture_sizes[:, founders - 1], minlength=DISPLAY_N[-1] + 1
        )[DISPLAY_N] / SAMPLE_SIZE
        analytic = rupture_pmf(founders, int(DISPLAY_N[-1]))
        assert np.max(np.abs(hist - analytic)) < 0.002

    fixed_means = np.array(
        [fixed_founder_mean_interval(k) for k in range(1, MAX_CHAIN + 1)]
    )
    assert np.all(np.diff(fixed_means) < 0.0)
    assert np.all(np.diff(interval_means) < 0.0)
    assert abs(fixed_means[0] - np.log(2.0)) < 1e-13
    assert abs(interval_means[0] - fixed_means[0]) < 0.003
    return fixed_means


def make_figure() -> None:
    rupture_sizes, interval_means = simulate_chain()
    fixed_means = run_asserts(rupture_sizes, interval_means)

    fig, (ax_size, ax_time) = plt.subplots(1, 2, figsize=(10.4, 4.25))
    colours = ["tab:blue", "tab:orange", "tab:green", "tab:red"]
    offsets = np.array([-0.27, -0.09, 0.09, 0.27])

    for index, founders in enumerate(range(1, 5)):
        histogram = np.bincount(
            rupture_sizes[:, founders - 1], minlength=DISPLAY_N[-1] + 1
        )[DISPLAY_N] / SAMPLE_SIZE
        analytic = rupture_pmf(founders, int(DISPLAY_N[-1]))
        ax_size.bar(
            DISPLAY_N + offsets[index],
            histogram,
            width=0.17,
            color=colours[index],
            alpha=0.28,
            edgecolor=colours[index],
            linewidth=0.7,
            label=rf"$k={founders}$",
            zorder=2,
        )
        ax_size.plot(
            DISPLAY_N,
            analytic,
            color=colours[index],
            marker="o",
            markersize=2.7,
            linewidth=1.45,
            zorder=3,
        )

    ax_size.set_xlim(0.5, 20.5)
    ax_size.set_ylim(0.0, 0.53)
    ax_size.set_xticks(np.arange(1, 21, 2))
    ax_size.set_xlabel(r"Rupture size $n$")
    ax_size.set_ylabel("Probability")
    ax_size.set_title("(a) Rupture-size laws")
    ax_size.legend(ncol=2, loc="upper right")

    chain_index = np.arange(1, MAX_CHAIN + 1)
    ax_time.plot(
        chain_index,
        fixed_means,
        color="tab:blue",
        marker="o",
        markersize=4.5,
        label=r"fixed $k$ founders (analytic)",
        zorder=3,
    )
    ax_time.plot(
        chain_index,
        interval_means,
        color="tab:orange",
        linestyle="--",
        marker="s",
        markersize=4.5,
        label=r"chain interval $T_k$ (simulation)",
        zorder=3,
    )
    ax_time.set_xlim(0.8, 6.2)
    ax_time.set_ylim(0.0, 0.75)
    ax_time.set_xticks(chain_index)
    ax_time.set_xlabel(r"Index $k$")
    ax_time.set_ylabel("Mean interval")
    ax_time.set_title("(b) Inter-rupture intervals")
    ax_time.legend(loc="upper right")

    fig.tight_layout()
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH)
    plt.close(fig)
    print("fixed-founder means:", np.array2string(fixed_means, precision=6))
    print("simulated chain means:", np.array2string(interval_means, precision=6))


if __name__ == "__main__":
    make_figure()
    print(f"asserts: pass; wrote {PDF_PATH} and {PNG_PATH}")
