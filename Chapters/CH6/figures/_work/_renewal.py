"""Shared renewal / classical BMVR solver for this chapter's overlay figures.

The five `overlay_*` figures and `peff_dr_curves` had no generation script
anywhere in the tree.  This module is the replacement: one validated
implementation that all of them import, rather than six transcriptions of the
same integration.

The renewal system of the chapter is

    I(t) = I0 Ifix(t) + (i * Ifix)(t),
    V'(t) = I0 g(t) + (i * g)(t) - c V(t),      i(t) = gT V(t).

Solving the V equation with the integrating factor e^{ct} turns it into a
second-kind Volterra equation in V alone,

    V(t) = V0 e^{-ct} + I0 (g * e^{-c.})(t) + (A * V)(t),
    A = gT (g * e^{-c.}),

in which A is exactly the chapter's generation kernel.  Because A(0) = 0 the
trapezoidal step is explicit, so no inner solve is needed.

Validated in `_renewal_check.py` against the chapter's own published values:
V_inf, E[T_prod], R0 = gT V_inf / c, and the late growth rate against the root
of the characteristic equation r + c = gT dK~(r).
"""
from __future__ import annotations

import numpy as np

__all__ = ["Rates", "kernels", "kernels_scaled", "solve_renewal", "solve_classical",
           "char_root", "p_eff", "d_eff", "V_inf", "T_prod", "theta_of"]


class Rates:
    """The intracellular triple and everything the closed forms derive from it."""

    def __init__(self, lam: float, mu: float, delta: float):
        self.lam, self.mu, self.delta = float(lam), float(mu), float(delta)
        eta = (self.lam + self.mu + self.delta) / (2.0 * self.lam)
        root = np.sqrt(eta ** 2 - self.mu / self.lam)
        self.a = eta + root
        self.b = eta - root
        self.A = self.a - 1.0
        self.B = 1.0 - self.b
        self.theta = self.lam * (self.a - self.b)
        self.kappa = 1.0 + self.delta / (2.0 * self.lam)

    def __repr__(self) -> str:
        return f"Rates({self.lam:g}, {self.mu:g}, {self.delta:g})"

    @property
    def label(self) -> str:
        d = self.delta
        ds = "1/3" if abs(d - 1 / 3) < 1e-12 else f"{d:g}"
        return rf"$({self.lam:g},\,{self.mu:g},\,{ds})$"


def theta_of(R: Rates) -> float:
    return R.theta


def kernels(R: Rates, t):
    """Survival Ifix and release g = delta*K at ages t, in a stable form.

    Written in v = e^{-theta t} rather than w = e^{+theta t}: the w form
    overflows for theta*t beyond ~700 and silently returns NaN.
    """
    t = np.asarray(t, dtype=float)
    v = np.exp(-R.theta * t)
    a, b, A, B = R.a, R.b, R.A, R.B
    I = (a * B * v + b * A) / (B * v + A)
    Ifix = (a - b) ** 2 * v / ((B * v + A) * (a - b * v))
    J = (a - b) ** 2 * v / (B * v + A) ** 2
    g = 2.0 * R.lam * (R.kappa - I) * J          # = delta * K
    return Ifix, g


def kernels_scaled(R: Rates, t):
    """Ifix and g with the leading e^{-theta t} divided out.

    Both kernels behave like  const * e^{-theta t}  at large age.  For r < 0
    the Laplace integrand e^{-r t} f(t) is perfectly finite, but forming it as
    a product of e^{-r t} (which overflows) and f(t) (which underflows) gives
    inf * 0 = NaN.  Returning the bounded factors lets the caller combine them
    as e^{-(r + theta) t} * bounded, which never overflows for r > -theta.
    """
    t = np.asarray(t, dtype=float)
    v = np.exp(-R.theta * t)
    a, b, A, B = R.a, R.b, R.A, R.B
    I = (a * B * v + b * A) / (B * v + A)
    Ifix_hat = (a - b) ** 2 / ((B * v + A) * (a - b * v))
    J_hat = (a - b) ** 2 / (B * v + A) ** 2
    g_hat = 2.0 * R.lam * (R.kappa - I) * J_hat
    return Ifix_hat, g_hat


def V_inf(R: Rates) -> float:
    return R.a * R.B / R.A


def T_prod(R: Rates) -> float:
    return np.log(R.a / (R.a - 1.0)) / R.lam


def _trapz_conv(f, h, y):
    """(f * y)(t_n) on a uniform grid, trapezoidal, for n = 0..N-1."""
    n = len(y)
    out = np.empty(n)
    out[0] = 0.0
    for k in range(1, n):
        seg = f[: k + 1] * y[k::-1]
        out[k] = h * (seg.sum() - 0.5 * (seg[0] + seg[-1]))
    return out


def solve_renewal(R: Rates, gT: float, c: float, t_max: float,
                  I0: float = 1.0, V0: float = 0.0, n: int = 4001):
    """Integrate the renewal system; return (t, I, V)."""
    t = np.linspace(0.0, t_max, n)
    h = t[1] - t[0]
    Ifix, g = kernels(R, t)
    decay = np.exp(-c * t)

    # GE = (g * e^{-c.}) and the generation kernel A = gT * GE
    GE = _trapz_conv(g, h, decay)
    A = gT * GE

    V = np.zeros(n)
    V[0] = V0
    for k in range(1, n):
        # (A * V)(t_k), trapezoidal; A[0] = 0 so the V[k] term drops out
        seg = A[: k + 1] * V[k::-1]
        conv = h * (seg.sum() - 0.5 * (seg[0] + seg[-1]))
        V[k] = V0 * decay[k] + I0 * GE[k] + conv

    I = I0 * Ifix + gT * _trapz_conv(Ifix, h, V)
    return t, I, V


def solve_classical(p: float, d: float, gT: float, c: float, t_max: float,
                    I0: float = 1.0, V0: float = 0.0, n: int = 4001):
    """Classical BMVR  I' = gT V - d I,  V' = p I - c V,  by RK4."""
    t = np.linspace(0.0, t_max, n)
    h = t[1] - t[0]
    I = np.empty(n); V = np.empty(n)
    I[0], V[0] = I0, V0

    def f(y):
        return np.array([gT * y[1] - d * y[0], p * y[0] - c * y[1]])

    y = np.array([I0, V0], dtype=float)
    for k in range(1, n):
        k1 = f(y); k2 = f(y + 0.5 * h * k1)
        k3 = f(y + 0.5 * h * k2); k4 = f(y + h * k3)
        y = y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        I[k], V[k] = y
    return t, I, V


# --- transforms and the effective-parameter map ----------------------------

def _laplace(R: Rates, r: float, which: str, span: float = 60.0,
             n: int = 200001) -> float:
    """int_0^inf e^{-r a} f(a) da by Simpson, on a grid adapted to r.

    Both kernels decay like e^{-theta a}, so the integrand decays like
    e^{-(theta + r) a} and the integration span has to follow r: a span fixed
    at 60/theta silently under-resolves the decay once r is large, and a span
    that ignores r wastes points once r is close to -theta.
    """
    rate = R.theta + r
    if rate <= 0.0:
        raise ValueError(f"r={r} is outside the domain of convergence r > -theta")
    T = min(span / rate, 4.0e4 / R.theta)
    t = np.linspace(0.0, T, n)
    h = t[1] - t[0]
    Ifix_hat, g_hat = kernels_scaled(R, t)
    # e^{-r t} f(t) = e^{-(r + theta) t} * f_hat(t): finite for every r > -theta
    y = np.exp(-rate * t) * (Ifix_hat if which == "S" else g_hat)
    w = np.ones(n); w[1:-1:2] = 4.0; w[2:-1:2] = 2.0
    return h / 3.0 * float(np.sum(w * y))


def p_eff(R: Rates, r: float) -> float:
    """delta*K~(r) / Ifix~(r).  Defined for r > -theta."""
    return _laplace(R, r, "g") / _laplace(R, r, "S")


def d_eff(R: Rates, r: float) -> float:
    return 1.0 / _laplace(R, r, "S") - r


def p_eff_old_cell(R: Rates) -> float:
    """The r -> -theta endpoint: delta * E_QS[X^2] = delta a(a+1)/(a-1)^2.

    Derived from AB = delta/lambda; see the chapter's old-cell limit.  This is
    the third endpoint of the map, opposite the young-cell value delta.
    """
    return R.delta * R.a * (R.a + 1.0) / (R.a - 1.0) ** 2


def char_root(R: Rates, gT: float, c: float) -> float:
    """r solving r + c = gT * delta*K~(r)."""
    f = lambda r: gT * _laplace(R, r, "g") - (r + c)
    lo, hi = -0.999 * R.theta, 50.0
    flo = f(lo)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if flo * f(mid) <= 0: hi = mid
        else: lo = mid
    return 0.5 * (lo + hi)
