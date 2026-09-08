"""Phase C figure migration helpers: strip in-graphic titles, capture their text."""
import re, sys

def _balanced_end(s, i):
    """i points at the '(' of a call; return index just past its ')'."""
    d=0
    while i < len(s):
        if s[i]=='(': d+=1
        elif s[i]==')':
            d-=1
            if d==0: return i+1
        elif s[i] in '"\'':
            q=s[i]
            trip = s[i:i+3]==q*3
            i += 3 if trip else 1
            while i<len(s):
                if trip and s[i:i+3]==q*3: i+=3; break
                if not trip and s[i]==q and s[i-1]!='\\': i+=1; break
                i+=1
            continue
        i+=1
    raise ValueError("unbalanced")

def strip_titles(src, methods=("set_title","suptitle")):
    """Remove every set_title/suptitle *statement*; return (src, [captured text])."""
    caught=[]
    for meth in methods:
        while True:
            m=re.search(r'^([ \t]*)([A-Za-z_][\w\.\[\]0-9, ]*)\.'+meth+r'\(', src, re.M)
            if not m: break
            open_par=src.index('(', m.end()-1)
            end=_balanced_end(src, open_par)
            stmt=src[m.start():end]
            # swallow a trailing comma/newline
            while end<len(src) and src[end] in ' \t': end+=1
            if end<len(src) and src[end]=='\n': end+=1
            caught.append(" ".join(stmt.split()))
            src=src[:m.start()]+src[end:]
    return src, caught

def strip_kwarg_title(src):
    """Remove `title=...,` lines inside .set(...) blocks."""
    caught=re.findall(r'^\s*title=(.+?),\s*$', src, re.M)
    src=re.sub(r'^\s*title=.+?,\s*\n', '', src, flags=re.M)
    return src, caught

PALETTE=[('"tab:blue"','style_rc.BLUE'),("'tab:blue'",'style_rc.BLUE'),
         ('"tab:orange"','style_rc.VERMILLION'),("'tab:orange'",'style_rc.VERMILLION'),
         ('"tab:gray"','style_rc.SOFT'),("'tab:gray'",'style_rc.SOFT'),
         ('"tab:green"','style_rc.TEAL'),('"tab:purple"','style_rc.PURPLE')]

AGE=[(r'cell age $a$', r'cell age $\alpha$'),
     (r'producer age $a$', r'cell age $\alpha$'),
     (r'I_{\rm fix}(a)', r'I_{\rm fix}(\alpha)'),
     (r'I_{\mathrm{fix}}(a)', r'I_{\mathrm{fix}}(\alpha)'),
     (r'g(a)=\delta K(a)', r'g(\alpha)=\delta K(\alpha)'),
     (r'g(a) = \delta K(a)', r'g(\alpha) = \delta K(\alpha)'),
     (r'$g(a)$', r'$g(\alpha)$'), (r'$S(a)$', r'$S(\alpha)$')]

def apply_all(src):
    for a,b in PALETTE+AGE: src=src.replace(a,b)
    return src
