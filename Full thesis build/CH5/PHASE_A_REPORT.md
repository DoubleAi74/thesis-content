# Chapter 5 — Phase A report

**Scope.** Structure, content, mathematics, hygiene, compile. Prose polish,
flow and cadence are Phase B's and were not attempted. Science is frozen apart
from the three licensed additions of plan §6.

**Build.** `latexmk -pdf main.tex`, exit 0.

| | result | criterion |
|---|---|---|
| Overfull boxes | **0** | 0 |
| Underfull boxes | **0** | 0 |
| Undefined citations | **0** | 0 |
| Undefined references, non-`m:` | **0** | 0 |
| Undefined references, `m:…` | 11 | licensed — Chapter 2 labels, standalone compile |
| Body pages | **30** | ≤ 30 ✓ |
| Total pages | **38** | ≤ 36 ✗ (+2) |
| Figures | 14, all cross-referenced | ~13, all cross-referenced |
| `$$` in section files | **0** | 0 (55 in source) |
| Chapter numbers / "Part II" in prose | **0** | 0 (39 in source) |
| Ledger check | **PASS** | — |
| Recheck script | 42 values, **0 mismatches**; 3 key checks PASS | — |
| Preservation passages | **6 of 6 found** | 6 |

---

## 1. Files written

All under `Chapter numbers/CH5_REWRITE/`. Nothing outside it was created or
modified.

**Architecture** (CH2's three-file split)
- `preamble.tex` — packages, ~22 macros, `cleveref` with CH2's four `\crefformat`
  declarations verbatim, `\newtheorem{theorem}{Theorem}[chapter]`,
  `\graphicspath{{figures/}}`, the five `\Ch*` cross-chapter macros and `\fwd`
- `chapter.tex` — thesis-ready fragment opening `\chapter{…}\label{dist:ch:distribution-theory}`
- `main.tex` — `report`-class standalone wrapper, `a4paper`

**Sections** (twelve, renamed for their contents)
`01_introduction` · `02_recap` · `03_generating_function` · `04_geometric` ·
`05_quasi_stationary` · `06_burst_size` · `07_burst_time` ·
`08_conditional_means` · `09_several_founders` · `10_chained_transfer` ·
`11_bursting_budding` · `12_discussion`

**Appendices** `A_formula_table` · `B_verification_record` · `C_technical_derivations`

**Records**
- `CH5_invariants.md` — the ledger: 112 `EQ-*`, 45 `NUM-*`, 6 `TAB-*`, 18 figure
  rows, every formal statement, old label → new label, status, and a `VERIFIED`
  line for every deferral
- `CH5_figure_workorder.md` — plan §11.5
- `notes/ch5_handoffs.md` — plan §16, seven entries
- `PHASE_A_REPORT.md` — this file

**Verification**
- `verification/recheck_numbers.py` — 42 numerical claims recomputed from closed
  forms, plus the three named checks of plan §3.3
- `verification/ledger_check.sh` — greps every new label, every Chapter 2
  deferral target and every preservation passage; prints the table below
- `verification/wordcount.py` — the counter used for the budget table
- `verification/verify_chained_transfer.py` + its report, metrics JSON and
  figures — copied from `Thesis content 🎓 /OLD/4 BDC additional and BMVR/N=2
  Immediate Transfer content/`, **not re-run** (plan §18)

**Figures** `figures/` — twelve re-placed PDFs, plus
`fig01_two_mechanisms/` (built) and `fig02_late_burst_mean/` (regenerated),
each with `README.md`, `caption.md`, `meta.json`, `src/`, PDF and PNG; and
`figures/_style/style_rc.py`, a replacement for a missing upstream module.

---

## 2. Word and page counts against plan §4

Word counts use `verification/wordcount.py`: displayed maths and `tabular`
bodies removed, captions and proofs kept, each inline `$…$` counted as one
word. Run against the source chapter that counter returns 9,046 body words
where the plan says 8,696, so it reads about 9 % high; the **adj** column
divides by 1.09 to compare like with like. Both columns are given so the
correction is visible rather than assumed.

| § | Section | pages | raw | adj | target | diff |
|---|---|---|---|---|---|---|
| 1 | Introduction | 3–4 | 1139 | 1045 | 1100 | -55 |
| 2 | What we need from \ChCore | 5–7 | 576 | 528 | 400 | +128 |
| 3 | The generating function | 8–9 | 801 | 735 | 700 | +35 |
| 4 | The load is geometric at every time | 10–11 | 512 | 470 | 450 | +20 |
| 5 | The quasi-stationary distribution | 12–14 | 1106 | 1015 | 950 | +65 |
| 6 | Burst size, and why it is the QS law | 15–17 | 1028 | 943 | 850 | +93 |
| 7 | Burst time | 18–21 | 794 | 728 | 800 | -72 |
| 8 | Conditional burst means | 22 | 508 | 466 | 450 | +16 |
| 9 | Several founders | 23–25 | 899 | 825 | 750 | +75 |
| 10 | Chained immediate transfer | 26–27 | 889 | 816 | 700 | +116 |
| 11 | Bursting against budding | 28–29 | 580 | 532 | 500 | +32 |
| 12 | Discussion | 30–32 | 1187 | 1089 | 1000 | +89 |
| A | Master formula table | 33 | 118 | 108 | — | — |
| B | Verification record | 33 | 206 | 189 | — | — |
| C | Technical derivations | 34–37 | 575 | 528 | — | — |
| | **Body total** | **3–32 (30 pp)** | | **9192** | **8650** | **+542** |

### The two budget misses

**§2 is 528 words against a 400 target (+128), the largest per-section
overage.** The cause is structural, not stylistic. Plan §4.2 asks §2 to keep
the notation table, the process definition and joint process, the roots and
the $AB$ identity, and to point the closed forms at Appendix A. But eight of
those closed forms — `dist:eq:idihat`, `dist:eq:riccati`, `dist:eq:j`,
`dist:eq:k`, `dist:eq:v`, `dist:eq:vinf`, `dist:eq:ab`, `dist:eq:ew2` — are
`\cref`-ed by later sections and by four proofs. Appendix A is a table and
carries no equation numbers, so removing the displays from §2 would either
leave dangling references or require numbering them twice. They stay in §2,
compressed into two `align` blocks rather than six separate displays, and the
prose around them is what exceeds budget. The section is nonetheless down from
842 raw words to 576, and holds a notation table grown from 15 rows to 28 —
plan §4.2 requires every symbol appearing in more than one section — in the
same 3 pp the source spent.

**The chapter is 38 pages against a 36 target (+2), with the body exactly on
budget at 30.** The arithmetic: front matter 2 pp (title page, contents) +
body 30 pp + appendices 5 pp + bibliography 1 pp = 38. The source was 2 + 34 +
4 + 1 = 41. Body came down by the full four pages the plan asked for. The
appendices went **up** by one, because the plan itself moves content into
them: §10.5–10.6 to Appendix C.3 (plan §4.10), §10.7 folded into Appendix B,
and a provenance column added to Appendix A (plan §4.13). A 36-page total with
a 30-page body would require the non-body matter to fit in 6 pp; it occupies
8. This is not recoverable by trimming prose, and no content was cut to chase
it.

---

## 3. Ledger check, in full

`bash verification/ledger_check.sh` — exit 0.

Section 1 lists every `dist:` label: whether it is defined exactly once, and
how many times it is `\cref`-ed. **"never referenced" is not a defect for a
sectioning or equation label** — plan §7.2 requires every section and
subsection to *carry* a label, not to be pointed at, and a numbered display is
available for reference whether or not this chapter uses it. It *would* be a
defect for a figure, and plan §15 item 9 requires every figure to be called
out: all fourteen are.

Status against the ledger (`CH5_invariants.md`), counted from its `STATUS`
lines: **112 `EQ-*` entries and 45 `NUM-*` rows**. 108 carry a verbatim status
(103 plain `verbatim`, plus three `verbatim, proof verbatim`, one `verbatim
statement` and one `verbatim mathematics`); 8 are `moved`, meaning the same
text in a different section or appendix; 4 are `deferred`; 2 are `**promoted**`
(the geometric theorem and the normalisation corollary, promoted from
unnumbered subsections without change to their mathematics); 3 are the licensed
additions. **Five equation entries are `altered`** — EQ-022 and EQ-023 under
SUB-1, EQ-103 and EQ-104 under SUB-3, EQ-111 under SUB-2 — and PROP-002 carries
SUB-4 and SUB-5 on the absorbed Chapter 2 block. Every alteration is one of the
five permitted substitutions; **nothing is altered outside that list**.

| Permitted substitution | Where | Ledger |
|---|---|---|
| SUB-1 $\tau\to\xi$, characteristic coordinate | §3.2 | EQ-022, EQ-023 |
| SUB-2 $K_i\to C_i$, Appendix C binomial constants | C.2 | EQ-111 |
| SUB-3 $P_1(m,u)\to\Pi(m,u)$, Laplace product | C.3 | EQ-103, EQ-104 |
| SUB-4 $T_0\to T_{\rm fix}$, $\kappa_i\to\delta i$ | §5.3 | PROP-002 |
| SUB-5 $K\to\mathcal Q$, $\theta\to\vartheta$ | §5.3 | PROP-002 |

Six items leave this chapter and are carried elsewhere — the four marked
`deferred`, the $\E{W_t^2}$ entry whose formula stays boxed here while its
derivation goes to \ChCore, and the ${}_2F_1$ antiderivative, which stays in
Appendix C.2 but now cites the Chapter 2 result it had been using without
attribution. Each carries the grep that proves the target resolves:

| Deferred | Carried by | File |
|---|---|---|
| Coefficient-extraction formula (was `stateFormula`) | `m:eq:stateProb`, `m:app:extract` | `CH2/sections/app_d_coefficient_extraction.tex` |
| Initial-curve choice (was `ICs`) | `m:sec:moc`, `m:eq:genericcharacteristics` | `CH2/sections/04_method_of_characteristics.tex` |
| Generic characteristic system (was `Char1`) | `m:eq:genericcharacteristics`, `m:fig:characteristics` | `CH2/sections/04_method_of_characteristics.tex` |
| ${}_2F_1$ antiderivative | `m:app:hyp`, `m:prop:hypIden`, `m:eq:hypIden` | `CH2/sections/app_c_hypergeometric_identity.tex` |
| Quasi-stationarity, Yaglom limit | `m:def:qsd`, `m:sec:condmeans` | `CH2/sections/03_methods.tex` |
| $\E{W_t^2}$ **derivation** (formula stays boxed) | `\ChCore` prose — see deviation 8 | `CH4/sections/08_variance_and_standard_deviation_of.tex`, `thm:Wsq` L156, `eq:Wsq` L159 |

Full output:

```text

1. NEW LABELS  (defined in sections/, and referenced at least once)
============================================================================
LABEL                              DEFINED    REFS       STATUS
----------------------------------------------------------------------------
dist:app:chained-transforms        1          3          ok
dist:app:extract                   1          2          ok
dist:app:formulae                  1          2          ok
dist:app:technical                 1          0          ok (never referenced)
dist:app:verification              1          2          ok
dist:app:vk                        1          1          ok
dist:cor:sum                       1          2          ok
dist:def:bdc                       1          0          ok (never referenced)
dist:def:fixation                  1          0          ok (never referenced)
dist:eq:ab                         1          3          ok
dist:eq:abtheta                    1          1          ok
dist:eq:antideriv                  1          1          ok
dist:eq:arec                       1          0          ok (never referenced)
dist:eq:bud                        1          0          ok (never referenced)
dist:eq:budgeom                    1          1          ok
dist:eq:burstintegral              1          2          ok
dist:eq:burstlaw                   1          4          ok
dist:eq:burstlawcond               1          1          ok
dist:eq:catpde                     1          1          ok
dist:eq:cexpand                    1          1          ok
dist:eq:clockchange                1          0          ok (never referenced)
dist:eq:condcdf                    1          0          ok (never referenced)
dist:eq:condgeom                   1          0          ok (never referenced)
dist:eq:condp                      1          1          ok
dist:eq:consistent                 1          0          ok (never referenced)
dist:eq:conventions                1          0          ok (never referenced)
dist:eq:decaycheck                 1          0          ok (never referenced)
dist:eq:decayrate                  1          1          ok
dist:eq:dnG                        1          0          ok (never referenced)
dist:eq:ew2                        1          1          ok
dist:eq:fixprob                    1          0          ok (never referenced)
dist:eq:gcat                       1          3          ok
dist:eq:gdef                       1          0          ok (never referenced)
dist:eq:genfix                     1          1          ok
dist:eq:geometric                  1          1          ok
dist:eq:geomevents                 1          1          ok
dist:eq:gk                         1          2          ok
dist:eq:gkflux                     1          4          ok
dist:eq:gkgamma                    1          0          ok (never referenced)
dist:eq:gkill                      1          0          ok (never referenced)
dist:eq:gumbel                     1          0          ok (never referenced)
dist:eq:hypantideriv               1          0          ok (never referenced)
dist:eq:idefs                      1          0          ok (never referenced)
dist:eq:idihat                     1          4          ok
dist:eq:ifixdef                    1          0          ok (never referenced)
dist:eq:ihatk                      1          1          ok
dist:eq:j                          1          0          ok (never referenced)
dist:eq:jk                         1          0          ok (never referenced)
dist:eq:k                          1          0          ok (never referenced)
dist:eq:kcond                      1          2          ok
dist:eq:kdecomp                    1          0          ok (never referenced)
dist:eq:killpde                    1          1          ok
dist:eq:kk                         1          1          ok
dist:eq:kolmogorov                 1          0          ok (never referenced)
dist:eq:kolmogorovcat              1          0          ok (never referenced)
dist:eq:latelimit                  1          1          ok
dist:eq:latemean                   1          1          ok
dist:eq:lt2                        1          0          ok (never referenced)
dist:eq:ltk                        1          1          ok
dist:eq:ltkhyp                     1          0          ok (never referenced)
dist:eq:meank                      1          0          ok (never referenced)
dist:eq:meant                      1          1          ok
dist:eq:patient                    1          0          ok (never referenced)
dist:eq:pdef                       1          2          ok
dist:eq:phi                        1          2          ok
dist:eq:phidefect                  1          0          ok (never referenced)
dist:eq:pkintegral                 1          0          ok (never referenced)
dist:eq:plimits                    1          0          ok (never referenced)
dist:eq:pnsum                      1          0          ok (never referenced)
dist:eq:ponelaw                    1          0          ok (never referenced)
dist:eq:qsd                        1          4          ok
dist:eq:qsddef                     1          0          ok (never referenced)
dist:eq:qsmoments                  1          1          ok
dist:eq:r1                         1          0          ok (never referenced)
dist:eq:r234                       1          0          ok (never referenced)
dist:eq:riccati                    1          3          ok
dist:eq:rkdecomp                   1          6          ok
dist:eq:rkgf                       1          0          ok (never referenced)
dist:eq:rklaw                      1          5          ok
dist:eq:rkmoments                  1          0          ok (never referenced)
dist:eq:roots                      1          1          ok
dist:eq:sinv                       1          1          ok
dist:eq:sizebias                   1          2          ok
dist:eq:srho                       1          0          ok (never referenced)
dist:eq:stateprob                  1          4          ok
dist:eq:survivalloss               1          1          ok
dist:eq:t1m                        1          0          ok (never referenced)
dist:eq:t2cond                     1          0          ok (never referenced)
dist:eq:tauburst                   1          2          ok
dist:eq:taugivenk                  1          2          ok
dist:eq:taugivenkasymp             1          0          ok (never referenced)
dist:eq:telescope                  1          0          ok (never referenced)
dist:eq:tkdecomp                   1          0          ok (never referenced)
dist:eq:tn                         1          0          ok (never referenced)
dist:eq:tprod                      1          1          ok
dist:eq:tprodint                   1          0          ok (never referenced)
dist:eq:v                          1          0          ok (never referenced)
dist:eq:vinf                       1          5          ok
dist:eq:vk                         1          3          ok
dist:eq:vk1                        1          0          ok (never referenced)
dist:eq:vkmuzero                   1          1          ok
dist:eq:voveri                     1          0          ok (never referenced)
dist:eq:wdef                       1          0          ok (never referenced)
dist:eq:zchar                      1          1          ok
dist:eq:zHGk                       1          0          ok (never referenced)
dist:eq:zsolve                     1          0          ok (never referenced)
dist:fig:budding                   1          1          ok
dist:fig:bursttime                 1          1          ok
dist:fig:chained                   1          1          ok
dist:fig:joint                     1          1          ok
dist:fig:jointtauk                 1          1          ok
dist:fig:latemean                  1          1          ok
dist:fig:lifetime                  1          1          ok
dist:fig:moi                       1          1          ok
dist:fig:qsmeans                   1          1          ok
dist:fig:slide                     1          1          ok
dist:fig:subextensive              1          1          ok
dist:fig:taugivenk                 1          1          ok
dist:fig:threemeans                1          1          ok
dist:fig:two-mechanisms            1          1          ok
dist:prop:conventions              1          2          ok
dist:prop:decay                    1          1          ok
dist:prop:lifetime                 1          1          ok
dist:prop:tauburst                 1          0          ok (never referenced)
dist:prop:taugivenk                1          1          ok
dist:rem:circularity               1          0          ok (never referenced)
dist:rem:coefficient               1          0          ok (never referenced)
dist:rem:criterion                 1          2          ok
dist:rem:gk                        1          1          ok
dist:rem:ihatk                     1          1          ok
dist:sec:assumptions               1          1          ok
dist:sec:budding                   1          1          ok
dist:sec:burst-law                 1          1          ok
dist:sec:burst-size                1          4          ok
dist:sec:burst-time                1          1          ok
dist:sec:burst-time-marginal       1          0          ok (never referenced)
dist:sec:chained                   1          9          ok
dist:sec:chained-scope             1          1          ok
dist:sec:characteristics           1          1          ok
dist:sec:circularity               1          0          ok (never referenced)
dist:sec:cond-means                1          2          ok
dist:sec:conditioning              1          0          ok (never referenced)
dist:sec:contributions             1          0          ok (never referenced)
dist:sec:conventions               1          0          ok (never referenced)
dist:sec:decay-rate                1          0          ok (never referenced)
dist:sec:discussion                1          1          ok
dist:sec:discussion-assay          1          0          ok (never referenced)
dist:sec:exports                   1          2          ok
dist:sec:geometric                 1          3          ok
dist:sec:identity                  1          0          ok (never referenced)
dist:sec:intro                     1          0          ok (never referenced)
dist:sec:key-observation           1          3          ok
dist:sec:lifetime                  1          0          ok (never referenced)
dist:sec:masterpde                 1          0          ok (never referenced)
dist:sec:moi                       1          4          ok
dist:sec:moi-fixation              1          0          ok (never referenced)
dist:sec:moi-moments               1          0          ok (never referenced)
dist:sec:moi-yield                 1          0          ok (never referenced)
dist:sec:moments-recap             1          2          ok
dist:sec:next                      1          1          ok
dist:sec:notation-tab              1          0          ok (never referenced)
dist:sec:open-problems             1          5          ok
dist:sec:overall-mean              1          0          ok (never referenced)
dist:sec:pgf                       1          3          ok
dist:sec:pgf-k-founders            1          2          ok
dist:sec:probes                    1          0          ok (never referenced)
dist:sec:process                   1          0          ok (never referenced)
dist:sec:qsd                       1          1          ok
dist:sec:qsd-geometric             1          0          ok (never referenced)
dist:sec:recap                     1          1          ok
dist:sec:roots                     1          1          ok
dist:sec:rupture-sizes             1          0          ok (never referenced)
dist:sec:rupture-times             1          0          ok (never referenced)
dist:sec:size-bias                 1          2          ok
dist:sec:sliding                   1          0          ok (never referenced)
dist:sec:sum-ihat                  1          0          ok (never referenced)
dist:sec:tau-burst-mu-pos          1          0          ok (never referenced)
dist:sec:tau-given-k               1          0          ok (never referenced)
dist:sec:two-extremes              1          1          ok
dist:tab:budburst                  1          1          ok
dist:tab:notation                  1          1          ok
dist:tab:threemeans                1          3          ok
dist:tab:twoextremes               1          2          ok
dist:thm:burst                     1          1          ok
dist:thm:geometric                 1          7          ok
dist:thm:identity                  1          3          ok
dist:thm:qsd                       1          3          ok

2. CHAPTER 2 DEFERRAL TARGETS  (must resolve in CH2/sections/)
============================================================================
LABEL                              FILE
----------------------------------------------------------------------------
m:sec:moc                          04_method_of_characteristics.tex 
m:eq:genericcharacteristics        04_method_of_characteristics.tex 
m:fig:characteristics              04_method_of_characteristics.tex 
m:app:extract                      app_d_coefficient_extraction.tex 
m:eq:stateProb                     app_d_coefficient_extraction.tex 
m:app:hyp                          app_c_hypergeometric_identity.tex 
m:prop:hypIden                     app_c_hypergeometric_identity.tex 
m:eq:hypIden                       app_c_hypergeometric_identity.tex 
m:def:qsd                          03_methods.tex 
m:sec:condmeans                    03_methods.tex 

3. PRESERVATION LIST  (plan section 13; grep on opening words)
============================================================================
#   PASSAGE                                        FOUND IN
----------------------------------------------------------------------------
1   black-box opening                              01_introduction.tex 
2   answers in advance                             01_introduction.tex 
3a  Icarus passage                                 05_quasi_stationary.tex 
3b  Icarus callback                                05_quasi_stationary.tex 
4   circularity diagnosis                          08_conditional_means.tex 
5a  rem:ihatk trap                                 09_several_founders.tex 
5b  rem:gk trap                                    09_several_founders.tex 
6   budding/bursting contrast                      11_bursting_budding.tex 

4. HYGIENE
============================================================================
Chapter[~ ][0-9]               ok
Part II                        ok
\$\$                           ok
\\Secref                       ok
\\Figref                       ok
\\Eqref                        ok
\\Tabref                       ok
\\Chapref                      ok
\\eqref                        ok
\\figureflag                   ok
\\noindent                     ok
\\vspace                       ok
figures included               14

RESULT
============================================================================
ledger check: PASS
```

---

## 4. Recheck script

`python3 verification/recheck_numbers.py` — exit 0. **42 quoted values, 0
mismatches. All three named checks of plan §3.3 pass.**

The three that matter, and what they license:

1. **$p_1(t)=P'(t)/\lambda$** — licensed addition (b) rests on it. Checked at
   $t=0.3,1,3,8$ across four parameter sets. A double-precision central
   difference fails at $(2,0.1,0.7)$, $t=8$, where $p_1\approx5.7\times10^{-10}$
   and cancellation swamps the derivative; the check is therefore run in
   60-digit decimal arithmetic with step $10^{-15}$. **Worst relative
   discrepancy $1.3\times10^{-30}$.**
2. **$\vartheta=\mu\nu_1+\sum_i\delta i\,\nu_i=\lambda(a-b)$** — licensed
   addition (c), the absorbed Chapter 2 block, rests on it. Four parameter
   sets, **worst relative error $8.1\times10^{-16}$**; the algebraic route of
   plan §6.3, $\lambda b(a-1)+\lambda a(1-b)$, returns $0.873212459829=\theta$.
3. **$\Ifix_{,k}=I^k-D^k$ against $\Ifix^{\,k}$** at $(1,0.2,0.05)$, $t=1$ —
   $0.8458$ and $0.6542$, the two numbers `dist:rem:ihatk` quotes. **Both to
   four decimal places.**

Full output:

```text
==============================================================================
CHAPTER 5 --- recheck of numerical claims
==============================================================================

KEY CHECK 1.  p_1(t) = P'(t)/lambda, several t and several parameter sets
  (central difference in 60-digit decimal arithmetic, step h = 1e-15)
------------------------------------------------------------------------------
  (lam,mu,dlt)=(1.0, 0.2, 0.05)  t= 0.3  p_1=6.983649143934e-01  P'/lam=6.983649143934e-01  rel=2.67e-31
  (lam,mu,dlt)=(1.0, 0.2, 0.05)  t= 1.0  p_1=3.295808555058e-01  P'/lam=3.295808555058e-01  rel=1.93e-31
  (lam,mu,dlt)=(1.0, 0.2, 0.05)  t= 3.0  p_1=5.057291695509e-02  P'/lam=5.057291695509e-02  rel=1.37e-31
  (lam,mu,dlt)=(1.0, 0.2, 0.05)  t= 8.0  p_1=6.260437767101e-04  P'/lam=6.260437767101e-04  rel=1.27e-31
  (lam,mu,dlt)=(1.0, 0.0, 0.1)  t= 0.3  p_1=7.189237334319e-01  P'/lam=7.189237334319e-01  rel=2.02e-31
  (lam,mu,dlt)=(1.0, 0.0, 0.1)  t= 1.0  p_1=3.328710836981e-01  P'/lam=3.328710836981e-01  rel=2.02e-31
  (lam,mu,dlt)=(1.0, 0.0, 0.1)  t= 3.0  p_1=3.688316740124e-02  P'/lam=3.688316740124e-02  rel=2.02e-31
  (lam,mu,dlt)=(1.0, 0.0, 0.1)  t= 8.0  p_1=1.507330750955e-04  P'/lam=1.507330750955e-04  rel=2.02e-31
  (lam,mu,dlt)=(0.5, 0.9, 0.3)  t= 0.3  p_1=6.216338660870e-01  P'/lam=6.216338660870e-01  rel=4.61e-31
  (lam,mu,dlt)=(0.5, 0.9, 0.3)  t= 1.0  p_1=2.430230580634e-01  P'/lam=2.430230580634e-01  rel=2.91e-31
  (lam,mu,dlt)=(0.5, 0.9, 0.3)  t= 3.0  p_1=2.579671687699e-02  P'/lam=2.579671687699e-02  rel=1.93e-31
  (lam,mu,dlt)=(0.5, 0.9, 0.3)  t= 8.0  p_1=1.365914591551e-04  P'/lam=1.365914591551e-04  rel=1.82e-31
  (lam,mu,dlt)=(2.0, 0.1, 0.7)  t= 0.3  p_1=4.377494168232e-01  P'/lam=4.377494168232e-01  rel=1.26e-30
  (lam,mu,dlt)=(2.0, 0.1, 0.7)  t= 1.0  p_1=6.693409315616e-02  P'/lam=6.693409315616e-02  rel=1.19e-30
  (lam,mu,dlt)=(2.0, 0.1, 0.7)  t= 3.0  p_1=3.306599748648e-04  P'/lam=3.306599748648e-04  rel=1.17e-30
  (lam,mu,dlt)=(2.0, 0.1, 0.7)  t= 8.0  p_1=5.725403369205e-10  P'/lam=5.725403369205e-10  rel=1.17e-30
  worst relative discrepancy: 1.26e-30   PASS

KEY CHECK 2.  vartheta = mu nu_1 + sum_i delta i nu_i  equals  lambda(a-b)
------------------------------------------------------------------------------
  (lam,mu,dlt)=(1.0, 0.2, 0.05)  vartheta=0.873212459829  lambda(a-b)=0.873212459829  rel=0.00e+00
  (lam,mu,dlt)=(1.0, 0.0, 0.1)  vartheta=1.100000000000  lambda(a-b)=1.100000000000  rel=8.07e-16
  (lam,mu,dlt)=(0.5, 0.9, 0.3)  vartheta=1.044030650891  lambda(a-b)=1.044030650891  rel=2.13e-16
  (lam,mu,dlt)=(2.0, 0.1, 0.7)  vartheta=2.653299832284  lambda(a-b)=2.653299832284  rel=5.02e-16
  algebraic form  lambda b(a-1)+lambda a(1-b) = 0.873212459829 vs theta = 0.873212459829
  worst relative discrepancy: 8.07e-16   PASS

KEY CHECK 3.  Ifix_k = I^k - D^k  against  (Ifix)^k  at (1,0.2,0.05), t=1
------------------------------------------------------------------------------
  I(1)=0.927299  D(1)=0.118501
  Ifix_2 = I^2-D^2 = 0.8458   (chapter quotes 0.8458)
  (Ifix)^2         = 0.6542   (chapter quotes 0.6542)
  difference 2D(I-D) = 0.191687
  PASS

STRUCTURAL IDENTITIES
------------------------------------------------------------------------------
  sum_n p_n(t) = Ifix(t):                 max err 3.33e-16
  E[W_inf^2] at mu=0 vs (2-s)/s^2:        231.000000 vs 231.000000
  sum_k (delta/lam) a^-k = 1-b:           0.8116062299 vs 0.8116062299
  sum_k k (delta/lam) a^-k = V_infty:     13.985700 vs 13.985700
  telescoped burst law vs closed form:    max err 3.47e-18
  E[tau|K=n]/(1/theta) at n=1,5,20:        0.9091, 2.0758, 3.2707  (theta=1.1)

QUOTED-VALUE COMPARISONS
==============================================================================
ID        claim                                            quoted   recomputed  
------------------------------------------------------------------------------
NUM-001   a at (1,0.2,0.05)                                1.0616       1.0616  ok
NUM-002   b at (1,0.2,0.05)                                0.1880       0.1884  ok
NUM-003   AB = delta/lambda                            0.05000000   0.05000000  ok
NUM-004   ab = mu/lambda                               0.20000000   0.20000000  ok
NUM-005   V_infty                                         13.9857      13.9857  ok
NUM-006   E[K|burst] = a/(a-1)                            17.2321      17.2321  ok
NUM-007   late-burst limit (a+1)/(a-1)                    33.4642      33.4642  ok
NUM-008   QS variance a/(a-1)^2                                --     279.7140  ok
NUM-009   late/average burst ratio (a+1)/a at work          1.940        1.942  ok
NUM-010   late/average burst ratio (a+1)/a at anthrax       1.380        1.376  ok
NUM-011   E[T_prod]                                        2.8468       2.8468  ok
NUM-012   matched death rate d_I = 1/E[T_prod]             0.3513       0.3513  ok
NUM-013   Ifix_2 = I^2 - D^2 at t=1                        0.8458       0.8458  ok
NUM-014   (Ifix)^2 at t=1 (the wrong guess)                0.6542       0.6542  ok
NUM-015   K_2 at t=1 (true, eq. Kk)                       22.2645      22.2645  ok
NUM-016   K_2 at t=1 (free sum, wrong)                    23.3923      23.3923  ok
NUM-017   V_infty^(1)                                     13.9900      13.9857  ok
NUM-018   V_infty^(2)                                     17.4300      17.4321  ok
NUM-019   V_infty^(3)                                     18.8900      18.8930  ok
NUM-020   V_infty^(5)                                     21.0000      20.9962  ok
NUM-021   V^(1)/(1-b)                                     17.2300      17.2321  ok
NUM-022   V^(2)/(1-b^2)                                   18.0700      18.0736  ok
NUM-023   V^(3)/(1-b^3)                                   19.0200      19.0202  ok
NUM-024   V^(5)/(1-b^5)                                   21.0000      21.0012  ok
NUM-025   2 V_infty (naive scaling)                       27.9700      27.9714  ok
NUM-026   V_infty^(k)=k+lambda/delta at mu=0, (1,0,0.1), k=1..5         --     7.11e-15  ok
NUM-027   budding Pr{K=0} at matched mean                  0.0548       0.0548  ok
NUM-028   E[T(1)] at (lam,dlt)=(1,1)                        0.693        0.693  ok
NUM-029   E[T(2)]                                           0.386        0.386  ok
NUM-030   E[T(3)]                                           0.273        0.273  ok
NUM-031   E[T(4)]                                           0.212        0.212  ok
NUM-032   F. tularensis b (%)                                6.66         6.66  ok
NUM-033   F. tularensis E[K|burst]                          934.0        934.4  ok
NUM-034   F. tularensis E[T_prod] (h)                        45.6         45.6  ok
NUM-035   F. tularensis E[tau|burst] (h)                     48.4         48.4  ok
NUM-036   F. tularensis median burst size                     647          648  ok
NUM-037   F. tularensis a                                  1.0010       1.0011  ok
NUM-038   B. anthracis b (%)                                96.24        96.24  ok
NUM-039   B. anthracis E[K|burst]                           1.600        1.601  ok
NUM-040   B. anthracis E[T_prod] (h)                        0.740        0.736  ok
NUM-041   B. anthracis E[tau|burst] (h)                     0.930        0.929  ok
NUM-042   B. anthracis a                                   2.6600       2.6626  ok
------------------------------------------------------------------------------
42 quoted values checked; 0 mismatches.
three key checks: 1 PASS, 2 PASS, 3 PASS
```

**One quoted value was corrected.** NUM-036, the *F. tularensis* median burst
size. Plan §4.12 says "the median about 647", which is $\log2/\log a=647.33$.
The median proper — the least $k$ with $\pr{\Kb\le k}\ge\frac12$ — is **648**,
since $\pr{\Kb\le647}=0.49982$ and $\pr{\Kb\le648}=0.50036$. The chapter
states 648, the computed value. No other quoted number was changed.

**One value is not recomputable and is marked as such.** NUM-043, the
simulated chain intervals $0.691,\,0.500,\,0.377,\,0.292$, is output of
`verify_chained_transfer.py`, which plan §18 forbids re-running. It is carried
in the ledger with that provenance rather than a `RECOMPUTED` line.

---

## 5. Preservation list — six of six found

Grepped by opening words with `verification/ledger_check.sh` section 3. The
passages are line-wrapped in the source, so each file is flattened to a single
line before matching; a naive line-wise grep reports items 3a and 3b as
missing when they are present.

| # | Passage | Opening words | Found in | Moved? |
|---|---|---|---|---|
| 1 | §1's black-box opening | *"The standard models of within-host infection treat…"* | `01_introduction.tex` | no |
| 2 | §1's answers-in-advance | *"The answers, in advance and in brief, are these."* | `01_introduction.tex` | no |
| 3a | The Icarus passage | *"But suppose there is an example of a particular…"* | `05_quasi_stationary.tex` | §6 → §5, kept at the section opening |
| 3b | Its §6.3 callback | *"the productive lifetime is precisely the time needed…"* | `05_quasi_stationary.tex` | §6.3 → §5.4, **still adjacent to 3a**, as the pair requires |
| 4 | §8's closing diagnosis | *"The circularity was never in the mathematics…"* | `08_conditional_means.tex` | promoted into `dist:rem:circularity`, which now closes the section |
| 5a | `rem:ihatk` | *"The tempting guess is…"* | `09_several_founders.tex` | no, verbatim |
| 5b | `rem:gk` | *"It is tempting to write…"* | `09_several_founders.tex` | no, verbatim |
| 6 | §7.7's structural contrast | *"…release and death are the* same *event"* | `11_bursting_budding.tex` | §7.7 → §11, promoted to a top-level section |

Items 3 and 6 moved under the restructure, which is why the list bound Phase A
and not only Phase B. Item 3's pair is intact and adjacent: Icarus opens §5,
the callback closes §5.4, with the quasi-stationary and decay-rate material
between them.

---

## 6. Deviations from the plan, with reasons

1. **`CH2/notes/bdc_material_for_later_chapters.tex` was not edited.** Plan
   §6.3 licensed a dated comment header there — the only edit permitted outside
   `CH5_REWRITE/`. Author instruction overrode it. The comment that would have
   been written is recorded verbatim in `notes/ch5_handoffs.md` entry 6,
   addressed to whoever next opens the file, including the four notation
   substitutions and the fact that the block's closing sentence is no longer
   true. **Nothing outside `CH5_REWRITE/` was written to.**

2. **`a4paper` added to `geometry`, on instruction.** Recorded because the
   stated premise does not hold: `CH4/main.tex` reads
   `\usepackage[margin=1in]{geometry}` with no paper size, as do `CH2` and
   `CH6`, so all three default to US Letter. Chapter 5 is now the only one on
   A4. The change is right for a Leeds submission and was made; the other
   chapters need the same one-line change or the thesis will mix paper sizes.
   It cost nothing and **saved two pages**: 40 → 38, body 31 → 30. One display
   in `dist:prop:lifetime`'s proof overflowed the narrower A4 measure and was
   split from `\[…\]` into `align*`; that is typographic, and the mathematics
   is unchanged.

3. **`CH4_REWRITE/` and `CH6_REWRITE/` were absent at the start of this pass
   and present at the end.** Plan §0.1.2 asks that the `\Ch*` wording be copied
   from them; when I checked, `Chapter numbers/` held `CH1`–`CH10` and no
   `*_REWRITE` tree, so Chapter 5 uses the plan's own wording. Both directories
   now exist — created alongside this pass, not by it — and the wording has
   been compared against them: **`\ChM`, `\ChCore`, `\ChTwoType` and
   `\ChPath` agree verbatim**, and the label prefixes do not collide (`m:`,
   `bdc:`, `dist:`, `p:`). Two items remain, both recorded in
   `notes/ch5_handoffs.md` entry 7: Chapter 5's `\ChCore` carries a
   discretionary hyphen, `birth--death--cata\-strophe`, that CH6's identical
   definition lacks and without which §2's heading sets an overfull box, so the
   hyphenated definition should win on assembly; and CH6 has no self-name, so
   whether `\ChPop` = "the chapter on population dynamics" is the right
   description of a chapter titled "From one cell to a population" is a
   decision for assembly.

4. **"What comes next" is a numbered *subsection*, §12.5, not a top-level
   section.** Plan §4.12 asks for a numbered section, matching \ChCore; plan §4
   fixes the architecture at twelve sections. A thirteenth top-level section
   would break the second to satisfy the first. The actual complaint — that
   the paragraph handing the kernels to \ChPop was `\subsection*` and so
   invisible in the table of contents — is fixed: at `tocdepth=2` it appears,
   numbered, as 1.12.5.

5. **Fourteen figures, not "about thirteen".** 17 floats − 4 cut (`N4a_1`, the
   `QS1`/`QS2` pair as one float, `F4a_3`, `N4a_7`) = 13, + 1 built = 14.
   `F4a_5` survives as a float, regenerated single-panel, because plan §11.2
   cuts its panel (a) rather than the figure. The count is arithmetic, not a
   choice; nothing the plan named for cutting was kept.

6. **The §9 consolidation cut `N4a_7`, not `F4a_6` panel (a).** Plan §11.2
   says only that one duplicates the other and that two figures suffice for
   §9. Cutting `N4a_7` leaves `F4a_6` (flux + conditional mean) and `N4a_8`
   (sub-extensive yield) and requires no regeneration; cutting `F4a_6`'s panel
   would have required rebuilding it through the broken style path — see
   deviation 7.

7. **The upstream figure style module is gone.** Every `_work/*/generate.py`
   imports `style_rc` from a `Figures run/style` directory that does not exist
   on this machine; `find ~/Desktop -name style_rc.py` returns nothing. The
   twelve re-placed figures therefore cannot be regenerated as things stand and
   ship as the source's PDFs. `figures/_style/style_rc.py` is a new
   self-contained replacement used by the two figures built here, written to
   the `SHARED_CONVENTIONS.md` palette that plan §11.3 specifies. The chapter
   is consequently in a **mixed palette** — `fig01` and `fig02` on
   `#0072B2`/`#D55E00`, the other twelve on matplotlib `tab:` defaults. The
   difference is mild and legible, and regenerating twelve figures under a shim
   written in this pass would have been a larger and less reversible change
   than leaving them. `CH5_figure_workorder.md` §4 states the two author
   actions that resolve it.

8. **The $\E{W_t^2}$ deferral is a prose pointer, not a `\cref`.** \ChCore's
   labels are unprefixed (`thm:Wsq`, `eq:Wsq`) and collide across chapters; a
   `\cref` at one today would resolve on assembly to whichever chapter loads
   last. Plan §3.2's requirement is met by a `VERIFIED` grep in the ledger
   giving file and line. `notes/ch5_handoffs.md` entry 5 asks for the pointer
   to become a `\cref` once \ChCore{} is renamespaced. **No label was
   invented.**

9. **Appendix A's provenance column has four values, not three.** Plan §4.13
   asks for *quoted from \ChCore* / *standard* / *new here*. Two rows — the
   decay-rate formula and the ${}_2F_1$ antiderivative — come from \ChM{} and
   from neither of the other two, so the column reads **R**, **M**, **S**, **N**
   with a legend. Single letters rather than words because the spelled-out
   `\ChCore` made the table 128 pt too wide.

10. **The killing/catastrophe distinction is body prose in §1, not a
    subsection.** The source's `sec:rupture-conventions` promised that both
    conventions would be carried in parallel and then abandoned the thread.
    Four sentences in §1 now state the distinction and point at
    `dist:prop:conventions`, which closes the loop in §3.4 rather than leaving
    it open. Nothing was lost: both PDEs are still displayed
    (`dist:eq:catpde`, `dist:eq:killpde`) and both generating functions still
    appear (`dist:eq:gcat`, `dist:eq:gkill`), the second now as a proof rather
    than a parallel computation.

11. **Appendices use CH2's `\thesection` renewal, not `\appendix`.** Copied
    from `CH2/sections/app_a_small_populations.tex` so that they number
    1.A, 1.B, 1.C inside the chapter. This is CH2 winning over the plan's
    silence, as plan §0.1.1 directs.

12. **Word budgets exceeded in eight of twelve sections, by +542 adjusted
    overall.** Reported in full in §2 above rather than trimmed to hit the
    numbers, per plan §4. Four sections carry most of it: §2 (+128, see above),
    §10 (+116, though down from 1,180 raw source words to 889), §6 (+93,
    carrying the new staging, the criterion remark and three figure captions)
    and §12 (+89, carrying the timing table and the robustness/fragility
    subsection the plan adds). §1, §7 and the page budget for the body are all
    on or under target.

---

## 7. What was not done, and why

- **Prose polish, flow, cadence** — Phase B. The chapter has been written once
  and not smoothed; that is deliberate.
- **`verify_chained_transfer.py` was copied, not run** — plan §18, author
  action. Appendix B's reproduction path now points at
  `verification/`, and the suite, its report, its metrics and its figures are
  all present.
- **The *F. tularensis* time-lapse recordings are not verified** — author
  action. `% NEEDS-REF: F. tularensis macrophage time-lapse rupture
  recordings` sits at the sentence in §12.2 that needs it.
- **No BibTeX entry was composed.** Nine of the 22 entries in
  `references.bib` were cited in the source; **eighteen are cited now**,
  including all eight orphans plan §8.2 lists. Four remain uncited —
  `artigiani1987revolution`, `hawkes1971spectra`, `stehfest1970algorithm`,
  `gaver1965observations` — because no sentence in this chapter needs them.
  They are left in `references.bib`.
- **No QSD anchors were added** — plan §8.3. Chapter 5 cites `m:def:qsd`,
  `m:sec:condmeans`, `karlin1957classification` and the `yaglom1947certain`
  entry it already had.
- **$a$ and $b$ were not renamed** — plan §17. Recorded in
  `notes/ch5_handoffs.md` entry 4 as a thesis-wide question.
- **Chapters 4, 6, 7 and 8 were not edited.** Every outward claim is in
  `notes/ch5_handoffs.md` with draft insertion text.

---

## 8. Note for Phase B

The ledger is untouchable: displayed equations, theorem and proposition
statements, proofs, every number, every parameter triple, every table cell.
Proofs are not to be restyled. Three things in particular are load-bearing and
easy to damage:

- **$P$ is the protagonist.** It must be called $P$ in §§4–7 without
  variation, and the same goes for $\Kb$, $\Ifix$, $\tau$, $a$ and $b$.
  Elegant variation would undo the restructure.
- **The Icarus pair** (§5 opening and §5.4 close) only works together and must
  stay adjacent.
- **The legacy register is already gone** — "the somewhat dark art of
  characteristics", "Thankfully, these do compress neatly", "As we've seen",
  "A word of warning before we proceed", "So far, so good", and the
  trap-springing conceit of §8 were all removed in this pass. Phase B should
  not need to hunt for them.

The two known weak points, both flagged rather than fixed: §2 reads compressed
because it is, and §10's opening carries more setup than the rest of the
chapter's register would suggest.
