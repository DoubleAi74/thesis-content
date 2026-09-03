# Chapter figures

Run `python3 generate_chapter_figures.py` from this directory to regenerate the
five vector PDF figures used by `main.tex`.  The tested package versions are
recorded in `requirements.txt`; install them with
`python3 -m pip install -r requirements.txt` if an isolated figure environment
is required.  The script selects Matplotlib's non-interactive `Agg` backend and
a temporary writable configuration directory, so it is safe to run in a
headless build environment.

The Galton--Watson plots evaluate the exact recurrence

`S[n+1] = 2*p*S[n] - p*S[n]**2`.

The Kolmogorov constant uses its exact infinite product and stops only when a
bound on the omitted logarithmic tail is below tolerance. The figures do not
use the exploratory genetic-regression fits or Monte Carlo data elsewhere in
the workspace.
