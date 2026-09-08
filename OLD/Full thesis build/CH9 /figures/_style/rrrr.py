"""Rise–run–ruin–rejuvenation PDMP (var:eq:rrrrV, var:eq:rrrr)."""

from __future__ import annotations

import numpy as np


def simulate(phi, c, lam, delta, omega, t_max, X0=1, V0=5.0, seed=0, v_min=1e-6):
    rng = np.random.default_rng(seed)
    t = 0.0
    X = int(X0)
    V = float(V0)
    ts = [t]
    Xs = [X]
    Vs = [V]
    n_cat = 0
    while t < t_max:
        if X == 0:
            wait = rng.exponential(1.0 / omega)
            if t + wait > t_max:
                V += phi * (t_max - t)
                t = t_max
                ts.append(t)
                Xs.append(0)
                Vs.append(V)
                break
            V += phi * wait
            t += wait
            X = 1
            ts.append(t)
            Xs.append(X)
            Vs.append(V)
            continue
        V = max(V, v_min)
        alpha = phi - c * X
        u = rng.exponential(1.0)
        # Solve H(s) = λ X s + ∫ δ X / V(u) du = u
        # If alpha >= 0, V grows or holds; no hitting 0.
        # If alpha < 0, V hits v_min at s_hit = (V - v_min)/(-alpha).
        s = _invert_hazard(u, X, V, lam, delta, alpha, v_min)
        if t + s > t_max:
            dt = t_max - t
            V = max(V + alpha * dt, v_min)
            t = t_max
            ts.append(t)
            Xs.append(X)
            Vs.append(V)
            break
        V = max(V + alpha * s, v_min)
        t += s
        # Which event? birth vs catastrophe, given the time s.
        rate_b = lam * X
        rate_c = delta * X / V
        if rng.random() < rate_b / (rate_b + rate_c):
            X += 1
        else:
            X = 0
            n_cat += 1
        ts.append(t)
        Xs.append(X)
        Vs.append(V)
        if n_cat > 400:
            break
    return np.array(ts), np.array(Xs, dtype=float), np.array(Vs)


def _invert_hazard(u, X, V, lam, delta, alpha, v_min):
    """Invert A s + B ln(1 + C s) = u, with a cap if V would hit v_min."""
    A = lam * X
    if abs(alpha) < 1e-12:
        rate = A + delta * X / V
        return u / rate
    if alpha < 0.0:
        s_hit = (V - v_min) / (-alpha)
        s_hit = max(s_hit, 1e-12)
    else:
        s_hit = np.inf
    B = delta * X / alpha  # coefficient of ln

    def H(s):
        return A * s + B * np.log((V + alpha * s) / V)

    if np.isfinite(s_hit) and H(s_hit) <= u:
        return s_hit
    # Newton from the linearised guess.
    s = min(u / max(A, 1e-12), 0.5 * s_hit if np.isfinite(s_hit) else u / max(A, 1e-12))
    s = max(s, 1e-12)
    for _ in range(40):
        cap = V + alpha * s
        if cap <= 0:
            s *= 0.5
            continue
        h = A * s + B * np.log(cap / V) - u
        hp = A + delta * X / cap
        s_new = s - h / hp
        if s_new <= 0:
            s *= 0.5
            continue
        if np.isfinite(s_hit):
            s_new = min(s_new, 0.999 * s_hit)
        if abs(s_new - s) < 1e-10 * max(1.0, s):
            return s_new
        s = s_new
    return s
