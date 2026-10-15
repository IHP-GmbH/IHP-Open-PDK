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

`timescale 1ns/10ps
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
