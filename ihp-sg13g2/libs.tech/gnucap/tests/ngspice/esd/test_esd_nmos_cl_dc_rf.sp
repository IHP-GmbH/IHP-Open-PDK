* test_esd_nmos_cl_dc_rf.sp
* DC I-V sweep for the RF/NQS ESD NMOS clamps nmoscl_2 and nmoscl_4.
* Adapted from tests/gnucap/esd/test_esd_nmos_cl_dc.gc.

.LIB "cornerMOSlv.lib" mos_tt

I1   0  Vin1 1m
XD1  0  Vin1 nmoscl_2 m=1 l=0.36u w=168u rfmode=1

I2   0  Vin2 1m
XD2  0  Vin2 nmoscl_4 m=1 l=0.36u w=168u rfmode=1


.control

dc I1 -20m 20m 10u
dc I2 -20m 20m 10u

set wr_vecnames
set wr_singlescale
wrdata check/test_esd_nmos_cl_dc_rf.sp.out dc1.v(Vin1) dc2.v(Vin2)

.endc

.end
