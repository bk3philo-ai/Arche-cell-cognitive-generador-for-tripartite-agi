# Getting started

## 1. Clone and install

```bash
git clone https://github.com/YOUR_USERNAME/arche-cell.git
cd arche-cell
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r src/python/requirements.txt
```

## 2. Run the minimal example

```bash
python examples/minimal_update.py
```

## 3. Run the small-grid demo

```bash
cd src/python
python -m arche_cell.demo
```

## 4. Read the formal pseudocode

See `src/pseudocode/arche_cell.md`. It is the authoritative algorithmic description that any language implementation should follow.

## 5. Hardware path

The Verilog file under `hardware/verilog/` is only a structural sketch. It is not synthesised. Resource and timing notes live in `hardware/constraints/notes.md`.

## Next steps for a real deployment

1. Implement the full candidate evaluation pipeline (combinational or multi-cycle).
2. Add AXI-Stream or AXI-Lite interfaces for valence injection and state readout.
3. Synthesise on the target mid-range FPGA and measure power under the protocol of `benchmarks/protocol.md`.
4. Close any of the open problems listed in `open_problems/`.
