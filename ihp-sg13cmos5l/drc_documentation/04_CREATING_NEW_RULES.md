# Creating New DRC Rules

## Table of Contents
1. [Overview](#overview)
2. [Step-by-Step Guide](#step-by-step-guide)
3. [Adding a Simple Rule](#adding-a-simple-rule)
4. [Adding a Complex Rule](#adding-a-complex-rule)
5. [Creating a New Rule File](#creating-a-new-rule-file)
6. [Adding Parameters to JSON](#adding-parameters-to-json)
7. [Testing Your Rules](#testing-your-rules)
8. [Best Practices](#best-practices)

---

## Overview

There are three ways to add new DRC rules:

1. **Add to existing rule file** - For rules related to existing layers
2. **Create new rule file** - For new layer categories
3. **Modify derived layers** - For rules requiring new computations

### Prerequisites

- Understanding of KLayout DRC Ruby API
- Knowledge of the layer being checked
- Rule specification (width, space, enclosure values)

---

## Step-by-Step Guide

### Quick Checklist

1. [ ] Identify the layer(s) involved
2. [ ] Determine rule type (width, space, enclosure, etc.)
3. [ ] Get rule values (from design manual or specification)
4. [ ] Choose target file (existing or new)
5. [ ] Add parameter to JSON (if parameterized)
6. [ ] Write the rule code
7. [ ] Test with sample layout
8. [ ] Verify violations are reported correctly

---

## Adding a Simple Rule

### Example: Add Min Width Rule to Metal5

**Goal**: Add rule M5.a - Minimum Metal5 width of 0.20um

#### Step 1: Identify Target File

Metal5 uses the templated `5_17_metaln.drc`, but for a standalone rule:
- Could add to main entry `ihp-sg13g2.drc`
- Or create `5_17b_metal5_custom.drc`

#### Step 2: Add Parameter to JSON

Edit `rule_decks/sg13g2_tech_default.json`:

```json
{
  "drc_rules": {
    ...
    "M5_a_custom": 0.20,
    ...
  }
}
```

#### Step 3: Write the Rule

```ruby
# In appropriate location (after layer definitions)

if TABLES.include?('metal5') || BEOL
  # Rule M5.a_custom: Min. Metal5 width is 0.20um
  logger.info('Executing rule M5.a_custom')
  m5_a_value = drc_rules['M5_a_custom'].to_f
  m5_a_l = metal5_drw.width(m5_a_value.um, euclidian)
  m5_a_l.output('M5.a_custom', "Custom M5.a: Min. Metal5 width: #{m5_a_value} um")
  m5_a_l.forget
end
```

#### Step 4: Test

```bash
python run_drc.py --layout=test.gds --table=metal5 -o test_results.lyrdb
```

---

## Adding a Complex Rule

### Example: Add Custom Enclosure Rule

**Goal**: Via2 must be enclosed by Metal2 by at least 0.05um on all sides

#### Step 1: Understand the Check

- **Layer 1**: Via2 (GDS 29/0) - `via2_drw`
- **Layer 2**: Metal2 (GDS 10/0) - `metal2_drw`
- **Check type**: Enclosure
- **Value**: 0.05um

#### Step 2: Add Parameter

```json
{
  "drc_rules": {
    ...
    "V2_enc_custom": 0.05,
    ...
  }
}
```

#### Step 3: Write the Rule

```ruby
if TABLES.include?('vian') || BEOL
  # Custom Rule: Via2 enclosure by Metal2
  logger.info('Executing custom V2 enclosure rule')
  v2_enc_value = drc_rules['V2_enc_custom'].to_f

  # Check that via2 is enclosed by metal2
  v2_enc_l = via2_drw.enclosed(metal2_drw, v2_enc_value.um, euclidian)
  v2_enc_l.output('V2.enc_custom',
    "Custom: Min. Via2 enclosure by Metal2: #{v2_enc_value} um")
  v2_enc_l.forget
end
```

### Example: Wide Metal Spacing Rule

**Goal**: If Metal3 is wider than 2um, spacing must be at least 0.5um

```ruby
if TABLES.include?('metaln') || BEOL
  # Custom Wide Metal3 Rule
  logger.info('Executing custom M3 wide spacing rule')

  wide_threshold = 1.0  # Half of 2um (for shrink/grow technique)
  spacing = 0.5

  # Select wide metal (shapes that survive shrink then grow)
  m3_wide = metal3_drw.sized(-wide_threshold.um).sized(wide_threshold.um)

  # Check spacing between any M3 and wide M3
  violations = metal3_drw.sep(m3_wide, spacing.um, euclidian)
  violations.output('M3.wide_custom',
    "Custom: Wide Metal3 (>2um) spacing: #{spacing} um")

  # Cleanup
  m3_wide.forget
  violations.forget
end
```

---

## Creating a New Rule File

### When to Create New File

- New layer category not in existing files
- Significant number of related rules
- Custom/project-specific rules you want to isolate

### File Template

```ruby
# frozen_string_literal: true

#=========================================================================================
# Copyright 2025 IHP PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# ...
#=========================================================================================

if TABLES.include?('custom_layer') || FEOL  # or BEOL
  #================================================
  #------------- Custom Layer Rules ---------------
  #================================================

  logger.info('Starting Custom Layer table')

  # ==========================================
  # Derivations (if needed)
  # ==========================================

  # custom_derived = layer1.and(layer2)

  # ==========================================
  # Rules
  # ==========================================

  # Rule CL.a: Min. width
  logger.info('Executing rule CL.a')
  cl_a_value = drc_rules['CL_a'].to_f
  cl_a_l = custom_layer_drw.width(cl_a_value.um, euclidian)
  cl_a_l.output('CL.a', "Custom Layer min width: #{cl_a_value} um")
  cl_a_l.forget

  # Rule CL.b: Min. space
  logger.info('Executing rule CL.b')
  cl_b_value = drc_rules['CL_b'].to_f
  cl_b_l = custom_layer_drw.space(cl_b_value.um, euclidian)
  cl_b_l.output('CL.b', "Custom Layer min space: #{cl_b_value} um")
  cl_b_l.forget

  # ==========================================
  # Cleanup derivations
  # ==========================================

  # custom_derived.forget

end
```

### Registering the New File

Add include to main entry (`ihp-sg13g2.drc`):

```ruby
#================================================
#------------------- INCLUDES -------------------
#================================================

# ... existing includes ...

# Custom rules
# %include rule_decks/custom/custom_layer.drc
```

### Adding to Table Discovery

The table name is extracted from the filename:
- File: `99_1_custom_layer.drc`
- Table name: `custom_layer`

`run_drc.py` auto-discovers files in `feol/` and `beol/` directories.

---

## Adding Parameters to JSON

### Parameter Naming Convention

```
LayerPrefix_RuleLetter[_suffix]

Examples:
  M1_a         = Metal1 rule 'a' (typically width)
  M1_b         = Metal1 rule 'b' (typically space)
  M1_e         = Metal1 rule 'e' (wide spacing)
  M1_e_w       = Width threshold for M1.e
  M1_e_cr      = Critical length (parallel run) for M1.e
```

### JSON Structure

```json
{
  "drc_rules": {
    "ExistingRule": 0.16,

    "NewRule_a": 0.20,
    "NewRule_b": 0.25,
    "NewRule_c": 0.10,
    "NewRule_c_threshold": 2.0
  }
}
```

### Reading Parameters in Rules

```ruby
# Simple parameter
value = drc_rules['NewRule_a'].to_f

# With default fallback
value = (drc_rules['NewRule_a'] || 0.20).to_f

# Multiple related parameters
width = drc_rules['NewRule_c'].to_f
threshold = drc_rules['NewRule_c_threshold'].to_f
```

---

## Testing Your Rules

### Method 1: Command Line

```bash
# Test specific table
python run_drc.py --layout=test.gds --table=custom_layer -o results.lyrdb

# View results in KLayout
klayout test.gds -e &
# Then: Tools > Marker Browser > Load results.lyrdb
```

### Method 2: Create Test GDS

Create a GDS with known violations:

```
test_custom_rule.gds
├── Cell: test_width_violation
│   └── Shape narrower than min width
├── Cell: test_space_violation
│   └── Two shapes too close
└── Cell: test_passing
    └── Shapes meeting all rules
```

### Method 3: Regression Testing

Add to `testing/testcases/`:

```
testcases/
├── custom_layer/
│   ├── custom_layer_test.gds
│   └── custom_layer_test.gds.lyrdb.golden
```

Run regression:
```bash
python testing/run_regression.py
```

### Debugging Tips

1. **Add logging**:
```ruby
logger.info("Debug: value = #{value}")
logger.info("Debug: layer count = #{layer.count}")
```

2. **Check intermediate results**:
```ruby
# Temporarily output intermediate layer
temp_result.output('DEBUG.temp', "Debug: intermediate result")
```

3. **Verify layer reading**:
```ruby
logger.info("metal5_drw polygon count: #{metal5_drw.count}")
```

---

## Best Practices

### 1. Always Use Parameters

```ruby
# BAD - hardcoded value
violations = layer.width(0.16.um, euclidian)

# GOOD - parameterized
value = drc_rules['Layer_a'].to_f
violations = layer.width(value.um, euclidian)
```

### 2. Always Free Memory

```ruby
# ALWAYS call .forget on results
violations.output('Rule.x', "Description")
violations.forget

# And on intermediate results
temp = layer1.and(layer2)
result = temp.width(value.um, euclidian)
temp.forget  # Free intermediate
result.output('Rule.x', "Description")
result.forget
```

### 3. Use Meaningful Rule IDs

```ruby
# BAD - unclear
violations.output('R1', "Some rule")

# GOOD - follows convention
violations.output('M3.custom_enc', "Metal3 custom enclosure: 0.1um")
```

### 4. Include Context in Messages

```ruby
# BAD - no context
violations.output('M1.a', "Width check")

# GOOD - full context
violations.output('M1.a', "5.16. M1.a: Min. Metal1 width: #{value} um")
```

### 5. Guard with Table Checks

```ruby
# GOOD - only runs when needed
if TABLES.include?('metal1') || BEOL
  # Rule code here
end
```

### 6. Use Conditional Derivations

```ruby
# GOOD - compute only if needed
if TABLES.include?('custom') || TABLES.include?('related')
  expensive_derivation = layer1.and(layer2).not(layer3)
end
```

### 7. Log Rule Execution

```ruby
# GOOD - helps with debugging
logger.info('Executing rule X.y')
```

---

## Common Rule Patterns

### Pattern: Minimum Width

```ruby
logger.info('Executing rule X.a')
x_a = drc_rules['X_a'].to_f
violations = layer_drw.width(x_a.um, euclidian)
violations.output('X.a', "Min. width: #{x_a} um")
violations.forget
```

### Pattern: Minimum Spacing

```ruby
logger.info('Executing rule X.b')
x_b = drc_rules['X_b'].to_f
violations = layer_drw.space(x_b.um, euclidian)
violations.output('X.b', "Min. space: #{x_b} um")
violations.forget
```

### Pattern: Enclosure

```ruby
logger.info('Executing rule X.c')
x_c = drc_rules['X_c'].to_f
violations = inner_layer.enclosed(outer_layer, x_c.um, euclidian)
violations.output('X.c', "Min. enclosure: #{x_c} um")
violations.forget
```

### Pattern: Separation Between Layers

```ruby
logger.info('Executing rule X.d')
x_d = drc_rules['X_d'].to_f
violations = layer1.sep(layer2, x_d.um, euclidian)
violations.output('X.d', "Min. separation: #{x_d} um")
violations.forget
```

### Pattern: Area Check

```ruby
logger.info('Executing rule X.e')
x_e = drc_rules['X_e'].to_f
violations = layer_drw.with_area(0, x_e.um2)  # Shapes smaller than min
violations.output('X.e', "Min. area: #{x_e} um^2")
violations.forget
```

### Pattern: Count Check

```ruby
logger.info('Executing rule X.f')
# Check that via has at least N contacts
min_contacts = drc_rules['X_f'].to_i
via_with_few = via_layer.select { |v| contact_layer.interacting(v).count < min_contacts }
via_with_few.output('X.f', "Min. #{min_contacts} contacts per via")
via_with_few.forget
```

---

## Next Steps

- See [05_QUICK_REFERENCE.md](./05_QUICK_REFERENCE.md) for quick lookup
- Review existing rules in `rule_decks/` for more examples
