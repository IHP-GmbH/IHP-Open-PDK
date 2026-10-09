** test_svaricaphv_ac_fs.sp
** adapted from:
** sch_path: ihp-sg13g2/libs.tech/xschem/sg13g2_tests/ac_svaricap_test.sch

.GLOBAL GND

V1 wb GND dc 1
V2 G1 GND ac 1
L3 W wb 1m
V3 G2 GND dc 0

XC1 G1 W G2 GND sg13_hv_svaricap w=3.74u l=0.3u

.lib cornerMOShv.lib mos_fs

.control
  save all

  ac lin 100 1GHz 100GHz

  let I1 = i(V3)
  let Ctot = imag(I1) / (2 * pi * frequency)

  set wr_vecnames
  set wr_singlescale
  wrdata check/test_svaricaphv_ac_fs.sp.out I1 Ctot
.endc

.end
