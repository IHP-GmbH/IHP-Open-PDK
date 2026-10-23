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

// type: a21o 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_a21o_1
//   cell_description : 2-input AND into first input of 2-input OR.
//*****************************************************************

module sg13cmos5l_a21o_1 (X, A1, A2, B1
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
	
	output X;
	input A1, A2, B1;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function
	wire int_fwire_0;

	and (int_fwire_0, A1, A2);
	or (raw_X, int_fwire_0, B1);

	// Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		if (B1 == 1'b0)
			(A1 => X) = 0;
		ifnone (A1 => X) = 0;
		if (B1 == 1'b0)
			(A2 => X) = 0;
		ifnone (A2 => X) = 0;
		if (A1 == 1'b1 && A2 == 1'b0)
			(B1 => X) = 0;
		if (A1 == 1'b0 && A2 == 1'b1)
			(B1 => X) = 0;
		if (A1 == 1'b0 && A2 == 1'b0)
			(B1 => X) = 0;
		ifnone (B1 => X) = 0;
	endspecify

endmodule
`endcelldefine

// type: a21o 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_a21o_2
//   cell_description : 2-input AND into first input of 2-input OR.
//*****************************************************************

module sg13cmos5l_a21o_2 (X, A1, A2, B1
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output X;
	input A1, A2, B1;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	wire int_fwire_0;

	and (int_fwire_0, A1, A2);
	or (raw_X, int_fwire_0, B1);
        
	// Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		if (B1 == 1'b0)
			(A1 => X) = 0;
		ifnone (A1 => X) = 0;
		if (B1 == 1'b0)
			(A2 => X) = 0;
		ifnone (A2 => X) = 0;
		if (A1 == 1'b1 && A2 == 1'b0)
			(B1 => X) = 0;
		if (A1 == 1'b0 && A2 == 1'b1)
			(B1 => X) = 0;
		if (A1 == 1'b0 && A2 == 1'b0)
			(B1 => X) = 0;
		ifnone (B1 => X) = 0;
	endspecify

endmodule
`endcelldefine

// type: a21oi 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_a21oi_1
//   cell_description : 2-input AND into first input of 2-input NOR.
//*****************************************************************

module sg13cmos5l_a21oi_1 (Y, A1, A2, B1
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output Y;
	input A1, A2, B1;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire int_fwire_0, int_fwire_1;

	and (int_fwire_0, A1, A2);
	or (int_fwire_1, int_fwire_0, B1);
	not (raw_Y, int_fwire_1);
        
	// Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

    specify
		(A1 => Y) = 0;
		(A2 => Y) = 0;
		if ((A1 == 1'b1 && A2 == 1'b0))
			(B1 => Y) = 0;
		if ((A1 == 1'b0 && A2 == 1'b1))
			(B1 => Y) = 0;
		if ((A1 == 1'b0 && A2 == 1'b0))
			(B1 => Y) = 0;
		ifnone (B1 => Y) = 0;
	endspecify

endmodule
`endcelldefine

// type: a21oi 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_a21oi_2
//   cell_description : 2-input AND into first input of 2-input NOR.
//*****************************************************************

module sg13cmos5l_a21oi_2 (Y, A1, A2, B1
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
                      );
		
	output Y;
	input A1, A2, B1;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire int_fwire_0, int_fwire_1;

	and (int_fwire_0, A1, A2);
	or (int_fwire_1, int_fwire_0, B1);
	not (raw_Y, int_fwire_1);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

    specify
		(A1 => Y) = 0;
		(A2 => Y) = 0;
		if ((A1 == 1'b1 && A2 == 1'b0))
			(B1 => Y) = 0;
		if ((A1 == 1'b0 && A2 == 1'b1))
			(B1 => Y) = 0;
		if ((A1 == 1'b0 && A2 == 1'b0))
			(B1 => Y) = 0;
		ifnone (B1 => Y) = 0;
	endspecify

endmodule
`endcelldefine

// type: a221oi 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_a221oi_1
//   cell_description : 2-input AND into first two inputs of 3-input NOR.
//*****************************************************************

module sg13cmos5l_a221oi_1 (Y, A1, A2, B1, B2, C1
		        `ifdef USE_POWER_PINS , VDD, VSS `endif);
		
	output Y;
	input A1, A2, B1, B2, C1;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire int_fwire_0, int_fwire_1, int_fwire_2;

	and (int_fwire_0, B1, B2);
	and (int_fwire_1, A1, A2);
	or (int_fwire_2, int_fwire_1, int_fwire_0, C1);
	not (raw_Y, int_fwire_2);
        
	// Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

    specify
		if ((A2 == 1'b1 && B1 == 1'b1 && B2 == 1'b0 && C1 == 1'b0))
			(A1 => Y) = 0;
		if ((A2 == 1'b1 && B1 == 1'b0 && B2 == 1'b1 && C1 == 1'b0))
			(A1 => Y) = 0;
		if ((A2 == 1'b1 && B1 == 1'b0 && B2 == 1'b0 && C1 == 1'b0))
			(A1 => Y) = 0;
		ifnone (A1 => Y) = 0;
		if ((A1 == 1'b1 && B1 == 1'b1 && B2 == 1'b0 && C1 == 1'b0))
			(A2 => Y) = 0;
		if ((A1 == 1'b1 && B1 == 1'b0 && B2 == 1'b1 && C1 == 1'b0))
			(A2 => Y) = 0;
		if ((A1 == 1'b1 && B1 == 1'b0 && B2 == 1'b0 && C1 == 1'b0))
			(A2 => Y) = 0;
		ifnone (A2 => Y) = 0;
		if ((A1 == 1'b1 && A2 == 1'b0 && B2 == 1'b1 && C1 == 1'b0))
			(B1 => Y) = 0;
		if ((A1 == 1'b0 && A2 == 1'b1 && B2 == 1'b1 && C1 == 1'b0))
			(B1 => Y) = 0;
		if ((A1 == 1'b0 && A2 == 1'b0 && B2 == 1'b1 && C1 == 1'b0))
			(B1 => Y) = 0;
		ifnone (B1 => Y) = 0;
		if ((A1 == 1'b1 && A2 == 1'b0 && B1 == 1'b1 && C1 == 1'b0))
			(B2 => Y) = 0;
		if ((A1 == 1'b0 && A2 == 1'b1 && B1 == 1'b1 && C1 == 1'b0))
			(B2 => Y) = 0;
		if ((A1 == 1'b0 && A2 == 1'b0 && B1 == 1'b1 && C1 == 1'b0))
			(B2 => Y) = 0;
		ifnone (B2 => Y) = 0;
		if ((A1 == 1'b1 && A2 == 1'b0 && B1 == 1'b0 && B2 == 1'b0))
			(C1 => Y) = 0;
		if ((A1 == 1'b0 && A2 == 1'b1 && B1 == 1'b0 && B2 == 1'b0))
			(C1 => Y) = 0;
		if ((A1 == 1'b0 && A2 == 1'b0 && B1 == 1'b1 && B2 == 1'b0))
			(C1 => Y) = 0;
		if ((A1 == 1'b0 && A2 == 1'b0 && B1 == 1'b0 && B2 == 1'b1))
			(C1 => Y) = 0;
		if ((A1 == 1'b0 && A2 == 1'b0 && B1 == 1'b0 && B2 == 1'b0))
			(C1 => Y) = 0;
		ifnone (C1 => Y) = 0;
	endspecify

endmodule
`endcelldefine

// type: a22oi 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_a22oi_1
//   cell_description : 2-input AND into both inputs of 2-input NOR.
//*****************************************************************

module sg13cmos5l_a22oi_1 (Y, A1, A2, B1, B2
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output Y;
	input A1, A2, B1, B2;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire int_fwire_0, int_fwire_1, int_fwire_2;

	and (int_fwire_0, B1, B2);
	and (int_fwire_1, A1, A2);
	or (int_fwire_2, int_fwire_1, int_fwire_0);
	not (raw_Y, int_fwire_2);
        
	// Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

    specify
		if (A2 == 1'b1 && B1 == 1'b1)
			(A1 => Y) = 0;
		ifnone (A1 => Y) = 0;
		if (A1 == 1'b1 && B1 == 1'b1)
			(A2 => Y) = 0;
		ifnone (A2 => Y) = 0;
		if (A1 == 1'b1 && A2 == 1'b0)
			(B1 => Y) = 0;
		if (A1 == 1'b0 && A2 == 1'b1)
			(B1 => Y) = 0;
		ifnone (B1 => Y) = 0;
		if (A1 == 1'b1 && A2 == 1'b0)
			(B2 => Y) = 0;
		if (A1 == 1'b0 && A2 == 1'b1)
			(B2 => Y) = 0;
		ifnone (B2 => Y) = 0;
	endspecify

endmodule
`endcelldefine

// type: and2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_and2_1
//   cell_description : 2-input AND
//*****************************************************************

module sg13cmos5l_and2_1 (X, A, B
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output X;
	input A, B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	and (raw_X, A, B);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		(A => X) = 0;
		(B => X) = 0;
	endspecify

endmodule
`endcelldefine

// type: and2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_and2_2
//   cell_description : 2-input AND
//*****************************************************************

module sg13cmos5l_and2_2 (X, A, B
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output X;
	input A, B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	and (raw_X, A, B);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		(A => X) = 0;
		(B => X) = 0;
	endspecify

endmodule
`endcelldefine

// type: and3 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_and3_1
//   cell_description : 3-input AND
//*****************************************************************

module sg13cmos5l_and3_1 (X, A, B, C
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output X;
	input A, B, C;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	and (raw_X, A, B, C);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		(A => X) = 0;
		(B => X) = 0;
		(C => X) = 0;
	endspecify

endmodule
`endcelldefine

// type: and3 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_snd3_2
//   cell_description : 3-input AND
//*****************************************************************

module sg13cmos5l_and3_2 (X, A, B, C
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output X;
	input A, B, C;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	and (raw_X, A, B, C);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		(A => X) = 0;
		(B => X) = 0;
		(C => X) = 0;
	endspecify

endmodule
`endcelldefine

// type: and4 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_and4_1
//   cell_description : 4-input AND
//*****************************************************************

module sg13cmos5l_and4_1 (X, A, B, C, D
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output X;
	input A, B, C, D;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	and (raw_X, A, B, C, D);

	// Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		(A => X) = 0;
		(B => X) = 0;
		(C => X) = 0;
		(D => X) = 0;
	endspecify

endmodule
`endcelldefine

// type: and4 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_and4_2
//   cell_description : 4-input AND
//*****************************************************************

module sg13cmos5l_and4_2 (X, A, B, C, D
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output X;
	input A, B, C, D;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	and (raw_X, A, B, C, D);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		(A => X) = 0;
		(B => X) = 0;
		(C => X) = 0;
		(D => X) = 0;
	endspecify

endmodule
`endcelldefine

// type: antennanp 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_antennanp
//   cell_description : Antenna effect protection cell (gate charge) at manufacture, P-diode in N-Well, N-diode in substrate
//*****************************************************************

module sg13cmos5l_antennanp (A
			 `ifdef USE_POWER_PINS , VDD, VSS `endif
			);
	input A;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif

        // Timing

	specify
	endspecify

endmodule
`endcelldefine

// type: buf 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_buf_1
//   cell_description : Buffer drive strength 1
//*****************************************************************

module sg13cmos5l_buf_1 (X, A
		     `ifdef USE_POWER_PINS , VDD, VSS `endif
		    );
		
	output X;
	input A;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	buf (raw_X, A);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		(A => X) = 0;
	endspecify

endmodule
`endcelldefine

// type: buf 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_buf_16
//   cell_description : Buffer drive strength 16
//*****************************************************************

module sg13cmos5l_buf_16 (X, A
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output X;
	input A;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	buf (raw_X, A);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		(A => X) = 0;
	endspecify

endmodule
`endcelldefine

// type: buf 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_buf_2
//   cell_description : Buffer drive strength 2
//*****************************************************************

module sg13cmos5l_buf_2 (X, A
		     `ifdef USE_POWER_PINS , VDD, VSS `endif
		    );
		
	output X;
	input A;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	buf (raw_X, A);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		(A => X) = 0;
	endspecify

endmodule
`endcelldefine

// type: buf 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_buf_4
//   cell_description : Buffer drive strength 4
//*****************************************************************

module sg13cmos5l_buf_4 (X, A
		     `ifdef USE_POWER_PINS , VDD, VSS `endif
		    );
		
	output X;
	input A;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	buf (raw_X, A);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		(A => X) = 0;
	endspecify

endmodule
`endcelldefine

// type: buf 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_buf_8
//   cell_description : Buffer drive strength 8
//*****************************************************************

module sg13cmos5l_buf_8 (X, A
		     `ifdef USE_POWER_PINS , VDD, VSS `endif
		    );
		
	output X;
	input A;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	buf (raw_X, A);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		(A => X) = 0;
	endspecify

endmodule
`endcelldefine

// type: decap 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_decap_4
//   cell_description : Decoupling capasitance filler cell
//*****************************************************************

module sg13cmos5l_decap_4 (
		       `ifdef USE_POWER_PINS VDD, VSS `endif
		      );
	
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif

        // Timing

	specify
	endspecify

endmodule
`endcelldefine

// type: decap 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_decap_8
//   cell_description : Decoupling capasitance filler cell
//*****************************************************************

module sg13cmos5l_decap_8 (
		       `ifdef USE_POWER_PINS VDD, VSS `endif
		      );

	`ifdef USE_POWER_PINS inout VDD, VSS; `endif

        // Timing

	specify
	endspecify

endmodule
`endcelldefine

// type: dfrbp 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_dfrbp_1
//   cell_description : Posedge Two-Outputs Q and Q_N D-Flip-Flop with Low-Active Reset
//*****************************************************************

module sg13cmos5l_dfrbp_1 (Q, Q_N, CLK, D, RESET_B
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output Q, Q_N;
	input CLK, D, RESET_B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif
	reg notifier;
	wire delayed_D, delayed_RESET_B, delayed_CLK;


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Q;
    wire raw_Q_N;
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    wire power_aware_notifier = notifier ^ (power_good ? 1'b0 : 1'bx);
`else
    wire power_aware_notifier = notifier;
`endif

	// Function
	wire int_fwire_IQ, int_fwire_IQN, int_fwire_r;
	wire xcr_0;

	not (int_fwire_r, delayed_RESET_B);
	buf (xcr_0, 0);
	ihp_dff_r (int_fwire_IQ, power_aware_notifier, delayed_CLK, delayed_D, int_fwire_r, xcr_0);
	buf (raw_Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (raw_Q_N, int_fwire_IQN);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    assign Q = power_good ? raw_Q : 1'bx;
    assign Q_N = power_good ? raw_Q_N : 1'bx;
`else
    buf (Q, raw_Q);
    buf (Q_N, raw_Q_N);
`endif


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

// type: dfrbp 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_dfrbp_2
//   cell_description : Posedge Two-Outputs Q and Q_N D-Flip-Flop with Low-Active Reset
//*****************************************************************

module sg13cmos5l_dfrbp_2 (Q, Q_N, CLK, D, RESET_B
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output Q, Q_N;
	input CLK, D, RESET_B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif
	reg notifier;
	wire delayed_D, delayed_RESET_B, delayed_CLK;


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Q;
    wire raw_Q_N;
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    wire power_aware_notifier = notifier ^ (power_good ? 1'b0 : 1'bx);
`else
    wire power_aware_notifier = notifier;
`endif

	// Function
	wire int_fwire_IQ, int_fwire_IQN, int_fwire_r;
	wire xcr_0;

	not (int_fwire_r, delayed_RESET_B);
	buf (xcr_0, 0);
	ihp_dff_r (int_fwire_IQ, power_aware_notifier, delayed_CLK, delayed_D, int_fwire_r, xcr_0);
	buf (raw_Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (raw_Q_N, int_fwire_IQN);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    assign Q = power_good ? raw_Q : 1'bx;
    assign Q_N = power_good ? raw_Q_N : 1'bx;
`else
    buf (Q, raw_Q);
    buf (Q_N, raw_Q_N);
`endif


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

// type: dfrbpq 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_dfrbpq_1
//   cell_description : Posedge Single-Output Q D-Flip-Flop with Low-Active Reset
//*****************************************************************

module sg13cmos5l_dfrbpq_1 (Q, CLK, D, RESET_B
			`ifdef USE_POWER_PINS , VDD, VSS `endif
		       );
		
	output Q;
	input CLK, D, RESET_B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif
	reg notifier;
	wire delayed_D, delayed_RESET_B, delayed_CLK;


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Q;
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    wire power_aware_notifier = notifier ^ (power_good ? 1'b0 : 1'bx);
`else
    wire power_aware_notifier = notifier;
`endif

	// Function
	wire int_fwire_IQ, int_fwire_r, xcr_0;

	not (int_fwire_r, delayed_RESET_B);
	buf (xcr_0, 0);
	ihp_dff_r (int_fwire_IQ, power_aware_notifier, delayed_CLK, delayed_D, int_fwire_r, xcr_0);
	buf (raw_Q, int_fwire_IQ);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    assign Q = power_good ? raw_Q : 1'bx;
`else
    buf (Q, raw_Q);
`endif


    specify
		(negedge RESET_B => (Q+:1'b0)) = 0;
		(posedge CLK => (Q+:D)) = 0;
		$setuphold (posedge CLK, posedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, negedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$recrem (posedge RESET_B, posedge CLK, 0, 0, notifier,,, delayed_RESET_B, delayed_CLK);
		$width (negedge RESET_B, 0, 0, notifier);
		$width (posedge CLK, 0, 0, notifier);
		$width (negedge CLK, 0, 0, notifier);
	endspecify

endmodule
`endcelldefine

// type: dfrbpq 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_dfrbpq_2
//   cell_description : Posedge Single-Output Q D-Flip-Flop with Low-Active Reset
//*****************************************************************

module sg13cmos5l_dfrbpq_2 (Q, CLK, D, RESET_B
			`ifdef USE_POWER_PINS , VDD, VSS `endif
		       );
		
	output Q;
	input CLK, D, RESET_B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif
	reg notifier;
	wire delayed_D, delayed_RESET_B, delayed_CLK;


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Q;
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    wire power_aware_notifier = notifier ^ (power_good ? 1'b0 : 1'bx);
`else
    wire power_aware_notifier = notifier;
`endif

	// Function
	wire int_fwire_IQ, int_fwire_r, xcr_0;

	not (int_fwire_r, delayed_RESET_B);
	buf (xcr_0, 0);
	ihp_dff_r (int_fwire_IQ, power_aware_notifier, delayed_CLK, delayed_D, int_fwire_r, xcr_0);
	buf (raw_Q, int_fwire_IQ);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    assign Q = power_good ? raw_Q : 1'bx;
`else
    buf (Q, raw_Q);
`endif


    specify
		(negedge RESET_B => (Q+:1'b0)) = 0;
		(posedge CLK => (Q+:D)) = 0;
		$setuphold (posedge CLK, posedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, negedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$recrem (posedge RESET_B, posedge CLK, 0, 0, notifier,,, delayed_RESET_B, delayed_CLK);
		$width (negedge RESET_B, 0, 0, notifier);
		$width (posedge CLK, 0, 0, notifier);
		$width (negedge CLK, 0, 0, notifier);
	endspecify

endmodule
`endcelldefine

// type: dlhq 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_dlhq_1
//   cell_description : High-Active GATE Single-Output Q D-latch
//*****************************************************************

module sg13cmos5l_dlhq_1 (Q, D, GATE
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output Q;
	input D, GATE;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif
	reg notifier;
	wire delayed_D, delayed_GATE;


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Q;
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    wire power_aware_notifier = notifier ^ (power_good ? 1'b0 : 1'bx);
`else
    wire power_aware_notifier = notifier;
`endif

	// Function

	wire int_fwire_IQ;

	ihp_latch (int_fwire_IQ, power_aware_notifier, delayed_GATE, delayed_D);
	buf (raw_Q, int_fwire_IQ);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    assign Q = power_good ? raw_Q : 1'bx;
`else
    buf (Q, raw_Q);
`endif


    specify
		(D => Q) = 0;
		(posedge GATE => (Q+:D)) = 0;
		$setuphold (negedge GATE, posedge D, 0, 0, notifier,,, delayed_GATE, delayed_D);
		$setuphold (negedge GATE, negedge D, 0, 0, notifier,,, delayed_GATE, delayed_D);
		$width (posedge GATE, 0, 0, notifier);
	endspecify

endmodule
`endcelldefine

// type: dlhr 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_dlhr_1
//   cell_description : High-Active GATE Two-Outputs Q Q_N D-latch with Low-Active Reset
//*****************************************************************

module sg13cmos5l_dlhr_1 (Q, Q_N, D, GATE, RESET_B
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output Q, Q_N;
	input D, GATE, RESET_B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif
	reg notifier;
	wire delayed_D, delayed_RESET_B, delayed_GATE;


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Q;
    wire raw_Q_N;
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    wire power_aware_notifier = notifier ^ (power_good ? 1'b0 : 1'bx);
`else
    wire power_aware_notifier = notifier;
`endif

	// Function

	wire int_fwire_IQ, int_fwire_IQN, int_fwire_r;

	not (int_fwire_r, delayed_RESET_B);
	ihp_latch_r (int_fwire_IQ, power_aware_notifier, delayed_GATE, delayed_D, int_fwire_r);
	buf (raw_Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (raw_Q_N, int_fwire_IQN);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    assign Q = power_good ? raw_Q : 1'bx;
    assign Q_N = power_good ? raw_Q_N : 1'bx;
`else
    buf (Q, raw_Q);
    buf (Q_N, raw_Q_N);
`endif


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


// type: dlhrq 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_dlhrq_1
//   cell_description : High-Active Gate Single-Output Q D-latch with Low-Active Reset
//*****************************************************************

module sg13cmos5l_dlhrq_1 (Q, D, GATE, RESET_B
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output Q;
	input D, GATE, RESET_B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif
	reg notifier;
	wire delayed_D, delayed_RESET_B, delayed_GATE;


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Q;
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    wire power_aware_notifier = notifier ^ (power_good ? 1'b0 : 1'bx);
`else
    wire power_aware_notifier = notifier;
`endif

	// Function

	wire int_fwire_IQ, int_fwire_r;

	not (int_fwire_r, delayed_RESET_B);
	ihp_latch_r (int_fwire_IQ, power_aware_notifier, delayed_GATE, delayed_D, int_fwire_r);
	buf (raw_Q, int_fwire_IQ);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    assign Q = power_good ? raw_Q : 1'bx;
`else
    buf (Q, raw_Q);
`endif


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


// type: dllr 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_dllr_1
//   cell_description : Low-Active GATE_N Two-Outputs Q Q_N D-latch with Low-Active Reset
//*****************************************************************

module sg13cmos5l_dllr_1 (Q, Q_N, D, GATE_N, RESET_B
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output Q, Q_N;
	input D, GATE_N, RESET_B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif
	reg notifier;
	wire delayed_D, delayed_RESET_B, delayed_GATE_N;


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Q;
    wire raw_Q_N;
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    wire power_aware_notifier = notifier ^ (power_good ? 1'b0 : 1'bx);
`else
    wire power_aware_notifier = notifier;
`endif

	// Function

	wire int_fwire_clk, int_fwire_IQ, int_fwire_IQN;
	wire int_fwire_r;

	not (int_fwire_clk, delayed_GATE_N);
	not (int_fwire_r, delayed_RESET_B);
	ihp_latch_r (int_fwire_IQ, power_aware_notifier, int_fwire_clk, delayed_D, int_fwire_r);
	buf (raw_Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (raw_Q_N, int_fwire_IQN);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    assign Q = power_good ? raw_Q : 1'bx;
    assign Q_N = power_good ? raw_Q_N : 1'bx;
`else
    buf (Q, raw_Q);
    buf (Q_N, raw_Q_N);
`endif


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


// type: dllrq 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_dllrq_1
//   cell_description : Low-Active GATE_N Single-Output Q D-latch with Low-Active Reset
//*****************************************************************

module sg13cmos5l_dllrq_1 (Q, D, GATE_N, RESET_B
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output Q;
	input D, GATE_N, RESET_B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif
	reg notifier;
	wire delayed_D, delayed_RESET_B, delayed_GATE_N;


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Q;
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    wire power_aware_notifier = notifier ^ (power_good ? 1'b0 : 1'bx);
`else
    wire power_aware_notifier = notifier;
`endif

	// Function

	wire int_fwire_clk, int_fwire_IQ, int_fwire_r;

	not (int_fwire_clk, delayed_GATE_N);
	not (int_fwire_r, delayed_RESET_B);
	ihp_latch_r (int_fwire_IQ, power_aware_notifier, int_fwire_clk, delayed_D, int_fwire_r);
	buf (raw_Q, int_fwire_IQ);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    assign Q = power_good ? raw_Q : 1'bx;
`else
    buf (Q, raw_Q);
`endif


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


// type: dlygate4sd1 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_dlygate4sd1_1
//   cell_description : Delay Cell, typical 0.4 ns
//*****************************************************************

module sg13cmos5l_dlygate4sd1_1 (X, A
			     `ifdef USE_POWER_PINS , VDD, VSS `endif
			    );
		
	output X;
	input A;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	buf (raw_X, A);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		(A => X) = 0;
	endspecify

endmodule
`endcelldefine


// type: dlygate4sd2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_dlygate4sd2_1
//   cell_description : Delay Cell, typical 0.45 ns
//*****************************************************************

module sg13cmos5l_dlygate4sd2_1 (X, A
			     `ifdef USE_POWER_PINS , VDD, VSS `endif
			    );
		
	output X;
	input A;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	buf (raw_X, A);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		(A => X) = 0;
	endspecify

endmodule
`endcelldefine


// type: dlygate4sd3 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_dlygate4sd3_1
//   cell_description : Delay Cell, typical 0.7 ns
//*****************************************************************

module sg13cmos5l_dlygate4sd3_1 (X, A
			     `ifdef USE_POWER_PINS , VDD, VSS `endif
			    );
		
	output X;
	input A;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	buf (raw_X, A);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		(A => X) = 0;
	endspecify

endmodule
`endcelldefine


// type: ebufn 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_ebufn_2
//   cell_description : Tristate Buffer with Low-Active Enable TE_B
//*****************************************************************

module sg13cmos5l_ebufn_2 (Z, A, TE_B
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output Z;
	input A, TE_B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Z;

	// Function

	bufif0 (raw_Z, A, TE_B);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Z = power_good ? raw_Z : 1'bx;
`else
    buf (Z, raw_Z);
`endif

    specify
		(A => Z) = 0;
		(TE_B => Z) = 0;
	endspecify

endmodule
`endcelldefine


// type: ebufn 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_ebufn_4
//   cell_description : Tristate Buffer with Low-Active Enable TE_B
//*****************************************************************

module sg13cmos5l_ebufn_4 (Z, A, TE_B
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output Z;
	input A, TE_B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Z;

	// Function

	bufif0 (raw_Z, A, TE_B);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Z = power_good ? raw_Z : 1'bx;
`else
    buf (Z, raw_Z);
`endif

    specify
		(A => Z) = 0;
		(TE_B => Z) = 0;
	endspecify

endmodule
`endcelldefine


// type: ebufn 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_ebufn_8
//   cell_description : Tristate Buffer with Low-Active Enable TE_B
//*****************************************************************

module sg13cmos5l_ebufn_8 (Z, A, TE_B
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output Z;
	input A, TE_B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Z;

	// Function

	bufif0 (raw_Z, A, TE_B);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Z = power_good ? raw_Z : 1'bx;
`else
    buf (Z, raw_Z);
`endif

    specify
		(A => Z) = 0;
		(TE_B => Z) = 0;
	endspecify

endmodule
`endcelldefine


// type: einvn 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_einvn_2
//   cell_description : Tristate Inverter with Low-Active Enable TE_B
//*****************************************************************

module sg13cmos5l_einvn_2 (Z, A, TE_B
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output Z;
	input A, TE_B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Z;

	// Function

	notif0 (raw_Z, A, TE_B);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Z = power_good ? raw_Z : 1'bx;
`else
    buf (Z, raw_Z);
`endif

    specify
		(A => Z) = 0;
		(posedge TE_B => (Z:!A)) = 0;
		(negedge TE_B => (Z:!A)) = 0;
	endspecify

endmodule
`endcelldefine


// type: einvn 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_einvn_4
//   cell_description : Tristate Inverter with Low-Active Enable TE_B
//*****************************************************************

module sg13cmos5l_einvn_4 (Z, A, TE_B
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output Z;
	input A, TE_B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Z;

	// Function

	notif0 (raw_Z, A, TE_B);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Z = power_good ? raw_Z : 1'bx;
`else
    buf (Z, raw_Z);
`endif

    specify
		(A => Z) = 0;
		(posedge TE_B => (Z:!A)) = 0;
		(negedge TE_B => (Z:!A)) = 0;
	endspecify

endmodule
`endcelldefine


// type: einvn 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_einvn_8
//   cell_description : Tristate Inverter with Low-Active Enable TE_B
//*****************************************************************

module sg13cmos5l_einvn_8 (Z, A, TE_B
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output Z;
	input A, TE_B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Z;

	// Function

	notif0 (raw_Z, A, TE_B);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Z = power_good ? raw_Z : 1'bx;
`else
    buf (Z, raw_Z);
`endif

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
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_fill_1
//   cell_description : Filler 1 Track Width
//*****************************************************************

module sg13cmos5l_fill_1 (`ifdef USE_POWER_PINS VDD, VSS `endif);

	`ifdef USE_POWER_PINS inout VDD, VSS; `endif
 
       // Timing

	specify
	endspecify

endmodule
`endcelldefine


// type: fill 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_fill_2
//   cell_description : Filler 2 Tracks Width
//*****************************************************************

module sg13cmos5l_fill_2 (`ifdef USE_POWER_PINS VDD, VSS `endif);

	`ifdef USE_POWER_PINS inout VDD, VSS; `endif

        // Timing

	specify
	endspecify

endmodule
`endcelldefine


// type: fill 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_fill_4
//   cell_description : Filler 4 Tracks Width
//*****************************************************************

module sg13cmos5l_fill_4 (`ifdef USE_POWER_PINS VDD, VSS `endif);

	`ifdef USE_POWER_PINS inout VDD, VSS; `endif

        // Timing

	specify
	endspecify

endmodule
`endcelldefine


// type: fill 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_fill_8
//   cell_description : Filler 8 Tracks Width
//*****************************************************************

module sg13cmos5l_fill_8 (`ifdef USE_POWER_PINS VDD, VSS `endif);

	`ifdef USE_POWER_PINS inout VDD, VSS; `endif

        // Timing

	specify
	endspecify

endmodule
`endcelldefine


// type: inv 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_inv_1
//   cell_description : Inverter
//*****************************************************************

module sg13cmos5l_inv_1 (Y, A
		     `ifdef USE_POWER_PINS , VDD, VSS `endif
		    );

	output Y;
	input A;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	not (raw_Y, A);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

    specify
		(A => Y) = 0;
	endspecify

endmodule
`endcelldefine


// type: inv 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_inv_16
//   cell_description : Inverter
//*****************************************************************

module sg13cmos5l_inv_16 (Y, A
                      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output Y;
	input A;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	not (raw_Y, A);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

    specify
		(A => Y) = 0;
	endspecify

endmodule
`endcelldefine


// type: inv 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_inv_2
//   cell_description : Inverter
//*****************************************************************

module sg13cmos5l_inv_2 (Y, A
		     `ifdef USE_POWER_PINS , VDD, VSS `endif
		    );
		
	output Y;
	input A;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	not (raw_Y, A);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

    specify
		(A => Y) = 0;
	endspecify

endmodule
`endcelldefine


// type: inv 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_inv_4
//   cell_description : Inverter
//*****************************************************************

module sg13cmos5l_inv_4 (Y, A
		     `ifdef USE_POWER_PINS , VDD, VSS `endif
		    );
		
	output Y;
	input A;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	not (raw_Y, A);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

    specify
		(A => Y) = 0;
	endspecify

endmodule
`endcelldefine


// type: inv 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_inv_8
//   cell_description : Inverter
//*****************************************************************

module sg13cmos5l_inv_8 (Y, A
		     `ifdef USE_POWER_PINS , VDD, VSS `endif
		    );
		
	output Y;
	input A;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	not (raw_Y, A);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

    specify
		(A => Y) = 0;
	endspecify

endmodule
`endcelldefine


// type: lgcp 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_lgcp_1
//   cell_description : Posedge Clock Gating cell, Low Latch Enable
//*****************************************************************

module sg13cmos5l_lgcp_1 (GCLK, CLK, GATE
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output GCLK;
	input CLK, GATE;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif
	reg notifier;
	wire delayed_GATE, delayed_CLK;


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_GCLK;
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    wire power_aware_notifier = notifier ^ (power_good ? 1'b0 : 1'bx);
`else
    wire power_aware_notifier = notifier;
`endif

	// Function

	wire int_fwire_clk, int_fwire_int_GATE;

	not (int_fwire_clk, delayed_CLK);
	ihp_latch (int_fwire_int_GATE, power_aware_notifier, int_fwire_clk, delayed_GATE);
	and (raw_GCLK, delayed_CLK, int_fwire_int_GATE);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    assign GCLK = power_good ? raw_GCLK : 1'bx;
`else
    buf (GCLK, raw_GCLK);
`endif


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
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_mux2_1
//   cell_description : Multiplexer from 2 to 1
//*****************************************************************

module sg13cmos5l_mux2_1 (X, A0, A1, S
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output X;
	input A0, A1, S;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	ihp_mux2 (raw_X, A0, A1, S);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		(A0 => X) = 0;
		(A1 => X) = 0;
		if (A0 == 1'b0 && A1 == 1'b1)
			(S => X) = 0;
		ifnone (S => X) = 0;
		if (A0 == 1'b1 && A1 == 1'b0)
			(S => X) = 0;
	endspecify

endmodule
`endcelldefine

// Verilog for cell sg13cmos5l_mux2_2 created entirely by Liberate 23.1.3.126.isr3

// type: mux2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_mux2_2
//   cell_description : Multiplexer from 2 to 1
//*****************************************************************

module sg13cmos5l_mux2_2 (X, A0, A1, S
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output X;
	input A0, A1, S;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	ihp_mux2 (raw_X, A0, A1, S);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		(A0 => X) = 0;
		(A1 => X) = 0;
		if (A0 == 1'b0 && A1 == 1'b1)
			(S => X) = 0;
		ifnone (S => X) = 0;
		if (A0 == 1'b1 && A1 == 1'b0)
			(S => X) = 0;
	endspecify

endmodule
`endcelldefine


// type: mux4 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_mux4_1
//   cell_description : Multiplexer from 4 to 1
//*****************************************************************

module sg13cmos5l_mux4_1 (X, A0, A1, A2, A3, S0, S1
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output X;
	input A0, A1, A2, A3, S0, S1;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	ihp_mux4 (raw_X, A0, A1, A2, A3, S0, S1);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		(A0 => X) = 0;
		(A1 => X) = 0;
		(A2 => X) = 0;
		(A3 => X) = 0;
		if (A2 == 1'b0 && A3 == 1'b1 && S1 == 1'b1)
			(S0 => X) = 0;
		if (A0 == 1'b0 && A1 == 1'b1 && S1 == 1'b0)
			(S0 => X) = 0;
		ifnone (S0 => X) = 0;
		if (A2 == 1'b1 && A3 == 1'b0 && S1 == 1'b1)
			(S0 => X) = 0;
		if (A0 == 1'b1 && A1 == 1'b0 && S1 == 1'b0)
			(S0 => X) = 0;
		if (A1 == 1'b0 && A3 == 1'b1 && S0 == 1'b1)
			(S1 => X) = 0;
		if (A0 == 1'b0 && A2 == 1'b1 && S0 == 1'b0)
			(S1 => X) = 0;
		ifnone (S1 => X) = 0;
		if (A1 == 1'b1 && A3 == 1'b0 && S0 == 1'b1)
			(S1 => X) = 0;
		if (A0 == 1'b1 && A2 == 1'b0 && S0 == 1'b0)
			(S1 => X) = 0;
	endspecify

endmodule
`endcelldefine


// type: nand2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_nand2_1
//   cell_description : 2-input NAND
//*****************************************************************

module sg13cmos5l_nand2_1 (Y, A, B
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output Y;
	input A, B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire int_fwire_0;

	and (int_fwire_0, A, B);
	not (raw_Y, int_fwire_0);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

    specify
		(A => Y) = 0;
		(B => Y) = 0;
	endspecify

endmodule
`endcelldefine


// type: nand2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_nand2_2
//   cell_description : 2-input NAND
//*****************************************************************

module sg13cmos5l_nand2_2 (Y, A, B
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output Y;
	input A, B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire int_fwire_0;

	and (int_fwire_0, A, B);
	not (raw_Y, int_fwire_0);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

    specify
		(A => Y) = 0;
		(B => Y) = 0;
	endspecify

endmodule
`endcelldefine


// type: nand2b 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_nand2b_1
//   cell_description : 2-input NAND with Inverted Input A_N
//*****************************************************************

module sg13cmos5l_nand2b_1 (Y, A_N, B
		        `ifdef USE_POWER_PINS , VDD, VSS `endif
		       );
		
	output Y;
	input A_N, B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire A_N__bar, int_fwire_0;

	not (A_N__bar, A_N);
	and (int_fwire_0, A_N__bar, B);
	not (raw_Y, int_fwire_0);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

    specify
		(A_N => Y) = 0;
		(B => Y) = 0;
	endspecify

endmodule
`endcelldefine


// type: nand2b 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_nand2b_2
//   cell_description : 2-input NAND with Inverted Input A_N
//*****************************************************************

module sg13cmos5l_nand2b_2 (Y, A_N, B
		        `ifdef USE_POWER_PINS , VDD, VSS `endif
		       );
		
	output Y;
	input A_N, B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire A_N__bar, int_fwire_0;

	not (A_N__bar, A_N);
	and (int_fwire_0, A_N__bar, B);
	not (raw_Y, int_fwire_0);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

    specify
		(A_N => Y) = 0;
		(B => Y) = 0;
	endspecify

endmodule
`endcelldefine


// type: nand3 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_nand3_1
//   cell_description : 3-input NAND
//*****************************************************************

module sg13cmos5l_nand3_1 (Y, A, B, C
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output Y;
	input A, B, C;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire int_fwire_0;

	and (int_fwire_0, A, B, C);
	not (raw_Y, int_fwire_0);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

    specify
		(A => Y) = 0;
		(B => Y) = 0;
		(C => Y) = 0;
	endspecify

endmodule
`endcelldefine


// type: nand3b 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_nand3b_1
//   cell_description : 3-input NAND3 with Inverted Input A_N
//*****************************************************************

module sg13cmos5l_nand3b_1 (Y, A_N, B, C
		        `ifdef USE_POWER_PINS , VDD, VSS `endif
		       );
		
	output Y;
	input A_N, B, C;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire A_N__bar, int_fwire_0;

	not (A_N__bar, A_N);
	and (int_fwire_0, A_N__bar, B, C);
	not (raw_Y, int_fwire_0);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

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
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_nand4_1
//   cell_description : 4-input NAND
//*****************************************************************

module sg13cmos5l_nand4_1 (Y, A, B, C, D
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output Y;
	input A, B, C, D;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire int_fwire_0;

	and (int_fwire_0, A, B, C, D);
	not (raw_Y, int_fwire_0);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

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
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_nor2_1
//   cell_description : 2-input NOR
//*****************************************************************

module sg13cmos5l_nor2_1 (Y, A, B
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output Y;
	input A, B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire int_fwire_0;

	or (int_fwire_0, A, B);
	not (raw_Y, int_fwire_0);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

    specify
		(A => Y) = 0;
		(B => Y) = 0;
	endspecify

endmodule
`endcelldefine


// type: nor2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_nor2_2
//   cell_description : 2-input NOR
//*****************************************************************

module sg13cmos5l_nor2_2 (Y, A, B
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output Y;
	input A, B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire int_fwire_0;

	or (int_fwire_0, A, B);
	not (raw_Y, int_fwire_0);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

    specify
		(A => Y) = 0;
		(B => Y) = 0;
	endspecify

endmodule
`endcelldefine


// type: nor2b 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_nor2b_1
//   cell_description : 2-input NOR2 with Inverted Input B_N
//*****************************************************************

module sg13cmos5l_nor2b_1 (Y, A, B_N
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output Y;
	input A, B_N;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire B_N__bar, int_fwire_0;

	not (B_N__bar, B_N);
	or (int_fwire_0, A, B_N__bar);
	not (raw_Y, int_fwire_0);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

    specify
		(A => Y) = 0;
		(B_N => Y) = 0;
	endspecify

endmodule
`endcelldefine


// type: nor2b 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_nor2b_1
//   cell_description : 2-input NOR2 with Inverted Input B_N
//*****************************************************************

module sg13cmos5l_nor2b_2 (Y, A, B_N
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output Y;
	input A, B_N;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire B_N__bar, int_fwire_0;

	not (B_N__bar, B_N);
	or (int_fwire_0, A, B_N__bar);
	not (raw_Y, int_fwire_0);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

    specify
		(A => Y) = 0;
		(B_N => Y) = 0;
	endspecify

endmodule
`endcelldefine


// type: nor3 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_nor3_1
//   cell_description : 3-input NOR
//*****************************************************************

module sg13cmos5l_nor3_1 (Y, A, B, C
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output Y;
	input A, B, C;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire int_fwire_0;

	or (int_fwire_0, A, B, C);
	not (raw_Y, int_fwire_0);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

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
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_nor3_2
//   cell_description : 3-input NOR
//*****************************************************************

module sg13cmos5l_nor3_2 (Y, A, B, C
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output Y;
	input A, B, C;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire int_fwire_0;

	or (int_fwire_0, A, B, C);
	not (raw_Y, int_fwire_0);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

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
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_nor4_1
//   cell_description : 4-input NOR
//*****************************************************************

module sg13cmos5l_nor4_1 (Y, A, B, C, D
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output Y;
	input A, B, C, D;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire int_fwire_0;

	or (int_fwire_0, A, B, C, D);
	not (raw_Y, int_fwire_0);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

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
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_nor4_2
//   cell_description : 4-input NOR
//*****************************************************************

module sg13cmos5l_nor4_2 (Y, A, B, C, D
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output Y;
	input A, B, C, D;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire int_fwire_0;

	or (int_fwire_0, A, B, C, D);
	not (raw_Y, int_fwire_0);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

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
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_o21ai_1
//   cell_description : 2-input OR into 2-input NAND
//*****************************************************************

module sg13cmos5l_o21ai_1 (Y, A1, A2, B1
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output Y;
	input A1, A2, B1;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire int_fwire_0, int_fwire_1;

	or (int_fwire_0, A1, A2);
	and (int_fwire_1, int_fwire_0, B1);
	not (raw_Y, int_fwire_1);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

    specify
		(A1 => Y) = 0;
		(A2 => Y) = 0;
		if ((A1 == 1'b0 && A2 == 1'b1))
			(B1 => Y) = 0;
		ifnone (B1 => Y) = 0;
	endspecify

endmodule
`endcelldefine


// type: or2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_or2_1
//   cell_description : 2-input OR
//*****************************************************************

module sg13cmos5l_or2_1 (X, A, B
		     `ifdef USE_POWER_PINS , VDD, VSS `endif
		    );
		
	output X;
	input A, B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	or (raw_X, A, B);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		(A => X) = 0;
		(B => X) = 0;
	endspecify

endmodule
`endcelldefine


// type: or2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_or2_2
//   cell_description : 2-input OR
//*****************************************************************

module sg13cmos5l_or2_2 (X, A, B
		     `ifdef USE_POWER_PINS , VDD, VSS `endif
		    );
		
	output X;
	input A, B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	or (raw_X, A, B);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		(A => X) = 0;
		(B => X) = 0;
	endspecify

endmodule
`endcelldefine


// type: or3 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_or3_1
//   cell_description : 3-input OR
//*****************************************************************

module sg13cmos5l_or3_1 (X, A, B, C
		     `ifdef USE_POWER_PINS , VDD, VSS `endif
		    );
		
	output X;
	input A, B, C;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	or (raw_X, A, B, C);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

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
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_or3_2
//   cell_description : 3-input OR
//*****************************************************************

module sg13cmos5l_or3_2 (X, A, B, C
		     `ifdef USE_POWER_PINS , VDD, VSS `endif
		    );
		
	output X;
	input A, B, C;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	or (raw_X, A, B, C);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

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
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_or4_1
//   cell_description : 4-input OR
//*****************************************************************

module sg13cmos5l_or4_1 (X, A, B, C, D
		     `ifdef USE_POWER_PINS , VDD, VSS `endif
		    );
		
	output X;
	input A, B, C, D;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	or (raw_X, A, B, C, D);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

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
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_or4_2
//   cell_description : 4-input OR
//*****************************************************************

module sg13cmos5l_or4_2 (X, A, B, C, D
		     `ifdef USE_POWER_PINS , VDD, VSS `endif
		    );
		
	output X;
	input A, B, C, D;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	or (raw_X, A, B, C, D);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		(A => X) = 0;
		(B => X) = 0;
		(C => X) = 0;
		(D => X) = 0;
	endspecify

endmodule
`endcelldefine


// type: sdfbbp 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_sdfbbp_1
//   cell_description : Posedge Two-Outputs D-Flip-Flop with Reset, Set and Scan
//*****************************************************************

module sg13cmos5l_sdfbbp_1 (Q, Q_N, CLK, D, RESET_B, SCD, SCE, SET_B
		        `ifdef USE_POWER_PINS , VDD, VSS `endif
		       );
		
	output Q, Q_N;
	input CLK, D, RESET_B, SCD, SCE, SET_B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif
	reg notifier;
	wire delayed_D, delayed_SCD, delayed_SCE, delayed_RESET_B, delayed_SET_B, delayed_CLK;


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Q;
    wire raw_Q_N;
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    wire power_aware_notifier = notifier ^ (power_good ? 1'b0 : 1'bx);
`else
    wire power_aware_notifier = notifier;
`endif

	// Function
	wire int_fwire_d, int_fwire_IQ, int_fwire_IQN;
	wire int_fwire_r, int_fwire_s, xcr_0;

	ihp_mux2 (int_fwire_d, delayed_D, delayed_SCD, delayed_SCE);
	not (int_fwire_s, delayed_SET_B);
	not (int_fwire_r, delayed_RESET_B);
	buf (xcr_0, 0);
	ihp_dff_sr_1 (int_fwire_IQ, power_aware_notifier, delayed_CLK, int_fwire_d, int_fwire_s, int_fwire_r, xcr_0);
	buf (raw_Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (raw_Q_N, int_fwire_IQN);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    assign Q = power_good ? raw_Q : 1'bx;
    assign Q_N = power_good ? raw_Q_N : 1'bx;
`else
    buf (Q, raw_Q);
    buf (Q_N, raw_Q_N);
`endif


    specify
		(negedge RESET_B => (Q+:1'b0)) = 0;
		(negedge SET_B => (Q+:1'b1)) = 0;
		if (SCE == 1'b1)
			(posedge CLK => (Q+:((D && SCD) || (D && !SCD && !SCE) || (!D && SCD && SCE)))) = 0;
		ifnone (CLK => Q) = 0;
		(negedge RESET_B => (Q_N-:1'b0)) = 0;
		(negedge SET_B => (Q_N-:1'b1)) = 0;
		if (SCE == 1'b1)
			(posedge CLK => (Q_N-:((D && SCD) || (D && !SCD && !SCE) || (!D && SCD && SCE)))) = 0;
		ifnone (CLK => Q_N) = 0;
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


// type: sdfrbp 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_sdfrbp_1
//   cell_description : Posedge Two-Outputs Q and Q_N D-Flip-Flop with Reset and Scan
//*****************************************************************

module sg13cmos5l_sdfrbp_1 (Q, Q_N, CLK, D, RESET_B, SCD, SCE
		        `ifdef USE_POWER_PINS , VDD, VSS `endif
		       );
		
	output Q, Q_N;
	input CLK, D, RESET_B, SCD, SCE;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif
	reg notifier;
	wire delayed_D, delayed_SCD, delayed_SCE, delayed_RESET_B, delayed_CLK;


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Q;
    wire raw_Q_N;
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    wire power_aware_notifier = notifier ^ (power_good ? 1'b0 : 1'bx);
`else
    wire power_aware_notifier = notifier;
`endif

	// Function
	wire int_fwire_d, int_fwire_IQ, int_fwire_IQN;
	wire int_fwire_r, xcr_0;

	ihp_mux2 (int_fwire_d, delayed_D, delayed_SCD, delayed_SCE);
	not (int_fwire_r, delayed_RESET_B);
	buf (xcr_0, 0);
	ihp_dff_r (int_fwire_IQ, power_aware_notifier, delayed_CLK, int_fwire_d, int_fwire_r, xcr_0);
	buf (raw_Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (raw_Q_N, int_fwire_IQN);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    assign Q = power_good ? raw_Q : 1'bx;
    assign Q_N = power_good ? raw_Q_N : 1'bx;
`else
    buf (Q, raw_Q);
    buf (Q_N, raw_Q_N);
`endif


    specify
		(negedge RESET_B => (Q+:1'b0)) = 0;
		if (SCE == 1'b1)
			(posedge CLK => (Q+:((D && SCD) || (D && !SCD && !SCE) || (!D && SCD && SCE)))) = 0;
		ifnone (CLK => Q) = 0;
		(negedge RESET_B => (Q_N-:1'b0)) = 0;
		if (SCE == 1'b1)
			(posedge CLK => (Q_N-:((D && SCD) || (D && !SCD && !SCE) || (!D && SCD && SCE)))) = 0;
		ifnone (CLK => Q_N) = 0;
		$setuphold (posedge CLK, posedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, negedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, posedge SCD, 0, 0, notifier,,, delayed_CLK, delayed_SCD);
		$setuphold (posedge CLK, negedge SCD, 0, 0, notifier,,, delayed_CLK, delayed_SCD);
		$setuphold (posedge CLK, posedge SCE, 0, 0, notifier,,, delayed_CLK, delayed_SCE);
		$setuphold (posedge CLK, negedge SCE, 0, 0, notifier,,, delayed_CLK, delayed_SCE);
		$recrem (posedge RESET_B, posedge CLK, 0, 0, notifier,,, delayed_RESET_B, delayed_CLK);
		$width (negedge RESET_B, 0, 0, notifier);
		$width (posedge CLK, 0, 0, notifier);
	endspecify

endmodule
`endcelldefine


// type: sdfrbp 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_sdfrbp_2
//   cell_description : Posedge Two-Outputs Q and Q_N D-Flip-Flop with Reset and Scan
//*****************************************************************

module sg13cmos5l_sdfrbp_2 (Q, Q_N, CLK, D, RESET_B, SCD, SCE
		        `ifdef USE_POWER_PINS , VDD, VSS `endif
		       );
		
	output Q, Q_N;
	input CLK, D, RESET_B, SCD, SCE;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif
	reg notifier;
	wire delayed_D, delayed_SCD, delayed_SCE, delayed_RESET_B, delayed_CLK;


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Q;
    wire raw_Q_N;
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    wire power_aware_notifier = notifier ^ (power_good ? 1'b0 : 1'bx);
`else
    wire power_aware_notifier = notifier;
`endif

	// Function
	wire int_fwire_d, int_fwire_IQ, int_fwire_IQN;
	wire int_fwire_r, xcr_0;

	ihp_mux2 (int_fwire_d, delayed_D, delayed_SCD, delayed_SCE);
	not (int_fwire_r, delayed_RESET_B);
	buf (xcr_0, 0);
	ihp_dff_r (int_fwire_IQ, power_aware_notifier, delayed_CLK, int_fwire_d, int_fwire_r, xcr_0);
	buf (raw_Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (raw_Q_N, int_fwire_IQN);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    assign Q = power_good ? raw_Q : 1'bx;
    assign Q_N = power_good ? raw_Q_N : 1'bx;
`else
    buf (Q, raw_Q);
    buf (Q_N, raw_Q_N);
`endif


    specify
		(negedge RESET_B => (Q+:1'b0)) = 0;
		if (SCE == 1'b1)
			(posedge CLK => (Q+:((D && SCD) || (D && !SCD && !SCE) || (!D && SCD && SCE)))) = 0;
		ifnone (CLK => Q) = 0;
		(negedge RESET_B => (Q_N-:1'b0)) = 0;
		if (SCE == 1'b1)
			(posedge CLK => (Q_N-:((D && SCD) || (D && !SCD && !SCE) || (!D && SCD && SCE)))) = 0;
		ifnone (CLK => Q_N) = 0;
		$setuphold (posedge CLK, posedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, negedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, posedge SCD, 0, 0, notifier,,, delayed_CLK, delayed_SCD);
		$setuphold (posedge CLK, negedge SCD, 0, 0, notifier,,, delayed_CLK, delayed_SCD);
		$setuphold (posedge CLK, posedge SCE, 0, 0, notifier,,, delayed_CLK, delayed_SCE);
		$setuphold (posedge CLK, negedge SCE, 0, 0, notifier,,, delayed_CLK, delayed_SCE);
		$recrem (posedge RESET_B, posedge CLK, 0, 0, notifier,,, delayed_RESET_B, delayed_CLK);
		$width (negedge RESET_B, 0, 0, notifier);
		$width (posedge CLK, 0, 0, notifier);
	endspecify

endmodule
`endcelldefine


// type: sdfrbpq 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_sdfrbpq_1
//   cell_description : Posedge Single-Output Q D-Flip-Flop with Reset and Scan
//*****************************************************************

module sg13cmos5l_sdfrbpq_1 (Q, CLK, D, RESET_B, SCD, SCE
			 `ifdef USE_POWER_PINS , VDD, VSS `endif
			);
		
	output Q;
	input CLK, D, RESET_B, SCD, SCE;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif
	reg notifier;
	wire delayed_D, delayed_SCD, delayed_SCE, delayed_RESET_B, delayed_CLK;


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Q;
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    wire power_aware_notifier = notifier ^ (power_good ? 1'b0 : 1'bx);
`else
    wire power_aware_notifier = notifier;
`endif

	// Function
	wire int_fwire_d, int_fwire_IQ, int_fwire_r;
	wire xcr_0;

	ihp_mux2 (int_fwire_d, delayed_D, delayed_SCD, delayed_SCE);
	not (int_fwire_r, delayed_RESET_B);
	buf (xcr_0, 0);
	ihp_dff_r (int_fwire_IQ, power_aware_notifier, delayed_CLK, int_fwire_d, int_fwire_r, xcr_0);
	buf (raw_Q, int_fwire_IQ);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    assign Q = power_good ? raw_Q : 1'bx;
`else
    buf (Q, raw_Q);
`endif


    specify
		(negedge RESET_B => (Q+:1'b0)) = 0;
		if (SCE == 1'b1)
			(posedge CLK => (Q+:((D && SCD) || (D && !SCD && !SCE) || (!D && SCD && SCE)))) = 0;
		if (SCE == 1'b0)
			(posedge CLK => (Q+:((D && SCD) || (D && !SCD && !SCE) || (!D && SCD && SCE)))) = 0;
		ifnone (CLK => Q) = 0;
		$setuphold (posedge CLK, posedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, negedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, posedge SCD, 0, 0, notifier,,, delayed_CLK, delayed_SCD);
		$setuphold (posedge CLK, negedge SCD, 0, 0, notifier,,, delayed_CLK, delayed_SCD);
		$setuphold (posedge CLK, posedge SCE, 0, 0, notifier,,, delayed_CLK, delayed_SCE);
		$setuphold (posedge CLK, negedge SCE, 0, 0, notifier,,, delayed_CLK, delayed_SCE);
		$recrem (posedge RESET_B, posedge CLK, 0, 0, notifier,,, delayed_RESET_B, delayed_CLK);
		$width (negedge RESET_B, 0, 0, notifier);
		$width (posedge CLK, 0, 0, notifier);
		$width (negedge CLK, 0, 0, notifier);
	endspecify

endmodule
`endcelldefine


// type: sdfrbpq 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_sdfrbpq_2
//   cell_description : Posedge Single-Output Q D-Flip-Flop with Reset and Scan
//*****************************************************************

module sg13cmos5l_sdfrbpq_2 (Q, CLK, D, RESET_B, SCD, SCE
			 `ifdef USE_POWER_PINS , VDD, VSS `endif
			);
		
	output Q;
	input CLK, D, RESET_B, SCD, SCE;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif
	reg notifier;
	wire delayed_D, delayed_SCD, delayed_SCE, delayed_RESET_B, delayed_CLK;


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Q;
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    wire power_aware_notifier = notifier ^ (power_good ? 1'b0 : 1'bx);
`else
    wire power_aware_notifier = notifier;
`endif

	// Function
	wire int_fwire_d, int_fwire_IQ, int_fwire_r;
	wire xcr_0;

	ihp_mux2 (int_fwire_d, delayed_D, delayed_SCD, delayed_SCE);
	not (int_fwire_r, delayed_RESET_B);
	buf (xcr_0, 0);
	ihp_dff_r (int_fwire_IQ, power_aware_notifier, delayed_CLK, int_fwire_d, int_fwire_r, xcr_0);
	buf (raw_Q, int_fwire_IQ);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    assign Q = power_good ? raw_Q : 1'bx;
`else
    buf (Q, raw_Q);
`endif


    specify
		(negedge RESET_B => (Q+:1'b0)) = 0;
		if (SCE == 1'b1)
			(posedge CLK => (Q+:((D && SCD) || (D && !SCD && !SCE) || (!D && SCD && SCE)))) = 0;
		if (SCE == 1'b0)
			(posedge CLK => (Q+:((D && SCD) || (D && !SCD && !SCE) || (!D && SCD && SCE)))) = 0;
		ifnone (CLK => Q) = 0;
		$setuphold (posedge CLK, posedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, negedge D, 0, 0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, posedge SCD, 0, 0, notifier,,, delayed_CLK, delayed_SCD);
		$setuphold (posedge CLK, negedge SCD, 0, 0, notifier,,, delayed_CLK, delayed_SCD);
		$setuphold (posedge CLK, posedge SCE, 0, 0, notifier,,, delayed_CLK, delayed_SCE);
		$setuphold (posedge CLK, negedge SCE, 0, 0, notifier,,, delayed_CLK, delayed_SCE);
		$recrem (posedge RESET_B, posedge CLK, 0, 0, notifier,,, delayed_RESET_B, delayed_CLK);
		$width (negedge RESET_B, 0, 0, notifier);
		$width (posedge CLK, 0, 0, notifier);
		$width (negedge CLK, 0, 0, notifier);
	endspecify

endmodule
`endcelldefine


// type: slgcp 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_slgcp_1
//   cell_description : Scan gated clock
//*****************************************************************

module sg13cmos5l_slgcp_1 (GCLK, GATE, CLK, SCE
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output GCLK;
	input GATE, CLK, SCE;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif
	reg notifier;
	wire delayed_GATE, delayed_SCE, delayed_CLK;


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_GCLK;
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    wire power_aware_notifier = notifier ^ (power_good ? 1'b0 : 1'bx);
`else
    wire power_aware_notifier = notifier;
`endif

	// Function

	wire int_fwire_clk, int_fwire_int_GATE, int_fwire_test;

	not (int_fwire_clk, delayed_CLK);
	or (int_fwire_test, delayed_GATE, delayed_SCE);
	ihp_latch (int_fwire_int_GATE, power_aware_notifier, int_fwire_clk, int_fwire_test);
	and (raw_GCLK, delayed_CLK, int_fwire_int_GATE);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    assign GCLK = power_good ? raw_GCLK : 1'bx;
`else
    buf (GCLK, raw_GCLK);
`endif


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

//type: sighold
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_sighold
//   cell_description : Leakage current compensator (bus holder)
//*****************************************************************

module sg13cmos5l_sighold (SH
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );

   inout SH;
   `ifdef USE_POWER_PINS inout VDD, VSS; `endif

// Logic section

`ifdef USE_POWER_PINS
    wire power_good;
    assign power_good = (VDD === 1'b1) && (VSS === 1'b0);
`endif

`ifdef DISPLAY_HOLD

    wire n1;

    buf (n1, SH);

    `ifdef USE_POWER_PINS
        // Bus keeper is active only when properly powered.
        bufif1 (pull1, pull0) (SH, n1, power_good);
    `else
        // Original behavior without power awareness.
        buf (pull1, pull0) (SH, n1);
    `endif

    initial begin
        #0 $display("  > Warning: compiler directive DISPLAY_HOLD is set in cell");
           $display("  > %m");
           $display("  > sg13cmos5l_sighold cell model is switched to provide logic levels");
           $display("  >  - danger of reading not really driven values");
           $display("  >  - undriven bus states are not detectable now");
           $display("  >");
    end

`else

    // No holding behavior is modeled.
    // The bus holder does not drive SH.

    wire n1;

    buf (n1, SH);
    bufif1 (SH, n1, 1'b0);

`endif

// no timing modelled for sg13cmos5l_sighold cell
// no backannotation possible for sg13cmos5l_sighold cell 
    
	
        // Timing

	specify
	endspecify

endmodule
//****************************************************************************
`endcelldefine


// type: tiehi 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_tiehi
//   cell_description : Constant logic 0
//*****************************************************************

module sg13cmos5l_tiehi (L_HI
		     `ifdef USE_POWER_PINS , VDD, VSS `endif
		    );
		
	output L_HI;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_L_HI;

	// Function

	buf (raw_L_HI, 1'b1);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign L_HI = power_good ? raw_L_HI : 1'bx;
`else
    buf (L_HI, raw_L_HI);
`endif

    specify
	endspecify

endmodule
`endcelldefine


// type: tielo 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_tielo
//   cell_description : Constant logic 1
//*****************************************************************

module sg13cmos5l_tielo (L_LO
		     `ifdef USE_POWER_PINS , VDD, VSS `endif
		    );
		
	output L_LO;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_L_LO;

	// Function

	buf (raw_L_LO, 1'b0);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign L_LO = power_good ? raw_L_LO : 1'bx;
`else
    buf (L_LO, raw_L_LO);
`endif

    specify
	endspecify

endmodule
`endcelldefine


// type: xnor2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_xnor2_1
//   cell_description : 2-input XNOR
//*****************************************************************

module sg13cmos5l_xnor2_1 (Y, A, B
		       `ifdef USE_POWER_PINS , VDD, VSS `endif
		      );
		
	output Y;
	input A, B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_Y;

	// Function

	wire int_fwire_0;

	xor (int_fwire_0, A, B);
	not (raw_Y, int_fwire_0);
        
        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign Y = power_good ? raw_Y : 1'bx;
`else
    buf (Y, raw_Y);
`endif

    specify
		if ((B == 1'b1))
			(A => Y) = 0;
		ifnone (A => Y) = 0;
		if ((B == 1'b0))
			(A => Y) = 0;
		if ((A == 1'b1))
			(B => Y) = 0;
		ifnone (B => Y) = 0;
		if ((A == 1'b0))
			(B => Y) = 0;
	endspecify

endmodule
`endcelldefine


// type: xor2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : sg13cmos5l
//   module name      : sg13cmos5l_xor2_1
//   cell_description : 2-input XOR
//*****************************************************************

module sg13cmos5l_xor2_1 (X, A, B
		      `ifdef USE_POWER_PINS , VDD, VSS `endif
		     );
		
	output X;
	input A, B;
	`ifdef USE_POWER_PINS inout VDD, VSS; `endif


    // Explicit declarations before primitive instantiations (avoid implicit nets).
    wire raw_X;

	// Function

	xor (raw_X, A, B);

        // Timing

	
    // Power-aware functional output gating (enabled only with USE_POWER_PINS).
`ifdef USE_POWER_PINS
    wire power_good = (VDD === 1'b1) && (VSS === 1'b0);
    assign X = power_good ? raw_X : 1'bx;
`else
    buf (X, raw_X);
`endif

    specify
		if ((B == 1'b0))
			(A => X) = 0;
		ifnone (A => X) = 0;
		if ((B == 1'b1))
			(A => X) = 0;
		if ((A == 1'b0))
			(B => X) = 0;
		ifnone (B => X) = 0;
		if ((A == 1'b1))
			(B => X) = 0;
	endspecify

endmodule
`endcelldefine
