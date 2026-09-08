** adapted from:
** sch_path: ihp-sg13g2/libs.tech/xschem/sg13g2_tests/dc_hbt_13g2.sch
**.subckt dc_hbt_13g2
Vce net3 GND 1.5
I0 GND net_ib 1u
Vb net_ib net1 0
Vc net3 net2 0
XQ1 net2 net1 GND GND npn13G2 Nx=1 mm_ok=1
**** begin user architecture code

.lib cornerHBT.lib hbt_bcs

.options savecurrents
.param temp=27
.control
op
dc Vce 0.01 1.5 0.01 I0 0.5u 5u 0.5u
set wr_vecnames
set wr_singlescale
wrdata check/tb_dc_hbt_13g2_bcs.sp.out i(vb) i(vc)
.endc

**** end user architecture code
**.ends
.GLOBAL GND
.end
