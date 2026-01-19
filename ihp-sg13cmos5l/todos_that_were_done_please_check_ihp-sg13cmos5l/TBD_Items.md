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

**Status**: BACKLOG - New development required

**Current State**: RECOGNITION LAYER ONLY
- Layer 99 includes `mom` marker (datatype for recognition)
- **No dedicated MOM PCell** in the PDK

**Design Notes**:
- MOM capacitors can be manually constructed using interdigitated M1-M4 routing
- No PCell automation currently available
- SG13G2 PDK also lacks dedicated MOM PCell (only MIM caps exist, which are removed in SG13CMOS5L)
- Requires new PCell development from scratch

**Decision**: PCell development planned for future release

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

### DRC Verification (2026-01-19)

**topVia1**: PASS (density violations expected for small test cell)

**sealring_complete**: PASS (after PCell fix)
- Issue: Original sealring designed for TopVia2 which allows large vias
- TopVia1 requires exactly 0.42um x 0.42um via size
- Fix: Modified sealring_code.py to generate TopVia1 arrays instead of solid fills
- QA cell updated with regenerated sealring from fixed PCell

---

## tbd.5: Tech LEF

### Completed (2026-01-19)

**Issue**: Tech LEF was deleted (commit dabd71e) because it contained forbidden layers.

**Solution**: Recreated `sg13cmos5l_tech.lef` with correct M1-M4-TM1 metal stack.

**Removed**:
- Layer definitions: Via4, Metal5, TopVia2, TopMetal2
- Via definitions: All Via4_* (single/double cut), TopVia2EWNS
- ViaRules: via4Array, viagen67

**Modified**:
- TopVia1EWNS: Metal5 → Metal4 (connects M4 to TM1)
- viagen56 → viagen45: Metal5 → Metal4

**Verification**: OpenROAD loaded successfully (15 layers, 52 vias, 84 stdcells)
