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
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_Corner
//   cell_description : Physical I/O filler - corner.
//*****************************************************************
module sg13g2_Corner (vdd, vss, iovdd, iovss);
	inout vdd;
	inout vss;	
	inout iovdd;
	inout iovss;

	specify
	endspecify

endmodule
`endcelldefine

// type: Filler200
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_Filler200
//   cell_description : Physical I/O filler width 1 um.
//*****************************************************************
module sg13g2_Filler200 (vdd, vss, iovdd, iovss);
	inout vdd;
	inout vss;	
	inout iovdd;
	inout iovss;

	specify
	endspecify

endmodule
`endcelldefine

// type: Filler400
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_Filler400
//   cell_description : Physical I/O filler width 2 um.
//*****************************************************************
module sg13g2_Filler400 (vdd, vss, iovdd, iovss);
	inout vdd;
	inout vss;	
	inout iovdd;
	inout iovss;

	specify
	endspecify

endmodule
`endcelldefine

// type: Filler1000
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_Filler1000
//   cell_description : Physical I/O filler width 5 um.
//*****************************************************************
module sg13g2_Filler1000 (vdd, vss, iovdd, iovss);
	inout vdd;
	inout vss;	
	inout iovdd;
	inout iovss;

	specify
	endspecify

endmodule
`endcelldefine

// type: Filler2000
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_Filler2000
//   cell_description : Physical I/O filler width 10 um.
//*****************************************************************
module sg13g2_Filler2000 (vdd, vss, iovdd, iovss);
	inout vdd;
	inout vss;
	inout iovdd;
	inout iovss;

	specify
	endspecify

endmodule
`endcelldefine

// type: Filler4000
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_Filler4000
//   cell_description : Physical I/O filler width 20 um.
//*****************************************************************
module sg13g2_Filler4000 (vdd, vss, iovdd, iovss);
	inout vdd;
	inout vss;
	inout iovdd;
	inout iovss;

	specify
	endspecify

endmodule
`endcelldefine

// type: Filler10000
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_Filler10000
//   cell_description : Physical I/O filler width 50 um.
//*****************************************************************
module sg13g2_Filler10000 (vdd, vss, iovdd, iovss);
	inout vdd;
	inout vss;
	inout iovdd;
	inout iovss;

	specify
	endspecify

endmodule
`endcelldefine

// type: Input
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_IOPadIn
//   cell_description : 3.3V CMOS input GPIO buffer.
//*****************************************************************
module sg13g2_IOPadIn (pad, p2c, vdd, vss, iovdd, iovss);
	input pad;
	output p2c;
	inout vdd;
	inout vss;
	inout iovdd;
	inout iovss;
	
	// Function
	assign p2c = pad;

	// Timing

	specify
		(posedge pad => (p2c : pad)) = (0.0,0.0);
		(negedge pad => (p2c : pad)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: Output4mA
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_IOPadOut4mA
//   cell_description : 3.3V CMOS 4 mA output GPIO buffer.
//*****************************************************************
module sg13g2_IOPadOut4mA (pad, c2p, vdd, vss, iovdd, iovss);
	output pad;
	input c2p;
	inout vdd;
	inout vss;
	inout iovdd;
	inout iovss;

	// Function
	assign pad = c2p;

	// Timing

	specify
		(posedge c2p => (pad : c2p)) = (0.0,0.0);
		(negedge c2p => (pad : c2p)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: Output16mA
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_IOPadOut16mA
//   cell_description : 3.3V CMOS 16 mA output GPIO buffer.
//*****************************************************************
module sg13g2_IOPadOut16mA (pad, c2p, vdd, vss, iovdd, iovss);
	output pad;
	input c2p;
	inout vdd;
	inout vss;
	inout iovdd;
	inout iovss;

	// Function
	assign pad = c2p;

	// Timing

	specify
		(posedge c2p => (pad : c2p)) = (0.0,0.0);
		(negedge c2p => (pad : c2p)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: Output30mA
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_IOPadOut30mA
//   cell_description : 3.3V CMOS 30 mA output GPIO buffer.
//*****************************************************************
module sg13g2_IOPadOut30mA (pad, c2p, vdd, vss, iovdd, iovss);
	output pad;
	input c2p;
	inout vdd;
	inout vss;
	inout iovdd;
	inout iovss;

	// Function
	assign pad = c2p;

	// Timing

	specify
		(posedge c2p => (pad : c2p)) = (0.0,0.0);
		(negedge c2p => (pad : c2p)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: TriStateOutput4mA
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_IOPadTriOut4mA
//   cell_description : 3.3V CMOS 4 mA output GPIO buffer with tri-state option.
//*****************************************************************
module sg13g2_IOPadTriOut4mA (pad, c2p, c2p_en, vdd, vss, iovdd, iovss);
	output pad;
	input c2p;
	input c2p_en;
	inout vdd;
	inout vss;
	inout iovdd;
	inout iovss;

	// Function
	assign pad = (c2p_en) ? c2p : 1'bz;

	// Timing

	specify
		(posedge c2p => (pad : c2p)) = (0.0,0.0);
		(negedge c2p => (pad : c2p)) = (0.0,0.0);
		(negedge c2p_en => (pad:c2p_en)) = (0.0,0.0);
		(posedge c2p_en => (pad:c2p_en)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: TriStateOutput16mA
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_IOPadTriOut16mA
//   cell_description : 3.3V CMOS 16 mA output GPIO buffer with tri-state option.
//*****************************************************************
module sg13g2_IOPadTriOut16mA (pad, c2p, c2p_en, vdd, vss, iovdd, iovss);
	output pad;
	input c2p;
	input c2p_en;
	inout vdd;
	inout vss;
	inout iovdd;
	inout iovss;

	// Function
	assign pad = (c2p_en) ? c2p : 1'bz;

	// Timing

	specify
		(posedge c2p => (pad : c2p)) = (0.0,0.0);
		(negedge c2p => (pad : c2p)) = (0.0,0.0);
		(negedge c2p_en => (pad:c2p_en)) = (0.0,0.0);
		(posedge c2p_en => (pad:c2p_en)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: TriStateOutput30mA
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_IOPadTriOut30mA
//   cell_description : 3.3V CMOS 30 mA output GPIO buffer with tri-state option.
//*****************************************************************
module sg13g2_IOPadTriOut30mA (pad, c2p, c2p_en, vdd, vss, iovdd, iovss);
	output pad;
	input c2p;
	input c2p_en;
	inout vdd;
	inout vss;
	inout iovdd;
	inout iovss;

	// Function
	assign pad = (c2p_en) ? c2p : 1'bz;

	// Timing

	specify
		(posedge c2p => (pad : c2p)) = (0.0,0.0);
		(negedge c2p => (pad : c2p)) = (0.0,0.0);
		(negedge c2p_en => (pad:c2p_en)) = (0.0,0.0);
		(posedge c2p_en => (pad:c2p_en)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: InputOutput4mA
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_IOPadInOut4mA
//   cell_description : 3.3V CMOS 4 mA bidirectional GPIO buffer with tri-state option.
//*****************************************************************
module sg13g2_IOPadInOut4mA (pad, c2p, p2c, c2p_en, vdd, vss, iovdd, iovss);
	inout pad;
	input c2p;
	output p2c;
	input c2p_en;
	inout vdd;
	inout vss;
	inout iovdd;
	inout iovss;

	// Function
	assign pad = (c2p_en) ? c2p : 1'bz;
	assign p2c = pad;

	// Timing

	specify
		(posedge pad => (p2c : pad)) = (0.0,0.0);
		(negedge pad => (p2c : pad)) = (0.0,0.0);
		(posedge c2p => (pad : c2p)) = (0.0,0.0);
		(negedge c2p => (pad : c2p)) = (0.0,0.0);
		(negedge c2p_en => (pad:c2p_en)) = (0.0,0.0);
		(posedge c2p_en => (pad:c2p_en)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: InputOutput4mA
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_IOPadInOut16mA
//   cell_description : 3.3V CMOS 16 mA bidirectional GPIO buffer with tri-state option.
//*****************************************************************
module sg13g2_IOPadInOut16mA (pad, c2p, p2c, c2p_en, vdd, vss, iovdd, iovss);
	inout pad;
	input c2p;
	output p2c;
	input c2p_en;
	inout vdd;
	inout vss;
	inout iovdd;
	inout iovss;

	// Function
	assign pad = (c2p_en) ? c2p : 1'bz;
	assign p2c = pad;

	// Timing

	specify
		(posedge pad => (p2c : pad)) = (0.0,0.0);
		(negedge pad => (p2c : pad)) = (0.0,0.0);
		(posedge c2p => (pad : c2p)) = (0.0,0.0);
		(negedge c2p => (pad : c2p)) = (0.0,0.0);
		(negedge c2p_en => (pad:c2p_en)) = (0.0,0.0);
		(posedge c2p_en => (pad:c2p_en)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: InputOutput4mA
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_IOPadInOut30mA
//   cell_description : 3.3V CMOS 30 mA bidirectional GPIO buffer with tri-state option.
//*****************************************************************
module sg13g2_IOPadInOut30mA (pad, c2p, p2c, c2p_en, vdd, vss, iovdd, iovss);
	inout pad;
	input c2p;
	output p2c;
	input c2p_en;
	inout vdd;
	inout vss;
	inout iovdd;
	inout iovss;

	// Function
	assign pad = (c2p_en) ? c2p : 1'bz;
	assign p2c = pad;

	// Timing

	specify
		(posedge pad => (p2c : pad)) = (0.0,0.0);
		(negedge pad => (p2c : pad)) = (0.0,0.0);
		(posedge c2p => (pad : c2p)) = (0.0,0.0);
		(negedge c2p => (pad : c2p)) = (0.0,0.0);
		(negedge c2p_en => (pad:c2p_en)) = (0.0,0.0);
		(posedge c2p_en => (pad:c2p_en)) = (0.0,0.0);
	endspecify

endmodule
`endcelldefine

// type: Analog
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_IOPadAnalog
//   cell_description : 0 - 3.3V 27 mA analog pad (600 uA "padres" low-power input-to-gate analog bus).
//*****************************************************************
module sg13g2_IOPadAnalog (pad, padres, vdd, vss, iovdd, iovss);
	inout pad;
	inout padres;
	inout vdd;
	inout vss;	
	inout iovdd;
	inout iovss;
	
	// Function
	assign pad = padres;
	assign padres = pad;

	// Timing

	specify
	endspecify

endmodule
`endcelldefine

// type: IOVss
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_IOPadIOVss
//   cell_description : External IO ground pad.
//*****************************************************************
module sg13g2_IOPadIOVss (vdd, vss, iovdd, iovss);
	inout vdd;
	inout vss;
	inout iovdd;
	inout iovss;

	specify
	endspecify

endmodule
`endcelldefine

// type: IOVdd
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_IOPadIOVdd
//   cell_description : External IO 3.3V supply pad.
//*****************************************************************
module sg13g2_IOPadIOVdd (vdd, vss, iovdd, iovss);
	inout vdd;
	inout vss;
	inout iovdd;
	inout iovss;

	specify
	endspecify

endmodule
`endcelldefine

// type: Vss
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_IOPadVss
//   cell_description : Core ground pad.
//*****************************************************************
module sg13g2_IOPadVss (vdd, vss, iovdd, iovss);
	inout vdd;
	inout vss;
	inout iovdd;
	inout iovss;

	specify
	endspecify

endmodule
`endcelldefine

// type: Vdd
`timescale 1ns/10ps
`celldefine
//*****************************************************************
//   technology       : SG13G2
//   module name      : sg13g2_IOPadVdd
//   cell_description : Core 1.2V supply pad.
//*****************************************************************
module sg13g2_IOPadVdd (vdd, vss, iovdd, iovss);
	inout vdd;
	inout vss;
	inout iovdd;
	inout iovss;

	specify
	endspecify

endmodule
`endcelldefine
