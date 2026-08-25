* CMOS inverter

.LIB "cornerMOSlv.lib" mos_fs

.option reltol=1e-4

VDD vdd 0 1.2
VIN in 0 1.2

X1 out in vdd vdd sg13_lv_pmos w=0.28u l=0.34u rfmode=1
X2 out in 0 0 sg13_lv_nmos w=0.35u l=0.34u rfmode=1

.control
set wr_vecnames
set wr_singlescale
dc VIN 0.0 1.2 0.02
wrdata check/tb_moslv_inv_fs_rf.sp.out v(out) i(VDD)
.endc
.end
