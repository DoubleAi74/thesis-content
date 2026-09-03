# Chapter 4 — Full Chapter Plan
**Working title:** *The birth–death–catastrophe process: further results, and a burst-aware model of viral replication*
(standalone draft title currently: "Birth death catastrophe — further results and potential use")

Prepared 2026-08-07 from a full reading of every item in `4 BDC additional and BMVR/`.

---

## 0. Authority of sources

The folder contains four generations of the same material. Where they disagree, use the newest:

| Priority | Source | Role |
|---|---|---|
| 1 (authoritative) | `new_notes3/Comprehensive_Corrected_Notes.tex` | Corrected master notes; all errata applied; verified numerically |
| 2 | `new_notes2/Core_Publishable_Work_Summary.tex` | Clean statements; overlays, HIV contrast, Cases 1–5, reset, partial release, Hawkes models. (Its MOI kernel `g_k` lacks the I-powers — superseded.) |
| 3 | `new_notes/BMVR_extension_notes.tex` | Consolidation + renewal BMVR + full tagged errata catalogue (Part IV) + open tasks (Part III) |
| 4 (historical) | `document MAIN/sections/*.tex` | Current chapter draft: PGF derivations good; §6–§9 incomplete or wrong as written |

Other assets:

| Item | Content |
|---|---|
| `N=2 Immediate Transfer content/N_eq_2.tex` | Chained immediate-transfer model (μ=0 rupture-size laws; first/second rupture-time distributions; PGF coefficient extraction) |
| `figures/` | `kernels.pdf`, `overlay_I.pdf`, `overlay_V.pdf`, `overlay_rel_diff.pdf`, `overlay_growth_phase.pdf`, `overlay_V_with_naive.pdf`, generator `plot_bmvr_comparison.py` |
| `document MAIN/figures/IMG_ch5/QSmean/` | Simulation plots QS1/QS2 (μ=0, μ>0 QS means), QSmeanNE0, QSMu0 |
| `new_notes3/verify_result_20_1.py` (+report, metrics, `verify_figures/`) | Numerical verification of the renewal system: **53/53 PASS**; figures D (exponential reduction), E (growth-rate match), F (R₀ threshold), H (Gillespie cohort) |
| `paper.pdf` | Hataye et al. 2019, *Cell Host & Microbe* 26:748–763 — the HIV-establishment reference for the contrast section |
| `3 BDC core/` | Stale duplicate of Chapter 3, kept here for continuity checks (errata 4.17 says delete/archive it) |
| `Chapter4_BDC_further_results.pdf` | Compiled snapshot of the current draft |

---

## 1. What the chapter is

**Position.** Chapter 3 defines the BDC process and derives I, J, K, V. Chapter 4 does two things:

1. **Completes the single-cell theory** — full transient distribution (PGF route), quasi-stationary distribution, burst-time and burst-size laws, and the headline identity *burst-size distribution = QSD*.
2. **Scales the theory up** — embeds the closed-form single-cell kernels into a renewal (age-structured) version of the Basic Model of Viral Replication, replacing the phenomenological constant release rate *p*, and extracts the consequences (effective parameters, R₀ invariance, identifiability, flooding advantage, growth-rate trade-off).

**One-page story** (from master notes §J.4, to be expanded into the introduction):
> Within-host models treat infected cells as black boxes releasing at constant rate p. Lytic pathogens grow inside a cell and dump their load in one burst. Model one cell as a classical BDC process; derive closed forms for survival, load, release, burst timing and size; embed those in a renewal BMVR forced by the intracellular process. At fixed total output, R₀ is unchanged by bursting, but generation times change: bursting lowers establishment extinction iff 1/δ < 1/β + 1/μ, while deterministic growth is typically faster under budding. The cleanest single-cell fact: the burst-size distribution is exactly the quasi-stationary load distribution — both geometric with ratio 1/a.

**Estimated length:** 45–60 pages of main text + appendices.

---

## 2. Notation and convention decisions (fix first)

Adopt the canonical table from master notes §3 throughout. Concretely:

- **Rates:** β (birth), μ (death), δ (catastrophe) — drop λ for birth (Ch.3 uses both; unify to β). γ = population infection rate; c = virion clearance; d_𝓘 = infected-cell removal (never δ).
- **States/variables:** X_t intracellular count; R the rupture state (Ch.3 uses H — flag the cross-chapter mismatch); W_t released count (not Y_t); 𝒦 burst size (never bare K, since K(t) = 𝔼[X_t²]).
- **Functions:** I(t) no-burst probability; D(t) internal clearance without burst (= p₀); Î(t) = I − D productive-infection probability (the thesis formula is wrong for μ>0 — restate the corrected form and note the correction); J, K moments; V(t) = 𝔼[W_t].
- **Shortcuts:** a, b characteristic roots (b<1<a); A = a−1, B = 1−b, θ = β(a−b); workhorse identity AB = δ/β.
- **Population:** 𝓘(t) infected-cell count, 𝓥(t) free-virion count, i(t) = γT𝓥 incidence (T held constant), kernels Î(a), g(a) = δK(a); Laplace transforms with tilde; q = γT/(γT+c).
- **Theorem environments:** reuse the existing `theorem/proposition/lemma/corollary/definition/remark` block in main.tex; add a `result` style if desired (master notes use it).
- **Macros to add to main.tex:** `\Ihat`, `\Kb`, `\Icell`, `\Vfree`, `\Lap`, `\Prob`, `\E`, `\Fhyp`, `\wt` (exists), `\ddt` (exists). Fix `\Vt` (currently renders as a stray leading subscript).

---

## 3. Section-by-section outline

Status tags: **[keep]** minor edits · **[rewrite]** exists but must be rebuilt · **[new]** must be written.

### 4.1 Chapter introduction — **[new]** (replaces empty `01_opening.tex`)
- Motivation: the BMVR's constant-p assumption vs lytic biology (Y. pestis, F. tularensis, lytic phage); what Ch.3 already supplies.
- Research questions (deliver on Ch.1 RQ3's promise of "a potential update to the standard BMVR" — the renewal model is the delivery).
- The killing-vs-catastrophe distinction (absorb current `02_specification_of_rupture_state.tex` here as a short subsection; fix typos "occurrs/seperate/killng").
- Chapter map.

### 4.2 Recap: process, roots, fixation functions, moments — **[new]** (≈3 pages)
- Restate (from Ch.3, with corrections applied so the chapter is self-contained):
  - process definition and joint process (X_t, W_t); burst time τ.
  - roots a, b; A, B, θ; Vieta + AB = δ/β.
  - I, D, Î closed forms (Result res:IDIhat) — flag the corrected Î and the wrong thesis formula in a remark.
  - J, K, V simplified forms; V′ = δK; V∞ = aB/A; 𝔼[𝒦 | burst] = a/(a−1); the μ=0 collapse (b=0, V∞ = 1+β/δ = QS mean).
- Source: master notes Part A. This section is the reference table the rest of the chapter cites.

### 4.3 The probability generating function — **[rewrite]** (`03_…pdes.tex` + `04_identifying_the_pgfs.tex`)
- PGF definition; forward Kolmogorov equations; PDEs for catastrophe and killing variants.
  - Fixes: "PDF"→"PGF"; misspellings; the `\pdx{}{t}{…}` three-argument macro bug; state explicitly that the catastrophe PGF is **defective** (G(1,t) = I(t) ≠ 1), the killing one is proper.
- Method of characteristics: full derivation for killing (keep current structure, which is good), catastrophe as the simpler variant; identify G(z,t) in both forms (the differentiation-friendly form for later).
- Extraction: mean via ∂zG|_{z=1}; state-probability formula via n-fold differentiation (current eq. `stateFormula`).
- Optional: move the longer algebra to an appendix if the chapter runs long.

### 4.4 State probabilities and the quasi-stationary distribution — **[rewrite + major upgrade]** (`05_state_probabilities.tex` + `06_quasi_stationary_distribution.tex`)
- p₀(t) for both variants; p_n(t) formula (current eq. `stateprob`).
- **[new]** Conditional on X_t ≥ 1 the load is geometric with ratio P(t) = (1−w)/(b−aw) at every t, P(t) → 1/a.
- **[new]** Consistency: Σ_{n≥1} p_n(t) = Î(t) (corrected Î) — closes the loop with §4.2 and silently validates the Ch.3 correction.
- QSD definition via conditional probabilities; fixation probability F(t) = 1 − Î(t) (discharges the section's own open question "what form does F(t) take").
- **Headline Result: QSD = geometric(1/a)** on {1,2,…}: QSD(n) = (a−1)a^{−n}; moments ⟨X⟩_QS = a/(a−1), Var = a/(a−1)².
- Keep the Icarus passage only if it matches thesis voice (it is the draft's most literary paragraph — trim or keep deliberately); fix the garbled "Ignoring, for now…" sentence; fix figure caption (two curves both called "yellow").
- Figures: QSmean/QS1 + QS2 (or QSMu0/QSmeanNE0 pair).
- **[new]** Mean productive lifetime 𝔼[T_prod] = ∫Î = β⁻¹ log(a/(a−1)); interpretation as time for exponential growth to reach the QS level.

### 4.5 Burst time and burst size — **[rewrite + major upgrade]** (`07_burst_size_distribution.tex`)
- **[new]** Burst time: Pr{τ>t} = I(t); defective density φ(t) = −I′(t) = δJ(t); mass b at τ=∞; conditional density δJ/(1−b). Write φ = δJ wherever the draft says "known pdf".
- Burst size: replace "The current goal is to verify this using Gillespie simulations" with the **analytic proof**: d/dt[P^k/(kβ)] = p_k(t) ⇒ Pr{𝒦=k} = (δ/β)a^{−k}; conditional law (a−1)a^{−k}; checks Σ = 1−b and Σk· = V∞. (Gillespie figure becomes optional bonus.)
- **[new]** Identity burst size = QSD, stated as a Result; note the open conceptual proof (size-biasing/Yaglom argument) honestly.
- **[new]** Size-biasing and late bursts: Pr{𝒦=k | τ=t} = k p_k(t)/J(t); 𝔼[𝒦 | τ=t] = K/J → 1 + (2β/δ)(1−b): a very late burst is roughly twice an average one.
- **[new]** Second moment of release 𝔼[W_t²] (corrected eq:EW2, with the sign/+1 fix explained in a remark) and Var(W_t) — needed later for the assay predictions.

### 4.6 Conditional burst means: resolving the "curious circularity" — **[rewrite]** (`08_further_considerations.tex`)
- Keep the V(t) decomposition and 𝔼[𝒦] = V∞/(1−b) = (β−μ)/δ + 1/(1−b) (discharges the "(check)").
- Replace the recorded confusion with the resolution:
  - 𝔼[𝒦·1{burst} | τ>t] = (V∞−V(t))/I(t) → 0 (conditioning on "not yet" converges to "never").
  - The interesting limit conditions on *eventual* burst: (V∞−V(t))/(I(t)−b) → ⟨X²⟩_QS/⟨X⟩_QS by l'Hôpital (V′=δK, I′=−δJ).
- Short section (1–2 pages); can merge into §4.5.

### 4.7 Multiplicity of infection — **[new]** (master notes Part C)
- k founders, shared catastrophe clock: I_k = I^k, D_k = D^k, Î_k = I^k − D^k (flag the false thesis claim Î_k = Î^k).
- Corrected moments J_k, K_k and release kernel g_k = δK_k (the I-powers matter; master-equation check value K₂ = 22.264 at (1, 0.2, 0.05), t=1).
- Lifetime yield V∞^(k) integral formula; μ=0 closed form k + β/δ; the biological point: yield is **not** k·V∞ because the first catastrophe dumps the whole cell once. Superlinearity of g_k in k as a testable low-MOI prediction.
- Decide here whether MOI belongs in Ch.4 or later; the notes file it under Ch.4 material.

### 4.8 Chained immediate transfer — **[new, from `N_eq_2.tex`]** (scope decision — see §8)
- Setup: M host cells; on rupture the whole load transfers immediately to a fresh cell; extreme caricature of serial passage; motivation (O(100) CFU vs huge macrophage pool).
- Rupture-size laws (μ=0): Pr{r_k = n} = 𝒜_k^{(n)} s^k ρ^{n−1}; binomial-coefficient closed form; recurrence; special cases r₁ (geometric — matches one-cell BDC), r₂, r₃; induction proof of the coefficient formula (draft says "perhaps possible to prove by induction" — do it).
- Rupture times: first rupture from m founders, Pr{t₁>t} = S(t)^m, density −mS^{m−1}S′; burst-only vs general-fixation CDF/PDF pairs (t̂₁: δJ/(1−b); t₁: δJ + μp₁).
- PGF of r₁ and of r̂₁ (geometric-series derivation, already written).
- Status flags: the draft's r₂ distribution formula is unverified → either verify numerically before inclusion or state the partial result and mark the joint (t₂, r₂) law and general-μ intervals as open.

### 4.9 From one cell to a population: why constant-p fails — **[rewrite of `09_…bmvr.tex` opening]**
- Classical BMVR as comparator, with the **correct** infection term γT𝓥 (Ch.1's βSI form is an erratum; Ch.4 §9 already uses the right one).
- The failed proposal p = ⟨X⟩_QS: dimensional obstruction (count ≠ rate); when μ=0 it equals V∞, i.e. lifetime output substituted for a rate; both candidate integrals give counts, not rates; the right weight is the age distribution of infected cells, not the burst-time density.
- 𝓥(t) = N₀V(t) only for synchronous infection; asynchrony is the problem — and the renewal structure is the answer.
- Close with the draft's own "Iterating cycles" paragraph, which already describes the renewal object in words: formalize it in §4.10. (This turns the chapter's failed attempt into motivation — good thesis narrative.)

### 4.10 Burst-aware renewal BMVR — **[new, core of the chapter]** (master notes Part D)
- The two kernels: Î(a) (survival/productive) and g(a) = δK(a) = V′(a) (expected release flux — burst rate δX times size X gives δ𝔼[X²]).
- **Result (new viral dynamics):** 𝓘 = 𝓘₀Î + i∗Î; 𝓥′ = 𝓘₀g + i∗g − c𝓥, i = γT𝓥. Classical-vs-new replacement table.
- Honest novelty remark: the renewal/age-structured framework is standard (McKendrick–von Foerster; Nelson–Gilchrist–Perelson); the contribution is closed-form mechanistic kernels + consequences.
- Numerical verification summary in text (kernel integrity; γT=0 reduction; exponential kernels ⇒ classical BMVR; growth rate = characteristic root; R₀ threshold; Gillespie cohort match) with the **headline: 53/53 checks pass**; full test catalogue → appendix; figures D, E, F, H from `verify_figures/`.
- Overlays: `kernels.pdf`; `overlay_I.pdf`, `overlay_V.pdf`, `overlay_rel_diff.pdf`, `overlay_growth_phase.pdf`, `overlay_V_with_naive.pdf` (legend: solid navy = renewal; dashed orange = classical matched at r=0; dotted green = naive p = ⟨X⟩_QS). Reading: even fairly matched classical ODEs miss the early lag, peak timing and late growth; relative virion discrepancy often order-one in supercritical regimes.

### 4.11 Effective parameters, R₀, and identifiability — **[new]**
- p_eff(r) = δK̃(r)/Î̃(r); d_eff(r) = 1/Î̃(r) − r; exact for exponential solutions only.
- Limits: r=0 → p_eff = βV∞/log(a/(a−1)), d_eff = β/log(a/(a−1)); r→∞ → δ and μ+δ (young-cell limit). p_eff decreasing in r.
- Closed Laplace transforms (₂F₁ forms) — body if short, else appendix.
- Characteristic equation r + c = γT·δK̃(r); **R₀^ODE = γT V∞/c is invariant** to bursting at fixed total output (bursting changes generation times, hence r and extinction, not the threshold).
- Careful two-notions caveat: ODE R₀ vs branching mean m = qV∞ (agree when γT ≪ c).
- **Identifiability negative result:** three intracellular rates map to two BMVR parameters at any fixed r — not invertible; three observables that rescue it (burst-size dispersion 1/a; no-burst fraction b; shape of φ). Ch.4 §9's aim of recovering rates from p alone is impossible — say so.
- Prediction for fitting practice: acute-phase vs set-point fits should give systematically different p; the eclipse-like delay emerges without extra parameters.
- **New figure (high value, currently an open task):** p_eff(r), d_eff(r) across a physiological range of r for representative (β,μ,δ).

### 4.12 Flooding advantage and the growth-rate trade-off — **[new]** (placement decision — see §8)
- Offspring of one infected cell: G_off(z) = b + (δ/β)·y/(a−y), y = 1−q+qz; mean m = qV∞; variance.
- Extinction probability in closed form: z_ext^burst = [a(1−q+qb) − 1 + q]/q.
- **Main theorem:** vs matched-mean budding (geometric offspring), z_ext^burst − z_ext^bud = (L−1)(1/m − 1), L = a(1−b). Bursting strictly lowers extinction iff L>1 ⇔ 1/δ < 1/β + 1/μ (μ=0: always). Numerical checks table ((1,0,0.1) burst wins; (1,0.9,0.1) budding wins; (1,0.5,1/3) tie).
- L=1 strengthening: offspring law exactly geometric (laws, not just extinction probabilities, coincide); variance ordering flips with L.
- Deterministic trade-off: at matched R₀ and matched mean productive lifetime, r_bud > r_burst in all checked regimes (example: (1,0,0.1), R₀=2: 0.25 vs 0.18).
- Biological headline: at fixed output, bursting can lower early extinction while slowing deterministic invasion; R₀ fixed, z_ext and r move in opposite directions.
- Caveat: comparison holds offspring mean fixed (branching structure only); nonlinear effects separate.
- Optional: optimal burst rate at fixed m (δ threshold δ* = βμ/(β+μ) when μ>0).

### 4.13 Spectrum of release models — **[new, deliberately brief]** (scope decision — see §8)
- Universal renewal skeleton: any intracellular model supplying (S, g) induces the same IDE pair; table of 6 models (classical BMVR, absorbing BDC, MOI-k, reset, HIV multi-stage, two-type/GATE).
- One paragraph each (with pointers to appendix or Ch.6): the five modular ODE cases (eclipse; stock+export; proportional dump); reset catastrophe (one cell dumps many times; mature-cell limit p∞ = δ𝔼_π[X²]); boolean partial release (binomial thinning, φ∈[0,1] interpolates budding↔bursting); self-exciting/Hawkes variants.
- Keep to ~2 pages; the detail lives in new_notes2 and belongs in the paper/Ch.6, not the thesis main text.

### 4.14 Contrast with HIV: what not to claim — **[new, brief]**
- What Hataye et al. 2019 show (the folder's `paper.pdf` is this paper): stochastic initial release; critical threshold for transition to exponential spread; Allee-type establishment; high silent fraction.
- Supported-vs-not table: HIV buds with a multi-stage eclipse and short productive pulse; it is **not** a literal one-type load-proportional terminal catastrophe; memoryless constant-p from t=0 also rejected.
- HIV intracellular mean growth is mean-linear (immigration-type), not exponential — fixed provirus template; pure m′ = rm BDC fits lytic bacteria/phage, not HIV.
- Function in the chapter: scope protection for the claims above + bridge to later chapters.

### 4.15 Discussion — **[new]**
- Single-cell assay predictions for lytic systems (the five predictions: no-release fraction b; single terminal step; jump-time density δJ/(1−b); jump sizes geometric(1/a) = QSD; between-well variance from Var(W∞)).
- Consequences for BMVR fitting practice; "p is not a constant of the pathogen".
- Connections forward: Ch.5 two-type process → mechanistic eclipse (GATE observation: δ₁=0<δ₂ gives S′(0)=0, the eclipse signature usually inserted by hand); Ch.6 budding-vs-bursting spectrum.
- Open problems (from master notes §J.3): conceptual proof of QSD = burst size; two-type killed second moments; flooding boundary vs real pathogen parameters; population-level variance propagation; logistic intracellular growth sensitivity (referee defence: burst hazard ∝ load already regulates; QSD is the conditional stabilisation).

### Appendices
- **A.** Master formula tables (single-cell + population) — from master notes Part J, cleaned.
- **B.** Verification record: full 53-check catalogue (condensed), parameter sets, reproduction instructions (`python3 verify_result_20_1.py`, `python3 plot_bmvr_comparison.py`).
- **C.** (optional) Technical material if the body runs long: hypergeometric Laplace transforms; V∞^(k) integral derivation; chained-transfer PGF coefficient extraction (Θ/Ω machinery from N_eq_2).

---

## 4. Figure and table plan

**Existing, ready to use:**
| Figure | File | Section |
|---|---|---|
| Single-cell kernels Î, g (+classical comparators) | `figures/kernels.pdf` | 4.10 |
| Infected cells overlay | `figures/overlay_I.pdf` | 4.10 |
| Free virions overlay | `figures/overlay_V.pdf` | 4.10 |
| Relative discrepancy | `figures/overlay_rel_diff.pdf` | 4.10 |
| Growth-phase zoom | `figures/overlay_growth_phase.pdf` | 4.10/4.11 |
| Naive-p comparison | `figures/overlay_V_with_naive.pdf` | 4.9/4.10 |
| Exponential-kernel reduction | `verify_figures/D_exponential_reduction.pdf` | 4.10 |
| Growth rate = char. root | `verify_figures/E_growth_rate_match.pdf` | 4.10 |
| R₀ threshold scan | `verify_figures/F_R0_threshold.pdf` | 4.10/4.11 |
| Gillespie cohort (μ=0, μ>0) | `verify_figures/H_gillespie_*.pdf` | 4.10 |
| QS conditional means | `IMG_ch5/QSmean/QS1.png`, `QS2.png` | 4.4 |

**To create:**
| Figure | Section | Effort |
|---|---|---|
| Schematic: single-cell BDC with burst (and bursting vs budding cartoon) | 4.1/4.2 | low (TikZ) |
| Burst-size bars vs QSD geometric(1/a) overlay; burst-time density φ with mass-at-∞ annotation | 4.5 | low (reuse kernels.py machinery) |
| Size-biased late-burst means K/J vs t | 4.5 | low |
| p_eff(r), d_eff(r) over physiological r for several (β,μ,δ) | 4.11 | medium (open task, "the figure that sells the paper") |
| Flooding: z_ext vs q for burst vs bud; L>1/L=1/L<1 triplet | 4.12 | medium |
| Chained-transfer rupture-size laws r₁..r₄ (μ=0) | 4.8 | low |
| Renewal construction diagram (incidence → age-structured cohorts → kernels) | 4.10 | low (TikZ) |

**Tables:** notation table (4.2 or front); classical-vs-renewal replacement table (4.10); verification summary (4.10 body / appendix B full); flooding numerical checks (4.12); master formula tables (Appendix A).

---

## 5. References to add (`references.bib` currently has 1 entry)

Needed at minimum: Brockwell–Gani–Resnick 1982/83 (BDC origin); Karlin & Tavaré (linear growth with catastrophe); van Doorn & Pollett 2011 (QSD — already present); Yaglom 1947 (QSD limit, if cited); Nowak & Bangham 1996 and Perelson et al. 1996 (BMVR attribution — check McLean 1993 claim); McKendrick 1926 / von Foerster or Diekmann et al. (age structure); Nelson–Gilchrist–Perelson (age-structured within-host); Gilchrist & Coombs (nested models); Heffernan & Wahl (burst-size evolution); Pearson–Krapivsky–Perelson (early stochastic infection); Carruthers et al. 2020 (F. tularensis BDC); Hataye et al. 2019 (HIV contrast — `paper.pdf`); possibly McKendrick/Keeling for branching. Verify all BMVR attributions against Ch.1 (erratum 1.5).

---

## 6. Errata that must be absorbed into this chapter

From extension notes Part IV, Chapter 4 items (each mapped to the plan):

| # | Issue | Handled in |
|---|---|---|
| 4.1 | §9's p = ⟨X⟩_QS dimensionally wrong | §4.9 (motivation) + §4.10–11 (replacement) |
| 4.2 | QS-mean formula missing; μ=0 subtlety | §4.4 (⟨X⟩_QS = a/(a−1); V∞ equal only when μ=0) |
| 4.3 | Two candidate integrals unresolved | §4.9 (both fail for stated reasons) |
| 4.4 | N₀V(t) only for synchronous infection | §4.9 |
| 4.5 | "Iterating cycles" stops in words | §4.10 (formalized as renewal) |
| 4.6 | R vs H; I double-meaning | §2 notation decisions |
| 4.7 | `\Vt` macro broken | §2 (fix macros) |
| 4.8 | §7 awaiting Gillespie verification | §4.5 (analytic proof replaces it) |
| 4.9 | Antiderivative duplicated/n↔k | §4.5 cleanup |
| 4.10 | §6's open F(t) question | §4.4 (F = 1 − Î) |
| 4.11 | QSD never identified | §4.4 headline result |
| 4.12–13 | Garbled sentence; caption "yellow" twice | §4.4 |
| 4.14 | §8 circularity + "(check)" | §4.6 |
| 4.15–16 | Defective PGF unstated; "PDF", typos | §4.3 |
| 4.17 | Empty `01_opening.tex` | §4.1 |
| 4.18 | Stale Ch.3 duplicate in this folder | housekeeping: archive/delete `3 BDC core/` here |

**Cross-chapter dependencies (Ch.3 must eventually agree):** corrected Î (3.1), Î_k = I^k − D^k (3.2), 𝔼[W²] signs (3.3), K(I) form (3.4), duplicated sections 08/10 and 09/11 (3.5), λ→β / Y→W / H→R unification (3.6). Plan: Ch.4 restates the corrected forms self-contained with brief remarks, so the chapter is correct standalone; apply the Ch.3 fixes as a separate workstream so the two chapters agree at submission.

---

## 7. Build and verification steps

1. Update `document MAIN/main.tex`: new macros (§2), title/date, added section files, appendix machinery.
2. Rewrite/create section files in place (`01_…`–`09_…`), then add `10_`–`15_` + appendix files, keeping the existing numbered-file convention.
3. Extend `references.bib` (~15–20 entries).
4. Regenerate figures: `python3 figures/plot_bmvr_comparison.py`; `python3 new_notes3/verify_result_20_1.py` (confirms 53/53 still passes; refreshes report/figures). Copy/link `verify_figures/` into `document MAIN/figures/`.
5. New figure scripts (§4 table) — extend `plot_bmvr_comparison.py` or sibling scripts in `figures/`.
6. Compile `latexmk -pdf main.tex` (unsrt bibliography; expect 2 passes for cleveref).
7. QA pass: every boxed formula in the master formula tables appears in the chapter; all [CORRECTED] items carry a remark; no "need to", "(check)", "perhaps" left in body text.

---

## 8. Decision points (need your call)

1. **Flooding / budding-vs-bursting material (§4.12).** The thesis tree has a dedicated Chapter 6 "Bursting and budding". Options: (a) keep flooding + trade-off here as the chapter's population-level climax (as the master notes recommend); (b) keep here only the offspring/extinction machinery needed for the renewal chapter and move the flooding theorem + r-trade-off to Ch.6. **Recommendation: (a)** — the results are interlocked, and Ch.6 can take the evolutionary/intermediate-release discussion instead.
2. **Spectrum + HIV depth (§4.13–14).** Options: (a) brief versions as planned (~2 pages + ~1.5 pages); (b) full Cases 1–5/reset/boolean/HIV-stage detail (~+12 pages). **Recommendation: (a)** — the detail is paper material and overlaps Ch.6.
3. **Chained transfer scope (§4.8).** Options: (a) verified μ=0 rupture-size laws + time distributions, with r₂/t₂ joint laws marked open; (b) attempt to verify/derive the unverified r₂ formula and t₂ distribution first. **Recommendation: (a)** for the chapter; (b) as a follow-up task.
4. **Housekeeping:** archive or delete the stale `3 BDC core/` copy inside this folder (erratum 4.18), and update the "November 2024" date line.

---

## 9. Suggested writing order

1. **Phase 0 — scaffolding:** macros, notation table, `main.tex` restructure, bib entries. *(unblocks everything)*
2. **Phase 1 — single-cell part:** §4.2 → §4.3 → §4.4 → §4.5 → §4.6 (mostly rewriting existing text against corrected formulas).
3. **Phase 2 — population core (largest new writing):** §4.9 → §4.10 → §4.11, interleaving existing figures; run verification suite early so figures are final.
4. **Phase 3 — extensions and framing:** §4.7, §4.8, §4.12, §4.13, §4.14, §4.1, §4.15, appendices.
5. **Phase 4 — QA:** formula-table sweep, errata checklist (§6) sign-off, compile, proofread.
