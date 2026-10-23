** test_svaricaphv_mc_stat_ac.sp

.GLOBAL GND

V1 wb GND dc 1
V2 G1 GND ac 1
L3 W wb 1m
V3 G2 GND dc 0

XC1 G1 W G2 GND sg13_hv_svaricap w=3.74u l=0.3u mm_ok=0

.lib cornerMOShv.lib mos_tt_stat

.control
let mc_runs = 100
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

  ac lin 100 1G 100G

  let I1 = i(V3)
  let Ctot = imag(I1) / (2 * pi * frequency)
  let sv = run + 1

  set acplot = $curplot
  setplot $acplot
  wrdata check/test_svaricaphv_mc_stat_ac.sp.out Ctot

  setplot $scratch
  destroy $acplot
  let run = run + 1
end

setplot $scratch
.endc

.end
