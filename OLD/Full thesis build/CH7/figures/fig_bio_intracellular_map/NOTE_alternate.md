# Alternate figure for §5.1 — comparison and swap-in

Two figures were built for the same slot (the mapping schematic that
accompanies Table 1, `tab:bio-mapping`, in §5.1):

| | `fig_bio_mapping` | `fig_bio_intracellular_map` |
|---|---|---|
| Status | **currently in `sections/07_biological_application.tex`** | alternate, not included |
| Build | TikZ + pdflatex | TikZ + pdflatex (same convention) |
| Outputs | PDF / PNG / SVG | PDF / PNG / SVG |
| Palette | Okabe–Ito, manuscript standard | same, plus lowered-chroma body tints |

Both satisfy the scientific caveats of §5.1: coarse-grained type 2, `δᵢ` as
effective associations rather than active rupture, no privileged regime, no
T3SS-as-survival-engine claim, extracellular phase marked out of model.

## Where they differ

**Compartment.** `fig_bio_mapping` draws one shared dashed vacuole containing
both populations. `fig_bio_intracellular_map` draws two vacuolar outlines with
the right-hand one labelled "same compartment", which keeps the left-to-right
sequence more readable at the cost of one extra outline.

**Bacterial morphology.** `fig_bio_mapping` uses flat ellipses.
`fig_bio_intracellular_map` uses round-capped rods (coccobacillary, ~2.4:1),
with a faint halo and sparse surface hairlines on type 2 only.

**Death events.** `fig_bio_mapping` uses bare downward arrows labelled `μᵢ`.
`fig_bio_intracellular_map` reuses Figure 1's grammar — a self-loop for birth
and an arrow into `∅` for ordinary death — with the words "replication" and
"loss" underneath, so the mapping to the mathematics is explicit.

**Extracellular phase.** In `fig_bio_mapping` this is two very pale ellipses at
the far right plus a caption line; it is easy to miss. In
`fig_bio_intracellular_map` it is a dashed panel with seven pale rods and the
label "extracellular phase / outside this model".

**Key.** `fig_bio_mapping` has a bottom-left key block, leaving the bottom-right
quadrant empty. `fig_bio_intracellular_map` uses a full-width four-column strip
with a separate italic caveat line stating that arrow weights are equal and no
ordering of `δ₁, δ₂` is assumed.

**Greyscale.** `fig_bio_intracellular_map` deliberately makes type 1 lighter
than type 2 and adds texture to type 2, so the states separate by lightness and
shape as well as hue. Verified with `gs -sDEVICE=pnggray`.

**Aspect and page cost.** `fig_bio_mapping` is 1.45:1 (≈4.5 in tall at full
text width). `fig_bio_intracellular_map` is 1.74:1 (≈3.7 in tall at full text
width), so it costs less vertical space if included at `\textwidth`.

## To swap this one in

In `sections/07_biological_application.tex`, in the figure environment that
currently loads `figures/fig_bio_mapping/fig_bio_mapping.png`:

1. Replace the `\includegraphics` line with

   ```latex
   \includegraphics[width=\textwidth]{figures/fig_bio_intracellular_map/fig_bio_intracellular_map.pdf}
   ```

   Use the PDF, not the PNG — it is vector and tight-cropped. This figure is
   designed for the full `\textwidth`; scaling it down below about
   `0.85\textwidth` pushes the tertiary labels under 7 pt.

2. Take the caption from [`caption.md`](caption.md) (a shorter variant is
   provided there if the float is tight).

3. Keep whatever `\label{...}` the slot ends up using. Every cross-reference in
   the manuscript goes through `\cref`, so figure numbering updates itself on
   recompile; nothing needs renumbering by hand. Note that inserting any figure
   here shifts `fig:bio-regimes` from 10 to 11 and the appendix figures
   accordingly, again automatically.

4. If the caption refers to the four regimes by cross-reference rather than by
   name, add `\label{sec:regimes}` under
   `\subsection{Four catastrophe-rate regimes}` first — that label does not
   currently exist.

Nothing in `figures/fig_bio_mapping/` needs to be deleted; leaving both
directories in place costs about 800 kB.
