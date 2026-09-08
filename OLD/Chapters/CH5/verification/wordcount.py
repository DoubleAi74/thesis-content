#!/usr/bin/env python3
"""Word count of body prose: displayed maths and tabular bodies removed,
captions and proofs kept, inline maths counted as one word."""
import re, sys, glob, os

def count(path):
    s = open(path).read()
    s = re.sub(r'^\s*%.*$', '', s, flags=re.M)
    for env in ('equation', r'equation\*', 'align', r'align\*', 'tabular',
                r'gather', r'gather\*', 'verbatim'):
        s = re.sub(r'\\begin\{' + env + r'\}.*?\\end\{' + env + r'\}', ' ',
                   s, flags=re.S)
    s = re.sub(r'\$\$.*?\$\$', ' ', s, flags=re.S)
    s = re.sub(r'\\\[.*?\\\]', ' ', s, flags=re.S)
    s = re.sub(r'\$[^$]*\$', ' X ', s)
    s = re.sub(r'\\[a-zA-Z]+\*?', ' ', s)
    s = re.sub(r'[{}\\&~]', ' ', s)
    return len(s.split())

tot = 0
for f in sorted(sys.argv[1:]):
    c = count(f); tot += c
    print(f'{os.path.basename(f):<38} {c:>6}')
print(f'{"TOTAL":<38} {tot:>6}')
