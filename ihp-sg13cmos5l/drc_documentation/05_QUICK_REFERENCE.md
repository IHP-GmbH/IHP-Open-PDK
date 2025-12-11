# DRC Quick Reference Card

## Running DRC

```bash
# Basic run
python run_drc.py --layout=design.gds

# Specific tables only
python run_drc.py --layout=design.gds --table=metal1 --table=via1

# All FEOL rules
python run_drc.py --layout=design.gds --no_beol

# All BEOL rules
python run_drc.py --layout=design.gds --no_feol

# Output to specific file
python run_drc.py --layout=design.gds -o results.lyrdb

# Parallel execution
python run_drc.py --layout=design.gds --threads=8 --mp
```

---

## DRC Operations

| Operation | Syntax | Description |
|-----------|--------|-------------|
| **Width** | `layer.width(val.um, euclidian)` | Min width check |
| **Space** | `layer.space(val.um, euclidian)` | Min space/notch |
| **Separation** | `layer1.sep(layer2, val.um, euclidian)` | Space between layers |
| **Enclosure** | `inner.enclosed(outer, val.um, euclidian)` | Enclosure check |
| **Overlap** | `layer1.overlap(layer2, val.um, euclidian)` | Overlap check |

---

## Boolean Operations

| Operation | Syntax | Result |
|-----------|--------|--------|
| **AND** | `layer1.and(layer2)` | Intersection |
| **OR** | `layer1.or(layer2)` | Union |
| **JOIN** | `layer1.join(layer2)` | Union (alias) |
| **NOT** | `layer1.not(layer2)` | Subtraction |
| **XOR** | `layer1.xor(layer2)` | Exclusive OR |

---

## Selection Operations

| Operation | Syntax | Description |
|-----------|--------|-------------|
| **Interacting** | `layer1.interacting(layer2)` | Shapes touching layer2 |
| **Not interacting** | `layer1.not_interacting(layer2)` | Shapes not touching |
| **With area** | `layer.with_area(min, max)` | By area range |
| **With length** | `edges.with_length(min, max)` | By edge length |
| **With angle** | `edges.with_angle(angle, absolute)` | By edge angle |

---

## Edge Operations

```ruby
# Get all edges
edges = layer.edges

# Filter by angle
horizontal = layer.edges.with_angle(0, absolute)
vertical = layer.edges.with_angle(90, absolute)
diagonal = layer.edges.with_angle(45, absolute)

# Edge-to-edge spacing
violations = layer.edges.sep(other_edges, val.um, euclidian)
```

---

## Rule Template

```ruby
# Rule X.y: Description
logger.info('Executing rule X.y')
xy_value = drc_rules['X_y'].to_f
xy_l = layer_drw.width(xy_value.um, euclidian)
xy_l.output('X.y', "Description: #{xy_value} um")
xy_l.forget
```

---

## Layer Variables

### FEOL
| Variable | GDS | Description |
|----------|-----|-------------|
| `activ_drw` | 1/0 | Active area |
| `gatpoly_drw` | 5/0 | Gate poly |
| `cont_drw` | 6/0 | Contacts |
| `nsd_drw` | 7/0 | N-source/drain |
| `psd_drw` | 14/0 | P-source/drain |
| `nwell_drw` | 31/0 | N-well |
| `nbulay_drw` | 32/0 | N-buried |
| `thickgateox_drw` | 44/0 | Thick gate oxide |

### BEOL
| Variable | GDS | Description |
|----------|-----|-------------|
| `metal1_drw` | 8/0 | Metal 1 |
| `metal2_drw` | 10/0 | Metal 2 |
| `metal3_drw` | 30/0 | Metal 3 |
| `metal4_drw` | 50/0 | Metal 4 |
| `metal5_drw` | 67/0 | Metal 5 |
| `via1_drw` | 19/0 | Via 1 |
| `via2_drw` | 29/0 | Via 2 |
| `via3_drw` | 49/0 | Via 3 |
| `via4_drw` | 66/0 | Via 4 |
| `passiv_drw` | 9/0 | Passivation |

### TopMetal (Full PDK only)
| Variable | GDS | Description |
|----------|-----|-------------|
| `topvia1_drw` | 125/0 | Top Via 1 |
| `topmetal1_drw` | 126/0 | Top Metal 1 |
| `topvia2_drw` | 133/0 | Top Via 2 |
| `topmetal2_drw` | 134/0 | Top Metal 2 |

---

## Derived Layers

```ruby
# PWell (computed)
pwell = CHIP.not(pwell_block).not(nwell_drw)

# N-type activ
nactiv = activ_drw.not(psd_drw.join(nsd_block))

# P-type activ
pactiv = activ_drw.and(psd_drw)

# Taps
ptap = pactiv.and(pwell)
ntap = nactiv.and(nwell_drw)

# FET regions
nact_fet = nactiv.and(pwell)
pact_fet = pactiv.and(nwell_drw)
```

---

## JSON Parameter Format

```json
{
  "drc_rules": {
    "Layer_rule": 0.16,
    "Layer_rule_w": 0.3,
    "Layer_rule_cr": 1.0
  }
}
```

**Common suffixes:**
- `_w` = width threshold
- `_cr` = critical length (parallel run)
- `_nr` = number/count
- `_min` = minimum value

---

## Global Variables

| Variable | Type | Description |
|----------|------|-------------|
| `$input` | String | Input GDS path |
| `$report` | String | Output .lyrdb path |
| `$tables` | String | Space-separated table names |
| `$threads` | Integer | Thread count |
| `$run_mode` | String | 'deep', 'flat', 'tiling' |

---

## Constants

| Constant | Type | Description |
|----------|------|-------------|
| `TABLES` | Array | Selected table names |
| `FEOL` | Boolean | Run all FEOL |
| `BEOL` | Boolean | Run all BEOL |
| `PRECHECK_DRC` | Boolean | Minimal rules |
| `CONNECTIVITY_RULES` | Boolean | Enable nets |

---

## Memory Management

```ruby
# ALWAYS free results
result.forget

# Free intermediate results too
temp1 = layer1.sized(-val.um)
temp2 = temp1.sized(val.um)
temp1.forget  # Free immediately
result = temp2.and(layer2)
temp2.forget
result.output('X.y', "Desc")
result.forget
```

---

## File Locations

```
ihp-sg13g2/libs.tech/klayout/tech/drc/
├── ihp-sg13g2.drc              # Main entry
├── run_drc.py                  # CLI runner
└── rule_decks/
    ├── layers_def.drc          # Layer definitions
    ├── sg13g2_tech_default.json # Parameters
    ├── feol/                   # FEOL rules
    └── beol/                   # BEOL rules
```

---

## Debugging

```ruby
# Log message
logger.info("Debug message")

# Log layer count
logger.info("layer count: #{layer.count}")

# Output intermediate result
temp.output('DEBUG', "Debug layer")
```

---

## Common Patterns

### Wide Metal Rule
```ruby
threshold = width_value / 2
wide = layer.sized(-threshold.um).sized(threshold.um)
violations = layer.sep(wide, space.um,
  projection_limits(run_length.um, nil))
wide.forget
violations.output('X.y', "Wide spacing")
violations.forget
```

### Conditional Derivation
```ruby
if TABLES.any?{|t| needed_tables.include?(t)}
  derived = layer1.and(layer2)
end
```

### Loop Over Layers
```ruby
layers = [metal2_drw, metal3_drw, metal4_drw, metal5_drw]
layers.each_with_index do |lay, idx|
  met_no = idx + 2
  # ... rules using lay and met_no
end
```
