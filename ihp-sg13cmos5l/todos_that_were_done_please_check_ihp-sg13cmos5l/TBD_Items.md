# TBD Items - IHP SG13CMOS5L PDK

## tbd.1: High-Resistance Poly Resistors

**Current State**: ENABLED
- `rppd_code` - P+ poly resistor (symlink to G2 PDK)
- `rhigh_code` - High-R poly resistor (symlink to G2 PDK)

**Layers Required**:
- PolyRes (GDS 128) - included in SG13CMOS5L
- ThinFilmRes (GDS 146) - included in SG13CMOS5L (if needed)

**Decision Needed**: Should hi-res poly resistors (rppd, rhigh) remain in the SG13CMOS5L PDK?

---

## tbd.2: MOM Capacitors (M1-M4)


**Current State**: RECOGNITION LAYER ONLY
- Layer 99 includes `mom` marker (datatype for recognition)
- **No dedicated MOM PCell** in the PDK

**Design Notes**:
- MOM capacitors can be manually constructed using interdigitated M1-M4 routing
- No PCell automation currently available. POssible to implement.
- SG13G2 PDK also lacks dedicated MOM PCell (only MIM caps exist, which are removed in SG13CMOS5L)

**Decision Needed**: Is a MOM capacitor PCell required for the SG13CMOS5L PDK? If yes, this would need custom development.

---

## tbd.3: Parasitic PNP (pnpMPA)


**Current State**: NOW ENABLED (2025-12-15)
- `pnpMPA_code` added to `__init__.py` moduleNames
- Symlink created: `ihp/pnpMPA_code.py` -> full SG13G2 PDK

**Technical Details**:
- pnpMPA parameters defined in `sg13cmos5l_tech.json`
- Parasitic vertical PNP substrate device
- Uses existing CMOS layers (no additional layers required)


**Decision Needed**: Should the parasitic PNP (pnpMPA) remain in the SG13CMOS5L PDK release?

---
