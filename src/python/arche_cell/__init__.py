"""
Arche-Cell reference simulation.

Minimal pure-Python + NumPy implementation of the core update rule.
Intended for verification, calibration experiments and educational use.
Not a production FPGA model.
"""

from .core import ArcheCell, Grid, compute_xi, hamming
from .demo import run_demo

__all__ = ["ArcheCell", "Grid", "compute_xi", "hamming", "run_demo"]
__version__ = "0.1.0"
