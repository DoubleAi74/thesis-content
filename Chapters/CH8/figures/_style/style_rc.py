"""Shared matplotlib style for the pathogenesis chapter.

Palette and typography follow the house conventions used in Chapters 5 and 7
(Okabe–Ito: #0072B2 blue, #D55E00 vermillion, #1a1c1f ink). The survival
diverging map is local (extinct vermillion → certain teal).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

BLUE = "#0072B2"
VERMILLION = "#D55E00"
INK = "#1a1c1f"
SOFT = "#565b62"
GRID = "#e3e6ea"
TEAL = "#009E73"
CATA = "#9A2820"
YELLOW = "#F0E442"
BLUE_FILL = "#E9F1F8"
VERMILLION_FILL = "#FBEEE5"

SURVIVAL = [CATA, VERMILLION, YELLOW, TEAL]


def survival_cmap():
    from matplotlib.colors import LinearSegmentedColormap

    return LinearSegmentedColormap.from_list("ch8_surv", SURVIVAL)


def apply() -> None:
    plt.rcParams.update(
        {
            "figure.dpi": 120,
            "savefig.dpi": 400,
            "font.family": "serif",
            "font.serif": ["DejaVu Serif"],
            "mathtext.fontset": "cm",
            "font.size": 9.5,
            "axes.titlesize": 10,
            "axes.labelsize": 9.5,
            "legend.fontsize": 8.5,
            "xtick.labelsize": 8.5,
            "ytick.labelsize": 8.5,
            "axes.edgecolor": INK,
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": False,
            "legend.frameon": False,
            "lines.linewidth": 1.5,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "pdf.fonttype": 42,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.02,
        }
    )
