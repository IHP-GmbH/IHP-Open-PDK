# Gnucap Verilog-A/AMS Style Guide

Use these conventions for new and refactored PDK sources and tests within
`gnucap/`. 

## File headers

Use two layered headers in module, corner, and paramset sources: 
1. Apache-2.0 license block
2. an optional file-content banner. 

Apply rules consistently across `.va` files in `gnucap/models/`.

### License header

```text
//******************************************************************************
//
// Copyright <YEAR> IHP PDK Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     https://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
//******************************************************************************
```
### File-Content banner

An optional purpose banner sits immediately after the license block.
Its interior follows a fixed three-block order, separated by blank `//` lines:

1. A single purpose line naming the file's content, such as
  `// Resistor corner modules` or `// SG13G2 MOSLV paramsets`.
2. An attribution line beginning `// Adapted from `and pointing to the relevant 
   Ngspice source path or library name, for example 
  `// Adapted from ngspice/models/cornerRES.lib.`
3. An optional `// Modifications:` block followed by `- <change>` bullets,
   one bullet per line.

```text
//******************************************************************************
// Resistor corner modules
//
// Adapted from ngspice/models/cornerRES.lib
//
// Modifications:
// - Removed mismatch corners; mismatch is implemented in paramsets
// - Renamed dw_par_* and mismatch parameters for consistency
//******************************************************************************
```

## Organization and responsibilities

- Use `models/` directory for device modules and corner definitions: 
  - Device modules (`<device_name>_module.va`): connect primitive instances into 
    composite PDK devices and expose their ports and parameters for use in 
    circuits and testbenches.
  - Corner modules (`corner<NAME>.va`): own and provide global process-dependent 
    parameter values for deterministic and statistical corners. 

- Use `models/paramset` directory for PDK primitives:
  - Give each primitive its own file `<device_name>.va` containing its paramset
    declaration. A paramset selects a generic compact model, assigns
    device-specific model parameter values, and declares the parameters that 
    users can set during instantiation.
  - Paramsets should own the primitives' local mismatch implementation. For 
    primitives with mismatch support, provide two overloaded paramset 
    declarations in the same file; one without and one with mismatch.
  - Optional: Group related device primitives that share a compact model in a
    family file `<family_name>_paramset.va`. This file includes the compact-model
    source and device-specific paramsets and is used to build a family device 
    plugin. 

## Intended use

- User loads `plugins/models/` directory to make primitive devices available 
  to the simulator:
  ```text 
  load ./plugins/models/      
  ```
- User includes `models/` directory to make composite devices and corners
  available to the simulator:
  ```verilog
   `include ./models/;
  ```
- Select corners by instantiating the desired corner modules in the testbench:
  ```verilog
  res_typ corner_res();
  ```
  Corner instances must match the hierarchical references used by the paramsets. 
  Use the naming convention `corner_<family>`   

- For convenience, collect common corner combinations in reusable include files. 
- For example, typical corners for several device families.
  ```verilog
  moslv_tt corner_moslv();
  res_typ corner_res();
  cap_typ corner_cap();
   //...
   ```

## Device modules

```verilog
(* desc = "cap_cmim capacitor module" *)
module cap_cmim(plus, minus);
    inout plus, minus;
    electrical plus, minus;

    electrical n1;

    (* desc = "Device width",  units = "m" *)
    parameter real w = 7u from [7u:75u];
    (* desc = "Device length", units = "m" *)
    parameter real l = 7u from [7u:75u];
    (* desc = "Enable mismatch" *)
    parameter integer mm_ok = 0 from [0:1];

    resistor #(.r(55m)) R1(plus, n1);
    cmim_core #(.l(l), .w(w), .mm_ok(mm_ok)) C1(n1, minus);
endmodule
```
### Structure
 
- Module header:
  - Use the device name from ngspice reference `subckt`
  - Preserve terminal order and use lowercase port names
- Body, in order:
  1. Port direction and discipline declarations 
  2. Internal node declarations, separated from ports by a blank line. 
  3. Public `parameter` declarations, in ngspice reference order  
  4. Private constants and derived `localparam` declarations, in dependency order. 
  5. Device instances in their connections 

Separate these groups with blank lines. 

## Paramsets

```verilog
(* desc = "cmim_core capacitor paramset, without mismatch" *)
paramset cmim_core sp_capacitor
    (* desc = "Device length", units = "m" *)
    parameter real l = 7.0u;
    (* desc = "Device width",  units = "m" *)
    parameter real w = 7.0u;
    (* desc = "Enable mismatch" *)
    parameter integer mm_ok = 0 from [0:0];
    
    .l = l;
    .w = w;
    .scale = 1;
    .tnom = 27.0;
    .tc1 = 3.6E-6;
    .tc2 = 2E-9;
    .cj = corner_cap.cap_carea;
    .cjsw = 40E-12; 
endparamset
```

### Structure

- Paramset header:
  - Use the device name from ngspice modelcard
- Body, in order: 
  1. Public `parameter` declarations, in ngspice reference order
  2. Private constants and derived `localparam` declarations, in dependency order.  
  3. Model parameter assignments `.name = value`, in modelcard order. Only 
  assigned model parameters influence model behavior.

Separate these groups with blank lines. 

## Parameters 

### `parameter`

- Format default values with engineering suffixes or scientific notation. 
- Specify parameter ranges when known.
- Add a `desc` attribute to document parameters.
- Add `units` attribute to parameters representing physical quantities.

```verilog
(* desc = "Device width", units = "m" *)
parameter real w = 0.5u from [0.5u:10u);
```

### `localparam`

```verilog
(* desc = "Device width", units = "m" *)
parameter real w = 0.35u;
(* desc = "Number of fingers" *)
parameter integer ng = 1 from [1:inf);

localparam real wf = w / ng;
```

- `desc` attributes for local parameters are optional. Use them to document 
  non-obvious calculations or scaling where useful. 

## Formatting

- Indent module and paramset bodies with four spaces. 
- Use spaces around operators and `=`, and after commas. 
- By default, put each declaration or assignment on its own line.
- Use single spacing, allowing column alignment for related declarations.
- Use **80 characters per line** as the boundary, with exceptions where necessary.

### Column alignment

Use column alignment inside groups of related declarations so long lists stay
visually scannable. The `moshv_tt_stat()` module in `cornerMOShv.va` is the
canonical example.

- **Align identifiers and operators within a block.** Pad each
  recurring identifier or operator so it falls on a fixed column across
  the lines of one block.
- **Pad after commas, not before.** In calls like `$rdist_normal(...)`,
  add spaces after each `,` to push the next argument to its column. Do
  not pad variable names and do not widen numeric operands.
- **One block per concept.** Keep alignment local to one role (nominal,
  sigma, sampled) and one family (nmos or pmos).
- **Precision and outliers.** Pad short decimals (`1.0` → `1.0000`). If a
  line would exceed 80 characters, drop the line or split the group.

```verilog
// nominal values - aligned LHS, equal-width decimals
localparam real sg13g2_hv_nmos_vfbo_nomv= 1.0;
localparam real sg13g2_hv_nmos_rsgo_nomv= 1.0000;
localparam real sg13g2_hv_nmos_rsw1_nomv= 0.7886;
localparam real sg13g2_hv_nmos_mueo_nomv= 1.0780;

// sigmas - aligned LHS and RHS multiplier
localparam real sg13g2_hv_nmos_vfbo_sig = 0.004  * sg13g2_hv_nmos_vfbo_nom;
localparam real sg13g2_hv_nmos_rsgo_sig = 1e-9   * sg13g2_hv_nmos_rsgo_nom;
localparam real sg13g2_hv_nmos_rsw1_sig = 0.0001 * sg13g2_hv_nmos_rsw1_nom;

// sampled values - aligned LHS, comma column inside $rdist_normal
localparam real sg13g2_hv_nmos_vfbo    = sg13g2_hv_nmos_vfbo_nom    + $rdist_normal(seed + 1,  0.0, sg13g2_hv_nmos_vfbo_sig,    "global");
localparam real sg13g2_hv_nmos_rsgo    = sg13g2_hv_nmos_rsgo_nom    + $rdist_normal(seed + 2,  0.0, sg13g2_hv_nmos_rsgo_sig,    "global");
localparam real sg13g2_hv_nmos_thesato = sg13g2_hv_nmos_thesato_nom + $rdist_normal(seed + 10, 0.0, sg13g2_hv_nmos_thesato_sig, "global");
```

Each block above is its own conceptual group (nominal, sigma, sampled);
they are intentionally not aligned to one another.

### Line breaks in device instantiation

When a device instantiation exceeds the 80-character line limit, split it
across multiple lines using the backslash `\` line-continuation marker. Apply
this consistently for both the parameter list and the port list:

- Use `\` at the end of every broken line so the simulator treats the
  fragments as a single logical line.
- Place the opening `<module>` and `#(` on the first line, with `\` immediately
  after `#(`.
- Put each named parameter on its own line, indented by four spaces, with
  `, \` after every parameter including the last (`))` is on the closing
  parameter line).
- Place the closing `))` on the same line as the final parameter, then `\` and
  the instance name with its port list on a separate line, indented to match
  the module body.

```verilog
sg13g2_lv_nmos_psp #( \
    .w(w), \
    .l(l), \
    .ng(ng), \
    .m(m), \
    .as(as), \
    .ad(ad), \
    .ps(ps), \
    .pd(pd), \
    .trise(trise), \
    .delvto(0.0), \
    .factuo(1.0), \
    .pre_layout(pre_layout), \
    .rfmode(rfmode)) \
sg13_lv_nmos(d, g, s, b);
```

## Naming

- Preserve reference PDK identifiers for device, ports and parameters by default.
- Omit simulator-specific instance prefixes, such as `X` for subcircuits and 
  `N` for OSDI
- For new identifiers use descriptive `lower_snake_case`  

## Global process variation

Implement global process variation and use a statistical corner module. 
Randomize parameters with `$rdist_*` functions, using the "global" type_string
argument, which ensures that the same random value is used by every parameter
referenced by each device instance.

```verilog
(* desc = "statistical resistor corner" *)
module res_stat();
    parameter integer seed = 1;
    // rsil
    localparam real rsh_rsil = 7.0;
    localparam real dw_par_rsil = 0.01e-6;
    localparam real nsig_rsh_rsil = $rdist_normal(seed,   0, 1, "global");
    localparam real nsig_w_rsil   = $rdist_normal(seed+1, 0, 1, "global");
    localparam real nsig_l_rsil   = $rdist_normal(seed+2, 0, 1, "global");
    //...
endmodule
```

Optionally, we could use a `stat_ok` switch on supported corner configurations,
defaulting to zero. This has the advantage that nominal values are one place and
don't need to be dupicated. We could use a ternary to select nominal or sampled
values

```verilog
(* desc = "Enable global process variation" *)
parameter integer stat_ok = 0 from [0:1];

localparam real vfbo = stat_ok
    ? vfbo_nom + $rdist_normal(seed + 1, 0.0, vfbo_sig, "global")
    : vfbo_nom;
```

## Local mismatch variation

Implement local mismatch variation for primitive devices in their paramsets. 
Use `localparam` declarations together with `$rdist_*` functions to generate
instance-specific random values. Pass the "instance" type_string argument to
`$rdist_*` to ensure that each instance receives a different random value.

Then use these values in model parameter assignments.   

```verilog
// with mismatch
paramset npn13G2_NX_vbic vbic13_4t
    parameter integer mm_ok = 1 from [1:1];
    parameter integer Nx = 1 from [1:10];
    parameter real dtemp = 0.0;
    parameter real selft = 1.0;
    parameter integer sw_nqs = 0 from [0:1];
    localparam real Nx_scale = 0.25 * Nx;
    localparam real inv_Nx_scale = 1.0 / Nx_scale;
    // mismatch
    localparam real mm_scale = 1.0 / sqrt(Nx);
    localparam real mm_vbic_cje = mm_scale * $rdist_normal(1, 0.0, 0.017, "instance");
        
    .cje = 8.418E-15 * pow(Nx_scale, 0.975) * corner_hbt.vbic_cje * (1 + mm_vbic_cje);
    // ...
endparamset

```

## Process variation and mismatch

Following the Ngspice PDK terminology, **`stat` means global process variation**
and **`mm` means local device mismatch**, although both are statistical effects.
Use `_nom` for nominal values, `_sig` for standard deviations, and `_mm` for
mismatch-specific quantities; explain scaling where the name is insufficient.

## Tests

- Put reusable circuits in `tb_*.va` and corner selection, testbench instantiation,
  and simulation commands in `test_*.gc`.
- Use pattern `test_<device>_<type>[_<detail>][_<corner>].gc`.
- Types are `op`, `dc`, `ac`, `tran`, `mc_mm` (mismatch only), and
  `mc_stat` (global process variation only).
- Optional detail distinguishes tests such as `dc_id_vgs` and `dc_id_vds`.
  Preserve actual family corner names such as `typ` or `tt`.
- Corresponding Ngspice `.sp` drivers share the same basename. Reusable
  testbench names need not repeat analysis or corner information selected by
  the driver.

For example: `test_sg13_lv_nmos_dc_id_vgs_tt.gc` and its matching `.sp` driver.

During refactoring, update reference-output names and plotting references with
test renames, and includes/build dependencies with source moves. Run the affected
builds and regressions for code changes; verify numerical behavior when changing
calculations or variation handling. Documentation-only edits require document
and link checks rather than simulator regressions.
