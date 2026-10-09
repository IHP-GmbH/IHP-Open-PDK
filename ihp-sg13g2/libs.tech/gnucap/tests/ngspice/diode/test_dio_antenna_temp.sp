* test_dio_antenna_temp.sp
* DC at fixed bias current versus temperature for the sg13g2
* dantenna/dpantenna antenna-protection diodes.
* Originally emitted from:
*   ihp-sg13g2/libs.tech/xschem/sg13g2_tests/dc_diode_temp.sch

.include diodes.lib

I0 0 Vd  200n
XXD1 Vd   0 dantenna   l=780n w=780n
I1 0 Vdp 200n
XXD2 Vdp  0 dpantenna  l=780n w=780n

.temp 27

.control
save all
op
print v(Vd)
reset
dc temp -40 125 1
set wr_vecnames
set wr_singlescale
wrdata check/test_dio_antenna_temp.sp.out v(Vd) v(Vdp)
.endc

.end
