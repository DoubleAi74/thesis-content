#!/usr/bin/env python3
"""
Generate the simulated figures for the mathematical introduction.

Produces, in the directory containing this script:
    random_walk.pdf       -- section 2.1.1, simple random walks
    poisson_process.pdf   -- section 2.2.2, the Poisson process
    coupled_ode_ctmc.pdf  -- section 2.4, coupled ODE-CTMC systems
    birth_death_paths.pdf -- section 2.2.3, birth-death in three regimes
    extinction_and_law.pdf-- sections 3.2.2 and 3.2.5

The schematic figures (transition-rate diagrams, characteristic curves) are
drawn inline with TikZ/pgfplots in the section files and are not produced here.

Run:  python3 make_figures.py
Deps: numpy, matplotlib.  Seeds are fixed, so output is reproducible.
"""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent

# --- House style: match the 11pt serif body text of the chapter ------------
mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif", "Times New Roman"],
    "mathtext.fontset": "dejavuserif",
    "font.size": 9,
    "axes.labelsize": 9,
    "axes.titlesize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "axes.linewidth": 0.7,
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
    "lines.linewidth": 1.1,
    "figure.dpi": 150,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
})

INK = "#1a1a1a"
ACCENT = "#8c1d18"      # muted red, for the highlighted object
COOL = "#1f4e79"        # muted blue
GREY = "#9a9a9a"


def _tidy(ax):
    """Strip the top and right spines; keep the frame light."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(INK)
    ax.spines["bottom"].set_color(INK)


# ---------------------------------------------------------------------------
# Figure 1 -- simple random walks (section 2.1.1)
# ---------------------------------------------------------------------------
def random_walk():
    rng = np.random.default_rng(20260806)

    q = 0.45            # up-probability; drift 2q-1 = -0.1
    n_steps = 300
    n_paths = 7

    steps = np.where(rng.random((n_paths, n_steps)) < q, 1, -1)
    paths = np.concatenate([np.zeros((n_paths, 1)), steps.cumsum(axis=1)], axis=1)
    n = np.arange(n_steps + 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.3, 2.5))

    # (a) sample paths against the drift line and one-sd envelope
    for path in paths:
        ax1.plot(n, path, color=GREY, lw=0.8, alpha=0.85)
    mean = n * (2 * q - 1)
    sd = np.sqrt(4 * n * q * (1 - q))
    ax1.plot(n, mean, color=ACCENT, lw=1.4, zorder=5)
    ax1.plot(n, mean + sd, color=ACCENT, lw=0.9, ls="--", zorder=5)
    ax1.plot(n, mean - sd, color=ACCENT, lw=0.9, ls="--", zorder=5)
    ax1.axhline(0, color=INK, lw=0.6, ls=":")
    ax1.set_xlabel("$n$")
    ax1.set_ylabel("$X_n$")
    ax1.set_xlim(0, n_steps)
    ax1.text(0.04, 0.06, r"$q=0.45$", transform=ax1.transAxes, color=ACCENT)
    ax1.set_title("(a)", loc="left", fontsize=9)
    _tidy(ax1)

    # (b) gambler's ruin: probability of reaching M before 0
    M = 20
    i = np.arange(0, M + 1)
    for theta, style in [(0.7, "-"), (0.85, "-"), (1.0, "-"),
                         (1.2, "-"), (1.5, "-")]:
        if np.isclose(theta, 1.0):
            h = i / M
            colour, lw = ACCENT, 1.4
        else:
            h = (1 - theta ** i) / (1 - theta ** M)
            colour, lw = COOL, 1.0
        ax2.plot(i, h, style, color=colour, lw=lw)

    ax2.annotate(r"$\theta=0.7$", xy=(6, (1 - 0.7 ** 6) / (1 - 0.7 ** M)),
                 xytext=(7.0, 0.80), color=COOL,
                 arrowprops=dict(arrowstyle="-", lw=0.5, color=COOL))
    ax2.annotate(r"$\theta=1$", xy=(13, 13 / M), xytext=(14.0, 0.45),
                 color=ACCENT,
                 arrowprops=dict(arrowstyle="-", lw=0.5, color=ACCENT))
    ax2.annotate(r"$\theta=1.5$", xy=(16, (1 - 1.5 ** 16) / (1 - 1.5 ** M)),
                 xytext=(8.5, 0.12), color=COOL,
                 arrowprops=dict(arrowstyle="-", lw=0.5, color=COOL))

    ax2.set_xlabel("$i$")
    ax2.set_ylabel("$h_i$")
    ax2.set_xlim(0, M)
    ax2.set_ylim(0, 1.02)
    ax2.set_title("(b)", loc="left", fontsize=9)
    _tidy(ax2)

    fig.tight_layout(w_pad=2.0)
    fig.savefig(OUT / "random_walk.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 2 -- the Poisson process (section 2.2.2)
# ---------------------------------------------------------------------------
def poisson_process():
    rng = np.random.default_rng(11)

    alpha = 1.5
    t_max = 8.0

    waits = rng.exponential(1 / alpha, size=40)
    arrivals = np.cumsum(waits)
    arrivals = arrivals[arrivals < t_max]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.3, 2.5))

    # (a) the counting staircase, with holding times marked on the axis
    t_grid = np.concatenate([[0.0], arrivals, [t_max]])
    counts = np.arange(len(t_grid))
    counts[-1] = counts[-2]
    ax1.step(t_grid, counts, where="post", color=COOL, lw=1.2)
    ax1.plot(arrivals, np.arange(1, len(arrivals) + 1), "o", color=COOL,
             ms=2.6, zorder=5)
    ax1.plot([0, t_max], [0, alpha * t_max], color=ACCENT, lw=1.1, ls="--")

    # holding times as alternating bars just below the axis
    y0 = -1.15
    edges = np.concatenate([[0.0], arrivals])
    for k in range(len(edges) - 1):
        ax1.plot([edges[k], edges[k + 1]], [y0, y0], lw=2.2,
                 color=(GREY if k % 2 else INK), solid_capstyle="butt")
    ax1.text(0.15, y0 - 1.15, r"holding times $\sim\mathrm{Exp}(\alpha)$",
             fontsize=7.5, color=INK)

    ax1.set_xlabel("$t$")
    ax1.set_ylabel("$N_t$")
    ax1.set_xlim(0, t_max)
    ax1.set_ylim(y0 - 1.8, alpha * t_max + 2.0)
    ax1.set_yticks([0, 5, 10])
    ax1.text(4.55, 4.4, r"$\mathbb{E}(N_t)=\alpha t$", color=ACCENT, fontsize=8,
             rotation=27, rotation_mode="anchor")
    ax1.set_title("(a)", loc="left", fontsize=9)
    _tidy(ax1)

    # (b) the law at three times: mean equals variance, and both grow with t
    from math import lgamma
    for t, colour, alpha_f in [(1.0, COOL, 0.95), (3.0, ACCENT, 0.8),
                               (6.0, INK, 0.55)]:
        lam = alpha * t
        n = np.arange(0, 22)
        pmf = np.exp(-lam + n * np.log(lam) - np.array([lgamma(k + 1) for k in n]))
        ax2.plot(n, pmf, "o-", color=colour, ms=2.4, lw=0.9, alpha=alpha_f,
                 label=fr"$\alpha t={lam:.1f}$")
    ax2.set_xlabel("$n$")
    ax2.set_ylabel(r"$\mathbb{P}(N_t=n)$")
    ax2.set_xlim(0, 21)
    ax2.set_ylim(0, None)
    ax2.legend(frameon=False, handlelength=1.4, borderpad=0.2)
    ax2.set_title("(b)", loc="left", fontsize=9)
    _tidy(ax2)

    fig.tight_layout(w_pad=2.0)
    fig.savefig(OUT / "poisson_process.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 3 -- a coupled ODE-CTMC system (section 2.4)
# ---------------------------------------------------------------------------
def coupled_ode_ctmc():
    """
    Illustration of the two-way coupling of equation (2.16):

        dy/dt = a(X_t) - b y          (the flow depends on the chain)
        rate 1 -> 2 = kappa * y       (the rates depend on the flow)
        rate 2 -> 1 = nu              (constant)

    A generic system, chosen only to display the mechanism; it is not a model
    used elsewhere in the thesis.
    """
    rng = np.random.default_rng(7)

    a = {1: 2.4, 2: 0.25}     # forcing in each discrete state
    b = 0.55                  # relaxation rate, common to both states
    kappa = 0.10              # 1 -> 2 rate per unit y  (depends on the ODE)
    nu = 0.45                 # 2 -> 1 rate, constant

    dt = 2.0e-4
    t_max = 40.0
    n = int(t_max / dt)

    t = np.linspace(0, t_max, n + 1)
    y = np.empty(n + 1)
    x = np.empty(n + 1, dtype=int)
    y[0], x[0] = 0.2, 1

    for k in range(n):
        rate = kappa * max(y[k], 0.0) if x[k] == 1 else nu
        if rng.random() < rate * dt:
            x[k + 1] = 2 if x[k] == 1 else 1
        else:
            x[k + 1] = x[k]
        y[k + 1] = y[k] + dt * (a[x[k]] - b * y[k])

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(6.3, 2.9), sharex=True,
        gridspec_kw={"height_ratios": [3.0, 1.0], "hspace": 0.12})

    # Plot a decimated copy: the integration is fine-grained, but drawing every
    # step would emit a path with 2e5 vertices and a multi-megabyte PDF.
    keep = max(1, n // 8000)
    tp, yp, xp = t[::keep], y[::keep], x[::keep]

    # switching times, for shading the intervals spent in state 2
    switch = np.flatnonzero(np.diff(x) != 0) + 1
    edges = np.concatenate([[0], switch, [n]])

    # continuous component, shaded by the discrete state
    ax1.plot(tp, yp, color=INK, lw=1.0)
    for lo, hi in zip(edges[:-1], edges[1:]):
        if x[lo] == 2:
            ax1.axvspan(t[lo], t[hi], color=ACCENT, alpha=0.13, lw=0)
    for state, colour in [(1, COOL), (2, ACCENT)]:
        ax1.axhline(a[state] / b, color=colour, lw=0.8, ls="--")
    ax1.text(t_max * 0.995, a[1] / b + 0.30, r"$a_1/b$", color=COOL,
             ha="right", fontsize=8)
    ax1.text(t_max * 0.995, a[2] / b + 0.22, r"$a_2/b$", color=ACCENT,
             ha="right", fontsize=8)
    ax1.set_ylabel("$y(t)$")
    ax1.set_ylim(0, y.max() * 1.28)
    _tidy(ax1)

    # discrete component: draw from the switching times, not the fine grid
    t_steps = np.concatenate([[0.0], t[switch], [t_max]])
    x_steps = np.concatenate([[x[0]], x[switch], [x[-1]]])
    ax2.step(t_steps, x_steps, where="post", color=COOL, lw=1.0)
    ax2.set_yticks([1, 2])
    ax2.set_yticklabels(["$1$", "$2$"])
    ax2.set_ylim(0.7, 2.3)
    ax2.set_xlabel("$t$")
    ax2.set_ylabel("$X_t$")
    ax2.set_xlim(0, t_max)
    _tidy(ax2)

    fig.savefig(OUT / "coupled_ode_ctmc.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 4 -- birth-death realisations in the three regimes (section 2.2.3)
# ---------------------------------------------------------------------------
def _simulate_bd(lam, mu, n0, t_max, rng):
    """One Gillespie trajectory of the linear birth-death process."""
    t, n = 0.0, n0
    ts, ns = [0.0], [n0]
    while 0 < n and t < t_max:
        total = (lam + mu) * n
        t += rng.exponential(1.0 / total)
        if t >= t_max:
            break
        n += 1 if rng.random() < lam / (lam + mu) else -1
        ts.append(t)
        ns.append(n)
    ts.append(min(t, t_max))
    ns.append(n)
    return np.array(ts), np.array(ns)


def birth_death_paths():
    rng = np.random.default_rng(2718)

    mu = 1.0
    n0 = 5
    t_max = 6.0
    regimes = [(0.6, r"subcritical, $\lambda<\mu$"),
               (1.0, r"critical, $\lambda=\mu$"),
               (1.4, r"supercritical, $\lambda>\mu$")]

    fig, axes = plt.subplots(1, 3, figsize=(6.3, 2.35), sharex=True)

    for ax, (lam, title) in zip(axes, regimes):
        extinct = 0
        for _ in range(9):
            ts, ns = _simulate_bd(lam, mu, n0, t_max, rng)
            ax.step(ts, ns, where="post", color=GREY, lw=0.8, alpha=0.9)
            if ns[-1] == 0:
                extinct += 1
                ax.plot(ts[-1], 0, "o", color=INK, ms=2.2, zorder=6)
        tt = np.linspace(0, t_max, 200)
        ax.plot(tt, n0 * np.exp((lam - mu) * tt), color=ACCENT, lw=1.5, zorder=5)
        ax.set_title(title, fontsize=8.5)
        ax.set_xlabel("$t$")
        ax.set_xlim(0, t_max)
        ax.set_ylim(0, 26)
        ax.text(0.05, 0.90, fr"$\lambda={lam}$", transform=ax.transAxes,
                fontsize=8, color=INK)
        _tidy(ax)

    axes[0].set_ylabel("$X_t$")
    for ax in axes[1:]:
        ax.set_yticklabels([])

    fig.tight_layout(w_pad=1.2)
    fig.savefig(OUT / "birth_death_paths.pdf")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 5 -- extinction probability, and why the mean is uninformative
# (sections 3.2.2 and 3.2.5)
# ---------------------------------------------------------------------------
def extinction_and_law():
    mu = 1.0
    t = np.linspace(1e-3, 8.0, 600)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.3, 2.5))

    # (a) extinction probability p_0(t), equation (m:eq:p0t)
    def p0(lam, N):
        if np.isclose(lam, mu):
            return (lam * t / (1 + lam * t)) ** N
        e = np.exp((mu - lam) * t)
        return ((mu - mu * e) / (lam - mu * e)) ** N

    for lam, colour in [(0.6, COOL), (1.0, ACCENT), (1.4, INK)]:
        y1, y5 = p0(lam, 1), p0(lam, 5)
        ax1.plot(t, y1, color=colour, lw=1.2)
        ax1.plot(t, y5, color=colour, lw=1.0, ls="--")
        if lam > mu:                      # the only finite limit below one
            ax1.axhline((mu / lam), color=colour, lw=0.5, ls=":", alpha=0.7)
        # label each curve at its right-hand endpoint, clear of the plot
        ax1.text(8.15, y1[-1], fr"$\lambda={lam:g}$", color=colour,
                 fontsize=7.5, va="center", ha="left")

    ax1.set_xlabel("$t$")
    ax1.set_ylabel("$p_0(t)$")
    ax1.set_xlim(0, 9.6)
    ax1.set_xticks([0, 2, 4, 6, 8])
    ax1.set_ylim(0, 1.03)
    ax1.set_title("(a)", loc="left", fontsize=9)
    _tidy(ax1)

    # (b) the critical law from one founder: mass piles at 0, the tail stretches,
    #     and the mean stays at 1 throughout
    lam = 1.0
    nmax = 30
    n = np.arange(1, nmax + 1)
    for tt, colour, mk in [(1.0, COOL, "o"), (3.0, ACCENT, "s"), (10.0, INK, "^")]:
        lt = lam * tt
        pn = lt ** (n - 1) / (1 + lt) ** (n + 1)
        ax2.plot(n, pn, mk + "-", color=colour, ms=2.2, lw=0.9,
                 label=fr"$t={tt:g}$   $p_0={lt/(1+lt):.2f}$")
    ax2.set_yscale("log")
    ax2.set_ylim(1e-4, 1.0)
    ax2.set_xlim(1, nmax)
    ax2.set_xlabel("$n$")
    ax2.set_ylabel(r"$\mathbb{P}(X_t=n)$")
    ax2.legend(frameon=False, handlelength=1.5, borderpad=0.2, loc="upper right")
    ax2.set_title("(b)", loc="left", fontsize=9)
    _tidy(ax2)

    fig.tight_layout(w_pad=2.0)
    fig.savefig(OUT / "extinction_and_law.pdf")
    plt.close(fig)


if __name__ == "__main__":
    random_walk()
    poisson_process()
    coupled_ode_ctmc()
    birth_death_paths()
    extinction_and_law()
    print(f"wrote 5 figures to {OUT}")
