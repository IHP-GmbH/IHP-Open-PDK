// Copyright 2024 IHP PDK Authors
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//    https://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// type: AO21 
`timescale 1ns/10ps
`celldefine
module sg13g2_a21o_1 (X, A1, A2, B1);
	output X;
	input A1, A2, B1;

	// Function
	wire int_fwire_0;

	and (int_fwire_0, A1, A2);
	or (X, int_fwire_0, B1);

	// Timing
	specify
		(A1 => X) = 0;
		(A2 => X) = 0;
		if (A1 == 1'b1 & A2 == 1'b0)
			(B1 => X) = 0;
		if (A1 == 1'b0 & A2 == 1'b1)
			(B1 => X) = 0;
		ifnone (B1 => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: AO21 
`timescale 1ns/10ps
`celldefine
module sg13g2_a21o_2 (X, A1, A2, B1);
	output X;
	input A1, A2, B1;

	// Function
	wire int_fwire_0;

	and (int_fwire_0, A1, A2);
	or (X, int_fwire_0, B1);

	// Timing
	specify
		(A1 => X) = 0;
		(A2 => X) = 0;
		if (A1 == 1'b1 & A2 == 1'b0)
			(B1 => X) = 0;
		if (A1 == 1'b0 & A2 == 1'b1)
			(B1 => X) = 0;
		ifnone (B1 => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: a21oi 
`timescale 1ns/10ps
`celldefine
module sg13g2_a21oi_1 (Y, A1, A2, B1);
	output Y;
	input A1, A2, B1;

	// Function
	wire int_fwire_0, int_fwire_1;

	and (int_fwire_0, A1, A2);
	or (int_fwire_1, int_fwire_0, B1);
	not (Y, int_fwire_1);

	// Timing
	specify
		(A1 => Y) = 0;
		(A2 => Y) = 0;
		if (A1 == 1'b1 & A2 == 1'b0)
			(B1 => Y) = 0;
		if (A1 == 1'b0 & A2 == 1'b1)
			(B1 => Y) = 0;
		if (A1 == 1'b0 & A2 == 1'b0)
			(B1 => Y) = 0;
		ifnone (B1 => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: a21oi 
`timescale 1ns/10ps
`celldefine
module sg13g2_a21oi_2 (Y, A1, A2, B1);
	output Y;
	input A1, A2, B1;

	// Function
	wire int_fwire_0, int_fwire_1;

	and (int_fwire_0, A1, A2);
	or (int_fwire_1, int_fwire_0, B1);
	not (Y, int_fwire_1);

	// Timing
	specify
		(A1 => Y) = 0;
		(A2 => Y) = 0;
		if (A1 == 1'b1 & A2 == 1'b0)
			(B1 => Y) = 0;
		if (A1 == 1'b0 & A2 == 1'b1)
			(B1 => Y) = 0;
		if (A1 == 1'b0 & A2 == 1'b0)
			(B1 => Y) = 0;
		ifnone (B1 => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: a221oi 
`timescale 1ns/10ps
`celldefine
module sg13g2_a221oi_1 (Y, A1, A2, B1, B2, C1);
	output Y;
	input A1, A2, B1, B2, C1;

	// Function
	wire int_fwire_0, int_fwire_1, int_fwire_2;

	and (int_fwire_0, B1, B2);
	and (int_fwire_1, A1, A2);
	or (int_fwire_2, int_fwire_1, int_fwire_0, C1);
	not (Y, int_fwire_2);

	// Timing
	specify
		if (B1 == 1'b1 & B2 == 1'b0)
			(A1 => Y) = 0;
		if (B1 == 1'b0 & B2 == 1'b1)
			(A1 => Y) = 0;
		if (B1 == 1'b0 & B2 == 1'b0)
			(A1 => Y) = 0;
		ifnone (A1 => Y) = 0;
		if (B1 == 1'b1 & B2 == 1'b0)
			(A2 => Y) = 0;
		if (B1 == 1'b0 & B2 == 1'b1)
			(A2 => Y) = 0;
		if (B1 == 1'b0 & B2 == 1'b0)
			(A2 => Y) = 0;
		ifnone (A2 => Y) = 0;
		if (A1 == 1'b1 & A2 == 1'b0)
			(B1 => Y) = 0;
		if (A1 == 1'b0 & A2 == 1'b1)
			(B1 => Y) = 0;
		if (A1 == 1'b0 & A2 == 1'b0)
			(B1 => Y) = 0;
		ifnone (B1 => Y) = 0;
		if (A1 == 1'b1 & A2 == 1'b0)
			(B2 => Y) = 0;
		if (A1 == 1'b0 & A2 == 1'b1)
			(B2 => Y) = 0;
		if (A1 == 1'b0 & A2 == 1'b0)
			(B2 => Y) = 0;
		ifnone (B2 => Y) = 0;
		if (A1 == 1'b0 & A2 == 1'b1)
			(C1 => Y) = 0;
		ifnone (C1 => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: a22oi 
`timescale 1ns/10ps
`celldefine
module sg13g2_a22oi_1 (Y, A1, A2, B1, B2);
	output Y;
	input A1, A2, B1, B2;

	// Function
	wire int_fwire_0, int_fwire_1, int_fwire_2;

	and (int_fwire_0, B1, B2);
	and (int_fwire_1, A1, A2);
	or (int_fwire_2, int_fwire_1, int_fwire_0);
	not (Y, int_fwire_2);

	// Timing
	specify
		(A1 => Y) = 0;
		(A2 => Y) = 0;
		(B1 => Y) = 0;
		(B2 => Y) = 0;
	endspecify
endmodule
`endcelldefine


// type: AND2 
`timescale 1ns/10ps
`celldefine
module sg13g2_and2_1 (X, A, B);
	output X;
	input A, B;

	// Function
	and (X, A, B);

	// Timing
	specify
		(A => X) = 0;
		(B => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: AND2 
`timescale 1ns/10ps
`celldefine
module sg13g2_and2_2 (X, A, B);
	output X;
	input A, B;

	// Function
	and (X, A, B);

	// Timing
	specify
		(A => X) = 0;
		(B => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: AND3 
`timescale 1ns/10ps
`celldefine
module sg13g2_and3_1 (X, A, B, C);
	output X;
	input A, B, C;

	// Function
	and (X, A, B, C);

	// Timing
	specify
		(A => X) = 0;
		(B => X) = 0;
		(C => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: AND3 
`timescale 1ns/10ps
`celldefine
module sg13g2_and3_2 (X, A, B, C);
	output X;
	input A, B, C;

	// Function
	and (X, A, B, C);

	// Timing
	specify
		(A => X) = 0;
		(B => X) = 0;
		(C => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: AND4 
`timescale 1ns/10ps
`celldefine
module sg13g2_and4_1 (X, A, B, C, D);
	output X;
	input A, B, C, D;

	// Function
	and (X, A, B, C, D);

	// Timing
	specify
		(A => X) = 0;
		(B => X) = 0;
		(C => X) = 0;
		(D => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: AND4 
`timescale 1ns/10ps
`celldefine
module sg13g2_and4_2 (X, A, B, C, D);
	output X;
	input A, B, C, D;

	// Function
	and (X, A, B, C, D);

	// Timing
	specify
		(A => X) = 0;
		(B => X) = 0;
		(C => X) = 0;
		(D => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: NP_ant 
`timescale 1ns/10ps
`celldefine
module sg13g2_antennanp (A);
	input A;
	// Timing
	specify
	endspecify
endmodule
`endcelldefine

// type: BU 
`timescale 1ns/10ps
`celldefine
module sg13g2_buf_1 (X, A);
	output X;
	input A;

	// Function
	buf (X, A);

	// Timing
	specify
		(A => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: BU 
`timescale 1ns/10ps
`celldefine
module sg13g2_buf_16 (X, A);
	output X;
	input A;

	// Function
	buf (X, A);

	// Timing
	specify
		(A => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: BU 
`timescale 1ns/10ps
`celldefine
module sg13g2_buf_2 (X, A);
	output X;
	input A;

	// Function
	buf (X, A);

	// Timing
	specify
		(A => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: BU 
`timescale 1ns/10ps
`celldefine
module sg13g2_buf_4 (X, A);
	output X;
	input A;

	// Function
	buf (X, A);

	// Timing
	specify
		(A => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: BU 
`timescale 1ns/10ps
`celldefine
module sg13g2_buf_8 (X, A);
	output X;
	input A;

	// Function
	buf (X, A);

	// Timing
	specify
		(A => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: DECAP 
`timescale 1ns/10ps
`celldefine
module sg13g2_decap_4 ();
	// Timing
	specify
	endspecify
endmodule
`endcelldefine

// type: DECAP 
`timescale 1ns/10ps
`celldefine
module sg13g2_decap_8 ();
	// Timing
	specify
	endspecify
endmodule
`endcelldefine

// type: dffrr 
`timescale 1ns/10ps
`celldefine
module sg13g2_dfrbp_1 (Q, Q_N, D, RESET_B, CLK);
	output Q, Q_N;
	input D, RESET_B, CLK;
	reg notifier;
	wire delayed_D, delayed_RESET_B, delayed_CLK;

	// Function
	wire int_fwire_IQ, int_fwire_IQN, int_fwire_r;
	wire xcr_0;

	not (int_fwire_r, delayed_RESET_B);
	ihp_dff_r_err (xcr_0, delayed_CLK, delayed_D, int_fwire_r);
	ihp_dff_r (int_fwire_IQ, notifier, delayed_CLK, delayed_D, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (Q_N, int_fwire_IQN);

	// Timing
	specify
		(negedge RESET_B => (Q+:1'b0)) = 0;
		(posedge CLK => (Q+:D)) = 0;
		(negedge RESET_B => (Q_N-:1'b0)) = 0;
		(posedge CLK => (Q_N-:D)) = 0;
		$setuphold (posedge CLK, posedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, negedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$recrem (posedge RESET_B, posedge CLK, 0, 0, notifier,,, delayed_RESET_B, delayed_CLK);
		$width (negedge RESET_B, 0, 0, notifier);
		$width (posedge CLK, 0, 0, notifier);
		$width (negedge CLK, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type: dffrr 
`timescale 1ns/10ps
`celldefine
module sg13g2_dfrbp_2 (Q, Q_N, D, RESET_B, CLK);
	output Q, Q_N;
	input D, RESET_B, CLK;
	reg notifier;
	wire delayed_D, delayed_RESET_B, delayed_CLK;

	// Function
	wire int_fwire_IQ, int_fwire_IQN, int_fwire_r;
	wire xcr_0;

	not (int_fwire_r, delayed_RESET_B);
	ihp_dff_r_err (xcr_0, delayed_CLK, delayed_D, int_fwire_r);
	ihp_dff_r (int_fwire_IQ, notifier, delayed_CLK, delayed_D, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (Q_N, int_fwire_IQN);

	// Timing
	specify
		(negedge RESET_B => (Q+:1'b0)) = 0;
		(posedge CLK => (Q+:D)) = 0;
		(negedge RESET_B => (Q_N-:1'b0)) = 0;
		(posedge CLK => (Q_N-:D)) = 0;
		$setuphold (posedge CLK, posedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, negedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$recrem (posedge RESET_B, posedge CLK, 0, 0, notifier,,, delayed_RESET_B, delayed_CLK);
		$width (negedge RESET_B, 0, 0, notifier);
		$width (posedge CLK, 0, 0, notifier);
		$width (negedge CLK, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type: DLHQ 
`timescale 1ns/10ps
`celldefine
module sg13g2_dlhq_1 (Q, D, GATE);
	output Q;
	input D, GATE;
	reg notifier;
	wire delayed_D, delayed_GATE;

	// Function
	wire int_fwire_IQ;

	ihp_latch (int_fwire_IQ, notifier, delayed_GATE, delayed_D);
	buf (Q, int_fwire_IQ);

	// Timing
	specify
		(D => Q) = 0;
		(posedge GATE => (Q+:D)) = 0;
		$setuphold (negedge GATE, posedge D, 0, 0, notifier,,, delayed_GATE, delayed_D);
		$setuphold (negedge GATE, negedge D, 0, 0, notifier,,, delayed_GATE, delayed_D);
		$width (posedge GATE, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type: DLHR 
`timescale 1ns/10ps
`celldefine
module sg13g2_dlhr_1 (Q, Q_N, D, RESET_B, GATE);
	output Q, Q_N;
	input D, RESET_B, GATE;
	reg notifier;
	wire delayed_D, delayed_RESET_B, delayed_GATE;

	// Function
	wire int_fwire_IQ, int_fwire_IQN, int_fwire_r;

	not (int_fwire_r, delayed_RESET_B);
	ihp_latch_r (int_fwire_IQ, notifier, delayed_GATE, delayed_D, int_fwire_r);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (Q_N, int_fwire_IQN);

	// Timing
	specify
		(D => Q) = 0;
		(negedge RESET_B => (Q+:1'b0)) = 0;
		(posedge GATE => (Q+:D)) = 0;
		(D => Q_N) = 0;
		(negedge RESET_B => (Q_N-:1'b0)) = 0;
		(posedge GATE => (Q_N-:D)) = 0;
		$setuphold (negedge GATE, posedge D, 0, 0, notifier,,, delayed_GATE, delayed_D);
		$setuphold (negedge GATE, negedge D, 0, 0, notifier,,, delayed_GATE, delayed_D);
		$recrem (posedge RESET_B, negedge GATE, 0, 0, notifier,,, delayed_RESET_B, delayed_GATE);
		$width (negedge RESET_B, 0, 0, notifier);
		$width (posedge GATE, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type: DLHRQ 
`timescale 1ns/10ps
`celldefine
module sg13g2_dlhrq_1 (Q, D, RESET_B, GATE);
	output Q;
	input D, RESET_B, GATE;
	reg notifier;
	wire delayed_D, delayed_RESET_B, delayed_GATE;

	// Function
	wire int_fwire_IQ, int_fwire_r;

	not (int_fwire_r, delayed_RESET_B);
	ihp_latch_r (int_fwire_IQ, notifier, delayed_GATE, delayed_D, int_fwire_r);
	buf (Q, int_fwire_IQ);

	// Timing
	specify
		(D => Q) = 0;
		(negedge RESET_B => (Q+:1'b0)) = 0;
		(posedge GATE => (Q+:D)) = 0;
		$setuphold (negedge GATE, posedge D, 0, 0, notifier,,, delayed_GATE, delayed_D);
		$setuphold (negedge GATE, negedge D, 0, 0, notifier,,, delayed_GATE, delayed_D);
		$recrem (posedge RESET_B, negedge GATE, 0, 0, notifier,,, delayed_RESET_B, delayed_GATE);
		$width (negedge RESET_B, 0, 0, notifier);
		$width (posedge GATE, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type: DLLR 
`timescale 1ns/10ps
`celldefine
module sg13g2_dllr_1 (Q, Q_N, D, RESET_B, GATE_N);
	output Q, Q_N;
	input D, RESET_B, GATE_N;
	reg notifier;
	wire delayed_D, delayed_RESET_B, delayed_GATE_N;

	// Function
	wire int_fwire_clk, int_fwire_IQ, int_fwire_IQN;
	wire int_fwire_r;

	not (int_fwire_clk, delayed_GATE_N);
	not (int_fwire_r, delayed_RESET_B);
	ihp_latch_r (int_fwire_IQ, notifier, int_fwire_clk, delayed_D, int_fwire_r);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (Q_N, int_fwire_IQN);

	// Timing
	specify
		(D => Q) = 0;
		(negedge RESET_B => (Q+:1'b0)) = 0;
		(negedge GATE_N => (Q+:D)) = 0;
		(D => Q_N) = 0;
		(negedge RESET_B => (Q_N-:1'b0)) = 0;
		(negedge GATE_N => (Q_N-:D)) = 0;
		$setuphold (posedge GATE_N, posedge D, 0, 0, notifier,,, delayed_GATE_N, delayed_D);
		$setuphold (posedge GATE_N, negedge D, 0, 0, notifier,,, delayed_GATE_N, delayed_D);
		$recrem (posedge RESET_B, posedge GATE_N, 0, 0, notifier,,, delayed_RESET_B, delayed_GATE_N);
		$width (negedge RESET_B, 0, 0, notifier);
		$width (negedge GATE_N, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type: DLLRQ 
`timescale 1ns/10ps
`celldefine
module sg13g2_dllrq_1 (Q, D, RESET_B, GATE_N);
	output Q;
	input D, RESET_B, GATE_N;
	reg notifier;
	wire delayed_D, delayed_RESET_B, delayed_GATE_N;

	// Function
	wire int_fwire_clk, int_fwire_IQ, int_fwire_r;

	not (int_fwire_clk, delayed_GATE_N);
	not (int_fwire_r, delayed_RESET_B);
	ihp_latch_r (int_fwire_IQ, notifier, int_fwire_clk, delayed_D, int_fwire_r);
	buf (Q, int_fwire_IQ);

	// Timing
	specify
		(D => Q) = 0;
		(negedge RESET_B => (Q+:1'b0)) = 0;
		(posedge RESET_B => (Q+:1'b1)) = 0;
		(negedge GATE_N => (Q+:D)) = 0;
		$setuphold (posedge GATE_N, posedge D, 0, 0, notifier,,, delayed_GATE_N, delayed_D);
		$setuphold (posedge GATE_N, negedge D, 0, 0, notifier,,, delayed_GATE_N, delayed_D);
		$recrem (posedge RESET_B, posedge GATE_N, 0, 0, notifier,,, delayed_RESET_B, delayed_GATE_N);
		$width (negedge RESET_B, 0, 0, notifier);
		$width (negedge GATE_N, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type: DLY1 
`timescale 1ns/10ps
`celldefine
module sg13g2_dlygate4sd1_1 (X, A);
	output X;
	input A;

	// Function
	buf (X, A);

	// Timing
	specify
		(A => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: DLY2 
`timescale 1ns/10ps
`celldefine
module sg13g2_dlygate4sd2_1 (X, A);
	output X;
	input A;

	// Function
	buf (X, A);

	// Timing
	specify
		(A => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: DLY4 
`timescale 1ns/10ps
`celldefine
module sg13g2_dlygate4sd3_1 (X, A);
	output X;
	input A;

	// Function
	buf (X, A);

	// Timing
	specify
		(A => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: BTL 
`timescale 1ns/10ps
`celldefine
module sg13g2_ebufn_2 (Z, A, TE_B);
	output Z;
	input A, TE_B;

	// Function
	bufif0 (Z, A, TE_B);

	// Timing
	specify
		(A => Z) = 0;
		(TE_B => Z) = 0;
	endspecify
endmodule
`endcelldefine

// type: BTL 
`timescale 1ns/10ps
`celldefine
module sg13g2_ebufn_4 (Z, A, TE_B);
	output Z;
	input A, TE_B;

	// Function
	bufif0 (Z, A, TE_B);

	// Timing
	specify
		(A => Z) = 0;
		(TE_B => Z) = 0;
	endspecify
endmodule
`endcelldefine

// type: BTL 
`timescale 1ns/10ps
`celldefine
module sg13g2_ebufn_8 (Z, A, TE_B);
	output Z;
	input A, TE_B;

	// Function
	bufif0 (Z, A, TE_B);

	// Timing
	specify
		(A => Z) = 0;
		(TE_B => Z) = 0;
	endspecify
endmodule
`endcelldefine

// type: einvin 
`timescale 1ns/10ps
`celldefine
module sg13g2_einvn_2 (Z, A, TE_B);
	output Z;
	input A, TE_B;

	// Function
	notif0 (Z, A, TE_B);

	// Timing
	specify
		(A => Z) = 0;
		(posedge TE_B => (Z:!A)) = 0;
		(negedge TE_B => (Z:!A)) = 0;
	endspecify
endmodule
`endcelldefine

// type: einvin 
`timescale 1ns/10ps
`celldefine
module sg13g2_einvn_4 (Z, A, TE_B);
	output Z;
	input A, TE_B;

	// Function
	notif0 (Z, A, TE_B);

	// Timing
	specify
		(A => Z) = 0;
		(posedge TE_B => (Z:!A)) = 0;
		(negedge TE_B => (Z:!A)) = 0;
	endspecify
endmodule
`endcelldefine

// type: ITL 
`timescale 1ns/10ps
`celldefine
module sg13g2_einvn_8 (Z, A, TE_B);
	output Z;
	input A, TE_B;

	// Function
	notif0 (Z, A, TE_B);

	// Timing
	specify
		(A => Z) = 0;
		(posedge TE_B => (Z:!A)) = 0;
		(negedge TE_B => (Z:!A)) = 0;
	endspecify
endmodule
`endcelldefine

// type: fill 
`timescale 1ns/10ps
`celldefine
module sg13g2_fill_1 ();
	// Timing
	specify
	endspecify
endmodule
`endcelldefine

// type: fill 
`timescale 1ns/10ps
`celldefine
module sg13g2_fill_2 ();
	// Timing
	specify
	endspecify
endmodule
`endcelldefine

// type: fill 
`timescale 1ns/10ps
`celldefine
module sg13g2_fill_4 ();
	// Timing
	specify
	endspecify
endmodule
`endcelldefine

// type: fill 
`timescale 1ns/10ps
`celldefine
module sg13g2_fill_8 ();
	// Timing
	specify
	endspecify
endmodule
`endcelldefine

// type: IN 
`timescale 1ns/10ps
`celldefine
module sg13g2_inv_1 (Y, A);
	output Y;
	input A;

	// Function
	not (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: IN 
`timescale 1ns/10ps
`celldefine
module sg13g2_inv_16 (Y, A);
	output Y;
	input A;

	// Function
	not (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: IN 
`timescale 1ns/10ps
`celldefine
module sg13g2_inv_2 (Y, A);
	output Y;
	input A;

	// Function
	not (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: IN 
`timescale 1ns/10ps
`celldefine
module sg13g2_inv_4 (Y, A);
	output Y;
	input A;

	// Function
	not (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: IN 
`timescale 1ns/10ps
`celldefine
module sg13g2_inv_8 (Y, A);
	output Y;
	input A;

	// Function
	not (Y, A);

	// Timing
	specify
		(A => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: gclk 
`timescale 1ns/10ps
`celldefine
module sg13g2_lgcp_1 (GCLK, GATE, CLK);
	output GCLK;
	input GATE, CLK;
	reg notifier;
	wire delayed_GATE, delayed_CLK;

	// Function
	wire int_fwire_clk, int_fwire_int_GATE;

	not (int_fwire_clk, delayed_CLK);
	ihp_latch (int_fwire_int_GATE, notifier, int_fwire_clk, delayed_GATE);
	and (GCLK, delayed_CLK, int_fwire_int_GATE);

	// Timing
	specify
		(CLK => GCLK) = 0;
		$setuphold (posedge CLK, posedge GATE, 0, 0, notifier,,, delayed_CLK, delayed_GATE);
		$setuphold (posedge CLK, negedge GATE, 0, 0, notifier,,, delayed_CLK, delayed_GATE);
		$width (posedge CLK, 0, 0, notifier);
		$width (negedge CLK, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type: mux2 
`timescale 1ns/10ps
`celldefine
module sg13g2_mux2_1 (X, A0, A1, S);
	output X;
	input A0, A1, S;

	// Function
	ihp_mux2 (X, A0, A1, S);

	// Timing
	specify
		(A0 => X) = 0;
		(A1 => X) = 0;
		if (A0 == 1'b0 & A1 == 1'b1)
			(S => X) = 0;
		ifnone (S => X) = 0;
		if (A0 == 1'b1 & A1 == 1'b0)
			(S => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: mux2 
`timescale 1ns/10ps
`celldefine
module sg13g2_mux2_2 (X, A0, A1, S);
	output X;
	input A0, A1, S;

	// Function
	ihp_mux2 (X, A0, A1, S);

	// Timing
	specify
		(A0 => X) = 0;
		(A1 => X) = 0;
		if (A0 == 1'b0 & A1 == 1'b1)
			(S => X) = 0;
		ifnone (S => X) = 0;
		if (A0 == 1'b1 & A1 == 1'b0)
			(S => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: mux4 
`timescale 1ns/10ps
`celldefine
module sg13g2_mux4_1 (X, A0, A1, A2, A3, S0, S1);
	output X;
	input A0, A1, A2, A3, S0, S1;

	// Function
	ihp_mux4 (X, A0, A1, A2, A3, S0, S1);

	// Timing
	specify
		(A0 => X) = 0;
		(A1 => X) = 0;
		(A2 => X) = 0;
		(A3 => X) = 0;
		if (A2 == 1'b0 & A3 == 1'b1 & S1 == 1'b1)
			(S0 => X) = 0;
		if (A0 == 1'b0 & A1 == 1'b1 & S1 == 1'b0)
			(S0 => X) = 0;
		ifnone (S0 => X) = 0;
		if (A2 == 1'b1 & A3 == 1'b0 & S1 == 1'b1)
			(S0 => X) = 0;
		if (A0 == 1'b1 & A1 == 1'b0 & S1 == 1'b0)
			(S0 => X) = 0;
		if (A1 == 1'b0 & A3 == 1'b1 & S0 == 1'b1)
			(S1 => X) = 0;
		if (A0 == 1'b0 & A2 == 1'b1 & S0 == 1'b0)
			(S1 => X) = 0;
		ifnone (S1 => X) = 0;
		if (A1 == 1'b1 & A3 == 1'b0 & S0 == 1'b1)
			(S1 => X) = 0;
		if (A0 == 1'b1 & A2 == 1'b0 & S0 == 1'b0)
			(S1 => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: nand2 
`timescale 1ns/10ps
`celldefine
module sg13g2_nand2_1 (Y, A, B);
	output Y;
	input A, B;

	// Function
	wire int_fwire_0;

	and (int_fwire_0, A, B);
	not (Y, int_fwire_0);

	// Timing
	specify
		(A => Y) = 0;
		(B => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: nand2 
`timescale 1ns/10ps
`celldefine
module sg13g2_nand2_2 (Y, A, B);
	output Y;
	input A, B;

	// Function
	wire int_fwire_0;

	and (int_fwire_0, A, B);
	not (Y, int_fwire_0);

	// Timing
	specify
		(A => Y) = 0;
		(B => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: nand2b1 
`timescale 1ns/10ps
`celldefine
module sg13g2_nand2b_1 (Y, A_N, B);
	output Y;
	input A_N, B;

	// Function
	wire A_N__bar, int_fwire_0;

	not (A_N__bar, A_N);
	and (int_fwire_0, A_N__bar, B);
	not (Y, int_fwire_0);

	// Timing
	specify
		(A_N => Y) = 0;
		(B => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: nand2b2 
`timescale 1ns/10ps
`celldefine
module sg13g2_nand2b_2 (Y, A_N, B);
	output Y;
	input A_N, B;

	// Function
	wire A_N__bar, int_fwire_0;

	not (A_N__bar, A_N);
	and (int_fwire_0, A_N__bar, B);
	not (Y, int_fwire_0);

	// Timing
	specify
		(A_N => Y) = 0;
		(B => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: nand3 
`timescale 1ns/10ps
`celldefine
module sg13g2_nand3_1 (Y, A, B, C);
	output Y;
	input A, B, C;

	// Function
	wire int_fwire_0;

	and (int_fwire_0, A, B, C);
	not (Y, int_fwire_0);

	// Timing
	specify
		(A => Y) = 0;
		(B => Y) = 0;
		(C => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: nand3b1 
`timescale 1ns/10ps
`celldefine
module sg13g2_nand3b_1 (Y, A_N, B, C);
	output Y;
	input A_N, B, C;

	// Function
	wire A_N__bar, int_fwire_0;

	not (A_N__bar, A_N);
	and (int_fwire_0, A_N__bar, B, C);
	not (Y, int_fwire_0);

	// Timing
	specify
		(A_N => Y) = 0;
		(B => Y) = 0;
		(C => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: nand4 
`timescale 1ns/10ps
`celldefine
module sg13g2_nand4_1 (Y, A, B, C, D);
	output Y;
	input A, B, C, D;

	// Function
	wire int_fwire_0;

	and (int_fwire_0, A, B, C, D);
	not (Y, int_fwire_0);

	// Timing
	specify
		(A => Y) = 0;
		(B => Y) = 0;
		(C => Y) = 0;
		(D => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: nor2 
`timescale 1ns/10ps
`celldefine
module sg13g2_nor2_1 (Y, A, B);
	output Y;
	input A, B;

	// Function
	wire int_fwire_0;

	or (int_fwire_0, A, B);
	not (Y, int_fwire_0);

	// Timing
	specify
		(A => Y) = 0;
		(B => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: nor2 
`timescale 1ns/10ps
`celldefine
module sg13g2_nor2_2 (Y, A, B);
	output Y;
	input A, B;

	// Function
	wire int_fwire_0;

	or (int_fwire_0, A, B);
	not (Y, int_fwire_0);

	// Timing
	specify
		(A => Y) = 0;
		(B => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: nor2b 
`timescale 1ns/10ps
`celldefine
module sg13g2_nor2b_1 (Y, A, B_N);
	output Y;
	input A, B_N;

	// Function
	wire B_N__bar, int_fwire_0;

	not (B_N__bar, B_N);
	or (int_fwire_0, A, B_N__bar);
	not (Y, int_fwire_0);

	// Timing
	specify
		(A => Y) = 0;
		(B_N => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: nor2b 
`timescale 1ns/10ps
`celldefine
module sg13g2_nor2b_2 (Y, A, B_N);
	output Y;
	input A, B_N;

	// Function
	wire B_N__bar, int_fwire_0;

	not (B_N__bar, B_N);
	or (int_fwire_0, A, B_N__bar);
	not (Y, int_fwire_0);

	// Timing
	specify
		(A => Y) = 0;
		(B_N => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: nor3 
`timescale 1ns/10ps
`celldefine
module sg13g2_nor3_1 (Y, A, B, C);
	output Y;
	input A, B, C;

	// Function
	wire int_fwire_0;

	or (int_fwire_0, A, B, C);
	not (Y, int_fwire_0);

	// Timing
	specify
		(A => Y) = 0;
		(B => Y) = 0;
		(C => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: nor3 
`timescale 1ns/10ps
`celldefine
module sg13g2_nor3_2 (Y, A, B, C);
	output Y;
	input A, B, C;

	// Function
	wire int_fwire_0;

	or (int_fwire_0, A, B, C);
	not (Y, int_fwire_0);

	// Timing
	specify
		(A => Y) = 0;
		(B => Y) = 0;
		(C => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: nor4 
`timescale 1ns/10ps
`celldefine
module sg13g2_nor4_1 (Y, A, B, C, D);
	output Y;
	input A, B, C, D;

	// Function
	wire int_fwire_0;

	or (int_fwire_0, A, B, C, D);
	not (Y, int_fwire_0);

	// Timing
	specify
		(A => Y) = 0;
		(B => Y) = 0;
		(C => Y) = 0;
		(D => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: nor4 
`timescale 1ns/10ps
`celldefine
module sg13g2_nor4_2 (Y, A, B, C, D);
	output Y;
	input A, B, C, D;

	// Function
	wire int_fwire_0;

	or (int_fwire_0, A, B, C, D);
	not (Y, int_fwire_0);

	// Timing
	specify
		(A => Y) = 0;
		(B => Y) = 0;
		(C => Y) = 0;
		(D => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: o21ai 
`timescale 1ns/10ps
`celldefine
module sg13g2_o21ai_1 (Y, A1, A2, B1);
	output Y;
	input A1, A2, B1;

	// Function
	wire int_fwire_0, int_fwire_1;

	or (int_fwire_0, A1, A2);
	and (int_fwire_1, int_fwire_0, B1);
	not (Y, int_fwire_1);

	// Timing
	specify
		(A1 => Y) = 0;
		(A2 => Y) = 0;
		if (A1 == 1'b1 & A2 == 1'b0)
			(B1 => Y) = 0;
		if (A1 == 1'b0 & A2 == 1'b1)
			(B1 => Y) = 0;
		ifnone (B1 => Y) = 0;
	endspecify
endmodule
`endcelldefine

// type: or2 
`timescale 1ns/10ps
`celldefine
module sg13g2_or2_1 (X, A, B);
	output X;
	input A, B;

	// Function
	or (X, A, B);

	// Timing
	specify
		(A => X) = 0;
		(B => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: or2 
`timescale 1ns/10ps
`celldefine
module sg13g2_or2_2 (X, A, B);
	output X;
	input A, B;

	// Function
	or (X, A, B);

	// Timing
	specify
		(A => X) = 0;
		(B => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: or3 
`timescale 1ns/10ps
`celldefine
module sg13g2_or3_1 (X, A, B, C);
	output X;
	input A, B, C;

	// Function
	or (X, A, B, C);

	// Timing
	specify
		(A => X) = 0;
		(B => X) = 0;
		(C => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: or3 
`timescale 1ns/10ps
`celldefine
module sg13g2_or3_2 (X, A, B, C);
	output X;
	input A, B, C;

	// Function
	or (X, A, B, C);

	// Timing
	specify
		(A => X) = 0;
		(B => X) = 0;
		(C => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: or4 
`timescale 1ns/10ps
`celldefine
module sg13g2_or4_1 (X, A, B, C, D);
	output X;
	input A, B, C, D;

	// Function
	or (X, A, B, C, D);

	// Timing
	specify
		(A => X) = 0;
		(B => X) = 0;
		(C => X) = 0;
		(D => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: or4 
`timescale 1ns/10ps
`celldefine
module sg13g2_or4_2 (X, A, B, C, D);
	output X;
	input A, B, C, D;

	// Function
	or (X, A, B, C, D);

	// Timing
	specify
		(A => X) = 0;
		(B => X) = 0;
		(C => X) = 0;
		(D => X) = 0;
	endspecify
endmodule
`endcelldefine

// type: sdfrrs 
`timescale 1ns/10ps
`celldefine
module sg13g2_sdfbbp_1 (Q, Q_N, D, SCD, SCE, RESET_B, SET_B, CLK);
	output Q, Q_N;
	input D, SCD, SCE, RESET_B, SET_B, CLK;
	reg notifier;
	wire delayed_D, delayed_SCD, delayed_SCE, delayed_RESET_B, delayed_SET_B, delayed_CLK;

	// Function
	wire int_fwire_d, int_fwire_IQ, int_fwire_IQN;
	wire int_fwire_r, int_fwire_s, xcr_0;

	ihp_mux2 (int_fwire_d, delayed_D, delayed_SCD, delayed_SCE);
	not (int_fwire_s, delayed_SET_B);
	not (int_fwire_r, delayed_RESET_B);
	ihp_dff_sr_err (xcr_0, delayed_CLK, int_fwire_d, int_fwire_s, int_fwire_r);
	ihp_dff_sr_1 (int_fwire_IQ, notifier, delayed_CLK, int_fwire_d, int_fwire_s, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (Q_N, int_fwire_IQN);

	// Timing
	specify
		(negedge RESET_B => (Q+:1'b0)) = 0;
		(negedge SET_B => (Q+:1'b1)) = 0;
		if (SCE == 1'b1)
			(posedge CLK => (Q+:((D && SCD) || (D && !SCD && !SCE) || (!D && SCD && SCE)))) = 0;
		ifnone (posedge CLK => (Q+:((D && SCD) || (D && !SCD && !SCE) || (!D && SCD && SCE)))) = 0;
		(negedge RESET_B => (Q_N-:1'b0)) = 0;
		(negedge SET_B => (Q_N-:1'b1)) = 0;
		if (SCE == 1'b1)
			(posedge CLK => (Q_N-:((D && SCD) || (D && !SCD && !SCE) || (!D && SCD && SCE)))) = 0;
		ifnone (posedge CLK => (Q_N-:((D && SCD) || (D && !SCD && !SCE) || (!D && SCD && SCE)))) = 0;
		$setuphold (posedge CLK, posedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, negedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, posedge SCD, 0, 0, notifier,,, delayed_CLK, delayed_SCD);
		$setuphold (posedge CLK, negedge SCD, 0, 0, notifier,,, delayed_CLK, delayed_SCD);
		$setuphold (posedge CLK, posedge SCE, 0, 0, notifier,,, delayed_CLK, delayed_SCE);
		$setuphold (posedge CLK, negedge SCE, 0, 0, notifier,,, delayed_CLK, delayed_SCE);
		$recrem (posedge RESET_B, posedge CLK, 0, 0, notifier,,, delayed_RESET_B, delayed_CLK);
		$recrem (posedge SET_B, posedge CLK, 0, 0, notifier,,, delayed_SET_B, delayed_CLK);
		$setuphold (posedge RESET_B, posedge SET_B, 0, 0, notifier,,, delayed_RESET_B, delayed_SET_B);
		$width (negedge RESET_B, 0, 0, notifier);
		$width (negedge SET_B, 0, 0, notifier);
		$width (posedge CLK, 0, 0, notifier);
		$width (negedge CLK, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type: keepstate 
`timescale 1ns/10ps
`celldefine
module sg13g2_sighold (SH);
	inout SH;
	// Missing function for pin SH
	// Timing
	specify
	endspecify
endmodule
`endcelldefine

// type: sgclk 
`timescale 1ns/10ps
`celldefine
module sg13g2_slgcp_1 (GCLK, GATE, SCE, CLK);
	output GCLK;
	input GATE, SCE, CLK;
	reg notifier;
	wire delayed_GATE, delayed_SCE, delayed_CLK;

	// Function
	wire int_fwire_clk, int_fwire_int_GATE, int_fwire_test;

	not (int_fwire_clk, delayed_CLK);
	or (int_fwire_test, delayed_GATE, delayed_SCE);
	ihp_latch (int_fwire_int_GATE, notifier, int_fwire_clk, int_fwire_test);
	and (GCLK, delayed_CLK, int_fwire_int_GATE);

	// Timing
	specify
		(CLK => GCLK) = 0;
		$setuphold (posedge CLK, posedge GATE, 0, 0, notifier,,, delayed_CLK, delayed_GATE);
		$setuphold (posedge CLK, negedge GATE, 0, 0, notifier,,, delayed_CLK, delayed_GATE);
		$setuphold (posedge CLK, posedge SCE, 0, 0, notifier,,, delayed_CLK, delayed_SCE);
		$setuphold (posedge CLK, negedge SCE, 0, 0, notifier,,, delayed_CLK, delayed_SCE);
		$width (posedge CLK, 0, 0, notifier);
		$width (negedge CLK, 0, 0, notifier);
	endspecify
endmodule
`endcelldefine

// type: tie1 
`timescale 1ns/10ps
`celldefine
module sg13g2_tiehi (L_HI);
	output L_HI;

	// Function
	buf (L_HI, 1'b1);

	// Timing
	specify
	endspecify
endmodule
`endcelldefine

// type: tie0 
`timescale 1ns/10ps
`celldefine
module sg13g2_tielo (L_LO);
	output L_LO;

	// Function
	buf (L_LO, 1'b0);

	// Timing
	specify
	endspecify
endmodule
`endcelldefine

// type: xnor2_1 
`timescale 1ns/10ps
`celldefine
module sg13g2_xnor2_1 (Y, A, B);
	output Y;
	input A, B;

	// Function
	wire int_fwire_0;

	xor (int_fwire_0, A, B);
	not (Y, int_fwire_0);

	// Timing
	specify
		(posedge A => (Y:A)) = 0;
		(negedge A => (Y:A)) = 0;
		(posedge B => (Y:B)) = 0;
		(negedge B => (Y:B)) = 0;
	endspecify
endmodule
`endcelldefine

// type: xor2_1 
`timescale 1ns/10ps
`celldefine
module sg13g2_xor2_1 (X, A, B);
	output X;
	input A, B;

	// Function
	xor (X, A, B);

	// Timing
	specify
		(posedge A => (X:A)) = 0;
		(negedge A => (X:A)) = 0;
		(posedge B => (X:B)) = 0;
		(negedge B => (X:B)) = 0;
	endspecify
endmodule
`endcelldefine


`ifdef _udp_def_ihp_latch_
`else
`define _udp_def_ihp_latch_
primitive ihp_latch (q, v, clk, d);
	output q;
	reg q;
	input v, clk, d;

	table
		* ? ? : ? : x;
		? 1 0 : ? : 0;
		? 1 1 : ? : 1;
		? x 0 : 0 : -;
		? x 1 : 1 : -;
		? 0 ? : ? : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_ihp_dff_err_
`else
`define _udp_def_ihp_dff_err_
primitive ihp_dff_err (q, clk, d);
	output q;
	reg q;
	input clk, d;

	table
		(0x) ? : ? : 0;
		(1x) ? : ? : 1;
	endtable
endprimitive
`endif

`ifdef _udp_def_ihp_dff_
`else
`define _udp_def_ihp_dff_
primitive ihp_dff (q, v, clk, d, xcr);
	output q;
	reg q;
	input v, clk, d, xcr;

	table
		*  ?   ? ? : ? : x;
		? (x1) 0 0 : ? : 0;
		? (x1) 1 0 : ? : 1;
		? (x1) 0 1 : 0 : 0;
		? (x1) 1 1 : 1 : 1;
		? (x1) ? x : ? : -;
		? (bx) 0 ? : 0 : -;
		? (bx) 1 ? : 1 : -;
		? (x0) b ? : ? : -;
		? (x0) ? x : ? : -;
		? (01) 0 ? : ? : 0;
		? (01) 1 ? : ? : 1;
		? (10) ? ? : ? : -;
		?  b   * ? : ? : -;
		?  ?   ? * : ? : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_ihp_dff_r_err_
`else
`define _udp_def_ihp_dff_r_err_
primitive ihp_dff_r_err (q, clk, d, r);
	output q;
	reg q;
	input clk, d, r;

	table
		 ?   0 (0x) : ? : -;
		 ?   0 (x0) : ? : -;
		(0x) ?  0   : ? : 0;
		(0x) 0  x   : ? : 0;
		(1x) ?  0   : ? : 1;
		(1x) 0  x   : ? : 1;
	endtable
endprimitive
`endif

`ifdef _udp_def_ihp_dff_r_
`else
`define _udp_def_ihp_dff_r_
primitive ihp_dff_r (q, v, clk, d, r, xcr);
	output q;
	reg q;
	input v, clk, d, r, xcr;

	table
		*  ?   ?  ?   ? : ? : x;
		?  ?   ?  1   ? : ? : 0;
		?  b   ? (1?) ? : 0 : -;
		?  x   0 (1?) ? : 0 : -;
		?  ?   ? (10) ? : ? : -;
		?  ?   ? (x0) ? : ? : -;
		?  ?   ? (0x) ? : 0 : -;
		? (x1) 0  ?   0 : ? : 0;
		? (x1) 1  0   0 : ? : 1;
		? (x1) 0  ?   1 : 0 : 0;
		? (x1) 1  0   1 : 1 : 1;
		? (x1) ?  ?   x : ? : -;
		? (bx) 0  ?   ? : 0 : -;
		? (bx) 1  0   ? : 1 : -;
		? (x0) 0  ?   ? : ? : -;
		? (x0) 1  0   ? : ? : -;
		? (x0) ?  0   x : ? : -;
		? (01) 0  ?   ? : ? : 0;
		? (01) 1  0   ? : ? : 1;
		? (10) ?  ?   ? : ? : -;
		?  b   *  ?   ? : ? : -;
		?  ?   ?  ?   * : ? : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_ihp_dff_s_err_
`else
`define _udp_def_ihp_dff_s_err_
primitive ihp_dff_s_err (q, clk, d, s);
	output q;
	reg q;
	input clk, d, s;

	table
		 ?   1 (0x) : ? : -;
		 ?   1 (x0) : ? : -;
		(0x) ?  0   : ? : 0;
		(0x) 1  x   : ? : 0;
		(1x) ?  0   : ? : 1;
		(1x) 1  x   : ? : 1;
	endtable
endprimitive
`endif

`ifdef _udp_def_ihp_dff_s_
`else
`define _udp_def_ihp_dff_s_
primitive ihp_dff_s (q, v, clk, d, s, xcr);
	output q;
	reg q;
	input v, clk, d, s, xcr;

	table
		*  ?   ?  ?   ? : ? : x;
		?  ?   ?  1   ? : ? : 1;
		?  b   ? (1?) ? : 1 : -;
		?  x   1 (1?) ? : 1 : -;
		?  ?   ? (10) ? : ? : -;
		?  ?   ? (x0) ? : ? : -;
		?  ?   ? (0x) ? : 1 : -;
		? (x1) 0  0   0 : ? : 0;
		? (x1) 1  ?   0 : ? : 1;
		? (x1) 1  ?   1 : 1 : 1;
		? (x1) 0  0   1 : 0 : 0;
		? (x1) ?  ?   x : ? : -;
		? (bx) 1  ?   ? : 1 : -;
		? (bx) 0  0   ? : 0 : -;
		? (x0) 1  ?   ? : ? : -;
		? (x0) 0  0   ? : ? : -;
		? (x0) ?  0   x : ? : -;
		? (01) 1  ?   ? : ? : 1;
		? (01) 0  0   ? : ? : 0;
		? (10) ?  ?   ? : ? : -;
		?  b   *  ?   ? : ? : -;
		?  ?   ?  ?   * : ? : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_ihp_dff_sr_err_
`else
`define _udp_def_ihp_dff_sr_err_
primitive ihp_dff_sr_err (q, clk, d, s, r);
	output q;
	reg q;
	input clk, d, s, r;

	table
		 ?   1 (0x)  ?   : ? : -;
		 ?   0  ?   (0x) : ? : -;
		 ?   0  ?   (x0) : ? : -;
		(0x) ?  0    0   : ? : 0;
		(0x) 1  x    0   : ? : 0;
		(0x) 0  0    x   : ? : 0;
		(1x) ?  0    0   : ? : 1;
		(1x) 1  x    0   : ? : 1;
		(1x) 0  0    x   : ? : 1;
	endtable
endprimitive
`endif

`ifdef _udp_def_ihp_dff_sr_0
`else
`define _udp_def_ihp_dff_sr_0
primitive ihp_dff_sr_0 (q, v, clk, d, s, r, xcr);
	output q;
	reg q;
	input v, clk, d, s, r, xcr;

	table
	//	v,  clk, d, s, r : q' : q;

		*  ?   ?   ?   ?   ? : ? : x;
		?  ?   ?   ?   1   ? : ? : 0;
		?  ?   ?   1   0   ? : ? : 1;
		?  b   ? (1?)  0   ? : 1 : -;
		?  x   1 (1?)  0   ? : 1 : -;
		?  ?   ? (10)  0   ? : ? : -;
		?  ?   ? (x0)  0   ? : ? : -;
		?  ?   ? (0x)  0   ? : 1 : -;
		?  b   ?  0   (1?) ? : 0 : -;
		?  x   0  0   (1?) ? : 0 : -;
		?  ?   ?  0   (10) ? : ? : -;
		?  ?   ?  0   (x0) ? : ? : -;
		?  ?   ?  0   (0x) ? : 0 : -;
		? (x1) 0  0    ?   0 : ? : 0;
		? (x1) 1  ?    0   0 : ? : 1;
		? (x1) 0  0    ?   1 : 0 : 0;
		? (x1) 1  ?    0   1 : 1 : 1;
		? (x1) ?  ?    0   x : ? : -;
		? (x1) ?  0    ?   x : ? : -;
		? (1x) 0  0    ?   ? : 0 : -;
		? (1x) 1  ?    0   ? : 1 : -;
		? (x0) 0  0    ?   ? : ? : -;
		? (x0) 1  ?    0   ? : ? : -;
		? (x0) ?  0    0   x : ? : -;
		? (0x) 0  0    ?   ? : 0 : -;
		? (0x) 1  ?    0   ? : 1 : -;
		? (01) 0  0    ?   ? : ? : 0;
		? (01) 1  ?    0   ? : ? : 1;
		? (10) ?  0    ?   ? : ? : -;
		? (10) ?  ?    0   ? : ? : -;
		?  b   *  0    ?   ? : ? : -;
		?  b   *  ?    0   ? : ? : -;
		?  ?   ?  ?    ?   * : ? : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_ihp_dff_sr_1
`else
`define _udp_def_ihp_dff_sr_1
primitive ihp_dff_sr_1 (q, v, clk, d, s, r, xcr);
	output q;
	reg q;
	input v, clk, d, s, r, xcr;

	table
	//	v,  clk, d, s, r : q' : q;

		*  ?   ?   ?   ?   ? : ? : x;
		?  ?   ?   0   1   ? : ? : 0;
		?  ?   ?   1   ?   ? : ? : 1;
		?  b   ? (1?)  0   ? : 1 : -;
		?  x   1 (1?)  0   ? : 1 : -;
		?  ?   ? (10)  0   ? : ? : -;
		?  ?   ? (x0)  0   ? : ? : -;
		?  ?   ? (0x)  0   ? : 1 : -;
		?  b   ?  0   (1?) ? : 0 : -;
		?  x   0  0   (1?) ? : 0 : -;
		?  ?   ?  0   (10) ? : ? : -;
		?  ?   ?  0   (x0) ? : ? : -;
		?  ?   ?  0   (0x) ? : 0 : -;
		? (x1) 0  0    ?   0 : ? : 0;
		? (x1) 1  ?    0   0 : ? : 1;
		? (x1) 0  0    ?   1 : 0 : 0;
		? (x1) 1  ?    0   1 : 1 : 1;
		? (x1) ?  ?    0   x : ? : -;
		? (x1) ?  0    ?   x : ? : -;
		? (1x) 0  0    ?   ? : 0 : -;
		? (1x) 1  ?    0   ? : 1 : -;
		? (x0) 0  0    ?   ? : ? : -;
		? (x0) 1  ?    0   ? : ? : -;
		? (x0) ?  0    0   x : ? : -;
		? (0x) 0  0    ?   ? : 0 : -;
		? (0x) 1  ?    0   ? : 1 : -;
		? (01) 0  0    ?   ? : ? : 0;
		? (01) 1  ?    0   ? : ? : 1;
		? (10) ?  0    ?   ? : ? : -;
		? (10) ?  ?    0   ? : ? : -;
		?  b   *  0    ?   ? : ? : -;
		?  b   *  ?    0   ? : ? : -;
		?  ?   ?  ?    ?   * : ? : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_ihp_latch_r_
`else
`define _udp_def_ihp_latch_r_
primitive ihp_latch_r (q, v, clk, d, r);
	output q;
	reg q;
	input v, clk, d, r;

	table
		* ? ? ? : ? : x;
		? ? ? 1 : ? : 0;
		? 0 ? 0 : ? : -;
		? 0 ? x : 0 : -;
		? 1 0 0 : ? : 0;
		? 1 0 x : ? : 0;
		? 1 1 0 : ? : 1;
		? x 0 0 : 0 : -;
		? x 0 x : 0 : -;
		? x 1 0 : 1 : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_ihp_latch_s_
`else
`define _udp_def_ihp_latch_s_
primitive ihp_latch_s (q, v, clk, d, s);
	output q;
	reg q;
	input v, clk, d, s;

	table
		* ? ? ? : ? : x;
		? ? ? 1 : ? : 1;
		? 0 ? 0 : ? : -;
		? 0 ? x : 1 : -;
		? 1 1 0 : ? : 1;
		? 1 1 x : ? : 1;
		? 1 0 0 : ? : 0;
		? x 1 0 : 1 : -;
		? x 1 x : 1 : -;
		? x 0 0 : 0 : -;
	endtable
endprimitive
`endif

`ifdef _udp_def_ihp_latch_sr_0
`else
`define _udp_def_ihp_latch_sr_0
primitive ihp_latch_sr_0 (q, v, clk, d, s, r);
	output q;
	reg q;
	input v, clk, d, s, r;

	table
		* ? ? ? ? : ? : x;
		? 1 1 ? 0 : ? : 1;
		? 1 0 0 ? : ? : 0;
		? ? ? 1 0 : ? : 1;
		? ? ? ? 1 : ? : 0;
		? 0 * ? ? : ? : -;
		? 0 ? * 0 : 1 : 1;
		? 0 ? 0 * : 0 : 0;
		? * 1 ? 0 : 1 : 1;
		? * 0 0 ? : 0 : 0;
		? ? 1 * 0 : 1 : 1;
		? ? 0 0 * : 0 : 0;
	endtable
endprimitive
`endif

`ifdef _udp_def_ihp_latch_sr_1
`else
`define _udp_def_ihp_latch_sr_1
primitive ihp_latch_sr_1 (q, v, clk, d, s, r);
	output q;
	reg q;
	input v, clk, d, s, r;

	table
		* ? ? ? ? : ? : x;
		? 1 1 ? 0 : ? : 1;
		? 1 0 0 ? : ? : 0;
		? ? ? 1 ? : ? : 1;
		? ? ? 0 1 : ? : 0;
		? 0 * ? ? : ? : -;
		? 0 ? * 0 : 1 : 1;
		? 0 ? 0 * : 0 : 0;
		? * 1 ? 0 : 1 : 1;
		? * 0 0 ? : 0 : 0;
		? ? 1 * 0 : 1 : 1;
		? ? 0 0 * : 0 : 0;
	endtable
endprimitive
`endif

`ifdef _udp_def_ihp_mux2
`else
`define _udp_def_ihp_mux2
primitive ihp_mux2 (z, a, b, s);
	output z;
	input a, b, s;

	table
//                 a  b  s : z
                   1  ?  0 : 1;
                   0  ?  0 : 0;
                   ?  1  1 : 1;
                   ?  0  1 : 0;
                   0  0  x : 0;
                   1  1  x : 1;
	endtable
endprimitive
`endif

`ifdef _udp_def_ihp_mux4
`else
`define _udp_def_ihp_mux4
primitive ihp_mux4 (z, a, b , c, d, s0, s1);
	output z;
	input d, c, b, a, s1, s0;

	table
//                a  b  c  d s0 s1 : z
                  0  ?  ?  ?  0  0 : 0;
                  1  ?  ?  ?  0  0 : 1;
                  ?  0  ?  ?  1  0 : 0;
                  ?  1  ?  ?  1  0 : 1;
                  ?  ?  0  ?  0  1 : 0;
                  ?  ?  1  ?  0  1 : 1;
                  ?  ?  ?  0  1  1 : 0;
                  ?  ?  ?  1  1  1 : 1;
                  0  0  ?  ?  x  0 : 0;
                  1  1  ?  ?  x  0 : 1;
                  ?  ?  0  0  x  1 : 0;
                  ?  ?  1  1  x  1 : 1;
                  0  ?  0  ?  0  x : 0;
                  1  ?  1  ?  0  x : 1;
                  ?  0  ?  0  1  x : 0;
                  ?  1  ?  1  1  x : 1;
                  1  1  1  1  x  x : 1;
                  0  0  0  0  x  x : 0;
	endtable
endprimitive
`endif

`ifdef _udp_def_ihp_mux8
`else
`define _udp_def_ihp_mux8
primitive ihp_mux8 (z, a, b , c, d, e, f, g, h, s0, s1, s2);
	output z;
	input h, g, f, e, d, c, b, a, s2, s1, s0;

	table
//                a  b  c  d  e  f  g  h s0 s1 s2 : z
                  0  ?  ?  ?  ?  ?  ?  ?  0  0  0 : 0;
                  1  ?  ?  ?  ?  ?  ?  ?  0  0  0 : 1;
                  ?  0  ?  ?  ?  ?  ?  ?  1  0  0 : 0;
                  ?  1  ?  ?  ?  ?  ?  ?  1  0  0 : 1;
                  ?  ?  0  ?  ?  ?  ?  ?  0  1  0 : 0;
                  ?  ?  1  ?  ?  ?  ?  ?  0  1  0 : 1;
                  ?  ?  ?  0  ?  ?  ?  ?  1  1  0 : 0;
                  ?  ?  ?  1  ?  ?  ?  ?  1  1  0 : 1;
                  ?  ?  ?  ?  0  ?  ?  ?  0  0  1 : 0;
                  ?  ?  ?  ?  1  ?  ?  ?  0  0  1 : 1;
                  ?  ?  ?  ?  ?  0  ?  ?  1  0  1 : 0;
                  ?  ?  ?  ?  ?  1  ?  ?  1  0  1 : 1;
                  ?  ?  ?  ?  ?  ?  0  ?  0  1  1 : 0;
                  ?  ?  ?  ?  ?  ?  1  ?  0  1  1 : 1;
                  ?  ?  ?  ?  ?  ?  ?  0  1  1  1 : 0;
                  ?  ?  ?  ?  ?  ?  ?  1  1  1  1 : 1;
                  0  0  ?  ?  ?  ?  ?  ?  x  0  0 : 0;
                  1  1  ?  ?  ?  ?  ?  ?  x  0  0 : 1;
                  ?  ?  0  0  ?  ?  ?  ?  x  1  0 : 0;
                  ?  ?  1  1  ?  ?  ?  ?  x  1  0 : 1;
                  ?  ?  ?  ?  0  0  ?  ?  x  0  1 : 0;
                  ?  ?  ?  ?  1  1  ?  ?  x  0  1 : 1;
                  ?  ?  ?  ?  ?  ?  0  0  x  1  1 : 0;
                  ?  ?  ?  ?  ?  ?  1  1  x  1  1 : 1;
                  0  ?  0  ?  ?  ?  ?  ?  0  x  0 : 0;
                  1  ?  1  ?  ?  ?  ?  ?  0  x  0 : 1;
                  ?  0  ?  0  ?  ?  ?  ?  1  x  0 : 0;
                  ?  1  ?  1  ?  ?  ?  ?  1  x  0 : 1;
                  ?  ?  ?  ?  0  ?  0  ?  0  x  1 : 0;
                  ?  ?  ?  ?  1  ?  1  ?  0  x  1 : 1;
                  ?  ?  ?  ?  ?  0  ?  0  1  x  1 : 0;
                  ?  ?  ?  ?  ?  1  ?  1  1  x  1 : 1;
                  0  ?  ?  ?  0  ?  ?  ?  0  0  x : 0;
                  1  ?  ?  ?  1  ?  ?  ?  0  0  x : 1;
                  ?  0  ?  ?  ?  0  ?  ?  1  0  x : 0;
                  ?  1  ?  ?  ?  1  ?  ?  1  0  x : 1;
                  ?  ?  0  ?  ?  ?  0  ?  0  1  x : 0;
                  ?  ?  1  ?  ?  ?  1  ?  0  1  x : 1;
                  ?  ?  ?  0  ?  ?  ?  0  1  1  x : 0;
                  ?  ?  ?  1  ?  ?  ?  1  1  1  x : 1;
                  0  0  0  0  ?  ?  ?  ?  x  x  0 : 0;
                  1  1  1  1  ?  ?  ?  ?  x  x  0 : 1;
                  ?  ?  ?  ?  0  0  0  0  x  x  1 : 0;
                  ?  ?  ?  ?  1  1  1  1  x  x  1 : 1;
                  0  0  ?  ?  0  0  ?  ?  x  0  x : 0;
                  1  1  ?  ?  1  1  ?  ?  x  0  x : 1;
                  ?  ?  0  0  ?  ?  0  0  x  1  x : 0;
                  ?  ?  1  1  ?  ?  1  1  x  1  x : 1;
                  0  ?  0  ?  0  ?  0  ?  0  x  x : 0;
                  1  ?  1  ?  1  ?  1  ?  0  x  x : 1;
                  ?  0  ?  0  ?  0  ?  0  1  x  x : 0;
                  ?  1  ?  1  ?  1  ?  1  1  x  x : 1;
                  0  0  0  0  0  0  0  0  x  x  x : 0;
                  1  1  1  1  1  1  1  1  x  x  x : 1;
	endtable
endprimitive
`endif
