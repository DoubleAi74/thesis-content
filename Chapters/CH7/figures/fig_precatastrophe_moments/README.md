# fig_precatastrophe_moments

Six-panel figure: expected pre-catastrophe counts $E[X_{\tau_c-}]$ (top row) and
$E[Y_{\tau_c-}]$ (bottom row) over the $(\delta_1,\delta_2)$ plane, at three
conversion rates $\nu$.

Supports section 11 of `teaching_precatastrophe.tex` (*The parameter plane*).
This figure is **not** part of `main.tex`. Every value is computed from the exact moment hierarchy
obtained by differentiating the killed generating-function system at
$(x,y)=(1,1)$; **no simulation enters the figure**.

## Regenerate

From project root:

```bash
python figures/fig_precatastrophe_moments/src/generate_fig_precatastrophe_moments.py
```

Roughly 15 minutes for the default $111\times111$ grid at three $\nu$ values.
Add `--quick` for a coarse $41\times41$ preview, `--no-usetex` if a LaTeX
installation is not on `PATH`.

Requires: `numpy`, `matplotlib`. LaTeX text rendering uses `lmodern` so the
figure typography matches the document.

## Parameters

Birth and death are equal across the two types and fixed throughout, with birth
above death:

$$\lambda_1=\lambda_2=1.2,\qquad \mu_1=\mu_2=0.8,$$

so the only demographic parameter varying between columns is $\nu$. The middle
column $\nu=0.4=\lambda-\mu$ sits exactly at type-1 criticality.

**These rates differ deliberately** from both `fig_bio_regimes` and the worked
example in section 10 of the teaching document, which share
$\lambda_1=1.0$, $\mu_1=0.45$, $\nu=0.35$, $\lambda_2=0.85$, $\mu_2=0.40$.
The two parameter sets are not one family and should not be read across.

See `meta.json` for the full parameter record.

## Domain

- $\delta_1=0$ is **regular** and is retained: catastrophe remains reachable
  through the type-2 channel.
- $\delta_2=0$ is **singular** and is excluded. There $G\equiv1$, so
  $\theta_2=\lambda_2-\mu_2>0$ and $\E[Y_{\tau_c-}]$ diverges whenever
  $\theta_1(\infty)+\lambda_2-\mu_2>0$. The grid therefore starts at
  $\delta_2=0.02$. Thresholds in $\delta_1$ below which that edge diverges:
  $0.0166$ at $\nu=0.1$, $0.0331$ at $\nu=0.4$, and none at $\nu=1.0$.

## Validation

Four independent checks, all recorded in `meta.json`:

1. **Horizon** — fraction of each running integral accumulated in the last 5% of
   $[0,T]$ is $0$ to machine precision.
2. **Step halving** — doubling the RK4 steps changes $\E[X],\E[Y]$ by
   $\lesssim 2\times10^{-12}$.
3. **Flux identity** — $\mathcal J_1(1,1,t)=-S'(t)$ and
   $\mathcal J_2(1,1,t)=-G'(t)$ hold to $1.9\times10^{-13}$. This tests the
   hierarchy against the closed-form probabilities of the main text.
4. **Gillespie** — 12 parameter points, $1.2\times10^5$ exact paths each,
   recording $(X,Y)$ in the instant before catastrophe. All 24 comparisons agree
   within about two standard errors.

## Open observation (not claimed in the paper)

At $\nu=\lambda-\mu$ with $\delta_1=\delta_2=\delta$, the computed
$E[Y_{\tau_c-}]$ equals $(\lambda-\mu)/\delta$ to all printed digits — $4.0000$
at $\delta=0.10$ and $1.6000$ at $\delta=0.25$. It fails at other $\nu$ and when
$\delta_1\neq\delta_2$. This is a numerical observation that has **not** been
derived; it is recorded here and as a remark in the teaching document as a
lead, not a result.
