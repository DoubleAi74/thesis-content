#!/usr/bin/env python3
"""
Verification suite for the chained immediate-transfer model (mu = 0).

Model: M host cells. One starts with a single particle. Each cell runs a pure
birth--catastrophe process (birth beta*n, catastrophe delta*n). On catastrophe
the whole load transfers immediately into the next cell. r_k / t_k are the
size / time of the k-th rupture; T_k = t_k - t_{k-1} the inter-rupture interval.

Key structural fact used throughout: at load n the next event is a birth with
probability rho = beta/(beta+delta) and a catastrophe with probability
s = delta/(beta+delta), independent of n. Hence each cell i contributes an
independent G_i ~ Geom_0(s) (births before catastrophe) and

    r_k = 1 + G_1 + ... + G_k,
    T_k = sum_{j=r_{k-1}}^{r_{k-1}+G_k} Exp((beta+delta) j),
    T_k conditionally independent of t_{k-1} given (r_{k-1}, G_k).

Claims checked (all for mu = 0):

  A. Coefficients A_k^{(n)} = C(n+k-2, k-1) satisfy the recurrence
     A_k^{(n)} = sum_{i=1}^n A_{k-1}^{(i)},  A_1^{(n)} = 1  (exact integer).
     NOTE: this corrects the draft's closed form (1/k!)(n+k-1)!/(n-1)!,
     which is C(n+k-1, k) and contradicts the draft's own r_2, r_3 cases.
  B. Rupture-size laws  P{r_k = n} = C(n+k-2, k-1) s^k rho^{n-1}, k = 1..4.
  C. Moments  E[r_k] = 1 + k*rho/s,  Var(r_k) = k*rho/s^2.
  D. PGF  E[z^{r_k}] = z * (s/(1 - rho z))^k  (SE-aware comparison).
  E. First rupture-time density f_{t_1}(t) = delta*J(t) (the mu=0 BDC flux).
  F. Interval Laplace transform for FIXED founder counts k in {1,2,3,5}:
       L_T(k, u) = sum_{g>=0} s rho^g prod_{j=k}^{k+g} lam_j/(lam_j+u),
     lam_j = (beta+delta) j; equals [s*k/(k+u')] * 2F1(k+1,1;k+1+u';rho),
     u' = u/(beta+delta) (checked when scipy is available).
     Plus mixture consistency for the chain intervals:
       E[e^{-u T_k}] = sum_n pmf_{r_{k-1}}(n) L_T(n, u), k = 2, 3.
  G. Second rupture time: t_2 = t_1 + T_2 with
       L_2(u) = sum_g s rho^g P_1(1+g, u) L_T(1+g, u),
     P_1(m, u) = prod_{j=1}^{m} lam_j/(lam_j + u).
  H. Density of t_2 computed EXACTLY as a hypoexponential mixture
     (t_2 | G_1, G_2 is a sum of independent exponentials; rate lam_{1+G_1}
     appears twice), compared with the simulation histogram.
  I. Mean inter-rupture intervals: E[T(k)] strictly decreasing in fixed k
     (the draft's "loads increasing, intervals reducing" claim), matched
     against the exact series E[T(k)] = sum_{m>=0} rho^m / lam_{k+m};
     chain means E[T_k] reported as the random-founder version.

Writes: verify_chained_transfer_report.txt, verify_chained_transfer_metrics.json,
and (if matplotlib is available) verify_chained_transfer_figures.pdf.

Usage:  python3 verify_chained_transfer.py
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from math import comb

import numpy as np

OUTDIR = os.path.dirname(os.path.abspath(__file__))

RNG = np.random.default_rng(20260807)

PARAM_SETS = [
    ("symmetric", 1.0, 1.0),    # rho = 0.5
    ("slow_burst", 1.0, 0.1),   # rho ~ 0.909
    ("fast_burst", 2.0, 0.5),   # rho = 0.8
]

N_SIZE = 1_000_000   # chains for size checks (B, C, D)
N_TIME = 250_000     # chains for time checks (E, F, G, H, I)
N_FIXED = 300_000    # samples per fixed-founder interval check
M_CELLS = 4

report_lines: list[str] = []
metrics: dict = {}
n_pass = 0
n_fail = 0


def log(msg: str) -> None:
    report_lines.append(msg)
    print(msg)


def check(tag: str, ok: bool, detail: str) -> bool:
    global n_pass, n_fail
    if ok:
        n_pass += 1
        log(f"[PASS] {tag}\n       {detail}")
    else:
        n_fail += 1
        log(f"[FAIL] {tag}\n       {detail}")
    metrics[tag] = {"ok": bool(ok), "detail": detail}
    return ok


def gmax_for(rho: float, floor: float = 1e-14) -> int:
    return int(math.ceil(math.log(floor) / math.log(rho))) + 10


# ---------------------------------------------------------------------------
# Theory: sizes
# ---------------------------------------------------------------------------

def pmf_r(k: int, n: np.ndarray, s: float, rho: float) -> np.ndarray:
    """P{r_k = n} = C(n+k-2, k-1) s^k rho^{n-1}, n >= 1."""
    n = np.asarray(n)
    out = np.zeros(n.shape, dtype=float)
    m = n[n >= 1]
    coeff = np.array([comb(int(x) + k - 2, k - 1) for x in m], dtype=float)
    out[n >= 1] = coeff * s**k * rho ** (m - 1)
    return out


# ---------------------------------------------------------------------------
# Theory: times
# ---------------------------------------------------------------------------

def L_T_series(k: int, u: float, beta: float, delta: float) -> float:
    """E[e^{-u T} | k founders] via the defining series (vectorised)."""
    rho = beta / (beta + delta)
    s = delta / (beta + delta)
    gmax = gmax_for(rho)
    g = np.arange(gmax + 1, dtype=float)
    lam = (beta + delta) * (k + g)
    prods = np.cumprod(lam / (lam + u))
    weights = s * rho**g
    return float(np.dot(weights, prods))


def L_T_vec(k_values: np.ndarray, u: float, beta: float, delta: float) -> np.ndarray:
    """L_T(k, u) for an array of k values (row-wise vectorised series)."""
    rho = beta / (beta + delta)
    s = delta / (beta + delta)
    gmax = gmax_for(rho)
    m = np.arange(gmax + 1, dtype=float)
    weights = s * rho**m
    out = np.empty(len(k_values), dtype=float)
    for i, k in enumerate(k_values):
        lam = (beta + delta) * (k + m)
        out[i] = np.dot(weights, np.cumprod(lam / (lam + u)))
    return out


def L_T_hyper(k: int, u: float, beta: float, delta: float) -> float | None:
    """Closed form [s*k/(k+u')] * 2F1(k+1, 1; k+1+u'; rho); None without scipy."""
    try:
        from scipy.special import hyp2f1
    except Exception:
        return None
    rho = beta / (beta + delta)
    s = delta / (beta + delta)
    up = u / (beta + delta)
    return float((s * k / (k + up)) * hyp2f1(k + 1, 1.0, k + 1 + up, rho))


def L_t2(u: float, beta: float, delta: float) -> float:
    """Laplace transform of t_2 = t_1 + T_2."""
    rho = beta / (beta + delta)
    s = delta / (beta + delta)
    gmax = gmax_for(rho)
    g = np.arange(gmax + 1, dtype=float)
    lam = (beta + delta) * (1.0 + g)              # lam_j, j = 1..gmax+1
    P1 = np.cumprod(lam / (lam + u))              # P1[g] = prod_{j=1}^{1+g}
    weights = s * rho**g
    LT = L_T_vec((1 + g).astype(float), u, beta, delta)
    return float(np.dot(weights * P1, LT))


def mean_T_series(k: int, beta: float, delta: float) -> float:
    """E[T | k founders] = sum_{m>=0} rho^m / ((beta+delta)(k+m))."""
    rho = beta / (beta + delta)
    gmax = gmax_for(rho)
    m = np.arange(gmax + 1, dtype=float)
    return float(np.sum(rho**m / ((beta + delta) * (k + m))))


def J_mu0(t: np.ndarray, beta: float, delta: float) -> np.ndarray:
    """Mean of the mu=0 BDC process from one founder."""
    a = 1.0 + delta / beta
    theta = beta * a  # beta(a-b) with b=0
    A = delta / beta
    w = np.exp(theta * t)
    return a**2 * w / (1.0 + A * w) ** 2


def t2_density_exact(grid: np.ndarray, dt: float, beta: float, delta: float,
                     tail: float = 1e-10):
    """Exact density of t_2 as a hypoexponential mixture, computed by
    sequential FFT convolution of exponential densities (numerically stable,
    no partial fractions).

    t_1 | G_1=g1:  sum of Exp(lam_1..lam_{1+g1})            (distinct rates)
    T_2 | g1, g2:  sum of Exp(lam_{1+g1}..lam_{1+g1+g2})    (distinct rates)
    t_2 = t_1 + T_2; the two sums use independent exponentials (rate
    lam_{1+g1} appears once in each), so the density is their convolution.
    """
    rho = beta / (beta + delta)
    s = delta / (beta + delta)
    gmax = int(math.ceil(math.log(tail) / math.log(rho))) + 5
    c = beta + delta

    def fft_conv(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        n = len(a) + len(b) - 1
        nfft = 1 << int(math.ceil(math.log2(n)))
        out = np.fft.irfft(np.fft.rfft(a, nfft) * np.fft.rfft(b, nfft), nfft)
        return out[:len(a)] * dt

    def exp_density(lam: float) -> np.ndarray:
        # normalised to unit rectangle-rule mass: the FFT convolution below
        # conserves that quadrature exactly, so unit-mass factors stay unit-mass
        e = lam * np.exp(-lam * grid)
        return e / (e.sum() * dt)

    # H_list[m] = density of a sum Exp(lam_1..lam_m)  (t_1 given g1 = m-1)
    H0 = np.zeros_like(grid)
    H0[0] = 1.0 / dt  # delta at 0, unit mass
    H_list = [H0]
    for m in range(1, gmax + 3):
        H_list.append(fft_conv(H_list[m - 1], exp_density(c * m)))

    out = np.zeros_like(grid)
    for g1 in range(gmax + 1):
        w1 = s * rho**g1
        h1 = H_list[1 + g1]
        # mix T_2 densities over g2, building incrementally;
        # T_2 | (g1, g2) = sum of Exp(lam_{start}..lam_{start+g2}), start=1+g1
        start = 1 + g1
        R = exp_density(c * start)           # g2 = 0: single exponential
        fT2 = s * R
        for g2 in range(1, gmax + 1):
            R = fft_conv(R, exp_density(c * (start + g2)))
            fT2 = fT2 + (s * rho**g2) * R
        out += w1 * fft_conv(h1, fT2)
    return out


# ---------------------------------------------------------------------------
# Simulation (exact sampling, mu = 0)
# ---------------------------------------------------------------------------

def sample_chains(beta: float, delta: float, n: int, m_cells: int):
    """Exact sampling: G_i ~ Geom0(s); T_i sums independent exponentials.

    Returns sizes r[1..m], cumulative times t[1..m], intervals T[1..m].
    """
    rho = beta / (beta + delta)
    logr = math.log(rho)

    r = np.empty((m_cells, n), dtype=np.int64)
    T = np.empty((m_cells, n), dtype=float)
    k = np.ones(n, dtype=np.int64)

    gcap = int(math.ceil(60.0 / (-logr))) + 30
    for i in range(m_cells):
        g = np.floor(np.log(RNG.random(n)) / logr).astype(np.int64)
        gmax = int(g.max())
        assert gmax <= gcap, f"increase gcap (got {gmax} > {gcap})"
        U = RNG.random((gmax + 1, n))
        acc = np.zeros(n, dtype=float)
        for mm in range(gmax + 1):
            active = g >= mm
            j = k[active] + mm
            acc[active] += -np.log(U[mm, active]) / ((beta + delta) * j)
        r[i] = k + g
        T[i] = acc
        k = r[i]

    t = np.cumsum(T, axis=0)
    return r, t, T


def sample_intervals(beta: float, delta: float, k: int, n: int) -> np.ndarray:
    """Exact samples of T(k): duration of a cell founded by k particles."""
    rho = beta / (beta + delta)
    logr = math.log(rho)
    g = np.floor(np.log(RNG.random(n)) / logr).astype(np.int64)
    gmax = int(g.max())
    U = RNG.random((gmax + 1, n))
    acc = np.zeros(n, dtype=float)
    for mm in range(gmax + 1):
        active = g >= mm
        j = k + mm
        acc[active] += -np.log(U[mm, active]) / ((beta + delta) * j)
    return acc


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def test_A_coefficients() -> None:
    ok = True
    bad = []
    for k in range(2, 9):
        for n in range(1, 12):
            lhs = comb(n + k - 2, k - 1)
            rhs = sum(comb(i + k - 3, k - 2) for i in range(1, n + 1))
            if lhs != rhs:
                ok = False
                bad.append(f"k={k}, n={n}: {lhs} != {rhs}")
    detail = ("A_k^{(n)} = C(n+k-2,k-1) obeys the recurrence for "
              "k=2..8, n=1..11 (exact integers); A_1^{(n)} = 1"
              if ok else "; ".join(bad[:3]))
    check("A.coefficients", ok, detail)


def test_B_pmf(r: np.ndarray, beta: float, delta: float, name: str) -> None:
    rho = beta / (beta + delta)
    s = delta / (beta + delta)
    worst = 0.0
    for k in range(1, M_CELLS + 1):
        mean = 1 + k * rho / s
        nmax = int(mean + 14 * math.sqrt(k * rho) / s + 60)
        n = np.arange(1, nmax + 1)
        theo = pmf_r(k, n, s, rho)
        counts, _ = np.histogram(r[k - 1], bins=np.append(n, nmax + 1) - 0.5)
        exp = N_SIZE * theo
        keep = exp >= 25.0
        if keep.sum() == 0:
            continue
        p_emp = counts[keep] / N_SIZE
        p_theo = theo[keep]
        dev = np.max(np.abs(p_emp - p_theo)
                     / np.sqrt(p_theo * (1 - p_theo) / N_SIZE))
        worst = max(worst, dev)
    check(f"B.pmf[{name}]", worst < 5.0,
          f"max deviation of empirical pmf from C(n+k-2,k-1) s^k rho^(n-1), "
          f"k=1..{M_CELLS}, in SE units: {worst:.2f} (n={N_SIZE})")


def test_C_moments(r: np.ndarray, beta: float, delta: float, name: str) -> None:
    rho = beta / (beta + delta)
    s = delta / (beta + delta)
    worst_m = 0.0
    worst_v = 0.0
    for k in range(1, M_CELLS + 1):
        x = r[k - 1].astype(float)
        m_theo = 1 + k * rho / s
        v_theo = k * rho / s**2
        worst_m = max(worst_m, abs(x.mean() - m_theo) / m_theo)
        worst_v = max(worst_v, abs(x.var() - v_theo) / v_theo)
    check(f"C.moments[{name}]", worst_m < 5e-3 and worst_v < 2e-2,
          f"E[r_k] rel err {worst_m:.1e}; Var(r_k) rel err {worst_v:.1e} "
          f"vs 1+k*rho/s and k*rho/s^2, k=1..{M_CELLS}")


def test_D_pgf(r: np.ndarray, beta: float, delta: float, name: str) -> None:
    rho = beta / (beta + delta)
    s = delta / (beta + delta)
    worst = 0.0
    for z in (0.3, 0.6, 0.9):
        for k in range(1, M_CELLS + 1):
            x = z ** r[k - 1]
            emp = x.mean()
            se = x.std(ddof=1) / math.sqrt(len(x))
            theo = z * (s / (1 - rho * z)) ** k
            worst = max(worst, abs(emp - theo) / max(se, 1e-300))
    check(f"D.pgf[{name}]", worst < 5.0,
          f"max deviation of E[z^r_k] from z(s/(1-rho z))^k, in SE units: "
          f"{worst:.2f} (z in {{0.3,0.6,0.9}}, k=1..{M_CELLS})")


def test_E_t1_density(t: np.ndarray, beta: float, delta: float, name: str):
    t1 = t[0]
    scale = float(np.percentile(t1, 99))
    bins = np.linspace(0, scale, 120)
    hist, edges = np.histogram(t1, bins=bins, density=True)
    mid = 0.5 * (edges[:-1] + edges[1:])
    theo = delta * J_mu0(mid, beta, delta)
    rel = np.sqrt(np.mean((hist - theo) ** 2)) / np.sqrt(np.mean(theo**2))
    check(f"E.t1_density[{name}]", rel < 0.03,
          f"histogram of t_1 vs delta*J(t): rel L2 = {rel:.1e} (n={N_TIME})")
    return mid, hist


def test_F_interval_laplace(beta: float, delta: float, name: str) -> None:
    # fixed-founder transforms against dedicated samples
    worst_ser = 0.0
    worst_hyp = 0.0
    hyp_available = True
    for u in (0.05, 0.2, 1.0):
        for k in (1, 2, 3, 5):
            emp = float(np.mean(np.exp(-u * sample_intervals(beta, delta, k, N_FIXED))))
            ser = L_T_series(k, u, beta, delta)
            worst_ser = max(worst_ser, abs(emp - ser) / ser)
            hyp = L_T_hyper(k, u, beta, delta)
            if hyp is None:
                hyp_available = False
            else:
                worst_hyp = max(worst_hyp, abs(ser - hyp) / hyp)
    ok_fixed = worst_ser < 1e-2 and (not hyp_available or worst_hyp < 1e-10)
    det_fixed = (f"fixed founders k in {{1,2,3,5}}: empirical vs series max rel "
                 f"err {worst_ser:.1e}; series vs 2F1 closed form: "
                 + (f"{worst_hyp:.1e}" if hyp_available else "scipy unavailable"))
    check(f"F.interval_laplace[{name}]", ok_fixed, det_fixed)


def test_F2_mixture(r: np.ndarray, T: np.ndarray, beta: float, delta: float,
                    name: str) -> None:
    # chain intervals: E[e^{-u T_k}] = sum_n pmf_{r_{k-1}}(n) L_T(n, u)
    rho = beta / (beta + delta)
    s = delta / (beta + delta)
    worst = 0.0
    for u in (0.05, 0.5):
        for k in (2, 3):
            emp = float(np.mean(np.exp(-u * T[k - 1])))
            n = np.arange(1, 4000)
            pmf = pmf_r(k - 1, n, s, rho)
            keep = pmf > 1e-15
            n_keep = n[keep]
            theo = float(np.dot(pmf[keep], L_T_vec(n_keep.astype(float), u,
                                                   beta, delta)))
            worst = max(worst, abs(emp - theo) / theo)
    check(f"F2.interval_mixture[{name}]", worst < 1e-2,
          f"chain intervals T_2, T_3 (random founders): empirical vs "
          f"pmf-weighted L_T mixture, max rel err {worst:.1e}")


def test_G_t2_laplace(t: np.ndarray, beta: float, delta: float,
                      name: str) -> None:
    t2 = t[1]
    worst = 0.0
    for u in (0.05, 0.2, 1.0):
        emp = float(np.mean(np.exp(-u * t2)))
        theo = L_t2(u, beta, delta)
        worst = max(worst, abs(emp - theo) / theo)
    check(f"G.t2_laplace[{name}]", worst < 1e-2,
          f"max rel err of empirical E[e^-u t2] vs "
          f"sum_g s rho^g P1(1+g,u) L_T(1+g,u): {worst:.1e}")


def test_H_t2_density(t: np.ndarray, beta: float, delta: float, name: str):
    t2 = t[1]
    scale = float(np.percentile(t2, 98))
    n_bins = 240
    refine = 4
    bins = np.linspace(0, scale, n_bins + 1)
    hist, edges = np.histogram(t2, bins=bins, density=True)
    # exact density on a refined grid, then bin-averaged onto the histogram
    # bins (removes the O(dt) discretisation bias of the convolution chain)
    fine_bins = np.linspace(0, scale, n_bins * refine + 1)
    fine_mid = 0.5 * (fine_bins[:-1] + fine_bins[1:])
    dt_fine = fine_bins[1] - fine_bins[0]
    f_fine = t2_density_exact(fine_mid, dt_fine, beta, delta, tail=1e-8)
    f = f_fine.reshape(n_bins, refine).mean(axis=1)
    rel = np.sqrt(np.mean((hist - f) ** 2)) / np.sqrt(np.mean(f**2))
    mid = 0.5 * (edges[:-1] + edges[1:])
    check(f"H.t2_density[{name}]", rel < 0.06,
          f"histogram of t_2 vs exact hypoexponential-mixture density: "
          f"rel L2 = {rel:.1e}")
    return mid, f, hist


def test_H2_t2_mean(t: np.ndarray, beta: float, delta: float, name: str) -> None:
    """Lightweight exact check for slow sets: E[t_2] = E[t_1] + E[T(r_1)]."""
    rho = beta / (beta + delta)
    s = delta / (beta + delta)
    t2 = t[1]
    n = np.arange(1, 3000)
    pmf = pmf_r(1, n, s, rho)
    keep = pmf > 1e-16
    theo = mean_T_series(1, beta, delta) + float(
        np.dot(pmf[keep],
               np.array([mean_T_series(int(x), beta, delta) for x in n[keep]])))
    emp = float(t2.mean())
    rel = abs(emp - theo) / theo
    check(f"H2.t2_mean[{name}]", rel < 1e-2,
          f"E[t_2]: empirical {emp:.4f} vs exact E[t_1] + E[T(r_1)] {theo:.4f} "
          f"(rel err {rel:.1e})")


def test_I_intervals(T_chain: np.ndarray, beta: float, delta: float, name: str):
    # fixed-founder means: simulation vs exact series, k = 1..6
    worst = 0.0
    for k in (1, 2, 3, 4, 6):
        emp = float(sample_intervals(beta, delta, k, N_FIXED).mean())
        ana = mean_T_series(k, beta, delta)
        worst = max(worst, abs(emp - ana) / ana)
    ana_seq = [mean_T_series(k, beta, delta) for k in range(1, 7)]
    decreasing = all(ana_seq[i + 1] < ana_seq[i] for i in range(len(ana_seq) - 1))
    chain_means = [float(T_chain[k - 1].mean()) for k in range(1, M_CELLS + 1)]
    chain_dec = all(chain_means[i + 1] < chain_means[i]
                    for i in range(len(chain_means) - 1))
    txt = ", ".join(f"E[T({k})]={ana_seq[k - 1]:.3f}" for k in range(1, 5))
    check(f"I.intervals[{name}]", worst < 1e-2 and decreasing and chain_dec,
          f"fixed-founder means strictly decreasing ({txt}, ...); sim vs exact "
          f"series max rel err {worst:.1e}; chain means (random founders) also "
          f"decreasing: {', '.join(f'{m:.3f}' for m in chain_means)}")
    return chain_means


# ---------------------------------------------------------------------------
# Figures (optional)
# ---------------------------------------------------------------------------

def make_figures(fig_data: dict) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        log("[INFO] matplotlib unavailable; skipping figures")
        return
    name, beta, delta = fig_data["set"]
    r, t = fig_data["r"], fig_data["t"]
    rho = beta / (beta + delta)
    s = delta / (beta + delta)
    n_fig = r.shape[1]

    fig, axes = plt.subplots(2, 2, figsize=(11, 8))

    ax = axes[0, 0]
    colors = ["C0", "C1", "C2", "C3"]
    for k in range(1, M_CELLS + 1):
        mean = 1 + k * rho / s
        nmax = int(mean + 10 * math.sqrt(k * rho) / s + 30)
        n = np.arange(1, nmax + 1)
        theo = pmf_r(k, n, s, rho)
        counts, _ = np.histogram(r[k - 1], bins=np.append(n, nmax + 1) - 0.5)
        ax.plot(n, counts / n_fig, "o", ms=3, color=colors[k - 1], alpha=0.5)
        ax.plot(n, theo, "-", color=colors[k - 1], label=f"$r_{k}$")
    ax.set_xlabel("$n$")
    ax.set_ylabel("$\\Pr\\{r_k = n\\}$")
    ax.set_title("Rupture-size laws (points: sim; lines: theory)")
    ax.legend(fontsize=7)

    ax = axes[0, 1]
    mid, hist = fig_data["t1"]
    ax.bar(mid, hist, width=mid[1] - mid[0], color="0.75", label="sim")
    ax.plot(mid, delta * J_mu0(mid, beta, delta), "r-", lw=2, label="$\\delta J(t)$")
    ax.set_xlabel("$t$")
    ax.set_ylabel("density")
    ax.set_title("First rupture time")
    ax.legend()

    ax = axes[1, 0]
    mid, f_exact, hist = fig_data["t2"]
    ax.bar(mid, hist, width=mid[1] - mid[0], color="0.75", label="sim")
    ax.plot(mid, f_exact, "r-", lw=2, label="exact mixture")
    ax.set_xlabel("$t$")
    ax.set_ylabel("density")
    ax.set_title("Second rupture time")
    ax.legend()

    ax = axes[1, 1]
    means = fig_data["means"]
    ax.plot(range(1, len(means) + 1), means, "o-")
    ax.set_xlabel("rupture index $k$")
    ax.set_ylabel("chain mean of $T_k$")
    ax.set_title("Inter-rupture intervals shrink as load grows")
    ax.set_xticks(range(1, len(means) + 1))

    fig.suptitle(f"Chained immediate transfer ($\\mu=0$): "
                 f"$(\\beta,\\delta)=({beta},{delta})$, $s={s:.3f}$, $\\rho={rho:.3f}$")
    fig.tight_layout()
    out = os.path.join(OUTDIR, "verify_chained_transfer_figures.pdf")
    fig.savefig(out)
    plt.close(fig)
    log(f"[INFO] wrote {out}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    t0 = time.time()
    log("=" * 72)
    log("Chained immediate-transfer model (mu = 0) --- verification suite")
    log("=" * 72)
    log(f"chains: {N_SIZE} (sizes), {N_TIME} (times); cells per chain: {M_CELLS}; "
        f"fixed-founder samples: {N_FIXED}")

    log("\n" + "=" * 72)
    log("TEST A --- coefficient identity (exact)")
    log("=" * 72)
    test_A_coefficients()

    fig_data = {}
    for name, beta, delta in PARAM_SETS:
        rho = beta / (beta + delta)
        s = delta / (beta + delta)
        log("\n" + "=" * 72)
        log(f"Parameter set '{name}': beta={beta}, delta={delta} "
            f"(s={s:.4f}, rho={rho:.4f})")
        log("=" * 72)
        r_s, _, _ = sample_chains(beta, delta, N_SIZE, M_CELLS)
        r_t, t_t, T_t = sample_chains(beta, delta, N_TIME, M_CELLS)
        test_B_pmf(r_s, beta, delta, name)
        test_C_moments(r_s, beta, delta, name)
        test_D_pgf(r_s, beta, delta, name)
        t1_data = test_E_t1_density(t_t, beta, delta, name)
        test_F_interval_laplace(beta, delta, name)
        test_F2_mixture(r_t, T_t, beta, delta, name)
        test_G_t2_laplace(t_t, beta, delta, name)
        if name == "slow_burst":
            # exact density double-sum is heavy at rho ~ 0.91; use exact mean
            test_H2_t2_mean(t_t, beta, delta, name)
            t2_data = None
        else:
            t2_data = test_H_t2_density(t_t, beta, delta, name)
        means = test_I_intervals(T_t, beta, delta, name)
        if name == "symmetric":
            fig_data = {
                "set": (name, beta, delta),
                "r": r_t,
                "t": t_t,
                "t1": t1_data,
                "t2": t2_data,
                "means": means,
            }

    make_figures(fig_data)

    dt = time.time() - t0
    log("\n" + "=" * 72)
    log(f"TOTAL: {n_pass} PASS / {n_fail} FAIL  ({n_pass + n_fail} checks, "
        f"wall time {dt:.1f} s)")
    log("=" * 72)

    metrics["total"] = {"pass": n_pass, "fail": n_fail, "wall_s": round(dt, 1)}
    with open(os.path.join(OUTDIR, "verify_chained_transfer_report.txt"), "w") as f:
        f.write("\n".join(report_lines) + "\n")
    with open(os.path.join(OUTDIR, "verify_chained_transfer_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)
    if n_fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
