module \$_MUX_ (
    output Y,
    input A,
    input B,
    input S
    );
  sg13g2_mux2_1 _TECHMAP_MUX (
      .X(Y),
      .A0(A),
      .A1(B),
      .S(S)
  );
endmodule
