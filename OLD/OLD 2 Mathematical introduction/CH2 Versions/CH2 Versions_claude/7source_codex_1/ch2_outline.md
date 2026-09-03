# Chapter 2 outline, source audit and correction record

## Delivered design

The chapter has two mathematical spines.

1. A branching spine develops Galton–Watson extinction, critical power laws,
   conditioning on survival, quasi-stationarity, small founding populations,
   continuous-time birth–death, killed birth–death–catastrophe processes, and the
   survival amplitude \(A(p)\).
2. A jump-process spine introduces only the CTMC/PGF machinery needed to derive and
   solve transfer, transfer–death, and transfer–birth–death generating-function
   PDEs by characteristics.

The CTMC/PGF toolkit occupies Sections 2.2.1–2.2.3, approximately three pages in
the standalone build. Distinctive calculations are proved in the main text.
Longer secondary calculations are in chapter-local appendices 2.A–2.C.

## Section map

| Section | Purpose | Principal source role |
|---|---|---|
| 2.1 | One-page motivation, two-spine roadmap, notation | Recomposition of seed introduction; AA hooks |
| 2.2 | Exponential clocks, races, CTMC generator conventions, forward equations, PGFs | Minimal toolkit selected from **topics_index**; not seed replacement |
| 2.3 | General and binary Galton–Watson processes, extinction, critical survival, extinction time, total progeny | **Ch2_seed** Section 2 |
| 2.4 | QSD/Yaglom definitions, \(A(p)\), conditional mean and variance, Riccati guide | **Ch2_seed** Section 3; QSD hook |
| 2.5 | Founding size, rupture exposure, continuous birth–death, killed BDC generator | **Ch2_seed** Section 4; BDC hook |
| 2.6 | Product and series for \(A(p)\), bounds, endpoint, near-critical theorem, continuous-time comparison, Koenigs representation | **Ch2_seed** Section 5 |
| 2.7 | Transfer models, PGF PDEs, checked characteristics, hypergeometric solution, regular integral representation, coefficients | **Ch2_seed** Section 6; method-of-characteristics hook |
| 2.A | Symbolic-regression records, quadratic conjugacy, elementary comparison cases | Secondary material from **Ch2_seed** Section 5 |
| 2.B | Full proof of the exponential–rational hypergeometric integral | **Ch2_seed** Section 7 |
| 2.C | Full coefficient extraction, trinomial cases, ABD convolution coefficients | **Ch2_seed** Section 7 |

## Seed-coverage audit

| Seed block | Coverage | Notes |
|---|---|---|
| **01_introduction.tex** | Covered in 2.1 | Application narrative removed; mathematical roadmap retained |
| **02_galton_watson.tex** | Covered in 2.3 | General PGF iteration, binary recursion, extinction threshold, critical \(2/n\), infinite mean extinction time, lifetime and progeny exponents retained |
| **03_quasi_stationarity.tex** | Covered in 2.4 and 2.6 | Survival scale, conditional moments and Riccati calculation retained; second moment derived by conditional branching rather than the longer nested-MGF calculation |
| **04_small_populations.tex** | Covered in 2.5 and 2.6 | Early survival, \(k\) founders, rupture exposure, continuous birth–death and \(A_{\mathrm c}\) retained |
| **05_constant_A.tex** | Covered in 2.6 and Appendix 2.A | Product, series, bounds, parity, table, asymptotic, comparison, fitted candidates, Koenigs value, conjugacy and elementary cases retained |
| **06_method_of_characteristics.tex** | Covered in 2.7 | All three jump models, forward equations, PDEs, characteristic test, ABD closed form, hypergeometric reduction, domain and resonance retained |
| **07_appendices.tex** | Covered in Appendices 2.B–2.C | Hypergeometric identity and coefficient extraction retained with full proofs |

The following seed figures were omitted as mathematically non-essential: the
period-doubling overview and the separate harmonic-series illustration. Their
mathematical statements remain in the text. The topic index was used only to
select the compact toolkit; no inference, sensitivity, spatial, phase-type or
simulation encyclopaedia was imported.

## Material mathematical corrections and sharpened labels

1. **Endpoint definition.** \(A(0)\) is defined by the right limit. The raw ratio
   \(S_n/(2p)^n\) is not defined at \(p=0\).
2. **Critical survival.** The statement \(S_n\sim2/n\) is proved from reciprocal
   increments. The Riccati equation is explicitly an approximation and is not
   used as a proof.
3. **Quasi-stationarity.** Existence of the binary Yaglom limit is attributed to
   the branching-process theorem. Convergence of the first two moments is not
   presented as proof of convergence of the full conditional law.
4. **Moment asymptotics.** The exact second-moment recurrence and solution are
   used. Decaying terms are described by asymptotic equivalence rather than as a
   non-zero limiting variance.
5. **Total progeny.** The \(3/2\) exponent is stated on the admissible odd support;
   even total population sizes have probability zero.
6. **Rupture exposure.** With death, the no-rupture probability is the path
   expectation \(\mathbb E[(1-\kappa)^{H_n}]\). Substitution of the mean exposure
   is a Jensen lower bound, not an identity. Non-rupture is distinguished from
   joint non-rupture and population survival.
7. **CTMC convention.** The generator is explicitly indexed as rate from \(i\) to
   \(j\); row-vector forward and matrix backward equations are stated separately.
8. **Continuous birth–death.** The finite-time extinction formula is derived from
   the backward Riccati equation, including the equal-rate case and its conditional
   mean.
9. **Killed BDC setup.** A state-dependent catastrophe rate is formulated through
   a killed subgenerator. The QSD left-eigenvector relation and absorption decay
   rate are derived. Constant killing is separated from state-dependent killing.
10. **Certified computation of \(A\).** Partial products carry an explicit lower
    and upper tail bracket. The table's factor counts are regenerated at relative
    bracket tolerance \(10^{-14}\).
11. **Near-critical asymptotic.** The leading constant is proved with relative
    error \(O(\varepsilon\log(1/\varepsilon))\). The numerical next-order constant
    is labelled empirical.
12. **Discrete/continuous comparison.** Endpoint ratios are proved. The observed
    monotonicity of \(A/A_{\mathrm c}\) is labelled numerical and is not promoted to
    a theorem.
13. **Hypertranscendence.** Becker–Bergweiler is applied to the fixed-parameter
    function \(z\mapsto\psi_r(z)\). It is not used to claim that
    \(p\mapsto A(p)\) is non-elementary.
14. **Exceptional logistic parameters.** The \(r=2\) and \(r=4\) elementary
    linearisers are identified as repelling comparison cases outside the
    subcritical branching window.
15. **Rate degeneracies.** The transfer–death formula includes the removable
    case \(\alpha=\mu\). The transfer–birth–death calculation includes a regular
    representation at \(\beta=\mu\).
16. **Hypergeometric domains.** The subcritical series domain is separated from
    supercritical analytic continuation. A real transfer-time convolution fixes
    the branch and avoids the coordinate singularity at \(x=\mu/\beta\).
17. **Resonance.** Poles in the separated \(\Psi\)-terms are shown to cancel in
    the full PGF. Resonance is a removable defect of the antiderivative, not a
    singularity of the stochastic model.
18. **Fitted formulae.** \(\widehat A_1,\ldots,\widehat A_4\) are retained only as
    exploratory approximations and tested against the proved critical endpoint
    behaviour.

## Source roles

- **Seed authority:** all substantive seed mathematics is carried into the main
  chapter or chapter-local appendices.
- **Topic-index use:** only exponential clocks, CTMC generators/forward equations,
  and PGF identities were selected to make the chapter self-contained.
- **Forward-reference only:** later models use the BDC killed-generator and rupture
  ideas, but their parameter catalogues and later results are not pre-empted.
- **Primary attribution:** Yaglom's 1947 paper, Koenigs' 1884 paper, and
  Becker–Bergweiler's 1995 classification are cited directly. Standard branching
  and CTMC facts are supported by the cited monographs.

## Verification record

The final handoff checks are:

~~~sh
sh scripts/run_checks.sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
~~~

The scripts reproduce the amplitude table and conditional-mean data; check the
second-moment, telescoping-product, conjugacy, factorisation and Pochhammer
identities in exact rational arithmetic; verify coefficient normalisation; and
compare the transfer–birth–death PGF with a truncated master equation in
subcritical, supercritical and equal-rate cases.

The final run completed successfully. All reproducibility checks passed; a clean
pdfLaTeX/BibTeX build produced a 41-page A4 PDF; and the log contained no
undefined citations or references, overfull or underfull boxes, or other LaTeX
warnings. All 41 pages were rendered to images and visually inspected, with
full-size checks of the densest derivations, tables, figures and appendices.
