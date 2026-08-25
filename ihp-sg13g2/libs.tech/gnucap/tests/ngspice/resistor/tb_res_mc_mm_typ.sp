.LIB "cornerRES.lib" res_typ_mismatch

* instantiate current sources
* TODO: verify current source direction and make consistent with idc.va
Ir1 0 n1 1m
Ir2 0 n2 1m
Ir3 0 n3 1m
Ir4 0 n4 1m
Ir5 0 n5 1m
Ir6 0 n6 1m
* instantiate resistor pairs to measure mismatch across mc trials
XR1 n1 0 0 rsil l=0.5u w=0.5u mm_ok=1
XR2 n2 0 0 rsil l=0.5u w=0.5u mm_ok=1
XR3 n3 0 0 rhigh l=0.96u w=0.5u mm_ok=1
XR4 n4 0 0 rhigh l=0.96u w=0.5u mm_ok=1
XR5 n5 0 0 rppd  l=0.5u w=0.5u mm_ok=1
XR6 n6 0 0 rppd  l=0.5u w=0.5u mm_ok=1

* run mc op simulation
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

* allocate vectors for voltage across resistors
let v1_vec = 0 * unitvec(mc_runs)
let v2_vec = 0 * unitvec(mc_runs)
let v3_vec = 0 * unitvec(mc_runs)
let v4_vec = 0 * unitvec(mc_runs)
let v5_vec = 0 * unitvec(mc_runs)
let v6_vec = 0 * unitvec(mc_runs)

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
  * write voltages into vectors
  let v1_vec[run] = {$opplot}.v(n1)
  let v2_vec[run] = {$opplot}.v(n2)
  let v3_vec[run] = {$opplot}.v(n3)
  let v4_vec[run] = {$opplot}.v(n4)
  let v5_vec[run] = {$opplot}.v(n5)
  let v6_vec[run] = {$opplot}.v(n6)

  destroy $opplot
  let run = run + 1
end

* write voltage vectors to file
set wr_vecnames
set wr_singlescale
wrdata check/tb_res_mc_mm_typ.sp.out v1_vec v2_vec v3_vec v4_vec v5_vec v6_vec
.endc
.end
