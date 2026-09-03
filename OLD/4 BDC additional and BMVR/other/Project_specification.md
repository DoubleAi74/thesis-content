# Project Specification — Three-Chapter BDC Build

This is the binding specification for building `BDC_core/` (Chapter 3),
`BDC_extra/` (Chapter 4a) and `BDC_odes/` (Chapter 4b). Read `Startup.md`
first. Where this document and `CHAPTER4_PLAN.md` disagree, this document
wins. Track execution in `Progress.md`.

---

## 1. Chapter identities and folder layout

Create, at the root of the current directory:

```
BDC_core/
  main.tex  references.bib  sections/  figures/
BDC_extra/
  main.tex  references.bib  sections/  figures/
BDC_odes/
  main.tex  references.bib  sections/  figures/
```

| Build | Chapter | Working title |
|---|---|---|
| `BDC_core` | Chapter 3 | The birth–death–catastrophe process: definition and main results |
| `BDC_extra` | Chapter 4a | The birth–death–catastrophe process: distribution theory, quasi-stationarity, and burst statistics |
| `BDC_odes` | Chapter 4b | From one cell to a population: burst-aware renewal dynamics and the bursting–budding comparison |

Titles may be refined during the final edit if clearer wording is found; any
change is recorded in `Progress.md`. Each `main.tex`: `article` class at 11pt
(matching the sources), the package list of the source `main.tex` files
(which must include `xcolor` — required by the flag macro — with `hyperref`
loaded after it), the
unified macros of §2 below, the figure-flag macro of §7, the theorem
environments (`theorem/proposition/lemma/corollary` numbered per section,
`definition`, `remark`), `\tableofcontents`, `\bibliographystyle{unsrt}`,
date line "Chapter N of AA Thesis --- University of Leeds / Draft compiled
\today". Each build compiles with `latexmk -pdf main.tex` from its own folder.

---

## 2. The unified notation regime (binding for all three chapters)

Applied to prose, formulas, captions, table entries, and figure-flag text.
Python *identifiers* inside scripts may remain as they are; anything a reader
sees uses this regime.

### 2.1 Single-cell symbols

| Symbol | Meaning | LaTeX macro | Notes |
|---|---|---|---|
| $\lambda$ | birth rate (per capita) | `\lambda` | **replaces β everywhere** |
| $\mu$ | death rate | `\mu` | unchanged |
| $\delta$ | catastrophe rate | `\delta` | unchanged |
| $X_t$ | intracellular count | `\xt` (`{\bf X}_t`) | unchanged |
| $0$ | internal extinction state | — | unchanged |
| $H$ | absorbing rupture state | `H` | **replaces R everywhere** |
| $W_t$ | released count (0 before burst, $X_{\tau^-}$ after) | `\wt` | **Chapter 3's mid-chapter Y_t is retired** |
| $\tau$ | burst/catastrophe time | `\tau` | unchanged |
| $\mathcal{K}$ | burst size | `\Kb` | unchanged |
| $I(t)$ | $\Pr\{\text{no burst by }t\}$ | `I(t)` | unchanged |
| $D(t)$ | $\Pr\{\text{internal extinction, no burst}\} = p_0(t)$ | `D(t)` | kept by name, defined as $p_0$ |
| $I_{\mathrm{fix}}(t)$ | $\Pr\{X_t\notin\{0,H\}\} = I(t)-D(t)$ | `\Ifix(t)` → `I_{\mathrm{fix}}(t)` | **replaces Î, \hat I, and Chapter 3's conflicting definitions** |
| $J(t),K(t)$ | $\mathrm{E}[X_t]$, $\mathrm{E}[X_t^2]$ | unchanged | |
| $V(t)$ | $\mathrm{E}[W_t]$ | unchanged | |
| $p_n(t)$ | state probabilities | unchanged | |
| $\eta$ | $(\lambda+\mu+\delta)/(2\lambda)$ | `\eta` | unchanged |
| $a,b$ | roots, $b<1<a$ | plain | **retire I₊, I₋ after one line: $I_+=a$, $I_-=b$** |
| $A,B,\theta$ | $a-1$, $1-b$, $\lambda(a-b)$ | plain | |
| $\kappa$ | $1+\delta/(2\lambda)$ | `\kappa` | appears in $K(t)$ and $K(I)$ |
| $L$ | $a(1-b)=a-\mu/\lambda$ | plain | flooding parameter (Chapter 4b) |

### 2.2 Identities

$$
ab=\frac{\mu}{\lambda},\quad a+b=\frac{\lambda+\mu+\delta}{\lambda},\quad
AB=\frac{\delta}{\lambda},\quad A+B=a-b,\quad \theta=\lambda(a-b).
$$
These must appear in Chapter 3 (reference values + derivation) and in
Chapter 4a's recap.

### 2.3 Population symbols (Chapter 4b only)

| Symbol | Meaning | Macro |
|---|---|---|
| $T$ | target cells (held fixed) | plain |
| $\gamma$ | infection rate | `\gamma` |
| $c$ | virion clearance | plain |
| $d_{\mathcal{I}}$ | infected-cell removal (phenomenological) | `d_{\Icell}` |
| $\mathcal{I},\mathcal{V}$ | infected-cell / free-particle counts | `\Icell`, `\Vfree` |
| $i(t)$ | incidence $\gamma T\mathcal{V}$ | `i(t)` |
| $q$ | infection success $\gamma T/(\gamma T+c)$ | plain |
| $I_{\mathrm{fix}}(a)$, $g(a)$ | survival / release kernels | `\Ifix(a)`, `g(a)` |
| $\widetilde{f}$ | Laplace transform | `\Lap{f}` |
| $p_{\rm eff}(r)$, $d_{\mathcal{I},{\rm eff}}(r)$ | effective parameters | as drafted |
| $G_{\rm off}$, $z_{\rm ext}$, $m$ | offspring pgf, extinction probability, mean $=qV_\infty$ | as drafted |

### 2.4 Local renamings to avoid collisions (Chapter 4b)

The draft uses a few symbols twice; resolve as follows and record in
`Progress.md`:
- §15 Model 10 (jumping release rate): the intensity decay rate, drafted as
  $\kappa$, collides with $\kappa=1+\delta/(2\lambda)$ — rename it to $\zeta$.
- Boolean partial-release fraction (§15–16), drafted as $q$, collides with the
  infection success probability — rename the boolean fraction to $\varphi$
  (and write the burst-time density as $\delta J$ in 4b rather than reusing
  $\varphi$).
- Eclipse conversion rate stays $\alpha$; telegraph switching stays
  $\sigma_{\rm on},\sigma_{\rm off}$; eclipse division stays $\rho_{\rm div}$.
- Everything else as drafted.

### 2.5 Conversion duties on the Chapter 4 draft sources

When material moves from `document MAIN/sections/` into the builds:
1. `\beta` → `\lambda` throughout (search–replace, then re-read every affected
   display for sense — e.g. $\theta=\lambda(a-b)$, $AB=\delta/\lambda$,
   $V_\infty$ forms, $\mathrm{E}[W^2]$).
2. `R` (rupture state) → `H`.
3. `\Ihat` → `\Ifix` (macro renamed in each `main.tex`; all occurrences).
4. Delete the correction remarks: Remark "Correction of the Chapter 3 formula
   for Î" (draft 02), Remark "Correction and check" on $\mathrm{E}[W^2]$
   (draft 02), Remark "A guess that fails" numerical contrast *is kept as
   mathematics* but its "thesis formula" framing is reworded as a neutral
   "the naive guess $\Ifix_k=\Ifix^k$" remark, Remark "Correction of the
   draft's closed form" (draft 10) reworded as a neutral statement of the
   correct coefficient, the "53 vs 54 checks" history note (drop the history,
   state 54). Rule: no sentence in the builds may say or imply that an earlier
   chapter or draft was wrong.
5. `D(t)` stays named $D(t)$ with the definition $D(t)=p_0(t)$ at first use.

### 2.6 Conversion duties on Chapter 3

1. Body sections 04–11: `\beta` → `\lambda` (about 120 occurrences; §5's mixed
   formulas rewritten wholly in λ; figure captions likewise).
2. `\hat I` → `\Ifix` with the corrected definition (§3.3 below).
3. $Y_t$ → $W_t$ in sections 07–11 (headings included).
4. $I_+,I_-$ → $a,b$ with one explicit correspondence line.
5. $I_{\mathrm{death}}$ removed from the reference values (its definition was
   inverted and it is used nowhere); $D:=p_0$ added instead.

### 2.7 Reading `Grant_paper.pdf` — notation translation

The co-authored paper is a first-class source (see `Startup.md` §2.5), but it
uses a different (older) notation. **Direction of unification: the chapters'
unified regime of §2 is canonical.** Everything taken from the paper is
translated *into* it — never the other way round. In particular the
catastrophe rate stays $\delta$ (the paper's $\alpha$ is not adopted), the
rupture state stays $H$, the burst size stays $\mathcal{K}$, and the roots
stay labelled $b<1<a$. The paper's $\mu=0$ shorthands may optionally be
adopted *inside* the $\mu=0$ subsections where they lighten the algebra —
translated as $r=\lambda/\delta$ and $\sigma=\lambda+\delta=\theta$ — but
must be defined at first use and never leak into the general-$\mu$ text.
Before taking any formula, figure idea, or prose from the paper, translate:

| Paper | Chapters (unified regime) | Meaning |
|---|---|---|
| $\lambda$, $\mu$ | $\lambda$, $\mu$ | birth, death (same) |
| $\alpha$ | $\delta$ | catastrophe rate — **δ is retained; α is not imported** |
| $\delta$ | $d_{\mathcal{I}}$ | infected-cell death in the BMVR equations |
| roots $a,b$ with $0<a<1<b$ | our $b,a$ with $b<1<a$ | **the paper's labels are swapped**; paper's $ab=\mu/\lambda$ = ours |
| $R$ (burst size) | $\mathcal{K}$ | |
| $\tau$ | $\tau$ | same |
| $I,J,K,V$ | $I,J,K,V$ | same single-cell meanings |
| $I_{\mathrm{fix}}$ not used; $I(t)-p_0(t)$ appears | $I_{\mathrm{fix}}=I-D$ | |
| $r=\lambda/\alpha$, $\sigma=\lambda+\alpha$ | $r=\lambda/\delta$, $\sigma=\theta$; only in $\mu=0$ subsections, defined at first use | |
| paper's $g(t)$ (geometric ratio) | our $P(t)$ of Chapter 4a §5 | do not import the symbol $g$ (reserved for the release kernel in Chapter 4b) |

The paper's results quoted in §4.1, §5.1, and the formula block §6 below have
already been translated and verified; use the forms given there, not the
paper's raw forms.

---

## 3. Chapter 3 — `BDC_core` (upgrade, nothing removed)

Source: `3 BDC core/document MAIN/`. Copy `sections/`, `figures/IMG_ch4/*`,
`references.bib` into the build, then work in the build only.

### 3.1 Structural plan (files)

| Source file | Treatment |
|---|---|
| `01_opening.tex` | Empty placeholder — merge into the introduction file (record the deletion of the empty file). |
| `02_chapter_introduction.tex` | Keep all content including the "Further interest" excursus. Fix the documented typos (continuois-time, occuring, macrophaegs, arives, behavious, accross, astroid, mammels, sppured, provinding, evoultionary, populance) plus "et. al." → "et al." (two occurrences); fix the self-referential "explored in chapter 3" leftover; soften the most informal first-person asides ("But yet I quite like it") to the thesis register without flattening the voice; unstack the four-citation sentence; end with a new closing subsection setting up Chapters 4a and 4b (what each will do; why the single-cell theory must be completed and then embedded in a population model). |
| `03_reference_values.tex` | Unify to the §2 regime: keep λ; fix the $p_k/P_k$ index mismatch (k vs i); remove $I_{\mathrm{death}}$, add $D:=p_0$ and $\Ifix:=I-D$; add $A,B,\theta$ and the identities of §2.2; clean the `$\ddt{I}$` splitting. |
| `04_process_definition.tex` | Fix the duplicated `BDRsims` label (distinct labels, both referenced from text); remove the stray `\title{$\wt$}`; β→λ including captions; keep H; light grammar. |
| `05_analytical_quantities.tex` | Rewrite all displays wholly in λ (the J(t) formula currently mixes λ prefactor with β exponents); fix the broken sentence "When μ>0 and process death is possible…"; delete the orphaned line "PLOT E[𝒦] against δ…" (replace with a figure flag, §3.5); fix the "have have" double word; **multi-founder block (audit B1):** keep $I_k=I^k$ with a one-line branching justification; the "(Is this correct?)" marker in the source attaches to the *false* claim $\Ifix_k=(\Ifix)^k$ — replace that claim by the correct $\Ifix_k=I^k-D^k$ and delete the marker, with a forward pointer to Chapter 4a where multi-founder kernels are derived and used; "Kalin and Tavare" → Karlin and Tavaré; remove the unused `\xdef\mysum`; correct the $\Ifix$ definition and closed form (§3.3). |
| `06_derivation_of_equations_and_results.tex` | All λ; fix `\eqref{ddIIfact}` to $(I-a)(I-b)$; retire $I_\pm$ with one correspondence line; replace the wrong $\Ifix$ material with the corrected derivation (§3.3); fix "in in terms". |
| `07_expected_number_of_units_j_t.tex` | $Y_t$→$W_t$ throughout; fix/remove the `Voft` label inside `equation*`; tidy the $\hat p_0$ discussion by defining $D=p_0$ once properly; "compenent" → component. |
| `08_variance…` + `10_variance…` | **Merge into one file** (08 is the superset; 10 is an earlier partial draft). Keep every unique piece: the full $K(t)$ derivation, the factored $K(I)$ (corrected, §3.3), Var/Std of $X_t$, and the $\mathrm{E}[W_t^2]$/Var($W_t$) subsection (from 08, with $Y$→$W$ and the corrected final formula §3.3). Remove the duplicate `Kderev1/2` labels. Record the merge and the removal of file 10 in `Progress.md`. |
| `09_variable_dependencies…` + `11_variable dependencies…` | **Merge into one file.** Keep 09's structure and Var expansions, but with file 11's algebraically correct $K(I)=\frac{2\lambda^2}{\delta^2}(I-\kappa)(I-a)(I-b)$, 11's compact $V(I)=\frac{\lambda-\mu}{\delta}(1-I)-J(I)+1$ and Var(X) forms; and enforce $J=-\delta^{-1}I'$ with $I'=\lambda(I-a)(I-b)$ consistently throughout the merged file (file 11's lead-in contains the sign slip $J=\delta^{-1}I'$, which must not survive the merge). Record the merge and removal of file 11. |
| new closing section | "What comes next": the two directions (complete distribution theory → Chapter 4a; population embedding → Chapter 4b), what each needs from this chapter, and which open questions of this chapter they answer. |

### 3.2 Mathematical errors to fix (exact corrected forms, all verified)

1. **Factored Riccati:** $\dot I=\lambda(I-a)(I-b)$ (draft has $(I-I_+)(I-I_+)$).
2. **$\Ifix$ for $\mu>0$:** definition $\Ifix=I-D$; closed form
   $\Ifix(t)=\dfrac{(a-b)^2 w}{(B+Aw)(aw-b)}$, $w=e^{\theta t}$; the branching
   term in its ODE is $\lambda(I^2-D^2)$, not $\lambda\Ifix^2$; limits
   $\Ifix(0)=1$, $\Ifix(\infty)=0$, $\Ifix'(0)=-(\mu+\delta)$. Note the μ=0
   collapse $\Ifix=I$.
3. **$K(I)$:** $K(I)=\dfrac{2\lambda^2}{\delta^2}(I-\kappa)(I-a)(I-b)$
   (the −2β²/δ version in 08/09 is wrong; file 11's +2β²/δ² version is right).
4. **Second moment of release:**
   $$\mathrm{E}[W_t^2]=\frac{2(\lambda-\mu)}{\delta}V-\frac{\lambda+\mu}{\delta}I-K+\frac{\lambda+\mu}{\delta}+1,$$
   derived via $\ddt{}\mathrm{E}[W^2]=\delta\mathrm{E}[X^3]$ and eliminating
   $\mathrm{E}[X^3]$ through $K'=2(\lambda-\mu)K+(\lambda+\mu)J-\delta\mathrm{E}[X^3]$;
   the integration constant uses $K(0)=1$. Include the μ=0 check:
   $\mathrm{E}[W_\infty^2]=2\lambda^2/\delta^2+3\lambda/\delta+1$, matching the
   geometric law with success probability $\delta/(\lambda+\delta)$.
5. **Vieta/identity block** added (§2.2).
6. **Multi-founder fixation (audit B1):** $I_k=I^k$ is retained, justified by
   the branching property in one line. The source's "(Is this correct?)"
   marker attaches to the *next* line, the false claim $\Ifix_k=(\Ifix)^k$:
   that claim is replaced by $\Ifix_k=I^k-D^k$ (correct for all $\mu$, as
   Chapter 4a proves), and the marker is deleted because the false claim is
   removed — not because it was true. Do not ship $I_{\mathrm{fix},k}
   =I_{\mathrm{fix}}^k$ in any form.

### 3.3 Corrected main-results statements

State the chapter's headline results as boxed results or theorems (the
theorem environments currently exist unused): the Riccati equation and $I(t)$;
$J(t)$; $V(t)$ and $V_\infty=aB/A$; $K(t)$ and $K(I)$; $\Ifix(t)$;
$\mathrm{E}[W_t^2]$. Use the closed forms exactly as given in §6 of this
specification (they agree with the Chapter 4 draft).

### 3.4 Figures for Chapter 3

Copy `figures/IMG_ch4/{BDRsimulations.jpg, BDRsimulationsY2.jpg, I_of_t_1.pdf,
I_of_t_2.pdf, J_of_t_1.pdf, V_of_t_1.pdf}` into `BDC_core/figures/` (drop the
`IMG_ch4` folder layer) **and rewrite every `\includegraphics` path in the
copied sections to `figures/<filename>`** — the source paths contain
`IMG_ch4/` and will not resolve otherwise. Keep all six references, rewrite
captions into the
unified notation (λ), and reference every figure from the text (`poem.jpeg`
stays on disk, unreferenced — record this). Insert figure flags per §7 at the
locations below (you may add more where they materially help):

- **F3.1 — Process transition diagram** (in *Process definition*). TikZ
  schematic. States $0,1,2,\ldots,H$ in a row (ellipse for $H$); arrows
  $n\to n+1$ labelled $\lambda n$, $n\to n-1$ labelled $\mu n$, $n\to H$
  labelled $\delta n$; mark $0$ and $H$ absorbing. Purpose: the definition of
  the process at a glance.
- **F3.2 — Rupture conventions** (in *Choice of rupture state*). TikZ, two
  panels: "killing" (rupture transition lands in 0) vs "catastrophe" (separate
  state H), showing the sample-path difference. Purpose: fix the convention
  distinction used throughout the thesis.
- **F3.3 — Fixation functions** (in *Analytical quantities*). Python analytic
  plot. Three curves $I(t)$, $D(t)$, $I_{\mathrm{fix}}(t)$ for
  $(\lambda,\mu,\delta)=(1,0.2,0.05)$ on $t\in[0,15]$, using the closed forms
  of §6; horizontal asymptotes $b,b,0$ dashed; annotate
  $I_{\mathrm{fix}}'(0)=-(\mu+\delta)$. Axes: $t$, probability. Unified style.
- **F3.4 — Conditional mean convergence** (in *J(t)* or after). Python
  analytic, two panels: (a) $\mu=0$, $(\lambda,\delta)=(1,0.1)$: $J(t)/I(t)$
  and $V(t)$ tending to $1+\lambda/\delta$; (b) $\mu>0$,
  $(1,0.2,0.05)$: $J/I_{\mathrm{fix}}\to a/(a-1)$ and $J/I\to0$. Purpose: the
  quasi-stationary level before the QSD is formally defined; set up Chapter 4a.
- **F3.5 — Burst-size preview** (near *What comes next*). Python bars:
  $\Pr\{\mathcal{K}=k\}=(\delta/\lambda)a^{-k}$ for $(\lambda,\mu,\delta)=(1,0,0.1)$,
  $k=1..30$, with the geometric$(1/a)$ curve overlaid and the mass-at-zero
  note ($b=0$ here). Purpose: preview the Chapter 4a burst-size result.
- **F3.6 — Upgrade flag** (in *Process definition*, next to the existing
  Gillespie figures): re-render the two Gillespie simulations in the unified
  Python style — 100 realisations of $X_t$ and of $W_t$,
  $(\lambda,\mu,\delta)=(1,0,0.1)$, same parameters as the existing jpgs,
  clean PDF output. The existing jpgs remain in place until then.

### 3.5 Bibliography for Chapter 3

Keep the five existing entries verbatim; add
```bibtex
@article{brockwell1982birth,
  title={Birth, immigration and catastrophe processes},
  author={Brockwell, Peter J and Gani, Joseph and Resnick, Sidney I},
  journal={Journal of Applied Probability},
  volume={19}, number={4}, pages={709--731}, year={1982},
  publisher={Cambridge University Press}
}
```
and cite it where Brockwell is named in the introduction. If Pakes et al. 1979
can be cited from your own knowledge with a reliable entry, add and cite it;
otherwise leave the prose mention and record the gap in `Progress.md`. No web
searches.

### 3.6 Acceptance criteria (Chapter 3)

Compiles clean (0 errors, 0 undefined refs; 0 overfull boxes outside
figure-flag boxes — overfulls inside flag boxes are exempt, underfulls are
allowed; figure flags intentional); all of §3.2 fixed; duplicates merged
with unique content preserved and recorded; unified notation per §2;
forward-looking closing section present; every figure referenced and every
`\includegraphics` path resolves; no deleted content unrecorded.

---

## 4. Chapter 4a — `BDC_extra`

Source: `document MAIN/sections/01…10`, `17_discussion.tex` (partial),
appendix material from `A_formula_tables.tex` and `C_technical_derivations.tex`
(partial), `figures/IMG_ch5/QSmean/`.

### 4.1 Structure and content mapping

| New section | Source | Treatment |
|---|---|---|
| §1 Introduction | draft `01_chapter_introduction.tex` | Rewrite to Chapter 4a's scope: motivation (complete the single-cell description), what Chapter 3 supplies, research questions 1–2 and the single-cell half of the rest; one-page-story condensed to the single-cell results; chapter map; forward pointer to Chapter 4b. Keep the killing/catastrophe subsection. |
| §2 What we need from Chapter 3 | draft `02_recap_single_cell_bdc.tex` | Compact recap subsection/section: process + joint process; roots and identities; $I,D,\Ifix$; $J,K,V$; $V_\infty$, $\mathrm{E}[\mathcal{K}\mid\text{burst}]$; $\mathrm{E}[W^2]$. Boxed formulas from §6 below, with pointers to Chapter 3; no proofs except one-line derivations. All correction remarks deleted (§2.5 rule 4). Keep the notation table (converted). |
| §3 PGF PDEs | draft 03 | Converted; defective-PGF caveat kept. |
| §4 Identifying the PGFs | draft 04 | Converted; $k$-founder subsection kept. |
| §5 State probabilities | draft 05 | Converted. |
| §6 Quasi-stationary distribution | draft 06 | Converted; QSD theorem kept; mean productive lifetime kept. |
| §7 Burst time and burst size | draft 07 + `Grant_paper.pdf` §3 | Converted; analytic proof, burst=QSD corollary, size-biasing kept. **Enriched from the paper (translated, verified) — incorporated fluidly, as part of the section's own development, not as an addendum:** (i) the conditional rupture-time law for $\mu=0$: $\mathrm{E}[\tau\mid\mathcal{K}=n]=\theta^{-1}\sum_{k=1}^n\frac1k$ with the large-$n$ approximation $\theta^{-1}(\log n+\gamma)$ and the Gumbel form of the conditioned rupture-time distribution, and the maximiser $t_n=(\log n)/\theta$ of $p_n(t)$; (ii) for $\mu>0$, the mean burst time conditioned on bursting, $\mathrm{E}[\tau\mid\text{burst}]=\frac{1}{\lambda(1-b)}\log\frac{a-b}{a-1}$ — a distinct quantity from $\mathrm{E}[T_{\mathrm{prod}}]$, keep the distinction explicit; (iii) the budding-vs-bursting comparison (paper Table 3.1) adapted to unified notation as a small table or passage. |
| §8 Conditional burst means | draft 08 | Converted. |
| §9 Multiplicity of infection | draft 09 | Converted; the "guess that fails" remark reworded neutrally (§2.5 rule 4). |
| §10 Chained immediate transfer | draft 10 | Converted; verification record kept (state "28 checks, all passing", no history); the closed-form correction remark reworded neutrally. |
| §11 Discussion | draft `17_discussion.tex` + `Grant_paper.pdf` §4 | This chapter's share: the five single-cell assay predictions; open problems — conceptual proof of burst=QSD, general-μ chained joint laws, logistic intracellular growth sensitivity. Forward pointer to Chapter 4b. **Add the paper's biological grounding** (model claims kept distinct from biological claims): *F. tularensis* SCHU S4 estimates $\lambda=0.15\,\mathrm{h}^{-1}$, $\mu=0.01\,\mathrm{h}^{-1}$, $\delta=1.5\times10^{-4}\,\mathrm{h}^{-1}$ (fewer than 7% of cells fail to burst; geometric burst sizes in the hundreds; dose as low as 10 CFU can infect) and *B. anthracis* estimates $\lambda\approx0.64\,\mathrm{h}^{-1}$, $\mu\approx1.64\,\mathrm{h}^{-1}$, $\delta\approx0.04\,\mathrm{h}^{-1}$ (over 96% of phagocytes clear the infection; rupturing cells release on average ~1.6 bacteria; infectious dose $8\times10^3$–$5\times10^4$ spores) — showing the same theory spanning the two extremes. |
| Appendix A | draft `A_formula_tables.tex` | Single-cell table only (population table moves to 4b), plus the μ=0 specialisation block. |
| Appendix B | draft `B_verification_records.tex` | Chained-transfer suite record only (renewal record moves to 4b). |
| Appendix C | draft `C_technical_derivations.tex` | $V_\infty^{(k)}$ derivation and PGF coefficient extraction (hypergeometric transforms move to 4b). |

**Orphan files:** `document MAIN/sections/` also contains
`01_opening.tex` (empty comment), `02_specification_of_rupture_state.tex`,
and `09_potential_application_in_bmvr.tex`, which are **not** in that
folder's `main.tex` `\input` list. They are historical orphans — do not copy
them; their content already lives in the draft introduction (killing vs
catastrophe) and file 11 respectively.

**Discussion split — explicit cut list** (draft `17_discussion.tex`):

| Draft §17 item | Goes to |
|---|---|
| Assay predictions subsection | Chapter 4a |
| Fitting-practice subsection | Chapter 4b |
| Forward-connections subsection | Chapter 4b |
| Open problem 1 (conceptual proof, burst = QSD) | Chapter 4a |
| Open problem 2 (two-type killed second moments) | Chapter 4b |
| Open problem 3 (flooding boundary vs real parameters) | Chapter 4b |
| Open problem 4 (population-level variance) | Chapter 4b |
| Open problem 5 (partial-release flooding boundary in $\varphi$) | Chapter 4b |
| Open problem 6 (logistic intracellular growth) | Chapter 4a |
| Open problem 7 (literature positioning) | Chapter 4b |
| General-μ chained joint laws (Chapter 4a open problem) | sourced from draft §10's scope flags, not from §17 |

### 4.2 Figures for Chapter 4a

Copy `document MAIN/figures/IMG_ch5/QSmean/{QS1.png, QS2.png}` into
`BDC_extra/figures/` **and rewrite the two `\includegraphics` paths in the
copied §6 from `figures/IMG_ch5/QSmean/QS1` to `figures/QS1` (and QS2)**;
keep the §6 figure with its corrected caption. Insert
figure flags (you may add more):

- **F4a.1 — Joint-process schematic** (§2). TikZ: a timeline with the load
  $X_t$ growing stochastically, the burst at $\tau$, and $W_t$ jumping from 0
  to $X_{\tau^-}$; mark $H$. Purpose: the object $(X_t,W_t)$ at a glance.
- **F4a.2 — Geometric slide of the state probabilities** (§5). Python analytic:
  $p_n(t)$ for $(\lambda,\mu,\delta)=(1,0.2,0.05)$ at $t\in\{0.5,1,2,5,15\}$
  against $n$, showing the geometric ratio $P(t)\to1/a$; annotate $P(t)$
  values. Purpose: "geometric at every time" made visible.
- **F4a.3 — Convergence to the QSD** (§6). Python: conditional pmf
  $p_n(t)/I_{\mathrm{fix}}(t)$ at $t=1,5,20$ plus the limiting geometric
  $(a-1)a^{-n}$, same parameters; optionally overlay a simulated conditional
  histogram. Purpose: the QSD theorem numerically.
- **F4a.4 — Burst-time density** (§7). Python analytic: $\varphi(t)=\delta J(t)$
  for $(1,0.2,0.05)$ and $(1,0,0.1)$; shaded annotation of the mass $b$ at
  $\infty$; the conditional density $\delta J/(1-b)$ dashed. Purpose: the
  defective density made explicit.
- **F4a.5 — Burst size and late bursts** (§7). Python: bars of
  $(\delta/\lambda)a^{-k}$ with the conditional geometric overlay (panel a);
  the size-biased mean $K(t)/J(t)$ against $t$ tending to $(a+1)/(a-1)$
  (panel b), parameters $(1,0.2,0.05)$. Purpose: the burst=QSD identity and
  the size-biasing effect.
- **F4a.6 — Multiplicity of infection** (§9). Python: release fluxes $g_k$ for
  $k=1..4$ against age showing superlinearity; inset or second panel:
  conditional mean burst $V_\infty^{(k)}/(1-b^k)$ against $k$, parameters
  $(1,0.2,0.05)$. Purpose: MOI effects.
- **F4a.7 — Chained transfer** (§10). Python: rupture-size pmfs $r_k$,
  $k=1..4$, simulation points against the closed forms
  $\binom{n+k-2}{k-1}s^k\rho^{n-1}$ for $(\lambda,\delta)=(1,1)$; second panel:
  mean inter-rupture intervals $\mathrm{E}[T(k)]$ decreasing against $k$.
  Adapt the exact-sampling machinery of
  `N=2 Immediate Transfer content/verify_chained_transfer.py` (do not modify
  that file; write a chapter-local script). Purpose: the section's results in
  one figure.
- **F4a.8 — Conditional rupture time vs burst size** (§7). Python: the exact
  mean $\mathrm{E}[\tau\mid\mathcal{K}=n]=\theta^{-1}\sum_{k=1}^n 1/k$ against
  $n$ (red dots), the large-$n$ approximation $\theta^{-1}(\log n+\gamma)$
  (dotted), and the budding comparator $(n+1)/(d_{\mathcal{I}}+p)$ from the
  paper (dashed straight line), $\mu=0$ with $\theta=\lambda+\delta=1.1$;
  optional second panel: three values of $\mu$ (paper uses
  $\lambda=0.5$, $\delta=0.01$, $\mu\in\{0,0.005,0.01\}$) with the
  approximation $(\log n+\gamma-\mu/\lambda)/(\lambda+\delta-\mu)$ overlaid.
  Purpose: the harmonic-number law and its budding contrast.

### 4.3 Bibliography for Chapter 4a

Copy from `document MAIN/references.bib` the entries actually cited after
conversion: `brockwell1982birth`, `karlin1957classification`,
`karlin1982linear`, `di2008note`, `van2011quasi`, `yaglom1947certain`
(plus any other you cite). Keep `TODO(verify)` notes as they are. Add, for the
biological grounding in the discussion:

```bibtex
@article{williams2024reproduction,
  title={The reproduction number and its probability distribution for stochastic viral dynamics},
  author={Williams, Bevelynn and Carruthers, Jonathan and Gillard, Joseph J and Lythe, Grant and Perelson, Alan S and Ribeiro, Ruy M and Molina-Par{\'\i}s, Carmen and L{\'o}pez-Garc{\'\i}a, Mart{\'\i}n},
  journal={Journal of the Royal Society Interface},
  volume={21}, number={210}, pages={20230400}, year={2024}
}
@article{williams2021anthrax,
  title={A stochastic intracellular model of anthrax infection with spore germination heterogeneity},
  author={Williams, Bevelynn and L{\'o}pez-Garc{\'\i}a, Mart{\'\i}n and Gillard, Joseph J and Laws, Thomas R and Lythe, Grant and Carruthers, Jonathan and Finnie, Thomas and Molina-Par{\'\i}s, Carmen},
  journal={Frontiers in Immunology},
  volume={12}, pages={688257}, year={2021}
}
```

**Do not cite `Grant_paper.pdf` in the chapters** (user decision,
2026-08-08): it is source material and register model only. Where its
estimates or results are used, cite the primary literature instead (the
Williams entries above; Carruthers et al. via `carruthers2020stochastic`).

### 4.4 Acceptance criteria (Chapter 4a)

Compiles clean (0 errors, 0 undefined refs; 0 overfull boxes outside
figure-flag boxes — overfulls inside flag boxes are exempt, underfulls are
allowed); all source §1–10 content present and converted per §2; no
correction-history remarks; opening recap subsection with boxed formulas;
closing discussion per §4.1; appendices assembled; figures copied, every
`\includegraphics` path resolves, and flags placed; chained suite re-run at
final QA with result recorded.

---

## 5. Chapter 4b — `BDC_odes`

Source: `document MAIN/sections/11…17`, appendix material from
`A_formula_tables.tex`, `B_verification_records.tex`,
`C_technical_derivations.tex` (partial), `document MAIN/figures/*` (12 PDFs).

### 5.1 Structure and content mapping

| New section | Source | Treatment |
|---|---|---|
| §1 What we need from Chapters 3 and 4a | new, from draft 02 + draft 12's kernel subsection | Compact opening section: boxed formulas from §6 below — $I,D,\Ifix,J,K,V$; $V_\infty$; $\varphi=\delta J$ and the burst-size law; QSD; $\mathrm{E}[T_{\mathrm{prod}}]=\lambda^{-1}\log(a/(a-1))$; $g=\delta K$; the MOI kernels in two lines. Pointers to Chapters 3 and 4a; no proofs. |
| §2 Why a constant release rate fails | draft 11 + `Grant_paper.pdf` §§1–2 | Converted (β→λ etc.); BMVR citations kept. **Incorporate the paper's single-cell budding picture fluidly** as the comparator's completion: the budding cell as two independent event types (release at rate $p$, death at rate $d_{\mathcal{I}}$); $I(t)=e^{-d_{\mathcal{I}}t}$ and $V(t)=\frac{p}{d_{\mathcal{I}}}(1-I)$, equivalently $\dd V/\dd I=-p/d_{\mathcal{I}}$; lifetime release $p/d_{\mathcal{I}}$; and the geometric release law of the stochastic interpretation, $\Pr\{\mathcal{K}_{\rm bud}=k\}=\bigl(\frac{d_{\mathcal{I}}}{d_{\mathcal{I}}+p}\bigr)\bigl(\frac{p}{d_{\mathcal{I}}+p}\bigr)^k$, $k=0,1,2,\ldots$ — the contrast that makes bursting's simultaneous release-and-death structurally different. This sets up the renewal section and the spectrum comparison. |
| §3 Burst-aware renewal viral dynamics | draft 12 | Converted; kernel notation $I_{\mathrm{fix}}(a)$; the Result, replacement table, novelty remark, verification subsection ("54 checks, all passing"), overlay subsection — all kept. |
| §4 Effective parameters, R₀, identifiability | draft 13 | Converted; the appendix pointer kept (point to this chapter's Appendix C). |
| §5 Flooding advantage and growth-rate trade-off | draft 14 | Converted; tables and proofs kept. |
| §6 Spectrum of release models | draft 15 | Converted; apply §2.4 renamings ($\zeta$, $\varphi$); keep the TikZ spectrum map. |
| §7 Contrast with HIV | draft 16 | Converted; keep the TikZ stage diagram. |
| §8 Discussion | draft `17_discussion.tex` | This chapter's share: fitting-practice consequences; forward connections (Chapter 5's two-type/GATE, Chapter 6's spectrum, Chapter 7's nonlinear mechanisms — by chapter working name, flagged as forward references); open problems — flooding boundary against real parameters, population-level variance, partial-release flooding boundary in $\varphi$, two-type killed second moments, literature positioning. |
| Appendix A | draft A | Population formula table only (+ $L=1$, young-cell, $r=0$ blocks). |
| Appendix B | draft B | Renewal suite record only (54 checks; keep the honest-gap note). |
| Appendix C | draft C | Hypergeometric Laplace transforms (with the convergence caveat). |

### 5.2 Figures for Chapter 4b

Copy these 12 files from `document MAIN/figures/` into `BDC_odes/figures/` and
keep every existing reference: `kernels.pdf`, `overlay_I.pdf`, `overlay_V.pdf`,
`overlay_rel_diff.pdf`, `overlay_growth_phase.pdf`, `overlay_V_with_naive.pdf`,
`peff_dr_curves.pdf`, `D_exponential_reduction.pdf`, `E_growth_rate_match.pdf`,
`F_R0_threshold.pdf`, `H_gillespie_mu0.pdf`, `H_gillespie_mu_pos.pdf`. Keep the
two existing TikZ figures in the source (spectrum map §6, HIV stages §7) — they
are code, already written. Insert figure flags (you may add more):

- **F4b.1 — Renewal construction schematic** (§3, before the Result). TikZ:
  infection events at rate $i(t)$ start cohorts; cohorts age along an axis;
  survival weighted by $I_{\mathrm{fix}}(a)$, release weighted by $g(a)$;
  the convolutions feeding $\mathcal{I}(t)$ and $\mathcal{V}(t)$. Purpose: the
  bookkeeping of the Result in one picture.
- **F4b.2 — Flooding** (§5). Python: $z_{\mathrm{ext}}^{\mathrm{burst}}(q)$
  against $z_{\mathrm{ext}}^{\mathrm{bud}}(q)=1/m$ for the three regimes —
  $L>1$: $(\lambda,\mu,\delta)=(1,0,0.1)$; $L=1$: $(1,0.5,1/3)$; $L<1$:
  $(1,0.9,0.1)$ — using the closed forms of §6; annotate the difference
  $(L-1)(1/m-1)$ and the $m=1$ boundary. Purpose: the theorem's three regimes.
- **F4b.3 — Growth-rate trade-off** (§5). Python: at matched $R_0=2$, $c=1$,
  $d_{\mathcal{I}}=1/\mathrm{E}[T_{\mathrm{prod}}]$, $p=V_\infty d_{\mathcal{I}}$:
  paired bars of $r_{\mathrm{bud}}$ vs $r_{\mathrm{burst}}$ for the three
  parameter sets (values $0.250/0.180$, $0.395/0.294$, $0.343/0.198$ — verify
  against the characteristic equation when you write the spec into the flag).
  Purpose: the trade-off made visible.
- **F4b.4 — Partial-release continuum** (§6, optional/exploratory flag): the
  flooding criterion as a function of the boolean fraction $\varphi$ — flag
  only if you can specify it precisely; otherwise omit.

### 5.3 Bibliography for Chapter 4b

Copy from `document MAIN/references.bib` all entries cited after conversion,
including `mckendrick1926applications`, `vonfoerster1959some`,
`hataye2019principles`, `perelson1996hiv`, `nowak1996population`,
`mclean1993balance`, `pearson2011stochastic`, `gilchrist2006evolution`,
plus the single-cell entries you cite. Keep `TODO(verify)` notes as they are;
list the flagged entries in `Progress.md`.

### 5.4 Acceptance criteria (Chapter 4b)

Compiles clean (0 errors, 0 undefined refs; 0 overfull boxes outside
figure-flag boxes — overfulls inside flag boxes are exempt, underfulls are
allowed); all source §11–17 content present and converted per §2
(including §2.4 renamings); opening "what we need" section with boxed
formulas; closing discussion per §5.1; appendices assembled; 12 figures
copied and referenced, every `\includegraphics` path resolves (the draft's
paths for these 12 are already flat — no rewriting needed); two TikZ figures
intact; flags placed; renewal suite re-run at
final QA with result recorded.

---

## 6. Key formula reference (verified; use exactly)

$w=e^{\theta t}$, $\theta=\lambda(a-b)$ throughout.

**Single cell.**
$$
I(t)=\frac{aB+bAw}{B+Aw},\quad
D(t)=\frac{ab(w-1)}{aw-b},\quad
I_{\mathrm{fix}}(t)=\frac{(a-b)^2w}{(B+Aw)(aw-b)}.
$$
$$
J(t)=\frac{(a-b)^2w}{(B+Aw)^2}=-\frac{\lambda}{\delta}(I-a)(I-b),\qquad
K(t)=\Bigl[1+\frac{2\lambda}{\delta}(1-I)\Bigr]J=\frac{2\lambda}{\delta}(\kappa-I)J.
$$
$$
V(t)=(1-I)\Bigl[1+\frac{\lambda}{\delta}(1-I)\Bigr],\qquad
V_\infty=\frac{aB}{A}=\frac{\lambda-\mu}{\delta}(1-b)+1.
$$
$$
\mathrm{E}[\mathcal{K}\mid\text{burst}]=\frac{a}{a-1},\qquad
\mathrm{E}[W_t^2]=\frac{2(\lambda-\mu)}{\delta}V-\frac{\lambda+\mu}{\delta}I-K+\frac{\lambda+\mu}{\delta}+1.
$$
$$
\varphi(t)=\delta J(t)\ (\text{mass }1-b),\qquad
\Pr\{\mathcal{K}=k\}=\frac{\delta}{\lambda}a^{-k},\qquad
\mathrm{QSD}(n)=(a-1)a^{-n}.
$$
$$
\mathrm{E}[T_{\mathrm{prod}}]=\int_0^\infty I_{\mathrm{fix}}
=\frac{1}{\lambda}\log\frac{a}{a-1},\qquad
K(I)=\frac{2\lambda^2}{\delta^2}(I-\kappa)(I-a)(I-b).
$$
Conditional rupture times (from `Grant_paper.pdf`, translated to the unified
regime, verified by simulation 2026-08-08): with $\mu=0$ and
$\theta=\lambda+\delta$,
$$
\mathrm{E}[\tau\mid\mathcal{K}=n]=\frac{1}{\theta}\sum_{k=1}^{n}\frac{1}{k}
\simeq\frac{\log n+\gamma}{\theta}\quad(n\gg1),\qquad
p_n(t)\ \text{maximised at}\ t_n=\frac{\log n}{\theta};
$$
with $\mu>0$, the mean burst time conditioned on bursting is
$$
\mathrm{E}[\tau\mid\text{burst}]=\frac{1}{\lambda(1-b)}\log\frac{a-b}{a-1}
$$
(distinct from $\mathrm{E}[T_{\mathrm{prod}}]$; both reduce to
$\lambda^{-1}\log(1+\lambda/\delta)$ as $\mu\to0$).
**MOI ($k$ founders):** $I_k=I^k$, $D_k=D^k$, $I_{\mathrm{fix},k}=I^k-D^k$;
$J_k=kI^{k-1}J$; $K_k=kKI^{k-1}+k(k-1)J^2I^{k-2}$; $g_k=\delta K_k$;
$V_\infty^{(k)}=k+\lambda/\delta$ when $\mu=0$.

**Chained transfer ($\mu=0$):** $s=\delta/(\lambda+\delta)$,
$\rho=\lambda/(\lambda+\delta)$;
$\Pr\{r_k=n\}=\binom{n+k-2}{k-1}s^k\rho^{n-1}$;
$\mathrm{E}[r_k]=1+k\lambda/\delta$; $\mathrm{Var}(r_k)=k\rho/s^2$;
$\mathrm{E}[z^{r_k}]=z(s/(1-\rho z))^k$;
$\widetilde{T}(k,u)=\frac{sk}{k+u'}\,{}_2F_1(k+1,1;k+1+u';\rho)$,
$u'=u/(\lambda+\delta)$; $\mathrm{E}[T(k)]=\sum_{m\ge0}\rho^m/((\lambda+\delta)(k+m))$.

**Population (Chapter 4b).**
$$
\mathcal{I}=\mathcal{I}_0 I_{\mathrm{fix}}+i*I_{\mathrm{fix}},\quad
\dot{\mathcal{V}}=\mathcal{I}_0 g+i*g-c\mathcal{V},\quad i=\gamma T\mathcal{V},\quad g=\delta K.
$$
$$
p_{\mathrm{eff}}(r)=\frac{\delta\widetilde{K}(r)}{\widetilde{I_{\mathrm{fix}}}(r)},
\qquad
d_{\mathcal{I},\mathrm{eff}}(r)=\frac{1}{\widetilde{I_{\mathrm{fix}}}(r)}-r.
$$
Limits: $r=0$: $p_{\mathrm{eff}}=\lambda V_\infty/\log(a/(a-1))$,
$d_{\mathrm{eff}}=\lambda/\log(a/(a-1))$; $r\to\infty$: $p_{\mathrm{eff}}\to\delta$,
$d_{\mathrm{eff}}\to\mu+\delta$. Characteristic equation
$r+c=\gamma T\delta\widetilde{K}(r)$; $R_0^{\mathrm{ODE}}=\gamma T V_\infty/c$;
branching mean $m=qV_\infty$, $q=\gamma T/(\gamma T+c)$.
$$
G_{\mathrm{off}}(z)=b+\frac{\delta}{\lambda}\frac{y}{a-y},\ y=1-q+qz;\qquad
z_{\mathrm{ext}}^{\mathrm{burst}}=\frac{a(1-q+qb)-1+q}{q};
$$
$$
z_{\mathrm{ext}}^{\mathrm{burst}}-z_{\mathrm{ext}}^{\mathrm{bud}}=(L-1)\Bigl(\frac1m-1\Bigr),\
L=a(1-b);\quad
\mathrm{Var}_{\mathrm{bud}}-\mathrm{Var}_{\mathrm{burst}}=\frac{2q^2V_\infty(L-1)}{a-1}.
$$

---

## 7. The figure-flag system

Figures are generated later by a different agent. Your job is to place
**visible flags** in the LaTeX so they appear in the compiled PDFs, each
carrying a complete generation specification. Put this macro in every
`main.tex`:

```latex
% Figure flag: a compiled-in specification for a figure to be generated
% later by a figure agent. Do not remove until the figure exists.
% Overfull boxes INSIDE flag boxes are exempt from the overfull-free
% acceptance criterion (raggedright + small keep them rare anyway).
\newcommand{\figureflag}[3]{\par\medskip\noindent
\fcolorbox{orange!70!black}{orange!6}{\parbox{0.94\linewidth}{%
\raggedright\small
\textbf{\textcolor{orange!50!black}{FIGURE FLAG #1 --- #2}}\\[2pt]#3\par}}%
\par\medskip}
```

Usage: `\figureflag{F3.3}{Fixation functions}{...spec...}`.

**ID scheme:** `F3.n`, `F4a.n`, `F4b.n`, numbered in order of appearance.

**Every flag spec must contain:** (1) *Purpose* — why the figure materially
improves its section; (2) *Type* — TikZ schematic / Python analytic plot /
Python simulation / parameter sweep; (3) *Exact content* — every curve,
formula, and parameter value (from §6 or stated explicitly); (4) *Axes and
labels* — axis variables, ranges, legend entries; (5) *Style* — unified
Python style: default matplotlib with `tab:` colours, grid alpha 0.25,
`tight_layout`, PDF output, fonts matching the chapter (or "TikZ, inline with
chapter fonts"); (6) *Data source* — analytic formulas to evaluate, or the
existing script to adapt (named), or simulation recipe (algorithm + counts);
(7) *Placement* — the section/figure environment it belongs to.

**Existing figures are not flagged** — they are copied and kept (upgrades,
where worthwhile, get an *upgrade flag* saying so, e.g. F3.6).

Keep a registry of every flag (ID, title, section, one-line purpose) in
`Progress.md` **Log C (Figure-flag registry)**. Log C is the placement
registry only; the full generation specs live in §§3.4, 4.2, 5.2.

---

## 8. Prose standard (binding)

Two references govern the prose, and both apply to every sentence written or
rewritten:

1. **The `/aa-flow-lucid` skill.** Invoke it at the start of each writing
   phase. Non-negotiables: continuous academic flow (no bullet-point thinking
   in prose); laddered complexity; stable notation and terminology (once a
   symbol is named, never vary it); assumptions and uncertainty located
   explicitly; model conclusions kept distinct from biological claims;
   British English; academic "we"; no popular-science chattiness, no AI-prose
   tells.
2. **`Grant_paper.pdf` as the register model.** It is polished, co-authored
   prose and mathematical writing on exactly this material: imitate its
   clarity, its sentence economy, and the way its equations are introduced
   and followed through (the budding section and the four-function bursting
   development are the best models).

The chapters are thesis chapters, not a succinct paper: they are naturally
**more expansive** than the paper — more motivation, more connective tissue
between results, more step-by-step exposition, and space for the discursive
passages the thesis already has. Expansive must never mean looser: every
extra sentence must carry the reader forward, and every formula must be
integrated into the prose, not displayed and abandoned. The result must read
as final-draft chapters of a rigorous interdisciplinary applied-mathematics
PhD thesis — not notes, not a lightly edited draft, not a paper stretched
thin. Mathematical exposition keeps the author's existing voice where the
draft already has one (it is largely there); your work is integration,
consistency, and polish.

## 9. Out of scope

Thesis Chapters 1, 5, 6, 7 and their errata; any editing of `new_notes*/`,
`document MAIN/`, `3 BDC core/`, `figures/`, `N=2 Immediate Transfer
content/`, `CHAPTER4_PLAN.md`; new figure generation; web searches; deletion
of the stale `3 BDC core/` duplicate; resolution of thesis-wide chapter
numbering.
