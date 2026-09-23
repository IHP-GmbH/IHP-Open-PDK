set current_folder [file dirname [file normalize [info script]]]

# Technology lib
set ::env(LIB) [dict create]
dict set ::env(LIB) nom_typ_1p20V_25C "\
    $::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lib/sg13cmos5l_stdcell_typ_1p20V_25C.lib\
    $::env(PDK_ROOT)/$::env(PDK)/libs.ref/sg13cmos5l_io/lib/sg13cmos5l_io_typ_1p2V_3p3V_25C.lib\
"
dict set ::env(LIB) nom_fast_1p32V_m40C "\
    $::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lib/sg13cmos5l_stdcell_fast_1p32V_m40C.lib\
    $::env(PDK_ROOT)/$::env(PDK)/libs.ref/sg13cmos5l_io/lib/sg13cmos5l_io_fast_1p32V_3p6V_m40C.lib\
"
dict set ::env(LIB) nom_slow_1p08V_125C "\
    $::env(PDK_ROOT)/$::env(PDK)/libs.ref/$::env(STD_CELL_LIBRARY)/lib/sg13cmos5l_stdcell_slow_1p08V_125C.lib\
    $::env(PDK_ROOT)/$::env(PDK)/libs.ref/sg13cmos5l_io/lib/sg13cmos5l_io_slow_1p08V_3p0V_125C.lib\
"


# Corners
set ::env(STA_CORNERS) "\
nom_fast_1p32V_m40C \
nom_slow_1p08V_125C \
nom_typ_1p20V_25C \
"

set ::env(DEFAULT_CORNER) "nom_typ_1p20V_25C"

set ::env(TIMING_VIOLATION_CORNERS) "*typ*"

# Synthesis mapping
 # Latch mapping
set ::env(SYNTH_LATCH_MAP) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/$::env(STD_CELL_LIBRARY)/latch_map.v"

 # MUX4 mapping
set ::env(SYNTH_MUX4_MAP) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/$::env(STD_CELL_LIBRARY)/mux4_map.v"

 # MUX2 mapping
set ::env(SYNTH_MUX_MAP) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/$::env(STD_CELL_LIBRARY)/mux2_map.v"

# Tri-state buffer mapping
set ::env(SYNTH_TRISTATE_MAP) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/$::env(STD_CELL_LIBRARY)/tribuff_map.v"

# Placement site for core cells
# This can be found in the technology lef
set ::env(PLACE_SITE) "CoreSite"
set ::env(PLACE_SITE_WIDTH) 0.48
set ::env(PLACE_SITE_HEIGHT) 3.78

# Welltap and endcap cells
# There are no endcap and welltie cells in ihp-sg13cmos5l
# thus set to undefined to skip insertion
#set ::env(WELLTAP_CELL) ""
#set ::env(ENDCAP_CELL) ""

# defaults (can be overridden by designs):
# Cell names for CMOS5L use sg13cmos5l_ prefix
set ::env(SYNTH_DRIVING_CELL) "sg13cmos5l_buf_4"
set ::env(SYNTH_DRIVING_CELL_PIN) "X"
set ::env(OUTPUT_CAP_LOAD) "6.0"
set ::env(SYNTH_MIN_BUF_PORT) "sg13cmos5l_buf_1 A X"
set ::env(SYNTH_TIEHI_PORT) "sg13cmos5l_tiehi L_HI"
set ::env(SYNTH_TIELO_PORT) "sg13cmos5l_tielo L_LO"

# Fillcell insertion
set ::env(FILL_CELLS) "sg13cmos5l_fill_1 sg13cmos5l_fill_2"
set ::env(DECAP_CELLS) "sg13cmos5l_decap_*"

# Diode insertion
set ::env(DIODE_CELL) "sg13cmos5l_antennanp"

set ::env(GPL_CELL_PADDING) {0}
set ::env(DPL_CELL_PADDING) {0}

set ::env(CELL_PAD_EXCLUDE) "sg13cmos5l_fill_* sg13cmos5l_decap_*"

# PDN
set ::env(FP_PDN_RAIL_WIDTH) 0.44

# CTS
# Buffer selection still needs some work
# There were situations where only the largest buffer was used
# Ultimately, OpenROAD should select the buffers automatically
set ::env(CTS_ROOT_BUFFER) sg13cmos5l_buf_8
set ::env(CTS_CLK_BUFFERS) "sg13cmos5l_buf_8 sg13cmos5l_buf_4 sg13cmos5l_buf_2 sg13cmos5l_buf_1"

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
