#!/usr/bin/env python3
"""
Minimal single-cell update example.
Run from the repository root:

    python examples/minimal_update.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "python"))

import numpy as np
from arche_cell.core import ArcheCell, compute_xi

def main():
    cell = ArcheCell(W=8, T=4, lambda_=1.0, mu=1.0, rng=np.random.default_rng(0))
    print("Initial state :", "".join(map(str, cell.s)))
    print("Initial Ξ     :", compute_xi(cell.s))

    for t in range(5):
        valence = 0.5 * np.sin(0.7 * t)
        new_s = cell.step(neighbour_buffers=[], valence=valence)
        print(f"t={t}  state={''.join(map(str, new_s))}  Ξ={compute_xi(new_s)}")

if __name__ == "__main__":
    main()
