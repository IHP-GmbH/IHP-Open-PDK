.LIB "cornerCAP.lib" cap_bcs_mismatch
.GLOBAL GND

* instantiate two cmim capacitors to measure mismatch across mc trials
V1 in1 GND dc 0 ac 1
R1 out1 GND 100k
XC1 out1 in1 cap_cmim w=10.0e-6 l=70.0e-6 mm_ok=1
V2 in2 GND dc 0 ac 1
R2 out2 GND 100k
XC2 out2 in2 cap_cmim w=10.0e-6 l=70.0e-6 mm_ok=1

* run mc ac simulation
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

* allocate vectors for capacitance values
let C1_vec = 0 * unitvec(mc_runs)
let C2_vec = 0 * unitvec(mc_runs)

* mc loop
dowhile run < mc_runs
  * set seed for stable ref files
  let seed = run + 1
  setseed $&seed
  mc_source

  * run ac analysis, this creates and activates a new plot
  ac dec 1000 1e6 1e9
  * measure cutoff freq
  let mag1 = abs(v(out1))
  let mag2 = abs(v(out2))
  meas ac fcut1 when mag1 = 0.707 rise=1
  meas ac fcut2 when mag2 = 0.707 rise=1
  * approximate capacitance from cutoff freq
  let C1 = 1/(2*pi*fcut1*1e5)
  let C2 = 1/(2*pi*fcut2*1e5)

  * remember current ac plot, then switch to storage plot
  set acplot = $curplot
  setplot $scratch

  let C1_vec[run] = {$acplot}.C1
  let C2_vec[run] = {$acplot}.C2

  destroy $acplot
  let run = run + 1
end

* write capacitance vectors to file
setplot $scratch
set wr_vecnames
set wr_singlescale
wrdata check/tb_cap_cutoff_mc_mm_bcs.sp.out C1_vec C2_vec
.endc
.end
