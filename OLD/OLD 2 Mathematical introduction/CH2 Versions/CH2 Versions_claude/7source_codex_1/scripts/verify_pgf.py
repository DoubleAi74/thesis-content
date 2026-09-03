#!/usr/bin/env python3
"""Compare the transfer--birth--death PGF with a truncated master equation."""

from __future__ import annotations

import math


def interior_pgf(x: float, v: float, beta: float, mu: float) -> float:
    if abs(beta - mu) < 1e-14:
        return 1.0 - (1.0 - x) / (1.0 + beta * v * (1.0 - x))
    b = beta - mu
    rho = mu / beta
    w = (x - 1.0) / (x - rho)
    z = w * math.exp(b * v)
    return (1.0 - rho * z) / (1.0 - z)


def convolution_pgf(
    x: float, y: float, t: float, alpha: float, beta: float, mu: float
) -> float:
    panels = 12000
    step = t / panels
    total = 0.0
    for k in range(panels + 1):
        v = k * step
        weight = 1 if k in (0, panels) else (4 if k % 2 else 2)
        total += weight * math.exp(alpha * v) * interior_pgf(x, v, beta, mu)
    integral = step * total / 3.0
    return math.exp(-alpha * t) * (y + alpha * integral)


def derivative(
    state: list[float], time: float, alpha: float, beta: float, mu: float
) -> list[float]:
    size = len(state)
    out = [0.0] * size
    exterior = math.exp(-alpha * time)
    for i in range(size):
        if i > 0:
            out[i] -= (beta + mu) * i * state[i]
        if i + 1 < size:
            out[i] += mu * (i + 1) * state[i + 1]
        if i >= 1:
            out[i] += beta * (i - 1) * state[i - 1]
    out[1] += alpha * exterior
    return out


def rk4(
    alpha: float, beta: float, mu: float, t_end: float, size: int = 180
) -> list[float]:
    steps = 4000
    dt = t_end / steps
    state = [0.0] * size
    time = 0.0
    for _ in range(steps):
        k1 = derivative(state, time, alpha, beta, mu)
        s2 = [v + 0.5 * dt * k for v, k in zip(state, k1)]
        k2 = derivative(s2, time + 0.5 * dt, alpha, beta, mu)
        s3 = [v + 0.5 * dt * k for v, k in zip(state, k2)]
        k3 = derivative(s3, time + 0.5 * dt, alpha, beta, mu)
        s4 = [v + dt * k for v, k in zip(state, k3)]
        k4 = derivative(s4, time + dt, alpha, beta, mu)
        state = [
            v + dt * (a + 2 * b + 2 * c + d) / 6.0
            for v, a, b, c, d in zip(state, k1, k2, k3, k4)
        ]
        time += dt
    return state


def check_case(alpha: float, beta: float, mu: float, t: float) -> None:
    x, y = 0.63, 0.41
    state = rk4(alpha, beta, mu, t)
    direct = math.exp(-alpha * t) * y
    direct += sum(probability * x**i for i, probability in enumerate(state))
    closed = convolution_pgf(x, y, t, alpha, beta, mu)
    mass = math.exp(-alpha * t) + sum(state)
    assert abs(mass - 1.0) < 2e-10
    assert abs(direct - closed) < 2e-9
    print(
        f"alpha={alpha:g}, beta={beta:g}, mu={mu:g}: "
        f"|PGF difference|={abs(direct-closed):.3e}"
    )


def main() -> None:
    check_case(0.8, 0.6, 1.0, 0.9)
    check_case(0.8, 1.0, 0.6, 0.7)
    check_case(0.8, 0.8, 0.8, 0.7)
    print("PASS: PGF against truncated master equation")


if __name__ == "__main__":
    main()
