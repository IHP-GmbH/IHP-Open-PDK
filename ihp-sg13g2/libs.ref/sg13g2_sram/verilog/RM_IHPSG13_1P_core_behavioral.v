// ------------------------------------------------------
//
//		Copyright 2023 IHP PDK Authors
//
//		Licensed under the Apache License, Version 2.0 (the "License");
//		you may not use this file except in compliance with the License.
//		You may obtain a copy of the License at
//		
//		   https://www.apache.org/licenses/LICENSE-2.0
//		
//		Unless required by applicable law or agreed to in writing, software
//		distributed under the License is distributed on an "AS IS" BASIS,
//		WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//		See the License for the specific language governing permissions and
//		limitations under the License.
//		
//		Generated on Mon Apr  7 14:15:45 2025		
//
// ------------------------------------------------------ 
`timescale 1ns/10ps
module SRAM_1P_behavioral (A_ADDR,
                                A_DIN,
                                A_MEN,	// Memory enable input	-> if disabled, the memory is deactivated
                                A_WEN,	// Common write enable input (bytes maskable with BM[23:0])
                                A_REN,	// Read enable input ->  if enabled for read access when WEN=1 --> Write-through
                                A_CLK,	// Clock input
                                A_DLY,	// Delay selection signals
                                A_DOUT
                                );

parameter  P_DATA_WIDTH=24;
parameter  P_ADDR_WIDTH=14;

input wire  [P_ADDR_WIDTH-1:0]	A_ADDR;
input wire  [P_DATA_WIDTH-1:0] 	A_DIN;
input wire                      A_MEN;	// Memory enable input	-> if disabled, the memory is deactivated
input wire                      A_WEN;	// Common write enable input (bytes maskable with BM[23:0])
input wire                      A_REN;	// Read enable input ->  if enabled for read access when WEN=1 --> Write-through
input wire                      A_CLK;	// Clock input
input wire                      A_DLY;	// Delay selection signals
output wire [P_DATA_WIDTH-1:0]  A_DOUT;	// 24 Data outputs





reg [P_DATA_WIDTH-1:0]    memory [0:2**(P_ADDR_WIDTH)-1]; // memory
reg [P_DATA_WIDTH-1:0]    dr_r;



wire  [P_ADDR_WIDTH-1:0]	ADDR_MUX;
wire  [P_DATA_WIDTH-1:0] 	DIN_MUX;
wire                        MEN_MUX;
wire                        WEN_MUX;
wire                        REN_MUX;
wire                        CLK_MUX;

//BIST-MUX
assign ADDR_MUX=A_ADDR;
assign DIN_MUX=A_DIN;
assign MEN_MUX=A_MEN;
assign WEN_MUX=A_WEN;
assign REN_MUX=A_REN;
assign CLK_MUX=A_CLK;

always @(posedge CLK_MUX) begin
   if(MEN_MUX==1'b1 && WEN_MUX==1'b1) begin
		memory[ADDR_MUX] <= DIN_MUX;
		if (REN_MUX==1'b1) begin
			dr_r<= DIN_MUX;
		end
    end
    else if(MEN_MUX==1'b1 && REN_MUX==1'b1) begin
        dr_r<=memory[ADDR_MUX];
    end
end

assign A_DOUT=  dr_r;


endmodule
