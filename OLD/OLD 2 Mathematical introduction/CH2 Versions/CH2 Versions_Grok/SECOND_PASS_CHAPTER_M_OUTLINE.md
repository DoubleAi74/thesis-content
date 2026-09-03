# Second pass — Chapter M redesign (target structure)

**Status:** target outline locked for planning; **execute only after** the first-pass merge (`IMPLEMENTATION_PLAN_TWO_CHAPTERS.md`) has produced:

- `merged/chapter_M_math_intro/` (full harvested content)
- `merged/chapter_A_constant_Ap/`
- `MERGE_LOG.md`

**Do not** implement this redesign during pass 1. Pass 1 should still harvest the full content inventory so pass 2 has material to rearrange, compress, or move.

**Voice (unchanged):** abstract mathematical.  
**Relation to Chapter A:** discrete amplitude / Koenigs theory remains Chapter A; this outline only *points* there.

---

## 1. Target structure (user specification)

# Mathematical Introduction

## 1. Overview

Provide an overview of the mathematical framework and methods used throughout the thesis.

## 2. Markov Chains

### 2.1 Discrete-Time Markov Chains

- Simple random walks  
- Galton–Watson processes  
  - Discussed in greater detail later  

### 2.2 Continuous-Time Markov Chains

- Poisson processes  
- Birth–death processes  
- Birth–death–catastrophe processes  

### 2.3 Time-Inhomogeneous Processes

- Logistic speciation model  

### 2.4 Coupled ODE–CTMC Systems

Introduce systems in which:

- The ODE dynamics depend on the state of a continuous-time Markov chain  
- The transition rates of the continuous-time Markov chain depend on the ODE variables  
- The dependence may operate in both directions  

## 3. Methods for Markov Chains

### 3.1 Discrete-Time Methods

Provide a brief introduction to discrete-time methods, while noting that these will be treated more fully in the following chapter through Koenigs-function methods.

### 3.2 Continuous-Time Methods

Introduce the principal methods for analysing continuous-time Markov chains, using birth–death processes as the main example:

- Backward equations  
- Mean population size  
- Variance and higher moments  
- Hitting probabilities  
- Extinction probabilities  
- Conditional means  
  - Include a brief indication of their role in the following chapter  

### 3.3 Method of Characteristics

- Present the method in an accessible, easy-to-follow form  
- Include a worked example  

---

## 2. How this differs from pass-1 Chapter M

Pass 1 (merge) still builds the **claude_1-shaped** chapter: prelims → full GW → QSD/conditioning → small populations → full MoC ladder → synthesis.

Pass 2 **re-architects** M into a **framework + methods** chapter:

| Pass-1 emphasis | Pass-2 emphasis |
|---|---|
| Deep binary GW + critical lifetime as main spine | GW only as DTMC example; detail later (A and/or later thesis chapters) |
| Light \(A(p)\), detailed \(A_{\mathrm{c}}\), small-pops narrative | Conditional means as a **method**, with pointer to Chapter A |
| Full absorption-model catalogue in MoC | MoC as **accessible method + worked example** (may keep more in app or compress) |
| Toolkit ordered by objects then applications | **§2 objects / process classes**, then **§3 methods** |

Pass 1 is still valuable: it assembles notation, proofs, figures, and wording to **mine** in pass 2.

---

## 3. Content map: target block → sources / status

Legend: **H** = harvest from existing drafts in pass 1 · **N** = largely new (not in current CH2 Versions drafts) · **C** = compress/reshape in pass 2 · **→A** = detail belongs in Chapter A

| Target | Status | Mine from (after pass 1) | Notes |
|---|---|---|---|
| **§1 Overview** | C/N | claude_1/2 intros; synthesis | Rewrite for framework/methods thesis map, not two-thread A(p) focus alone |
| **§2.1 Random walks** | **N** | (none substantial) | Needs new short subsection or external notes |
| **§2.1 Galton–Watson** | C / →A | M GW section; A setup | Keep definition + one-step structure; defer depth |
| **§2.2 Poisson** | **N** (thin if any) | planned/codex CTMC asides only | Usually 1–2 pages: counting process, exponential waits, link to CTMC |
| **§2.2 Birth–death** | H/C | prelims + small pops CT BD | Core example process class |
| **§2.2 BDC** | H/C | claude CT BDC def + codex killed-chain | Definition + rates + role; not full results catalogue |
| **§2.3 Time-inhomogeneous + logistic speciation** | **N** | (not in reviewed drafts) | User must supply notes/ref or accept placeholder + cite |
| **§2.4 Coupled ODE–CTMC** | **N** | (not in reviewed drafts) | Conceptual framework section; examples from thesis later chapters if available |
| **§3.1 Discrete-time methods** | C / →A | GW iteration, first-step, PGF iteration | **Brief**; hand off to Chapter A / Koenigs |
| **§3.2 Backward equations** | H/C | CTMC Kolmogorov; BD master/PGF PDE | |
| **§3.2 Mean** | H | linear BD mean ODE | |
| **§3.2 Variance / higher moments** | H | BD / GW second moment material (trim) | |
| **§3.2 Hitting probabilities** | H/partial | first-step; absorption sketches | May need modest expansion |
| **§3.2 Extinction probabilities** | H | GW + BD extinction | |
| **§3.2 Conditional means** | H/C / →A | QSD mean; \(A_{\mathrm{c}}\); light \(A(p)\) | Brief role of next chapter |
| **§3.3 Method of characteristics** | H/C | full MoC ladder | **Accessible + one worked example** as main text; park full abs-only / abs-death / ABD catalogue in appendix or compress |

---

## 4. Disposition of pass-1 M bulk under this outline

After pass 2, material currently in pass-1 M should land as follows:

| Pass-1 block | Pass-2 fate |
|---|---|
| Exponential clocks, CTMC generator | Under §2.2 + §3.2 setup |
| Full binary GW critical theory, phase portraits | **Compress hard** in §2.1; optional appendix; or leave detail only where later chapters need it — **not** a long § as now |
| QSD variance full derivation | Trim in §3.2 or appendix; Chapter A owns amplitude theory |
| Discrete BDC full calculation | Short in §2.2; long form → appendix or later modelling chapter |
| Full MoC three-model development | **One clean worked example** in §3.3; remaining models → appendix (recommended) or later chapter |
| Synthesis / outlook | Fold into §1 Overview and end-of-chapter pointer to A + later modelling |
| Hypergeometric / coefficient apps | Keep as Chapter M appendix supporting §3.3 |

Chapter A is **unchanged in role** by this outline: still the home of product/series/bounds/Koenigs/HT/PSLQ. Pass-2 M must not re-absorb that bulk.

---

## 5. Second-pass execution plan (when started)

### Phase S0 — Preconditions

- [ ] Pass 1 complete; both chapters compile  
- [ ] This outline still matches user intent  
- [ ] Answers recorded for open questions in §7 below  

### Phase S1 — Freeze pass-2 outline file

- [ ] Copy final section titles into `merged/chapter_M_math_intro/OUTLINE_PASS2.md`  
- [ ] List which pass-1 section files are donors for each new §  

### Phase S2 — Restructure (empty vessels, then pour)

1. Create new section files matching §1–§3 (and apps).  
2. For each target subsection, **move/adapt** prose from pass-1 M (and only if needed from original drafts).  
3. Write **new** subsections (random walk, Poisson, logistic speciation, coupled ODE–CTMC) only when content is available (user notes or agreed sources).  
4. Rewrite §1 Overview last (or first as a sketch, then finalize last).  

### Phase S3 — Compression rules

- §2.1 GW: ≤ definition, offspring PGF, mean recursion, pointer “detail later / Chapter A for amplitude methods.”  
- §3.1: first-step + functional iteration + generating functions in discrete time; **no** Koenigs development.  
- §3.2 Conditional means: \(A_{\mathrm{c}}\) sketch + definition of discrete \(A(p)\) + “Chapter A.”  
- §3.3: prefer absorption–death (or abs-only) as the single worked example; ABD full closed form may stay as “further example” or appendix.  

### Phase S4 — Consistency

- Notation freeze from pass 1 preserved  
- Cross-refs to Chapter A updated  
- Figures: keep only those that serve the new structure; move A-only figures out if any remain  
- Compile; update `MERGE_LOG.md` with a “Pass 2” section  

### Phase S5 — Stop conditions

Pass 2 stops when structure matches §1 of this document, new process classes are present at agreed depth, MoC is accessible + worked example, and Chapter A still owns deep \(A(p)\). **Not** a final literary rewrite.

---

## 6. Recommended depth defaults (unless user overrides)

| Block | Default depth for pass 2 |
|---|---|
| Simple random walk | 1–2 pages: definition, transition, optional gambler’s ruin / hitting as method teaser |
| Poisson process | 1–2 pages: axioms or holding-time construction; link to pure birth |
| Birth–death | 3–6 pages: rates, embedded jump chain pointer, PGF PDE template |
| BDC | 1–3 pages: rates, two absorbing mechanisms, generating-function form |
| Logistic speciation (time-inhomogeneous) | **TBD** — needs source material |
| Coupled ODE–CTMC | 2–4 pages conceptual + one schematic example |
| Discrete-time methods | 2–4 pages brief |
| Continuous-time methods | 6–12 pages (main technical weight of methods §) |
| MoC | 4–8 pages main text + appendix for extended models |

---

## 7. Open questions (resolve before executing pass 2)

1. **Where does “greater detail later” on GW live?** Chapter A only, a later modelling chapter, or an appendix to M?  
2. **Logistic speciation model:** do you have existing notes/LaTeX/refs to import, or should pass 2 leave a structured stub?  
3. **Coupled ODE–CTMC:** abstract framework only, or a concrete thesis model (which one)?  
4. **MoC worked example:** which model — absorption only, absorption–death, or absorption–birth–death?  
5. **Hitting probabilities:** general CTMC or only BD/absorption examples?  
6. **Should pass-1 full GW critical theory / full ABD closed form** go to M appendix, Chapter A, or a later chapter?  
7. **Chapter numbering in the thesis:** is this still “Chapter 2” with A as “Chapter 3”, or titles only for now?  

---

## 8. Interaction with pass-1 implementation plan

| Pass 1 instruction | Still valid? |
|---|---|
| Harvest full claude_1 spine into M | **Yes** — raw material for pass 2 |
| Do not put deep \(A(p)\) in M | **Yes** — reinforced by §3.1/3.2 pointers |
| \(A_{\mathrm{c}}\) detail + forward ref to A | **Yes** — fits §3.2 conditional means |
| Two standalone projects under `merged/` | **Yes** |
| Prose only, no scripts | **Yes** |
| Prelims redesign in pass 1 | **No** — deferred; this document is the redesign |

**Agent rule:** If implementing pass 1, ignore this file’s target section order except to avoid deleting content that pass 2 will need (especially MoC ladder, BD, BDC, conditional means, clocks/CTMC/PGF).

---

## 9. One-page brief for a future agent

```
AFTER pass-1 merge only:
1. Read SECOND_PASS_CHAPTER_M_OUTLINE.md and user answers to §7.
2. Restructure merged/chapter_M_math_intro to:
   §1 Overview
   §2 Markov chains (DTMC incl. RW + GW brief; CTMC Poisson/BD/BDC;
      time-inhomogeneous logistic speciation; coupled ODE–CTMC)
   §3 Methods (brief discrete → Chapter A/Koenigs; CT methods via BD;
      MoC accessible + worked example)
3. Compress pass-1 GW/QSD/small-pops/MoC bulk; do not move Chapter A theory into M.
4. Write truly new blocks only with supplied sources or agreed stubs.
5. Compile; append Pass 2 notes to MERGE_LOG.md.
```
