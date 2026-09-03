#!/usr/bin/env python3
"""
Comprehensive numerical verification of Result 20.1
(Burst-aware renewal BMVR / new viral dynamics).

Writes:
  verify_result_20_1_report.txt
  verify_figures/*.pdf
"""
from __future__ import annotations

import os
import json
import time
import numpy as np
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

# Phase C: the suite's figures go into the chapter, so they carry the chapter's
# palette and typography rather than matplotlib's defaults.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "figures" / "_style"))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt

OUTDIR = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(OUTDIR, "verify_figures")
os.makedirs(FIGDIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Single-cell BDC closed forms
# ---------------------------------------------------------------------------

def bdc_roots(beta, mu, delta):
    eta = (beta + mu + delta) / (2.0 * beta)
    disc = np.sqrt(max(eta**2 - mu / beta, 0.0))
    a = eta + disc
    b = eta - disc
    return a, b, a - 1.0, 1.0 - b, beta * (a - b)


def single_cell(t, beta, mu, delta):
    a, b, A, B, theta = bdc_roots(beta, mu, delta)
    w = np.exp(theta * t)
    I = (a * B + b * A * w) / (B + A * w)
    Ihat = (a - b) ** 2 * w / ((B + A * w) * (a * w - b))
    Ihat = np.where(t == 0.0, 1.0, Ihat)
    J = (a - b) ** 2 * w / (B + A * w) ** 2
    K = (1.0 + (2.0 * beta / delta) * (1.0 - I)) * J
    g = delta * K
    Vcum = (1.0 - I) * (1.0 + (beta / delta) * (1.0 - I))  # E[W_t]
    Vinf = a * (1.0 - b) / (a - 1.0)
    Tprod = np.log(a / (a - 1.0)) / beta
    return dict(
        a=a, b=b, A=A, B=B, theta=theta, I=I, Ihat=Ihat, J=J, K=K, g=g,
        Vcum=Vcum, Vinf=Vinf, Tprod=Tprod,
        peff0=Vinf / Tprod, deff0=1.0 / Tprod,
    )


# The five intracellular triples the chapter's verification appendix names:
# the three regimes of tab:trio plus two further sets that spread the kernel
# shapes.  Used by tests L and M, added in Phase C.
PARAM_SETS = [
    (1.0, 0.0, 0.1),
    (1.0, 0.2, 0.05),
    (1.0, 0.0, 0.5),
    (1.0, 0.9, 0.1),
    (1.0, 0.5, 1.0 / 3.0),
]


def laplace_trap(f, t, r):
    return np.trapezoid(np.exp(-r * t) * f, t)


def laplace_simpson(f, t, r):
    """Composite Simpson; needs an odd number of samples on a uniform grid."""
    n = len(t)
    assert n % 2 == 1, "Simpson needs an odd sample count"
    h = t[1] - t[0]
    y = np.exp(-r * t) * f
    w = np.ones(n)
    w[1:-1:2] = 4.0
    w[2:-1:2] = 2.0
    return h / 3.0 * float(np.sum(w * y))


def trap_conv_partial(V, ker, n, h):
    if n == 0:
        return 0.0
    s = 0.5 * V[n] * ker[0] + 0.5 * V[0] * ker[n]
    if n >= 2:
        s += np.dot(V[1:n], ker[n - 1 : 0 : -1])
    return h * s


def solve_renewal(t, Ihat, g, gammaT, c, I0, V0, method="rk2"):
    """
    Solve V' = I0 g + gammaT (V * g) - c V
    Icell = I0 Ihat + gammaT (V * Ihat)
    method: 'euler' or 'rk2' (Heun predictor-corrector on V)
    """
    n = len(t)
    h = t[1] - t[0]
    V = np.zeros(n)
    Icell = np.zeros(n)
    V[0] = V0
    Icell[0] = I0 * Ihat[0]

    def rhs(i, Varr):
        conv_g = trap_conv_partial(Varr, g, i, h)
        return I0 * g[i] + gammaT * conv_g - c * Varr[i]

    for i in range(n - 1):
        if method == "euler":
            V[i + 1] = max(V[i] + h * rhs(i, V), 0.0)
        else:
            # Heun: predict, then average slopes (use predicted V for conv at i+1 approx)
            k1 = rhs(i, V)
            Vpred = V.copy()
            Vpred[i + 1] = max(V[i] + h * k1, 0.0)
            # approximate conv at i+1 with predicted V
            conv_g_pred = trap_conv_partial(Vpred, g, i + 1, h)
            k2 = I0 * g[i + 1] + gammaT * conv_g_pred - c * Vpred[i + 1]
            V[i + 1] = max(V[i] + 0.5 * h * (k1 + k2), 0.0)

    for i in range(n):
        conv_I = trap_conv_partial(V, Ihat, i, h)
        Icell[i] = I0 * Ihat[i] + gammaT * conv_I
    return Icell, V


def solve_classical(t, gammaT, c, p, dI, I0, V0):
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


def char_root(gammaT, c, g, t, rmax=5.0):
    """Solve r + c = gammaT * Lap(g)(r) for dominant real r (or 0 if subcritical)."""
    def f(r):
        return r + c - gammaT * laplace_trap(g, t, r)

    f0 = f(0.0)
    if f0 >= 0:
        return 0.0, f0  # subcritical or critical; growth rate 0 for pure exponential
    lo, hi = 0.0, 0.1
    while f(hi) < 0 and hi < rmax:
        hi *= 2
    if f(hi) < 0:
        return np.nan, f0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi), f0


def fit_log_growth(t, y, t0_frac=0.55, t1_frac=0.95, ymin_frac=1e-8):
    """Linear fit of log y on late window; return slope or nan."""
    y = np.asarray(y)
    t = np.asarray(t)
    mask = (t >= t0_frac * t[-1]) & (t <= t1_frac * t[-1]) & (y > max(ymin_frac, 1e-14))
    if mask.sum() < 10:
        return np.nan
    tt, yy = t[mask], np.log(y[mask])
    # polyfit degree 1
    coeff = np.polyfit(tt, yy, 1)
    return float(coeff[0])


# ---------------------------------------------------------------------------
# Gillespie: single BDC cell until absorption
# ---------------------------------------------------------------------------

def gillespie_one_cell(beta, mu, delta, rng, t_max=80.0, n_max=5000):
    """Return (burst_time or inf, burst_size or 0), and path samples optional."""
    x = 1
    t = 0.0
    while t < t_max and x > 0 and x < n_max:
        rate = (beta + mu + delta) * x
        t += rng.exponential(1.0 / rate)
        u = rng.random() * rate
        if u < beta * x:
            x += 1
        elif u < (beta + mu) * x:
            x -= 1
        else:
            return t, x  # catastrophe, release x
    return np.inf, 0  # cleared or truncated


def ensemble_gamma0(beta, mu, delta, c, I0, n_cells, n_reps, t_grid, rng):
    """
    Stochastic hybrid: I0 independent BDC cells, free virus ODE
      V' = release_flux - c V
    where release_flux is sum of delta*X_i^2 for living cells... actually for
    CTMC, release is only at burst instants (impulses of size X).
    Mean flux is delta E[X^2 1_alive] = g(t) per cell.

    For ensemble of means: average over reps of
      V solved with jump releases; Icell(t) = number still productively infected.
    """
    nt = len(t_grid)
    I_acc = np.zeros(nt)
    V_acc = np.zeros(nt)
    # For efficiency: for each cell simulate burst time and size; then
    # V' = -c V between jumps, jumps +size at burst.
    # Productive infected: cell contributes 1 until burst or internal extinction.
    # Internal extinction: tau=inf, size=0 — cell is "not productively infected"
    # after hitting 0 without burst. For Ihat we need still in {1,2,...}.
    # Simulating full path for Ihat is heavier; for V we only need burst events.
    # For Icell we need time of leaving productive class (burst or hit 0).

    def simulate_cell_full(rng):
        x = 1
        t = 0.0
        t_max = t_grid[-1] + 1.0
        # return list of (t, x) events and exit_time, burst_time, burst_size
        # exit = first time x=0 or catastrophe
        while t < t_max and x > 0:
            rate = (beta + mu + delta) * x
            dt = rng.exponential(1.0 / rate)
            t += dt
            u = rng.random() * rate
            if u < beta * x:
                x += 1
            elif u < (beta + mu) * x:
                x -= 1
                if x == 0:
                    return t, None  # cleared, no burst
            else:
                return t, x  # burst
        return t_max, None

    for _ in range(n_reps):
        bursts = []  # (time, size)
        exit_times = []
        for _c in range(n_cells):
            te, bs = simulate_cell_full(rng)
            exit_times.append(te)
            if bs is not None:
                bursts.append((te, bs))
        # Icell on grid: count of cells with exit_time > t
        et = np.array(exit_times)
        for i, ti in enumerate(t_grid):
            I_acc[i] += np.sum(et > ti)
        # V trajectory with jumps
        V = 0.0
        bursts_sorted = sorted(bursts, key=lambda z: z[0])
        bi = 0
        t_cur = 0.0
        V_path = np.zeros(nt)
        for i, ti in enumerate(t_grid):
            # advance from t_cur to ti
            while bi < len(bursts_sorted) and bursts_sorted[bi][0] <= ti:
                tb, sz = bursts_sorted[bi]
                # decay to tb
                V *= np.exp(-c * (tb - t_cur))
                V += sz
                t_cur = tb
                bi += 1
            V *= np.exp(-c * (ti - t_cur))
            t_cur = ti
            V_path[i] = V
        V_acc += V_path

    return I_acc / n_reps, V_acc / n_reps


# ---------------------------------------------------------------------------
# Test suite
# ---------------------------------------------------------------------------

class Report:
    def __init__(self):
        self.lines = []
        self.results = []

    def section(self, title):
        self.lines.append("")
        self.lines.append("=" * 72)
        self.lines.append(title)
        self.lines.append("=" * 72)

    def log(self, s=""):
        self.lines.append(s)
        print(s)

    def add(self, name, passed, detail, metrics=None):
        status = "PASS" if passed else "FAIL"
        self.results.append(dict(name=name, passed=bool(passed), detail=detail, metrics=metrics or {}))
        self.log(f"[{status}] {name}")
        self.log(f"       {detail}")

    def summary(self):
        n = len(self.results)
        p = sum(1 for r in self.results if r["passed"])
        self.section(f"SUMMARY: {p}/{n} checks passed")
        for r in self.results:
            self.log(f"  {'PASS' if r['passed'] else 'FAIL'}  {r['name']}")
        return p, n

    def save(self, path):
        with open(path, "w") as f:
            f.write("\n".join(self.lines))
            f.write("\n")


def main():
    rep = Report()
    rng = np.random.default_rng(42)
    t0wall = time.time()

    # Common parameter sets
    PARAMS = [
        dict(name="mu0_slow", beta=1.0, mu=0.0, delta=0.1),
        dict(name="mu_pos", beta=1.0, mu=0.2, delta=0.05),
        dict(name="fast_burst", beta=1.0, mu=0.0, delta=0.5),
        dict(name="high_death", beta=1.0, mu=0.9, delta=0.1),
        dict(name="L_eq_1", beta=1.0, mu=0.5, delta=1.0 / 3.0),
    ]

    # =====================================================================
    rep.section("TEST A — Kernel self-consistency (inputs to Result 20.1)")
    # =====================================================================
    for p in PARAMS:
        t = np.linspace(0, 60, 120001)
        sc = single_cell(t, p["beta"], p["mu"], p["delta"])
        # V' ≈ g = delta K
        dV = np.gradient(sc["Vcum"], t)
        err_g = np.max(np.abs(dV - sc["g"]) / (np.max(sc["g"]) + 1e-12))
        # int g = Vinf
        int_g = np.trapezoid(sc["g"], t)
        err_Vinf = abs(int_g - sc["Vinf"]) / sc["Vinf"]
        # int Ihat = Tprod
        int_I = np.trapezoid(sc["Ihat"], t)
        err_T = abs(int_I - sc["Tprod"]) / sc["Tprod"]
        # I' = -delta J
        dI = np.gradient(sc["I"], t)
        err_IJ = np.max(np.abs(dI + p["delta"] * sc["J"]) / (np.max(np.abs(dI)) + 1e-12))
        ok = err_g < 5e-3 and err_Vinf < 1e-3 and err_T < 1e-3 and err_IJ < 5e-3
        rep.add(
            f"A.kernels[{p['name']}]",
            ok,
            f"max|V'-g|/maxg={err_g:.2e}, |∫g-V∞|/V∞={err_Vinf:.2e}, "
            f"|∫Ihat-Tprod|/Tprod={err_T:.2e}, max|I'+δJ| rel={err_IJ:.2e}",
            dict(err_g=err_g, err_Vinf=err_Vinf, err_T=err_T, err_IJ=err_IJ),
        )

    # =====================================================================
    rep.section("TEST B — γT=0 cohort: renewal reduces to single-cell formulas")
    # =====================================================================
    # Icell(t) = I0 Ihat(t); with c>0: V solves V' = I0 g - c V, V(0)=0
    # closed form V(t) = I0 ∫_0^t e^{-c(t-s)} g(s) ds
    for p in PARAMS:
        for c in [0.0, 0.25, 1.0]:
            I0 = 7.0
            t = np.linspace(0, 40, 8001)
            sc = single_cell(t, p["beta"], p["mu"], p["delta"])
            Icell, V = solve_renewal(t, sc["Ihat"], sc["g"], gammaT=0.0, c=c, I0=I0, V0=0.0)
            # Icell check
            err_I = np.max(np.abs(Icell - I0 * sc["Ihat"]) / I0)
            # V check vs convolution
            h = t[1] - t[0]
            V_exact = np.zeros_like(t)
            for i in range(len(t)):
                # I0 * int_0^{t_i} exp(-c(ti-s)) g(s) ds
                s = t[: i + 1]
                ker = np.exp(-c * (t[i] - s)) * sc["g"][: i + 1]
                V_exact[i] = I0 * np.trapezoid(ker, s)
            scale = max(np.max(V_exact), 1e-12)
            err_V = np.max(np.abs(V - V_exact)) / scale
            # c=0: V should approach I0 * Vcum (cumulative mean release, no clearance)
            if c == 0.0:
                err_V0 = np.max(np.abs(V - I0 * sc["Vcum"])) / (I0 * sc["Vinf"] + 1e-12)
            else:
                err_V0 = 0.0
            ok = err_I < 1e-10 and err_V < 2e-2 and (c > 0 or err_V0 < 2e-2)
            rep.add(
                f"B.gamma0[{p['name']},c={c}]",
                ok,
                f"max|Icell-I0 Ihat|/I0={err_I:.2e}, max|V-conv|/scale={err_V:.2e}"
                + (f", max|V-I0 Vcum| rel={err_V0:.2e}" if c == 0 else ""),
                dict(err_I=err_I, err_V=err_V, err_V0=err_V0),
            )

    # =====================================================================
    rep.section("TEST C — Residual of the V-equation on the numerical solution")
    # =====================================================================
    SCENARIOS = [
        dict(name="super_mu0", beta=1, mu=0, delta=0.1, gammaT=0.04, c=0.25, I0=5, V0=0, tmax=45),
        dict(name="super_mu", beta=1, mu=0.2, delta=0.05, gammaT=0.03, c=0.2, I0=5, V0=0, tmax=50),
        dict(name="subcrit", beta=1, mu=0, delta=0.1, gammaT=0.01, c=0.4, I0=20, V0=0, tmax=50),
        dict(name="V0_seed", beta=1, mu=0, delta=0.1, gammaT=0.05, c=0.2, I0=0, V0=3, tmax=40),
        dict(name="high_death", beta=1, mu=0.9, delta=0.1, gammaT=0.5, c=0.25, I0=10, V0=0, tmax=40),
    ]
    for scn in SCENARIOS:
        t = np.linspace(0, scn["tmax"], int(scn["tmax"] / 0.01) + 1)
        sc = single_cell(t, scn["beta"], scn["mu"], scn["delta"])
        Icell, V = solve_renewal(t, sc["Ihat"], sc["g"], scn["gammaT"], scn["c"], scn["I0"], scn["V0"])
        h = t[1] - t[0]
        # residual r_i = V'(t_i) - I0 g_i - gammaT (V*g)_i + c V_i
        Vp = np.gradient(V, t)
        conv = np.array([trap_conv_partial(V, sc["g"], i, h) for i in range(len(t))])
        resid = Vp - scn["I0"] * sc["g"] - scn["gammaT"] * conv + scn["c"] * V
        # relative to scale of terms
        scale = np.max(np.abs(Vp) + scn["I0"] * sc["g"] + scn["c"] * np.abs(V)) + 1e-12
        rel = np.max(np.abs(resid)) / scale
        # Icell residual: Icell - I0 Ihat - gammaT (V*Ihat)
        convI = np.array([trap_conv_partial(V, sc["Ihat"], i, h) for i in range(len(t))])
        residI = Icell - scn["I0"] * sc["Ihat"] - scn["gammaT"] * convI
        relI = np.max(np.abs(residI)) / (np.max(Icell) + 1e-12)
        ok = rel < 0.05 and relI < 1e-9
        R0 = scn["gammaT"] * sc["Vinf"] / scn["c"]
        rep.add(
            f"C.residual[{scn['name']}]",
            ok,
            f"R0={R0:.3f}, max|V-eq residual|/scale={rel:.3e}, "
            f"max|Icell-def residual|/maxI={relI:.3e}",
            dict(R0=R0, rel_V=rel, rel_I=relI),
        )

    # =====================================================================
    rep.section("TEST D — Exponential kernels reduce to classical BMVR exactly")
    # =====================================================================
    # S(a)=e^{-d a}, g(a)=p e^{-d a}  => renewal ≡ classical ODE
    for p, dI, gammaT, c, I0, V0, tmax in [
        (2.0, 0.5, 0.3, 0.4, 3.0, 1.0, 25.0),
        (4.5, 0.4, 0.2, 0.3, 5.0, 0.0, 30.0),
        (1.0, 1.0, 0.5, 0.5, 2.0, 2.0, 20.0),
    ]:
        t = np.linspace(0, tmax, int(tmax / 0.005) + 1)
        S = np.exp(-dI * t)
        g = p * np.exp(-dI * t)
        Ir, Vr = solve_renewal(t, S, g, gammaT, c, I0, V0, method="rk2")
        Ic, Vc = solve_classical(t, gammaT, c, p, dI, I0, V0)
        errV = np.max(np.abs(Vr - Vc)) / (np.max(Vc) + 1e-12)
        errI = np.max(np.abs(Ir - Ic)) / (np.max(Ic) + 1e-12)
        ok = errV < 0.02 and errI < 0.02
        rep.add(
            f"D.exp_kernel[p={p},d={dI}]",
            ok,
            f"max|Vren-Vcls|/maxV={errV:.3e}, max|Iren-Icls|/maxI={errI:.3e}",
            dict(errV=errV, errI=errI),
        )

    # plot one exponential reduction
    t = np.linspace(0, 25, 5001)
    p, dI, gammaT, c, I0, V0 = 2.0, 0.5, 0.3, 0.4, 3.0, 1.0
    S = np.exp(-dI * t)
    g = p * np.exp(-dI * t)
    Ir, Vr = solve_renewal(t, S, g, gammaT, c, I0, V0)
    Ic, Vc = solve_classical(t, gammaT, c, p, dI, I0, V0)
    fig, ax = plt.subplots(1, 2, figsize=(4.89, 2.0))
    ax[0].plot(t, Vr, color=style_rc.BLUE, lw=1.9, label="renewal")
    ax[0].plot(t, Vc, color=style_rc.VERMILLION, lw=1.8, ls="--",
               label="classical BMVR")
    ax[0].set_xlabel(r"time $t$")
    ax[0].set_ylabel(r"free particles $\mathcal{V}(t)$")
    ax[1].plot(t, Ir, color=style_rc.BLUE, lw=1.9, label="renewal")
    ax[1].plot(t, Ic, color=style_rc.VERMILLION, lw=1.8, ls="--",
               label="classical BMVR")
    ax[1].set_xlabel(r"time $t$")
    ax[1].set_ylabel(r"infected cells $\mathcal{I}(t)$")
    style_rc.panel_label(ax[0], "(a)")
    style_rc.panel_label(ax[1], "(b)")
    h, lb = ax[0].get_legend_handles_labels()
    fig.legend(h, lb, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.01),
               fontsize=8.3)
    fig.tight_layout(rect=(0, 0, 1, 0.86))
    fig.savefig(os.path.join(FIGDIR, "D_exponential_reduction.pdf"))
    plt.close(fig)

    # =====================================================================
    rep.section("TEST E — Growth rate matches characteristic equation")
    # =====================================================================
    growth_cases = [
        dict(name="A", beta=1, mu=0, delta=0.1, gammaT=0.04, c=0.25, I0=5, V0=0, tmax=60),
        dict(name="B", beta=1, mu=0.2, delta=0.05, gammaT=0.03, c=0.2, I0=5, V0=0, tmax=70),
        dict(name="C", beta=1, mu=0, delta=0.5, gammaT=0.25, c=0.3, I0=5, V0=0, tmax=40),
        dict(name="E", beta=1, mu=0.9, delta=0.1, gammaT=0.5, c=0.25, I0=10, V0=0, tmax=50),
        dict(name="F", beta=1, mu=0, delta=0.1, gammaT=0.05, c=0.2, I0=0, V0=3, tmax=55),
    ]
    r_rows = []
    for scn in growth_cases:
        t = np.linspace(0, scn["tmax"], int(scn["tmax"] / 0.01) + 1)
        sc = single_cell(t, scn["beta"], scn["mu"], scn["delta"])
        R0 = scn["gammaT"] * sc["Vinf"] / scn["c"]
        r_star, f0 = char_root(scn["gammaT"], scn["c"], sc["g"], t)
        Icell, V = solve_renewal(t, sc["Ihat"], sc["g"], scn["gammaT"], scn["c"], scn["I0"], scn["V0"])
        r_fit = fit_log_growth(t, V)
        # also check peff reduction: classical with peff(r*), deff(r*) should share r*
        if np.isfinite(r_star) and r_star > 1e-6:
            Lg = laplace_trap(sc["g"], t, r_star)
            LI = laplace_trap(sc["Ihat"], t, r_star)
            peff = Lg / LI
            deff = 1.0 / LI - r_star
            # eigenvalue of classical: solve (r+d)(r+c)=gammaT p
            # r should satisfy that
            resid_cls = (r_star + deff) * (r_star + scn["c"]) - scn["gammaT"] * peff
        else:
            peff = deff = resid_cls = np.nan
            Lg = LI = np.nan

        if R0 > 1.05 and r_star > 1e-4:
            # relative error on growth rates
            err = abs(r_fit - r_star) / max(r_star, 1e-8)
            ok = err < 0.08 and abs(resid_cls) < 1e-2
        elif R0 < 0.95:
            # should decay: fitted "growth" negative or near 0 from below
            ok = (not np.isfinite(r_fit)) or r_fit < 0.02
            err = r_fit
        else:
            ok = True
            err = abs(r_fit - r_star) if np.isfinite(r_fit) and np.isfinite(r_star) else np.nan

        r_rows.append(dict(name=scn["name"], R0=R0, r_star=r_star, r_fit=r_fit, err=err, peff=peff, deff=deff))
        rep.add(
            f"E.growth[{scn['name']}]",
            ok,
            f"R0={R0:.3f}, r_char={r_star:.5f}, r_fit={r_fit:.5f}, "
            f"rel_err={err if np.isfinite(err) else float('nan'):.3e}, "
            f"peff(r*)={peff if np.isfinite(peff) else float('nan'):.4f}, "
            f"class_eigs_resid={resid_cls if np.isfinite(resid_cls) else float('nan'):.2e}",
            dict(R0=R0, r_star=r_star, r_fit=r_fit, err=err),
        )

    # growth figure for case A
    scn = growth_cases[0]
    t = np.linspace(0, scn["tmax"], int(scn["tmax"] / 0.01) + 1)
    sc = single_cell(t, scn["beta"], scn["mu"], scn["delta"])
    r_star, _ = char_root(scn["gammaT"], scn["c"], sc["g"], t)
    _, V = solve_renewal(t, sc["Ihat"], sc["g"], scn["gammaT"], scn["c"], scn["I0"], scn["V0"])
    fig, ax = plt.subplots(figsize=(3.01, 2.3))
    ax.semilogy(t, V, color=style_rc.BLUE, lw=1.9, label=r"renewal $\mathcal{V}(t)$")
    # reference slope
    t_ref = t[t > 0.5 * t[-1]]
    V_ref = V[t > 0.5 * t[-1]][0] * np.exp(r_star * (t_ref - t_ref[0]))
    ax.semilogy(t_ref, V_ref, color=style_rc.INK, ls="--", lw=1.5,
                label=rf"$\mathrm{{e}}^{{rt}}$, $r=r_\star={r_star:.4f}$")
    ax.set_xlabel(r"time $t$")
    ax.set_ylabel(r"free particles $\mathcal{V}(t)$")
    ax.legend(fontsize=8.0)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "E_growth_rate_match.pdf"))
    plt.close(fig)

    # =====================================================================
    rep.section("TEST F — R0 threshold (growth vs decay)")
    # =====================================================================
    # Fix beta,mu,delta,c and vary gammaT across threshold
    beta, mu, delta, c = 1.0, 0.0, 0.1, 0.25
    t = np.linspace(0, 80, 8001)
    sc = single_cell(t, beta, mu, delta)
    Vinf = sc["Vinf"]
    # R0 = gammaT Vinf / c  => gammaT = R0 * c / Vinf
    R0_list = [0.5, 0.8, 0.95, 1.05, 1.2, 1.5, 2.0, 3.0]
    signs = []
    fig, ax = plt.subplots(figsize=(3.01, 2.3))
    for R0 in R0_list:
        gammaT = R0 * c / Vinf
        _, V = solve_renewal(t, sc["Ihat"], sc["g"], gammaT, c, I0=5.0, V0=0.0)
        r_fit = fit_log_growth(t, V, 0.6, 0.95)
        r_star, _ = char_root(gammaT, c, sc["g"], t)
        growing = R0 > 1
        # late value vs mid
        late_ratio = V[-1] / (V[len(V) // 2] + 1e-15)
        if growing:
            ok_case = (r_star > 0) and (V[-1] > V[len(V) // 2])
        else:
            ok_case = (r_star == 0.0) and (V[-1] < V[len(V) // 2] or r_fit < 0)
        signs.append(ok_case)
        ax.semilogy(t, V + 1e-16, lw=1.5, label=rf"$R_0={R0:g}$")
        rep.add(
            f"F.threshold[R0={R0}]",
            ok_case,
            f"gammaT={gammaT:.5f}, r_char={r_star:.5f}, r_fit={r_fit:.5f}, "
            f"Vfinal/Vmid={late_ratio:.3e}",
            dict(R0=R0, r_star=r_star, r_fit=r_fit, late_ratio=late_ratio),
        )
    ax.set_xlabel(r"time $t$")
    ax.set_ylabel(r"free particles $\mathcal{V}(t)$")
    ax.legend(fontsize=7.2, ncol=2, handlelength=1.5, columnspacing=1.0)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "F_R0_threshold.pdf"))
    plt.close(fig)

    # =====================================================================
    rep.section("TEST G — peff(r) classical matches renewal growth rate")
    # =====================================================================
    for scn in growth_cases[:4]:
        t = np.linspace(0, scn["tmax"], int(scn["tmax"] / 0.01) + 1)
        sc = single_cell(t, scn["beta"], scn["mu"], scn["delta"])
        R0 = scn["gammaT"] * sc["Vinf"] / scn["c"]
        if R0 <= 1.05:
            rep.add(f"G.peff[{scn['name']}]", True, f"skip subcritical R0={R0:.3f}", {})
            continue
        r_star, _ = char_root(scn["gammaT"], scn["c"], sc["g"], t)
        Lg = laplace_trap(sc["g"], t, r_star)
        LI = laplace_trap(sc["Ihat"], t, r_star)
        peff = Lg / LI
        deff = 1.0 / LI - r_star
        # Solve classical with these constants; fit its growth rate
        _, Vc = solve_classical(t, scn["gammaT"], scn["c"], peff, deff, scn["I0"], scn["V0"])
        _, Vr = solve_renewal(t, sc["Ihat"], sc["g"], scn["gammaT"], scn["c"], scn["I0"], scn["V0"])
        r_cls = fit_log_growth(t, Vc)
        r_ren = fit_log_growth(t, Vr)
        err = abs(r_cls - r_ren) / max(r_ren, 1e-8)
        # trajectories need not match transiently — only asymptotic rate
        ok = err < 0.1 and abs(r_cls - r_star) / r_star < 0.1
        rep.add(
            f"G.peff_match[{scn['name']}]",
            ok,
            f"r*={r_star:.5f}, r_ren={r_ren:.5f}, r_cls(peff)={r_cls:.5f}, "
            f"|r_cls-r_ren|/r_ren={err:.3e}, peff={peff:.4f}, deff={deff:.4f}",
            dict(r_star=r_star, r_ren=r_ren, r_cls=r_cls, peff=peff, deff=deff),
        )

    # =====================================================================
    rep.section("TEST H — Gillespie ensemble vs renewal (γT=0 cohort)")
    # =====================================================================
    # Mean field exact for independent cells + linear clearance
    stoch_cases = [
        dict(name="mu0", beta=1.0, mu=0.0, delta=0.1, c=0.25, I0=20, tmax=25.0, n_reps=400),
        dict(name="mu_pos", beta=1.0, mu=0.2, delta=0.05, c=0.2, I0=30, tmax=20.0, n_reps=500),
    ]
    _H_PANELS = []
    for scn in stoch_cases:
        t = np.linspace(0, scn["tmax"], 201)
        sc = single_cell(t, scn["beta"], scn["mu"], scn["delta"])
        I_ren, V_ren = solve_renewal(
            t, sc["Ihat"], sc["g"], 0.0, scn["c"], float(scn["I0"]), 0.0
        )
        # For stochastic: burst impulses — mean V satisfies same IDE with g=δK
        # only in expectation of flux. Impulse process: E[dRelease] = g dt per cell.
        print(f"  Gillespie ensemble {scn['name']} ({scn['n_reps']} reps x {scn['I0']} cells)...")
        I_st, V_st = ensemble_gamma0(
            scn["beta"], scn["mu"], scn["delta"], scn["c"],
            scn["I0"], scn["I0"], scn["n_reps"], t, rng,
        )
        # relative L2 errors
        def rel_l2(a, b):
            return np.sqrt(np.mean((a - b) ** 2)) / (np.sqrt(np.mean(b ** 2)) + 1e-12)

        eI = rel_l2(I_st, I_ren)
        eV = rel_l2(V_st, V_ren)
        ok = eI < 0.12 and eV < 0.15
        rep.add(
            f"H.gillespie_gamma0[{scn['name']}]",
            ok,
            f"rel L2 Icell={eI:.3e}, rel L2 V={eV:.3e} "
            f"(n_reps={scn['n_reps']}, I0={scn['I0']})",
            dict(eI=eI, eV=eV),
        )
        _H_PANELS.append(dict(name=scn["name"], t=t, I_ren=I_ren, I_st=I_st,
                              V_ren=V_ren, V_st=V_st, mu=scn.get("mu", 0.0)))

    # Phase C: one 2x2 figure rather than two files placed at 31% of native
    # size.  Columns are the two scenarios, rows the two state variables.
    if _H_PANELS:
        fig, axes = plt.subplots(2, len(_H_PANELS), figsize=(5.89, 4.05),
                                 sharex="col", squeeze=False)
        tags = [["a", "b"], ["c", "d"]]
        for col, pan in enumerate(_H_PANELS):
            for row, (ren, st, name) in enumerate(
                    [(pan["I_ren"], pan["I_st"], r"infected cells $\mathcal{I}(t)$"),
                     (pan["V_ren"], pan["V_st"], r"free particles $\mathcal{V}(t)$")]):
                axx = axes[row][col]
                axx.plot(pan["t"], ren, color=style_rc.BLUE, lw=1.9,
                         label="renewal")
                axx.plot(pan["t"], st, color=style_rc.VERMILLION, lw=1.7,
                         ls="--", label="Gillespie ensemble mean")
                if col == 0:
                    axx.set_ylabel(name)
                style_rc.panel_label(axx, f"({tags[row][col]})")
                if row == 1:
                    axx.set_xlabel(r"time $t$")
            head = r"$\mu=0$" if pan["mu"] == 0 else r"$\mu>0$"
            axes[0][col].text(0.5, 1.12, head, transform=axes[0][col].transAxes,
                              ha="center", va="bottom", fontsize=9.0)
        h, lb = axes[0][0].get_legend_handles_labels()
        fig.legend(h, lb, loc="upper center", ncol=2,
                   bbox_to_anchor=(0.5, 1.005), columnspacing=2.0)
        fig.tight_layout(pad=1.0, w_pad=1.9, h_pad=0.9, rect=(0, 0, 1, 0.93))
        fig.savefig(os.path.join(FIGDIR, "H_gillespie.pdf"), bbox_inches="tight")
        plt.close(fig)

    # =====================================================================
    rep.section("TEST I — Initial free-virus seed (I0=0) consistency")
    # =====================================================================
    # Early time: V(t) ≈ V0 e^{-c t} before secondary release builds
    t = np.linspace(0, 40, 8001)
    sc = single_cell(t, 1.0, 0.0, 0.1)
    gammaT, c, V0 = 0.05, 0.2, 3.0
    Icell, V = solve_renewal(t, sc["Ihat"], sc["g"], gammaT, c, 0.0, V0)
    # at very early t, V ~ V0 e^{-ct}
    t_early = t[t <= 0.5]
    V_early = V[t <= 0.5]
    V_decay = V0 * np.exp(-c * t_early)
    err_early = np.max(np.abs(V_early - V_decay)) / V0
    # Icell(0)=0; Icell increases from infections
    ok = Icell[0] == 0.0 and err_early < 0.05 and Icell[-1] > 0
    R0 = gammaT * sc["Vinf"] / c
    rep.add(
        "I.V0_seed_early",
        ok,
        f"R0={R0:.3f}, max early |V - V0*exp(-c t)|/V0={err_early:.3e}, "
        f"Icell[0]={Icell[0]:.2e}, Icell[final]={Icell[-1]:.3f}",
        dict(err_early=err_early, R0=R0),
    )

    # =====================================================================
    rep.section("TEST J — Mass / lifetime output check under γT=0, c=0")
    # =====================================================================
    for p in PARAMS:
        t = np.linspace(0, 80, 16001)
        sc = single_cell(t, p["beta"], p["mu"], p["delta"])
        I0 = 1.0
        _, V = solve_renewal(t, sc["Ihat"], sc["g"], 0.0, 0.0, I0, 0.0)
        # V(∞) should be Vinf
        err = abs(V[-1] - sc["Vinf"]) / sc["Vinf"]
        ok = err < 5e-3
        rep.add(
            f"J.lifetime_output[{p['name']}]",
            ok,
            f"V(final)={V[-1]:.6f}, V∞={sc['Vinf']:.6f}, rel_err={err:.3e}",
            dict(err=err),
        )

    # =====================================================================
    rep.section("TEST K — Monotonicity / comparison sanity vs classical matched")
    # =====================================================================
    # Not a correctness proof, but documents that solutions are well-behaved
    t = np.linspace(0, 45, 4501)
    sc = single_cell(t, 1.0, 0.0, 0.1)
    gammaT, c, I0 = 0.04, 0.25, 5.0
    Ir, Vr = solve_renewal(t, sc["Ihat"], sc["g"], gammaT, c, I0, 0.0)
    Ic, Vc = solve_classical(t, gammaT, c, sc["peff0"], sc["deff0"], I0, 0.0)
    R0 = gammaT * sc["Vinf"] / c
    # finite, non-negative, not NaN
    ok = np.all(np.isfinite(Vr)) and np.all(Vr >= -1e-10) and np.all(Ir >= -1e-10)
    rep.add(
        "K.well_posed_nonneg",
        ok,
        f"R0={R0:.3f}, max V_ren={Vr.max():.3f}, max V_cls={Vc.max():.3f}, "
        f"final V_ren/V_cls={(Vr[-1]/(Vc[-1]+1e-15)):.3f}",
        dict(R0=R0),
    )

    # =====================================================================
    rep.section("TEST L — Old-cell limit of the release flux per surviving cell")
    # =====================================================================
    # g/S -> delta * E_QS[X^2] = delta a(a+1)/(a-1)^2, the third endpoint of
    # the effective-parameter map.  Added in Phase C with Proposition
    # p:prop:oldcell.
    for (beta, mu, delta) in PARAM_SETS:
        a, b, _, _, theta = bdc_roots(beta, mu, delta)
        alpha = np.array([80.0 / theta])
        scL = single_cell(alpha, beta, mu, delta)
        ratio = float(scL["g"][0] / scL["Ihat"][0])
        target = delta * a * (a + 1.0) / (a - 1.0) ** 2
        err = abs(ratio - target) / target
        rep.add(
            f"L.old_cell_limit[{beta},{mu},{delta}]",
            err < 1e-8,
            f"g/S at large age = {ratio:.8f}, delta*E_QS[X^2] = {target:.8f}, "
            f"rel err = {err:.2e}",
            dict(ratio=ratio, target=target, err=err),
        )

    # =====================================================================
    rep.section("TEST M — p_eff monotone in r, and rho = g/S monotone in age")
    # =====================================================================
    # The hypothesis of Proposition p:prop:peff-monotone is that rho is
    # non-decreasing; the conclusion is that p_eff is non-increasing.  Both are
    # swept over a wide region of the rate plane.
    rng_m = np.random.default_rng(20260823)
    n_draw = 4000
    bad_rho = 0
    for _ in range(n_draw):
        mu = 10.0 ** rng_m.uniform(-3, 1.3)
        delta = 10.0 ** rng_m.uniform(-3, 1.3)
        a, b, A, B, theta = bdc_roots(1.0, mu, delta)
        kappa = 1.0 + delta / 2.0
        v = np.exp(-theta * np.linspace(0.0, 25.0 / theta, 4000))
        rho = 2.0 * (B * (kappa - a) * v + A * (kappa - b)) * (a - b * v) / (B * v + A) ** 2
        if np.any(np.diff(rho) < -1e-11):
            bad_rho += 1
    rep.add(
        "M.rho_monotone_sweep",
        bad_rho == 0,
        f"rho = g/S non-decreasing in age at {n_draw - bad_rho}/{n_draw} random "
        f"(mu,delta) in [1e-3,20]^2 at lambda=1",
        dict(n=n_draw, violations=bad_rho),
    )
    bad_peff = 0
    r_grid = [0.0, 0.02, 0.05, 0.1, 0.3, 0.7, 1.5, 3.0, 8.0, 25.0]
    for (beta, mu, delta) in PARAM_SETS:
        a, b, _, _, theta = bdc_roots(beta, mu, delta)
        tt = np.linspace(0.0, 70.0 / theta, 40001)
        scM = single_cell(tt, beta, mu, delta)
        vals = [laplace_trap(scM["g"], tt, r) / laplace_trap(scM["Ihat"], tt, r)
                for r in r_grid]
        if any(vals[i + 1] >= vals[i] for i in range(len(vals) - 1)):
            bad_peff += 1
    rep.add(
        "M.peff_decreasing",
        bad_peff == 0,
        f"p_eff strictly decreasing on a 10-point r grid for "
        f"{len(PARAM_SETS) - bad_peff}/{len(PARAM_SETS)} parameter sets",
        dict(violations=bad_peff),
    )

    # =====================================================================
    rep.section("TEST N — Laplace order of the release age, bursting vs budding")
    # =====================================================================
    # Proposition p:prop:rorder: r_bud > r_burst for every coupling iff
    # Lap(g_burst)(r) <= Lap(g_bud)(r) = p/(r+d) for all r > 0.
    rng_n = np.random.default_rng(11)
    n_draw = 1500
    r_vals = np.logspace(-4, 2, 60)
    bad_order = 0
    worst = np.inf
    for _ in range(n_draw):
        mu = 10.0 ** rng_n.uniform(-3, 1.0)
        delta = 10.0 ** rng_n.uniform(-3, 1.2)
        a, b, _, _, theta = bdc_roots(1.0, mu, delta)
        base = single_cell(np.array([0.0]), 1.0, mu, delta)
        Vinf, ET = base["Vinf"], base["Tprod"]
        d_I = 1.0 / ET
        pbud = Vinf * d_I
        for r in r_vals:
            tt = np.linspace(0.0, 70.0 / (theta + r), 20001)
            lhs = laplace_simpson(single_cell(tt, 1.0, mu, delta)["g"], tt, r)
            rhs = pbud / (r + d_I)
            # relative test: the two transforms coincide at r = 0, so the true
            # gap is O(r) near the origin and an absolute tolerance would be
            # testing the integrator rather than the ordering
            if lhs > rhs * (1.0 + 1e-6):
                bad_order += 1
                break
            worst = min(worst, (rhs - lhs) / rhs)
    rep.add(
        "N.laplace_order",
        bad_order == 0,
        f"Lap(g_burst) <= Lap(g_bud) at all 60 r values for "
        f"{n_draw - bad_order}/{n_draw} random (mu,delta); "
        f"smallest normalised gap {worst:.2e}",
        dict(n=n_draw, violations=bad_order, worst_gap=worst),
    )

    # =====================================================================
    # Final summary
    # =====================================================================
    p, n = rep.summary()
    rep.log(f"\nWall time: {time.time() - t0wall:.1f}s")
    rep.log(f"Figures written to: {FIGDIR}")
    report_path = os.path.join(OUTDIR, "verify_result_20_1_report.txt")
    rep.save(report_path)

    # JSON metrics for potential later use
    json_path = os.path.join(OUTDIR, "verify_result_20_1_metrics.json")
    with open(json_path, "w") as f:
        json.dump(rep.results, f, indent=2, default=float)

    print(f"\nReport: {report_path}")
    print(f"Metrics: {json_path}")
    return p, n


if __name__ == "__main__":
    main()
