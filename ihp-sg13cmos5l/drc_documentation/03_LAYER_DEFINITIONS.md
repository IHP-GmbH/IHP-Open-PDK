# Layer Definitions System

## Table of Contents
1. [Overview](#overview)
2. [GDS Layer Structure](#gds-layer-structure)
3. [Layer Variable Naming](#layer-variable-naming)
4. [The get_polygons Function](#the-get_polygons-function)
5. [Derived Layers](#derived-layers)
6. [Connectivity Setup](#connectivity-setup)
7. [IHP-SG13G2 Layer Map](#ihp-sg13g2-layer-map)

---

## Overview

The `layers_def.drc` file defines how GDS layers are read and made available to DRC rules. It:
1. Reads polygons from GDS layers
2. Creates named Ruby variables for each layer
3. Logs polygon counts for debugging
4. Sets up layer connectivity for net extraction

**Key Behavior**: If a GDS layer doesn't exist in the layout, `get_polygons()` returns an **empty polygon set** (not an error). This means:
- Unused layer definitions are harmless
- Rules checking non-existent layers produce no violations
- The same `layers_def.drc` can work for layouts with different layer subsets

---

## GDS Layer Structure

### GDS Layer Numbers and Datatypes

Each GDS layer is identified by two numbers:
- **Layer Number**: Primary identifier (1-255)
- **Datatype**: Sub-classification (0-255)

```
GDS Layer Format: layer_number/datatype
Example: 8/0 = Metal1 drawing
         8/2 = Metal1 pin
         8/22 = Metal1 filler
```

### Common Datatypes

| Datatype | Purpose | Suffix |
|----------|---------|--------|
| 0 | Drawing (main geometry) | `_drw` |
| 2 | Pin (text labels) | `_pin` |
| 20 | Mask data | `_mask` |
| 21 | Block/exclude regions | `_block` |
| 22 | Filler shapes | `_filler` |
| 23 | No-fill regions | `_nofill` |
| 24 | Slit (for slotting) | `_slit` |
| 25 | Text labels | `_text` |
| 26 | OPC markers | `_opc` |
| 27 | Inverse OPC | `_iopc` |
| 28 | No QRC extraction | `_noqrc` |
| 29 | Resistor marker | `_res` |
| 33 | Current probe | `_iprobe` |
| 34 | Differential probe | `_diffprb` |

---

## Layer Variable Naming

### Convention

```
{layer_name}_{datatype_suffix}

Examples:
  metal1_drw     = Metal1 drawing (8/0)
  metal1_pin     = Metal1 pin (8/2)
  metal1_filler  = Metal1 filler (8/22)
  metal1_res     = Metal1 resistor marker (8/29)
  activ_drw      = Activ drawing (1/0)
  cont_drw       = Contact drawing (6/0)
```

### Full Layer Name Examples

| Layer | GDS | Variable |
|-------|-----|----------|
| Activ drawing | 1/0 | `activ_drw` |
| Activ pin | 1/2 | `activ_pin` |
| Activ filler | 1/22 | `activ_filler` |
| GatPoly drawing | 5/0 | `gatpoly_drw` |
| Contact drawing | 6/0 | `cont_drw` |
| nSD drawing | 7/0 | `nsd_drw` |
| nSD block | 7/21 | `nsd_block` |
| Metal1 drawing | 8/0 | `metal1_drw` |
| Metal1 slit | 8/24 | `metal1_slit` |
| Metal1 resistor | 8/29 | `metal1_res` |
| pSD drawing | 14/0 | `psd_drw` |
| Via1 drawing | 19/0 | `via1_drw` |
| NWell drawing | 31/0 | `nwell_drw` |

---

## The get_polygons Function

### Definition

```ruby
def get_polygons(layer, data_type)
  ps = polygons(layer, data_type)
  $run_mode == 'deep' ? ps : ps.merged
end
```

### How It Works

1. `polygons(layer, datatype)` - KLayout built-in that reads GDS layer
2. If `deep` mode: returns as-is (hierarchy preserved)
3. Otherwise: merges overlapping polygons (flattened)

### Usage in layers_def.drc

```ruby
# Read a layer and log count
metal1_drw = get_polygons(8, 0)
count = metal1_drw.count
logger.info("metal1_drw has #{count} polygons")
polygons_count += count
```

### Empty Layer Behavior

```ruby
# If GDS doesn't have layer 126 (TopMetal1):
topmetal1_drw = get_polygons(126, 0)
# Returns empty polygon set, count = 0
# Any rules checking topmetal1_drw will find no violations
```

---

## Derived Layers

Derived layers are computed from base layers using Boolean operations.

### PWell Derivation

```ruby
# PWell = everywhere except NWell and PWell blocks
pwell_allowed = CHIP.not(pwell_block)
digisub_gap = digisub_drw.not(digisub_drw.sized(-1.nm))
pwell = pwell_allowed.not(nwell_drw).not(digisub_gap)
```

### Activ Derivations

```ruby
# N-type activ: Activ NOT covered by pSD or nSD_block
nactiv = activ_drw.not(psd_drw.join(nsd_block))

# P-type activ: Activ AND pSD
pactiv = activ_drw.and(psd_drw)
```

### Tap Derivations

```ruby
# P-tap: P-type activ in PWell
ptap = pactiv.and(pwell)

# N-tap: N-type activ in NWell
ntap = nactiv.and(nwell_drw)
```

### FET Derivations

```ruby
# P-channel FET active: P-activ in NWell
pact_fet = pactiv.and(nwell_drw)

# N-channel FET active: N-activ in PWell
nact_fet = nactiv.and(pwell)

# Gate regions
res_mk = polyres_drw.join(res_drw)  # Resistor markers
ngate = nact_fet.and(gatpoly_drw)
pgate = pact_fet.and(gatpoly_drw)
```

### Contact Derivations

```ruby
# Contacts excluding sealring
cont_nseal = cont_drw.not(edgeseal_drw)

# Square vs bar contacts
contbar = cont_nseal.non_squares
cont_sq = cont_nseal.not(contbar)
```

### Conditional Derivation

Derivations are wrapped in conditionals to save time/memory:

```ruby
# Only compute if needed by selected tables
nbulay_tables = %w[main nbulay nwell activfiller schottkydiode]
if TABLES.any?{|x| nbulay_tables.include?(x)}
  nbulay_gen_sized = nwell_drw.sized(-1.495.um).sized(0.495.um)
  nbuLay_gen = nbulay_gen_sized.not(nbulay_block.join(res_drw))
  nbuLay_gen_nbulay = nbuLay_gen.join(nbulay_drw)
end
```

---

## Connectivity Setup

Connectivity enables net extraction for antenna rules and other connectivity-based checks.

### connect() Syntax

```ruby
connect(layer1, layer2)
# Declares that layer1 and layer2 form electrical connections
```

### Full Connectivity Stack

```ruby
if CONNECTIVITY_RULES
  # Well connections
  connect(pwell_sub, pwell)
  connect(pwell, ptap)
  connect(nwell_drw, ntap)

  # Device connections
  connect(cont_drw, nactiv)
  connect(cont_drw, pactiv)
  connect(nbulay_drw, nbuLay_gen_nbulay)
  connect(nbuLay_gen_nbulay, nwell_drw)
  connect(ntap, cont_drw)
  connect(ptap, cont_drw)
  connect(poly_con, cont_drw)
  connect(nact_fet, cont_drw)
  connect(pact_fet, cont_drw)

  # Metal stack (M1 to M5)
  connect(cont_drw, metal1_con)
  connect(metal1_con, via1_drw)
  connect(via1_drw, metal2_con)
  connect(metal2_con, via2_drw)
  connect(via2_drw, metal3_con)
  connect(metal3_con, via3_drw)
  connect(via3_drw, metal4_con)
  connect(metal4_con, via4_drw)
  connect(via4_drw, metal5_con)

  # Top metals (NOT in slim PDK)
  connect(metal5_con, topvia1_n_cap)
  connect(topvia1_n_cap, topmetal1_con)
  connect(topmetal1_con, topvia2_drw)
  connect(topvia2_drw, topmetal2_con)
end
```

### Metal Connection Layers

```ruby
# Metal connection layers exclude resistor markers
poly_con = gatpoly_drw.not(res_mk)
metal1_con = metal1_drw.not(metal1_res)
metal2_con = metal2_drw.not(metal2_res)
metal3_con = metal3_drw.not(metal3_res)
metal4_con = metal4_drw.not(metal4_res)
metal5_con = metal5_drw.not(metal5_res)
```

---

## IHP-SG13G2 Layer Map

### FEOL Layers (Device Layers)

| GDS | Name | Purpose |
|-----|------|---------|
| 1 | Activ | Active silicon area |
| 3 | BiWind | Bipolar window (HBT) |
| 5 | GatPoly | Polysilicon gate |
| 6 | Cont | Contact cuts |
| 7 | nSD | N-type source/drain implant |
| 11 | pEmWind | P emitter window (HBT) |
| 14 | pSD | P-type source/drain implant |
| 28 | SalBlock | Salicide block |
| 31 | NWell | N-well implant |
| 32 | nBuLay | N-buried layer |
| 33 | EmWind | Emitter window (HBT) |
| 34 | EmWiHV | HV emitter window |
| 40 | Substrate | Substrate contact |
| 44 | ThickGateOx | Thick gate oxide (HV) |
| 46 | PWell | P-well marker |

### BEOL Layers (Metal Stack)

| GDS | Name | Purpose |
|-----|------|---------|
| 8 | Metal1 | First metal layer |
| 10 | Metal2 | Second metal layer |
| 19 | Via1 | M1-M2 via |
| 29 | Via2 | M2-M3 via |
| 30 | Metal3 | Third metal layer |
| 49 | Via3 | M3-M4 via |
| 50 | Metal4 | Fourth metal layer |
| 66 | Via4 | M4-M5 via |
| 67 | Metal5 | Fifth metal layer |
| 125 | TopVia1 | M5-TM1 via |
| 126 | TopMetal1 | Thick metal 1 |
| 133 | TopVia2 | TM1-TM2 via |
| 134 | TopMetal2 | Thick metal 2 |
| 9 | Passiv | Passivation opening |

### Special Layers

| GDS | Name | Purpose |
|-----|------|---------|
| 24 | RES | Resistor ID |
| 27 | IND | Inductor ID |
| 36 | MIM | MIM capacitor bottom |
| 128 | PolyRes | Poly resistor ID |
| 129 | Vmim | MIM via |
| 146 | ThinFilmRes | TFR ID |
| 63 | EdgeSeal | Seal ring marker |
| 160 | NoMetFiller | No metal fill region |
| 189 | prBoundary | PR boundary |

---

## Slim PDK Layer Subset

For `ihp-sg13cmos5l`, only these layers are included:

### Included Layers (29 total)

| GDS | Name | Included |
|-----|------|----------|
| 1 | Activ | Yes |
| 5 | GatPoly | Yes |
| 6 | Cont | Yes |
| 7 | nSD | Yes |
| 8 | Metal1 | Yes |
| 9 | Passiv | Yes |
| 10 | Metal2 | Yes |
| 14 | pSD | Yes |
| 19 | Via1 | Yes |
| 24 | RES | Yes |
| 28 | SalBlock | Yes |
| 29 | Via2 | Yes |
| 30 | Metal3 | Yes |
| 31 | NWell | Yes |
| 32 | nBuLay | Yes |
| 40 | Substrate | Yes |
| 44 | ThickGateOx | Yes |
| 46 | PWell | Yes |
| 49 | Via3 | Yes |
| 50 | Metal4 | Yes |
| 66 | Via4 | Yes |
| 67 | Metal5 | Yes |

### Excluded Layers (Key Categories)

| Category | Layers |
|----------|--------|
| HBT/Bipolar | 3, 11, 33, 34 |
| TopMetal | 125, 126, 133, 134 |
| MIM | 36, 129 |
| Inductor | 27 |
| Photonics | 78, 79, 85-89, etc. |

---

## Next Steps

- See [04_CREATING_NEW_RULES.md](./04_CREATING_NEW_RULES.md) for adding custom rules
- See [05_QUICK_REFERENCE.md](./05_QUICK_REFERENCE.md) for quick lookup
