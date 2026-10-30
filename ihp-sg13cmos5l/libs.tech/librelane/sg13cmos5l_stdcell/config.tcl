set current_folder [file dirname [file normalize [info script]]]

# Technology lib
set ::env(CELL_LIBS) [dict create]
dict set ::env(CELL_LIBS) "*_typ_1p20V_25C" "\
    $::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lib/sg13cmos5l_stdcell_typ_1p20V_25C.lib\
"
dict set ::env(CELL_LIBS) "*_fast_1p32V_m40C" "\
    $::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lib/sg13cmos5l_stdcell_fast_1p32V_m40C.lib\
"
dict set ::env(CELL_LIBS) "*_slow_1p08V_125C" "\
    $::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lib/sg13cmos5l_stdcell_slow_1p08V_125C.lib\
"

# Synthesis mapping
 # Latch mapping
set ::env(SYNTH_LATCH_MAP) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/$::env(STD_CELL_LIBRARY)/latch_map.v"

# Tri-state buffer mapping
set ::env(SYNTH_TRISTATE_MAP) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/$::env(STD_CELL_LIBRARY)/tribuff_map.v"

# Placement site for core cells
# This can be found in the technology lef
set ::env(PLACE_SITE) "CoreSite"

# Welltap and endcap cells
# There are no endcap and welltie cells in ihp-sg13cmos5l
# thus set to undefined to skip insertion
#set ::env(WELLTAP_CELL) ""
#set ::env(ENDCAP_CELL) ""

# defaults (can be overridden by designs):
set ::env(SYNTH_DRIVING_CELL) "sg13cmos5l_buf_4/X"
set ::env(OUTPUT_CAP_LOAD) "6.0"
set ::env(SYNTH_BUFFER_CELL) "sg13cmos5l_buf_1/A/X"
set ::env(SYNTH_TIEHI_CELL) "sg13cmos5l_tiehi/L_HI"
set ::env(SYNTH_TIELO_CELL) "sg13cmos5l_tielo/L_LO"

# Fillcell insertion
set ::env(FILL_CELLS) "sg13cmos5l_fill_1 sg13cmos5l_fill_2"
set ::env(DECAP_CELLS) "sg13cmos5l_decap_*"

# Diode insertion
set ::env(DIODE_CELL) "sg13cmos5l_antennanp/A"

set ::env(GPL_CELL_PADDING) {0}
set ::env(DPL_CELL_PADDING) {0}

set ::env(CELL_PAD_EXCLUDE) "sg13cmos5l_fill_* sg13cmos5l_decap_*"

# PDN
set ::env(FP_PDN_RAIL_WIDTH) 0.44

# CTS
set ::env(CTS_ROOT_BUFFER) "sg13cmos5l_buf_16"
set ::env(CTS_CLK_BUFFERS) "sg13cmos5l_buf_8 sg13cmos5l_buf_4 sg13cmos5l_buf_2"

# FIXME: A bit random ... from sky130
set ::env(MAX_FANOUT_CONSTRAINT) 10
set ::env(CLOCK_UNCERTAINTY_CONSTRAINT) 0.25
set ::env(CLOCK_TRANSITION_CONSTRAINT) 0.15
set ::env(TIME_DERATING_CONSTRAINT) 5
set ::env(IO_DELAY_CONSTRAINT) 20

# Tristate cells
set ::env(TRISTATE_CELLS) "sg13cmos5l_ebufn_* sg13cmos5l_einvn_*"

# TODO adjust threshold
set ::env(HEURISTIC_ANTENNA_THRESHOLD) 90
