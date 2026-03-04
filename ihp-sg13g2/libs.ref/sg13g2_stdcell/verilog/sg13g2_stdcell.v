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
//   technology       : SG13G2
//   module name      : sg13g2_a21o_1
//   cell_description : 2-input AND into first input of 2-input OR.
//*****************************************************************

module sg13g2_a21o_1 (X, A1, A2, B1);
	
	output X;
	input A1, A2, B1;

	// Function
	wire int_fwire_0;

	and (int_fwire_0, A1, A2);
	or (X, int_fwire_0, B1);

	// Timing

	specify
		if (B1 == 1'b0)
			(posedge A1 => (X : A1)) = (0.0,0.0);
		if (B1 == 1'b0)
			(negedge A1 => (X : A1)) = (0.0,0.0);
		ifnone 
			(posedge A1 => (X : A1)) = (0.0,0.0);
		ifnone 
			(negedge A1 => (X : A1)) = (0.0,0.0);
		if (B1 == 1'b0)
			(posedge A2 => (X : A2)) = (0.0,0.0);
		if (B1 == 1'b0)
			(negedge A2 => (X : A2)) = (0.0,0.0);
		ifnone 
			(posedge A2 => (X : A2)) = (0.0,0.0);
		ifnone 
			(negedge A2 => (X : A2)) = (0.0,0.0);
		if (A1 == 1'b1 && A2 == 1'b0)
			(posedge B1 => (X : B1)) = (0.0,0.0);
		if (A1 == 1'b1 && A2 == 1'b0)
			(negedge B1 => (X : B1)) = (0.0,0.0);
		if (A1 == 1'b0 && A2 == 1'b1)
			(posedge B1 => (X : B1)) = (0.0,0.0);
		if (A1 == 1'b0 && A2 == 1'b1)
			(negedge B1 => (X : B1)) = (0.0,0.0);
		if (A1 == 1'b0 && A2 == 1'b0)
			(posedge B1 => (X : B1)) = (0.0,0.0);
		if (A1 == 1'b0 && A2 == 1'b0)
			(negedge B1 => (X : B1)) = (0.0,0.0);
		ifnone 
			(posedge B1 => (X : B1)) = (0.0,0.0);
		ifnone 
			(negedge B1 => (X : B1)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: a21o 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_a21o_2
//   cell_description : 2-input AND into first input of 2-input OR.
//*****************************************************************

module sg13g2_a21o_2 (X, A1, A2, B1);
		
	output X;
	input A1, A2, B1;

	// Function

	wire int_fwire_0;

	and (int_fwire_0, A1, A2);
	or (X, int_fwire_0, B1);
        
	// Timing

	specify
		if (B1 == 1'b0)
			(posedge A1 => (X : A1)) = (0.0,0.0);
		if (B1 == 1'b0)
			(negedge A1 => (X : A1)) = (0.0,0.0);
		ifnone 
			(posedge A1 => (X : A1)) = (0.0,0.0);
		ifnone 
			(negedge A1 => (X : A1)) = (0.0,0.0);
		if (B1 == 1'b0)
			(posedge A2 => (X : A2)) = (0.0,0.0);
		if (B1 == 1'b0)
			(negedge A2 => (X : A2)) = (0.0,0.0);
		ifnone 
			(posedge A2 => (X : A2)) = (0.0,0.0);
		ifnone 
			(negedge A2 => (X : A2)) = (0.0,0.0);
		if (A1 == 1'b1 && A2 == 1'b0)
			(posedge B1 => (X : B1)) = (0.0,0.0);
		if (A1 == 1'b1 && A2 == 1'b0)
			(negedge B1 => (X : B1)) = (0.0,0.0);
		if (A1 == 1'b0 && A2 == 1'b1)
			(posedge B1 => (X : B1)) = (0.0,0.0);
		if (A1 == 1'b0 && A2 == 1'b1)
			(negedge B1 => (X : B1)) = (0.0,0.0);
		if (A1 == 1'b0 && A2 == 1'b0)
			(posedge B1 => (X : B1)) = (0.0,0.0);
		if (A1 == 1'b0 && A2 == 1'b0)
			(negedge B1 => (X : B1)) = (0.0,0.0);
		ifnone 
			(posedge B1 => (X : B1)) = (0.0,0.0);
		ifnone 
			(negedge B1 => (X : B1)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: a21oi 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_a21oi_1
//   cell_description : 2-input AND into first input of 2-input NOR.
//*****************************************************************

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
		(posedge A1 => (Y : A1)) = (0.0,0.0);
		(negedge A1 => (Y : A1)) = (0.0,0.0);
		(posedge A2 => (Y : A2)) = (0.0,0.0);
		(negedge A2 => (Y : A2)) = (0.0,0.0);
		if ((A1 == 1'b1 && A2 == 1'b0))
			(posedge B1 => (Y : B1)) = (0.0,0.0);
		if ((A1 == 1'b1 && A2 == 1'b0))
			(negedge B1 => (Y : B1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b1))
			(posedge B1 => (Y : B1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b1))
			(negedge B1 => (Y : B1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b0))
			(posedge B1 => (Y : B1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b0))
			(negedge B1 => (Y : B1)) = (0.0,0.0);
		ifnone 
			(posedge B1 => (Y : B1)) = (0.0,0.0);
		ifnone 
			(negedge B1 => (Y : B1)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: a21oi 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_a21oi_2
//   cell_description : 2-input AND into first input of 2-input NOR.
//*****************************************************************

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
		(posedge A1 => (Y : A1)) = (0.0,0.0);
		(negedge A1 => (Y : A1)) = (0.0,0.0);
		(posedge A2 => (Y : A2)) = (0.0,0.0);
		(negedge A2 => (Y : A2)) = (0.0,0.0);
		if ((A1 == 1'b1 && A2 == 1'b0))
			(posedge B1 => (Y : B1)) = (0.0,0.0);
		if ((A1 == 1'b1 && A2 == 1'b0))
			(negedge B1 => (Y : B1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b1))
			(posedge B1 => (Y : B1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b1))
			(negedge B1 => (Y : B1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b0))
			(posedge B1 => (Y : B1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b0))
			(negedge B1 => (Y : B1)) = (0.0,0.0);
		ifnone 
			(posedge B1 => (Y : B1)) = (0.0,0.0);
		ifnone 
			(negedge B1 => (Y : B1)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: a221oi 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_a221oi_1
//   cell_description : 2-input AND into first two inputs of 3-input NOR.
//*****************************************************************

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
		if ((A2 == 1'b1 && B1 == 1'b1 && B2 == 1'b0 && C1 == 1'b0))
			(posedge A1 => (Y : A1)) = (0.0,0.0);
		if ((A2 == 1'b1 && B1 == 1'b1 && B2 == 1'b0 && C1 == 1'b0))
			(negedge A1 => (Y : A1)) = (0.0,0.0);
		if ((A2 == 1'b1 && B1 == 1'b0 && B2 == 1'b1 && C1 == 1'b0))
			(posedge A1 => (Y : A1)) = (0.0,0.0);
		if ((A2 == 1'b1 && B1 == 1'b0 && B2 == 1'b1 && C1 == 1'b0))
			(negedge A1 => (Y : A1)) = (0.0,0.0);
		if ((A2 == 1'b1 && B1 == 1'b0 && B2 == 1'b0 && C1 == 1'b0))
			(posedge A1 => (Y : A1)) = (0.0,0.0);
		if ((A2 == 1'b1 && B1 == 1'b0 && B2 == 1'b0 && C1 == 1'b0))
			(negedge A1 => (Y : A1)) = (0.0,0.0);
		ifnone 
			(posedge A1 => (Y : A1)) = (0.0,0.0);
		ifnone 
			(negedge A1 => (Y : A1)) = (0.0,0.0);
		if ((A1 == 1'b1 && B1 == 1'b1 && B2 == 1'b0 && C1 == 1'b0))
			(posedge A2 => (Y : A2)) = (0.0,0.0);
		if ((A1 == 1'b1 && B1 == 1'b1 && B2 == 1'b0 && C1 == 1'b0))
			(negedge A2 => (Y : A2)) = (0.0,0.0);
		if ((A1 == 1'b1 && B1 == 1'b0 && B2 == 1'b1 && C1 == 1'b0))
			(posedge A2 => (Y : A2)) = (0.0,0.0);
		if ((A1 == 1'b1 && B1 == 1'b0 && B2 == 1'b1 && C1 == 1'b0))
			(negedge A2 => (Y : A2)) = (0.0,0.0);
		if ((A1 == 1'b1 && B1 == 1'b0 && B2 == 1'b0 && C1 == 1'b0))
			(posedge A2 => (Y : A2)) = (0.0,0.0);
		if ((A1 == 1'b1 && B1 == 1'b0 && B2 == 1'b0 && C1 == 1'b0))
			(negedge A2 => (Y : A2)) = (0.0,0.0);
		ifnone 
			(posedge A2 => (Y : A2)) = (0.0,0.0);
		ifnone 
			(negedge A2 => (Y : A2)) = (0.0,0.0);
		if ((A1 == 1'b1 && A2 == 1'b0 && B2 == 1'b1 && C1 == 1'b0))
			(posedge B1 => (Y : B1)) = (0.0,0.0);
		if ((A1 == 1'b1 && A2 == 1'b0 && B2 == 1'b1 && C1 == 1'b0))
			(negedge B1 => (Y : B1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b1 && B2 == 1'b1 && C1 == 1'b0))
			(posedge B1 => (Y : B1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b1 && B2 == 1'b1 && C1 == 1'b0))
			(negedge B1 => (Y : B1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b0 && B2 == 1'b1 && C1 == 1'b0))
			(posedge B1 => (Y : B1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b0 && B2 == 1'b1 && C1 == 1'b0))
			(negedge B1 => (Y : B1)) = (0.0,0.0);
		ifnone 
			(posedge B1 => (Y : B1)) = (0.0,0.0);
		ifnone 
			(negedge B1 => (Y : B1)) = (0.0,0.0);
		if ((A1 == 1'b1 && A2 == 1'b0 && B1 == 1'b1 && C1 == 1'b0))
			(posedge B2 => (Y : B2)) = (0.0,0.0);
		if ((A1 == 1'b1 && A2 == 1'b0 && B1 == 1'b1 && C1 == 1'b0))
			(negedge B2 => (Y : B2)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b1 && B1 == 1'b1 && C1 == 1'b0))
			(posedge B2 => (Y : B2)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b1 && B1 == 1'b1 && C1 == 1'b0))
			(negedge B2 => (Y : B2)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b0 && B1 == 1'b1 && C1 == 1'b0))
			(posedge B2 => (Y : B2)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b0 && B1 == 1'b1 && C1 == 1'b0))
			(negedge B2 => (Y : B2)) = (0.0,0.0);
		ifnone 
			(posedge B2 => (Y : B2)) = (0.0,0.0);
		ifnone 
			(negedge B2 => (Y : B2)) = (0.0,0.0);
		if ((A1 == 1'b1 && A2 == 1'b0 && B1 == 1'b0 && B2 == 1'b0))
			(posedge C1 => (Y : C1)) = (0.0,0.0);
		if ((A1 == 1'b1 && A2 == 1'b0 && B1 == 1'b0 && B2 == 1'b0))
			(negedge C1 => (Y : C1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b1 && B1 == 1'b0 && B2 == 1'b0))
			(posedge C1 => (Y : C1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b1 && B1 == 1'b0 && B2 == 1'b0))
			(negedge C1 => (Y : C1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b0 && B1 == 1'b1 && B2 == 1'b0))
			(posedge C1 => (Y : C1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b0 && B1 == 1'b1 && B2 == 1'b0))
			(negedge C1 => (Y : C1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b0 && B1 == 1'b0 && B2 == 1'b1))
			(posedge C1 => (Y : C1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b0 && B1 == 1'b0 && B2 == 1'b1))
			(negedge C1 => (Y : C1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b0 && B1 == 1'b0 && B2 == 1'b0))
			(posedge C1 => (Y : C1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b0 && B1 == 1'b0 && B2 == 1'b0))
			(negedge C1 => (Y : C1)) = (0.0,0.0);
		ifnone 
			(posedge C1 => (Y : C1)) = (0.0,0.0);
		ifnone 
			(negedge C1 => (Y : C1)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: a22oi 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_a22oi_1
//   cell_description : 2-input AND into both inputs of 2-input NOR.
//*****************************************************************

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
		if (A2 == 1'b1 && B1 == 1'b1)
			(posedge A1 => (Y : A1)) = (0.0,0.0);
		if (A2 == 1'b1 && B1 == 1'b1)
			(negedge A1 => (Y : A1)) = (0.0,0.0);
		ifnone 
			(posedge A1 => (Y : A1)) = (0.0,0.0);
		ifnone 
			(negedge A1 => (Y : A1)) = (0.0,0.0);
		if (A1 == 1'b1 && B1 == 1'b1)
			(posedge A2 => (Y : A2)) = (0.0,0.0);
		if (A1 == 1'b1 && B1 == 1'b1)
			(negedge A2 => (Y : A2)) = (0.0,0.0);
		ifnone 
			(posedge A2 => (Y : A2)) = (0.0,0.0);
		ifnone 
			(negedge A2 => (Y : A2)) = (0.0,0.0);
		if (A1 == 1'b1 && A2 == 1'b0)
			(posedge B1 => (Y : B1)) = (0.0,0.0);
		if (A1 == 1'b1 && A2 == 1'b0)
			(negedge B1 => (Y : B1)) = (0.0,0.0);
		if (A1 == 1'b0 && A2 == 1'b1)
			(posedge B1 => (Y : B1)) = (0.0,0.0);
		if (A1 == 1'b0 && A2 == 1'b1)
			(negedge B1 => (Y : B1)) = (0.0,0.0);
		ifnone 
			(posedge B1 => (Y : B1)) = (0.0,0.0);
		ifnone 
			(negedge B1 => (Y : B1)) = (0.0,0.0);
		if (A1 == 1'b1 && A2 == 1'b0)
			(posedge B2 => (Y : B2)) = (0.0,0.0);
		if (A1 == 1'b1 && A2 == 1'b0)
			(negedge B2 => (Y : B2)) = (0.0,0.0);
		if (A1 == 1'b0 && A2 == 1'b1)
			(posedge B2 => (Y : B2)) = (0.0,0.0);
		if (A1 == 1'b0 && A2 == 1'b1)
			(negedge B2 => (Y : B2)) = (0.0,0.0);
		ifnone 
			(posedge B2 => (Y : B2)) = (0.0,0.0);
		ifnone 
			(negedge B2 => (Y : B2)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: and2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_and2_1
//   cell_description : 2-input AND
//*****************************************************************

module sg13g2_and2_1 (X, A, B);
		
	output X;
	input A, B;

	// Function

	and (X, A, B);

        // Timing

	specify
		(posedge A => (X : A)) = (0.0,0.0);
		(negedge A => (X : A)) = (0.0,0.0);
		(posedge B => (X : B)) = (0.0,0.0);
		(negedge B => (X : B)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: and2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_and2_2
//   cell_description : 2-input AND
//*****************************************************************

module sg13g2_and2_2 (X, A, B);
		
	output X;
	input A, B;

	// Function

	and (X, A, B);

        // Timing

	specify
		(posedge A => (X : A)) = (0.0,0.0);
		(negedge A => (X : A)) = (0.0,0.0);
		(posedge B => (X : B)) = (0.0,0.0);
		(negedge B => (X : B)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: and3 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_and3_1
//   cell_description : 3-input AND
//*****************************************************************

module sg13g2_and3_1 (X, A, B, C);
		
	output X;
	input A, B, C;

	// Function

	and (X, A, B, C);

        // Timing

	specify
		(posedge A => (X : A)) = (0.0,0.0);
		(negedge A => (X : A)) = (0.0,0.0);
		(posedge B => (X : B)) = (0.0,0.0);
		(negedge B => (X : B)) = (0.0,0.0);
		(posedge C => (X : C)) = (0.0,0.0);
		(negedge C => (X : C)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: and3 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_sighold
//   cell_description : 3-input AND
//*****************************************************************

module sg13g2_and3_2 (X, A, B, C);
		
	output X;
	input A, B, C;

	// Function

	and (X, A, B, C);

        // Timing

	specify
		(posedge A => (X : A)) = (0.0,0.0);
		(negedge A => (X : A)) = (0.0,0.0);
		(posedge B => (X : B)) = (0.0,0.0);
		(negedge B => (X : B)) = (0.0,0.0);
		(posedge C => (X : C)) = (0.0,0.0);
		(negedge C => (X : C)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: and4 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_and4_1
//   cell_description : 4-input AND
//*****************************************************************

module sg13g2_and4_1 (X, A, B, C, D);
		
	output X;
	input A, B, C, D;

	// Function

	and (X, A, B, C, D);

	// Timing

	specify
		(posedge A => (X : A)) = (0.0,0.0);
		(negedge A => (X : A)) = (0.0,0.0);
		(posedge B => (X : B)) = (0.0,0.0);
		(negedge B => (X : B)) = (0.0,0.0);
		(posedge C => (X : C)) = (0.0,0.0);
		(negedge C => (X : C)) = (0.0,0.0);
		(posedge D => (X : D)) = (0.0,0.0);
		(negedge D => (X : D)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: and4 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_and4_2
//   cell_description : 4-input AND
//*****************************************************************

module sg13g2_and4_2 (X, A, B, C, D);
		
	output X;
	input A, B, C, D;

	// Function

	and (X, A, B, C, D);

        // Timing

	specify
		(posedge A => (X : A)) = (0.0,0.0);
		(negedge A => (X : A)) = (0.0,0.0);
		(posedge B => (X : B)) = (0.0,0.0);
		(negedge B => (X : B)) = (0.0,0.0);
		(posedge C => (X : C)) = (0.0,0.0);
		(negedge C => (X : C)) = (0.0,0.0);
		(posedge D => (X : D)) = (0.0,0.0);
		(negedge D => (X : D)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: antennanp 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_antennanp
//   cell_description : Antenna effect protection cell (gate charge) at manufacture, P-diode in N-Well, N-diode in substrate
//*****************************************************************

module sg13g2_antennanp (A);
	input A;

        // Timing

	specify
	endspecify

endmodule
`endcelldefine

// type: buf 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_buf_1
//   cell_description : Buffer drive strength 1
//*****************************************************************

module sg13g2_buf_1 (X, A);
		
	output X;
	input A;

	// Function

	buf (X, A);

        // Timing

	specify
		(posedge A => (X : A)) = (0.0,0.0);
		(negedge A => (X : A)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: buf 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_buf_16
//   cell_description : Buffer drive strength 16
//*****************************************************************

module sg13g2_buf_16 (X, A);
		
	output X;
	input A;

	// Function

	buf (X, A);

        // Timing

	specify
		(posedge A => (X : A)) = (0.0,0.0);
		(negedge A => (X : A)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: buf 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_buf_2
//   cell_description : Buffer drive strength 2
//*****************************************************************

module sg13g2_buf_2 (X, A);
		
	output X;
	input A;

	// Function

	buf (X, A);

        // Timing

	specify
		(posedge A => (X : A)) = (0.0,0.0);
		(negedge A => (X : A)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: buf 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_buf_4
//   cell_description : Buffer drive strength 4
//*****************************************************************

module sg13g2_buf_4 (X, A);
		
	output X;
	input A;

	// Function

	buf (X, A);

        // Timing

	specify
		(posedge A => (X : A)) = (0.0,0.0);
		(negedge A => (X : A)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: buf 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_buf_8
//   cell_description : Buffer drive strength 8
//*****************************************************************

module sg13g2_buf_8 (X, A);
		
	output X;
	input A;

	// Function

	buf (X, A);

        // Timing

	specify
		(posedge A => (X : A)) = (0.0,0.0);
		(negedge A => (X : A)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: decap 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_decap_4
//   cell_description : Decoupling capasitance filler cell
//*****************************************************************

module sg13g2_decap_4 ();

        // Timing

	specify
	endspecify

endmodule
`endcelldefine

// type: decap 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_decap_8
//   cell_description : Decoupling capasitance filler cell
//*****************************************************************

module sg13g2_decap_8 ();

        // Timing

	specify
	endspecify

endmodule
`endcelldefine

// type: dfrbp 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_dfrbp_1
//   cell_description : Posedge Two-Outputs Q and Q_N D-Flip-Flop with Low-Active Reset
//*****************************************************************

module sg13g2_dfrbp_1 (Q, Q_N, CLK, D, RESET_B);
		
	output Q, Q_N;
	input CLK, D, RESET_B;
	reg notifier;
	wire delayed_D, delayed_RESET_B, delayed_CLK;

	// Function
	wire int_fwire_IQ, int_fwire_IQN, int_fwire_r;
	wire xcr_0;

	not (int_fwire_r, delayed_RESET_B);
	buf (xcr_0, 0);
	ihp_dff_r (int_fwire_IQ, notifier, delayed_CLK, delayed_D, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (Q_N, int_fwire_IQN);

        // Timing

	specify
		(negedge RESET_B => (Q :1'b0)) = (0.0,0.0);
		(posedge CLK => (Q : D)) = (0.0,0.0);
		(negedge CLK => (Q : D)) = (0.0,0.0);
		(negedge RESET_B => (Q_N :1'b0)) = (0.0,0.0);
		(posedge CLK => (Q_N : D)) = (0.0,0.0);
		(negedge CLK => (Q_N : D)) = (0.0,0.0);
		$setuphold (posedge CLK, posedge D, 0.0, 0.0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, negedge D, 0.0, 0.0, notifier,,, delayed_CLK, delayed_D);
		$recrem (posedge RESET_B, posedge CLK, 0.0, 0.0, notifier,,, delayed_RESET_B, delayed_CLK);
		$width (negedge RESET_B, 0.0, 0, notifier);
		$width (posedge CLK, 0.0, 0, notifier);
		$width (negedge CLK, 0.0, 0, notifier);
	endspecify

endmodule
`endcelldefine

// type: dfrbp 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_dfrbp_2
//   cell_description : Posedge Two-Outputs Q and Q_N D-Flip-Flop with Low-Active Reset
//*****************************************************************

module sg13g2_dfrbp_2 (Q, Q_N, CLK, D, RESET_B);
		
	output Q, Q_N;
	input CLK, D, RESET_B;
	reg notifier;
	wire delayed_D, delayed_RESET_B, delayed_CLK;

	// Function
	wire int_fwire_IQ, int_fwire_IQN, int_fwire_r;
	wire xcr_0;

	not (int_fwire_r, delayed_RESET_B);
	buf (xcr_0, 0);
	ihp_dff_r (int_fwire_IQ, notifier, delayed_CLK, delayed_D, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (Q_N, int_fwire_IQN);

        // Timing

	specify
		(negedge RESET_B => (Q :1'b0)) = (0.0,0.0);
		(posedge CLK => (Q : D)) = (0.0,0.0);
		(negedge CLK => (Q : D)) = (0.0,0.0);
		(negedge RESET_B => (Q_N :1'b0)) = (0.0,0.0);
		(posedge CLK => (Q_N : D)) = (0.0,0.0);
		(negedge CLK => (Q_N : D)) = (0.0,0.0);
		$setuphold (posedge CLK, posedge D, 0.0, 0.0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, negedge D, 0.0, 0.0, notifier,,, delayed_CLK, delayed_D);
		$recrem (posedge RESET_B, posedge CLK, 0.0, 0.0, notifier,,, delayed_RESET_B, delayed_CLK);
		$width (negedge RESET_B, 0.0, 0, notifier);
		$width (posedge CLK, 0.0, 0, notifier);
		$width (negedge CLK, 0.0, 0, notifier);
	endspecify

endmodule
`endcelldefine

// type: dfrbpq 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_dfrbpq_1
//   cell_description : Posedge Single-Output Q D-Flip-Flop with Low-Active Reset
//*****************************************************************

module sg13g2_dfrbpq_1 (Q, CLK, D, RESET_B);
		
	output Q;
	input CLK, D, RESET_B;
	reg notifier;
	wire delayed_D, delayed_RESET_B, delayed_CLK;

	// Function
	wire int_fwire_IQ, int_fwire_r, xcr_0;

	not (int_fwire_r, delayed_RESET_B);
	buf (xcr_0, 0);
	ihp_dff_r (int_fwire_IQ, notifier, delayed_CLK, delayed_D, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);

        // Timing

	specify
		(negedge RESET_B => (Q :1'b0)) = (0.0,0.0);
		(posedge CLK => (Q : D)) = (0.0,0.0);
		(negedge CLK => (Q : D)) = (0.0,0.0);
		$setuphold (posedge CLK, posedge D, 0.0, 0.0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, negedge D, 0.0, 0.0, notifier,,, delayed_CLK, delayed_D);
		$recrem (posedge RESET_B, posedge CLK, 0.0, 0.0, notifier,,, delayed_RESET_B, delayed_CLK);
		$width (negedge RESET_B, 0.0, 0, notifier);
		$width (posedge CLK, 0.0, 0, notifier);
		$width (negedge CLK, 0.0, 0, notifier);
	endspecify

endmodule
`endcelldefine

// type: dfrbpq 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_dfrbpq_2
//   cell_description : Posedge Single-Output Q D-Flip-Flop with Low-Active Reset
//*****************************************************************

module sg13g2_dfrbpq_2 (Q, CLK, D, RESET_B);
		
	output Q;
	input CLK, D, RESET_B;
	reg notifier;
	wire delayed_D, delayed_RESET_B, delayed_CLK;

	// Function
	wire int_fwire_IQ, int_fwire_r, xcr_0;

	not (int_fwire_r, delayed_RESET_B);
	buf (xcr_0, 0);
	ihp_dff_r (int_fwire_IQ, notifier, delayed_CLK, delayed_D, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);

        // Timing

	specify
		(negedge RESET_B => (Q :1'b0)) = (0.0,0.0);
		(posedge CLK => (Q : D)) = (0.0,0.0);
		(negedge CLK => (Q : D)) = (0.0,0.0);
		$setuphold (posedge CLK, posedge D, 0.0, 0.0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, negedge D, 0.0, 0.0, notifier,,, delayed_CLK, delayed_D);
		$recrem (posedge RESET_B, posedge CLK, 0.0, 0.0, notifier,,, delayed_RESET_B, delayed_CLK);
		$width (negedge RESET_B, 0.0, 0, notifier);
		$width (posedge CLK, 0.0, 0, notifier);
		$width (negedge CLK, 0.0, 0, notifier);
	endspecify

endmodule
`endcelldefine

// type: dlhq 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_dlhq_1
//   cell_description : High-Active GATE Single-Output Q D-latch
//*****************************************************************

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
		(posedge D => (Q : D)) = (0.0,0.0);
		(negedge D => (Q : D)) = (0.0,0.0);
		(posedge GATE => (Q : D)) = (0.0,0.0);
		(negedge GATE => (Q : D)) = (0.0,0.0);
		$setuphold (negedge GATE, posedge D, 0.0, 0.0, notifier,,, delayed_GATE, delayed_D);
		$setuphold (negedge GATE, negedge D, 0.0, 0.0, notifier,,, delayed_GATE, delayed_D);
		$width (posedge GATE, 0.0, 0, notifier);
	endspecify

endmodule
`endcelldefine

// type: dlhr 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_dlhr_1
//   cell_description : High-Active GATE Two-Outputs Q Q_N D-latch with Low-Active Reset
//*****************************************************************

module sg13g2_dlhr_1 (Q, Q_N, D, GATE, RESET_B);
		
	output Q, Q_N;
	input D, GATE, RESET_B;
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
		(posedge D => (Q : D)) = (0.0,0.0);
		(negedge D => (Q : D)) = (0.0,0.0);
		(negedge RESET_B => (Q :1'b0)) = (0.0,0.0);
		(posedge GATE => (Q : D)) = (0.0,0.0);
		(negedge GATE => (Q : D)) = (0.0,0.0);
		(posedge D => (Q_N : D)) = (0.0,0.0);
		(negedge D => (Q_N : D)) = (0.0,0.0);
		(negedge RESET_B => (Q_N :1'b0)) = (0.0,0.0);
		(posedge GATE => (Q_N : D)) = (0.0,0.0);
		(negedge GATE => (Q_N : D)) = (0.0,0.0);
		$setuphold (negedge GATE, posedge D, 0.0, 0.0, notifier,,, delayed_GATE, delayed_D);
		$setuphold (negedge GATE, negedge D, 0.0, 0.0, notifier,,, delayed_GATE, delayed_D);
		$recrem (posedge RESET_B, negedge GATE, 0.0, 0.0, notifier,,, delayed_RESET_B, delayed_GATE);
		$width (negedge RESET_B, 0.0, 0, notifier);
		$width (posedge GATE, 0.0, 0, notifier);
	endspecify

endmodule
`endcelldefine


// type: dlhrq 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_dlhrq_1
//   cell_description : High-Active Gate Single-Output Q D-latch with Low-Active Reset
//*****************************************************************

module sg13g2_dlhrq_1 (Q, D, GATE, RESET_B);
		
	output Q;
	input D, GATE, RESET_B;
	reg notifier;
	wire delayed_D, delayed_RESET_B, delayed_GATE;

	// Function

	wire int_fwire_IQ, int_fwire_r;

	not (int_fwire_r, delayed_RESET_B);
	ihp_latch_r (int_fwire_IQ, notifier, delayed_GATE, delayed_D, int_fwire_r);
	buf (Q, int_fwire_IQ);

        // Timing

	specify
		(posedge D => (Q : D)) = (0.0,0.0);
		(negedge D => (Q : D)) = (0.0,0.0);
		(negedge RESET_B => (Q :1'b0)) = (0.0,0.0);
		(posedge GATE => (Q : D)) = (0.0,0.0);
		(negedge GATE => (Q : D)) = (0.0,0.0);
		$setuphold (negedge GATE, posedge D, 0.0, 0.0, notifier,,, delayed_GATE, delayed_D);
		$setuphold (negedge GATE, negedge D, 0.0, 0.0, notifier,,, delayed_GATE, delayed_D);
		$recrem (posedge RESET_B, negedge GATE, 0.0, 0.0, notifier,,, delayed_RESET_B, delayed_GATE);
		$width (negedge RESET_B, 0.0, 0, notifier);
		$width (posedge GATE, 0.0, 0, notifier);
	endspecify

endmodule
`endcelldefine


// type: dllr 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_dllr_1
//   cell_description : Low-Active GATE_N Two-Outputs Q Q_N D-latch with Low-Active Reset
//*****************************************************************

module sg13g2_dllr_1 (Q, Q_N, D, GATE_N, RESET_B);
		
	output Q, Q_N;
	input D, GATE_N, RESET_B;
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
		(posedge D => (Q : D)) = (0.0,0.0);
		(negedge D => (Q : D)) = (0.0,0.0);
		(negedge RESET_B => (Q :1'b0)) = (0.0,0.0);
		(negedge GATE_N => (Q : D)) = (0.0,0.0);
		(posedge GATE_N => (Q : D)) = (0.0,0.0);
		(posedge D => (Q_N : D)) = (0.0,0.0);
		(negedge D => (Q_N : D)) = (0.0,0.0);
		(negedge RESET_B => (Q_N :1'b0)) = (0.0,0.0);
		(negedge GATE_N => (Q_N : D)) = (0.0,0.0);
		(posedge GATE_N => (Q_N : D)) = (0.0,0.0);
		$setuphold (posedge GATE_N, posedge D, 0.0, 0.0, notifier,,, delayed_GATE_N, delayed_D);
		$setuphold (posedge GATE_N, negedge D, 0.0, 0.0, notifier,,, delayed_GATE_N, delayed_D);
		$recrem (posedge RESET_B, posedge GATE_N, 0.0, 0.0, notifier,,, delayed_RESET_B, delayed_GATE_N);
		$width (negedge RESET_B, 0.0, 0, notifier);
		$width (negedge GATE_N, 0.0, 0, notifier);
	endspecify

endmodule
`endcelldefine


// type: dllrq 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_dllrq_1
//   cell_description : Low-Active GATE_N Single-Output Q D-latch with Low-Active Reset
//*****************************************************************

module sg13g2_dllrq_1 (Q, D, GATE_N, RESET_B);
		
	output Q;
	input D, GATE_N, RESET_B;
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
		(posedge D => (Q : D)) = (0.0,0.0);
		(negedge D => (Q : D)) = (0.0,0.0);
		(negedge RESET_B => (Q :1'b0)) = (0.0,0.0);
		(posedge RESET_B => (Q :1'b1)) = (0.0,0.0);
		(negedge GATE_N => (Q : D)) = (0.0,0.0);
		(posedge GATE_N => (Q : D)) = (0.0,0.0);
		$setuphold (posedge GATE_N, posedge D, 0.0, 0.0, notifier,,, delayed_GATE_N, delayed_D);
		$setuphold (posedge GATE_N, negedge D, 0.0, 0.0, notifier,,, delayed_GATE_N, delayed_D);
		$recrem (posedge RESET_B, posedge GATE_N, 0.0, 0.0, notifier,,, delayed_RESET_B, delayed_GATE_N);
		$width (negedge RESET_B, 0.0, 0, notifier);
		$width (negedge GATE_N, 0.0, 0, notifier);
	endspecify

endmodule
`endcelldefine


// type: dlygate4sd1 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_dlygate4sd1_1
//   cell_description : Delay Cell, typical 0.4 ns
//*****************************************************************

module sg13g2_dlygate4sd1_1 (X, A);
		
	output X;
	input A;

	// Function

	buf (X, A);

        // Timing

	specify
		(posedge A => (X : A)) = (0.0,0.0);
		(negedge A => (X : A)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: dlygate4sd2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_dlygate4sd2_1
//   cell_description : Delay Cell, typical 0.45 ns
//*****************************************************************

module sg13g2_dlygate4sd2_1 (X, A);
		
	output X;
	input A;

	// Function

	buf (X, A);

        // Timing

	specify
		(posedge A => (X : A)) = (0.0,0.0);
		(negedge A => (X : A)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: dlygate4sd3 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_dlygate4sd3_1
//   cell_description : Delay Cell, typical 0.7 ns
//*****************************************************************

module sg13g2_dlygate4sd3_1 (X, A);
		
	output X;
	input A;

	// Function

	buf (X, A);

        // Timing

	specify
		(posedge A => (X : A)) = (0.0,0.0);
		(negedge A => (X : A)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: ebufn 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_ebufn_2
//   cell_description : Tristate Buffer with Low-Active Enable TE_B
//*****************************************************************

module sg13g2_ebufn_2 (Z, A, TE_B);
		
	output Z;
	input A, TE_B;

	// Function

	bufif0 (Z, A, TE_B);

        // Timing

	specify
		(posedge A => (Z : A)) = (0.0,0.0);
		(negedge A => (Z : A)) = (0.0,0.0);
		(negedge TE_B => (Z:TE_B)) = (0.0,0.0);
		(posedge TE_B => (Z:TE_B)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: ebufn 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_ebufn_4
//   cell_description : Tristate Buffer with Low-Active Enable TE_B
//*****************************************************************

module sg13g2_ebufn_4 (Z, A, TE_B);
		
	output Z;
	input A, TE_B;

	// Function

	bufif0 (Z, A, TE_B);

        // Timing

	specify
		(posedge A => (Z : A)) = (0.0,0.0);
		(negedge A => (Z : A)) = (0.0,0.0);
		(negedge TE_B => (Z:TE_B)) = (0.0,0.0);
		(posedge TE_B => (Z:TE_B)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: ebufn 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_ebufn_8
//   cell_description : Tristate Buffer with Low-Active Enable TE_B
//*****************************************************************

module sg13g2_ebufn_8 (Z, A, TE_B);
		
	output Z;
	input A, TE_B;

	// Function

	bufif0 (Z, A, TE_B);

        // Timing

	specify
		(posedge A => (Z : A)) = (0.0,0.0);
		(negedge A => (Z : A)) = (0.0,0.0);
		(negedge TE_B => (Z:TE_B)) = (0.0,0.0);
		(posedge TE_B => (Z:TE_B)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: einvn 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_einvn_2
//   cell_description : Tristate Inverter with Low-Active Enable TE_B
//*****************************************************************

module sg13g2_einvn_2 (Z, A, TE_B);
		
	output Z;
	input A, TE_B;

	// Function

	notif0 (Z, A, TE_B);

        // Timing

	specify
		(posedge A => (Z : A)) = (0.0,0.0);
		(negedge A => (Z : A)) = (0.0,0.0);
		(posedge TE_B => (Z : TE_B)) = (0.0,0.0);
		(negedge TE_B => (Z : TE_B)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: einvn 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_einvn_4
//   cell_description : Tristate Inverter with Low-Active Enable TE_B
//*****************************************************************

module sg13g2_einvn_4 (Z, A, TE_B);
		
	output Z;
	input A, TE_B;

	// Function

	notif0 (Z, A, TE_B);

        // Timing

	specify
		(posedge A => (Z : A)) = (0.0,0.0);
		(negedge A => (Z : A)) = (0.0,0.0);
		(posedge TE_B => (Z : TE_B)) = (0.0,0.0);
		(negedge TE_B => (Z : TE_B)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: einvn 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_einvn_8
//   cell_description : Tristate Inverter with Low-Active Enable TE_B
//*****************************************************************

module sg13g2_einvn_8 (Z, A, TE_B);
		
	output Z;
	input A, TE_B;

	// Function

	notif0 (Z, A, TE_B);

        // Timing

	specify
		(posedge A => (Z : A)) = (0.0,0.0);
		(negedge A => (Z : A)) = (0.0,0.0);
		(posedge TE_B => (Z : TE_B)) = (0.0,0.0);
		(negedge TE_B => (Z : TE_B)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: fill 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_fill_1
//   cell_description : Filler 1 Track Width
//*****************************************************************

module sg13g2_fill_1 ();
 
       // Timing

	specify
	endspecify

endmodule
`endcelldefine


// type: fill 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_fill_2
//   cell_description : Filler 2 Tracks Width
//*****************************************************************

module sg13g2_fill_2 ();

        // Timing

	specify
	endspecify

endmodule
`endcelldefine


// type: fill 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_fill_4
//   cell_description : Filler 4 Tracks Width
//*****************************************************************

module sg13g2_fill_4 ();

        // Timing

	specify
	endspecify

endmodule
`endcelldefine


// type: fill 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_fill_8
//   cell_description : Filler 8 Tracks Width
//*****************************************************************

module sg13g2_fill_8 ();

        // Timing

	specify
	endspecify

endmodule
`endcelldefine


// type: inv 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_inv_1
//   cell_description : Inverter
//*****************************************************************

module sg13g2_inv_1 (Y, A);
		
	output Y;
	input A;

	// Function

	not (Y, A);

        // Timing

	specify
		(posedge A => (Y : A)) = (0.0,0.0);
		(negedge A => (Y : A)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: inv 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_inv_16
//   cell_description : Inverter
//*****************************************************************

module sg13g2_inv_16 (Y, A);
		
	output Y;
	input A;

	// Function

	not (Y, A);

        // Timing

	specify
		(posedge A => (Y : A)) = (0.0,0.0);
		(negedge A => (Y : A)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: inv 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_inv_2
//   cell_description : Inverter
//*****************************************************************

module sg13g2_inv_2 (Y, A);
		
	output Y;
	input A;

	// Function

	not (Y, A);

        // Timing

	specify
		(posedge A => (Y : A)) = (0.0,0.0);
		(negedge A => (Y : A)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: inv 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_inv_4
//   cell_description : Inverter
//*****************************************************************

module sg13g2_inv_4 (Y, A);
		
	output Y;
	input A;

	// Function

	not (Y, A);

        // Timing

	specify
		(posedge A => (Y : A)) = (0.0,0.0);
		(negedge A => (Y : A)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: inv 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_inv_8
//   cell_description : Inverter
//*****************************************************************

module sg13g2_inv_8 (Y, A);
		
	output Y;
	input A;

	// Function

	not (Y, A);

        // Timing

	specify
		(posedge A => (Y : A)) = (0.0,0.0);
		(negedge A => (Y : A)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: lgcp 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_lgcp_1
//   cell_description : Posedge Clock Gating cell, Low Latch Enable
//*****************************************************************

module sg13g2_lgcp_1 (GCLK, CLK, GATE);
		
	output GCLK;
	input CLK, GATE;
	reg notifier;
	wire delayed_GATE, delayed_CLK;

	// Function

	wire int_fwire_clk, int_fwire_int_GATE;

	not (int_fwire_clk, delayed_CLK);
	ihp_latch (int_fwire_int_GATE, notifier, int_fwire_clk, delayed_GATE);
	and (GCLK, delayed_CLK, int_fwire_int_GATE);

        // Timing

	specify
		(posedge CLK => (GCLK :CLK)) = (0.0,0.0);
		(negedge CLK => (GCLK :CLK)) = (0.0,0.0);
		$setuphold (posedge CLK, posedge GATE, 0.0, 0.0, notifier,,, delayed_CLK, delayed_GATE);
		$setuphold (posedge CLK, negedge GATE, 0.0, 0.0, notifier,,, delayed_CLK, delayed_GATE);
		$width (posedge CLK, 0.0, 0, notifier);
		$width (negedge CLK, 0.0, 0, notifier);
	endspecify

endmodule
`endcelldefine


// type: mux2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_mux2_1
//   cell_description : Multiplexer from 2 to 1
//*****************************************************************

module sg13g2_mux2_1 (X, A0, A1, S);
		
	output X;
	input A0, A1, S;

	// Function

	ihp_mux2 (X, A0, A1, S);

        // Timing

	specify
		(posedge A0 => (X : A0)) = (0.0,0.0);
		(negedge A0 => (X : A0)) = (0.0,0.0);
		(posedge A1 => (X : A1)) = (0.0,0.0);
		(negedge A1 => (X : A1)) = (0.0,0.0);
		if (A0 == 1'b0 && A1 == 1'b1)
			(posedge S => (X : S)) = (0.0,0.0);
		if (A0 == 1'b0 && A1 == 1'b1)
			(negedge S => (X : S)) = (0.0,0.0);
		ifnone 
			(negedge S => (X:S)) = (0.0,0.0);
		ifnone 
			(posedge S => (X:S)) = (0.0,0.0);
		if (A0 == 1'b1 && A1 == 1'b0)
			(posedge S => (X : S)) = (0.0,0.0);
		if (A0 == 1'b1 && A1 == 1'b0)
			(negedge S => (X : S)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// Verilog for cell sg13g2_mux2_2 created entirely by Liberate 23.1.3.126.isr3

// type: mux2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_mux2_2
//   cell_description : Multiplexer from 2 to 1
//*****************************************************************

module sg13g2_mux2_2 (X, A0, A1, S);
		
	output X;
	input A0, A1, S;

	// Function

	ihp_mux2 (X, A0, A1, S);

        // Timing

	specify
		(posedge A0 => (X : A0)) = (0.0,0.0);
		(negedge A0 => (X : A0)) = (0.0,0.0);
		(posedge A1 => (X : A1)) = (0.0,0.0);
		(negedge A1 => (X : A1)) = (0.0,0.0);
		if (A0 == 1'b0 && A1 == 1'b1)
			(posedge S => (X : S)) = (0.0,0.0);
		if (A0 == 1'b0 && A1 == 1'b1)
			(negedge S => (X : S)) = (0.0,0.0);
		ifnone 
			(negedge S => (X:S)) = (0.0,0.0);
		ifnone 
			(posedge S => (X:S)) = (0.0,0.0);
		if (A0 == 1'b1 && A1 == 1'b0)
			(posedge S => (X : S)) = (0.0,0.0);
		if (A0 == 1'b1 && A1 == 1'b0)
			(negedge S => (X : S)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: mux4 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_mux4_1
//   cell_description : Multiplexer from 4 to 1
//*****************************************************************

module sg13g2_mux4_1 (X, A0, A1, A2, A3, S0, S1);
		
	output X;
	input A0, A1, A2, A3, S0, S1;

	// Function

	ihp_mux4 (X, A0, A1, A2, A3, S0, S1);

        // Timing

	specify
		(posedge A0 => (X : A0)) = (0.0,0.0);
		(negedge A0 => (X : A0)) = (0.0,0.0);
		(posedge A1 => (X : A1)) = (0.0,0.0);
		(negedge A1 => (X : A1)) = (0.0,0.0);
		(posedge A2 => (X : A2)) = (0.0,0.0);
		(negedge A2 => (X : A2)) = (0.0,0.0);
		(posedge A3 => (X : A3)) = (0.0,0.0);
		(negedge A3 => (X : A3)) = (0.0,0.0);
		if (A2 == 1'b0 && A3 == 1'b1 && S1 == 1'b1)
			(posedge S0 => (X : S0)) = (0.0,0.0);
		if (A2 == 1'b0 && A3 == 1'b1 && S1 == 1'b1)
			(negedge S0 => (X : S0)) = (0.0,0.0);
		if (A0 == 1'b0 && A1 == 1'b1 && S1 == 1'b0)
			(posedge S0 => (X : S0)) = (0.0,0.0);
		if (A0 == 1'b0 && A1 == 1'b1 && S1 == 1'b0)
			(negedge S0 => (X : S0)) = (0.0,0.0);
		ifnone 
			(negedge S0 => (X:S0)) = (0.0,0.0);
		ifnone 
			(posedge S0 => (X:S0)) = (0.0,0.0);
		if (A2 == 1'b1 && A3 == 1'b0 && S1 == 1'b1)
			(posedge S0 => (X : S0)) = (0.0,0.0);
		if (A2 == 1'b1 && A3 == 1'b0 && S1 == 1'b1)
			(negedge S0 => (X : S0)) = (0.0,0.0);
		if (A0 == 1'b1 && A1 == 1'b0 && S1 == 1'b0)
			(posedge S0 => (X : S0)) = (0.0,0.0);
		if (A0 == 1'b1 && A1 == 1'b0 && S1 == 1'b0)
			(negedge S0 => (X : S0)) = (0.0,0.0);
		if (A1 == 1'b0 && A3 == 1'b1 && S0 == 1'b1)
			(posedge S1 => (X : S1)) = (0.0,0.0);
		if (A1 == 1'b0 && A3 == 1'b1 && S0 == 1'b1)
			(negedge S1 => (X : S1)) = (0.0,0.0);
		if (A0 == 1'b0 && A2 == 1'b1 && S0 == 1'b0)
			(posedge S1 => (X : S1)) = (0.0,0.0);
		if (A0 == 1'b0 && A2 == 1'b1 && S0 == 1'b0)
			(negedge S1 => (X : S1)) = (0.0,0.0);
		ifnone 
			(negedge S1 => (X:S1)) = (0.0,0.0);
		ifnone 
			(posedge S1 => (X:S1)) = (0.0,0.0);
		if (A1 == 1'b1 && A3 == 1'b0 && S0 == 1'b1)
			(posedge S1 => (X : S1)) = (0.0,0.0);
		if (A1 == 1'b1 && A3 == 1'b0 && S0 == 1'b1)
			(negedge S1 => (X : S1)) = (0.0,0.0);
		if (A0 == 1'b1 && A2 == 1'b0 && S0 == 1'b0)
			(posedge S1 => (X : S1)) = (0.0,0.0);
		if (A0 == 1'b1 && A2 == 1'b0 && S0 == 1'b0)
			(negedge S1 => (X : S1)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: nand2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_nand2_1
//   cell_description : 2-input NAND
//*****************************************************************

module sg13g2_nand2_1 (Y, A, B);
		
	output Y;
	input A, B;

	// Function

	wire int_fwire_0;

	and (int_fwire_0, A, B);
	not (Y, int_fwire_0);

        // Timing

	specify
		(posedge A => (Y : A)) = (0.0,0.0);
		(negedge A => (Y : A)) = (0.0,0.0);
		(posedge B => (Y : B)) = (0.0,0.0);
		(negedge B => (Y : B)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: nand2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_nand2_2
//   cell_description : 2-input NAND
//*****************************************************************

module sg13g2_nand2_2 (Y, A, B);
		
	output Y;
	input A, B;

	// Function

	wire int_fwire_0;

	and (int_fwire_0, A, B);
	not (Y, int_fwire_0);

        // Timing

	specify
		(posedge A => (Y : A)) = (0.0,0.0);
		(negedge A => (Y : A)) = (0.0,0.0);
		(posedge B => (Y : B)) = (0.0,0.0);
		(negedge B => (Y : B)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: nand2b 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_nand2b_1
//   cell_description : 2-input NAND with Inverted Input A_N
//*****************************************************************

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
		(posedge A_N => (Y : A_N)) = (0.0,0.0);
		(negedge A_N => (Y : A_N)) = (0.0,0.0);
		(posedge B => (Y : B)) = (0.0,0.0);
		(negedge B => (Y : B)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: nand2b 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_nand2b_2
//   cell_description : 2-input NAND with Inverted Input A_N
//*****************************************************************

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
		(posedge A_N => (Y : A_N)) = (0.0,0.0);
		(negedge A_N => (Y : A_N)) = (0.0,0.0);
		(posedge B => (Y : B)) = (0.0,0.0);
		(negedge B => (Y : B)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: nand3 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_nand3_1
//   cell_description : 3-input NAND
//*****************************************************************

module sg13g2_nand3_1 (Y, A, B, C);
		
	output Y;
	input A, B, C;

	// Function

	wire int_fwire_0;

	and (int_fwire_0, A, B, C);
	not (Y, int_fwire_0);

        // Timing

	specify
		(posedge A => (Y : A)) = (0.0,0.0);
		(negedge A => (Y : A)) = (0.0,0.0);
		(posedge B => (Y : B)) = (0.0,0.0);
		(negedge B => (Y : B)) = (0.0,0.0);
		(posedge C => (Y : C)) = (0.0,0.0);
		(negedge C => (Y : C)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: nand3b 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_nand3b_1
//   cell_description : 3-input NAND3 with Inverted Input A_N
//*****************************************************************

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
		(posedge A_N => (Y : A_N)) = (0.0,0.0);
		(negedge A_N => (Y : A_N)) = (0.0,0.0);
		(posedge B => (Y : B)) = (0.0,0.0);
		(negedge B => (Y : B)) = (0.0,0.0);
		(posedge C => (Y : C)) = (0.0,0.0);
		(negedge C => (Y : C)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: nand4 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_nand4_1
//   cell_description : 4-input NAND
//*****************************************************************

module sg13g2_nand4_1 (Y, A, B, C, D);
		
	output Y;
	input A, B, C, D;

	// Function

	wire int_fwire_0;

	and (int_fwire_0, A, B, C, D);
	not (Y, int_fwire_0);

        // Timing

	specify
		(posedge A => (Y : A)) = (0.0,0.0);
		(negedge A => (Y : A)) = (0.0,0.0);
		(posedge B => (Y : B)) = (0.0,0.0);
		(negedge B => (Y : B)) = (0.0,0.0);
		(posedge C => (Y : C)) = (0.0,0.0);
		(negedge C => (Y : C)) = (0.0,0.0);
		(posedge D => (Y : D)) = (0.0,0.0);
		(negedge D => (Y : D)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: nor2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_nor2_1
//   cell_description : 2-input NOR
//*****************************************************************

module sg13g2_nor2_1 (Y, A, B);
		
	output Y;
	input A, B;

	// Function

	wire int_fwire_0;

	or (int_fwire_0, A, B);
	not (Y, int_fwire_0);

        // Timing

	specify
		(posedge A => (Y : A)) = (0.0,0.0);
		(negedge A => (Y : A)) = (0.0,0.0);
		(posedge B => (Y : B)) = (0.0,0.0);
		(negedge B => (Y : B)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: nor2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_nor2_2
//   cell_description : 2-input NOR
//*****************************************************************

module sg13g2_nor2_2 (Y, A, B);
		
	output Y;
	input A, B;

	// Function

	wire int_fwire_0;

	or (int_fwire_0, A, B);
	not (Y, int_fwire_0);

        // Timing

	specify
		(posedge A => (Y : A)) = (0.0,0.0);
		(negedge A => (Y : A)) = (0.0,0.0);
		(posedge B => (Y : B)) = (0.0,0.0);
		(negedge B => (Y : B)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: nor2b 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_nor2b_1
//   cell_description : 2-input NOR2 with Inverted Input B_N
//*****************************************************************

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
		(posedge A => (Y : A)) = (0.0,0.0);
		(negedge A => (Y : A)) = (0.0,0.0);
		(posedge B_N => (Y : B_N)) = (0.0,0.0);
		(negedge B_N => (Y : B_N)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: nor2b 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_nor2b_1
//   cell_description : 2-input NOR2 with Inverted Input B_N
//*****************************************************************

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
		(posedge A => (Y : A)) = (0.0,0.0);
		(negedge A => (Y : A)) = (0.0,0.0);
		(posedge B_N => (Y : B_N)) = (0.0,0.0);
		(negedge B_N => (Y : B_N)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: nor3 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_nor3_1
//   cell_description : 3-input NOR
//*****************************************************************

module sg13g2_nor3_1 (Y, A, B, C);
		
	output Y;
	input A, B, C;

	// Function

	wire int_fwire_0;

	or (int_fwire_0, A, B, C);
	not (Y, int_fwire_0);

        // Timing

	specify
		(posedge A => (Y : A)) = (0.0,0.0);
		(negedge A => (Y : A)) = (0.0,0.0);
		(posedge B => (Y : B)) = (0.0,0.0);
		(negedge B => (Y : B)) = (0.0,0.0);
		(posedge C => (Y : C)) = (0.0,0.0);
		(negedge C => (Y : C)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: nor3 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_nor3_2
//   cell_description : 3-input NOR
//*****************************************************************

module sg13g2_nor3_2 (Y, A, B, C);
		
	output Y;
	input A, B, C;

	// Function

	wire int_fwire_0;

	or (int_fwire_0, A, B, C);
	not (Y, int_fwire_0);

        // Timing

	specify
		(posedge A => (Y : A)) = (0.0,0.0);
		(negedge A => (Y : A)) = (0.0,0.0);
		(posedge B => (Y : B)) = (0.0,0.0);
		(negedge B => (Y : B)) = (0.0,0.0);
		(posedge C => (Y : C)) = (0.0,0.0);
		(negedge C => (Y : C)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: nor4 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_nor4_1
//   cell_description : 4-input NOR
//*****************************************************************

module sg13g2_nor4_1 (Y, A, B, C, D);
		
	output Y;
	input A, B, C, D;

	// Function

	wire int_fwire_0;

	or (int_fwire_0, A, B, C, D);
	not (Y, int_fwire_0);

        // Timing

	specify
		(posedge A => (Y : A)) = (0.0,0.0);
		(negedge A => (Y : A)) = (0.0,0.0);
		(posedge B => (Y : B)) = (0.0,0.0);
		(negedge B => (Y : B)) = (0.0,0.0);
		(posedge C => (Y : C)) = (0.0,0.0);
		(negedge C => (Y : C)) = (0.0,0.0);
		(posedge D => (Y : D)) = (0.0,0.0);
		(negedge D => (Y : D)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: nor4 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_nor4_2
//   cell_description : 4-input NOR
//*****************************************************************

module sg13g2_nor4_2 (Y, A, B, C, D);
		
	output Y;
	input A, B, C, D;

	// Function

	wire int_fwire_0;

	or (int_fwire_0, A, B, C, D);
	not (Y, int_fwire_0);

        // Timing

	specify
		(posedge A => (Y : A)) = (0.0,0.0);
		(negedge A => (Y : A)) = (0.0,0.0);
		(posedge B => (Y : B)) = (0.0,0.0);
		(negedge B => (Y : B)) = (0.0,0.0);
		(posedge C => (Y : C)) = (0.0,0.0);
		(negedge C => (Y : C)) = (0.0,0.0);
		(posedge D => (Y : D)) = (0.0,0.0);
		(negedge D => (Y : D)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: o21ai 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_o21ai_1
//   cell_description : 2-input OR into 2-input NAND
//*****************************************************************

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
		(posedge A1 => (Y : A1)) = (0.0,0.0);
		(negedge A1 => (Y : A1)) = (0.0,0.0);
		(posedge A2 => (Y : A2)) = (0.0,0.0);
		(negedge A2 => (Y : A2)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b1))
			(posedge B1 => (Y : B1)) = (0.0,0.0);
		if ((A1 == 1'b0 && A2 == 1'b1))
			(negedge B1 => (Y : B1)) = (0.0,0.0);
		ifnone 
			(posedge B1 => (Y : B1)) = (0.0,0.0);
		ifnone 
			(negedge B1 => (Y : B1)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: or2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_or2_1
//   cell_description : 2-input OR
//*****************************************************************

module sg13g2_or2_1 (X, A, B);
		
	output X;
	input A, B;

	// Function

	or (X, A, B);

        // Timing

	specify
		(posedge A => (X : A)) = (0.0,0.0);
		(negedge A => (X : A)) = (0.0,0.0);
		(posedge B => (X : B)) = (0.0,0.0);
		(negedge B => (X : B)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: or2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_or2_2
//   cell_description : 2-input OR
//*****************************************************************

module sg13g2_or2_2 (X, A, B);
		
	output X;
	input A, B;

	// Function

	or (X, A, B);

        // Timing

	specify
		(posedge A => (X : A)) = (0.0,0.0);
		(negedge A => (X : A)) = (0.0,0.0);
		(posedge B => (X : B)) = (0.0,0.0);
		(negedge B => (X : B)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: or3 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_or3_1
//   cell_description : 3-input OR
//*****************************************************************

module sg13g2_or3_1 (X, A, B, C);
		
	output X;
	input A, B, C;

	// Function

	or (X, A, B, C);

        // Timing

	specify
		(posedge A => (X : A)) = (0.0,0.0);
		(negedge A => (X : A)) = (0.0,0.0);
		(posedge B => (X : B)) = (0.0,0.0);
		(negedge B => (X : B)) = (0.0,0.0);
		(posedge C => (X : C)) = (0.0,0.0);
		(negedge C => (X : C)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: or3 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_or3_2
//   cell_description : 3-input OR
//*****************************************************************

module sg13g2_or3_2 (X, A, B, C);
		
	output X;
	input A, B, C;

	// Function

	or (X, A, B, C);

        // Timing

	specify
		(posedge A => (X : A)) = (0.0,0.0);
		(negedge A => (X : A)) = (0.0,0.0);
		(posedge B => (X : B)) = (0.0,0.0);
		(negedge B => (X : B)) = (0.0,0.0);
		(posedge C => (X : C)) = (0.0,0.0);
		(negedge C => (X : C)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: or4 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_or4_1
//   cell_description : 4-input OR
//*****************************************************************

module sg13g2_or4_1 (X, A, B, C, D);
		
	output X;
	input A, B, C, D;

	// Function

	or (X, A, B, C, D);

        // Timing

	specify
		(posedge A => (X : A)) = (0.0,0.0);
		(negedge A => (X : A)) = (0.0,0.0);
		(posedge B => (X : B)) = (0.0,0.0);
		(negedge B => (X : B)) = (0.0,0.0);
		(posedge C => (X : C)) = (0.0,0.0);
		(negedge C => (X : C)) = (0.0,0.0);
		(posedge D => (X : D)) = (0.0,0.0);
		(negedge D => (X : D)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: or4 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_or4_2
//   cell_description : 4-input OR
//*****************************************************************

module sg13g2_or4_2 (X, A, B, C, D);
		
	output X;
	input A, B, C, D;

	// Function

	or (X, A, B, C, D);

        // Timing

	specify
		(posedge A => (X : A)) = (0.0,0.0);
		(negedge A => (X : A)) = (0.0,0.0);
		(posedge B => (X : B)) = (0.0,0.0);
		(negedge B => (X : B)) = (0.0,0.0);
		(posedge C => (X : C)) = (0.0,0.0);
		(negedge C => (X : C)) = (0.0,0.0);
		(posedge D => (X : D)) = (0.0,0.0);
		(negedge D => (X : D)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: sdfbbp 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_sdfbbp_1
//   cell_description : Posedge Two-Outputs D-Flip-Flop with Reset, Set and Scan
//*****************************************************************

module sg13g2_sdfbbp_1 (Q, Q_N, CLK, D, RESET_B, SCD, SCE, SET_B);
		
	output Q, Q_N;
	input CLK, D, RESET_B, SCD, SCE, SET_B;
	reg notifier;
	wire delayed_D, delayed_SCD, delayed_SCE, delayed_RESET_B, delayed_SET_B, delayed_CLK;

	// Function
	wire int_fwire_d, int_fwire_IQ, int_fwire_IQN;
	wire int_fwire_r, int_fwire_s, xcr_0;

	ihp_mux2 (int_fwire_d, delayed_D, delayed_SCD, delayed_SCE);
	not (int_fwire_s, delayed_SET_B);
	not (int_fwire_r, delayed_RESET_B);
	buf (xcr_0, 0);
	ihp_dff_sr_1 (int_fwire_IQ, notifier, delayed_CLK, int_fwire_d, int_fwire_s, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (Q_N, int_fwire_IQN);

        // Timing

	specify
		(negedge RESET_B => (Q :1'b0)) = (0.0,0.0);
		(negedge SET_B => (Q :1'b1)) = (0.0,0.0);
		if (SCE == 1'b1)
			(posedge CLK => (Q : D)) = (0.0,0.0);
		if (SCE == 1'b1)
			(posedge CLK => (Q : D)) = (0.0,0.0);
		ifnone 
			(posedge CLK => (Q : D)) = (0.0,0.0);
		ifnone 
			(negedge CLK => (Q : D)) = (0.0,0.0);
		(negedge RESET_B => (Q_N :1'b0)) = (0.0,0.0);
		(negedge SET_B => (Q_N :1'b1)) = (0.0,0.0);
		if (SCE == 1'b1)
			(posedge CLK => (Q_N : D)) = (0.0,0.0);
		if (SCE == 1'b1)
			(posedge CLK => (Q_N : D)) = (0.0,0.0);
		ifnone 
			(posedge CLK => (Q_N : D)) = (0.0,0.0);
		ifnone 
			(negedge CLK => (Q_N : D)) = (0.0,0.0);
		$setuphold (posedge CLK, posedge D, 0.0, 0.0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, negedge D, 0.0, 0.0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, posedge SCD, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCD);
		$setuphold (posedge CLK, negedge SCD, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCD);
		$setuphold (posedge CLK, posedge SCE, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCE);
		$setuphold (posedge CLK, negedge SCE, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCE);
		$recrem (posedge RESET_B, posedge CLK, 0.0, 0.0, notifier,,, delayed_RESET_B, delayed_CLK);
		$recrem (posedge SET_B, posedge CLK, 0.0, 0.0, notifier,,, delayed_SET_B, delayed_CLK);
		$setuphold (posedge RESET_B, posedge SET_B, 0.0, 0.0, notifier,,, delayed_RESET_B, delayed_SET_B);
		$width (negedge RESET_B, 0.0, 0, notifier);
		$width (negedge SET_B, 0.0, 0, notifier);
		$width (posedge CLK, 0.0, 0, notifier);
		$width (negedge CLK, 0.0, 0, notifier);
	endspecify

endmodule
`endcelldefine


// type: sdfrbp 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_sdfrbp_1
//   cell_description : Posedge Two-Outputs Q and Q_N D-Flip-Flop with Reset and Scan
//*****************************************************************

module sg13g2_sdfrbp_1 (Q, Q_N, CLK, D, RESET_B, SCD, SCE);
		
	output Q, Q_N;
	input CLK, D, RESET_B, SCD, SCE;
	reg notifier;
	wire delayed_D, delayed_SCD, delayed_SCE, delayed_RESET_B, delayed_CLK;

	// Function
	wire int_fwire_d, int_fwire_IQ, int_fwire_IQN;
	wire int_fwire_r, xcr_0;

	ihp_mux2 (int_fwire_d, delayed_D, delayed_SCD, delayed_SCE);
	not (int_fwire_r, delayed_RESET_B);
	buf (xcr_0, 0);
	ihp_dff_r (int_fwire_IQ, notifier, delayed_CLK, int_fwire_d, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (Q_N, int_fwire_IQN);

        // Timing

	specify
		(negedge RESET_B => (Q :1'b0)) = (0.0,0.0);
		if (SCE == 1'b1)
			(posedge CLK => (Q : D)) = (0.0,0.0);
		if (SCE == 1'b1)
			(posedge CLK => (Q : D)) = (0.0,0.0);
		ifnone 
			(posedge CLK => (Q : D)) = (0.0,0.0);
		ifnone 
			(negedge CLK => (Q : D)) = (0.0,0.0);
		(negedge RESET_B => (Q_N :1'b0)) = (0.0,0.0);
		if (SCE == 1'b1)
			(posedge CLK => (Q_N : D)) = (0.0,0.0);
		if (SCE == 1'b1)
			(posedge CLK => (Q_N : D)) = (0.0,0.0);
		ifnone 
			(posedge CLK => (Q_N : D)) = (0.0,0.0);
		ifnone 
			(negedge CLK => (Q_N : D)) = (0.0,0.0);
		$setuphold (posedge CLK, posedge D, 0.0, 0.0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, negedge D, 0.0, 0.0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, posedge SCD, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCD);
		$setuphold (posedge CLK, negedge SCD, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCD);
		$setuphold (posedge CLK, posedge SCE, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCE);
		$setuphold (posedge CLK, negedge SCE, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCE);
		$recrem (posedge RESET_B, posedge CLK, 0.0, 0.0, notifier,,, delayed_RESET_B, delayed_CLK);
		$width (negedge RESET_B, 0.0, 0, notifier);
		$width (posedge CLK, 0.0, 0, notifier);
	endspecify

endmodule
`endcelldefine


// type: sdfrbp 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_sdfrbp_2
//   cell_description : Posedge Two-Outputs Q and Q_N D-Flip-Flop with Reset and Scan
//*****************************************************************

module sg13g2_sdfrbp_2 (Q, Q_N, CLK, D, RESET_B, SCD, SCE);
		
	output Q, Q_N;
	input CLK, D, RESET_B, SCD, SCE;
	reg notifier;
	wire delayed_D, delayed_SCD, delayed_SCE, delayed_RESET_B, delayed_CLK;

	// Function
	wire int_fwire_d, int_fwire_IQ, int_fwire_IQN;
	wire int_fwire_r, xcr_0;

	ihp_mux2 (int_fwire_d, delayed_D, delayed_SCD, delayed_SCE);
	not (int_fwire_r, delayed_RESET_B);
	buf (xcr_0, 0);
	ihp_dff_r (int_fwire_IQ, notifier, delayed_CLK, int_fwire_d, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);
	not (int_fwire_IQN, int_fwire_IQ);
	buf (Q_N, int_fwire_IQN);

        // Timing

	specify
		(negedge RESET_B => (Q :1'b0)) = (0.0,0.0);
		if (SCE == 1'b1)
			(posedge CLK => (Q : D)) = (0.0,0.0);
		if (SCE == 1'b1)
			(posedge CLK => (Q : D)) = (0.0,0.0);
		ifnone 
			(posedge CLK => (Q : D)) = (0.0,0.0);
		ifnone 
			(negedge CLK => (Q : D)) = (0.0,0.0);
		(negedge RESET_B => (Q_N :1'b0)) = (0.0,0.0);
		if (SCE == 1'b1)
			(posedge CLK => (Q_N : D)) = (0.0,0.0);
		if (SCE == 1'b1)
			(posedge CLK => (Q_N : D)) = (0.0,0.0);
		ifnone 
			(posedge CLK => (Q_N : D)) = (0.0,0.0);
		ifnone 
			(negedge CLK => (Q_N : D)) = (0.0,0.0);
		$setuphold (posedge CLK, posedge D, 0.0, 0.0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, negedge D, 0.0, 0.0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, posedge SCD, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCD);
		$setuphold (posedge CLK, negedge SCD, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCD);
		$setuphold (posedge CLK, posedge SCE, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCE);
		$setuphold (posedge CLK, negedge SCE, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCE);
		$recrem (posedge RESET_B, posedge CLK, 0.0, 0.0, notifier,,, delayed_RESET_B, delayed_CLK);
		$width (negedge RESET_B, 0.0, 0, notifier);
		$width (posedge CLK, 0.0, 0, notifier);
	endspecify

endmodule
`endcelldefine


// type: sdfrbpq 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_sdfrbpq_1
//   cell_description : Posedge Single-Output Q D-Flip-Flop with Reset and Scan
//*****************************************************************

module sg13g2_sdfrbpq_1 (Q, CLK, D, RESET_B, SCD, SCE);
		
	output Q;
	input CLK, D, RESET_B, SCD, SCE;
	reg notifier;
	wire delayed_D, delayed_SCD, delayed_SCE, delayed_RESET_B, delayed_CLK;

	// Function
	wire int_fwire_d, int_fwire_IQ, int_fwire_r;
	wire xcr_0;

	ihp_mux2 (int_fwire_d, delayed_D, delayed_SCD, delayed_SCE);
	not (int_fwire_r, delayed_RESET_B);
	buf (xcr_0, 0);
	ihp_dff_r (int_fwire_IQ, notifier, delayed_CLK, int_fwire_d, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);

        // Timing

	specify
		(negedge RESET_B => (Q :1'b0)) = (0.0,0.0);
		if (SCE == 1'b1)
			(posedge CLK => (Q : D)) = (0.0,0.0);
		if (SCE == 1'b1)
			(posedge CLK => (Q : D)) = (0.0,0.0);
		if (SCE == 1'b0)
			(posedge CLK => (Q : D)) = (0.0,0.0);
		if (SCE == 1'b0)
			(posedge CLK => (Q : D)) = (0.0,0.0);
		ifnone 
			(posedge CLK => (Q : D)) = (0.0,0.0);
		ifnone 
			(negedge CLK => (Q : D)) = (0.0,0.0);
		$setuphold (posedge CLK, posedge D, 0.0, 0.0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, negedge D, 0.0, 0.0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, posedge SCD, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCD);
		$setuphold (posedge CLK, negedge SCD, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCD);
		$setuphold (posedge CLK, posedge SCE, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCE);
		$setuphold (posedge CLK, negedge SCE, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCE);
		$recrem (posedge RESET_B, posedge CLK, 0.0, 0.0, notifier,,, delayed_RESET_B, delayed_CLK);
		$width (negedge RESET_B, 0.0, 0, notifier);
		$width (posedge CLK, 0.0, 0, notifier);
		$width (negedge CLK, 0.0, 0, notifier);
	endspecify

endmodule
`endcelldefine


// type: sdfrbpq 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_sdfrbpq_2
//   cell_description : Posedge Single-Output Q D-Flip-Flop with Reset and Scan
//*****************************************************************

module sg13g2_sdfrbpq_2 (Q, CLK, D, RESET_B, SCD, SCE);
		
	output Q;
	input CLK, D, RESET_B, SCD, SCE;
	reg notifier;
	wire delayed_D, delayed_SCD, delayed_SCE, delayed_RESET_B, delayed_CLK;

	// Function
	wire int_fwire_d, int_fwire_IQ, int_fwire_r;
	wire xcr_0;

	ihp_mux2 (int_fwire_d, delayed_D, delayed_SCD, delayed_SCE);
	not (int_fwire_r, delayed_RESET_B);
	buf (xcr_0, 0);
	ihp_dff_r (int_fwire_IQ, notifier, delayed_CLK, int_fwire_d, int_fwire_r, xcr_0);
	buf (Q, int_fwire_IQ);

        // Timing

	specify
		(negedge RESET_B => (Q :1'b0)) = (0.0,0.0);
		if (SCE == 1'b1)
			(posedge CLK => (Q : D)) = (0.0,0.0);
		if (SCE == 1'b1)
			(posedge CLK => (Q : D)) = (0.0,0.0);
		if (SCE == 1'b0)
			(posedge CLK => (Q : D)) = (0.0,0.0);
		if (SCE == 1'b0)
			(posedge CLK => (Q : D)) = (0.0,0.0);
		ifnone 
			(posedge CLK => (Q : D)) = (0.0,0.0);
		ifnone 
			(negedge CLK => (Q : D)) = (0.0,0.0);
		$setuphold (posedge CLK, posedge D, 0.0, 0.0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, negedge D, 0.0, 0.0, notifier,,, delayed_CLK, delayed_D);
		$setuphold (posedge CLK, posedge SCD, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCD);
		$setuphold (posedge CLK, negedge SCD, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCD);
		$setuphold (posedge CLK, posedge SCE, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCE);
		$setuphold (posedge CLK, negedge SCE, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCE);
		$recrem (posedge RESET_B, posedge CLK, 0.0, 0.0, notifier,,, delayed_RESET_B, delayed_CLK);
		$width (negedge RESET_B, 0.0, 0, notifier);
		$width (posedge CLK, 0.0, 0, notifier);
		$width (negedge CLK, 0.0, 0, notifier);
	endspecify

endmodule
`endcelldefine


// type: slgcp 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_slgcp_1
//   cell_description : Scan gated clock
//*****************************************************************

module sg13g2_slgcp_1 (GCLK, GATE, CLK, SCE);
		
	output GCLK;
	input GATE, CLK, SCE;
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
		(posedge CLK => (GCLK :CLK)) = (0.0,0.0);
		(negedge CLK => (GCLK :CLK)) = (0.0,0.0);
		$setuphold (posedge CLK, posedge GATE, 0.0, 0.0, notifier,,, delayed_CLK, delayed_GATE);
		$setuphold (posedge CLK, negedge GATE, 0.0, 0.0, notifier,,, delayed_CLK, delayed_GATE);
		$setuphold (posedge CLK, posedge SCE, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCE);
		$setuphold (posedge CLK, negedge SCE, 0.0, 0.0, notifier,,, delayed_CLK, delayed_SCE);
		$width (posedge CLK, 0.0, 0, notifier);
		$width (negedge CLK, 0.0, 0, notifier);
	endspecify

endmodule
`endcelldefine

//type: sighold
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_sighold
//   cell_description : Leakage current compensator (bus holder)
//*****************************************************************

module sg13g2_sighold (SH);

   inout SH;

// logic section  
  `ifdef DISPLAY_HOLD 
  
        buf (n1, SH);
        buf (pull1, pull0) (SH, n1);

     initial
     begin
      #0 $display("  > Warning: compiler directive DISPLAY_HOLD is set in cell"
                               );
         $display("  > %m");
         $display("  > sg13g2_sighold cell model is switched to provide logic levels"
                  );
         $display("  >  - danger of reading not really driven values ");   
                   
         $display("  >  - undriven bus states are not detectable now ");   
                   
         $display("  >");    
     end

  `else
// - no logic behaviour modelled for the electrical function of 
//   sg13g2_sighold cell 
// - sg13g2_sighold cell compensates leackage current only in case of
//   undriven node/bus and system stop
// - sg13g2_sighold cell holds the bus bit on "0" or "1", but does not 
//   drive it, this is not in every case the same as the last valid 
//   logic value considering the desired application meaning
// - undriven bus bit should not be used as sequential element
// - reading from undriven bus_bit ("Z") has to provide ("X") in the
//   related block to detect such cases in simulation
//
// Use the compiler directive command
//   `define  DISPLAY_HOLD yes
// to enable the logic pullup/down behaviour of the Leakage current 
// compensator cell sg13g2_sighold*
//
     buf (n1, SH);
     bufif1 (SH, n1, 1'b0); /* always inactive */
  `endif
 
// no timing modelled for sg13g2_sighold cell
// no backannotation possible for sg13g2_sighold cell 
    
	
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
//   technology       : SG13G2
//   module name      : sg13g2_tiehi
//   cell_description : Constant logic 0
//*****************************************************************

module sg13g2_tiehi (L_HI);
		
	output L_HI;

	// Function

	buf (L_HI, 1'b1);

        // Timing

	specify
	endspecify

endmodule
`endcelldefine


// type: tielo 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_tielo
//   cell_description : Constant logic 1
//*****************************************************************

module sg13g2_tielo (L_LO);
		
	output L_LO;

	// Function

	buf (L_LO, 1'b0);

        // Timing

	specify
	endspecify

endmodule
`endcelldefine


// type: xnor2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_xnor2_1
//   cell_description : 2-input XNOR
//*****************************************************************

module sg13g2_xnor2_1 (Y, A, B);
		
	output Y;
	input A, B;

	// Function

	wire int_fwire_0;

	xor (int_fwire_0, A, B);
	not (Y, int_fwire_0);
        
        // Timing

	specify
		if ((B == 1'b1))
			(posedge A => (Y : A)) = (0.0,0.0);
		if ((B == 1'b1))
			(negedge A => (Y : A)) = (0.0,0.0);
		ifnone 
			(negedge A => (Y:A)) = (0.0,0.0);
		ifnone 
			(posedge A => (Y:A)) = (0.0,0.0);
		if ((B == 1'b0))
			(posedge A => (Y : A)) = (0.0,0.0);
		if ((B == 1'b0))
			(negedge A => (Y : A)) = (0.0,0.0);
		if ((A == 1'b1))
			(posedge B => (Y : B)) = (0.0,0.0);
		if ((A == 1'b1))
			(negedge B => (Y : B)) = (0.0,0.0);
		ifnone 
			(negedge B => (Y:B)) = (0.0,0.0);
		ifnone 
			(posedge B => (Y:B)) = (0.0,0.0);
		if ((A == 1'b0))
			(posedge B => (Y : B)) = (0.0,0.0);
		if ((A == 1'b0))
			(negedge B => (Y : B)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine


// type: xor2 
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_xor2_1
//   cell_description : 2-input XOR
//*****************************************************************

module sg13g2_xor2_1 (X, A, B);
		
	output X;
	input A, B;

	// Function

	xor (X, A, B);

        // Timing

	specify
		if ((B == 1'b0))
			(posedge A => (X : A)) = (0.0,0.0);
		if ((B == 1'b0))
			(negedge A => (X : A)) = (0.0,0.0);
		ifnone 
			(negedge A => (X:A)) = (0.0,0.0);
		ifnone 
			(posedge A => (X:A)) = (0.0,0.0);
		if ((B == 1'b1))
			(posedge A => (X : A)) = (0.0,0.0);
		if ((B == 1'b1))
			(negedge A => (X : A)) = (0.0,0.0);
		if ((A == 1'b0))
			(posedge B => (X : B)) = (0.0,0.0);
		if ((A == 1'b0))
			(negedge B => (X : B)) = (0.0,0.0);
		ifnone 
			(negedge B => (X:B)) = (0.0,0.0);
		ifnone 
			(posedge B => (X:B)) = (0.0,0.0);
		if ((A == 1'b1))
			(posedge B => (X : B)) = (0.0,0.0);
		if ((A == 1'b1))
			(negedge B => (X : B)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine
