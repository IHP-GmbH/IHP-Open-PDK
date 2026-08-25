.LIB "cornerRES.lib" res_bcs

* TODO: verify current source direction and make consistent with idc.va
Ir1 0 n1 1m
Ir2 0 n2 1m
Ir3 0 n3 1m

XR1 n1 0 0 rsil l=0.5u w=0.5u
XR2 n2 0 0 rppd l=0.5u w=0.5u
XR3 n3 0 0 rhigh l=0.96u w=0.5u
* TODO: res_rpara is missing in cornerRES.lib
* XR4 n4 0 Rparasitic R=100

.control
op
print v(n1) v(n2) v(n3) > check/tb_res_basic_bcs.sp.out
.endc
.end

