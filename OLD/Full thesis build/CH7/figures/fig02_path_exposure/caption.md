# Figure: path exposure (paper caption)

Why the no-catastrophe probability is an occupation-time functional rather than a function of the terminal counts.
Two deterministic, hand-designed population histories on $t\in[0,10]$ both begin at $(X_0,Y_0)=(1,0)$ and end at the same terminal state $(X_{10},Y_{10})=(2,1)$.
(a)~Path~A grows to an early peak and then dies back; (b)~Path~B lingers small and blooms late (common vertical scale).
(c)~Instantaneous catastrophe rate $\lambda(t)=\delta_1X_t+\delta_2Y_t$ for each history: the terminal hazard $\lambda(10)$ is shared, but the integrated exposure $\int_0^{10}\lambda$ differs by a factor of about $2.4$.
(d)~Pathwise weights $\exp\{-\int_0^t\lambda\,ds\}$, the quantities averaged in the occupation-time transform of \cref{prop:feynman-kac}.
Catastrophe-rate weights $\delta_1=0.15$, $\delta_2=0.10$; paths tabulated in \texttt{figures/fig02\_path\_exposure/paths.json}.
