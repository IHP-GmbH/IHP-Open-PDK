* NMOS Id-Vd

.LIB "cornerMOShv.lib" mos_tt

.option reltol=1e-4

vg 1 0 -1.2
vd 2 0 -1.2

X1 2 1 0 0 sg13_hv_pmos w=1.6u l=0.4u ng=4 rfmode=0

.control
set wr_vecnames
set wr_singlescale
dc vd 0.0 -1.2 -0.02 vg -0.2 -1.2 -0.2
wrdata check/tb_moshv_pmos_id_vd_ng4.sp.out v(1) i(vd)
.endc

.end

