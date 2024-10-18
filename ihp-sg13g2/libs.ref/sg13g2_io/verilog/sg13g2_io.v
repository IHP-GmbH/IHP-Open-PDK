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

// type: Corner
`timescale 1ns/10ps
`celldefine
module sg13g2_Corner ();
endmodule
`endcelldefine

// type: Filler200
`timescale 1ns/10ps
`celldefine
module sg13g2_Filler200 ();
endmodule
`endcelldefine

// type: Filler400
`timescale 1ns/10ps
`celldefine
module sg13g2_Filler400 ();
endmodule
`endcelldefine

// type: Filler1000
`timescale 1ns/10ps
`celldefine
module sg13g2_Filler1000 ();
endmodule
`endcelldefine

// type: Filler2000
`timescale 1ns/10ps
`celldefine
module sg13g2_Filler2000 ();
endmodule
`endcelldefine

// type: Filler4000
`timescale 1ns/10ps
`celldefine
module sg13g2_Filler4000 ();
endmodule
`endcelldefine

// type: Filler10000
`timescale 1ns/10ps
`celldefine
module sg13g2_Filler10000 ();
endmodule
`endcelldefine
// type: Input
`timescale 1ns/10ps
`celldefine
module sg13g2_IOPadIn (pad, p2c);
	inout pad;
	output p2c;

	// Function
	assign p2c = pad;

	// Timing
	specify
		(pad => p2c) = 0;
	endspecify
endmodule
`endcelldefine

// type: Output4mA
`timescale 1ns/10ps
`celldefine
module sg13g2_IOPadOut4mA (pad, c2p);
	inout pad;
	input c2p;

	// Function
	assign pad = c2p;

	// Timing
	specify
		(c2p => pad) = 0;
	endspecify
endmodule
`endcelldefine

// type: Output16mA
`timescale 1ns/10ps
`celldefine
module sg13g2_IOPadOut16mA (pad, c2p);
	inout pad;
	input c2p;

	// Function
	assign pad = c2p;

	// Timing
	specify
		(c2p => pad) = 0;
	endspecify
endmodule
`endcelldefine

// type: Output30mA
`timescale 1ns/10ps
`celldefine
module sg13g2_IOPadOut30mA (pad, c2p);
	inout pad;
	input c2p;

	// Function
	assign pad = c2p;

	// Timing
	specify
		(c2p => pad) = 0;
	endspecify
endmodule
`endcelldefine

// type: TriStateOutput4mA
`timescale 1ns/10ps
`celldefine
module sg13g2_IOPadTriOut4mA (pad, c2p, c2p_en);
	inout pad;
	input c2p;
	input c2p_en;

	// Function
	assign pad = (c2p_en) ? c2p : 1'bz;

	// Timing
	specify
		if (c2p_en == 1'b1)
			(c2p => pad) = 0;
	endspecify
endmodule
`endcelldefine

// type: TriStateOutput16mA
`timescale 1ns/10ps
`celldefine
module sg13g2_IOPadTriOut16mA (pad, c2p, c2p_en);
	inout pad;
	input c2p;
	input c2p_en;

	// Function
	assign pad = (c2p_en) ? c2p : 1'bz;

	// Timing
	specify
		if (c2p_en == 1'b1)
			(c2p => pad) = 0;
	endspecify
endmodule
`endcelldefine

// type: TriStateOutput30mA
`timescale 1ns/10ps
`celldefine
module sg13g2_IOPadTriOut30mA (pad, c2p, c2p_en);
	inout pad;
	input c2p;
	input c2p_en;

	// Function
	assign pad = (c2p_en) ? c2p : 1'bz;

	// Timing
	specify
		if (c2p_en == 1'b1)
			(c2p => pad) = 0;
	endspecify
endmodule
`endcelldefine

// type: InputOutput4mA
`timescale 1ns/10ps
`celldefine
module sg13g2_IOPadInOut4mA (pad, c2p, c2p_en, p2c);
	inout pad;
	input c2p;
	input c2p_en;
	output p2c;

	// Function
	assign pad = (c2p_en) ? c2p : 1'bz;
	assign p2c = pad;

	// Timing
	specify
		if (c2p_en == 1'b1)
			(c2p => pad) = 0;
		(pad => p2c) = 0;
	endspecify
endmodule
`endcelldefine

// type: InputOutput4mA
`timescale 1ns/10ps
`celldefine
module sg13g2_IOPadInOut16mA (pad, c2p, c2p_en, p2c);
	inout pad;
	input c2p;
	input c2p_en;
	output p2c;

	// Function
	assign pad = (c2p_en) ? c2p : 1'bz;
	assign p2c = pad;

	// Timing
	specify
		if (c2p_en == 1'b1)
			(c2p => pad) = 0;
		(pad => p2c) = 0;
	endspecify
endmodule
`endcelldefine

// type: InputOutput4mA
`timescale 1ns/10ps
`celldefine
module sg13g2_IOPadInOut30mA (pad, c2p, c2p_en, p2c);
	inout pad;
	input c2p;
	input c2p_en;
	output p2c;

	// Function
	assign pad = (c2p_en) ? c2p : 1'bz;
	assign p2c = pad;

	// Timing
	specify
		if (c2p_en == 1'b1)
			(c2p => pad) = 0;
		(pad => p2c) = 0;
	endspecify
endmodule
`endcelldefine

// type: Analog
`timescale 1ns/10ps
`celldefine
module sg13g2_IOPadAnalog (pad, padres);
	inout pad;
	inout padres;

	// Function
	assign pad = padres;
	assign padres = pad;

	// Timing
	specify
		(pad => padres) = 0;
		(padres => pad) = 0;
	endspecify
endmodule
`endcelldefine

// type: IOVss
`timescale 1ns/10ps
`celldefine
module sg13g2_IOPadIOVss ();
endmodule
`endcelldefine

// type: IOVdd
`timescale 1ns/10ps
`celldefine
module sg13g2_IOPadIOVdd ();
endmodule
`endcelldefine

// type: Vss
`timescale 1ns/10ps
`celldefine
module sg13g2_IOPadVss ();
endmodule
`endcelldefine

// type: Vdd
`timescale 1ns/10ps
`celldefine
module sg13g2_IOPadVdd ();
endmodule
`endcelldefine
