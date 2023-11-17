////////////////////////////////////////////////////////////////////////
//
// Copyright 2023 IHP PDK Authors
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
//
////////////////////////////////////////////////////////////////////////

`celldefine
module RM_IHPSG13_1P_256x64_c2_bm_bist (
    A_CLK,
    A_MEN,
    A_WEN,
    A_REN,
    A_ADDR,
    A_DIN,
    A_DLY,
    A_DOUT,
    A_BM,
    A_BIST_CLK,
    A_BIST_EN,
    A_BIST_MEN,
    A_BIST_WEN,
    A_BIST_REN,
    A_BIST_ADDR,
    A_BIST_DIN,
    A_BIST_BM
);

    input A_CLK;
    input A_MEN;
    input A_WEN;
    input A_REN;
    input [7:0] A_ADDR;
    input [63:0] A_DIN;
    input A_DLY;
    output [63:0] A_DOUT;
    input [63:0] A_BM;
    input A_BIST_CLK;
    input A_BIST_EN;
    input A_BIST_MEN;
    input A_BIST_WEN;
    input A_BIST_REN;
    input [7:0] A_BIST_ADDR;
    input [63:0] A_BIST_DIN;
    input [63:0] A_BIST_BM;


`ifdef FUNCTIONAL  //  functional //


    SRAM_1P_behavioral_bm_bist #(
	.P_DATA_WIDTH(64),
	.P_ADDR_WIDTH(8)
	) i_SRAM_1P_behavioral_bm_bist (
                    .A_CLK(A_CLK),
                    .A_MEN(A_MEN),
                    .A_WEN(A_WEN),
                    .A_REN(A_REN),
                    .A_ADDR(A_ADDR),
                    .A_DLY(A_DLY),
                    .A_DIN(A_DIN),
                    .A_DOUT(A_DOUT), 
                    .A_BM(A_BM), 
                    .A_BIST_CLK(A_BIST_CLK),
                    .A_BIST_EN(A_BIST_EN),
                    .A_BIST_MEN(A_BIST_MEN),
                    .A_BIST_WEN(A_BIST_WEN),
                    .A_BIST_REN(A_BIST_REN),
                    .A_BIST_ADDR(A_BIST_ADDR),
                    .A_BIST_DIN(A_BIST_DIN), 
                    .A_BIST_BM(A_BIST_BM)
		);

`else

    wire A_CLK_DELAY;
    wire A_MEN_DELAY;
    wire A_WEN_DELAY;
    wire A_REN_DELAY;
    wire [7:0] A_ADDR_DELAY;
    wire [63:0] A_DIN_DELAY;
    wire [63:0] A_BM_DELAY;
    wire A_BIST_CLK_DELAY;
    wire A_BIST_MEN_DELAY;
    wire A_BIST_WEN_DELAY;
    wire A_BIST_REN_DELAY;
    wire [7:0] A_BIST_ADDR_DELAY;
    wire [63:0] A_BIST_DIN_DELAY;
    wire [63:0] A_BIST_BM_DELAY;

    reg notifier;

    wire A_RW_ACCESS = (A_WEN || A_REN) && A_MEN;
    wire A_W_ACCESS  = A_WEN && A_MEN;
    wire A_BIST_RW_ACCESS = (A_BIST_WEN || A_BIST_REN) && A_BIST_MEN;
    wire A_BIST_W_ACCESS  = A_BIST_WEN && A_BIST_MEN;



    SRAM_1P_behavioral_bm_bist #(
	.P_DATA_WIDTH(64),
	.P_ADDR_WIDTH(8)
	) i_SRAM_1P_behavioral_bm_bist (
                    .A_CLK(A_CLK_DELAY),
                    .A_MEN(A_MEN_DELAY),
                    .A_WEN(A_WEN_DELAY),
                    .A_REN(A_REN_DELAY),
                    .A_ADDR(A_ADDR_DELAY),
                    .A_DLY(A_DLY),
                    .A_DIN(A_DIN_DELAY),
                    .A_DOUT(A_DOUT), 
                    .A_BM(A_BM_DELAY), 
                    .A_BIST_CLK(A_BIST_CLK_DELAY),
                    .A_BIST_EN(A_BIST_EN),
                    .A_BIST_MEN(A_BIST_MEN_DELAY),
                    .A_BIST_WEN(A_BIST_WEN_DELAY),
                    .A_BIST_REN(A_BIST_REN_DELAY),
                    .A_BIST_ADDR(A_BIST_ADDR_DELAY),
                    .A_BIST_DIN(A_BIST_DIN_DELAY), 
                    .A_BIST_BM(A_BIST_BM_DELAY)
		);


    specify

      (posedge A_CLK *> (A_DOUT : A_DIN)) = (1.0, 1.0);
      $width(posedge A_CLK, 1.0,0,notifier);
      $setuphold(posedge A_CLK &&& A_MEN, posedge A_MEN, 1.0, 1.0,notifier,,,A_CLK_DELAY, A_MEN_DELAY);
      $setuphold(posedge A_CLK &&& A_MEN, posedge A_REN, 1.0, 1.0,notifier,,,A_CLK_DELAY, A_REN_DELAY);
      $setuphold(posedge A_CLK &&& A_MEN, posedge A_WEN, 1.0, 1.0,notifier,,,A_CLK_DELAY, A_WEN_DELAY);
      $setuphold(posedge A_CLK &&& A_MEN, negedge A_MEN, 1.0, 1.0,notifier,,,A_CLK_DELAY, A_MEN_DELAY);
      $setuphold(posedge A_CLK &&& A_MEN, negedge A_REN, 1.0, 1.0,notifier,,,A_CLK_DELAY, A_REN_DELAY);
      $setuphold(posedge A_CLK &&& A_MEN, negedge A_WEN, 1.0, 1.0,notifier,,,A_CLK_DELAY, A_WEN_DELAY);
      $setuphold(posedge A_CLK &&& A_RW_ACCESS, posedge A_ADDR, 1.0 ,1.0, notifier,,,A_CLK_DELAY, A_ADDR_DELAY);
      $setuphold(posedge A_CLK &&& A_RW_ACCESS, negedge A_ADDR, 1.0 ,1.0, notifier,,,A_CLK_DELAY, A_ADDR_DELAY);

      $setuphold(posedge A_CLK &&& A_W_ACCESS, posedge A_DIN, 1.0 ,1.0, notifier,,,A_CLK_DELAY, A_DIN_DELAY);
      $setuphold(posedge A_CLK &&& A_W_ACCESS, negedge A_DIN, 1.0 ,1.0, notifier,,,A_CLK_DELAY, A_DIN_DELAY);
      $setuphold(posedge A_CLK &&& A_W_ACCESS, posedge A_BM, 1.0 ,1.0, notifier,,,A_CLK_DELAY, A_BM_DELAY);
      $setuphold(posedge A_CLK &&& A_W_ACCESS, negedge A_BM, 1.0 ,1.0, notifier,,,A_CLK_DELAY, A_BM_DELAY);
      (posedge A_BIST_CLK *> (A_DOUT : A_BIST_DIN)) = (1.0, 1.0);
      $width(posedge A_BIST_CLK, 1.0,0,notifier);
      $setuphold(posedge A_BIST_CLK &&& A_BIST_MEN, posedge A_BIST_MEN, 1.0, 1.0,notifier,,,A_BIST_CLK_DELAY, A_BIST_MEN_DELAY);
      $setuphold(posedge A_BIST_CLK &&& A_BIST_MEN, posedge A_BIST_REN, 1.0, 1.0,notifier,,,A_BIST_CLK_DELAY, A_BIST_REN_DELAY);
      $setuphold(posedge A_BIST_CLK &&& A_BIST_MEN, posedge A_BIST_WEN, 1.0, 1.0,notifier,,,A_BIST_CLK_DELAY, A_BIST_WEN_DELAY);
      $setuphold(posedge A_BIST_CLK &&& A_BIST_MEN, negedge A_BIST_MEN, 1.0, 1.0,notifier,,,A_BIST_CLK_DELAY, A_BIST_MEN_DELAY);
      $setuphold(posedge A_BIST_CLK &&& A_BIST_MEN, negedge A_BIST_REN, 1.0, 1.0,notifier,,,A_BIST_CLK_DELAY, A_BIST_REN_DELAY);
      $setuphold(posedge A_BIST_CLK &&& A_BIST_MEN, negedge A_BIST_WEN, 1.0, 1.0,notifier,,,A_BIST_CLK_DELAY, A_BIST_WEN_DELAY);
      $setuphold(posedge A_BIST_CLK &&& A_BIST_RW_ACCESS, posedge A_BIST_ADDR, 1.0 ,1.0, notifier,,,A_BIST_CLK_DELAY, A_BIST_ADDR_DELAY);
      $setuphold(posedge A_BIST_CLK &&& A_BIST_RW_ACCESS, negedge A_BIST_ADDR, 1.0 ,1.0, notifier,,,A_BIST_CLK_DELAY, A_BIST_ADDR_DELAY);

      $setuphold(posedge A_BIST_CLK &&& A_BIST_W_ACCESS, posedge A_BIST_DIN, 1.0 ,1.0, notifier,,,A_BIST_CLK_DELAY, A_BIST_DIN_DELAY);
      $setuphold(posedge A_BIST_CLK &&& A_BIST_W_ACCESS, negedge A_BIST_DIN, 1.0 ,1.0, notifier,,,A_BIST_CLK_DELAY, A_BIST_DIN_DELAY);
      $setuphold(posedge A_BIST_CLK &&& A_BIST_W_ACCESS, posedge A_BIST_BM, 1.0 ,1.0, notifier,,,A_BIST_CLK_DELAY, A_BIST_BM_DELAY);
      $setuphold(posedge A_BIST_CLK &&& A_BIST_W_ACCESS, negedge A_BIST_BM, 1.0 ,1.0, notifier,,,A_BIST_CLK_DELAY, A_BIST_BM_DELAY);


    endspecify

`endif

endmodule
`endcelldefine
