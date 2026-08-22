#!/usr/bin/env python3
"""
Small experiment that produces numbers useful for the paper.
"""

from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "python"))

import numpy as np
from arche_cell.core import Grid, compute_xi


def run_single(seed: int, steps: int = 40, rows: int = 6, cols: int = 6, W: int = 16):
    rng = np.random.default_rng(seed)
    grid = Grid(rows=rows, cols=cols, W=W, T=4, lambda_=0.8, mu=1.2, rng=rng)

    xi_series = []
    self_loop_count = 0
    total_decisions = 0

    for t in range(steps):
        valence = np.sin(0.25 * t + 0.4 * np.arange(rows)[:, None]
                         + 0.25 * np.arange(cols)[None, :])
        valence = np.clip(valence, -1.0, 1.0)

        prev_states = [[cell.s.copy() for cell in row] for row in grid.cells]
        grid.step(valence)

        for i in range(rows):
            for j in range(cols):
                total_decisions += 1
                if np.array_equal(grid.cells[i][j].s, prev_states[i][j]):
                    self_loop_count += 1

        xis = [compute_xi(cell.s) for row in grid.cells for cell in row]
        xi_series.append(float(np.mean(xis)))

    self_loop_rate = self_loop_count / total_decisions
    return np.array(xi_series), self_loop_rate


def main():
    seeds = list(range(12))
    steps = 40
    all_xi = []
    rates = []

    print("Arche-Cell paper experiment")
    print(f"Grid 6x6 | W=16 | T=4 | steps={steps} | seeds={len(seeds)}")
    print("-" * 60)

    for s in seeds:
        xi_series, rate = run_single(s, steps=steps)
        all_xi.append(xi_series)
        rates.append(rate)
        print(f"seed {s:2d}  final mean Ξ = {xi_series[-1]:5.2f}  self-loop rate = {rate:.3f}")

    all_xi = np.stack(all_xi)
    mean_xi = all_xi.mean(axis=0)
    std_xi = all_xi.std(axis=0)

    print("-" * 60)
    print("Average Ξ trajectory (mean ± std across seeds):")
    for t in range(0, steps, 5):
        print(f"  t={t:2d}  Ξ = {mean_xi[t]:5.2f} ± {std_xi[t]:4.2f}")

    print("-" * 60)
    print(f"Overall self-loop rate: {np.mean(rates):.3f} ± {np.std(rates):.3f}")
    print(f"Final Ξ (last tick):    {mean_xi[-1]:.2f} ± {std_xi[-1]:.2f}")
    print()
    print("These numbers can be used as a small empirical illustration")
    print("of stabilisation behaviour under the self-loop property.")


if __name__ == "__main__":
    main()
