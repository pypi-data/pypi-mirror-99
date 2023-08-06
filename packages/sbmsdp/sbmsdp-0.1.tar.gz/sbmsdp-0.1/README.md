# SBMSDP2
This repository uses semi-definite programming to recover labels of stochastic block model.

## Note
The code in this repository can only recover symmetric SBM with two underlining communities.
Symmetric SBM means that the two communities have equal size.

The SBM generator is $\textrm{SBM}(n, \frac{a \log n}{n}, \frac{b \log n}{n})$.

## Sample code
```Python
from sbmsdp import sbm2, sdp2
G = sbm2(100, 16, 4)
X = sdp2(G)
print(X)
```

## Reference
