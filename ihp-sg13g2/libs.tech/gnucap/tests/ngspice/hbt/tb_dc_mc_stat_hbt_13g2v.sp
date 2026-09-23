** adapted from:
** sch_path: ihp-sg13g2/libs.tech/xschem/sg13g2_tests/mc_hbt_13g2.sch
**.subckt mc_hbt_13g2v

.GLOBAL GND

Vce net3 GND 1.5
I0 GND net1 1u
Vc net3 net2 0
.save i(vc)
XQ1 net2 net1 GND GND npn13G2v Nx=1 El=2.5 mm_ok=1
**** begin user architecture code

.lib cornerHBT.lib hbt_typ_stat

.param temp=27
.param mc_ok = 1

.control
save all

let mc_runs = 1000
let run = 0

set curplot=new
set scratch=$curplot
setplot $scratch

* write mc trial index as first column
let run_vec = vector(mc_runs)
setscale run_vec

* allocate vectors for c current
let ic_vec = unitvec(mc_runs)

***************** LOOP *********************
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

  let ic_vec[run]= {$opplot}.I(Vc)

  destroy $opplot
  let run=run+1
end
***************** LOOP *********************

* write current vector to file
setplot $scratch
set wr_vecnames
set wr_singlescale
wrdata check/tb_dc_mc_stat_hbt_13g2v.sp.out ic_vec
.endc
.end
