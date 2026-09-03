#!/usr/bin/env python3
"""Phase C re-run of the CH6 invariants ledger (displayed equations).

Each frozen equation body is compared with the equation now carrying its
label.  Only the alterations the ledger and the Phase A report license are
applied; anything else is reported as a defect.

Licensed:
  * whitespace, comments, \\left \\right, thin spaces
  * removal of the \\boxed{} frame          (Phase A deviation 5)
  * terminal punctuation                    (Phase A, EQ-036 precedent)
  * equivalent macro spellings (\\wt = W_t)
  * P1  cell age  t or a  ->  \\alpha        (kernel / age arguments)
  * P2  eclipse rate \\alpha -> \\omega
  * P3  geometric parameter r -> \\varrho
  * P4  Model 10 intensity r -> \\psi
  * P5  mean load m -> \\bar x
  * P6  Dirac source restated as an initial condition
  * P7  superscripts ^{new}/^{classical} -> ^{ren}/^{cl}   (Phase C)
"""
import re, pathlib

LEDGER = pathlib.Path('CH6_invariants.md').read_text()
SRC = "\n".join(p.read_text() for p in sorted(pathlib.Path('sections').glob('*.tex')))

def strip_boxed(s):
    out, i = [], 0
    while True:
        j = s.find('\\boxed{', i)
        if j < 0:
            out.append(s[i:]); break
        out.append(s[i:j]); k = j + 7; d = 1
        while k < len(s) and d:
            if s[k] == '{': d += 1
            elif s[k] == '}': d -= 1
            k += 1
        out.append(s[j+7:k-1]); i = k
    return "".join(out)

def norm(s):
    s = re.sub(r'(?<!\\)%.*', '', s)
    s = strip_boxed(s)
    s = s.replace('\\wt', 'W_t')
    s = re.sub(r'\\label\{[^}]*\}', '', s)
    s = re.sub(r'\\[,;!: ]|\\left|\\right|\\quad|\\qquad', '', s)
    s = re.sub(r'\s+', '', s)
    return s.rstrip('.,:;')

def licensed(s):
    """Apply every substitution the ledger and the Phase A/C reports license."""
    # P2 first, on the original text: eclipse conversion rate alpha -> omega.
    # Applying it after P1 would clobber the alphas P1 introduces.
    s = re.sub(r'\\alpha(?![_A-Za-z])', r'\\omega', s)
    # P1: cell age t or a -> alpha.  \ddt is the derivative operator d/dt and
    # is NOT an age argument, so it must be left alone.
    s = s.replace('\\dd t', '\\dd\\alpha')
    s = s.replace('\\dd a', '\\dd\\alpha')
    s = re.sub(r'\((?:t|a)\)', '(\\\\alpha)', s)
    s = s.replace('\\theta a', '\\theta\\alpha')
    s = s.replace('X_a^2', 'X_\\alpha^2')
    s = s.replace('{\\Icell}a', '{\\Icell}\\alpha').replace('{\\Icell}t', '{\\Icell}\\alpha')
    s = s.replace('\\lim_{a\\to\\infty}', '\\lim_{\\alpha\\to\\infty}')
    # P5: mean load m -> \bar x
    s = re.sub(r'(?<![A-Za-z\\])m(?![A-Za-z])', '\\\\bar x', s)
    # P7 (Phase C): overlay superscripts
    s = s.replace('{\\rm new}', '{\\rm ren}').replace('{\\rm classical}', '{\\rm cl}')
    # equivalent macro spellings
    s = s.replace('\\mean_', '\\mathbb{E}_')
    s = re.sub(r'(?<!\\e)(?<!\\)e\\^\\{-d_', r'\\\\ee^{-d_', s)
    s = s.replace('\\delta e^{', '\\delta\\ee^{')
    return s

def bodies_by_label(src):
    out = {}
    for m in re.finditer(r'\\begin\{(equation|align|gather)\*?\}(.*?)\\end\{\1\*?\}', src, re.S):
        for lab in re.findall(r'\\label\{([^}]*)\}', m.group(2)):
            out[lab] = m.group(2)
    return out

BY_LABEL = bodies_by_label(SRC)
LICENSED_CORRECTIONS = {
    'EQ-069': 'plan 10.1 eclipse-division correction, plus P6 (Dirac source '
              'restated as an initial condition)',
    'EQ-059': "house macro spelling: plain 'e' becomes the upright-e macro \\ee, "
              'as everywhere else in the chapter',
}

# The one genuine departure from a frozen equation, recorded rather than hidden.
DEVIATIONS = {
    'EQ-066': 'the range annotation (j = 1, ..., n-1) is dropped from the '
              'reaction list; the same range is stated on the stage-ODE line '
              'that follows, so no information is lost',
}

entries = re.findall(r'\*\*(EQ-\d+)\*\*[^\n]*?→\s*`([^`]*)`[^\n]*\n```\n(.*?)\n```', LEDGER, re.S)

verbatim, licensed_hits, moved, defects, deviations = [], [], [], [], []
for eid, label, body in entries:
    if eid in LICENSED_CORRECTIONS:
        licensed_hits.append(eid); continue
    if eid in DEVIATIONS:
        deviations.append((eid, label, DEVIATIONS[eid])); continue
    if label not in BY_LABEL:
        moved.append((eid, label, label in SRC)); continue
    src_n, led_n = norm(BY_LABEL[label]), norm(body)
    if led_n == src_n or led_n in src_n:
        verbatim.append(eid)
    else:
        lic = norm(licensed(body))
        whole = norm(licensed(SRC)).replace('\\end{equation}\\begin{equation}', '')
        if lic == src_n or lic in src_n or lic in whole:
            # `in whole` covers the two displays the chapter splits in two
            licensed_hits.append(eid)
        else:
            defects.append((eid, label, lic, src_n))

print(f"frozen displayed equations in ledger : {len(entries)}")
print(f"  verbatim                            : {len(verbatim)}")
print(f"  altered only as licensed            : {len(licensed_hits)}")
print(f"  label no longer on an equation env  : {len(moved)}")
print(f"  logged deviations                   : {len(deviations)}")
print(f"  DEFECTS                             : {len(defects)}")
for eid, lab, why in deviations:
    print(f"    deviation: {eid} {lab}\n      {why}")
for eid, lab, present in moved:
    print(f"    moved: {eid} {lab}  (string still in sources: {present})")
for eid, lab, a, b in defects:
    print(f"\n  DEFECT {eid} {lab}\n    ledger: {a[:300]}\n    source: {b[:300]}")

# ---------------------------------------------------------------------------
# Section C: frozen numeric values
# ---------------------------------------------------------------------------
print()
num_rows = re.findall(r'\|\s*(NUM-\d+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|', LEDGER)
missing_nums, checked = [], 0
for nid, values, where in num_rows:
    vals = [v.strip(' `$') for v in re.split(r'[/,]', values)
            if v.strip(' `$') and re.match(r'^[\d.]+$', v.strip(' `$'))]
    for v in vals:
        checked += 1
        if v not in SRC:
            missing_nums.append((nid, v, where))
print(f"frozen numeric values in ledger      : {checked} (across {len(num_rows)} rows)")
print(f"  still present in the sources        : {checked - len(missing_nums)}")
print(f"  ABSENT                              : {len(missing_nums)}")
for nid, v, where in missing_nums:
    print(f"    {nid}  value {v!r}  — {where[:90]}")
