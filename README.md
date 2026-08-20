# Arche-Cell

Hardware-bound reactive component for tripartite cognitive architectures.

This repository contains the formal specification, reference Python simulation, hardware-oriented pseudocode, and open problems of the Arche-Cell: a local, memoryful, generative primitive designed for ultra-low-latency, ultra-low-power reactive control on FPGA.

The Arche-Cell is a per-tick, per-cell instantiation of the Arche Selector operator (Kowalski, 2026). It is not a general-purpose cognitive system. It is the low-level actuator (AI-1) that receives a valence field from an external predictor (AI-2) and produces deterministic actions with bounded latency.

## Status

Engineering hypothesis. No silicon results yet. All claims are falsifiable.

## Key properties

- State width `W = 64`
- Temporal buffer `T = 8`
- Hamming search radius `r = 1` (65 candidates per cell per tick)
- Structural complexity `Ξ` computed via circular popcount in O(1)
- Incremental similarity update O(T) per candidate
- Fixed-point valence decay with explicit error bound (~4.8 % at full horizon)
- Self-loop monotonic ascent of the objective functional inside each tick (inherited from the Selector framework)

## Repository layout

```
arche-cell/
├── paper/                  # Original paper (PDF)
├── src/
│   ├── python/             # Reference simulation
│   └── pseudocode/         # Language-agnostic algorithms
├── hardware/
│   ├── verilog/            # RTL sketches
│   └── constraints/        # Timing / resource notes
├── examples/               # Minimal runnable demos
├── benchmarks/             # Proposed evaluation protocol
├── open_problems/          # Explicit open questions
├── docs/                   # Additional notes
├── LICENSE
├── CITATION.cff
└── README.md
```

## Quick start (simulation)

```bash
cd src/python
python -m arche_cell.demo
```

Requirements: Python >= 3.10, numpy.

## Formal core (summary)

Each cell is the structure

```
K_i = (s_i, M_i^(t), L_i, Π, Ξ)
```

- `s_i ∈ {0,1}^W`
- `L_i(s)` = Hamming ball of radius 1 around `s` (includes self)
- Objective:

```
F^(t)(s') = Ξ(s')/Ξ_max
          + λ · Γ(s', neighbours) / Γ_max
          + μ · (1/2) · (V̂(s', Ω, t)/V̂_max + 1)
```

- Update:

```
s_i^(t+1) = τ( arg max_{s' ∈ L_i(s_i^(t))} F^(t)(s') )
```

where `τ` is a fixed deterministic tie-breaker (lexicographic on bit index).

All terms are normalised to [0,1]. The self-loop guarantees monotonic ascent of `F` inside a frozen tick.

## Hardware target

- Clock: 100 MHz (example)
- Grid: 64 × 64 = 4096 cells
- Evaluations per tick: 266 240
- Projected resources: < 200 000 LUTs, < 300 KB BRAM (mid-range FPGA)
- Control loop latency target: 200 ns

## Citation (obrigatória)

Se você usar este software, o pseudocódigo, a especificação formal ou qualquer parte deste repositório, **é obrigatório citar o autor**.

Forma recomendada:

```
Kowalski, B. (2026). The Arche-Cell: A Hardware-Bound Reactive Component for Tripartite Cognitive Architectures.
```

Também cite este repositório (veja o arquivo `CITATION.cff`).

A licença Apache 2.0 exige que o aviso de copyright e a atribuição ao autor sejam preservados em qualquer redistribuição ou trabalho derivado.

## License

Apache License 2.0. Veja o arquivo `LICENSE`.

Copyright 2026 Bob Kowalski.

## Open problems

See the folder `open_problems/` and Section 10 of the paper. Contributions that close any of them are welcome.
