# cap_cmomf: what the model contains and what it rests on

No value here is a silicon value for this process. Everything is EM simulation of the drawn PCell, the process specification, or publications on other processes. Replace them when test structures are measured.

| effect | value | evidence |
|---|---|---|
| shape | `C = dens (l - 2 rim)(w - 2 rim)` | Palace order 3, 13 cells |
| process corner | C x0.87 / x1.17, R x1.25 / x0.80, anti-correlated | process specification limits |
| series R | closed form in `cap_cmomf.va`, 1.71 ohm at 25 x 10 Metal2..4 | Palace with filled metal, one anchor |
| temperature on R | +3500 ppm/K | process specification |
| substrate | `k subscale (0.00277 A + 0.0595 P)` fF per plate, in series with 7 kohm | Palace, RC extraction, `cap_cmomi` EM |
| temperature on C | +30 ppm/K, an estimate | one measured plate device |
| dielectric loss | tan d = 1e-3 at `fref`, bracket 1e-4 to 1.2e-3 | no room-temperature oxide figure found |
| local mismatch | sigma(C)/C = 0.85 % / sqrt(C / fF), an upper bound | 32 nm silicon |
| series L | 0.4 pH per um of `l` | one point, only gives the device an SRF |

Left out on purpose:

- **Voltage coefficient:** about 0.1 ppm/V2, scaled from a measured plate device.
- **Skin effect:** skin depth 2.1 um against 0.49 um of metal, R flat to 0.02 %.
- **Distributed RC:** wRC = 5e-3 on a 25 x 10 device at 2.44 GHz.

## Capacitance shape

The outer rim of the drawn device holds feeds and bars, so C does not scale with drawn area. The fit covers every converged Palace point at order 3: five Metal2..4, three Metal3..4 and five Metal1..4.

| stack | `dens` fF/um2 | `rim` um | rms | max | area model max error |
|---|---:|---:|---:|---:|---:|
| Metal1..4 | 1.107 | 0.207 | 1.5 % | 2.5 % | +62 % |
| Metal2..4 | 0.852 | 0.193 | 2.6 % | 4.5 % | +43 % |
| Metal3..4 | 0.504 | 0.121 | 6.4 % | 8.0 % | +47 % |

Sample of the fitted points, l x w in um, C in fF:

| stack | size | Palace | area model | this model |
|---|---|---:|---:|---:|
| Metal2..4 | 25 x 10 | 202.46 | 228.75 (+13 %) | 201.62 (-0.4 %) |
| Metal2..4 | 5 x 2 | 6.42 | 9.15 (+43 %) | 6.34 (-1.2 %) |
| Metal2..4 | 5 x 2.8 | 9.81 | 12.81 (+31 %) | 9.49 (-3.3 %) |
| Metal2..4 | 40 x 2 | 52.07 | 73.20 (+41 %) | 54.47 (+4.6 %) |
| Metal2..4 | 40 x 2.8 | 81.27 | 102.48 (+26 %) | 81.48 (+0.3 %) |
| Metal3..4 | 2.44 x 2.4 | 2.43 | 3.57 (+47 %) | 2.39 (-1.6 %) |
| Metal3..4 | 40 x 2.6 | 43.70 | 63.44 (+45 %) | 47.25 (+8.1 %) |
| Metal1..4 | 40 x 2.6 | 95.33 | 133.85 (+40 %) | 95.79 (+0.5 %) |

- Metal3..4 is weak: three points, and the rim moves with aspect ratio. Use it with an 8 % error bar.
- Metal1..2, Metal1..3, Metal2..3 and single levels have no converged EM point. Their densities are RC extraction values divided by 0.97 and interpolated, with rim 0.20 um. The earlier 0.305 fF/um2 per level is 1.8x too high on a single level, because the first level has no inter-level term.
- Finger parity is not in this form. An even finger count puts both outer fingers on one net. Cells 2.4 um wide sit 7 to 14 % under the fit, about 0.19 fF per um of finger. It fades as 1/N, so it matters on narrow devices only. Adding it needs the PCell's finger count in the model.

## Corners

Process specification section 3.2 limits the line width, and a comb's gap is the drawn gap minus the width delta. Metal2..4 delta is -56 / -16 / +24 nm on a 0.21 um gap. With a lateral share of 0.75 of C (an estimate, bracket 0.65 to 0.85) and `C ~ 1/gap`:

| | min | target | max |
|---|---:|---:|---:|
| against drawn | -15.8 % | -5.3 % | +9.7 % |
| against target | -11.1 % | 0 | +15.8 % |

- **All EM here is of drawn geometry, so the densities sit about 5 % above what the target line width gives.** That bias is not folded in, because no biased solve or silicon confirms it yet.
- Adding metal thickness (assumed half of the sheet R spread, about +/-6 % on C) and permittivity (4.1 +/- 0.1, +/-2.4 %) in RSS gives C x0.87 and x1.17.
- R goes the other way, since narrow, thin metal raises R and lowers C. The pass/fail snake limits give R x1.25 at low C and x0.80 at high C.
- As in `ihp-sg13g2`, `cap_bcs` is low C and `cap_wcs` is high C.
- `cap_typ_stat` takes the limits as 3 sigma: sigma 4.5 %, one draw per die shared by all `cap_cmomf`, with R following as `cscale^-1.5`.

## Series R, L and dielectric loss

`cap_cmomf.va` sums spine, finger and via cut resistance per level and scales the result by 1.2355 to meet the filled-metal Palace figure of 1.71 ohm on a 25 x 10 Metal2..4 device.

- **There is one anchor.** All other sizes are extrapolation, and R depends on how the device is fed.
- The EM behind these numbers has a loss tangent of 0, so tan d is added by hand. On small devices tan d sets Q, not metal: about Q 900 against 10000 on the 2.44 x 2.4 cell, if 1e-3 holds.
- tan d has no good public number. TEOS oxide reads 1.2e-3 in a superconducting wiring study, a cryogenic figure. Patra et al. see dielectric loss dominate a 40 nm MoM above 15 GHz. 1e-3 is conservative.
- A constant tan d has no simple SPICE form. The model adds `tand / (2 pi fref C)` to the series R, correct at `fref` and too small below it, and it has no dielectric absorption.
- L = 0.4 pH/um reproduces 10 pH on a 25 um device. It moves C by 0.05 % at 2.44 GHz and only gives the device an SRF, about 110 GHz.

## Substrate

Per plate, with `A = l w` and `P = 2 (l + w)` in um, and `k` = 1.00, 0.80, 0.58 for `mmin` 1, 2, 3 and above.

- The form fits four Metal1..4 points within 8 %. Each of 0.80 and 0.58 rests on one point.
- `subscale` = 0.57 inside an array comes from one EM comparison of a plate alone and in a 2 x 4 array.
- `rsub` is borrowed. It is the series equivalent of EM results on `cap_cmomi` (5.4 to 9.8 kohm per plate). That is defensible because it is a property of the epi and substrate rather than of the comb, but `cap_cmomf` has no EM of its own for it yet.
- One branch per plate keeps the device symmetric, unlike `cap_cmomi`, which hangs its shunt on MINUS only.

## Temperature

Public evidence is thin, and none of it is for a comb in SiO2 at this node.

| source | structure | TC of C |
|---|---|---:|
| Geng et al., read off their Fig. 8 (9.281, 9.293, 9.303, 9.313 pF at -40, 25, 75, 125 C) | 0.25 um plate, measured | +21 ppm/K |
| Patra et al. (191 fF at 300 K, 197 fF at 4 K) | 40 nm comb in extra-low-k | -107 ppm/K, not used |

The last row has the opposite sign, so the coefficient belongs to the dielectric and does not transfer between processes. `tc1` = +30 ppm/K is the measured oxide value plus an allowance for a fringe device.

A ratio of two MoM combs cannot measure this, because a common coefficient cancels. A test structure needs a non-MoM reference.

## Voltage

Geng et al., Fig. 7, on the same plate device: 9.358, 9.3495 and 9.3505 pF at -10, 0, +10 V, so -40 ppm/V and +5.1 ppm/V2 on about 31 nm of oxide. A field effect scales with the square of the gap ratio, so at 0.21 um the quadratic term is about 0.1 ppm/V2. The linear term comes from an asymmetric stack, which a comb does not have.

## Mismatch

Tripathi and Murmann measured 1.2 % at 0.45 fF and 0.8 % at 1.2 fF on single-layer lateral-field caps in 32 nm, which gives 0.80 to 0.88 % x sqrt(fF). Omran et al. report that matching depends on capacitor area, not spacing. Only the abstracts were reachable, so whether the figure is for one capacitor or a pair is unconfirmed. 0.85 % is taken as an upper bound, since this process has much wider lines.

`cornerCAP.lib` enables it in the `*_mismatch` sections. Each instance draws its own deviate, gated by `mm_ok`, and `m` parallel devices average out.

## Using it

- `rfmodel=0` costs about 20 % more than the earlier model on 512 devices in a transient (4.4 s against 3.7 s, one run).
- Do not add hand-made series or substrate elements around a device with `rfmodel=1`, and do not rescale `l` or `w` to correct the earlier area model.

## Sources

- Geng, Do, Zeng, Boyland, [A Scalable RF Model of the Metal-Oxide-Metal (MOM) Capacitor](https://briefs.techconnect.org/wp-content/volumes/MSM2001/pdf/159.pdf), MSM 2001. Values read from the plots by eye.
- Patra et al., [Characterization and Analysis of On-Chip Microwave Passive Components at Cryogenic Temperatures](https://arxiv.org/pdf/1911.13084), 2019.
- Tripathi, Murmann, Mismatch Characterization of Small Metal Fringe Capacitors, IEEE TCAS-I, 2014. Abstract only.
- Omran, Alahmadi, Salama, [Matching Properties of Femtofarad and Sub-Femtofarad MOM Capacitors](https://academia.kaust.edu.sa/en/publications/matching-properties-of-femtofarad-and-sub-femtofarad-mom-capacito), IEEE TCAS-I, 2016. Abstract only.
- SG13CMOS5L process specification: sections 3.2, 3.6, metal TC and snake rows.
