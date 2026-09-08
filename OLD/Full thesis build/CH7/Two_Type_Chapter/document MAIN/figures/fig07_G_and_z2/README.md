# Figure 7 — $G(t)$ and the moving coordinate $z_2(t)$

This package contains the deterministic three-panel figure for the paper's exact autonomous type-2 solution. It shows the physical-time probability $G(t)$, the exponential coordinate $z_2(\lambda_1t)$, and the rational relation between them.

## Regenerate

From the project root:

```bash
python3 figures/fig07_G_and_z2/src/generate_fig07.py
```

Dependencies: Python 3, NumPy and Matplotlib. The script writes `fig07.png`, `fig07.pdf` and `meta.json` into this folder.

No random seed is used because the figure is deterministic. No AI image generation is used.

## Parameters, scaling and panels

Physical rates are $\lambda_1=1.00$, $\lambda_2=0.85$, $\mu_2=0.40$ and $\delta_2=0.18$. The plotted horizontal axis is physical time $t$. The code first forms the scaled rates of the paper, evaluates the internal closed form at $\hat t=\lambda_1t$, and then reports $G(t)=\widehat G(\lambda_1t)$.

- **(a)** The exact $G(t)$ (solid vermillion) and fixed-step RK4 markers from the independent unscaled ODE, with the asymptote $r_{2,-}$.
- **(b)** The moving coordinate $z_2(\lambda_1t)=z_{2,0}\exp(\hat q_2\lambda_1t)$, which remains negative and approaches zero.
- **(c)** The parametric trajectory in $(z_2,G)$, exposing the rational relation $G=r_{2,-}-\alpha_2z_2/(1-z_2)$ used to change independent variable in Section 4.

Machine-readable parameters, derived constants, software versions and the exact-versus-RK4 error are recorded in `meta.json`.
