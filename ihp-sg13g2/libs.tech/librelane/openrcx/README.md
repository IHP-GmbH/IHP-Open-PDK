# OpenRCX rules for SG13G2

* `IHP_rcx_patterns.rules` — rules file provided by IHP (used by default)
* `ihp-sg13g2.{min,nom,max}.magic.rules` — generated with magic as
  reference extractor
* `sg13g2.{TYP,MIN,MAX}.process` — layer stack from
  `SG13G2_os_process_spec.pdf` Rev. 1.2 (Fig. 1.1.1/1.1.2, corner tables
  3.1, 3.2, 3.7), input for the shared FasterCap flow
  (`ihp-common/libs.tech/librelane/openrcx/README.md`):

  ```
  ./gen_rcx_model.sh sg13g2.TYP.process
  ```

  Comparing its output against `IHP_rcx_patterns.rules` validates the flow
  before it is trusted for SG13G2CMOS5L, whose Metal1..Metal4 stack is
  identical.
