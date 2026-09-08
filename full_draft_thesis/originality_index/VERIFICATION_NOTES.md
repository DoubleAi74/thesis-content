# Verification notes

What was checked before writing `originality.tex`, what held up, and what needs action.
Every claim in the index was tested against the chapter text; page and theorem numbers were
resolved from `main.aux`, not from the audit.

---

## Method

The novelty audit in `Novel all/novelty_index.tex` grades 320 extracted results as
Original (4) / Extends (109) / Already (162) / Not a result (45). Its `CHx-Rnn` identifiers
appear nowhere in the thesis, so every claim had to be matched semantically to a theorem or
formula in the chapter source. Ten chapters were read against the audit's claims; the pivotal
ancestor papers were checked against the published record.

Two preliminary checks cleared the audit for use: it describes the **current** text (the old
folder names it cites are stale, but Chapter 6 differs by two lines and Chapter 7's differences
are the label rename `thm:main` → `tt:thm:main` from the stitch), and its counts table is
arithmetically self-consistent.

---

## The four Original claims — all confirmed

| Claim | Where | Status |
|---|---|---|
| Flooding identity $(L-1)(1/m-1)$, criterion $L>1$ | **Thm 6.8, p.163** | Confirmed. Proof complete: algebra plus a positivity case-split. |
| Offspring laws coincide at $L=1$ | **Prop 6.9, p.165** | Confirmed. The stronger of the two — a PGF-level identity, not a moment coincidence. |
| Exact finite-time two-type survival | **Thm 7.4, p.189** | Confirmed. See defect A below. |
| Killed bivariate PGF | **Eq. 7.50, p.201** | Confirmed. No theorem wrapper; introduced by analogy. |

The load-bearing assertion behind Thm 7.4 — that setting $\delta=0$ does **not** recover
Antal–Krapivsky — is argued by the chapter itself in three separate places
(`ch07/sections/01_introduction.tex:8`, `appendices.tex:109`, `app_killed_pgf.tex:68`), not
merely asserted by the audit. Setting $\delta=0$ in $S,G$ forces $S\equiv G\equiv1$; recovering
AK requires the companion killed PGF with generating-function initial data. Antal–Krapivsky
(arXiv:1105.1157) was checked against the primary source: equations (25)–(29) confirmed
verbatim, zero occurrences of "catastrophe" or "killing", and modified Bessel functions
confirmed in the bi-critical section — so the Prop 7.9 contrast holds too.

No prior art was found for the joint (population, released-count) process, so the $W_t$
coordinate of Chapter 4 appears unclaimed.

---

## Defects found — ordered by urgency

**A. Theorem 7.4 has no proof in the compiled thesis.**
`chapters/ch07/sections/04_main_result.tex:283-289` — the `\begin{proof}...\end{proof}` block
after the boxed main theorem is entirely commented out, every line prefixed `%`. The derivation
exists as running prose through §§7.4.1–7.4.3, so the mathematics is present and traceable, but
one of the four strongest results currently stands in the PDF as a boxed theorem with nothing
after it. Uncommenting restores it.

**B. Chapter 3 presents Kolmogorov's constant without Kolmogorov.**
`chapters/ch03/chapter.tex` runs to 1,447 lines and contains exactly five citations:
Becker–Bergweiler (×2), Koenigs + Milnor, Rubel, Yaglom. The string "Kolmogorov" appears
nowhere in the chapter and nowhere in `references.bib`. $A(p)$ is introduced and its existence
proved in the first person with no ancestor named. The chapter's real contribution — the
Koenigs dictionary and the hypertranscendence corollary (Thm 3.5, p.82) — is properly cited and
carefully hedged, and reads as an increment only once Kolmogorov is named.

**C. Four sentences over-claim what is new.**
The phrase "a result of this thesis" appears three times — `ch02/sections/01_overview.tex:69`,
`app_b_absorption_models.tex:7`, `04_method_of_characteristics.tex:330` — attached to the
absorption–birth–death generating function (Prop 2.8, p.52) and a hypergeometric integral
identity (Prop 2.11, p.55). The first is Kendall's interior PGF integrated against exponential
absorption; the second is structurally Gradshteyn–Ryzhik 3.194.1, and the chapter derives it
from Olver's Euler integral representation. The Chapter 1 roadmap line "the hardest member of
that family is solved here for the first time"
(`ch01/sections/09_how_the_content_is_divided_amongst_the_chapters.tex:32`) rests on the same
claim and is the most exposed sentence in the thesis.

The fourth is in the same Chapter 1 section, at lines 71–73 (p.19):

> Some of the results have been found by others before, but several — the second moment
> expressed through $I$, the variances, and the joint load–release moments — go beyond what the
> existing literature had recorded.

Only one of those three survives. The second moment of the **load** is $\partial_{zz}G(1,t)$ from
Karlin and Tavaré's generating function, so it is not beyond the literature; what is new is the
polynomial organisation of the whole hierarchy (Prop 4.17, p.103), which is a different claim.
$\mathrm{Var}(X_t)=K-J^2$ is inherited for the same reason — only the **release** variance
$\mathrm{Var}(W_t)$ (Eq. 4.26, p.101) is an increment. The joint load–release moments are close
to definitional, since $X_tW_t\equiv0$ before rupture. Narrowing the sentence to the release
moments would make it defensible and lose nothing.

One caution in the same paragraph, in the opposite direction. It introduces the autonomous
Riccati equation for $I(t)$ as the classical route that makes the calculation close. That is
correct — the generating function of a linear birth–death process satisfies a first-order PDE
that characteristics reduce to a Riccati ODE, which is standard (Kendall 1948). It is simply not
in **Karlin and Tavaré**, who work by Karlin–McGregor spectral theory. So the fix is the citation
target, not the classification: do not claim the Riccati route as new.

**D. Theorem 6.6 states a published result as an unattributed theorem.**
`chapters/ch06/chapter.tex:865-881` — "$R_0$ is unchanged by bursting" is a numbered theorem
with its own proof and no citation to Pearson et al. (2011). More broadly there is **not one
`\cite` in lines 1030–1250**, the stretch containing both of Chapter 6's Original theorems.
The novelty is real, but it is currently asserted by silence rather than argued against the
literature.

**E. Chapter 3 should engage with Pakes (2026).**
Anthony G. Pakes, *Remarks on Kolmogorov's constant for simple branching processes*, J. Appl.
Prob., 28 April 2026, DOI `10.1017/jpr.2026.10094`. The CrossRef abstract states that the simple
explicit representation "is an upper bound that is attained only if the offspring-number
probability-generating function is **quadratic**" — that is, exact for binary branching, which is
precisely §3.B's case. §3.B (p.83) reports a computational search that found no elementary form
for $A(p)$ there. Verified from CrossRef only; the Cambridge full text is paywalled, and Pakes's
$\hat\mu$ is the reciprocal of $A(p)$, so confirm the correspondence before acting. The chapter
is already hedged ("not a proof that $p\mapsto A(p)$ has none"), so this is an addition rather
than a retraction. Related: Imomov, arXiv:2205.03024.

**F. Citation gaps that are real.**
`Kolmogorov`, `Pilyugin`, `Rabosky`, `Etienne` and `Lanchester` have no entry in
`references.bib` at all. `Yuan and Allen (2011)` has an entry but is cited nowhere in Chapter 8,
the chapter whose central reversal result most needs to be distinguished from theirs. Karlin–Tavaré
is cited but orphaned: in Chapter 5 it appears only at `02_recap.tex:76`, never at Theorems 5.4,
5.6, 5.9 or 5.10. At the quasi-stationary theorem the chapter cites `karlin1957classification` —
Karlin **& McGregor**, a different paper by different authors — so a reader chasing "Karlin"
there lands on the wrong reference.

**G. Housekeeping.** `chapters/ch10/sections/` and `chapters/ch07/sections/06_interpretation.tex`
are orphaned files that no chapter `\input`s. They are not compiled and not examined, but they
are the source of the errors in the next section.

---

## Where the audit is wrong

The audit is not a reliable document on its own. Its arithmetic is sound; its charges are not.

- **The Karlin–Tavaré charge is false as written.** It says KT 1982 is "the missing citation for
  Chapters 4 and 5". Chapter 4 cites it three times *and* carries Remark 4.1 (p.89), "What is
  classical here, and what is developed here", crediting KT with the Riccati equation and its
  roots. The true finding is weaker: cited, but orphaned from the results it supports.
- **All seven of Chapter 10's claimed extensions are not in the thesis.**
  `chapters/ch10/chapter.tex` is a generated file with zero `\input` statements; the audit built
  its Chapter 10 section almost entirely from the orphaned drafts in `ch10/sections/`. The
  compiled chapter cannot carry those results and says so: "There is no host-to-host layer".
- **The sign error is real but not in the thesis.** The flipped threshold
  $p_N > (\mu_E-\mu_M)/(\mu_M-\mu_N)$ sits in the orphaned
  `sections/03_quadrant_argument.tex:71`. The live boxed Eq. 10.9 (p.263) has the correct
  $(\mu_E-\mu_M)/(\mu_N-\mu_M)$.
- **Three of its four charges against Chapters 9–10 collapse.** Chapter 9 never claims a logistic
  speciation model is unpublished — it says the opposite ("The substitution is not new in
  itself"). It never claims to test the push of the past with a pure-birth model — it explicitly
  disclaims that. The neutrophil-threshold charge is overstated: the chapter calls the argument
  "the weakest piece of mathematics in the thesis". Only the narrower point survives, that
  Ke, Chen and Yang (2013) is cited in Chapters 1, 7 and 8 but not in Chapter 10.
- **It invented supporting detail.** Its Chapter 3 discussion cites Pollak, Seneta, Pakes and a
  specific Imomov counterexample ("2.25 vs 2.825"); none appear in your chapter or bibliography.
  It names a "five-ODE ladder" in Chapter 6 that does not exist. It cites a Quirouette 2023 that
  is absent from your bibliography.
- **It has the Pakes result backwards** — see defect E.
- **Its own citations need correcting.** Zhang & Zhu is **2013**, J. Appl. Prob. 50(1):114–126,
  not 2011. Brockwell–Gani–Resnick is pages 709–731.
- **Its detail disagrees with its own counts** in three chapters: Ch 1 (15/10 listed against
  14/11 tabulated), Ch 5 (25/23 against 26/22), and Ch 7, where only 25 of 31 claimed items are
  listed at all.

---

## Results that may be under-claimed

The audit graded conservatively, and in several places too harshly.

- **Burst size equals the quasi-stationary law (Thm 5.10, p.126)** may be more yours than the
  audit allows. Karlin & Tavaré was read in full: the linear-fractional PGF (2.5), the geometric
  killing position (Lemma 1, eq. 2.8) and the Green's-function lifetime (4.1–4.2) are all
  confirmed theirs, but the *identity* connecting the killing-position law to the
  quasi-stationary law is not stated there — the two are computed separately, in different
  lemmas. If that holds, Thm 5.10 is not merely a new proof of a known identity.
- **Karlin & Tavaré never mention Riccati.** They work by Karlin–McGregor spectral theory; the
  word does not appear in the paper. This is a citation-target correction, not a novelty claim —
  the Riccati reduction is classical in its own right (Kendall 1948), so Remark 4.1 is right to
  call it classical and wrong only to attribute it to KT.
- Other candidates: the QSD decay rate (Prop 5.7, p.124); the $k$-founder result refuting
  $\widehat I_k=\widehat I^{\,k}$ (Rem 5.15, p.134); Cor 8.9 (p.219), which carries Chapter 8's
  central point that subcriticality exists only because of removal; the variance
  $\mathrm{Var}[S_t]$ of Prop 9.2 (p.232), which the chapter says had not been recorded before;
  and the Feynman–Kac occupation-time representation (Prop 7.2, p.179), folded by the audit into
  "standard first-step bookkeeping".

Two Chapter 8 items are graded too generously in the other direction: R04 duplicates R03
(numerical against analytic), and R07 is a self-declared open problem counted as an extension.

---

## Not covered

The audit does not grade Chapter 9's §9.5 (the ~440-line multiplicative-dissipation and
automaton section, pp.246–252) or the Chapter 9 public-good appendix (p.254) at all. Neither is
classified in any bucket.

---

## Literature checks

Verified against the published record rather than against the audit.

**Karlin & Tavaré (1982)**, *Linear birth and death processes with killing*, J. Appl. Prob.
19:477–487 — read in full. Confirmed theirs: the linear-fractional generating function (2.5),
the geometric killing position (Lemma 1, eq. 2.8), the Green's-function mean productive lifetime
(4.1–4.2). Geometric occupancy at every $t$ is implied by the algebra but never stated. The
identity linking burst size to the quasi-stationary law is **not** stated — see under-claiming
above. They work by Karlin–McGregor spectral theory; "Riccati" does not appear.

**Antal & Krapivsky (2011)** (arXiv:1105.1157 = J. Stat. Mech. P08018) — read from the primary
source. Equations (25)–(29) confirmed verbatim as the bivariate PGF; zero occurrences of
"catastrophe" or "killing"; modified Bessel functions confirmed in the bi-critical section.
Chapter 7's contrast holds on every point.

**Pearson, Krapivsky & Perelson (2011)**, PLoS Comput. Biol. 7(2) — this one **strengthens**
Chapter 6. Their $p_v$ is the extinction probability from a single virion, and they find
$p_v^{\mathrm{burst}} \le p_v^{\mathrm{cont}}$: bursting is favoured *unconditionally*. Their main
comparison is derived for a fixed burst size; a random burst size is treated separately
(eqs. 22–25) and found "similar". They derive **no dimensionless criterion** that could change
sign. So Thm 6.8 is not merely a sharper version of their comparison — it shows the ordering they
found to be one-directional is in fact governed by $L$ and reverses at $L=1$. Worth saying
explicitly in Chapter 6.

**Pilyugin & Antia (2000)** is *Modeling immune responses with handling time*, Bull. Math. Biol.
62:869–890. The limiting mechanism is handling time: macrophages split into free and engaged
states, and an engaged effector is occupied rather than consumed, then returns to the free pool.
That is the right contrast for Chapter 8's unreplenished suppressors, and naming the mechanism is
sharper than saying the effectors "recycle". No entry in `references.bib`.

**Yuan & Allen (2011)** is *Stochastic models for virus and immune system dynamics*, Math.
Biosci. (December 2011). CTMC and SDE models of early infection covering both budding and
bursting; extinction probability depends on initial dose, on whether the immune response is
activated, and on the release strategy. The substance of the audit's charge stands: this is a
published dependence of the budding/bursting ranking on an immune term, and Chapter 8 does not
cite it.

**Corrections to the audit's own citations.** Zhang & Zhu is 2013, J. Appl. Prob. 50(1):114–126.
Brockwell–Gani–Resnick is pages 709–731. Pakes (2026) is real — see defect E — but its result is
reported backwards.

*Note on coverage:* two subagent attempts at the virology and evolution citation checks were
terminated by a safety classifier before completing. Those checks were then run directly. The
papers above were verified; **Komarova (2007), Nelson et al. (2004), Miao et al. (2011),
Ke/Chen/Yang (2013) and the Nee/Rabosky/Etienne diversification cluster were not
independently re-checked**, and the report's characterisations of them still rest on the audit.
None of the four Original claims depends on them.
