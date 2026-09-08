#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Figure 02 - Path-dependent catastrophe exposure.

Pedagogical multi-panel figure for the two-type birth-death-conversion model
with a global catastrophe of hazard  lambda(t) = delta1 * X_t + delta2 * Y_t.

Two DETERMINISTIC, hand-designed illustrative population histories share the
same initial state (1,0) and the same terminal state (2,1) at t = T, yet
accumulate very different type-weighted exposure and hence very different
path-wise no-catastrophe weights  exp(-\int_0^t lambda ds)  (the Feynman-Kac
integrand of Prop. 2.1 / eq. (10) in the paper).

These are illustrative paths, NOT ensemble averages.  No random-number
generator is used, so the output is bit-for-bit reproducible.

Requires: numpy, matplotlib.  A LaTeX install (TeX Live) enables authentic
Computer Modern typography; the script falls back to matplotlib mathtext (cm)
if LaTeX is unavailable.

Run:
    python3 make_fig02.py
Outputs (written next to the src/ folder, i.e. in fig02_path_exposure/):
    fig02.png, fig02.pdf, paths.json, meta.json
"""

import os
import sys
import json
import datetime

# --- make a system TeX Live visible to matplotlib usetex, if present --------
for _texbin in (
    "/usr/local/texlive/2024/bin/universal-darwin",
    "/usr/local/texlive/2023/bin/universal-darwin",
    "/Library/TeX/texbin",
    "/usr/local/bin",
):
    if os.path.isdir(_texbin) and _texbin not in os.environ.get("PATH", ""):
        os.environ["PATH"] = _texbin + os.pathsep + os.environ["PATH"]

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ===========================================================================
# 1.  Parameters
# ===========================================================================
# Per-capita catastrophe-hazard weights.  The paper's worked example suggests
# (delta1, delta2) = (0.15, 0.25); over the horizon T = 10 with a genuine
# early boom those weights drive exp(-\int lambda) below ~1e-3, which hugs zero
# on a linear axis.  We keep the paper's ordering delta2 > delta1 (type-2
# individuals are more hazardous per unit time) but scale both down so that a
# vivid boom-versus-small contrast still leaves BOTH path-wise weights legible
# on a linear axis.  The pedagogical point -- path dependence -- is unchanged.
DELTA1 = 0.06          # type-1 per-capita hazard weight
DELTA2 = 0.10          # type-2 per-capita hazard weight
T = 10.0               # physical-time horizon (unscaled)

# Deterministic, hand-designed integer-valued histories.
# Each row (t, X, Y) fixes the state held from time t until the next row;
# the final row's state is held until t = T.  Both paths start at (1,0)
# and end at (2,1).
PATH_A = [           # early boom to 6, then a slow die-back
    (0.0, 1, 0),
    (0.5, 2, 0),
    (0.9, 3, 0),
    (1.4, 4, 0),
    (1.9, 5, 0),
    (2.5, 6, 0),     # peak of 6, held ~1.1 time units
    (3.6, 5, 1),     # first conversion 1 -> 2, decline begins
    (4.6, 4, 1),
    (5.8, 3, 1),
    (7.8, 2, 1),     # terminal state (2,1), held to T
]

PATH_B = [           # lingers at a single individual, blooms only late
    (0.0, 1, 0),
    (5.8, 2, 0),     # first birth, late
    (6.6, 1, 1),     # conversion 1 -> 2
    (7.6, 2, 1),     # grows to terminal (2,1), held to T
]

# ===========================================================================
# 2.  Palette (baseline from SHARED_CONVENTIONS.md)
# ===========================================================================
C_TYPE1 = "#0072B2"   # type 1 / X  (blue)
C_TYPE2 = "#D55E00"   # type 2 / Y  (vermillion)
INK = "#1a1c1f"       # axes / primary text
SOFT = "#565b62"      # secondary annotation text
GRID = "#e3e6ea"      # light rules
# One extra muted hue (permitted): the *derived* catastrophe quantities
# (the combined hazard and the survival weight) that belong to neither type.
C_DERV = "#6B4C9A"    # muted purple
C_DERV_FILL = "#6B4C9A"

# ===========================================================================
# 3.  Path -> curves and exact occupation-time integrals
# ===========================================================================
def segments(path):
    """Yield (t0, t1, x, y) segments; last segment runs to T."""
    out = []
    for i, (t, x, y) in enumerate(path):
        t1 = path[i + 1][0] if i + 1 < len(path) else T
        out.append((t, t1, float(x), float(y)))
    return out


def step_arrays(path, key):
    """Breakpoint arrays suitable for a 'steps-post' plot of X, Y or lambda."""
    segs = segments(path)
    ts, vs = [], []
    for t0, t1, x, y in segs:
        val = {"X": x, "Y": y, "lam": DELTA1 * x + DELTA2 * y}[key]
        ts.append(t0)
        vs.append(val)
    ts.append(T)
    vs.append(vs[-1])
    return np.asarray(ts), np.asarray(vs)


def exposure_integral(path):
    r"""Exact \int_0^T (delta1 X + delta2 Y) dt, plus type-split person-times."""
    sx = sy = 0.0
    for t0, t1, x, y in segments(path):
        dt = t1 - t0
        sx += x * dt
        sy += y * dt
    return DELTA1 * sx + DELTA2 * sy, sx, sy


def cumulative(path, grid):
    r"""
    Exact cumulative exposure Lambda(t)=\int_0^t lambda ds and weight
    W(t)=exp(-Lambda) evaluated on `grid`.  lambda is piecewise constant, so
    Lambda is piecewise linear and this is analytic (no quadrature error).
    """
    segs = segments(path)
    bpt = np.array([s[0] for s in segs] + [T])          # breakpoint times
    lam = np.array([DELTA1 * s[2] + DELTA2 * s[3] for s in segs])  # per segment
    Lam_bp = np.concatenate([[0.0], np.cumsum(lam * np.diff(bpt))])  # at bpts
    # locate each grid point in its segment
    idx = np.clip(np.searchsorted(bpt, grid, side="right") - 1, 0, len(lam) - 1)
    Lam = Lam_bp[idx] + lam[idx] * (grid - bpt[idx])
    return Lam, np.exp(-Lam)


# Fine grid that INCLUDES every breakpoint (so an independent trapezoid check
# is exact to machine precision -- our quantitative validation).
def build_grid(n=4000):
    base = np.linspace(0.0, T, n)
    bpts = np.unique(
        np.concatenate([[s[0] for s in segments(PATH_A)],
                        [s[0] for s in segments(PATH_B)], [T]])
    )
    # straddle each jump with points at t +/- eps so an independent trapezoid
    # rule resolves the step discontinuities (validation to ~1e-8).
    eps = 1e-7
    straddle = np.concatenate([bpts - eps, bpts + eps])
    g = np.unique(np.concatenate([base, bpts, straddle]))
    return g[(g >= 0.0) & (g <= T)]


grid = build_grid()
LamA, WA = cumulative(PATH_A, grid)
LamB, WB = cumulative(PATH_B, grid)

IA, sxA, syA = exposure_integral(PATH_A)
IB, sxB, syB = exposure_integral(PATH_B)
WA_T, WB_T = float(WA[-1]), float(WB[-1])
lamT = DELTA1 * 2 + DELTA2 * 1          # terminal hazard, identical for both
ratio_weight = WB_T / WA_T
ratio_expo = IA / IB

# --- quantitative validation: analytic Lambda vs independent trapezoid ------
def lam_on_grid(path, g):
    ts, vs = step_arrays(path, "lam")
    idx = np.clip(np.searchsorted(ts, g, side="right") - 1, 0, len(vs) - 2)
    return vs[idx]

lamA_g = lam_on_grid(PATH_A, grid)
lamB_g = lam_on_grid(PATH_B, grid)
trapA = np.concatenate([[0.0], np.cumsum(0.5 * (lamA_g[1:] + lamA_g[:-1]) * np.diff(grid))])
trapB = np.concatenate([[0.0], np.cumsum(0.5 * (lamB_g[1:] + lamB_g[:-1]) * np.diff(grid))])
max_err = float(max(np.max(np.abs(trapA - LamA)), np.max(np.abs(trapB - LamB))))

print("=" * 68)
print("Figure 02  --  path-dependent catastrophe exposure")
print("=" * 68)
print(f"delta1 = {DELTA1},  delta2 = {DELTA2},  T = {T}")
print(f"Path A: start (1,0) -> terminal (2,1) | "
      f"int(lambda)={IA:.3f}  W={WA_T:.4f}  (X-time {sxA:.1f}, Y-time {syA:.1f})")
print(f"Path B: start (1,0) -> terminal (2,1) | "
      f"int(lambda)={IB:.3f}  W={WB_T:.4f}  (X-time {sxB:.1f}, Y-time {syB:.1f})")
print(f"terminal hazard lambda(T) = {lamT:.3f} (both paths)")
print(f"exposure ratio  A/B = {ratio_expo:.2f}")
print(f"weight ratio    B/A = {ratio_weight:.2f}")
print(f"validation: max |trapezoid - analytic Lambda| = {max_err:.2e}")

# ===========================================================================
# 4.  Typography
# ===========================================================================
def enable_latex():
    try:
        matplotlib.rcParams.update({
            "text.usetex": True,
            "font.family": "serif",
            "font.serif": ["Computer Modern Roman"],
            "text.latex.preamble": r"\usepackage{amsmath}\usepackage{amssymb}",
        })
        fig = plt.figure()
        fig.text(0.5, 0.5, r"$\lambda_1\,\delta_2$")
        fig.canvas.draw()
        plt.close(fig)
        return True
    except Exception as exc:                       # pragma: no cover
        print("  [typography] usetex unavailable, using mathtext cm:", exc)
        matplotlib.rcParams.update({
            "text.usetex": False,
            "font.family": "serif",
            "font.serif": ["STIX Two Text", "DejaVu Serif"],
            "mathtext.fontset": "cm",
        })
        return False

USETEX = enable_latex()
plt.rcParams.update({
    "axes.edgecolor": INK, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK, "text.color": INK,
    "axes.linewidth": 1.1, "axes.labelpad": 5.0,
    "xtick.direction": "out", "ytick.direction": "out",
    "font.size": 15,
})
BF = (lambda s: r"\textbf{" + s + "}") if USETEX else (lambda s: s)


def style_axes(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(True, color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlim(-0.15, T + 0.15)
    ax.set_xlabel(r"time $t$")
    ax.tick_params(length=4, labelsize=13)
    ax.set_xticks([0, 2, 4, 6, 8, 10])


# ===========================================================================
# 5.  Figure
# ===========================================================================
fig, axs = plt.subplots(2, 2, figsize=(12.4, 9.4))
(axA, axB), (axC, axD) = axs
YMAX = 6.7

# ---- (a) Path A counts -----------------------------------------------------
def plot_counts(ax, path, ls, tag, title):
    tX, vX = step_arrays(path, "X")
    tY, vY = step_arrays(path, "Y")
    ax.step(tX, vX, where="post", color=C_TYPE1, lw=2.6, ls=ls,
            label=r"type 1 $X_t$", zorder=4, solid_capstyle="round")
    ax.step(tY, vY, where="post", color=C_TYPE2, lw=2.6, ls=ls,
            label=r"type 2 $Y_t$", zorder=3, solid_capstyle="round")
    style_axes(ax)
    ax.set_ylim(-0.35, YMAX)
    ax.set_yticks(range(0, 7))
    ax.set_ylabel("individuals")
    ax.set_title(BF(tag) + " " + title, loc="left", fontsize=15, pad=8)
    # start and terminal markers (shared by both paths)
    ax.plot(0, 1, "o", ms=7, mfc="white", mec=INK, mew=1.6, zorder=6)
    ax.plot(T, 2, "o", ms=7, mfc=C_TYPE1, mec="white", mew=1.4, zorder=6)
    ax.plot(T, 1, "o", ms=7, mfc=C_TYPE2, mec="white", mew=1.4, zorder=6)
    ax.legend(loc="upper right", fontsize=12, frameon=True, framealpha=0.95,
              edgecolor=GRID, handlelength=1.9, borderpad=0.5)


plot_counts(axA, PATH_A, "-", "(a)", "Path A: early expansion, then die-back")
plot_counts(axB, PATH_B, (0, (5, 2)), "(b)", "Path B: small for long, increases late")

# ---- (c) instantaneous hazard ---------------------------------------------
tLA, vLA = step_arrays(PATH_A, "lam")
tLB, vLB = step_arrays(PATH_B, "lam")
axC.fill_between(tLA, 0, vLA, step="post", color=C_DERV_FILL, alpha=0.16, zorder=1)
axC.fill_between(tLB, 0, vLB, step="post", color=C_DERV_FILL, alpha=0.16, zorder=2,
                 hatch="////", edgecolor=C_DERV, linewidth=0.0)
axC.step(tLA, vLA, where="post", color=C_DERV, lw=2.6, ls="-",
         label="Path A", zorder=5, solid_capstyle="round")
axC.step(tLB, vLB, where="post", color=C_DERV, lw=2.6, ls=(0, (5, 2)),
         label="Path B", zorder=5)
style_axes(axC)
axC.set_ylim(0, 0.66)
axC.set_ylabel(r"hazard $\lambda(t)$")
axC.set_title(BF("(c)") + r" Instantaneous hazard $\lambda=\delta_1 X_t+\delta_2 Y_t$",
              loc="left", fontsize=15, pad=8)
# exposure numbers stacked in the top-right of panel (c)
axC.text(0.98, 0.96, r"Path A: $\int_0^{10}\!\lambda\,dt\approx %.1f$" % IA,
         transform=axC.transAxes, fontsize=13.5, color=C_DERV,
         ha="right", va="top", zorder=6)
axC.text(0.98, 0.86, r"Path B: $\int_0^{10}\!\lambda\,dt\approx %.1f$" % IB,
         transform=axC.transAxes, fontsize=13.5, color=C_DERV,
         ha="right", va="top", zorder=6)
# terminal hazard: both curves meet at lambda(10)
axC.plot(T, lamT, "o", ms=7, mfc=C_DERV, mec="white", mew=1.4, zorder=6)

# ---- (d) path-wise no-catastrophe weight ----------------------------------
axD.plot(grid, WA, color=C_DERV, lw=2.8, ls="-", label="Path A", zorder=4)
axD.plot(grid, WB, color=C_DERV, lw=2.8, ls=(0, (5, 2)), label="Path B", zorder=4)
style_axes(axD)
axD.set_ylim(0, 1.035)
axD.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
axD.set_ylabel(r"weight $\exp\!\left(-\int_0^t\lambda\,ds\right)$")
axD.set_title(BF("(d)") + r" Path-wise no-catastrophe weight",
              loc="left", fontsize=15, pad=8)
# terminal weight markers
axD.plot(T, WA_T, "o", ms=7.5, mfc=C_DERV, mec="white", mew=1.4, zorder=6)
axD.plot(T, WB_T, "o", ms=7.5, mfc=C_DERV, mec="white", mew=1.4, zorder=6)
axD.legend(loc="center right", fontsize=12, frameon=True, framealpha=0.95,
           edgecolor=GRID, handlelength=2.4, bbox_to_anchor=(1.0, 0.87))

fig.tight_layout()
fig.subplots_adjust(hspace=0.34, wspace=0.24)

# ===========================================================================
# 6.  Save
# ===========================================================================
here = os.path.dirname(os.path.abspath(__file__))
outdir = os.path.dirname(here)          # fig02_path_exposure/
png = os.path.join(outdir, "fig02.png")
pdf = os.path.join(outdir, "fig02.pdf")
fig.savefig(png, dpi=300, facecolor="white", bbox_inches="tight")
fig.savefig(pdf, facecolor="white", bbox_inches="tight")
print(f"\nwrote {png}")
print(f"wrote {pdf}")

# ---- paths.json + meta.json -----------------------------------------------
paths_doc = {
    "description": "Deterministic hand-designed illustrative population "
                   "histories (t, X, Y); state held from t until the next row; "
                   "final row held to T. Both start (1,0), both end (2,1).",
    "T": T, "delta1": DELTA1, "delta2": DELTA2,
    "path_A": [{"t": t, "X": x, "Y": y} for (t, x, y) in PATH_A],
    "path_B": [{"t": t, "X": x, "Y": y} for (t, x, y) in PATH_B],
}
with open(os.path.join(outdir, "paths.json"), "w") as fh:
    json.dump(paths_doc, fh, indent=2)

meta = {
    "figure": "fig02_path_exposure",
    "generated": datetime.datetime.now().isoformat(timespec="seconds"),
    "deterministic": True, "seed": None,
    "parameters": {"delta1": DELTA1, "delta2": DELTA2, "T": T},
    "results": {
        "exposure_A": IA, "exposure_B": IB,
        "weight_A": WA_T, "weight_B": WB_T,
        "terminal_hazard": lamT,
        "exposure_ratio_A_over_B": ratio_expo,
        "weight_ratio_B_over_A": ratio_weight,
        "person_time": {"A": {"X": sxA, "Y": syA}, "B": {"X": sxB, "Y": syB}},
    },
    "validation": {"max_abs_trapezoid_vs_analytic_Lambda": max_err,
                   "note": "lambda is piecewise constant, so the exposure "
                           "integral Lambda(t) is computed in closed form; an "
                           "independent trapezoidal quadrature on a grid that "
                           "straddles every jump agrees to the reported "
                           "tolerance (limited only by the +/-1e-7 straddle)."},
    "typography": "usetex" if USETEX else "mathtext-cm",
    "tool_versions": {"python": sys.version.split()[0],
                      "numpy": np.__version__,
                      "matplotlib": matplotlib.__version__},
}
with open(os.path.join(outdir, "meta.json"), "w") as fh:
    json.dump(meta, fh, indent=2)
print("wrote paths.json, meta.json")
