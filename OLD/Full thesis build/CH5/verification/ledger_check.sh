#!/usr/bin/env bash
# Ledger check for the Chapter 5 rewrite.  Run from CH5_REWRITE/.
#   bash verification/ledger_check.sh
# Prints, in full: every new label found or not found in sections/, every
# Chapter 2 deferral target found or not found in CH2/sections/, and every
# preservation-list passage found or not found by its opening words.

# CH2 lives beside this chapter; in the "Current best" layout that is
# ../Good examples/CH2.  Override with CH2=... in the environment.
CH2="${CH2:-$(for c in "../CH2" "../Good examples/CH2"; do \
      [ -d "$c/sections" ] && echo "$c" && break; done)}"
[ -d "$CH2/sections" ] || echo "WARNING: CH2 sections not found (CH2=$CH2)"
SEC="sections"
fail=0

hdr () { printf '\n%s\n%s\n' "$1" "$(printf '=%.0s' $(seq 1 76))"; }

hdr "1. NEW LABELS  (defined in sections/, and referenced at least once)"
printf '%-34s %-10s %-10s %s\n' "LABEL" "DEFINED" "REFS" "STATUS"
printf -- '-%.0s' $(seq 1 76); echo
for lab in $(grep -rho '\\label{dist:[^}]*}' "$SEC" | sed 's/\\label{//;s/}//' | sort); do
  d=$(grep -rl "\\\\label{$lab}" "$SEC" | wc -l | tr -d ' ')
  r=$(grep -rho "\\\\[Cc]ref[a-z]*{[^}]*}" "$SEC" | grep -c "\b$lab\b")
  st="ok"
  [ "$d" -ne 1 ] && { st="DUPLICATE/MISSING DEFINITION"; fail=1; }
  [ "$r" -eq 0 ] && st="$st (never referenced)"
  printf '%-34s %-10s %-10s %s\n' "$lab" "$d" "$r" "$st"
done

hdr "2. CHAPTER 2 DEFERRAL TARGETS  (must resolve in CH2/sections/)"
printf '%-34s %s\n' "LABEL" "FILE"
printf -- '-%.0s' $(seq 1 76); echo
for lab in m:sec:moc m:eq:genericcharacteristics m:fig:characteristics \
           m:app:extract m:eq:stateProb \
           m:app:hyp m:prop:hypIden m:eq:hypIden \
           m:def:qsd m:sec:condmeans; do
  f=$(grep -rl "\\\\label{$lab}" "$CH2/sections" 2>/dev/null | sed 's|.*/||' | tr '\n' ' ')
  if [ -z "$f" ]; then f="*** NOT FOUND ***"; fail=1; fi
  printf '%-34s %s\n' "$lab" "$f"
done

hdr "3. PRESERVATION LIST  (plan section 13; grep on opening words)"
# Passages are line-wrapped in the source, so each file is flattened to one
# line before matching.
check_pass () {
  n="$1"; pat="$2"; desc="$3"
  hits=""
  for f in "$SEC"/*.tex; do
    if tr '\n' ' ' < "$f" | tr -s ' ' | grep -q "$pat"; then
      hits="$hits$(basename "$f") "
    fi
  done
  if [ -z "$hits" ]; then hits="*** NOT FOUND ***"; fail=1; fi
  printf '%-3s %-46s %s\n' "$n" "$desc" "$hits"
}
printf '%-3s %-46s %s\n' "#" "PASSAGE" "FOUND IN"
printf -- '-%.0s' $(seq 1 76); echo
check_pass 1 "The standard models of within-host infection treat" "black-box opening"
check_pass 2 "The answers, in advance and in brief, are these" "answers in advance"
check_pass 3a "has had to hold a middle course" "middle-course passage"
check_pass 3b "the productive lifetime is precisely the time needed" "Icarus callback"
check_pass 4 "The circularity was never in the mathematics" "circularity diagnosis"
check_pass 5a "The tempting guess is" "rem:ihatk trap"
check_pass 5b "It is tempting to write" "rem:gk trap"
check_pass 6 "release and death are the" "budding/bursting contrast"

hdr "4. HYGIENE"
for t in 'Chapter[~ ][0-9]' 'Part II' '\$\$' '\\Secref' '\\Figref' '\\Eqref' \
         '\\Tabref' '\\Chapref' '\\eqref' '\\figureflag' '\\noindent' '\\vspace'; do
  n=$(grep -rc "$t" "$SEC"/*.tex 2>/dev/null | awk -F: '{s+=$2} END {print s+0}')
  s="ok"; [ "$n" -ne 0 ] && { s="*** $n FOUND ***"; fail=1; }
  printf '%-30s %s\n' "$t" "$s"
done
nfig=$(grep -rc 'includegraphics' "$SEC"/*.tex | awk -F: '{s+=$2} END {print s+0}')
printf '%-30s %s\n' "figures included" "$nfig"

hdr "RESULT"
if [ "$fail" -eq 0 ]; then echo "ledger check: PASS"; else echo "ledger check: FAILURES ABOVE"; fi
exit $fail
