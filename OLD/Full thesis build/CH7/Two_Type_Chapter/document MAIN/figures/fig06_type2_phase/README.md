# fig06_type2_phase — Type-2 roots and phase line

Supports **§3, "The autonomous type-2 probability"** (`sections/03_autonomous.tex`).
Makes the autonomous Riccati geometry obvious: the equilibria
\(r_{2,-}<1<r_{2,+}\), the flow on \([0,1]\) toward the stable root
\(r_{2,-}\), and the reading of \(r_{2,-}=\lim_{t\to\infty}G(t)\) as the
probability that catastrophe is avoided forever.

## Panels

- **(a)** The right-hand side \(f(G)=\lambda_2 G^2-(\lambda_2+\mu_2+\delta_2)G+\mu_2\)
  vs \(G\), with both roots as filled markers, the factored form in the title,
  the endpoint witnesses \(f(0)=\mu_2>0\) and \(f(1)=-\delta_2<0\) (the
  root-ordering argument), and the admissible band \([0,1]\) shaded.
- **(b)** The phase line of \(\dot G=f(G)\) on the same \(G\) axis (shared with
  panel a, so zeros sit above equilibria): flow arrows, the **stable** root
  \(r_{2,-}\) (filled) and the **repelling** root \(r_{2,+}\) (open), and the
  initial value \(G(0)=1\) sliding left into \(r_{2,-}\).
- **(c)** Physical-time relaxation \(G(t):1\to r_{2,-}\): closed form (line) vs
  an independent RK4 integration (markers), with the limit line annotated as
  \(r_{2,-}=\lim_{t\to\infty}G(t)=\mathbb P(\text{avoid catastrophe forever})\).

## Parameters

| Symbol | Value | Role |
|---|---|---|
| \(\lambda_2\) | 0.90 | type-2 birth rate |
| \(\mu_2\) | 0.35 | type-2 death rate |
| \(\delta_2\) | 0.20 | type-2 catastrophe hazard |
| \(\lambda_1\) | 1.0 | time unit (type-2 picture is \(\lambda_1\)-independent) |

Chosen for a clear root gap. Derived: \(r_{2,-}=0.295623\),
\(r_{2,+}=1.315488\), \(\alpha_2=1.019864\), \(\hat\Delta_2=0.917878\).
No random seed is used (the figure is fully deterministic).

## Regenerate

From this directory:

```bash
/opt/homebrew/bin/python3.14 src/generate_fig06.py
```

Any Python ≥ 3.9 with `numpy` and `matplotlib` works; the script has no other
dependencies (RK4 is hand-rolled, so `scipy` is **not** required). It writes
`fig06.png` (3660×1650 px, 300 dpi), `fig06.pdf` (vector), and `meta.json`.
The script asserts the root ordering \(0\le r_{2,-}<1<r_{2,+}\), the three
closed-form checks \(G(0)=1\), \(G'(0)=-\delta_2\), \(G(\infty)=r_{2,-}\), and
that the closed form agrees with RK4 to \(<10^{-5}\) (achieved:
\(1.2\times10^{-15}\)); it exits non-zero if any check fails.

To explore other rates, edit the `lam2, mu2, del2` line near the top of the
script. Any admissible choice (\(\lambda_2,\delta_2>0\)) automatically satisfies
\(0\le r_{2,-}<1<r_{2,+}\); the assertions guard this.

## Files

```
fig06_type2_phase/
  fig06.png              # primary deliverable (full-width, 300 dpi)
  fig06.pdf              # vector version
  caption.md             # journal-style caption + parameters + method
  README.md              # this file
  meta.json              # machine-readable parameters / derived values / max error
  src/generate_fig06.py  # generation script (numpy + matplotlib only)
```

## Notes

- Colours follow the paper palette (Okabe–Ito, colour-blind safe): vermillion
  `#D55E00` for the type-2 emphasis, near-black ink, soft-grey annotations, and
  a green `#2e7d32` accent for the validated infinite-time limit.
- Typography uses a serif body (DejaVu Serif) with Computer-Modern mathtext to
  match the paper and the Galton–Watson chapter style.
- Stability convention: **filled** marker = stable equilibrium, **open** marker
  = repelling equilibrium.
