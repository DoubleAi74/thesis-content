"""Public-good PDMP of var:eq:publicgood, with P floored at zero."""

from __future__ import annotations

import numpy as np


def _next_time(X, P, lam0, mu, alpha, g, c, rng, t_left):
    """Waiting time to next jump, or t_left if none. Also returns new P."""
    if X <= 0:
        return t_left, max(P, 0.0)
    gamma = g * X - c  # dP/dt
    u = rng.exponential(1.0)
    P = max(P, 0.0)

    def quadratic_root(A, B, target):
        """Smallest s>0 with A s + B s^2 = target. B may be 0."""
        if B <= 1e-18:
            return target / A if A > 0 else np.inf
        disc = A * A + 4.0 * B * target
        if disc < 0:
            return np.inf
        return (-A + np.sqrt(disc)) / (2.0 * B)

    if gamma >= 0.0:
        A = X * (lam0 + alpha * P + mu)
        B = 0.5 * X * alpha * gamma
        s = quadratic_root(A, B, u)
        s = min(s, t_left)
        return s, P + gamma * s

    # P falling. Hit zero at s_hit.
    s_hit = P / (-gamma) if P > 0 else 0.0
    A = X * (lam0 + alpha * P + mu)
    B = 0.5 * X * alpha * gamma  # negative
    # Hazard while P>0: A s + B s^2, B<0, defined on [0, s_hit].
    H_hit = A * s_hit + B * s_hit * s_hit
    if u <= H_hit and s_hit > 0:
        s = quadratic_root(A, B, u)
        s = min(max(s, 0.0), s_hit, t_left)
        return s, max(P + gamma * s, 0.0)
    # Event after P has hit 0, with constant rates λ0, μ.
    u2 = u - max(H_hit, 0.0)
    rate0 = X * (lam0 + mu)
    s2 = u2 / rate0 if rate0 > 0 else np.inf
    s = s_hit + s2
    if s >= t_left:
        # evolve P up to t_left
        if t_left <= s_hit:
            return t_left, max(P + gamma * t_left, 0.0)
        return t_left, 0.0
    return s, 0.0


def survive(K, lam0, mu, alpha, g, c, rng, t_max=40.0, x_surv=250):
    """True if the lineage is still alive (or has exploded) by t_max."""
    X = int(K)
    P = 0.0
    t = 0.0
    steps = 0
    while t < t_max and 0 < X < x_surv and steps < 50_000:
        dt, Pnew = _next_time(X, P, lam0, mu, alpha, g, c, rng, t_max - t)
        t += dt
        P = max(Pnew, 0.0)
        if t >= t_max:
            break
        # Which jump? birth vs death at the current (X, P).
        lam = lam0 + alpha * P
        if lam < 0:
            lam = 0.0
        tot = (lam + mu) * X
        if tot <= 0:
            break
        if rng.random() < lam / (lam + mu):
            X += 1
        else:
            X -= 1
        steps += 1
    return X > 0


def survival_prob(K, lam0, mu, alpha, g, c, n_paths=800, seed=0, **kw):
    rng = np.random.default_rng(seed)
    hits = sum(
        survive(K, lam0, mu, alpha, g, c, rng, **kw) for _ in range(n_paths)
    )
    return hits / n_paths


def kstar(lam0, mu, alpha, g, c, n_paths=800, k_max=40, seed=1, thresh=0.5):
    """Smallest integer K with estimated survival > thresh."""
    for K in range(1, k_max + 1):
        p = survival_prob(K, lam0, mu, alpha, g, c, n_paths=n_paths, seed=seed + K)
        if p > thresh:
            return K, p
    return None, None
