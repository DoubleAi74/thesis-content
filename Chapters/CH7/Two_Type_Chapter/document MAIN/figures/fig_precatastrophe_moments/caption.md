# Caption — fig_precatastrophe_moments

Mirror of the live caption in `teaching_precatastrophe.tex`, section 11
(*The parameter plane*). Keep the two in step if either is edited.

---

Expected counts in the instant before catastrophe, from one type-1 founder,
over the plane of catastrophe rates. Top row $\E[X_{\tau_c-}]$, bottom row
$\E[Y_{\tau_c-}]$, both conditional on catastrophe occurring. Columns vary
$\nu$ at the fixed rates $\lambda_1=\lambda_2=1.2$, $\mu_1=\mu_2=0.8$. All six
panels share one logarithmic colour scale, so they can be read across $\nu$ and
between the two types; contours carry the values. Every pixel is the moment
hierarchy integrated to machine precision — no simulation enters the figure.
The domain stops at $\delta_2 = 0.02$ because the edge $\delta_2 = 0$ is
singular.

---

## Notes

- The middle column, $\nu = 0.4 = \lambda-\mu$, sits exactly at type-1
  criticality. By the simplified divergence criterion
  $|\lambda_1-\mu_1-\nu| < \lambda_2-\mu_2$, that makes it the worst case for
  the singular edge: the left-hand side is zero there.
- Contour labels are placed only on levels crossing the panel interior. Levels
  in the extreme tail of a panel's range hug a corner, and their inline labels
  would be clipped by the axes edge.
- Gillespie validation at these rates is in `meta.json` and is reproduced as a
  table in section 11 of the teaching document.
