# Chapter 2 — Mathematical introduction

This directory is a self-contained, pdfLaTeX-compatible build of Chapter 2. The
source remains modular: each numbered section and each chapter-local appendix is a
separate file included by **main.tex**.

## Build

From this directory:

~~~sh
sh scripts/run_checks.sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
~~~

The build uses only standard TeX Live packages and Python's standard library.
**scripts/reproduce_numerics.py** regenerates
**figures/conditional_means.csv**; the other scripts perform exact-algebra,
coefficient, and master-equation checks.

The resulting PDF is **main.pdf**. To integrate the chapter into a thesis, retain
the section and appendix inputs, move the preamble macros into the thesis preamble,
and include the files after setting the thesis chapter counter in the usual way.

## File map

- **main.tex** — standalone wrapper and integration point
- **sections/** — main chapter spine
- **appendices/** — chapter-local appendices, numbered 2.A–2.C
- **references.bib** — chapter bibliography
- **figures/** — required source figures and generated plot data
- **scripts/** — reproducibility and verification scripts
- **ch2_outline.md** — outline, source audit, and correction record

