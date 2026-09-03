# CH6 invariants ledger

Built by Phase A **before any prose was written**, per plan §3.
Source: `CH6 revise/4b BDC_odes DRAFT U/` (byte-identical twin of `Chapter numbers/CH6/`).

**Rule.** Every entry below is frozen. The *only* permitted alterations are the
notation substitutions of plan §6, listed here once and referred to as
"P1"–"P6":

| ID | Substitution | Scope |
|---|---|---|
| **P1** | cell age `a` → `\alpha` | kernels, convolutions, all age arguments. Does **not** touch the root `a` of the characteristic quadratic. |
| **P2** | eclipse conversion rate `\alpha` → `\omega` | §6.1 Cases 2, 5; §6.5 HIV Erlang chain |
| **P3** | geometric parameter `r` → `\varrho` | inside the proof of `prop:L1` only |
| **P4** | Model 10 release intensity `r(t), r_0, \bar r` → `\psi(t), \psi_0, \bar\psi` | App E |
| **P5** | mean load per productive cell `m` → `\bar x` | §6.1 Case 3/4/5, §6.2 mature limit, §6.5 growth law |
| **P6** | Dirac source `\delta_0(t)` → restated as an initial condition | §6.5 HIV stage ODEs |

Anything else that differs from the LaTeX recorded below is a defect.

---

## A. Displayed equations

Recorded as: `ID (old label, old file:line) → new label | lands in | permitted edits`.

### From `01_what_we_need.tex`

**EQ-001** (unlabelled, 01:37–41) → `p:eq:roots` | App A / §1.4 | none
```
a=\eta+\sqrt{\eta^2-\frac{\mu}{\lambda}},\qquad
b=\eta-\sqrt{\eta^2-\frac{\mu}{\lambda}},\qquad
\eta=\frac{\lambda+\mu+\delta}{2\lambda},
```

**EQ-002** (unlabelled, 01:43–45) → `p:eq:derived` | §1.4 | none
```
A=a-1,\qquad B=1-b,\qquad \theta=\lambda(a-b),\qquad \kappa=1+\frac{\delta}{2\lambda}.
```

**EQ-003** (`eq:AB`, 01:47–51) → `p:eq:AB` | §1.4 | none
```
\boxed{ab=\frac{\mu}{\lambda},\quad a+b=\frac{\lambda+\mu+\delta}{\lambda},\quad
AB=\frac{\delta}{\lambda},\quad A+B=a-b,\quad \theta=\lambda(a-b).}
```

**EQ-004** (`eq:IDIhat`, 01:57–62) → `p:eq:IDIhat` | §1.4 | P1 (`t`→`\alpha` not required; kept as `t`)
```
\boxed{I(t)=\frac{aB+bAw}{B+Aw},\qquad
D(t)=\frac{ab\,(w-1)}{aw-b},\qquad
\Ifix(t)=I(t)-D(t)=\frac{(a-b)^2\,w}{(B+Aw)(aw-b)}.}
```

**EQ-005** (`eq:J`, 01:71–74) → `p:eq:J` | §1.4 | none
```
\boxed{J(t)=\frac{(a-b)^2\,w}{(B+Aw)^2}=-\frac{\lambda}{\delta}(I-a)(I-b),}
```

**EQ-006** (`eq:K`, 01:75–79) → `p:eq:K` | §1.4 | none
```
\boxed{K(t)=\Bigl[1+\frac{2\lambda}{\delta}(1-I)\Bigr]J
=\frac{2\lambda}{\delta}(\kappa-I)J,}
```

**EQ-007** (`eq:V`, 01:81–84) → `p:eq:V` | §1.4 | none
```
\boxed{V(t)=(1-I)\Bigl[1+\frac{\lambda}{\delta}(1-I)\Bigr].}
```

**EQ-008** (`eq:Vinf`, 01:86–92) → `p:eq:Vinf` | §1.4 | none
```
\boxed{V_\infty=\frac{a(1-b)}{a-1}=\frac{aB}{A}
=\frac{\lambda-\mu}{\delta}(1-b)+1,
\qquad
\mean{\Kb\mid\text{burst}}=\frac{V_\infty}{1-b}=\frac{a}{a-1}.}
```

**EQ-009** (`eq:phi`, 01:100–103) → `p:eq:bursttime` | App A | none
```
-I'(t)=\delta J(t),
```

**EQ-010** (`eq:burstlaw`, 01:106–109) → `p:eq:burstlaw` | App A | none
```
\pr{\Kb=k}=\frac{\delta}{\lambda}\,a^{-k},\qquad k\ge1,
```

**EQ-011** (`eq:sizebias`, 01:115–119) → `p:eq:sizebias` | App A | none
```
\boxed{\mean{\Kb\mid\tau=t}=\frac{K(t)}{J(t)}
=1+\frac{2\lambda}{\delta}\bigl(1-I(t)\bigr),}
```

**EQ-012** (`eq:EW2`, 01:126–134) → `p:eq:EW2` | App A | none
```
\boxed{\mean{\wt^2}
=\frac{2(\lambda-\mu)}{\delta}V
-\frac{\lambda+\mu}{\delta}I
-K
+\frac{\lambda+\mu}{\delta}
+1,}
```

**EQ-013** (`prop:lifetime`, 01:141–146) → `p:eq:lifetime` | §1.4 | none
```
\boxed{\mean{T_{\rm prod}}=\int_0^\infty\Ifix(t)\,\dd t
=\frac{1}{\lambda}\log\frac{a}{a-1}
=\frac{1}{\lambda}\log\mean{\Kb\mid\text{burst}}.}
```

**EQ-014** (unlabelled, 01:152–155) → `p:eq:JkKk` | App A | none
```
J_k(t)=kJ(t)I(t)^{k-1},\qquad
K_k(t)=kK(t)I(t)^{k-1}+k(k-1)J(t)^2I(t)^{k-2},
```

**EQ-015** (`eq:gk`, 01:156–160) → `p:eq:gk` | App A | none
```
\boxed{g_k(t)=\delta K_k(t)
=\delta\lrb{kK I^{k-1}+k(k-1)J^2I^{k-2}},}
```

**EQ-016** (`eq:Vk`, 01:162–168) → `p:eq:Vk` | App A | none
```
\boxed{V_\infty^{(k)}
=(1-b^k)
+\frac{2\lambda}{\delta}\Biggl[\frac{1}{k+1}-b^k+\frac{k\,b^{k+1}}{k+1}\Biggr]
+k(k-1)\frac{\lambda}{\delta}\int_1^b (x-a)(x-b)\,x^{k-2}\,\dd x,}
```
with the specialisation `V_\infty^{(k)}=k+\lambda/\delta` when `\mu=0`.

### From `02_why_constant_release_fails.tex`

**EQ-017** (`eq:BMVR-classical`, 02:20–25) → `p:eq:bmvr-classical` | §2.1 | none
```
\ddt{\Icell} = \gamma T\,\Vfree - d_{\Icell}\,\Icell,
\qquad
\ddt{\Vfree} = p\,\Icell - c\,\Vfree,
```

**EQ-018** (unlabelled, 02:32–34) → `p:eq:R0classical` | §2.1 | none
```
R_0=\frac{\gamma T\,p}{c\,d_{\Icell}}.
```

**EQ-019** (`eq:bud-cell`, 02:46–52) → `p:eq:bud-cell` | §2.1 | none
```
I_{\rm bud}(t)=\ee^{-d_{\Icell}t},\qquad
V_{\rm bud}(t)=\frac{p}{d_{\Icell}}\lrb{1-\ee^{-d_{\Icell}t}},
\qquad
\dda{V_{\rm bud}}{I_{\rm bud}}=-\frac{p}{d_{\Icell}}:
```
plus the inline geometric law
`\pr{\Kb_{\rm bud}=k}=\frac{d_{\Icell}}{d_{\Icell}+p}(\frac{p}{d_{\Icell}+p})^k`.

**EQ-020** (unlabelled, 02:83–85) → `p:eq:cohort` | §2.2 | none
```
\Vfree(t)=N_0\,V(t),
```

**EQ-021** (`eq:naive-p`, 02:112–115) → `p:eq:naive-p` | §2.3 | none
```
p\ \stackrel{?}{=}\ \langle X\rangle_{\rm QS}=\frac{a}{a-1}.
```

**EQ-022** (unlabelled, 02:128–132) → `p:eq:naive-repair` | §2.3 | none
```
\int_0^\infty\delta J(t)\,\mean{\Kb\mid\tau=t}\,\dd t
=\delta\int_0^\infty K(t)\,\dd t
=V_\infty,
```

### From `03_renewal_bmvr.tex`

**EQ-023** (`eq:Skernel`, 03:19–23) → `p:eq:Skernel` | §3.1 | **P1** (`S(a)`→`S(\alpha)`, `\ee^{\theta a}`→`\ee^{\theta\alpha}`; the roots `a`, `b`, `A`, `B` are untouched)
```
S(a):=\Ifix(a)=\frac{(a-b)^2\,\ee^{\theta a}}
{\lrb{B+A\ee^{\theta a}}\lrb{a\ee^{\theta a}-b}}.
```
→ `S(\alpha):=\Ifix(\alpha)=\frac{(a-b)^2\,\ee^{\theta\alpha}}{\lrb{B+A\ee^{\theta\alpha}}\lrb{a\ee^{\theta\alpha}-b}}.`

**EQ-024** (`eq:gkernel`, 03:25–28) → `p:eq:gkernel` | §3.1 | **P1**
```
g(a):=\delta K(a)=V'(a).
```

**EQ-025** (unlabelled, 03:69–71) → `p:eq:incidence` | §3.2 | none
```
i(t)=\gamma T\,\Vfree(t).
```

**EQ-026** (`eq:Icell`, 03:111–115) → `p:eq:Icell` | §3.2 | none (already uses `\alpha`)
```
\Icell(t)=\Icell_0\,\Ifix(t)+\int_0^t i(t-\alpha)\,\Ifix(\alpha)\,\dd\alpha
=\Icell_0\,\Ifix+(i*\Ifix)(t),
```

**EQ-027** (`eq:Vfree`, 03:116–121) → `p:eq:Vfree` | §3.2 | none
```
\ddt{\Vfree}(t)
=\Icell_0\,g(t)+\int_0^t i(t-\alpha)\,g(\alpha)\,\dd\alpha-c\,\Vfree(t)
=\Icell_0\,g+(i*g)(t)-c\,\Vfree(t).
```

**EQ-028** (unlabelled, 03:151–154) → `p:eq:Icell-diff` | §3.2 | none
```
\ddt{\Icell}
= i(t)+\Icell_0\,\Ifix'(t)+\int_0^t i(t-\alpha)\,\Ifix'(\alpha)\,\dd\alpha,
```

**EQ-029** (`eq:r0match`, 03:235–241) → `p:eq:r0match` | §4.3 | none
```
p=p_{\rm eff}(0)=\frac{V_\infty}{\mean{T_{\rm prod}}}
=\frac{\lambda V_\infty}{\log\bigl(a/(a-1)\bigr)},
\qquad
d_{\Icell}=d_{\Icell,{\rm eff}}(0)=\frac{\lambda}{\log\bigl(a/(a-1)\bigr)},
```

**EQ-030** (unlabelled, 03:278–281) → `p:eq:reldiff` | §4.3 | none
```
\frac{\bigl|\Vfree^{\rm new}(t)-\Vfree^{\rm classical}(t)\bigr|}
{\max_s \Vfree^{\rm new}(s)},
```

### From `04_effective_parameters_r0_identifiability.tex`

**EQ-031** (unlabelled, 04:19–23) → `p:eq:expphase` | §4.1 | none
```
\Icell(t)=i_0\ee^{rt}\Lap{\Ifix}(r),
\qquad
\Vfree'(t)=i_0\ee^{rt}\,\delta\Lap{K}(r)-c\,\Vfree(t),
```
with `\Lap{f}(r)=\int_0^\infty\ee^{-r\alpha}f(\alpha)\,\dd\alpha`.

**EQ-032** (`eq:peff`, 04:29–34) → `p:eq:peff` | §4.1 | none
```
p_{\rm eff}(r)=\frac{\delta\,\Lap{K}(r)}{\Lap{\Ifix}(r)},
\qquad
d_{\Icell,{\rm eff}}(r)=\frac{1}{\Lap{\Ifix}(r)}-r.
```

**EQ-033** (`eq:char`, 04:38–41) → `p:eq:char` | §4.1 | none
```
r+c=\gamma T\,\delta\Lap{K}(r),
```

**EQ-034** (`eq:peff0`, 04:53–60) → `p:eq:peff0` | §4.1 | none
```
r=0:\qquad
p_{\rm eff}(0)=\frac{V_\infty}{\mean{T_{\rm prod}}}
=\frac{\lambda\,V_\infty}{\log\bigl(a/(a-1)\bigr)},
\qquad
d_{\Icell,{\rm eff}}(0)=\frac{\lambda}{\log\bigl(a/(a-1)\bigr)};
```

**EQ-035** (`eq:peffinf`, 04:65–71) → `p:eq:peffinf` | §4.1 | none
```
r\to\infty:\qquad
p_{\rm eff}(r)\to\delta,
\qquad
d_{\Icell,{\rm eff}}(r)\to\mu+\delta,
```

**EQ-036** (`eq:R0ODE`, 04:103–106) → `p:eq:R0ODE` | §4.4 | none
```
R_0^{\mathrm{ODE}}=\frac{\gamma T\,V_\infty}{c}.
```

**EQ-037** (unlabelled, 04:161–163) → `p:eq:identmap` | §4.5 | none
```
(\lambda,\mu,\delta)\ \longmapsto\ \lrb{p_{\rm eff}(r),\,d_{\Icell,{\rm eff}}(r)}
```

### From `05_flooding_and_growth_rate_tradeoff.tex`

**EQ-038** (unlabelled, 05:21–23) → `p:eq:q` | §5.1 | none
```
q=\frac{\gamma T}{\gamma T+c}.
```

**EQ-039** (`eq:Goff`, 05:29–33) → `p:eq:Goff` | §5.1 | none
```
G_{\rm off}(z)=b+\frac{\delta}{\lambda}\,\frac{y}{a-y},
\qquad y=1-q+qz.
```
with the preceding inline `G_{\Kb}(z)=b+(\delta/\lambda)\,z/(a-z)`.

**EQ-040** (`eq:offmoments`, 05:36–42) → `p:eq:offmoments` | §5.1 | none
```
m=G_{\rm off}'(1)=q\,V_\infty,
\qquad
\mathrm{Var}_{\rm burst}
=\frac{2q^2V_\infty}{a-1}+qV_\infty-q^2V_\infty^2,
```

**EQ-041** (`eq:zext`, 05:53–58) → `p:eq:zext` | §5.2 | none
```
z_{\rm ext}^{\rm burst}
=\frac{a(1-q+qb)-1+q}{q}
=\frac{a-1}{q}+1-a(1-b).
```

**EQ-042** (unlabelled, 05:69–71) → `p:eq:zextbud` | §5.3 | none
```
z_{\rm ext}^{\rm bud}=\frac{1}{m}\qquad(m>1).
```

**EQ-043** (`eq:flood`, 05:76–80) → `p:eq:flood` | §5.3 (Thm) | none
```
z_{\rm ext}^{\rm burst}-z_{\rm ext}^{\rm bud}
=\bigl(L-1\bigr)\Bigl(\frac{1}{m}-1\Bigr).
```

**EQ-044** (unlabelled, 05:83–87) → `p:eq:floodcrit` | §5.3 (Thm) | none
```
\delta(\lambda+\mu)>\lambda\mu
\qquad\Longleftrightarrow\qquad
\boxed{\;\frac{1}{\delta}<\frac{1}{\lambda}+\frac{1}{\mu}\;}
```

**EQ-045** (unlabelled, 05:184–192) → `p:eq:L1equiv` | §5.4 (Prop) | none
```
L=1
\;\Longleftrightarrow\;
a=1+\frac{\mu}{\lambda}
\;\Longleftrightarrow\;
\delta(\lambda+\mu)=\lambda\mu
\;\Longleftrightarrow\;
\frac{1}{\delta}=\frac{1}{\lambda}+\frac{1}{\mu}.
```

**EQ-046** (`eq:varorder`, 05:197–201) → `p:eq:varorder` | §5.4 (Prop) | none
```
\mathrm{Var}_{\rm bud}-\mathrm{Var}_{\rm burst}
=\frac{2q^2V_\infty(L-1)}{a-1},
```

**EQ-047** (proof body, 05:210–225) → in proof of `p:prop:L1` | **P3** (`r`→`\varrho`)
```
G_{\rm off}(z)=b\Bigl(1+\frac{y}{a-y}\Bigr)=\frac{ab}{a-y}
=\frac{a-1}{a-y}
=\frac{(a-1)/a}{1-y/a},
1-\frac{y}{a}=\frac{a-1+q}{a}\Bigl(1-\frac{q}{a-1+q}\,z\Bigr),
G_{\rm off}(z)=\frac{1-r}{1-rz},
\qquad
r=\frac{q}{a-1+q}=\frac{m}{1+m},
\qquad m=\frac{q}{a-1}=qV_\infty,
```
→ last line becomes `G_{\rm off}(z)=\frac{1-\varrho}{1-\varrho z}, \varrho=\frac{q}{a-1+q}=\frac{m}{1+m}`.

**EQ-048** (unlabelled, 05:249–251) → `p:eq:rorder` | §5.5 | none
```
r_{\rm bud}>r_{\rm burst}.
```

### From `06_spectrum_of_release_models.tex`

**EQ-049** (`eq:skeleton`, 06:67–72) → `p:eq:skeleton` | §3.3 | none
```
\Icell(t)=\Icell_0\,S(t)+(i*S)(t),
\qquad
\ddt{\Vfree}=\Icell_0\,g(t)+(i*g)(t)-c\,\Vfree(t),
```
with `p_{\rm eff}(r)=\Lap{g}(r)/\Lap{S}(r)` and `R_0=(\gamma T/c)\int_0^\infty g`.

**EQ-050** (Case 1, 06:115–121) → `p:eq:case1` | §6.1 | none
```
\ddt{\Icell}=\gamma T\,\Vfree-d_{\Icell}\Icell,
\qquad
\ddt{\Vfree}=p\,\Icell-c\,\Vfree,
\qquad
R_0=\frac{\gamma T\,p}{c\,d_{\Icell}}.
```

**EQ-051** (Case 2, 06:130–139) → `p:eq:case2`, `p:eq:case2R0` | §6.1 | **P2** (`\alpha`→`\omega`)
```
\ddt{E}=\gamma T\,\Vfree-(\alpha+d_E)E,
\qquad
\ddt{\Icell}=\alpha E-d_{\Icell}\Icell,
\qquad
\ddt{\Vfree}=p\,\Icell-c\,\Vfree,
R_0=\frac{\gamma T}{c}\cdot\frac{\alpha}{\alpha+d_E}\cdot\frac{p}{d_{\Icell}}.
```

**EQ-052** (Case 3, 06:154–160) → `p:eq:case3` | §6.1 | none
```
\ddt{\Icell}=\gamma T\,\Vfree-d_{\Icell}\Icell,
\qquad
\ddt{Q}=\nu\Icell-\varepsilon Q-d_{\Icell}Q,
\qquad
\ddt{\Vfree}=\varepsilon Q-c\,\Vfree.
```

**EQ-053** (Case 3 QSS, 06:163–168) → `p:eq:case3qss` | §6.1 | **P5** (`m`→`\bar x` in surrounding prose)
```
Q_*=\frac{\nu}{\varepsilon+d_{\Icell}}\,\Icell,
\qquad
p_{\mathrm{eff}}:=\frac{\varepsilon Q_*}{\Icell}
=\frac{\varepsilon\nu}{\varepsilon+d_{\Icell}},
```

**EQ-054** (Case 3 R0, 06:175–178) → `p:eq:case3R0` | §6.1 | none
```
R_0=\frac{\gamma T\,\nu\,\varepsilon}{c\,d_{\Icell}(\varepsilon+d_{\Icell})}
```

**EQ-055** (Case 4, 06:189–195) → `p:eq:case4` | §6.1 | none
```
\ddt{\Icell}=\gamma T\,\Vfree-d_{\Icell}\Icell,
\qquad
\ddt{Q}=\nu\Icell-\delta\frac{Q^2}{\Icell}-d_{\Icell}Q,
\qquad
\ddt{\Vfree}=\delta\frac{Q^2}{\Icell}-c\,\Vfree,
```

**EQ-056** (Case 4 QSS, 06:202–206) → `p:eq:case4qss` | §6.1 | **P5** (`m`→`\bar x`)
```
m=\frac{-d_{\Icell}+\sqrt{d_{\Icell}^2+4\delta\nu}}{2\delta},
\qquad
p_{\mathrm{eff}}=\delta m^2,
```
→ `\bar x=\frac{-d_{\Icell}+\sqrt{d_{\Icell}^2+4\delta\nu}}{2\delta}, \quad p_{\mathrm{eff}}=\delta\bar x^2`.
Balance relation `\nu=\delta m^2+d_{\Icell}m` → `\nu=\delta\bar x^2+d_{\Icell}\bar x`.

**EQ-057** (Case 5, 06:217–226) → `p:eq:case5` | §6.1 | **P2**
```
\ddt{E}=\gamma T\,\Vfree-(\alpha+d_E)E,
\qquad
\ddt{\Icell}=\alpha E-d_{\Icell}\Icell,
\ddt{Q}=\nu\Icell-\delta\frac{Q^2}{\Icell}-d_{\Icell}Q,
\qquad
\ddt{\Vfree}=\delta\frac{Q^2}{\Icell}-c\,\Vfree.
```

**EQ-058** (Case 5 R0, 06:231–233) → `p:eq:case5R0` | §6.1 | **P2**
```
R_0=\frac{\gamma T}{c}\cdot\frac{\alpha}{\alpha+d_E}\cdot V_\infty.
```

**EQ-059** (reset kernels, 06:274–278) → `p:eq:reset-kernels` | §6.2 | **P1**
```
S(a)=e^{-d_{\Icell}a},
\qquad
g(a)=\delta\,e^{-d_{\Icell}a}\,\mean{X_a^2},
```

**EQ-060** (reset peff, 06:284–288) → `p:eq:reset-peff` | §6.2 | none
```
p_{\rm eff}(r)=\lrb{r+d_{\Icell}}\Lap{g}(r),
\qquad
d_{\Icell,{\rm eff}}\equiv d_{\Icell},
```

**EQ-061** (reset mature limit, 06:292–295) → `p:eq:reset-mature` | §6.2 | **P1**
```
p_\infty=\lim_{a\to\infty}\frac{g(a)}{S(a)}=\delta\,\mean_\pi[X^2]:
```

**EQ-062** (Model 6 ODEs, 06:376–385) → `p:eq:model6` | App E | none
```
\ddt{I_{\rm OFF}}=\gamma T\,\Vfree+\sigma_{\rm off}I_{\rm ON}
-(\sigma_{\rm on}+d_{\Icell})I_{\rm OFF},
\ddt{I_{\rm ON}}=\sigma_{\rm on}I_{\rm OFF}
-(\sigma_{\rm off}+d_{\Icell})I_{\rm ON},
\qquad
\ddt{\Vfree}=\rho\,I_{\rm ON}-c\,\Vfree,
```
duty cycle `p_{\rm eff}=\rho\,\sigma_{\rm on}/(\sigma_{\rm on}+\sigma_{\rm off})`.

**EQ-063** (Model 10 intensity, 06:391–400, inline) → App E | **P4**
```
\dd r=-\zeta(r-r_0)\dd t+\eta\,\dd N_t
```
→ `\dd\psi=-\zeta(\psi-\psi_0)\dd t+\eta\,\dd N_t`; `R=\sum r_i`, `\bar r=R/\Icell`,
flux `\approx\bar r Q` → `\Psi=\sum\psi_i`, `\bar\psi=\Psi/\Icell`, flux `\approx\bar\psi Q`.

**EQ-064** (Model 2 intensity, inline 06:355, 06:403) → App E | none
```
\lambda(t)=f(X_t)+\sum_{t_i<t}h(t-t_i)
```

**EQ-065** (partial release, 06:482–488) → `p:eq:partial` | §6.3 | none
```
\ddt{\Icell}=\gamma T\,\Vfree-d_{\Icell}\Icell,
\qquad
\ddt{Q}=\nu\Icell-\delta\varphi\,\frac{Q^2}{\Icell}-d_{\Icell}Q,
\qquad
\ddt{\Vfree}=\delta\varphi\,\frac{Q^2}{\Icell}-c\,\Vfree.
```

### From `07_hiv_contrast.tex`

**EQ-066** (pathways, 07:126–137) → `p:eq:hiv-paths` | §6.5 | **P2** (Erlang step rate `\alpha`→`\omega`)
```
L_0\xrightarrow{\alpha_A}E_1^{(A)},
\qquad
L_0\xrightarrow{\alpha_B}E^{(B)},
E_j^{(A)}\xrightarrow{\alpha}E_{j+1}^{(A)}\ (j=1,\dots,n-1),
\qquad
E_n^{(A)}\xrightarrow{\alpha}I^{(A)},
\qquad
E^{(B)}\xrightarrow{\alpha_B}I^{(B)}.
```
(`\alpha_A`, `\alpha_B` are pathway conversion rates and are **kept**; only the bare
Erlang step rate `\alpha` becomes `\omega`.)

**EQ-067** (eclipse events, 07:184–188) → `p:eq:hiv-eclipse-events` | §6.5 | none
```
E\xrightarrow{\rho_{\rm div}}E+E,
\qquad
E\xrightarrow{\mu_E}\varnothing,
```

**EQ-068** (productive events, 07:191–199) → `p:eq:hiv-prod-events` | §6.5 | none
```
I^{(A)}\xrightarrow{p_A}I^{(A)}+\Vfree,
\qquad
I^{(A)}\xrightarrow{\delta_I}\varnothing,
\qquad
I^{(B)}\xrightarrow{p_B}I^{(B)}+\Vfree,
\qquad
I^{(B)}\xrightarrow{\delta_I}\varnothing,
```

**EQ-069** (stage ODEs, 07:204–217) → `p:eq:hiv-stage-odes` | §6.5 | **P2**, **P6**, and the §10.1 **correction**
```
\ddt{E_1}=\alpha_A L_0\,\delta_0(t)+\rho_{\rm div}E_1
-(\mu_E+\rho_{\rm div}+\alpha)E_1,
\ddt{E_j}=\alpha E_{j-1}+\rho_{\rm div}E_j
-(\mu_E+\rho_{\rm div}+\alpha)E_j,\quad j=2,\dots,n,
\ddt{I^{(A)}}=\alpha E_n-\delta_I I^{(A)},
\qquad
\ddt{\Vfree}=p_A I^{(A)}-c\,\Vfree
\quad(+\,p_B I^{(B)}),
```
**LICENSED CORRECTION (plan §10.1).** The `\rho_{\rm div}` terms cancel
identically as printed. Corrected to
`\ddt{E_j}=\omega E_{j-1}+\rho_{\rm div}E_j-(\mu_E+\omega)E_j`,
with the Dirac source replaced by the initial condition `E_1(0)=\alpha_A L_0`.
This is the one permitted equation-level correction in the chapter; recorded
in `CH6_figure_workorder.md` as an author-confirm item.

**EQ-070** (incidence split, 07:221–227) → `p:eq:hiv-incidence` | §6.5 | none
```
i(t)=f\bigl(\Vfree(t),T\bigr),
\qquad
\text{source into }E_1^{(A)}=\pi_A i(t),
\qquad
\text{source into }E^{(B)}=\pi_B i(t).
```

**EQ-071** (Allee incidence, 07:233–235) → `p:eq:allee` | §6.5 | none
```
f(\Vfree,T)=\gamma T\,\Vfree\cdot\frac{\Vfree}{K_A+\Vfree},
```

**EQ-072** (HIV renewal, 07:249–253) → `p:eq:hiv-renewal` | §6.5 | none
```
\Icell(t)=\Icell_0S_{\rm HIV}(t)+(i*S_{\rm HIV})(t),
\qquad
\ddt{\Vfree}=\Icell_0g_{\rm HIV}(t)+(i*g_{\rm HIV})(t)-c\,\Vfree(t).
```

**EQ-073** (HIV effective params, 07:261–266) → `p:eq:hiv-peff` | §6.5 | none
```
p_{\rm eff}(r)=\frac{\Lap{g}_{\rm HIV}(r)}{\Lap{S}_{\rm HIV}(r)},
\qquad
R_0=\frac{\gamma T}{c}\int_0^\infty g_{\rm HIV}(a)\,\dd a
\quad\text{(linear incidence)},
```
(the `a` here is an integration variable of age → **P1**, `\alpha`.)

**EQ-074** (coarse regime, 07:334–337) → §6.5 prose | none
```
\textbf{eclipse}\ \longrightarrow\
\textbf{mean-linear (immigration-type) accumulation of }X,
```

### From `C_technical_derivations.tex`

**EQ-075** (`eq:LIhat`, C:28–35) → `p:eq:LIhat` | App D | none
```
\Lap{\Ifix}(r)=\frac{1}{\lambda(s+1)}
\Biggl[
\Psi(A,B,s)
+\frac{b}{a}\,\Fhyp\Bigl(1,s+1;s+2;\frac{b}{a}\Bigr)
\Biggr],
```

**EQ-076** (`\Psi` cases, C:37–43) → `p:eq:Psi` | App D | none
```
\Psi(A,B,s)=
\begin{cases}
\Fhyp\bigl(1,s+1;s+2;-\frac{A}{B}\bigr), & B\ge A,\\[0.4em]
\frac{B}{A}\,\Fhyp\bigl(1,s+1;s+2;-\frac{B}{A}\bigr), & A>B,
\end{cases}
```

**EQ-077** (`eq:dLK`, C:52–60) → `p:eq:dLK` | App D | none
```
\delta\Lap{K}(r)=\frac{\delta}{\lambda}
\Biggl[
\frac{\Fhyp(1,s;s+2;z)}{A(s+1)}
+\frac{2\,\Fhyp(2,s;s+3;z)}{A^2(s+1)(s+2)}
\Biggr],
\qquad z=-\frac{B}{A},
```
plus the unnumbered display of `\Ifix(t)` and of `\Lap{\Ifix}(r)` in the
`v`-substitution (C:15–22), and the partial-fraction identity
`(a-b)/[(A+Bv)(a-bv)]=B/(A+Bv)+b/(a-bv)`.

### Licensed addition (plan §9) — NOT a ledger entry to be checked against source

**EQ-NEW-01** → `p:eq:genkernel` | §4.2 | licensed by plan §9
```
\mathcal A(\alpha)=\gamma T\,(g*\ee^{-c\,\cdot})(\alpha)
=\gamma T\int_0^\alpha g(u)\,\ee^{-c(\alpha-u)}\,\dd u
```
**EQ-NEW-02** → `p:eq:Atilde` | §4.2 | `\Lap{\mathcal A}(r)=\gamma T\,\Lap{g}(r)/(r+c)`,
so `p:eq:char` is `\Lap{\mathcal A}(r)=1` (Euler–Lotka).
**EQ-NEW-03** → `p:eq:R0gen` | §4.2 | `R_0=\int_0^\infty\mathcal A=\gamma TV_\infty/c`;
the generation-time density is `\mathcal A(\alpha)/R_0`.

> **Symbol note (deviation from plan §9).** The plan writes the generation
> kernel `A(\alpha)`. In this chapter `A=a-1` is a *frozen* derived constant
> (EQ-002) appearing in EQ-003, EQ-023, EQ-075 and EQ-077, so a bare `A` would
> reintroduce exactly the kind of collision plan §6 exists to remove. The
> kernel is therefore written **`\mathcal A(\alpha)`**, consistent with the
> calligraphic population objects `\Icell`, `\Vfree`, `\Kb`.

---

## B. Theorem / proposition / remark statements and proofs

| ID | Old | New label | Status | Rule |
|---|---|---|---|---|
| **TH-001** | `theorem` "New viral dynamics — burst-aware BMVR", `res:new-vde` (03:109–122) | `p:def:renewal-system` | **environment converted to `definition`, plan §4.3**; equations EQ-026/EQ-027 verbatim; one sentence added on status + `% HOOK-MATHS` | statement content frozen |
| **TH-002** | `theorem` "$R_0$ is unchanged by bursting", `thm:R0inv` (04:108–115) | `p:thm:R0inv` | statement **verbatim**; **proof added** (plan §4.4, one line from the generation kernel) | statement frozen |
| **TH-003** | `theorem` "The flooding advantage", `thm:flood` (05:73–91) | `p:thm:flood` | statement verbatim, incl. EQ-043, EQ-044 and the `L:=a(1-b)=a-\mu/\lambda`, `V_\infty=L/(a-1)` preamble | frozen |
| **PF-001** | `\begin{proof}[Proof sketch]` of `thm:flood` (05:93–100) | proof of `p:thm:flood` | **verbatim, including the "Proof sketch" label** (plan §3.1) | frozen |
| **TH-004** | `proposition` `prop:L1` (05:181–204) | `p:prop:L1` | statement verbatim, incl. EQ-045, EQ-046 | frozen |
| **PF-002** | `\begin{proof}` of `prop:L1` (05:206–230) | proof of `p:prop:L1` | verbatim **modulo P3** (`r`→`\varrho`) | P3 only |
| **RM-001** | `remark` "What is and is not new", `rem:novelty` (03:162–172) | `p:rem:novelty` | **rewritten** per plan §4.1/§0.1.3 dev. 4 and §8.4: two confident sentences, `nelson2004agestructured` engaged head-on, "Any honest write-up must say so plainly" deleted | content, not wording, frozen |
| **RM-002** | `remark` "Scope of the comparison" (05:346–353) | `p:rem:flood-scope` | scope content moves to §7.3 Limitations; remark retained in §5 in shortened form | content frozen |

---

## C. Numeric values

Every number below must appear unchanged, in the place named.

| ID | Value | Where it appears |
|---|---|---|
| NUM-001 | `4.59` | $p_{\rm eff}(0)$ at $(1,0,0.1)$ — §4.1 body |
| NUM-002 | `0.1` | $p_{\rm eff}(\infty)=\delta$ at $(1,0,0.1)$ — §4.1 body |
| NUM-003 | `0.417` | $d_{\Icell}$ at $(1,0,0.1)$ — §5.5 table |
| NUM-004 | `0.250` / `0.180` | $r_{\rm bud}$ / $r_{\rm burst}$ at $(1,0,0.1)$ — §5.5 table, `N4b_6` caption |
| NUM-005 | `0.910`, `0.395`, `0.294` | $d_{\Icell}$, $r_{\rm bud}$, $r_{\rm burst}$ at $(1,0.5,1/3)$ — §5.5 table |
| NUM-006 | `0.701`, `0.343`, `0.198` | $d_{\Icell}$, $r_{\rm bud}$, $r_{\rm burst}$ at $(1,0.9,0.1)$ — §5.5 table |
| NUM-007 | `3.398` = `2.398+1` | budding mean generation time — `N4b_6` caption, §4.2 derivation |
| NUM-008 | `4.089` = `3.089+1` | bursting mean generation time — `N4b_6` caption, §4.2 derivation |
| NUM-009 | `2.398` | $\mean{T_{\rm prod}}$ at $(1,0,0.1)$ — `N4b_1` caption |
| NUM-010 | `1.10`, `1.00`, `0.42` | $L$ for the canonical trio — §2.5, §3.1 caption, §5 tables, `N4b_4`/`F4b_2`/`F4b_3` captions |
| NUM-011 | `11.00`, `2.00`, `1.32` | $V_\infty$ for the canonical trio — `N4b_7` caption |
| NUM-012 | `11` | $V_\infty$ at $(1,0,0.1)$ — `N4b_1` caption |
| NUM-013 | `54` | verification checks — §3.4, App C |
| NUM-014 | `5\times10^{-5}` | exponential-reduction relative error — §3.4, App C, `D_exponential_reduction` caption |
| NUM-015 | `10^{-7}` (and `10^{-6}`) | growth-rate match — §3.4, §4.4, App C, `EF` caption |
| NUM-016 | `1`–`2\%` | Gillespie relative $L^2$ — §3.4, App C, `H_gillespie` caption |
| NUM-017 | `1.05` | $R_0$ at which the threshold is resolved — §4.4 |
| NUM-018 | `0.400`, `0.455`, `0.935`, `0.844`, `0.833`, `0.833`, `0.556`, `0.556` | flooding table $z_{\rm ext}$ — §5.3 |
| NUM-019 | `0.2`, `0.9`, `0.6`, `0.9` | flooding table $q$ column — §5.3 |
| NUM-020 | `2` | matched $R_0$ in §5.5 and in `N4b_2` caption |
| NUM-021 | `1` | $c=1$, $\gamma T=1$ throughout §5.5, `N4b_2`, `N4b_5` |
| NUM-022 | `0.294` | $r_\star$ in `N4b_2` caption |
| NUM-023 | `0.03` to `0.8` | $\delta$ sweep in `N4b_5` caption |
| NUM-024 | `0.5/`day | $\rho_{\rm div}\approx\mu_E$ — §6.5 |
| NUM-025 | `0.41` | $f_{\rm HIV}$ — §6.5 |
| NUM-026 | `2.3` | critical $\Lambda$ — §6.5 |
| NUM-027 | `5100` | detected HIV RNA copies at threshold — §6.5 |
| NUM-028 | `2\times10^5` | establishment definition — §6.5 |
| NUM-029 | `2\%` | establishment from one cell — §6.5 |
| NUM-030 | `\sim5\times10^3` | RNA copies at inflection — §6.5 (twice) |
| NUM-031 | `\approx5` | favoured eclipse stages $n$ — §6.5 |
| NUM-032 | day `3`, days `3`–`5`, day `1` | Hataye release timing — §6.5 |
| NUM-033 | `10^{-8}` | App D quadrature check |
| NUM-034 | `10^{-6}` | App C tests J |
| NUM-035 | test tallies `5/5, 15/15, 5/5, 3/3, 5/5, 8/8, 4/4, 2/2, 1/1, 5/5, 1/1`, total `54/54` | App C table |
| NUM-036 | `\{0.5,\ldots,3\}` | App C test F range |
| NUM-037 | `26`–`28^\circ`C / `37^\circ`C | §7.3 limitations (drawn from the two-type biology document) |

## D. Parameter triples

| ID | Triple | Role |
|---|---|---|
| PAR-001 | `(1,0,0.1)` | canonical regime $L>1$ |
| PAR-002 | `(1,0.5,1/3)` | canonical regime $L=1$ |
| PAR-003 | `(1,0.9,0.1)` | canonical regime $L<1$ |
| PAR-004 | `(1,0.2,0.05)` | verification suite only (App C) |
| PAR-005 | `(1,0,0.5)` | verification suite only (App C) |

## E. Table data cells (headers and captions may be rewritten; cells may not)

| ID | Table | Source |
|---|---|---|
| TAB-001 | population notation table | 01:186–204 (extended per plan §6) |
| TAB-002 | classical / renewal correspondence | 03:126–142 |
| TAB-003 | flooding numerical table (4 rows) | 05:116–128 |
| TAB-004 | growth-rate trade-off table (3 rows) | 05:253–264 |
| TAB-005 | $(S,g)$ model table (6 rows) | 06:76–91 |
| TAB-006 | five-case summary (5 rows) | 06:237–251 |
| TAB-007 | absorbing vs reset comparison (6 rows) | 06:301–316 |
| TAB-008 | 12-model self-excitation menu | 06:333–354 → App E |
| TAB-009 | four-model comparison (6 rows) | 06:411–426 → App E |
| TAB-010 | boolean nested limits (4 rows) | 06:466–479 → App E |
| TAB-011 | HIV supported / not supported (5 rows) | 07:80–94 |
| TAB-012 | lytic BDC vs HIV (7 rows) | 07:99–115 |
| TAB-013 | mean-exponential vs mean-linear (2 rows) | 07:295–306 |
| TAB-014 | master formula table (19 rows) | `A_formula_tables.tex` |
| TAB-015 | verification catalogue (11 rows + total) | `B_verification_records.tex` |
| TAB-016 | derived quantities for the canonical trio | **new**, assembled from frozen numbers only (§2.5) |

## F. Figures — `\includegraphics` targets

Unchanged file names; `figures/` prefix stripped once `\graphicspath` is set.

| File | Old label | New label | Disposition |
|---|---|---|---|
| `NX_1_trilogy_handoff.pdf` | `fig:NX_1_trilogy_handoff` | `p:fig:handoff` | App A |
| `N4b_1_constant_release_fails.pdf` | `fig:N4b_1` | `p:fig:constant-fails` | §2.2 |
| `kernels.pdf` | `fig:kernels` | — | **DROPPED** (plan §11.2) |
| `N4b_7_kernels_three_regimes.pdf` | `fig:N4b_7` | `p:fig:kernels` | §3.1 |
| `F4b_1_renewal_schematic.pdf` | `fig:F4b_1_renewal_schematic` | `p:fig:renewal-schematic` | §3.2 |
| `D_exponential_reduction.pdf` | `fig:D-exp` | `p:fig:D-exp` | **App C** |
| `H_gillespie_mu0.pdf`, `H_gillespie_mu_pos.pdf` | `fig:H-gill` | `p:fig:gillespie` | §3.4 |
| `overlay_V.pdf` | `fig:overlay-V` | `p:fig:overlay-V` | §4.3 |
| `overlay_I.pdf` | `fig:overlay-I` | `p:fig:overlay-I` | §4.3 |
| `overlay_V_with_naive.pdf` | `fig:overlay-V-naive` | `p:fig:overlay-naive` | §4.3 |
| `overlay_rel_diff.pdf` | `fig:rel-diff` | `p:fig:rel-diff` | §4.3 |
| `overlay_growth_phase.pdf` | `fig:growth-phase` | `p:fig:growth-phase` | §4.3 |
| `peff_dr_curves.pdf` | `fig:peff-curves` | `p:fig:peff` | §4.1 |
| `E_growth_rate_match.pdf` | `fig:E-growth` | `p:fig:E-growth` | **App C** |
| `F_R0_threshold.pdf` | `fig:F-R0` | `p:fig:F-R0` | **App C** |
| (subfig pair) | `fig:EF` | `p:fig:EF` | App C |
| `N4b_2_identifiability_levels.pdf` | `fig:N4b_2` | `p:fig:identifiability` | §4.5 |
| `N4b_4_L_landscape.pdf` | `fig:N4b_4` | `p:fig:L-landscape` | §5.3 |
| `F4b_2_flooding_regimes.pdf` | `fig:F4b_2_flooding_regimes` | `p:fig:flooding-regimes` | §5.3 |
| `F4b_3_growth_tradeoff.pdf` | `fig:F4b_3_growth_tradeoff` | `p:fig:growth-tradeoff` | §5.5 |
| `N4b_6_generation_times.pdf` | `fig:N4b_6` | `p:fig:generation-times` | §5.5 |
| `N4b_5_pareto_extinction_growth.pdf` | `fig:N4b_5` | `p:fig:pareto` | §5.5 |
| `N4b_3_release_spectrum.pdf` | `fig:N4b_3_release_spectrum` | — | **DROPPED** (plan §11.2) |
| inline TikZ spectrum | `fig:spectrum-map` | `p:fig:spectrum` | §6 opening; label collision repaired (plan §11.4) |
| inline TikZ HIV stages | `fig:hiv-stages` | `p:fig:hiv-stages` | §6.5; `\alpha`→`\omega` (P2) |

## G. Label map (old → new), complete

| Old | New |
|---|---|
| `sec:needed` | → App A `p:app:quoted` (+ core moved to `p:sec:introduction`) |
| `sec:needed-roots` | `p:sec:quoted-results` (in §1.4) |
| `eq:AB` | `p:eq:AB` |
| `eq:IDIhat` | `p:eq:IDIhat` |
| `eq:J` | `p:eq:J` |
| `eq:K` | `p:eq:K` |
| `eq:V` | `p:eq:V` |
| `eq:Vinf` | `p:eq:Vinf` |
| `eq:phi` | `p:eq:bursttime` |
| `eq:burstlaw` | `p:eq:burstlaw` |
| `eq:sizebias` | `p:eq:sizebias` |
| `eq:EW2` | `p:eq:EW2` |
| `prop:lifetime` | `p:eq:lifetime` |
| `eq:gk` | `p:eq:gk` |
| `eq:Vk` | `p:eq:Vk` |
| `tab:notation-pop` | `p:tab:notation` |
| `fig:NX_1_trilogy_handoff` | `p:fig:handoff` |
| `sec:why-constant-fails` | `p:sec:comparator` |
| `sec:bmvr-classical` | `p:sec:classical` |
| `eq:BMVR-classical` | `p:eq:bmvr-classical` |
| `eq:bud-cell` | `p:eq:bud-cell` |
| `sec:sync-cohort` | `p:sec:cohort` |
| `fig:N4b_1` | `p:fig:constant-fails` |
| `sec:proposal-fails` | `p:sec:obstruction` |
| `eq:naive-p` | `p:eq:naive-p` |
| `sec:attempt-right` | `p:sec:survives` |
| `sec:renewal` | `p:sec:renewal` |
| `eq:Skernel` | `p:eq:Skernel` |
| `eq:gkernel` | `p:eq:gkernel` |
| `fig:kernels` | *(dropped)* |
| `fig:N4b_7` | `p:fig:kernels` |
| `fig:F4b_1_renewal_schematic` | `p:fig:renewal-schematic` |
| `res:new-vde` | `p:def:renewal-system` |
| `eq:Icell` | `p:eq:Icell` |
| `eq:Vfree` | `p:eq:Vfree` |
| `rem:novelty` | `p:rem:novelty` |
| `sec:renewal-verification` | `p:sec:verification` |
| `fig:D-exp` | `p:fig:D-exp` |
| `fig:H-gill` | `p:fig:gillespie` |
| `sec:overlays` | `p:sec:overlays` |
| `eq:r0match` | `p:eq:r0match` |
| `fig:overlay-V` | `p:fig:overlay-V` |
| `fig:overlay-I` | `p:fig:overlay-I` |
| `fig:overlay-V-naive` | `p:fig:overlay-naive` |
| `fig:rel-diff` | `p:fig:rel-diff` |
| `fig:growth-phase` | `p:fig:growth-phase` |
| `sec:peff-section` | `p:sec:projection` |
| `eq:peff` | `p:eq:peff` |
| `eq:char` | `p:eq:char` |
| `eq:peff0` | `p:eq:peff0` |
| `eq:peffinf` | `p:eq:peffinf` |
| `fig:peff-curves` | `p:fig:peff` |
| `eq:R0ODE` | `p:eq:R0ODE` |
| `thm:R0inv` | `p:thm:R0inv` |
| `fig:E-growth` | `p:fig:E-growth` |
| `fig:F-R0` | `p:fig:F-R0` |
| `fig:EF` | `p:fig:EF` |
| `sec:identifiability` | `p:sec:identifiability` |
| `fig:N4b_2` | `p:fig:identifiability` |
| `sec:flooding` | `p:sec:flooding` |
| `eq:Goff` | `p:eq:Goff` |
| `eq:offmoments` | `p:eq:offmoments` |
| `eq:zext` | `p:eq:zext` |
| `thm:flood` | `p:thm:flood` |
| `eq:flood` | `p:eq:flood` |
| `fig:N4b_4` | `p:fig:L-landscape` |
| `fig:F4b_2_flooding_regimes` | `p:fig:flooding-regimes` |
| `prop:L1` | `p:prop:L1` |
| `eq:varorder` | `p:eq:varorder` |
| `sec:r-tradeoff` | `p:sec:tradeoff` |
| `fig:F4b_3_growth_tradeoff` | `p:fig:growth-tradeoff` |
| `fig:N4b_6` | `p:fig:generation-times` |
| `fig:N4b_5` | `p:fig:pareto` |
| `sec:spectrum` | `p:sec:reach` |
| `fig:spectrum-map` | `p:fig:spectrum` |
| `fig:N4b_3_release_spectrum` | *(dropped)* |
| `sec:skeleton` | `p:sec:generality` (promoted into §3.3) |
| `eq:skeleton` | `p:eq:skeleton` |
| `sec:five-cases` | `p:sec:odecases` |
| `sec:reset` | `p:sec:reset` |
| `sec:self-excite` | `p:sec:selfexcite` |
| `sec:boolean` | `p:sec:partial` |
| `sec:hiv` | `p:sec:hiv` |
| `sec:hiv-eqns` | `p:sec:hiv` (merged) |
| `fig:hiv-stages` | `p:fig:hiv-stages` |
| `sec:hiv-growth` | `p:sec:hiv` (merged) |
| `sec:discussion` | `p:sec:discussion` |
| `sec:discussion-fitting` | `p:sec:fitting-consequences` |
| `sec:discussion-forward` | `p:sec:forward` |
| `sec:open-problems` | `p:sec:open-problems` |
| `app:formula-tables` | `p:app:formulae` |
| `app:verification` | `p:app:verification` |
| `app:technical` | `p:app:technical` |
| `app:transforms` | `p:app:transforms` |
| `eq:LIhat` | `p:eq:LIhat` |
| `eq:dLK` | `p:eq:dLK` |
| *(new)* | `p:ch:one-cell-to-population`, `p:sec:introduction`, `p:sec:assumptions`, `p:app:quoted`, `p:app:catalogue`, `p:eq:genkernel`, `p:eq:Atilde`, `p:eq:gentime`, `p:sec:limitations`, `p:sec:generation-kernel`, `p:tab:trio`, and the `p:tab:*` labels created by §12.2's tabular→table conversion |

## H. Deletions authorised by the plan

| Item | Authority |
|---|---|
| §7.5 "Suggested role of this material" | plan §4.6 |
| Open problem 5 (Carruthers check) | plan §10.3 — becomes an author action in the work-order |
| `kernels.pdf`, `N4b_3_release_spectrum.pdf` floats | plan §11.2 |
| both `\figureflag` blocks and the macro | plan §12.3 |
| dead macros `\xx \ww \zz \xt \wt \xs \xdt \eec \lrbq \pdxn \pdx \pt \p \delt \de` etc. | plan §12.3 |
| `\Figref \Eqref \Tabref \Chapref` | plan §7.3 |
| "Confidence: …" ratings, "The recommendation:", "The practical ranking:", "**Headline:**", four of five uses of *honest* | plan §13 |
| the three "this is not the other one" parentheticals | plan §6 |

---

## I. Verification gate — result (Phase A, post-compile)

Run against the written chapter, normalising whitespace and stripping comments.

| Class | Entries | Found | Verbatim | Altered (permitted) | Missing |
|---|---|---|---|---|---|
| Displayed equations | 73 | 73 | 60 | 13 | **0** |
| Theorem / proposition statements and proofs | 10 | 10 | 5 | 5 (`\eqref`→`\cref` only) | **0** |
| Numeric values | 61 | 61 | 61 | 0 | **0** |
| Parameter triples | 5 | 5 | 5 | 0 | **0** |
| Table data blocks | 13 | 13 | 8 | 5 | **0** |
| **Total** | **162** | **162** | **139** | **23** | **0** |

Every altered entry is a plan §6 substitution (P1–P5), the plan §10.1 licensed
correction, or the plan §7.3 reference-macro change. No entry was altered for
any other reason.

Altered entries, itemised:

| Entry | Substitution |
|---|---|
| EQ-019 | P1 — budding-cell age `t`→`\alpha` |
| EQ-023, EQ-024 | P1 — `S(a)`, `g(a)`, `\ee^{\theta a}` → `\alpha` |
| EQ-047 | P3 — geometric parameter `r`→`\varrho` inside the `prop:L1` proof |
| EQ-051a, EQ-051b, EQ-057, EQ-058 | P2 — eclipse conversion `\alpha`→`\omega` |
| EQ-056 | P5 — mean load `m`→`\bar x` |
| EQ-059, EQ-061 | P1, plus `e^`→`\ee^`; in EQ-061 the source's `\mean_\pi[X^2]` is invalid LaTeX (subscripted macro) and is set as `\mathbb{E}_\pi[X^2]` |
| EQ-073 | P1 — integration variable `a`→`\alpha` |
| EQ-069 | **plan §10.1 licensed correction** — the `\rho_{\rm div}` terms cancelled identically as printed; plus P2 and P6 |
| TAB-005, TAB-006, TAB-008, TAB-009, TAB-013 | P1, P4, P5, and `+`→`$+$` in table cells |
| PF-001, PF-002, TH-004 (3 fragments) | plan §7.3 — `\eqref{eq:X}` → `\cref{p:eq:X}` |

Boxing: the source `\boxed{...}` on EQ-003, EQ-004, EQ-005, EQ-006, EQ-007,
EQ-008, EQ-011, EQ-012, EQ-013, EQ-015 and EQ-016 was removed. The mathematics
inside each box is byte-identical; only the frame is gone, the boxes having been
a device of the reference card that §1.4 and Appendix A replace. Recorded here
as a presentational change, not a ledger alteration.
