#---------------------------------------------------------------
# Setup file for netgen LVS
# IHP sg13g2
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
lappend devices Rparasitic
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
	property "-circuit1 $dev" parallel {value par}
	property "-circuit1 $dev" tolerance {l 0.01} {w 0.01}
	# Ignore these properties
	property "-circuit1 $dev" delete mult
    }
    if {[lsearch $cells2 $dev] >= 0} {
	permute "-circuit2 $dev" 1 2
	property "-circuit2 $dev" series enable
	property "-circuit2 $dev" series {w critical}
	property "-circuit2 $dev" series {l add}
	property "-circuit2 $dev" parallel enable
	property "-circuit2 $dev" parallel {l critical}
	property "-circuit2 $dev" parallel {w add}
	property "-circuit2 $dev" parallel {value par}
	property "-circuit2 $dev" tolerance {l 0.01} {w 0.01}
	# Ignore these properties
	property "-circuit2 $dev" delete mult
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
	property "-circuit1 $dev" parallel {value par}
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
	property "-circuit2 $dev" parallel {value par}
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
	property "-circuit1 $dev" delete as ad ps pd mult sa sb sd nf nrd nrs
    }
    if {[lsearch $cells2 $dev] >= 0} {
	permute "-circuit2 $dev" 1 3
	property "-circuit2 $dev" parallel enable
	property "-circuit2 $dev" parallel {l critical}
	property "-circuit2 $dev" parallel {w add}
	property "-circuit2 $dev" tolerance {w 0.01} {l 0.01}
	# Ignore these properties
	property "-circuit2 $dev" delete as ad ps pd mult sa sb sd nf nrd nrs
    }
}

#---------------------------------------------------------------------
# Extended drain MOSFET devices.  These have asymmetric source and
# drain, and so the source and drain are not permutable.
#---------------------------------------------------------------------

set devices {}
lappend devices nmoscl_2
lappend devices nmoscl_4

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
	property "-circuit1 $dev" parallel {area add}
	property "-circuit1 $dev" parallel {perim add}
	property "-circuit1 $dev" parallel {value add}
	property "-circuit1 $dev" tolerance {area 0.02} {perim 0.02}
	# Ignore these properties
	property "-circuit1 $dev" delete mult perim
    }
    if {[lsearch $cells2 $dev] >= 0} {
	property "-circuit2 $dev" parallel enable
	property "-circuit2 $dev" parallel {area add}
	property "-circuit2 $dev" parallel {perim add}
	property "-circuit2 $dev" parallel {value add}
	property "-circuit2 $dev" tolerance {area 0.02} {perim 0.02}
	# Ignore these properties
	property "-circuit2 $dev" delete mult perim
    }
}

#-------------------------------------------
# capacitors
# MiM capacitors
#-------------------------------------------

set devices {}
lappend devices cparasitic
lappend devices cap_cmim
lappend devices cap_rfcmim

foreach dev $devices {
    if {[lsearch $cells1 $dev] >= 0} {
	property "-circuit1 $dev" parallel enable
	property "-circuit1 $dev" parallel {area add}
	property "-circuit1 $dev" parallel {value add}
	property "-circuit1 $dev" tolerance {l 0.01} {w 0.01}
	# Ignore these properties
	property "-circuit1 $dev" delete mult perim mf
    }
    if {[lsearch $cells2 $dev] >= 0} {
	property "-circuit2 $dev" parallel enable
	property "-circuit2 $dev" parallel {area add}
	property "-circuit2 $dev" parallel {value add}
	property "-circuit2 $dev" tolerance {l 0.01} {w 0.01}
	# Ignore these properties
	property "-circuit2 $dev" delete mult perim mf
    }
}

#-------------------------------------------
# Fixed-layout devices
# bipolar transistors
#-------------------------------------------

set devices {}
lappend devices npn13g2
lappend devices npn13g2l
lappend devices npn13g2v
lappend devices pnpMPA

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
}
foreach cell $cells2 {
    if {[regexp {sg13g2_decap_[[:digit:]]+} $cell match]} {
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
