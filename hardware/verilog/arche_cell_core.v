// Arche-Cell core – RTL sketch (not synthesised)
// Implements one cell update for W=64, r=1.
// This is a structural outline; timing, reset and AXI interfaces are omitted.

`timescale 1ns / 1ps

module arche_cell_core #(
    parameter W = 64,
    parameter T = 8
)(
    input  wire             clk,
    input  wire             rst_n,
    input  wire [W-1:0]     state_in,
    input  wire [T*W-1:0]   buffer_flat,   // T consecutive states
    input  wire signed [15:0] valence,     // fixed-point Q8.8 example
    input  wire signed [15:0] valence_max,
    input  wire [15:0]      lambda_q,      // Q8.8
    input  wire [15:0]      mu_q,
    output reg  [W-1:0]     state_out,
    output reg              done
);

    // ------------------------------------------------------------------
    // Ξ = popcount(s XOR rotate_right(s,1))
    // ------------------------------------------------------------------
    function automatic [6:0] popcount64;
        input [63:0] x;
        integer i;
        begin
            popcount64 = 0;
            for (i = 0; i < 64; i = i + 1)
                popcount64 = popcount64 + x[i];
        end
    endfunction

    function automatic [6:0] compute_xi;
        input [W-1:0] s;
        reg [W-1:0] rotated;
        begin
            rotated = {s[0], s[W-1:1]};   // rotate right by 1
            compute_xi = popcount64(s ^ rotated);
        end
    endfunction

    // ------------------------------------------------------------------
    // Candidate generation (self + 64 single-bit flips)
    // ------------------------------------------------------------------
    // In a real design this would be unrolled or sequenced over a few cycles.
    // Here we show the combinatorial idea only.

    // ------------------------------------------------------------------
    // Incremental similarity sketch
    // ------------------------------------------------------------------
    // Pre-compute base Hamming distances once per tick.
    // For each flipped bit k, the distance to each of the T history states
    // changes by ±1. Cost per candidate becomes O(T) instead of O(T*W).

    // ------------------------------------------------------------------
    // Fixed-point decay (zero DSP)
    // V_next = V - (V >> 19)
    // ------------------------------------------------------------------
    // wire signed [31:0] valence_next = valence - (valence >>> 19);

    // ------------------------------------------------------------------
    // Selector: argmax of F over the 65 candidates with lex tie-break
    // ------------------------------------------------------------------
    // Real implementation would use a tree of comparators or a sequential
    // scan. The self-state is always present, guaranteeing the monotonic
    // ascent property inside a frozen tick.

    // Placeholder sequential logic
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state_out <= {W{1'b0}};
            done      <= 1'b0;
        end else begin
            // TODO: full evaluation pipeline
            state_out <= state_in;   // temporary identity
            done      <= 1'b1;
        end
    end

endmodule
