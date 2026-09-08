#!/usr/bin/env python3
"""Recompute every numerical claim made in Chapter 5 from the closed forms.

Each check prints  ID | claim | quoted | recomputed | verdict.
Nothing here reads the chapter source: the closed forms are transcribed from
the ledger (CH5_invariants.md) and the quoted values from the chapter text,
so a disagreement means either the chapter or this file is wrong, and the
disagreement is reported rather than silently absorbed.

Run:  python3 verification/recheck_numbers.py
"""

from __future__ import annotations

import math
from decimal import Decimal, getcontext

getcontext().prec = 60

# --------------------------------------------------------------------------
# closed forms
# --------------------------------------------------------------------------


def roots(lam: float, mu: float, dlt: float) -> tuple[float, float, float]:
    eta = (lam + mu + dlt) / (2.0 * lam)
    disc = eta * eta - mu / lam
    a = eta + math.sqrt(disc)
    b = eta - math.sqrt(disc)
    return a, b, lam * (a - b)


def I_t(t, lam, mu, dlt):
    a, b, th = roots(lam, mu, dlt)
    A, B, w = a - 1.0, 1.0 - b, math.exp(th * t)
    return (a * B + b * A * w) / (B + A * w)


def D_t(t, lam, mu, dlt):
    a, b, th = roots(lam, mu, dlt)
    w = math.exp(th * t)
    return a * b * (w - 1.0) / (a * w - b)


def Ifix_t(t, lam, mu, dlt):
    a, b, th = roots(lam, mu, dlt)
    A, B, w = a - 1.0, 1.0 - b, math.exp(th * t)
    return (a - b) ** 2 * w / ((B + A * w) * (a * w - b))


def J_t(t, lam, mu, dlt):
    a, b, th = roots(lam, mu, dlt)
    A, B, w = a - 1.0, 1.0 - b, math.exp(th * t)
    return (a - b) ** 2 * w / (B + A * w) ** 2


def K_t(t, lam, mu, dlt):
    return (1.0 + 2.0 * lam * (1.0 - I_t(t, lam, mu, dlt)) / dlt) * J_t(t, lam, mu, dlt)


def V_t(t, lam, mu, dlt):
    I = I_t(t, lam, mu, dlt)
    return (1.0 - I) * (1.0 + lam * (1.0 - I) / dlt)


def EW2_t(t, lam, mu, dlt):
    I, K, V = I_t(t, lam, mu, dlt), K_t(t, lam, mu, dlt), V_t(t, lam, mu, dlt)
    return (
        2.0 * (lam - mu) / dlt * V
        - (lam + mu) / dlt * I
        - K
        + (lam + mu) / dlt
        + 1.0
    )


def P_t(t, lam, mu, dlt):
    a, b, th = roots(lam, mu, dlt)
    w = math.exp(th * t)
    return (1.0 - w) / (b - a * w)


def p_n(n, t, lam, mu, dlt):
    a, b, th = roots(lam, mu, dlt)
    w = math.exp(th * t)
    p1 = ((a - b) / (b - a * w)) ** 2 * w
    return p1 * P_t(t, lam, mu, dlt) ** (n - 1)


def Vinf(lam, mu, dlt):
    a, b, _ = roots(lam, mu, dlt)
    return a * (1.0 - b) / (a - 1.0)


def T_prod(lam, mu, dlt):
    a, _, _ = roots(lam, mu, dlt)
    return math.log(a / (a - 1.0)) / lam


def tau_given_burst(lam, mu, dlt):
    a, b, _ = roots(lam, mu, dlt)
    return math.log((a - b) / (a - 1.0)) / (lam * (1.0 - b))


def Vinf_k(k, lam, mu, dlt):
    """Lifetime yield from k founders, eq. (Vk)."""
    a, b, _ = roots(lam, mu, dlt)
    first = (1.0 - b**k) + (2.0 * lam / dlt) * (
        1.0 / (k + 1.0) - b**k + k * b ** (k + 1.0) / (k + 1.0)
    )
    if k == 1:
        return first
    # k(k-1)(lam/dlt) * int_1^b (x-a)(x-b) x^{k-2} dx
    def anti(x):
        return (
            x ** (k + 1.0) / (k + 1.0)
            - (a + b) * x**k / k
            + a * b * x ** (k - 1.0) / (k - 1.0)
        )

    return first + k * (k - 1.0) * (lam / dlt) * (anti(b) - anti(1.0))


def meanT_chain(k, lam, dlt, terms=4_000_000):
    """E[T(k)] = sum_{m>=0} rho^m / ((lam+dlt)(k+m)) for the mu=0 chain."""
    rho = lam / (lam + dlt)
    total, term = 0.0, 1.0
    m = 0
    while m < terms:
        contrib = term / ((lam + dlt) * (k + m))
        total += contrib
        if term < 1e-18 and m > 50:
            break
        term *= rho
        m += 1
    return total


# --------------------------------------------------------------------------
# the same two formulas in 60-digit decimal arithmetic, so that the numerical
# derivative in key check 1 is not swamped by cancellation at late t
# --------------------------------------------------------------------------


def dec_roots(pars):
    lam, mu, dlt = (Decimal(repr(x)) for x in pars)
    eta = (lam + mu + dlt) / (2 * lam)
    r = (eta * eta - mu / lam).sqrt()
    a, b = eta + r, eta - r
    return a, b, lam * (a - b)


def dec_P(t, pars):
    a, b, th = dec_roots(pars)
    w = (th * t).exp()
    return (1 - w) / (b - a * w)


def dec_p1(t, pars):
    a, b, th = dec_roots(pars)
    w = (th * t).exp()
    return ((a - b) / (b - a * w)) ** 2 * w


# --------------------------------------------------------------------------
# harness
# --------------------------------------------------------------------------

RESULTS: list[tuple[str, str, str, str, bool]] = []


def check(cid: str, claim: str, quoted, computed, tol=5e-3, fmt="{:.4f}"):
    if quoted is None:
        ok = True
        q = "--"
    else:
        ok = abs(quoted - computed) <= tol
        q = fmt.format(quoted)
    RESULTS.append((cid, claim, q, fmt.format(computed), ok))


WORK = (1.0, 0.2, 0.05)          # the chapter's running parameter set
FT = (0.15, 0.01, 1.5e-4)        # F. tularensis SCHU S4, per hour
BA = (0.64, 1.64, 0.04)          # B. anthracis, per hour

lam, mu, dlt = WORK
a, b, th = roots(lam, mu, dlt)
A, B = a - 1.0, 1.0 - b

# --- roots and identities -------------------------------------------------
check("NUM-001", "a at (1,0.2,0.05)", 1.0616, a)
check("NUM-002", "b at (1,0.2,0.05)", 0.1884, b, tol=1e-3, fmt="{:.4f}")
check("NUM-003", "AB = delta/lambda", dlt / lam, A * B, tol=1e-12, fmt="{:.8f}")
check("NUM-004", "ab = mu/lambda", mu / lam, a * b, tol=1e-12, fmt="{:.8f}")

# --- lifetime release and burst means ------------------------------------
check("NUM-005", "V_infty", 13.9857, Vinf(*WORK))
check("NUM-006", "E[K|burst] = a/(a-1)", 17.2321, a / (a - 1.0))
check("NUM-007", "late-burst limit (a+1)/(a-1)", 33.4642, (a + 1.0) / (a - 1.0))
check("NUM-008", "QS variance a/(a-1)^2", None, a / (a - 1.0) ** 2)
check(
    "NUM-009",
    "late/average burst ratio (a+1)/a at work",
    1.94,
    (a + 1.0) / a,
    tol=5e-3,
    fmt="{:.3f}",
)
aB, bB, _ = roots(*BA)
check(
    "NUM-010",
    "late/average burst ratio (a+1)/a at anthrax",
    1.38,
    (aB + 1.0) / aB,
    tol=5e-3,
    fmt="{:.3f}",
)

# --- productive lifetime --------------------------------------------------
check("NUM-011", "E[T_prod]", 2.8468, T_prod(*WORK))
check("NUM-012", "matched death rate d_I = 1/E[T_prod]", 0.3513, 1.0 / T_prod(*WORK))

# --- multi-founder --------------------------------------------------------
I1, D1 = I_t(1.0, *WORK), D_t(1.0, *WORK)
check("NUM-013", "Ifix_2 = I^2 - D^2 at t=1", 0.8458, I1**2 - D1**2)
check("NUM-014", "(Ifix)^2 at t=1 (the wrong guess)", 0.6542, (I1 - D1) ** 2)
J1, K1 = J_t(1.0, *WORK), K_t(1.0, *WORK)
K2_true = 2.0 * K1 * I1 + 2.0 * J1**2
K2_free = 2.0 * K1 + 2.0 * J1**2
check("NUM-015", "K_2 at t=1 (true, eq. Kk)", 22.2645, K2_true)
check("NUM-016", "K_2 at t=1 (free sum, wrong)", 23.3923, K2_free)
vk = [Vinf_k(k, *WORK) for k in (1, 2, 3, 5)]
check("NUM-017", "V_infty^(1)", 13.99, vk[0], tol=6e-3, fmt="{:.4f}")
check("NUM-018", "V_infty^(2)", 17.43, vk[1], tol=6e-3, fmt="{:.4f}")
check("NUM-019", "V_infty^(3)", 18.89, vk[2], tol=6e-3, fmt="{:.4f}")
check("NUM-020", "V_infty^(5)", 21.00, vk[3], tol=6e-3, fmt="{:.4f}")
cond = [vk[i] / (1.0 - b ** k) for i, k in enumerate((1, 2, 3, 5))]
check("NUM-021", "V^(1)/(1-b)", 17.23, cond[0], tol=6e-3, fmt="{:.4f}")
check("NUM-022", "V^(2)/(1-b^2)", 18.07, cond[1], tol=6e-3, fmt="{:.4f}")
check("NUM-023", "V^(3)/(1-b^3)", 19.02, cond[2], tol=6e-3, fmt="{:.4f}")
check("NUM-024", "V^(5)/(1-b^5)", 21.00, cond[3], tol=6e-3, fmt="{:.4f}")
check("NUM-025", "2 V_infty (naive scaling)", 27.97, 2.0 * Vinf(*WORK), tol=6e-3)
check(
    "NUM-026",
    "V_infty^(k)=k+lambda/delta at mu=0, (1,0,0.1), k=1..5",
    None,
    max(abs(Vinf_k(k, 1.0, 0.0, 0.1) - (k + 10.0)) for k in (1, 2, 3, 4, 5)),
    fmt="{:.2e}",
)

# --- budding comparator ---------------------------------------------------
p_over_d = a / (a - 1.0)          # budding mean matched to the BDC conditional mean
check("NUM-027", "budding Pr{K=0} at matched mean", 0.0548, 1.0 / (1.0 + p_over_d))

# --- chained transfer -----------------------------------------------------
mt = [meanT_chain(k, 1.0, 1.0) for k in (1, 2, 3, 4)]
check("NUM-028", "E[T(1)] at (lam,dlt)=(1,1)", 0.693, mt[0], tol=1e-3, fmt="{:.3f}")
check("NUM-029", "E[T(2)]", 0.386, mt[1], tol=1e-3, fmt="{:.3f}")
check("NUM-030", "E[T(3)]", 0.273, mt[2], tol=1e-3, fmt="{:.3f}")
check("NUM-031", "E[T(4)]", 0.212, mt[3], tol=1e-3, fmt="{:.3f}")

# --- biology --------------------------------------------------------------
aF, bF, _ = roots(*FT)
check("NUM-032", "F. tularensis b (%)", 6.66, 100.0 * bF, tol=5e-3, fmt="{:.2f}")
check("NUM-033", "F. tularensis E[K|burst]", 934.0, aF / (aF - 1.0), tol=0.5, fmt="{:.1f}")
check("NUM-034", "F. tularensis E[T_prod] (h)", 45.6, T_prod(*FT), tol=5e-2, fmt="{:.1f}")
check(
    "NUM-035",
    "F. tularensis E[tau|burst] (h)",
    48.4,
    tau_given_burst(*FT),
    tol=5e-2,
    fmt="{:.1f}",
)
check(
    "NUM-036",
    "F. tularensis median burst size",
    647.0,
    math.ceil(math.log(2.0) / math.log(aF)),
    tol=1.0,
    fmt="{:.0f}",
)
check("NUM-037", "F. tularensis a", 1.001, aF, tol=5e-4, fmt="{:.4f}")
check("NUM-038", "B. anthracis b (%)", 96.24, 100.0 * bB, tol=5e-3, fmt="{:.2f}")
check("NUM-039", "B. anthracis E[K|burst]", 1.60, aB / (aB - 1.0), tol=5e-3, fmt="{:.3f}")
check("NUM-040", "B. anthracis E[T_prod] (h)", 0.74, T_prod(*BA), tol=5e-3, fmt="{:.3f}")
check(
    "NUM-041",
    "B. anthracis E[tau|burst] (h)",
    0.93,
    tau_given_burst(*BA),
    tol=5e-3,
    fmt="{:.3f}",
)
check("NUM-042", "B. anthracis a", 2.66, aB, tol=5e-3, fmt="{:.4f}")

# --------------------------------------------------------------------------
# the three checks that carry licensed additions (b) and (c)
# --------------------------------------------------------------------------

print("=" * 78)
print("CHAPTER 5 --- recheck of numerical claims")
print("=" * 78)
print()
print("KEY CHECK 1.  p_1(t) = P'(t)/lambda, several t and several parameter sets")
print("  (central difference in 60-digit decimal arithmetic, step h = 1e-15)")
print("-" * 78)
h = Decimal("1e-15")
key1_worst = 0.0
for pars in (WORK, (1.0, 0.0, 0.1), (0.5, 0.9, 0.3), (2.0, 0.1, 0.7)):
    for t in (0.3, 1.0, 3.0, 8.0):
        td = Decimal(repr(t))
        dP = (dec_P(td + h, pars) - dec_P(td - h, pars)) / (2 * h)
        lhs = dec_p1(td, pars)
        rhs = dP / Decimal(repr(pars[0]))
        rel = abs((lhs - rhs) / lhs)
        key1_worst = max(key1_worst, float(rel))
        print(
            f"  (lam,mu,dlt)={pars}  t={t:>4}  p_1={float(lhs):.12e}  "
            f"P'/lam={float(rhs):.12e}  rel={float(rel):.2e}"
        )
print(f"  worst relative discrepancy: {key1_worst:.2e}   "
      f"{'PASS' if key1_worst < 1e-20 else 'FAIL'}")
print()

print("KEY CHECK 2.  vartheta = mu nu_1 + sum_i delta i nu_i  equals  lambda(a-b)")
print("-" * 78)
key2_worst = 0.0
for pars in (WORK, (1.0, 0.0, 0.1), (0.5, 0.9, 0.3), (2.0, 0.1, 0.7)):
    L, M, Dl = pars
    aa, bb, tt = roots(*pars)
    nu = [(aa - 1.0) * aa ** (-n) for n in range(1, 200_001)]
    vth = M * nu[0] + sum(Dl * (n + 1) * nu[n] for n in range(len(nu)))
    rel = abs(vth - tt) / tt
    key2_worst = max(key2_worst, rel)
    print(
        f"  (lam,mu,dlt)={pars}  vartheta={vth:.12f}  "
        f"lambda(a-b)={tt:.12f}  rel={rel:.2e}"
    )
# the algebraic route of the plan: lambda b(a-1) + lambda a(1-b) = lambda(a-b)
alg = lam * b * (a - 1.0) + lam * a * (1.0 - b)
print(f"  algebraic form  lambda b(a-1)+lambda a(1-b) = {alg:.12f} "
      f"vs theta = {th:.12f}")
print(f"  worst relative discrepancy: {key2_worst:.2e}   "
      f"{'PASS' if key2_worst < 1e-6 else 'FAIL'}")
print()

print("KEY CHECK 3.  Ifix_k = I^k - D^k  against  (Ifix)^k  at (1,0.2,0.05), t=1")
print("-" * 78)
print(f"  I(1)={I1:.6f}  D(1)={D1:.6f}")
print(f"  Ifix_2 = I^2-D^2 = {I1**2 - D1**2:.4f}   (chapter quotes 0.8458)")
print(f"  (Ifix)^2         = {(I1-D1)**2:.4f}   (chapter quotes 0.6542)")
print(f"  difference 2D(I-D) = {2*D1*(I1-D1):.6f}")
key3 = (
    abs((I1**2 - D1**2) - 0.8458) < 5e-4 and abs((I1 - D1) ** 2 - 0.6542) < 5e-4
)
print(f"  {'PASS' if key3 else 'FAIL'}")
print()

# --- structural identities, no quoted value ------------------------------
print("STRUCTURAL IDENTITIES")
print("-" * 78)
# sum_{n>=1} p_n = Ifix
worst = max(
    abs(sum(p_n(n, t, *WORK) for n in range(1, 6000)) - Ifix_t(t, *WORK))
    for t in (0.5, 1.0, 3.0, 10.0)
)
print(f"  sum_n p_n(t) = Ifix(t):                 max err {worst:.2e}")
# E[W_inf^2] at mu=0 against the geometric second moment
lam0, dlt0 = 1.0, 0.1
s0 = dlt0 / (lam0 + dlt0)
lhs = EW2_t(120.0, lam0, 0.0, dlt0)
rhs = (2.0 - s0) / s0**2
print(f"  E[W_inf^2] at mu=0 vs (2-s)/s^2:        {lhs:.6f} vs {rhs:.6f}")
# burst-size law normalisation and first moment
tot = sum((dlt / lam) * a ** (-k) for k in range(1, 20_000))
fst = sum(k * (dlt / lam) * a ** (-k) for k in range(1, 20_000))
print(f"  sum_k (delta/lam) a^-k = 1-b:           {tot:.10f} vs {1.0-b:.10f}")
print(f"  sum_k k (delta/lam) a^-k = V_infty:     {fst:.6f} vs {Vinf(*WORK):.6f}")
# telescoping: delta k int p_k dt = (delta/lambda) a^-k, by the P-clock
tel = max(
    abs(dlt * k * (1.0 / (k * lam)) * (1.0 / a) ** k - (dlt / lam) * a ** (-k))
    for k in range(1, 40)
)
print(f"  telescoped burst law vs closed form:    max err {tel:.2e}")
# K/J = (1+P)/(1-P) exactly, at every t -- the identity behind eq:kjP, which
# is what makes the limit at eq:latemean continuity rather than an interchange
kj_worst = max(
    abs(K_t(t, *WORK) / J_t(t, *WORK)
        - (1.0 + P_t(t, *WORK)) / (1.0 - P_t(t, *WORK)))
    for t in (0.25, 0.5, 1.0, 2.0, 5.0, 10.0, 25.0, 60.0)
)
print(f"  K/J = (1+P)/(1-P) at every t:           max err {kj_worst:.2e}")
# harmonic law for tau | K = n, mu = 0
th0 = lam0 + dlt0
harm = [sum(1.0 / j for j in range(1, n + 1)) / th0 for n in (1, 5, 20)]
print(f"  E[tau|K=n]/(1/theta) at n=1,5,20:        "
      f"{harm[0]:.4f}, {harm[1]:.4f}, {harm[2]:.4f}  (theta={th0})")
print()

# --------------------------------------------------------------------------
print("QUOTED-VALUE COMPARISONS")
print("=" * 78)
print(f"{'ID':<9} {'claim':<44} {'quoted':>10} {'recomputed':>12}  ")
print("-" * 78)
bad = 0
for cid, claim, q, c, ok in RESULTS:
    flag = "ok" if ok else "MISMATCH"
    bad += 0 if ok else 1
    print(f"{cid:<9} {claim:<44} {q:>10} {c:>12}  {flag}")
print("-" * 78)
print(f"{len(RESULTS)} quoted values checked; {bad} mismatches.")
print(
    "three key checks: "
    f"1 {'PASS' if key1_worst < 1e-8 else 'FAIL'}, "
    f"2 {'PASS' if key2_worst < 1e-6 else 'FAIL'}, "
    f"3 {'PASS' if key3 else 'FAIL'}"
)
