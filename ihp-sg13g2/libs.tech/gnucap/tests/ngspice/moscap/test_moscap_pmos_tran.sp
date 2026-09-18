** adopted from;
** sch_path: ihp-sg13g2/libs.tech/xschem/sg13g2_tests/tran_moscap_p.sch
**.subckt tran_moscap_p
V1 M GND pwl 0 0 10n 0 410n 2.4
XC1 M VDD sg13_moscap_p w=1u l=1u m=1 mm_ok=0
V2 VDD GND DC 1.2
**** begin user architecture code

.lib cornerMOSCAP.lib moscap_tt

.param  TEMP = 27
.control
  save all
  tran 0.1n 410n
  let dvdt = deriv(v(m))
  let vcap = v(m)-v(vdd)
  let Cp_abs = abs(i(v1)) / max(abs(dvdt), 1e1)
  meas tran C_max MAX Cp_abs
  meas tran C_min MIN Cp_abs from=5n to=400n
  meas tran t_c_min MIN_AT Cp_abs from=5n to=400n
  meas tran V_th FIND vcap AT=t_c_min
  set wr_vecnames
  set wr_singlescale
  wrdata check/test_moscap_pmos_tran.sp.out v(m) i(V1) Cp_abs
.endc

**** end user architecture code
**.ends
.GLOBAL GND
.end
