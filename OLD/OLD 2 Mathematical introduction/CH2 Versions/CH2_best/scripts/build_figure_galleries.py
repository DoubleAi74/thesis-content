#!/usr/bin/env python3
"""
Stage every figure binary from the four base merges (plus the current CH2_best
production assets) into per-chapter candidate directories, and generate the
temporary gallery appendices that display them all.

Follows AGENT_INSTRUCTIONS_FIGURE_GALLERY.md.  Re-runnable: it wipes and
rebuilds figures/candidates/ and sections/app_figure_gallery.tex in both
chapter projects, and rewrites the inventory and checklist.  Nothing outside
CH2_best/ is ever written to.

Run:  python3 scripts/build_figure_galleries.py     (from anywhere)
Deps: standard library only.  pdfinfo is used when present to validate PDFs.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

BEST = Path(__file__).resolve().parent.parent          # CH2_best/
ROOT = BEST.parent                                     # CH2 Versions/

IMAGE_EXT = {".pdf", ".png", ".jpg", ".jpeg", ".eps"}

# source tag -> version-tree directory name; order is harvest order
SOURCE_TREES = [
    ("claude", "CH2 Versions_claude"),
    ("qwen",   "CH2 Versions_Qwen"),
    ("grok",   "CH2 Versions_Grok"),
    ("codex",  "CH2 Versions_codex"),
]

# display order inside a comparison group
SOURCE_RANK = {"best": 0, "claude": 1, "qwen": 2, "grok": 3, "codex": 4}

CHAPTERS = [
    ("chapter_M_math_intro",  "m", "M"),
    ("chapter_A_constant_Ap", "a", "A"),
]

PER_ROW = 2          # panels per row
ROWS_PER_FLOAT = 2   # rows per float, so 4 panels per float
PANEL_WIDTH = "0.47\\textwidth"
PANEL_HEIGHT = "0.27\\textheight"


@dataclass
class Candidate:
    chapter: str          # chapter directory name
    source: str           # claude | qwen | grok | codex | best
    rel: str              # path relative to that source's figures/ root
    name: str             # candidate filename under figures/candidates/
    group: str            # group key (lowercased stem)
    size: int
    sha: str
    ok: bool              # passed the binary sanity check
    error: str            # reason, when not ok


# --------------------------------------------------------------------------
#  Harvest
# --------------------------------------------------------------------------
def safe_stem(rel: Path) -> str:
    """Relative path -> candidate filename body: '/' -> '__', ' ' -> '_'."""
    return str(rel).replace("/", "__").replace(" ", "_")


def sha256_short(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 16), b""):
            h.update(block)
    return h.hexdigest()[:12]


def looks_valid(path: Path) -> tuple[bool, str]:
    """Cheap integrity check, so a corrupt binary is reported and not silently lost."""
    if path.stat().st_size == 0:
        return False, "zero-length file"
    suffix = path.suffix.lower()
    head = path.open("rb").read(8)
    if suffix == ".pdf":
        if not head.startswith(b"%PDF"):
            return False, "missing \\%PDF header"
        try:
            out = subprocess.run(["pdfinfo", str(path)], capture_output=True, timeout=30)
            if out.returncode != 0:
                msg = out.stderr.decode(errors="replace").strip()[:100]
                return False, "pdfinfo rejected the file: " + msg
        except FileNotFoundError:
            pass          # pdfinfo unavailable; the header check stands
        except subprocess.TimeoutExpired:
            return False, "pdfinfo timed out"
    elif suffix == ".png":
        if not head.startswith(b"\x89PNG\r\n\x1a\n"):
            return False, "missing PNG signature"
    elif suffix in {".jpg", ".jpeg"}:
        if not head.startswith(b"\xff\xd8"):
            return False, "missing JPEG signature"
    return True, ""


def source_files(base: Path, recursive: bool) -> list[Path]:
    if not base.is_dir():
        return []
    it = base.rglob("*") if recursive else base.iterdir()
    return sorted(p for p in it if p.is_file() and p.suffix.lower() in IMAGE_EXT)


def harvest() -> tuple[list[Candidate], list[str]]:
    candidates: list[Candidate] = []
    notes: list[str] = []

    for chapter, _prefix, _short in CHAPTERS:
        cand_dir = BEST / chapter / "figures" / "candidates"
        if cand_dir.exists():
            shutil.rmtree(cand_dir)
        cand_dir.mkdir(parents=True)

        jobs: list[tuple[str, Path, Path]] = []   # (source, figures_root, file)

        # current production assets first: top level only, candidates/ excluded
        best_root = BEST / chapter / "figures"
        for f in source_files(best_root, recursive=False):
            jobs.append(("best", best_root, f))

        for tag, tree in SOURCE_TREES:
            root = ROOT / tree / "merged" / chapter / "figures"
            if not root.is_dir():
                notes.append(f"{tag}/{chapter}: no figures directory found")
                continue
            for f in source_files(root, recursive=True):
                jobs.append((tag, root, f))

        taken: dict[str, Path] = {}
        for source, root, path in jobs:
            if path.is_symlink():
                notes.append(f"{source}/{chapter}: {path} is a symlink; copied once")
            rel = path.relative_to(root)
            name = f"{source}__{safe_stem(rel)}"
            if name in taken:
                n = 2
                stem, ext = Path(name).stem, Path(name).suffix
                while f"{stem}__dup{n}{ext}" in taken:
                    n += 1
                notes.append(f"collision in {chapter}: {name} already held by "
                             f"{taken[name]}; stored as {stem}__dup{n}{ext}")
                name = f"{stem}__dup{n}{ext}"
            taken[name] = path

            shutil.copy2(path, cand_dir / name)
            ok, err = looks_valid(cand_dir / name)
            if not ok:
                notes.append(f"integrity: {chapter}/{name} -- {err}")
            candidates.append(Candidate(
                chapter=chapter, source=source, rel=str(rel), name=name,
                group=Path(rel).stem.lower(), size=path.stat().st_size,
                sha=sha256_short(path), ok=ok, error=err,
            ))

    return candidates, notes


# --------------------------------------------------------------------------
#  Gallery TeX
# --------------------------------------------------------------------------
def esc(text: str) -> str:
    return text.replace("_", r"\_")


def label_key(group: str) -> str:
    return "".join(ch if ch.isalnum() else "-" for ch in group)


def grouped(cands: list[Candidate]) -> list[tuple[str, list[Candidate]]]:
    buckets: dict[str, list[Candidate]] = defaultdict(list)
    for c in cands:
        buckets[c.group].append(c)
    for members in buckets.values():
        members.sort(key=lambda c: (SOURCE_RANK.get(c.source, 9), c.rel, c.name))
    return sorted(buckets.items())


def panel(c: Candidate) -> list[str]:
    """Lines for one minipage; the caller appends the row separator to the last."""
    if c.ok:
        art = (f"    \\includegraphics[width=\\linewidth,height={PANEL_HEIGHT},"
               f"keepaspectratio]{{candidates/{c.name}}}\\\\[3pt]")
    else:
        art = ("    \\fbox{\\parbox[c][0.16\\textheight][c]{0.86\\linewidth}"
               "{\\centering\\footnotesize failed the integrity check; it is listed "
               "at the end of this appendix}}\\\\[3pt]")
    return [f"  \\begin{{minipage}}[t]{{{PANEL_WIDTH}}}",
            "    \\centering",
            art,
            f"    {{\\footnotesize\\ttfamily {esc(c.name)}}}",
            "  \\end{minipage}"]


def gallery_tex(prefix: str, cands: list[Candidate]) -> str:
    groups = grouped(cands)
    multi = [(k, v) for k, v in groups if len(v) > 1]
    single = [(k, v) for k, v in groups if len(v) == 1]
    failures = [c for c in cands if not c.ok]

    keys = [label_key(k) for k, _ in groups]
    if len(set(keys)) != len(keys):
        raise SystemExit("label collision after sanitising group keys")

    L: list[str] = []
    add = L.append

    add("% ===========================================================================")
    add("%  TEMPORARY -- generated by scripts/build_figure_galleries.py.")
    add("%  Asset-selection aid only.  To remove: delete this file, drop its \\input")
    add("%  from chapter.tex, delete figures/candidates/, and recompile.")
    add("% ===========================================================================")
    add("")
    add("\\clearpage")
    add("% The last real appendix restores arabic section numbering for the chapters")
    add("% that follow, so the gallery has to re-enter appendix numbering itself and")
    add("% hand it back afterwards.  Nothing else about the numbering is disturbed.")
    add("\\renewcommand{\\thesection}{\\thechapter.\\Alph{section}}")
    add("\\section{Figure candidate gallery (temporary)}")
    add(f"\\label{{{prefix}:app:figuregallery}}")
    add("")
    add("This appendix is a temporary asset-selection aid and forms no part of the")
    add("chapter's argument. It displays every figure binary collected from the Claude,")
    add("Qwen, Grok and Codex merges, together with the assets currently used in this")
    add("project, which carry the \\texttt{best} tag. Each panel is labelled with its")
    add("candidate filename: the prefix is the source, and the remainder is the path the")
    add("file occupied in that source's \\texttt{figures/} tree, with directory")
    add("separators written as double underscores. Variants sharing a filename stem are")
    add("grouped so that they can be compared side by side. Nothing has been dropped as")
    add("redundant, so byte-identical binaries appear more than once by design. After")
    add("selection, this appendix and the unused candidates will be removed.")
    add("")
    add(f"There are {len(cands)} candidates here in {len(groups)} groups: {len(multi)}")
    add(f"with more than one variant, and {len(single)} one-offs.")
    add("")

    # --- index -------------------------------------------------------------
    add("\\subsection*{Index of groups}")
    add("")
    add("\\begingroup\\footnotesize\\raggedright")
    add("\\setlength{\\parskip}{1.5pt}\\setlength{\\parindent}{0pt}")
    for key, members in groups:
        sources = ", ".join(m.source for m in members)
        add(f"\\texttt{{{esc(key)}}} \\quad {len(members)} "
            f"({esc(sources)}) \\quad $\\rightarrow$ "
            f"\\cref{{{prefix}:fig:cand-{label_key(key)}-1}}\\par")
    add("\\endgroup")
    add("")

    # --- groups ------------------------------------------------------------
    def emit(entries: list[tuple[str, list[Candidate]]]) -> None:
        per_float = PER_ROW * ROWS_PER_FLOAT
        for key, members in entries:
            add(f"\\subsection*{{Group: \\texttt{{{esc(key)}}}}}")
            add("")
            chunks = [members[i:i + per_float]
                      for i in range(0, len(members), per_float)]
            for ci, chunk in enumerate(chunks, start=1):
                add("\\begin{figure}[htbp]")
                add("  \\centering")
                for pi, c in enumerate(chunk):
                    lines = panel(c)
                    if pi != len(chunk) - 1:
                        lines[-1] += "\\hfill" if (pi + 1) % PER_ROW else "\\\\[10pt]"
                    L.extend(lines)
                part = f", part {ci} of {len(chunks)}" if len(chunks) > 1 else ""
                plural = "s" if len(members) != 1 else ""
                add(f"  \\caption{{Candidates for group \\texttt{{{esc(key)}}} "
                    f"({len(members)} variant{plural}){part}. Filenames are printed "
                    f"beneath the panels.}}")
                add(f"  \\label{{{prefix}:fig:cand-{label_key(key)}-{ci}}}")
                add("\\end{figure}")
                add("")
            add("\\FloatBarrier")
            add("")

    if multi:
        add("\\subsection*{Comparison groups: two or more variants}")
        add("")
        emit(multi)
    if single:
        add("\\subsection*{Unique assets: a single source}")
        add("")
        emit(single)

    # --- failures ----------------------------------------------------------
    add("\\subsection*{Candidates that failed the integrity check}")
    add("")
    if failures:
        add("\\begingroup\\footnotesize\\raggedright")
        add("\\setlength{\\parskip}{1.5pt}\\setlength{\\parindent}{0pt}")
        for c in failures:
            add(f"\\texttt{{{esc(c.name)}}} \\quad --- \\quad {c.error} "
                f"\\quad (from \\texttt{{{esc(c.rel)}}})\\par")
        add("\\endgroup")
    else:
        add("None. Every staged candidate passed the header and \\texttt{pdfinfo}")
        add("checks, and every one of them is displayed above.")
    add("")
    add("\\FloatBarrier")
    add("")
    add("% --- restore default section numbering for subsequent chapters -------------")
    add("\\renewcommand{\\thesection}{\\thechapter.\\arabic{section}}")

    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------
#  Markdown logs
# --------------------------------------------------------------------------
def write_inventory(cands: list[Candidate]) -> None:
    L = ["# Figure candidate inventory — `CH2_best`", "",
         "Generated by `scripts/build_figure_galleries.py`; one row per staged file.",
         "`Original path` is relative to that source's `figures/` root — for the `best`",
         "tag, to the production `figures/` directory of this project. Group key is the",
         "lowercased filename stem, which is what the gallery compares on.", ""]

    for chapter, _prefix, short in CHAPTERS:
        rows = [c for c in cands if c.chapter == chapter]
        groups = grouped(rows)
        multi = [g for g in groups if len(g[1]) > 1]
        single = [g for g in groups if len(g[1]) == 1]
        per_source = Counter(c.source for c in rows)

        L += [f"## Chapter {short} (`{chapter}`)", "",
              f"- candidates staged: **{len(rows)}**",
              f"- groups: **{len(groups)}** — {len(multi)} with two or more variants, "
              f"{len(single)} one-offs",
              "- per source: " + ", ".join(
                  f"`{s}` {per_source[s]}" for s in
                  sorted(per_source, key=lambda s: SOURCE_RANK.get(s, 9))),
              f"- failed the integrity check: **{sum(1 for c in rows if not c.ok)}**",
              "",
              "| Group key | Source | Candidate filename | Original path | Bytes | "
              "SHA256 (12) | In gallery |",
              "|---|---|---|---|---|---|---|"]
        for key, members in groups:
            for c in members:
                L.append(f"| `{key}` | `{c.source}` | `{c.name}` | `{c.rel}` | "
                         f"{c.size} | `{c.sha}` | "
                         f"{'rendered' if c.ok else 'listed as a failure'} |")
        L.append("")

        L += ["### Comparison groups (two or more variants)", ""]
        for key, members in multi:
            L.append(f"- `{key}` ({len(members)}) — "
                     + ", ".join(f"`{m.source}`" for m in members))
        L += ["", "### One-offs (a single candidate)", ""]
        L.append(", ".join(f"`{k}`" for k, _ in single) or "_none_")
        L.append("")

        # identical binaries, which are the safest deletions for the selector
        by_sha: dict[str, list[Candidate]] = defaultdict(list)
        for c in rows:
            by_sha[c.sha].append(c)
        dupes = {s: v for s, v in by_sha.items() if len(v) > 1}
        L += ["### Byte-identical sets", "",
              "Candidates sharing a SHA256 are the same file under different names.",
              "They are all staged and all displayed; this list is here only so that the",
              "selector can see which comparisons are not real comparisons.", ""]
        if dupes:
            for sha, members in sorted(dupes.items(),
                                       key=lambda kv: -len(kv[1])):
                L.append(f"- `{sha}` ({len(members)}) — "
                         + ", ".join(f"`{m.name}`" for m in members))
        else:
            L.append("_none_")
        L.append("")

    m_groups = {k for k, _ in grouped([c for c in cands
                                       if c.chapter == "chapter_M_math_intro"])}
    a_groups = {k for k, _ in grouped([c for c in cands
                                       if c.chapter == "chapter_A_constant_Ap"])}
    both = sorted(m_groups & a_groups)
    L += ["## Group keys present in both chapters", "",
          "These stems were found in both an M figures tree and an A figures tree, so",
          "they are staged in both galleries. Each gallery shows the copy that lives in",
          "that chapter's source tree; no file was cross-copied between chapters.", "",
          ", ".join(f"`{g}`" for g in both) or "_none_", ""]

    (BEST / "FIGURE_CANDIDATE_INVENTORY.md").write_text("\n".join(L), encoding="utf-8")


def write_checklist(cands: list[Candidate]) -> None:
    L = ["# Figure selection checklist", "",
         "One row per candidate group. Write the candidate filename you want promoted",
         "to production after `keep:`, and the rest after `drop:` (`all` and `none` are",
         "fine). Nothing here is read by the build; it is a worksheet.", "",
         "When the sheet is filled in, a later pass rewires the body",
         "`\\includegraphics` calls to the winners, deletes `figures/candidates/` and",
         "`sections/app_figure_gallery.tex`, removes the `\\input` from `chapter.tex`,",
         "and recompiles. Groups marked `(production)` below are the ones the narrative",
         "currently uses; the others are unused candidates.", ""]

    production = {chapter: production_stems(chapter) for chapter, _, _ in CHAPTERS}

    for chapter, _prefix, short in CHAPTERS:
        rows = [c for c in cands if c.chapter == chapter]
        L += [f"## Chapter {short}", "", "```text"]
        for key, members in grouped(rows):
            tags = ", ".join(m.source for m in members)
            flag = "  (production)" if key in production[chapter] else ""
            L.append(f"- [ ] {key}{flag}")
            L.append(f"        {len(members)} candidate(s): {tags}")
            L.append("        keep: ____________________   drop: ____________________")
        L += ["```", ""]
    (BEST / "FIGURE_SELECTION_CHECKLIST.md").write_text("\n".join(L), encoding="utf-8")


def production_stems(chapter: str) -> set[str]:
    """Filename stems the chapter's narrative actually includes."""
    stems: set[str] = set()
    for tex in sorted((BEST / chapter / "sections").glob("*.tex")):
        if tex.name == "app_figure_gallery.tex":
            continue
        for chunk in tex.read_text(encoding="utf-8").split("\\includegraphics")[1:]:
            if "{" not in chunk:
                continue
            arg = chunk.split("{", 1)[1].split("}", 1)[0]
            stems.add(Path(arg).stem.lower())
    return stems


# --------------------------------------------------------------------------
def main() -> None:
    cands, notes = harvest()

    for chapter, prefix, _short in CHAPTERS:
        rows = [c for c in cands if c.chapter == chapter]
        out = BEST / chapter / "sections" / "app_figure_gallery.tex"
        out.write_text(gallery_tex(prefix, rows), encoding="utf-8")
        print(f"{chapter}: {len(rows)} candidates in {len(grouped(rows))} groups "
              f"-> {out.relative_to(BEST)}")

    write_inventory(cands)
    write_checklist(cands)

    body = "\n".join(notes) if notes else \
        "no collisions, no symlinks, no integrity failures"
    (BEST / "scripts" / "last_run_notes.txt").write_text(body + "\n", encoding="utf-8")
    if notes:
        print("\nnotes:")
        for n in notes:
            print("  -", n)
    print(f"\ntotal staged: {len(cands)}")


if __name__ == "__main__":
    main()
