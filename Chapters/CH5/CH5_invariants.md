# Chapter 5 — invariants ledger

Built before any prose was written, per plan §3. Every displayed equation,
every formal statement, every proof, every numeric value, every parameter
triple and every table cell of the source chapter appears below with its old
label, its new label, and its status.

**Status vocabulary.**

| Status | Meaning |
|---|---|
| `verbatim` | mathematics unchanged; label renamed; macro spelling may change (`\ee^{\lambda(a-b)t}` → `w`, `$$` → `\[`), which is typography, not content |
| `altered` | one of the **five permitted substitutions** (plan §15 item 3); no other alteration is permitted |
| `deferred` | removed from Chapter 5 and carried by a named label elsewhere; every deferral carries a `VERIFIED` line proving that label resolves |
| `moved` | same text, different section or appendix |
| `new` | one of the **three licensed additions** of plan §6, or an entry derived from them |
| `cut` | removed with nothing carrying it; only figures and build provenance are cut |

**The five permitted substitutions, and nothing else.**

1. `SUB-1` characteristic coordinate $\tau \to \xi$ (plan §4.3)
2. `SUB-2` Appendix C binomial constants $K_i \to C_i$ (plan §4.10)
3. `SUB-3` Appendix C Laplace product $P_1(m,u) \to \Pi(m,u)$ (plan §4.10)
4. `SUB-4` CH2 block: $T_0 \to T_{\rm fix}$, $\kappa_i \to \delta i$ (plan §6.3)
5. `SUB-5` CH2 block: killed subgenerator $K \to \mathcal Q$, decay rate $\theta \to \vartheta$ (plan §6.3)

Substitutions 4 and 5 apply **only** inside the absorbed Chapter 2 block; no
symbol of the source Chapter 5 is renamed by them.

---

## 0. Section map

| new § | title | source | new label |
|---|---|---|---|
| 1 | Introduction | §1 | `dist:sec:intro` |
| 2 | The process, its roots, and its closed forms | §2 | `dist:sec:recap` |
| 3 | The generating function | §3 + §4 | `dist:sec:pgf` |
| 4 | The load is geometric at every time | §5 | `dist:sec:geometric` |
| 5 | The quasi-stationary distribution | §6 + CH2 block | `dist:sec:qsd` |
| 6 | Burst size, and why it is the quasi-stationary law | §7.2–7.4 | `dist:sec:burst-size` |
| 7 | Burst time | §7.1, §7.5, §7.6 | `dist:sec:burst-time` |
| 8 | Conditional burst means | §8 | `dist:sec:cond-means` |
| 9 | Several founders | §9 | `dist:sec:moi` |
| 10 | Chained immediate transfer | §10 | `dist:sec:chained` |
| 11 | Bursting against budding | §7.7 | `dist:sec:budding` |
| 12 | Discussion | §11 | `dist:sec:discussion` |
| A | Master formula table | App. A | `dist:app:formulae` |
| B | Verification record | App. B + §10.7 | `dist:app:verification` |
| C | Technical derivations | App. C + §10.5–10.6 | `dist:app:technical` |

Subsection labels: `dist:sec:assumptions`, `dist:sec:contributions`,
`dist:sec:exports`, `dist:sec:notation-tab`, `dist:sec:process`,
`dist:sec:roots`, `dist:sec:fixation-funcs`, `dist:sec:moments-recap`,
`dist:sec:conventions`, `dist:sec:sum-ihat`, `dist:sec:qsd-geometric`,
`dist:sec:decay-rate`, `dist:sec:lifetime`, `dist:sec:burst-law`,
`dist:sec:identity`, `dist:sec:size-bias`, `dist:sec:tau-given-k`,
`dist:sec:tau-burst-mu-pos`, `dist:sec:circularity`,
`dist:sec:moi-fixation`, `dist:sec:moi-moments`, `dist:sec:moi-yield`,
`dist:sec:key-observation`, `dist:sec:rupture-sizes`,
`dist:sec:rupture-times`, `dist:sec:discussion-assay`,
`dist:sec:two-extremes`, `dist:sec:open-problems`, `dist:sec:next`,
`dist:app:vk`, `dist:app:extract`, `dist:app:chained-transforms`.

---

## 1. Displayed equations

### EQ-001  (roots and $\eta$, `02_recap_single_cell_bdc.tex:116`)
NEW LABEL   `dist:eq:roots`
STATUS      verbatim
TEXT        $\eta=\frac{\lambda+\mu+\delta}{2\lambda},\ a=\eta+\sqrt{\eta^2-\mu/\lambda},\ b=\eta-\sqrt{\eta^2-\mu/\lambda}$

### EQ-002  ($A$, $B$, $\theta$, `02:123`)
NEW LABEL   `dist:eq:abtheta`
STATUS      verbatim
TEXT        $A:=a-1>0,\ B:=1-b>0,\ \theta:=\lambda(a-b)=\sqrt{(\lambda+\mu+\delta)^2-4\lambda\mu}$

### EQ-003  (was `eq:AB`, `02:130`)
NEW LABEL   `dist:eq:ab`
STATUS      verbatim
TEXT        $AB=(a-1)(1-b)=(a+b)-ab-1=\delta/\lambda,\qquad A+B=a-b$

### EQ-004  (definitions of $I$, $D$, `02:145`)
NEW LABEL   `dist:eq:idefs`
STATUS      verbatim

### EQ-005  (definition of $\Ifix$, `02:149`)
NEW LABEL   `dist:eq:ifixdef`
STATUS      verbatim

### EQ-006  (was `eq:riccati`, `02:156`)
NEW LABEL   `dist:eq:riccati`
STATUS      verbatim
TEXT        $\ddt{I}=\lambda(I-a)(I-b)=\mu-(\lambda+\mu+\delta)I+\lambda I^2$

### EQ-007  (was `eq:IDIhat`, `02:164` — the boxed triplet)
NEW LABEL   `dist:eq:idihat`
STATUS      verbatim
TEXT        $I=\frac{aB+bAw}{B+Aw},\quad D=\frac{ab(w-1)}{aw-b},\quad \Ifix=\frac{(a-b)^2w}{(B+Aw)(aw-b)}$

### EQ-008  (was `eq:J`, `02:183`)
NEW LABEL   `dist:eq:j`
STATUS      verbatim
TEXT        $J=-\frac1\delta\ddt{I}=\frac{(a-b)^2w}{(B+Aw)^2}=-\frac\lambda\delta(I-a)(I-b)$

### EQ-009  (was `eq:K`, `02:190`)
NEW LABEL   `dist:eq:k`
STATUS      verbatim
TEXT        $K=[1+\tfrac{2\lambda}\delta(1-I)]J=\tfrac{2\lambda}\delta(\kappa-I)J,\ \kappa=1+\tfrac\delta{2\lambda}$

### EQ-010  ($V'=\delta K$, `02:203`)
NEW LABEL   `dist:eq:vflux`
STATUS      verbatim

### EQ-011  (was `eq:V`, `02:207`)
NEW LABEL   `dist:eq:v`
STATUS      verbatim
TEXT        $V(t)=(1-I)[1+\tfrac\lambda\delta(1-I)]$

### EQ-012  (was `eq:Vinf`, `02:216`)
NEW LABEL   `dist:eq:vinf`
STATUS      verbatim
TEXT        $V_\infty=\frac{a(1-b)}{a-1}=\frac{aB}{A}=\frac{\lambda-\mu}\delta(1-b)+1;\quad \mean{\Kb\mid\text{burst}}=\frac{V_\infty}{1-b}=\frac a{a-1}$

### EQ-013  (was `eq:EW2`, `02:246`)
NEW LABEL   `dist:eq:ew2`
STATUS      verbatim (formula); its **derivation** is deferred
CARRIED BY  \ChCore's variance section — `CH4/sections/08_variance_and_standard_deviation_of.tex`, `thm:Wsq` / `eq:Wsq` (lines 141–166), same result and same $\mu=0$ check
VERIFIED    `grep -n "label{thm:Wsq}\|label{eq:Wsq}" CH4/sections/08_variance_and_standard_deviation_of.tex` → lines 156, 159
NOTE        Chapter 4 is not yet on the `bdc:` prefix, so the pointer is prose
            through `\fwd`, not a `\cref`; no label is invented.

### EQ-014  (the $\mu=0$ check on $\E{W_\infty^2}$, `02:255`)
NEW LABEL   — (inline)
STATUS      verbatim
RECOMPUTED  $2\lambda^2/\delta^2+3\lambda/\delta+1=(2-s)/s^2=231.000000$ at $(1,0,0.1)$ ✓

### EQ-015  (was `catEq1`, `03:12`)
NEW LABEL   `dist:eq:catpde`
STATUS      verbatim
TEXT        $\pdx{G}{t}=(\lambda z^2-(\lambda+\mu+\delta)z+\mu)\pdx{G}{z}$

### EQ-016  (was `killEq1`, `03:19`)
NEW LABEL   `dist:eq:killpde`
STATUS      verbatim
TEXT        $\pdx{G}{t}=\delta J(t)+(\lambda z^2-(\lambda+\mu+\delta)z+\mu)\pdx{G}{z}$

### EQ-017  (forward Kolmogorov system, `03:39`)
NEW LABEL   `dist:eq:kolmogorov`
STATUS      verbatim ($$ → `equation`)

### EQ-018  (the catastrophe Kolmogorov system, `03:51`, prose)
NEW LABEL   `dist:eq:kolmogorovcat`
STATUS      verbatim (promoted from prose to a display; content unchanged)

### EQ-019  (was `stateFormula`, `04:11`)
NEW LABEL   —
STATUS      deferred to CH2
CARRIED BY  `m:eq:stateProb`, `m:app:extract`
VERIFIED    `grep -rl "label{m:eq:stateProb}" CH2/sections/` → `app_d_coefficient_extraction.tex`
            `grep -rl "label{m:app:extract}" CH2/sections/` → `app_d_coefficient_extraction.tex`

### EQ-020  (was `ICs`, the initial curve $z(s,0)=s$, $t(s,0)=0$, `04:25`)
NEW LABEL   —
STATUS      deferred to CH2
CARRIED BY  `m:sec:moc`, `m:eq:genericcharacteristics`
VERIFIED    `grep -rl "label{m:sec:moc}" CH2/sections/` → `04_method_of_characteristics.tex`

### EQ-021  (generic characteristic system $\dda{G}{\tau}=0$, $\dda t\tau=-1$, was `Char1`, `04:51`)
NEW LABEL   —
STATUS      deferred to CH2 (label `Char1` sat inside `align*` and labelled nothing — deleted, plan §4.3)
CARRIED BY  `m:eq:genericcharacteristics`, `m:fig:characteristics`
VERIFIED    `grep -rl "label{m:eq:genericcharacteristics}" CH2/sections/` → `04_method_of_characteristics.tex`
            `grep -rl "label{m:fig:characteristics}" CH2/sections/` → `04_method_of_characteristics.tex`

### EQ-022  (was `char3cat`, `04:66`)
NEW LABEL   `dist:eq:zchar`
STATUS      altered — **SUB-1**, $\tau\to\xi$
TEXT        $\dda z\xi=\lambda z^2-(\lambda+\mu+\delta)z+\mu$

### EQ-023  ($z(\xi)$ along a characteristic, `04:71`)
NEW LABEL   `dist:eq:zsolve`
STATUS      altered — **SUB-1**
TEXT        $z=\dfrac{a(s-b)-b(s-a)\ee^{\theta\xi}}{(s-b)-(s-a)\ee^{\theta\xi}}$

### EQ-024  (was `s2343`, `04:76`)
NEW LABEL   `dist:eq:sinv`
STATUS      verbatim ($\ee^{\lambda(a-b)t}$ written $w$, plan §12.3)
TEXT        $s=\dfrac{a(z-b)-b(z-a)w}{(z-b)-(z-a)w}$

### EQ-025  ($G_{\rm cat}$, first form, `04:81`)
NEW LABEL   `dist:eq:gcat`
STATUS      verbatim
TEXT        $G(z,t)=\dfrac{a(z-b)-b(z-a)w}{(z-b)-(z-a)w}$

### EQ-026  ($G_{\rm cat}$, extraction form, `04:85`)
NEW LABEL   `dist:eq:gcatextract`
STATUS      verbatim
TEXT        $G(z,t)=\dfrac{ab(1-w)-z(a-bw)}{(b-aw)-z(1-w)}$

### EQ-027  (killing characteristic system, was `Char2`, `04:101`)
NEW LABEL   — (dead label deleted; the parallel solve becomes a corollary of PROP-001)
STATUS      deferred to PROP-001 (licensed addition (a))
CARRIED BY  `dist:prop:conventions`

### EQ-028  ($G_{\rm kill}$, `04:125`)
NEW LABEL   `dist:eq:gkill`
STATUS      verbatim
TEXT        $G_{\rm kill}(z,t)=1-I(t)+\dfrac{ab(1-w)-z(a-bw)}{(b-aw)-z(1-w)}$

### EQ-029  (was `eq:Gk`, `04:135`)
NEW LABEL   `dist:eq:gk`
STATUS      verbatim
TEXT        $G_k(z,t)=(G(z,t))^k$

### EQ-030  ($G(0,t)$ under both conventions, `05:7`)
NEW LABEL   `dist:eq:pzero`
STATUS      verbatim ($$ → `equation`)

### EQ-031  ($\partial_z^nG$, `05:17`)
NEW LABEL   `dist:eq:dnG`
STATUS      verbatim ($$ → `equation`)

### EQ-032  (was `stateprob`, `05:20`)
NEW LABEL   `dist:eq:stateprob`
STATUS      verbatim
TEXT        $p_n(t)=\left(\frac{a-b}{b-aw}\right)^2 w\left(\frac{1-w}{b-aw}\right)^{n-1}$

### EQ-033  (was `eq:Pdef`, `05:29`)
NEW LABEL   `dist:eq:pdef`
STATUS      verbatim
TEXT        $P(t):=\dfrac{1-w}{b-aw}$

### EQ-034  ($p_n=p_1P^{n-1}$, `05:35`)
NEW LABEL   `dist:eq:geometric`
STATUS      verbatim; **promoted into THM-001**

### EQ-035  ($P(0)=0$, $P(\infty)=1/a$, `05:41`)
NEW LABEL   `dist:eq:plimits`
STATUS      verbatim; **promoted into THM-001**

### EQ-036  (geometric sum $\sum p_n=p_1/(1-P)$, `05:52`)
NEW LABEL   — (inline in the proof of COR-001)
STATUS      verbatim ($$ → `\[`)

### EQ-037  ($1-P$ rearranged, `05:57`)
NEW LABEL   — (inline in the proof of COR-001)
STATUS      verbatim ($$ → `\[`)

### EQ-038  (was `eq:pnsum`, `05:63`)
NEW LABEL   `dist:eq:pnsum`
STATUS      verbatim
TEXT        $\sum_{n\ge1}p_n(t)=\frac{(a-b)^2w}{(B+Aw)(aw-b)}=\Ifix(t)$

### EQ-039  ($F(t)=1-\Ifix$, `06:27`)
NEW LABEL   `dist:eq:fixprob`
STATUS      verbatim

### EQ-040  (conditional decomposition, `06:32`)
NEW LABEL   — (inline)
STATUS      verbatim ($$ → `\[`)

### EQ-041  (was `eq:condp`, `06:35`)
NEW LABEL   `dist:eq:condp`
STATUS      verbatim
TEXT        $\pr{\xt=i\mid\text{non-fixation}}=p_i(t)/\Ifix(t)$

### EQ-042  (definition of the QSD, `06:42`)
NEW LABEL   `dist:eq:qsddef`
STATUS      verbatim

### EQ-043  (conditional law $=(1-P)P^{n-1}$, `06:51`)
NEW LABEL   `dist:eq:condgeom`
STATUS      verbatim ($$ → `equation`); now the proof of THM-002

### EQ-044  (was `eq:qsd`, `06:63`)
NEW LABEL   `dist:eq:qsd`
STATUS      verbatim
TEXT        $q_n=(1-1/a)(1/a)^{n-1}=(a-1)a^{-n}$

### EQ-045  (was `eq:QSmoments`, `06:71`)
NEW LABEL   `dist:eq:qsmoments`
STATUS      verbatim
TEXT        $\langle X\rangle_{\rm QS}=a/A$, $\langle X^2\rangle_{\rm QS}=a(a+1)/A^2$, $\mathrm{Var}_{\rm QS}=a/A^2$

### EQ-046  ($\lim J/I=\lim V=1+\lambda/\delta$, `06:162`)
NEW LABEL   `dist:eq:mu0limit`
STATUS      moved — the prose at `06:157–163` referred to the cut QS1/QS2 pair and
            had drifted two figures from it; the identity is kept, attached to
            `dist:fig:qsmeans`, and the "shown in red''/"left above'' deictics are gone

### EQ-047  ($\E{T_{\rm prod}}=\int\Ifix$, `06:172`)
NEW LABEL   `dist:eq:tprodint`
STATUS      verbatim

### EQ-048  (Proposition statement, `06:179`)
NEW LABEL   `dist:eq:tprod`
STATUS      verbatim
TEXT        $\E{T_{\rm prod}}=\frac1\lambda\log\frac a{a-1}=\frac1\lambda\log\langle X\rangle_{\rm QS}$

### EQ-049  (was `eq:phi`, `07:13`)
NEW LABEL   `dist:eq:phi`
STATUS      verbatim
TEXT        $\varphi(t):=-I'(t)=\delta J(t)$

### EQ-050  (defect $\int\varphi=1-b$, `07:19`)
NEW LABEL   `dist:eq:phidefect`
STATUS      verbatim

### EQ-051  (was `eq:burstintegral`, `07:64`)
NEW LABEL   `dist:eq:burstintegral`
STATUS      verbatim
TEXT        $\pr{\Kb=k}=\delta k\int_0^\infty p_k(t)\dd t$

### EQ-052  (the discretisation, `07:71`)
NEW LABEL   — (inline)
STATUS      verbatim ($$ → `\[`)

### EQ-053  (was `eq:antideriv`, `07:79`)
NEW LABEL   `dist:eq:antideriv`
STATUS      verbatim
TEXT        $\dda{}{t}\left[\frac{P^k}{k\lambda}\right]=\frac1\lambda P^{k-1}P'=p_k(t)$

### EQ-054  ($\int_0^\infty p_k\dd t=\frac1{k\lambda}a^{-k}$, `07:90`)
NEW LABEL   `dist:eq:pkintegral`
STATUS      verbatim

### EQ-055  (was `eq:burstlaw`, `07:98`)
NEW LABEL   `dist:eq:burstlaw`
STATUS      verbatim
TEXT        $\pr{\Kb=k}=\frac\delta\lambda a^{-k},\ k\ge1$

### EQ-056  (was `eq:burstlaw-cond`, `07:103`)
NEW LABEL   `dist:eq:burstlawcond`
STATUS      verbatim
TEXT        $\pr{\Kb=k\mid\text{burst}}=(a-1)a^{-k},\ k\ge1$

### EQ-057  (normalisation check, `07:123`)
NEW LABEL   — (inline)
STATUS      verbatim ($$ → `\[`)
RECOMPUTED  $\sum_k(\delta/\lambda)a^{-k}=0.8116062299=1-b$ ✓

### EQ-058  (first-moment check, `07:129`)
NEW LABEL   — (inline)
STATUS      verbatim ($$ → `\[`)
RECOMPUTED  $\sum_k k(\delta/\lambda)a^{-k}=13.985700=V_\infty$ ✓

### EQ-059  (was `eq:sizebias`, `07:167`)
NEW LABEL   `dist:eq:sizebias`
STATUS      verbatim
TEXT        $\pr{\Kb=k\mid\tau=t}=kp_k/J$, $\ \E{\Kb\mid\tau=t}=K/J=1+\frac{2\lambda}\delta(1-I)$

### EQ-060  (late-burst limit, `07:175`)
NEW LABEL   `dist:eq:latelimit`
STATUS      verbatim
TEXT        $\E{\Kb\mid\tau=t}\to1+\frac{2\lambda}\delta(1-b)=\langle X^2\rangle_{\rm QS}/\langle X\rangle_{\rm QS}$

### EQ-061  (was `eq:tn`, `07:242`)
NEW LABEL   `dist:eq:tn`
STATUS      verbatim
TEXT        $t_n=\log n/\theta$

### EQ-062  (was `eq:tau-given-k`, `07:253`)
NEW LABEL   `dist:eq:taugivenk`
STATUS      verbatim
TEXT        $\E{\tau\mid\Kb=n}=\frac1\theta\sum_{k=1}^n\frac1k=\frac{H_n}\theta$

### EQ-063  ($p_n$ at $\mu=0$ and the two integrals $L_1,L_2$, `07:263`, `07:266`)
NEW LABEL   — (inside the proof)
STATUS      verbatim ($$ → `\[`)

### EQ-064  (the $L_2$ recurrence, `07:274`)
NEW LABEL   — (inside the proof)
STATUS      verbatim ($$ → `\[`)

### EQ-065  (was `eq:tau-given-k-asymp`, `07:280`)
NEW LABEL   `dist:eq:taugivenkasymp`
STATUS      verbatim
TEXT        $\E{\tau\mid\Kb=n}\simeq(\log n+\gamma)/\theta$

### EQ-066  (was `eq:cond-cdf`, `07:288`)
NEW LABEL   `dist:eq:condcdf`
STATUS      verbatim
TEXT        $\pr{\tau<t\mid\Kb=n}=(1-\ee^{-\theta t})^n$

### EQ-067  (Gumbel limit, `07:295`)
NEW LABEL   `dist:eq:gumbel`
STATUS      verbatim
TEXT        $\pr{\tau<t\mid\Kb=n}\simeq\exp(-n\ee^{-\theta t})=\exp(-\ee^{-T})$

### EQ-068  (was `eq:tau-burst`, `07:314`)
NEW LABEL   `dist:eq:tauburst`
STATUS      verbatim
TEXT        $\E{\tau\mid\text{burst}}=\frac1{\lambda(1-b)}\log\frac{a-b}{a-1}$

### EQ-069  (integration by parts in the proof, `07:326`, `07:333`)
NEW LABEL   — (inside the proof)
STATUS      verbatim ($$ → `\[`)

### EQ-070  ($I_{\rm bud}$, $V_{\rm bud}$, `07:358`)
NEW LABEL   `dist:eq:bud`
STATUS      verbatim ($$ → `equation`)

### EQ-071  (was `eq:bud-geom`, `07:363`)
NEW LABEL   `dist:eq:budgeom`
STATUS      verbatim
TEXT        $\pr{\Kb_{\rm bud}=k}=\frac{d_{\Icell}}{d_{\Icell}+p}\left(\frac p{d_{\Icell}+p}\right)^k$, $k\ge0$

### EQ-072  ($\mean{\wt}$ decomposition, `08:13`)
NEW LABEL   — (inline)
STATUS      verbatim ($$ → `\[`)

### EQ-073  (was `eq:VoverI`, `08:17`)
NEW LABEL   `dist:eq:voveri`
STATUS      verbatim
TEXT        $\mean{\wt\mid\wt>0}=V(t)/(1-I(t))$

### EQ-074  (was `eq:meanK`, `08:24`)
NEW LABEL   `dist:eq:meank`
STATUS      verbatim
TEXT        $\mean{\Kb}=V_\infty/(1-b)=\frac{\lambda-\mu}\delta+\frac1{1-b}$

### EQ-075  ($\mean{\Kb}$ decomposed on $\{\tau>t\}$, `08:41`)
NEW LABEL   `dist:eq:kdecomp`
STATUS      verbatim

### EQ-076  (was `eq:Kcond`, `08:46`)
NEW LABEL   `dist:eq:kcond`
STATUS      verbatim
TEXT        $\mean{\Kb\mid\tau>t}=(\mean{\Kb}-V(t))/I(t)$

### EQ-077  (the apparent limit, `08:53`)
NEW LABEL   — (inline)
STATUS      verbatim ($$ → `\[`)

### EQ-078  (consistent form → 0, `08:69`)
NEW LABEL   `dist:eq:consistent`
STATUS      verbatim

### EQ-079  (the genuinely interesting limit, `08:78`)
NEW LABEL   `dist:eq:patient`
STATUS      verbatim

### EQ-080  (was `eq:latemean`, `08:84`)
NEW LABEL   `dist:eq:latemean`
STATUS      verbatim
TEXT        $\lim_t\mean{\Kb\mid\tau>t,\ \text{burst}}=\lim K/J=\langle X^2\rangle_{\rm QS}/\langle X\rangle_{\rm QS}=1+\frac{2\lambda}\delta(1-b)$

### EQ-081  (was `eq:Ihatk`, `09:26`)
NEW LABEL   `dist:eq:ihatk`
STATUS      verbatim
TEXT        $I_k=I^k$, $D_k=D^k$, $\Ifix[,k]=I^k-D^k$

### EQ-082  (was `eq:Jk`, `09:55`)
NEW LABEL   `dist:eq:jk`
STATUS      verbatim
TEXT        $J_k=kI^{k-1}J$

### EQ-083  (was `eq:Kk`, `09:60`)
NEW LABEL   `dist:eq:kk`
STATUS      verbatim
TEXT        $K_k=kKI^{k-1}+k(k-1)J^2I^{k-2}$

### EQ-084  (was `eq:gk`, `09:68`)
NEW LABEL   `dist:eq:gkflux`
STATUS      verbatim
TEXT        $g_k=\delta K_k=\delta(kKI^{k-1}+k(k-1)J^2I^{k-2})$

### EQ-085  ($V_\infty^{(1)}=V_\infty$, `09:107`)
NEW LABEL   `dist:eq:vk1`
STATUS      verbatim

### EQ-086  (was `eq:Vk`, `09:111`)
NEW LABEL   `dist:eq:vk`
STATUS      verbatim
TEXT        $V_\infty^{(k)}=(1-b^k)+\frac{2\lambda}\delta[\frac1{k+1}-b^k+\frac{kb^{k+1}}{k+1}]+k(k-1)\frac\lambda\delta\int_1^b(x-a)(x-b)x^{k-2}\dd x$

### EQ-087  (was `eq:Vkmu0`, `09:119`)
NEW LABEL   `dist:eq:vkmuzero`
STATUS      verbatim
TEXT        $V_\infty^{(k)}=k+\lambda/\delta$ ($\mu=0$)

### EQ-088  ($s$, $\rho$, `10:34`)
NEW LABEL   `dist:eq:srho`
STATUS      verbatim
TEXT        $s=\delta/(\lambda+\delta)$, $\rho=\lambda/(\lambda+\delta)=1-s$

### EQ-089  ($G\sim\mathrm{Geom}_0(s)$, `10:50`)
NEW LABEL   `dist:eq:geomevents`
STATUS      verbatim

### EQ-090  (was `eq:rkdecomp`, `10:60`)
NEW LABEL   `dist:eq:rkdecomp`
STATUS      verbatim
TEXT        $r_k=1+G_1+\cdots+G_k$

### EQ-091  (was `eq:rklaw`, `10:71`)
NEW LABEL   `dist:eq:rklaw`
STATUS      verbatim
TEXT        $\pr{r_k=n}=\mathcal A^{(n)}_k s^k\rho^{n-1}$, $\mathcal A^{(n)}_k=\binom{n+k-2}{k-1}$

### EQ-092  ($r_1$, `10:79`)
NEW LABEL   `dist:eq:r1`
STATUS      verbatim

### EQ-093  ($r_2$, $r_3$, $r_4$, `10:82`)
NEW LABEL   `dist:eq:r234`
STATUS      verbatim

### EQ-094  (coefficient recurrence, `10:91`)
NEW LABEL   `dist:eq:arec`
STATUS      verbatim

### EQ-095  (was `eq:rkmoments`, `10:115`)
NEW LABEL   `dist:eq:rkmoments`
STATUS      verbatim
TEXT        $\mean{r_k}=1+k\lambda/\delta$, $\mathrm{Var}(r_k)=k\rho/s^2$

### EQ-096  (was `eq:rkgf`, `10:120`)
NEW LABEL   `dist:eq:rkgf`
STATUS      verbatim
TEXT        $\mean{z^{r_k}}=z(s/(1-\rho z))^k$

### EQ-097  (was `eq:t1m`, `10:134`)
NEW LABEL   `dist:eq:t1m`
STATUS      verbatim
TEXT        $\pr{t_1>t}=I(t)^m$, $f^{(m)}_{t_1}=mI^{m-1}\delta J$

### EQ-098  (general-fixation density, `10:147`)
NEW LABEL   `dist:eq:genfix`
STATUS      verbatim; the wrapper "as in the original investigation'' deleted (plan §4.10)

### EQ-099  ($T(k)=\sum_{j=k}^{k+G}\xi_j$, `10:158`)
NEW LABEL   `dist:eq:tkdecomp`
STATUS      moved to Appendix C.3 (plan §4.10)

### EQ-100  (was `eq:LTk`, `10:164`)
NEW LABEL   `dist:eq:ltk`
STATUS      moved to Appendix C.3
TEXT        $\Lap T(k,u)=\sum_{g\ge0}s\rho^g\prod_{j=k}^{k+g}\frac{(\lambda+\delta)j}{(\lambda+\delta)j+u}$

### EQ-101  (was `eq:LTk-hyp`, `10:173`)
NEW LABEL   `dist:eq:ltkhyp`
STATUS      moved to Appendix C.3
TEXT        $\Lap T(k,u)=\frac{sk}{k+u'}\Fhyp(k+1,1;k+1+u';\rho)$

### EQ-102  (was `eq:meanT`, `10:178`)
NEW LABEL   `dist:eq:meant`
STATUS      moved to Appendix C.3
TEXT        $\mean{T(k)}=\sum_{m\ge0}\frac{\rho^m}{(\lambda+\delta)(k+m)}$

### EQ-103  (conditional factorisation and $P_1(m,u)$, `10:197`)
NEW LABEL   `dist:eq:t2cond`
STATUS      moved to Appendix C.3; **altered — SUB-3**, $P_1(m,u)\to\Pi(m,u)$

### EQ-104  (was `eq:Lt2`, `10:204`)
NEW LABEL   `dist:eq:lt2`
STATUS      moved to Appendix C.3; **altered — SUB-3**
TEXT        $\Lap{t_2}(u)=\sum_{g\ge0}s\rho^g\,\Pi(1+g,u)\Lap T(1+g,u)$

### EQ-105  ($\mean{t_2}$ assembly, `10:218`)
NEW LABEL   — (inline, Appendix C.3)
STATUS      verbatim

### EQ-106  (Appendix C.1, first part of $g_k$ integral, `C:16`)
NEW LABEL   — (inside the derivation)
STATUS      verbatim ($$ → `\[`)

### EQ-107  (Appendix C.1, integrated first part, `C:23`)
NEW LABEL   — (inside the derivation)
STATUS      verbatim ($$ → `\[`)

### EQ-108  (Appendix C.1, second part, `C:32`)
NEW LABEL   — (inside the derivation)
STATUS      verbatim ($$ → `\[`)

### EQ-109  (Appendix C.2, $G_k$ in $\gamma,v$, `C:52`)
NEW LABEL   `dist:eq:gkgamma`
STATUS      verbatim ($$ → `equation`)

### EQ-110  (Appendix C.2, coefficient extraction $[z^H]G_k$, `C:64`)
NEW LABEL   `dist:eq:zHGk`
STATUS      verbatim ($$ → `equation`)

### EQ-111  (Appendix C.2, binomial expansion constants, `C:72`)
NEW LABEL   `dist:eq:cexpand`
STATUS      **altered — SUB-2**, $K_i\to C_i$
TEXT        $(1-\ee^{\theta t})^n(b\ee^{\theta t}-a)^m=\sum_{i=0}^{n+m}C_i(\ee^{\theta t})^i$

### EQ-112  (Appendix C.2, the ${}_2F_1$ antiderivative, `C:78`)
NEW LABEL   `dist:eq:hypantideriv`
STATUS      verbatim; now cites `m:app:hyp` (plan §9 item 3)
CARRIED BY  `m:app:hyp`, `m:prop:hypIden`, `m:eq:hypIden` — the identity itself,
            flagged in CH2's overview as a result of this thesis
VERIFIED    `grep -rl "label{m:app:hyp}" CH2/sections/` → `app_c_hypergeometric_identity.tex`
            `grep -rl "label{m:prop:hypIden}" CH2/sections/` → `app_c_hypergeometric_identity.tex`
            `grep -rl "label{m:eq:hypIden}" CH2/sections/` → `app_c_hypergeometric_identity.tex`

---

## 2. The three licensed additions

### PROP-001  the two conventions differ by a function of time (plan §6.1)
NEW LABEL   `dist:prop:conventions`
STATUS      new — licensed addition (a)
TEXT        $G_{\rm kill}(z,t)=G_{\rm cat}(z,t)+(1-I(t))$, exactly, for all $z$ and all $t$
DERIVED FROM  EQ-026 and EQ-028, both already on the page
CONSEQUENCES  `dist:eq:convseq` — $p_n^{\rm kill}=p_n^{\rm cat}$ ($n\ge1$);
              $p_0^{\rm kill}=p_0^{\rm cat}+(1-I)$; moments on $n\ge1$
              convention-independent; $G(1,t)=I(t)$ under catastrophe

### THM-003  burst size is the quasi-stationary law, with the telescoping proof (plan §6.2)
NEW LABEL   `dist:thm:identity`  (was `cor:burst-qsd`, promoted from corollary to theorem)
STATUS      new proof of an old statement — licensed addition (b)
PROOF       $p_k\dd t=\lambda^{-1}\sigma^{k-1}\dd\sigma$ under $\sigma=P(t)$;
            $\pr{\Kb=k}=\frac\delta\lambda\int_0^{1/a}k\sigma^{k-1}\dd\sigma=\frac\delta\lambda a^{-k}$
NEW LABEL (proof display)  `dist:eq:telescope`
VERIFIED    key check 1 — $p_1=P'/\lambda$ to $1.3\times10^{-30}$ relative,
            four parameter sets × four times, 60-digit arithmetic
VERIFIED    telescoped law against the closed form, max error $3.5\times10^{-18}$
CRITERION   `dist:rem:criterion` — the identity holds for any killed process
            whose transient conditional law is geometric in a single sliding
            ratio $P(t)$ with $p_1=P'/\lambda$ and killing hazard linear in load

### PROP-002  the quasi-stationary decay rate (plan §6.3, the absorbed CH2 block)
NEW LABEL   `dist:prop:decay`
STATUS      new to Chapter 5 — absorbed from `CH2/notes/bdc_material_for_later_chapters.tex`,
            block `%% BEGIN: BDC quasi-stationarity paragraph`
TEXT        $\nu\mathcal Q=-\vartheta\nu$, $\ \mathbb P_\nu\{T_{\rm fix}>t\}=\ee^{-\vartheta t}$,
            $\ \vartheta=\mu\nu_1+\sum_{i\ge1}\delta i\,\nu_i$
ALTERED     **SUB-4** ($T_0\to T_{\rm fix}$, $\kappa_i\to\delta i$),
            **SUB-5** ($K\to\mathcal Q$, $\theta\to\vartheta$)
CLOSING SENTENCE  rewritten: the source block says the question "is not settled
            by the argument above, and is best approached by simulation in the
            first instance''; Chapter 5 has the analytic answer (plan §6.3)
CONSISTENCY CHECK  `dist:eq:decaycheck` —
            $\vartheta=\mu\frac{a-1}a+\delta\frac a{a-1}=\lambda b(a-1)+\lambda a(1-b)=\lambda(a-b)=\theta$
VERIFIED    key check 2 — four parameter sets, worst relative error $8.1\times10^{-16}$;
            algebraic form $\lambda b(a-1)+\lambda a(1-b)=0.873212459829=\theta$
EDIT OUTSIDE `CH5_REWRITE/`  the dated comment header added to
            `CH2/notes/bdc_material_for_later_chapters.tex` (comment only; that
            file is never `\input`)

---

## 3. Formal statements

### THM-001  the load is geometric at every time
NEW LABEL   `dist:thm:geometric`
STATUS      **promoted** — was the unnumbered subsection "Geometric at every time'' (`05:25`),
            stated in italic prose with no theorem environment
CONTENT     verbatim: EQ-034 and EQ-035, unchanged; the promotion adds an
            environment and a proof, not mathematics

### COR-001  the sum is $\Ifix$
NEW LABEL   `dist:cor:sum`
STATUS      **promoted** — was the subsection "Normalisation: the sum is $\Ifix$'' (`05:47`)
CONTENT     verbatim: EQ-038

### THM-002  quasi-stationary distribution of the BDC  (was `thm:qsd`, `06:59`)
NEW LABEL   `dist:thm:qsd`
STATUS      verbatim statement; **gains a `proof` environment** (plan §4.5) whose
            content is the existing EQ-043 argument, moved inside it

### PROP-003  mean productive lifetime  (was `prop:lifetime`, `06:177`)
NEW LABEL   `dist:prop:lifetime`
STATUS      verbatim; **gains a bracketed name** (it was the only proposition without one);
            the manual `\qquad\square` at `06:217` deleted (amsthm adds the box)

### THM-004  burst-size distribution  (was `thm:burst`, `07:95`)
NEW LABEL   `dist:thm:burst`
STATUS      verbatim, proof verbatim

### PROP-004  conditional rupture time, $\mu=0$  (was `prop:tau-given-k`, `07:250`)
NEW LABEL   `dist:prop:taugivenk`
STATUS      verbatim, proof verbatim

### PROP-005  mean burst time conditioned on bursting  (was `prop:tau-burst`, `07:311`)
NEW LABEL   `dist:prop:tauburst`
STATUS      verbatim, proof verbatim

### REM-001  a guess that fails  (was `rem:ihatk`, `09:33`)
NEW LABEL   `dist:rem:ihatk`
STATUS      verbatim — **preservation list item 5**

### REM-002  the free-sum trap  (was `rem:gk`, `09:74`)
NEW LABEL   `dist:rem:gk`
STATUS      verbatim — **preservation list item 5**

### REM-003  the coefficient, and a near miss  (`10:102`, unlabelled)
NEW LABEL   `dist:rem:coefficient`
STATUS      verbatim mathematics; the clause "supplying the proof that the original
            investigation had conjectured but not completed'' and the phrase
            "and a near miss'' deleted (plan §4.10 — four references to the
            original investigation)

### REM-004  the circularity  (`08:92`, prose)
NEW LABEL   `dist:rem:circularity`
STATUS      moved into a `remark` environment (plan §4.8) — **preservation list item 4**

### DEF-001  process definition  (`02:56`)
NEW LABEL   `dist:def:bdc`
STATUS      verbatim

### DEF-002  the three fixation functions  (`02:144`)
NEW LABEL   `dist:def:fixation`
STATUS      verbatim

---

## 4. Numerical claims

All recomputed by `verification/recheck_numbers.py`; 42 quoted values, 0 mismatches.
Working parameters $(\lambda,\mu,\delta)=(1,0.2,0.05)$ unless stated.

| ID | quantity | source | value | recomputed |
|---|---|---|---|---|
| NUM-001 | $a$ | plan §4.1(d) | 1.0616 | 1.0616 ✓ |
| NUM-002 | $b$ | `07:52` | 0.188 | 0.1884 ✓ |
| NUM-003 | $AB=\delta/\lambda$ | `02:130` | 0.05 | 0.05000000 ✓ |
| NUM-004 | $ab=\mu/\lambda$ | `02:127` | 0.2 | 0.20000000 ✓ |
| NUM-005 | $V_\infty$ | `06:83`, `08:99` | 13.99 | 13.9857 ✓ |
| NUM-006 | $\E{\Kb\mid\text{burst}}=a/(a-1)$ | `06:83` | 17.23 | 17.2321 ✓ |
| NUM-007 | $(a+1)/(a-1)$ | `07:214` | 33.46 | 33.4642 ✓ |
| NUM-008 | $\mathrm{Var}_{\rm QS}=a/A^2$ | `06:76` | — | 279.7140 ✓ |
| NUM-009 | $(a+1)/a$, working | plan §4.6 | 1.94 | 1.942 ✓ |
| NUM-010 | $(a+1)/a$, anthrax | plan §4.6 | 1.38 | 1.376 ✓ |
| NUM-011 | $\E{T_{\rm prod}}$ | `06:230` | 2.847 | 2.8468 ✓ |
| NUM-012 | $d_{\Icell}=1/\E{T_{\rm prod}}$ | `06:231` | 0.351 | 0.3513 ✓ |
| NUM-013 | $\Ifix[,2]=I^2-D^2$, $t=1$ | `09:44` | 0.8458 | 0.8458 ✓ |
| NUM-014 | $\Ifix^{\,2}$, $t=1$ | `09:44` | 0.6542 | 0.6542 ✓ |
| NUM-015 | $K_2$, $t=1$ (true) | `09:81` | 22.264 | 22.2645 ✓ |
| NUM-016 | $K_2$, $t=1$ (free sum) | `09:80` | 23.39 | 23.3923 ✓ |
| NUM-017 | $V_\infty^{(1)}$ | `09:133` | 13.99 | 13.9857 ✓ |
| NUM-018 | $V_\infty^{(2)}$ | `09:135` | 17.43 | 17.4321 ✓ |
| NUM-019 | $V_\infty^{(3)}$ | polish review §0 | 18.89 | 18.8930 ✓ |
| NUM-020 | $V_\infty^{(5)}$ | polish review §0 | 21.00 | 20.9962 ✓ |
| NUM-021 | $V^{(1)}/(1-b)$ | `09:138` | 17.23 | 17.2321 ✓ |
| NUM-022 | $V^{(2)}/(1-b^2)$ | `09:138` | 18.07 | 18.0736 ✓ |
| NUM-023 | $V^{(3)}/(1-b^3)$ | `09:138` | 19.02 | 19.0202 ✓ |
| NUM-024 | $V^{(5)}/(1-b^5)$ | `09:138` | 21.00 | 21.0012 ✓ |
| NUM-025 | $2V_\infty$ | `09:134` | 27.97 | 27.9714 ✓ |
| NUM-026 | $V_\infty^{(k)}=k+\lambda/\delta$, $\mu=0$ | `09:128` | 11,12,13,14,15 | max err 7.1e-15 ✓ |
| NUM-027 | budding $\pr{\Kb=0}$ at matched mean | `07:417` | 0.055 | 0.0548 ✓ |
| NUM-028 | $\mean{T(1)}$, $(\lambda,\delta)=(1,1)$ | `10:185` | 0.693 | 0.693 ✓ |
| NUM-029 | $\mean{T(2)}$ | `10:185` | 0.386 | 0.386 ✓ |
| NUM-030 | $\mean{T(3)}$ | `10:185` | 0.273 | 0.273 ✓ |
| NUM-031 | $\mean{T(4)}$ | `10:185` | 0.212 | 0.212 ✓ |
| NUM-032 | *F. tularensis* $b$ | `11:63` | 6.66 % | 6.66 % ✓ |
| NUM-033 | *F. tularensis* $\E{\Kb\mid\text{burst}}$ | plan §4.12 | 934 | 934.4 ✓ |
| NUM-034 | *F. tularensis* $\E{T_{\rm prod}}$ | plan §4.12 | 45.6 h | 45.6 h ✓ |
| NUM-035 | *F. tularensis* $\E{\tau\mid\text{burst}}$ | plan §4.12 | 48.4 h | 48.4 h ✓ |
| NUM-036 | *F. tularensis* median burst | plan §4.12 | "about 647" | **648** — see note |
| NUM-037 | *F. tularensis* $a$ | plan §4.1(d) | 1.001 | 1.0011 ✓ |
| NUM-038 | *B. anthracis* $b$ | `11:81` | 96.24 % | 96.24 % ✓ |
| NUM-039 | *B. anthracis* $\E{\Kb\mid\text{burst}}$ | `11:82` | 1.60 | 1.601 ✓ |
| NUM-040 | *B. anthracis* $\E{T_{\rm prod}}$ | plan §4.12 | 0.74 h | 0.736 h ✓ |
| NUM-041 | *B. anthracis* $\E{\tau\mid\text{burst}}$ | plan §4.12 | 0.93 h | 0.929 h ✓ |
| NUM-042 | *B. anthracis* $a$ | plan §4.1(d) | 2.66 | 2.6626 ✓ |
| NUM-043 | simulated chain intervals | `10:188` | 0.691, 0.500, 0.377, 0.292 | simulation output of `verify_chained_transfer.py`; not recomputed (plan §18: do not re-run) |
| NUM-044 | $\theta=\lambda+\delta$ for `dist:fig:taugivenk` | `07:452` | 1.1 | 1.1 ✓ |
| NUM-045 | $\E{\Kb\mid\tau=t}\to21$ at $(1,0,0.1)$ | `07:224` | 21 | $1+2\lambda/\delta=21$ ✓ |

**NUM-036 note.** The plan quotes "the median about 647''. The value
$\log 2/\log a=647.33$ is what that rounds; the median proper — the least $k$
with $\pr{\Kb\le k}\ge\tfrac12$ — is $648$, since $\pr{\Kb\le647}=0.49982$ and
$\pr{\Kb\le648}=0.50036$. The chapter states 648, the computed value, not 647.

**Parameter triples used in the chapter.** $(1,0.2,0.05)$ working;
$(1,0,0.1)$ the $\mu=0$ comparator; $(\lambda,\delta)=(1,1)$ and
$(1,0.1)$, $(2,0.5)$ for the chain; $(0.15,0.01,1.5\times10^{-4})$
*F. tularensis*; $(0.64,1.64,0.04)$ *B. anthracis*; $\lambda=1$,
$\delta=0.1$, $d_{\Icell}+p=8$ for `dist:fig:taugivenk`. All unchanged.

---

## 5. Tables

| ID | table | old label | new label | status |
|---|---|---|---|---|
| TAB-001 | canonical notation | `tab:notation` | `dist:tab:notation` | **extended** — plan §4.2 requires every symbol appearing in more than one section; 14 rows → 26. No existing row altered. |
| TAB-002 | budding vs bursting | `tab:budburst` | `dist:tab:budburst` | verbatim, every cell |
| TAB-003 | master formula table | (unlabelled, App. A) | `dist:tab:formulae` | verbatim rows + a **provenance column** (plan §4.13) + one row for $\Pi$/$\Lap{t_2}$ |
| TAB-004 | verification record | (unlabelled, App. B) | `dist:tab:verification` | verbatim, all 28 counts |
| TAB-005 | three means | — | `dist:tab:threemeans` | **new presentation** of EQ-074, EQ-012, EQ-080; every number already in the chapter (NUM-005, NUM-006, NUM-007) |
| TAB-006 | two extremes | — | `dist:tab:twoextremes` | **new presentation**; $b$ and $\E{\Kb\mid\text{burst}}$ from `11:63`/`11:82`, the timing rows NUM-034/035/040/041 from the recheck |

---

## 6. Citations

Placement unchanged where it exists; nine entries were cited, thirteen were not.
**No BibTeX entry composed.**

| key | old placement | new placement |
|---|---|---|
| `brockwell1982birth`, `karlin1982linear`, `di2008note` | §2 process definition | §2, unchanged |
| `van2011quasi` | §6 opening (dangling — rendered as "**[4].**") | §5, attached to a sentence |
| `yaglom1947certain` | §7.3, §11.3 | §6, §12 |
| `carruthers2020stochastic` | §11.2 | §12 |
| `williams2021anthrax` | §11.2 ×2 | §12 |
| `oyston2004tularaemia` | §11.2 | §12 |
| `williams2024reproduction` | §11.1 | §12 |
| `perelson1996hiv`, `nowak1996population`, `mclean1993balance` | uncited | §1, the Basic Model of Viral Replication |
| `karlin1957classification` | uncited | §5, beside `m:def:qsd` |
| `gilchrist2006evolution` | uncited | §11, the trade-off |
| `hataye2019principles` | uncited | §12, the budding caveat |
| `pearson2011stochastic` | uncited | §12, within-host stochastic context |
| `mckendrick1926applications`, `vonfoerster1959some` | uncited | §12, the renewal pointer |
| `artigiani1987revolution`, `hawkes1971spectra`, `stehfest1970algorithm`, `gaver1965observations` | uncited | still uncited — no sentence in this chapter needs them; left in `references.bib` |

`% NEEDS-REF: F. tularensis macrophage time-lapse rupture recordings` — §12.

---

## 7. What is cut, and what carries it

| cut | carried by |
|---|---|
| §3's derivation of the killing PDE as a *parallel* computation | PROP-001; both PDEs still displayed (EQ-015, EQ-016) |
| §4's second characteristic solve | PROP-001 |
| §4's generic method-of-characteristics exposition | `m:sec:moc`, `m:eq:genericcharacteristics`, `m:fig:characteristics` |
| §4's coefficient-extraction formula | `m:app:extract`, `m:eq:stateProb` |
| §2.6's re-derivation of $\E{W_t^2}$ | \ChCore's variance section; the formula stays boxed (EQ-013) |
| §10.7's verification narrative | Appendix B (`dist:app:verification`), which said the same thing |
| §10.5–10.6 | Appendix C.3 (`dist:app:chained-transforms`), EQ-099–EQ-105 |
| four "original investigation'' passages (`10:102`, `10:143`, `10:183`, `10:209`) and `07:24` | nothing — they narrate an unpublished predecessor's drafting history; the mathematics they wrap is kept in full |
| seven commented `\figureflag` blocks, provenance comments | nothing — build provenance |
| `figures/F4a_6_FAILED.pdf` | nothing |
| `\label{Char1}`, `\label{Char2}` | nothing — inside `align*`, labelled nothing |
| `\xx \ww \zz \eec \lrbq \pdxn \Chapref \Tabref \Figref \Eqref \Secref`, `lemma` | nothing — dead macros |

---

## 8. Figures

17 floats in the source; 4 cut, 1 built, so 14 in the rewrite.

| old label | file | new label | status |
|---|---|---|---|
| `fig:F4a_1_joint_process` | `F4a_1_joint_process.pdf` | `dist:fig:joint` | re-placed, caption only |
| `fig:N4a_1` | `N4a_1_pgf_characteristics.pdf` | — | **cut** — a consequence of the plan §9 deferral; `m:fig:characteristics` does this job |
| `fig:F4a_2_geometric_slide` | `F4a_2_geometric_slide.pdf` | `dist:fig:slide` | re-placed, caption only |
| `fig:N4a_6` | `N4a_6_qs_vs_release_means.pdf` | `dist:fig:qsmeans` | re-placed; absorbs the orphaned prose of `06:157–163` |
| `fig:two_figures` (+`fig:figure1`, `fig:figure2`) | `QS1.png`, `QS2.png` | — | **cut** — 72 dpi rasters, no axis labels, no legend, parameters unstated; content covered by `dist:fig:qsmeans` and `N4a_2(b)` |
| `fig:F4a_3_qsd_convergence` | `F4a_3_qsd_convergence.pdf` | — | **absorbed** into `dist:fig:two-mechanisms` (left panel) |
| `fig:N4a_2` | `N4a_2_productive_lifetime.pdf` | `dist:fig:lifetime` | re-placed, caption only |
| `fig:F4a_4_burst_time_density` | `F4a_4_burst_time_density.pdf` | `dist:fig:bursttime` | re-placed, caption only |
| `fig:F4a_5_burst_size_late` | `F4a_5_burst_size_late.pdf` | `dist:fig:latemean` | **regenerated single-panel**: panel (a) absorbed into `dist:fig:two-mechanisms`, panel (b) kept unchanged in content |
| `fig:N4a_5` | `N4a_5_joint_tau_K.pdf` | `dist:fig:jointtauk` | re-placed, caption only |
| `fig:F4a_8_tau_given_k` | `F4a_8_tau_given_k.pdf` | `dist:fig:taugivenk` | re-placed, caption only |
| `fig:N4a_4` | `N4a_4_three_burst_means.pdf` | `dist:fig:threemeans` | re-placed, caption only |
| `fig:N4a_7` | `N4a_7_moi_flux_ratios.pdf` | — | **cut** — duplicates panel (a) of `F4a_6_moi` (plan §11.2, "consolidate one'') |
| `fig:N4a_8` | `N4a_8_yield_subextensive.pdf` | `dist:fig:subextensive` | re-placed, caption only |
| `fig:F4a_6_moi` | `F4a_6_moi.pdf` | `dist:fig:moi` | re-placed, caption only |
| `fig:F4a_7_chained_transfer` | `F4a_7_chained_transfer.pdf` | `dist:fig:chained` | re-placed, caption only |
| `fig:N4a_3` | `N4a_3_burst_vs_budding_pmf.pdf` | `dist:fig:budding` | re-placed, caption only |
| — | `fig01_two_mechanisms.pdf` | `dist:fig:two-mechanisms` | **built** — the chapter's signature image (plan §11.2) |

Every surviving figure is cross-referenced by `\cref` at the sentence it
supports; in the source, one of seventeen was referenced and every other
`fig:` label was dead.

---

## 9. Ledger check

Run `bash verification/ledger_check.sh` from `CH5_REWRITE/`. It greps every
new label out of `sections/`, every deferral target out of `CH2/sections/`,
and the six preservation passages out of `sections/`, and prints the table.

---

## Review pass, 2026-08-22

Presentation only; no result changed and no equation was restated. Verified
after every pass: `latexmk` clean (0 warnings, 0 undefined refs, 0 bad boxes),
`ledger_check.sh` PASS, `recheck_numbers.py` 42/42, `verify_chained_transfer.py`
28/28. Changes that touch this ledger:

- **§2 retitled** to *The process, its roots, and its closed forms*; the label
  `dist:sec:recap` is unchanged.
- **New equation** `dist:eq:kjP`, $K/J=(1+P)/(1-P)$, in §8. An identity at
  every $t$, not a limit; it closes the step at `dist:eq:latemean` that the
  introduction previously flagged as heuristic, and the introduction now
  claims one heuristic argument rather than two.
- **New figure** `dist:fig:readings` (fig. 5.2) in §4, and a third panel on
  `dist:fig:two-mechanisms` computing both routes independently.
- **`dist:fig:budding` reduced to one panel**: the tail comparison could not
  show what its title claimed (the two tails agree to within 1% over the
  plotted range) and was dropped.
- **Preservation item 3a retargeted** in `ledger_check.sh`: the Icarus passage
  was rewritten (Daedalus holds the middle course; Icarus fell), so the check
  now greps the replacement. The §5.4 "hover" callback is preserved and still
  checked by item 3b.
- **Provenance letter** for $\vartheta$ changed **M** to **N** in App. A: the
  decay rate is derived here, not quoted.
