# Process node
set ::env(PROCESS) 130
set ::env(DEF_UNITS_PER_MICRON) 1000

if { ![info exist ::env(STD_CELL_LIBRARY)] } {
	set ::env(STD_CELL_LIBRARY) sg13g2_stdcell
}

# Tools
set ::env(PRIMARY_GDSII_STREAMOUT_TOOL) "magic"

# Placement site for core cells
# This can be found in the technology lef
set ::env(VDD_PIN) "VPWR"
set ::env(GND_PIN) "VGND"

set ::env(VDD_PIN_VOLTAGE) "1.20"
set ::env(GND_PIN_VOLTAGE) "0.00"

set ::env(SCL_POWER_PINS) "VDD"
set ::env(SCL_GROUND_PINS) "VSS"

# Technology LEF
set ::env(TECH_LEF) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lef/sg13g2_tech.lef"
set ::env(TECH_LEF_MIN) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lef/sg13g2_tech.lef"
set ::env(TECH_LEF_MAX) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lef/sg13g2_tech.lef"

# Standard cells
set ::env(CELL_LEFS) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lef/$::env(STD_CELL_LIBRARY).lef"
set ::env(CELL_GDS) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/gds/$::env(STD_CELL_LIBRARY).gds"
set ::env(CELL_VERILOG_MODELS) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/verilog/$::env(STD_CELL_LIBRARY).v"
set ::env(CELL_SPICE_MODELS) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/spice/$::env(STD_CELL_LIBRARY).spice"
set ::env(CELL_CDLS) "$::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/cdl/$::env(STD_CELL_LIBRARY).cdl"

# GPIO Pads
set ::env(GPIO_PADS_LEF) "\
	$::env(PDK_ROOT)/$::env(PDK)/libs.ref/sg13g2_io/lef/sg13g2_io.lef\
	$::env(PDK_ROOT)/$::env(PDK)/libs.ref/sg13g2_io/lef/sg13g2_io_notracks.lef\
"

set ::env(GPIO_PADS_VERILOG) "\
	$::env(PDK_ROOT)/$::env(PDK)/libs.ref/sg13g2_io/verilog/sg13g2_io.v
"

## magic setup
set ::env(MAGICRC) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/magic/ihp-sg13g2.magicrc"
set ::env(MAGIC_TECH) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/magic/ihp-sg13g2.tech"

# Klayout setup
set ::env(KLAYOUT_TECH) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/tech/sg13g2.lyt"
set ::env(KLAYOUT_PROPERTIES) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/tech/sg13g2.lyp"
set ::env(KLAYOUT_DEF_LAYER_MAP) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/tech/sg13g2.map"
set ::env(KLAYOUT_DRC_RUNSET) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/tech/drc/sg13g2_maximal.lydrc"
set ::env(KLAYOUT_DRC_OPTIONS) [dict create densityRules 0 ]
set ::env(KLAYOUT_LVS_SCRIPT) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/tech/lvs/sg13g2.lvs"
set ::env(KLAYOUT_LVS_OPTIONS) [dict create run_mode deep ]

# netgen setup
set ::env(NETGEN_SETUP) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/netgen/ihp-sg13g2_setup.tcl"

# No tap cells
set ::env(FP_TAPCELL_DIST) 0

# Tracks info
set ::env(FP_TRACKS_INFO) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/$::env(STD_CELL_LIBRARY)/tracks.info"

# Default Synth Exclude List
set ::env(SYNTH_EXCLUDED_CELL_FILE) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/$::env(STD_CELL_LIBRARY)/synth_exclude.cells"

# Default PNR Exclude List
set ::env(PNR_EXCLUDED_CELL_FILE) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/$::env(STD_CELL_LIBRARY)/pnr_exclude.cells"

## DRC Exclude List for Optimization library
#set ::env(DRC_EXCLUDE_CELL_LIST_OPT) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/$::env(STD_CELL_LIBRARY_OPT)/drc_exclude.cells"

# Open-RCX Rules File
set ::env(RCX_RULES) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/IHP_rcx_patterns.rules"
#set ::env(RCX_RULES_MIN) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/rules.openrcx.$::env(PDK).min.spef_extractor"
#set ::env(RCX_RULES_MAX) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/rules.openrcx.$::env(PDK).max.spef_extractor"

# Extra PDN configs
set ::env(FP_PDN_RAIL_LAYER) Metal1
set ::env(FP_PDN_RAIL_OFFSET) 0

set ::env(FP_PDN_VERTICAL_LAYER) TopMetal1
set ::env(FP_PDN_HORIZONTAL_LAYER) TopMetal2

set ::env(FP_PDN_VWIDTH) 2.2
set ::env(FP_PDN_VSPACING) 4.0
set ::env(FP_PDN_VPITCH) 75.6
set ::env(FP_PDN_VOFFSET) 13.6

set ::env(FP_PDN_HWIDTH) 2.2
set ::env(FP_PDN_HSPACING) 4.0
set ::env(FP_PDN_HPITCH) 75.6
set ::env(FP_PDN_HOFFSET) 13.6


# Core Ring PDN defaults
set ::env(FP_PDN_CORE_RING_VWIDTH) 5.0
set ::env(FP_PDN_CORE_RING_HWIDTH) 5.0
set ::env(FP_PDN_CORE_RING_VSPACING) 2.0
set ::env(FP_PDN_CORE_RING_HSPACING) 2.0
set ::env(FP_PDN_CORE_RING_VOFFSET) 4.5
set ::env(FP_PDN_CORE_RING_HOFFSET) 4.5

# PDN Macro blockages list
set ::env(MACRO_BLOCKAGES_LAYER) "Metal1 Metal2 Metal3 Metal4 Metal5 TopMetal1"

# Used for parasitics estimation, IR drop analysis, etc
set ::env(LAYERS_RC) [dict create]

# Don't set RC values manually, they appear to be inaccurate
# If not set, OpenROAD seems to pick them up from the tech lef?
# TODO needs more investigation

#dict set ::env(LAYERS_RC) "*" Metal1 res 0.135e-03
#dict set ::env(LAYERS_RC) "*" Metal1 cap 3.49E-05
#dict set ::env(LAYERS_RC) "*" Metal2 res 0.103e-03
#dict set ::env(LAYERS_RC) "*" Metal2 cap 1.81E-05
#dict set ::env(LAYERS_RC) "*" Metal3 res 0.103e-03
#dict set ::env(LAYERS_RC) "*" Metal3 cap 2.14962E-04
#dict set ::env(LAYERS_RC) "*" Metal4 res 0.103e-03
#dict set ::env(LAYERS_RC) "*" Metal4 cap 1.48128E-04
#dict set ::env(LAYERS_RC) "*" Metal5 res 0.103e-03
#dict set ::env(LAYERS_RC) "*" Metal5 cap 1.54087E-04
#dict set ::env(LAYERS_RC) "*" TopMetal1 res 0.021e-03
#dict set ::env(LAYERS_RC) "*" TopMetal1 cap 1.54087E-04
#dict set ::env(LAYERS_RC) "*" TopMetal2 res 0.0145e-03
#dict set ::env(LAYERS_RC) "*" TopMetal2 cap 1.54087E-04

#set ::env(VIAS_R) [dict create]

#dict set ::env(VIAS_R) "*" Cont res 2.2E-3
#dict set ::env(VIAS_R) "*" Via1 res 2.0E-3
#dict set ::env(VIAS_R) "*" Via2 res 2.0E-3
#dict set ::env(VIAS_R) "*" Via3 res 2.0E-3
#dict set ::env(VIAS_R) "*" Via4 res 2.0E-3
#dict set ::env(VIAS_R) "*" TopVia1 res 0.4E-3
#dict set ::env(VIAS_R) "*" TopVia2 res 0.22E-3

# Don't set DATA_WIRE_RC_LAYER, CLOCK_WIRE_RC_LAYER
# Have been renamed to SIGNAL_WIRE_RC_LAYERS, CLOCK_WIRE_RC_LAYERS
# If unset, RT_MIN_LAYER and RT_MAX_LAYER are used for the calculation

#set ::env(DATA_WIRE_RC_LAYER) "Metal2"
#set ::env(CLOCK_WIRE_RC_LAYER) "Metal5"

# I/O Layer info
set ::env(FP_IO_HLAYER) "Metal3"
set ::env(FP_IO_VLAYER) "Metal2"

# Routing Layer Info
set ::env(GRT_LAYER_ADJUSTMENTS) "0.00,0.00,0.00,0.00,0.00,0.00,0.00"

set ::env(RT_MIN_LAYER) "Metal2"
set ::env(RT_MAX_LAYER) "TopMetal2"

#set ::env(RT_CLOCK_MIN_LAYER) "met3"

## CVC
#set ::env(CVC_SCRIPTS_DIR) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/cvc"
