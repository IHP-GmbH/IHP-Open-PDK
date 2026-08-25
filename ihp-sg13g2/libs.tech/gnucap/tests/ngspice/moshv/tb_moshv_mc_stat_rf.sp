.LIB "cornerMOShv.lib" mos_tt_stat
.GLOBAL GND

*nmos
I1 GND Vgs1 10u
I2 GND Vgs2 10u
XM1 Vgs1 Vgs1 GND GND sg13_hv_nmos w=1.0u l=0.45u ng=1 rfmode=1
XM2 Vgs2 Vgs2 GND GND sg13_hv_nmos w=1.0u l=0.45u ng=1 rfmode=1
*pmos
I3 GND Vgs3 -10u
I4 GND Vgs4 -10u
XM3 Vgs3 Vgs3 GND GND sg13_hv_pmos w=1.0u l=0.4u ng=1 rfmode=1
XM4 Vgs4 Vgs4 GND GND sg13_hv_pmos w=1.0u l=0.4u ng=1 rfmode=1

.control

let mc_runs = 1000
let run = 0

* create storage plot
set curplot=new
set scratch=$curplot
setplot $scratch
* write mc trial index as first column
let run_vec = vector(mc_runs)
setscale run_vec

* allocate vectors for gate-source voltages
let vgs1_vec = 0 * unitvec(mc_runs)
let vgs2_vec = 0 * unitvec(mc_runs)
let vgs3_vec = 0 * unitvec(mc_runs)
let vgs4_vec = 0 * unitvec(mc_runs)

* mc loop
dowhile run < mc_runs
  * set seed for stable ref files
  let seed = run + 1
  setseed $&seed
  * reload circuit with trial seed
  mc_source
  * run op analysis, this creates and activates a new plot
  op
  * remember current op plot, then switch to storage plot
  set opplot = $curplot
  setplot $scratch
  * write gate voltages to vectors
  let vgs1_vec[run] = {$opplot}.v(Vgs1)
  let vgs2_vec[run] = {$opplot}.v(Vgs2)
  let vgs3_vec[run] = {$opplot}.v(Vgs3)
  let vgs4_vec[run] = {$opplot}.v(Vgs4)

  destroy $opplot
  let run=run+1
end
* write voltage vectors to file
set wr_vecnames
set wr_singlescale
wrdata check/tb_moshv_mc_stat_rf.sp.out vgs1_vec vgs2_vec vgs3_vec vgs4_vec
.endc
.end
