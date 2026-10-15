# IHP Common Library

Content shared by more than one PDK in this repository. It mirrors the
open-pdks directory structure, but it is **not a PDK**: files a working PDK
needs are deliberately absent, so this directory can never be used as `$PDK`.

What belongs here:

* Data that is identical across PDKs. The SRAM cells, for example, are the
  same in SG13G2 and SG13CMOS5L.
* PDK-aware scripts and build rules that would otherwise be duplicated.

Anything specific to a single PDK stays in that PDK.
