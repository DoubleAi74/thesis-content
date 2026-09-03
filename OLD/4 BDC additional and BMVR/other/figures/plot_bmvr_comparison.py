#!/usr/bin/env python3
"""
Overlay classical BMVR vs burst-aware renewal BMVR for several parameter sets.
Writes PDF figures into this directory.
"""
from __future__ import annotations

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

OUTDIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Single-cell BDC closed forms
# ---------------------------------------------------------------------------

def bdc_roots(beta: float, mu: float, delta: float):
    eta = (beta + mu + delta) / (2.0 * beta)
    disc = np.sqrt(eta**2 - mu / beta)
    a = eta + disc
    b = eta - disc
    A = a - 1.0
    B = 1.0 - b
    theta = beta * (a - b)
    return a, b, A, B, theta


def kernels(t: np.ndarray, beta: float, mu: float, delta: float):
    """Return Ihat(t), J(t), K(t), g(t)=delta*K, I(t) on grid t."""
    a, b, A, B, theta = bdc_roots(beta, mu, delta)
    # stable evaluation of Ihat for large theta*t
    wt = np.exp(theta * t)
    # I(t)
    I = (a * B + b * A * wt) / (B + A * wt)
    # D(t) — only used for checks; prefer direct Ihat form
    denom_D = a * wt - b
    # Ihat closed form (avoids cancellation I-D at large t)
    Ihat = (a - b) ** 2 * wt / ((B + A * wt) * denom_D)
    # numerical safety at t=0
    Ihat = np.where(t == 0.0, 1.0, Ihat)
    J = (a - b) ** 2 * wt / (B + A * wt) ** 2
    K = (1.0 + (2.0 * beta / delta) * (1.0 - I)) * J
    g = delta * K
    V_inf = a * (1.0 - b) / (a - 1.0)
    E_Tprod = (1.0 / beta) * np.log(a / (a - 1.0))
    p0 = V_inf / E_Tprod
    d0 = 1.0 / E_Tprod
    meta = dict(
        a=a, b=b, A=A, B=B, theta=theta,
        V_inf=V_inf, E_Tprod=E_Tprod, p_eff0=p0, d_eff0=d0,
    )
    return Ihat, J, K, g, I, meta


# ---------------------------------------------------------------------------
# Population models
# ---------------------------------------------------------------------------

def trap_conv_partial(V: np.ndarray, ker: np.ndarray, n: int, h: float) -> float:
    """Trapezoidal convolution (V * ker)(t_n) using V[0..n] and ker[0..n]."""
    if n == 0:
        return 0.0
    # sum_{k=0}^n w_k V[n-k] ker[k], trapezoidal endpoint weights
    s = 0.5 * V[n] * ker[0] + 0.5 * V[0] * ker[n]
    if n >= 2:
        s += np.dot(V[1:n], ker[n - 1:0:-1])
    return h * s


def solve_renewal(
    t: np.ndarray,
    Ihat: np.ndarray,
    g: np.ndarray,
    gammaT: float,
    c: float,
    I0: float,
    V0: float,
):
    """
    Forward-Euler for the linear Volterra IDE
      V' = I0 g(t) + gammaT (V * g) - c V
    Icell recovered by convolution against Ihat.
    """
    n = len(t)
    h = t[1] - t[0]
    V = np.zeros(n)
    Icell = np.zeros(n)
    V[0] = V0
    Icell[0] = I0 * Ihat[0]

    for i in range(n - 1):
        conv_g = trap_conv_partial(V, g, i, h)
        dV = I0 * g[i] + gammaT * conv_g - c * V[i]
        V[i + 1] = max(V[i] + h * dV, 0.0)

    for i in range(n):
        conv_I = trap_conv_partial(V, Ihat, i, h)
        Icell[i] = I0 * Ihat[i] + gammaT * conv_I

    return Icell, V


def solve_classical(
    t: np.ndarray,
    gammaT: float,
    c: float,
    p: float,
    dI: float,
    I0: float,
    V0: float,
):
    """RK4 for classical BMVR ODEs."""
    n = len(t)
    h = t[1] - t[0]
    I = np.zeros(n)
    V = np.zeros(n)
    I[0], V[0] = I0, V0

    def f(Ii, Vi):
        return gammaT * Vi - dI * Ii, p * Ii - c * Vi

    for i in range(n - 1):
        Ii, Vi = I[i], V[i]
        k1I, k1V = f(Ii, Vi)
        k2I, k2V = f(Ii + 0.5 * h * k1I, Vi + 0.5 * h * k1V)
        k3I, k3V = f(Ii + 0.5 * h * k2I, Vi + 0.5 * h * k2V)
        k4I, k4V = f(Ii + h * k3I, Vi + h * k3V)
        I[i + 1] = max(Ii + (h / 6.0) * (k1I + 2 * k2I + 2 * k3I + k4I), 0.0)
        V[i + 1] = max(Vi + (h / 6.0) * (k1V + 2 * k2V + 2 * k3V + k4V), 0.0)

    return I, V


# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------

SCENARIOS = [
    # Supercritical and subcritical cases; classical matched at p_eff(0), d_eff(0).
    dict(
        label=r"(a) supercritical, $\mu=0$",
        key="A",
        beta=1.0, mu=0.0, delta=0.1,
        gammaT=0.04, c=0.25, I0=5.0, V0=0.0, t_max=45.0,
    ),
    dict(
        label=r"(b) supercritical, $\mu>0$",
        key="B",
        beta=1.0, mu=0.2, delta=0.05,
        gammaT=0.03, c=0.2, I0=5.0, V0=0.0, t_max=50.0,
    ),
    dict(
        label=r"(c) fast burst (large $\delta$)",
        key="C",
        beta=1.0, mu=0.0, delta=0.5,
        gammaT=0.25, c=0.3, I0=5.0, V0=0.0, t_max=30.0,
    ),
    dict(
        label=r"(d) subcritical $R_0<1$",
        key="D",
        beta=1.0, mu=0.0, delta=0.1,
        gammaT=0.01, c=0.4, I0=20.0, V0=0.0, t_max=50.0,
    ),
    dict(
        label=r"(e) high intracellular death",
        key="E",
        beta=1.0, mu=0.9, delta=0.1,
        gammaT=0.5, c=0.25, I0=10.0, V0=0.0, t_max=40.0,
    ),
    dict(
        label=r"(f) free-virion seed only ($\mathcal{I}_0=0$)",
        key="F",
        beta=1.0, mu=0.0, delta=0.1,
        gammaT=0.05, c=0.2, I0=0.0, V0=3.0, t_max=40.0,
    ),
]


def run_scenario(sc, dt=0.01):
    t = np.arange(0.0, sc["t_max"] + dt, dt)
    Ihat, J, K, g, I_surv, meta = kernels(t, sc["beta"], sc["mu"], sc["delta"])
    gammaT, c = sc["gammaT"], sc["c"]
    I0, V0 = sc["I0"], sc["V0"]

    I_ren, V_ren = solve_renewal(t, Ihat, g, gammaT, c, I0, V0)
    I_cls, V_cls = solve_classical(
        t, gammaT, c, meta["p_eff0"], meta["d_eff0"], I0, V0
    )
    # also classical with naive p = V_inf * d_eff0  (same mean lifetime output rate matching)
    # which is actually same as p_eff0 since p_eff0 = V_inf / E_Tprod and d_eff0 = 1/E_Tprod
    # so instead use naive constant-p = QSD mean  (dimensionally wrong, scaled by unit time=1)
    p_naive = meta["a"] / (meta["a"] - 1.0)  # <X>_QS
    d_naive = meta["d_eff0"]
    I_naive, V_naive = solve_classical(t, gammaT, c, p_naive, d_naive, I0, V0)

    R0 = gammaT * meta["V_inf"] / c
    return dict(
        t=t, Ihat=Ihat, g=g, J=J,
        I_ren=I_ren, V_ren=V_ren,
        I_cls=I_cls, V_cls=V_cls,
        I_naive=I_naive, V_naive=V_naive,
        meta=meta, R0=R0, sc=sc,
    )


# ---------------------------------------------------------------------------
# Plotting style — maximise classical vs new readability
# ---------------------------------------------------------------------------

plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 11,
    "legend.fontsize": 8.5,
    "figure.dpi": 120,
    "savefig.dpi": 220,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "axes.axisbelow": True,
})

# High-contrast pair: solid blue = NEW, dashed orange = CLASSICAL
COLOR_NEW = "#0B3D91"       # solid navy
COLOR_CLS = "#E65C00"       # dashed orange
COLOR_CLS2 = "#7A1FA2"      # dash-dot purple (second classical variant)
LW_NEW = 2.8
LW_CLS = 2.6

LABEL_NEW = "NEW model  (renewal / burst-aware)"
LABEL_CLS = "CLASSICAL BMVR  (constant p and d)"
LABEL_CLS_MATCH = "CLASSICAL  (matched p = p_eff(0))"
LABEL_CLS_YOUNG = "CLASSICAL  (young-cell p = \u03b4)"
LABEL_CLS_NAIVE = "CLASSICAL  (naive p = QSD mean)"


def panel_title(res):
    sc = res["sc"]
    return (
        f"{sc['label']}\n"
        rf"$\beta={sc['beta']},\;\mu={sc['mu']},\;\delta={sc['delta']}$"
        rf"  |  $\gamma T={sc['gammaT']},\;c={sc['c']}$"
        rf"  |  $R_0={res['R0']:.2f}$"
    )


def style_legend(ax, loc="best"):
    leg = ax.legend(
        loc=loc,
        frameon=True,
        fancybox=False,
        edgecolor="0.3",
        framealpha=0.95,
        fontsize=7.5,
        borderpad=0.4,
        handlelength=2.8,
    )
    leg.get_frame().set_linewidth(0.8)
    return leg


def annotate_curve_ends(ax, t, y_new, y_cls, y_max_hint=None):
    """Label curve ends with NEW / CLASSICAL text."""
    # pick a late index where both are still visible
    i = int(0.88 * (len(t) - 1))
    ymax = y_max_hint if y_max_hint is not None else max(np.max(y_new), np.max(y_cls), 1e-12)
    # only annotate if points are in axes range-ish
    ax.annotate(
        "NEW",
        xy=(t[i], y_new[i]),
        xytext=(6, 8),
        textcoords="offset points",
        color=COLOR_NEW,
        fontsize=8,
        fontweight="bold",
        ha="left",
        va="bottom",
    )
    ax.annotate(
        "CLASSICAL",
        xy=(t[i], y_cls[i]),
        xytext=(6, -10),
        textcoords="offset points",
        color=COLOR_CLS,
        fontsize=8,
        fontweight="bold",
        ha="left",
        va="top",
    )


def plot_new_vs_classical(ax, t, y_new, y_cls, ylabel, title, mark_every=None):
    """Two-curve overlay with unmistakable styling."""
    if mark_every is None:
        mark_every = max(len(t) // 25, 1)

    ax.plot(
        t, y_new,
        color=COLOR_NEW,
        ls="-",
        lw=LW_NEW,
        solid_capstyle="round",
        label=LABEL_NEW,
        zorder=3,
    )
    ax.plot(
        t, y_cls,
        color=COLOR_CLS,
        ls="--",
        lw=LW_CLS,
        dashes=(7, 3),
        marker="o",
        markevery=mark_every,
        markersize=4.5,
        markerfacecolor="white",
        markeredgecolor=COLOR_CLS,
        markeredgewidth=1.2,
        label=LABEL_CLS,
        zorder=2,
    )
    ax.set_xlabel(r"time $t$")
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize=9, pad=6)
    ax.set_xlim(t[0], t[-1])
    ax.set_ylim(bottom=0)
    style_legend(ax, loc="best")
    annotate_curve_ends(ax, t, y_new, y_cls)


def plot_overlays():
    results = [run_scenario(sc) for sc in SCENARIOS]

    # Shared figure banner
    banner = (
        "Solid navy  =  NEW model (renewal / burst-aware)     |     "
        "Dashed orange + circles  =  CLASSICAL BMVR (constant release rate p)"
    )

    # ---- Figure 1: V(t) overlays, 6 panels ----
    fig, axes = plt.subplots(2, 3, figsize=(12.2, 7.8))
    fig.subplots_adjust(left=0.07, right=0.99, top=0.86, bottom=0.08,
                        wspace=0.28, hspace=0.42)
    for ax, res in zip(axes.ravel(), results):
        plot_new_vs_classical(
            ax, res["t"], res["V_ren"], res["V_cls"],
            ylabel=r"free virions  $\mathcal{V}(t)$",
            title=panel_title(res),
        )
    fig.suptitle(
        "Free virions: NEW model vs CLASSICAL BMVR\n" + banner,
        fontsize=11, fontweight="bold", y=0.98,
    )
    path = os.path.join(OUTDIR, "overlay_V.pdf")
    fig.savefig(path)
    plt.close(fig)
    print("wrote", path)

    # ---- Figure 2: I(t) overlays ----
    fig, axes = plt.subplots(2, 3, figsize=(12.2, 7.8))
    fig.subplots_adjust(left=0.07, right=0.99, top=0.86, bottom=0.08,
                        wspace=0.28, hspace=0.42)
    for ax, res in zip(axes.ravel(), results):
        plot_new_vs_classical(
            ax, res["t"], res["I_ren"], res["I_cls"],
            ylabel=r"infected cells  $\mathcal{I}(t)$",
            title=panel_title(res),
        )
    fig.suptitle(
        "Infected cells: NEW model vs CLASSICAL BMVR\n" + banner,
        fontsize=11, fontweight="bold", y=0.98,
    )
    path = os.path.join(OUTDIR, "overlay_I.pdf")
    fig.savefig(path)
    plt.close(fig)
    print("wrote", path)

    # ---- Figure 2b: same free-virion data, include naive classical for one view ----
    fig, axes = plt.subplots(2, 3, figsize=(12.2, 7.8))
    fig.subplots_adjust(left=0.07, right=0.99, top=0.84, bottom=0.08,
                        wspace=0.28, hspace=0.42)
    for ax, res in zip(axes.ravel(), results):
        t = res["t"]
        me = max(len(t) // 25, 1)
        ax.plot(t, res["V_ren"], color=COLOR_NEW, ls="-", lw=LW_NEW,
                label=LABEL_NEW, zorder=3)
        ax.plot(t, res["V_cls"], color=COLOR_CLS, ls="--", lw=LW_CLS, dashes=(7, 3),
                marker="o", markevery=me, markersize=4.5,
                markerfacecolor="white", markeredgecolor=COLOR_CLS, markeredgewidth=1.2,
                label=LABEL_CLS_MATCH, zorder=2)
        ax.plot(t, res["V_naive"], color="#1B7A3D", ls=":", lw=2.2,
                label=LABEL_CLS_NAIVE, zorder=1)
        ax.set_xlabel(r"time $t$")
        ax.set_ylabel(r"free virions  $\mathcal{V}(t)$")
        ax.set_title(panel_title(res), fontsize=9, pad=6)
        ax.set_xlim(t[0], t[-1])
        ax.set_ylim(bottom=0)
        style_legend(ax, loc="best")
    fig.suptitle(
        "Free virions: NEW model vs two CLASSICAL choices\n"
        "Solid navy = NEW   |   Dashed orange = CLASSICAL matched   |   "
        "Dotted green = CLASSICAL naive (wrong units for p)",
        fontsize=10.5, fontweight="bold", y=0.98,
    )
    path = os.path.join(OUTDIR, "overlay_V_with_naive.pdf")
    fig.savefig(path)
    plt.close(fig)
    print("wrote", path)

    # ---- Figure 3: kernels ----
    intra = [
        (1.0, 0.0, 0.1, r"$\beta=1,\mu=0,\delta=0.1$"),
        (1.0, 0.2, 0.05, r"$\beta=1,\mu=0.2,\delta=0.05$"),
        (1.0, 0.0, 0.5, r"$\beta=1,\mu=0,\delta=0.5$"),
        (1.0, 0.9, 0.1, r"$\beta=1,\mu=0.9,\delta=0.1$"),
    ]
    t_k = np.linspace(0, 30, 600)
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.0))
    fig.subplots_adjust(left=0.08, right=0.98, top=0.84, bottom=0.14, wspace=0.28)
    for beta, mu, delta, lab in intra:
        Ihat, J, K, g, I, meta = kernels(t_k, beta, mu, delta)
        axes[0].plot(t_k, Ihat, lw=2.2, label=lab)
        axes[1].plot(t_k, g, lw=2.2, label=lab)
    axes[0].set_xlabel(r"cell age $a$")
    axes[0].set_ylabel(r"$\widehat{I}(a)$")
    axes[0].set_title("Cell-survival kernel\n(used only by the NEW model)", fontsize=10)
    style_legend(axes[0], loc="upper right")
    axes[0].set_ylim(bottom=0)
    axes[1].set_xlabel(r"cell age $a$")
    axes[1].set_ylabel(r"$g(a)=\delta K(a)$")
    axes[1].set_title("Release kernel\n(used only by the NEW model)", fontsize=10)
    style_legend(axes[1], loc="upper right")
    axes[1].set_ylim(bottom=0)
    fig.suptitle(
        "Single-cell kernels that drive the NEW (renewal) BMVR\n"
        "The CLASSICAL model has no age kernels — only constants p and d.",
        fontsize=11, fontweight="bold", y=0.98,
    )
    path = os.path.join(OUTDIR, "kernels.pdf")
    fig.savefig(path)
    plt.close(fig)
    print("wrote", path)

    # ---- Figure 4: relative difference ----
    fig, axes = plt.subplots(2, 3, figsize=(12.2, 7.2))
    fig.subplots_adjust(left=0.08, right=0.99, top=0.88, bottom=0.08,
                        wspace=0.30, hspace=0.40)
    for ax, res in zip(axes.ravel(), results):
        t = res["t"]
        scale = max(np.max(res["V_ren"]), 1e-12)
        rel = np.abs(res["V_ren"] - res["V_cls"]) / scale
        ax.fill_between(t, 0, rel, color=COLOR_CLS, alpha=0.15)
        ax.plot(t, rel, color="#5A189A", lw=2.4,
                label="|NEW − CLASSICAL| / max(NEW)")
        ax.set_xlabel(r"time $t$")
        ax.set_ylabel("relative difference")
        ax.set_title(res["sc"]["label"] + rf"   ($R_0={res['R0']:.2f}$)", fontsize=9)
        ax.set_xlim(t[0], t[-1])
        ax.set_ylim(bottom=0)
        style_legend(ax, loc="best")
    fig.suptitle(
        "How far CLASSICAL (matched) drifts from the NEW model\n"
        "Larger values = classical constant-p ODEs fail to track renewal dynamics",
        fontsize=11, fontweight="bold", y=0.98,
    )
    path = os.path.join(OUTDIR, "overlay_rel_diff.pdf")
    fig.savefig(path)
    plt.close(fig)
    print("wrote", path)

    # ---- Figure 5: growth-phase ----
    sc = SCENARIOS[0]
    t = np.arange(0.0, 60.0 + 0.01, 0.01)
    Ihat, J, K, g, I_surv, meta = kernels(t, sc["beta"], sc["mu"], sc["delta"])
    gammaT, c, I0, V0 = 0.025, 0.2, 5.0, 0.0
    I_ren, V_ren = solve_renewal(t, Ihat, g, gammaT, c, I0, V0)
    I0m, V0m = solve_classical(t, gammaT, c, meta["p_eff0"], meta["d_eff0"], I0, V0)
    I_y, V_y = solve_classical(t, gammaT, c, sc["delta"], sc["mu"] + sc["delta"], I0, V0)
    R0 = gammaT * meta["V_inf"] / c
    me = max(len(t) // 30, 1)

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4))
    fig.subplots_adjust(left=0.08, right=0.98, top=0.78, bottom=0.14, wspace=0.28)

    axes[0].semilogy(t, np.maximum(V_ren, 1e-16), color=COLOR_NEW, ls="-", lw=LW_NEW,
                     label=LABEL_NEW, zorder=3)
    axes[0].semilogy(t, np.maximum(V0m, 1e-16), color=COLOR_CLS, ls="--", lw=LW_CLS,
                     dashes=(7, 3), marker="o", markevery=me, markersize=4.5,
                     markerfacecolor="white", markeredgecolor=COLOR_CLS,
                     markeredgewidth=1.2, label=LABEL_CLS_MATCH, zorder=2)
    axes[0].semilogy(t, np.maximum(V_y, 1e-16), color=COLOR_CLS2, ls="-.", lw=2.4,
                     label=LABEL_CLS_YOUNG, zorder=1)
    axes[0].set_xlabel(r"time $t$")
    axes[0].set_ylabel(r"free virions  $\mathcal{V}(t)$  (log scale)")
    axes[0].set_title(rf"Free virions   ($R_0={R0:.2f}$)", fontsize=10)
    style_legend(axes[0], loc="lower right")
    axes[0].set_xlim(0, 60)
    axes[0].text(0.03, 0.95, "NEW = solid navy", transform=axes[0].transAxes,
                 color=COLOR_NEW, fontsize=8, fontweight="bold", va="top")
    axes[0].text(0.03, 0.88, "CLASSICAL = dashed / dash-dot", transform=axes[0].transAxes,
                 color=COLOR_CLS, fontsize=8, fontweight="bold", va="top")

    axes[1].plot(t, I_ren, color=COLOR_NEW, ls="-", lw=LW_NEW, label=LABEL_NEW, zorder=3)
    axes[1].plot(t, I0m, color=COLOR_CLS, ls="--", lw=LW_CLS, dashes=(7, 3),
                 marker="o", markevery=me, markersize=4.5,
                 markerfacecolor="white", markeredgecolor=COLOR_CLS,
                 markeredgewidth=1.2, label=LABEL_CLS_MATCH, zorder=2)
    axes[1].plot(t, I_y, color=COLOR_CLS2, ls="-.", lw=2.4, label=LABEL_CLS_YOUNG, zorder=1)
    axes[1].set_xlabel(r"time $t$")
    axes[1].set_ylabel(r"infected cells  $\mathcal{I}(t)$")
    axes[1].set_title("Infected cells", fontsize=10)
    style_legend(axes[1], loc="best")
    axes[1].set_xlim(0, 60)
    axes[1].set_ylim(bottom=0)

    fig.suptitle(
        "Growth-phase mismatch: one NEW curve vs two CLASSICAL parameter choices\n"
        rf"Intracellular $(\beta,\mu,\delta)=(1,0,0.1)$;  population $\gamma T={gammaT}$, $c={c}$",
        fontsize=11, fontweight="bold", y=0.98,
    )
    path = os.path.join(OUTDIR, "overlay_growth_phase.pdf")
    fig.savefig(path)
    plt.close(fig)
    print("wrote", path)

    # print summary table
    print("\nScenario summary:")
    print(f"{'key':3} {'R0':>7} {'Vinf':>8} {'peff0':>8} {'deff0':>8} {'max|rel|':>10}")
    for res in results:
        scale = max(np.max(res["V_ren"]), 1e-12)
        rel = np.abs(res["V_ren"] - res["V_cls"]) / scale
        print(
            f"{res['sc']['key']:3} {res['R0']:7.3f} {res['meta']['V_inf']:8.3f} "
            f"{res['meta']['p_eff0']:8.3f} {res['meta']['d_eff0']:8.3f} {rel.max():10.4f}"
        )


if __name__ == "__main__":
    plot_overlays()
