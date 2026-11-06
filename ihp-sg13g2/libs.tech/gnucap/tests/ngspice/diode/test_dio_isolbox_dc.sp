* test_dio_isolbox_dc.sp
* DC I-V sweep for the sg13g2 isolbox (sub-NWell isolation junction)
* at fixed width and length.
* Originally emitted from:
*   ihp-sg13g2/libs.tech/xschem/sg13g2_tests/dc_isolbox.sch

.include diodes.lib

I0 0 isosub_net 1m
XD1 isosub_net nwell_net 0 isolbox l=3.0u w=3.0u

.temp 27

.control
save all
dc I0 -1m 1m 1u
echo Evaluating breakdown voltages:
meas dc vbk_pos find v(isosub_net) at=1u
meas dc vbk_neg find v(isosub_net) at=-1u
set wr_vecnames
set wr_singlescale
wrdata check/test_dio_isolbox_dc.sp.out v(isosub_net)
.endc

.end
