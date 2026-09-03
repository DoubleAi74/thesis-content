#!/usr/bin/env python3
"""Generate N4b.7: survival and release kernels in three flooding regimes."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/bdc_odes_n4b7_mplconfig")

import numpy as np
from numpy.polynomial.legendre import leggauss

sys.path.insert(
    0,
    "/Users/adamaldridge/Desktop/Thesis content 🎓 /4 BDC additional and BMVR/Figures run/style",
)
import style_rc  # noqa: E402

style_rc.apply()

import matplotlib.pyplot as plt  # noqa: E402


WORKDIR = Path(__file__).resolve().parent
CHAPTER_DIR = WORKDIR.parents[2]
PDF_PATH = CHAPTER_DIR / "figures" / "N4b_7_kernels_three_regimes.pdf"
PNG_PATH = WORKDIR / "preview.png"

_NODES, _WEIGHTS = leggauss(360)
_X = 0.5 * (_NODES + 1.0)
_WEIGHTS = 0.5 * _WEIGHTS


@dataclass(frozen=True)
class Regime:
    lam: float
    mu: float
    delta: float
    relation: str
    parameters: str
    colour: str
    linestyle: str
    survival_story: str
    release_story: str

    @property
    def roots(self) -> tuple[float, float]:
        eta = (self.lam + self.mu + self.delta) / (2.0 * self.lam)
        radical = np.sqrt(eta**2 - self.mu / self.lam)
        return float(eta + radical), float(eta - radical)

    @property
    def derived(self) -> tuple[float, float, float, float]:
        a, b = self.roots
        flooding_parameter = a * (1.0 - b)
        v_inf = flooding_parameter / (a - 1.0)
        productive_lifetime = np.log(a / (a - 1.0)) / self.lam
        return a, b, flooding_parameter, v_inf, productive_lifetime


REGIMES = (
    Regime(
        1.0,
        0.0,
        0.1,
        r"$L>1$",
        r"$(1,0,0.1)$",
        "#1f77b4",
        "-",
        "no internal death\nlong-lived survival",
        "release accumulates\na late, high-yield pulse",
    ),
    Regime(
        1.0,
        0.5,
        1.0 / 3.0,
        r"$L=1$",
        r"$(1,0.5,1/3)$",
        "#6b4c9a",
        "--",
        "boundary regime\nrapid survival loss",
        "release arrives earlier\na moderate pulse",
    ),
    Regime(
        1.0,
        0.9,
        0.1,
        r"$L<1$",
        r"$(1,0.9,0.1)$",
        "#ff7f0e",
        "-.",
        "internal loss\na longer survival tail",
        "loss spreads release\na broad, low-yield pulse",
    ),
)


def kernels(t: np.ndarray, regime: Regime) -> tuple[np.ndarray, np.ndarray]:
    """Return I_fix(t) and g(t)=delta*K(t) from the chapter closed forms."""
    a, b, _, _, _ = regime.derived
    cap_a = a - 1.0
    cap_b = 1.0 - b
    theta = regime.lam * (a - b)
    t_arr = np.asarray(t, dtype=float)
    w = np.exp(theta * t_arr)
    fixation_i = (a * cap_b + b * cap_a * w) / (cap_b + cap_a * w)
    first_moment_j = (a - b) ** 2 * w / (cap_b + cap_a * w) ** 2
    second_moment_k = (
        1.0 + 2.0 * regime.lam / regime.delta * (1.0 - fixation_i)
    ) * first_moment_j
    productive_survival = (
        (a - b) ** 2
        * w
        / ((cap_b + cap_a * w) * (a * w - b))
    )
    return productive_survival, regime.delta * second_moment_k


def kernel_integrals(regime: Regime) -> tuple[float, float]:
    """Integrate I_fix and g over [0,infinity) after x=exp(-theta*t)."""
    a, b, _, _, _ = regime.derived
    cap_a = a - 1.0
    cap_b = 1.0 - b
    theta = regime.lam * (a - b)
    x = _X
    fixation_i = (a * cap_b * x + b * cap_a) / (cap_b * x + cap_a)
    first_moment_j = (a - b) ** 2 * x / (cap_b * x + cap_a) ** 2
    second_moment_k = (
        1.0 + 2.0 * regime.lam / regime.delta * (1.0 - fixation_i)
    ) * first_moment_j
    productive_survival = (a - b) ** 2 * x / (
        (cap_b * x + cap_a) * (a - b * x)
    )
    survival_integral = float(
        np.sum(_WEIGHTS * productive_survival / (theta * x))
    )
    release_integral = float(
        np.sum(_WEIGHTS * regime.delta * second_moment_k / (theta * x))
    )
    return survival_integral, release_integral


def run_asserts() -> list[dict[str, float]]:
    checked: list[dict[str, float]] = []
    expected_relations = (1, 0, -1)
    t_check = np.linspace(0.0, 20.0, 12_000)
    for regime, sign in zip(REGIMES, expected_relations):
        a, b, flooding_parameter, v_inf, productive_lifetime = regime.derived
        assert b < 1.0 < a
        assert abs(a * b - regime.mu / regime.lam) < 2e-13
        assert abs((a - 1.0) * (1.0 - b) - regime.delta / regime.lam) < 2e-13
        if sign > 0:
            assert flooding_parameter > 1.0
        elif sign < 0:
            assert flooding_parameter < 1.0
        else:
            assert abs(flooding_parameter - 1.0) < 2e-13

        survival_integral, release_integral = kernel_integrals(regime)
        assert abs(survival_integral - productive_lifetime) < 2e-10
        assert abs(release_integral - v_inf) < 2e-9

        survival, release = kernels(t_check, regime)
        assert abs(survival[0] - 1.0) < 2e-13
        assert abs(release[0] - regime.delta) < 2e-12
        assert np.all(survival >= 0.0)
        assert np.all(release >= 0.0)
        assert np.all(np.diff(survival) < 0.0)
        assert survival[-1] < 2e-4
        assert release[-1] < 6e-4
        checked.append(
            {
                "L": flooding_parameter,
                "V_inf": v_inf,
                "T_prod": productive_lifetime,
                "int_survival": survival_integral,
                "int_release": release_integral,
            }
        )
    return checked


def add_integral_note(
    ax: plt.Axes,
    value: float,
    label: str,
    colour: str,
    y: float = 0.92,
) -> None:
    ax.text(
        0.96,
        y,
        label + rf" $={value:.2f}$",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9.5,
        color=colour,
        bbox=dict(boxstyle="round,pad=0.18", facecolor="white", edgecolor="none", alpha=0.84),
    )


def make_figure(checked: list[dict[str, float]]) -> None:
    t = np.linspace(0.0, 12.0, 2_500)
    fig, axes = plt.subplots(
        2,
        3,
        figsize=(8.4, 5.45),
        sharex=True,
        gridspec_kw={"height_ratios": (1.0, 1.05)},
    )

    top_letters = ("a", "b", "c")
    bottom_letters = ("d", "e", "f")
    for column, (regime, values) in enumerate(zip(REGIMES, checked)):
        ax_survival = axes[0, column]
        ax_release = axes[1, column]
        survival, release = kernels(t, regime)

        ax_survival.fill_between(
            t,
            0.0,
            survival,
            color=regime.colour,
            alpha=0.12,
            linewidth=0.0,
        )
        ax_survival.plot(
            t,
            survival,
            color=regime.colour,
            linestyle=regime.linestyle,
            linewidth=2.35,
        )
        add_integral_note(
            ax_survival,
            values["T_prod"],
            r"area $=\mathbb{E}[T_{\rm prod}]$",
            regime.colour,
        )
        ax_survival.text(
            0.96,
            0.78,
            regime.parameters,
            transform=ax_survival.transAxes,
            ha="right",
            va="top",
            fontsize=9.0,
            color="#4b4b4b",
        )
        ax_survival.set_ylim(0.0, 1.04)
        ax_survival.set_title(
            rf"({top_letters[column]}) {regime.relation}: {regime.survival_story}",
            loc="left",
            fontweight="bold",
            fontsize=10.4,
            pad=7,
        )

        ax_release.fill_between(
            t,
            0.0,
            release,
            color=regime.colour,
            alpha=0.14,
            linewidth=0.0,
        )
        ax_release.plot(
            t,
            release,
            color=regime.colour,
            linestyle=regime.linestyle,
            linewidth=2.35,
        )
        peak_index = int(np.argmax(release))
        ax_release.scatter(
            [t[peak_index]],
            [release[peak_index]],
            s=30,
            facecolor=regime.colour,
            edgecolor="white",
            linewidth=0.7,
            zorder=5,
        )
        ax_release.annotate(
            rf"peak age $={t[peak_index]:.2f}$",
            xy=(t[peak_index], release[peak_index]),
            xytext=(6, -10 if column == 0 else 7),
            textcoords="offset points",
            ha="left",
            va="top" if column == 0 else "bottom",
            fontsize=9.0,
            color=regime.colour,
        )
        add_integral_note(
            ax_release,
            values["V_inf"],
            r"area $=V_\infty$",
            regime.colour,
        )
        ax_release.set_ylim(0.0, release.max() * 1.17)
        ax_release.set_title(
            rf"({bottom_letters[column]}) {regime.release_story}",
            loc="left",
            fontweight="bold",
            fontsize=10.4,
            pad=7,
        )
        ax_release.set_xlabel(r"cell age $a$")

    axes[0, 0].set_ylabel(r"productive survival $I_{\rm fix}(a)$")
    axes[1, 0].set_ylabel(r"release kernel $g(a)=\delta K(a)$")
    for ax in axes.flat:
        ax.set_xlim(0.0, 12.0)
        ax.set_xticks(np.arange(0.0, 12.1, 2.0))
        ax.tick_params(labelsize=9.5)

    fig.suptitle(
        "The same intracellular kernels change character across the flooding boundary",
        x=0.075,
        y=0.995,
        ha="left",
        fontsize=11.5,
        fontweight="bold",
    )
    fig.tight_layout(w_pad=0.9, h_pad=1.1, rect=(0.0, 0.0, 1.0, 0.955))
    style_rc.save_figure(fig, PDF_PATH, PNG_PATH, dpi=240)
    plt.close(fig)


def main() -> None:
    checked = run_asserts()
    make_figure(checked)
    print("asserts: pass")
    for regime, values in zip(REGIMES, checked):
        print(
            f"{regime.parameters}: L={values['L']:.9f}, "
            f"integral g={values['int_release']:.12f}=V_inf={values['V_inf']:.12f}, "
            f"integral I_fix={values['int_survival']:.12f}="
            f"E[T_prod]={values['T_prod']:.12f}"
        )
    print(f"wrote {PDF_PATH} and {PNG_PATH}")


if __name__ == "__main__":
    main()
