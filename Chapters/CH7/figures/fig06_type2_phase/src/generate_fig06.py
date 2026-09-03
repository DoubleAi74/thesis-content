#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figure 6 -- Type-2 roots and phase line (autonomous Riccati geometry).

Makes the geometry of the autonomous type-2 equation obvious:

    (a) the right-hand side  f(G) = lam2 G^2 - (lam2+mu2+del2) G + mu2,
        its two roots r_{2,-} < 1 < r_{2,+}, and the admissible band [0,1];
    (b) the 1-D phase line of  dG/dt = f(G): flow arrows, the stable
        equilibrium r_{2,-} and the repelling equilibrium r_{2,+};
    (c) a short physical-time series G(t) from G(0)=1 decaying to r_{2,-},
        the forever-avoidance probability, validated against RK4.

Panels (a) and (b) share the G axis, so the zeros of f(G) sit directly
above the phase-line equilibria.

Method: numpy + matplotlib only. Roots solved analytically as in the paper
(eq:type2-roots); the closed form (eq:G-solution-unscaled) is checked against
an independent fixed-step RK4 integration of the unscaled ODE (eq:G-unscaled).
No AI, no fitting.

Reference: sections/03_autonomous.tex, sections/02_model.tex.

Regenerate:
    /opt/homebrew/bin/python3.14 generate_fig06.py
"""

import os
import sys
import json
import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# ---------------------------------------------------------------------------
# Palette (paper / visualiser baseline; Okabe-Ito, colour-blind safe)
# ---------------------------------------------------------------------------
VERM = "#D55E00"   # type 2 / G  -- emphasis
INK  = "#1a1c1f"   # axes, strong ink
SOFT = "#565b62"   # secondary annotation
GRID = "#e3e6ea"   # light rules
BAND = "#eef0f2"   # [0,1] admissible-probability shading
GREEN = "#2e7d32"  # "agree" accent (RK4 validation / limit)
VERM_FILL = "#D55E00"

# ---------------------------------------------------------------------------
# Typography -- serif body, Computer Modern maths (matches paper + GW chapter)
# ---------------------------------------------------------------------------
mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman", "Times"],
    "mathtext.fontset": "cm",
    "axes.linewidth": 0.9,
    "axes.edgecolor": INK,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.width": 0.9,
    "ytick.major.width": 0.9,
    "xtick.color": INK,
    "ytick.color": INK,
    "text.color": INK,
    "axes.labelcolor": INK,
    "savefig.dpi": 300,
    "figure.dpi": 130,
})

# ===========================================================================
# 1. Physical rates and the autonomous type-2 quadratic
# ===========================================================================
# Parameters chosen for a clear root gap (see prompt fig_gen_6).
lam2, mu2, del2 = 0.9, 0.35, 0.20
lam1 = 1.0                      # type-1 birth timescale; here physical == scaled

# RHS of the unscaled type-2 ODE  dG/dt = f(G)   (eq:G-unscaled)
b = lam2 + mu2 + del2           # linear coefficient magnitude, = 1.45

def f(G):
    """Right-hand side f(G) = lam2 G^2 - (lam2+mu2+del2) G + mu2."""
    return lam2 * G**2 - b * G + mu2

# ---- Analytic roots (eq:Delta2, eq:type2-roots) ---------------------------
Delta2 = np.sqrt(b**2 - 4.0 * lam2 * mu2)     # hat-Delta_2 (lam1 = 1)
r_minus = (b - Delta2) / (2.0 * lam2)
r_plus  = (b + Delta2) / (2.0 * lam2)
alpha2  = r_plus - r_minus                    # root gap = Delta2 / lam2
q2      = -Delta2                             # scaled decay rate  hat-q_2 = -hat-Delta_2

# ---- Analytic self-checks -------------------------------------------------
assert 0.0 <= r_minus < 1.0 < r_plus, "root ordering 0 <= r- < 1 < r+ failed"
assert np.isclose(r_minus + r_plus, b / lam2)          # sum of roots
assert np.isclose(r_minus * r_plus, mu2 / lam2)        # product of roots
assert np.isclose(f(r_minus), 0.0) and np.isclose(f(r_plus), 0.0)
assert np.isclose(f(0.0), mu2)                          # f(0) = mu2 > 0
assert np.isclose(f(1.0), -del2)                        # f(1) = -del2 < 0
assert np.isclose(alpha2, Delta2 / lam2)

# ===========================================================================
# 2. Closed-form solution and independent RK4 validation
# ===========================================================================
# Closed form (eq:G-solution-unscaled) in physical time t (lam1 = 1 => t-hat = t)
z20 = (r_minus - 1.0) / (r_plus - 1.0)          # z_{2,0} < 0

def G_closed(t):
    z = z20 * np.exp(q2 * lam1 * t)             # z_2(t) = z_{2,0} e^{q2 t}
    return r_minus - alpha2 * z / (1.0 - z)

# checks: G(0)=1, G'(0)=-del2, G(inf)=r_minus
assert np.isclose(G_closed(0.0), 1.0)
_hh = 1e-6
assert abs((G_closed(_hh) - G_closed(0.0)) / _hh + del2) < 1e-3
assert np.isclose(G_closed(60.0), r_minus, atol=1e-6)

def rk4(rhs, y0, t0, t1, dt):
    """Fixed-step classical RK4 for a scalar autonomous ODE y' = rhs(y)."""
    n = int(round((t1 - t0) / dt))
    ts = t0 + dt * np.arange(n + 1)
    ys = np.empty(n + 1)
    ys[0] = y = y0
    for i in range(1, n + 1):
        k1 = rhs(y)
        k2 = rhs(y + 0.5 * dt * k1)
        k3 = rhs(y + 0.5 * dt * k2)
        k4 = rhs(y + dt * k3)
        y += dt * (k1 + 2.0 * k2 + 2.0 * k3 + k4) / 6.0
        ys[i] = y
    return ts, ys

T_MAX = 12.0
DT = 0.001
t_rk, G_rk = rk4(f, 1.0, 0.0, T_MAX, DT)
max_err = float(np.max(np.abs(G_rk - G_closed(t_rk))))
assert max_err < 1e-5, f"closed form vs RK4 disagree: max_err={max_err:.2e}"

print("Type-2 autonomous geometry")
print(f"  lam2={lam2}, mu2={mu2}, del2={del2}  (lam1={lam1})")
print(f"  Delta2   = {Delta2:.9f}")
print(f"  r_2,-    = {r_minus:.9f}   (stable, = lim G(t))")
print(f"  r_2,+    = {r_plus:.9f}   (repelling)")
print(f"  alpha2   = {alpha2:.9f}   root gap")
print(f"  q2 (hat) = {q2:.9f}       decay rate")
print(f"  z_2,0    = {z20:.9f}")
print(f"  closed form vs RK4 (dt={DT}, t<= {T_MAX}): max abs err = {max_err:.2e}")

# ===========================================================================
# 3. Figure
# ===========================================================================
GXMIN, GXMAX = -0.05, 1.55           # shared G-axis for panels (a) and (b)

fig = plt.figure(figsize=(12.2, 5.5))
gs = fig.add_gridspec(
    2, 2,
    width_ratios=[1.18, 1.0],
    height_ratios=[3.05, 1.0],
    hspace=0.10, wspace=0.20,
    left=0.075, right=0.986, top=0.90, bottom=0.115,
)
axA = fig.add_subplot(gs[0, 0])
axB = fig.add_subplot(gs[1, 0], sharex=axA)
axC = fig.add_subplot(gs[:, 1])


def panel_tag(ax, s, x=0.017, y=0.955):
    ax.text(x, y, s, transform=ax.transAxes, ha="left", va="top",
            fontsize=13.5, fontweight="bold", color=INK)


# ---------------------------------------------------------------------------
# Panel (a): the right-hand side f(G)
# ---------------------------------------------------------------------------
Gg = np.linspace(GXMIN, GXMAX, 1000)
fg = f(Gg)

# admissible probability band [0,1]
axA.axvspan(0.0, 1.0, color=BAND, zorder=0)
# zero line
axA.axhline(0.0, color=INK, lw=0.9, zorder=2)

# faint warmth under the positive lobes (ties to the f>0 flow direction);
# the negative well is left clear so it does not double up with the band.
axA.fill_between(Gg, 0, fg, where=(fg > 0), color=VERM, alpha=0.10,
                 interpolate=True, zorder=1)

# the curve
axA.plot(Gg, fg, color=VERM, lw=2.4, zorder=5, solid_capstyle="round")

# roots as filled markers on the G-axis
for rr in (r_minus, r_plus):
    axA.plot([rr], [0.0], "o", ms=9, mfc=VERM, mec="white", mew=1.4, zorder=6)

# endpoint witness f(0)=mu2>0 (the sign-change argument)
axA.plot([0.0], [mu2],  "o", ms=6.5, mfc="white", mec=INK, mew=1.4, zorder=6)
axA.annotate(r"$f(0)=\mu_2>0$", xy=(0.0, mu2), xytext=(0.075, 0.40),
             fontsize=10.5, color=INK, va="center",
             arrowprops=dict(arrowstyle="-", color=SOFT, lw=0.8,
                             shrinkA=0, shrinkB=3))

# root labels
axA.annotate(r"$r_{2,-}\approx %.3f$" % r_minus, xy=(r_minus, 0.0),
             xytext=(r_minus - 0.02, 0.175), ha="center", fontsize=11,
             color=VERM,
             arrowprops=dict(arrowstyle="-", color=VERM, lw=0.9,
                             shrinkA=1, shrinkB=4))
axA.annotate(r"$r_{2,+}\approx %.3f$" % r_plus, xy=(r_plus, 0.0),
             xytext=(r_plus + 0.005, 0.135), ha="center", fontsize=11,
             color=VERM,
             arrowprops=dict(arrowstyle="-", color=VERM, lw=0.9,
                             shrinkA=1, shrinkB=4))

# sign-of-f flags (these become the arrow directions in panel b)
axA.text(0.145, -0.055, r"$f>0$", color=SOFT, fontsize=9.5, ha="center")
axA.text(0.80, -0.055, r"$f<0$", color=SOFT, fontsize=9.5, ha="center")
axA.text(1.45, -0.055, r"$f>0$", color=SOFT, fontsize=9.5, ha="center")

axA.text(0.95, 0.455, "probability range  $[0,1]$", color=SOFT, fontsize=9.5,
         ha="right", va="center", style="italic")

axA.set_ylim(-0.32, 0.52)
axA.set_ylabel(r"$f(G)=\dot G$", fontsize=13)
axA.set_title(
    r"$f(G)=\lambda_2\,(G-r_{2,-})(G-r_{2,+})$",
    fontsize=12.5, pad=9, color=INK)
panel_tag(axA, "(a)")
axA.grid(True, color=GRID, lw=0.6, alpha=0.7, zorder=0)
axA.tick_params(labelbottom=False, labelsize=10.5, length=4, top=True, right=True)

# ---------------------------------------------------------------------------
# Panel (b): the phase line of  dG/dt = f(G)
#   number line drawn at y=0; ticks + G-labels hang below, everything
#   descriptive rides above, so nothing collides with the shared axis.
# ---------------------------------------------------------------------------
axB.axvspan(0.0, 1.0, color=BAND, zorder=0)
axB.axhline(0.0, color=INK, lw=1.5, zorder=3, solid_capstyle="round")


def flow_arrow(ax, x0, x1, color, lw=3.0):
    ax.add_patch(FancyArrowPatch(
        (x0, 0.0), (x1, 0.0),
        arrowstyle="-|>", mutation_scale=20, lw=lw, color=color,
        shrinkA=0, shrinkB=0, zorder=4, capstyle="round"))


HL = 0.058  # half-length of a flow arrow, in G units
FLANK = 0.15  # symmetric offset of the arrows flanking the stable root r_{2,-}
# flow toward the stable root from the left  (f>0  ->  moving right)
flow_arrow(axB, (r_minus - FLANK) - HL, (r_minus - FLANK) + HL, INK)
# flow toward the stable root from the right (f<0  ->  moving left)
for c in (r_minus + FLANK, 0.75, 1.20):
    flow_arrow(axB, c + HL, c - HL, INK)
# repelled beyond the upper root           (f>0  ->  moving right)
flow_arrow(axB, 1.40, 1.40 + 2 * HL, SOFT)

# equilibria: filled = stable, open = unstable (standard convention)
axB.plot([r_minus], [0.0], "o", ms=16, mfc=VERM, mec="white", mew=1.8,
         zorder=6, clip_on=False)
axB.plot([r_plus], [0.0], "o", ms=16, mfc="white", mec=VERM, mew=2.8,
         zorder=6, clip_on=False)

# equilibrium names ride just above the line (symbol on top, role below)
axB.annotate(r"$r_{2,-}$", xy=(r_minus, 0.0), xytext=(r_minus, 0.47),
             ha="center", va="bottom", fontsize=13, color=VERM)
axB.annotate(r"$r_{2,+}$", xy=(r_plus, 0.0), xytext=(r_plus, 0.47),
             ha="center", va="bottom", fontsize=13, color=VERM)

# initial condition G(0)=1 sits inside (r-, r+); it slides left to r_minus
axB.plot([1.0], [0.0], marker="v", ms=9, mfc=INK, mec="white", mew=1.0,
         zorder=7, clip_on=False)
axB.annotate(r"$G(0)=1$", xy=(1.0, 0.06), xytext=(1.0, 0.86), ha="center",
             va="bottom", fontsize=10.5, color=INK,
             arrowprops=dict(arrowstyle="-", color=SOFT, lw=0.8,
                             shrinkA=2, shrinkB=2))

axB.set_ylim(-0.58, 1.18)
axB.set_yticks([])
axB.set_xlim(GXMIN, GXMAX)
axB.set_xlabel(r"$G$", fontsize=13, labelpad=2)
panel_tag(axB, "(b)", y=0.92)
# move the x-axis onto the number line; ticks point down, labels below.
# the thin bottom spine sits under the thicker phase-line axhline and only
# carries the tick marks.
axB.spines["bottom"].set_position(("data", 0.0))
axB.spines["bottom"].set_linewidth(0.9)
for sp in ("left", "right", "top"):
    axB.spines[sp].set_visible(False)
axB.tick_params(axis="x", labelsize=10.5, length=5, width=0.9, color=INK,
                direction="out", top=False, pad=5)

# ---------------------------------------------------------------------------
# Panel (c): physical-time relaxation  G(t): 1 -> r_{2,-}
# ---------------------------------------------------------------------------
tt = np.linspace(0.0, T_MAX, 700)
Gt = G_closed(tt)

# limit line r_{2,-}
axC.axhline(r_minus, ls=(0, (6, 4)), color=GREEN, lw=1.4, zorder=2)
# closed-form curve
axC.plot(tt, Gt, color=VERM, lw=2.4, zorder=4, solid_capstyle="round",
         label="closed form  " r"$G(t)$")

# start point (initial condition is self-evident from the curve's origin)
axC.plot([0.0], [1.0], "o", ms=8, mfc=VERM, mec="white", mew=1.4, zorder=6)
axC.text(0.62, 0.923, r"$G(0)=1,\;\; G'(0)=-\delta_2$", fontsize=10.5,
         color=INK, va="center", ha="left")

# meaning of the limit -- one line below the horizontal asymptote (no leader arrow)
axC.text(7.0, r_minus - 0.048,
         r"$r_{2,-}=\lim_{t\to\infty}G(t)"
         r"=\mathbb{P}(\mathrm{catastrophe\ avoided\ forever})$",
         fontsize=10.5, color=GREEN, va="center", ha="center")
axC.text(11.7, r_minus + 0.030, r"$%.3f$" % r_minus, fontsize=10,
         color=GREEN, va="bottom", ha="right")

axC.set_xlim(0.0, T_MAX)
axC.set_ylim(0.20, 1.035)
axC.set_xlabel(r"physical time  $t$", fontsize=13)
axC.set_ylabel(r"$G(t)$", fontsize=13)
panel_tag(axC, "(c)")
axC.grid(True, color=GRID, lw=0.6, alpha=0.7, zorder=0)
axC.tick_params(labelsize=10.5, length=4, top=True, right=True)
leg = axC.legend(loc="upper right", frameon=True, framealpha=0.96,
                 edgecolor=GRID, fontsize=10, borderpad=0.6,
                 handletextpad=0.6)
leg.get_frame().set_linewidth(0.8)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, ".."))
png = os.path.join(OUT, "fig06.png")
pdf = os.path.join(OUT, "fig06.pdf")
fig.savefig(png, dpi=300)
fig.savefig(pdf)
print(f"\nwrote {png}")
print(f"wrote {pdf}")

# ---------------------------------------------------------------------------
# Machine-readable metadata
# ---------------------------------------------------------------------------
meta = {
    "figure": "fig06_type2_phase",
    "description": "Autonomous type-2 roots, phase line, and relaxation G(t).",
    "parameters": {"lambda1": lam1, "lambda2": lam2, "mu2": mu2, "delta2": del2},
    "derived": {
        "Delta2": Delta2,
        "r_2_minus": r_minus,
        "r_2_plus": r_plus,
        "alpha2_root_gap": alpha2,
        "q2_decay_rate": q2,
        "z2_0": z20,
    },
    "root_ordering_ok": bool(0.0 <= r_minus < 1.0 < r_plus),
    "validation": {
        "method": "fixed-step RK4 of unscaled dG/dt=f(G)",
        "dt": DT, "t_max": T_MAX,
        "max_abs_error_closed_vs_rk4": max_err,
    },
    "tools": {
        "python": "Python " + sys.version.split()[0],
        "numpy": np.__version__,
        "matplotlib": mpl.__version__,
    },
    "seed": None,
    "ai_used": False,
}
with open(os.path.join(OUT, "meta.json"), "w") as fh:
    json.dump(meta, fh, indent=2)
print(f"wrote {os.path.join(OUT, 'meta.json')}")
