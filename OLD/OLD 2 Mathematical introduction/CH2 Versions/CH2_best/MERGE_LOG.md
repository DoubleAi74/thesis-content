# Merge log — `CH2_best`

**Date:** 9 August 2026
**What this is:** the best-of-breed merge specified by `AGENT_INSTRUCTIONS_BEST_MERGE.md`
— Claude's two merged chapters as base, with grafts from the Qwen merge rewritten into
Claude's voice. This is not a fourth parallel draft; it supersedes the four version
trees at the root, none of which was modified.

**Explicit statement of policy:** Codex and Grok *prose* were not used as a base and were
not used at all. They were consulted only as potential figure donors, and in the end no
Codex or Grok asset was imported (see §5).

---

## 1. Bases and donors

| Role | Path |
|---|---|
| Base, Chapter M | `CH2 Versions_claude/merged/chapter_M_math_intro/` |
| Base, Chapter A | `CH2 Versions_claude/merged/chapter_A_constant_Ap/` |
| Notation freeze | `CH2 Versions_claude/merged/NOTATION.md` |
| Primary donor | `CH2 Versions_Qwen/merged/chapter_M_math_intro/` |
| Figure donors considered | `CH2 Versions_Grok/merged/…/figures/tikz_gen/`, `CH2 Versions_codex/merged/…/figures/generated/` |

Copied wholesale into `CH2_best/`, then modified only here. The four source trees are
untouched.

**Baseline check.** Both Claude projects were compiled before any edit:
`latexmk -pdf -halt-on-error` succeeded on each, with no undefined references or
citations in the final pass. M was 44 pages, A was 28. Grafting started from a green
build.

**Not copied from the base:** `chapter_M_math_intro/sections_pass1/` (superseded pass-1
drafts) and `chapter_M_math_intro/OUTLINE_PASS2.md` (a builder document that described
the two stubs this merge resolves, and would have been stale on arrival). Both remain in
the Claude tree.

---

## 2. Chapter M — section-by-section graft table

| Region | File | What changed | Source |
|---|---|---|---|
| Overview | `01_overview.tex` | Roadmap sentence widened to name the logistic model and the rupture schematic, so the promise matches the final inventory. Nothing else touched. | Claude, edited |
| DTMC definitions | `02_markov_chains.tex` §1.2.1 | Chapman–Kolmogorov identity `m:eq:chapmankolmogorov` added; the "powers of $P$" sentence now derives rather than asserts. | Qwen `02_discrete_markov.tex`, rewritten |
| Random walk | §1.2.1.1 | Exact $n$-step binomial law `m:eq:rwlaw` added, with a paragraph on why this chain surrenders its law and later ones do not; new figure `rw_transition.pdf`. | Qwen `02_discrete_markov.tex`, rewritten; figure regenerated (§5) |
| Galton–Watson object | §1.2.1.2 | Unchanged. Claude's compressed treatment kept; critical theory stays in App. A. | Claude |
| Exponential clocks, generator, Poisson, BD, BDC | §1.2.2 | Unchanged. Claude's competing-clocks proposition, Gillespie remark, rate diagram, killed subgenerator and mean-field remark all retained; Qwen offered nothing here that Claude did not already have in stronger form. | Claude |
| Time-inhomogeneous framework | §1.2.3 | Unchanged (two-time kernels, time-ordered product). | Claude |
| **Time-inhomogeneous linear BD** | §1.2.3.1 | **New subsection.** Generating-function equation with moving coefficients, mean via integrated net growth, Riccati equation for extinction. Closes with a three-way separation of the Riccati equations in the chapter, one of which is an approximation and two of which are exact. | Qwen `04_time_inhomogeneous.tex`, rewritten |
| **Logistic speciation** | §1.2.3.2 | **Stub `m:rem:speciationstub` deleted and replaced.** Diversity-dependent rate; explicit statement that the mean-field replacement is a modelling step, tied back to `m:rem:notmeanfield`; logistic solution, surrogate rate, integrated intensity, mean diversity; early/late limits ending at the near-critical drift. Figure `logspec_mean.pdf`. | Qwen `04_time_inhomogeneous.tex`, rewritten |
| Coupled framework | §1.2.4 | Claude's three-coupling taxonomy and joint generator kept as master. One addition: `\cite{Davis1993}` on the piecewise-deterministic classification. | Claude + Qwen citation |
| **Simulating a coupled system** | §1.2.4.1 | **New subsection.** Non-constant-rate holding time `m:eq:coupledholding`, rejection/quadrature, and the two weak-coupling closures — with the logistic surrogate identified as exactly one of them. | Qwen `05_coupled_ode_ctmc.tex`, rewritten |
| **Rupture into a shared medium** | §1.2.4.2 | **Stub `m:rem:coupledstub` deleted and replaced.** The schematic Claude's stub had only conjectured, now written out: medium clearance, impulsive release at rupture, both coupling arrows active. Labelled a schematic once, then developed. Two structural features isolated (impulsive continuous variable; released cohort is a state at a stopping time). Figure `rupture_sawtooth.pdf`. | Qwen `05_coupled_ode_ctmc.tex`, rewritten |
| Discrete methods | `03_methods.tex` §1.3.1 | Unchanged. First-step, generating functions, functional iteration, and the "where the methods run out → Koenigs → Chapter A" bridge all preserved. | Claude |
| Continuous methods | §1.3.2 | One clause added, pointing `m:eq:condvar` at its new derivation. Full ladder otherwise untouched: backward equations, mean, variance, hitting, extinction, conditional means, $\Ac$, light $A(p)$, two-absorbing-mechanism QSD. | Claude |
| Method of characteristics | `04_method_of_characteristics.tex` | Unchanged, including the worked absorption–death example and "what the example shows". | Claude |
| **App. A** | `app_a_critical_gw.tex` | Retitled to cover conditional moments. **New §1.A.4 "The limiting conditional variance"** deriving the second moment quoted in §1.3.2.6. **New "The exact object"** in §1.A.5: the marked generating function $F_n(s)=\ex{s^{\widetilde Z_n}(1-\kappa)^{H_n}}$ and its exact recursion, which closes the loop `m:rem:notmeanfield` opened. | Qwen `12_app_variance.tex`, `13_app_dbdc.tex`, rewritten |
| App. B, C, D | unchanged | Absorption models in full, hypergeometric identity, coefficient extraction. | Claude |

### Grafts considered and declined

- **Qwen `01_overview.tex`** — donor phrases only were permitted; on reading, Claude's
  three-thread opening is stronger and absorbing Qwen's distributional-versus-absorption
  framing would have added a fourth parallel taxonomy. Declined.
- **Qwen `06`–`08` methods files** — Claude's methods spine is longer, better motivated
  and better cross-referenced. Declined, per policy.
- **Qwen `10_app_critical.tex`, `11_app_cohorts.tex`** — fully covered by Claude's App. A
  (critical power law, infinite expected lifetime, total progeny, cohort of size $k$,
  push of the past). Declined as duplication.
- **Qwen `14_app_moc_catalogue.tex`, `09_app_moc_support.tex`** — Claude's App. B/C/D
  cover the same ground and go further (parameter-regular representation, resonance,
  coefficient recovery). Declined.
- **Qwen `13_app_dbdc.tex`, killed-chain half** — already present verbatim in Claude's
  §1.3.2.6 (eigenrelation, decay rate, constant-versus-state-dependent catastrophe).
  Only the weighted-generating-function half was new, and only that was taken.
- **Qwen's first-catastrophe mass function** `Pr(K=n) = c^{2^n-1}(1-c^{2^n})` — **not
  imported: it is off by one.** With $S_n=c^{2^n-1}$ the probability of surviving to
  generation $n$ and $h_n=1-c^{2^{n-1}}$ the conditional hazard at step $n$, the product
  $S_nh_n$ is $c^{2^n-1}(1-c^{2^{n-1}})$, not what the donor prints. Claude's appendix
  already states $S_n$ and $h_n$ separately with the correct caution about confusing a
  conditional hazard with an exact-time probability, so nothing was lost by dropping it.

---

## 3. Chapter A — complete list of changes

**None.** Chapter A is Claude's, unmodified, and this is a deliberate outcome rather than
an oversight. It was audited against the interface contract before being left alone:

- All twelve sections plus both appendices retained in Claude's order.
- Claim hygiene verified against §1.2 of the instructions and intact:
  hypertranscendence of $z\mapsto\psi_r$ is stated as a theorem at every subcritical
  parameter; transcendence and irrationality of individual values $A(p_0)$ are stated
  as *not proved*; readings (E) and (D) for the parameter map $p\mapsto A(p)$ are
  stated as open; the PSLQ battery is presented as finite-height negative evidence,
  "evidence for the conjecture, not a proof of it"; the Mandelbrot figure is labelled
  "illustration and not argument".
- Compiles clean; no undefined references, citations or figure paths; no verification
  or PSLQ scripts ship with the chapter (the text says they are archived with the
  project sources, and they are not in the directory).
- Qwen A figures (`Ap_bounds_ratio.pdf`, `Ap_nearcrit.pdf`, `koenigs_domain.pdf`) were
  examined and **not** imported: Claude's A text does not expect them, and importing a
  figure no sentence asks for is how a chapter acquires orphans.

One inherited oddity is recorded rather than fixed: `figures/conditionalMean.pdf` sits in
Chapter A's figure directory but is referenced by no section. It is left in place, unused
and unreferenced.

---

## 4. Bibliography

Started from Claude's `references.bib` in each chapter.

| Chapter | Keys added | Reason |
|---|---|---|
| M | `Davis1993` (Davis, *Markov Models and Optimization*) | Piecewise-deterministic Markov processes, cited in §1.2.4 case (i). Taken from Qwen's M bibliography. |
| A | none | |

No keys were removed or renamed, and no duplicates were introduced. Every `\cite` in both
chapters resolves in the final pass.

---

## 5. Figure provenance

See `FIGURE_SOURCES.md` for the full per-figure table. Two points belong in the log
proper, because they are judgement calls rather than transcription.

**Both imported Qwen figures were regenerated rather than copied.**

1. `rw_transition.pdf` — the donor binary labels the step probability $p$, which
   `NOTATION.md` reserves for the Galton–Watson division probability; Chapter M writes
   the walk's step probability as $q$. Shipping the donor PDF would have put two meanings
   of $p$ on facing pages. Regenerated from `figures/make_rw_transition.py` with $q$
   throughout.

2. `rupture_sawtooth.pdf` — **the donor binary does not depict the system its caption
   describes.** In the donor script the medium's stored value is never decayed before the
   release is added: the reconstruction decays $y$ for display, but the state variable
   carries the undecayed total forward, so each drawn jump is larger than
   $c\,X_{\tau-}$. At the third rupture the drawn increment is $9.4$ where
   $c\,X_{\tau-}=6.0$. Regenerated from `figures/make_inhomogeneous_figures.py`, which
   clears the medium to the event time before applying the jump; every drawn release now
   equals $c\,X_{\tau-}$ exactly. A seed giving five well-separated ruptures was chosen,
   in place of the donor's realisation containing two ruptures $0.019$ apart.

`logspec_mean.pdf` was also regenerated, for notation only: the donor axis label reads
$r=\lambda_0-\mu$, and $r$ is frozen as $2p$. The curve is unchanged.

**No Grok or Codex figure was imported.** All six Grok `tikz_gen` panels and both Codex
`generated` figures were candidates for the conditional-mean and critical-GW material.
Chapter M already carries `birth_death_paths.pdf` for the three regimes,
`extinction_and_law.pdf` for extinction and the surviving law, `conditionalMean.pdf` for
the quasi-stationary plateau, and `power_law_fixed.pdf` plus three `kvals` panels for
critical behaviour and cohorts. None of the optional figures had a sentence waiting for
it, and the instruction that each figure must earn a caption and a textual purpose is
what decided it. This is the first item on the triage list, and it was taken.

---

## 6. Interface contract and quality gates

| Gate | Status |
|---|---|
| G1 both PDFs compile with `latexmk -pdf -halt-on-error` | pass — both exit 0 from a clean `latexmk -C` |
| G2 M has overview, objects (incl. time-inhomogeneous + coupled), methods, MoC, appendices | pass |
| G3 M carries no product/series/Koenigs/BB/PSLQ development | pass — M names Koenigs once, in §1.3.1.4, as the handover |
| G4 M derives $\Ac(p)=(1-2p)/(1-p)$ and defines $A(p)$ only lightly | pass — `m:eq:Acts` derived, `m:eq:Apdef` defined and forwarded |
| G5 A retains all twelve sections and both appendices | pass |
| G6 claim hygiene | pass — see §3 |
| G7 abstract mathematical voice, no application bleed, no merge-meta in body | pass — full-text scan for meta language returns nothing |
| G8 no verification/PSLQ scripts shipped | pass — the only scripts are the three figure generators in M |
| G9 notation freeze; `m:` / `a:` label prefixes | pass — additions documented in `NOTATION.md` |
| G10 this log | pass |
| G11 no unresolved `\ref`/`\cite`, no missing figures | pass — final-pass logs are clean; every `\includegraphics` target exists |
| G12 no `TODO` / `Placeholder` in final section files | pass |

**M ↔ A interface.** M contains the survival recursion, the light definition
$A(p)=\lim_nS_n/(2p)^n$ with $\ex{Z_n\mid Z_n>0}\to1/A(p)$, the full derivation of
$\Ac(p)$ and the competing-clocks match $p=\lambda/(\lambda+\mu)$, and forward references
to A routed through `\ChA`. A owns the product, series, bounds, near-critical theory,
closed-form search, Koenigs identity, hypertranscendence and PSLQ. Neither chapter
re-proves the other's material. The grafts did not touch this boundary.

---

## 7. Page counts

| | Claude base | `CH2_best` |
|---|---|---|
| Chapter M | 44 | **50** |
| Chapter A | 28 | **28** |

The six pages are the two resolved stubs and the two appendix recoveries. A continuity
read of §1.2 through §1.2.4 found no duplicated definition, no contradictory notation and
no register seam to cut against, so no compensating reduction was made. There are no
overfull boxes above 20 pt in either chapter, and none at all in M.

---

## 8. Known issues and residual risks

1. **The logistic speciation model is a surrogate, and the chapter says so twice.** The
   state-dependent chain `m:eq:speciationrate` is not solved; what is solved is its
   mean-field linearisation. The text marks the substitution at the point it is made and
   ties it to `m:rem:notmeanfield`, which shows the same substitution failing elsewhere.
   No result in the thesis rests on it.
2. **The rupture schematic is a schematic.** It fixes a mechanism and forwards the model
   itself to the later rupture chapter through `\fwd`. Should that chapter's model differ
   from this sketch, §1.2.4.2 is the paragraph to revisit — the framework above it is
   general and would not need changing.
3. **`\fwd` targets are unresolved by construction.** The macro prints its second
   argument and ignores the first, so forward references to later chapters read as prose
   ("in the chapter on compartment rupture") rather than numbers. That is Claude's design
   and is correct until the thesis chapter order is fixed.
4. **Figure scripts assume a fixed RNG stream.** `make_inhomogeneous_figures.py` uses
   `numpy.random.default_rng(24)`. A future NumPy that changed the PCG64 stream would
   redraw the sawtooth realisation; the caption quotes only parameters, not event times,
   so it would remain true.
5. **Chapter A was audited, not re-verified.** Its numerical claims — 1150-digit
   agreement, 123 PSLQ tests, the eleven parameters — are carried over from the Claude
   merge unchanged. Nothing was invented, and nothing was independently recomputed.

---

## Addendum — figure candidate gallery

**Date:** 9 August 2026. Follows `AGENT_INSTRUCTIONS_FIGURE_GALLERY.md`; the merge record
above is unchanged and none of its claims are revised here.

All figure binaries from the Claude, Qwen, Grok and Codex merges, together with the
current production assets of this project, are staged under
`chapter_*/figures/candidates/` and displayed in a temporary gallery appendix in each
chapter — 1.E in M, 2.C in A. 153 candidates in 51 groups; nothing was dropped for
redundancy, so byte-identical files appear several times over by design.

**No figure selection has been made.** The narrative's `\includegraphics` calls are
untouched: M still uses the 18 production filenames and A the 7 recorded in
`FIGURE_SOURCES.md`, and §5 above still describes what the chapters actually print. The
declined-donor table in §5 remains the record of the merge's own decisions; the gallery
exists so that those decisions can be revisited by eye, not because they were reversed.

Two entries above are narrowed by this addendum rather than contradicted. §3 records that
Chapter A had no changes; A's `chapter.tex` has now gained one `\input` line for the
gallery, and its `figures/candidates/` directory is new. No A section file, figure path
or claim was touched. Likewise §5's statement that no Grok or Codex asset was imported
still holds for the *narrative*: their binaries are now staged as candidates, and none is
used by the text.

Details in `FIGURE_GALLERY_LOG.md`, `FIGURE_CANDIDATE_INVENTORY.md` and
`FIGURE_SELECTION_CHECKLIST.md`. Page counts grew from 50 to 72 (M) and 28 to 49 (A);
removing the gallery restores the earlier documents exactly.
