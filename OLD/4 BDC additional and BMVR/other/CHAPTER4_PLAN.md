# Chapter 4 — Full Chapter Plan (rev. 2, decisions applied)
**Working title:** *The birth–death–catastrophe process: further results, and a burst-aware model of viral replication*
(standalone draft title currently: "Birth death catastrophe — further results and potential use")

Prepared 2026-08-07 from a full reading of every item in `4 BDC additional and BMVR/`.

**Decisions taken (2026-08-07):**
1. **Flooding advantage + growth-rate trade-off stay in Chapter 4** (chapter's population-level climax). Ch.6 takes the evolutionary/intermediate-release *discussion*.
2. **Full detail** for the release-model spectrum: five ODE cases, reset catastrophe, boolean partial release, self-excitation/Hawkes models, and the complete HIV/Hataye treatment with stage equations.
3. **Chained transfer (N=2/M) completed before writing** — the open r₂/t₂ questions have now been solved and numerically verified (see §4.8 and the new verification suite `N=2 Immediate Transfer content/verify_chained_transfer.py`).
4. **All content of all three `new_notes*` folders is incorporated** — the mapping table in §1.1 shows where every part lands.

---

## 0. Authority of sources

The folder contains four generations of the same material. Where they disagree, use the newest:

| Priority | Source | Role |
|---|---|---|
| 1 (authoritative for mathematics) | `new_notes3/Comprehensive_Corrected_Notes.tex` | Corrected master notes; all errata applied; renewal model verified 53/53 |
| 2 (authoritative for spectrum/HIV detail) | `new_notes2/Core_Publishable_Work_Summary.tex` | Clean statements + the full Cases 1–5, reset, boolean partial release, self-excitation menu, Hataye analysis, HIV stage equations |
| 3 | `new_notes/BMVR_extension_notes.tex` | Consolidation + renewal BMVR + full tagged errata catalogue (Part IV) + open tasks (Part III) + verification record |
| 4 (historical) | `document MAIN/sections/*.tex` | Current chapter draft: PGF derivations good; §6–§9 incomplete or wrong as written |

### 1.1 Complete incorporation map (all three note folders)

| Source location | Content | Lands in chapter § |
|---|---|---|
| new_notes3 §1–2 (how to use, map) | meta; not chapter material | — |
| new_notes3 §3 (canonical notation) | symbol table, collision fixes | 4.2 + front notation table |
| new_notes3 Part A (§4–7: process, roots, I/D/Î, moments, E[W²]) | corrected single-cell closed forms | 4.2 |
| new_notes3 Part B (§8–13: burst time, p_n, QSD=burst, size-bias, circularity, lifetime) | | 4.4–4.6 |
| new_notes3 Part C (§14–15: MOI kernels, chained transfer) | | 4.7, 4.8 |
| new_notes3 Part D (§16–21: why-p-fails, classical BMVR, kernels, renewal + 53/53 verification, overlays, p_eff/R₀/identifiability) | | 4.9–4.11 |
| new_notes3 Part E (§22–25: offspring, extinction, flooding, L=1, variance ordering, r-trade-off, optimal δ) | | 4.12 |
| new_notes3 Part F (§26–29: skeleton, Cases 1–5 summary, reset, boolean, Hawkes pointer) | skeleton table; pointers | 4.13 (full versions from new_notes2) |
| new_notes3 Part G (§30–32: Hataye, HIV growth regime, assay predictions) | | 4.14, 4.15 (full versions from new_notes2) |
| new_notes3 Part H (§33: two-type/GATE) | forward reference | 4.15 |
| new_notes3 Part I (§34–35: verification summary, condensed errata) | | Appendix B + §6 errata checklist |
| new_notes3 Part J (§36–40: formula tables, thesis/paper structure, open tasks, one-page story) | | Appendices A/C; 4.1 intro; 4.15 |
| new_notes Part I (§3–8: consolidated single-cell theory incl. framed corrections and proofs) | proof texts to lift | 4.2–4.6 |
| new_notes Part II (§9–18: why §9 fails, renewal system, literature honesty, p_eff proof incl. 𝔼[T_prod] derivation, transforms, R₀, identifiability, flooding, MOI, two-type/GATE, assay confrontation) | | 4.9–4.12, 4.15 |
| new_notes Part III (open tasks) | | 4.15 open problems |
| new_notes Part IV (errata Ch.1/3/4/5/6, cross-cutting, paper outline, verification record) | | §6 of this plan (worklist); cross-cutting items → thesis-wide |
| new_notes2 §1–3 (one-page story, notation, single-cell process) | | 4.1, 4.2 |
| new_notes2 §4–5 (burst/QSD with proof, size-bias) | | 4.4–4.5 |
| new_notes2 §6–7 (renewal equations with replacement table, differential form, novelty remark; overlays with captions and reading guide) | | 4.10 |
| new_notes2 §8 (effective parameters, exact reduction, R₀, p-not-constant, identifiability) | | 4.11 |
| new_notes2 §9 (flooding, offspring, extinction, matched-R₀ comparison) | | 4.12 |
| new_notes2 §10 (MOI, two-type/eclipse, assay predictions) | | 4.7, 4.15 |
| new_notes2 §11 (Hataye findings list, supported/not table, biology table, candidate HIV stage equations (4.19)–(4.30), Allee incidence, renewal kernels (S_HIV, g_HIV), what-to-keep/not-claim, suggested role) | | 4.14 (full) |
| new_notes2 §12 (reset-catastrophe process: table, kernels, renewal, p_eff, mature limit p∞ = δ𝔼_π[X²], comparison table, optional eclipse) | | 4.13.3 |
| new_notes2 §13 (HIV linear-vs-exponential dichotomy, Tat analysis, recommended regime, model ranking) | | 4.14.4 |
| new_notes2 §14 (Cases 1–5 with all equations, R₀'s, multi-stage eclipse, quasi-steady limits, composability, summary table) | | 4.13.2 |
| new_notes2 §15 (self-excitation: 12-model menu, nesting, focal Models 7/6/10/2 with equations, comparison table, confidence ranking) | | 4.13.4 |
| new_notes2 §16 (partial release: options A–G, boolean process, feasibility table, partial-vs-continuous visibility, recommendation) | | 4.13.5 |
| new_notes2 §17–18 (publishable claims, paper structure, omissions; quick-reference sheet) | | 4.15 discussion; Appendix A; companion paper plan |
| N_eq_2.tex (rupture-size laws, time distributions, PGF coefficient machinery, open t₂ question) | completed + corrected (below) | 4.8 |
| verify_chained_transfer.py (new) | 25-check suite for 4.8 | 4.8 + Appendix B |

Other assets:

| Item | Content |
|---|---|
| `figures/` | `kernels.pdf`, `overlay_I.pdf`, `overlay_V.pdf`, `overlay_rel_diff.pdf`, `overlay_growth_phase.pdf`, `overlay_V_with_naive.pdf`, generator `plot_bmvr_comparison.py` |
| `document MAIN/figures/IMG_ch5/QSmean/` | Simulation plots QS1/QS2 (μ=0, μ>0 QS means), QSmeanNE0, QSMu0 |
| `new_notes3/verify_result_20_1.py` (+report, metrics, `verify_figures/`) | Numerical verification of the renewal system: **53/53 PASS**; figures D, E, F, H |
| `N=2 Immediate Transfer content/verify_chained_transfer.py` (+report, metrics, figures) | **NEW**: verification of the completed chained-transfer results (run log kept with the folder) |
| `paper.pdf` | Hataye et al. 2019, *Cell Host & Microbe* 26:748–763 — the HIV-establishment reference for §4.14 |
| `3 BDC core/` | Stale duplicate of Chapter 3, kept here for continuity checks (errata 4.17 says delete/archive it) |
| `Chapter4_BDC_further_results.pdf` | Compiled snapshot of the current draft |

---

## 2. What the chapter is

**Position.** Chapter 3 defines the BDC process and derives I, J, K, V. Chapter 4 does three things:

1. **Completes the single-cell theory** — full transient distribution (PGF route), quasi-stationary distribution, burst-time and burst-size laws, the headline identity *burst-size distribution = QSD*, MOI, and the completed chained-transfer (N=2/M) model.
2. **Scales the theory up** — embeds the closed-form single-cell kernels into a renewal (age-structured) version of the Basic Model of Viral Replication, replacing the phenomenological constant release rate *p*; extracts effective parameters, R₀ invariance, identifiability, the flooding advantage, and the growth-rate trade-off.
3. **Maps the modelling spectrum** — five ODE BMVR cases, reset catastrophe, boolean partial release, self-exciting release — with the renewal skeleton as the unifying object — and closes with an honest HIV contrast (Hataye-guided) and a discussion of predictions.

**One-page story** (from master notes §J.4, expanded into the introduction):
> Within-host models treat infected cells as black boxes releasing at constant rate p. Lytic pathogens grow inside a cell and dump their load in one burst. Model one cell as a classical BDC process; derive closed forms for survival, load, release, burst timing and size; embed those in a renewal BMVR forced by the intracellular process. At fixed total output, R₀ is unchanged by bursting, but generation times change: bursting lowers establishment extinction iff 1/δ < 1/β + 1/μ, while deterministic growth is typically faster under budding. The cleanest single-cell fact: the burst-size distribution is exactly the quasi-stationary load distribution — both geometric with ratio 1/a.

**Estimated length:** 65–85 pages of main text + appendices (full-detail spectrum and HIV material add ~20 pages over the lean version).

---

## 3. Notation and convention decisions (fix first)

Adopt the canonical table from master notes §3 / extension notes §2 throughout:

- **Rates:** β (birth), μ (death), δ (catastrophe) — drop λ for birth. γ = population infection rate; c = virion clearance; d_𝓘 = infected-cell removal (never δ). ν = immigration/production rate; ε = per-unit export; a = eclipse conversion (context-dependent; avoid clash with root a in the same scope — the HIV section uses its own scope and says so).
- **States/variables:** X_t intracellular count; R the rupture state (Ch.3 uses H — flag the cross-chapter mismatch); W_t released count (not Y_t); 𝒦 burst size (never bare K, since K(t) = 𝔼[X_t²]).
- **Functions:** I(t) no-burst probability; D(t) internal clearance without burst (= p₀); Î(t) = I − D productive-infection probability (thesis formula wrong for μ>0 — restate corrected form with a remark); J, K moments; V(t) = 𝔼[W_t].
- **Shortcuts:** a, b characteristic roots (b<1<a); A = a−1, B = 1−b, θ = β(a−b); workhorse identity AB = δ/β; L = a(1−b) = a − μ/β (flooding parameter; context-separate from the HIV latent class "L" — rename the HIV latent class to L₀ in §4.14 to avoid collision).
- **Population:** 𝓘(t) infected-cell count, 𝓥(t) free-virion count, i(t) = γT𝓥 incidence (T held constant), kernels Î(a), g(a) = δK(a); Laplace transforms with tilde; q = γT/(γT+c); Q = total intracellular stock; E = eclipse class.
- **Theorem environments:** reuse the existing block in main.tex; add a `result` style (master notes use it).
- **Macros to add to main.tex:** `\Ihat`, `\Kb`, `\Icell`, `\Vfree`, `\Lap`, `\Prob`, `\E`, `\Fhyp`, plus `\wt`, `\ddt` (exist). Fix `\Vt` (currently renders as a stray leading subscript).

---

## 4. Section-by-section outline

Status tags: **[keep]** minor edits · **[rewrite]** exists but must be rebuilt · **[new]** must be written.

### 4.1 Chapter introduction — **[new]** (replaces empty `01_opening.tex`)
- Motivation: the BMVR's constant-p assumption vs lytic biology (Y. pestis, F. tularensis, lytic phage); what Ch.3 already supplies; the "perilous beginning" theme of Ch.3 §2.
- Research questions (deliver on Ch.1 RQ3's promise of "a potential update to the standard BMVR" — the renewal model + its consequences are the delivery).
- The killing-vs-catastrophe distinction (absorb current `02_specification_of_rupture_state.tex` as a short subsection; fix typos "occurrs/seperate/killng").
- One-page story adapted; chapter map.

### 4.2 Recap: process, roots, fixation functions, moments — **[new]** (≈3–4 pages)
- Restate (from Ch.3, with corrections applied so the chapter is self-contained):
  - process definition and joint process (X_t, W_t); burst time τ.
  - roots a, b; A, B, θ; Vieta + AB = δ/β (flag: belongs in the Ch.3 reference table too).
  - I, D, Î closed forms (Result res:IDIhat) — remark on the corrected Î and the wrong thesis formula (Î′ ODE; the I² − D² branching term; numeric contrast 0.8087 vs 0.6675 at (1, 0.2, 0.5), t=1).
  - J, K, V simplified forms (remark on the cancellations); V′ = δK; V∞ = aB/A; 𝔼[𝒦 | burst] = a/(a−1); the μ=0 collapse (b=0, V∞ = 1+β/δ = QS mean).
  - Corrected 𝔼[W_t²] and Var(W_t) with the geometric-moment check (μ=0 limit).
- Source: master notes Part A + extension notes Part I §5. This section is the reference table the rest of the chapter cites.

### 4.3 The probability generating function — **[rewrite]** (`03_…pdes.tex` + `04_identifying_the_pgfs.tex`)
- PGF definition; forward Kolmogorov equations; PDEs for catastrophe and killing variants.
  - Fixes: "PDF"→"PGF"; misspellings; the `\pdx{}{t}{…}` three-argument macro bug; state explicitly that the catastrophe PGF is **defective** (G(1,t) = I(t) ≠ 1), the killing one is proper.
- Method of characteristics: full derivation for killing (keep current structure), catastrophe as the simpler variant; identify G(z,t) in both forms (the differentiation-friendly form for later). Include the k-founder PGF G_k = G₁^k (needed by §4.7–4.8).
- Extraction: mean via ∂zG|_{z=1}; state-probability formula via n-fold differentiation (current eq. `stateFormula`).
- Optional: move the longer algebra to an appendix if the chapter runs long.

### 4.4 State probabilities and the quasi-stationary distribution — **[rewrite + major upgrade]** (`05_state_probabilities.tex` + `06_quasi_stationary_distribution.tex`)
- p₀(t) for both variants; p_n(t) formula (current eq. `stateprob`).
- **[new]** Conditional on X_t ≥ 1 the load is geometric with ratio P(t) = (1−w)/(b−aw) at every t, P(t) → 1/a.
- **[new]** Consistency: Σ_{n≥1} p_n(t) = Î(t) (corrected Î) — closes the loop with §4.2.
- QSD definition via conditional probabilities; fixation probability F(t) = 1 − Î(t) (discharges the section's own open question).
- **Headline Result: QSD = geometric(1/a)** on {1,2,…}: QSD(n) = (a−1)a^{−n}; moments ⟨X⟩_QS = a/(a−1), Var = a/(a−1)², ⟨X²⟩_QS = a(a+1)/(a−1)².
- Keep the Icarus passage only if it matches thesis voice; fix the garbled "Ignoring, for now…" sentence; fix figure caption (two curves both called "yellow").
- Figures: QSmean/QS1 + QS2 (or QSMu0/QSmeanNE0).
- **[new]** Mean productive lifetime 𝔼[T_prod] = ∫Î = β⁻¹ log(a/(a−1)) = β⁻¹ log⟨X⟩_QS, with the partial-fractions proof (extension notes §10.1); interpretation: time for exponential growth at rate β to reach the QS level.

### 4.5 Burst time and burst size — **[rewrite + major upgrade]** (`07_burst_size_distribution.tex`)
- **[new]** Burst time: Pr{τ>t} = I(t); defective density φ(t) = −I′(t) = δJ(t); mass b at τ=∞; conditional density δJ/(1−b). Write φ = δJ wherever the draft says "known pdf".
- Burst size: replace "verify using Gillespie simulations" with the **analytic proof**: d/dt[P^k/(kβ)] = p_k(t) ⇒ Pr{𝒦=k} = (δ/β)a^{−k}; conditional law (a−1)a^{−k}; the two consistency checks (Σ = 1−b via AB = δ/β; first moment = V∞, validating three results at once).
- **[new]** Identity burst size = QSD, stated as a Result; honest remark that the conceptual proof (size-biasing/Yaglom) is open.
- **[new]** Size-biasing and late bursts: Pr{𝒦=k | τ=t} = k p_k(t)/J(t); 𝔼[𝒦 | τ=t] = K/J → 1 + (2β/δ)(1−b): a very late burst is roughly twice an average one — the signature of size-biasing a geometric.

### 4.6 Conditional burst means: resolving the "curious circularity" — **[rewrite]** (`08_further_considerations.tex`)
- Keep the V(t) decomposition and 𝔼[𝒦] = V∞/(1−b) = (β−μ)/δ + 1/(1−b) (discharges "(check)").
- Replace the recorded confusion with the resolution:
  - 𝔼[𝒦·1{burst} | τ>t] = (V∞−V(t))/I(t) → 0 (conditioning on "not yet" converges to "never").
  - The interesting limit conditions on *eventual* burst: (V∞−V(t))/(I(t)−b) → ⟨X²⟩_QS/⟨X⟩_QS by l'Hôpital (V′=δK, I′=−δJ).
- Short section (1–2 pages); can merge into §4.5.

### 4.7 Multiplicity of infection — **[new]** (master notes Part C; extension notes §17)
- k founders, shared catastrophe clock: I_k = I^k, D_k = D^k, Î_k = I^k − D^k (flag the false thesis claim Î_k = Î^k; "the instinct was right").
- Corrected moments J_k = kI^{k−1}J, K_k = kKI^{k−1} + k(k−1)J²I^{k−2} and release kernel g_k = δK_k (master-equation check K₂ = 22.264 vs wrong 23.39 at (1, 0.2, 0.05), t=1).
- Lifetime yield V∞^(k) integral formula; μ=0 closed form k + β/δ; the biological point: yield is **not** k·V∞ (shared first catastrophe dumps the whole cell once). Superlinearity of g_k in k as a testable low-MOI prediction.

### 4.8 Chained immediate transfer: completed — **[new, from `N_eq_2.tex` + new verification]**
*Status: the draft's open questions are now solved; results below are verified by `verify_chained_transfer.py` (report + metrics + figure in the same folder).*

- **Setup.** M host cells; on rupture the whole load transfers immediately to a fresh cell; no extracellular phase. Motivation: O(100) CFU founding censuses vs huge macrophage pool; extreme caricature of serial passage; a tractable multi-cell burst-statistics model bridging single-cell and population.
- **Structural observation (the key).** For μ=0, at load n the next event is birth with probability ρ = β/(β+δ) and catastrophe with probability s = δ/(β+δ), *independent of n*. Hence each cell i contributes an independent G_i ~ Geom₀(s) (births before its catastrophe) and
  - **r_k = 1 + G₁ + ⋯ + G_k** ⇒ Pr{r_k = n} = C(n+k−2, k−1) s^k ρ^{n−1}.
  - This proves the draft's recurrence 𝒜_k^{(n)} = Σ_{i≤n} 𝒜_{k−1}^{(i)} (hockey-stick), gives the induction proof the draft asked for, and **corrects the draft's closed form**: (1/k!)(n+k−1)!/(n−1)! = C(n+k−1,k) is off by one shift and contradicts the draft's own r₂, r₃ cases; correct is C(n+k−2, k−1).
  - Consequences (all verified): E[r_k] = 1 + kβ/δ; Var(r_k) = kρ/s²; PGF E[z^{r_k}] = z(s/(1−ρz))^k; normalisation automatic (burst is certain for μ=0).
- **Rupture times.** First rupture from m founders: Pr{t₁>t} = I(t)^m, density −mI^{m−1}I′ = mI^{m−1}δJ (draft's F_m formula, confirmed). Burst-only vs general-fixation pairs for μ>0 (t̂₁: δJ/(1−b); t₁: δJ + μp₁) kept as the general-μ statement.
- **Inter-rupture intervals (new).** Given k founders and G = g births, T(k) = Σ_{j=k}^{k+g} Exp((β+δ)j); hence the Laplace transform
  - L_T(k,u) = Σ_{g≥0} sρ^g Π_{j=k}^{k+g} λ_j/(λ_j+u) = [s·k/(k+u′)]·₂F₁(k+1, 1; k+1+u′; ρ), u′ = u/(β+δ) — continuing the chapter's hypergeometric theme (extension notes remark §10.3).
  - Exact mean E[T(k)] = Σ_{m≥0} ρ^m/((β+δ)(k+m)); **E[T_k] strictly decreasing** — the draft's qualitative "increasing loads, reducing intervals" claim is now quantified.
- **Second rupture time (new, resolves the draft's closing question).** t₂ = t₁ + T₂ with the joint structure coupled through G₁:
  - L₂(u) = Σ_g sρ^g P₁(1+g, u)·L_T(1+g, u), P₁(m,u) = Π_{j=1}^{m} λ_j/(λ_j+u);
  - density available two ways: (i) the exact hypoexponential-mixture density, computed stably by sequential convolution of exponential densities (t₁|G₁ and T₂|(G₁,G₂) are sums of independent exponentials; the repeated rate λ_{1+G₁} is handled by convolution), and (ii) the Laplace form L₂ for transforms/moments. An early Gaver–Stehfest inversion attempt was abandoned (numerically unstable here). The draft's guessed convolution ρ(t₂) = ∫f(τ)Σ_k Pr{r₁=k|τ}φ_k(t₂−τ)dτ is the same statement in different clothes; the Laplace / mixture forms are the tractable ones.
- **Verification record.** Suite `verify_chained_transfer.py`: coefficient identity (exact); size laws k=1..4 × 3 parameter sets (SE-unit pmf comparison, 10⁶ chains); moments; PGF; t₁ density vs δJ; interval Laplace vs series for fixed founders k∈{1,2,3,5} (+₂F₁ cross-check when scipy present); random-founder mixture consistency for chain intervals T₂,T₃; t₂ Laplace; t₂ density vs exact hypoexponential mixture (rel L₂ ≈ 3%); exact t₂ mean for the slow set; monotone interval means vs exact series. **Final run 2026-08-07: 28/28 PASS** (~36 s). Note: environment has numpy + matplotlib but no scipy/mpmath, so the suite must not depend on them.
- **Scope flags.** General-μ joint laws and the M-cell joint law of (t_M, r_M) remain open (state plainly); the PGF coefficient-extraction machinery (Θ/Ω, γ^n v^m integrals) moves to Appendix C as the general-μ route.

### 4.9 From one cell to a population: why constant-p fails — **[rewrite of `09_…bmvr.tex` opening]**
- Classical BMVR as comparator, with the **correct** infection term γT𝓥 (Ch.1's βSI form is an erratum).
- The failed proposal p = ⟨X⟩_QS: dimensional obstruction (count ≠ rate); when μ=0 it equals V∞, i.e. lifetime output substituted for a rate; both candidate integrals fail (∫φ 𝔼[𝒦|τ=t] = V∞, a count; the second has the right dimensions but weights by the burst-time density instead of the age distribution of infected cells).
- 𝓥(t) = N₀V(t) only for synchronous infection; asynchrony is the problem — and the renewal structure is the answer.
- Close with the draft's own "Iterating cycles" paragraph, which already describes the renewal object in words: formalize it next. (The failed attempt becomes the chapter's motivation.)

### 4.10 Burst-aware renewal BMVR — **[new, core of the chapter]**
- The two kernels: Î(a) (survival/productive) and g(a) = δK(a) = V′(a) (expected release flux — burst rate δX times size X gives δ𝔼[X²]).
- **Result (new viral dynamics):** 𝓘 = 𝓘₀Î + i∗Î; 𝓥′ = 𝓘₀g + i∗g − c𝓥, i = γT𝓥. Full replacement table (constant removal AND constant release both replaced — the draft only ever proposed the second). Optional differential form for 𝓘 with the no-constant-d argument.
- Honest novelty remark: the renewal/age-structured framework is standard (McKendrick–von Foerster; Nelson–Gilchrist–Perelson); the contribution is closed-form mechanistic kernels + consequences. State plainly.
- Numerical verification summary in text (kernel integrity; γT=0 reduction; exponential kernels ⇒ classical BMVR; growth rate = characteristic root; R₀ threshold; p_eff(r_*) projection; Gillespie cohort match) with the **headline: 53/53 checks pass**; full test catalogue → Appendix B; figures D, E, F, H from `verify_figures/`.
- Overlays (from new_notes2 §7 with its captions and reading guide): `kernels.pdf`; `overlay_I.pdf`, `overlay_V.pdf`, `overlay_rel_diff.pdf`, `overlay_growth_phase.pdf`, `overlay_V_with_naive.pdf` (legend: solid navy = renewal; dashed orange = classical matched at r=0; dotted green = naive p = ⟨X⟩_QS). Reading: even fairly matched classical ODEs miss the early lag, peak timing and late growth; relative virion discrepancy often order-one in supercritical regimes, worst in high-death; discrepancies grow with R₀ and kernel age-structure.

### 4.11 Effective parameters, R₀, and identifiability — **[new]**
- p_eff(r) = δK̃(r)/Î̃(r); d_eff(r) = 1/Î̃(r) − r; exact for exponential solutions, not transients (frame: for any r there is a unique constant-parameter BMVR reproducing the exponential solution exactly).
- Limits: r=0 → p_eff = βV∞/log(a/(a−1)), d_eff = β/log(a/(a−1)) (= naive moment-matching, consistency); r→∞ → δ and μ+δ (young-cell limit). p_eff decreasing in r.
- Closed Laplace transforms (₂F₁ forms) with the v = e^{−θt} substitution derivation — body or Appendix C.
- 𝔼[T_prod] as the r=0 bridge (already proved in §4.4).
- Characteristic equation r + c = γT·δK̃(r); **R₀^ODE = γT V∞/c is invariant** to bursting at fixed total output (generation times change, threshold doesn't).
- Two-notions caveat: ODE R₀ vs branching mean m = qV∞ (agree when γT ≪ c).
- **Identifiability negative result:** three intracellular rates map to two BMVR parameters at any fixed r — not invertible; three rescuing observables (burst-size dispersion 1/a; no-burst fraction b; shape of φ). Ch.4 §9's aim of recovering rates from p alone is impossible — state as a result, not buried.
- Prediction for fitting practice: acute-phase vs set-point fits give systematically different p (at (1,0,0.1): 4.59 vs 0.1); the eclipse-like delay emerges without extra parameters.
- **New figure (high value):** p_eff(r), d_eff(r) across a physiological range of r for representative (β,μ,δ) — "the figure that sells the paper".

### 4.12 Flooding advantage and the growth-rate trade-off — **[new]** (kept in Ch.4 by decision)
- Offspring of one infected cell: G_off(z) = b + (δ/β)·y/(a−y), y = 1−q+qz; mean m = qV∞; variance.
- Extinction probability in closed form: z_ext^burst = [a(1−q+qb) − 1 + q]/q.
- Comparator: matched-mean budding cell (Exp(d_𝓘) lifetime, constant p, p/d_𝓘 = V∞) → geometric offspring, z_ext^bud = 1/m.
- **Main theorem:** z_ext^burst − z_ext^bud = (L−1)(1/m − 1), L = a(1−b) = a − μ/β. Bursting strictly lowers extinction iff L>1 ⇔ 1/δ < 1/β + 1/μ (μ=0: always, all δ>0). For m ≤ 1 both die out; the sign-flip artefact explained. Numerical checks table ((1,0,0.1) q=0.2: 0.400 vs 0.455; (1,0.9,0.1) q=0.9: 0.935 vs 0.844; (1,0.5,1/3) tie).
- L=1 strengthening: offspring law **exactly geometric** (equivalence chain L=1 ⇔ a = 1+μ/β ⇔ δ(β+μ) = βμ ⇔ 1/δ = 1/β + 1/μ); variance ordering flips with L.
- Deterministic trade-off: at matched R₀ and matched mean productive lifetime, r_bud > r_burst in all checked regimes (example: (1,0,0.1), R₀=2: 0.25 vs 0.18). Optional: optimal burst rate at fixed m (threshold δ* = βμ/(β+μ) for μ>0).
- Biological headline: at fixed output, bursting can lower early extinction while slowing deterministic invasion; R₀ fixed, z_ext and r move in opposite directions.
- Caveat: comparison holds offspring mean fixed (branching structure only); nonlinear effects (immune saturation, local depletion — where Komarova's "all run out at once" intuition lives) are separate; name both mechanisms. Connect to Ch.1 §6 and Ch.7's Komarova discussion; Ch.6 takes the evolutionary framing.

### 4.13 The spectrum of release models — **[new, FULL DETAIL by decision]**
Unifying frame: **any** intracellular model supplying a survival kernel S(a) and release kernel g(a) induces the renewal skeleton i = γT𝓥 (or nonlinear f(𝓥,T)), 𝓘 = 𝓘₀S + i∗S, 𝓥′ = 𝓘₀g + i∗g − c𝓥; effective parameters p_eff = g̃/S̃, R₀ = (γT/c)∫g. Master table of six models (classical BMVR, absorbing BDC, MOI-k, reset, HIV multi-stage, two-type/GATE).

**4.13.1 Classical BMVR as Case 0** (already §4.9; recap its R₀).

**4.13.2 Five modular ODE cases** (from new_notes2 §14, complete):
- Case 1 classic: equations, R₀ = γTp/(c d_𝓘).
- Case 2 eclipse + classic: E-equation, R₀ with factor a/(a+d_E); multi-stage (Erlang) eclipse variant; the standard-within-HIV-modelling status.
- Case 3 stock + continuous export: (𝓘, Q, 𝓥) system with production ν, export ε; quasi-steady stock gives p_eff = εν/(ε+d_𝓘) — **classic BMVR is the fast-export limit**; eclipse-stacked variant; R₀.
- Case 4 stock + proportional full clear: mean-field closure δ𝔼ΣXᵢ² ≈ δQ²/𝓘; quadratic-vs-linear contrast with Case 3; mature balance m = (−d + √(d²+4δν))/(2δ), p_eff = δm²; linearisation caveat at 𝓘≈0 (use single-cell/renewal for thresholds).
- Case 5 eclipse + stock + full clear: the composite; staged lag it produces; R₀ sketch.
- Summary table (intracellular story × free-virus source term); composability notes; link back to the renewal skeleton.

**4.13.3 Reset catastrophe** (from new_notes2 §12, complete): process table (birth/death/immigration/dump-reset at rate δn; cell death d_𝓘 separate); kernels S = e^{−d_𝓘a}, g = δe^{−d_𝓘a}𝔼[X_a²]; moment-closed tractability; renewal BMVR identical in form; p_eff = (r+d_𝓘)g̃(r); R₀ finite only for d_𝓘>0; **mature-cell limit p∞ = δ𝔼_π[X²]** — long-lived cells behave as classical constant-p; comparison table vs absorbing BDC; optional eclipse; the take-away: one cell can dump many times — the multi-pulse caricature on the budding–bursting spectrum (biological-status sentence included).

**4.13.4 Self-exciting release** (from new_notes2 §15, complete):
- Motivation (cooperative Gag nucleation, membrane platforms, recruited ESCRT) balanced against depletion; two levels of BMVR (ODE needs low-dimensional Markov state; renewal always available).
- The 12-model menu table (classical Hawkes, Hawkes+stock, marked, ETAS, Cox+latent, ON/OFF telegraph, λ∝X², nucleation, age-since-last, jumping rate, spatial, full clear) with ODE/renewal feasibility.
- Nesting relations (Model 2 as general form; exponential kernel ⇔ Model 10; recoveries of Cases 3–5).
- Focal models with equations: **7** (λ = δX², cooperative; ODEs = Cases 4–5), **6** (ON/OFF telegraph; split-I ODEs; duty-cycle limit p_eff = ρ·α/(α+β)), **10** (jumping rate r(t), shot-noise; mean-field (𝓘,Q,R,𝓥) ODEs), **2** (Hawkes + stock X; intensity λ = f(X) + Σφ(t−tᵢ); renewal always, ODE only via exponential φ).
- Four-way comparison table (carrier/memory/clusters/ODE/renewal/classic-p limit); biological-confidence caveat (medium–high for clustered release as hypothesis; low–medium for bare Hawkes); practical ranking.

**4.13.5 Boolean / partial release** (from new_notes2 §16, complete):
- Two ingredients: when (event rate λ(X)) and how much (B | X=n).
- Options A–G: boolean/binomial thinning (recommended default), fixed fraction, Beta random fraction, capped batch, size-biased, threshold-then-partial, short high-export window.
- Single-cell boolean process table; nested limits (q=1 → Cases 4–5; B≡1 unit budding → Case 3 discrete; λ=δ constant → mean-equivalent to Case 3 with ε_eff = δq while single-cell paths stay pulsed).
- Mean-field ODEs for boolean λ = δX: Case 4 scaled by q.
- Feasibility table (ODE vs renewal by setup); visibility analysis (partial vs full invisible in mean ODEs under constant clock, visible under load-dependent clock and always in single-cell distributions).
- Recommendation paragraph (boolean q with λ = δX primary; fixed fraction secondary).
- **Link to Ch.6:** this is the budding–bursting spectrum; the flooding boundary as a function of φ remains an open task (state it).

### 4.14 Contrast with HIV: what not to claim — **[new, FULL DETAIL by decision]**
**4.14.1 What Hataye et al. 2019 show** (new_notes2 §11.1, complete; `paper.pdf` in folder):
- Initial release (viral inhibition cultures): high variability; delayed mean release with bulk around days 3–5; constant-p productive-cell model under-dispersed; single exponential eclipse fits poorly (mode day 1), multi-stage (n≈5) fixes timing; transcriptional toggling insufficient; best structure Model 3 = two eclipse paths (high/low potential) + multi-stage + division/death in eclipse; f_HIV ≈ 0.41 detectable; productive sojourns ~1 day; multi-day detection from staggered descendants.
- Establishment (outgrowth cultures): sigmoid establishment law → Allee effect; critical threshold Λ ≈ 2.3 LICs ≈ 5100 detected RNA copies; single-LIC establishment ~2%.
- Supported-vs-not-supported table; biological-distinction table (lytic BDC vs Hataye-guided HIV across 7 axes).

**4.14.2 Candidate HIV stage equations** (new_notes2 §11.3, complete): latent L₀ → two eclipse paths A (Erlang chain E₁..E_n → I^A) and B (E^B → I^B); division/death in eclipse (ρ ≈ μ_E ≈ 0.5/day); productive release p_A ≫ p_B with death δ_I; clearance c; mean-field stage ODEs; coupling to de novo infection with pathway split (π_A, π_B); linear incidence f = γT𝓥 vs **Allee incidence** f = γT𝓥·𝓥/(K_A+𝓥) with K_A anchored to the Hataye threshold; renewal kernels (S_HIV, g_HIV) induced by the stage model — g_HIV ≈ 0 for small age, the mathematical expression of "nothing for a long time, then a lot"; effective parameters carry over by substitution.

**4.14.3 What to keep, what not to claim** (list): keep renewal coupling, stage kernels, "constant p is only an exponential-phase projection", stochastic early failure, eclipse as a real object; do not claim terminal catastrophe δX for HIV, QSD=geometric as an HIV law, one-shot release as the only trajectory, independent branching as the full establishment story near threshold; flooding comparison valid only as a linear baseline, synergy can dominate near ~5×10³ copies.

**4.14.4 HIV intracellular mean growth: linear vs exponential** (new_notes2 §13, complete): the dichotomy table; why HIV is not mean-exponential (fixed provirus template, Pol II, Gag not self-replicating); Tat positive feedback as acceleration *up to* the late ceiling, not overshoot (with the two caveats: stochastic bursts; export balance); confidence grading (high/medium–high/medium); recommended coarse regime **eclipse → mean-linear (immigration-type) accumulation**; model-ranking table; take-away.

**4.14.5 Suggested role** (new_notes2 §11.5): core lytic results are the chapter; this section is the honest boundary + the bridge to any companion paper.

### 4.15 Discussion — **[new]**
- Single-cell assay predictions for lytic systems (the five predictions: no-release fraction b; single-terminal-jump cumulative release; jump-time density δJ/(1−b); jump sizes geometric(1/a) = QSD; between-well variance Var(W∞) from the corrected second moment — which deterministic BMVR cannot produce). Honest caveat: too strong for HIV as literally stated; use for lytic hosts or as the bursting endpoint of the spectrum.
- Consequences for BMVR fitting practice; "p is not a constant of the pathogen".
- Connections forward: Ch.5 two-type process → mechanistic eclipse (**GATE observation**: δ₁=0<δ₂ gives S′(0)=0 — zero initial hazard then rising; the eclipse signature usually inserted by hand, emerging mechanistically with duration set by ν; strongest reason to build the renewal model on the two-type kernel, making Ch.4–5 one story); Ch.6 budding-vs-bursting spectrum and the flooding discussion; Ch.7 Komarova/nonlinear mechanisms.
- Open problems (master notes §J.3 + extension notes Part III): conceptual proof of QSD = burst size; two-type killed second moments + two-type D (the main technical obstacle, with the differentiate-the-backward-system route stated); flooding boundary vs real pathogen parameters (Y. pestis map + size of advantage via eq. flood); population-level variance propagation; partial-release flooding boundary in φ; logistic intracellular growth sensitivity (referee defence: burst hazard ∝ load already regulates; QSD is the conditional stabilisation); literature-positioning items (Carruthers coupling check, Pearson–Krapivsky–Perelson, Nelson–Gilchrist–Perelson, Gilchrist–Coombs, Heffernan–Wahl, BMVR attribution).

### Appendices
- **A.** Master formula tables (single-cell + population) — from master notes Part J, cleaned; quick-reference specialisations (μ=0; L=1; young-cell; r=0 matching).
- **B.** Verification records: renewal suite (53-check catalogue condensed, parameter sets, reproduction instructions) + chained-transfer suite (25-check catalogue, reproduction). Full tables fine in an appendix.
- **C.** Technical material: hypergeometric Laplace transforms with derivation; V∞^(k) integral; chained-transfer PGF coefficient extraction (Θ/Ω machinery, γ^n v^m integrals, the ₂F₁ antiderivative) as the general-μ route; Stehfest inversion summary if not in body.

---

## 5. Figure and table plan

**Existing, ready to use:**
| Figure | File | Section |
|---|---|---|
| Single-cell kernels Î, g | `figures/kernels.pdf` | 4.10 |
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
| Chained transfer (sizes, t₁, t₂, intervals) | `N=2 …/verify_chained_transfer_figures.pdf` | 4.8 |

**To create:**
| Figure | Section | Effort |
|---|---|---|
| Schematic: single-cell BDC with burst; bursting vs budding cartoon | 4.1/4.2 | low (TikZ) |
| Burst-size bars vs QSD geometric(1/a); burst-time density φ with mass-at-∞ annotation | 4.5 | low |
| Size-biased late-burst means K/J vs t | 4.5 | low |
| p_eff(r), d_eff(r) over physiological r, several (β,μ,δ) | 4.11 | medium (open task, "sells the paper") |
| Flooding: z_ext vs q for burst vs bud; L>1/L=1/L<1 triplet | 4.12 | medium |
| Renewal construction diagram (incidence → age cohorts → kernels) | 4.10 | low (TikZ) |
| Spectrum map (budding ↔ bursting axis with Cases/reset/boolean positions) | 4.13 | low (TikZ) |
| HIV stage-model diagram (L₀ → A/B paths → I → 𝓥) | 4.14 | low |

**Tables:** notation table (4.2/front); classical-vs-renewal replacement (4.10); verification summaries (4.10/4.8 body; full in Appendix B); flooding numerical checks (4.12); five-cases summary (4.13.2); 12-model self-excitation menu + four-way comparison (4.13.4); partial-release options + feasibility (4.13.5); Hataye supported/not + biological distinction (4.14); master formula tables (Appendix A).

---

## 6. References to add (`references.bib` currently has 1 entry)

Needed at minimum: Brockwell–Gani–Resnick 1982/83 (BDC origin); Karlin & Tavaré; van Doorn & Pollett 2011 (present); Yaglom 1947 (if the QSD-limit language is used); Nowak & Bangham 1996, Perelson et al. 1996, McLean 1993 (BMVR attribution — verify against Ch.1); McKendrick 1926 / von Foerster (age structure); Nelson–Gilchrist–Perelson; Gilchrist & Coombs; Heffernan & Wahl (burst size); Pearson–Krapivsky–Perelson; Carruthers et al. 2020 (F. tularensis); Hataye et al. 2019 (`paper.pdf`); Hawkes 1971 (self-excitation); Gaver 1965 / Stehfest 1970 (inversion, if Appendix C); Komarova (if Ch.7's discussion is cited). Verify BMVR attributions (erratum 1.5).

---

## 7. Errata that must be absorbed into this chapter

From extension notes Part IV, Chapter 4 items (each mapped to the plan):

| # | Issue | Handled in |
|---|---|---|
| 4.1 | §9's p = ⟨X⟩_QS dimensionally wrong | 4.9 (motivation) + 4.10–11 (replacement) |
| 4.2 | QS-mean formula missing; μ=0 subtlety | 4.4 (⟨X⟩_QS = a/(a−1); V∞ equal only when μ=0) |
| 4.3 | Two candidate integrals unresolved | 4.9 (both fail for stated reasons) |
| 4.4 | N₀V(t) only for synchronous infection | 4.9 |
| 4.5 | "Iterating cycles" stops in words | 4.10 (formalized as renewal) |
| 4.6 | R vs H; I double-meaning | §3 notation decisions |
| 4.7 | `\Vt` macro broken | §3 (fix macros) |
| 4.8 | §7 awaiting Gillespie verification | 4.5 (analytic proof replaces it) |
| 4.9 | Antiderivative duplicated/n↔k | 4.5 cleanup |
| 4.10 | §6's open F(t) question | 4.4 (F = 1 − Î) |
| 4.11 | QSD never identified | 4.4 headline result |
| 4.12–13 | Garbled sentence; caption "yellow" twice | 4.4 |
| 4.14 | §8 circularity + "(check)" | 4.6 |
| 4.15–16 | Defective PGF unstated; "PDF", typos | 4.3 |
| 4.17 | Empty `01_opening.tex` | 4.1 |
| 4.18 | Stale Ch.3 duplicate in this folder | housekeeping: archive/delete `3 BDC core/` here |

**New corrections from the N=2 completion (this plan's own findings):**
- Draft's general coefficient (1/k!)(n+k−1)!/(n−1)! is C(n+k−1, k) — contradicts its own r₂/r₃ cases; correct is C(n+k−2, k−1). Fixed and verified.
- Draft's unverified r₂ formula: the *pattern* it extrapolated is correct (verified for k ≤ 4); the draft's hedging can now be replaced by the iid-geometric proof.
- Draft's closing guess for ρ(t₂): confirmed equivalent to the Laplace decomposition now implemented.

**Cross-chapter dependencies (Ch.3 must eventually agree):** corrected Î (3.1), Î_k = I^k − D^k (3.2), 𝔼[W²] signs (3.3), K(I) form (3.4), duplicated sections 08/10 and 09/11 (3.5), λ→β / Y→W / H→R unification (3.6). Plan: Ch.4 restates the corrected forms self-contained with brief remarks; apply the Ch.3 fixes as a separate workstream so both chapters agree at submission. Ch.1 infection terms (1.1–1.2) and notation collisions (1.3–1.4) are blocking-level for joining the models — resolve before final assembly.

---

## 8. Build and verification steps

1. Update `document MAIN/main.tex`: new macros (§3), title/date, added section files, appendix machinery.
2. Rewrite/create section files in place (`01_…`–`09_…`), then add `10_`–`15_` + appendix files, keeping the numbered-file convention.
3. Extend `references.bib` (~20 entries).
4. Regenerate figures: `python3 figures/plot_bmvr_comparison.py`; `python3 new_notes3/verify_result_20_1.py` (confirms 53/53; refreshes report/figures); `python3 "N=2 Immediate Transfer content/verify_chained_transfer.py"` (confirms the chained-transfer checks; refreshes its report/figures). Copy/link figure folders into `document MAIN/figures/`.
5. New figure scripts (§5 table) — extend `plot_bmvr_comparison.py` or sibling scripts in `figures/`.
6. Compile `latexmk -pdf main.tex` (unsrt bibliography; expect 2 passes for cleveref).
7. QA pass: every boxed formula in the master formula tables appears in the chapter; all [CORRECTED] items carry a remark; no "need to", "(check)", "perhaps" left in body text; all verification tallies quoted from the actual reports.

---

## 9. Suggested writing order

1. **Phase 0 — scaffolding: DONE (2026-08-07).** `main.tex` restructured (17 sections + 3 appendices), canonical macros added (`\Ihat`, `\Kb`, `\Icell`, `\Vfree`, `\Lap`, `\Prob`, `\E`, `\Fhyp`, `\todo`; `\Vt` fixed), notation table in file 02, bib extended 1 → 19 entries. Section files: new skeletons 01, 02, 09–17, A/B/C with verified anchor formulas and `\todo` markers; old 03–08 compile unchanged; old 09 content relocated verbatim to 11; old 01/02/09 files remain on disk but are no longer `\input`. Clean compile (30 pp, no undefined refs). Next: Phase 1.
2. **Phase 1 — single-cell part: DONE (2026-08-07).** Files 02 (recap with corrected boxed anchors + notation table), 03 (PGF PDEs: typo/`\pdx` fixes, defective-PGF caveat), 04 (+ k-founder PGF subsection), 05 (+ geometric-at-every-time, Σp_n = Î check), 06 (+ F = 1−Î, QSD = geometric(1/a) theorem, moments, caption fixes, mean productive lifetime with proof), 07 (burst time φ = δJ; analytic proof of burst law; burst=QSD corollary; size-biasing), 08 (circularity resolved). All new identities numerically re-verified 2026-08-07. Clean compile (35 pp).
3. **Phase 2 — multi-cell: DONE (2026-08-07).** File 09 (MOI: I_k/D_k/Î_k with the failed-guess remark and numeric contrast; PGF derivation of J_k, K_k; g_k with the free-sum correction 22.264 vs 23.39; V∞^(k) integral formula + μ=0 elementary derivation k+β/δ; conditional mean burst increasing in k — all numbers re-verified) and file 10 (chained transfer: full prose around the verified laws — event-type decomposition, rupture sizes with corrected coefficient and induction via hockey-stick, rupture times incl. μ>0 companion forms, interval transforms with ₂F₁ closed form (verified to 1.4e-15 against the defining series), t₂ resolution of the draft's open question, verification record 28/28, open scope). Clean compile (37 pp).
4. **Phase 3 — population core: DONE (2026-08-07).** File 11 rewritten as the diagnosis (classical BMVR comparator with correct γT𝓥 term; synchronous cohort; the failed p = ⟨X⟩_QS proposal with dimensional obstruction and both failed candidate integrals; "what the attempt got right" bridge). File 12: kernels, boxed renewal Result with replacement table, novelty remark, verification subsection (figures D + Gillespie H pair), overlay subsection with all five overlay figures and reading guide. File 13: exact exponential-phase reduction derivation, p_eff/d_eff with limits and the (1,0,0.1) example 4.59 → 0.1, NEW figure `peff_dr_curves.pdf` (script `figures/plot_peff_curves.py`), characteristic equation + R₀ invariance theorem with the two-R₀ caution (figures E, F), identifiability negative result, fitting prediction. File 14: offspring PGF derivation, extinction closed form, matched-mean budding comparator, flooding theorem with proof sketch + exact numeric table, L=1 proposition with full geometric-law proof and variance-ordering identity Var_bud − Var_burst = 2q²V∞(L−1)/(a−1), growth-rate trade-off with verified table (c=1, R₀=2: 0.250/0.180, 0.395/0.294, 0.343/0.198), scope remark. All cited numbers re-verified 2026-08-07 (flooding identity exact in 5 cases; L=1 geometric to 1e-16; trade-off in 3 regimes). Both figure suites regenerated fresh (53-check renewal suite: 0 FAIL; overlays). Figures copied into `document MAIN/figures/`. Clean compile, 45 pp, no overfulls.
5. **Phase 4 — spectrum and HIV (full detail): DONE (2026-08-07).** File 15: universal skeleton with the 6-model (S,g) table; Cases 1–5 complete (equations, R₀'s, quasi-steady limits, composability, summary table); reset catastrophe (process, kernels, p_eff, mature limit p∞ = δ𝔼_π[X²], comparison table, optional eclipse); self-excitation (12-model menu, nesting, focal Models 7/6/10/2 with equations, 4-way comparison, confidence ranking); boolean partial release (options A–G, nested limits, mean-field Case-4-scaled-by-q ODEs, visibility analysis, recommendation). File 16: Hataye findings in full (initial release 6 points, establishment 4 points), supported/not-supported + 7-axis biological distinction tables, candidate stage equations (two pathways, Erlang eclipse, division/death in eclipse, Allee incidence, renewal kernels S_HIV/g_HIV, effective parameters by substitution), what-to-keep/not-claim, linear-vs-exponential growth analysis with confidence grades and model ranking, suggested role. Notation collisions fixed vs sources (eclipse rate α, telegraph σ_on/σ_off, eclipse division ρ_div, latent class L₀). Clean compile, 52 pp. Remaining for Phase 5/6: two optional TikZ figures (spectrum map, HIV stage diagram) still on the to-create list.
6. **Phase 5 — framing: DONE (2026-08-07).** File 01 (full chapter introduction: motivation, four research questions, one-page story, chapter map; killing/catastrophe subsection with typos fixed; label sec:pgf-pdes added to file 03). File 17 (discussion: five assay predictions, fitting-practice consequences, forward connections to Ch. 5/6/7, seven numbered open problems). Appendix A (single-cell + population master formula tables with corr./new tags, quick-reference specialisations). Appendix B (renewal suite catalogue — actual tally 54/54 on the 2026-08-07 run, noted against the older "53" summaries, §12.3 updated to match; chained suite 28/28; reproduction blocks). Appendix C (hypergeometric transforms with the convergence caveat — verified against quadrature; V∞^(k) derivation via x=I substitution, incl. μ=0 recovery; PGF coefficient-extraction route for general-μ chained laws). First complete draft: 58 pp, 0 undefined refs, 0 overfulls, 0 remaining todos.
7. **Phase 6 — QA: DONE (2026-08-08).** Errata sign-off below; sweeps clean (0 errors, 0 undefined refs, 0 overfulls, 0 todos, no bibtex warnings); 59 pp.

**Errata checklist (Ch.4 items, all resolved in the drafted chapter):**
4.1 p = ⟨X⟩_QS irreparable → §11.3 diagnosis + §12 replacement ✓ · 4.2 QS-mean formula + μ=0 subtlety → §6 theorem + coincidence remark ✓ · 4.3 candidate integrals → §11.3 ✓ · 4.4 N₀V(t) synchrony → §11.2 ✓ · 4.5 iterating cycles → §11.4→§12 ✓ · 4.6 R/H and I collisions → §2 canonical notation ✓ · 4.7 \Vt macro → fixed (now unused) ✓ · 4.8 Gillespie goal → analytic proof, §7 ✓ · 4.9 duplicated antiderivative → §7 ✓ · 4.10 F(t) question → §6.1 ✓ · 4.11 QSD never identified → §6.2 theorem ✓ · 4.12 garbled sentence → §6 ✓ · 4.13 double-yellow caption → §6 ✓ · 4.14 circularity + "(check)" → §8 ✓ · 4.15 defective PGF + typos → §3 ✓ · 4.17 empty opening → §1 full introduction ✓ · 4.18 stale `3 BDC core/` duplicate folder inside this folder → **left on disk; delete/archive is the user's call**.

**New issues found and resolved during drafting:** N_eq_2 closed form off by one shift (corrected C(n+k−2,k−1), §10 remark); renewal suite actually runs 54 checks (aligned §12.3 + App. B); ₂F₁ transform series diverges when δ < β−μ (convergent branch + caveat in App. C, verified vs quadrature); BMVR attribution citations added to §11.1, Pearson/Gilchrist–Coombs citations added to §17. Two TikZ figures created (spectrum map §15, HIV stage diagram §16).

**Still open (flagged, not blocking):** TODO(verify) bib entries (mclean1993balance, nowak1996population, mckendrick1926applications, vonfoerster1959some, gaver1965observations; Heffernan–Wahl and Nelson–Gilchrist–Perelson have no entries yet — prose mentions only); cross-chapter errata (Ch.1/3/5/6) live in `new_notes` Part IV and belong to those chapters' folders.

---

## 10. Remaining open items (flagged in-chapter, not blocking)

- Conceptual proof of QSD = burst size (algebra done; structural argument open).
- Two-type killed second moments + two-type D (blocks the eclipse-aware renewal BMVR from Ch.5).
- General-μ chained-transfer joint laws (Appendix C machinery is the route).
- Flooding boundary mapped against real pathogen parameters; population-level variance propagation; partial-release flooding boundary in φ; logistic intracellular growth sensitivity.
- Literature positioning checks (esp. whether Carruthers et al. already couple BDC to a between-cell model — novelty claim depends on it).
