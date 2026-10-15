** adapted from:
** sch_path: ihp-sg13g2/libs.tech/xschem/sg13g2_tests/tran_moscap_n.sch
**.subckt tran_moscap_n

* add 10 ns delay to align transient initialization with Gnucap
V1 P GND pwl 0 -1.2 10n -1.2 410n 1.2
XC1 P GND sg13_moscap_n w=1.0u l=1.0u m=1 mm_ok=0

**** begin user architecture code

.lib cornerMOSCAP.lib moscap_tt

* use Gear integration to suppress ringing
.options method=gear

.param  TEMP = 27
.control
  save all
  tran 0.1n 410n
  let dvdt = deriv(v(p))
  * floor dvdt to avoid 0/0 during initial hold
  let Cn_abs = abs(i(v1)) / max(abs(dvdt), 1e1)
  meas tran C_max MAX Cn_abs
  meas tran C_min MIN Cn_abs from=10n to=400n
  meas tran t_c_min MIN_AT Cn_abs from=10n to=400n
  meas tran V_th FIND v(p) AT=t_c_min
  let Cn_norm = Cn_abs / C_max
  set wr_vecnames
  set wr_singlescale
  wrdata check/test_moscap_nmos_tran.sp.out v(p) i(V1) Cn_abs
.endc

**** end user architecture code
**.ends
.GLOBAL GND
.end
