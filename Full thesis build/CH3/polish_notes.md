# Polish notes: targeted fix specifications for Chapter B

**Working source:** `chapterB.tex` (structure of draft 2A — Galton–Watson and the constant \(A(p)\)).  
**PDF build:** `chapterB.pdf` (compile from this folder).  
Do not reverse the 2A section order or restore 1A’s spine. Apply only the fixes below.

---

## Technical correctness

### F1 — Handle \(p = 0\) precisely
- **Where:** Definition of \(A(p)\) and any use of \(S_n/(2p)^n\).
- **Problem:** The ratio \(S_n/(2p)^n\) is not defined for \(n \ge 1\) when \(p = 0\).
- **Fix:** State the main definition for \(0 < p < 1/2\). Define \(A(0) = 1/2\) by continuous extension and/or the product formula. Ensure all statements that use the ratio are restricted to \(p > 0\) or rewritten for the \(p = 0\) case.

### F2 — Critical-section sample-mean wording
- **Where:** Critical case discussion of sample averages / infinite mean.
- **Problem:** An infinite-mean power-law sample average need not increase monotonically with sample size.
- **Fix:** Replace monotonic-growth claims with: the sample mean does not converge to a finite expectation and is repeatedly dominated by rare, very large observations.

### F3 — Numerical discussion: convergence criterion and cutoff
- **Where:** Practical / computational scheme for \(A(p)\).
- **Problem:** Text that treats \(S_n\) as becoming “stationary” is wrong; the proposed cutoff \(c = 0.49999\) is presented without an error criterion.
- **Fix:**
  1. Monitor convergence of the **normalised ratio** or the **truncated product**, not of \(S_n\) itself.
  2. Replace the universal-looking cutoff with an error criterion (or justify \(c = 0.49999\) in terms of a stated tolerance).

### F4 — Hypertranscendence caveat (everywhere)
- **Where:** Abstract, §5 (Koenigs / Becker–Bergweiler), conclusion, and any parallel claim.
- **Problem:** Easy to overclaim that hypertranscendence kills an elementary formula for \(p \mapsto A(p)\).
- **Fix:** Keep this distinction consistent in every place the claim appears:
  - Hypertranscendence rules out an elementary formula for \(z \mapsto \psi_r(z)\) at fixed \(r\).
  - It does **not** by itself prove that \(p \mapsto A(p) = 2\psi_{2p}(1/2)\) has no elementary form.
- **Do not** restore 1A’s abstract wording that transfers the theorem from \(\psi_r\) to \(A(p)\).

---

## Structure and signposting

### F5 — Duplicated rescaling \(S_n = 2w_n\), \(r = 2p\)
- **Where:** Opening of §4 and derivation in §5.
- **Problem:** §4 introduces the substitution; §5 re-derives it from scratch.
- **Fix:** Let §4 own the definition. In §5, **recall** it only (no second full derivation).

### F6 — Introduction: promised order vs delivered order
- **Where:** Framing paragraph / roadmap in the introduction.
- **Problem:** Stated order is exists → computed → elementary expression. Delivered order is exists (§3–4) → elementary (§5) → computed (§6–8).
- **Fix:** Swap the last two items in the roadmap sentence so the promise matches the chapter: existence → elementary / dynamical identification → computation (and near-critical).

### F7 — §2 → §3 transition: drop routing scaffolding
- **Where:** Seam between §2 and §3 (or equivalent “critical returns later” bridge).
- **Problem:** Phrases that narrate the chapter’s own routing (e.g. that the critical endpoint returns immediately before near-critical analysis) are scaffolding, not argument.
- **Fix:** Remove self-routing. Prefer a content promissory note in the spirit of 1A at that seam (extinction certain, yet expected lifetime infinite), without mapping the later section plan.

---

## Prose and figures

### F8 — Section 5 polish (prose and notation)
- **Where:** Logistic map / Koenigs section.
- **Problem:** Rough phrasing (e.g. “Taking, the nonlinear map”; “Here will be demonstrated”); Koenigs definition may be incomplete or notationally inconsistent.
- **Fix:** Rewrite broken or incomplete sentences. Define the Koenigs function with consistent notation and complete grammatical statements throughout the section.

### F9 — Chaos / bifurcation figure
- **Where:** Figure using the logistic bifurcation diagram with \(r > 1\).
- **Problem:** The branching problem uses \(0 < r < 1\); the chaotic regime is an aside that does not advance the subcritical argument.
- **Fix:** Either remove the figure, move it to an optional remark/appendix with an explicit “aside” label, or replace it with a figure for the attracting regime \(0 < r < 1\) that the argument actually uses.

---

## Out of scope

- Do **not** return to 1A’s overall structure (critical-first spine; formula search as main-text finale; no conclusion).
- **Keep** from 2A: order mean → product → Koenigs → critical → near-critical → practice → conclusion; careful BB wording; formula search in Appendix B; dedicated conclusion.
- Optional only: isolated critical-section tone from 1A — not its architecture.
- Do **not** re-open chapter architecture debates or import material from Chapter A / review trees unless a fix above requires a local wording change.
