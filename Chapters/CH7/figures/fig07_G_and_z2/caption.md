**Figure 7 | The exact type-2 probability in its moving coordinate.** (a) Starting from $G(0)=1$, the exact closed form (solid vermillion) decreases monotonically towards the admissible equilibrium $r_{2,-}=0.354361$ (dashed grey). Open markers are an independent RK4 solution of the unscaled physical-time equation

$$
\frac{\mathrm dG}{\mathrm dt}
=\lambda_2G^2-(\lambda_2+\mu_2+\delta_2)G+\mu_2.
$$

(b) On the same physical-time interval, the separated coordinate $z_2(\lambda_1t)=z_{2,0}\exp(\hat q_2\lambda_1t)$ starts at $z_{2,0}=-1.968459$ and remains negative while increasing monotonically towards zero. Here $\hat q_2=-0.827587<0$. (c) Eliminating time exposes the linear-fractional relation

$$
G=r_{2,-}-\alpha_2\frac{z_2}{1-z_2},
$$

which motivates using $z_2$ as the independent variable for the driven type-1 equation. Markers indicate selected physical times; the arrow gives the direction of increasing time towards $(0,r_{2,-})$.

Parameters: $\lambda_1=1.00$, $\lambda_2=0.85$, $\mu_2=0.40$ and $\delta_2=0.18$. The horizontal axes in panels (a) and (b) show physical time $t$. Internally the paper's scaled rates are used with $\hat t=\lambda_1t$, and the plotted solution is $G(t)=\widehat G(\lambda_1t)$. Derived constants are $r_{2,+}=1.327992$, $\alpha_2=0.973632$, $\hat\Delta_2=0.827587$ and $\hat q_2=-\hat\Delta_2$.

**Method note.** The closed form is evaluated directly from the paper's formulas. Open markers in panel (a) come from fixed-step classical RK4 integration of the unscaled ODE with step $10^{-3}$. The maximum absolute discrepancy on the complete RK4 grid over $0\leq t\leq15$ is $2.44\times10^{-15}$. No random seed or AI-generated content is used.
