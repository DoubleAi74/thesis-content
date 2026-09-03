# Progress — Three-Chapter BDC Build

**Status:** COMPLETE — all phases done; definition of done (Startup.md §7) fully met
**Last updated:** 2026-08-08 (final QA: BDC_core 24 pp, BDC_extra 34 pp, BDC_odes 37 pp — all 0 errors / 0 undefined refs / 0 undefined cites / 0 overfulls; renewal 54/54 and chained 28/28 green; 17 figure flags rendered)

This is the live tracking and recovery document for the project specified in
`Startup.md` and `Project_specification.md` (read those first). It serves two
purposes:

1. **Tracking** — every phase and task below is checked off as it completes.
2. **Recovery** — if the working agent is interrupted, the replacing agent
   reads `Startup.md` → `Project_specification.md` → **this file**, and resumes
   from the first unchecked task, guided by the logs at the bottom.

**Update discipline (binding).** Update this document continuously, not in
arrears: after every task completion, every decision, every formula change,
every deletion, every build, every suite run. Entries are dated. An entry is
better than a perfect entry. The record must be precise enough that a fresh
agent can resume immediately without re-deriving the state of the work.

---

## Phase 0 — Setup

- [x] 0.1 Create `BDC_core/`, `BDC_extra/`, `BDC_odes/` with `sections/` and `figures/` subfolders.
- [x] 0.2 Copy Chapter 3 sources into `BDC_core/` (`sections/*`, `figures/IMG_ch4/*` flattened into `figures/`, `references.bib`); **rewrite every `\includegraphics` path in the copied sections to `figures/<filename>`** (drop the `IMG_ch4/` layer) — acceptance: all paths resolve at the 0.9 baseline compile.
- [x] 0.3 Copy Chapter 4a sources into `BDC_extra/` (draft `sections/01…10`, the relevant parts of `17_discussion.tex` per the cut list in spec §4.1, `A_formula_tables.tex`, `C_technical_derivations.tex`, `figures/IMG_ch5/QSmean/{QS1.png,QS2.png}` flattened into `figures/`); **rewrite the two QS `\includegraphics` paths to `figures/QS1` / `figures/QS2`**. Do NOT copy the orphan files `01_opening.tex`, `02_specification_of_rupture_state.tex`, `09_potential_application_in_bmvr.tex` (not in the draft's `\input` list; content already lives in the draft intro and file 11). Note: `B_verification_records.tex` also copied (chained record will be carved out of it; renewal record removed) — harmless superset at Phase 0.
- [x] 0.4 Copy Chapter 4b sources into `BDC_odes/` (draft `sections/11…17`, the relevant parts of `17_discussion.tex`, `A…C` appendix material, the 12 PDFs from `document MAIN/figures/`).
- [x] 0.5 Write `BDC_core/main.tex` (title per spec §1, unified macros per spec §2 with `\Ifix`, the figure-flag macro per spec §7, theorem environments, unsrt bibliography).
- [x] 0.6 Write `BDC_extra/main.tex` (same pattern; macros converted per spec §2.5).
- [x] 0.7 Write `BDC_odes/main.tex` (same pattern; plus the §2.4 collision renamings prepared). Section files renumbered to the new structure (11→02, 12→03, 13→04, 14→05, 15→06, 16→07, 17→08; new 01_what_we_needed placeholder).
- [x] 0.8 Write each `references.bib` per spec §§3.5, 4.3, 5.3. (BDC_core: five originals verbatim + brockwell1982birth. BDC_extra: draft bib + williams2024reproduction + williams2021anthrax. BDC_odes: draft bib, will adjust to actual citations during Phase 3.)
- [x] 0.9 Baseline compile of all three builds (`latexmk -pdf`); record results in Log E. All three compile with 0 errors. Also performed early (mechanical, spec §2.5/§2.6): `\Ihat`→`\Ifix` everywhere in 4a/4b (subscripts braced as `\Ifix[,{k}]`, macro takes optional subscript), `\yt/\yy`→`\wt/\ww` in Ch. 3.
- [x] 0.10 Re-run both verification suites once (unmodified) to confirm the green starting state; record in Log F.
- [x] 0.11 Read `Grant_paper.pdf` in full as a first-class source: register model for prose and mathematical sentences (alongside `/aa-flow-lucid`; chapters are naturally more expansive than the paper), and source of material to incorporate fluidly. Internalise the notation translation in specification §2.7 (chapters' regime is canonical — δ stays the catastrophe rate). Citation status is already decided (user, 2026-08-08): **do not cite the paper in the chapters** — record this decision in Log A. Paper internals noted for translation: paper's a↔our b, paper's b↔our a; paper α↔our δ; paper eq. (3.26) → spec §6 μ>0 conditional burst-time form; paper Tables 3.1/3.2 → Chapter 4a §7; paper §2 budding → Chapter 4b §2; paper §4 parameter estimates → Chapter 4a discussion (cite carruthers2020stochastic, williams2021anthrax, williams2024reproduction, not the paper).

## Phase 1 — Chapter 3 (`BDC_core`)

Work per `Project_specification.md` §3. Notation regime §2 applies throughout.

- [x] 1.1 Merge `01_opening.tex` into the introduction; fix the introduction's documented typos and register issues; unstack the four-citation sentence; fix the "explored in chapter 3" leftover (spec §3.1). (01_opening was an empty comment; intro fully rewritten with typos fixed, citations unstacked, "Further interest" excursus kept, first-person asides softened; forward pointers now to Chapters 4a/4b.)
- [x] 1.2 Reference values: unify notation; fix $p_k/P_k$ indices; remove $I_{\mathrm{death}}$; add $D:=p_0$, $I_{\mathrm{fix}}:=I-D$, $A,B,\theta$, and the identities (spec §§2.2, 3.1). ($\phi_k$ row also replaced by the burst-time *density* $\varphi(t)=\delta J(t)$, since $\tau$ is continuous; recorded in Log D.)
- [x] 1.3 Process definition: fix duplicate `BDRsims` labels (→ `fig:BDRsimsX`, `fig:BDRsimsW`); remove stray `\title`; β→λ; captions unified; light grammar.
- [x] 1.4 Analytical quantities: all displays wholly in λ; broken sentences fixed; "have have" double word fixed; orphaned PLOT line removed (its residue becomes flag F3.5 in the closing section); **multi-founder block (audit B1): $I_k=I^k$ kept with branching justification; false claim $I_{\mathrm{fix},k}=(I_{\mathrm{fix}})^k$ replaced by $I_{\mathrm{fix},k}=I^k-D^k$, "(Is this correct?)" marker deleted; forward pointer to Chapter 4a**; Karlin–Tavaré spelling fixed; `\xdef` family removed; $I_{\mathrm{fix}}$ corrected per spec §3.2.2 (Theorem 3.2.3).
- [x] 1.5 Derivations: λ unified; `ddIIfact` fixed to $\lambda(I-a)(I-b)$; $I_\pm$ retired with one correspondence line ("some treatments" framing, no draft history); corrected $I_{\mathrm{fix}}$ derivation inserted (ODE branching term $\lambda(I^2-D^2)$; closed form; limits; $\Ifix'(0)=-(\mu+\delta)$); Vieta/identity block derived; separation-of-variables solution given for both $I$ and $D$.
- [x] 1.6 $J(t)$/$V(t)$ section: $Y$→$W$ throughout (mechanical pass in Phase 0, prose rewritten in Phase 1); `Voft` label kept in a numbered equation; $\hat p_0$ discussion replaced by the clean forward equation for state $H$ (§6.5 "The forward relation"); "compenent" fixed.
- [x] 1.7 Merge 08+10 (variance sections) keeping all unique content; $K(I)$ corrected to $+2\lambda^2/\delta^2$ form; **whole $\mathrm{E}[W_t^2]$ derivation block replaced** with the correct integration (constant $K(0)=1$, signs per spec §3.2.4), the μ=0 geometric check included, no correction-history framing; duplicate labels removed (file 10 content was a subset).
- [x] 1.8 Merge 09+11 (dependencies on $I$) keeping all unique content: correct $K(I)$ (file 11's), compact $V(I)$ (file 11's), Var expansions (file 09's, signs corrected); $J=-\delta^{-1}I'$ enforced throughout (file 11's sign slip removed).
- [x] 1.9 State the headline results as theorems/corollaries: Theorems for $I(t)$, $D(t)$+$\Ifix(t)$, $J(t)$, $V(t)$+$V_\infty$, $K(t)$+$K(I)$, $\mathrm{E}[W_t^2]$, plus corollary $\mathrm{E}[\Kb|\text{burst}]=a/(a-1)$ (spec §3.3, forms from spec §6).
- [x] 1.10 Write the closing "What comes next" section setting up Chapters 4a and 4b (two subsections + open questions settled downstream; carries flag F3.5).
- [x] 1.11 Six existing figures copied (Phase 0); captions rewritten to λ; all six referenced from text (incl. restored `I_of_t_2` with new $\Ifix$ caption); `poem.jpeg` copied but unreferenced (recorded in Log D).
- [x] 1.12 Figure flags F3.1–F3.6 inserted with full specs per spec §§3.4, 7; Log C updated.
- [x] 1.13 Bibliography: `brockwell1982birth` added and cited at the Brockwell mention; Pakes et al. 1979 kept as an uncited prose mention ("the models of Pakes and collaborators from the late 1970s") — no reliable entry available from memory without web search; gap recorded (spec §3.5).
- [x] 1.14 Compile clean: 24 pages, 0 errors, 0 undefined refs, 0 overfulls (flag boxes exempt), 0 undefined citations; recorded in Log E.
- [x] 1.15 Prose written to spec §8 standard during the rewrite (aa-flow-lucid loaded and applied end-to-end; final polish pass in Phase 4).

## Phase 2 — Chapter 4a (`BDC_extra`)

Work per `Project_specification.md` §4. Conversions per spec §2.5 (β→λ, R→H, `\Ihat`→`\Ifix`, correction remarks deleted).

- [x] 2.1 Rewrite §1 Introduction to Chapter 4a scope (motivation, what Chapter 3 supplies, three research questions, condensed one-page story of the single-cell results, chapter map, forward pointer to Chapter 4b; killing/catastrophe subsection kept, $R$→$H$).
- [x] 2.2 Build §2 "What we need from Chapter 3": boxed formulas from spec §6, pointers to Chapter 3, no proofs beyond one-liners; notation table converted (single-cell rows only; population rows belong to Chapter 4b's table); rem:ihat and rem:EW2 deleted, the μ=0 geometric check of E[W²] kept as neutral mathematics. Carries flag F4a.1.
- [x] 2.3 Convert draft §3–§4 (PGF PDEs; identifying the PGFs): β→λ, R→H, defective-PGF caveat, $k$-founder subsection. Prose error fixed in §3's derivation: the catastrophe-convention $p_0$ equation is $\dot p_0=\mu p_1$, not "$p_0\equiv0$" (recorded in Log B).
- [x] 2.4 Convert draft §5–§6 (state probabilities; QSD): geometric-at-every-time, $\sum p_n=\Ifix$ (correction-history framing removed, replaced by a cross-reference to §2's closed form), QSD theorem, moments, QS1/QS2 figure with converted caption ($R$→$H$, β→λ), mean productive lifetime; `\S\ref{sec:peff-section}` forward ref replaced by Chapter 4b pointer. Carries flags F4a.2, F4a.3.
- [x] 2.5 Convert draft §7 (burst time and size): β→λ, $\varphi=\delta J$, analytic proof, burst=QSD corollary, size-biasing. **Enriched per spec §4.1:** new subsections — harmonic conditional rupture-time law with $L_1/L_2$ proof (μ=0), Gumbel limit and $t_n=(\log n)/\theta$ maximiser; μ>0 $\mathrm{E}[\tau\mid\text{burst}]=\frac{1}{\lambda(1-b)}\log\frac{a-b}{a-1}$ with the explicit distinction from $\mathrm{E}[T_{\mathrm{prod}}]$; single-cell budding-vs-bursting comparison (paper Table 3.1) translated to unified notation as Table~\ref{tab:budburst}. Carries flags F4a.4, F4a.5, F4a.8.
- [x] 2.6 Convert draft §8 (conditional burst means): β→λ; cross-ref fixed to eq:Vinf.
- [x] 2.7 Convert draft §9 (MOI): β→λ; rem:gk reworded neutrally ("The free-sum trap", no "earlier note"); sec:renewal forward ref replaced by Chapter 4b pointer. Carries flag F4a.6.
- [x] 2.8 Convert draft §10 (chained transfer): β→λ; verification record now "28 checks, all passing" (date/history dropped); closed-form remark neutral ("The coefficient, and a near miss", with stars-and-bars reading); sec:peff-section ref replaced by Chapter 4b pointer; draft-Θ/Ω phrasing neutralised. Carries flag F4a.7.
- [x] 2.9 Assemble §11 Discussion: assay predictions (five predictions, β→λ, HIV caveat reworded to point at Chapter 4b's spectrum) + single-cell open problems (burst=QSD conceptual proof; general-μ chained laws; logistic sensitivity) + forward pointer + new biological-grounding subsection "The same theory at two extremes" (*F. tularensis* SCHU S4 and *B. anthracis* estimates; model claims kept distinct from biological claims; cites carruthers2020stochastic, williams2021anthrax, williams2024reproduction, oyston2024tularaemia — Grant paper NOT cited).
- [x] 2.10 Appendices: A = single-cell formula table (+ μ=0 block, flooding line dropped) with the Grant-paper conditional-time laws added as rows; B = chained verification record only (28/28); C = $V_\infty^{(k)}$ derivation + PGF extraction (hypergeometric transforms moved to 4b).
- [x] 2.11 QS1/QS2 figures flattened (Phase 0); §6 figure kept with converted caption.
- [x] 2.12 Figure flags F4a.1–F4a.8 inserted with full specs; Log C updated.
- [x] 2.13 Compile clean: 34 pages, 0 errors, 0 undefined refs, 0 overfulls, 0 undefined citations; recorded in Log E.
- [x] 2.14 Chained-transfer suite re-run: 28/28 PASS (2026-08-08); recorded in Log F.
- [x] 2.15 Bibliography: `williams2024reproduction`, `williams2021anthrax` added, plus `oyston2004tularaemia` (from the paper's reference list) for the 10 CFU dose claim (decision in Log A). `Grant_paper.pdf` NOT cited (user decision 2026-08-08).

## Phase 3 — Chapter 4b (`BDC_odes`)

Work per `Project_specification.md` §5. Conversions per spec §2.5 + the §2.4 renamings ($\zeta$; boolean fraction $\varphi$).

- [x] 3.1 Build §1 "What we need from Chapters 3 and 4a" (new `01_what_we_need.tex`): boxed formulas of spec §6 with local labels (eq:AB, eq:IDIhat, eq:J/K/V/Vinf, eq:burstlaw, eq:sizebias, eq:EW2, prop:lifetime, eq:gk, eq:Vk), the δJ-vs-φ naming decision stated up front, population notation table (incl. the ζ and φ rows), no proofs.
- [x] 3.2 Convert draft §11 (why constant release fails); BMVR citations kept. Paper's single-cell budding picture incorporated in §2.1 as the comparator's completion (two independent Poisson event types; $I_{\rm bud}$, $V_{\rm bud}=\frac{p}{d_{\Icell}}(1-I_{\rm bud})$; geometric release law on $\{0,1,\ldots\}$; independent release/death vs simultaneous release-and-death contrast) per spec §5.1; $\varphi=\delta J$ written as $\delta J$; cross-chapter refs to prose.
- [x] 3.3 Convert draft §12 (renewal BMVR): kernel notation $\Ifix(a)$; Result; replacement table; novelty remark; verification subsection; overlay subsection; "original attempt of Chapter 4" rephrased to §2 pointer; carries flag F4b.1.
- [x] 3.4 Convert draft §13 (effective parameters, R₀, identifiability); appendix pointer to this chapter's Appendix C kept; sec:burst-size/sec:burst-time refs → Chapter 4a prose.
- [x] 3.5 Convert draft §14 (flooding + trade-off): tables and proofs intact; thm:burst ref → local eq:burstlaw; trade-off values re-verified by direct quadrature of the characteristic equation at flag-writing. Carries flags F4b.2, F4b.3.
- [x] 3.6 Convert draft §15 (spectrum): β→λ; κ→ζ (Model 10); boolean q→φ (all sites incl. TikZ map); Hawkes kernel φ→h (avoids the new φ collision); R→H in reset table; sec:moi → Chapter 4a prose; TikZ spectrum map intact.
- [x] 3.7 Convert draft §16 (HIV contrast): β→λ; TikZ stage diagram intact; no cross-chapter refs needed.
- [x] 3.8 Assemble §8 Discussion (4b's share of draft §17): fitting consequences (three items); forward connections (Chapter 5 two-type/GATE, Chapter 6 spectrum/evolutionary home, Chapter 7 nonlinear mechanisms — by working chapter name); population open problems (two-type killed moments; flooding boundary vs real parameters; population-level variance, citing williams2024reproduction; partial-release boundary in φ; literature positioning); pointer back to Chapter 4a's single-cell open problems.
- [x] 3.9 Appendices: A = population formula table (+ μ=0, L=1, young-cell, r=0 blocks); B = renewal verification record ("Fifty-four checks, all passing", no history, honest-gap paragraph kept); C = hypergeometric transforms with convergence caveat (Vk derivation + PGF extraction moved to 4a's C).
- [x] 3.10 All 12 copied figures referenced (verified by 0 undefined refs at compile); both TikZ figures compile.
- [x] 3.11 Flags F4b.1–F4b.3 inserted with full specs; **F4b.4 omitted** — the flooding criterion as a function of φ has no closed-form offspring law to specify against (spec §5.2 permits omission); Log C updated.
- [x] 3.12 Compile clean: 37 pages, 0 errors, 0 undefined refs, 0 overfulls, 0 undefined citations; recorded in Log E.
- [x] 3.13 Renewal suite re-run (unmodified) after conversion: 54 PASS / 0 FAIL (2026-08-08); recorded in Log F.

## Phase 4 — Prose pass (all three chapters)

- [x] 4.1 Invoke `/aa-flow-lucid` (invoked at the start of Phase 1; all four references read; register applied end-to-end as each chapter was written/rewritten); final polish pass over `BDC_core` ("Actually"→"In fact"; "within within-host" de-doubled; full re-read of intro/derivations/analysis sections).
- [x] 4.2 End-to-end pass over `BDC_extra` (intro, §2 recap, §7 enrichments, discussion re-read; flow and rails verified; no register breaks).
- [x] 4.3 End-to-end pass over `BDC_odes` (§1, §2.1 budding enrichment, discussion re-read; prop:lifetime reference style fixed from "Proposition~\ref" to \eqref since the label is now an equation in §1).
- [x] 4.4 Cross-chapter consistency sweep: 0 β, 0 $\hat I$, 0 $Y_t$, 0 bare `\Ifix_` subscripts, 0 burst-size bare-K misuse, 0 rupture-state $R$ (the only remaining $R$ is Model 10's total excitation $R=\sum r_i$, a distinct defined quantity); 0 correction-history remarks in visible text; 0 double words; 0 American spellings; 0 AI-tell words; cross-references by chapter number only; titles final as spec §1.
- [x] 4.5 Recompile all three after the prose pass: 24/34/37 pages, each 0 errors / 0 overfulls / 0 undefined refs / 0 undefined citations; recorded in Log E.

## Phase 5 — Final QA

- [x] 5.1 All three builds final: BDC_core 24 pp, BDC_extra 34 pp, BDC_odes 37 pp — each with 0 errors, 0 undefined references, 0 undefined citations, 0 overfull boxes (none occurred even inside flag boxes). All 17 figure flags verified present in the compiled PDFs by text extraction (F3.1–F3.6, F4a.1–F4a.8, F4b.1–F4b.3); F4b.4 omitted by decision (Log A).
- [x] 5.2 Both verification suites re-run at final QA: renewal 54 PASS / 0 FAIL; chained 28 PASS / 0 FAIL (2026-08-08); recorded in Log F.
- [x] 5.3 Figure-flag registry (Log C) complete: every flag listed with ID, title, section, one-line purpose; F4b.4's omission recorded with reason.
- [x] 5.4 Deletion log (Log D) complete: every merged-away file, orphaned line, dead macro, and superseded formula block recorded with former location and where its unique content now lives.
- [x] 5.5 `TODO(verify)` bibliography entries listed below Log F with their status unchanged by design.
- [x] 5.6 This document finalised: all phases checked, Status set to COMPLETE, Last updated set; every judgment call recorded in Log A, every formula-level change in Log B.

---

## Log A — Decisions

| Date | Decision | Reason |
|---|---|---|
| 2026-08-08 | `Grant_paper.pdf` is NOT cited in any chapter (user decision, carried from spec §4.3); it is source material and register model only. Where its estimates/results are used, cite carruthers2020stochastic, williams2024reproduction, williams2021anthrax (and oyston2004tularaemia if added). | Binding user decision recorded in spec §4.3 and task 0.11. |
| 2026-08-08 | `\Ifix` macro defined with optional subscript argument `\newcommand{\Ifix}[1][]{I_{\mathrm{fix}#1}}`; multi-founder variants written `\Ifix[,{k}]` → $I_{\mathrm{fix},k}$ (comma subscript, per spec §6). | Plain `\Ifix_k` is a double subscript; comma form is the spec's canonical multi-founder notation. |
| 2026-08-08 | Chapter titles kept as spec §1; date lines "Chapter 3 / 4a / 4b of AA Thesis --- University of Leeds / Draft compiled \today". Cross-chapter references in prose as "Chapter 3", "Chapter 4a", "Chapter 4b". | Spec §1 fixes titles; the handoff consistently names the chapters 3/4a/4b. |
| 2026-08-08 | 4b section files renumbered 02–08 (plus new 01) to match the new chapter structure; 4a discussion file renamed 17→11. Recorded here rather than Log D (renames, not content removals). | Keeps `\input` order transparent in each main.tex. |
| 2026-08-08 | Added `oyston2004tularaemia` (Oyston, Sjöstedt & Titball 2004, Nat. Rev. Microbiol. 2(12):967–978) to BDC_extra's bib, for the "doses as low as 10 CFU" claim in the 4a discussion. Entry transcribed from `Grant_paper.pdf`'s reference list [36]. | Spec §4.3 says cite primary literature for the paper's grounding claims; the dose claim's primary source is Oyston et al. per the paper's own citation. |
| 2026-08-08 | Chapter 4a Appendix A table gains two rows (conditional rupture-time laws) beyond the draft's table; population table rows and flooding/young-cell/$r=0$ blocks move to 4b's Appendix A per spec §4.1. | Spec §4.1/§5.1 appendix split. |
| 2026-08-08 | In 4b's spectrum section, the Hawkes self-excitation kernel (draft $\phi$) is renamed $h$ — the classical triggering-function notation. | Spec §2.4 renames the boolean fraction to $\varphi$; both live in the same section, so the draft's $\phi$ for the kernel would have collided. $h(t)$ is standard for Hawkes kernels and creates no new collision. |
| 2026-08-08 | F4b.4 (partial-release continuum) omitted rather than flagged. | Spec §5.2 permits omission when the figure cannot be specified precisely; the flooding criterion as a function of $\varphi$ has no closed-form offspring law for the boolean process to plot against. |

## Log B — Formula changes

Record here any change to formula *content* (renaming β→λ etc. is logged once,
globally, not per occurrence). Every entry requires suite re-run results in Log F.

| Date | Location | Change | Suite results |
|---|---|---|---|
| 2026-08-08 | global | β→λ, R→H, `\Ihat`→`\Ifix`, $Y$→$W$, $I_\pm$→$a,b$ (renamings only, no content change) | renewal 54/54 PASS (Phase 0); chained 28/28 PASS (re-run after 4a conversion, Phase 2) |
| 2026-08-08 | BDC_extra §3 (PGF PDEs), derivation prose | Draft stated "$p_0(t)\equiv0$" under the catastrophe convention; replaced by the correct forward equation $\dot p_0=\mu p_1$ (internal extinction by death still feeds state 0). This corrects an erroneous draft *statement*; no verified formula was altered — the PDE displays themselves were already correct and are unchanged. | chained 28/28 PASS (2026-08-08, re-run as precaution; suites do not test this prose) |
| 2026-08-08 | Ch. 3 §08/§09 merged files | Wrong-sign forms replaced by the verified spec §6 forms: $K(I)=+2\lambda^2/\delta^2\,(I-\kappa)(I-a)(I-b)$; $\mathrm{E}[W_t^2]=\frac{2(\lambda-\mu)}{\delta}V-\frac{\lambda+\mu}{\delta}I-K+\frac{\lambda+\mu}{\delta}+1$; Var($W_t$) signs likewise. These are the corrections anticipated by the handoff (spec §3.2); the Chapter 4 draft and notes already contained the verified forms. | no formula-level change relative to the verified draft forms; suites green (renewal 54/54, chained 28/28, 2026-08-08) |
| 2026-08-08 | Ch. 3 §06 | Corrected $\Ifix$ derivation inserted (ODE branching term $\lambda(I^2-D^2)$; closed form $(a-b)^2w/[(B+Aw)(aw-b)]$; $\Ifix'(0)=-(\mu+\delta)$), replacing the draft-Chapter-3 wrong-ODE material. Verified against the Chapter 4 draft's corrected forms (spec §6) by hand (limits and initial slope checked). | suites green (above); no change to verified content |

## Log C — Figure-flag registry

Full generation specs live in `Project_specification.md` §§3.4, 4.2, 5.2;
this log is the placement registry only (fill in as flags are placed).

| ID | Title | Chapter/section | One-line purpose |
|---|---|---|---|
| F3.1 | Process transition diagram | Ch. 3, §Process definition (top) | the process at a glance |
| F3.2 | Rupture conventions | Ch. 3, Choice of rupture state | killing vs catastrophe |
| F3.3 | Fixation functions | Ch. 3, Analytical quantities (after $\Ifix$) | $I,D,I_{\mathrm{fix}}$ over time |
| F3.4 | Conditional mean convergence | Ch. 3, Analytical quantities (after $J$ figure) | the QS level preview |
| F3.5 | Burst-size preview | Ch. 3, What comes next | geometric burst law preview |
| F3.6 | Gillespie upgrade | Ch. 3, Process definition | re-render existing jpgs |
| F4a.1 | Joint-process schematic | Ch. 4a, §2 recap | $(X_t,W_t)$ at a glance |
| F4a.2 | Geometric slide of state probabilities | Ch. 4a, §5 state probs | geometric at every time, $P(t)\to1/a$ |
| F4a.3 | Convergence to the QSD | Ch. 4a, §6 QSD | conditional pmf → geometric limit |
| F4a.4 | Burst-time density | Ch. 4a, §7 burst time | defective density, mass $b$ at $\infty$ |
| F4a.5 | Burst size and late bursts | Ch. 4a, §7 size-bias | burst law + size-biased late mean |
| F4a.6 | Multiplicity of infection | Ch. 4a, §9 MOI | superlinear $g_k$ + rising conditional mean |
| F4a.7 | Chained transfer | Ch. 4a, §10 chained | negative-binomial sizes + decreasing intervals |
| F4a.8 | Conditional rupture time vs burst size | Ch. 4a, §7 τ-given-k | harmonic law + Gumbel + budding contrast |
| F4b.1 | Renewal construction schematic | Ch. 4b, §3 before the Result | the bookkeeping in one picture |
| F4b.2 | Flooding advantage: three regimes | Ch. 4b, §5 after the theorem table | $z_{\rm ext}$ burst vs bud, $L>1,=1,<1$ |
| F4b.3 | Growth-rate trade-off | Ch. 4b, §5 after the trade-off table | paired $r_{\rm bud}>r_{\rm burst}$ bars |
| ~~F4b.4~~ | Partial-release continuum | — | omitted: no closed-form offspring law to specify against (spec §5.2 permits) |

## Log D — Deletions and merges

| Date | What | Former location | Where the unique content lives now |
|---|---|---|---|
| 2026-08-08 | `01_opening.tex` (empty comment placeholder) deleted | `BDC_core/sections/01_opening.tex` (source: `3 BDC core/document MAIN/sections/01_opening.tex`, unchanged) | n/a — contained no content |
| 2026-08-08 | `10_variance_and_standard_deviation_of.tex` deleted (earlier partial draft of 08) | `BDC_core/sections/10_variance_...tex` (source unchanged) | its K(t)/Var(X) content was a subset of file 08's; merged file is `BDC_core/sections/08_variance_and_standard_deviation_of.tex` |
| 2026-08-08 | `11_variable_dependencies_on.tex` deleted (merged into 09) | `BDC_core/sections/11_variable_dependencies_on.tex` (source unchanged) | its correct $K(I)$ and compact $V(I)$ forms live in merged `BDC_core/sections/09_variable_dependencies_on.tex` |
| 2026-08-08 | Orphaned line "PLOT $\mean{\mathcal{K}}$ against $\delta$ for $\mu=0$, $\lambda=1$" removed | `BDC_core` old 05, after the $V(t)$ discussion | replaced by figure flag F3.5 (burst-size preview) in the closing section |
| 2026-08-08 | `$I_{\mathrm{death}}$` reference-value row removed (definition was inverted, never used) | old 03 reference values | replaced by $D:=p_0$ row and $\Ifix:=I-D$ row (spec §2.6 duty 5) |
| 2026-08-08 | `$\phi_k=\pr{\tau=i}$` reference-value row removed ($\tau$ is continuous; the row was ill-formed) | old 03 reference values | replaced by burst-time density row $\varphi(t)=\delta J(t)$ |
| 2026-08-08 | `\xdef\mydelt/\mybeta/\mymu/\mysum` parameter-stash lines removed | old 04/05 figure environments | parameter values written directly into captions |
| 2026-08-08 | Stray `\title{$\wt$}` line removed | old 04, second figure environment | n/a |
| 2026-08-08 | "(Is this correct?)" marker removed | old 05, multi-founder block | attached to the false claim $\Ifix[,{k}]=\Ifix^k$, which is replaced by $\Ifix[,{k}]=I^k-D^k$ |
| 2026-08-08 | Wrong $\Ifix$ material ($\hat I' = -(\beta+\mu+\delta)\hat I+\beta\hat I^2$, $\hat\eta$ closed form) removed | old 06, "Alternative quantity" subsection | corrected $\Ifix$ derivation (branching term $\lambda(I^2-D^2)$) in `BDC_core/sections/06_...tex` §6.4 |
| 2026-08-08 | `poem.jpeg` copied into `BDC_core/figures/` but deliberately unreferenced | source `figures/IMG_ch4/poem.jpeg` | stays on disk only (spec §3.4) |

## Log E — Build status

| Date | Build | Pages | Errors | Undefined refs | Overfulls | Notes |
|---|---|---|---|---|---|---|
| 2026-08-08 | BDC_core (baseline) | 18 | 0 | 0 | 0 | Phase 0 baseline; sources copied, figure paths flattened |
| 2026-08-08 | BDC_extra (baseline) | 32 | 0 | 48 | 2 | undefined refs expected: draft cross-refs to sections moving to 4b (fixed during split); placeholder discussion |
| 2026-08-08 | BDC_core (Phase 1 final) | 24 | 0 | 0 | 0 | all six figures referenced; flags F3.1–F3.6 rendered |
| 2026-08-08 | BDC_extra (Phase 2 final) | 34 | 0 | 0 | 0 | full conversion + enrichment + appendices; flags F4a.1–F4a.8 rendered; QS figures flattened |
| 2026-08-08 | BDC_odes (baseline) | 35 | 0 | 60 | 0 | undefined refs expected (same cause); 10 citation warnings transient (bbl resolves on later passes) |
| 2026-08-08 | BDC_odes (Phase 3 final) | 37 | 0 | 0 | 0 | full conversion + renamings + discussion + appendices; flags F4b.1–F4b.3 rendered; all 12 PDFs + 2 TikZ figures referenced |
| 2026-08-08 | all three (post prose pass) | 24 / 34 / 37 | 0 | 0 | 0 | final compile after Phase 4 prose edits; all 17 flags verified in PDF text |
| 2026-08-08 | all three (final QA) | 24 / 34 / 37 | 0 | 0 | 0 | definition-of-done compile state |

## Log F — Verification status

| Date | Suite | Result | Notes |
|---|---|---|---|
| 2026-08-08 | ad-hoc simulation check | PASS | Grant-paper conditional rupture-time laws verified before handoff: $\mathrm{E}[\tau\mid\mathcal{K}=n]=\theta^{-1}\sum_{k=1}^n 1/k$ (μ=0; rel. err ≤2.1e-3 at n=2,5,10,30) and $\mathrm{E}[\tau\mid\text{burst}]=\frac{1}{\lambda(1-b)}\log\frac{a-b}{a-1}$ (μ>0; rel. err 8.4e-4; burst fraction 0.811 vs $1-b$ = 0.812) |
| 2026-08-08 | renewal (54 checks) | PASS 54/54, 0 FAIL | Phase 0 green-state confirmation; wall time 17.1 s |
| 2026-08-08 | chained (28 checks) | PASS 28/28, 0 FAIL | Phase 0 green-state confirmation; wall time 34.9 s. Note: the chained suite's ₂F₁ series-vs-closed-form line may report "scipy unavailable" (no scipy in this environment) — expected; acceptance is the overall 28/28 PASS |
| 2026-08-08 | chained (28 checks), re-run | PASS 28/28, 0 FAIL | Phase 2 re-run after 4a conversion (formulas moved/renamed); wall time 34.5 s |
| 2026-08-08 | renewal (54 checks), re-run | PASS 54/54, 0 FAIL | Phase 3 re-run after 4b conversion; wall time 16.9 s |
| 2026-08-08 | renewal (54 checks), final QA | PASS 54/54, 0 FAIL | definition-of-done run |
| 2026-08-08 | chained (28 checks), final QA | PASS 28/28, 0 FAIL | definition-of-done run; wall time 34.9 s |

**Outstanding `TODO(verify)` bibliography entries (unchanged by design):**
mclean1993balance, nowak1996population, mckendrick1926applications,
vonfoerster1959some, gaver1965observations; Heffernan–Wahl and
Nelson–Gilchrist–Perelson have no entries (prose mentions only); Pakes et al.
1979 pending in Chapter 3.
