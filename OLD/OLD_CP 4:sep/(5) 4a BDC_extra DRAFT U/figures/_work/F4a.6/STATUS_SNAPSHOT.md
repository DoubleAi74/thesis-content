# F4a.6 status snapshot

Status: `claim_contradiction`

The conditional-mean half of the brief is internally consistent.  Direct
evaluation of Eq. (Vk) gives conditional means

`17.2321, 18.0736, 19.0202, 20.0050, 21.0012, 22.0003`

for founders `k=1,...,6`, with the first value equal to `a/(a-1)`.

The release-flux half is inconsistent with the immutable pointwise claim.
Using exactly

`K_k = k K I^(k-1) + k(k-1) J^2 I^(k-2)` and `g_k = delta K_k`

at `(lambda, mu, delta)=(1, 0.2, 0.05)` gives:

- `t=1`: `(g1,g2,g3,g4)=(0.387835, 1.113224, 2.096395, 3.269474)`;
- `t=3`: `(g1,g2,g3,g4)=(3.117543, 5.292878, 6.232182, 6.220450)`;
- `t=7.5`: `(g1,g2,g3,g4)=(0.454577, 0.193647, 0.061772, 0.017490)`;
- `t=15`: `(g1,g2,g3,g4)=(0.000689, 0.000259, 0.000073, 0.000018)`.

Thus the early ordering crosses and reverses within the requested domain
`t in [0,15]`.  A production panel cannot both use the authoritative formula
and truthfully annotate `g4 > g3 > g2 > g1` at each age.

No production asset was written and the TeX flag was not changed.
