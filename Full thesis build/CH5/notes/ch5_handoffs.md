# Chapter 5 — outward handoffs

Phase A. Plan §16. One entry per outward-pointing claim this chapter now
makes. **No chapter outside `CH5_REWRITE/` has been edited**, including
`CH2/notes/bdc_material_for_later_chapters.tex` — see entry 6, which carries
the comment that would otherwise have been written into that file.

Each entry gives: the destination, the sentence Chapter 5 now asserts, what
the destination needs to say for the handoff to land, and draft insertion
text. The draft text is a starting point for whoever edits the destination,
not a patch to be applied unread.

---

## 1. \ChPop — the export set

**Where in Chapter 5.** §1.3 "What this chapter exports"
(`dist:sec:exports`), and the five points of derivation it names.

**What Chapter 5 now asserts.**

> \ChPop{} needs five things from here: $\Ifix(a)$ and $g(a)=\delta K(a)$ as
> the survival and release kernels of a renewal model; $g_k$ as the kernel for
> a cell founded at multiplicity $k$; the mean productive lifetime
> $\E{T_{\rm prod}}$ together with the matched constant-rate death rate
> $d_{\Icell}=0.351$ it implies; and $\E{W_t^2}$, for the between-well
> variance that a limiting-dilution assay measures.

This is new framing. In the source, only the mean productive lifetime was
flagged as needed downstream, and it was flagged as a chore ("one more
integral will be needed when, in Chapter 4b…"). Naming the whole consignment
is what makes §2.6 and §5.4 purposeful rather than orphaned.

**What \ChPop{} needs to say.** That these five are what it takes in, by the
same names, and in particular that its renewal kernels *are* Chapter 5's
$\Ifix$ and $g$ rather than quantities re-derived. If \ChPop{} uses a matched
constant-rate comparator, it should quote $d_{\Icell}=1/\E{T_{\rm prod}}=0.351$
at $(1,0.2,0.05)$ and attribute the matching to `dist:prop:lifetime`.

**Draft insertion, for \ChPop's "What we need from" section.**

> The single-cell theory supplies this chapter with five objects, all in
> closed form: the productive-survival kernel $\Ifix(a)$, the release-flux
> kernel $g(a)=\delta K(a)$, the multiplicity-$k$ release kernel $g_k(a)$, the
> mean productive lifetime $\E{T_{\rm prod}}=\lambda^{-1}\log\bigl(a/(a-1)\bigr)$
> — whose reciprocal is the constant-rate infected-cell death rate that best
> matches it — and the second moment of the release $\E{W_t^2}$. Nothing else
> from that chapter is used, and none of the five is re-derived here.

**Risk if it does not land.** Chapter 5's §1 promises a consignment that
\ChPop{} never acknowledges receiving, which is worse than the source's
silence.

---

## 2. \ChPop and \ChPath — the single-cell scoping of §11

**Where in Chapter 5.** §11 "Bursting against budding"
(`dist:sec:budding`), closing paragraph.

**What Chapter 5 now asserts.**

> The comparison is deliberately confined to one cell. What happens when these
> descriptions are embedded in a population, where the timing of release
> governs establishment and invasion speed, belongs to \ChPop; the
> pathogenesis-level comparison belongs to \fwd{path}{the chapter on bursting
> and budding pathogenesis}. All three chapters return to this contrast, and
> answer different questions with it.

**Why this matters.** Bursting-versus-budding appears in three chapters. Read
without this scoping it looks like a three-way overlap; read with it, it is a
division of labour. The division only exists if the other two chapters state
their half of it.

**What \ChPop{} needs to say.** That its comparison is *population-level* and
takes the single-cell release laws as given — explicitly, that it is not
re-opening the single-cell question Chapter 5 settled.

**Draft insertion, for \ChPop.**

> The single-cell comparison — the two release laws, their supports, and the
> coupling of lifetime to yield that bursting has and budding lacks — is
> settled elsewhere and is taken as given. What is at stake here is what those
> laws do to a population: establishment probability from a small inoculum,
> invasion speed, and which of the two mechanisms a fitted constant-rate model
> can distinguish from data.

**What \ChPath{} needs to say.** That its treatment is about which pathogens
sit where on the spectrum and why, not about the distributional contrast.

**Draft insertion, for \ChPath.**

> The distributional contrast between bursting and budding at the level of one
> cell, and its population-level consequences, are established in the two
> preceding modelling chapters. The question here is biological: which
> organisms occupy which end of that spectrum, what intracellular constraints
> put them there, and what the histology shows.

---

## 3. \ChPath — §10's motivation

**Where in Chapter 5.** §10 "Chained immediate transfer"
(`dist:sec:chained`), second paragraph.

**What Chapter 5 now asserts.**

> Serial rupture of this kind is not a fiction: \fwd{path}{the chapter on
> bursting and budding pathogenesis} gives the biological account, with its
> Brownian-drift and macrophage-motility caveats.

**What changed.** The source justified the chained model itself, in two
sentences about plague colony-forming units, and that justification was the
weakest-motivated passage in the chapter. It now leans on \ChPath{} §2.1
"Successive birth death catastrophe", which already carries the biological
account properly, with the caveats.

**What \ChPath{} needs to say.** Nothing new — §2.1 already says it. The
requirement is only that the section survives, keeps its Brownian-drift and
macrophage-motility caveats, and is not itself reduced to a pointer at
Chapter 5. **This handoff is the one at risk of becoming circular**, and
whoever edits \ChPath{} should check that it does not.

**Action.** Verify, do not insert.

---

## 4. \ChTwoType — the notation correspondence

**Where in Chapter 5.** §2.3 (`dist:sec:roots`), one sentence; and §12.5
(`dist:sec:next`), the closing paragraph.

**What Chapter 5 now asserts.**

> \fwd{twotype}{The two-type chapter} solves a Riccati equation of exactly this
> shape under unrelated names — roots straddling one, a root gap in the part of
> $a-b$, the same factorisation.

and, in the discussion, that aligning the two notations is a thesis-wide
decision rather than a local one.

**The correspondence in full**, for whoever takes the decision:

| Chapter 5 | \ChTwoType |
|---|---|
| $b<1<a$ | $0\le r_{2,-}<1<r_{2,+}$ |
| root gap $a-b$ | $\alpha_2$ |
| $I'=\lambda(I-a)(I-b)$ | $\widehat G'=\hat\lambda_2(\widehat G-r_{2,-})(\widehat G-r_{2,+})$ |

**What \ChTwoType{} needs to say.** One reciprocal sentence, so the reader
meeting the second Riccati equation recognises the first.

**Draft insertion, for \ChTwoType.**

> The factorisation here is structurally that of the single-cell
> birth--death--catastrophe process, whose two roots likewise straddle one and
> whose root gap plays the part of $\alpha_2$; the notations differ because
> the two calculations were done independently.

**Explicitly not done.** No renaming. Aligning Chapter 5 to \ChTwoType{} would
mean a global rename of $a$ and $b$ through roughly 2,450 lines and sixteen
figures, and would break \ChCore{} and \ChPop, which both use $a,b$. Plan §17
rules it out and this note records it as a thesis-wide question for later.

---

## 5. \ChCore — the two derivations Chapter 5 now defers to it

**Where in Chapter 5.** §2.4 (`dist:sec:moments-recap`), the $\E{W_t^2}$
paragraph.

**What Chapter 5 now asserts.**

> \ChCorecap{} obtains it from the moment hierarchy, eliminating $\E{X_t^3}$
> through the equation for $K$:

followed by the boxed formula. The source re-derived $\E{W_t^2}$ from scratch,
including the third-moment elimination and the $\mu=0$ check, inside a section
titled "What we need from Chapter 3" — which broke the recap's own contract.

**Where it went.** `CH4/sections/08_variance_and_standard_deviation_of.tex`,
`thm:Wsq` at line 156 and `eq:Wsq` at line 159, same result and same $\mu=0$
check. Ledger entry EQ-013, status `deferred`, with the grep recorded.

**Why this is prose and not a `\cref`.** \ChCore{} is not yet on a namespaced
label prefix — its labels are unprefixed (`thm:Wsq`, `eq:Wsq`) and collide
across chapters. Pointing a `\cref` at `thm:Wsq` today would resolve to
whichever chapter loads last on assembly. The pointer is therefore routed
through `\ChCore` prose, and **should become a `\cref` once \ChCore{} is
renamespaced** — presumably to `bdc:thm:wsq`.

**Action for whoever rewrites \ChCore.** When the `bdc:` prefix lands, replace
the prose pointer in Chapter 5 §2.4 with a `\cref`, and check that the
$\E{W_t^2}$ derivation is still there to point at.

---

## 6. \ChM — the absorbed quasi-stationarity block

**This entry replaces an edit.** Plan §6.3 licensed one edit outside
`CH5_REWRITE/`: a dated comment header on
`CH2/notes/bdc_material_for_later_chapters.tex` recording that its
quasi-stationarity block has been absorbed. **That file has not been touched.**
The comment is recorded here instead, addressed to whoever next opens it.

**What was absorbed.** The block marked `%% BEGIN: BDC quasi-stationarity
paragraph`, whose own header reads *"LIKELY DESTINATION: BDC quasi-stationarity
discussion after the core single-cell results"*. That destination is Chapter 5
§5.3, `dist:sec:decay-rate`, where it is now
`dist:prop:decay` with its proof and consistency check.

**The comment, for the top of that block.**

```latex
% ---------------------------------------------------------------------------
% ABSORBED 20 August 2026 into Chapter 5 (distribution theory,
% quasi-stationarity and burst statistics), section "The decay rate, and what
% it validates" --- label dist:sec:decay-rate, proposition dist:prop:decay.
%
% DO NOT DELETE.  The original notation and the integration warnings above are
% what made the translation checkable, and the four substitutions below are
% recorded in Chapter 5's ledger (CH5_invariants.md, PROP-002) as permitted:
%     T_0        -> T_fix        (absorption at either 0 or H)
%     kappa_i    -> delta*i      (per-capita catastrophe rate)
%     K          -> \mathcal Q   (killed subgenerator; K is E[X_t^2] there)
%     theta      -> \vartheta    (decay rate; theta is lambda(a-b) there)
%
% The block's closing sentence --- that whether a quasi-stationary
% distribution survives conditioning on NEITHER extinction nor rupture "is not
% settled by the argument above, and is best approached by simulation in the
% first instance" --- is NO LONGER TRUE and was rewritten on absorption.
% Chapter 5 settles it analytically: the conditional law exists in closed form
% for all mu >= 0 and is geometric with ratio 1/a.  That inversion is the
% chapter's headline contribution.
%
% This file is never \input, so the comment cannot affect CH2's build.
% ---------------------------------------------------------------------------
```

**The consistency check Chapter 5 adds.** Substituting Chapter 5's own
quasi-stationary law $\nu_n=(a-1)a^{-n}$ into the absorbed decay-rate formula,
with $\mu=\lambda ab$ and $\delta=\lambda(a-1)(1-b)$:

$$\vartheta=\mu\frac{a-1}{a}+\delta\frac{a}{a-1}
=\lambda b(a-1)+\lambda a(1-b)=\lambda(a-b)=\theta.$$

The eigenvalue of the killed subgenerator is the chapter's own time constant.
Verified numerically over four parameter sets, worst relative error
$8.1\times10^{-16}$ (`verification/recheck_numbers.py`, key check 2).

**What \ChM{} may want to say.** `m:sec:condmeans` currently leaves the
two-absorbing-mechanism question open. It could now point forward: the
question is answered, in closed form, in Chapter 5. That is a change to
\ChM{} and is not made here.

---

## 7. Cross-chapter macro wording — reconciled, with two items outstanding

**Not a claim; a coordination item.** Plan §0.1.2 asks that the `\fwd` targets
be copied from `CH4_REWRITE/preamble.tex` and `CH6_REWRITE/preamble.tex` so
that the thesis does not describe the same chapter two ways. Both directories
were **absent** when this pass began and **present** when it ended — they were
created alongside it, not by it. The comparison below was made against them as
they stand on 20 August 2026.

**The shared targets agree.** Chapter 5's wording, taken from plan §0.1.2, is
identical to what the other two rewrites use:

| Macro | CH4\_REWRITE | CH5\_REWRITE | CH6\_REWRITE |
|---|---|---|---|
| `\ChM` | the mathematical introduction | the mathematical introduction | — |
| `\ChCore` | — | the chapter on the birth--death--catastrophe process | the chapter on the birth--death--catastrophe process |
| `\ChTwoType` | — | the two-type chapter | the two-type chapter |
| `\ChPath` | — | the chapter on bursting and budding pathogenesis | the chapter on bursting and budding pathogenesis |

**Label prefixes do not collide**, as the plan assumed: `m:` (CH2), `bdc:`
(CH4), `dist:` (CH5), `p:` (CH6).

**Outstanding item 1 — the discretionary hyphen.** Chapter 5 defines

```latex
\newcommand{\ChCore}{the chapter on the birth--death--cata\-strophe process}
```

with a discretionary hyphen that CH6's otherwise identical definition lacks.
Without it, Chapter 5's §2 heading sets an overfull box, because
`birth--death--catastrophe` cannot be hyphenated across the `--`. On assembly
these two definitions collide and one must win: **the hyphenated one should**,
and CH6's headings should then be checked for the same problem.

**Outstanding item 2 — what to call \ChPop.** Chapter 5 refers to the
population chapter as `\ChPop` = *"the chapter on population dynamics"*. That
chapter's own title is *"From one cell to a population: burst-aware renewal
dynamics and the bursting--budding comparison"*, and it defines no self-name.
Reciprocally, CH6 refers to Chapter 5 as `\ChDist` = *"the chapter on its
distribution theory"*, which Chapter 5 does not use for itself — it says "this
chapter" throughout, so nothing contradicts. Whoever assembles should decide
whether "the chapter on population dynamics" is the description to keep, or
whether CH6's renewal framing wants a phrase closer to its title.

**`\fwd` keys in use** in Chapter 5, so a later pass can find every forward
reference mechanically: `twotype` (§2.3, §12.5), `path` (§10, §11).
