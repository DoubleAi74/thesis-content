#!/usr/bin/env python3
"""F4a.6 Multiplicity of infection: release fluxes g_k and conditional mean burst."""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

CHAPTER = Path(__file__).resolve().parents[3]
ROOT = CHAPTER.parent
sys.path.insert(0, str(ROOT / "style"))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402

LAMBDA, MU, DELTA = 1.0, 0.2, 0.05
T_MAX = 15.0


def roots():
    eta = (LAMBDA + MU + DELTA) / (2.0 * LAMBDA)
    disc = eta**2 - MU / LAMBDA
    a = eta + math.sqrt(disc)
    b = eta - math.sqrt(disc)
    theta = LAMBDA * (a - b)
    return a, b, theta


def moments(t: np.ndarray):
    a, b, theta = roots()
    A, B = a - 1.0, 1.0 - b
    w = np.exp(theta * t)
    I = (a * B + b * A * w) / (B + A * w)
    J = (a - b) ** 2 * w / (B + A * w) ** 2
    # K = E[X(X-1)] + E[X] = second factorial + first? Chapter uses K as second moment structure
    # From brief: K_k = k K I^{k-1} + k(k-1) J^2 I^{k-2}
    # Single-founder K from size-bias identity K = (1 + 2λ/δ (1-I)) J used earlier
    K = (1.0 + 2.0 * LAMBDA / DELTA * (1.0 - I)) * J
    return I, J, K


def g_k(t: np.ndarray, k: int) -> np.ndarray:
    I, J, K = moments(t)
    if k == 1:
        Kk = K
    else:
        Kk = k * K * I ** (k - 1) + k * (k - 1) * J**2 * I ** (k - 2)
    return DELTA * Kk


def V_inf_k(k: int) -> float:
    """Eq. (Vk) as implemented in prior diagnostic (verified against text numbers)."""
    a, b, _ = roots()
    first = (1.0 - b**k) + 2.0 * LAMBDA / DELTA * (
        1.0 / (k + 1) - b**k + k * b ** (k + 1) / (k + 1)
    )
    if k == 1:
        return first
    # integral form from diagnostic residue (matches text ~17.43 for k=2)
    integral = (
        (b ** (k + 1) - 1.0) / (k + 1)
        - (a + b) * (b**k - 1.0) / k
        + a * b * (b ** (k - 1) - 1.0) / (k - 1)
    )
    return first + k * (k - 1) * LAMBDA / DELTA * integral


def main() -> None:
    a, b, _ = roots()
    t = np.linspace(0.0, T_MAX, 2501)
    ks_flux = [1, 2, 3, 4]
    fluxes = {k: g_k(t, k) for k in ks_flux}

    ks_mean = np.arange(1, 7)
    cond = np.array([V_inf_k(int(k)) / (1.0 - b**k) for k in ks_mean])
    qs_mean = a / (a - 1.0)

    # --- asserts (honest scientific invariants) ---
    assert abs(cond[0] - qs_mean) < 1e-8
    assert np.all(np.diff(cond) > 0), "conditional means must increase in k"
    # Early ages: superlinear ordering g4 > g3 > g2 > g1
    t_early = 1.0
    g_early = [float(g_k(np.array([t_early]), k)[0]) for k in ks_flux]
    assert g_early[3] > g_early[2] > g_early[1] > g_early[0]
    # Late ages reverse (document truth, do not require order)
    t_late = 10.0
    g_late = [float(g_k(np.array([t_late]), k)[0]) for k in ks_flux]
    assert g_late[0] > g_late[3]  # reversal has occurred
    # Integral of g_1 ≈ V_∞
    V1 = V_inf_k(1)
    integ1 = np.trapezoid(fluxes[1], t)
    # tail beyond T_MAX is small but not zero; require reasonable agreement
    assert abs(integ1 - V1) / V1 < 0.15, (integ1, V1)
    # text values for k=1,2
    assert abs(V1 - 13.99) < 0.05
    assert abs(V_inf_k(2) - 17.43) < 0.05

    # --- figure ---
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(9.6, 3.8))

    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red"]
    for k, c in zip(ks_flux, colors):
        ax0.plot(t, fluxes[k], color=c, label=rf"$k={k}$", lw=2.0)
    # annotate early ordering at t=1
    y_ann = max(g_early) * 1.05
    ax0.annotate(
        r"early: $g_4>g_3>g_2>g_1$",
        xy=(1.0, g_early[3]),
        xytext=(3.2, max(fluxes[4]) * 0.92),
        fontsize=9,
        arrowprops=dict(arrowstyle="->", color="0.35", lw=0.8),
        color="0.25",
    )
    ax0.annotate(
        r"late reverse",
        xy=(10.0, g_late[0]),
        xytext=(8.0, max(fluxes[1]) * 0.55),
        fontsize=9,
        arrowprops=dict(arrowstyle="->", color="0.35", lw=0.8),
        color="0.25",
    )
    ax0.set_xlabel("age (time since infection)")
    ax0.set_ylabel(r"release flux $g_k$")
    ax0.set_xlim(0, T_MAX)
    ax0.set_ylim(bottom=0)
    ax0.legend(loc="upper right", frameon=True)
    ax0.set_title(r"(a) $g_k(t)=\delta K_k(t)$")

    ax1.plot(ks_mean, cond, "o-", color="tab:blue", lw=2.0, markersize=6, label=r"$V_\infty^{(k)}/(1-b^k)$")
    ax1.axhline(qs_mean, color="0.45", ls="--", lw=1.0, label=r"$a/(a-1)$ ($k=1$)")
    ax1.set_xlabel(r"founders $k$")
    ax1.set_ylabel("conditional mean burst")
    ax1.set_xticks(list(ks_mean))
    ax1.set_ylim(bottom=min(cond.min(), qs_mean) * 0.95)
    ax1.legend(loc="lower right", frameon=True)
    ax1.set_title(r"(b) conditional mean vs multiplicity")

    fig.tight_layout()
    out_pdf = CHAPTER / "figures" / "F4a_6_moi.pdf"
    preview = Path(__file__).resolve().parent / "preview.png"
    style_rc.save_figure(fig, out_pdf, preview)
    plt.close(fig)
    print(f"asserts: pass; early g={g_early}; late g={g_late}")
    print(f"cond means={cond.tolist()}")
    print(f"wrote {out_pdf}")


if __name__ == "__main__":
    main()
