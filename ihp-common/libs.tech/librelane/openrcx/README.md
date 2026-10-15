# OpenRCX model generation

`gen_rcx_model.sh` turns a process stack description into an OpenRCX
model file, using FasterCap as the reference field solver. It follows
OpenROAD's `src/rcx/test/rcx_v2/FasterCapModel` flow, but with its own
geometry step:

1. `gen_solver_patterns` (openroad) — 3D wire patterns and resistance table
2. `solve_pattern.py` + `FasterCap` — capacitance matrix per pattern
3. `fasterCapParse.py` (openroad) — capacitance tables
4. `init_rcx_model` / `read_rcx_tables` / `write_rcx_model` (openroad)
5. `expand_resover.py` — RESOVER tables in the layout the extractor expects

`solve_pattern.py` replaces OpenROAD's `UniversalFormat2FasterCap` converter
because that one overestimates coupling about 3x for this stack: its
patterns are only 10 wire widths long (1.6 um for Metal1), so the 3D end
fringing dominates, and its dielectric interface panels placed on the
conductor sidewalls inflate the coupling a further 1.7x. Our step solves
each pattern at two lengths (10 and 20 um) and differences them, which
removes the end effects exactly, and uses a uniform dielectric: the IHP
SG13 stack is 4.1 +- 0.1 from Metal1 to the passivation (effective 4.11
below Metal1 including field oxide and ILD0 nitride). Not modelled is the
0.4 um nitride passivation (er 6.6) 1.5 um above the top metal.

Each PDK keeps its stack in `libs.tech/librelane/openrcx/<name>.process`
and symlinks this script next to it:

```
cd ihp-sg13cmos5l/libs.tech/librelane/openrcx
./gen_rcx_model.sh sg13cmos5l.TYP.process          # all stages
./gen_rcx_model.sh sg13cmos5l.TYP.process patterns  # single stage
```

Output: `<name>.<CORNER>.rules` next to the process file. It is an
extraction rules file for the default OpenRCX extractor:

```tcl
extract_parasitics -ext_model_file <name>.TYP.rules
```

(`extract_parasitics -version 2` reads the file but extracts no
capacitance from it; use the default.) `expand_resover.py` runs as the
last step: the extractor needs the `RESOVER` tables as a grid of neighbour
spacing pairs, the solver flow measures resistance only once per metal.

Requirements: `openroad` with OpenRCX v2, `FasterCap`
(https://github.com/ediloren/FasterCap, build headless with
`-DFASTFIELDSOLVERS_HEADLESS=ON`), python3 with `xlsxwriter`, `pandas`,
`matplotlib` and `numpy` (imported by the parser). The two OpenROAD helper
scripts are fetched from a pinned commit unless `OPENROAD_SRC` points to
a checkout. Environment knobs: `OPENROAD`, `FASTERCAP`, `CORNER`, `WORK`,
`OUT`, `EPS`, `EXT`, `ACCURACY`, `TIMEOUT`, `JOBS` (see the script header).

The FasterCap stage runs two solver jobs per pattern (about a minute
together, ~300 patterns for a 5-metal stack) and is incremental. A run
that does not converge within `TIMEOUT` is killed and its last completed
matrix used; `<pattern>/solve.log` reports the achieved relative change
per pattern.

## Process file format

```
CONDUCTOR <name> {
        distance    <gap to the top of the conductor below, um>
        thickness   <um>
        min_width   <um>
        min_spacing <um>
        resistivity <ohm*um, i.e. RPSQ * thickness>
}
DIELECTRIC <name> {
        epsilon   <er>
        thickness <um>
        next_met N   # fills the gap below metal N
        met N        # at the level of metal N
}
```

Dielectrics without `met`/`next_met` are the passivation above the top
metal. The dielectric layers only position the conductors; the solver
step uses the uniform `EPS`. Names follow OpenROAD's convention
(`m<N>_<k>` at metal level N, no `m` in other names) so the file stays
usable with OpenROAD's own converter.

## Corners

`MIN` (low RC) and `MAX` (high RC) process files are derived from the
`TYP` one with the min/max columns of the process specification:

* sheet resistance (spec 3.1) → `resistivity`
* line width delta (spec 3.2) → `width_delta`: the solver widens or
  narrows the wires of that metal, tables stay keyed by drawn width
* plate capacitance min/max (spec 3.7) → dielectric gaps (`distance` and
  the `next_met` dielectrics) scaled by C_typ/C_corner: 37/31 and 37/43
  aF/um² for Metal1 to substrate, 68/54 and 68/82 between metals

Metal thickness stays at target (no tolerance in the spec), the
permittivity stays 4.1 (its ±0.1 is inside the capacitance spread). TYP
uses drawn widths without the typical line width delta; IHP's own typical
rules agree with that within 2–3 %.
