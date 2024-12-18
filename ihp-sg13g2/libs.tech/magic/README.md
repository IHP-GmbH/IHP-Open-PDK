# IHP SG13G2 Open PDK technology files

for use with the Magic VLSI
layout tool and netgen LVS tool

## Notes and guidelines

**Installation**:

The tech files for magic are integrated into the IHP Open PDK
and will be installed where the PDK is installed.  The location
of the top level directory (for this repository, IHP-Open-PDK)
is represented by the shell environment variable `$PDK_ROOT`.  For
the purposes of this document, the location of the IHP Open PDK
will be assumed to be `$PDK_ROOT`.

**Requirements**:

There is a minimum version of magic required to run correctly
with the IHP Open PDK.  This minimum version is stated in the
tech file (`ihp-sg13g2.tech`) in the "version" section.  As of the
beta pre-release of magic/netgen support for IHP SG13G2, the
minimum required version of magic is 8.3.506.  Earlier versions
of magic can be used by commenting out the "requires" line from
the tech file, but some tech file contents may not be recognized
or may not work correctly.

**Starting magic**:

The correct way to start magic and have it correctly set up for
use with the IHP Open PDK is to invoke the startup script:

    magic -d XR -rcfile ${PDK_ROOT}/ihp-sg13g2/libs.tech/magic/ihp-sg13g2.magicrc

The `-d XR` invokes the Cairo 2D hardware-accelerated graphics.
Either `XR` or `OGL` (OpenGL) are preferred for the quality of
rendering.

## Using magic with IHP SG13G2

Most layers in magic follow historical naming conventions and drawing
styles common to magic tech files.  Polysilicon (GatPoly) is referred
to as "poly" and is drawn in solid red.  Diffusion (Activ) is automatically
split into derived layers representing N, P, N+, and P+ types ("ndiff",
"pdiff", "nsd", and "psd", respectively, with N-types drawn in green and
P-types drawn in brown).

Contacts are drawn as a contact area which is automatically filled with
contact cuts during GDS output.  All device types recognized for device
extraction are represented by unique layers (e.g., "nmos" or "pres" or
"mimcap").  Layers in diffusion and polysilicon are drawn on the same
"plane" and do not overlap;  overlap areas are replaced by derived types
representing the area of the overlap (e.g., "nmos" is the intersection of
"poly" and "ndiff").  Contact areas include any required surrounding
material out to the distance that is required on both top and bottom
metal layers.  DRC rule violation descriptions incorporate all IHP rules
that comprise the magic rule (e.g., "(V1.a + 2 * M2.c)" for via1 minimum
width).

Most layers that are implant types or ID marker layers are not drawn
explicitly in magic but are auto-generated on GDS output.  Among these
are nSD block, pSD, SalBlock, and ThickGateOx.  These mask layers are
inferred from their use in specific device types.  Mask layers can be
viewed in magic using the "cif see" command.  Mask layer names also
follow historical naming conventions in magic and are in all capital
letters;  most are only slight variations of the names used in the
klayout mapping (e.g., SBLK instead of SalBlock;  THKOX instead of
ThickGateOx;  DIFF instead of Activ).

DRC error reports have text for each DRC error that includes the rule
as specified in the document `GS13G2_os_layout_rules.pdf`.  Note that
there is not always a one-to-one mapping between Magic layout and
documented DRC rules.  For example, contact cut spacing rules are not
checked because contact cut spacing is guaranteed correct by design.
However, contact areas may not partially overlap between subcells
due to the automatic placement of cuts.

Some device layouts with complicated automatic generation of implant
layers require that the device layout adhere strictly to the
generated cell layout in the PDK (the pymacro layouts in klayout)
or else unexpected DRC errors may result when automatically
generating mask layers for GDS.  These devices include the bipolar
transistors, silicon-controlled rectifier (SCR), schottky diode,
ESD devices, and varactor capacitor.

A list of essential layer names in magic vs. IHP documentation is as
follows (this list is not exhaustive):

| IHP layer name or combination     | magic layer name |
|-----------------------------------|------------------|
| Activ + pSD + NWell               | pdiff            |
| Activ + pSD                       | psd              |
| Activ + NWell                     | nsd              |
| Activ                             | ndiff            |
| Activ + pSD + NWell + ThickGateOx | hvpdiff          |
| Activ + pSD + ThickGateOx         | hvpsd            |
| Activ + NWell + ThickGateOx       | hvnsd            |
| Activ + ThickGateOx               | hvndiff          |
| NWell                             | nwell            |
| nBuLay                            | dnwell           |
| GatPoly                           | poly             |
| GatPoly + Cont                    | pc               |
| Metal1                            | metal1           |
| ...                               | ...              |
| Metal5                            | metal5           |
| TopMetal1                         | metal6           |
| TopMetal2                         | metal7           |

Layers which are not available in the Open PDK are not represented
in the magic tech file, and will generate an error message when
read from a GDS file.  Magic will not generate any of these layers
in GDS output (unless GDS is designated "vendor" and copied
directly from a file to output, bypassing processing in magic).

A list of essential mask names in magic vs. IHP documentation is as
follows (this list is not exhaustive).  Note that mask names do not
exist in GDS output, which defines only numerical designations for
each layer;  however, each GDS layer is mapped to a name in the
IHP documentation and in the klayout layout technology file, and
in magic, these are CIF format name equivalents to GDS layers:

| IHP documented layer name | magic CIF layer name |
|---------------------------|----------------------|
| Activ                     | DIFF                 |
| NWell                     | NWELL                |
| nBuLay                    | DNWELL               |
| nSD.block                 | NSDBLOCK             |
| pSD                       | PSD                  |
| ThickGateOx               | THKOX                |
| SalBlock                  | SBLK                 |
| ExtBlock                  | EXTBLOCK             |
| EmWind                    | EMITTER              |
| EmWiHV                    | HVEMITTER            |
| prBoundary                | BOUND                |
| Cont                      | CONT                 |
| MIM                       | MIM                  |
| Passiv                    | GLASS                |
| Metal1                    | MET1                 |
| ...                       | ...                  |
| Metal5                    | MET5                 |
| TopMetal1                 | MET6                 |
| TopMetal2                 | MET7                 |
| Via1                      | VIA1                 |
| ...                       | ...                  |
| Via4                      | VIA4                 |
| TopVia1                   | VIA5                 |
| TopVia2                   | VIA6                 |

## DRC styles

Magic has an interactive DRC engine that detects and flags DRC
errors during layout.  Because the full set of DRC rules is
computationally expensive to compute in real time during layout
creation, magic defines different DRC "styles", corresponding
roughly to levels.  The DRC styles are as follows (and follow
usual naming conventions in magic):

- `drc(full)`: Complete set of DRC rules. Fine for use with small layouts.

- `drc(fast)`: Limited set of DRC rules, good for reasonably quick checking of large layouts.
			
- `drc(routing)`: DRC rules limited to metal layer rules only.  Good for working with large digital standard cell layouts.

The `drc(full)` style must always be used for final sign-off of
a design.  The best practice, especially for an open PDK in
active development, is to use magic DRC for interactive layout
work, and klayout DRC results for final sign-off of the design
layout.

## Device extraction

As of the pre-release version of the magic tech file, the list
of devices in layout vs. device models in ngspice is not
entirely consistent.  A list of extracted devices follows.
Note that in some cases, such as the ESD transistors in the
clamps, the presence of silicide block produces device behavior
that is a significant departure from the extracted device type.

There are two styles of device extraction.  When using magic
with netgen, always use the default style for both LVS and
simulation extraction:

	extract style ngspice()

There is an extract style that is equivalent to what klayout
produces for LVS netlists, using low-level SPICE component
identifiers for what are actually subcircuit devices.  This
style is

	extract style ngspice(lvs)

It is not recommended for use with the magic/netgen LVS flow.

| devices recognized by magic          | device type extracted |
|--------------------------------------|-----------------------|
| pfet                                 | sg13_lv_pmos          |
| nfet                                 | sg13_lv_nmos          |
| hvpfet                               | sg13_hv_pmos          |
| hvnfet                               | sg13_hv_nmos          |
| hvnmosesd (nmoscl_2, nmoscl_4, scr1) | sg13_hv_nmos          |
| npn (base layer) with gec emitter    | npn13g2               |
| npn (base layer) with nec emitter    | npn13g2l              |
| npn (base layer) with hvnec emitter  | npn13g2v              |
| pnp (base layer)                     | pnpMPA                |
| mimcap                               | cap_cmim              |
| pdiode                               | dpantenna             |
| ndiode                               | dantenna              |
| schottky                             | schottky              |
| nres                                 | rsil                  |
| pres                                 | rppd                  |
| xres                                 | rhigh                 |

| Devices not extracted                                                            |
|----------------------------------------------------------------------------------|
| diodevdd_2kv, diodevdd_4kv, diodevss_2kv, diodevss_4kv (no diode identifier)     |
| idiodevdd_2kv, idiodevdd_4kv, idiodevss_2kv, idiodevss_4kv (no diode identifier) |
| inductor (requires additional information provided by the device generator)      |
| iprobe, diffstbprobe (insufficient information and no device model)              |
| SVaricap (no device model)                                                       |
| ptap1 (to be completed)                                                          |
| ntap1 (to be completed)                                                          |

"RF" versions of devices are not separate device models but are enabled by
passing parameter "rfmode" to the device model.  This parameter passing
will be handled by the device generator.  The sole exception is the
"cap_rfcmim" model, which likely will also be handled by the device
generator.

**Undocumented device extraction**:

The following resistor devices are extracted but do not have device models,
and so are extracted as ideal SPICE components with value estimated from
known sheet resistance values.

| device       | description                               |
|--------------|-------------------------------------------|
| rm1          | metal1 resistor (net breaker)             |
| rm2          | metal2 resistor (net breaker)             |
| rm3          | metal3 resistor (net breaker)             |
| rm4          | metal4 resistor (net breaker)             |
| rm5          | metal5 resistor (net breaker)             |
| rm6          | metal6 (TopMetal1) resistor (net breaker) |
| rm7          | metal7 (TopMetal2) resistor (net breaker) |
| hvndiffres   | drain extension resistor on ESD nFETs     |
| isodiffres   | diffusion resistor in isolated pwell taps |
| hvisodiffres | diffusion resistor in SCR ptap            |

**Ignored devices**:

| device      | description                                         |
|-------------|-----------------------------------------------------|
| hvpvaractor | parasitic device formed at the ends of SVaricap     |
| fillfet     | device formed at the junction of fill diff and poly |
