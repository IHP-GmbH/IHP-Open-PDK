.LIB "cornerCAP.lib" cap_bcs
.GLOBAL GND

* cap_cmim
V1 in1 GND dc 0 ac 1
R1 out1 GND 100k
XC1 out1 in1 cap_cmim w=10.0u l=70.0u
* cap_rfcmim
V2 in2 GND dc 0 ac 1
R2 out2 GND 100k
XC2 out2 in2 GND cap_rfcmim w=10.0u l=70.0u

.control
set wr_vecnames
set wr_singlescale
* run ac
ac dec 1000 1e6 1e9
* output manitudes
let mag1=abs(out1)
let mag2=abs(out2)
* measure the -3 dB cutoff frequency
meas ac freq1_at when mag1 = 0.707
meas ac freq2_at when mag2 = 0.707
* approximate capacitance from cutoff frequency
let C1 = 1/(2*PI*freq1_at*1e+5)
let C2 = 1/(2*PI*freq2_at*1e+5)
print C1
print C2
wrdata check/tb_cap_cutoff_bcs.sp.out abs(out1) abs(out2)
.endc
.end

