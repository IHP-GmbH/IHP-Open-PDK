# Tcl script:  Setup for reading SRAM GDS into magic
#
# This requires flattening certain subcells to avoid layer
# ambiguities which in turn cause overlap errors to appear
# in magic.
#
# NOTES:
# 1. Flattening lvsres_* and *_CELL_SUB prevents metal2/rm2 overlap errors.
# 2. VIA_M1_* cells are ambiguous to magic.
# 3. VIA_M2_* and RSC_* cells have ContBar vias in different alignments,
#    which interferes with magic's check for bad via overlaps.
# 4. _CELL_CORNER has NWELL that does not extend under diffusion,
#    causing magic to misinterpret the layer.

gds flatglob lvsres_*
gds flatglob *_CELL_SUB
gds flatglob VIA_M1_*
gds flatglob VIA_M2_*
gds flatglob RSC_*
gds flatglob *_CELL_CORNER
