// The only characterized latch with a layout is sg13g2_hv_dlhrq_1
// (positive-enable, active-low async reset, Q only), so every fine-grained
// latch type maps onto it: the reset is tied off where unused and the
// enable inverted for the negative-enable types. The inverter is written
// as an explicit \$_NOT_ gate, not as ~E: this file is applied after the
// synth pass's lowering, so a coarse $not from an inline expression would
// survive to the netlist unmapped, while fine-grained gates are absorbed
// by the following ABC pass.

module \$_DLATCH_P_ (input E, input D, output Q);
  sg13g2_hv_dlhrq_1 _TECHMAP_DLATCH_P (
    .D(D),
    .Q(Q),
    .GATE(E),
    .RESET_B(1'b1)
  );
endmodule

module \$_DLATCH_PN0_ (input E, input R, input D, output Q);
  sg13g2_hv_dlhrq_1 _TECHMAP_DLATCH_PN0 (
    .D(D),
    .Q(Q),
    .GATE(E),
    .RESET_B(R)
  );
endmodule

module \$_DLATCH_N_ (input E, input D, output Q);
  wire en;
  \$_NOT_ _TECHMAP_EN (.A(E), .Y(en));
  sg13g2_hv_dlhrq_1 _TECHMAP_DLATCH_N (
    .D(D),
    .Q(Q),
    .GATE(en),
    .RESET_B(1'b1)
  );
endmodule

module \$_DLATCH_NN0_ (input E, input R, input D, output Q);
  wire en;
  \$_NOT_ _TECHMAP_EN (.A(E), .Y(en));
  sg13g2_hv_dlhrq_1 _TECHMAP_DLATCH_NN0 (
    .D(D),
    .Q(Q),
    .GATE(en),
    .RESET_B(R)
  );
endmodule
