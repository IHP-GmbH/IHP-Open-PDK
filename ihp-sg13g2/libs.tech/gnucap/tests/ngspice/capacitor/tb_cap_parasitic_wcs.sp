.LIB "cornerCAP.lib" cap_wcs
.GLOBAL GND

* cap_parasitic
VSTEP vsrc 0 DC 0 PULSE(0 1 10n 100p 100p 0.5u 1u)
XC1 n1 gnd  cparasitic c=100f
XC2 n2 gnd  cparasitic c=5p
XC3 n3 gnd  cparasitic c=10p
R1 vsrc n1 10k
R2 vsrc n2 10k
R3 vsrc n3 10k

.control

tran 0.1n 2u

set wr_vecnames
set wr_singlescale
wrdata check/tb_cap_parasitic_wcs.sp.out v(vsrc) v(n1) v(n2) v(n3)

* Measure vpulse input edge at 50% of the 1V step
meas tran t0 WHEN V(vsrc)=0.5 RISE=1
* Measure capacitor 63.2% voltage crossings for RC time constant
meas tran t1 WHEN V(n1)=0.632 RISE=1
meas tran t2 WHEN V(n2)=0.632 RISE=1
meas tran t3 WHEN V(n3)=0.632 RISE=1
* Extract RC time constants relative to pulse edge
let tau1 = t1 - t0
let tau2 = t2 - t0
let tau3 = t3 - t0
* Extract capacitance from C = tau / R
let C1 = tau1 / 10k
let C2 = tau2 / 10k
let C3 = tau3 / 10k
print C1 C2 C3 >> check/tb_cap_parasitic_wcs.sp.out
.endc
.end
