"""Discrete-time Pimentel competition chain (var:eq:kernel)."""

from __future__ import annotations

import numpy as np


def icrit(N, pa, pb):
    if pa > 0.0 and pb == 0.0:
        return N * (1.0 - pa) / (2.0 - pa)
    if pb > 0.0 and pa == 0.0:
        return N / (2.0 - pb)
    return 0.5 * N


def simulate(N, alpha, eps, n_steps, A0=None, Ra0=1.0, Rb0=1.0, seed=0):
    """Return arrays A, ic, t up to absorption or n_steps."""
    rng = np.random.default_rng(seed)
    if A0 is None:
        A0 = N // 2
    A = np.empty(n_steps + 1, dtype=np.int64)
    ic = np.empty(n_steps + 1, dtype=np.float64)
    A[0] = A0
    Ra, Rb = float(Ra0), float(Rb0)
    pa = max(0.0, 1.0 - Rb / Ra)
    pb = max(0.0, 1.0 - Ra / Rb)
    ic[0] = icrit(N, pa, pb)
    a = int(A0)
    for t in range(n_steps):
        if a <= 0 or a >= N:
            A[t + 1 :] = a
            ic[t + 1 :] = ic[t]
            return A[: t + 1], ic[: t + 1]
        pa = max(0.0, 1.0 - Rb / Ra)
        pb = max(0.0, 1.0 - Ra / Rb)
        qa = (a / N) * (1.0 - pb)
        qb = (1.0 - a / N) * (1.0 - pa)
        u = rng.random()
        if u < qa:
            a += 1
        elif u < qa + qb:
            a -= 1
        A[t + 1] = a
        if 0 < a < N:
            dRa = (float(N - a) / float(a)) ** alpha
            dRb = (float(a) / float(N - a)) ** alpha
            Ra += eps * dRa
            Rb += eps * dRb
        pa = max(0.0, 1.0 - Rb / Ra) if Ra > 0 else 0.0
        pb = max(0.0, 1.0 - Ra / Rb) if Rb > 0 else 0.0
        ic[t + 1] = icrit(N, pa, pb)
    return A, ic
