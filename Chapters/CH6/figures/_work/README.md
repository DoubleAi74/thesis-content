# Figure sources

Every figure in `figures/` is regenerated from here. Recovered and rebuilt in
Phase C; see `../../CH6_PHASE_C_REPORT.md` §4.

## Shared

| file | purpose |
|---|---|
| `../_style/style_rc.py` | house palette and typography (copied from the two-type chapter) and `panel_label()` |
| `../_style/tikz_style.tex` | shared TikZ conventions for the three standalone diagrams |
| `_renewal.py` | the renewal / classical BMVR solver used by the overlay figures |
| `_renewal_check.py` | validates `_renewal.py` against the chapter's published values — run it before trusting any overlay |
| `_scenarios.py` | the six overlay scenarios |
| `_migrate.py` | Phase C migration helpers (title stripping, palette and age-variable maps) |

## Per figure

`N4b.*`, `F4b.2`, `F4b.3` — `python3 <dir>/generate.py`
`F4b.1`, `N4b.3`, `NX.1`  — `pdflatex figure.tex`, then copy `figure.pdf` across
`OVL_*`, `PEFF`          — `python3 <dir>/generate.py`
`D`, `E`, `F`, `H`       — written by `../../verification/verify_result_20_1.py`

`N4b.3` is not used by the chapter: §6 carries an inline TikZ spectrum instead.
Its source is kept live so it compiles.

## Rebuild everything

```sh
for d in N4b.1 N4b.2 N4b.4 N4b.5 N4b.6 N4b.7 F4b.2 F4b.3 PEFF \
         OVL_MAIN OVL_RELDIFF OVL_GROWTH OVL_NAIVE; do
  (cd "$d" && python3 generate.py)
done
for d in F4b.1 NX.1; do
  (cd "$d" && pdflatex -interaction=nonstopmode figure.tex >/dev/null \
     && cp figure.pdf "../../$(sed -n 's/.*\/\([A-Za-z0-9_]*\)\.pdf/\1/p' <<<"$d")")
done
(cd ../../verification && python3 verify_result_20_1.py && cp verify_figures/*.pdf ../figures/)
```
