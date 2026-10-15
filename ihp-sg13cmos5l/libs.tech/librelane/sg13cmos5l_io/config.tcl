set current_folder [file dirname [file normalize [info script]]]

# Pad IO sites
set ::env(PAD_SITE_NAME) "sg13cmos5l_ioSite"
set ::env(PAD_CORNER_SITE_NAME) "sg13cmos5l_cornerSite"

# Set IO pad information
set ::env(PAD_CELLS) [dict create]
dict set ::env(PAD_CELLS) "sg13cmos5l_IOPad*" "80, 180"
set ::env(PAD_CORNER) "sg13cmos5l_Corner"
set ::env(PAD_FILLERS) "\
    sg13cmos5l_Filler10000\
    sg13cmos5l_Filler4000\
    sg13cmos5l_Filler2000\
    sg13cmos5l_Filler1000\
    sg13cmos5l_Filler400\
    sg13cmos5l_Filler200\
"

# Pad bondpad information (if needed)
# TODO bondpads need to be part of the PDK
set ::env(PAD_BONDPAD_NAME) "bondpad_70x70"
set ::env(PAD_BONDPAD_WIDTH) "70"
set ::env(PAD_BONDPAD_HEIGHT) "70"
set ::env(PAD_BONDPAD_OFFSETS) [dict create]
dict set ::env(PAD_BONDPAD_OFFSETS) "sg13cmos5l_IOPad*" "5.0, -70.0"

# Pad io terminals (if needed)
#set ::env(PAD_PLACE_IO_TERMINALS)

# Sealring offset
set ::env(PAD_EDGE_SPACING) "140"

set ::env(KLAYOUT_SEALRING_SCRIPT) "$::env(PDK_ROOT)/$::env(PDK)/libs.tech/klayout/tech/scripts/sealring.py"
