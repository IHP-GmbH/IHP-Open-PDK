# Standard Cell Symbols

## Overview

This directory contains tool-specific symbol files for the `sg13g2_stdcell` library.
The corresponding schematics are located in `$PDK/libs.ref/sg13g2_stdcell/sch`.

## Directory Layout

- `qucs-s/`: Qucs-S symbol definitions
- `xschem/`: Xschem symbol definitions

## Qucs-S

The `qucs-s/` directory contains:

- XML symbol definitions used by Qucs-S
- `.sym` geometry files referenced by the XML symbols

A symbolic link to this directory is created at `$PDK/libs.tech/qucs-s/symbols_stdcell` so that Qucs-S can use the standard-cell symbols as schematic components.

## Xschem

The `xschem/` directory contains `.sym` files for Xschem.

All standard-cell symbols are defined as `subcircuit` symbols. The corresponding schematic is selected through the `hierarchy_config` procedure defined in `$PDK/libs.tech/xschem/xschemrc`.

Projects must use the correct `xschemrc` configuration. Otherwise, Xschem will not resolve the intended standard-cell schematics for netlist.

## Xschem Hierarchy Selection

### Default Behavior

By default, each Xschem symbol descends into the corresponding standard-cell schematic, and the generated netlist includes that schematic.

### Empty Schematic

To use a symbol without descending into its default schematic, provide an empty schematic named `<cell>_empty.sch` in `$PDK/libs.ref/sg13g2_stdcell/sch`.

Select `IHP -> Select stdcell hierarchy`, then choose the empty-schematic option.

![Select stdcell hierarchy menu](TODO: add GitHub attachment URL)
![Empty stdcell hierarchy selection dialog](TODO: add GitHub attachment URL)

After this selection, Xschem uses `<cell>_empty.sch` for each standard cell when that file exists. If no matching empty schematic exists, Xschem falls back to the default schematic.

When using this mode, the top-level design must provide the required subcircuit definition, typically through `.include`.

### Custom Schematic

To use a custom simulation schematic, provide a schematic named `<cell>_custom.sch` in `$PDK/libs.ref/sg13g2_stdcell/sch`.

Select `IHP -> Select stdcell hierarchy`, then choose the custom-schematic option.

![Custom stdcell hierarchy selection dialog](TODO: add GitHub attachment URL)

After this selection, Xschem uses `<cell>_custom.sch` for each standard cell when that file exists. If no matching custom schematic exists, Xschem falls back to the default schematic.

