# Standard Cell Schematics

## Overview

This directory contains tool-specific schematic files for the
`sg13cmos5l_stdcell` library.

These schematics are used by the symbols defined in
`$PDK_ROOT/$PDK/libs.ref/sg13cmos5l_stdcell/sym`.

## Directory Layout

- `xschem/`: Xschem schematic files

## Relation to Symbols

The schematics in this directory provide the hierarchical source used by the
standard-cell symbols.

In particular, the Xschem symbols in `../sym/xschem/` are defined as
`subcircuit` symbols and descend into the corresponding schematics from this
directory.

The `sg13cmos5l_stdcell` cells are transistor-for-transistor identical to the
`sg13g2_stdcell` cells, and the schematics contain no PDK-specific references.
Each `sg13cmos5l_<cell>.sch` is therefore a symbolic link to the matching
`sg13g2_<cell>.sch` in `ihp-sg13g2/libs.ref/sg13g2_stdcell/sch/xschem`.

## Additional Documentation

For symbol usage, hierarchy selection, and alternate schematic behavior, see
the [Standard Cell Symbols README](../sym/README.md).
