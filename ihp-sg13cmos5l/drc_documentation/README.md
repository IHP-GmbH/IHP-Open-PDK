# IHP-SG13G2 DRC Documentation

This directory contains comprehensive documentation for understanding and extending the IHP-SG13G2 PDK's DRC (Design Rule Check) system.

## Documentation Files

| File | Description |
|------|-------------|
| [01_ARCHITECTURE_OVERVIEW.md](./01_ARCHITECTURE_OVERVIEW.md) | High-level system architecture, directory structure, execution flow |
| [02_RULE_FILE_SYNTAX.md](./02_RULE_FILE_SYNTAX.md) | Ruby DRC syntax, operations, edge handling, memory management |
| [03_LAYER_DEFINITIONS.md](./03_LAYER_DEFINITIONS.md) | Layer system, GDS mapping, derived layers, connectivity |
| [04_CREATING_NEW_RULES.md](./04_CREATING_NEW_RULES.md) | Step-by-step guide for adding custom rules |
| [05_QUICK_REFERENCE.md](./05_QUICK_REFERENCE.md) | Quick lookup card for common operations |

## Recommended Reading Order

1. **Start with Architecture** - Understand the overall system
2. **Learn Rule Syntax** - How to write DRC checks
3. **Understand Layers** - How layers are defined and derived
4. **Create New Rules** - Add your own custom rules
5. **Keep Quick Reference handy** - For day-to-day work

## Quick Links

### Running DRC

```bash
# Basic
python run_drc.py --layout=design.gds

# Specific tables
python run_drc.py --layout=design.gds --table=metal1 --table=via1

# With output file
python run_drc.py --layout=design.gds -o results.lyrdb
```

### File Locations

```
ihp-sg13g2/libs.tech/klayout/tech/drc/
├── ihp-sg13g2.drc              # Main entry point
├── run_drc.py                  # Python CLI
└── rule_decks/
    ├── layers_def.drc          # Layer definitions
    ├── sg13g2_tech_default.json # Rule parameters
    ├── feol/                   # FEOL rules (14 files)
    └── beol/                   # BEOL rules (19 files)
```

### Basic Rule Template

```ruby
logger.info('Executing rule X.y')
xy_value = drc_rules['X_y'].to_f
xy_l = layer_drw.width(xy_value.um, euclidian)
xy_l.output('X.y', "Description: #{xy_value} um")
xy_l.forget
```

## Slim PDK (ihp-sg13cmos5l)

The slim PDK is a subset of the full PDK with:
- CMOS devices only (no HBT/bipolar)
- Metal stack M1-M5 (no TopMetal1/2)
- Reduced DRC rule set

See the [slim PDK DRC](../ihp-sg13cmos5l/libs.tech/klayout/tech/drc/) for the adapted version.

## Contributing

When adding new rules:
1. Follow naming conventions (see Quick Reference)
2. Add parameters to JSON file
3. Use proper memory management (`.forget`)
4. Add test cases
5. Update documentation if needed
