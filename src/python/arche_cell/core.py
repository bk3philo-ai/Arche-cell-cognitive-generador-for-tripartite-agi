"""
Core Arche-Cell primitives.

Implements the formal definitions of Section 2 of the paper with
exact integer arithmetic for Ξ and Hamming distances.
"""

from __future__ import annotations

from typing import List, Sequence, Tuple
import numpy as np


def hamming(a: np.ndarray, b: np.ndarray) -> int:
    """Hamming distance between two binary vectors of equal length."""
    return int(np.count_nonzero(a != b))


def compute_xi(s: np.ndarray) -> int:
    """
    Structural complexity Ξ: number of 0-1 transitions in a circular chain.

    Ξ(s) = popcount(s XOR rotate_right(s, 1))
    Maximum value is W for an alternating pattern.
    """
    rotated = np.roll(s, 1)
    return int(np.count_nonzero(s != rotated))


def xi_delta_after_flip(s: np.ndarray, k: int) -> int:
    """
    O(1) change in Ξ when bit k is flipped.
    Depends only on the three-bit circular neighbourhood.
    """
    W = len(s)
    prev = (k - 1) % W
    nxt = (k + 1) % W

    # Current contribution of the two edges that touch k
    old = (s[prev] != s[k]) + (s[k] != s[nxt])
    # After flip
    new = (s[prev] != (1 - s[k])) + ((1 - s[k]) != s[nxt])
    return new - old


class ArcheCell:
    """
    Single Arche-Cell.

    State is a binary vector of width W.
    Memory buffer holds the last T states.
    """

    def __init__(
        self,
        W: int = 64,
        T: int = 8,
        lambda_: float = 1.0,
        mu: float = 1.0,
        rng: np.random.Generator | None = None,
    ):
        self.W = W
        self.T = T
        self.lambda_ = lambda_
        self.mu = mu
        self.rng = rng or np.random.default_rng()

        self.s = self.rng.integers(0, 2, size=W, dtype=np.uint8)
        self.buffer = np.tile(self.s, (T, 1))  # shape (T, W)
        self.xi_max = float(W)
        self.gamma_max = 1.0

    def candidates(self) -> List[np.ndarray]:
        """Hamming ball of radius 1 (self + all single-bit flips)."""
        cands = [self.s.copy()]
        for k in range(self.W):
            flipped = self.s.copy()
            flipped[k] = 1 - flipped[k]
            cands.append(flipped)
        return cands

    def similarity(self, s_prime: np.ndarray) -> float:
        """Average normalised Hamming similarity against the local buffer."""
        total = 0
        for t in range(self.T):
            total += hamming(s_prime, self.buffer[t])
        return 1.0 - total / (self.T * self.W)

    def objective(
        self,
        s_prime: np.ndarray,
        neighbour_sims: Sequence[float],
        valence: float,
        valence_max: float,
    ) -> float:
        """
        F(s') = Ξ/Ξ_max + λ·Γ/Γ_max + μ·(1/2)·(V̂/V̂_max + 1)
        All terms are in [0, 1].
        """
        xi_term = compute_xi(s_prime) / self.xi_max
        gamma = float(np.mean(neighbour_sims)) if neighbour_sims else self.similarity(s_prime)
        gamma_term = gamma / self.gamma_max
        # Map valence from [-1, 1] onto [0, 1]
        val_term = 0.5 * (valence / max(valence_max, 1e-9) + 1.0)
        return xi_term + self.lambda_ * gamma_term + self.mu * val_term

    def step(
        self,
        neighbour_buffers: Sequence[np.ndarray],
        valence: float,
        valence_max: float = 1.0,
    ) -> np.ndarray:
        """
        One deterministic update.

        Returns the new state (also stored internally).
        """
        cands = self.candidates()
        best_f = -np.inf
        best_s = self.s

        for s_prime in cands:
            # Local similarity + average over neighbours
            sims = [self.similarity(s_prime)]
            for buf in neighbour_buffers:
                # crude average similarity against neighbour memory
                total = sum(hamming(s_prime, buf[t]) for t in range(self.T))
                sims.append(1.0 - total / (self.T * self.W))
            f = self.objective(s_prime, sims, valence, valence_max)
            # Lexicographic tie-break on the bit vector viewed as integer
            if f > best_f or (np.isclose(f, best_f) and _lex_smaller(s_prime, best_s)):
                best_f = f
                best_s = s_prime

        # Shift buffer and insert new state
        self.buffer = np.roll(self.buffer, -1, axis=0)
        self.buffer[-1] = best_s
        self.s = best_s
        return best_s


def _lex_smaller(a: np.ndarray, b: np.ndarray) -> bool:
    """True if a is lexicographically smaller than b (bit 0 is MSB)."""
    for x, y in zip(a, b):
        if x != y:
            return bool(x < y)
    return False


class Grid:
    """
    Simple 2-D grid of Arche-Cells with 4-neighbour connectivity.
    Used only for small-scale experiments.
    """

    def __init__(self, rows: int, cols: int, **cell_kwargs):
        self.rows = rows
        self.cols = cols
        self.cells = [
            [ArcheCell(**cell_kwargs) for _ in range(cols)] for _ in range(rows)
        ]

    def neighbours(self, i: int, j: int) -> List[Tuple[int, int]]:
        dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        res = []
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.rows and 0 <= nj < self.cols:
                res.append((ni, nj))
        return res

    def step(self, valence_field: np.ndarray):
        """
        Advance the whole grid one tick.
        valence_field has shape (rows, cols) with values in [-1, 1].
        """
        # Snapshot of buffers so that updates are simultaneous
        buffers = [
            [cell.buffer.copy() for cell in row] for row in self.cells
        ]
        for i in range(self.rows):
            for j in range(self.cols):
                nbufs = [buffers[ni][nj] for ni, nj in self.neighbours(i, j)]
                self.cells[i][j].step(nbufs, float(valence_field[i, j]))
