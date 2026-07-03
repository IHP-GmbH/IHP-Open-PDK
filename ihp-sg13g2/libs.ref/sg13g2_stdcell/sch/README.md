# Standard Cell Schematics

## Overview

This directory contains tool-specific schematic files for the `sg13g2_stdcell`
library.

These schematics are used by the symbols defined in
`$PDK_ROOT/$PDK/libs.ref/sg13g2_stdcell/sym`.

## Directory Layout

- `qucs-s/`: Qucs-S schematic files
- `xschem/`: Xschem schematic files

## Relation to Symbols

The schematics in this directory provide the source (hierarchical for Xschem) used by the
standard-cell symbols.

In particular, the Xschem symbols in `../sym/xschem/` are defined as
`subcircuit` symbols and descend into the corresponding schematics from this
directory.

## Additional Documentation

For symbol usage, hierarchy selection, and alternate schematic behavior, see
the [Standard Cell Symbols README](../sym/README.md).
