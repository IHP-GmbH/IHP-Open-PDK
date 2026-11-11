# IHP Common Library

Content shared by more than one PDK in this repository. It mirrors the
open-pdks directory structure, but it is **not a PDK**: files a working PDK
needs are deliberately absent, so this directory can never be used as `$PDK`.

What belongs here:

* Data that is identical across PDKs. The SRAM cells, for example, are the
  same in SG13G2 and SG13CMOS5L.
* PDK-aware scripts and build rules that would otherwise be duplicated.

Anything specific to a single PDK stays in that PDK.

## Maximal DRC regression

`make test-DRC-main` also runs `libs.tech/klayout/tech/drc/testing/test_gat_b1_endcaps.py`,
which checks `Gat.b1` with the complete maximal deck of each PDK (the modular golden
suite does not cover maximal-only rules). To run it alone and keep the layouts and reports:

```bash
python3 ihp-common/libs.tech/klayout/tech/drc/testing/test_gat_b1_endcaps.py --pdk ihp-sg13g2 --run-dir /tmp/gat-b1
```
