# Hardware constraints and resource notes

Target (from paper Section 8):

| Resource / Parameter       | Specification                  |
|----------------------------|--------------------------------|
| Clock frequency            | 100 MHz (example)              |
| Grid size                  | 64 × 64 = 4096 cells           |
| State width & buffer       | W = 64 bits, T = 8 states      |
| Search radius              | r = 1 (65 candidates/cell)     |
| Total evaluations / tick   | 266 240                        |
| BRAM usage                 | < 300 KB                       |
| LUT usage                  | < 200 000 (mid-range compatible)|
| Control loop latency       | 200 ns (20 cycles @ 100 MHz)   |
| Decay approximation        | fixed-point shift (0 DSP)      |
| Similarity update          | incremental O(T) per candidate |
| Ξ computation              | popcount(s XOR rotr(s,1))      |

## Combinatorial wall

For r = 3 the candidate set size is 43 745 per cell.
With 4096 cells this yields ~1.79 × 10^8 evaluations per tick – infeasible on mid-range FPGAs.

Restriction to r = 1 reduces the set to 65 candidates and makes the design practical.

## σ₀ cost model (incremental similarity)

```
σ₀ = κ · (T · W + (C(1,W) - 1) · T)
   = κ · (8 · 64 + 64 · 8)
   = κ · 1024
```

The first term computes the base Hamming distance of the parent state once.
The second term updates each of the 64 single-flip candidates in O(T).

## Open synthesis tasks

- Full place-and-route on a mid-range Xilinx / Intel / Lattice device
- Accurate dynamic power measurement under the quadrotor stabilisation benchmark
- Comparison against a quantised 3-layer neural network on the same fabric (static power controlled)
