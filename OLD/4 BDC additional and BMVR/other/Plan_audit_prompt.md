# Plan Audit — Agent Brief

## Mission

You are an independent **plan auditor**. A handoff package has been written for
a fresh execution agent that will build three polished thesis chapters
(`BDC_core`, `BDC_extra`, `BDC_odes`) from existing sources. Your job is to
read the entire handoff package and enough of the underlying source material
to judge it, then deliver a written report identifying **issues, risks, and
potential improvements**. You are adversarial but fair: assume nothing, verify
claims against the sources, and distinguish genuine defects from matters of
taste. **You do not implement anything and you do not rewrite the plan** —
your only written output is the report.

Work from this directory:
`/Users/adamaldridge/Desktop/Thesis content 🎓 /4 BDC additional and BMVR/`

## Reading list (in this order)

1. **The handoff package (read in full):**
   - `Startup.md` — overview, state of work, guardrails, definition of done.
   - `Project_specification.md` — the binding specification (notation regime,
     per-chapter construction specs, figure-flag system, formula reference,
     prose standard).
   - `Progress.md` — the phased task breakdown and tracking logs.
2. **The primary sources (verify the plan's claims against these):**
   - `document MAIN/sections/01…17 + A/B/C` — the completed 59-page Chapter 4
     draft that Chapters 4a/4b are built from. Read enough to check the
     specification's content-mapping tables (§4.1, §5.1) against reality.
   - `3 BDC core/document MAIN/` — the Chapter 3 source. Check the
     specification's §3 error list (mathematical errors, duplicates, typos,
     label problems) against the actual files.
   - `Grant_paper.pdf` (17 pages, read in full) — the co-authored paper used
     as source and register model. Check the specification's §2.7 translation
     table and every formula attributed to the paper.
   - `new_notes3/Comprehensive_Corrected_Notes.tex` — the corrected master
     notes; authoritative for formulas where the draft and notes are cited.
   - `CHAPTER4_PLAN.md` — history of how the draft was built (context for
     errata claims).
3. **Supporting material (skim as needed):** `new_notes/`, `new_notes2/`,
   `N=2 Immediate Transfer content/`, the two verification reports
   (`new_notes3/verify_result_20_1_report.txt`,
   `N=2 Immediate Transfer content/verify_chained_transfer_report.txt`),
   `document MAIN/references.bib`, and the figure folders
   (`figures/`, `document MAIN/figures/`, `3 BDC core/document MAIN/figures/`).

## What to audit

**A. Completeness and clean-context executability.** The execution agent
starts with an empty context and only these documents. Identify anywhere it
would have to guess, backtrack, or make an unguided judgment call: missing
definitions, unstated ordering constraints, tasks without acceptance
criteria, references to things not introduced, ambiguities a fresh agent
could plausibly resolve the wrong way.

**B. Factual and formula correctness.** Do not trust the plan's claims —
spot-check them. Concrete checks (at minimum):
   - Every formula in specification §6 against the draft's appendices and
     `new_notes3`; the two conditional rupture-time formulas attributed to
     `Grant_paper.pdf` against the paper (including the root-labelling
     translation).
   - The §2.7 translation table against the paper's actual notation
     (especially the swapped root labels and the α/δ swap).
   - Each Chapter 3 defect listed in §3.1–3.2 (the `(I−I₊)(I−I₊)` typo, the
     K(I) coefficient conflict between files 08 and 11, the duplicate section
     pairs, the `BDRsims` duplicate label, the `Voft` label in an unnumbered
     environment, the orphaned "PLOT…" line, the "(Is this correct?)" line,
     the claimed typo list) — verify each exists where the plan says it does,
     and check whether the plan missed any comparable defect.
   - The content-mapping tables (§4.1, §5.1) against the actual draft files.
   - The claimed figure inventories against the actual folders (12 PDFs in
     `document MAIN/figures/`; QSmean pair; the six Chapter 3 figures).
   - The claimed verification tallies (54 checks; 28 checks) against the
     actual report files.
   - That every bib key the plan says to copy actually exists in
     `document MAIN/references.bib`.

**C. Internal consistency across the three documents.** Section numbers,
cross-references between the documents, figure-flag IDs (F3.x, F4a.x,
F4b.x), task IDs, the notation table vs the formulas vs the conversion
duties, the split point (§11), the discussion split between 4a and 4b, the
appendix splits.

**D. Coherence with settled decisions.** The following are settled and are
**not** open for relitigation — only flag a document if it contradicts them:
the split at §11; the unified notation (λ birth, H rupture state,
I_fix = I − D, D := p₀, W post-catastrophe count, roots b < 1 < a, δ the
catastrophe rate); Chapter 3 upgraded with nothing removed; correction-history
remarks deleted from 4a/4b; no new figure generation (flags with detailed
specs instead); chapter-number-only cross-references; the guardrails and
recovery model; the prose standard (/aa-flow-lucid plus the paper as register
model, thesis prose naturally more expansive).

**E. Risks and failure modes.** LaTeX build risks (macro definitions, label
schemes across three builds, the figure-flag macro's robustness, hyperref
bookmark warnings from math in section titles, bibliography completeness);
the "re-run suites after formula changes" rule (is it clear when it
triggers?); figure-flag spec quality (would a later figure agent actually be
able to generate each flagged figure from its spec alone?); prose-guidance
actionability; anything in the environment assumptions (no scipy; TeX Live
2024) that the plan relies on unstated.

## Constraints

- **Read-only**, with exactly one exception: you create
  `Plan_audit_report.md` at the folder root. Do not modify the handoff
  documents, the sources, the notes, the suites, or any build folder.
- Do **not** re-run the verification suites (their reports would be
  overwritten); read the existing reports instead.
- You may compile the existing `document MAIN/main.tex` to check build claims
  if you judge it necessary (this touches only build artifacts), but never
  edit its sources. You may compile-test the figure-flag macro in a scratch
  folder of your own (e.g. `_audit_scratch/`) if you wish; remove nothing
  else.
- Stay bounded: thorough, but do not attempt exhaustive proof-checking of
  every derivation. Prioritise the spot-check list above and anything that
  smells wrong.

## Deliverable

Write `Plan_audit_report.md` at the folder root with:

1. **Executive summary** — overall verdict: `READY` / `READY WITH FIXES` /
   `NOT READY`, with counts of findings by severity and the three most
   important items.
2. **Findings**, each with: severity tag (**BLOCKER** — execution would fail
   or produce wrong output; **SHOULD-FIX** — real defect or meaningful risk;
   **IMPROVEMENT** — worth doing, not required; **QUESTION** — needs the
   user's judgment), location (document and section), the issue, the
   evidence (quote the relevant lines), and a concrete proposed fix.
3. **Spot-check results table** — each item from section B above with
   PASS / FAIL / CONCERN and a one-line note.
4. **Open questions for the user**, if any.

Then return an inline summary of the report: the verdict, the counts by
severity, and the full text of every BLOCKER and SHOULD-FIX finding.
