# OpenRCX rules for SG13G2CMOS5L

`sg13cmos5l.{TYP,MIN,MAX}.rules` are the extraction rules files used
by `../config.tcl` for the nom/min/max STA corners. It replaces the earlier symlink to the SG13G2 rules (7
metal layers), which were wrong for CMOS5L: no Metal5 and no TopMetal2,
TopMetal1 sits directly on Metal4.

`sg13cmos5l.{TYP,MIN,MAX}.process` describe the CMOS5L stack from
`SG13CMOS5L_os_process_spec.pdf` Rev. 0.2, Fig. 1.1/1.2 (see also
`../../parasitics/itf/sg13cmos5l_typ.itf`). Metal1..Metal4 are identical
to SG13G2; TopMetal1 sits 0.85 um above Metal4 (bottom at ~5.16 um instead
of 6.16 um), followed by 1.5 um oxide and 0.4 um nitride passivation.

Regenerate the model with the shared flow
(`ihp-common/libs.tech/librelane/openrcx/README.md`):

```
./gen_rcx_model.sh sg13cmos5l.TYP.process
./gen_rcx_model.sh sg13cmos5l.MIN.process
./gen_rcx_model.sh sg13cmos5l.MAX.process
```
