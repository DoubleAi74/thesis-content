# Kickoff prompt — Chapter A polish agent

Copy everything below the line into an agent session opened on this folder (`ChapterA/`).

---

You are editing the mathematical introduction (Chapter A) in this workspace.

## Mission

Implement a **targeted series of fixes** specified in `polish_notes.md`. Prefer surgical LaTeX edits. Do not rewrite the chapter, expand scope, or restore full 1A side paths into the compiled chapter.

## Read first

1. `polish_notes.md` (authoritative fix list + checklist + current-tree status)
2. `sections/02_markov_chains.tex` (BDC def, rate diagram, mean-field remark — main touch surface)
3. Grep the tree for: `later chapter`, `factorise`, `\\delta`, `\\mathcal{E}_n`, `E_n`
4. `notes/bdc_material_for_later_chapters.tex` (holding file only — do not `\input` into `main.tex` / `chapter.tex`)
5. Optionally `sections/app_b_absorption_models.tex` for the hypergeometric `\delta` collision (fix A2)

## Priority order

1. **Must in Chapter A:** B3 (narrow multi-founder factorisation), B4 (named forward refs), A2 (`\delta` disentangle) if you can do it cleanly without breaking the appendix identity chain  
2. **Confirm / light touch:** A1 (exposure symbol), B1–B2 (captions), C1 (typos)  
3. **Optional:** D1 only if destination chapters lack the bridge — one paragraph max  
4. **Do not re-inflate Chapter A with E1–E3.** If you touch the holding file, only annotate/correct for later integration (especially `T_0 \wedge T_H` in E2). Prefer leaving E* for a follow-up unless a one-line annotation is clearly useful.

## Constraints

- Keep thesis voice and existing label/cref scheme (`m:def:bdc`, `m:fig:ratediagram`, `m:rem:notmeanfield`, …).
- Notation changes must be **global and consistent** within the compiled chapter (and figure labels on the TikZ rate diagram).
- Do not restore killed-subgenerator, full rupture schematic, or two-absorber QSD into sections that compile with Chapter A.
- Do not edit PDFs; edit `.tex` sources.
- Avoid drive-by refactors unrelated to `polish_notes.md`.

## Done criteria

- Checklist items you claim in `polish_notes.md` are actually fixed in source.
- `main.tex` still builds (run the project latexmk/pdflatex flow if available; report errors if not).
- Short final report: what changed (files + IDs), what you skipped and why, any residual notation risk.

## Out of scope

- Rewriting BDC core chapter content in `3 BDC_core DRAFT U/` beyond necessary cross-ref naming
- Full thesis-wide rename campaigns outside Chapter A unless required for A2 consistency inside this chapter’s appendices
