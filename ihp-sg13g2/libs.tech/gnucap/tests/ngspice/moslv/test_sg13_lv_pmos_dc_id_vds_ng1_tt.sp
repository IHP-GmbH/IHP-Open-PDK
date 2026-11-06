* NMOS Id-Vd

.LIB "cornerMOSlv.lib" mos_tt

.option reltol=1e-4

vg 1 0 -1.2
vd 2 0 -1.2

X1 2 1 0 0 sg13_lv_pmos w=0.3u l=0.34u ng=1 rfmode=0

.control
set wr_vecnames
set wr_singlescale
dc vd 0.0 -1.2 -0.02 vg -0.2 -1.2 -0.2
wrdata check/test_sg13_lv_pmos_dc_id_vds_ng1_tt.sp.out v(1) i(vd)
.endc

.end
