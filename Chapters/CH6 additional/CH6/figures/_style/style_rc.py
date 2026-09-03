"""Shared matplotlib style for this chapter's figures.

Copied from the two-type chapter's `_style/style_rc.py` during the Phase C
figure rebuild, so that this chapter's figures carry the same palette and
typography as CH2, CH5 and CH7 rather than matplotlib's `tab:` defaults.
The `NAVY` alias below keeps the chapter's older `_work/*/generate.py`
scripts running against it unchanged.

Palette and typography follow `Prompts/SHARED_CONVENTIONS.md` (the standard
that governs the two-type chapter's figures): #0072B2 blue, #D55E00
vermillion, #1a1c1f ink, with line style preferred over extra hues.

The upstream `style_rc` module named by the source chapter's older
`_work/*/generate.py` scripts no longer exists on this machine; this file
replaces it for the figures built or regenerated here, and is the reason the
two rebuilt figures carry the conventions palette rather than matplotlib's
`tab:` defaults.
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
PURPLE = "#6B4C9A"

# Compatibility alias: the pre-Phase-C generate.py scripts name the primary
# series colour NAVY.  It maps onto the conventions blue.
NAVY = BLUE


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
            "axes.grid": True,
            "grid.color": GRID,
            "grid.linewidth": 0.7,
            "grid.alpha": 1.0,
            "legend.frameon": False,
            "lines.linewidth": 1.5,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )



def ramp(n: int, dark: str = BLUE):
    """`n` shades of one hue, light to dark, for an *ordered* series.

    Ordered categories -- successive times, founding multiplicities, nested
    conditionings -- read as a sequence when they share a hue and differ in
    lightness.  Distinct hues are reserved for series that genuinely contrast.
    """
    import matplotlib.colors as mcolors

    base = mcolors.to_rgb(dark)
    # interpolate from 30% toward white down to the full hue
    return [
        mcolors.to_hex(tuple(c + (1.0 - c) * f for c in base))
        for f in [0.62 * (1.0 - i / max(n - 1, 1)) for i in range(n)]
    ]


def panel_label(ax, tag: str, dx: float = 0.012, dy: float = 1.015) -> None:
    """Bare panel label above the axes, top left.

    The calibration chapters put nothing else inside the graphic: no titles,
    no suptitles, just `(a)`, `(b)`, `(c)`.  Everything explanatory belongs in
    the caption.
    """
    ax.text(dx, dy, tag, transform=ax.transAxes,
            ha="left", va="bottom", fontweight="bold")


def save_figure(fig, pdf_path: Path, png_path: Path, dpi=None) -> None:
    """Write the vector PDF the chapter includes, plus a raster preview.

    `dpi` is accepted for compatibility with the older generation scripts;
    it applies to the PNG preview only, the PDF being vector throughout.
    """
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    png_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(pdf_path, bbox_inches="tight")
    fig.savefig(png_path, bbox_inches="tight", **({"dpi": dpi} if dpi else {}))
