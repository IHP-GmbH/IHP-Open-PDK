# IHP-SG13G2 DRC Architecture Overview

## Table of Contents
1. [Introduction](#introduction)
2. [Directory Structure](#directory-structure)
3. [Execution Flow](#execution-flow)
4. [Key Components](#key-components)
5. [Table-Based Execution](#table-based-execution)
6. [Switches and Configuration](#switches-and-configuration)

---

## Introduction

The IHP-SG13G2 DRC (Design Rule Check) system uses KLayout's Ruby-based DRC engine. It is a modular system organized into:
- **Main entry point** (`ihp-sg13g2.drc`)
- **Rule decks** (individual `.drc` files for each layer/category)
- **Layer definitions** (`layers_def.drc`)
- **Parameter values** (JSON configuration)

The DRC can be run via:
1. **KLayout GUI**: Tools > DRC
2. **Command line**: `python run_drc.py --layout=design.gds`

---

## Directory Structure

```
ihp-sg13g2/libs.tech/klayout/tech/drc/
├── ihp-sg13g2.drc              # Main entry point (468 lines)
├── run_drc.py                  # Python CLI runner (890 lines)
├── README.md                   # User documentation
│
├── rule_decks/
│   ├── layers_def.drc          # Layer definitions (~1700 lines)
│   ├── sg13g2_tech_default.json # Rule parameter values (376 params)
│   │
│   ├── feol/                   # Front-End-Of-Line rules (14 files)
│   │   ├── 5_1_nwell.drc
│   │   ├── 5_2_pwellblock.drc
│   │   ├── 5_3_nbulay.drc
│   │   ├── 5_5_activ.drc
│   │   ├── 5_6_activfiller.drc
│   │   ├── 5_7_thickgateox.drc
│   │   ├── 5_8_gatpoly.drc
│   │   ├── 5_9_gatpolyfiller.drc
│   │   ├── 5_10_psd.drc
│   │   ├── 5_14_cont.drc
│   │   ├── 5_15_contbar.drc
│   │   ├── 6_1_npnsubstratetie.drc  # HBT-specific
│   │   ├── 6_7_schottkydiode.drc    # Schottky-specific
│   │   └── 7_2_latchup.drc
│   │
│   ├── beol/                   # Back-End-Of-Line rules (19 files)
│   │   ├── 5_16_metal1.drc
│   │   ├── 5_17_metaln.drc         # M2-M5 (templated)
│   │   ├── 5_18_metalnfiller.drc
│   │   ├── 5_19_via1.drc
│   │   ├── 5_20_vian.drc           # Via2-4 (templated)
│   │   ├── 5_21_topvia1.drc
│   │   ├── 5_22_topmetal1.drc
│   │   ├── 5_23_topmetal1filler.drc
│   │   ├── 5_24_topvia2.drc
│   │   ├── 5_25_topmetal2.drc
│   │   ├── 5_26_topmetal2filler.drc
│   │   ├── 5_27_passiv.drc
│   │   ├── 6_9_copperpillar.drc
│   │   ├── 6_9_pad.drc
│   │   ├── 6_9_solderbump.drc
│   │   ├── 6_10_sealring.drc
│   │   ├── 6_11_mim.drc
│   │   ├── 7_3_metalslits.drc
│   │   └── 9_1_lbe.drc
│   │
│   ├── forbidden/              # Forbidden pattern rules
│   │   └── 3_2_forbidden.drc
│   │
│   └── pin/                    # Pin rules
│       └── 7_4_pin.drc
│
└── testing/
    ├── run_regression.py       # Regression test runner
    ├── gen_golden.py           # Generate golden references
    └── testcases/              # Unit test GDS files + golden refs
```

---

## Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        run_drc.py                               │
│  (Python CLI - parses arguments, calls KLayout)                 │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     ihp-sg13g2.drc                              │
│                    (Main Entry Point)                           │
├─────────────────────────────────────────────────────────────────┤
│ 1. Setup logging and file I/O                                   │
│ 2. Parse switches ($tables, $no_feol, $no_beol, etc.)          │
│ 3. Load layer definitions (%include layers_def.drc)            │
│ 4. Load DRC parameters from JSON                                │
│ 5. Compute common derivations (pwell, nactiv, pactiv, etc.)    │
│ 6. Setup connectivity (connect() statements)                    │
│ 7. Include rule decks based on TABLES variable                  │
│ 8. Output results to .lyrdb file                               │
└─────────────────────────┬───────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ FEOL     │    │ BEOL     │    │ Special  │
    │ Rules    │    │ Rules    │    │ Rules    │
    └──────────┘    └──────────┘    └──────────┘
```

### Detailed Flow

1. **Python Runner (`run_drc.py`)**:
   - Parses command-line arguments
   - Validates input files
   - Sets up KLayout environment variables (`$input`, `$report`, `$tables`, etc.)
   - Invokes KLayout with the main DRC deck

2. **Main Entry (`ihp-sg13g2.drc`)**:
   - Initializes logging
   - Loads the GDS/OAS file via `source($input)`
   - Evaluates switches to determine which rules to run
   - Loads layer definitions
   - Loads rule values from JSON
   - Computes derived layers (pwell, nactiv, etc.)
   - Sets up connectivity for net extraction
   - Includes individual rule decks via `%include`

3. **Rule Decks**:
   - Each rule deck contains related rules
   - Guarded by `if TABLES.include?('tablename') || FEOL/BEOL`
   - Executes checks and outputs violations

---

## Key Components

### 1. Global Variables (Passed from run_drc.py)

| Variable | Description | Example |
|----------|-------------|---------|
| `$input` | Input GDS/OAS file path | `/path/to/design.gds` |
| `$report` | Output .lyrdb file path | `/path/to/results.lyrdb` |
| `$topcell` | Top cell name (optional) | `TOP` |
| `$tables` | Space-separated table names | `"metal1 via1 cont"` |
| `$threads` | Number of parallel threads | `8` |
| `$run_mode` | Execution mode | `deep`, `flat`, `tiling` |
| `$no_feol` | Disable FEOL rules | `true`/`false` |
| `$no_beol` | Disable BEOL rules | `true`/`false` |
| `$precheck_drc` | Run only essential rules | `true`/`false` |

### 2. Key Ruby Constants

| Constant | Description |
|----------|-------------|
| `TABLES` | Array of selected table names |
| `FEOL` | Boolean - run all FEOL rules |
| `BEOL` | Boolean - run all BEOL rules |
| `PRECHECK_DRC` | Boolean - minimal rule set |
| `CONNECTIVITY_RULES` | Boolean - enable net extraction |

### 3. Layer Variables (from layers_def.drc)

Layers are read using the `get_polygons()` function:

```ruby
# Format: get_polygons(gds_layer, datatype)
activ_drw = get_polygons(1, 0)    # Activ drawing layer
metal1_drw = get_polygons(8, 0)   # Metal1 drawing layer
metal1_pin = get_polygons(8, 2)   # Metal1 pin layer
```

Naming convention:
- `*_drw` = drawing layer (datatype 0)
- `*_pin` = pin layer (datatype 2)
- `*_filler` = filler layer (datatype 22)
- `*_mask` = mask layer (datatype 20)
- `*_res` = resistor marker (datatype 29)

---

## Table-Based Execution

The DRC uses a **table** system to selectively run rules:

### Available Tables (from run_drc.py)

| Table | File | Category |
|-------|------|----------|
| `nwell` | 5_1_nwell.drc | FEOL |
| `pwellblock` | 5_2_pwellblock.drc | FEOL |
| `nbulay` | 5_3_nbulay.drc | FEOL |
| `activ` | 5_5_activ.drc | FEOL |
| `activfiller` | 5_6_activfiller.drc | FEOL |
| `thickgateox` | 5_7_thickgateox.drc | FEOL |
| `gatpoly` | 5_8_gatpoly.drc | FEOL |
| `gatpolyfiller` | 5_9_gatpolyfiller.drc | FEOL |
| `psd` | 5_10_psd.drc | FEOL |
| `cont` | 5_14_cont.drc | FEOL |
| `contbar` | 5_15_contbar.drc | FEOL |
| `metal1` | 5_16_metal1.drc | BEOL |
| `metaln` | 5_17_metaln.drc | BEOL |
| `metalnfiller` | 5_18_metalnfiller.drc | BEOL |
| `via1` | 5_19_via1.drc | BEOL |
| `vian` | 5_20_vian.drc | BEOL |
| `topvia1` | 5_21_topvia1.drc | BEOL |
| `topmetal1` | 5_22_topmetal1.drc | BEOL |
| `passiv` | 5_27_passiv.drc | BEOL |
| ... | ... | ... |

### How Tables Work

```ruby
# In rule file (e.g., 5_16_metal1.drc):
if TABLES.include?('metal1') || BEOL
  # Rules execute if:
  # 1. 'metal1' is in TABLES, OR
  # 2. BEOL is true (all BEOL rules enabled)

  # ... rule definitions ...
end
```

### Running Specific Tables

```bash
# Run only Metal1 and Via1 rules
python run_drc.py --layout=design.gds --table=metal1 --table=via1

# Run all FEOL rules
python run_drc.py --layout=design.gds --no_beol

# Run all BEOL rules
python run_drc.py --layout=design.gds --no_feol

# Run everything (default)
python run_drc.py --layout=design.gds --table=main
```

---

## Switches and Configuration

### Command Line Switches (run_drc.py)

```bash
python run_drc.py [OPTIONS]

Required:
  --layout, -l PATH       Input GDS/OAS layout file

Optional:
  --output, -o PATH       Output .lyrdb report file
  --topcell, -c NAME      Top cell name
  --table, -t NAME        Rule table to run (can repeat)
  --threads THREADS       Parallel thread count
  --run_mode MODE         'deep', 'flat', or 'tiling'
  --no_feol               Skip FEOL rules
  --no_beol               Skip BEOL rules
  --no_offgrid            Skip offgrid checks
  --no_pin                Skip pin rules
  --no_forbidden          Skip forbidden pattern rules
  --no_recommended        Skip recommended (non-critical) rules
  --precheck_drc          Run minimal essential rules only
  --mp                    Enable multiprocessing
```

### JSON Parameter File

Rule values are stored in `sg13g2_tech_default.json`:

```json
{
  "drc_rules": {
    "grid": 0.005,
    "M1_a": 0.16,      // Min. Metal1 width
    "M1_b": 0.18,      // Min. Metal1 space
    "M1_e": 0.22,      // Wide metal spacing
    "M1_e_w": 0.3,     // Width threshold for M1.e
    "M1_e_cr": 1.0,    // Parallel run threshold for M1.e
    ...
  }
}
```

**Naming Convention:**
- `LayerPrefix_rule` = rule value
- `LayerPrefix_rule_suffix` = associated parameter

**Common Prefixes:**
| Prefix | Layer/Rule Category |
|--------|---------------------|
| `NW` | NWell |
| `PWB` | PWell Block |
| `Act` | Activ |
| `Gat` | GatPoly |
| `Cnt` | Contact |
| `M1` | Metal1 |
| `Mn` | Metal2-5 |
| `V1` | Via1 |
| `Vn` | Via2-4 |
| `TM1` | TopMetal1 |
| `TM2` | TopMetal2 |
| `Mim` | MIM Capacitor |

---

## Next Steps

- See [02_RULE_FILE_SYNTAX.md](./02_RULE_FILE_SYNTAX.md) for rule writing syntax
- See [03_LAYER_DEFINITIONS.md](./03_LAYER_DEFINITIONS.md) for layer system details
- See [04_CREATING_NEW_RULES.md](./04_CREATING_NEW_RULES.md) for adding custom rules
