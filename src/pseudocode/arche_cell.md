# Arche-Cell – Language-Agnostic Pseudocode

All indices are 0-based unless noted. Bit vectors are of width `W`.

## Constants (fixed by the paper)

```
W          := 64
T          := 8
r          := 1
Ξ_max      := W
Γ_max      := 1
T_cell     := 10 ns          # example clock period
T_decay    := 5 ms           # example valence decay constant
γ_approx   := 1 - 2^(-19)    # fixed-point approximation of exp(-T_cell / T_decay)
```

## Data structures

```
State          : bit-vector[W]
Buffer         : array[T] of State
Neighbourhood  : list of cell indices (spatial neighbours under Π)
ValenceCache   : real  (or fixed-point)
```

## Structural complexity Ξ (circular 1-D chain)

```
function Ξ(s : State) → integer
    return popcount( s XOR rotate_right(s, 1) )
end
```

Locality proof: flipping bit k changes exactly two transitions
(k-1, k) and (k, k+1) modulo W. ΔΞ depends only on the 3-bit
neighbourhood of k. O(1) update is therefore uniform, including
boundaries.

## Similarity metric

```
function sim(s' : State, M : Buffer) → real in [0,1]
    total_dist := 0
    for k = 0 to T-1 do
        total_dist := total_dist + Hamming(s', M[k])
    end
    return 1 - total_dist / (T * W)
end
```

## Incremental similarity (r = 1 optimisation)

```
# Precompute once per tick for the parent state s
base_dist[j][k]  := Hamming(s, M_j[k])   for every neighbour j and buffer slot k

# For a candidate that differs from s by a single flip at index bit
function delta_sim(bit, M_j, base_dist_j) → real
    delta := 0
    for k = 0 to T-1 do
        if M_j[k][bit] == s[bit] then
            delta := delta + 1   # distance increases
        else
            delta := delta - 1   # distance decreases
        end
    end
    # new_sim = 1 - (old_total + delta) / (T*W)
    return delta
end
```

Cost per candidate drops from O(T·W) to O(T).

## Objective functional

```
function F(t, s', neighbours, V̂) → real
    xi_term  := Ξ(s') / Ξ_max
    gamma    := average over j in neighbours of sim(s', M_j)
    gamma_term := gamma / Γ_max
    val_term := 0.5 * (V̂ / V̂_max + 1)   # maps [-1,1] → [0,1]
    return xi_term + λ * gamma_term + μ * val_term
end
```

All three terms lie in [0,1]. They are therefore commensurable.

## Selector and deterministic update

```
function update_cell(i, t)
    s      := current state of cell i
    candidates := { s } ∪ { s with bit k flipped | k = 0 … W-1 }

    best_F := -∞
    best_s := s
    for each s' in candidates do
        f := F(t, s', N(i), V̂(t))
        if f > best_F or (f == best_F and lex_smaller(s', best_s)) then
            best_F := f
            best_s := s'
        end
    end
    return best_s   # τ is the lexicographic tie-breaker
end
```

Because the Hamming ball of radius 1 always contains the self-state,
the self-loop property holds and

```
F^(t)(s_i^(t+1)) ≥ F^(t)(s_i^(t))
```

with equality if and only if s already maximises F over the ball.
This is intra-tick only; F itself changes between ticks.

## Valence decay (fixed-point)

```
# Exact: V̂(t) = V * exp( -(t - t_last) / T_decay )
# Hardware: V̂ ← V̂ - (V̂ >> 19)     # equivalent to multiply by (1 - 2^(-19))

function decay_step(V̂)
    return V̂ - (V̂ >> 19)
end
```

Error analysis (paper Section 2.4):

- Per-tick relative error ≈ 9.3 × 10^{-8}
- Over N = 500 000 ticks the accumulated relative error is bounded by ≈ 4.8 %

This is acceptable for reactive control.

## Sensor Dynamic Variance (relaxation trigger)

```
function SDV(sensors, Δt, R)
    sum := 0
    for each sensor m do
        delta := |sensor_m(t) - sensor_m(t-Δt)| / R_m
        sum := sum + min(delta, 1)
    end
    return sum / M
end
```

SDV is guaranteed in [0,1] by construction.
