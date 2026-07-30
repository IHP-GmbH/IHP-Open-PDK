* tb_cap_cmomi_typ -- ngspice cross-validation of the gnucap tb_cap_cmomi_typ.gc
*
* Copyright 2026 IHP PDK Authors
* Licensed under the Apache License, Version 2.0 (the "License").
*
* Same testbench as the gnucap tb_cap_cmomi_typ.gc: a high-pass R-C whose -3 dB
* corner f_3dB = 1/(2*pi*R*C) recovers the low-frequency capacitance of the MoM
* cap.  Running it here through ngspice -- cap_cmomi via the OSDI compiled from the
* SAME libs.tech/verilog-a/cap_cmomi/cap_cmomi.va source the gnucap plugin uses --
* cross-checks the two simulators against each other.
*   Device: 5 um x 5 um, Metal1..Metal5, feed = double.
*   Expected (matches the .gc): f_3dB ~ 78.24 MHz -> C ~ 20.34 fF.
*
* The cap_cmomi OSDI is loaded by the directory .spiceinit; cap_cmomi.lib (the
* 2-terminal wrapper subckt, which ties SUB to ground) is resolved through the
* model sourcepath set there.
.include "cap_cmomi.lib"

* high-pass R-C: V drives in1, cap in1 -> out1, R out1 -> ground
V1 in1 0 dc 0 ac 1
R1 out1 0 100k
XC1 out1 in1 cap_cmomi w=5.0u l=5.0u mmin=1 mmax=5 feed=double

.control
set wr_vecnames
set wr_singlescale
* run ac (matches the .gc: dec, 1000 pts/decade, 1 MHz .. 1 GHz)
ac dec 1000 1e6 1e9
* magnitude at the probe node
let mag1=abs(out1)
* measure the -3 dB cutoff frequency
meas ac freq1_at when mag1 = 0.707
* approximate capacitance from the cutoff frequency (R = 100k)
let C1 = 1/(2*PI*freq1_at*1e+5)
print C1
wrdata check/tb_cap_cmomi_typ.sp.out abs(out1)
.endc
.end
