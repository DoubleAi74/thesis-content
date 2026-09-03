#!/usr/bin/env python3
"""Extra Chapter M figures: gambler's-ruin hitting probabilities and Poisson paths."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
OUT = Path(__file__).resolve().parents[1] / "figures" / "tikz_gen"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 12,
        "legend.fontsize": 9.5,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.dpi": 160,
        "savefig.dpi": 200,
        "savefig.bbox": "tight",
        "mathtext.fontset": "cm",
    }
)

BLUE = "#1f77b4"
ORANGE = "#ff7f0e"
GREEN = "#2ca02c"
RED = "#d62728"
PURPLE = "#9467bd"
GRAY = "#787878"


def hitting_prob(i, N, p):
    """Probability of hitting N before 0 starting from i (gambler's ruin).

    Symmetric case p = 1/2: h_i = i/N.
    Biased case p ≠ q: h_i = (r^i - 1)/(r^N - 1) with r = q/p, q = 1-p.
    """
    i = np.asarray(i, dtype=float)
    q = 1.0 - p
    if np.isclose(p, 0.5):
        return i / N
    r = q / p
    return (r**i - 1.0) / (r**N - 1.0)


def plot_ruin_hitting():
    """Hitting probabilities for gambler's ruin: symmetric vs biased."""
    N = 10
    states = np.arange(0, N + 1)
    x_cont = np.linspace(0, N, 300)

    fig, ax = plt.subplots(figsize=(5.6, 3.55))

    # Continuous guide curves
    ax.plot(
        x_cont,
        hitting_prob(x_cont, N, 0.5),
        color=BLUE,
        lw=2.0,
        label=r"symmetric $p=1/2$: $h_i=i/N$",
        zorder=2,
    )
    ax.plot(
        x_cont,
        hitting_prob(x_cont, N, 0.6),
        color=GREEN,
        lw=2.0,
        label=r"biased $p=0.6$: $h_i=(r^i-1)/(r^N-1)$",
        zorder=2,
    )
    ax.plot(
        x_cont,
        hitting_prob(x_cont, N, 0.4),
        color=ORANGE,
        lw=2.0,
        label=r"biased $p=0.4$",
        zorder=2,
    )

    # Integer-state markers
    ax.plot(
        states,
        hitting_prob(states, N, 0.5),
        "o",
        color=BLUE,
        ms=6,
        zorder=3,
        markeredgecolor="white",
        markeredgewidth=0.6,
    )
    ax.plot(
        states,
        hitting_prob(states, N, 0.6),
        "s",
        color=GREEN,
        ms=5.5,
        zorder=3,
        markeredgecolor="white",
        markeredgewidth=0.6,
    )
    ax.plot(
        states,
        hitting_prob(states, N, 0.4),
        "D",
        color=ORANGE,
        ms=5,
        zorder=3,
        markeredgecolor="white",
        markeredgewidth=0.6,
    )

    # Absorbing-boundary markers
    ax.axvline(0, color=RED, lw=1.0, ls=":", alpha=0.55)
    ax.axvline(N, color=GREEN, lw=1.0, ls=":", alpha=0.45)
    ax.annotate(
        "ruin",
        xy=(0, 0),
        xytext=(0.55, 0.18),
        fontsize=9,
        color=RED,
        arrowprops=dict(arrowstyle="->", color=RED, lw=0.9),
    )
    ax.annotate(
        "goal",
        xy=(N, 1),
        xytext=(N - 2.1, 0.82),
        fontsize=9,
        color=GREEN,
        arrowprops=dict(arrowstyle="->", color=GREEN, lw=0.9),
    )

    ax.set_xlabel(r"state $i$")
    ax.set_ylabel(r"hitting probability $h_i=\mathbb{P}_i(\tau_N<\tau_0)$")
    ax.set_xlim(-0.4, N + 0.4)
    ax.set_ylim(-0.03, 1.08)
    ax.set_xticks(states)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.legend(frameon=False, loc="upper left", fontsize=8.8)
    ax.set_title(rf"Gambler's ruin on $\{{0,\ldots,N\}}$ with $N={N}$")
    # Note r = q/p under the legend area via text
    ax.text(
        0.98,
        0.08,
        r"$r=q/p$, $q=1-p$",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=8.5,
        color=GRAY,
    )

    fig.tight_layout()
    fig.savefig(OUT / "ruin_hitting.pdf")
    fig.savefig(OUT / "ruin_hitting.png")
    plt.close(fig)
    print(f"Wrote {OUT / 'ruin_hitting.pdf'}")


def plot_poisson_paths():
    """Poisson process: sample counting path + interarrival density."""
    rng = np.random.default_rng(7)
    theta = 1.5
    T = 8.0

    # Generate interarrival times until past T
    interarrivals = []
    t_acc = 0.0
    while t_acc < T + 2.0:
        dt = rng.exponential(1.0 / theta)
        interarrivals.append(dt)
        t_acc += dt
    interarrivals = np.array(interarrivals)
    event_times = np.cumsum(interarrivals)
    event_times = event_times[event_times <= T]
    n_events = len(event_times)

    # Step-function path points for stairs
    t_step = np.concatenate([[0.0], event_times, [T]])
    n_step = np.concatenate([[0], np.arange(1, n_events + 1), [n_events]])

    fig, axes = plt.subplots(1, 2, figsize=(8.9, 3.45))

    # --- Left: counting path ---
    ax = axes[0]
    ax.step(
        t_step,
        n_step,
        where="post",
        color=BLUE,
        lw=2.0,
        label=r"$N_t$",
    )
    # Event markers on the path
    if n_events:
        ax.plot(
            event_times,
            np.arange(1, n_events + 1),
            "o",
            color=BLUE,
            ms=5,
            zorder=3,
            markeredgecolor="white",
            markeredgewidth=0.5,
        )
    # Mean line E[N_t] = θt
    t_line = np.linspace(0, T, 200)
    ax.plot(
        t_line,
        theta * t_line,
        color=ORANGE,
        lw=1.4,
        ls="--",
        label=r"$\mathbb{E}[N_t]=\theta t$",
        zorder=1,
    )
    ax.set_xlabel("$t$")
    ax.set_ylabel(r"$N_t$ (event count)")
    ax.set_xlim(0, T)
    ax.set_ylim(0, max(n_events + 1.5, theta * T * 1.15))
    ax.set_title(rf"Sample path ($\theta={theta:g}$)")
    ax.legend(frameon=False, loc="upper left", fontsize=9)

    # --- Right: interarrival density + realised marks ---
    ax = axes[1]
    # Density of Exp(θ)
    s = np.linspace(0, 4.5, 300)
    density = theta * np.exp(-theta * s)
    ax.fill_between(s, density, color=BLUE, alpha=0.18, zorder=1)
    ax.plot(
        s,
        density,
        color=BLUE,
        lw=2.0,
        label=rf"$\mathrm{{Exp}}(\theta)$ density, $\theta={theta:g}$",
        zorder=2,
    )
    # Realised interarrivals used in the path (within T)
    used = interarrivals[:n_events] if n_events else np.array([])
    if len(used):
        # Rug / stem marks for realised waits
        ymax = float(density.max())
        for k, w in enumerate(used):
            ax.plot([w, w], [0, 0.12 * ymax], color=ORANGE, lw=1.4, alpha=0.85, zorder=3)
        ax.plot(
            used,
            np.full_like(used, 0.06 * ymax),
            "|",
            color=ORANGE,
            ms=10,
            mew=1.6,
            label="realised interarrivals",
            zorder=4,
        )
        # Mean mark
        ax.axvline(
            1.0 / theta,
            color=GREEN,
            lw=1.3,
            ls="--",
            label=r"mean $1/\theta$",
            zorder=2,
        )

    ax.set_xlabel(r"interarrival time $s$")
    ax.set_ylabel(r"density $f(s)=\theta e^{-\theta s}$")
    ax.set_xlim(0, 4.5)
    ax.set_ylim(0, theta * 1.15)
    ax.set_title("Interarrival law")
    ax.legend(frameon=False, loc="upper right", fontsize=8.5)

    # Small annotation of N_T
    axes[0].text(
        0.98,
        0.05,
        rf"$N_T={n_events}$",
        transform=axes[0].transAxes,
        ha="right",
        va="bottom",
        fontsize=9,
        color=GRAY,
    )

    fig.tight_layout()
    fig.savefig(OUT / "poisson_path.pdf")
    fig.savefig(OUT / "poisson_path.png")
    plt.close(fig)
    print(f"Wrote {OUT / 'poisson_path.pdf'}")


def main():
    plot_ruin_hitting()
    plot_poisson_paths()
    print(f"All extra figures written to {OUT}")


if __name__ == "__main__":
    main()
