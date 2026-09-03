# Mathematical-background chapter

The chapter is assembled from `main.tex`; its four source sections are in
`sections/`, and the bibliography is in `references.bib`.

To regenerate the vector figures and compile the PDF:

```sh
python3 figures/generate_chapter_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The figure script requires Python 3, NumPy, and Matplotlib.  The document build
requires a LaTeX distribution providing `latexmk`, pdfLaTeX, and the packages
loaded by `main.tex`.  Run `latexmk -C main.tex` to remove LaTeX build products;
the generated figure PDFs are source-controlled outputs and are not removed by
that command.
