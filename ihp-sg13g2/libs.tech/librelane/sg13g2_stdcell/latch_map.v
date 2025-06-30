module \$_DLATCH_P_ (input E, input D, output Q);
  sg13g2_dlhq_1 _TECHMAP_DLATCH_P (
    .D(D),
    .Q(Q),
    .GATE(E)
  );
endmodule

module \$_DLATCH_PN0_ (input E, input R, input D, output Q);
  sg13g2_dlhrq_1 _TECHMAP_DLATCH_PN0 (
    .D(D),
    .Q(Q),
    .GATE(E),
    .RESET_B(R)
  );
endmodule

module \$_DLATCH_N_ (input E, input D, output Q);
  sg13g2_dllrq_1 _TECHMAP_DLATCH_N (
    .D(D),
    .Q(Q),
    .GATE_N(E),
    .RESET_B(1'b1)
  );
endmodule

module \$_DLATCH_NN0_ (input E, input R, input D, output Q);
  sg13g2_dllrq_1 _TECHMAP_DLATCH_NN0 (
    .D(D),
    .Q(Q),
    .GATE_N(E),
    .RESET_B(R)
  );
endmodule
