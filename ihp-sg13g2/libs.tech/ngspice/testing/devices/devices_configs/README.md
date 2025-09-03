# Device Configurations

This folder contains **per-device YAML configurations** and **ngspice netlist templates** for running SG13G2 device verification.
Each config defines the measurement data, model libraries, run settings, and output paths for one device type.

# Table of contents

* [Device Configurations](#device-configurations)
* [Table of contents](#table-of-contents)

  * [Folder Structure](#folder-structure)
  * [YAML Configuration](#yaml-configuration)

    * [Key Sections](#key-sections)



## Folder Structure

```text
📁 devices_configs
 ┣ 📁 mos
 ┃ ┣ 📜 cap_template.spice.j2   Template for MOS capacitance simulations.
 ┃ ┣ 📜 dc_template.spice.j2    Template for MOS DC sweeps.
 ┃ ┣ 📁 nmos_lv                 LV NMOS configuration.
 ┃ ┃ ┗ 📜 sg13_lv_nmos.yaml
 ┃ ┣ 📁 pmos_lv                 LV PMOS configuration.
 ┃ ┃ ┗ 📜 sg13_lv_pmos.yaml
 ┃ ┣ 📁 nmos_hv                 HV NMOS configuration.
 ┃ ┃ ┗ 📜 sg13_hv_nmos.yaml
 ┃ ┗ 📁 pmos_hv                 HV PMOS configuration.
 ┃   ┗ 📜 sg13_hv_pmos.yaml
 ┣ 📁 hbt
 ┃ ┣ 📜 hbt_dc.spice.j2         Template for HBT DC sweeps.
 ┃ ┣ 📁 npn13g2                 NPN13G2 configuration.
 ┃ ┃ ┗ 📜 npn13g2.yaml
 ┃ ┣ 📁 npn13g2l                NPN13G2L configuration.
 ┃ ┃ ┗ 📜 npn13g2l.yaml
 ┃ ┗ 📁 npn13g2v                NPN13G2V configuration.
 ┃   ┗ 📜 npn13g2v.yaml
 ┗ 📁 pnp_mpa
   ┣ 📜 pnpMPA_dc.spice.j2      Template for PNP DC sweeps.
   ┗ 📜 pnpmpa.yaml             Config for PNP MPA.
```

## YAML Configuration

Each YAML describes **what to simulate, how to run it, and how to evaluate results**.
Below is an excerpt from `sg13_hv_nmos.yaml`:

```yaml
# PDK Models Setup
mdm_dir: "../../../../libs.doc/meas/MOS/SG13_nmosHVXm1Y3"
corner_lib_path: "../../../../libs.tech/ngspice/models/cornerMOShv.lib"
osdi_path: "../../../../libs.tech/ngspice/osdi/psp103_nqs.osdi"

# Device Configuration
device_type: "mos"
device_name: "sg13_hv_nmos"

# Run Configuration
dc_template_path: "devices_configs/mos/dc_template.spice.j2"
generate_netlists: true  
max_workers: 4

# Output configuration
threshold_percent_oob: 5.0

metrics:
  - name: "id"
    meas: "id_meas"
    tt: "id_sim_mos_tt"
    ss: "id_sim_mos_ss"
    ff: "id_sim_mos_ff"
  - name: "ib"
    meas: "ib_meas"
    tt: "ib_sim_mos_tt"
    ss: "ib_sim_mos_ss"
    ff: "ib_sim_mos_ff"

# Output Paths
output_dir: "models_run/nmos_hv/"
```

### Key Sections

* **PDK Models Setup**

  * `mdm_dir`: Directory of measurement data (MDM format).
  * `corner_lib_path`: Path to the SPICE corner library.
  * `osdi_path`: Path to compiled OSDI Verilog-A models.

* **Device Configuration**

  * `device_type`: Device family (`mos`, `pnpmpa`, `hbt`).
  * `device_name`: Unique identifier for the device.

* **Run Configuration**

  * `dc_template_path`: Jinja2 netlist template for simulations.
  * `generate_netlists`: If `true`, netlists are saved to disk. If `false`, runs in-memory only.
  * `max_workers`: Number of parallel workers for simulations.

* **Output Configuration**

  * `threshold_percent_oob`: Maximum % of points allowed outside tolerance before test fails.
  * `threshold_count_oob`: Alternative to percentage — max absolute count of failing points.

* **Metrics**
  Defines which currents/voltages to check, and maps them to:

  * `meas`: Measured column in the MDM dataset.
  * `tt/ss/ff`: Simulated results for typical, slow, and fast corners.

* **Output Paths**

  * `output_dir`: Directory where results are stored (`models_run/<device>`).
