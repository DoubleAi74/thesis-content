# Chapter M Pass 2 outline

This file records the implemented Pass 2 structure and the Pass 1 donors. The
five files named below are the only chapter inputs in `main.tex`. The eight
retained Pass 1 donor files have been moved to `sections_pass1/`, so every file
left in `sections/` is compiled and no donor is silently orphaned.

## 1. Overview

- File: `sections/01_overview.tex`
- Donors: Pass 1 `01_introduction.tex` and `07_synthesis.tex`

## 2. Markov Chains

- File: `sections/02_markov_chains.tex`
- 2.1 Discrete-Time Markov Chains
  - Simple random walks: explicit source-gap stub
  - Galton-Watson processes: compressed from Pass 1 `03_galton_watson.tex`
  - Critical survival, extinction-time mass, Catalan total progeny, small-founder
    effects and rupture bridge: summarised here and proved in Appendix B
- 2.2 Continuous-Time Markov Chains
  - Exponential-clock and generator setup: Pass 1 `02_preliminaries.tex`
  - Poisson processes: explicit source-gap stub; only the supported
    exponential-clock connection is retained
  - Birth-death and birth-death-catastrophe definitions: Pass 1
    `02_preliminaries.tex` and `05_small_populations.tex`
- 2.3 Time-Inhomogeneous Processes
  - Logistic speciation model: explicit source-gap stub
- 2.4 Coupled ODE-CTMC Systems
  - Explicit source-gap stub

## 3. Methods for Markov Chains

- File: `sections/03_methods.tex`
- 3.1 Discrete-Time Methods
  - PGFs, iteration and first-step analysis: Pass 1 `02_preliminaries.tex` and
    `03_galton_watson.tex`
  - Light definition of discrete `A(p)` and forward reference to Chapter A:
    Pass 1 `04_conditioning.tex`
- 3.2 Continuous-Time Methods
  - Forward/backward equations, moments, hitting and extinction probabilities:
    Pass 1 `02_preliminaries.tex`
  - Conditional means and detailed `A_c(p)` derivation: Pass 1
    `05_small_populations.tex`
  - Killed-semigroup conditioning and method-selection summary: Pass 1
    `04_conditioning.tex` and Codex CTMC/BDC upgrades
- 3.3 Method of Characteristics
  - Accessible absorption-death worked example: compressed from Pass 1
    `06_method_of_characteristics.tex`

## Appendices

- File: `sections/04_extended_absorption.tex`
- Further absorption-only and absorption-birth-death models, parameter-regular
  formula and coefficient extraction: compressed from Pass 1
  `06_method_of_characteristics.tex` and `08_appendices.tex`
- File: `sections/05_branching_details.tex`
- Critical Galton--Watson proof, Catalan law, limiting conditional variance,
  early survival, founder-cohort effects, push of the past, and discrete rupture
  with Jensen bound: Pass 1 `03_galton_watson.tex`, `04_conditioning.tex` and
  `05_small_populations.tex`, strengthened from `7source_codex_1` where noted in
  the merge log

The deep product, series, bounds, Koenigs, hypertranscendence and PSLQ theory of
the discrete constant remains exclusively in Chapter A.
