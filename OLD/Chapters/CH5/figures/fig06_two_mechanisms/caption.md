# Figure 5.6 — caption

As typeset in `sections/06_burst_size.tex`, label `dist:fig:two-mechanisms`.
This file is a copy for reference; the chapter is the source of truth.

Two mechanisms, one law. (a) The load conditioned on being neither
ruptured nor extinct, $p_n(t)/\Ifix(t)$, at $t=1,5,20$ from
\cref{dist:eq:stateprob,dist:eq:idihat}, with the quasi-stationary law
$(a-1)a^{-n}$ dashed; on the logarithmic scale each transient law is a
straight line whose slope rotates onto the limiting slope as $P(t)$ slides up
to $1/a$. (b) The burst-size law $(\delta/\lambda)a^{-k}$ of
\cref{dist:eq:burstlaw} (markers) and the same law conditioned on the burst
occurring (dashed) --- the identical line, reached without taking a limit at
all; the two series differ by the constant factor $1-b=0.812$. The first
panel arrives by conditioning on survival along a single trajectory, the
second by weighting each state by its rupture hazard and integrating across
trajectories. (c) The two routes on one axis, each computed on its own terms:
the conditional law of (a) evaluated at $t=60$, against the occupation
integral of (b) evaluated by numerical quadrature rather than in closed form.
They agree to $10^{-8}$, which is the accuracy of the quadrature grid and not
of the identity --- \cref{dist:thm:identity} makes the two exactly equal.
Parameters $(\lambda,\mu,\delta)=(1,0.2,0.05)$, so $a=1.0616$ and
$b=0.1884$; closed forms throughout except where panel (c) integrates
numerically, and no simulation anywhere.
