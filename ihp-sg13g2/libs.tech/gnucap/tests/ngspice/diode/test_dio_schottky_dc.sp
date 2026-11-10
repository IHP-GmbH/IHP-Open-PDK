* test_dio_schottky_dc.sp
* DC I-V sweep for the sg13g2 schottky_nbl1 Schottky diode using the
* typical (tt) corner from cornerDIO.lib.
* Originally emitted from:
*   ihp-sg13g2/libs.tech/xschem/sg13g2_tests/dc_schottky.sch

.LIB "cornerDIO.lib" dio_tt

I0  0 net1 1m
XD1 0 net1 sub! schottky_nbl1 Nx=1 Ny=1
V1 sub! 0 0

.temp 27

.control
save all
dc I0 -1m 1m 1u
echo Evaluating breakdown voltages:
meas dc vbk_pos find v(net1) at=10u
meas dc vbk_neg find v(net1) at=-10u
set wr_vecnames
set wr_singlescale
wrdata check/test_dio_schottky_dc.sp.out v(net1)
.endc

.end
