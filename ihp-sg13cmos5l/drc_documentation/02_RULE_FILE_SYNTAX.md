# DRC Rule File Syntax

## Table of Contents
1. [File Structure](#file-structure)
2. [Rule Anatomy](#rule-anatomy)
3. [DRC Operations](#drc-operations)
4. [Working with Edges](#working-with-edges)
5. [Projection and Angles](#projection-and-angles)
6. [Output and Logging](#output-and-logging)
7. [Memory Management](#memory-management)
8. [Common Patterns](#common-patterns)

---

## File Structure

Every rule file follows this structure:

```ruby
# frozen_string_literal: true

# License header (Apache 2.0)
#=========================================================================================
# Copyright 2025 IHP PDK Authors
# ...
#=========================================================================================

# Guard clause - controls when rules execute
if TABLES.include?('tablename') || FEOL  # or BEOL for backend rules
  #================================================
  #--------------- Section Header -----------------
  #================================================

  logger.info('Starting tablename table')

  # Derivations (computed layers)
  # ...

  # Rule definitions
  # ...

end
```

### Guard Clause Patterns

```ruby
# Run if specific table selected OR all FEOL enabled
if TABLES.include?('activ') || FEOL

# Run if specific table selected OR all BEOL enabled
if TABLES.include?('metal1') || BEOL

# Skip if PRECHECK mode (for non-essential rules)
unless PRECHECK_DRC
  # Extended rules here
end
```

---

## Rule Anatomy

### Basic Rule Structure

```ruby
# Rule M1.a: Min. Metal1 width is 0.16um
logger.info('Executing rule M1.a')              # 1. Log execution
m1_a_value = drc_rules['M1_a'].to_f             # 2. Get value from JSON
m1_a_l = metal1_drw.width(m1_a_value.um, euclidian)  # 3. Execute check
m1_a_l.output('M1.a', "Description: #{m1_a_value} um")  # 4. Output violations
m1_a_l.forget                                   # 5. Free memory
```

### Components Explained

| Step | Code | Purpose |
|------|------|---------|
| 1 | `logger.info(...)` | Log progress (visible in console/log file) |
| 2 | `drc_rules['M1_a'].to_f` | Read parameter from JSON, convert to float |
| 3 | `layer.width(...)` | Execute geometric check, returns violations |
| 4 | `.output('Rule.ID', "message")` | Write violations to report database |
| 5 | `.forget` | Release memory (critical for large layouts) |

### Naming Convention

```
Rule ID format: LayerCode.letter

Examples:
  M1.a   = Metal1, rule 'a' (typically min width)
  M1.b   = Metal1, rule 'b' (typically min space)
  Act.a  = Activ, rule 'a'
  V1.a   = Via1, rule 'a'
  NW.c   = NWell, rule 'c'
```

---

## DRC Operations

### Width Check (Minimum Width)

```ruby
# Check minimum width of a layer
violations = layer.width(value.um, euclidian)
```

**Parameters:**
- `value.um` - minimum width in microns
- `euclidian` - measurement method (most common)

**Example:**
```ruby
# M1.a: Min. Metal1 width = 0.16um
m1_a_value = drc_rules['M1_a'].to_f
violations = metal1_drw.width(m1_a_value.um, euclidian)
violations.output('M1.a', "Min. Metal1 width: #{m1_a_value} um")
violations.forget
```

### Space Check (Minimum Spacing)

```ruby
# Check minimum space between shapes of same layer
violations = layer.space(value.um, euclidian)
```

**Example:**
```ruby
# M1.b: Min. Metal1 space = 0.18um
m1_b_value = drc_rules['M1_b'].to_f
violations = metal1_drw.space(m1_b_value.um, euclidian)
violations.output('M1.b', "Min. Metal1 space: #{m1_b_value} um")
violations.forget
```

### Separation Check (Between Different Layers)

```ruby
# Check minimum separation between two different layers
violations = layer1.sep(layer2, value.um, euclidian)
```

**Example:**
```ruby
# Check NWell to Activ separation
violations = nwell_drw.sep(activ_drw, 0.31.um, euclidian)
violations.output('NW.c', "Min. NWell to Activ space: 0.31 um")
violations.forget
```

### Enclosure Check

```ruby
# Check that layer1 is enclosed by layer2 by minimum value
violations = layer1.enclosed(layer2, value.um, euclidian)

# Alternative: check enclosure from layer2's perspective
violations = layer2.enclosing(layer1, value.um, euclidian)
```

**Example:**
```ruby
# Contact must be enclosed by Metal1 by at least 0.07um
violations = cont_drw.enclosed(metal1_drw, 0.07.um, euclidian)
violations.output('Cnt.d', "Min. Cont enclosure by Metal1: 0.07 um")
violations.forget
```

### Overlap Check

```ruby
# Check minimum overlap between layers
violations = layer1.overlap(layer2, value.um, euclidian)
```

### Extension Check

```ruby
# Check that layer1 extends past layer2 by minimum value
violations = layer1.extension(layer2, value.um, euclidian)
```

---

## Boolean Operations

### AND (Intersection)

```ruby
# Get intersection of two layers
result = layer1.and(layer2)

# Example: Activ inside NWell
nactiv_in_nwell = activ_drw.and(nwell_drw)
```

### OR / JOIN (Union)

```ruby
# Combine two layers
result = layer1.or(layer2)
result = layer1.join(layer2)  # Alias for .or

# Example: All metal resistance markers
all_res = metal1_res.join(metal2_res).join(metal3_res)
```

### NOT (Subtraction)

```ruby
# Subtract layer2 from layer1
result = layer1.not(layer2)

# Example: Activ outside of NWell
activ_in_pwell = activ_drw.not(nwell_drw)
```

### XOR (Exclusive OR)

```ruby
# Shapes in one layer but not both
result = layer1.xor(layer2)
```

### Interaction Checks

```ruby
# Get shapes from layer1 that touch/overlap layer2
touching = layer1.interacting(layer2)

# Get shapes from layer1 that DON'T touch layer2
not_touching = layer1.not_interacting(layer2)

# With count constraints
# layer1 shapes touching exactly 2 shapes of layer2
result = layer1.interacting(layer2, 2, 2)
```

---

## Working with Edges

### Get Edges

```ruby
# Get all edges of a layer
edges = layer.edges

# Get edges at specific angle
horizontal_edges = layer.edges.with_angle(0, absolute)
vertical_edges = layer.edges.with_angle(90, absolute)
diagonal_45 = layer.edges.with_angle(45, absolute)
```

### Edge Filtering

```ruby
# Filter edges by length
short_edges = layer.edges.with_length(0, 0.5.um)  # 0 to 0.5um
long_edges = layer.edges.with_length(10.um, nil)   # 10um or more

# Filter edges by angle range
angled = layer.edges.with_angle(44.5, 45.5, absolute)
```

### Edge-to-Edge Checks

```ruby
# Check space between edges
violations = layer.edges.sep(other_edges, value.um, euclidian)

# Example: 45-degree edge spacing
diagonal_edges = metal1_drw.edges.with_angle(45, absolute)
violations = metal1_drw.edges.sep(diagonal_edges, 0.22.um, euclidian)
```

---

## Projection and Angles

### Projection Limits (Wide Metal Rules)

Used for rules that depend on parallel run length:

```ruby
# Check spacing only where parallel run exceeds threshold
projection_limits(min_length, max_length)
```

**Example: Wide Metal Spacing Rule**

```ruby
# M1.e: If metal > 0.3um wide AND parallel run > 1.0um, space >= 0.22um
m1_e_value = 0.22      # Required spacing
m1_e_width = 0.15      # Half of width threshold (0.3/2)
m1_e_length = 1.0      # Parallel run threshold

# Select wide metal (shrink then grow back)
wide_metal = metal1_drw.sized(-m1_e_width.um).sized(m1_e_width.um)

# Check sep with projection limits
violations = metal1_drw.sep(wide_metal, m1_e_value.um,
                           projection_limits(m1_e_length.um + 0.001.um, nil))
violations.output('M1.e', "Wide metal spacing rule")
violations.forget
wide_metal.forget
```

### Angle Filtering

```ruby
# Absolute angles (relative to layout X-axis)
.with_angle(0, absolute)     # Horizontal
.with_angle(90, absolute)    # Vertical
.with_angle(45, absolute)    # 45-degree

# Angle ranges
.with_angle(44.5, 45.5, absolute)  # Range around 45 degrees
```

---

## Output and Logging

### Logging

```ruby
logger.info("Message")   # Informational
logger.warn("Message")   # Warning
logger.error("Message")  # Error
```

### Output Violations

```ruby
# Basic output
violations.output('Rule.ID', "Description")

# With dynamic values
violations.output('M1.a', "Min. Metal1 width: #{value} um")
violations.output("M#{met_no}.a", "Metal#{met_no} width: #{value} um")
```

---

## Memory Management

**CRITICAL**: Always call `.forget` on intermediate results!

```ruby
# BAD - memory leak
temp1 = layer1.sized(-0.1.um)
temp2 = temp1.sized(0.1.um)
result = temp2.and(layer2)
result.output('Rule.x', "Description")
# temp1, temp2 still consuming memory!

# GOOD - proper cleanup
temp1 = layer1.sized(-0.1.um)
temp2 = temp1.sized(0.1.um)
temp1.forget  # Free temp1
result = temp2.and(layer2)
temp2.forget  # Free temp2
result.output('Rule.x', "Description")
result.forget  # Free result
```

### Pattern: Chain with Cleanup

```ruby
# Create intermediate results
step1 = layer.sized(-value.um)
step2 = step1.sized(value.um)
step1.forget

# Do check
violations = step2.sep(other_layer, space.um, euclidian)
step2.forget

# Output and cleanup
violations.output('Rule.x', "Description")
violations.forget
```

---

## Common Patterns

### Pattern 1: Simple Width/Space Check

```ruby
# Rule X.a: Min. width
logger.info('Executing rule X.a')
x_a_value = drc_rules['X_a'].to_f
x_a_l = layer_drw.width(x_a_value.um, euclidian)
x_a_l.output('X.a', "Min. width: #{x_a_value} um")
x_a_l.forget

# Rule X.b: Min. space
logger.info('Executing rule X.b')
x_b_value = drc_rules['X_b'].to_f
x_b_l = layer_drw.space(x_b_value.um, euclidian)
x_b_l.output('X.b', "Min. space: #{x_b_value} um")
x_b_l.forget
```

### Pattern 2: Enclosure Check

```ruby
# Via must be enclosed by metal
logger.info('Executing rule V1.c')
v1_c_value = drc_rules['V1_c'].to_f
v1_c_l = via1_drw.enclosed(metal1_drw, v1_c_value.um, euclidian)
v1_c_l.output('V1.c', "Min. Via1 enclosure by Metal1: #{v1_c_value} um")
v1_c_l.forget
```

### Pattern 3: Wide Metal Rule (with Size/Shrink)

```ruby
# Select wide shapes using size/shrink technique
logger.info('Executing rule M1.e')
threshold = drc_rules['M1_e_w'].to_f / 2
space = drc_rules['M1_e'].to_f
run_length = drc_rules['M1_e_cr'].to_f

# Shapes wider than 2*threshold survive shrink+grow
wide_shapes = metal1_drw.sized(-threshold.um).sized(threshold.um)

violations = metal1_drw.sep(wide_shapes, space.um,
                           projection_limits(run_length.um + 0.001.um, nil))
violations.output('M1.e', "Wide metal spacing")
wide_shapes.forget
violations.forget
```

### Pattern 4: Templated Rules (Loop)

```ruby
# Apply same rule to multiple layers
mets_lay = [metal2_drw, metal3_drw, metal4_drw, metal5_drw]
metal_start_index = 2

mets_lay.each_with_index do |met_lay, index|
  met_no = index + metal_start_index

  # Rule Mn.a: Min. width
  logger.info("Executing rule M#{met_no}.a")
  mn_a_value = drc_rules['Mn_a'].to_f
  mn_a_l = met_lay.width(mn_a_value.um, euclidian)
  mn_a_l.output("M#{met_no}.a", "Min. Metal#{met_no} width: #{mn_a_value} um")
  mn_a_l.forget
end
```

### Pattern 5: Conditional Derivation

```ruby
# Only compute if needed (saves time/memory)
if TABLES.include?('cont') || TABLES.include?('contbar') || FEOL
  cont_nseal = cont_drw.not(edgeseal_drw)
  contbar = cont_nseal.non_squares
  cont_sq = cont_nseal.not(contbar)
  cont_nseal.forget
end
```

---

## Next Steps

- See [03_LAYER_DEFINITIONS.md](./03_LAYER_DEFINITIONS.md) for layer system
- See [04_CREATING_NEW_RULES.md](./04_CREATING_NEW_RULES.md) for adding new rules
