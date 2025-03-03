#---------------------------------------------------------------
# Setup file for netgen LVS
# IHP ihp-sg13g2
#---------------------------------------------------------------
permute default
property default
property parallel none

# Allow override of default #columns in the output format.
catch {format $env(NETGEN_COLUMNS)}

#---------------------------------------------------------------
# For the following, get the cell lists from
# circuit1 and circuit2.
#---------------------------------------------------------------

set cells1 [cells list -all -circuit1]
set cells2 [cells list -all -circuit2]

#-------------------------------------------
# Resistors (except metal)
#-------------------------------------------

set devices {}
lappend devices ptap1
lappend devices ntap1
lappend devices rsil
lappend devices rppd
lappend devices rhigh

foreach dev $devices {
    if {[lsearch $cells1 $dev] >= 0} {
	permute "-circuit1 $dev" 1 2
	property "-circuit1 $dev" series enable
	property "-circuit1 $dev" series {w critical}
	property "-circuit1 $dev" series {l add}
	property "-circuit1 $dev" parallel enable
	property "-circuit1 $dev" parallel {l critical}
	property "-circuit1 $dev" parallel {w add}
	property "-circuit1 $dev" tolerance {l 0.01} {w 0.01}
	# Ignore these properties
	property "-circuit1 $dev" delete b
    }
    if {[lsearch $cells2 $dev] >= 0} {
	permute "-circuit2 $dev" 1 2
	property "-circuit2 $dev" series enable
	property "-circuit2 $dev" series {w critical}
	property "-circuit2 $dev" series {l add}
	property "-circuit2 $dev" parallel enable
	property "-circuit2 $dev" parallel {l critical}
	property "-circuit2 $dev" parallel {w add}
	property "-circuit2 $dev" tolerance {l 0.01} {w 0.01}
	# Ignore these properties
	property "-circuit2 $dev" delete b
    }
}

#-------------------------------------------
# MRM (metal) resistors
#-------------------------------------------

set devices {}
lappend devices rm1
lappend devices rm2
lappend devices rm3
lappend devices rm4
lappend devices rm5
lappend devices rm6
lappend devices rm7

foreach dev $devices {
    if {[lsearch $cells1 $dev] >= 0} {
	permute "-circuit1 $dev" end_a end_b
	property "-circuit1 $dev" series enable
	property "-circuit1 $dev" series {w critical}
	property "-circuit1 $dev" series {l add}
	property "-circuit1 $dev" parallel enable
	property "-circuit1 $dev" parallel {l critical}
	property "-circuit1 $dev" parallel {w add}
	property "-circuit1 $dev" tolerance {l 10.0} {w 10.0}
	# Ignore these properties
	property "-circuit1 $dev" delete mult
    }
    if {[lsearch $cells2 $dev] >= 0} {
	permute "-circuit2 $dev" end_a end_b
	property "-circuit2 $dev" series enable
	property "-circuit2 $dev" series {w critical}
	property "-circuit2 $dev" series {l add}
	property "-circuit2 $dev" parallel enable
	property "-circuit2 $dev" parallel {l critical}
	property "-circuit2 $dev" parallel {w add}
	property "-circuit2 $dev" tolerance {l 10.0} {w 10.0}
	# Ignore these properties
	property "-circuit2 $dev" delete mult
    }
}

#-------------------------------------------
# (MOS) transistors
#-------------------------------------------

set devices {}
lappend devices sg13_hv_nmos
lappend devices sg13_hv_pmos
lappend devices sg13_lv_nmos
lappend devices sg13_lv_pmos
lappend devices nmosi
lappend devices nmosiHV
lappend devices scr1

foreach dev $devices {
    if {[lsearch $cells1 $dev] >= 0} {
	permute "-circuit1 $dev" 1 3
	property "-circuit1 $dev" parallel enable
	property "-circuit1 $dev" parallel {l critical}
	property "-circuit1 $dev" parallel {w add}
	property "-circuit1 $dev" tolerance {w 0.01} {l 0.01}
	# Ignore these properties
	property "-circuit1 $dev" delete ng as ad pd ps trise z1 z2 wmin rfmode pre_layout
    }
    if {[lsearch $cells2 $dev] >= 0} {
	permute "-circuit2 $dev" 1 3
	property "-circuit2 $dev" parallel enable
	property "-circuit2 $dev" parallel {l critical}
	property "-circuit2 $dev" parallel {w add}
	property "-circuit2 $dev" tolerance {w 0.01} {l 0.01}
	# Ignore these properties
	property "-circuit2 $dev" delete ng as ad pd ps trise z1 z2 wmin rfmode pre_layout
    }
}

#-------------------------------------------
# (HBT) transistors
#-------------------------------------------

set devices {}
lappend devices npn13G2
lappend devices npn13G2l
lappend devices npn13g2v
lappend devices pnpMPA

# TODO: check parallel merge
foreach dev $devices {
    if {[lsearch $cells1 $dev] >= 0} {
	permute "-circuit1 $dev" 1 3
	property "-circuit1 $dev" parallel enable
	property "-circuit1 $dev" parallel {le critical}
	property "-circuit1 $dev" parallel {we add}
	property "-circuit1 $dev" tolerance {we 0.01} {le 0.01}
	# Ignore these properties
	property "-circuit1 $dev" delete Nx Ny
    }
    if {[lsearch $cells2 $dev] >= 0} {
	permute "-circuit2 $dev" 1 3
	property "-circuit2 $dev" parallel enable
	property "-circuit2 $dev" parallel {le critical}
	property "-circuit2 $dev" parallel {we add}
	property "-circuit2 $dev" tolerance {we 0.01} {le 0.01}
	# Ignore these properties
	property "-circuit2 $dev" delete Nx Ny
    }
}

#---------------------------------------------------------------------
# Extended drain MOSFET devices.  These have asymmetric source and
# drain, and so the source and drain are not permutable.
#---------------------------------------------------------------------

set devices {}

foreach dev $devices {
    if {[lsearch $cells1 $dev] >= 0} {
	property "-circuit1 $dev" parallel enable
	property "-circuit1 $dev" parallel {l critical}
	property "-circuit1 $dev" parallel {w add}
	property "-circuit1 $dev" tolerance {w 0.01} {l 0.01}
	# Ignore these properties
	property "-circuit1 $dev" delete as ad ps pd mult sa sb sd nf nrd nrs area perim topography
    }
    if {[lsearch $cells2 $dev] >= 0} {
	property "-circuit2 $dev" parallel enable
	property "-circuit2 $dev" parallel {l critical}
	property "-circuit2 $dev" parallel {w add}
	property "-circuit2 $dev" tolerance {w 0.01} {l 0.01}
	# Ignore these properties
	property "-circuit2 $dev" delete as ad ps pd mult sa sb sd nf nrd nrs area perim topography
    }
}

#---------------------------------------------------------------------
# (MOS) ESD transistors. (Placeholder)
#---------------------------------------------------------------------

set devices {}

foreach dev $devices {
    if {[lsearch $cells1 $dev] >= 0} {
	permute "-circuit1 $dev" 1 3
	property "-circuit1 $dev" parallel enable
	property "-circuit1 $dev" parallel {l critical}
	property "-circuit1 $dev" parallel {w add}
	property "-circuit1 $dev" tolerance {w 0.07} {l 0.01}
	# Ignore these properties
	property "-circuit1 $dev" delete as ad ps pd mult sa sb sd nf nrd nrs area perim topography
    }
    if {[lsearch $cells2 $dev] >= 0} {
	permute "-circuit2 $dev" 1 3
	property "-circuit2 $dev" parallel enable
	property "-circuit2 $dev" parallel {l critical}
	property "-circuit2 $dev" parallel {w add}
	property "-circuit2 $dev" tolerance {w 0.07} {l 0.01}
	# Ignore these properties
	property "-circuit2 $dev" delete as ad ps pd mult sa sb sd nf nrd nrs area perim topography
    }
}

#-------------------------------------------
# diodes
#-------------------------------------------

set devices {}
lappend devices dantenna
lappend devices dpantenna
lappend devices schottky

foreach dev $devices {
    if {[lsearch $cells1 $dev] >= 0} {
	property "-circuit1 $dev" parallel enable
	property "-circuit1 $dev" parallel {l critical}
	property "-circuit1 $dev" parallel {w add}
	property "-circuit1 $dev" tolerance {w 0.01} {l 0.01}
	# Ignore these properties
	property "-circuit1 $dev" delete DEV_A DEV_P DEV_C
    }
    if {[lsearch $cells2 $dev] >= 0} {
	property "-circuit1 $dev" parallel enable
	property "-circuit1 $dev" parallel {l critical}
	property "-circuit1 $dev" parallel {w add}
	property "-circuit1 $dev" tolerance {w 0.01} {l 0.01}
	# Ignore these properties
	property "-circuit2 $dev" delete DEV_A DEV_P DEV_C
    }
}

#-------------------------------------------
# capacitors
# MiM capacitors
#-------------------------------------------

set devices {}
lappend devices cap_cmim
lappend devices cap_rfcmim

foreach dev $devices {
    if {[lsearch $cells1 $dev] >= 0} {
	property "-circuit1 $dev" parallel enable
	property "-circuit1 $dev" parallel {l critical}
	property "-circuit1 $dev" parallel {w add}
	property "-circuit1 $dev" tolerance {w 0.01} {l 0.01}
	# Ignore these properties
	property "-circuit1 $dev" delete ic
    }
    if {[lsearch $cells2 $dev] >= 0} {
	property "-circuit1 $dev" parallel enable
	property "-circuit1 $dev" parallel {l critical}
	property "-circuit1 $dev" parallel {w add}
	property "-circuit1 $dev" tolerance {w 0.01} {l 0.01}
	# Ignore these properties
	property "-circuit2 $dev" delete ic
    }
}

#-------------------------------------------
# Fixed-layout devices
# ESD devices
#-------------------------------------------

set devices {}
lappend devices nmoscl_2
lappend devices nmoscl_4

foreach dev $devices {
    if {[lsearch $cells1 $dev] >= 0} {
	property "-circuit1 $dev" parallel enable
	# Ignore these properties
	property "-circuit1 $dev" delete mult
    }
    if {[lsearch $cells2 $dev] >= 0} {
	property "-circuit2 $dev" parallel enable
	# Ignore these properties
	property "-circuit2 $dev" delete mult
    }
}

#---------------------------------------------------------------
# Schematic cells which are not extractable
#---------------------------------------------------------------

set devices {}
lappend devices Rparasitic
lappend devices cparasitic

foreach dev $devices {
    if {[lsearch $cells1 $dev] >= 0} {
	ignore class "-circuit1 $dev"
    }
    if {[lsearch $cells2 $dev] >= 0} {
	ignore class "-circuit2 $dev"
    }
}

#---------------------------------------------------------------
# Allow the fill, decap, etc., cells to be parallelized
#---------------------------------------------------------------

set devices {}
lappend devices sg13g2_antennap

foreach dev $devices {
    if {[lsearch $cells1 $dev] >= 0} {
	property "-circuit1 $cell" parallel enable
    }
    if {[lsearch $cells2 $dev] >= 0} {
	property "-circuit2 $cell" parallel enable
    }
}

foreach cell $cells1 {
    if {[regexp {sg13g2_decap_[[:digit:]]+} $cell match]} {
	property "-circuit1 $cell" parallel enable
    }
    if {[regexp {sg13g2_fill_[[:digit:]]+} $cell match]} {
	property "-circuit1 $cell" parallel enable
    }
}
foreach cell $cells2 {
    if {[regexp {sg13g2_decap_[[:digit:]]+} $cell match]} {
	property "-circuit2 $cell" parallel enable
    }
    if {[regexp {sg13g2_fill_[[:digit:]]+} $cell match]} {
	property "-circuit2 $cell" parallel enable
    }
}

#---------------------------------------------------------------
# Match pins on black-box cells if LVS is called with "-blackbox"
#---------------------------------------------------------------

if {[model blackbox]} {
    foreach cell $cells1 {
	if {[model "-circuit1 $cell"] == "blackbox"} {
	    if {[lsearch $cells2 $cell] >= 0} {
		puts stdout "Matching pins of $cell in circuits 1 and 2"
		equate pins "-circuit1 $cell" "-circuit2 $cell"
	    }
	}
    }
}

#---------------------------------------------------------------
