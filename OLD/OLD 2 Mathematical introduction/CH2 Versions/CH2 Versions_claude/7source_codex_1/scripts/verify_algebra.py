#!/usr/bin/env python3
"""Exact-arithmetic checks for identities used in Chapter 2."""

from __future__ import annotations

from fractions import Fraction as F


def check_second_moment() -> None:
    for m in (F(2, 5), F(3, 5), F(4, 5)):
        sigma2 = m * (2 - m)
        moment = F(1)
        for n in range(1, 10):
            moment = m * m * moment + sigma2 * m ** (n - 1)
            closed = m**n * (1 + 1 / (1 - m)) - m ** (2 * n) / (1 - m)
            assert moment == closed


def check_product_telescope() -> None:
    for p in (F(1, 10), F(1, 4), F(2, 5)):
        r = 2 * p
        survival = F(1)
        product = F(1)
        for n in range(1, 9):
            product *= 1 - survival / 2
            survival = r * survival * (1 - survival / 2)
            assert survival / r**n == product


def check_quadratic_conjugacy() -> None:
    for r in (F(1, 3), F(4, 5), F(2), F(4)):
        c = (2 * r - r * r) / 4
        for x in (F(0), F(1, 7), F(2, 5)):
            z = r * (F(1, 2) - x)
            x_next = r * x * (1 - x)
            z_next = r * (F(1, 2) - x_next)
            assert z_next == z * z + c


def check_characteristic_factorisation() -> None:
    for beta, mu, x in (
        (F(2), F(3), F(1, 5)),
        (F(5), F(2), F(7, 6)),
    ):
        rho = mu / beta
        lhs = mu - (mu + beta) * x + beta * x * x
        rhs = beta * (x - 1) * (x - rho)
        assert lhs == rhs


def rising(a: F, n: int) -> F:
    out = F(1)
    for k in range(n):
        out *= a + k
    return out


def check_pochhammer() -> None:
    for delta in (F(2, 3), F(7, 4), F(-2, 5)):
        for n in range(8):
            assert rising(delta, n) / rising(delta + 1, n) == delta / (delta + n)


def main() -> None:
    check_second_moment()
    check_product_telescope()
    check_quadratic_conjugacy()
    check_characteristic_factorisation()
    check_pochhammer()
    print("PASS: exact algebraic identities")


if __name__ == "__main__":
    main()

