// Map Yosys' fine-grained tri-state buffer onto the weakest drive, as the
// thin-oxide library does. The enable is active-low on the cell (TE_B),
// so it is inverted here; the inverter is written as an explicit
// fine-grained \$_NOT_ rather than as ~E so that it is guaranteed to be a
// gate ABC can absorb, whatever stage this map is applied at.

module \$_TBUF_ (input A, input E, output Y);
  wire te_b;
  \$_NOT_ _TECHMAP_TE_B (.A(E), .Y(te_b));
  sg13g2_hv_ebufn_2 _TECHMAP_EBUF_N_ (
    .A(A),
    .Z(Y),
    .TE_B(te_b)
  );
endmodule
