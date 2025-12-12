# rename_cells.py
# Run:
#   klayout -b -r rename_cells.py -rd infile=input.gds -rd outfile=output.gds
# Optional:
#   -rd from_s=sg13g2_ -rd to_s=sg13cmos5l_

import pya

# -rd variables become globals in KLayout batch scripts
g = globals()

infile  = g.get("infile", None)
outfile = g.get("outfile", None)
from_s  = g.get("from_s", "sg13g2_")
to_s    = g.get("to_s",   "sg13cmos5l_")

if not infile or not outfile:
    raise SystemExit(
        "Missing variables. Use:\n"
        "  klayout -b -r rename_cells.py -rd infile=input.gds -rd outfile=output.gds\n"
        "Optional:\n"
        "  -rd from_s=sg13g2_ -rd to_s=sg13cmos5l_"
    )

layout = pya.Layout()
layout.read(infile)

cells = [c for c in layout.each_cell()]

# Collision check: abort if a rename would clash with an existing *different* cell
name_to_index = {c.name: c.cell_index() for c in cells}

planned = []
for c in cells:
    old = c.name
    if from_s in old:
        new = old.replace(from_s, to_s)
        planned.append((c, old, new))

collisions = []
for c, old, new in planned:
    if new in name_to_index and name_to_index[new] != c.cell_index():
        collisions.append((old, new))

if collisions:
    lines = ["Name collisions detected; aborting to avoid unintended merges:"]
    for old, new in collisions[:100]:
        lines.append(f"  {old} -> {new} (already exists)")
    if len(collisions) > 100:
        lines.append(f"  ... and {len(collisions) - 100} more")
    raise SystemExit("\n".join(lines))

# Rename
for c, old, new in planned:
    c.name = new

print(f"Renamed {len(planned)} cells: '{from_s}' -> '{to_s}'")
layout.write(outfile)
print(f"Wrote: {outfile}")
