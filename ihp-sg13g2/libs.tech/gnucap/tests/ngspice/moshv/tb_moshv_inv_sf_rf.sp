* CMOS inverter

.LIB "cornerMOShv.lib" mos_sf

.option reltol=1e-4

VDD vdd 0 1.2
VIN in 0 1.2

X1 out in vdd vdd sg13_hv_pmos w=2.0u l=0.4u rfmode=1
X2 out in 0 0 sg13_hv_nmos w=1.0u l=0.45u rfmode=1

.control
set wr_vecnames
set wr_singlescale
dc VIN 0.0 1.2 0.02
wrdata check/tb_moshv_inv_sf_rf.sp.out v(out) i(VDD)
.endc
.end
