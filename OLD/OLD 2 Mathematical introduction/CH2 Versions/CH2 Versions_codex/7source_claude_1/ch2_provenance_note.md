# Provenance: seed vs index vs forward-reference only

Three-way split of everything in Chapter 2. Nothing was pasted from either source;
all prose is recomposed.

---

## 1. From `Ch2_seed` — all of its mathematics, recomposed

Every equation in the seed appears in the chapter. Section by section:

**Galton–Watson (§2.3).** Offspring law and PGF $\phi$, $\mathbb E[Z_n]=\mu^n$ by the
tower property, the iteration $u_{n+1}=\phi(u_n)$; the binary specialisation
$\phi(z)=pz^2+1-p$, $\mathbb E[Z_n]=(2p)^n$, $S_{n+1}=2pS_n-pS_n^2$ with its
first-step reading; monotone convergence to a fixed point, the roots $0$ and
$(2p-1)/p$, the trichotomy; the critical case $\mathbb E[T]=\sum_n S_n$,
$S_n\sim2/n$, the harmonic divergence, and the three critical exponents
($S_n\sim2/n$, $\mathbb P(T=n)\sim2/n^2$, $\mathbb P(\mathcal T=n)\sim n^{-3/2}$).

**Quasi-stationarity (§2.4).** The linearisation to $S_{n+1}\approx2pS_n$ and the
definition of $A(p)$; the caution that it is an equivalence not an identity; the
conditional mean $1/A(p)$; the full moment-generating-function derivation of
$\mathbb E[Z_n^2]$ through the composition identity
$M_n'(t)=(2p)^n M_{n-1}\cdots M_1 e^{2t}$; the conditional variance limit; the
Riccati continuum view and the observation that its integration constant *is*
$A(p)$.

**Small populations (§2.5.1–2.5.4).** The early-generation arithmetic and the
criticality values of $u_n$; $S_n^{(k)}=1-u_n^k$; the push-of-the-past parallel;
the discrete birth–death–catastrophe calculation ($\kappa$, the halting probability
$1-(1-\kappa)^{2^{n-1}}$, $S_n=(1-\kappa)^{2^n-1}$, and the Jensen argument);
the continuous-time survival probability, the limiting conditional mean
$\mu/(\mu-\lambda)$, and $A_{\mathrm c}(p)=(1-2p)/(1-p)$.

**The constant $A(p)$ (§2.6), in full.** The logistic substitution; the telescoping
infinite product $A=\frac12\prod_{k\ge1}(1-S_k/2)$ and its convergence proof; the
exact series $1/A = 1+\sum_n(2p)^n/(2-S_n)$; the two-sided bounds and the
$A>\frac12A_{\mathrm c}$ corollary, with proof; the parity bound, with proof; the
ten-row numerical table; the asymptotic $A\sim2(1-2p)$ by both routes and the
gradient-$-4$ diagnostic; the $\varepsilon\ln(1/\varepsilon)$ correction; the
discrete-versus-continuous reconciliation with its two endpoint interpretations;
the symbolic-regression search; the Koenigs/Schröder material — definition,
$A(p)=2\psi_r(\frac12)$ with proof, the conjugacy $c=(2r-r^2)/4$, Becker–Bergweiler,
hypertranscendence, the monomial and Chebyshev cases, the attracting/repelling
remark, the "what this does and does not establish" passage, and the Mandelbrot
cardioid; and the practical piecewise scheme.

**Absorption models (§2.7), in full,** and both appendices.

### What was trimmed from the seed (agreed at the checkpoint)

- The five-line symbolic-regression expression $\hat A_2$ is no longer displayed;
  it is described in one sentence. $\hat A_1$, $\hat A_3$ and the spliced $\hat A_4$
  are kept, as is the diagnostic that kills them.
- The footnote advertising the `Koenigs_plotter/gem_p1.html` visualiser is cut.
- Two autobiographical asides are cut: "two years after this work was set aside…"
  and the confession that a plot's vertical axis is mislabelled in the original
  script. The axis is simply described correctly in the caption instead.
- §2.5.2 keeps the push-of-the-past argument but states it abstractly, as an
  ensemble of birth–death processes retained only if alive at a large time. The
  empirical framing is gone; the citation remains.

### Errors in the seed that were corrected rather than reproduced

- Three distinct objects shared the symbol $\mathbf X$ (offspring variable,
  expected population, interior particle count). Now $L$, $Z_i$, $X_t$.
- $r$ meant $1-2p$ in the Riccati subsection and $2p$ in the $A(p)$ section, and a
  third $r$ was a characteristic coordinate. Now $\varepsilon$, $r$, $\eta$.
- The seed asserts $p=\lambda/(\lambda+\mu)$ without justification when comparing
  the discrete and continuous constants. It is now a consequence of the
  competing-clocks proposition (§2.2.1), cited at the point of use.
- The seed cites Allen for the continuous-time extinction probability $p_0(t)$.
  It is now derived, as $G(0,t)$ from the linear birth–death PGF PDE (§2.2.4).

---

## 2. From `topics_index` — used as a menu only, never quoted

The whole of **§2.2** is index-sourced. Nothing from the index appears anywhere
else in the chapter.

| Index topic | Where it lands |
|---|---|
| `prob-exp`, `prob-memoryless` | §2.2.1, Def. 2.1 and eq. (2.1) |
| `prob-exp-race` | §2.2.1, Prop. 2.2 — and it earns its place, since §2.5.4 needs exactly this |
| `ssa-gillespie` | §2.2.1, Rem. 2.3 — a 150-word remark, not a subsection |
| `ctmc-markov`, `ctmc-transitions`, `ctmc-generator` | §2.2.2, eqs. (2.2)–(2.4) |
| `ctmc-holding`, `ctmc-absorbing` | §2.2.2 |
| `ctmc-kolmogorov`, `bd-master` | §2.2.2, eqs. (2.5)–(2.6) |
| `pgf-def`, `pgf-multi`, `pgf-process` | §2.2.3 |
| `bd-general`, `bd-linear` | §2.2.4, eq. (2.7) |
| `bd-pgf-pde` | §2.2.4, eq. (2.8) — the template for all of §2.7 |
| `bd-extinction` | §2.2.4, eqs. (2.10)–(2.11) |

Index topics deliberately **not** used: `prob-sigma`, `prob-rv`, `prob-moments`,
`prob-discrete-laws`, `prob-uniform`, `prob-other-laws`, `prob-lst`, `sp-def`,
`ctmc-first-step`, `ctmc-poisson`, `bd-pure-birth`, `bp-ct`, `bp-multitype`. These
are the encyclopaedia bulk the exemplar card warns against; none is needed by any
later section of this chapter.

`bd-catastrophe-pointer` is a pointer in the index and is treated as one here —
see §3 below.

---

## 3. Setup and forward reference only — no results

**§2.5.5, the continuous-time birth–death–catastrophe process.** This is the one
piece of genuinely new material. It gives Definition 2.5 (rates
$q_{n,n+1}=\lambda n$, $q_{n,n-1}=\mu n$, $q_{n,\dagger}=\rho n$, two absorbing
states), notes the two features that distinguish it from linear birth–death, and
writes down the generating-function equation
$\partial_t G = (\lambda z^2-(\lambda+\mu+\rho)z+\mu)\,\partial_z G$ — pointing out
that it differs from the linear birth–death equation only in the coefficient of $z$,
and that the loss of the root at $z=1$ is what makes $G(1,t)$ a survival
probability rather than one.

Nothing further. No rates catalogue, no means or variances, no state
probabilities, no burst-size distributions, no two-type extension. Those are
forward-referenced, not previewed:

- birth–death–catastrophe results → "the later chapters on birth–death–catastrophe
  processes"
- two-type / multi-type → "the chapter on multi-type processes"
- compartment rupture and release → "the chapter on compartment rupture"
- time-inhomogeneous rates → "the later chapter on non-constant rates"

§2.8 closes by saying explicitly what has been withheld and why.

---

## 4. Bibliography

Eleven entries carried from the seed. Seven added, all standard and all cited:
Norris (CTMCs), Karlin–Taylor, Kendall 1948 (the linear birth–death solution),
Gillespie 1977, Méléard–Villemonais and Collet–Martínez–San Martín (modern
quasi-stationarity), and the NIST handbook (for ${}_2F_1$ and the Euler integral).

The Aldridge–Whaler–López-García–Molina-París–Gillard–Lythe paper in the kit is
**not** cited. It is a modelling paper about release from infected cells; citing it
would import precisely the applied narrative the chapter is required to exclude,
and the abstract rupture motif needs no citation to justify it. The verification
note the seed carries against the Becker–Bergweiler entry has been preserved in
`references.bib`, including its open item: the precise hypotheses of the rigidity
theorem quoted in §2.6.6 were not verifiable without the paper itself.
