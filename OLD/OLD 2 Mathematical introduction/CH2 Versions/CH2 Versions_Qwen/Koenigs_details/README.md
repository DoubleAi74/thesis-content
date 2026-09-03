# A_Koenigs_Chapter

Standalone note combining:

- the Galton–Watson / $A(p)$ development from `Galton_Watson_A.tex`, and
- the no-closed-form / Koenigs analysis from `NCFproof.tex`,

with full elementary cases ($r=2$, $r=4$) and conjugacy details in the **appendix**.

## Build

```bash
latexmk -pdf Galton_Watson_A.tex
```

## Structure (high level)

1. Introduction to binary Galton–Watson branching  
2. Critical extinction and lifetime material (from original note)  
3. Limiting conditional mean and $A(p)$  
4. Attempts to compute $A(p)$ (product, asymptotics, genetic search)  
5. **Link to the logistic map and Koenigs function**  
6. **No elementary closed form for $r\in(0,1)$** (NCF content, careful claim)  
7. Practical hybrid numerics for $A(p)$  
8. Conclusion  
**Appendix.** Elementary solutions at $r=2,4$; conjugacy $c(r)$; Becker–Bergweiler summary  

## Sources

- `../GW and Koenigs /Galton-Watson A(P) LaTeX/Galton_Watson_A.tex`  
- `../GW and Koenigs /Galton-Watson A(P) LaTeX/no closed form proof/NCFproof.tex`  
