** test_svaricaphv_mc_mm_ac_tt.sp

.GLOBAL GND

V1 wb1 GND dc 1
V2 G1 GND ac 1
L1 W1 wb1 1m
V3 G2 GND dc 0
XC1 G1 W1 G2 GND sg13_hv_svaricap w=3.74u l=0.4u mm_ok=1

V4 wb2 GND dc 1
V5 G3 GND ac 1
L2 W2 wb2 1m
V6 G4 GND dc 0
XC2 G3 W2 G4 GND sg13_hv_svaricap w=3.74u l=0.4u mm_ok=1

.lib cornerMOShv.lib mos_tt_mismatch

.control
let mc_runs = 1000
let run = 0

set curplot=new
set scratch=$curplot
setplot $scratch
set wr_singlescale
set wr_vecnames
set appendwrite

dowhile run < mc_runs
  let seedval = run + 1
  setseed $&seedval
  mc_source

  ac lin 100 1GHz 100GHz

  let I1 = i(V3)
  let I2 = i(V6)
  let C1 = imag(I1) / (2 * pi * frequency)
  let C2 = imag(I2) / (2 * pi * frequency)
  wrdata check/test_svaricaphv_mc_mm_ac_tt.sp.out C1 C2

  set acplot = $curplot
  setplot $scratch
  destroy $acplot
  let run = run + 1
end
.endc

.end
