########################################################################
#
# Copyright 2025 IHP PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
########################################################################

#----------------------------------------------------------------
# Drawn inductor routines
# NOTE:  Inductors are set up to extract the cell as a device;
# there is no direct extraction of inductors in magic.
#----------------------------------------------------------------

proc sg13g2::inductor2_defaults {} {
    return {diameter 25.35 width 2.0 space 2.1 turns 1 class inductor \
		wmin 2.0 smin 2.1 dmin 25.35 \
		compatible {inductor2 inductor3} \
		doports 1}
}

proc sg13g2::inductor3_defaults {} {
    return {diameter 25.84 width 2.0 space 2.1 turns 2 class inductor \
		wmin 2.0 smin 2.1 dmin 25.84 \
		compatible {inductor2 inductor3} \
		doports 1}
}

#----------------------------------------------------------------
# Inductor defaults:
#----------------------------------------------------------------
#  diameter	Spacing between inner turn inner edges
#  width	Width of the inductor wire
#  space	Spacing between wires
#  turns	Number of turns of wire
#
#  (not user-editable)
#
#  wmin   Minimum allowed width
#  dmin   Minimum allowed diameter
#  smin	  Minimum allowed spacing
#----------------------------------------------------------------

#----------------------------------------------------------------
# inductor: Conversion from SPICE netlist parameters to toolkit
#----------------------------------------------------------------

proc sg13g2::ind_convert {parameters} {
    set pdkparams [dict create]
    dict for {key value} $parameters {
	switch -nocase $key {
	    m {
                # Convert m to ny
		dict set pdkparams ny $value
	    }
	    default {
		# Allow unrecognized parameters to be passed unmodified
		dict set pdkparams $key $value
	    }
	}
    }
    return $pdkparams
}

proc sg13g2::inductor2_convert {parameters} {
    return [ind_convert $parameters]
}

proc sg13g2::inductor3_convert {parameters} {
    return [ind_convert $parameters]
}

#----------------------------------------------------------------
# inductor: Interactively specifies the fixed layout parameters
#----------------------------------------------------------------

proc sg13g2::ind_dialog {device parameters} {
    # Editable fields:      diameter, width, space, turns
    # Checked fields:  	    (none)

    magic::add_entry width "Width (um)" $parameters
    magic::add_entry space "Spacing (um)" $parameters
    magic::add_entry diameter "Diameter (um)" $parameters
    magic::add_entry turns "Turns" $parameters

    if {[dict exists $parameters compatible]} {
	set sellist [dict get $parameters compatible]
	magic::add_selectlist gencell "Device type" $sellist $parameters $device
    }

    if {[dict exists $parameters doports]} {
	magic::add_checkbox doports "Add ports" $parameters
    }
}

proc sg13g2::inductor2_dialog {parameters} {
    sg13g2::ind_dialog inductor2 $parameters
}

proc sg13g2::inductor3_dialog {parameters} {
    sg13g2::ind_dialog inductor3 $parameters
}

#----------------------------------------------------------------
# Inductor: Draw a single device
#----------------------------------------------------------------

proc sg13g2::ind_device {parameters} {
    set positions 2

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Recast inner diameter as the wire centerline
    set idiam [+ $diameter [/ $width 2.0]]

    # Calculate distance between wires center-to-center
    set wspace [+ $space $width]

    # Define the inductor wire area outer diameter
    set odiam [+ $diameter [* 2 $turns $width] [* 2 [- $turns 1] $space]]

    box values 0 0 0 0
    pushbox

    # Draw the keep-out area (inductor ID layer).  This area is also used
    # for pwell block.
    set kwidth [+ $odiam 60.0]
    set keepout_area [sg13g2::create_polygon 8 $kwidth $kwidth]
    polygon inductor {*}$keepout_area
    polygon pblock {*}$keepout_area

    # First draw all of the wires as full circles
    set wdiam [+ $diameter $width]
    for {set i 0} {$i < $turns} {incr i} {
	set wire_center [sg13g2::create_wire $npoints $wdiam $wdiam]
	wire segment metal7 ${width}um {*}$wire_center
	set wdiam [+ $wdiam [* 2 [+ $width $space]]]
    }

    if {$turns > 1} {

	# Add crossovers and contacts
	# Draw the crossover and then copy it to positions

	set hwidth [/ $width 2.0]
	set d 2.0	;# minimum spacing of metal7
	set xp [/ [* 0.4142 $width] 2.0]

	set xpoint [expr {0.5*($space + $width)}]
	set xend [expr {-$xpoint + $xp + $width + 2.0 + $d * 1.4142}]
	set xend [magic::i2u [magic::magceil [magic::u2i $xend]]]

	set xwire1 {}
	lappend xwire1 -${xend}um -${xpoint}um
	lappend xwire1 -${xpoint}um -${xpoint}um
	lappend xwire1 ${xpoint}um ${xpoint}um
	lappend xwire1 ${xend}um ${xpoint}um
	wire segment metal7 ${width}um {*}$xwire1 -noendcap
    
	set xwire2 {}
	lappend xwire2 -${xend}um ${xpoint}um
	lappend xwire2 -${xpoint}um ${xpoint}um
	lappend xwire2 ${xpoint}um -${xpoint}um
	lappend xwire2 ${xend}um -${xpoint}um
	wire segment metal6 ${width}um {*}$xwire2 -noendcap
    
	box size 0 0
	box position -${xend}um ${xpoint}um
	box grow n ${hwidth}um
	box grow s ${hwidth}um
	box grow e 2.0um
	paint via6
    
	box size 0 0
	box position ${xend}um -${xpoint}um
	box grow n ${hwidth}um
	box grow s ${hwidth}um
	box grow w 2.0um
	paint via6

	set aypos [+ [/ $diameter 2.0] $width [/ $space 2.0]]
	set xwidth [* $xend 2.0]
	set xheight [* $xpoint 2.0]

	for {set i 1} {$i < $turns} {incr i} {
	    set ypos $aypos
	    if {[% $i 2] == 0} {set ypos -$aypos}
	    box size 0 0
	    box position 0 ${ypos}um
	    box grow e ${xend}um
	    box grow w ${xend}um
	    box grow n ${xpoint}um
	    box grow s ${xpoint}um
	    box grow c ${hwidth}um
	    box grow e -${width}um
	    box grow w -${width}um
	    erase metal7

	    box move s ${ypos}um
	    box grow e ${width}um
	    box grow w ${width}um
	    box grow c 5
	    select area metal6,via6,metal7
	    copy n ${ypos}um

            set aypos [+ $aypos $width $space]
	}
	box move s ${ypos}um
	select area metal6,via6,metal7
	delete
    }
    
    # Add the stubs.  For 1 and 2 turns, the stubs are at
    # $space distance apart.  For 3 or more turns, they have
    # to allow space for one crossover between them.
    # Thes stubs always connect to the innermost ring

    if {$turns < 3} {
	set stubspace $space
    } else {
	# Stubs must be spaced apart by the width of the crossover
	# plus metal6 spacing on either side
	set stubspace [+ [* $xend 2.0] 3.28]
    }
    set hsspace [/ $stubspace 2.0]
    set vpos [+ [/ $diameter 2.0] $width]
    box values 0 0 0 0
    box move s ${vpos}um
    box grow n ${width}um
    box grow e ${hsspace}um
    box grow w ${hsspace}um
    erase metal7
    box move e ${stubspace}um
    box width ${width}um
    paint via6
    box move w ${stubspace}um
    box move w ${width}um
    paint via6
    set hkwidth [/ $kwidth 2.0]
    set ibottom [magic::u2i -$hkwidth]
    set curbox [box values]
    set curbox [lreplace $curbox 1 1 $ibottom]
    box values {*}$curbox
    paint metal6
    if {$doports} {
	pushbox
	box height ${width}um
	label LA c metal6
	select area label
	port make
	popbox
    }
    box move e ${width}um
    box move e ${stubspace}um
    paint metal6
    if {$doports} {
	pushbox
	box height ${width}um
	label LB c metal6
	select area label
	port make
	popbox
    }
    if {$positions == 3} {
	# Add center tap
	box move w ${hsspace}um
	box move w ${hwidth}um
	set diff [/ [- $odiam $diameter] 2.0]
	box grow n -${diff}um
	paint metal7
	if {$doports} {
	    pushbox
	    box height ${width}um
	    label LC c metal7
	    select area label
	    port make
	    popbox
	}
    }

    popbox
}

#----------------------------------------------------------------
# 2-port Inductor: Draw the device
#----------------------------------------------------------------

proc sg13g2::inductor2_draw {parameters} {
    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    npoints		8 \
	    positions		2 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::ind_device $drawdict]
}

#----------------------------------------------------------------
# 3-port Inductor (Balun): Draw the device
#----------------------------------------------------------------

proc sg13g2::inductor3_draw {parameters} {
    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    npoints		8 \
	    positions		3 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::ind_device $drawdict]
}

#----------------------------------------------------------------
# inductor: Check device parameters for out-of-bounds values
#----------------------------------------------------------------

proc sg13g2::ind_check {device parameters} {

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Normalize distance units to microns
    set width [magic::spice2float $width]
    set width [magic::3digitpastdecimal $width] 
    set space [magic::spice2float $space]
    set space [magic::3digitpastdecimal $space] 
    set diameter [magic::spice2float $diameter]
    set diameter [magic::3digitpastdecimal $diameter] 

    if {$width < $wmin} {
	puts stderr "Inductor wire width must be >= $wmin"
	dict set parameters width $wmin
	set width $wmin
    } 
    if {$space < $smin} {
	puts stderr "Inductor wire spacing must be >= $smin"
	dict set parameters space $smin
	set space $smin
    } 
    if {$diameter < $dmin} {
	puts stderr "Inductor inner diameter must be >= $dmin"
	dict set parameters diameter $dmin
	set diameter $dmin
    } 

    # Number of turns must be an integer
    if {![string is int $turns]} {
	puts stderr "Number of turns must be an integer!"
	if {$device == "inductor3"} {
	    dict set parameters turns 2
	} else {
	    dict set parameters turns 1
	}
    }

    # Number of turns for a balun must be an even integer
    if {$device == "inductor3"} {
	if {[% $turns 2] != 0} {
	    puts stderr "Number of turns must be an even integer!"
            dict set parameters turns 2
	}
    }

    return $parameters
}

proc sg13g2::inductor2_check {parameters} {
    return [sg13g2::ind_check inductor2 $parameters]
}

proc sg13g2::inductor3_check {parameters} {
    return [sg13g2::ind_check inductor3 $parameters]
}

#----------------------------------------------------------------
