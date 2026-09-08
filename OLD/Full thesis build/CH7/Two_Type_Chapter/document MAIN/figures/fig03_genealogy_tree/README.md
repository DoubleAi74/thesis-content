# Figure 3: two-type genealogy realisation with catastrophe

This directory contains a computationally simulated continuous-time
birth--death--conversion genealogy truncated by a global catastrophe. The main
panel is not AI-generated.

## Regenerate

From the paper project root:

```bash
python3 figures/fig03_genealogy_tree/src/simulate_tree.py
```

The command writes `fig03.png`, `fig03.pdf`, and `meta.json`. It requires Python 3 with NumPy and Matplotlib.

To rerun the same algorithm with another seed:

```bash
SEED=3624 python3 figures/fig03_genealogy_tree/src/simulate_tree.py
```

The horizon and catastrophe weights can be changed explicitly:

```bash
python3 figures/fig03_genealogy_tree/src/simulate_tree.py --seed 2869 --horizon 9
python3 figures/fig03_genealogy_tree/src/simulate_tree.py --delta1 0.05 --delta2 0.08
```

To draw a pure genealogy without catastrophe (\(\delta_1=\delta_2=0\)):

```bash
python3 figures/fig03_genealogy_tree/src/simulate_tree.py --no-catastrophe --seed 57
```

To inspect candidate seeds without rendering figures:

```bash
python3 figures/fig03_genealogy_tree/src/simulate_tree.py --scan 35 120 --horizon 9
```

Seed **2869** is the fixed default used for the delivered figure. Catastrophe
fires at \(t\approx5.75\), ending 25 extant lineages (with both types still
present among the broader tree history).

## Simulation semantics

- Type 1 gives birth at rate \(\lambda_1=1.0\), dies at rate \(\mu_1=0.55\), and converts irreversibly at rate \(\nu=0.40\).
- Type 2 gives birth at rate \(\lambda_2=0.90\) and dies at rate \(\mu_2=0.50\).
- Global catastrophe fires at rate \(\delta_1 X_t+\delta_2 Y_t\) with \(\delta_1=0.05\), \(\delta_2=0.08\); when it fires, every extant lineage ends at that instant (red vertical wavefront).
- At a birth, the event tree has two child edges: the parent's continuation and the newborn lineage. Conversion has one continuing type-2 edge. Death, the time horizon, and catastrophe are terminal events.
- The horizontal coordinate is the exact event time. Vertical coordinates are assigned retrospectively from descendant leaf order and carry no quantitative meaning.
- The x-axis still runs to the fixed horizon \(T=9\), so the empty region after the catastrophe line shows early absorption.

The script validates event chronology, child counts, simultaneous catastrophe
times, and the absence of type-2 to type-1 reversals before rendering. The run
metadata also checks the binary-tree identities `leaves = births + 1` and
`leaves = deaths + alive_at_horizon + killed_by_catastrophe`.
