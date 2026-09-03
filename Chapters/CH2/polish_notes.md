# Chapter A polish notes — targeted fix specifications

**Workspace:** this folder (`ChapterA/`)  
**Production sources:** `sections/*.tex`, `preamble.tex`, `chapter.tex`, `main.tex`  
**Holding file (not compiled):** `notes/bdc_material_for_later_chapters.tex`  
**Sibling process draft:** `3 BDC_core DRAFT U/` (destination for BDC-specific handoffs)  
**Do not compile** the holding file into Chapter A.

**Scope:** small, targeted edits to Chapter A; relocation only via the holding file or BDC core.  
Each item is one checkable fix. Do **not** restore full excised side paths into Chapter A.

**Current-tree notes (as of placement):**

| ID | Status in tree | Notes |
|----|----------------|--------|
| A1 | **Done** (2026-08-10) | Kept `\mathcal{E}_n`; both suggested alternatives collide with existing Chapter A notation. See pass record. |
| A2 | **Done** (2026-08-10) | Split three ways: `\delta` rate / `\chi` discrete probability / `\omega` hypergeometric ratio. |
| B1–B2 | **Done** (2026-08-10) | Caption rewritten; one residual cleveref-capitalisation style call left open. |
| B3 | **Done** (2026-08-10) | Narrowed to no-catastrophe probabilities up to the first trigger. |
| B4 | **Done** (2026-08-10) | Four sites routed through `\fwd`; no bare “later chapter” left. |
| C1 | **Done** (2026-08-10) | Swept for glued words, run-together sentences and doubled words; none found. |
| D1 | **Done** (2026-08-10) | One-paragraph bridge added at end of `m:sec:coupled`. |
| E* | Annotated, not integrated | Holding file carries three `INTEGRATION NOTE` blocks, incl. `T_0 \wedge T_H` and a newly found `\delta`/`\rho` inversion in the rupture block. |

---

## A. Notation

### A1. Cumulative exposure symbol

| | |
|---|---|
| **Where** | `sections/02_markov_chains.tex` — Remark `m:rem:notmeanfield` (`\mathcal{E}_n`); mirror any rename in `notes/bdc_material_for_later_chapters.tex` if still present |
| **Problem** | Historical risk: bare `E_n` collided with expectation. Tree now uses `\mathcal{E}_n`. |
| **Fix** | (1) Confirm no bare `E_n` remains for exposure. (2) If `\mathcal{E}_n` is still judged too close to expectation in prose, rename consistently to `A_n` or `S_n` (never `H_n`). |
| **Do not** | Use `H` for exposure (`H` is the rupture state). |
| **Done when** | Exposure has one symbol throughout; no expectation/exposure visual clash in the remark. |

### A2. One meaning for `\delta` (rate vs probability vs hypergeometric)

| | |
|---|---|
| **Where** | `sections/02_markov_chains.tex` — `m:def:bdc`, `m:eq:bdcrates`, Remark `m:rem:notmeanfield`; `sections/app_b_absorption_models.tex` (and any `\delta` in `app_c_*.tex` if used for the hypergeometric parameter) |
| **Problem** | Same letter: continuous per-capita catastrophe rate; discrete trigger probability in `(0,1)`; absorption/hypergeometric ratio `\alpha/(\lambda-\mu)` (or `\alpha/b_1`). |
| **Fix** | Disentangle symbols, e.g.: keep `\delta` for continuous rate **or** reassign; use a distinct letter (e.g. `\kappa`) for discrete per-individual trigger probability; use a third symbol for the hypergeometric ratio if it still needs a name. Update all equations, figure labels on the rate diagram (`\delta`, `2\delta`, `3\delta`), and prose cross-links. State the discrete–continuous counterpart relation once without reusing the rate letter as a bare probability. |
| **Done when** | Rate / discrete probability / hypergeometric parameter never share a letter silently; chapter still compiles with consistent notation. |

---

## B. Wording and captions

### B1. Figure rate-diagram caption — definition wording

| | |
|---|---|
| **Where** | `sections/02_markov_chains.tex` — caption of `m:fig:ratediagram` |
| **Problem** | Awkward “definition 1.3” style if present. |
| **Fix** | Prefer process-of-definition phrasing (tree already uses `\cref{m:def:bdc}` — keep or polish to “birth--death--catastrophe process of …”). |
| **Done when** | Caption is standard thesis English and cref-correct. |

### B2. Figure rate-diagram caption — structural contrast (optional)

| | |
|---|---|
| **Where** | Same caption as B1 |
| **Problem** | Caption should be self-contained if that is house style. |
| **Fix** | Ensure contrast is explicit: ordinary absorption only via state 1 vs catastrophe from any `n\ge1` at rate `\delta n` (or updated symbol). Avoid duplicating a full paragraph already in body text. |
| **Done when** | Caption alone states what the figure is for, or decision recorded that body text is enough. |

### B3. Narrow multi-founder factorisation claim

| | |
|---|---|
| **Where** | `sections/02_markov_chains.tex` — paragraph after `m:def:bdc` (~“probabilities for several founders factorise…”) |
| **Problem** | Claim is slightly too broad. |
| **Fix** | Restrict to **no-catastrophe** (pre-trigger) probabilities, up to the first trigger. Suggested shape: “No-catastrophe probabilities for several founders factorise into single-founder contributions up to the first trigger.” Align with the later sentence in `m:rem:notmeanfield` that already hedges factorisation before any trigger. |
| **Done when** | Claim matches independence actually used for generating functions under no rupture yet. |

### B4. Named chapter cross-references

| | |
|---|---|
| **Where** | Grep for `later chapter` / `later chapters` in `sections/*.tex` (at least `01_overview.tex`, `02_markov_chains.tex`, `03_methods.tex`) |
| **Problem** | Vague forward pointers. |
| **Fix** | Name destinations by role where known, e.g. single-cell BDC chapter (`3 BDC_core…`), multi-type processes chapter, compartment-rupture chapter. Prefer stable wording the thesis can keep (titles may still move). |
| **Done when** | Every Ch. A forward reference identifies a destination by role/title, not only “later.” |

---

## C. Typos and micro-prose

### C1. Spacing / compounding in BDC prose

| | |
|---|---|
| **Where** | `sections/02_markov_chains.tex` — `m:sec:bdc` and nearby; spot-check holding file |
| **Problem** | Historical glitches (“suffer acatastrophe”, “State0”). |
| **Fix** | Search/fix missing spaces and broken compounds. |
| **Done when** | No glued words in BDC definition and following paragraphs. |

---

## D. Optional bridge in Chapter A

### D1. Compact application bridge at end of § coupled ODE–CTMC

| | |
|---|---|
| **Where** | `sections/02_markov_chains.tex` — end of coupled ODE–CTMC subsection (near `coupled_ode_ctmc` figure) |
| **Problem** | Full rupture schematic was removed; motivation may be thin. |
| **Fix** | **Only if** the rupture / BDC application chapter does not already carry this: at most **one short paragraph** — rupture ⇒ impulsive jump in shared medium; released amount = compartment count at a stopping time; named forward ref. |
| **Do not** | Re-input the full schematic + event-driven figure from the holding file into Chapter A. |
| **Done when** | One-paragraph bridge present **or** note that destination chapter already covers it. |

---

## E. Relocate / later-chapter integration (not polish-in-place in A)

Material should live in `notes/bdc_material_for_later_chapters.tex` and/or be merged into `3 BDC_core DRAFT U/` — **not** re-expanded in Chapter A methods.

### E1. Shared-medium rupture schematic + figure

| | |
|---|---|
| **Source** | Holding file block on rupture-into-shared-medium / impulsive release / event-driven figure |
| **Target** | Compartment-rupture application chapter (or BDC core if that is where it lives) |
| **Preserve** | Impulsive jump map (not pure vector field); load = state at stopping time; link to QS at random time if relevant |
| **Done when** | Not compiled from Ch. A; present or ticketed in destination |

### E2. Conditioning under two absorbing mechanisms

| | |
|---|---|
| **Source** | Holding file QSD / two-absorber block |
| **Target** | BDC results chapter |
| **Must correct** | Use absorption time `T_0 \wedge T_H` (or thesis notation for first of extinction and rupture), **not** bare hitting time of `0` when both mechanisms are active |
| **Done when** | Corrected block in destination; Ch. A does not re-derive it |

### E3. Killed subgenerator / survival-mass material

| | |
|---|---|
| **Source** | Holding file killed-generator block |
| **Target** | BDC chapter |
| **Note** | Holding file still may use catastrophe-to-`0` / `\kappa_i` convention; reconcile with Ch. A’s `H` / rate notation when integrating |
| **Done when** | Deferred; Ch. A only defines BDC as far as needed |

---

## F. Out of scope for this polish pass

Do **not** put back into Chapter A:

- Full killed-subgenerator treatment of BDC  
- Full shared-medium schematic and extra simulation figure  
- Full two-absorber quasi-stationary excursion  

Fix later chapters / holding-file integration first if an examiner would otherwise have nowhere to find that material.

---

## Build / verify

After edits:

1. From this folder: compile with the project’s usual latexmk/pdflatex flow on `main.tex`.  
2. Grep for leftover issues: bare exposure `E_n`, overloaded `\delta` uses you meant to split, `later chapter`, broad factorise sentence.  
3. Tick the checklist below in this file or in the agent report.

---

## Checklist

- [x] **A1** Exposure symbol confirmed / renamed if needed — kept `\mathcal{E}_n`; see note below  
- [x] **A2** `\delta` / rate / probability / hypergeometric disentangled  
- [x] **B1** Rate-diagram caption wording — one residual style call recorded below  
- [x] **B2** Structural contrast in caption (or explicit skip)  
- [x] **B3** Multi-founder factorisation narrowed  
- [x] **B4** Named forward chapter references  
- [x] **C1** BDC spacing typos — verified clean, nothing to fix  
- [x] **D1** Optional one-paragraph bridge, or confirmed covered later  
- [x] **E1–E3** Holding file / BDC-core handoff verified (no re-inflate of A) — annotated only  
- [x] Chapter compiles cleanly — `latexmk -pdf main.tex`, 38 pp., no errors, no undefined refs  

---

## Pass record (2026-08-10)

**A1 — decision: keep `\mathcal{E}_n`.** No bare `E_n` survives anywhere. Both
alternatives the spec offered are already taken in Chapter A: `S_n` is the
Galton--Watson survival probability (`m:eq:SnIter`, used throughout
`03_methods.tex`) and `A_n` collides with the amplitude `A(p)` / `\Ac`. Script
`\mathcal{E}` against blackboard `\mathbb{E}` is the least bad option available
and the remark already explains why `H` is unavailable.

**A2 — three-way split, `\delta` retained for the rate.**

| meaning | symbol | where |
|---|---|---|
| continuous per-capita catastrophe rate | `\delta` (unchanged) | `m:def:bdc`, `m:eq:bdcrates`, TikZ labels `$\delta$ / $2\delta$ / $3\delta$`, `m:fig:ratediagram` caption |
| discrete per-individual trigger probability in $(0,1)$ | **`\chi`** | `m:rem:notmeanfield` |
| hypergeometric ratio $\alpha/b_1=\alpha/(\lambda-\mu)$ | **`\omega`** | `app_b_absorption_models.tex` |

`\delta` was kept for the rate because the BDC core chapter
(`3 BDC_core DRAFT U/`) uses it 176 times in that sense; changing it would have
forced a rename campaign there. **`\kappa` was rejected** for the discrete
probability despite the spec's suggestion: the BDC core already uses `\kappa`
for the unrelated reference constant $1+\delta/2\lambda$, and the holding file
uses `\kappa_i` for catastrophe rates. `\omega` was chosen over `\beta` in
app. B because `\beta` sits next to the Pochhammer parameter `b` and the growth
rate `b_1` in the same lines. `\chi` and `\omega` are free in Chapter A, its
appendices, and the BDC core. `app_c_hypergeometric_identity.tex` names the
ratio only as `h/k`, so the identity chain is untouched.

**B1 — residual style call, deliberately not taken.** `\cref{m:def:bdc}` renders
lowercase, so the caption reads "…process of definition 1.3". The broken
noun-phrase construction B1 objected to ("versus birth--death--catastrophe
definition 1.3") is gone, but capitalising would mean adding
`\crefname{definition}{Definition}{Definitions}` — and, for consistency, the
same for theorem/proposition/lemma/remark. That is a thesis-wide rendering
decision, outside a light-touch caption pass, and the lowercase form is already
consistent across the chapter. Flagged rather than changed.

**B4 — routed through the existing `\fwd` macro** (`preamble.tex`), reusing the
key vocabulary already established in the holding file: `bdc`, `multitype`,
`rupture`. Four sites: `01_overview.tex` (1), `02_markov_chains.tex` (2),
`03_methods.tex` (1). No bare "later chapter" remains in compiled sources.

**D1 — bridge added** (one paragraph, end of `m:sec:coupled`, after
`m:fig:coupled`). The BDC core's `10_what_comes_next.tex` covers release, burst
size and the population embedding, but not the ODE-coupling framing, and the
compiled chapter otherwise leaves the coupled class motivated only by an
explicitly generic figure. No schematic or figure was restored from the holding
file.

**E1–E3 — holding file annotated only, nothing integrated.** Three `INTEGRATION
NOTE` comment blocks added: the `T_0 \wedge T_H` correction for E2 (with the
reason the old `T_0` was self-consistent under the catastrophe-to-`0`
convention), the `\kappa_i` → `\delta i` rename plus the warning that `\kappa`
is *not* free in the BDC core, and — newly spotted — that the rupture block
**inverts** `\delta` and `\rho` relative to Chapter A (`\delta` is medium
clearance there, `\rho` the catastrophe rate), an inversion `rupture_sawtooth.pdf`
was generated under.
