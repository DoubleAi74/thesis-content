#!/usr/bin/env python3
"""R5 --- replication ratio under fixed removal. Writes ratio_removal.pdf.

Three panels, budgets 0, 1, 2. The first is the zero-removal case, where
R(0) = V_inf exactly, so the solid curve lies on the dashed reference: that
coincidence is the content of corollary "why removal creates a threshold at
all", and it is why this panel carries no crossing marker.
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_style"))
import style_rc  # noqa: E402

style_rc.apply()
import matplotlib.pyplot as plt  # noqa: E402

LAM, MU = 0.8, 0.0
THETAS = (0, 1, 2)


def roots(lam, mu, delta):
    eta = (lam + mu + delta) / (2.0 * lam)
    disc = np.sqrt(eta ** 2 - mu / lam)
    return eta + disc, eta - disc


def v_infty(lam, mu, delta):
    a, b = roots(lam, mu, delta)
    return a * (1.0 - b) / (a - 1.0)


def ratio(lam, mu, delta, theta):
    a, _ = roots(lam, mu, delta)
    return v_infty(lam, mu, delta) * a ** (-float(theta))


def crossing(lam, mu, theta, lo=1e-4, hi=50.0, tol=1e-13):
    f = lambda d: ratio(lam, mu, d, theta) - 1.0
    if f(lo) < 0 or f(hi) > 0:
        return float("nan")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


if __name__ == "__main__":
    delta = np.linspace(0.1, 2.5, 601)
    fig, axes = plt.subplots(1, 3, figsize=(7.6, 2.9), sharey=True)
    for ax, th, lab in zip(axes, THETAS, ("a", "b", "c")):
        ax.plot(delta, v_infty(LAM, MU, delta), color=style_rc.SOFT, lw=1.1,
                ls=(0, (4, 2)), label=r"$V_\infty=\mathcal{R}(0)$")
        ax.plot(delta, ratio(LAM, MU, delta, th), color=style_rc.BLUE, lw=1.5,
                label=r"$\mathcal{R}(\vartheta)$")
        ax.axhline(1.0, color=style_rc.SOFT, lw=0.7, ls=(0, (2, 2)))
        dstar = crossing(LAM, MU, th)
        if np.isfinite(dstar):
            ax.plot([dstar], [1.0], "o", ms=3.6, color=style_rc.CATA, zorder=5)
            ax.annotate(rf"$\delta={dstar:.3f}$", xy=(dstar, 1.0),
                        xytext=(dstar + 0.30, 2.9), fontsize=8,
                        color=style_rc.CATA,
                        arrowprops=dict(arrowstyle="-", lw=0.6,
                                        color=style_rc.CATA))
        else:
            ax.text(2.4, 0.5, r"$\mathcal{R}>1$ throughout", ha="right",
                    va="center", fontsize=8, color=style_rc.SOFT)
        ax.set_xlim(0, 2.5)
        ax.set_ylim(0, 10)
        ax.set_xlabel(r"catastrophe rate $\delta$")
        ax.set_title(rf"$({lab})$  $\vartheta={th}$", loc="left", fontsize=9.5)
    axes[0].set_ylabel("expected surviving release")
    axes[0].legend(loc="upper right", fontsize=8)
    fig.savefig("ratio_removal.pdf")
    plt.close(fig)
    print("wrote ratio_removal.pdf")
    for th in THETAS:
        d = crossing(LAM, MU, th)
        r = ratio(LAM, MU, d, th) if np.isfinite(d) else float("nan")
        print(f"  vartheta={th}: crossing delta = {d:.9f}, R = {r:.12f}")
    print(f"  closed-form checks at mu=0: vartheta=1 -> delta=lam={LAM}; "
          f"vartheta=2 -> delta=lam*(sqrt(5)-1)/2="
          f"{LAM * (5 ** 0.5 - 1) / 2:.9f}")
