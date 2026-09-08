#!/usr/bin/env python3
"""
fig_bio_regimes — Three-panel application figure for competing catastrophe-rate hypotheses.

Panel A: compact intracellular schematic (early / conversion / adapted →
         containment failure).
Panel B: S(t) for EQ, MAT, GATE, EARLY under shared growth rates.
Panel C: q_S(t) = -S'(t)/S(t) for the same four regimes.

Parameters are illustrative only (not fitted). Catastrophe-rate pairs satisfy
δ1+δ2=c as an illustrative normalisation of the two per-capita coefficients,
not as matched realised catastrophe rate (realised catastrophe rate is δ1 Xt + δ2 Yt).

Seed parameters (plan §8.3):
  λ1=1.0, μ1=0.45, ν=0.35, λ2=0.85, μ2=0.40, c=0.30
  EQ (0.15,0.15); MAT (0.05,0.25); GATE (0.00,0.30); EARLY (0.25,0.05)

Final parameters: identical to seed (no adjustment after pilot — curves
separate cleanly, GATE S'(0)=0 is visible, numerics stable).

Regenerate from project root:
    python figures/fig_bio_regimes/src/generate_fig_bio_regimes.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches, rcParams
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE.parent
sys.path.insert(0, str(HERE))

from bdc_closed_forms import BDCClosedForm, Rates  # noqa: E402

# ---------------------------------------------------------------------------
# Style (SHARED_CONVENTIONS)
# ---------------------------------------------------------------------------
BLUE = "#0072B2"
VERM = "#D55E00"
TEAL = "#009E73"
PURPLE = "#6B4C9A"
INK = "#1a1c1f"
INK_SOFT = "#565b62"
GRID = "#e3e6ea"
SOFT_FILL = "#fafafa"
EARLY_FILL = "#d6eaf8"
ADAPT_FILL = "#fde8d8"
FAIL_FILL = "#f2dede"

# Regime colours (colourblind-safe set)
REGIME_STYLE = {
    "EQ": {"color": BLUE, "ls": "-", "lw": 2.15},
    "MAT": {"color": VERM, "ls": "-", "lw": 2.15},
    "GATE": {"color": TEAL, "ls": (0, (5, 2.2)), "lw": 2.25},
    "EARLY": {"color": PURPLE, "ls": (0, (1.2, 1.4)), "lw": 2.15},
}

rcParams.update(
    {
        "font.family": "serif",
        "font.serif": [
            "DejaVu Serif",
            "Times New Roman",
            "Times",
            "Computer Modern Roman",
        ],
        "mathtext.fontset": "cm",
        "axes.linewidth": 0.9,
        "axes.labelsize": 13.2,
        "axes.titlesize": 13.8,
        "xtick.labelsize": 11.4,
        "ytick.labelsize": 11.4,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.top": True,
        "ytick.right": True,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "legend.fontsize": 10.32,
        "legend.frameon": False,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)

# ---------------------------------------------------------------------------
# Parameters (seed = final; documented in meta.json)
# ---------------------------------------------------------------------------
SEED_PARAMETERS = {
    "lambda1": 1.0,
    "mu1": 0.45,
    "nu": 0.35,
    "lambda2": 0.85,
    "mu2": 0.40,
    "c": 0.30,
    "regimes": {
        "EQ": {"delta1": 0.15, "delta2": 0.15},
        "MAT": {"delta1": 0.05, "delta2": 0.25},
        "GATE": {"delta1": 0.00, "delta2": 0.30},
        "EARLY": {"delta1": 0.25, "delta2": 0.05},
    },
}
FINAL_PARAMETERS = SEED_PARAMETERS  # no post-pilot adjustment
ADJUSTMENT_REASON = "none; seed parameters retained after pilot inspection"

T_MAX = 12.0
N_PLOT = 600
N_VAL = 2401
DT_SUB = 0.003
ORDER = ("EQ", "MAT", "GATE", "EARLY")


def make_rates(delta1: float, delta2: float) -> Rates:
    p = FINAL_PARAMETERS
    return Rates(
        p["lambda1"],
        p["mu1"],
        p["nu"],
        delta1,
        p["lambda2"],
        p["mu2"],
        delta2,
    )


def rhs_G(G: float, p: Rates) -> float:
    return p.lambda2 * G * G - (p.lambda2 + p.mu2 + p.delta2) * G + p.mu2


def rhs_S(S: float, G: float, p: Rates) -> float:
    return (
        p.lambda1 * S * S
        - (p.lambda1 + p.mu1 + p.nu + p.delta1) * S
        + p.mu1
        + p.nu * G
    )


def rk4_SG(t_grid: np.ndarray, p: Rates) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Fixed-step RK4 of unscaled triangular system; also return S' from RHS."""
    n = len(t_grid)
    S = np.empty(n, dtype=float)
    G = np.empty(n, dtype=float)
    Sp = np.empty(n, dtype=float)
    s, g = 1.0, 1.0
    S[0], G[0] = 1.0, 1.0
    Sp[0] = rhs_S(s, g, p)
    for i in range(1, n):
        dt = float(t_grid[i] - t_grid[i - 1])
        nsub = max(1, int(np.ceil(dt / DT_SUB)))
        h = dt / nsub
        for _ in range(nsub):
            k1g = rhs_G(g, p)
            k1s = rhs_S(s, g, p)
            k2g = rhs_G(g + 0.5 * h * k1g, p)
            k2s = rhs_S(s + 0.5 * h * k1s, g + 0.5 * h * k1g, p)
            k3g = rhs_G(g + 0.5 * h * k2g, p)
            k3s = rhs_S(s + 0.5 * h * k2s, g + 0.5 * h * k2g, p)
            k4g = rhs_G(g + h * k3g, p)
            k4s = rhs_S(s + h * k3s, g + h * k3g, p)
            g += (h / 6.0) * (k1g + 2 * k2g + 2 * k3g + k4g)
            s += (h / 6.0) * (k1s + 2 * k2s + 2 * k3s + k4s)
        S[i], G[i] = s, g
        Sp[i] = rhs_S(s, g, p)
    return S, G, Sp


def cf_S(p: Rates, t: np.ndarray) -> np.ndarray:
    sol = BDCClosedForm(p)
    return np.array([sol.S(float(ti)) for ti in t], dtype=float)


def panel_label(ax, letter: str, x: float = 0.02, y: float = 0.96):
    ax.text(
        x,
        y,
        f"({letter})",
        transform=ax.transAxes,
        fontsize=15.6,
        fontweight="bold",
        va="top",
        ha="left",
        color=INK,
    )


def draw_schematic(ax):
    """Panel A: compact process schematic (not a quantitative panel)."""
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.axis("off")
    ax.set_facecolor("white")

    # Early phenotype box
    early = patches.FancyBboxPatch(
        (0.35, 2.55),
        2.55,
        2.1,
        boxstyle="round,pad=0.08,rounding_size=0.18",
        facecolor=EARLY_FILL,
        edgecolor=BLUE,
        linewidth=1.4,
        zorder=2,
    )
    ax.add_patch(early)
    ax.text(
        1.62,
        4.0,
        "Early phenotype",
        ha="center",
        va="center",
        fontsize=9.5,
        color=INK,
        fontweight="bold",
        zorder=3,
    )
    ax.text(
        1.62,
        3.45,
        r"$X_t$  (type 1)",
        ha="center",
        va="center",
        fontsize=9.0,
        color=BLUE,
        zorder=3,
    )
    ax.text(
        1.62,
        2.95,
        r"birth $\lambda_1$ / death $\mu_1$",
        ha="center",
        va="center",
        fontsize=8.0,
        color=INK_SOFT,
        zorder=3,
    )

    # Adapted phenotype box
    adapted = patches.FancyBboxPatch(
        (4.0, 2.55),
        2.55,
        2.1,
        boxstyle="round,pad=0.08,rounding_size=0.18",
        facecolor=ADAPT_FILL,
        edgecolor=VERM,
        linewidth=1.4,
        zorder=2,
    )
    ax.add_patch(adapted)
    ax.text(
        5.27,
        4.0,
        "Adapted phenotype",
        ha="center",
        va="center",
        fontsize=9.5,
        color=INK,
        fontweight="bold",
        zorder=3,
    )
    ax.text(
        5.27,
        3.45,
        r"$Y_t$  (type 2)",
        ha="center",
        va="center",
        fontsize=9.0,
        color=VERM,
        zorder=3,
    )
    ax.text(
        5.27,
        2.95,
        r"birth $\lambda_2$ / death $\mu_2$",
        ha="center",
        va="center",
        fontsize=8.0,
        color=INK_SOFT,
        zorder=3,
    )

    # Conversion arrow
    ax.annotate(
        "",
        xy=(3.95, 3.6),
        xytext=(2.95, 3.6),
        arrowprops=dict(arrowstyle="->", color=INK, lw=1.6),
        zorder=4,
    )
    ax.text(
        3.45,
        3.95,
        r"conversion $\nu$",
        ha="center",
        va="bottom",
        fontsize=8.2,
        color=INK,
        zorder=4,
    )
    ax.text(
        3.45,
        3.15,
        "(one-way)",
        ha="center",
        va="top",
        fontsize=7.5,
        color=INK_SOFT,
        zorder=4,
    )

    # Containment-failure sink
    fail = patches.FancyBboxPatch(
        (7.45, 2.55),
        2.25,
        2.1,
        boxstyle="round,pad=0.08,rounding_size=0.18",
        facecolor=FAIL_FILL,
        edgecolor="#9a2820",
        linewidth=1.4,
        zorder=2,
    )
    ax.add_patch(fail)
    ax.text(
        8.57,
        3.85,
        "Containment\nfailure",
        ha="center",
        va="center",
        fontsize=9.3,
        color="#9a2820",
        fontweight="bold",
        zorder=3,
        linespacing=1.15,
    )
    ax.text(
        8.57,
        2.95,
        r"(absorbing $\tau_c$)",
        ha="center",
        va="center",
        fontsize=8.0,
        color=INK_SOFT,
        zorder=3,
    )

    # Catastrophe arrows into failure
    ax.annotate(
        "",
        xy=(7.4, 4.15),
        xytext=(2.95, 4.55),
        arrowprops=dict(
            arrowstyle="->",
            color=BLUE,
            lw=1.35,
            connectionstyle="arc3,rad=-0.22",
        ),
        zorder=4,
    )
    ax.text(
        4.55,
        5.05,
        r"per-capita $\delta_1$",
        ha="center",
        va="bottom",
        fontsize=8.0,
        color=BLUE,
        zorder=4,
    )

    ax.annotate(
        "",
        xy=(7.4, 3.05),
        xytext=(6.6, 3.05),
        arrowprops=dict(arrowstyle="->", color=VERM, lw=1.45),
        zorder=4,
    )
    ax.text(
        6.95,
        2.55,
        r"$\delta_2$",
        ha="center",
        va="top",
        fontsize=8.5,
        color=VERM,
        zorder=4,
    )

    # Catastrophe rate note
    ax.text(
        5.0,
        1.55,
        r"process catastrophe rate $=\delta_1 X_t+\delta_2 Y_t$",
        ha="center",
        va="center",
        fontsize=9.0,
        color=INK,
        zorder=3,
        bbox=dict(
            boxstyle="round,pad=0.28",
            facecolor=SOFT_FILL,
            edgecolor=GRID,
            linewidth=0.8,
        ),
    )
    ax.text(
        5.0,
        0.65,
        "Extracellular expansion after $\\tau_c$ lies beyond the model",
        ha="center",
        va="center",
        fontsize=8.0,
        color=INK_SOFT,
        style="italic",
        zorder=3,
    )

    ax.set_title(
        "Intracellular reading (schematic)",
        pad=4,
        color=INK,
        fontsize=11.2,
    )
    panel_label(ax, "A", x=0.01, y=0.98)


def main():
    t = np.linspace(0.0, T_MAX, N_PLOT)
    t_val = np.linspace(0.0, T_MAX, N_VAL)

    curves_S: dict[str, np.ndarray] = {}
    curves_q: dict[str, np.ndarray] = {}
    val_records = []

    for name in ORDER:
        d1 = FINAL_PARAMETERS["regimes"][name]["delta1"]
        d2 = FINAL_PARAMETERS["regimes"][name]["delta2"]
        p = make_rates(d1, d2)
        sol = BDCClosedForm(p)

        # Closed form for plotting S
        S_cf = cf_S(p, t)
        curves_S[name] = S_cf

        # ODE path for S' and q_S (stable; avoids differentiating hypergeometric noise)
        S_ode, G_ode, Sp_ode = rk4_SG(t, p)
        # Protect against tiny S near forever-avoidance floor
        q = np.where(S_ode > 1e-12, -Sp_ode / S_ode, np.nan)
        curves_q[name] = q

        # Validation on dense grid
        S_cf_v = cf_S(p, t_val)
        S_rk, G_rk, _ = rk4_SG(t_val, p)
        G_cf_v = np.array([sol.G(float(ti)) for ti in t_val], dtype=float)
        rec = {
            "regime": name,
            "delta1": d1,
            "delta2": d2,
            "branch": sol.branch,
            "max_abs_S": float(np.max(np.abs(S_cf_v - S_rk))),
            "max_abs_G": float(np.max(np.abs(G_cf_v - G_rk))),
            "S_prime_0_ode": float(Sp_ode[0]),
            "expected_S_prime_0": -d1,
            "h": float(sol.constants.get("h", sol.constants.get("S_inf", np.nan))),
            "r2_minus": float(
                sol.constants.get("r2_minus", sol.constants.get("G_inf", np.nan))
            ),
        }
        val_records.append(rec)

    max_err_S = max(r["max_abs_S"] for r in val_records)
    max_err_G = max(r["max_abs_G"] for r in val_records)

    # ------------------------------------------------------------------
    # Figure layout: two graph panels only (S and q_S)
    # ------------------------------------------------------------------
    fig, (ax_b, ax_c) = plt.subplots(
        1,
        2,
        figsize=(11.2, 4.15),
        gridspec_kw={"wspace": 0.28},
    )
    fig.subplots_adjust(left=0.07, right=0.985, top=0.90, bottom=0.14)

    # Panel A: S(t)
    for name in ORDER:
        st = REGIME_STYLE[name]
        d1 = FINAL_PARAMETERS["regimes"][name]["delta1"]
        d2 = FINAL_PARAMETERS["regimes"][name]["delta2"]
        ax_b.plot(
            t,
            curves_S[name],
            color=st["color"],
            ls=st["ls"],
            lw=st["lw"],
            label=rf"{name}: $(\delta_1,\delta_2)=({d1:g},{d2:g})$",
            zorder=3,
        )
    ax_b.set_xlim(0.0, T_MAX)
    ax_b.set_ylim(0.0, 1.05)
    ax_b.set_xlabel(r"physical time $t$")
    ax_b.set_ylabel(r"$S(t)=\mathbb{P}_{(1,0)}\{\tau_c>t\}$")
    ax_b.set_title(
        r"(A)  Containment survival from one early founder",
        pad=12,
        color=INK,
        loc="left",
    )
    ax_b.grid(True, color=GRID, lw=0.55, zorder=0)
    for spine in ax_b.spines.values():
        spine.set_color(INK)
    ax_b.legend(loc="upper right", fontsize=9.84, handlelength=2.4)

    # Panel B: q_S(t)
    for name in ORDER:
        st = REGIME_STYLE[name]
        ax_c.plot(
            t,
            curves_q[name],
            color=st["color"],
            ls=st["ls"],
            lw=st["lw"],
            label=name,
            zorder=3,
        )
    ax_c.set_xlim(0.0, T_MAX)
    ymax = max(float(np.nanmax(curves_q[n])) for n in ORDER)
    ax_c.set_ylim(0.0, max(0.35, 1.12 * ymax))
    ax_c.set_xlabel(r"physical time $t$")
    ax_c.set_ylabel(r"$q_S(t)=-S'(t)/S(t)$")
    ax_c.set_title(
        r"(B)  Conditional catastrophe intensity",
        pad=12,
        color=INK,
        loc="left",
    )
    ax_c.grid(True, color=GRID, lw=0.55, zorder=0)
    for spine in ax_c.spines.values():
        spine.set_color(INK)
    # Mark general GATE fact S'(0)=0 ⇒ q_S(0)=0
    ax_c.plot(0.0, 0.0, "o", color=TEAL, ms=5.5, zorder=5)
    ax_c.annotate(
        r"GATE: $S'(0)=0$",
        xy=(0.0, 0.0),
        xytext=(2.4, 0.04),
        fontsize=9.84,
        color=TEAL,
        arrowprops=dict(arrowstyle="->", color=TEAL, lw=0.9),
    )
    ax_c.legend(
        handles=[
            Line2D(
                [0],
                [0],
                color=REGIME_STYLE[n]["color"],
                ls=REGIME_STYLE[n]["ls"],
                lw=2.0,
                label=n,
            )
            for n in ORDER
        ],
        loc="upper right",
        fontsize=10.08,
        handlelength=2.4,
    )


    png_path = OUT_DIR / "fig_bio_regimes.png"
    pdf_path = OUT_DIR / "fig_bio_regimes.pdf"
    fig.savefig(png_path, dpi=350, bbox_inches="tight")
    fig.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)

    meta = {
        "figure": "fig_bio_regimes",
        "slug": "bio_regimes",
        "method": "closed_form_S_plus_RK4_unscaled_backward_ODEs_for_qS_and_validation",
        "seed_parameters": SEED_PARAMETERS,
        "final_parameters": FINAL_PARAMETERS,
        "adjustment_reason": ADJUSTMENT_REASON,
        "t_max": T_MAX,
        "validation": {
            "method": (
                f"fixed-step RK4 of unscaled triangular ODEs vs closed form; "
                f"t∈[0,{T_MAX}], {N_VAL} points, substep≈{DT_SUB}"
            ),
            "regimes": val_records,
            "max_abs_error_S": max_err_S,
            "max_abs_error_G": max_err_G,
            "q_S_source": "ODE right-hand side S' along RK4 path; q_S=-S'/S",
            "note_normalisation": (
                "δ1+δ2=c is an illustrative normalisation of per-capita "
                "coefficients, not matched realised catastrophe rate δ1 Xt + δ2 Yt"
            ),
            "note_GATE": (
                "GATE is an idealised boundary of the maturation-associated family; "
                "under δ1+δ2=c both coefficients differ from MAT — not a one-parameter reduction"
            ),
        },
        "outputs": ["fig_bio_regimes.png", "fig_bio_regimes.pdf"],
    }
    with open(OUT_DIR / "meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")

    caption = f"""Illustrative competing catastrophe-rate regimes under an intracellular *Y.\\,pestis* reading.
(A)~Schematic mapping: early and adapted intracellular phenotypes convert one-way;
each type contributes a per-capita route into a single absorbing containment-failure
state. Extracellular expansion after $\\tau_c$ lies beyond the model.
(B)~Containment survival $S(t)$ from one early founder under four catastrophe-rate hypotheses.
(C)~Conditional catastrophe intensity $q_S(t)=-S'(t)/S(t)$ among still-contained infections.
Catastrophe-rate pairs satisfy $\\delta_1+\\delta_2=c$ as an **illustrative normalisation** of the
two per-capita coefficients across regimes, **not** as matched realised catastrophe rate; the
process catastrophe rate remains $\\delta_1 X_t+\\delta_2 Y_t$ and differs across regimes through
composition. Shared rates:
$\\lambda_1={FINAL_PARAMETERS['lambda1']}$,
$\\mu_1={FINAL_PARAMETERS['mu1']}$,
$\\nu={FINAL_PARAMETERS['nu']}$,
$\\lambda_2={FINAL_PARAMETERS['lambda2']}$,
$\\mu_2={FINAL_PARAMETERS['mu2']}$,
$c={FINAL_PARAMETERS['c']}$;
EQ $(\\delta_1,\\delta_2)=(0.15,0.15)$,
MAT $(0.05,0.25)$,
GATE $(0.00,0.30)$,
EARLY $(0.25,0.05)$.
Parameters are **not fitted** to data; biological labels are an interpretation.
GATE is an idealised boundary of the maturation-associated family ($S'(0)=0$);
under the coefficient normalisation both $\\delta_1$ and $\\delta_2$ differ from MAT,
so GATE is **not** a one-parameter reduction of MAT.
Curves from the exact closed form for $S$; $q_S$ from the ODE right-hand side along
the solution path. Validation: fixed-step RK4 of the unscaled backward equations
agrees with the closed form to max $|S_{{\\mathrm{{CF}}}}-S_{{\\mathrm{{RK4}}}}|={max_err_S:.2e}$
(and max $|G|$ discrepancy ${max_err_G:.2e}$) on a dense grid $t\\in[0,{T_MAX}]$.
"""
    with open(OUT_DIR / "caption.md", "w", encoding="utf-8") as f:
        f.write(caption.strip() + "\n")

    readme = """# fig_bio_regimes

Three-panel application figure: schematic + $S(t)$ + $q_S(t)$ for EQ / MAT / GATE / EARLY.

## Regenerate

From project root:

```bash
python figures/fig_bio_regimes/src/generate_fig_bio_regimes.py
```

Requires: `numpy`, `matplotlib`. Closed forms in `src/bdc_closed_forms.py`.

## Parameters

See `meta.json` for `seed_parameters`, `final_parameters`, and `adjustment_reason`.
"""
    with open(OUT_DIR / "README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print(f"Wrote {png_path}")
    print(f"Wrote {pdf_path}")
    print(f"max |S_CF − S_RK4| = {max_err_S:.3e}")
    print(f"max |G_CF − G_RK4| = {max_err_G:.3e}")
    for r in val_records:
        print(
            f"  {r['regime']}: branch={r['branch']}  "
            f"errS={r['max_abs_S']:.2e}  errG={r['max_abs_G']:.2e}  "
            f"S'(0)_ode={r['S_prime_0_ode']:+.4f} (expect {-r['delta1']:+.4f})"
        )
    return max_err_S, max_err_G


if __name__ == "__main__":
    main()
