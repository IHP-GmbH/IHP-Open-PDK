* test_dio_antenna_dc.sp
* DC operating point and forward/reverse I-V sweep for the sg13g2
* dantenna/dpantenna antenna-protection diodes.
* Originally emitted from:
*   ihp-sg13g2/libs.tech/xschem/sg13g2_tests/dc_diode_op.sch

.include diodes.lib

V1 net1 0 0.7
Vmda net1 net2 0
Vmdp net1 net3 0
XD2 net2 0 dantenna  l=0.78u w=0.78u
XD1 net3 0 dpantenna l=0.78u w=0.78u

.temp 27

.control
save all
op
print I(Vmda) I(Vmdp)
reset
dc V1 -12 1 1m
set wr_vecnames
set wr_singlescale
wrdata check/test_dio_antenna_dc.sp.out i(Vmda) i(Vmdp)
.endc

.end
