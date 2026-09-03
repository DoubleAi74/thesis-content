


import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# Reproducibility & plot style
# -------------------------------
np.random.seed(42)

# plt.rcParams.update({
#     'font.family': 'serif',
#     'font.size': 11,
#     'axes.labelsize': 12,
#     'axes.titlesize': 12,
#     'legend.fontsize': 10,
#     'figure.figsize': (14, 4.5),
# })

plt.rcParams.update({
    'font.family': 'serif',

    # Base font size
    'font.size': 14,

    # Axes
    'axes.labelsize': 15,
    'axes.titlesize': 15,

    # Ticks
    'xtick.labelsize': 13,
    'ytick.labelsize': 13,

    # Legend
    'legend.fontsize': 13,

    # Figure
    'figure.figsize': (14, 4.5),
})

# -------------------------------
# Critical GW simulation
# -------------------------------
def simulate_critical_gw(p=0.5, max_generations=10000):
    """
    Binary critical GW:
    each individual produces 2 offspring with prob p=1/2,
    or 0 offspring otherwise.
    
    Returns:
        extinction_time
        total_progeny
    """
    Z = 1
    generation = 0
    total_progeny = 1  # count ancestor

    while Z > 0 and generation < max_generations:
        offspring = np.random.binomial(Z, p)
        Z = 2 * offspring
        total_progeny += Z
        generation += 1

    return generation, total_progeny


# -------------------------------
# Main experiment
# -------------------------------
def main():
    n_sims = 1000000
    print(f"Running {n_sims} simulations...")

    results = np.array([simulate_critical_gw() for _ in range(n_sims)])
    extinction_times = results[:, 0]
    total_progeny = results[:, 1]

    # ==========================================================
    # PANEL A: Survival probability P(T_ext > n)
    # ==========================================================
    max_t = extinction_times.max()
    n_vals = np.arange(1, max_t + 1)
    counts = np.array([np.sum(extinction_times > n) for n in n_vals])
    survival_probs = counts / n_sims

    mask_surv = counts > 5
    n_plot = n_vals[mask_surv]
    surv_plot = survival_probs[mask_surv]

    # ==========================================================
    # PANEL B: Extinction time PMF
    # ==========================================================
    bins_T = np.logspace(0, np.log10(max_t), 40)
    hist_T, edges_T = np.histogram(extinction_times, bins=bins_T)
    centers_T = np.sqrt(edges_T[:-1] * edges_T[1:])
    widths_T = np.diff(edges_T)
    pmf_T = (hist_T / n_sims) / widths_T

    # ==========================================================
    # PANEL C: Total progeny PMF
    # ==========================================================
    max_P = total_progeny.max()
    n_theory_P = np.logspace(0, np.log10(max_P), 200)

    bins_P = np.logspace(0, np.log10(max_P), 40)
    hist_P, edges_P = np.histogram(total_progeny, bins=bins_P)
    centers_P = np.sqrt(edges_P[:-1] * edges_P[1:])
    widths_P = np.diff(edges_P)
    pmf_P = (hist_P / n_sims) / widths_P

    # ==========================================================
    # Plotting
    # ==========================================================
    # fig, axes = plt.subplots(1, 3)
    fig, axes = plt.subplots(1, 3, constrained_layout=True)
    # for ax in axes:
    #     ax.set_aspect('equal', adjustable='box')

    # ---- (a) Survival probability ----
    axes[0].loglog(n_plot[::2], surv_plot[::2], 'o', ms=3, alpha=0.4,
                   label='Simulation')
    n_theory = np.logspace(0, np.log10(n_plot.max()), 200)
    axes[0].loglog(n_theory, 2 / n_theory, '--',
                   label=r'$2/n$')
    axes[0].set_title('(a) Survival probability')
    axes[0].set_xlabel('Generation $n$')
    # axes[0].set_ylabel(r'$P(T_{\rm ext} > n)$')
    axes[0].legend()
    axes[0].grid(True, which='both', alpha=0.2)

    # ---- (b) Extinction time PMF ----
    # mask_T = pmf_T > 0
    mask_T = (pmf_T > 0) & (hist_T > 10)

    axes[1].loglog(centers_T[mask_T], pmf_T[mask_T], 's', alpha=0.6,
                   label='Simulation')
    axes[1].loglog(n_theory, 2 / n_theory**2, '--',
                   label=r'$2/n^2$')
    axes[1].set_title('(b) Extinction time PMF')
    axes[1].set_xlabel(r'$T_{\rm extinct}$')
    # axes[1].set_ylabel('')
    axes[1].legend()
    axes[1].grid(True, which='both', alpha=0.2)

    # ---- (c) Total progeny PMF ----
    mask_P = pmf_P > 0
    axes[2].loglog(centers_P[mask_P], pmf_P[mask_P], 'd', alpha=0.6,
                   label='Simulation')
    # axes[2].loglog(n_theory, n_theory**(-1.5), '--',
    #                label=r'$n^{-3/2}$')
    # axes[2].loglog(n_theory_P, n_theory_P**(-1.5), '--',
    #            label=r'$n^{-3/2}$')
    
    axes[2].loglog(
        n_theory_P,
        (1/np.sqrt(2*np.pi)) * n_theory_P**(-1.5),
        '--',
        label=r'$\frac{1}{\sqrt{2\pi}} n^{-3/2}$'
    )
    

    axes[2].set_title('(c) Total progeny PMF')
    axes[2].set_xlabel(r'Total progeny $\mathcal{T}$')
    # axes[2].set_ylabel('')
    axes[2].legend()
    axes[2].grid(True, which='both', alpha=0.2)

    plt.savefig('power_law_fixed.pdf')
    # plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
