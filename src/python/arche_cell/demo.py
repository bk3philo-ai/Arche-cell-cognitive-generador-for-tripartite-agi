"""
Minimal runnable demonstration of a small Arche-Cell grid.
"""

from __future__ import annotations

import numpy as np
from .core import Grid, compute_xi


def run_demo(steps: int = 20, seed: int = 42) -> None:
    rng = np.random.default_rng(seed)
    grid = Grid(rows=4, cols=4, W=16, T=4, lambda_=0.8, mu=1.2, rng=rng)

    print("Arche-Cell demo – 4×4 grid, W=16, T=4")
    print("-" * 50)

    for t in range(steps):
        # Synthetic valence field: a slow travelling wave
        valence = np.sin(0.3 * t + 0.5 * np.arange(4)[:, None] + 0.3 * np.arange(4)[None, :])
        valence = np.clip(valence, -1.0, 1.0)

        grid.step(valence)

        # Report average structural complexity and a sample state
        xis = [compute_xi(cell.s) for row in grid.cells for cell in row]
        mean_xi = float(np.mean(xis))
        sample = "".join(str(b) for b in grid.cells[0][0].s)
        print(f"t={t:3d}  mean Ξ = {mean_xi:5.2f}  cell[0,0] = {sample}")

    print("-" * 50)
    print("Demo finished. The self-loop property guarantees that,")
    print("inside each frozen tick, F never decreases.")


if __name__ == "__main__":
    run_demo()
