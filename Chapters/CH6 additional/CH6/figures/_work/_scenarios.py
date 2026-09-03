"""The six overlay scenarios, shared by the four `overlay_*` figures.

Reconstructed in Phase C from the parameter strings printed inside the
originals, whose generation scripts are absent from the tree.  Each triple and
coupling reproduces the R0 the original figure printed:

    (a) 0.04 * 11 / 0.25      = 1.76     as printed
    (b) 0.03 * 13.9857 / 0.2  = 2.0979   printed 2.10
    (d) 0.01 * 11 / 0.4       = 0.275    printed 0.27
    (e) 0.4  * 1.31623 / 0.2  = 2.6325   printed 2.63
    (f) 0.05 * 11 / 0.2       = 2.75     as printed

`_renewal_check.py` tests all of these.  Scenario (c), "fast burst", carried no
R0 in the extractable text of the original; its coupling is chosen here to sit
in the same supercritical range as (a) and (b).

The classical comparator is always matched at the r = 0 end of the
effective-parameter map, p = V_inf / E[T_prod] and d = 1 / E[T_prod], which is
the fairest constant pair available and the one the chapter's overlays use.
"""
from __future__ import annotations

import _renewal as RN


class Scenario:
    def __init__(self, tag, title, rates, gT, c, t_max, I0=1.0, V0=0.0, logV=True):
        self.tag, self.title = tag, title
        self.rates = RN.Rates(*rates)
        self.triple = rates
        self.gT, self.c, self.t_max = gT, c, t_max
        self.I0, self.V0 = I0, V0
        self.logV = logV

    @property
    def R0(self):
        return self.gT * RN.V_inf(self.rates) / self.c

    @property
    def matched(self):
        """(p, d) at the r = 0 end of the map."""
        T = RN.T_prod(self.rates)
        return RN.V_inf(self.rates) / T, 1.0 / T

    def solve(self, n=4001):
        t, I, V = RN.solve_renewal(self.rates, self.gT, self.c, self.t_max,
                                   I0=self.I0, V0=self.V0, n=n)
        p, d = self.matched
        tc, Ic, Vc = RN.solve_classical(p, d, self.gT, self.c, self.t_max,
                                        I0=self.I0, V0=self.V0, n=n)
        return t, (I, V), (Ic, Vc)

    @property
    def caption_line(self):
        l, m, dd = self.triple
        return (rf"$({l:g},{m:g},{dd:g})$, $\gamma T={self.gT:g}$, "
                rf"$c={self.c:g}$, $R_0={self.R0:.2f}$")


SCENARIOS = [
    Scenario("a", r"supercritical, $\mu=0$",        (1.0, 0.0, 0.1),  0.04, 0.25, 40.0),
    Scenario("b", r"supercritical, $\mu>0$",        (1.0, 0.2, 0.05), 0.03, 0.20, 40.0),
    Scenario("c", r"fast burst",                    (1.0, 0.0, 0.5),  0.15, 0.25, 30.0),
    Scenario("d", r"subcritical, $R_0<1$",          (1.0, 0.0, 0.1),  0.01, 0.40, 40.0,
             logV=False),
    Scenario("e", r"high intracellular death",      (1.0, 0.9, 0.1),  0.40, 0.20, 40.0),
    Scenario("f", r"free-particle seed only",       (1.0, 0.0, 0.1),  0.05, 0.20, 30.0,
             I0=0.0, V0=1.0),
]

BY_TAG = {s.tag: s for s in SCENARIOS}
