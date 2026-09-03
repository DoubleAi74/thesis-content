#!/usr/bin/env python3
"""Validate _renewal.py against values the chapter already publishes."""
import numpy as np, _renewal as RN

ok = True
def chk(name, got, want, tol):
    global ok
    rel = abs(got-want)/max(abs(want),1e-12)
    good = rel < tol
    ok &= good
    print(f"  {'PASS' if good else 'FAIL'}  {name:<44} got {got:>12.6f}  want {want:>12.6f}  rel {rel:.2e}")

print("A. closed forms against tab:trio")
for (l,m,d), a_w, b_w, L_w, V_w, T_w, de_w, pe_w in [
    ((1,0,0.1),   1.100, 0.000, 1.10, 11.00, 2.398, 0.417, 4.59),
    ((1,0.5,1/3), 1.500, 1/3,   1.00,  2.00, 1.099, 0.910, 1.82),
    ((1,0.9,0.1), 1.316, 0.684, 0.42,  1.32, 1.426, 0.701, 0.92)]:
    R = RN.Rates(l,m,d)
    chk(f"a  {(l,m,d)}", round(R.a,3), a_w, 1e-9)
    chk(f"L  {(l,m,d)}", round(R.a*(1-R.b),2), L_w, 1e-9)
    chk(f"V_inf {(l,m,d)}", round(RN.V_inf(R),2), V_w, 1e-9)
    chk(f"E[T_prod] {(l,m,d)}", round(RN.T_prod(R),3), T_w, 1e-9)
    chk(f"d_eff(0) {(l,m,d)}", round(RN.d_eff(R,0.0),3), de_w, 1e-9)
    chk(f"p_eff(0) {(l,m,d)}", round(RN.p_eff(R,0.0),2), pe_w, 1e-9)

print("\nB. kernel integrals")
for (l,m,d) in [(1,0,0.1),(1,0.2,0.05),(1,0.9,0.1)]:
    R=RN.Rates(l,m,d)
    chk(f"int g = V_inf {(l,m,d)}", RN._laplace(R,0.0,'g'), RN.V_inf(R), 1e-9)
    chk(f"int Ifix = E[T] {(l,m,d)}", RN._laplace(R,0.0,'S'), RN.T_prod(R), 1e-9)

print("\nC. young-cell and old-cell endpoints of p_eff")
for (l,m,d) in [(1,0,0.1),(1,0.5,1/3),(1,0.9,0.1)]:
    R=RN.Rates(l,m,d)
    chk(f"p_eff(large r) -> delta {(l,m,d)}", RN.p_eff(R,400.0), d, 3e-2)
    lim = RN.p_eff_old_cell(R)
    Ifix,g = RN.kernels(R, np.array([80.0/R.theta]))
    chk(f"g/S at large age -> d*E_QS[X^2] {(l,m,d)}", float(g[0]/Ifix[0]), lim, 1e-8)

print("\nD. solver: R0 threshold and the characteristic root")
for (l,m,d), gT, c, R0_w in [((1,0,0.1),0.04,0.25,1.76),
                             ((1,0.2,0.05),0.03,0.2,2.10),
                             ((1,0,0.1),0.01,0.4,0.275),
                             ((1,0.9,0.1),0.4,0.2,2.63),
                             ((1,0,0.1),0.05,0.2,2.75),
                             ((1,0,0.1),0.025,0.2,1.37)]:
    R=RN.Rates(l,m,d)
    chk(f"R0 = gT V_inf/c  {(l,m,d)} gT={gT}", gT*RN.V_inf(R)/c, R0_w, 6e-3)
    r_star = RN.char_root(R,gT,c)
    t,I,V = RN.solve_renewal(R,gT,c,t_max=min(160.0, 40/max(abs(r_star),0.05)), n=6001)
    j = slice(int(0.75*len(t)), None)
    slope = np.polyfit(t[j], np.log(V[j]), 1)[0]
    chk(f"late slope = char root  {(l,m,d)} gT={gT}", slope, r_star, 4e-3)

print("\nE. exponential kernels reproduce classical BMVR (chapter test D)")
# renewal with S=e^{-d a}, g=p e^{-d a} must equal the classical ODE
class ExpR:  # duck-typed stand-in
    pass
for p,d_,gT,c in [(4.0,0.4,0.05,0.3),(2.0,0.9,0.2,0.5)]:
    n=8001; t_max=25.0
    t=np.linspace(0,t_max,n); h=t[1]-t[0]
    S=np.exp(-d_*t); g=p*np.exp(-d_*t); decay=np.exp(-c*t)
    GE=RN._trapz_conv(g,h,decay); A=gT*GE
    V=np.zeros(n); V[0]=0.0; I0=1.0
    for k in range(1,n):
        seg=A[:k+1]*V[k::-1]
        V[k]=I0*GE[k]+h*(seg.sum()-0.5*(seg[0]+seg[-1]))
    tc,Ic,Vc = RN.solve_classical(p,d_,gT,c,t_max,I0=1.0,V0=0.0,n=n)
    rel=np.max(np.abs(V-Vc))/np.max(np.abs(Vc))
    print(f"  {'PASS' if rel<2e-4 else 'FAIL'}  exp-kernel renewal == BMVR  (p={p}, d={d_})   max rel err {rel:.2e}")
    ok &= rel<2e-4

print("\n" + ("ALL CHECKS PASS" if ok else "SOME CHECKS FAILED"))
