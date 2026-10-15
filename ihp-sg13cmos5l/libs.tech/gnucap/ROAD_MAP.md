# Port Device library to Verilog-A

Status for the SG13CMOS5L device set. Devices SG13G2 has but this PDK does not
(`cap_cmim`, `cap_rfcmim`, `cparasitic`, the `npn13G2*` HBTs, `schottky_nbl1`,
`isolbox`, inductors) are out of scope and not listed.

Checked here means the Verilog-A model exists, which is not the same as being
tested: `ptap1` and `ntap1` have paramsets that no testbench instantiates, and
`Rparasitic` is exercised on the Gnucap side only. Both are inherited from
SG13G2.

- [x] resistors
    - [x] parasitic
    - [x] rsil
    - [x] rhigh
    - [x] rppd
    - [x] ptap1
    - [x] ntap1

- [x] mosfets
    - [x] moslv (including rfmode)
    - [x] moshv (including rfmode)

- [ ] capacitors
    - [x] cap_cmomi
    - [x] cap_cmomf
    - [ ] moscap_n / moscap_p

- [ ] diode
    - [ ] dantenna
    - [ ] dpantenna

- [ ] esd
    - [ ] diodevdd_2kv / diodevdd_4kv
    - [ ] diodevss_2kv / diodevss_4kv
    - [ ] nmoscl_2 / nmoscl_4

- [ ] pnpMPA

- [ ] svaricap

- [ ] bondpad

## Notes

The two MoM capacitors are the only entries here that could not be taken from
SG13G2 unchanged, and for different reasons.

Both PDKs call the interdigitated device `cap_cmomi` and its Verilog-A module
interface is identical, but SG13CMOS5L builds it on Metal1..Metal4 rather than
Metal1..Metal5, so `mmin`/`mmax` are bounded to `[1:4]` and the `Nlay = 5`
coefficient branch is dropped. For `Nlay <= 4` the coefficients are the same
SG13G2-characterised values, transferred by layer count.

`cap_cmomf` is simpler: SG13G2 has no such device, so there is no upstream file
to reuse and no reference to compare against. Its paramset is 2-terminal and has
no `feed`, matching the module.

So `models/capacitor_paramset.va` is a real file here rather than a symlink,
carrying the `cmomi` and `cmomf` paramsets, since this PDK has none of the other
capacitors SG13G2's version covers. The reference data had to be regenerated
too. For `cap_cmomi` the testbench instantiates `mmax=4` where SG13G2 uses 5,
and since the row-count correction the models differ as well: this PDK bills
`floor(w/0.89)` coupled rows while the SG13G2 twin still subtracts one (until its
own fix lands). The measured cutoff for `mmax=4` is about 75.4 MHz. For
`cap_cmomf` there was never anything to regenerate from. Both live under
`tests/{gnucap,ngspice}/capacitor`, and the Ngspice `.spiceinit` there is a real
file because the shared one loads only `cap_cmomi.osdi`.

Everything else on the unchecked list is also unported in SG13G2, so those gaps
are inherited rather than introduced by the SG13CMOS5L port.

## TODOs

Inherited from the SG13G2 road map:

- test setting multiplicity via $mfactor during device instantiation
- decide which resistor, capacitor, inductor primitives to use
- improve performance of ngspice mc tests
- build a pipeline that compiles devices to osdi
