************************************************************************
* 
* Copyright 2023 IHP PDK Authors
* 
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
* 
*    https://www.apache.org/licenses/LICENSE-2.0
* 
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
* 
************************************************************************

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_a21o_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_a21o_1 X A1 A2 B1 VDD VSS
*.PININFO A1:I A2:I B1:I X:O VDD:B VSS:B
MN0 net1 A1 net2 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN1 net2 A2 VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN2 net1 B1 VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN3 X net1 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MP0 net1 B1 net3 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP1 net3 A1 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP2 net3 A2 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP3 X net1 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_a21o_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_a21o_2 X A1 A2 B1 VDD VSS
*.PININFO A1:I A2:I B1:I X:O VDD:B VSS:B
MN0 net1 A1 net2 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN1 net2 A2 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN2 net1 B1 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN3 X net1 VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MP0 net1 B1 net3 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP1 net3 A1 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP2 net3 A2 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP3 X net1 VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_a21oi_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_a21oi_1 Y A1 A2 B1 VDD VSS
*.PININFO A1:I A2:I B1:I Y:O VDD:B VSS:B
MMNB0 Y B1 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MMNA1 sndA1 A2 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MMNA0 Y A1 sndA1 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MMPB0 Y B1 pndA VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MMPA1 pndA A2 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MMPA0 pndA A1 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_a21oi_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_a21oi_2 Y A1 A2 B1 VDD VSS
*.PININFO A1:I A2:I B1:I Y:O VDD:B VSS:B
MMNB0 Y B1 VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MMNA1 sndA1 A2 VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MMNA0 Y A1 sndA1 VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MMPB0 Y B1 pndA VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MMPA1 pndA A2 VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MMPA0 pndA A1 VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_a221oi_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_a221oi_1 Y A1 A2 B1 B2 C1 VDD VSS
*.PININFO A1:I A2:I B1:I B2:I C1:I Y:O VDD:B VSS:B
MMPC0 Y C1 pndB VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MMPB1 pndB B2 pndA VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MMPB0 pndB B1 pndA VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MMPA1 pndA A2 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MMPA0 pndA A1 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MMNC0 Y C1 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MMNB1 sndB1 B2 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MMNB0 Y B1 sndB1 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MMNA1 sndA1 A2 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MMNA0 Y A1 sndA1 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_and2_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_and2_1 X A B VDD VSS
*.PININFO A:I B:I X:O VDD:B VSS:B
MX0 net4 A net2 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX2 X net4 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX3 net2 B VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX1 net4 B VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX4 X net4 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX5 net4 A VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_and2_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_and2_2 X A B VDD VSS
*.PININFO A:I B:I X:O VDD:B VSS:B
MX0 net4 A net2 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX2 X net4 VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MX3 net2 B VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX1 net4 B VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX4 X net4 VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MX5 net4 A VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_and3_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_and3_1 X A B C VDD VSS
*.PININFO A:I B:I C:I X:O VDD:B VSS:B
MX0 net3 C VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX2 X net2 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX5 net2 A net1 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX6 net1 B net3 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX3 X net2 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX1 net2 B VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX4 net2 A VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX7 net2 C VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_and3_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_and3_2 X A B C VDD VSS
*.PININFO A:I B:I C:I X:O VDD:B VSS:B
MX0 net3 C VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX2 X net2 VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MX5 net2 A net1 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX6 net1 B net3 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX3 X net2 VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MX1 net2 B VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX4 net2 A VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX7 net2 C VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_and4_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_and4_1 X A B C D VDD VSS
*.PININFO A:I B:I C:I D:I X:O VDD:B VSS:B
MN4 net17 D VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN3 net16 C net17 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN2 net15 B net16 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN1 net1 A net15 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN0 X net1 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MP0 net1 A VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MP4 X net1 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP3 net1 D VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MP2 net1 C VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MP1 net1 B VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_and4_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_and4_2 X A B C D VDD VSS
*.PININFO A:I B:I C:I D:I X:O VDD:B VSS:B
MN4 net17 D VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN3 net16 C net17 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN2 net15 B net16 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN1 net1 A net15 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN0 X net1 VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MP0 net1 A VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MP4 X net1 VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MP3 net1 D VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MP2 net1 C VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MP1 net1 B VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_antennanp
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_antennanp A VDD VSS
*.PININFO A:I VDD:B VSS:B
Ddn_1 VSS A dantenna m=1 w=780n l=780n a=608.4f p=3.12u
DD0 A VDD dpantenna m=1 w=1.05u l=1.34u a=1.407p p=4.78u
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_buf_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_buf_1 X A VDD VSS
*.PININFO A:I X:O VDD:B VSS:B
MN1 net1 A VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MN0 X net1 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MP1 X net1 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP0 net1 A VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_buf_16
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_buf_16 X A VDD VSS
*.PININFO A:I X:O VDD:B VSS:B
MN1 net1 A VSS VSS sg13_lv_nmos m=1 w=4.44u l=130.00n ng=6
MN0 X net1 VSS VSS sg13_lv_nmos m=1 w=11.84u l=130.00n ng=16
MP1 X net1 VDD VDD sg13_lv_pmos m=1 w=17.92u l=130.00n ng=16
MP0 net1 A VDD VDD sg13_lv_pmos m=1 w=6.72u l=130.00n ng=6
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_buf_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_buf_2 X A VDD VSS
*.PININFO A:I X:O VDD:B VSS:B
MN1 net1 A VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN0 X net1 VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MP1 X net1 VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MP0 net1 A VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_buf_4
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_buf_4 X A VDD VSS
*.PININFO A:I X:O VDD:B VSS:B
MN1 net1 A VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN0 X net1 VSS VSS sg13_lv_nmos m=1 w=2.96u l=130.00n ng=4
MP1 X net1 VDD VDD sg13_lv_pmos m=1 w=4.48u l=130.00n ng=4
MP0 net1 A VDD VDD sg13_lv_pmos m=1 w=1.68u l=130.00n ng=2
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_buf_8
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_buf_8 X A VDD VSS
*.PININFO A:I X:O VDD:B VSS:B
MN1 net1 A VSS VSS sg13_lv_nmos m=1 w=2.22u l=130.00n ng=3
MN0 X net1 VSS VSS sg13_lv_nmos m=1 w=5.92u l=130.00n ng=8
MP1 X net1 VDD VDD sg13_lv_pmos m=1 w=8.96u l=130.00n ng=8
MP0 net1 A VDD VDD sg13_lv_pmos m=1 w=3.36u l=130.00n ng=3
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_decap_4
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_decap_4 VDD VSS
*.PININFO VDD:B VSS:B
MX1 VSS VDD VSS VSS sg13_lv_nmos m=1 w=420.00n l=1.000u ng=1
MX0 VDD VSS VDD VDD sg13_lv_pmos m=1 w=1.000u l=1.000u ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_decap_8
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_decap_8 VDD VSS
*.PININFO VDD:B VSS:B
MX1 VSS VDD VSS VSS sg13_lv_nmos m=1 w=840.00n l=1.000u ng=2
MX0 VDD VSS VDD VDD sg13_lv_pmos m=1 w=2.000u l=1.000u ng=2
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_dfrbp_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_dfrbp_1 Q Q_N CLK D RESET_B VDD VSS
*.PININFO CLK:I D:I RESET_B:I Q:O Q_N:O VDD:B VSS:B
MN13 net12 net2 VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN14 net5 clkneg net12 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN15 net2 net5 net11 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN16 net11 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN6 Q_N net5 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN0 Db D net10 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN1 net10 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN7 Db clkneg net6 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN8 net6 clkpos net9 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN9 net9 net4 net8 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN10 net8 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN11 net4 net6 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN2 clkneg CLK VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN12 net4 clkpos net5 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN3 clkpos clkneg VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN4 Q net1 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN5 net1 net5 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MP14 net5 clkpos net3 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP15 net2 net5 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP16 net2 RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP6 Q_N net5 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP7 Db clkpos net6 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP0 Db RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP1 Db D VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP8 net7 net4 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP9 net6 clkneg net7 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP10 net6 RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP2 clkneg CLK VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP3 clkpos clkneg VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP11 net4 net6 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP12 net4 clkneg net5 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP4 Q net1 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP13 net3 net2 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP5 net1 net5 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_dfrbp_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_dfrbp_2 Q Q_N CLK D RESET_B VDD VSS
*.PININFO CLK:I D:I RESET_B:I Q:O Q_N:O VDD:B VSS:B
MN13 net12 net2 VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN14 net5 clkneg net12 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN15 net2 net5 net11 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN16 net11 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN6 Q_N net5 VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MN0 Db D net10 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN1 net10 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN7 Db clkneg net6 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN8 net6 clkpos net9 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN9 net9 net4 net8 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN10 net8 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN11 net4 net6 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN2 clkneg CLK VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN12 net4 clkpos net5 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN3 clkpos clkneg VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN4 Q net1 VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MN5 net1 net5 VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MP14 net5 clkpos net3 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP15 net2 net5 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP16 net2 RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP6 Q_N net5 VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MP7 Db clkpos net6 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP0 Db RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP1 Db D VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP8 net7 net4 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP9 net6 clkneg net7 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP10 net6 RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP2 clkneg CLK VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP3 clkpos clkneg VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP11 net4 net6 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP12 net4 clkneg net5 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP4 Q net1 VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MP13 net3 net2 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP5 net1 net5 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_dlhq_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_dlhq_1 Q D GATE VDD VSS
*.PININFO D:I GATE:I Q:O VDD:B VSS:B
MX17 Q qint_b VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX16 qint GATE_BB net8 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MX14 qint_b qint VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX12 Db D VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX9 GATE_B GATE VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX7 GATE_BB GATE_B VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX4 net8 qint_b VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MX3 net4 GATE_B qint VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX1 net4 Db VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX15 GATE_B GATE VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX13 GATE_BB GATE_B VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX11 qint GATE_B net9 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX10 Q qint_b VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX8 net7 Db VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX6 net9 qint_b VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX5 qint_b qint VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX2 qint GATE_BB net7 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX0 Db D VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_dlhr_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_dlhr_1 Q Q_N D GATE RESET_B VDD VSS
*.PININFO D:I GATE:I RESET_B:I Q:O Q_N:O VDD:B VSS:B
MX0 qint_b RESET_B VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX9 Q qint_b VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX15 qint GATE_BB net11 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MX6 net11 qint_b VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MX10 qint GATE_B net2 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX18 net2 Db VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX13 Db D VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX5 GATE_B GATE VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX3 Q_N qintn_b VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX1 qint_b qint VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX20 GATE_BB GATE_B VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX2 qintn_b qint_b VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX12 qint_b qint net9 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX21 net9 RESET_B VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX11 qint GATE_B net7 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX14 net7 qint_b VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX7 Q qint_b VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX16 qint GATE_BB net1 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX23 net1 Db VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX4 Db D VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX19 GATE_B GATE VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX8 Q_N qintn_b VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX17 GATE_BB GATE_B VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX22 qintn_b qint_b VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_dlhrq_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_dlhrq_1 Q D GATE RESET_B VDD VSS
*.PININFO D:I GATE:I RESET_B:I Q:O VDD:B VSS:B
MX21 net116 RESET_B VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX7 Q qint_b VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX17 GATE_BB GATE_B VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX11 qint GATE_B net89 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX12 qint_b qint net116 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX4 Db D VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX23 net61 Db VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX16 qint GATE_BB net61 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX14 net89 qint_b VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX19 GATE_B GATE VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX18 net60 Db VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX0 qint_b RESET_B VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX15 qint GATE_BB net92 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MX9 Q qint_b VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX6 net92 qint_b VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MX5 GATE_B GATE VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX13 Db D VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX10 qint GATE_B net60 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX20 GATE_BB GATE_B VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX1 qint_b qint VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_dllr_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_dllr_1 Q Q_N D GATE_N RESET_B VDD VSS
*.PININFO D:I GATE_N:I RESET_B:I Q:O Q_N:O VDD:B VSS:B
MX4 Db D VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX19 gnb GATE_N VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX17 gnbb gnb VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX14 net89 qint_b VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX12 qint_b qint net116 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX21 net116 RESET_B VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX11 qint gnbb net89 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX8 Q_N qintn_b VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX16 qint gnb net61 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX22 qintn_b qint_b VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX23 net61 Db VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX7 Q qint_b VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX20 gnbb gnb VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX10 qint gnbb net60 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX2 qintn_b qint_b VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX3 Q_N qintn_b VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX18 net60 Db VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX6 net92 qint_b VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MX0 qint_b RESET_B VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX13 Db D VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX5 gnb GATE_N VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX9 Q qint_b VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX15 qint gnb net92 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MX1 qint_b qint VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_dllrq_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_dllrq_1 Q D GATE_N RESET_B VDD VSS
*.PININFO D:I GATE_N:I RESET_B:I Q:O VDD:B VSS:B
MX11 qint gnbb net89 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX16 qint gnb net61 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX21 net116 RESET_B VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX7 Q qint_b VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX23 net61 Db VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX14 net89 qint_b VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX12 qint_b qint net116 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX4 Db D VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX19 gnb GATE_N VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX17 gnbb gnb VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX18 net59 Db VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX0 qint_b RESET_B VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX5 gnb GATE_N VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX6 net92 qint_b VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MX1 qint_b qint VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX9 Q qint_b VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX10 qint gnbb net59 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX13 Db D VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX20 gnbb gnb VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX15 qint gnb net92 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_dlygate4sd1_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_dlygate4sd1_1 X A VDD VSS
*.PININFO A:I X:O VDD:B VSS:B
MP3 X net3 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP2 net3 net2 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP1 net2 net1 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP0 net1 A VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MN3 X net3 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN2 net3 net2 VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN1 net2 net1 VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN0 net1 A VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_dlygate4sd2_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_dlygate4sd2_1 X A VDD VSS
*.PININFO A:I X:O VDD:B VSS:B
MP3 X net3 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP2 net3 net2 VDD VDD sg13_lv_pmos m=1 w=1.000u l=250.00n ng=1
MP1 net2 net1 VDD VDD sg13_lv_pmos m=1 w=1.000u l=250.00n ng=1
MP0 net1 A VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MN3 X net3 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN2 net3 net2 VSS VSS sg13_lv_nmos m=1 w=420.00n l=180.00n ng=1
MN1 net2 net1 VSS VSS sg13_lv_nmos m=1 w=420.00n l=180.00n ng=1
MN0 net1 A VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_dlygate4sd3_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_dlygate4sd3_1 X A VDD VSS
*.PININFO A:I X:O VDD:B VSS:B
MP3 X net3 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP2 net3 net2 VDD VDD sg13_lv_pmos m=1 w=1.000u l=500.0n ng=1
MP1 net2 net1 VDD VDD sg13_lv_pmos m=1 w=1.000u l=500.0n ng=1
MP0 net1 A VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MN3 X net3 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN2 net3 net2 VSS VSS sg13_lv_nmos m=1 w=420.00n l=500.0n ng=1
MN1 net2 net1 VSS VSS sg13_lv_nmos m=1 w=420.00n l=500.0n ng=1
MN0 net1 A VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_ebufn_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_ebufn_2 Z A TE_B VDD VSS
*.PININFO A:I TE_B:I Z:O VDD:B VSS:B
MN3 net4 net3 VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MN2 Z net1 net4 VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MN1 net3 TE_B VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN0 net1 A VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MP3 net2 TE_B VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MP2 Z net1 net2 VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MP1 net3 TE_B VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP0 net1 A VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_ebufn_4
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_ebufn_4 Z A TE_B VDD VSS
*.PININFO A:I TE_B:I Z:O VDD:B VSS:B
MN0 net23 A VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN1 net21 TE_B VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN2 Z net23 net22 VSS sg13_lv_nmos m=1 w=2.96u l=130.00n ng=4
MN3 net22 net21 VSS VSS sg13_lv_nmos m=1 w=2.96u l=130.00n ng=4
MP0 net23 A VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP1 net21 TE_B VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP2 Z net23 net24 VDD sg13_lv_pmos m=1 w=4.48u l=130.00n ng=4
MP3 net24 TE_B VDD VDD sg13_lv_pmos m=1 w=4.48u l=130.00n ng=4
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_ebufn_8
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_ebufn_8 Z A TE_B VDD VSS
*.PININFO A:I TE_B:I Z:O VDD:B VSS:B
MN3 net23 net22 VSS VSS sg13_lv_nmos m=1 w=5.92u l=130.00n ng=8
MN2 Z net21 net23 VSS sg13_lv_nmos m=1 w=5.92u l=130.00n ng=8
MN1 net22 TE_B VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN0 net21 A VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MP3 net24 TE_B VDD VDD sg13_lv_pmos m=1 w=8.96u l=130.00n ng=8
MP2 Z net21 net24 VDD sg13_lv_pmos m=1 w=8.96u l=130.00n ng=8
MP1 net22 TE_B VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP0 net21 A VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_einvn_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_einvn_2 Z A TE_B VDD VSS
*.PININFO A:I TE_B:I Z:O VDD:B VSS:B
MN2 TE TE_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN1 net1 TE VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MN0 Z A net1 VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MP2 TE TE_B VDD VDD sg13_lv_pmos m=1 w=640.00n l=130.00n ng=1
MP1 net2 TE_B VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MP0 Z A net2 VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_einvn_4
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_einvn_4 Z A TE_B VDD VSS
*.PININFO A:I TE_B:I Z:O VDD:B VSS:B
MN1 net16 TE VSS VSS sg13_lv_nmos m=1 w=2.96u l=130.00n ng=4
MN2 TE TE_B VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN0 Z A net16 VSS sg13_lv_nmos m=1 w=2.96u l=130.00n ng=4
MP2 TE TE_B VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP1 net17 TE_B VDD VDD sg13_lv_pmos m=1 w=4.48u l=130.00n ng=4
MP0 Z A net17 VDD sg13_lv_pmos m=1 w=4.48u l=130.00n ng=4
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_einvn_8
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_einvn_8 Z A TE_B VDD VSS
*.PININFO A:I TE_B:I Z:O VDD:B VSS:B
MN0 Z A net29 VSS sg13_lv_nmos m=1 w=5.92u l=130.00n ng=8
MN2 TE TE_B VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN1 net29 TE VSS VSS sg13_lv_nmos m=1 w=5.92u l=130.00n ng=8
MP1 net28 TE_B VDD VDD sg13_lv_pmos m=1 w=8.96u l=130.00n ng=8
MP0 Z A net28 VDD sg13_lv_pmos m=1 w=8.96u l=130.00n ng=8
MP2 TE TE_B VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_inv_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_inv_1 Y A VDD VSS
*.PININFO A:I Y:O VDD:B VSS:B
MX1 Y A VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX0 Y A VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_inv_16
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_inv_16 Y A VDD VSS
*.PININFO A:I Y:O VDD:B VSS:B
MX1 Y A VSS VSS sg13_lv_nmos m=1 w=11.84u l=130.00n ng=16
MX0 Y A VDD VDD sg13_lv_pmos m=1 w=17.92u l=130.00n ng=16
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_inv_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_inv_2 Y A VDD VSS
*.PININFO A:I Y:O VDD:B VSS:B
MX1 Y A VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MX0 Y A VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_inv_4
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_inv_4 Y A VDD VSS
*.PININFO A:I Y:O VDD:B VSS:B
MP0 Y A VDD VDD sg13_lv_pmos m=1 w=4.48u l=130.00n ng=4
MN0 Y A VSS VSS sg13_lv_nmos m=1 w=2.96u l=130.00n ng=4
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_inv_8
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_inv_8 Y A VDD VSS
*.PININFO A:I Y:O VDD:B VSS:B
MX1 Y A VSS VSS sg13_lv_nmos m=1 w=5.92u l=130.00n ng=8
MX0 Y A VDD VDD sg13_lv_pmos m=1 w=8.96u l=130.00n ng=8
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_lgcp_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_lgcp_1 GCLK CLK GATE VDD VSS
*.PININFO CLK:I GATE:I GCLK:O VDD:B VSS:B
MX15 CLKBB CLKB VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX14 net1 CLKBB net4 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX12 int_GATE net1 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX11 net4 GATE VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX9 net3 int_GATE VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX7 GCLK net3 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX5 net1 CLKB net6 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MX4 CLKB CLK VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX3 net3 CLK VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX2 net6 int_GATE VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MX19 GCLK net3 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX18 net3 int_GATE net5 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX17 int_GATE net1 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX16 CLKBB CLKB VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX13 net7 int_GATE VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX10 net2 GATE VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX8 net1 CLKBB net7 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX6 CLKB CLK VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX1 net5 CLK VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX0 net1 CLKB net2 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_mux2_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_mux2_1 X A0 A1 S VDD VSS
*.PININFO A0:I A1:I S:I X:O VDD:B VSS:B
MP0 net4 S VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP4 X net6 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP3 net6 A1 net5 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP5 Sb S VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MP2 net5 Sb VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP1 net6 A0 net4 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MN4 net3 S VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN1 net1 Sb VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN6 X net6 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN5 Sb S VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MN2 net6 A1 net3 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN0 net6 A0 net1 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_mux2_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_mux2_2 X A0 A1 S VDD VSS
*.PININFO A0:I A1:I S:I X:O VDD:B VSS:B
MP0 net4 S VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP4 X net6 VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MP3 net6 A1 net5 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP5 Sb S VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MP2 net5 Sb VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP1 net6 A0 net4 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MN4 net3 S VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN1 net1 Sb VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN6 X net6 VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MN5 Sb S VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MN2 net6 A1 net3 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN0 net6 A0 net1 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_mux4_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_mux4_1 X A0 A1 A2 A3 S0 S1 VDD VSS
*.PININFO A0:I A1:I A2:I A3:I S0:I S1:I X:O VDD:B VSS:B
MN12 X Xb VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN18 low S0b net7 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN17 net7 A0 VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN19 low S1b Xb VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN10 high S1 Xb VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN9 net4 A3 VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN8 high S0 net4 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN14 net6 A2 VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN13 high S0b net6 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN16 net2 A1 VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN15 low S0 net2 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN1 S1b S1 VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN0 S0b S0 VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MP19 low S1 Xb VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP11 high S1b Xb VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP10 X Xb VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP9 high S0b net3 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP8 net3 A3 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP14 high S0 net5 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP13 net5 A2 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP18 net8 A0 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP17 low S0 net8 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP1 S1b S1 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP0 S0b S0 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP16 low S0b net1 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP15 net1 A1 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_nand2_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_nand2_1 Y A B VDD VSS
*.PININFO A:I B:I Y:O VDD:B VSS:B
MP1 Y B VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP0 Y A VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MN1 net1 B VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN0 Y A net1 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_nand2_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_nand2_2 Y A B VDD VSS
*.PININFO A:I B:I Y:O VDD:B VSS:B
MP1 Y B VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MP0 Y A VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MN1 net1 B VSS VSS sg13_lv_nmos m=1 w=1.44u l=130.00n ng=2
MN0 Y A net1 VSS sg13_lv_nmos m=1 w=1.44u l=130.00n ng=2
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_nand2b_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_nand2b_1 Y A_N B VDD VSS
*.PININFO A_N:I B:I Y:O VDD:B VSS:B
MX0 Y net2 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX1 net2 A_N VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX3 Y B VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX2 Y net2 net1 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX4 net2 A_N VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX5 net1 B VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_nand2b_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_nand2b_2 Y A_N B VDD VSS
*.PININFO A_N:I B:I Y:O VDD:B VSS:B
MX0 Y A VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MX1 A A_N VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX3 Y B VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MX2 Y B net1 VSS sg13_lv_nmos m=1 w=1.44u l=130.00n ng=2
MX4 A A_N VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX5 net1 A VSS VSS sg13_lv_nmos m=1 w=1.44u l=130.00n ng=2
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_nand3_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_nand3_1 Y A B C VDD VSS
*.PININFO A:I B:I C:I Y:O VDD:B VSS:B
MX1 Y A VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX2 Y B VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX6 Y C VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX3 net2 B net3 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX4 net3 C VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX7 Y A net2 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_nand3b_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_nand3b_1 Y A_N B C VDD VSS
*.PININFO A_N:I B:I C:I Y:O VDD:B VSS:B
MX0 net1 A_N VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX1 Y net1 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX2 Y B VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX6 Y C VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX3 net2 B net3 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX4 net3 C VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX5 net1 A_N VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX7 Y net1 net2 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_nand4_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_nand4_1 Y A B C D VDD VSS
*.PININFO A:I B:I C:I D:I Y:O VDD:B VSS:B
MP0 Y D VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX1 Y A VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX2 Y B VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX6 Y C VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX3 net2 B net3 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX4 net3 C net5 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX7 Y A net2 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN0 net5 D VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_nor2_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_nor2_1 Y A B VDD VSS
*.PININFO A:I B:I Y:O VDD:B VSS:B
MX0 Y A VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX3 Y B VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX1 net1 A VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX2 Y B net1 VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_nor2_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_nor2_2 Y A B VDD VSS
*.PININFO A:I B:I Y:O VDD:B VSS:B
MX0 Y A VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MX3 Y B VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MX1 net1 A VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MX2 Y B net1 VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_nor2b_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_nor2b_1 Y A B_N VDD VSS
*.PININFO A:I B_N:I Y:O VDD:B VSS:B
MN0 B B_N VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX0 Y A VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX3 Y B VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MP0 B B_N VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX1 net1 B VDD VDD sg13_lv_pmos m=1 w=1.12e-06 l=130.00n ng=1
MX2 Y A net1 VDD sg13_lv_pmos m=1 w=1.12e-06 l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_nor2b_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_nor2b_2 Y A B_N VDD VSS
*.PININFO A:I B_N:I Y:O VDD:B VSS:B
MN0 B B_N VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX0 Y A VSS VSS sg13_lv_nmos m=1 w=1.44u l=130.00n ng=2
MX3 Y B VSS VSS sg13_lv_nmos m=1 w=1.44u l=130.00n ng=2
MP0 B B_N VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX1 net1 B VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MX2 Y A net1 VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_nor3_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_nor3_1 Y A B C VDD VSS
*.PININFO A:I B:I C:I Y:O VDD:B VSS:B
MX3 Y C net2 VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX0 net2 B net3 VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX2 net3 A VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX4 Y A VSS VSS sg13_lv_nmos m=1 w=770.00n l=130.00n ng=1
MX1 Y B VSS VSS sg13_lv_nmos m=1 w=770.00n l=130.00n ng=1
MX5 Y C VSS VSS sg13_lv_nmos m=1 w=770.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_nor3_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_nor3_2 Y A B C VDD VSS
*.PININFO A:I B:I C:I Y:O VDD:B VSS:B
MX3 Y C net2 VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MX0 net2 B net3 VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MX2 net3 A VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MX4 Y A VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MX1 Y B VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MX5 Y C VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_nor4_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_nor4_1 Y A B C D VDD VSS
*.PININFO A:I B:I C:I D:I Y:O VDD:B VSS:B
MX0 net3 A VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX5 net2 B net3 VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX6 net1 C net2 VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX7 Y D net1 VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX1 Y A VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX2 Y D VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX3 Y B VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX4 Y C VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_nor4_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_nor4_2 Y A B C D VDD VSS
*.PININFO A:I B:I C:I D:I Y:O VDD:B VSS:B
MX0 net3 A VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MX5 net2 B net3 VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MX6 net1 C net2 VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MX7 Y D net1 VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MX1 Y A VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MX2 Y D VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MX3 Y B VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MX4 Y C VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_o21ai_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_o21ai_1 Y A1 A2 B1 VDD VSS
*.PININFO A1:I A2:I B1:I Y:O VDD:B VSS:B
MP2 net14 A1 VDD VDD sg13_lv_pmos m=1 w=1.12u l=150.00n ng=1
MP1 Y A2 net14 VDD sg13_lv_pmos m=1 w=1.12u l=150.00n ng=1
MP0 Y B1 VDD VDD sg13_lv_pmos m=1 w=1.12u l=150.00n ng=1
MN2 net1 A2 VSS VSS sg13_lv_nmos m=1 w=740.00n l=150.00n ng=1
MN3 net1 A1 VSS VSS sg13_lv_nmos m=1 w=740.00n l=150.00n ng=1
MN0 Y B1 net1 VSS sg13_lv_nmos m=1 w=740.00n l=150.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_or2_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_or2_1 X A B VDD VSS
*.PININFO A:I B:I X:O VDD:B VSS:B
MP0 net2 B net3 VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MP1 net3 A VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MP2 X net2 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MN0 net2 A VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MN1 net2 B VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MN2 X net2 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_or2_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_or2_2 X A B VDD VSS
*.PININFO A:I B:I X:O VDD:B VSS:B
MP0 net2 B net3 VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MP1 net3 A VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MP2 X net2 VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MN0 net2 A VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MN1 net2 B VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MN2 X net2 VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_or3_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_or3_1 X A B C VDD VSS
*.PININFO A:I B:I C:I X:O VDD:B VSS:B
MX0 net1 C VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX1 X net1 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX6 net1 B VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX7 net1 A VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX2 X net1 VDD VDD sg13_lv_pmos m=1 w=1.12e-06 l=130.00n ng=1
MX3 net9 B net12 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX4 net12 A VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX5 net1 C net9 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_or3_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_or3_2 X A B C VDD VSS
*.PININFO A:I B:I C:I X:O VDD:B VSS:B
MX0 net1 C VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX1 X net1 VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MX6 net1 B VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX7 net1 A VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX2 X net1 VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MX3 net9 B net12 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX4 net12 A VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX5 net1 C net9 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_or4_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_or4_1 X A B C D VDD VSS
*.PININFO A:I B:I C:I D:I X:O VDD:B VSS:B
MN4 X net1 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN3 net1 D VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MN2 net1 C VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MN1 net1 B VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MN0 net1 A VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MP4 net4 A VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP3 net3 B net4 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP2 net2 C net3 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP1 net1 D net2 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP0 X net1 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_or4_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_or4_2 X A B C D VDD VSS
*.PININFO A:I B:I C:I D:I X:O VDD:B VSS:B
MN4 X net1 VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MN3 net1 D VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MN2 net1 C VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MN1 net1 B VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MN0 net1 A VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MP4 net4 A VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP3 net3 B net4 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP2 net2 C net3 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP1 net1 D net2 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP0 X net1 VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_sdfbbp_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_sdfbbp_1 Q Q_N CLK D RESET_B SCD SCE SET_B VDD VSS
*.PININFO CLK:I D:I RESET_B:I SCD:I SCE:I SET_B:I Q:O Q_N:O VDD:B VSS:B
MX46 resetbb RESET_B VDD VDD sg13_lv_pmos m=1 w=640.00n l=130.00n ng=1
MX45 pre_q DbbLatch2 net8 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX44 pre_q SET_B VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX41 CLKbb CLKb VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX39 SCEb SCE VDD VDD sg13_lv_pmos m=1 w=640.00n l=130.00n ng=1
MX38 Db D net3 VDD sg13_lv_pmos m=1 w=640.00n l=130.00n ng=1
MX33 DbbTG CLKb net10 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MX28 net10 DbLatchM VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MX27 net3 SCE VDD VDD sg13_lv_pmos m=1 w=640.00n l=130.00n ng=1
MX26 Q_N pre_q VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX24 net1 DbLatchM VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX19 net8 resetbb VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX17 DbLatchM SET_B VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX16 net2 SCD VDD VDD sg13_lv_pmos m=1 w=640.00n l=130.00n ng=1
MX15 CLKb CLK VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX14 DbLatchM DbbTG net7 VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX11 Db CLKbb DbbTG VDD sg13_lv_pmos m=1 w=640.00n l=130.00n ng=1
MX9 Db SCEb net2 VDD sg13_lv_pmos m=1 w=640.00n l=130.00n ng=1
MX8 pre_qb pre_q VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX7 net7 resetbb VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX6 net6 pre_q VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MX5 DbbLatch2 CLKbb net6 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MX4 DbbLatch2 CLKb net1 VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX3 Q pre_qb VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MN1 Db SCE net5 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN0 net5 SCD VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX47 pre_q DbbLatch2 net11 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX43 Db CLKb DbbTG VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX42 net4 SCEb VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX40 CLKbb CLKb VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX37 resetbb RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX36 net14 pre_q VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX35 DbLatchM DbbTG net12 VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX34 SCEb SCE VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX32 net12 SET_B VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX31 net15 DbLatchM VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX29 net11 SET_B VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX25 DbbTG CLKbb net15 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX23 Db D net4 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX22 pre_qb pre_q VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX21 DbbLatch2 CLKb net14 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX20 Q pre_qb VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX18 net13 DbLatchM VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX13 CLKb CLK VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX10 DbbLatch2 CLKbb net13 VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX2 DbLatchM resetbb net12 VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX1 Q_N pre_q VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX0 pre_q resetbb net11 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_sighold
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_sighold SH VDD VSS
*.PININFO SH:B VDD:B VSS:B
MN0 net1 SH VSS VSS sg13_lv_nmos m=1 w=300.0n l=130.00n ng=1
MN1 SH net1 VSS VSS sg13_lv_nmos m=1 w=300.0n l=700.0n ng=1
MP0 net1 SH VDD VDD sg13_lv_pmos m=1 w=450.00n l=130.00n ng=1
MP1 SH net1 VDD VDD sg13_lv_pmos m=1 w=300.0n l=700.0n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_slgcp_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_slgcp_1 GCLK CLK GATE SCE VDD VSS
*.PININFO CLK:I GATE:I SCE:I GCLK:O VDD:B VSS:B
MX19 GCLK net5 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX18 net1 CLKbb net6 VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX16 CLKbb CLKb VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX14 net5 int_GATE VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX13 net3 SCE VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX11 net6 CLKb net4 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MX9 int_GATE net6 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX7 CLKb CLK VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX5 net5 CLK VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX3 net4 int_GATE VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MX2 net1 GATE net3 VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MX21 int_GATE net6 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX20 net2 CLK VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX17 net1 SCE VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX15 net6 CLKb net1 VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX12 net7 int_GATE VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MX10 net5 int_GATE net2 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MX8 GCLK net5 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX6 CLKbb CLKb VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX4 net1 GATE VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX1 CLKb CLK VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX0 net6 CLKbb net7 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_tiehi
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_tiehi L_HI VDD VSS
*.PININFO L_HI:O VDD:B VSS:B
MMN2 net3 net2 VSS VSS sg13_lv_nmos m=1 w=795.00n l=130.00n ng=1
MMN1 net1 net1 VSS VSS sg13_lv_nmos m=1 w=300n l=130.00n ng=1
MMP2 L_HI net3 VDD VDD sg13_lv_pmos m=1 w=1.155u l=130.00n ng=1
MMP1 net2 net1 VDD VDD sg13_lv_pmos m=1 w=660.0n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_tielo
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_tielo L_LO VDD VSS
*.PININFO L_LO:O VDD:B VSS:B
MMN1 net3 net2 VSS VSS sg13_lv_nmos m=1 w=385.00n l=130.00n ng=1
MMN2 L_LO net1 VSS VSS sg13_lv_nmos m=1 w=880.0n l=130.00n ng=1
MMP1 net2 net2 VDD VDD sg13_lv_pmos m=1 w=300n l=130.00n ng=1
MMP2 net1 net3 VDD VDD sg13_lv_pmos m=1 w=1.045u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_xnor2_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_xnor2_1 Y A B VDD VSS
*.PININFO A:I B:I Y:O VDD:B VSS:B
MP9 Y net1 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP8 Y B net4 VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP7 net4 A VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP1 net1 B VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MP0 net1 A VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MN4 Y net1 net3 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN6 net2 A VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN5 net1 B net2 VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MN3 net3 B VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN2 net3 A VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_xor2_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_xor2_1 X A B VDD VSS
*.PININFO A:I B:I X:O VDD:B VSS:B
MX0 net1 A VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX4 X B net3 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX6 X net1 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX8 net3 A VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MX9 net1 B VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MX1 net6 A VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX2 net1 B net6 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MX3 net5 A VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX5 net5 B VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MX7 X net1 net5 VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_a22oi_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_a22oi_1 Y A1 A2 B1 B2 VDD VSS
*.PININFO A1:I A2:I B1:I B2:I Y:O VDD:B VSS:B
MN3 net1 B1 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MMNB0 Y B2 net1 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MMNA1 sndA1 A2 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MMNA0 Y A1 sndA1 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MP3 Y B1 pndA VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MMPB0 Y B2 pndA VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MMPA1 pndA A2 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MMPA0 pndA A1 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_sdfrbpq_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_sdfrbpq_2 Q CLK D RESET_B SCD SCE VDD VSS
*.PININFO CLK:I D:I RESET_B:I SCD:I SCE:I Q:O VDD:B VSS:B
MN22 Db SCD net63 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN21 Db D net65 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN19 SCEb SCE VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MN18 net63 SCE VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN17 net65 SCEb VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN23 Dbb Db VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN13 net12 net2 VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN14 net5 clkneg net12 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN15 net2 net5 net11 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN16 net11 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN6 Q net2 VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MN0 Dbbb Dbb net10 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN1 net10 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN7 Dbbb clkneg net6 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN8 net6 clkpos net9 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN9 net9 net4 net8 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN10 net8 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN11 net4 net6 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN2 clkneg CLK VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN12 net4 clkpos net5 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN3 clkpos clkneg VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MP22 net64 SCE VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP21 net62 SCEb VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP20 SCEb SCE VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MP18 Db SCD net62 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP17 Db D net64 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP23 Dbb Db VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP14 net5 clkpos net3 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP15 net2 net5 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP16 net2 RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP6 Q net2 VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MP7 Dbbb clkpos net6 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP0 Dbbb RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP1 Dbbb Dbb VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP8 net7 net4 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP9 net6 clkneg net7 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP10 net6 RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP2 clkneg CLK VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP3 clkpos clkneg VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP11 net4 net6 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP12 net4 clkneg net5 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP13 net3 net2 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_sdfrbpq_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_sdfrbpq_1 Q CLK D RESET_B SCD SCE VDD VSS
*.PININFO CLK:I D:I RESET_B:I SCD:I SCE:I Q:O VDD:B VSS:B
MN22 Db SCD net63 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN21 Db D net65 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN19 SCEb SCE VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MN18 net63 SCE VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN17 net65 SCEb VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN13 net12 net2 VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN14 net5 clkneg net12 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN15 net2 net5 net11 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN16 net11 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN6 Q net2 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN0 Dbbb Dbb net10 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN1 net10 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN7 Dbbb clkneg net6 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN8 net6 clkpos net9 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN9 net9 net4 net8 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN10 net8 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN11 net4 net6 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN2 clkneg CLK VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN12 net4 clkpos net5 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN3 clkpos clkneg VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN23 Dbb Db VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MP22 net64 SCE VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP21 net62 SCEb VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP20 SCEb SCE VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MP18 Db SCD net62 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP17 Db D net64 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP14 net5 clkpos net3 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP15 net2 net5 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP16 net2 RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP6 Q net2 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP7 Dbbb clkpos net6 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP0 Dbbb RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP1 Dbbb Dbb VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP8 net7 net4 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP9 net6 clkneg net7 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP10 net6 RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP2 clkneg CLK VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP3 clkpos clkneg VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP11 net4 net6 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP12 net4 clkneg net5 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP23 Dbb Db VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP13 net3 net2 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_sdfrbp_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_sdfrbp_2 Q Q_N CLK D RESET_B SCD SCE VDD VSS
*.PININFO CLK:I D:I RESET_B:I SCD:I SCE:I Q:O Q_N:O VDD:B VSS:B
MN22 Db SCD net63 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN21 Db D net65 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN19 SCEb SCE VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MN18 net63 SCE VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN17 net65 SCEb VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN23 Dbb Db VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN13 net12 net2 VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN14 net5 clkneg net12 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN15 net2 net5 net11 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN16 net11 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN6 Q_N net5 VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MN0 Dbbb Dbb net10 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN1 net10 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN7 Dbbb clkneg net6 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN8 net6 clkpos net9 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN9 net9 net4 net8 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN10 net8 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN11 net4 net6 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN2 clkneg CLK VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN12 net4 clkpos net5 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN3 clkpos clkneg VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN4 Q net1 VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MN5 net1 net5 VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MP22 net64 SCE VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP21 net62 SCEb VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP20 SCEb SCE VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MP18 Db SCD net62 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP17 Db D net64 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP23 Dbb Db VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP14 net5 clkpos net3 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP15 net2 net5 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP16 net2 RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP6 Q_N net5 VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MP7 Dbbb clkpos net6 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP0 Dbbb RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP1 Dbbb Dbb VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP8 net7 net4 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP9 net6 clkneg net7 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP10 net6 RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP2 clkneg CLK VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP3 clkpos clkneg VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP11 net4 net6 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP12 net4 clkneg net5 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP4 Q net1 VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MP13 net3 net2 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP5 net1 net5 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_sdfrbp_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_sdfrbp_1 Q Q_N CLK D RESET_B SCD SCE VDD VSS
*.PININFO CLK:I D:I RESET_B:I SCD:I SCE:I Q:O Q_N:O VDD:B VSS:B
MN22 Db SCD net63 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN21 Db D net65 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN19 SCEb SCE VSS VSS sg13_lv_nmos m=1 w=550.00n l=130.00n ng=1
MN18 net63 SCE VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN17 net65 SCEb VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN23 net13 Db VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN13 net12 net2 VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN14 net5 clkneg net12 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN15 net2 net5 net11 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN16 net11 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN6 Q_N net5 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN0 Dbb net13 net10 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN1 net10 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN7 Dbb clkneg net6 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN8 net6 clkpos net9 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN9 net9 net4 net8 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN10 net8 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN11 net4 net6 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN2 clkneg CLK VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN12 net4 clkpos net5 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN3 clkpos clkneg VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN4 Q net1 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN5 net1 net5 VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MP22 net64 SCE VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP21 net62 SCEb VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP20 SCEb SCE VDD VDD sg13_lv_pmos m=1 w=840.00n l=130.00n ng=1
MP18 Db SCD net62 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP17 Db D net64 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP23 net13 Db VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP14 net5 clkpos net3 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP15 net2 net5 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP16 net2 RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP6 Q_N net5 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP7 Dbb clkpos net6 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP0 Dbb RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP1 Dbb net13 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP8 net7 net4 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP9 net6 clkneg net7 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP10 net6 RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP2 clkneg CLK VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP3 clkpos clkneg VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP11 net4 net6 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP12 net4 clkneg net5 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP4 Q net1 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP13 net3 net2 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP5 net1 net5 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_dfrbpq_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_dfrbpq_2 Q CLK D RESET_B VDD VSS
*.PININFO CLK:I D:I RESET_B:I Q:O VDD:B VSS:B
MN13 net12 net2 VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN14 net5 clkneg net12 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN15 net2 net5 net11 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN16 net11 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN0 Db D net10 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN1 net10 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN7 Db clkneg net6 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN8 net6 clkpos net9 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN9 net9 net4 net8 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN10 net8 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN11 net4 net6 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN2 clkneg CLK VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN12 net4 clkpos net5 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN3 clkpos clkneg VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN4 Q net1 VSS VSS sg13_lv_nmos m=1 w=1.48u l=130.00n ng=2
MN5 net1 net5 VSS VSS sg13_lv_nmos m=1 w=640.00n l=130.00n ng=1
MP14 net5 clkpos net3 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP15 net2 net5 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP16 net2 RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP7 Db clkpos net6 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP0 Db RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP1 Db D VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP8 net7 net4 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP9 net6 clkneg net7 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP10 net6 RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP2 clkneg CLK VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP3 clkpos clkneg VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP11 net4 net6 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP12 net4 clkneg net5 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP4 Q net1 VDD VDD sg13_lv_pmos m=1 w=2.24u l=130.00n ng=2
MP13 net3 net2 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP5 net1 net5 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_dfrbpq_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_dfrbpq_1 Q CLK D RESET_B VDD VSS
*.PININFO CLK:I D:I RESET_B:I Q:O VDD:B VSS:B
MN13 net12 net2 VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN14 net5 clkneg net12 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN15 net2 net5 net11 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN16 net11 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN0 Db D net10 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN1 net10 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN7 Db clkneg net6 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN8 net6 clkpos net9 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN9 net9 net4 net8 VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN10 net8 RESET_B VSS VSS sg13_lv_nmos m=1 w=420.00n l=130.00n ng=1
MN11 net4 net6 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN2 clkneg CLK VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN12 net4 clkpos net5 VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN3 clkpos clkneg VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN4 Q net1 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MN5 net1 net5 VSS VSS sg13_lv_nmos m=1 w=740.00n l=130.00n ng=1
MP14 net5 clkpos net3 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP15 net2 net5 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP16 net2 RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP7 Db clkpos net6 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP0 Db RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP1 Db D VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP8 net7 net4 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP9 net6 clkneg net7 VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP10 net6 RESET_B VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP2 clkneg CLK VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP3 clkpos clkneg VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP11 net4 net6 VDD VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP12 net4 clkneg net5 VDD sg13_lv_pmos m=1 w=1.000u l=130.00n ng=1
MP4 Q net1 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
MP13 net3 net2 VDD VDD sg13_lv_pmos m=1 w=420.00n l=130.00n ng=1
MP5 net1 net5 VDD VDD sg13_lv_pmos m=1 w=1.12u l=130.00n ng=1
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_fill_1
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_fill_1 VDD VSS
*.PININFO VDD:B VSS:B
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_fill_2
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_fill_2 VDD VSS
*.PININFO VDD:B VSS:B
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_fill_4
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_fill_4 VDD VSS
*.PININFO VDD:B VSS:B
.ENDS

************************************************************************
* Library Name: sg13g2_stdcell
* Cell Name:    sg13g2_fill_8
* View Name:    schematic
************************************************************************

.SUBCKT sg13g2_fill_8 VDD VSS
*.PININFO VDD:B VSS:B
.ENDS
