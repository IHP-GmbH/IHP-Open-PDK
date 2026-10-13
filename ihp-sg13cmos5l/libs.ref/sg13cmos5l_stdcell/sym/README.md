# Standard Cell Symbols

## Overview

This directory contains tool-specific symbol files for the `sg13cmos5l_stdcell`
library. The corresponding schematics are located in
`$PDK_ROOT/$PDK/libs.ref/sg13cmos5l_stdcell/sch`.

The `sg13cmos5l_stdcell` cells are transistor-for-transistor identical to the
`sg13g2_stdcell` cells (compare the two `spice/` netlists). The symbols are
therefore copies of the `sg13g2_stdcell` symbols with the `sg13g2_` prefix
renamed to `sg13cmos5l_`, and the schematics are symbolic links into
`ihp-sg13g2/libs.ref/sg13g2_stdcell/sch/xschem`.

## Directory Layout

- `xschem/`: Xschem symbol definitions

## Xschem

The `xschem/` directory contains `.sym` files for Xschem.

All standard-cell symbols are defined as `subcircuit` symbols. The corresponding
schematic is selected through the `hierarchy_config` procedure defined in
`$PDK_ROOT/$PDK/libs.tech/xschem/xschemrc`.

**Projects must use the correct `xschemrc` configuration. Otherwise, Xschem will
not resolve the intended standard-cell schematics for netlisting.**

For backward compatibility, the symbols are also reachable under their former
location `$PDK_ROOT/$PDK/libs.tech/xschem/sg13cmos5l_stdcells/` through symbolic
links, so existing schematics referencing `sg13cmos5l_stdcells/<cell>.sym` keep
working.

## Xschem Hierarchy Selection

### Default Behavior

By default, each Xschem symbol descends into the corresponding standard-cell
schematic, and the generated netlist includes that schematic.

### Primitive (no hierarchy)

To use a symbol without descending into its schematic, switch the symbol type to
`primitive`. This causes the netlister to emit the cell inline using the symbol's
`format` string instead of a subcircuit call.

Open the menu via `IHP -> Select stdcell hierarchy`. In the
"Stdcell schematic view" dialog choose "Primitive (no hierarchy)" and press OK.

No `_empty.sch` file is required or used in this mode. The symbol `type` is
changed from `subcircuit` to `primitive`, so Xschem does not descend into any
schematic during netlisting.

When using this mode, the top-level design must provide the required subcircuit
definition, typically through `.include`:

```
.include $PDK_ROOT/ihp-sg13cmos5l/libs.ref/sg13cmos5l_stdcell/spice/sg13cmos5l_stdcell.spice
```

### Custom Schematic

To use a custom simulation schematic, provide a schematic named
`<cell>_custom.sch` in `$PDK_ROOT/$PDK/libs.ref/sg13cmos5l_stdcell/sch/xschem/`.

Open the menu via `IHP -> Select stdcell hierarchy`. In the
"Stdcell schematic view" dialog choose "Custom schematic" and press OK.

After this selection, Xschem uses `<cell>_custom.sch` for each standard cell
when that file exists. If no matching custom schematic exists, Xschem falls back
to the default schematic.
