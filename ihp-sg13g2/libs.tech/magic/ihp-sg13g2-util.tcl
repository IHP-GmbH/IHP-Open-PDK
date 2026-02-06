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
# Menu callback function to read a SPICE netlist and generate an
# initial layout using the IHP sg13g2A gencells.
#----------------------------------------------------------------

proc sg13g2::importspice {} {
   global CAD_ROOT

   set Layoutfilename [ tk_getOpenFile -filetypes \
	    {{SPICE {.spice .spc .spi .ckt .cir .sp \
	    {.spice .spc .spi .ckt .cir .sp}}} {"All files" {*}}}]
   if {$Layoutfilename != ""} {
      magic::netlist_to_layout $Layoutfilename sg13g2
   }
}

#----------------------------------------------------------------
# Polygon drawing routine --- Given number of points and
# edge diameter, return a set of coordinate pairs describing
# the polygon, centered at (0, 0).
#
# Normally width = height but for, e.g., a bond pad, it may
# be non-square, in which case the middle segment is elongated.
#----------------------------------------------------------------

proc sg13g2::create_polygon {npoints width height} {

    if {$width < $height} {set minside $width} else {set minside $height}

    set angle [/ 180.0 $npoints]
    set adelta [/ 360.0 $npoints]
    set pi 3.1415926
    set rad [/ [* $angle $pi] 180]
    set rdelta [/ [* $adelta $pi] 180]

    # Expand width so that the flats of the polygon reach the value of "minside"
    set pwidth [/ [/ $minside 2.0] [cos $rad]]

    set pointlist {}	;# List of points to return

    for {set i 0} {$i < $npoints} {incr i} {
	set x [* $pwidth [cos $rad]]
	set y [* $pwidth [sin $rad]]
	set ux [magic::i2u [magic::magceil [magic::u2i $x]]]
	set uy [magic::i2u [magic::magceil [magic::u2i $y]]]
        if {$width > $minside} {
	    if {$ux > 0} {
		set ux [+ $ux [/ [- $width $minside] 2.0]]
	    } else {
		set ux [- $ux [/ [- $width $minside] 2.0]]
	    }
	}
	if {$height > $minside} {
	    if {$uy > 0} {
		set uy [+ $uy [/ [- $height $minside] 2.0]]
	    } else {
		set uy [- $uy [/ [- $height $minside] 2.0]]
	    }
	}
	lappend pointlist ${ux}um ${uy}um

	set angle [+ $angle $adelta]
	set rad [+ $rad $rdelta]
    }

    return $pointlist
}

#----------------------------------------------------------------
# Octagon and circle wire drawing routine
#----------------------------------------------------------------

proc sg13g2::create_wire {npoints width height} {

    if {$width < $height} {set minside $width} else {set minside $height}

    set angle [/ 180.0 $npoints]
    set adelta [/ 360.0 $npoints]
    set pi 3.1415926
    set rad [/ [* $angle $pi] 180]
    set rdelta [/ [* $adelta $pi] 180]

    # Expand width so that the flats of the polygon reach the value of "minside"
    set wwidth [/ [/ $minside 2.0] [cos $rad]]

    set pointlist {}	;# List of points to return

    # Compute point at angle 0 for the wire endpoints, so that the
    # wire starts and ends on a straight edge.
    set x [/ $minside 2.0]
    set y 0.0
    set ux [magic::i2u [magic::magceil [magic::u2i $x]]]
    set uy [magic::i2u [magic::magceil [magic::u2i $y]]]
    if {$width > $minside} {
	if {$ux > 0} {
	    set ux [+ $ux [/ [- $width $minside] 2.0]]
	} else {
	    set ux [- $ux [/ [- $width $minside] 2.0]]
	}
    }
    lappend pointlist ${ux}um ${uy}um

    for {set i 0} {$i < $npoints} {incr i} {
	set x [* $wwidth [cos $rad]]
	set y [* $wwidth [sin $rad]]
	set ux [magic::i2u [magic::magfloor [magic::u2i $x]]]
	set uy [magic::i2u [magic::magfloor [magic::u2i $y]]]
        if {$width > $minside} {
	    if {$ux > 0} {
		set ux [+ $ux [/ [- $width $minside] 2.0]]
	    } else {
		set ux [- $ux [/ [- $width $minside] 2.0]]
	    }
	}
	if {$height > $minside} {
	    if {$uy > 0} {
		set uy [+ $uy [/ [- $height $minside] 2.0]]
	    } else {
		set uy [- $uy [/ [- $height $minside] 2.0]]
	    }
	}
	lappend pointlist ${ux}um ${uy}um

	set angle [+ $angle $adelta]
	set rad [+ $rad $rdelta]
    }

    # Repeat the first coordinate pair at the end of pointlist
    lappend pointlist {*}[lrange $pointlist 0 1]

    return $pointlist
}

#----------------------------------------------------------------
# getbox:  Get the current cursor box, in microns
#----------------------------------------------------------------

proc sg13g2::getbox {} {
    set curbox [box values]
    set newbox []
    set oscale [cif scale out]
    for {set i 0} {$i < 4} {incr i} {
        set v [* [lindex $curbox $i] $oscale]
        lappend newbox $v
    }
    return $newbox
}

#----------------------------------------------------------------
# minareabox:  Increase box size to meet minimum area requirement
# arguments:  area (in sq. microns), direction to grow (horz or
# vert).
#----------------------------------------------------------------

proc sg13g2::minareabox {minarea dir} {
    set curbox [box values]
    set oscale [cif scale out]
    set iarea [/ $minarea [* $oscale $oscale]]

    set curw [- [lindex $curbox 2] [lindex $curbox 0]]
    set curh [- [lindex $curbox 3] [lindex $curbox 1]]
    set cura [* $curw $curh]
    if {$cura < $iarea} {
	if {$dir == "horz"} {
	    set neww [- [/ $iarea $curh] $curw]
	    set hneww [ceil [/ $neww 2.0]]
	    box grow e ${hneww}i
	    box grow w ${hneww}i
	} else {	;# dir == "vert"
	    set newh [- [/ $iarea $curw] $curh]
	    set hnewh [ceil [/ $newh 2.0]]
	    box grow h ${hnewh}i
	    box grow s ${hnewh}i
	}
    }
}

#----------------------------------------------------------------
# setbox:  Set the current cursor box from the values, in microns
#----------------------------------------------------------------

proc sg13g2::setbox {umbox} {
    set llx [lindex $umbox 0]
    set lly [lindex $umbox 1]
    set urx [lindex $umbox 2]
    set ury [lindex $umbox 3]
    box values ${llx}um ${lly}um ${urx}um ${ury}um
}

#----------------------------------------------------------------
# unionbox:  Get the union bounding box of box1 and box2
#----------------------------------------------------------------

proc sg13g2::unionbox {box1 box2} {
    set newbox []
    for {set i 0} {$i < 2} {incr i} {
        set v [lindex $box1 $i]
        set o [lindex $box2 $i]
        if {$v < $o} {
            lappend newbox $v
        } else {
            lappend newbox $o
        }
    }
    for {set i 2} {$i < 4} {incr i} {
        set v [lindex $box1 $i]
        set o [lindex $box2 $i]
        if {$v > $o} {
            lappend newbox $v
        } else {
            lappend newbox $o
        }
    }
    return $newbox
}

#----------------------------------------------------------------
# Draw a contact
#----------------------------------------------------------------

proc sg13g2::draw_contact {w h s o x atype ctype mtype {orient vert}} {

    # Draw a minimum-size diff contact centered at current position
    # w is width, h is height.  Minimum size ensured.
    # x is contact size
    # s is contact diffusion (or poly) surround
    # o is contact metal surround
    # atype is active (e.g., ndiff) or bottom metal if a via
    # ctype is contact (e.g., ndc)
    # mtype is metal (e.g., m1) or top metal if a via
    # orient is the orientation of the contact top layer

    # Set orientations for the bottom material based on material type.
    # All diffusions overlap on all sides.  Metal1 overlaps on all
    # sides but in different amounts depending on the direction.

    set aorient "full"

    pushbox
    box size 0 0
    if {$w < $x} {set w $x}
    if {$h < $x} {set h $x}
    set hw [/ $w 2.0]
    set hh [/ $h 2.0]
    box grow n ${hh}um
    box grow s ${hh}um
    box grow e ${hw}um
    box grow w ${hw}um
    paint ${ctype}
    pushbox
    # Bottom layer surrounded on sides as declared by aorient
    if {($aorient == "vert") || ($aorient == "full")} {
	box grow n ${s}um
	box grow s ${s}um
    }
    if {($aorient == "horz") || ($aorient == "full")} {
	box grow e ${s}um
	box grow w ${s}um
    }
    paint ${atype}
    set extents [sg13g2::getbox]
    popbox
    # Top layer surrounded on sides as declared by orient
    if {($orient == "vert") || ($orient == "full")} {
        box grow n ${o}um
        box grow s ${o}um
    }
    if {($orient == "horz") || ($orient == "full")} {
        box grow e ${o}um
        box grow w ${o}um
    }
    paint ${mtype}
    popbox
    return $extents
}

#----------------------------------------------------------------
# Draw a metal1 ring
#----------------------------------------------------------------

proc sg13g2::metal_ring {gw gh parameters} {

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    set hx [/ $contact_size 2.0]
    set hw [/ $gw 2.0]
    set hh [/ $gh 2.0]

    pushbox
    box size 0 0

    set hmetw [/ [+ $gw $contact_size] 2.0]
    set hmeth [/ [+ $gh $contact_size] 2.0]
    pushbox
    box move n ${hh}um
    box grow n ${hx}um
    box grow s ${hx}um
    box grow e ${hmetw}um
    box grow w ${hmetw}um
    paint m1
    popbox
    pushbox
    box move s ${hh}um
    box grow n ${hx}um
    box grow s ${hx}um
    box grow e ${hmetw}um
    box grow w ${hmetw}um
    paint m1
    popbox
    pushbox
    box move e ${hw}um
    box grow e ${hx}um
    box grow w ${hx}um
    box grow n ${hmeth}um
    box grow s ${hmeth}um
    paint m1
    popbox
    pushbox
    box move w ${hw}um
    box grow e ${hx}um
    box grow w ${hx}um
    box grow n ${hmeth}um
    box grow s ${hmeth}um
    paint m1
    popbox
}

#----------------------------------------------------------------
# Draw a guard ring
#----------------------------------------------------------------

proc sg13g2::guard_ring {gw gh parameters} {

    # Set local default values if they are not in parameters
    set rlcov 100	;# Right-left contact coverage percentage
    set tbcov 100	;# Top-bottom contact coverage percentage
    set grc 1		;# Draw right side contact
    set glc 1		;# Draw left side contact
    set gtc 1		;# Draw right side contact
    set gbc 1		;# Draw left side contact
    set viagb 0		;# Draw bottom side via
    set viagt 0		;# Draw top side via
    set viagr 0		;# Draw right side via
    set viagl 0		;# Draw left side via
    set full_metal 1	;# Draw full (continuous) metal ring
    set guard_sub_type	 pwell	;# substrate type under guard ring
    set guard_sub_surround  0	;# substrate type surrounds guard ring
    set plus_diff_type   nsd	;# guard ring diffusion type
    set plus_contact_type nsc	;# guard ring diffusion contact type
    set plus_contact_size 0	;# guard ring contact size
    set sub_type	 pwell	;# substrate type
    set diff_width 0	;# default width if greater than minimum
    set bulk ""		;# Default no port label

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Set guard_sub_type to sub_type if it is not defined
    if {![dict exists $parameters guard_sub_type]} {
	set guard_sub_type $sub_type
    }

    # set plus_contact_size to contact_size if it is not defined
    if {$plus_contact_size == 0} {
	set plus_contact_size $contact_size
    }

    set hx [/ $plus_contact_size 2.0]
    set hw [/ $gw 2.0]
    set hh [/ $gh 2.0]

    # Compute diffusion width (the larger of contact + minimum surround, or
    # the value set by "diff_width")
    set difft [+ $plus_contact_size $diff_surround $diff_surround]
    if {$difft < $diff_width} {set difft $diff_width}
    set hdifft [/ $difft 2.0]
    # Compute guard ring diffusion width and height
    set hdiffw [/ [+ $gw $difft] 2.0]
    set hdiffh [/ [+ $gh $difft] 2.0]

    pushbox
    box size 0 0

    pushbox
    box move n ${hh}um
    box grow n ${hdifft}um
    box grow s ${hdifft}um
    box grow e ${hdiffw}um
    box grow w ${hdiffw}um
    paint $plus_diff_type
    if {$guard_sub_surround > 0} {
	box grow c ${guard_sub_surround}um
	paint $guard_sub_type
    }
    popbox
    pushbox
    box move s ${hh}um
    pushbox
    box grow n ${hdifft}um
    box grow s ${hdifft}um
    box grow e ${hdiffw}um
    box grow w ${hdiffw}um
    paint $plus_diff_type
    if {$guard_sub_surround > 0} {
	box grow c ${guard_sub_surround}um
	paint $guard_sub_type
    }
    popbox
    # At guard ring bottom center, place a port if requested
    if {$bulk != ""} {
	label $bulk c $plus_diff_type
	select area label
	port make
    }
    popbox
    pushbox
    box move e ${hw}um
    box grow e ${hdifft}um
    box grow w ${hdifft}um
    box grow n ${hdiffh}um
    box grow s ${hdiffh}um
    paint $plus_diff_type
    if {$guard_sub_surround > 0} {
	box grow c ${guard_sub_surround}um
	paint $guard_sub_type
    }
    popbox
    pushbox
    box move w ${hw}um
    box grow e ${hdifft}um
    box grow w ${hdifft}um
    box grow n ${hdiffh}um
    box grow s ${hdiffh}um
    paint $plus_diff_type
    if {$guard_sub_surround > 0} {
	box grow c ${guard_sub_surround}um
	paint $guard_sub_type
    }
    popbox

    if {$full_metal} {
	set hmetw [/ [+ $gw $plus_contact_size] 2.0]
	set hmeth [/ [+ $gh $plus_contact_size] 2.0]
	pushbox
	box move n ${hh}um
	box grow n ${hx}um
	box grow s ${hx}um
	box grow e ${hmetw}um
	box grow w ${hmetw}um
	paint m1
	popbox
	pushbox
	box move s ${hh}um
	box grow n ${hx}um
	box grow s ${hx}um
	box grow e ${hmetw}um
	box grow w ${hmetw}um
	paint m1
	popbox
	pushbox
	box move e ${hw}um
	box grow e ${hx}um
	box grow w ${hx}um
	box grow n ${hmeth}um
	box grow s ${hmeth}um
	paint m1
	popbox
	pushbox
	box move w ${hw}um
	box grow e ${hx}um
	box grow w ${hx}um
	box grow n ${hmeth}um
	box grow s ${hmeth}um
	paint m1
	popbox
    }

    # Set guard ring height so that contact metal reaches to end, scale by $per
    # set ch [* [+ $gh $plus_contact_size [* $metal_surround -2.0]] [/ $rlcov 100.0]]
    set ch [* [- $gh $plus_contact_size [* [+ $metal_surround $metal_spacing] \
		2.0]] [/ $rlcov 100.0]]
    if {$ch < $plus_contact_size} {set ch $plus_contact_size}

    # Set guard ring width so that contact metal reaches to side contacts
    set cw [* [- $gw $plus_contact_size [* [+ $metal_surround $metal_spacing] \
		2.0]] [/ $tbcov 100.0]]
    if {$cw < $plus_contact_size} {set cw $plus_contact_size}

    if {$tbcov > 0.0} {
        if {$gtc == 1} {
            pushbox
            box move n ${hh}um
            sg13g2::draw_contact $cw 0 $diff_surround $metal_surround \
		$plus_contact_size $plus_diff_type \
		$plus_contact_type m1 horz
            popbox
	}
	if {$gbc == 1} {
	    pushbox
	    box move s ${hh}um
	    sg13g2::draw_contact $cw 0 $diff_surround $metal_surround \
		$plus_contact_size $plus_diff_type \
		$plus_contact_type m1 horz
	    popbox
	}
    }
    if {$rlcov > 0.0} {
        if {$grc == 1} {
            pushbox
            box move e ${hw}um
            sg13g2::draw_contact 0 $ch $diff_surround $metal_surround \
		$plus_contact_size $plus_diff_type \
		$plus_contact_type m1 vert
            popbox
        }
        if {$glc == 1} {
            pushbox
            box move w ${hw}um
            sg13g2::draw_contact 0 $ch $diff_surround $metal_surround \
		$plus_contact_size $plus_diff_type \
		$plus_contact_type m1 vert
            popbox
        }
    }

    # Vias
    if {$viagb != 0} {
        pushbox
    	set ch $via_size
    	set cw [* [- $gw $via_size] [/ [expr abs($viagb)] 100.0]]
    	if {$cw < $via_size} {set cw $via_size}
        box move s ${hh}um
	box grow n [/ $ch 2.0]um
	box grow s [/ $ch 2.0]um
        set anchor [string index $viagb 0]
	if {$anchor == "+"} {
            box move w [/ [- $gw $via_size] 2.0]um
	    box grow e ${cw}um
	} elseif {$anchor == "-"} {
            box move e [/ [- $gw $via_size] 2.0]um
	    box grow w ${cw}um
	} else {
	    box grow e [/ $cw 2.0]um
	    box grow w [/ $cw 2.0]um
	}
        sg13g2::via1_draw horz
        popbox
    }
    if {$viagt != 0} {
        pushbox
    	set ch $via_size
    	set cw [* [- $gw $via_size] [/ [expr abs($viagt)] 100.0]]
    	if {$cw < $via_size} {set cw $via_size}
        box move n ${hh}um
	box grow n [/ $ch 2.0]um
	box grow s [/ $ch 2.0]um
        set anchor [string index $viagt 0]
	if {$anchor == "+"} {
            box move w [/ [- $gw $via_size] 2.0]um
	    box grow e ${cw}um
	} elseif {$anchor == "-"} {
            box move e [/ [- $gw $via_size] 2.0]um
	    box grow w ${cw}um
	} else {
	    box grow e [/ $cw 2.0]um
	    box grow w [/ $cw 2.0]um
	}
        sg13g2::via1_draw horz
        popbox
    }
    if {$viagr != 0} {
        pushbox
    	set ch [* [- $gh $via_size] [/ [expr abs($viagr)] 100.0]]
    	if {$ch < $via_size} {set ch $via_size}
    	set cw $via_size
        box move e ${hw}um
	box grow e [/ $cw 2.0]um
	box grow w [/ $cw 2.0]um
        set anchor [string index $viagr 0]
	if {$anchor == "+"} {
            box move s [/ [- $gh $via_size] 2.0]um
	    box grow n ${ch}um
	} elseif {$anchor == "-"} {
            box move n [/ [- $gh $via_size] 2.0]um
	    box grow s ${ch}um
	} else {
	    box grow n [/ $ch 2.0]um
	    box grow s [/ $ch 2.0]um
	}
        sg13g2::via1_draw vert
        popbox
    }
    if {$viagl != 0} {
        pushbox
    	set ch [* [- $gh $via_size] [/ [expr abs($viagl)] 100.0]]
    	if {$ch < $via_size} {set ch $via_size}
    	set cw $via_size
        box move w ${hw}um
	box grow e [/ $cw 2.0]um
	box grow w [/ $cw 2.0]um
        set anchor [string index $viagl 0]
	if {$anchor == "+"} {
            box move s [/ [- $gh $via_size] 2.0]um
	    box grow n ${ch}um
	} elseif {$anchor == "-"} {
            box move n [/ [- $gh $via_size] 2.0]um
	    box grow s ${ch}um
	} else {
	    box grow n [/ $ch 2.0]um
	    box grow s [/ $ch 2.0]um
	}
        sg13g2::via1_draw vert
        popbox
    }

    pushbox
    box grow e ${hw}um
    box grow w ${hw}um
    box grow n ${hh}um
    box grow s ${hh}um
    # Create boundary using properties
    property FIXED_BBOX [box values]
    box grow c ${hx}um  ;# to edge of contact
    box grow c ${diff_surround}um  ;# to edge of diffusion
    box grow c ${sub_surround}um  ;# sub/well overlap of diff (NOT guard_sub)
    paint $sub_type
    set cext [sg13g2::getbox]
    popbox
    popbox

    return $cext
}

#-------------------------------------------------------------------
# General-purpose routines for the PDK script in all technologies
#-------------------------------------------------------------------
# 
#----------------------------------------
# Number Conversion Functions
#----------------------------------------

#---------------------
# Microns to Lambda
#---------------------
proc magic::u2l {micron} {
    set techlambda [magic::tech lambda]
    set tech1 [lindex $techlambda 1]
    set tech0 [lindex $techlambda 0]
    set tscale [expr {$tech1 / $tech0}]
    set lambdaout [expr {((round([magic::cif scale output] * 10000)) / 10000.0)}]
    return [expr $micron / ($lambdaout*$tscale) ]
}

#---------------------
# Lambda to Microns
#---------------------
proc magic::l2u {lambda} {
    set techlambda [magic::tech lambda]
    set tech1 [lindex $techlambda 1] ; set tech0 [lindex $techlambda 0]
    set tscale [expr {$tech1 / $tech0}]
    set lambdaout [expr {((round([magic::cif scale output] * 10000)) / 10000.0)}]
    return [expr $lambda * $lambdaout * $tscale ]
}

#---------------------
# Internal to Microns
#---------------------
proc magic::i2u { value } {
    set value [expr {((round([magic::cif scale output] * 10000)) / 10000.0) * $value}]
    return [format "%.3f" $value]
}

#---------------------
# Microns to Internal
#---------------------
proc magic::u2i {value} {
    return [expr {round($value / ((round([magic::cif scale output] * 10000)) / 10000.0))}]
}

#--------------------------------------------------------------------------
# Find the smallest integer value greater in magnitude than the given value
#--------------------------------------------------------------------------
proc magic::magceil {value} {
    if {$value < 0} {
	return [::tcl::mathfunc::floor $value]
    } else {
	return [::tcl::mathfunc::ceil $value]
    }
}

#--------------------------------------------------------------------------
# Find the largest integer value less in magnitude than the given value
#--------------------------------------------------------------------------
proc magic::magfloor {value} {
    if {$value < 0} {
	return [::tcl::mathfunc::ceil $value]
    } else {
	return [::tcl::mathfunc::floor $value]
    }
}

#---------------------
# Float to Spice 
#---------------------
proc magic::float2spice {value} { 
    if {$value >= 1.0e+6} { 
	set exponent 1e+6
	set unit "meg"
    } elseif {$value >= 1.0e+3} { 
	set exponent 1e+3
	set unit "k"
    } elseif { $value >= 1} { 
	set exponent 1
	set unit ""
    } elseif {$value >= 1.0e-3} { 
	set exponent 1e-3
	set unit "m"
    } elseif {$value >= 1.0e-6} { 
	set exponent 1e-6
	set unit "u"
    } elseif {$value >= 1.0e-9} { 
	set exponent 1e-9
	set unit "n"
    } elseif {$value >= 1.0e-12} { 
	set exponent 1e-12
	set unit "p"
    } elseif {$value >= 1.0e-15} { 
	set exponent 1e-15
	set unit "f"
    } else {
	set exponent 1e-18
	set unit "a"
    }
    set val [expr $value / $exponent]
    set val [expr int($val * 1000) / 1000.0]
    if {$val == 0} {set unit ""}
    return $val$unit
}

#---------------------
# Spice to Float
#---------------------
proc magic::spice2float {value {faultval 0.0}} { 
    # Remove trailing units, at least for some common combinations
    set value [string tolower $value]
    set value [string map {um u nm n uF n nF n pF p aF a} $value]
    set value [string map {meg "* 1.0e6" k "* 1.0e3" m "* 1.0e-3" u "* 1.0e-6" \
		 n "* 1.0 e-9" p "* 1.0e-12" f "* 1.0e-15" a "* 1.0e-15"} $value]
    if {[catch {set rval [expr $value]}]} {
	puts stderr "Value is not numeric!"
	set rval $faultval
    }
    return $rval
}

#---------------------
# Numeric Precision
#---------------------
proc magic::3digitpastdecimal {value} {
    set new [expr int([expr $value * 1000 + 0.5 ]) / 1000.0]
    return $new
}

#-------------------------------------------------------------------
# File Access Functions
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# Ensures that a cell name does not already exist, either in
# memory or on disk. Modifies the name until it does.
#-------------------------------------------------------------------
proc magic:cellnameunique {cellname} {
    set i 0
    set newname $cellname
    while {[cellname list exists $newname] != 0 || [magic::searchcellondisk $newname] != 0} {
	incr i
	set newname ${cellname}_$i
    }
    return $newname
}

#-------------------------------------------------------------------
# Looks to see if a cell exists on disk
#-------------------------------------------------------------------
proc magic::searchcellondisk {name} {
    set rlist {}
    foreach dir [path search] {
	set ftry [file join $dir ${name}.mag]
	if [file exists $ftry] {
	    return 1
	}
    }
    return 0
} 

#-------------------------------------------------------------------
# Checks to see if a cell already exists on disk or in memory
#-------------------------------------------------------------------
proc magic::iscellnameunique {cellname} {
    if {[cellname list exists $cellname] == 0 && [magic::searchcellondisk $cellname] == 0} { 
	return 1
    } else {
	return 0
    }
}

#----------------------------------------------------------------
