// Map every posedge fine-grained Yosys flip-flop onto sg13g2_hv_sdfbbp_1,
// the only flop in sg13g2_stdcell_hv with both a liberty and a layout
// view today (the plain dfrbp*/dfrbpq* flops are characterized but not
// yet drawn, so the installed liberty does not ship them). dfflibmap
// cannot target a scan flop -- its next_state, (SCE & SCD) | (!SCE & D),
// is not a plain D function -- so this file runs as SYNTH_EXTRA_MAPPING_FILE
// (design-level; the variable is not PDK-scoped in LibreLane):
//
//   SYNTH_EXTRA_MAPPING_FILE: pdk_dir::libs.tech/librelane/sg13g2_stdcell_hv/sdfbbp_map.v
//
// Cell semantics (liberty ff group): posedge CLK; async clear !RESET_B,
// async preset !SET_B; next state (SCE & SCD) | (!SCE & D). Mapping per
// type:
//   - unused scan:    SCD=0, SCE=0       (next state = D)
//   - unused set/rst: SET_B=1, RESET_B=1
//   - clock enable:   the scan mux doubles as the enable mux --
//                     SCD=Q (hold path), SCE = "not enabled"
//   - sync reset:     folded into the D leg (and, where the reset has
//                     priority over the enable, into SCE as well)
// All glue logic is written as explicit fine-grained gates ($_NOT_,
// $_AND_, $_OR_): this file is applied after the synth pass's lowering,
// so coarse cells from inline expressions (~E, D & R) would survive to
// the netlist unmapped, while fine-grained gates are absorbed by the
// following ABC pass. All 23 clocked-only types below were proven
// equivalent to the Yosys cell semantics with equiv_induct against a
// behavioral model of the cell; the async types are direct pin ties.
//
// Deliberately NOT provided:
//   - negedge-clock types ($_DFF_N*_ etc.): mapping them through an
//     inverted CLK would silently distort a clock tree; synthesis fails
//     loudly on them instead.
//   - $_DFFSR_* both-active corner: the cell resolves simultaneous
//     set+reset as Q=1/Q_N=0 (clear_preset_var1 : H), Yosys models
//     reset-priority. Identical behavior whenever set and reset are
//     not asserted together, which RTL-derived DFFSRs satisfy.


// --- plain and async set/reset ---------------------------------------------


module \$_DFF_P_ (input C, input D, output Q);
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(D), .Q(Q), .Q_N(),
    .SCD(1'b0), .SCE(1'b0), .SET_B(1'b1), .RESET_B(1'b1));
endmodule

module \$_DFF_PN0_ (input C, input R, input D, output Q);
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(D), .Q(Q), .Q_N(),
    .SCD(1'b0), .SCE(1'b0), .SET_B(1'b1), .RESET_B(R));
endmodule

module \$_DFF_PP0_ (input C, input R, input D, output Q);
  wire rb;
  \$_NOT_ _TECHMAP_rb (.A(R), .Y(rb));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(D), .Q(Q), .Q_N(),
    .SCD(1'b0), .SCE(1'b0), .SET_B(1'b1), .RESET_B(rb));
endmodule

module \$_DFF_PN1_ (input C, input R, input D, output Q);
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(D), .Q(Q), .Q_N(),
    .SCD(1'b0), .SCE(1'b0), .SET_B(R), .RESET_B(1'b1));
endmodule

module \$_DFF_PP1_ (input C, input R, input D, output Q);
  wire sb;
  \$_NOT_ _TECHMAP_sb (.A(R), .Y(sb));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(D), .Q(Q), .Q_N(),
    .SCD(1'b0), .SCE(1'b0), .SET_B(sb), .RESET_B(1'b1));
endmodule

module \$_DFFSR_PNN_ (input C, input S, input R, input D, output Q);
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(D), .Q(Q), .Q_N(),
    .SCD(1'b0), .SCE(1'b0), .SET_B(S), .RESET_B(R));
endmodule

module \$_DFFSR_PNP_ (input C, input S, input R, input D, output Q);
  wire rb;
  \$_NOT_ _TECHMAP_rb (.A(R), .Y(rb));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(D), .Q(Q), .Q_N(),
    .SCD(1'b0), .SCE(1'b0), .SET_B(S), .RESET_B(rb));
endmodule

module \$_DFFSR_PPN_ (input C, input S, input R, input D, output Q);
  wire sb;
  \$_NOT_ _TECHMAP_sb (.A(S), .Y(sb));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(D), .Q(Q), .Q_N(),
    .SCD(1'b0), .SCE(1'b0), .SET_B(sb), .RESET_B(R));
endmodule

module \$_DFFSR_PPP_ (input C, input S, input R, input D, output Q);
  wire sb, rb;
  \$_NOT_ _TECHMAP_sb (.A(S), .Y(sb));
  \$_NOT_ _TECHMAP_rb (.A(R), .Y(rb));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(D), .Q(Q), .Q_N(),
    .SCD(1'b0), .SCE(1'b0), .SET_B(sb), .RESET_B(rb));
endmodule


// --- synchronous set/reset (folded into the D leg) -------------------------


module \$_SDFF_PN0_ (input C, input R, input D, output Q);
  wire dd;
  \$_AND_ _TECHMAP_dd (.A(D), .B(R), .Y(dd));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(dd), .Q(Q), .Q_N(),
    .SCD(1'b0), .SCE(1'b0), .SET_B(1'b1), .RESET_B(1'b1));
endmodule

module \$_SDFF_PP0_ (input C, input R, input D, output Q);
  wire rb, dd;
  \$_NOT_ _TECHMAP_rb (.A(R), .Y(rb));
  \$_AND_ _TECHMAP_dd (.A(D), .B(rb), .Y(dd));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(dd), .Q(Q), .Q_N(),
    .SCD(1'b0), .SCE(1'b0), .SET_B(1'b1), .RESET_B(1'b1));
endmodule

module \$_SDFF_PN1_ (input C, input R, input D, output Q);
  wire rb, dd;
  \$_NOT_ _TECHMAP_rb (.A(R), .Y(rb));
  \$_OR_ _TECHMAP_dd (.A(D), .B(rb), .Y(dd));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(dd), .Q(Q), .Q_N(),
    .SCD(1'b0), .SCE(1'b0), .SET_B(1'b1), .RESET_B(1'b1));
endmodule

module \$_SDFF_PP1_ (input C, input R, input D, output Q);
  wire dd;
  \$_OR_ _TECHMAP_dd (.A(D), .B(R), .Y(dd));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(dd), .Q(Q), .Q_N(),
    .SCD(1'b0), .SCE(1'b0), .SET_B(1'b1), .RESET_B(1'b1));
endmodule


// --- clock enable (scan mux as enable mux) ---------------------------------


module \$_DFFE_PN_ (input C, input E, input D, output Q);
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(D), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(E), .SET_B(1'b1), .RESET_B(1'b1));
endmodule

module \$_DFFE_PP_ (input C, input E, input D, output Q);
  wire en;
  \$_NOT_ _TECHMAP_en (.A(E), .Y(en));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(D), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(en), .SET_B(1'b1), .RESET_B(1'b1));
endmodule


// --- async set/reset + clock enable ----------------------------------------


module \$_DFFE_PN0N_ (input C, input R, input E, input D, output Q);
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(D), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(E), .SET_B(1'b1), .RESET_B(R));
endmodule

module \$_DFFE_PN0P_ (input C, input R, input E, input D, output Q);
  wire en;
  \$_NOT_ _TECHMAP_en (.A(E), .Y(en));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(D), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(en), .SET_B(1'b1), .RESET_B(R));
endmodule

module \$_DFFE_PN1N_ (input C, input R, input E, input D, output Q);
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(D), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(E), .SET_B(R), .RESET_B(1'b1));
endmodule

module \$_DFFE_PN1P_ (input C, input R, input E, input D, output Q);
  wire en;
  \$_NOT_ _TECHMAP_en (.A(E), .Y(en));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(D), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(en), .SET_B(R), .RESET_B(1'b1));
endmodule

module \$_DFFE_PP0N_ (input C, input R, input E, input D, output Q);
  wire rn;
  \$_NOT_ _TECHMAP_rn (.A(R), .Y(rn));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(D), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(E), .SET_B(1'b1), .RESET_B(rn));
endmodule

module \$_DFFE_PP0P_ (input C, input R, input E, input D, output Q);
  wire rn, en;
  \$_NOT_ _TECHMAP_rn (.A(R), .Y(rn));
  \$_NOT_ _TECHMAP_en (.A(E), .Y(en));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(D), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(en), .SET_B(1'b1), .RESET_B(rn));
endmodule

module \$_DFFE_PP1N_ (input C, input R, input E, input D, output Q);
  wire rn;
  \$_NOT_ _TECHMAP_rn (.A(R), .Y(rn));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(D), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(E), .SET_B(rn), .RESET_B(1'b1));
endmodule

module \$_DFFE_PP1P_ (input C, input R, input E, input D, output Q);
  wire rn, en;
  \$_NOT_ _TECHMAP_rn (.A(R), .Y(rn));
  \$_NOT_ _TECHMAP_en (.A(E), .Y(en));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(D), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(en), .SET_B(rn), .RESET_B(1'b1));
endmodule


// --- sync reset + enable, reset overrides enable ($_SDFFE_) ----------------
// The load must also open when the reset fires, so "reset
// active" is folded into SCE alongside the enable, and into
// the D leg as usual.


module \$_SDFFE_PN0N_ (input C, input R, input E, input D, output Q);
  wire dd, en;
  \$_AND_ _TECHMAP_dd (.A(D), .B(R), .Y(dd));
  \$_AND_ _TECHMAP_en (.A(E), .B(R), .Y(en));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(dd), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(en), .SET_B(1'b1), .RESET_B(1'b1));
endmodule

module \$_SDFFE_PN0P_ (input C, input R, input E, input D, output Q);
  wire dd, ne, en;
  \$_AND_ _TECHMAP_dd (.A(D), .B(R), .Y(dd));
  \$_NOT_ _TECHMAP_ne (.A(E), .Y(ne));
  \$_AND_ _TECHMAP_en (.A(ne), .B(R), .Y(en));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(dd), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(en), .SET_B(1'b1), .RESET_B(1'b1));
endmodule

module \$_SDFFE_PN1N_ (input C, input R, input E, input D, output Q);
  wire ra, dd, en;
  \$_NOT_ _TECHMAP_ra (.A(R), .Y(ra));
  \$_OR_ _TECHMAP_dd (.A(D), .B(ra), .Y(dd));
  \$_AND_ _TECHMAP_en (.A(E), .B(R), .Y(en));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(dd), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(en), .SET_B(1'b1), .RESET_B(1'b1));
endmodule

module \$_SDFFE_PN1P_ (input C, input R, input E, input D, output Q);
  wire ra, dd, ne, en;
  \$_NOT_ _TECHMAP_ra (.A(R), .Y(ra));
  \$_OR_ _TECHMAP_dd (.A(D), .B(ra), .Y(dd));
  \$_NOT_ _TECHMAP_ne (.A(E), .Y(ne));
  \$_AND_ _TECHMAP_en (.A(ne), .B(R), .Y(en));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(dd), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(en), .SET_B(1'b1), .RESET_B(1'b1));
endmodule

module \$_SDFFE_PP0N_ (input C, input R, input E, input D, output Q);
  wire ri, dd, en;
  \$_NOT_ _TECHMAP_ri (.A(R), .Y(ri));
  \$_AND_ _TECHMAP_dd (.A(D), .B(ri), .Y(dd));
  \$_AND_ _TECHMAP_en (.A(E), .B(ri), .Y(en));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(dd), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(en), .SET_B(1'b1), .RESET_B(1'b1));
endmodule

module \$_SDFFE_PP0P_ (input C, input R, input E, input D, output Q);
  wire ri, dd, er, en;
  \$_NOT_ _TECHMAP_ri (.A(R), .Y(ri));
  \$_AND_ _TECHMAP_dd (.A(D), .B(ri), .Y(dd));
  \$_OR_ _TECHMAP_er (.A(E), .B(R), .Y(er));
  \$_NOT_ _TECHMAP_en (.A(er), .Y(en));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(dd), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(en), .SET_B(1'b1), .RESET_B(1'b1));
endmodule

module \$_SDFFE_PP1N_ (input C, input R, input E, input D, output Q);
  wire ri, dd, en;
  \$_NOT_ _TECHMAP_ri (.A(R), .Y(ri));
  \$_OR_ _TECHMAP_dd (.A(D), .B(R), .Y(dd));
  \$_AND_ _TECHMAP_en (.A(E), .B(ri), .Y(en));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(dd), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(en), .SET_B(1'b1), .RESET_B(1'b1));
endmodule

module \$_SDFFE_PP1P_ (input C, input R, input E, input D, output Q);
  wire ri, dd, er, en;
  \$_NOT_ _TECHMAP_ri (.A(R), .Y(ri));
  \$_OR_ _TECHMAP_dd (.A(D), .B(R), .Y(dd));
  \$_OR_ _TECHMAP_er (.A(E), .B(R), .Y(er));
  \$_NOT_ _TECHMAP_en (.A(er), .Y(en));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(dd), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(en), .SET_B(1'b1), .RESET_B(1'b1));
endmodule


// --- sync reset + enable, enable gates reset ($_SDFFCE_) -------------------
// The reset only takes effect while loading, so SCE is the
// plain enable.


module \$_SDFFCE_PN0N_ (input C, input R, input E, input D, output Q);
  wire dd;
  \$_AND_ _TECHMAP_dd (.A(D), .B(R), .Y(dd));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(dd), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(E), .SET_B(1'b1), .RESET_B(1'b1));
endmodule

module \$_SDFFCE_PN0P_ (input C, input R, input E, input D, output Q);
  wire dd, en;
  \$_AND_ _TECHMAP_dd (.A(D), .B(R), .Y(dd));
  \$_NOT_ _TECHMAP_en (.A(E), .Y(en));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(dd), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(en), .SET_B(1'b1), .RESET_B(1'b1));
endmodule

module \$_SDFFCE_PN1N_ (input C, input R, input E, input D, output Q);
  wire ra, dd;
  \$_NOT_ _TECHMAP_ra (.A(R), .Y(ra));
  \$_OR_ _TECHMAP_dd (.A(D), .B(ra), .Y(dd));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(dd), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(E), .SET_B(1'b1), .RESET_B(1'b1));
endmodule

module \$_SDFFCE_PN1P_ (input C, input R, input E, input D, output Q);
  wire ra, dd, en;
  \$_NOT_ _TECHMAP_ra (.A(R), .Y(ra));
  \$_OR_ _TECHMAP_dd (.A(D), .B(ra), .Y(dd));
  \$_NOT_ _TECHMAP_en (.A(E), .Y(en));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(dd), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(en), .SET_B(1'b1), .RESET_B(1'b1));
endmodule

module \$_SDFFCE_PP0N_ (input C, input R, input E, input D, output Q);
  wire ri, dd;
  \$_NOT_ _TECHMAP_ri (.A(R), .Y(ri));
  \$_AND_ _TECHMAP_dd (.A(D), .B(ri), .Y(dd));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(dd), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(E), .SET_B(1'b1), .RESET_B(1'b1));
endmodule

module \$_SDFFCE_PP0P_ (input C, input R, input E, input D, output Q);
  wire ri, dd, en;
  \$_NOT_ _TECHMAP_ri (.A(R), .Y(ri));
  \$_AND_ _TECHMAP_dd (.A(D), .B(ri), .Y(dd));
  \$_NOT_ _TECHMAP_en (.A(E), .Y(en));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(dd), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(en), .SET_B(1'b1), .RESET_B(1'b1));
endmodule

module \$_SDFFCE_PP1N_ (input C, input R, input E, input D, output Q);
  wire ri, dd;
  \$_NOT_ _TECHMAP_ri (.A(R), .Y(ri));
  \$_OR_ _TECHMAP_dd (.A(D), .B(R), .Y(dd));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(dd), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(E), .SET_B(1'b1), .RESET_B(1'b1));
endmodule

module \$_SDFFCE_PP1P_ (input C, input R, input E, input D, output Q);
  wire ri, dd, en;
  \$_NOT_ _TECHMAP_ri (.A(R), .Y(ri));
  \$_OR_ _TECHMAP_dd (.A(D), .B(R), .Y(dd));
  \$_NOT_ _TECHMAP_en (.A(E), .Y(en));
  sg13g2_hv_sdfbbp_1 _TECHMAP_ (.CLK(C), .D(dd), .Q(Q), .Q_N(),
    .SCD(Q), .SCE(en), .SET_B(1'b1), .RESET_B(1'b1));
endmodule
