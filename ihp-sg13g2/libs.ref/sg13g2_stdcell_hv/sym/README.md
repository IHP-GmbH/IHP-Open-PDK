# Standard Cell Symbols

## Overview

This directory contains tool-specific symbol files for the
`sg13g2_stdcell_hv` (thick-oxide, 3.3 V) library. The corresponding
schematics are in `../sch`.

## Directory Layout

- `qucs-s/`: Qucs-S symbol definitions
- `xschem/`: Xschem symbol definitions

## Qucs-S

The `qucs-s/` directory contains:

- one XML component definition per cell, naming the `sg13g2_hv_*` model
- `.sym` geometry files referenced by those XML definitions

The gate shapes are function-level and identical to the thin-oxide library's,
so they are carried over unchanged; only the component definitions are
retargeted.

For Qucs-S to offer these cells as schematic components, this directory needs
to be visible under the Qucs-S component library path, the same way the
thin-oxide library is exposed as
`$PDK_ROOT/$PDK/libs.tech/qucs-s/symbols_stdcell`:

    ln -s $PDK_ROOT/$PDK/libs.ref/sg13g2_stdcell_hv/sym/qucs-s \
          $PDK_ROOT/$PDK/libs.tech/qucs-s/symbols_stdcell_hv
