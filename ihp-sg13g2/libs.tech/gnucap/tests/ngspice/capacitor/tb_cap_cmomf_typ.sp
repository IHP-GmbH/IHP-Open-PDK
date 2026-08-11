* tb_cap_cmomf_typ -- ngspice cross-validation of the gnucap tb_cap_cmomf_typ.gc
*
* Copyright 2026 IHP PDK Authors
* Licensed under the Apache License, Version 2.0 (the "License").
*
* Same testbench as the gnucap tb_cap_cmomf_typ.gc: a high-pass R-C whose -3 dB
* corner f_3dB = 1/(2*pi*R*C) recovers the low-frequency capacitance of the
* metal fringe MoM cap.  Running it here through ngspice cross-checks the two
* simulators against each other on the same device.
*   Device: 5 um x 5 um, Metal1..Metal5.
*
* Same geometry as tb_cap_cmomi_typ.sp on purpose, so the two are directly
* comparable.  The fringe cap is the denser of the pair here, 1.592 fF/um2
* against 1.36.
*
* The cap_cmomf OSDI is loaded by the directory .spiceinit; cap_cmomf.lib (the
* 2-terminal wrapper subckt) is resolved through the model sourcepath set
* there.  Build the OSDI with libs.tech/verilog-a/openvaf-compile-va.sh.
.include "cap_cmomf.lib"

* high-pass R-C: V drives in1, cap in1 -> out1, R out1 -> ground
V1 in1 0 dc 0 ac 1
R1 out1 0 100k
XC1 out1 in1 cap_cmomf w=5.0u l=5.0u mmin=1 mmax=5

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
wrdata check/tb_cap_cmomf_typ.sp.out abs(out1)
.endc
.end
