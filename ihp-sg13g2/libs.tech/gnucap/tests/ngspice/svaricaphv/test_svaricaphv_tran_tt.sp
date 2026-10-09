** test_svaricaphv_tran_tt.sp
** adapted from:
** sch_path: ihp-sg13g2/libs.tech/xschem/sg13g2_tests/tran_svaricap_test.sch

.GLOBAL GND

XC1 net2 GND net1 sub! sg13_hv_svaricap w=3.74u l=0.3u Nx=1 mm_ok=1
V1 net1 GND pulse(-2.5, 2.5, 1u, 10u, 100p)
V2 net2 GND pulse(-2.5, 2.5, 1u, 10u, 100p)

.lib cornerMOShv.lib mos_tt

* use Gear integration to suppress ringing
.options method=gear

.control

save all

tran 1n 11u

set wr_vecnames
set wr_singlescale
wrdata check/test_svaricaphv_tran_tt.sp.out v(net1) i(V1)

.endc
.end
