# SG13CMOS5L LibreLane PDK Configuration
# Metal stack: M1-M4-TM1 (5 layers, no Metal5/TopMetal2)

# Process node
set ::env(PROCESS) 130
set ::env(DEF_UNITS_PER_MICRON) 1000

if { ![info exist ::env(STD_CELL_LIBRARY)] } {
	set ::env(STD_CELL_LIBRARY) sg13cmos5l_stdcell
}

if { ![info exist ::env(PAD_CELL_LIBRARY)] } {
	set ::env(PAD_CELL_LIBRARY) sg13cmos5l_io
}
# Tools - use KLayout for GDS streaming (Magic doesn't have CMOS5L support)
set ::env(PRIMARY_GDSII_STREAMOUT_TOOL) "klayout"

# Placement site for core cells
# This can be found in the technology lef
set ::env(VDD_PIN) "VPWR"
set ::env(GND_PIN) "VGND"

set ::env(VDD_PIN_VOLTAGE) "1.20"
set ::env(GND_PIN_VOLTAGE) "0.00"

set ::env(SCL_POWER_PINS) "VDD"
set ::env(SCL_GROUND_PINS) "VSS"

# Technology LEF
set ::env(TECH_LEF) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lef/sg13cmos5l_tech.lef"
set ::env(TECH_LEF_MIN) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lef/sg13cmos5l_tech.lef"
set ::env(TECH_LEF_MAX) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lef/sg13cmos5l_tech.lef"

# Standard cells
set ::env(CELL_LEFS) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lef/$::env(STD_CELL_LIBRARY).lef"
set ::env(CELL_GDS) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/gds/$::env(STD_CELL_LIBRARY).gds"
set ::env(CELL_VERILOG_MODELS) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/verilog/$::env(STD_CELL_LIBRARY).v"
set ::env(CELL_SPICE_MODELS) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/spice/$::env(STD_CELL_LIBRARY).spice"
set ::env(CELL_CDLS) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/cdl/$::env(STD_CELL_LIBRARY).cdl"

# GPIO Pads - Not available for CMOS5L slim PDK
# set ::env(GPIO_PADS_LEF) ""
# set ::env(GPIO_PADS_VERILOG) ""
set ::env(PAD_LEFS) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/sg13cmos5l_io/lef/sg13cmos5l_io.lef"
set ::env(PAD_GDS) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/sg13cmos5l_io/gds/sg13cmos5l_io.gds"
set ::env(PAD_VERILOG_MODELS) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/sg13cmos5l_io/verilog/sg13cmos5l_io.v"
set ::env(PAD_SPICE_MODELS) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/sg13cmos5l_io/spice/sg13cmos5l_io.spi"
set ::env(PAD_CDLS) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/sg13cmos5l_io/cdl/sg13cmos5l_io.cdl"

# Klayout setup
set ::env(KLAYOUT_TECH) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/tech/sg13cmos5l.lyt"
set ::env(KLAYOUT_PROPERTIES) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/tech/sg13cmos5l.lyp"
set ::env(KLAYOUT_DEF_LAYER_MAP) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/tech/sg13cmos5l.map"
set ::env(KLAYOUT_DRC_RUNSET) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/tech/drc/ihp-sg13cmos5l.drc"
set ::env(KLAYOUT_DRC_OPTIONS) [dict create]
dict set ::env(KLAYOUT_DRC_OPTIONS) no_recommended true
dict set ::env(KLAYOUT_DRC_OPTIONS) run_mode deep

set ::env(KLAYOUT_DENSITY_RUNSET) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/tech/drc/rule_decks/density.drc"
set ::env(KLAYOUT_DENSITY_OPTIONS) [dict create]

set ::env(KLAYOUT_ANTENNA_RUNSET) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/tech/drc/rule_decks/antenna.drc"
set ::env(KLAYOUT_ANTENNA_OPTIONS) [dict create]

set ::env(KLAYOUT_FILLER_SCRIPT) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/tech/scripts/filler.py"

set ::env(KLAYOUT_LVS_SCRIPT) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/tech/lvs/sg13cmos5l.lvs"  
set ::env(KLAYOUT_LVS_OPTIONS) [dict create run_mode deep ]
# LVS not yet available for CMOS5L
# set ::env(KLAYOUT_LVS_SCRIPT) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/tech/lvs/sg13cmos5l.lvs"
# set ::env(KLAYOUT_LVS_OPTIONS) [dict create run_mode deep ]

## magic setup
set ::env(MAGICRC) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/magic/ihp-sg13cmos5l.magicrc"
set ::env(MAGIC_TECH) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/magic/ihp-sg13cmos5l.tech"
# netgen setup
set ::env(NETGEN_SETUP) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/netgen/ihp-sg13cmos5l_setup.tcl"

# No tap cells
set ::env(FP_TAPCELL_DIST) 0

# Tracks info
set ::env(FP_TRACKS_INFO) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/$::env(STD_CELL_LIBRARY)/tracks.info"

# Default Synth Exclude List
set ::env(SYNTH_EXCLUDED_CELL_FILE) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/$::env(STD_CELL_LIBRARY)/synth_exclude.cells"

# Default PNR Exclude List
set ::env(PNR_EXCLUDED_CELL_FILE) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/$::env(STD_CELL_LIBRARY)/pnr_exclude.cells"

# Open-RCX Rules File
set ::env(RCX_RULES) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/IHP_rcx_patterns.rules"

# Extra PDN configs
# CMOS5L: M1-M4-TM1 (no Metal5, no TopMetal2)
# Use Metal3 (H) for horizontal stripes, Metal4 (V) for vertical stripes
# Simpler via stack: M1->Via1->M2->Via2->M3->Via3->M4
set ::env(FP_PDN_RAIL_LAYER) Metal1
set ::env(FP_PDN_RAIL_OFFSET) 0

set ::env(FP_PDN_VERTICAL_LAYER) Metal4
set ::env(FP_PDN_HORIZONTAL_LAYER) TopMetal1

# Metal4 PDN vertical stripe settings (thin metal, 0.45um)
set ::env(FP_PDN_VWIDTH) 1.0
set ::env(FP_PDN_VSPACING) 2.0
set ::env(FP_PDN_VPITCH) 50.0
set ::env(FP_PDN_VOFFSET) 10.0

# TopMetal1 PDN horizontal stripe settings (thick metal, 2um)
set ::env(FP_PDN_HWIDTH) 2.0
set ::env(FP_PDN_HSPACING) 4.0
set ::env(FP_PDN_HPITCH) 50.0
set ::env(FP_PDN_HOFFSET) 10.0

# Core Ring PDN defaults
set ::env(FP_PDN_CORE_RING_VWIDTH) 2.0
set ::env(FP_PDN_CORE_RING_HWIDTH) 2.0
set ::env(FP_PDN_CORE_RING_VSPACING) 1.0
set ::env(FP_PDN_CORE_RING_HSPACING) 1.0
set ::env(FP_PDN_CORE_RING_VOFFSET) 2.0
set ::env(FP_PDN_CORE_RING_HOFFSET) 2.0

# PDN Macro blockages list - no Metal5/TopMetal2
set ::env(MACRO_BLOCKAGES_LAYER) "Metal1 Metal2 Metal3 Metal4 TopMetal1"

# Used for parasitics estimation, IR drop analysis, etc
set ::env(LAYERS_RC) [dict create]

# I/O Layer info
set ::env(FP_IO_HLAYER) "Metal3"
set ::env(FP_IO_VLAYER) "Metal2"

# Routing Layer Info
# 5 routing layers: Metal1, Metal2, Metal3, Metal4, TopMetal1
set ::env(GRT_LAYER_ADJUSTMENTS) "0.00,0.00,0.00,0.00,0.00"

set ::env(RT_MIN_LAYER) "Metal2"
set ::env(RT_MAX_LAYER) "TopMetal1"
