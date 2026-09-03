#!/usr/bin/env python3
"""Reproduce finite and truncated coefficient calculations from Appendix C."""

from __future__ import annotations

import math


def convolve(a: list[float], b: list[float], degree: int) -> list[float]:
    out = [0.0] * (degree + 1)
    for i, ai in enumerate(a):
        if ai == 0.0:
            continue
        for j, bj in enumerate(b[: degree + 1 - i]):
            out[i + j] += ai * bj
    return out


def polynomial_power(base: list[float], power: int, degree: int) -> list[float]:
    out = [1.0] + [0.0] * degree
    for _ in range(power):
        out = convolve(out, base, degree)
    return out


def simpson_integrals(
    alpha: float, beta: float, mu: float, t: float, degree: int, panels: int = 4000
) -> list[float]:
    """Coefficients of h(x,t) from the transfer-time convolution."""
    if panels % 2:
        panels += 1
    step = t / panels
    accum = [0.0] * (degree + 1)
    d = mu - beta
    if d <= 0:
        raise ValueError("this coefficient check uses a subcritical interior process")

    for panel in range(panels + 1):
        v = panel * step
        weight = 1 if panel in (0, panels) else (4 if panel % 2 else 2)
        q = math.exp(-d * v)
        den = mu - beta * q
        probabilities = [0.0] * (degree + 1)
        probabilities[0] = mu * (1.0 - q) / den
        if degree:
            first = d * d * q / (den * den)
            ratio = beta * (1.0 - q) / den
            probabilities[1] = first
            for k in range(2, degree + 1):
                probabilities[k] = probabilities[k - 1] * ratio
        scale = weight * math.exp(alpha * v)
        for k, value in enumerate(probabilities):
            accum[k] += scale * value

    prefactor = alpha * math.exp(-alpha * t) * step / 3.0
    return [prefactor * value for value in accum]


def check_trinomial() -> None:
    alpha, mu, t, n = 0.7, 1.1, 0.8, 5
    g = math.exp(-alpha * t)
    f = alpha * (math.exp(-alpha * t) - math.exp(-mu * t)) / (mu - alpha)
    c = 1.0 - f - g
    total = 0.0
    for i in range(n + 1):
        for j in range(n + 1 - i):
            coefficient = (
                math.factorial(n)
                / (math.factorial(i) * math.factorial(j) * math.factorial(n - i - j))
                * f**i
                * g**j
                * c ** (n - i - j)
            )
            total += coefficient
    assert abs(total - 1.0) < 2e-14


def check_abd_coefficients() -> None:
    alpha, beta, mu, t, n = 0.8, 0.6, 1.0, 0.9, 4
    degree = 160
    h = simpson_integrals(alpha, beta, mu, t, degree)
    exterior = math.exp(-alpha * t)
    assert abs(sum(h) - (1.0 - exterior)) < 2e-11

    total = 0.0
    target = None
    for j in range(n + 1):
        coeffs = polynomial_power(h, n - j, degree)
        factor = math.comb(n, j) * exterior**j
        total += factor * sum(coeffs)
        if j == 1:
            target = factor * coeffs[3]
    assert target is not None
    assert abs(total - 1.0) < 2e-9
    print(f"example p_3,1(t)={target:.12g}")


def main() -> None:
    check_trinomial()
    check_abd_coefficients()
    print("PASS: coefficient extraction and normalisation")


if __name__ == "__main__":
    main()

