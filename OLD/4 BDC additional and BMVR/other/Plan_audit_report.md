# Plan Audit Report — Three-Chapter BDC Build

**Auditor role:** independent plan auditor (read-only; no plan rewrites; no implementation)  
**Date:** 2026-08-08  
**Package audited:** `Startup.md`, `Project_specification.md`, `Progress.md`  
**Sources checked:** `document MAIN/`, `3 BDC core/document MAIN/`, `Grant_paper.pdf`, `new_notes3/`, verification reports, figure folders, `references.bib` files  

---

## 1. Executive summary

**Verdict: READY WITH FIXES**

The handoff package is strong: the split at §11, the unified notation regime, the formula reference (§6), the Grant-paper translation table (§2.7), the figure-flag system, the verification discipline, and the phased task breakdown are coherent and largely faithful to the sources. An execution agent could build the three chapters from this package alone **after a short list of fixes**, the most important of which is a **wrong resolution of the Chapter 3 multi-founder non-fixation claim**.

| Severity | Count |
|---|---|
| **BLOCKER** | 1 |
| **SHOULD-FIX** | 8 |
| **IMPROVEMENT** | 6 |
| **QUESTION** | 2 |

**Three most important items**

1. **BLOCKER — `Î_k = Î^k` is false, but the plan treats the adjacent doubt as “it is correct.”** Source lines put `(Is this correct?)` under `Î_k = Î^k`, not under `I_k = I^k`. Following Progress 1.4 / Spec §3.1–3.2.6 literally would ship a known-wrong multi-founder formula in Chapter 3 (or its converted `I_fix,k = I_fix^k` form).
2. **SHOULD-FIX — Cross-document section pointers to the formula block are off by one** (many “§5” references mean the formula reference, which is §6; Startup figure-flag pointers say §6 but flags live in §7). A cold agent will waste time or open the wrong section.
3. **SHOULD-FIX — Figure copy paths are under-specified** after “flatten `IMG_ch4` / copy QSmean”: current `\includegraphics` paths still contain `IMG_ch4/` and `IMG_ch5/QSmean/`. Without an explicit “rewrite paths” step, Phase 0 compiles fail.

Overall mathematical content of Spec §6, the Grant-paper conditional-time laws (with root swap), the Ch3 defect inventory (except the `I_k`/`Î_k` misread), figure counts, verification tallies (54 and 28), and bibliography keys check out.

---

## 2. Findings

### BLOCKER

#### B1. Multi-founder non-fixation: plan resolves the wrong claim as “correct”

| | |
|---|---|
| **Severity** | **BLOCKER** |
| **Location** | Spec §3.1 (file 05 row), §3.2 item 6; Progress task 1.4 |
| **Issue** | The plan says delete `(Is this correct?)` because “the claim is correct” and “`I_k = I^k` retained as correct.” In the source, the doubt marker sits on the **false** claim `Î_k = Î^k`, not on the true claim `I_k = I^k`. Chapter 4a’s own remark “A guess that fails” proves `Î_k = I^k − D^k ≠ Î^k` when μ>0. An agent that “resolves (it is correct)” will keep a false formula; after `\Ihat→\Ifix` conversion it becomes the still-false `I_{\mathrm{fix},k}=I_{\mathrm{fix}}^k`. |
| **Evidence** | `3 BDC core/.../05_analytical_quantities.tex` lines 65–68: |
| | `I_k(t)=\cdots=I(t)^k` (true); then `Î_k(t)=\cdots=(Î(t))^k` + `(Is this correct?)`. |
| | Draft `09_multiplicity_of_infection.tex` Remark “A guess that fails”: correct is `Î_k=I^k−D^k`; at (1,0.2,0.05), t=1: `Î_2≈0.8458` vs `Î^2≈0.6542`. |
| | Spec §3.2.6 only names `I_k=I^k`; it never instructs replacing `Î_k=Î^k`. |
| **Proposed fix** | Rewrite the task explicitly: (i) keep `I_k=I^k` with a one-line branching justification; (ii) **delete or replace** `Î_k=Î^k` by `I_{\mathrm{fix},k}=I^k−D^k` (or defer multi-founder non-fixation to Chapter 4a and remove the false line); (iii) delete the doubt marker because the false claim is removed, not because it was true. Align Progress 1.4 with that wording. |

---

### SHOULD-FIX

#### S1. Formula-reference section numbers are wrong throughout the package

| | |
|---|---|
| **Severity** | **SHOULD-FIX** |
| **Location** | Spec §§3.3, 3.4 (F3.3), 4.1 (§2 row), 5.1 (§1 row), 5.2 (F4b.2); also Spec §2.7 “§4.2/§4.4/§5.1” for paper results |
| **Issue** | Key formulas live in **§6**. Multiple instructions say “boxed formulas from §5” / “closed forms of §5.” Spec §5 is Chapter 4b construction. Spec §2.7 points paper results at §4.2/§4.4, but paper enrichment is in §4.1 (and figures are §4.2). |
| **Evidence** | Spec §3.3: “closed forms exactly as given in §5 of this specification”; §4.1: “Boxed formulas from §5 below”; §6 is titled “Key formula reference (verified; use exactly).” |
| **Proposed fix** | Global replace of those pointers to **§6**. Fix §2.7 to “§4.1 / §5.1 (and formula block §6).” |

#### S2. Startup points figure flags at specification §6 (actual: §7)

| | |
|---|---|
| **Severity** | **SHOULD-FIX** |
| **Location** | Startup.md §§1, 5.5, Definition of done item 5 |
| **Issue** | “specification §6” is used for the figure-flag system; §6 is formulas, §7 is flags. |
| **Evidence** | Startup line ~54: “Flag format and seed lists are in the specification (§6)”; DoD item 5: “listed in specification §6.” Spec §7 is “The figure-flag system.” |
| **Proposed fix** | Change those Startup pointers to §7. |

#### S3. Figure-flag registry pointer names the wrong Progress log

| | |
|---|---|
| **Severity** | **SHOULD-FIX** |
| **Location** | Spec §7 last paragraph |
| **Issue** | “Keep a registry … in `Progress.md` §F.” Log F is **Verification status**; the figure-flag registry is **Log C**. |
| **Evidence** | Spec §7: “`Progress.md` §F”; Progress.md Log C = Figure-flag registry; Log F = Verification status. |
| **Proposed fix** | Say “Log C — Figure-flag registry.” |

#### S4. Flattened figure copies will break `\includegraphics` paths unless rewritten

| | |
|---|---|
| **Severity** | **SHOULD-FIX** |
| **Location** | Progress 0.2, 0.3; Spec §3.4, §4.2 |
| **Issue** | Plan says flatten `IMG_ch4/*` into `BDC_core/figures/` and copy QS1/QS2 into `BDC_extra/figures/`, but does not require updating include paths. Source paths are nested. |
| **Evidence** | Ch3: `figures/IMG_ch4/BDRsimulations.jpg` (and five more). Ch4a: `figures/IMG_ch5/QSmean/QS1` (and QS2). Ch4b PDFs already use `figures/kernels.pdf` etc. (OK if copied flat). |
| **Proposed fix** | Add acceptance criteria: after copy, every `\includegraphics` resolves; explicitly “rewrite paths to `figures/<filename>`” (and for QS, drop `IMG_ch5/QSmean/`). |

#### S5. Typo list includes “Brokewel”, which is not in the source

| | |
|---|---|
| **Severity** | **SHOULD-FIX** |
| **Location** | Spec §3.1, file `02_chapter_introduction.tex` row |
| **Issue** | Agent is told to fix “Brokewel”; the file already has “Brockwell”. Harmless waste, but signals the typo list was not re-checked against the current files. |
| **Evidence** | Intro line ~26: `Brockwell et. al. 1982`. Grep for `Brokewel`: 0 hits. All other listed typos **do** exist (continuois, occuring, macrophaegs, arives, behavious, accross, astroid, mammels, sppured, provinding, evoultionary, populance). |
| **Proposed fix** | Drop “Brokewel” from the list; optionally add real remaining issues (e.g. “et. al.” → “et al.”; “have have” in 05). |

#### S6. Chapter 3 `E[W²]` wrong formula is documented, but the merge task should force the corrected IC story

| | |
|---|---|
| **Severity** | **SHOULD-FIX** |
| **Location** | Spec §3.2 item 4; Progress 1.7; source file 08 |
| **Issue** | Spec gives the correct formula (matches draft appendix and `new_notes3`). File 08 has wrong signs and `K(0)=0`. Task 1.7 says “corrected final formula” but does not explicitly say to replace the wrong IC paragraph and the sign-of-`J` slip that caused it. A minimal search-replace of the final display could leave contradictory derivation prose. |
| **Evidence** | File 08 `meanEY2`: `2(β−μ)/δ V + (β+μ)/δ I + K − (β+μ)/δ` with IC `K(0)=0`. Correct (notes + draft 02 + Spec §6): `2(λ−μ)/δ V − (λ+μ)/δ I − K + (λ+μ)/δ + 1` with `K(0)=1`. |
| **Proposed fix** | In 1.7, require replacing the derivation block through the IC line (not only the final display), citing Spec §3.2.4 / draft Remark “Correction and check” content *without* the “Chapter 3 was wrong” framing. |

#### S7. Long figure-flag specs vs “0 overfull boxes” acceptance criterion

| | |
|---|---|
| **Severity** | **SHOULD-FIX** |
| **Location** | Spec §7 macro; acceptance criteria §§3.6, 4.4, 5.4; Startup DoD; Progress 1.14, 2.13, 3.12, 5.1 |
| **Issue** | Flags put multi-paragraph generation specs inside `\fcolorbox...\parbox{0.94\linewidth}{...}`. Dense unbreakable math or long paths can create overfull `\hbox`es, fighting the hard “0 overfulls” gate. Current Chapter 4 draft log shows 0 overfulls (only underfulls), so the bar is currently met but fragile. |
| **Evidence** | Spec §7 macro; DoD “0 overfull boxes; figure flags intentional.” |
| **Proposed fix** | Either (a) allow overfulls **inside** figure-flag boxes only, or (b) prescribe `\sloppy` / `\raggedright` / `\small` / `\url`-style breaking inside the flag macro. State the rule in Spec §7 and the acceptance criteria. |

#### S8. Discussion open-problem split needs an explicit cut list from draft §17

| | |
|---|---|
| **Severity** | **SHOULD-FIX** |
| **Location** | Spec §4.1 Discussion row, §5.1 Discussion row; Progress 2.9, 3.8; draft `17_discussion.tex` |
| **Issue** | Draft §17 is a single discussion mixing assay predictions, fitting consequences, forward links, and a six-item open-problem list. Spec assigns themes to 4a vs 4b but does not map each draft subsection/item. “General-μ chained joint laws” is required for 4a open problems but is not a numbered open item in draft §17 (it lives in §10). Agent must invent the cut. |
| **Evidence** | Draft subsections: assay (→4a), fitting (→4b), forward (→4b), open problems 1–6 mixed. Spec 4a open problems: burst=QSD, general-μ chained, logistic. Spec 4b: flooding boundary, population variance, partial-release `φ`, two-type moments, literature. |
| **Proposed fix** | Add a one-row mapping table: draft subsection/item → 4a / 4b / drop, including where “general-μ chained” is sourced (§10). |

---

### IMPROVEMENT

#### I1. Orphan draft files not listed as “ignore”

| | |
|---|---|
| **Severity** | **IMPROVEMENT** |
| **Location** | Spec §4 / §5 sources; `document MAIN/sections/` |
| **Issue** | `01_opening.tex` (empty), `02_specification_of_rupture_state.tex`, `09_potential_application_in_bmvr.tex` exist but are **not** `\input` in `document MAIN/main.tex`. Plan never says to ignore them. |
| **Evidence** | `main.tex` inputs 01_chapter_introduction … 17 + A/B/C only. |
| **Proposed fix** | One line: “Files not in `main.tex`’s `\input` list are orphans; do not copy.” |

#### I2. β→λ occurrence count is approximate

| | |
|---|---|
| **Severity** | **IMPROVEMENT** |
| **Location** | Spec §2.6 |
| **Issue** | “≈140 occurrences”; actual `\beta` count in Ch3 section files is ~123. |
| **Proposed fix** | Say “all `\beta` in body sections 04–11” without a count, or “~120.” |

#### I3. File 11 intermediate prose still has `J = δ^{-1} I'` even though final `J(I)` is right

| | |
|---|---|
| **Severity** | **IMPROVEMENT** |
| **Location** | Spec §3.1 merge of 09+11; source file 11 lines 6–10 |
| **Issue** | Merge instructions focus on `K(I)` / `V(I)` correctness; file 11’s lead-in still writes `J = δ^{-1} dI/dt` (sign error that cancels later). |
| **Proposed fix** | When merging, force `J = −δ^{-1} I'` and `I' = λ(I−a)(I−b)` consistently. |

#### I4. Progress Log C pre-fills F3.1–F3.6 but not F4a/F4b detail

| | |
|---|---|
| **Severity** | **IMPROVEMENT** |
| **Location** | Progress Log C |
| **Issue** | F4a.1–F4a.8 and F4b.1–F4b.3 are stubs; fine for tracking, but a cold agent might think full specs only exist for Chapter 3. Spec §§4.2, 5.2 already have full specs. |
| **Proposed fix** | One line under Log C: “Full generation specs live in Spec §§3.4, 4.2, 5.2; Log C is the placement registry only.” |

#### I5. Chained suite notes “scipy unavailable” for ₂F₁ closed form

| | |
|---|---|
| **Severity** | **IMPROVEMENT** |
| **Location** | Environment (Startup §6); report `verify_chained_transfer_report.txt` |
| **Issue** | Suite still totals 28 PASS, but the ₂F₁ cross-check is skipped without scipy. Plan says no scipy (correct). Agent might worry a “skip” is a failure. |
| **Proposed fix** | Note in Progress Log F / Startup: “₂F₁ series-vs-closed-form line may report scipy unavailable; overall 28/28 PASS is the acceptance criterion.” |

#### I6. Optional: compile-smoke the figure-flag macro in the package

| | |
|---|---|
| **Severity** | **IMPROVEMENT** |
| **Location** | Spec §7; Progress 0.5–0.7 |
| **Issue** | Macro needs `xcolor`. Sources already load it; skeleton `main.tex` instructions say “package list of the source,” so this is fine if followed. A one-line “must include `xcolor`” would remove a failure mode. |
| **Proposed fix** | Add `xcolor` (and `hyperref` after it) to the explicit package minimum for each `main.tex`. |

---

### QUESTION

#### Q1. Publication status / citation form for `Grant_paper.pdf`

| | |
|---|---|
| **Severity** | **QUESTION** |
| **Location** | Spec §4.3; Progress 0.11, 2.15 |
| **Issue** | Plan correctly defers the citation decision to the agent’s Log A (“in preparation” vs other). User should confirm preferred citation string and author list before final bibliography lock. |
| **Evidence** | Spec: “cite it as ‘Aldridge et al., in preparation’ (or the status recorded in Progress.md).” PDF title page lists six authors, dated 1 April 2026. |

#### Q2. Hard “0 overfull boxes” vs thesis aesthetics

| | |
|---|---|
| **Severity** | **QUESTION** |
| **Location** | Startup DoD; all chapter acceptance criteria |
| **Issue** | Zero overfulls is stricter than many thesis workflows (underfulls already exist in the Chapter 4 draft). Confirm whether underfulls are allowed (presumably yes) and whether flag-internal overfulls are forbidden. |
| **Related** | Finding S7. |

---

## 3. Spot-check results table (audit brief §B)

| Spot-check item | Result | Note |
|---|---|---|
| Spec §6 single-cell formulas vs draft App. A / `new_notes3` | **PASS** | Match under β→λ; `I,D,I_fix,J,K,V,V_∞,E[W²],φ,QSD,K(I),MOI,chained` agree with App. A and notes master tables. |
| Spec §6 population formulas vs draft App. A | **PASS** | Renewal system, `p_eff`, `d_eff`, limits, `G_off`, `z_ext`, flooding `Δz`, variance gap match. |
| Conditional rupture times vs `Grant_paper.pdf` (incl. root swap) | **PASS** | Paper (3.22): `E[τ\|R=n]=(1/σ)H_n`, σ=λ+α → θ=λ+δ. Paper (3.26): `E[τ\|τ<∞]=1/(λ(1−a))log((b−a)/(b−1))` with 0<a<1<b → unified `1/(λ(1−b))log((a−b)/(a−1))`. Numeric identity checked. Distinct from `E[T_prod]`. |
| §2.7 translation table vs paper notation | **PASS** | α→δ (catastrophe); paper δ→`d_I`; roots swapped 0<a<1<b → b<1<a; R→`K`; g(t) geometric ratio ↛ release kernel g. Optional μ=0 `r,σ` shorthands correctly scoped. |
| Ch3 `(I−I₊)(I−I₊)` Riccati typo | **PASS** | File 06 line 36: `β(I−I₊)(I−I₊)`. |
| Ch3 `K(I)` conflict 08/09 vs 11 | **PASS** | 08/09: `−2β²/δ (I−κ)…` wrong; 11: `+2β²/δ² (I−k)…` matches Spec §6. |
| Ch3 duplicate section pairs 08+10, 09+11 | **PASS** | All four files `\input` in Ch3 `main.tex`; 10 is partial of 08; 11 is alternate of 09. |
| Ch3 duplicate `BDRsims` label | **PASS** | File 04 lines 20 and 49; log: multiply defined. |
| Ch3 `Voft` in `equation*` | **PASS** | File 07 lines 73–76: `\begin{equation*}\label{Voft}` (label on unnumbered env). |
| Ch3 orphaned “PLOT…” line | **PASS** | File 05 line 131. |
| Ch3 “(Is this correct?)” | **CONCERN** | Exists, but plan misattributes which claim it doubts — see **B1**. |
| Ch3 claimed typo list | **CONCERN** | 12/13 typos present; **Brokewel absent** — see **S5**. |
| Content map §4.1 (4a ← draft 01–10 + partial 17/A/C) | **PASS** | Mapping matches `main.tex` inputs; draft 07 title is “Burst time and burst size” as planned. Orphans not mapped (I1). |
| Content map §5.1 (4b ← draft 11–17 + partial A/B/C) | **PASS** | Split at file 11 matches Startup/settled decision; discussion split thematically sound but under-specified (S8). |
| Figure inventory: 12 PDFs in `document MAIN/figures/` | **PASS** | Exactly the 12 named PDFs; QS pair under `IMG_ch5/QSmean/`; extras `QSmeanNE0.png`, `QSMu0.png` unreferenced (OK). |
| Figure inventory: QSmean pair | **PASS** | QS1.png, QS2.png present and used in draft 06. |
| Figure inventory: six Chapter 3 figures + poem | **PASS** | Six named + `poem.jpeg` unreferenced as planned. |
| Verification tally renewal 54 | **PASS** | Report: `SUMMARY: 54/54 checks passed`. |
| Verification tally chained 28 | **PASS** | Report: `TOTAL: 28 PASS / 0 FAIL`. |
| Bib keys to copy from `document MAIN/references.bib` | **PASS** | All named keys exist: brockwell1982birth, karlin1957/1982, di2008note, van2011quasi, yaglom1947certain, mckendrick, vonfoerster, hataye, perelson1996hiv, nowak1996, mclean1993, pearson2011, gilchrist2006. `williams2024/2021` correctly supplied as new entries. Ch3 has 5 entries; brockwell to be added. |
| Draft page claims (59 / 20) | **PASS** | `pdfinfo`: 59 and 20 pages. Clean compile claim: 0 overfulls in current Ch4 log. |
| Progress ad-hoc Grant-paper simulation log | **PASS** | Consistent with paper formulas; not re-run (per audit rules). |

---

## 4. Internal consistency (audit brief §C) — condensed

| Topic | Status |
|---|---|
| Split at draft §11 | Consistent across Startup, Spec §4–5, Progress Phases 2–3. |
| Unified notation (λ, H, I_fix, D:=p₀, W, b<1<a, δ catastrophe) | Consistent; conversion duties §2.5–2.6 match §2.1 table. |
| Figure-flag IDs F3 / F4a / F4b | Consistent seed lists; Log C incomplete for 4a/4b by design. |
| Correction-remark deletion list | All named remarks exist in draft 02, 09, 10; “53 vs 54” history note exists in App. B. |
| §2.4 collisions κ→ζ, boolean q→φ | Confirmed real collisions in draft 15 (κ intensity decay; boolean q). |
| Settled decisions vs documents | No contradiction found with the settled list in the audit brief §D. |
| Cross-doc section pointers | **Broken** in places — S1–S3. |

---

## 5. Risks and failure modes (audit brief §E)

| Risk | Assessment |
|---|---|
| LaTeX macros / `\Ifix` | `\Ifix` does not exist in sources; must be defined in each `main.tex`. Spec is clear. |
| Label schemes across three builds | Duplicate-label fixes (BDRsims, Kderev, Voft) are listed; after split, 4a/4b may still share labels if both keep draft labels — usually OK (separate compiles). |
| Figure-flag macro robustness | Needs `xcolor`; long specs → overfull risk (S7). |
| Math in section titles / hyperref | Draft section titles are mostly text; low risk. TikZ spectrum/HIV kept as-is. |
| Suite re-run after formula changes | Clear: renames ≠ formula change; content change → Log B + Log F. Phase milestones re-run the relevant suite. “Both suites” on any formula change is slightly heavy but unambiguous. |
| Figure-flag spec quality | F3 and F4a specs are detailed enough for a later figure agent; F4b.3 gives numeric growth-rate pairs and says “verify against characteristic equation” — good. F4b.4 correctly optional. |
| Prose guidance | `/aa-flow-lucid` + Grant paper as register is actionable; skill exists on disk. British English / no correction-history remarks are crisp. |
| No scipy / TeX Live 2024 | Matches environment; suites already avoid hard scipy dependency for the pass criterion. |
| Path flatten without rewrite | High practical risk — S4. |
| Wrong `Î_k` kept | High mathematical risk — **B1**. |

---

## 6. Open questions for the user

1. **Grant paper citation:** Confirm the bibliography string (e.g. “Aldridge, Whaler, López-García, Molina-París, Gillard & Lythe, in preparation, 2026” vs shorter “Aldridge et al.”).
2. **Overfull policy:** Must figure-flag boxes also be overfull-free, or only the real chapter prose/floats?
3. **Chapter 3 multi-founder scope:** Prefer fixing `I_fix,k=I^k−D^k` in Chapter 3 now, or strip multi-founder non-fixation from Chapter 3 and leave it entirely to Chapter 4a?

---

## 7. What the plan gets right (fair balance)

- Settled architecture (3+4a+4b, split at §11, no new figures, flags with specs, suites never edited) is documented consistently.
- Unified notation and Grant-paper translation (especially **swapped roots** and **α/δ**) are correct and necessary; formulas were re-derived/checked against the paper and notes.
- Chapter 3 defect inventory is largely accurate and actionable (Riccati typo, `K(I)`, `E[W²]`, duplicates, `Voft`, PLOT line, intro typos, mixed λ/β in `J(t)`).
- Verification tallies and figure inventories match the filesystem.
- Bibliography plan is complete for cited keys; `TODO(verify)` policy is honest.
- Formula block §6 is high quality and aligns with the verified Chapter 4 draft.

---

## 8. Recommended pre-execution patch list (for the package owner)

Minimal set before handing to an execution agent:

1. Fix **B1** (`Î_k` / doubt resolution) in Spec §3.1–3.2 and Progress 1.4.  
2. Fix section pointers **S1–S3** (§6 formulas, §7 flags, Log C registry).  
3. Add explicit path-rewrite step **S4**.  
4. Trim “Brokewel” **S5**; harden `E[W²]` derivation task **S6**.  
5. Soften or special-case overfull rule for flags **S7**; add discussion cut table **S8**.  

After those, verdict would upgrade to **READY**.
