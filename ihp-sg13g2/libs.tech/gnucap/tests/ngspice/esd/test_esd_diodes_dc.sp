* test_esd_diode_dc.sp: DC I-V sweep across the four sg13g2 ESD clamp diodes
* Adopted from: ihp-sg13g2/libs.tech/xschem/sg13g2_tests/dc_esd_diodes.sch

.include sg13g2_esd.lib

* diodevdd_2kv
V1     Vin  0 0.7
Vmda1  Vin  net1 0
Vmda2  Vin  net2 0
XD1    0    net1 net2 diodevdd_2kv m=1

* diodevdd_4kv
Vmda3 Vin  net3 0
Vmda4 Vin  net4 0
XD2   0    net3 net4 diodevdd_4kv m=1

* diodevss_2kv
Vmda5 net5 0    0
Vmda6 net6 0    0
XD4   net5 net6 Vin diodevss_2kv m=1

* diodevss_4kv
Vmda7 net7 0   0
Vmda8 net8 0   0
XD5   net7 net8 Vin diodevss_4kv m=1

.control

save all

dc V1 -20.7 3 1m

set wr_vecnames
set wr_singlescale
wrdata check/test_esd_diodes_dc.sp.out v(Vin) i(Vmda1) i(Vmda2) i(Vmda3) i(Vmda4) i(Vmda5) i(Vmda6) i(Vmda7) i(Vmda8)

.endc

.end
