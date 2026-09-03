# Chapter 5 — figure work-order

Phase A. Plan §11. Seventeen floats in the source; four cut, one built, one
regenerated single-panel, twelve re-placed with captions rewritten. **Fourteen
figures ship**, and every one is called out by `\cref` at the sentence it
supports. In the source, one of seventeen was referenced and every other
`fig:` label was dead.

---

## 1. Cut, and what carries the content

| Figure | Files | Why cut | Carried by |
|---|---|---|---|
| `N4a_1_pgf_characteristics` | `N4a_1_pgf_characteristics.pdf` | A consequence of the plan §9 deferral, not a defect in the figure. Once §3 defers the generic method of characteristics to \ChM, there is nothing local for it to support. | `m:fig:characteristics` in `CH2/sections/04_method_of_characteristics.tex` (verified to resolve) |
| QS pair | `QS1.png`, `QS2.png` | 72 dpi rasters (539×416 and 462×422 px) in a chapter that is otherwise vector; no axis labels; no legend though four curves are drawn in each panel while the caption describes three; parameters unstated; panel (b)'s x-axis truncated mid-label; the caption identifies a curve as "shown in red" with no legend to read it against. | `dist:fig:qsmeans` (`N4a_6`) and panel (b) of `dist:fig:lifetime` (`N4a_2`). The orphaned prose at source `06:157–163`, which had drifted two figures from its subject while still saying "the left above", is folded into the `dist:fig:qsmeans` caption with the deictics removed. |
| `F4a_3_qsd_convergence` | `F4a_3_qsd_convergence.pdf` | **Absorbed, not deleted.** It did half the job of the new figure. | Panel (a) of `dist:fig:two-mechanisms` |
| `N4a_7_moi_flux_ratios` | `N4a_7_moi_flux_ratios.pdf` | Duplicates panel (a) of `F4a_6_moi` (plan §11.2, "consolidate one"). §9 carried three figures for three subsections; two suffice. | Panel (a) of `dist:fig:moi` (`F4a_6_moi`) |
| `F4a_6_FAILED.pdf` | — | Build artefact. An asset named "FAILED" should not ship in a thesis directory (plan §10 item 1). | nothing; it was never referenced |

Cut files were not copied into `CH5_REWRITE/figures/`; they remain in
`Chapter numbers/CH5/figures/`, which is read-only for this pass.

---

## 2. Built

### `figures/fig01_two_mechanisms/` → `dist:fig:two-mechanisms`

The chapter's signature image, and the one major result that previously had no
figure at all. Two panels, one law:

- **(a)** the conditional load pmf $p_n(t)/I_{\rm fix}(t)$ at $t=1,5,20$,
  rising to the geometric quasi-stationary law — a limit along a single
  trajectory;
- **(b)** the burst-size law and its renormalisation on the bursting event,
  which lands on the *identical* dashed line without any limit being taken —
  an average across trajectories.

The two panels are the union of the cut `F4a_3` and panel (a) of `F4a_5`,
overlaid on a shared logarithmic axis so that "the same law" reads as "the
same straight line". Sources: `dist:eq:stateprob`, `dist:eq:idihat`,
`dist:eq:burstlaw`, `dist:eq:burstlawcond`. No simulation.

Assertions run before export (all pass): $b<1<a$; $ab=\mu/\lambda$;
$(a-1)(1-b)=\delta/\lambda$; the conditional pmf equals $(1-P(t))P(t)^{n-1}$
to $2\times10^{-13}$; sup-norm distance to the limit decreases in $t$
($0.3495$, $0.0099$, $0.0000$ at $t=1,5,20$); the conditional burst law equals
the limit *exactly*; the unconditional law sums to $1-b$ to $10^{-10}$.

Deliverables in the folder: `fig01.pdf`, `fig01.png`, `README.md`,
`caption.md`, `meta.json`, `src/generate.py`.

### `figures/fig02_late_burst_mean/` → `dist:fig:latemean`

`F4a_5_burst_size_late` regenerated **single-panel**. Its panel (a) is now
`fig01`'s panel (b); only panel (b), the size-biased conditional mean
$K(t)/J(t)$, survives, unchanged in content. The regenerated version adds the
quasi-stationary mean $a/(a-1)=17.23$ as a second reference line, so that the
size-biasing factor $(a+1)/a=1.94$ is legible in the figure rather than only
in the text — which is what plan §4.6's correction to source `07:341` needs.

Assertions (all pass): asymptote $=33.4642$ and QS mean $=17.2321$ to
$5\times10^{-4}$; curve starts at exactly $1$; strictly increasing on the grid;
reaches the asymptote to $10^{-9}$ by $t=400$.

`F4a_5_burst_size_late.pdf` was deleted from `CH5_REWRITE/figures/` after
regeneration, so the superseded two-panel version does not ship.

---

## 3. Re-placed only (captions rewritten, files untouched)

Per plan §11.1 and §18, figures that are merely re-placed are not re-foldered
and their PDFs are byte-identical copies of the source chapter's.

| New label | File | New home |
|---|---|---|
| `dist:fig:joint` | `F4a_1_joint_process.pdf` | §2, the process and its release counter |
| `dist:fig:slide` | `F4a_2_geometric_slide.pdf` | §4, the sliding ratio |
| `dist:fig:qsmeans` | `N4a_6_qs_vs_release_means.pdf` | §5, the limit is geometric |
| `dist:fig:lifetime` | `N4a_2_productive_lifetime.pdf` | §5, mean productive lifetime |
| `dist:fig:jointtauk` | `N4a_5_joint_tau_K.pdf` | §6, size-biasing |
| `dist:fig:bursttime` | `F4a_4_burst_time_density.pdf` | §7, the marginal law and its defect |
| `dist:fig:taugivenk` | `F4a_8_tau_given_k.pdf` | §7, burst time given burst size |
| `dist:fig:threemeans` | `N4a_4_three_burst_means.pdf` | §8, the apparent circularity |
| `dist:fig:moi` | `F4a_6_moi.pdf` | §9, moments and the release kernel |
| `dist:fig:subextensive` | `N4a_8_yield_subextensive.pdf` | §9, lifetime yield |
| `dist:fig:chained` | `F4a_7_chained_transfer.pdf` | §10, rupture-size laws |
| `dist:fig:budding` | `N4a_3_burst_vs_budding_pmf.pdf` | §11, bursting against budding |

Every caption now states its parameters and says what to look at. All floats
are `[tbp]`; the source's nineteen `[H]` placements are gone, and with them
the third of a blank page at source page 16 and the figures that opened source
pages 17 and 31 before any prose.

---

## 4. What could not be rebuilt, and the style shim

**The upstream figure style module is missing.** Every `generate.py` under
`Chapter numbers/CH5/figures/_work/<FIG>/` opens with

```python
STYLE_DIR = Path("/Users/adamaldridge/Desktop/Thesis content 🎓 /"
                 "4 BDC additional and BMVR/Figures run/style")
sys.path.insert(0, str(STYLE_DIR)); import style_rc
```

and that directory does not exist on this machine. `find ~/Desktop -name
style_rc.py` returns nothing. **Consequence: none of the twelve re-placed
figures can be regenerated as things stand.** They ship as the PDFs the source
chapter already contains, which is what plan §11.1 asks for, but the
regeneration path in those scripts is broken and will stay broken until the
style module is restored or replaced.

**What I did instead of restoring it.** `figures/_style/style_rc.py` is a new,
self-contained replacement providing the two entry points those scripts use,
`apply()` and `save_figure(fig, pdf_path, png_path)`. It is written to the
`SHARED_CONVENTIONS.md` palette that plan §11.3 specifies — `#0072B2` blue,
`#D55E00` vermillion, `#1a1c1f` ink, `#565b62` soft ink, line style preferred
over extra hues — rather than to the matplotlib `tab:` defaults the older
scripts used.

**Author action, one of two.** Either (a) restore the original `style_rc.py`
and repoint the `_work` scripts at it, or (b) repoint them at
`figures/_style/style_rc.py` and regenerate the twelve, accepting a palette
shift from `tab:blue`/`tab:orange` to the conventions palette. Until one of
those happens the chapter is in a **mixed palette**: `fig01` and `fig02` use
the conventions palette, the other twelve use matplotlib defaults. The
difference is mild — `#1f77b4` against `#0072B2`, `#ff7f0e` against `#D55E00`
— and legible in print, but it is a real inconsistency and it is deliberate
rather than accidental: regenerating twelve figures under a shim I wrote
myself would have been a larger and less reversible change than leaving them.

**Not attempted.** `verify_chained_transfer_figures.pdf` was copied into
`verification/` alongside the suite and its report; the suite was not re-run
(plan §18 — author action).

---

## 5. Provenance of the numbers in captions

Every numeric value appearing in a caption is in `CH5_invariants.md` under a
`NUM-*` entry and was recomputed by `verification/recheck_numbers.py`: $b=0.188$,
$a=1.0616$, $1-b=0.812$, $17.23$, $33.46$, $(a+1)/a=1.94$, $21$, $2.847$,
$0.351$, $13.99$, $27.97$, $17.43$, $0.055$, $\theta=1.1$, $d_{\Icell}+p=8$,
seed 42, $10^6$ chains. Forty-two quoted values, zero mismatches.
