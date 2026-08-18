set current_folder [file dirname [file normalize [info script]]]

# Synthesis mapping
 # Latch mapping
set ::env(SYNTH_LATCH_MAP) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/$::env(STD_CELL_LIBRARY)/latch_map.v"

 # MUX4 mapping
set ::env(SYNTH_MUX4_MAP) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/$::env(STD_CELL_LIBRARY)/mux4_map.v"

 # MUX2 mapping
set ::env(SYNTH_MUX_MAP) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/librelane/$::env(STD_CELL_LIBRARY)/mux2_map.v"

# No tri-state buffer mapping: the drawn tri-state cells (sg13g2_hv_ebufn_4,
# sg13g2_hv_einvn_2/4/8) are not characterized, so a mapped tri-state could
# not be timed. Designs that infer $_TBUF_ fail loudly at synthesis instead.

# Flip-flops map through dfflibmap like the thin-oxide library: all 8
# dfrbp/dfrbpq/sdfrbp/sdfrbpq flops and the 5 latches carry liberty AND
# layout views. sdfbbp_map.v remains available for designs that want
# every flop on the scan cell (see its header; it conflicts with the
# sdfbbp_1 entry in synth_exclude.cells, remove that line first).

# Placement site for core cells
# This can be found in the cell lef
set ::env(PLACE_SITE) "CoreSiteHV"
set ::env(PLACE_SITE_WIDTH) 0.48
set ::env(PLACE_SITE_HEIGHT) 7.14

# Welltap and endcap cells
# There are no endcap and welltie cells in ihp-sg13g2
# thus set to undefined to skip insertion
#set ::env(WELLTAP_CELL) ""
#set ::env(ENDCAP_CELL) ""

# defaults (can be overridden by designs):
set ::env(SYNTH_DRIVING_CELL) "sg13g2_hv_buf_4"
set ::env(SYNTH_DRIVING_CELL_PIN) "X"
set ::env(OUTPUT_CAP_LOAD) "6.0"
set ::env(SYNTH_MIN_BUF_PORT) "sg13g2_hv_buf_1 A X"
set ::env(SYNTH_TIEHI_PORT) "sg13g2_hv_tiehi L_HI"
set ::env(SYNTH_TIELO_PORT) "sg13g2_hv_tielo L_LO"

# Fillcell insertion
set ::env(FILL_CELLS) "sg13g2_hv_fill_1 sg13g2_hv_fill_2 sg13g2_hv_fill_4 sg13g2_hv_fill_8"
set ::env(DECAP_CELLS) "sg13g2_hv_decap_*"

# Diode insertion
set ::env(DIODE_CELL) "sg13g2_hv_antennanp/A"

set ::env(GPL_CELL_PADDING) {0}
set ::env(DPL_CELL_PADDING) {0}

set ::env(CELL_PAD_EXCLUDE) "sg13g2_hv_fill_* sg13g2_hv_decap_*"

# PDN: the VSS rail is 0.44 um wide and symmetric about the row edge; the
# VDD pin shape is taller (0.535 um) and fully covers a 0.44 um strap.
set ::env(PDN_RAIL_WIDTH) 0.44

# CTS
set ::env(CTS_ROOT_BUFFER) sg13g2_hv_buf_16
set ::env(CTS_CLK_BUFFERS) "sg13g2_hv_buf_8 sg13g2_hv_buf_4 sg13g2_hv_buf_2"

# Mirrored from sg13g2_stdcell (themselves "a bit random ... from sky130").
# The 3.3 V cells switch roughly 3x slower than the thin-oxide library;
# raise CLOCK_TRANSITION_CONSTRAINT at design level if CTS reports
# unattainable clock slew.
set ::env(MAX_FANOUT_CONSTRAINT) 10
set ::env(CLOCK_UNCERTAINTY_CONSTRAINT) 0.25
set ::env(CLOCK_TRANSITION_CONSTRAINT) 0.15
set ::env(TIME_DERATING_CONSTRAINT) 5
set ::env(IO_DELAY_CONSTRAINT) 20

# No TRISTATE_CELLS: see the tri-state note above.

# TODO adjust threshold
set ::env(HEURISTIC_ANTENNA_THRESHOLD) 90
