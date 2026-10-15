* test_esd_nmos_cl_dc.sp
* DC I-V sweep for the sg13g2 ESD NMOS clamp devices nmoscl_2 and nmoscl_4.
* Adopted from:
* ihp-sg13g2/libs.tech/xschem/sg13g2_tests/dc_esd_nmos_cl.sch

.LIB "cornerMOSlv.lib" mos_tt

I1   0  Vin1 1m
XD1  0  Vin1 nmoscl_2 m=1

I2   0  Vin2 1m
XD2  0  Vin2 nmoscl_4 m=1


.control

dc I1 -20m 20m 10u
dc I2 -20m 20m 10u

set wr_vecnames
set wr_singlescale
wrdata check/test_esd_nmos_cl_dc.sp.out dc1.v(Vin1) dc2.v(Vin2)

.endc

.end
