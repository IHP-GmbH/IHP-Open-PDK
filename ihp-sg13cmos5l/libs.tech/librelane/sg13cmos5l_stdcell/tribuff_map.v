module \$_TBUF_ (input A, input E, output Y);
  sg13cmos5l_ebufn_2 _TECHMAP_EBUF_N_ (
    .A(A),
    .Z(Y),
    .TE_B(~E));
endmodule
