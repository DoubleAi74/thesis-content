# Figure selection checklist

One row per candidate group. Write the candidate filename you want promoted
to production after `keep:`, and the rest after `drop:` (`all` and `none` are
fine). Nothing here is read by the build; it is a worksheet.

When the sheet is filled in, a later pass rewires the body
`\includegraphics` calls to the winners, deletes `figures/candidates/` and
`sections/app_figure_gallery.tex`, removes the `\input` from `chapter.tex`,
and recompiles. Groups marked `(production)` below are the ones the narrative
currently uses; the others are unused candidates.

## Chapter M

```text
- [ ] a3_hat_plot
        1 candidate(s): codex
        keep: ____________________   drop: ____________________
- [ ] abs1  (production)
        5 candidate(s): best, claude, qwen, grok, codex
        keep: ____________________   drop: ____________________
- [ ] abs2  (production)
        5 candidate(s): best, claude, qwen, grok, codex
        keep: ____________________   drop: ____________________
- [ ] bd_conditional_mean
        2 candidate(s): grok, grok
        keep: ____________________   drop: ____________________
- [ ] bd_mean_regimes
        2 candidate(s): grok, grok
        keep: ____________________   drop: ____________________
- [ ] bd_mean_survival_panel
        2 candidate(s): grok, grok
        keep: ____________________   drop: ____________________
- [ ] bd_survival_regimes
        2 candidate(s): grok, grok
        keep: ____________________   drop: ____________________
- [ ] birth_death_paths  (production)
        2 candidate(s): best, claude
        keep: ____________________   drop: ____________________
- [ ] conditionalmean  (production)
        5 candidate(s): best, claude, qwen, grok, codex
        keep: ____________________   drop: ____________________
- [ ] coupled_ode_ctmc  (production)
        2 candidate(s): best, claude
        keep: ____________________   drop: ____________________
- [ ] dtcta  (production)
        4 candidate(s): best, claude, grok, codex
        keep: ____________________   drop: ____________________
- [ ] extinction_and_law  (production)
        2 candidate(s): best, claude
        keep: ____________________   drop: ____________________
- [ ] figure1_parameter_conjugacy
        1 candidate(s): codex
        keep: ____________________   drop: ____________________
- [ ] figure2_koenigs_linearization
        1 candidate(s): codex
        keep: ____________________   drop: ____________________
- [ ] figure4_mandelbrot_context
        1 candidate(s): codex
        keep: ____________________   drop: ____________________
- [ ] founder_cohort_survival
        1 candidate(s): codex
        keep: ____________________   drop: ____________________
- [ ] gw_regime_diagnostics
        1 candidate(s): codex
        keep: ____________________   drop: ____________________
- [ ] kvals  (production)
        5 candidate(s): best, claude, qwen, grok, codex
        keep: ____________________   drop: ____________________
- [ ] kvals495  (production)
        5 candidate(s): best, claude, qwen, grok, codex
        keep: ____________________   drop: ____________________
- [ ] kvals505  (production)
        5 candidate(s): best, claude, qwen, grok, codex
        keep: ____________________   drop: ____________________
- [ ] logspec_mean  (production)
        2 candidate(s): best, qwen
        keep: ____________________   drop: ____________________
- [ ] period_double
        1 candidate(s): codex
        keep: ____________________   drop: ____________________
- [ ] poisson_path
        2 candidate(s): grok, grok
        keep: ____________________   drop: ____________________
- [ ] poisson_process  (production)
        2 candidate(s): best, claude
        keep: ____________________   drop: ____________________
- [ ] power_law_fixed  (production)
        5 candidate(s): best, claude, qwen, grok, codex
        keep: ____________________   drop: ____________________
- [ ] random_walk  (production)
        2 candidate(s): best, claude
        keep: ____________________   drop: ____________________
- [ ] ruin_hitting
        2 candidate(s): grok, grok
        keep: ____________________   drop: ____________________
- [ ] ruin_prob
        1 candidate(s): qwen
        keep: ____________________   drop: ____________________
- [ ] rupture_sawtooth  (production)
        2 candidate(s): best, qwen
        keep: ____________________   drop: ____________________
- [ ] rw_transition  (production)
        2 candidate(s): best, qwen
        keep: ____________________   drop: ____________________
- [ ] simplegwvis  (production)
        5 candidate(s): best, claude, qwen, grok, codex
        keep: ____________________   drop: ____________________
- [ ] subgwvis  (production)
        5 candidate(s): best, claude, qwen, grok, codex
        keep: ____________________   drop: ____________________
```

## Chapter A

```text
- [ ] a3_hat_plot  (production)
        9 candidate(s): best, claude, qwen, grok, grok, grok, codex, codex, codex
        keep: ____________________   drop: ____________________
- [ ] abs1
        1 candidate(s): codex
        keep: ____________________   drop: ____________________
- [ ] abs2
        1 candidate(s): codex
        keep: ____________________   drop: ____________________
- [ ] ap_bounds_ratio
        1 candidate(s): qwen
        keep: ____________________   drop: ____________________
- [ ] ap_nearcrit
        1 candidate(s): qwen
        keep: ____________________   drop: ____________________
- [ ] conditionalmean
        4 candidate(s): best, claude, grok, codex
        keep: ____________________   drop: ____________________
- [ ] dtcta  (production)
        5 candidate(s): best, claude, qwen, grok, codex
        keep: ____________________   drop: ____________________
- [ ] figure1_parameter_conjugacy  (production)
        7 candidate(s): best, claude, qwen, grok, grok, codex, codex
        keep: ____________________   drop: ____________________
- [ ] figure2_koenigs_linearization  (production)
        7 candidate(s): best, claude, qwen, grok, grok, codex, codex
        keep: ____________________   drop: ____________________
- [ ] figure3_numerical_koenigs  (production)
        5 candidate(s): best, claude, qwen, grok, codex
        keep: ____________________   drop: ____________________
- [ ] figure4_mandelbrot_context  (production)
        7 candidate(s): best, claude, qwen, grok, grok, codex, codex
        keep: ____________________   drop: ____________________
- [ ] koenigs_domain
        1 candidate(s): qwen
        keep: ____________________   drop: ____________________
- [ ] kvals
        1 candidate(s): codex
        keep: ____________________   drop: ____________________
- [ ] kvals495
        1 candidate(s): codex
        keep: ____________________   drop: ____________________
- [ ] kvals505
        1 candidate(s): codex
        keep: ____________________   drop: ____________________
- [ ] period_double  (production)
        7 candidate(s): best, claude, qwen, grok, grok, codex, codex
        keep: ____________________   drop: ____________________
- [ ] power_law_fixed
        3 candidate(s): grok, codex, codex
        keep: ____________________   drop: ____________________
- [ ] simplegwvis
        3 candidate(s): grok, codex, codex
        keep: ____________________   drop: ____________________
- [ ] subgwvis
        3 candidate(s): grok, codex, codex
        keep: ____________________   drop: ____________________
```
