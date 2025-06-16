v {xschem version=3.4.7 file_version=1.2
* Copyright 2023 IHP PDK Authors
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     https://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.

}
G {}
K {}
V {}
S {}
E {}
L 7 360 -730 360 -60 {}
L 7 700 -730 700 -60 {}
L 7 1040 -730 1040 -60 {}
L 7 1380 -730 1380 -60 {}
L 7 20 -730 20 -60 {}
L 7 1750 -730 1750 -60 {}
L 7 2140 -730 2140 -60 {}
T {DC} 40 -710 0 0 0.8 0.8 {}
T {Transient} 380 -710 0 0 0.8 0.8 {}
T {AC} 730 -710 0 0 0.8 0.8 {}
T {Monte Carlo} 1060 -710 0 0 0.8 0.8 {}
T {S-param} 1440 -710 0 0 0.8 0.8 {}
T {Tools} 1800 -710 0 0 0.8 0.8 {}
C {devices/title.sym} 160 -30 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} 90 -780 0 0 {name=h1
descr="IHP-Open-PDK"
url="https://github.com/IHP-GmbH/IHP-Open-PDK/tree/main"}
C {sg13g2_tests/dc_hv_nmos.sym} 180 -600 0 0 {name=x6}
C {sg13g2_tests/dc_lv_pmos.sym} 180 -570 0 0 {name=x7}
C {sg13g2_tests/dc_hv_pmos.sym} 180 -540 0 0 {name=x8}
C {sg13g2_tests/dc_mos_temp.sym} 180 -510 0 0 {name=x11}
C {sg13g2_tests/dc_mos_cs_temp.sym} 180 -480 0 0 {name=x12}
C {sg13g2_tests/dc_res_temp.sym} 180 -440 0 0 {name=x13}
C {sg13g2_tests/dc_diode_op.sym} 180 -320 0 0 {name=x14}
C {sg13g2_tests/dc_diode_temp.sym} 180 -290 0 0 {name=x15}
C {sg13g2_tests/dc_hbt_13g2.sym} 180 -260 0 0 {name=x17}
C {sg13g2_tests/tran_mim_cap.sym} 520 -630 0 0 {name=x10}
C {sg13g2_tests/ac_lv_nmosrf.sym} 860 -630 0 0 {name=x9}
C {sg13g2_tests/ac_mim_cap.sym} 860 -590 0 0 {name=x21}
C {sg13g2_tests/mc_lv_nmos_cs_loop.sym} 1200 -630 0 0 {name=x1}
C {sg13g2_tests/mc_hv_nmos_cs_loop.sym} 1200 -590 0 0 {name=x2}
C {sg13g2_tests/mc_lv_pmos_cs_loop.sym} 1200 -550 0 0 {name=x3}
C {sg13g2_tests/mc_hv_pmos_cs_loop.sym} 1200 -510 0 0 {name=x4}
C {sg13g2_tests/mc_res_op.sym} 1200 -440 0 0 {name=x16}
C {sg13g2_tests/mc_hbt_13g2.sym} 1200 -380 0 0 {name=x18}
C {sg13g2_tests/mc_hbt_13g2_ac.sym} 1200 -350 0 0 {name=x19}
C {sg13g2_tests/mc_mim_cap_ac.sym} 1200 -300 0 0 {name=x24}
C {sg13g2_tests/sp_mim_cap.sym} 1560 -630 0 0 {name=x20}
C {sg13g2_tests/sp_parasitic_cap.sym} 1560 -590 0 0 {name=x22}
C {sg13g2_tests/sp_rfmim_cap.sym} 1560 -550 0 0 {name=x23}
C {sg13g2_tests/dc_ntap1.sym} 180 -400 0 0 {name=x25}
C {sg13g2_tests/dc_ptap1.sym} 180 -360 0 0 {name=x26}
C {sg13g2_tests/tran_logic_not.sym} 520 -590 0 0 {name=x27}
C {sg13g2_tests/dc_logic_not.sym} 180 -190 0 0 {name=x28}
C {sg13g2_tests/tran_logic_nand.sym} 520 -550 0 0 {name=x29}
C {sg13g2_tests/dc_pnpMPA.sym} 180 -230 0 0 {name=x30}
C {sg13g2_tests/dc_lv_nmos.sym} 180 -630 0 0 {name=x5}
C {sg13g2_tests/tran_bondpad.sym} 520 -510 0 0 {name=x31}
C {sg13g2_tests/dc_esd_diodes.sym} 180 -150 0 0 {name=x31}
C {sg13g2_tests/dc_esd_nmos_cl.sym} 180 -110 0 0 {name=x32}
C {sg13g2_tests/inv_mc_tb.sym} 1930 -630 0 0 {name=x33}
C {sg13g2_tests/inv_sweep_tb.sym} 1930 -590 0 0 {name=x34}
