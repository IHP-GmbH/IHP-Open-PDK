# TBD Items - IHP SG13CMOS5L PDK

## tbd.1: High-Resistance Poly Resistors

**Current State**: ENABLED
- `rppd_code` - P+ poly resistor (symlink to G2 PDK)
- `rhigh_code` - High-R poly resistor (symlink to G2 PDK)

**Layers Required**:
- PolyRes - included in SG13CMOS5L
- ThinFilmRes - included in SG13CMOS5L (if needed)

**Decision Needed**: Should hi-res poly resistors (rppd, rhigh) remain in the SG13CMOS5L PDK? 🟢 **YES**

---

## tbd.2: MOM Capacitors (M1-M4)


**Current State**: RECOGNITION LAYER ONLY
- Layer 99 includes `mom` marker (datatype for recognition)
- **No dedicated MOM PCell** in the PDK

**Design Notes**:
- MOM capacitors can be manually constructed using interdigitated M1-M4 routing
- No PCell automation currently available. Possible to implement.
- SG13G2 PDK also lacks dedicated MOM PCell (only MIM caps exist, which are removed in SG13CMOS5L)

**Decision Needed**: Is a MOM capacitor PCell required for the SG13CMOS5L PDK? If yes, this will need custom development. 🟢 **YES, Pcell is not available - we should plan development**

---

## tbd.3: Parasitic PNP (pnpMPA)


**Current State**: NOW ENABLED (2025-12-15)
- `pnpMPA_code` added to `__init__.py` moduleNames
- Symlink created: `ihp/pnpMPA_code.py` -> full SG13G2 PDK

**Technical Details**:
- pnpMPA parameters defined in `sg13cmos5l_tech.json`
- Parasitic vertical PNP substrate device
- Uses existing CMOS layers (no additional layers required)

**Decision Needed**: Should the parasitic PNP (pnpMPA) remain in the SG13CMOS5L PDK release? 🟢 **YES**

---

## tbd.4: QA cells

### Completed (2025-01-19)

Forbidden layers removed: nBuLay(32), Via4(66), Metal5(67), TopVia2(133), TopMetal2(134)
Note: TopVia1(125) is required for M4-TM1 connection.

layers:
- [x] activFiller - removed nBuLay
- [x] gatFiller - removed nBuLay
- [x] metalFiller - removed Metal5
- [x] metaln - removed Via4, Metal5
- [x] passiv - removed Via4, Metal5, TopVia2, TopMetal2
- [x] topMet1Filler - no changes needed
- [x] topVia1 - regenerated using via_stack PCell (M4-TopVia1-TM1)
- [x] vian - removed Via4, Metal5

devices:
- [x] sealring_complete - removed forbidden layers, added TopVia1(125) for M4-TM1 connection
