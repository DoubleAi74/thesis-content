#!/usr/bin/env python3
"""Generate F4b.2: extinction probabilities in the three flooding regimes."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/bdc_odes_mplconfig")

import numpy as np

STYLE_DIR = Path(
    "/Users/adamaldridge/Desktop/Thesis content 🎓 "
    "/4 BDC additional and BMVR/Figures run/style"
)
sys.path.insert(0, str(STYLE_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_style"))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402


@dataclass(frozen=True)
class Regime:
    parameters: tuple[float, float, float]
    parameter_label: str
    regime_label: str
    q_representative: float

    @property
    def derived(self) -> tuple[float, float, float, float]:
        lam, mu, delta = self.parameters
        eta = (lam + mu + delta) / (2.0 * lam)
        radical = np.sqrt(eta**2 - mu / lam)
        a = eta + radical
        b = eta - radical
        flooding_parameter = a * (1.0 - b)
        v_inf = flooding_parameter / (a - 1.0)
        return a, b, flooding_parameter, v_inf


REGIMES = (
    Regime((1.0, 0.0, 0.1), r"$(1,0,0.1)$", r"$L>1$", 0.2),
    Regime((1.0, 0.5, 1.0 / 3.0), r"$(1,0.5,1/3)$", r"$L=1$", 0.6),
    Regime((1.0, 0.9, 0.1), r"$(1,0.9,0.1)$", r"$L<1$", 0.9),
)


def extinction_probabilities(
    q: np.ndarray | float, regime: Regime
) -> tuple[np.ndarray, np.ndarray]:
    """Return the closed-form burst and matched-mean budding probabilities."""
    q_array = np.asarray(q, dtype=float)
    a, b, _, v_inf = regime.derived
    z_burst = (a - 1.0) / q_array + 1.0 - a * (1.0 - b)
    z_bud = 1.0 / (q_array * v_inf)
    return z_burst, z_bud


def run_asserts() -> None:
    """Check the table values, theorem identity, and all curve orderings."""
    expected = (
        (REGIMES[0], 0.2, 0.400, 0.455),
        (REGIMES[2], 0.9, 0.935, 0.844),
        (REGIMES[1], 0.6, 0.833, 0.833),
        (REGIMES[1], 0.9, 0.556, 0.556),
    )
    for regime, q_value, burst_expected, bud_expected in expected:
        burst, bud = extinction_probabilities(q_value, regime)
        assert abs(float(burst) - burst_expected) < 1e-3
        assert abs(float(bud) - bud_expected) < 1e-3

    for regime in REGIMES:
        _, _, flooding_parameter, v_inf = regime.derived
        q_boundary = 1.0 / v_inf
        assert 0.0 < q_boundary < regime.q_representative <= 1.0
        q_values = np.linspace(q_boundary, 1.0, 401)
        burst, bud = extinction_probabilities(q_values, regime)
        theorem_gap = (flooding_parameter - 1.0) * (bud - 1.0)
        assert np.max(np.abs((burst - bud) - theorem_gap)) < 1e-12
        assert np.all((burst >= -1e-12) & (burst <= 1.0 + 1e-12))
        assert np.all((bud >= -1e-12) & (bud <= 1.0 + 1e-12))
        if flooding_parameter > 1.0 + 1e-10:
            assert np.all(burst[1:] < bud[1:])
        elif flooding_parameter < 1.0 - 1e-10:
            assert np.all(burst[1:] > bud[1:])
        else:
            assert np.max(np.abs(burst - bud)) < 1e-12


NOTE_POS = {"a": (0.52, 0.62), "b": (0.46, 0.28), "c": (0.50, 0.30)}


def annotate_gap(ax: plt.Axes, regime: Regime, note_pos) -> None:
    q_value = regime.q_representative
    burst, bud = extinction_probabilities(q_value, regime)
    burst_value, bud_value = float(burst), float(bud)
    gap = burst_value - bud_value
    ax.plot(q_value, burst_value, marker="o", ms=3.2, color=style_rc.BLUE, zorder=5)
    ax.plot(q_value, bud_value, marker="o", ms=3.2, color=style_rc.VERMILLION, zorder=5)
    if abs(gap) > 1e-8:
        ax.annotate(
            "",
            xy=(q_value, burst_value),
            xytext=(q_value, bud_value),
            arrowprops=dict(arrowstyle="<->", color="black", lw=0.8),
        )
        midpoint = 0.5 * (burst_value + bud_value)
        ax.annotate(
            rf"$z_{{\mathrm{{burst}}}}-z_{{\mathrm{{bud}}}}={gap:+.3f}$",
            xy=note_pos,
            xycoords="axes fraction",
            ha="center",
            va="center",
            fontsize=8,
            bbox=dict(boxstyle="round,pad=0.14", facecolor="white",
                      edgecolor="none", alpha=0.85),
        )
    else:
        ax.annotate(
            r"$z_{\mathrm{burst}}-z_{\mathrm{bud}}=0$",
            xy=note_pos,
            xycoords="axes fraction",
            ha="center",
            va="center",
            fontsize=8,
        )


def make_figure() -> plt.Figure:
    fig, axes = plt.subplots(1, 3, figsize=(5.89, 2.55), sharey=True)
    panel_letters = ("a", "b", "c")

    for panel_letter, ax, regime in zip(panel_letters, axes, REGIMES):
        _, _, flooding_parameter, v_inf = regime.derived
        q_boundary = 1.0 / v_inf
        q_values = np.linspace(q_boundary, 1.0, 400)
        burst, bud = extinction_probabilities(q_values, regime)

        ax.plot(q_values, burst, color=style_rc.BLUE, label="burst")
        ax.plot(
            q_values,
            bud,
            color=style_rc.VERMILLION,
            linestyle="--",
            label="bud",
        )
        ax.axvline(q_boundary, color=style_rc.SOFT, linestyle=":", linewidth=1.1)
        ax.annotate(
            r"$m=1$",
            xy=(q_boundary, 1.0),
            xytext=(4, -6),
            textcoords="offset points",
            ha="left",
            va="top",
            fontsize=8,
            color=style_rc.SOFT,
        )
        annotate_gap(ax, regime, NOTE_POS[panel_letter])
        style_rc.panel_label(ax, f"({panel_letter})")
        ax.text(0.97, 0.03, rf"$L={flooding_parameter:.2f}$" "\n" + regime.parameter_label,
                transform=ax.transAxes, ha="right", va="bottom", fontsize=8.2,
                color=style_rc.SOFT, linespacing=1.35)

        ax.set_xlim(max(0.0, q_boundary - 0.035), 1.01)
        ax.set_ylim(0.0, 1.04)

    axes[0].set_ylabel(r"extinction probability $z_{\mathrm{ext}}$")
    fig.supxlabel(r"infection success probability $q$", y=0.02, fontsize=9.5)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2,
               bbox_to_anchor=(0.5, 1.005), columnspacing=2.2)
    fig.tight_layout(w_pad=1.25, rect=(0.0, 0.03, 1.0, 0.92))
    return fig


def main() -> None:
    run_asserts()
    workdir = Path(__file__).resolve().parent
    figures_dir = workdir.parents[1]
    production_pdf = figures_dir / "F4b_2_flooding_regimes.pdf"
    preview_png = workdir / "preview.png"
    fig = make_figure()
    style_rc.save_figure(fig, production_pdf, preview_png)
    plt.close(fig)
    print(f"asserts: pass; wrote {production_pdf} and {preview_png}")


if __name__ == "__main__":
    main()
