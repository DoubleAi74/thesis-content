# Chapter 9 — Phase A report

**Chapter:** *Models with non-constant rates* (was *Variability in evolution*).
**Tree:** `Chapter numbers/CH9_REWRITE/`. **Built:** `latexmk -pdf main.tex`, 34 pp, A4, zero overfull boxes, zero multiply-defined labels, zero undefined citations. 47 undefined references, all in the `m:`, `bdc:`, `dist:`, `p:` and `path:` namespaces, as expected in a standalone compile.

**Sources verified byte-identical after the run:** `Chapter numbers/CH9/` and `Chapter numbers/CH10/`, 83 files, `md5` before/after diff empty.

Phase B reads this file and the tree, and nothing else.

---

## 1. Final section structure

| § | Title | pp | Tier |
|---|---|---|---|
| — | titlepage, contents | 1–2 | — |
| 1 | Introduction | 3–5 | — |
| 2 | Logistic speciation | 6–11 | full |
| 3 | Competitive reversal: the Pimentel model | 12–15 | full |
| 4 | Coupling speciation to competition | 16–17 | specified |
| 5 | Rise, run, ruin, rejuvenation | 18–19 | simulated |
| 6 | The birth–plague model (6.2 the vitality variant) | 20–21 | simulated |
| 7 | Public good accumulation | 22–23 | specified |
| 8 | The two phases of infection | 24–27 | full |
| 9 | Discussion | 28–29 | — |
| A | Model summary | 30 | — |
| B | Figure and simulation record | 31–33 | — |
| — | bibliography | 34 | — |

Body 27 pp, appendices 4 pp. Against the plan's §3.2 allocation the introduction came in under (3 against 3.0), §2 over (6 against 5.0), §3 under (4 against 5.0) and §8 under (4 against 5.0). §9 is 2 pp against 1.5 because the open-problem table is a full-page float.

**24 figures**: 22 raster inclusions and 2 TikZ schematics. **45 numbered equations carrying `var:` labels**, 1 proposition, 1 corollary, 7 open-question remarks, 1 scope remark, 6 tables.

---

## 2. Passages carried over near-verbatim — Phase B must leave these alone

Three passages are the source's own writing, kept because they are better than anything a rewrite would put there. They have been de-first-personed and spell-corrected and nothing else.

| Passage | Source | Now at |
|---|---|---|
| The Pimentel experiment narrative — the compartmented enclosure, the delay exceeding a fly's lifespan, the war won over generations, the blowfly reversal | `09/05:5–17` | §3.1, four paragraphs |
| The Mann–Budd block quotation on the push of the past | `09/02:9–23` | §2.2, the chapter's one block quotation |
| The epistemic hedge on the public-good speculation — *"this is purely my speculation, and may not at all be the case, but even if it isn't, the dynamics may be interesting in and of themselves"* | `10/04:4` | §7.1, second paragraph, reworded out of the first person and **not** out of its honesty |

Two smaller ones, also near-verbatim: the four-clause Pimentel step rule (`09/05:37–46`, now a `description` list in §3.2) and the four-variant list (`10/02:71–78`, now a `description` list in §8.5).

The Mann–Budd quotation had PDF line-break hyphens (`accumu-late`) which were closed up. That is the only change inside a quotation anywhere in the chapter.

---

## 3. `NEEDS-REF` markers — three

All three are the citation gaps named in plan §8.4. None is filled and no entry was composed.

| Where | The sentence it supports |
|---|---|
| §2.1, after the motivation | Punctuated equilibria as a named theory (Eldredge & Gould 1972). No donor bibliography holds the 1972 paper. `gould1989wonderful` is in `references.bib` and is about the Cambrian, not that paper. **The claim is not made in the body at all** for want of the reference. |
| §2.3, inside `var:rem:scope` | "…better read as setting the initial condition for a density-dependent diversification model than as driving the rate." No donor bibliography holds a key for the DDD literature. |
| §5.1, after the motivation | The periodic shedding of turbulence in the wake of a cylinder, which `09/06:12,69` states as established fact. **The claim has been reduced to a bare analogy asserting nothing about a specific flow**, rather than carried with an invented citation. |

---

## 4. `NEEDS-AUTHOR` and `NEEDS-BIOLOGY` markers

### 4.1 `NEEDS-AUTHOR` — three modelling decisions the author must ratify

These are the blocking items. Each is a place where the source specifies a model incompletely and Phase A had to choose in order to write anything.

**(a) The vitality coupling — §6.2, `06_birth_plague.tex`.** `09/09:11` introduces `dV/dt = ξ − pX_t` and then uses `V` in **none** of the transition rates, so the model as printed is §6.1 plus a decorative equation. Written here as corruption at rate **δX_t/V(t)**, by consistency with the catastrophe channel of §5, which is the model the variant says it is borrowing from. The contact term `χY_t` is left uncoupled, since contact infection is not a scarcity mechanism.
*Alternatives named in the marker:* `δX_t²/V(t)`, if "per-capita scarcity" means scarcity per agency times the number exposed; or dividing the whole loss channel including contact by `V`. Nothing else in the chapter depends on the answer.

**(b) The two constants of the decaying death rate — §8.1, `08_two_phase.tex`.** `10/02:14` prints `μ(t) = a + a e^{−t}`, with the same letter for both constants — which forces the initial death rate to be exactly twice the asymptotic one for no stated reason, **and collides with `a`, CH4's larger root, used in that sense forty lines later in the same section.** Written here as `μ₂(t) = μ_∞ + μ₀e^{−t}`, two independent constants. The marker also raises a second question the source leaves silent: the bare `e^{−t}` fixes the decay timescale at 1, which should either be declared a choice of time unit or written `e^{−t/T}`.

**(c) The R → f notation shift — §4, `04_pimentel_plus.tex`.** `09/05:290` replaces `R_a, R_b` by `f_a, f_b` and asserts the dynamics are "at least qualitatively identical", without saying whether the two are the same quantity. Written here as **the same evolving quantity under a second name**, on the grounds that the update rule and its exponent are identical; the increment coefficient is therefore `ε` in both sections rather than `μ` in §3 and `δ` in §4.
*Alternative named in the marker:* they are different objects — resistance is the argument of a blocking probability, fitness is a Moran selection coefficient — in which case §3's and §4's kernels are not one model in two notations and the relation between them needs stating.

### 4.2 `NEEDS-BIOLOGY` — four

| Where | Claim wanted | Candidate keys, already in `references.bib` |
|---|---|---|
| §2.1 | Whether high early diversification following the opening of ecological space is established in the palaeontological record beyond the individual cases usually cited, and at what taxonomic level. **The Burgess Shale arthropod class count of `09/01:33` is not carried into the chapter at all** — it is stated as fact with no citation and no donor key exists. `gould1989wonderful` is explicitly *not* offered as its source. | — |
| §7.1 | Whether \yp\ resistance to macrophage toxic products could be mediated by an exported substance acting on neighbours as well as the producer — i.e. whether the public-good framing has experimental support for this organism | `PujolBliska2003`, `PujolBliska2005`, `ConnorEtAl2018` |
| §8.1 | That \yp\ adapts to host-specific bacteriophages within the handful of replication cycles one infection lasts. **The least supported claim in the chapter**, and the one the subductive variant exists to represent | `PujolBliska2005`, `ConnorEtAl2018`, `MonackEtAl1997` |
| §8.1 | That the switch from intracellular to extracellular replication is *driven by* the neutrophil response rather than merely coincident with it, and what the histology shows about the timing | `BosioEtAl2005`, `PetersEtAl2013`, `MonackEtAl1997` |

All candidate keys are offered as a starting point for the search and explicitly **not** as identifications.

---

## 5. Figure backlog

### 5.1 Eleven inclusions below 170 dpi — cannot be repaired by resizing
Every line plot except the four birth–plague realisations falls between **130 and 162 dpi** at its printed width: `LSMean` (162), the four Pimentel plots (130–137), the three VBC plots (132), and the three two-phase plots (135–136). The images are ~380 × 250 px screen captures. Widths were already reduced once during the page-budget pass, which bought roughly 15 dpi each; going further makes them illegible. **They are legible and they are not of thesis quality.** Full dpi table at `var:tab:figrecord`.

### 5.2 The three "rough" plots
`rough.png`, `rough2.png`, `rough3.png` carry §8's headline result and have **no axis labels, no units and no legend** (confirmed by rendering the compiled pages). They are the first three that should be redrawn — and now the cheapest, because `var:eq:EZ` gives the curve of `var:fig:rough1` in closed form and needs no simulation at all. See §7.3 of this report: the closed form was checked against the plotted curve and reproduces it.

### 5.3 The whiteboard photograph
`board.jpeg` (§7) is a photograph of a whiteboard. A drawn schematic — macrophage boundary, enclosed volume, count `X_t`, accumulating good `P(t)` — would carry the same content in house style. **Suggested, not attempted**, per the plan.

### 5.4 The cellular automaton: 11 panels → 6
Kept: **`pim1, pim3, pim6, pim8, pim11`** and **`pim9`**, in that chronological order. Dropped: `pim2, pim4, pim5, pim7, pim10`. Chosen by inspecting all eleven frames against the four stages the plan names: `pim1` initial advance, `pim3` the squeeze with blue confined to one corner, `pim6` the pale hardening fringe, `pim8` the crossing, `pim9` blue past halfway, `pim11` blue everywhere.

**One thing the source does not explain:** the first frame carries a large **green** region, and a purple one, neither of which appears in later frames; the source caption says only "blue and red squares represent houseflies and blowflies". The caption of `var:fig:automaton` records this as unexplained rather than inventing a reading for it.

### 5.5 Twenty files copied but not included
Five dropped automaton panels; three parked with the Bardo Thodol (`samsara.jpg`, `proverbe.jpg`, `lightning.jpg`); and **twelve** never used in either source: `proverb.jpg`, `proverbs.jpg`, `lightn.jpg`, `pow50N100mu10.png`, `pow3N10e5mu1.png`, `Finish_times.png`, `threshold1.png`, `auto1–3.png`, `Capture.PNG`, `Screenshot_2024-11-05_at_18.35.54.png`. All are kept in `figures/`.

**Plan §6.1 says thirteen never-used files; the count is twelve.** The plan's list itself enumerates twelve. Recorded rather than reconciled.

### 5.6 A notation mismatch inside two figures — flagged in their captions
The VBC plots' legends label the potential **`N(t)`**, which is what it was called when they were produced; §5 calls it `V(t)` after the rename of §9.1. The captions of `var:fig:vbc-two` and `var:fig:vbc-many` now say so explicitly, in the manner of `m:fig:lsmean`'s caveat. No other included figure carries an in-image symbol: the Pimentel plots, the bpPLOT panels and the three rough plots have no legends or axis labels at all.

---

## 6. Bibliography record

24 entries, **every one a verbatim byte-for-byte copy**. Five were spot-checked against their donors by exact string comparison and are identical: `Yule1925`, `PetersEtAl2013`, `asker2023coexistence`, `pimentel1965selection`, `prigogine2018order`.

| Donor | Keys |
|---|---|
| `CH9/document MAIN/references.bib` | `bak1991self`, `budd2018history`, `elitzur1994let`, `fisher1929genetical`, `gompertz1825xxiv`, `hutchingson2018ecological`, `nietzsche2013beyond`, `pease1984evolutionary`, `pimentel1965selection`, `poe2020masque`, `sharma2023assembly` |
| `CH10/document MAIN/references.bib` | `asker2023coexistence` |
| `CH2/references.bib` | `Yule1925`, `Nee1994` |
| `CH1/document MAIN/references.bib` | `prigogine2018order`, `gould1989wonderful`, `brockwell1985extinction`, `cairns2004extinction` |
| `CH8_REWRITE/references.bib` | `BosioEtAl2005`, `PujolBliska2003`, `PujolBliska2005`, `ConnorEtAl2018`, `MonackEtAl1997`, `PetersEtAl2013` |

**Duplicate-key resolutions (plan §7.4).** `Yule1925` (CH2) chosen over `yule1925ii` (CH1); `Nee1994` (CH2) over `nee1994extinction` (CH1). CH2 is the house standard, and its entries carry DOIs where CH1's do not. *Note for whoever merges the thesis bibliography:* CH1's `nee1994extinction` is **"Extinction rates can be estimated from molecular phylogenies"** while CH2's `Nee1994` is **"The reconstructed evolutionary process"** — these are two different 1994 papers by overlapping author sets, **not one work under two keys**. The plan treated them as duplicates; they are not, and merging them would lose a reference. This chapter cites `Nee1994`, *"The reconstructed evolutionary process"*, as the source of the push-of-the-past account. **Which of the two Budd and Mann's "Nee et al. (1994a)" points at has not been checked** — that would need their reference list, which is not in the tree. If it is the other paper, the citation in §2.2 should become `nee1994extinction`, copied verbatim from `CH1`.
   By contrast `Yule1925` and `yule1925ii` **are** the same work (Phil. Trans. B **213**, 21–87, 1925) under two keys, and that resolution stands.

`poe2020masque` is retained although it is cited nowhere in the chapter, so that `_parked/plague_in_popular_culture.tex` remains compilable if restored.

Two entries were **not** copied although the plan permitted them: `schrodinger1946life`, `monod1974chance`, `darwin1859origin` were offered "only if §2's motivation needs them — do not pad". It did not.

---

## 7. Source integrity, verification, and the C7 finding

### 7.1 Source integrity
`find "Chapter numbers/CH9" "Chapter numbers/CH10" -type f -exec md5 {} \;` sorted, before and after: **identical, 83 files.** Neither source chapter was opened for writing at any point. CH10 retains its own copies of both migrated sections; removing them is the author's job.

### 7.2 The numerical check of A1 and A2 — passed
Run in `numpy` 2.4.2, no other numerical library (`scipy` is not installed). Script retained at `/private/tmp/.../scratchpad/verify_A1_A2.py`.

**A1** was checked at two rate laws — the chapter's logistic law and an unrelated oscillatory law `β(t)=½(1+sin 3t)e^{−t/4}`, chosen to confirm the result uses only the integral — by two independent simulation routes: an integrated-hazard time change, and Ogata thinning in real time, which never forms the integral at all. At 200,000 paths per case:

| Case | mean rel. err | var rel. err | total variation from geometric(e^{−B}) |
|---|---|---|---|
| logistic, t=6, time change | 1.3 × 10⁻⁴ | 7.6 × 10⁻³ | 3.4 × 10⁻³ |
| logistic, t=6, thinning | 2.1 × 10⁻³ | 6.1 × 10⁻³ | 4.0 × 10⁻³ |
| oscillatory, t=5, time change | 3.1 × 10⁻³ | 3.2 × 10⁻³ | 4.2 × 10⁻³ |
| oscillatory, t=5, thinning | 3.3 × 10⁻³ | 2.5 × 10⁻³ | 4.0 × 10⁻³ |

All within Monte-Carlo error at that sample size (≈7 × 10⁻³ expected TV over ~40 support points).

**A2** was checked at three parameter sets. `B(t)` computed by Simpson quadrature agrees with the chapter's closed form to ≤ 1.6 × 10⁻¹⁴ at every `t`, and `B(40)` agrees with `(σK/ϱ)ln(K/N₀)` to ≤ 2.3 × 10⁻¹¹. The simulated law at `t=40` matches geometric(e^{−B(∞)}) to TV 4.2 × 10⁻³.

**A3** was checked: `∫₀^∞ σN′ = σ(K−N₀)` to ≤ 1.1 × 10⁻¹⁶ at two parameter sets.

### 7.3 C7 and A4 — the open question is **settled**, not marked
The plan left one thing open: whether `dist:eq:burstlaw` is conditioned on rupture, which decides whether `b` is free or determined. **CH5 settles it.** `CH5_REWRITE/sections/06_burst_size.tex:41–46` states the law as `dist:thm:burst` with the words *"Unconditionally, including the mass b of realisations that never burst"*, gives the conditional form separately as `dist:eq:burstlawcond`, and checks the normalisation `Σ_{k≥1}(δ/λ)a^{−k} = 1−b`.

So **`b` is determined, not free**: `b = 1 − (δ₁/λ₁)/(a−1)`, and it is also the smaller root of `bdc:lem:roots`. Confirmed numerically at three parameter sets to ≤ 7.8 × 10⁻¹⁶. This is written into §8.4 as `var:eq:bdetermined`, with the consequence stated: of `a`, `b` and `δ₁/λ₁`, only two may be chosen independently. **No `NEEDS-AUTHOR` marker was needed here.**

**A4 reproduces the source's own figures.** With `(λ₁,μ₁)=(1,0.2)`, `(λ₂,μ₂)=(1,0.9)` — the parameters printed on `rough.png` — the closed form `E(Z)=2(1−b−(δ₁/λ₁)μ₂/(aλ₂−μ₂))` gives 1.600 as `δ₁→0`, 0.614 at `δ₁=0.2`, and crosses 1 at `δ₁≈0.060`. The plotted curve reads 1.6 at the left, ≈0.61 at the right, and crosses the red unit line at ≈0.06. The mean burst size at `δ₁=0.2` is 4.35 against ≈4–5 read off the log axis of `rough2.png`. **This is an independent confirmation both of A4 and of the C7 reading that `a` and `b` are CH4's roots used correctly** — the source's numerics were produced from the same quantities.

### 7.4 What could not be executed
Nothing in the plan was skipped. Two things it asked for were found not to be needed: the C7 `NEEDS-AUTHOR` marker (§7.3 above), and any figure regeneration (none is permitted and none was attempted).

---

## 8. Changes needed in *other* chapters — listed, **not made**

Three, exactly as plan §10 item 7 anticipated, plus one found during the run.

1. **`CH6_REWRITE/preamble.tex:81` and `CH8_REWRITE/preamble.tex:90`.** Both define
   `\newcommand{\ChEvo}{the chapter on variability in evolution}`.
   That describes a chapter that no longer exists. Replacement: `{the chapter on models with non-constant rates}`. Both files verified to contain the string; **neither was edited.**

2. **`CH8_REWRITE/sections/06_discussion.tex:112–120`** (`path:sec:forward`). The paragraph hands the selection-gradient obligation to `\ChEvo{}` — which §2–§4 of this chapter now discharge — and then hands the \yp\ account to `\fwd{conclusion}{the concluding chapter}`. **The two-phase model that account leans on now lives in §8 of this chapter**, so that second sentence should point at both. It is also the natural place to name open problem 16 of `var:tab:openproblems`, which asks how `E(Z)` compares against `ϑ*`.

3. **`CH1/document MAIN/sections/09_how_the_content_is_divided_amongst_the_chapters.tex`** — the largest of the three. The CH9 summary describes a chapter that will no longer exist, and the CH10 summary describes two models that will have left it. Also **`sections/08_research_questions.tex`**, where research question 1 (biphasic pathogenesis) points at the conclusion; the two-phase treatment is now §8 here.

4. **Found during this run, not in the plan.** `CH2/sections/02_markov_chains.tex:700–789` (`m:sec:logisticspeciation`) already carries the logistic speciation model — the same ODE, the same `β(t)=σ(C−N(t))`, the same integrated rate, the same limiting mean — and it includes **the same image file `LSMean.png`** as `m:fig:lsmean`. Two consequences for the author to decide, neither actionable from here:
   - **CH2 writes the carrying capacity `C` and this chapter writes `K`**, and CH2 writes the logistic growth rate `r` where §7.2 of the plan requires `ϱ` (because `r` is the burst size thesis-wide). CH2's `r` is a pre-existing thesis-wide collision. Whichever way it is settled, the two sections must agree.
   - **The same figure appears in two chapters.** §2 cross-references `m:fig:lsmean` explicitly and repeats CH2's caveat that the figure shows the birth–death variant and not the pure-birth model, so the duplication is at least declared. Whether to keep it in both places is the author's call.

---

## 9. Pass record

Style and level of detail follow `CH2/polish_notes.md`.

### 9.1 The symbol renames — eight from plan §7.2, and six more it did not foresee

The eight the plan mandates were all made as specified:

| Was | Became | Where |
|---|---|---|
| `Y_t` species count | `S_t` | §2 |
| `r` logistic growth rate | `ϱ` | §2 |
| `ξ` potential inflow | `φ` | §5, §6.2 |
| `μ` evolution rate | `ε` | §3 |
| `γ(t)` birth rate | `λ(t)=λ₀+αP(t)` | §7 |
| `β, ν` phase-2 rates | `λ₂, μ₂` | §8 |
| `λ, μ, δ` phase-1 rates | `λ₁, μ₁, δ₁` | §8 |
| `a, b` | resolved under C7 — they **are** `bdc:`'s roots, used correctly, and are now declared as such | §8 |

Six more were forced by §7.1's own rule ("may never contradict a thesis-wide symbol", "may never serve two meanings within one section"), which the plan's list did not reach. Each is recorded here with the collision that caused it.

| # | Was | Became | Why |
|---|---|---|---|
| R9 | `λ`, the speciation exponent in `β_a=(A_t/N)^λ f_a` (`09/05:304`) | **`ζ`** | `λ` is the birth rate thesis-wide, and §4 uses `μ_a` as a death rate three lines away. `ζ` is free of any rate meaning in CH2–CH8 (it occurs only as a local function `ζ(τ)` in CH2 app. B and CH6). |
| R10 | `δ`, the fitness increment in `f_a + δ(B_t/A_t)^α` (`09/05:285`) | **`ε`** | `δ` is the catastrophe rate thesis-wide. This quantity is §3's evolution rate under a second letter, so the rename also discharges the plan's instruction to "reconcile to one symbol or state clearly why two are used" — see `NEEDS-AUTHOR` (c). |
| R11 | `N(t)`, the potential of §5 (`09/06:19`) | **`V(t)`** | Three meanings of `N` inside one chapter: abundance in §2, integer capacity in §3, potential in §5. §6.2 already calls the same object `V`, and **the plan's own §1(c) model table names it `V`.** |
| R12 | `μ`, the consumption coefficient in `dN/dt = ξ − μX_t` | **`c`** | `μ` is the death rate thesis-wide. `c` matches §7's clearance term, a cognate quantity; the notation table separates them. |
| R13 | `α`, the Poisson revival rate of §5 | **`ω`** | The plan sanctions exactly two meanings for `α` (Pimentel exponent §3–§4, public-good coefficient §7). Adding a third and a fourth in the middle of the chapter defeats the table. `ω` occurs elsewhere only as a bound hypergeometric parameter (CH2 app. B) and a seasonal angular frequency (`m:eq:lvkernel`). |
| R14 | `α`, the contact-infection coefficient of §6 (`09/08:8`) | **`χ`** | Same reason. `χ` occurs elsewhere only in `m:rem:notmeanfield`, as a discrete trigger probability, six times in one remark. |

Two further renames are *not* departures, because the plan's §7.2 closing sentence mandates them directly ("β is retained for the speciation rate and nothing else; λ, μ, δ are birth, death and catastrophe as in CH4–CH8"): §6's birth rate `β → λ`, and §7's base birth rate `β → λ₀`.

**One symbol was dropped rather than renamed.** The source's `Ψ(t)` (`09/04:153`) is `e^{B(t)}` and nothing else, and `Ψ` is taken in CH2 (`m:eq:Psidef`, `m:eq:Psihyp`). Writing `e^{𝓑(t)}` throughout removes the collision and shortens the derivation by several lines. No content is lost.

**And one departure from the plan's own notation.** The plan writes the integrated rate `B(t)`. This tree writes **`𝓑(t)`** (`\Bint`), for two reasons: plain `B(t)` is Kendall's extinction integral in `m:eq:inhomextforward`, and `B_t` is the second Pimentel population count in the very next section. **`𝓑(t)` is CH2's own symbol for exactly this object** (`m:eq:lambdaint`), so the change moves the chapter *towards* the house standard rather than away from it.

### 9.2 An eighth correction, of the C4 class, not in the plan's list
`09/05:276,278` prints both Pimentel+ step probabilities with the identical left-hand side `Pr(ΔA_t = 1)`. This is the same defect as C4 and produces a contradiction as printed. The second is written `Pr(ΔA_t = −1)`, by symmetry with the up/down structure of `var:eq:kernel`. Recorded here rather than silently absorbed, because the plan's constraint list says to flag rather than fix anything beyond the seven corrections — and a display asserting two different values for one probability is not something that can be carried across.

Separately, `10/02:63` prints `E(Z) = 2(1 − b + Σ)` where `p₀ = b + Σ`; the sign of the sum is wrong there. A4's `var:eq:EZ` carries the correct one and supersedes the line, so no marker was needed.

### 9.3 Departures in the text

- **§2 opens by conceding CH2's priority.** The plan presents A2 as answering a question the chapter never answers. It does, *distributionally* — but `m:eq:logspecmean` already records the mean and its limit, including the `(C/N₀)^{σC/r}` form. §1 and §2 both say plainly that the model and its mean are CH2's and that what this chapter adds is the distribution: the geometric law at every fixed time, the variance, the proper limit law, and the closure of two of the five alternative rate laws. Claiming the limiting mean as new would have been false.
- **The LSMean caption was rewritten against CH2, not against CH9.** The CH9 source captions it "Realisations of the logistic speciation model"; `m:fig:lsmean` says it is *not* that model but the birth–death variant with origination `σN′(t)` and constant extinction. CH2 is right — the figure's lower panel shows two crossing rate curves and its upper panel turns over, which the pure-birth model cannot do. The caption here follows CH2 and cross-references it.
- **§3.4's statement of which way the critical point moves was corrected during proofing.** The first draft said `i_c` is "dragged behind the population that is ahead… towards whichever population is losing". That is backwards. From `var:eq:kernel`, `q_a > q_b` exactly when `i > i_c`, so `i_c` is an **unstable** point; and if `a` is the majority then `b` accumulates resistance, `p_b > 0`, and `i_c = N/(2−p_b)` climbs *towards `N`*, i.e. after the leader. The reversal is `i_c` overtaking the trajectory. This was caught by rendering `var:fig:pim-critical`, where the red curve visibly saturates at whichever boundary the blue trajectory is heading for. Both the body sentence and the caption now say so, and the instability is stated because it is what makes open question 6 (a diffusion limit with a moving unstable equilibrium) coherent.
- **Transition probabilities are written conditionally.** The source writes `Pr(S_{t+Δt} − S_t = 1) = β(t)S_tΔt`, mixing an unconditional probability with a random right-hand side. Everywhere in this chapter such lines are conditioned explicitly (`| S_t = n`, `| X_t, Y_t`). A precision repair, not a change of claim.
- **`10/01:3`'s dangling "(see appendix B)"** was not carried across; nothing was imported from `10/01`.
- **Appendix A is portrait, not landscape.** The plan asks for "one landscape table". A `sidewaystable` is a full-page float and left the appendix heading stranded on a page of its own, costing a page against a budget with none to spare. The same six columns are set portrait at `\scriptsize` and fit on the heading page. **No content was cut** — the plan's instruction not to trim Appendix A is respected.
- **Open questions are one titled `remark` per section containing a short `enumerate`**, used seven times in §2–§8, with the gathered table `var:tab:openproblems` in §9. That is the single consistent form the plan asked for.

### 9.4 The page budget, reconciled
The plan projected ≈33.5 pp against a cap of 34 and called it tight. The first clean build came in at **36**. Getting to 34 took four passes, in the order the plan prescribes (§11: automaton panels first, §3's results prose second) plus two structural fixes it did not anticipate:

| Change | Δ pp |
|---|---|
| §1 notation table to `\footnotesize`, rows merged where the merge lost nothing | −0.4 |
| §1 roadmap and two §2 paragraphs compressed | −0.6 |
| All 22 raster figures reduced ~10 % (which also raised every dpi figure by ~15) | −0.3 |
| §3: automaton panels 0.29→0.225 width, two long captions tightened, one paragraph compressed | −0.4 |
| Appendix A landscape → portrait, recovering a stranded heading page | −1.0 |
| Appendix B table float relaxed to `[!tbp]`, recovering a second stranded heading page | −1.0 |
| §3 critical-point correction and §5 caption notes added back | +0.7 |

**Nothing in §5.2's additions, the open questions or Appendix A was trimmed.** The automaton stayed at six panels rather than dropping to four: the two float-placement fixes made the reduction unnecessary, and six panels carry the reversal that four do not.

### 9.5 Smaller calls
- **Figure file names were flattened with spaces replaced by underscores** (`pow3N10e4mu1 critical.png` → `pow3N10e4mu1_critical.png`). Both names are recorded in `var:tab:figrecord`.
- **`N = 10e5` and `N = 10e4`**, as printed in the source captions, are typeset `10 × 10⁵` and `10 × 10⁴` — the literal reading of the string. If the author meant `10⁵` and `10⁴`, the captions and `var:tab:figrecord` both need changing.
- **§7's framing follows the cited paper, not the source's description of it.** `10/04:3` says "antimicrobial resistance" and then "Cancerous cells"; `asker2023coexistence` is about competing *microbial* strains. §7.1 describes it as microbial.
- **The `\ChPathcap` macro is new**, formed from CH6's `\ChPath` by the capitalisation pattern the other `\Ch*cap` macros use. Every other `\Ch*` macro is a byte-for-byte copy.
- **`rotating` was added to the preamble and then removed** when Appendix A went portrait. The preamble carries no unused package.
- **`\Lw`, a length introduced to size the landscape table, was removed with it.**
- **The `remark` environment is shared** between the scope remark and the seven open-question blocks, so they are numbered in one sequence with the proposition and corollary. That is CH2's and CH8's convention.

---

## Note for Phase B

Where the work is, in order:

1. **§1.** Written plainly and new. It is the first thing an examiner reads and the axis lives or dies there — specifically in the two opening paragraphs, `var:tab:models`, the bridging paragraph at the head of §8, and §9.1. If any of those four is thin, the restructure has not landed.
2. **The 24 captions.** They are interpretive but not yet readable. `var:fig:automaton`, `var:fig:pim-runs` and `var:fig:bpplots` are the longest and the roughest.
3. **§4, §5 and §7** — the short specified-only sections. They must be brief without being curt and must state incompleteness without apologising. §4 is the hardest: it is one page carrying a hypothesis, a model and a `NEEDS-AUTHOR` marker.
4. **The seams.** Eight sections that were eight separate notebooks. §2→§3, §5→§6 and §7→§8 are the three transitions currently doing least work.

**Frozen:** every equation, `\label`, `\cite`, `\includegraphics`, `NEEDS-` marker, the fourteen renamed symbols of §9.1, and the three near-verbatim passages of item 2. **The page budget has no slack** — the chapter is at 34 against a cap of 34, so any addition must be paid for by a subtraction.
