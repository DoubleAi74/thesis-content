"""Closed-form survival probabilities for the two-type BDC process.

``BDCClosedForm`` rescales the seven model rates, prepares the elementary or
hypergeometric branch once, and then evaluates S(t) and G(t) in unscaled time.
The compact 2F1 evaluator is repeated here so that this file remains standalone.
"""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from typing import Iterable


# ---------------------------------------------------------------------------
# Gauss 2F1 evaluator (also provided separately in hypergeometric.py)


class HypergeometricError(ArithmeticError):
    """Raised when the series has a pole or does not converge."""


def _series(
    a: complex,
    b: complex,
    c: complex,
    z: complex,
    tol: float,
    max_terms: int,
) -> complex:
    term = total = 1.0 + 0.0j
    for k in range(max_terms):
        if term == 0:
            return total
        denominator = (c + k) * (k + 1)
        if abs(denominator) < 1e-30:
            raise HypergeometricError("the lower parameter c is at a series pole")
        term *= (a + k) * (b + k) * z / denominator
        total += term
        if abs(term) <= tol * max(1.0, abs(total)):
            return total
    raise HypergeometricError(f"2F1 did not converge in {max_terms} terms")


def hyp2f1(
    a: complex | float,
    b: complex | float,
    c: complex | float,
    z: complex | float,
    *,
    tol: float = 1e-15,
    max_terms: int = 5000,
) -> complex:
    """Evaluate 2F1, using a Pfaff transformation whenever it is advantageous."""
    a, b, c, z = complex(a), complex(b), complex(c), complex(z)
    if z == 0:
        return 1.0 + 0.0j
    if tol <= 0 or max_terms < 1:
        raise ValueError("tol and max_terms must be positive")

    w = z / (z - 1)
    negative_real_z = z.real < 0 and abs(z.imag) < 1e-15
    pfaff_is_better = abs(w) < 1 and (negative_real_z or abs(w) < abs(z))
    if pfaff_is_better:
        return (1 - z) ** (-a) * _series(a, c - b, c, w, tol, max_terms)
    if abs(z) < 1:
        return _series(a, b, c, z, tol, max_terms)
    if abs(w) < 1:
        return (1 - z) ** (-a) * _series(a, c - b, c, w, tol, max_terms)
    raise ValueError("z lies outside the supported continuation region")


# ---------------------------------------------------------------------------
# BDC closed forms


class ClosedFormError(ArithmeticError):
    """Raised when a degenerate closed-form representation is unreliable."""


@dataclass(frozen=True)
class Rates:
    """The seven unscaled, per-capita model rates."""

    lambda1: float
    mu1: float
    nu: float
    delta1: float
    lambda2: float
    mu2: float
    delta2: float

    def __post_init__(self) -> None:
        values = vars(self)
        if not all(math.isfinite(value) for value in values.values()):
            raise ValueError("all rates must be finite")
        if self.lambda1 <= 0 or self.lambda2 <= 0:
            raise ValueError("lambda1 and lambda2 must be positive")
        if any(values[name] < 0 for name in ("mu1", "nu", "delta1", "mu2", "delta2")):
            raise ValueError("death, conversion, and catastrophe rates cannot be negative")


def _riccati(t: float, lower: float, upper: float, initial: float = 1.0) -> float:
    """Solve y'=(y-lower)(y-upper) from y(0)=initial."""
    if abs(initial - lower) < 1e-14:
        return lower
    if abs(initial - upper) < 1e-14:
        return upper

    gap = upper - lower
    if abs(gap) < 1e-12:
        offset = initial - lower
        return lower + offset / (1 - offset * t)

    ratio = (initial - lower) / (initial - upper)
    decay = math.exp(-gap * t)
    return (lower - ratio * decay * upper) / (1 - ratio * decay)


class BDCClosedForm:
    """Prepared evaluators for the two survival functions S(t) and G(t)."""

    def __init__(self, rates: Rates) -> None:
        self.rates = rates
        self.notes: list[str] = []
        self.constants: dict[str, float | complex] = {}
        self._prepare()

    @staticmethod
    def _g_constants(L2: float, m2: float, d2: float) -> tuple[float, ...]:
        delta = math.sqrt((L2 + m2 + d2) ** 2 - 4 * L2 * m2)
        r_plus = (L2 + m2 + d2 + delta) / (2 * L2)
        r_minus = (L2 + m2 + d2 - delta) / (2 * L2)
        alpha = r_plus - r_minus
        q = -delta
        z0 = (r_minus - 1) / (r_plus - 1)
        return delta, r_plus, r_minus, alpha, q, z0

    def _prepare(self) -> None:
        r = self.rates
        m1, n, d1 = r.mu1 / r.lambda1, r.nu / r.lambda1, r.delta1 / r.lambda1
        L2, m2, d2_raw = r.lambda2 / r.lambda1, r.mu2 / r.lambda1, r.delta2 / r.lambda1
        kappa = 1 + m1 + n + d1
        self._scaled = (m1, n, d1, L2, m2, d2_raw)

        if d2_raw < 1e-6:
            self.branch = "delta2_zero"
            gap = math.sqrt(max(0.0, kappa * kappa - 4 * (m1 + n)))
            self._s_lower, self._s_upper = (kappa - gap) / 2, (kappa + gap) / 2
            s_inf = 1.0 if d1 < 1e-12 else self._s_lower
            self.constants = {
                "kappa1": kappa,
                "h": s_inf,
                "S_inf": s_inf,
                "G_inf": 1.0,
            }
            self.notes.append("delta2 = 0: G(t) is identically 1")
            return

        delta, r_plus, r_minus, alpha, q, z0 = self._g_constants(L2, m2, d2_raw)

        if n < 1e-12:
            self.branch = "decoupled"
            s_kappa = 1 + m1 + d1
            gap = math.sqrt(max(0.0, s_kappa * s_kappa - 4 * m1))
            self._s_lower, self._s_upper = (s_kappa - gap) / 2, (s_kappa + gap) / 2
            s_inf = 1.0 if d1 < 1e-12 else self._s_lower
            self._set_g(delta, r_plus, r_minus, alpha, q, z0)
            self.constants = {
                "Delta2": delta,
                "r2_plus": r_plus,
                "r2_minus": r_minus,
                "alpha2": alpha,
                "q2": q,
                "z2_0": z0,
                "kappa1": s_kappa,
                "h": s_inf,
                "S_inf": s_inf,
                "G_inf": r_minus,
            }
            self.notes.append("nu = 0: S and G are independent elementary Riccati solutions")
            return

        # The U,V basis degenerates when C is an integer.  As in the visualiser,
        # move d2 by an invisible amount and recompute every dependent constant.
        nudge = 1.25e-6
        for attempt in range(6):
            d2 = d2_raw + attempt * nudge
            delta, r_plus, r_minus, alpha, q, z0 = self._g_constants(L2, m2, d2)
            disc_h = kappa * kappa - 4 * (m1 + n * r_minus)
            if disc_h < -1e-11:
                raise ClosedFormError("the discriminant defining h is negative")
            h = (kappa - math.sqrt(max(0.0, disc_h))) / 2
            C = 1 + (kappa - 2 * h) / q

            if abs(q) < 1e-10 or abs(r_plus - 1) < 1e-12 or abs(C - round(C)) < 1e-6:
                continue

            root = cmath.sqrt((C - 1) ** 2 / 4 - n * alpha / q**2)
            A, B = (C - 1) / 2 + root, (C - 1) / 2 - root
            self._A, self._B, self._C = A, B, C
            self._A2, self._B2, self._C2 = A - C + 1, B - C + 1, 2 - C

            try:
                U0, Up0, V0, Vp0 = self._basis(z0)
                L = (h - 1) / (q * z0)
                a0, b0 = Up0 - L * U0, Vp0 - L * V0
                scale = max(abs(a0), abs(b0))
                if scale < 1e-12:
                    continue

                # These weights satisfy phi'(z0)=L*phi(z0) without dividing by
                # either basis coefficient, so no explicit D/basis swap is needed.
                weight_u, weight_v = b0 / scale, -a0 / scale
                if abs(weight_u * U0 + weight_v * V0) < 1e-12:
                    continue
            except (ArithmeticError, ValueError, OverflowError):
                continue

            self.branch = "hypergeometric"
            self._set_g(delta, r_plus, r_minus, alpha, q, z0)
            self._h, self._weight_u, self._weight_v = h, weight_u, weight_v
            self.constants = {
                "Delta2": delta,
                "r2_plus": r_plus,
                "r2_minus": r_minus,
                "alpha2": alpha,
                "q2": q,
                "z2_0": z0,
                "kappa1": kappa,
                "h": h,
                "C": C,
                "A": A,
                "B": B,
                "S_inf": h,
                "G_inf": r_minus,
                "d2_effective": d2,
            }
            if attempt:
                self.notes.append(f"integer-C guard: scaled d2 increased by {attempt * nudge:g}")
            if abs(A.imag) > 1e-12:
                self.notes.append("A and B are a complex-conjugate pair")
            return

        raise ClosedFormError("no reliable hypergeometric basis was found")

    def _set_g(
        self,
        delta: float,
        r_plus: float,
        r_minus: float,
        alpha: float,
        q: float,
        z0: float,
    ) -> None:
        self._delta2 = delta
        self._r_plus, self._r_minus = r_plus, r_minus
        self._alpha2, self._q2, self._z0 = alpha, q, z0

    def _basis(self, z: float) -> tuple[complex, complex, complex, complex]:
        """Return U, U', V, V' at a negative real z."""
        if not z < 0:
            raise ValueError("the BDC hypergeometric argument must be negative")

        A, B, C = self._A, self._B, self._C
        A2, B2, C2 = self._A2, self._B2, self._C2
        U = hyp2f1(A, B, C, z)
        Up = A * B / C * hyp2f1(A + 1, B + 1, C + 1, z)

        base_v = hyp2f1(A2, B2, C2, z)
        x = -z
        V = x ** (1 - C) * base_v
        Vp = -(1 - C) * x ** (-C) * base_v
        Vp += x ** (1 - C) * A2 * B2 / C2 * hyp2f1(A2 + 1, B2 + 1, C2 + 1, z)
        return U, Up, V, Vp

    @staticmethod
    def _time(t: float) -> float:
        t = float(t)
        if not math.isfinite(t) or t < 0:
            raise ValueError("time must be a finite, non-negative number")
        return t

    def G(self, t: float) -> float:
        """Evaluate G(t), starting from one type-2 individual."""
        t = self._time(t)
        if self.branch == "delta2_zero":
            return 1.0
        z = self._z0 * math.exp(self._q2 * self.rates.lambda1 * t)
        return self._r_minus - self._alpha2 * z / (1 - z)

    def S(self, t: float) -> float:
        """Evaluate S(t), starting from one type-1 individual."""
        t = self._time(t)
        scaled_t = self.rates.lambda1 * t
        if self.branch in {"delta2_zero", "decoupled"}:
            return _riccati(scaled_t, self._s_lower, self._s_upper)

        z = self._z0 * math.exp(self._q2 * scaled_t)
        if abs(z) < 1e-14:
            return self._h
        U, Up, V, Vp = self._basis(z)
        phi = self._weight_u * U + self._weight_v * V
        if abs(phi) < 1e-14:
            raise ClosedFormError("the selected hypergeometric combination vanished")
        phi_prime = self._weight_u * Up + self._weight_v * Vp
        value = self._h - self._q2 * z * phi_prime / phi
        if abs(value.imag) > 1e-8:
            raise ClosedFormError(f"imaginary cancellation failed: |Im S|={abs(value.imag):.3e}")
        return value.real

    def evaluate(self, times: Iterable[float]) -> tuple[list[float], list[float]]:
        """Return ``([S(t)], [G(t)])`` for any iterable of times."""
        time_list = list(times)
        return [self.S(t) for t in time_list], [self.G(t) for t in time_list]


if __name__ == "__main__":
    default = Rates(1.0, 0.5, 0.3, 0.25, 1.2, 0.4, 0.15)
    solution = BDCClosedForm(default)
    for time in (0.0, 1.0, 5.0, 10.0):
        print(f"t={time:>4g}: S={solution.S(time):.9f}, G={solution.G(time):.9f}")
