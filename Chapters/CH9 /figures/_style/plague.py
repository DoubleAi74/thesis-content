"""Birth–plague CTMC (var:eq:plague)."""

from __future__ import annotations

import numpy as np


def simulate(lam, delta, chi, mu, t_max, X0=80, Y0=2, seed=0):
    rng = np.random.default_rng(seed)
    t = 0.0
    X, Y = int(X0), int(Y0)
    ts = [t]
    Xs = [X]
    Ys = [Y]
    steps = 0
    while t < t_max and steps < 200_000:
        birth = lam * X
        loss = (delta + chi * Y) * X
        clear = mu * Y
        tot = birth + loss + clear
        if tot <= 0:
            break
        t += rng.exponential(1.0 / tot)
        if t > t_max:
            t = t_max
            ts.append(t)
            Xs.append(X)
            Ys.append(Y)
            break
        u = rng.random() * tot
        if u < birth:
            X += 1
        elif u < birth + loss:
            if X > 0:
                X -= 1
                Y += 1
        elif Y > 0:
            Y -= 1
        ts.append(t)
        Xs.append(X)
        Ys.append(Y)
        steps += 1
    return np.array(ts), np.array(Xs, dtype=float), np.array(Ys, dtype=float)
