# SRAM validation

`validate_sram.py` checks the consistency and basic functionality of the SRAM
deliverables in `ihp-sg13g2/libs.ref/sg13g2_sram`.

## Checks

- Every SRAM macro is present in CDL, documentation, GDS, LEF, Liberty, and
  Verilog views.
- Each macro has fast, slow, and typical Liberty corners.
- Macro names, ports, address widths, and data widths agree across views.
- GDS top-cell names and pin labels agree with the Verilog interface.
- Each Verilog model has exactly one `` `timescale 1ns/10ps`` directive.
- `A_DLY` and `B_DLY` are passed through, never tied to constants, documented
  as tie-high inputs, and checked during simulation.
- Every functional Verilog model compiles with and without `SYNTHESIS` defined.
- Runtime smoke tests exercise DLY error handling and 64x16 SRAM write/read
  behavior.

## Running locally

From the repository root:

```sh
make test-SRAM
```

The validator requires Python 3, [gdstk](https://pypi.org/project/gdstk/), and
Icarus Verilog (`iverilog` and `vvp`). For environments without all tools,
`--skip-gds` and `--skip-verilog` can be used for a reduced check:

```sh
python3 ihp-sg13g2/libs.qa/sram/validate_sram.py --skip-gds
```

GitHub Actions runs the complete check automatically when files in the SRAM
library or its validation workflow change.

## Scope

This check catches packaging, interface, and functional-model regressions. It
does not validate electrical characterization data and does not replace DRC,
LVS, or silicon qualification.

The validator was generated with OpenAI Codex (GPT-5).
