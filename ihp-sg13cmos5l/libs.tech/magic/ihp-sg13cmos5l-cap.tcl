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
# Drawn capacitor routines.  There is no capacitor device in the
# SG13CMOS5L process (not counting MOScaps and varactors, which
# are not considered capacitors by the device generator scripts).
# So capacitor layouts are created by interdigitating metal
# fingers, which yields the highest capacitance per unit area
# for metals 1 to 4.  TopMetal1 (metal 5 in magic) is practically
# useless as a capacitor and is not considered.  Layouts have
# been analyzed for parasitics and an approximate equation
# obtained for the capacitance per unit area given a specific
# metal stack.
#
# "square" is enabled by default so that reading the device from
# a netlist calculates w and l from the value and produces a
# square capacitor.
#----------------------------------------------------------------

proc sg13cmos5l::capacitor_defaults {} {
    return {w 2.00 l 2.00 value 9.28 class capacitor \
		mmin 1 mmax 4 square 1 subblock 0 \
		lmin 2.00 wmin 2.00 lmax 100.0 wmax 100.0}
}

#----------------------------------------------------------------
# Recalculate capacitor values from GUI entries.
# Recomputes W/L and Value as long as 2 of them are present
# (To be completed)
#----------------------------------------------------------------

proc sg13cmos5l::cap_recalc {field parameters} {
    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    set areacap 0.55
    if {$mmin == 1} {set areacap 0.67}
    for {set i [expr {$mmin + 1}]} {$i <= $mmax} {incr i} {
	set areacap [expr {$areacap + 0.55}]
    }

    switch  $field {
	value { 
	    if {$square == 1} {
		# If cap is square, then update both w and l.
		set wlval [expr {sqrt($value / $areacap)}]
		set w [format "%.3f" $wlval]
		set l [format "%.3f" $wlval]
	    } else {
		# Otherwise, keep w and update l.
		set area [expr {$value / $areacap}]
		set lval [expr {$area / $w}]
		set l [format "%.3f" $lval]
	    }
	}
	mmax -
	mmin -
	l -
	w   {
	    # Update value based on new width, length, or metal stack
	    set captotal [expr {$areacap * $w * $l}]
	    set value [format "%.3f" $captotal]
	}
    }

    # Note:  mmin and mmax never get modified automatically.
    dict set parameters value $value
    dict set parameters w $w
    dict set parameters l $l

    return $parameters
}

#----------------------------------------------------------------
# Capacitor defaults:
#----------------------------------------------------------------
#  w        Width of drawn cap
#  l        Length of drawn cap
#  mmin	    Metal stack lowest metal index
#  mmax	    Metal stack highest metal index
#  value    Default cap value
#  square   Make square capacitor
#  subblock Put PWELLBLK under device
#
#  (not user-editable)
#
#  wmin   Minimum allowed width
#  lmin   Minimum allowed length
#  wmax   Maximum allowed width
#  lmax   Maximum allowed length
#----------------------------------------------------------------

#----------------------------------------------------------------
# capacitor: Conversion from SPICE netlist parameters to toolkit
#----------------------------------------------------------------

proc sg13cmos5l::cap_convert {parameters} {
    set pdkparams [dict create]
    dict for {key dvalue} $parameters {
	switch -nocase $key {
	    l -
	    w {
		# Length and width are converted to units of microns
		set dvalue [magic::spice2float $dvalue]
		set dvalue [expr $dvalue * 1e6]
		set dvalue [magic::3digitpastdecimal $dvalue]
		dict set pdkparams [string tolower $key] $dvalue
	    }
	    value {
		# Convert SI units to fF
		set dvalue [magic::spice2float $dvalue]
		set dvalue [* $dvalue 1e15]
		dict set pdkparams [string tolower $key] $dvalue
		# Convert value back to W and L.
		set pdkparams [dict merge [sg13cmos5l::capacitor_defaults] $pdkparams]
		set pdkparams [sg13cmos5l::cap_recalc value $pdkparams]
	    }
	    default {
		# Allow unrecognized parameters to be passed unmodified
		dict set pdkparams $key $dvalue
	    }
	}
    }
    return $pdkparams
}

proc sg13cmos5l::capacitor_convert {parameters} {
    return [cap_convert $parameters]
}

#----------------------------------------------------------------
# capacitor: Interactively specifies the fixed layout parameters
#----------------------------------------------------------------

proc sg13cmos5l::cap_dialog {device parameters} {
    # Editable fields:      w, l, nx, ny, val
    # Checked fields:  	    square, dummy

    magic::add_entry value "Estimated value (fF)" $parameters
    magic::add_entry l "Length (um)" $parameters
    magic::add_entry w "Width (um)" $parameters
    magic::add_entry mmin "Bottom metal" $parameters
    magic::add_entry mmax "Top metal" $parameters

    if {[dict exists $parameters square]} {
	magic::add_checkbox square "Square capacitor" $parameters
    }
    if {[dict exists $parameters subblock]} {
	magic::add_checkbox subblock "Add substrate block" $parameters
    }

    magic::add_dependency sg13cmos5l::cap_recalc $device sg13cmos5l l w mmin mmax value
}

proc sg13cmos5l::capacitor_dialog {parameters} {
    sg13cmos5l::cap_dialog capacitor $parameters
}

#----------------------------------------------------------------
# capacitor: Check device parameters for out-of-bounds values
#----------------------------------------------------------------

proc sg13cmos5l::cap_check {devname parameters} {
    # In case wmax and/or lmax are undefined
    set lmax 0
    set wmax 0

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Normalize distance units to microns
    set l [magic::spice2float $l]
    set l [magic::3digitpastdecimal $l] 
    set w [magic::spice2float $w]
    set w [magic::3digitpastdecimal $w] 

    set value   [magic::spice2float $value]

    if {$value <= 0.0} {
	puts stderr "Capacitor value must be strictly positive!"
	# User entered a bad value;  Recalculate a sane value from W
	set parameters [sg13cmos5l::cap_recalc w $parameters]
    }
    if {$mmin != [int $mmin]} {
	puts stderr "Capacitor lowest metal value must be an integer"
	dict set parameters mmin [int $mmin]
	set mmin [int $mmin]
    }
    if {$mmax != [int $mmax]} {
	puts stderr "Capacitor highest metal value must be an integer"
	dict set parameters mmax [int $mmax]
	set mmax [int $mmax]
    }
    if {$mmin < 1} {
	puts stderr "Capacitor lowest metal must be >= 1"
	dict set parameters mmin 1
	set mmin 1
    }
    if {$mmin > 4} {
	puts stderr "Capacitor lowest metal must be <= 4"
	# Also set mmax, avoids secondary error below.
	dict set parameters mmin 4
	dict set parameters mmax 4
	set mmin 4
	set mmax 4
    }
    if {$mmax > 4} {
	puts stderr "Capacitor highest metal must be <= 4"
	dict set parameters mmax 4
	set mmax 4
    }
    if {$mmin > $mmax} {
	puts stderr "Capacitor highest metal must be >= lowest metal"
	dict set parameters mmax $mmin
	set mmax $mmin
    }

    if {$w < $wmin} {
	puts stderr "Capacitor width must be >= $wmin"
	dict set parameters w $wmin
	set w $wmin
    } 
    if {$l < $lmin} {
	puts stderr "Capacitor length must be >= $lmin"
	dict set parameters l $lmin
	set l $lmin
    } 
    if {($wmax > 0) && ($w > $wmax)} {
	puts stderr "Capacitor width must be <= $wmax"
	dict set parameters w $wmax
	set w $wmax
    } 
    if {($lmax > 0) && ($l > $lmax)} {
	puts stderr "Capacitor length must be <= $lmax"
	dict set parameters l $lmax
	set l $lmax
    } 
    return $parameters
}

proc sg13cmos5l::capacitor_check {parameters} {
    return [sg13cmos5l::cap_check capacitor $parameters]
}

#---------------------------------------------------------
# Capacitor:  draw the device
#---------------------------------------------------------

proc sg13cmos5l::cap_draw_interdigitated {parameters} {

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    set curunits [units]
    units microns 
    tech unlock *

    # Main parameters used for calculating the layout (other than the input
    # arguments):
    # 
    # edgel:  Width of left edge.  Determined by the size of contacts.
    #		Extra width given to metal4 for the larger via4.
    # edger:  Width of right edge.  Determined by the size of contacts.
    #		via4 does not contact on this side.
    # edget:  Width of top edge.  Determined by the size of contacts.
    #		Extra width given to metal4 for the larger via4.
    # edgeb:  Width of bottom edge.  Determined by the size of contacts.
    #		via4 does not contact on this side.
    # mw:     Minimum metal width.  Fingers will be this wide.
    # ms:     Minimum metal space.  Fingers will be separated by this
    #		amount unless run-length rules require extra space.
    # msxl:    Extra spacing required to satisfy run-length rules (left side)
    # msxr:    Extra spacing required to satisfy run-length rules (right side)
    # msxt:    Extra spacing required to satisfy run-length rules (top side)
    # msxb:    Extra spacing required to satisfy run-length rules (bottom side)
    # viaw:   Width of a via contacting to the metal layer above.
    # viabe:  Minimum bottom metal enclosure of via (only applies to via1).
    # m:      The metal layer index of the current metal layer
    # m1:     The metal layer index one less than m
    # viaw1:  The via width of the via between m1 and m
    # viabe1: Minimum bottom metal enclosure of the via between m1 and m
    #		(only relevant for via1).
    # viate1: Minimum top metal enclosure of the via between m1 and m
    #		(only relevant for via4).
    #
    # General topology:
    # 1. Fingers alternate in direction between metal layers.
    # 2. The bottom-most metal layer always has vertical fingers.
    # 3. The bottom-most metal layer and every other layer above it connects
    #    on the bottom and left sides.  All other layers connect on the top
    #    and right side.
    # 4. All but the outermost fingers connect to alternating sides.
    # 5. The outermost fingers connect to the side appropriate for the via
    #    stack.  This may break the fingering pattern by being the same
    #    terminal as the finger next to it.
    # 6. If the (thick) top metal is used, then it connects only on the top
    #	 and left sides.  It keeps a regular pattern of fingers.
    # 7. If the (thick) top metal is used, then the metal 4 edges are widened
    #	 on the top and left sides to accomodate the via4 contact.

    # Parameters:
    # mmin:     Bottom metal (1 to 5)
    # mmax:     Top metal (1 to 5)
    # w:        Width of capacitor layout
    # l:        Length (height) of capacitor layout
    # subblock: Add PWELLBLK under the device (disallows devices under the cap)

    set orient 0
    for {set m $mmin} {$m <= $mmax} {incr m} {
	set metal m$m
	set mw [tech drc width $metal]
	set ms [tech drc spacing $metal]
	# Extra metal space gets adjusted later as needed.
	set msxl 0.0
	set msxr 0.0
	set msxt 0.0
	set msxb 0.0
	if {$m == 1} {
	    set viabe 0.005
	} else {
	    set viabe 0
	}

	# Wide metal for run-length rule is 0.3 for m1, 0.39 for other metals.
	if {$m == 1} {
	    set widem 0.3
	    set extras 0.04
	} else {
	    set widem 0.39
	    set extras 0.03
	}

	# Values for the metal layer below the current one
	# (When m = 1 these values are not used.)

	set m1 [- $m 1]
	set viaw1 [tech drc width via3]
	set viate1 0
	if {$m == 2} {
	    set viabe1 0.005
	} else {
	    set viabe1 0
	}

	# Regular pitch of fingers, not including the ends
	set pitch [+ $mw $ms]

	# For most metals, the metal width on the edge is the via size
	# Use via3 as representative (they're all the same)
	set viaw [tech drc width via3]

	# Determine the width of edges.  For most metals this is independent
	# of orientation.
	if {$m == 1} {
	    set edgeb $mw	;# default is metal width only if no metal 2
	    if {$mmax >= 2} {
		# Edge must be wide enough for a contact + metal 1 surround
		set edgeb [+ $viaw [* 2 $viabe]]
	    }
	    set edget $edgeb
	    set edger $edgeb
	    set edgel $edgeb
	} elseif {$m == 2} {
	    set edgeb $viaw	;# default is metal width only if no metal 1
	    if {$mmin == 1} {
		set edgeb [+ $mw $viabe1]	;# because via1 is offset by $viabe
	    }
	    set edget $edgeb
	    set edger $edgeb
	    set edgel $edgeb
	} else {
	    set edgeb $viaw
	    set edget $edgeb
	    set edger $edgeb
	    set edgel $edgeb
	}

	# Now determine how many fingers will fit in the layer's orientation.
	# If the width does not match an integer number of fingers exactly,
	# then the extra amount is added to the edges.  For metal 4 when
	# metal 5 is present, the top and left sides have wide enough metal 4
	# to trigger a run-length width rule, so incorporate the extra space.
	
	if {$orient == 0} {	;# Vertical fingers
	    set wbase [+ $edgel $edger]
            # nfxi = number of interior fingers (not counting the edges)
	    set nfxi [int [/ [- $w [+ $wbase $ms]] $pitch]]

	    # Find the remainder of area to distribute to the edges
	    set xdelta [/ [- $w [+ [* $nfxi $pitch] $ms $wbase]] 2.0]
	    set edgel [+ $edgel $xdelta]
	    set edger [+ $edger $xdelta]


	    # If edges are wider than $widem then reduce by $extras
	    if {$edgel > $widem} {
		set msxl $extras
		set edgel [- $edgel $msxl]
	    }
	    if {$edger > $widem} {
		set msxr $extras
		set edger [- $edger $msxr]
	    }

	} else {	;# orient == 1,  Horizontal fingers
	    set lbase [+ $edget $edgeb]
            # nfyi = number of interior fingers (not counting the edges)
	    set nfyi [int [/ [- $l [+ $lbase $ms]] $pitch]]

	    # Find the remainder of area to distribute to the edges
	    set ydelta [/ [- $l [+ [* $nfyi $pitch] $ms $lbase]] 2.0]
	    set edget [+ $edget $ydelta]
	    set edgeb [+ $edgeb $ydelta]

	    # If edges are wider than 0.39um then reduce by $extras
	    if {$edget > $widem} {
		set msxt $extras
		set edget [- $edget $msxt]
	    }
	    if {$edgeb > $widem} {
		set msxb $extras
		set edgeb [- $edgeb $msxb]
	    }
	}

	# Paint the contacts based on the values for the metal on *top* of
	# the contact.

	if {$m > $mmin} {
	    # Get the maximum value of the edge widths for both the top metal
	    # and the bottom metal of the contact.
	    set maxedgel [max $edgel $lastedgel]
	    set maxedger [max $edger $lastedger]
	    set maxedgeb [max $edgeb $lastedgeb]
	    set maxedget [max $edget $lastedget]

	    # Contact bottom side
	    set bbox_llx [+ $maxedgel $pitch]
	    set bbox_urx [- $w [+ $maxedger $pitch]]
	    set bbox_lly $viabe1
	    set bbox_ury [+ $bbox_lly $viaw1]
	    box values $bbox_llx $bbox_lly $bbox_urx $bbox_ury
	    paint via$m1

	    # Contact left side
	    set bbox_lly [+ $maxedgeb $ms]
	    set bbox_ury [- $l [+ $maxedget $pitch]]
	    set bbox_llx [+ $viabe1 $viate1]
	    set bbox_urx [+ $bbox_llx $viaw1]
	    if {[- $bbox_ury $bbox_lly] < $viaw1} {
		set bbox_ury [+ $bbox_lly $viaw1]
	    }
	    box values $bbox_llx $bbox_lly $bbox_urx $bbox_ury
	    paint via$m1

	    # Contact right side (except for via4)
	    set bbox_lly [+ $maxedgeb $pitch]
	    set bbox_ury [- $l [+ $maxedget $ms]]
	    set bbox_urx [- $w $viabe1]
	    set bbox_llx [- $bbox_urx $viaw1]
	    box values $bbox_llx $bbox_lly $bbox_urx $bbox_ury
	    paint via$m1

	    # Contact top side
	    set bbox_ury [- $l [+ $viabe1 $viate1]]
	    set bbox_lly [- $bbox_ury $viaw1]
	    set bbox_llx [+ $maxedgel $pitch]
	    set bbox_urx [- $w [+ $maxedger $ms]]
	    if {[- $bbox_urx $bbox_llx] < $viaw1} {
		set bbox_urx [+ $bbox_llx $viaw1]
	    }
	    box values $bbox_llx $bbox_lly $bbox_urx $bbox_ury
	    paint via$m1
	}
	
	# Now paint the fingers 
	set bbox_llx 0
	set bbox_lly 0
	set bbox_urx 0
	set bbox_ury 0

	if {$orient == 0} {	;# Vertical fingers
	    # Draw the left edge
	    set bbox_llx 0
	    set bbox_urx $edgel
	    set bbox_lly 0
	    set bbox_ury $l
	    box values $bbox_llx $bbox_lly $bbox_urx $bbox_ury
	    paint $metal

	    # Draw the interior fingers
	    for {set x 0} {$x < $nfxi} {incr x} {
		set bbox_llx [+ [* $x $pitch] $edgel $msxl $ms]
		set bbox_urx [+ $bbox_llx $mw]
		set bbox_lly 0
		set bbox_ury $l

		box values $bbox_llx $bbox_lly $bbox_urx $bbox_ury
		if {[% $x 2] == 0} {
		    set inset [+ $edget $ms $msxt $viabe1]
		    box grow n -$inset
		} else {
		    set inset [+ $edgeb $ms $msxb $viabe1]
		    box grow s -$inset
		}
		paint $metal
	    }

	    # Draw the right edge
	    set bbox_llx [+ [* $nfxi $pitch] $edgel $msxl $msxr $ms]
	    set bbox_urx $w	;# should = $bbox_llx + $edger
	    set bbox_lly 0
	    set bbox_ury $l
	    box values $bbox_llx $bbox_lly $bbox_urx $bbox_ury
	    paint $metal

	    # Draw the bottom edge
	    set bbox_llx 0
	    set bbox_lly 0
	    set bbox_ury $edgeb
	    set bbox_urx [- $w [+ $edger $ms $msxr]]
	    box values $bbox_llx $bbox_lly $bbox_urx $bbox_ury
	    paint $metal

	    # Draw the top edge
	    set bbox_llx [+ $edgel $ms $msxl]
	    set bbox_lly [- $l $edget]
	    set bbox_ury $l
	    set bbox_urx $w
	    box values $bbox_llx $bbox_lly $bbox_urx $bbox_ury
	    paint $metal

	} else {	;# orient == 1;  Horizontal fingers
	    # Draw the bottom edge
	    set bbox_llx 0
	    set bbox_urx $w
	    set bbox_lly 0
	    set bbox_ury $edgeb
	    box values $bbox_llx $bbox_lly $bbox_urx $bbox_ury
	    paint $metal

	    # Draw the interior fingers
	    for {set y 0} {$y < $nfyi} {incr y} {
		set bbox_llx 0
		set bbox_urx $w
		set bbox_lly [+ [* $y $pitch] $edgeb $ms $msxb]
		set bbox_ury [+ $bbox_lly $mw]

		box values $bbox_llx $bbox_lly $bbox_urx $bbox_ury
		if {[% $y 2] == 0} {
		    set inset [+ $edgel $ms $msxl $viabe1]
		    box grow w -$inset
		} else {
		    set inset [+ $edger $ms $msxr $viabe1]
		    box grow e -$inset
		}
		paint $metal
	    }

	    # Draw the top edge
	    set bbox_llx 0
	    set bbox_urx $w
	    set bbox_lly [+ [* $nfyi $pitch] $edgeb $ms $msxb $msxt]
	    set bbox_ury $l	;# should = $bbox_lly + $edget
	    box values $bbox_llx $bbox_lly $bbox_urx $bbox_ury
	    paint $metal

	    # Draw the left edge
	    set bbox_llx 0
	    set bbox_lly 0
	    set bbox_urx $edgel
	    set bbox_ury [- $l [+ $edget $ms $msxt]]
	    box values $bbox_llx $bbox_lly $bbox_urx $bbox_ury
	    paint $metal

	    # Draw the right edge
	    set bbox_llx [- $w $edger]
	    set bbox_lly [+ $edgeb $ms $msxb]
	    set bbox_urx $w
	    set bbox_ury $l
	    box values $bbox_llx $bbox_lly $bbox_urx $bbox_ury
	    paint $metal
	}

	# Save the edge sizes for proper placement of contacts on the
	# next loop.
	set lastedgel $edgel
	set lastedger $edger
	set lastedget $edget
	set lastedgeb $edgeb

	set orient [- 1 $orient]
    }

    # Final touches:
    # 1. Paint pwell ring around the device.
    # 2. Paint PWELLBLK under the device to minimize parasitic cap to
    #    the substrate.
    # 3. Mark this area as the device area
    # 4. Create ports and labels
    #
    # The pwell ring is 0.31um larger than the PWELLBLK so that abutting
    # devices leaves sufficient space between PWELLBLK areas.

    box values 0 0 $w $l
    if {$subblock != 0} {
	box grow c 0.31
	paint pwell
    }
    property FIXED_BBOX [box values]
    if {$subblock != 0} {
	box grow c -0.31
	paint pblock

	# On the bottom pwell, make a "sub!" substrate connection pin
	box position [/ $w 2.0] -0.155
	box size 0 0
	label sub! c pwell
	port make
    }

    # On the top metal, make labels for terminals c1 (left) and c2 (top)
    box size 0 0
    box position 0.01 [/ $l 2.0]
    label c1 c m$mmax
    port make
    box position [/ $w 2.0] [- $l 0.01]
    label c2 c m$mmax
    port make

    # Extract the layout parasitic
    extract do local
    extract all

    # Read the SPICE subcircuit and get the capacitor value
    set capvalaF 0
    set cname [cellname list self]
    set f [open ${cname}.ext]
    while {true} {
	gets $f line
	if {[eof $f]} {
	    break
	}
	if {[string first cap $line 0] == 0} {
	    set llist [split $line]
	    set capvalaF [lindex $llist 3]
	    break
	}
    }
    close $f

    # Value of the device in the .ext file should be in fF, as opposed to
    # the parasitic value in aF, so convert from aF to fF.
    set value [* $capvalaF 1.0e-3]
   
    # The extraction file is no longer needed
    file delete ${cname}.ext

    # Set a property on this cell so that the entire cell extracts as an
    # ideal (unmodeled) capacitor component.  Note that handling the
    # capacitor this way loses the parasitic to substrate.

    if {$value != 0} {
	set propstr [format "devcap None 0 0 1 1 %.4f c1 0 0 c2 0 0" $value]
	property string device $propstr
    }

    # Restore units used prior to calling this procedure
    units {*}$curunits
    tech revert
}

#----------------------------------------------------------------

proc sg13cmos5l::capacitor_draw {parameters} {
    set drawdict [dict merge $sg13cmos5l::ruleset $parameters]
    return [sg13cmos5l::cap_draw_interdigitated $drawdict]
}

#-----------------------------------------------------------------------
