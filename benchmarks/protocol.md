# Falsifiable Benchmark Protocol

Task: stabilise a quadrotor drone in a wind tunnel under gust velocity up to 10 m/s.

## Comparisons

1. Classical PID controller (software baseline)
2. Quantised 3-layer neural network running on the **same** FPGA fabric (hardware baseline)

Static power overhead must be controlled so that the comparison is fair.

## Success criteria (against the neural baseline)

- RMS position error within 15 % of the neural network
- Total dynamic power ≤ 50 % of the neural network’s dynamic power
- Maximum control-loop latency < 10 µs

## Pre-registration

The full experimental protocol is intended to be registered on OSF before any silicon results are collected.

## Metrics to record

- RMS position and attitude error
- Dynamic and static power (board-level measurement)
- Worst-case and average control latency
- Fraction of ticks that trigger SDV relaxation
- Resource utilisation (LUTs, BRAM, DSP, registers)
