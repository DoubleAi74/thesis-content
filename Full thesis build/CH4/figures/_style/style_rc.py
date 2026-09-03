"""Shared matplotlib style for Chapter 4 figures.

Grammar follows Good examples/CH2/figures/make_figures.py: tidy spines, no
grid by default, serif type, figures sized for an 11pt thesis page.

Colours follow the two-type chapter: Okabe--Ito blue / vermillion on ink.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

BLUE = "#0072B2"
VERMILLION = "#D55E00"
INK = "#1a1c1f"
GREY = "#9a9a9a"
SOFT = "#565b62"
GRAY_REF = "#888888"


def apply() -> None:
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["DejaVu Serif", "Times New Roman"],
            "mathtext.fontset": "dejavuserif",
            "font.size": 9,
            "axes.labelsize": 9,
            "axes.titlesize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 8,
            "axes.linewidth": 0.7,
            "xtick.major.width": 0.7,
            "ytick.major.width": 0.7,
            "lines.linewidth": 1.1,
            "axes.edgecolor": INK,
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": False,
            "legend.frameon": False,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "figure.dpi": 150,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.02,
            "pdf.fonttype": 42,
        }
    )


def tidy(ax) -> None:
    """Strip the top and right spines; keep the frame light."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(INK)
    ax.spines["bottom"].set_color(INK)


def asymptote_hline(ax, y: float, label: str | None = None) -> None:
    ax.axhline(y, color=GRAY_REF, linestyle=(0, (4, 3)), linewidth=0.9, zorder=0)
    if label:
        ax.text(
            0.98,
            y,
            label,
            transform=ax.get_yaxis_transform(),
            ha="right",
            va="bottom",
            color=SOFT,
            fontsize=8,
        )


def save_figure(fig, pdf_path: Path, png_path: Path | None = None, dpi: int = 240) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(pdf_path)
    if png_path is not None:
        png_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(png_path, dpi=dpi)
