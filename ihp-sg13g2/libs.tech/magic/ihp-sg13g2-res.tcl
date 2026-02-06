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

proc sg13g2::res_recalc {field parameters} {
    set snake 0
    set sterm 0.0
    set caplen 0
    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }
    set val [magic::spice2float $val]
    set l [magic::spice2float $l]
    set w [magic::spice2float $w]

    if {$snake == 0} {
	# Straight resistor calculation
	switch  $field {
	    val { set l [expr ($val * ($w - $dw) - (2 * $term)) / $rho]
		  set w [expr ((2 * $term + $l * $rho) / $val) + $dw]
		}
	    w   { set val [expr (2 * $term + $l * $rho) / ($w - $dw)]
		  set l [expr ($val * ($w - $dw) - (2 * $term)) / $rho]
		}
	    l   { set val [expr (2 * $term + $l * $rho) / ($w - $dw)]
		  set w [expr ((2 * $term + $l * $rho) / $val) + $dw]
		}
	}
    } else {
        set term [expr $term + $sterm]
	# Snake resistor calculation
	switch  $field {
	    val { set l [expr (($val - $rho * ($nx - 1)) * ($w - $dw) \
			- (2 * $term) - ($rho * $caplen * ($nx - 1))) \
			/ ($rho * $nx)]

		  set w [expr ((2 * $term + $l * $rho * $nx \
			+ $caplen * $rho * ($nx - 1)) \
			/ ($val - $rho * ($nx - 1))) + $dw]
		}
	    w   { set val [expr $rho * ($nx - 1) + ((2 * $term) \
			+ ($rho * $l * $nx) + ($rho * $caplen * ($nx - 1))) \
			/ ($w - $dw)]

		  set l [expr (($val - $rho * ($nx - 1)) * ($w - $dw) \
			- (2 * $term) - ($rho * $caplen * ($nx - 1))) \
			/ ($rho * $nx)]
		}
	    l   { set val [expr $rho * ($nx - 1) + ((2 * $term) \
			+ ($rho * $l * $nx) + ($rho * $caplen * ($nx - 1))) \
			/ ($w - $dw)]

		  set w [expr ((2 * $term + $l * $rho * $nx \
			+ $caplen * $rho * ($nx - 1)) \
			/ ($val - $rho * ($nx - 1))) + $dw]
		}
	}
    }

    set val [magic::3digitpastdecimal $val]
    set w [magic::3digitpastdecimal $w]
    set l [magic::3digitpastdecimal $l]

    dict set parameters val $val
    dict set parameters w $w
    dict set parameters l $l

    return $parameters
}

#----------------------------------------------------------------
# Drawn resistors
#----------------------------------------------------------------

#----------------------------------------------------------------
# Resistor defaults:
#----------------------------------------------------------------
# User editable values:
#
#  val   Resistor value in ohms
#  w	 Width
#  l	 Length
#  t	 Number of turns
#  m	 Number devices in Y
#  nx	 Number devices in X
#  snake Use snake geometry (if not present, snake geometry not allowed)
#  dummy Flag to mark addition of dummy resistor
#
# Non-user editable values:
#
#  wmin  Minimum allowed width
#  lmin  Minimum allowed length
#  rho	 Resistance in ohms per square
#  dw    Delta width
#  term  Resistance per terminal
#  sterm Additional resistance per terminal for snake geometry
#----------------------------------------------------------------

#----------------------------------------------------------------
# rsil: Specify all user-editable default values and those
# needed by rp1_check
#----------------------------------------------------------------

proc sg13g2::rsil_defaults {} {
    return {w 0.50 l 2.00 m 1 nx 1 wmin 0.50 lmin 0.50 class resistor \
		rho 7.0 val 14.0 dummy 0 dw 0.0 term 0.0 \
		sterm 0.0 caplen 0 snake 0 guard 1 \
		glc 1 grc 1 gtc 1 gbc 1 roverlap 0 endcov 100 \
		full_metal 1 hv_guard 0 n_guard 0 vias 1 \
		viagb 0 viagt 0 viagl 0 viagr 0 doports 1}
}

proc sg13g2::rppd_defaults {} {
    return {w 0.50 l 2.00 m 1 nx 1 wmin 0.50 lmin 0.50 class resistor \
		rho 260.0 val 520.0 dummy 0 dw 0.0 term 0.0 \
		sterm 0.0 caplen 0 guard 1 glc 1 grc 1 gtc 1 gbc 1 \
		snake 0 full_metal 1 vias 1 n_guard 0 hv_guard 0 \
		viagb 0 viagt 0 viagl 0 viagr 0 doports 1}
}

proc sg13g2::rhigh_defaults {} {
    return {w 0.50 l 2.00 m 1 nx 1 wmin 0.50 lmin 0.50 class resistor \
		rho 1360 val 2720.0 dummy 0 dw 0.0 term 0.0 \
		sterm 0.0 caplen 0 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 \
		snake 0 full_metal 1 n_guard 0 hv_guard 0 vias 1 \
		viagb 0 viagt 0 viagl 0 viagr 0 doports 1}
}

#----------------------------------------------------------------
# metal resistors
#----------------------------------------------------------------
# rm*: Specify all user-editable default values and those needed
# by rm*_check
#----------------------------------------------------------------

proc sg13g2::rm1_defaults {} {
    return {w 0.160 l 0.100 m 1 nx 1 wmin 0.16 lmin 0.005 class resistor \
		compatible {rm1 rm2 rm3 rm4 rm5 rm6 rm7} \
		rho 0.110 val 0.069 dummy 0 dw 0.0 term 0.0 \
		roverlap 0 doports 1}
}

proc sg13g2::rm2_defaults {} {
    return {w 0.200 l 0.100 m 1 nx 1 wmin 0.20 lmin 0.005 class resistor \
		compatible {rm1 rm2 rm3 rm4 rm5 rm6 rm7} \
		rho 0.088 val 0.044 dummy 0 dw 0.0 term 0.0 \
		roverlap 0 doports 1}
}

proc sg13g2::rm3_defaults {} {
    return {w 0.200 l 0.100 m 1 nx 1 wmin 0.20 lmin 0.005 class resistor \
		compatible {rm1 rm2 rm3 rm4 rm5 rm6 rm7} \
		rho 0.088 val 0.044 dummy 0 dw 0.0 term 0.0 \
		roverlap 0 doports 1}
}

proc sg13g2::rm4_defaults {} {
    return {w 0.200 l 0.100 m 1 nx 1 wmin 0.20 lmin 0.005 class resistor \
		compatible {rm1 rm2 rm3 rm4 rm5 rm6 rm7} \
		rho 0.088 val 0.044 dummy 0 dw 0.0 term 0.0 \
		roverlap 0 doports 1}
}

proc sg13g2::rm5_defaults {} {
    return {w 0.200 l 0.100 m 1 nx 1 wmin 0.20 lmin 0.005 class resistor \
		compatible {rm1 rm2 rm3 rm4 rm5 rm6 rm7} \
		rho 0.088 val 0.044 dummy 0 dw 0.0 term 0.0 \
		roverlap 0 doports 1}
}

proc sg13g2::rm6_defaults {} {
    return {w 1.640 l 0.100 m 1 nx 1 wmin 1.64 lmin 0.005 class resistor \
		compatible {rm1 rm2 rm3 rm4 rm5 rm6 rm7} \
		rho 0.018 val 0.001098 dummy 0 dw 0.0 term 0.0 \
		roverlap 0 doports 1}
}

proc sg13g2::rm7_defaults {} {
    return {w 2.000 l 0.100 m 1 nx 1 wmin 2.00 lmin 0.005 class resistor \
		compatible {rm1 rm2 rm3 rm4 rm5 rm6 rm7} \
		rho 0.011 val 0.00055 dummy 0 dw 0.0 term 0.0 \
		roverlap 0 doports 1}
}

#----------------------------------------------------------------
# resistor: Conversion from SPICE netlist parameters to toolkit
#----------------------------------------------------------------

proc sg13g2::res_convert {parameters} {
    set pdkparams [dict create]
    dict for {key value} $parameters {
	switch -nocase $key {
	    l -
	    w {
		# Length and width are converted to units of microns
		set value [magic::spice2float $value]
		# set value [expr $value * 1e6]
		set value [magic::3digitpastdecimal $value]
		dict set pdkparams [string tolower $key] $value
	    }
	    default {
		# Allow unrecognized parameters to be passed unmodified
		dict set pdkparams $key $value
	    }
	}
    }
    return $pdkparams
}

#----------------------------------------------------------------

proc sg13g2::rsil_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::rppd_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::rhigh_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::rm1_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::rm2_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::rm3_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::rm4_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::rm5_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::rm6_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::rm7_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

#----------------------------------------------------------------
# resistor: Interactively specifies the fixed layout parameters
#----------------------------------------------------------------

proc sg13g2::res_dialog {device parameters} {
    # Editable fields:      w, l, t, nx, m, val
    # Checked fields:  

    magic::add_entry val "Value (ohms)" $parameters
    if {[dict exists $parameters snake]} {
	sg13g2::compute_ltot $parameters
	magic::add_message ltot "Total length (um)" $parameters
    }
    magic::add_entry l "Length (um)" $parameters
    magic::add_entry w "Width (um)" $parameters
    magic::add_entry nx "X Repeat" $parameters
    magic::add_entry m "Y Repeat" $parameters
    if {[dict exists $parameters endcov]} {
	magic::add_entry endcov "End contact coverage (%)" $parameters
    }

    if {[dict exists $parameters compatible]} {
	set sellist [dict get $parameters compatible]
	magic::add_selectlist gencell "Device type" $sellist $parameters $device
    }

    # magic::add_checkbox dummy "Add dummy" $parameters

    if {[dict exists $parameters snake]} {
	magic::add_checkbox snake "Use snake geometry" $parameters
    }
    if {[dict exists $parameters roverlap]} {
	if {[dict exists $parameters endcov]} {
            magic::add_checkbox roverlap "Overlap at end contact" $parameters
	} else {
            magic::add_checkbox roverlap "Overlap at ends" $parameters
	}
    }
    if {[dict exists $parameters guard]} {
	magic::add_checkbox guard "Add guard ring" $parameters

    	if {[dict exists $parameters hv_guard]} {
	    magic::add_checkbox hv_guard "High-voltage guard ring" $parameters
	}
	if {[dict exists $parameters n_guard]} {
	    magic::add_checkbox n_guard "N-well connected guard ring" $parameters
	}
	if {[dict exists $parameters full_metal]} {
	    magic::add_checkbox full_metal "Full metal guard ring" $parameters
	}
	if {[dict exists $parameters glc]} {
	    magic::add_checkbox glc "Add left guard ring contact" $parameters
	}
	if {[dict exists $parameters grc]} {
	    magic::add_checkbox grc "Add right guard ring contact" $parameters
	}
	if {[dict exists $parameters gtc]} {
	    magic::add_checkbox gtc "Add top guard ring contact" $parameters
	}
	if {[dict exists $parameters gbc]} {
	    magic::add_checkbox gbc "Add bottom guard ring contact" $parameters
	}


    	magic::add_entry viagb "Bottom guard ring via coverage \[+/-\](%)" $parameters
    	magic::add_entry viagt "Top guard ring via coverage \[+/-\](%)" $parameters
    	magic::add_entry viagr "Right guard ring via coverage \[+/-\](%)" $parameters
    	magic::add_entry viagl "Left guard ring via coverage \[+/-\](%)" $parameters
    }

    if {[dict exists $parameters vias]} {
	magic::add_checkbox vias "Add vias over contacts" $parameters
    }

    if {[dict exists $parameters snake]} {
       magic::add_dependency sg13g2::res_recalc $device sg13g2 l w val nx snake
    } else {
       magic::add_dependency sg13g2::res_recalc $device sg13g2 l w val nx
    }

    if {[dict exists $parameters doports]} {
	magic::add_checkbox doports "Add ports" $parameters
    }
}

#----------------------------------------------------------------

proc sg13g2::rsil_dialog {parameters} {
    sg13g2::res_dialog rsil $parameters
}

proc sg13g2::rppd_dialog {parameters} {
    sg13g2::res_dialog rppd $parameters
}

proc sg13g2::rhigh_dialog {parameters} {
    sg13g2::res_dialog rhigh $parameters
}

proc sg13g2::rm1_dialog {parameters} {
    sg13g2::res_dialog rm1 $parameters
}

proc sg13g2::rm2_dialog {parameters} {
    sg13g2::res_dialog rm2 $parameters
}

proc sg13g2::rm3_dialog {parameters} {
    sg13g2::res_dialog rm3 $parameters
}

proc sg13g2::rm4_dialog {parameters} {
    sg13g2::res_dialog rm4 $parameters
}

proc sg13g2::rm5_dialog {parameters} {
    sg13g2::res_dialog rm5 $parameters
}

proc sg13g2::rm6_dialog {parameters} {
    sg13g2::res_dialog rm6 $parameters
}

proc sg13g2::rm7_dialog {parameters} {
    sg13g2::res_dialog rm7 $parameters
}

#----------------------------------------------------------------
# Resistor: Draw a single device in straight geometry
#----------------------------------------------------------------

proc sg13g2::res_device {parameters} {
    # Epsilon for avoiding round-off errors
    set eps  0.0005

    # Set local default values if they are not in parameters
    set doports 0		;# no port labels by default
    set endcov 0	 	;# percent coverage of end contacts
    set roverlap 0		;# overlap resistors at end contacts
    set well_res_overlap 0 	;# not a well resistor
    set end_contact_type ""	;# no contacts for metal resistors
    set end_overlap_cont 0	;# additional end overlap on sides
    set vias 0			;# add vias over contacts
    set l_delta 0		;# delta between measured and drawn length
    set res_idtype none

    set term_t ""
    set term_b ""

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    if {![dict exists $parameters end_contact_size]} {
	set end_contact_size $contact_size
    }

    # Modify drawn length by the delta length
    set l [+ $l [* $l_delta 2.0]]

    # Draw the resistor and endcaps
    pushbox
    box size 0 0
    pushbox
    set hw [/ $w 2.0]
    set hl [/ $l 2.0]
    box grow n ${hl}um
    box grow s ${hl}um
    box grow e ${hw}um
    box grow w ${hw}um

    pushbox
    box grow n ${res_to_endcont}um
    box grow s ${res_to_endcont}um
    if {$well_res_overlap > 0} {
	set well_extend [+ ${well_res_overlap} [/ ${end_contact_size} 2.0] ${end_surround}]
	box grow n ${well_extend}um
	box grow s ${well_extend}um
	paint ${well_res_type}
    } else {
	paint ${end_type}
    }
    set cext [sg13g2::getbox]
    popbox

    if {$well_res_overlap > 0} {
	erase ${well_res_type}
    } else {
	erase ${end_type}
    }
    paint ${res_type}
    if {"$res_idtype" != "none"} {
	box grow c 2
	paint ${res_idtype}
    }
    popbox

    # Reduce contact sizes by (end type) surround so that
    # the contact area edges match the device type width.
    # (Minimum dimensions will be enforced by the contact drawing routine)
    set epl [- ${w} [* ${end_surround} 2]]     	    ;# end contact width

    # Reduce end material size for well resistor types
    if {$well_res_overlap > 0} {
	set epl [- ${epl} [* ${well_res_overlap} 2]]
    }

    # Reduce by coverage percentage unless overlapping at contacts
    if {(${roverlap} == 0) && (${endcov} > 0)} {
	set cpl [* ${epl} [/ ${endcov} 100.0]]
    } else {
	set cpl $epl
    }

    # Ensure additional overlap of diffusion contact if required
    set dov [* ${end_overlap_cont} 2]
    if {[- ${epl} ${cpl}] < $dov} {
	set cpl [- ${epl} $dov]    ;# additional end contact width
    }

    set hepl [+ [/ ${epl} 2.0] ${end_surround}]
    set hesz [/ ${end_contact_size} 2.0]

    # LV substrate diffusion types have a different surround requirement
    set lv_sub_types {"psd" "nsd"}
    if {[lsearch $lv_sub_types $end_type] < 0} {
	set hesz [+ ${hesz} ${end_surround}]
    }

    # Top end material & contact
    pushbox
    box move n ${hl}um
    box move n ${res_to_endcont}um

    pushbox
    box size 0 0
    box grow n ${hesz}um
    box grow s ${hesz}um
    box grow e ${hepl}um
    box grow w ${hepl}um
    paint ${end_type}
    set cext [sg13g2::unionbox $cext [sg13g2::getbox]]
    popbox

    if {$term_t != ""} {
	label $term_t c $end_type
	select area label
	port make
    }
    if {${end_contact_type} != ""} {
	# Draw via over contact first
	if {$vias != 0} {
            pushbox
            set ch $res_to_endcont
    	    if {$ch < $via_size} {set ch $via_size}
    	    set cw $epl
    	    if {$cw < $via_size} {set cw $via_size}
	    box grow n [/ $via_size 2.0]um
	    box grow s [- $ch [/ $via_size 2.0]]um
	    box grow w [/ $cw 2.0]um
	    box grow e [/ $cw 2.0]um
            sg13g2::via1_draw
            popbox
    	}
	set cext [sg13g2::unionbox $cext [sg13g2::draw_contact ${cpl} 0 \
		${end_surround} ${metal_surround} \
		${end_contact_size} ${end_type} ${end_contact_type} m1 horz]]
    }
    popbox

    # Bottom end material & contact
    pushbox
    box move s ${hl}um
    box move s ${res_to_endcont}um

    pushbox
    box size 0 0
    box grow n ${hesz}um
    box grow s ${hesz}um
    box grow e ${hepl}um
    box grow w ${hepl}um
    paint ${end_type}
    set cext [sg13g2::unionbox $cext [sg13g2::getbox]]
    popbox

    if {$term_b != ""} {
	label $term_b c $end_type
	select area label
	port make
    }
    if {${end_contact_type} != ""} {
	# Draw via over contact first
	if {$vias != 0} {
            pushbox
            set ch $res_to_endcont
    	    if {$ch < $via_size} {set ch $via_size}
    	    set cw $epl
    	    if {$cw < $via_size} {set cw $via_size}
	    box grow n [- $ch [/ $via_size 2.0]]um
	    box grow s [/ $via_size 2.0]um
	    box grow w [/ $cw 2.0]um
	    box grow e [/ $cw 2.0]um
            sg13g2::via1_draw
            popbox
    	}
	set cext [sg13g2::unionbox $cext [sg13g2::draw_contact ${cpl} 0 \
		${end_surround} ${metal_surround} \
		${end_contact_size} ${end_type} ${end_contact_type} m1 horz]]
    }
    popbox

    popbox
    return $cext
}

#----------------------------------------------------------------
# Resistor: Draw a single device in snake geometry
#----------------------------------------------------------------

proc sg13g2::res_snake_device {nf parameters} {
    # nf is the number of fingers of the snake geometry

    # Epsilon for avoiding round-off errors
    set eps  0.0005

    # Set local default values if they are not in parameters
    set doports 0		;# no port labels by default
    set endcov 100	 	;# percent coverage of end contacts
    set vias 0			;# add vias over terminal contacts
    set well_res_overlap 0 	;# not a well resistor
    set end_contact_type ""	;# no contacts for metal resistors
    set mask_clearance 0	;# additional length to clear mask

    set term_t ""
    set term_b ""

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    if {![dict exists $parameters end_contact_size]} {
	set end_contact_size $contact_size
    }

    # Compute half width and length
    set hw [/ $w 2.0]
    set hl [/ $l 2.0]

    # Reduce contact sizes by (end type) surround so that
    # the contact area edges match the device type width.
    # (Minimum dimensions will be enforced by the contact drawing routine)
    set epl [- ${w} [* ${end_surround} 2]]     	    ;# end contact width

    # Reduce contact size for well resistor types
    if {$well_res_overlap > 0} {
	set epl [- ${epl} [* ${well_res_overlap} 2]]
    }

    # Reduce contact part of end by coverage percentage
    if {${endcov} > 0} {
	set cpl [* ${epl} [/ ${endcov} 100.0]]
    } else {
	set cpl $epl
    }

    set hepl [+ [/ ${epl} 2.0] ${end_surround}]
    set hesz [+ [/ ${end_contact_size} 2.0] ${end_surround}]

    pushbox
    box size 0 0	;# Position is taken from caller

    # Front end contact (always bottom)
    pushbox
    box move s ${hl}um
    pushbox
    box move s ${mask_clearance}um
    box move s ${res_to_endcont}um

    pushbox
    box size 0 0
    box grow n ${hesz}um
    box grow s ${hesz}um
    box grow e ${hepl}um
    box grow w ${hepl}um
    paint ${end_type}
    set cext [sg13g2::getbox]
    popbox

    if {$term_t != ""} {
	label $term_t c $end_type
	select area label
	port make
    }
    if {${end_contact_type} != ""} {
        # Draw via over contact first
	if {$vias != 0} {
	    pushbox
	    set ch $res_to_endcont
	    if {$ch < $via_size} {set ch $via_size}
	    set cw $epl
	    if {$cw < $via_size} {set cw $via_size}
	    box grow n [- $ch [/ $via_size 2.0]]um
	    box grow s [/ $via_size 2.0]um
	    box grow w [/ $cw 2.0]um
	    box grow e [/ $cw 2.0]um
	    sg13g2::via1_draw
	    popbox
	}
	set cext [sg13g2::draw_contact ${cpl} 0 \
		${end_surround} ${metal_surround} \
		${end_contact_size} ${end_type} ${end_contact_type} m1 horz]
    }
    popbox

    # Draw portion between resistor end and contact.
    box grow e ${hw}um
    box grow w ${hw}um
    pushbox
    box grow s ${mask_clearance}um
    if {${mask_clearance} > 0} {
        paint ${res_type}
    }
    popbox
    box move s ${mask_clearance}um
    box grow s ${res_to_endcont}um
    if {$well_res_overlap > 0} {
	set well_extend [+ ${well_res_overlap} [/ ${end_contact_size} 2.0] ${end_surround}]
	box grow s ${well_extend}um
	paint ${well_res_type}
    } else {
	paint ${end_type}
    }
    set cext [sg13g2::unionbox $cext [sg13g2::getbox]]
    popbox

    # Draw the resistor and endcaps
    pushbox
    box grow n ${hl}um
    box grow s ${hl}um
    box grow e ${hw}um
    box grow w ${hw}um

    # Capture these extents in the bounding box in case both contacts
    # are on one side.
    set cext [sg13g2::unionbox $cext [sg13g2::getbox]]

    set deltax [+ ${res_spacing} ${w}]
    set deltay [- ${l} ${w}]
    for {set i 0} {$i < [- $nf 1]} {incr i} {
	# Really should be drawing endcaps last instead of working around 1st one
	if {($i == 0) && (${mask_clearance} < 0)} {
	    pushbox
	    box grow s ${mask_clearance}um
	    paint ${res_type}
	    popbox
	} else {
	    paint ${res_type}
	}
 	pushbox
	if {[% $i 2] == 0} {
	    box move n ${deltay}um
	}
	box height ${w}um
	box width ${deltax}um
	paint ${res_type}
 	popbox
	box move e ${deltax}um
    }
    paint ${res_type}
    # Capture these extents in the bounding box
    set cext [sg13g2::unionbox $cext [sg13g2::getbox]]
    popbox

    # Move box to last finger
    set lastf [* [- $nf 1] $deltax]
    box move e ${lastf}um

    # Back-end contact (top or bottom, depending if odd or even turns)
    pushbox

    if {[% $nf 2] == 1} {
	set dir n
    } else {
	set dir s
    }
    box move $dir ${hl}um
    pushbox
    box move $dir ${mask_clearance}um
    box move $dir ${res_to_endcont}um

    pushbox
    box size 0 0
    box grow n ${hesz}um
    box grow s ${hesz}um
    box grow e ${hepl}um
    box grow w ${hepl}um
    paint ${end_type}
    set cext [sg13g2::unionbox $cext [sg13g2::getbox]]
    popbox

    if {$term_b != ""} {
	label $term_b c $end_type
	select area label
	port make
    }
    if {${end_contact_type} != ""} {
	# Draw via over contact first
	if {$vias != 0} {
	    pushbox
	    set ch $res_to_endcont
	    if {$ch < $via_size} {set ch $via_size}
	    set cw $epl
	    if {$cw < $via_size} {set cw $via_size}
	    if {$dir == "n"} {
		box grow n [/ $via_size 2.0]um
		box grow s [- $ch [/ $via_size 2.0]]um
	    } else {
		box grow n [- $ch [/ $via_size 2.0]]um
		box grow s [/ $via_size 2.0]um
	    }
	    box grow w [/ $cw 2.0]um
	    box grow e [/ $cw 2.0]um
	    sg13g2::via1_draw
	    popbox
	}
	set cext [sg13g2::unionbox $cext [sg13g2::draw_contact ${cpl} 0 \
		${end_surround} ${metal_surround} \
		${end_contact_size} ${end_type} ${end_contact_type} m1 horz]]
    }
    popbox
    # Draw portion between resistor end and contact.
    box grow e ${hw}um
    box grow w ${hw}um
    pushbox
    box grow $dir ${mask_clearance}um
    if {${mask_clearance} > 0} {
        paint ${res_type}
    }
    popbox
    box move $dir ${mask_clearance}um
    box grow $dir ${res_to_endcont}um

    if {$well_res_overlap > 0} {
	set well_extend [+ ${well_res_overlap} [/ ${end_contact_size} 2.0] ${end_surround}]
	box grow $dir ${well_extend}um
	paint ${well_res_type}
    } else {
	paint ${end_type}
    }
    popbox

    popbox
    return $cext
}

#----------------------------------------------------------------
# Resistor: Draw the tiled device
#----------------------------------------------------------------

proc sg13g2::res_draw {parameters} {
    tech unlock *
    set savesnap [snap]
    snap internal

    # Set defaults if they are not in parameters
    set snake 0		;# some resistors don't allow snake geometry
    set roverlap 0	;# overlap resistors at contacts
    set guard 0		;# draw a guard ring
    set plus_diff_type   nsd	;# guard ring diffusion type
    set overlap_compress 0	;# special Y distance compression
    set well_res_overlap 0	;# additional well extension behind contact
    set res_diff_spacing 0	;# spacing from resistor to diffusion
    set res_idtype  none
    set doports 0

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # For devices where inter-device space is smaller than device-to-guard ring
    if {![dict exists $parameters end_to_end_space]} {
	set end_to_end_space $end_spacing
    }

    if {![dict exists $parameters end_contact_size]} {
	set end_contact_size $contact_size
    }

    # Normalize distance units to microns
    set w [magic::spice2float $w]
    set l [magic::spice2float $l]

    pushbox
    box values 0 0 0 0

    # Determine the base device dimensions by drawing one device
    # while all layers are locked (nothing drawn).  This allows the
    # base drawing routine to do complicated geometry without having
    # to duplicate it here with calculations.

    tech lock *
    set nf $nx
    if {($snake == 1) && ($nx == 1)} {set snake 0}
    if {$snake == 1} {
	set bbox [sg13g2::res_snake_device $nf $parameters]
	set nx 1
    } else {
	set bbox [sg13g2::res_device $parameters]
    }
    # puts stdout "Diagnostic: Device bounding box e $bbox (um)"
    tech unlock *

    set fw [- [lindex $bbox 2] [lindex $bbox 0]]
    set fh [- [lindex $bbox 3] [lindex $bbox 1]]
    set lw [+ [lindex $bbox 2] [lindex $bbox 0]]
    set lh [+ [lindex $bbox 3] [lindex $bbox 1]]

    # Determine tile width and height (depends on overlap)
    # Snake resistors cannot overlap.
    # However, snake resistors with an odd number of fingers can
    # compress the space if overlap_compress is defined

    if {($roverlap == 1) && ($snake == 1) && ([% $nf 2] == 1) && ($m > 1)} {
        set dy [- $fh $overlap_compress]
    } elseif {($roverlap == 0) || ($snake == 1)} {
        set dy [+ $fh $end_to_end_space]
    } else {
        # overlap poly
        set dy [- $fh [+ [* [+ $end_surround $well_res_overlap] 2.0] $end_contact_size]]
    }
    set dx [+ $fw $res_spacing]

    # Determine core width and height
    set corex [+ [* [- $nx 1] $dx] $fw]
    set corey [+ [* [- $m 1] $dy] $fh]
    set corellx [/ [+ [- $corex $fw] $lw] 2.0]
    set corelly [/ [+ [- $corey $fh] $lh] 2.0]

    set lv_sub_types {"psd" "nsd"}
    if {[lsearch $lv_sub_types $plus_diff_type] >= 0} {
	set guard_diff_surround 0
    } else {
	set guard_diff_surround ${diff_surround}
    }

    if {$guard != 0} {
	# Calculate guard ring size (measured to contact center)
	set gx [+ $corex [* 2.0 [+ $res_diff_spacing $guard_diff_surround]] $contact_size]
	set gy [+ $corey [* 2.0 [+ $end_spacing $guard_diff_surround]] $contact_size]

	# Draw the guard ring first, because well resistors are on the substrate plane
	if {$doports} {dict set parameters bulk B}
	sg13g2::guard_ring $gx $gy $parameters
    }

    pushbox
    box move w ${corellx}um
    box move s ${corelly}um
    # puts "Device position at = [sg13g2::getbox]"
    for {set xp 0} {$xp < $nx} {incr xp} {
	pushbox
	for {set yp 0} {$yp < $m} {incr yp} {
	    if {$doports} {
		if {($m == 1) && ($nx == 1)} {
		     dict set parameters term_t R1
		     dict set parameters term_b R2
		} elseif {$m == 1} {
		     dict set parameters term_t R1_$xp
		     dict set parameters term_b R2_$xp
		} elseif {$nx == 1} {
		     dict set parameters term_t R1_$yp
		     dict set parameters term_b R2_$yp
		} else {
		     dict set parameters term_t R1_${xp}_$yp
		     dict set parameters term_b R2_${xp}_$yp
		}
	    }
	    if {$snake == 1} {
		sg13g2::res_snake_device $nf $parameters
	    } else {
		sg13g2::res_device $parameters
	    }
            box move n ${dy}um
        }
	popbox
        box move e ${dx}um
    }
    popbox
    popbox

    snap $savesnap
    tech revert
}

#----------------------------------------------------------------

proc sg13g2::rsil_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    # Handle options related to guard ring type (high/low voltage, nwell/psub)
    if {[dict exists $parameters hv_guard]} {
	set use_hv_guard [dict get $parameters hv_guard]
    } else {
	set use_hv_guard 0
    }
    if {[dict exists $parameters n_guard]} {
	set use_n_guard [dict get $parameters n_guard]
    } else {
	set use_n_guard 0
    }

    if {$use_hv_guard == 1} {
	if {$use_n_guard == 1} {
	    set gdifftype hvnsd
	    set gdiffcont hvnsc
	} else {
	    set gdifftype hvpsd
	    set gdiffcont hvpsc
	}
	set gsurround 0.33
    } else {
	if {$use_n_guard == 1} {
	    set gdifftype nsd
	    set gdiffcont nsc
	} else {
	    set gdifftype psd
	    set gdiffcont psc
	}
	set gsurround $sub_surround
    }
    if {$use_n_guard == 1} {
	set gsubtype nwell
    } else {
	set gsubtype psub
    }

    set newdict [dict create \
	    res_type		nres \
	    end_type 		poly \
	    end_contact_type	pc \
	    plus_diff_type	$gdifftype \
	    plus_contact_type	$gdiffcont \
	    sub_type		$gsubtype \
	    guard_sub_surround	$gsurround \
	    end_surround	$poly_surround \
	    end_spacing		0.48 \
	    end_to_end_space	0.52 \
	    res_to_cont		0.575 \
	    res_to_endcont	0.2 \
	    res_spacing		$poly_spacing \
	    res_diff_spacing	0.48 \
	    mask_clearance	0.0 \
	    overlap_compress	0.36 \
    ]

    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::rppd_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    # Handle options related to guard ring type (high/low voltage, nwell/psub)
    if {[dict exists $parameters hv_guard]} {
	set use_hv_guard [dict get $parameters hv_guard]
    } else {
	set use_hv_guard 0
    }
    if {[dict exists $parameters n_guard]} {
	set use_n_guard [dict get $parameters n_guard]
    } else {
	set use_n_guard 0
    }

    if {$use_hv_guard == 1} {
	if {$use_n_guard == 1} {
	    set gdifftype hvnsd
	    set gdiffcont hvnsc
	} else {
	    set gdifftype hvpsd
	    set gdiffcont hvpsc
	}
	set gsurround 0.33
    } else {
	if {$use_n_guard == 1} {
	    set gdifftype nsd
	    set gdiffcont nsc
	} else {
	    set gdifftype psd
	    set gdiffcont psc
	}
	set gsurround $sub_surround
    }
    if {$use_n_guard == 1} {
	set gsubtype nwell
	set gresdiff_spacing 0.785
	set gresdiff_end 0.525
    } else {
	set gsubtype psub
	set gresdiff_spacing 0.48
	set gresdiff_end 0.48
    }

    set newdict [dict create \
	    res_type		pres \
	    end_type 		poly \
	    end_contact_type	pc \
	    plus_diff_type	$gdifftype \
	    plus_contact_type	$gdiffcont \
	    sub_type		$gsubtype \
	    guard_sub_surround	$gsurround \
	    end_surround	$poly_surround \
	    end_spacing		$gresdiff_end \
	    end_to_end_space	0.52 \
	    res_to_cont		0.575 \
	    res_to_endcont	0.28 \
	    res_spacing		0.48 \
	    res_diff_spacing	$gresdiff_spacing \
	    mask_clearance	0.20 \
	    overlap_compress	0.36 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::rhigh_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    # Handle options related to guard ring type (high/low voltage, nwell/psub)
    if {[dict exists $parameters hv_guard]} {
	set use_hv_guard [dict get $parameters hv_guard]
    } else {
	set use_hv_guard 0
    }
    if {[dict exists $parameters n_guard]} {
	set use_n_guard [dict get $parameters n_guard]
    } else {
	set use_n_guard 0
    }

    if {$use_hv_guard == 1} {
	if {$use_n_guard == 1} {
	    set gdifftype hvnsd
	    set gdiffcont hvnsc
	} else {
	    set gdifftype hvpsd
	    set gdiffcont hvpsc
	}
	set gsurround 0.33
    } else {
	if {$use_n_guard == 1} {
	    set gdifftype nsd
	    set gdiffcont nsc
	} else {
	    set gdifftype psd
	    set gdiffcont psc
	}
	set gsurround $sub_surround
    }
    if {$use_n_guard == 1} {
	set gsubtype nwell
	set gresdiff_spacing 0.785
	set gresdiff_end 0.525
    } else {
	set gsubtype psub
	set gresdiff_spacing 0.48
	set gresdiff_end 0.48
    }

    set newdict [dict create \
	    res_type		xres \
	    end_type 		poly \
	    end_contact_type	pc \
	    plus_diff_type	$gdifftype \
	    plus_contact_type	$gdiffcont \
	    sub_type		$gsubtype \
	    guard_sub_surround	$gsurround \
	    end_surround	$poly_surround \
	    end_spacing		$gresdiff_end \
	    end_to_end_space	0.52 \
	    res_to_cont		0.575 \
	    res_to_endcont	0.28 \
	    res_spacing		0.48 \
	    res_diff_spacing	$gresdiff_spacing \
	    mask_clearance	0.20 \
	    overlap_compress	0.36 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::rm1_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    guard		0 \
	    res_type		rm1 \
	    end_type 		m1 \
	    end_surround	0.0 \
	    end_spacing		0.0 \
	    end_to_end_space	0.28 \
	    res_to_endcont	0.2 \
	    res_spacing		$mmetal_spacing \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::rm2_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    guard		0 \
	    res_type		rm2 \
	    end_type 		m2 \
	    end_surround	0.0 \
	    end_spacing		0.0 \
	    end_to_end_space	0.28 \
	    res_to_endcont	0.2 \
	    res_spacing		$mmetal_spacing \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::rm3_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    guard		0 \
	    res_type		rm3 \
	    end_type 		m3 \
	    end_surround	0.0 \
	    end_spacing		0.0 \
	    end_to_end_space	0.28 \
	    res_to_endcont	0.2 \
	    res_spacing		$mmetal_spacing \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::rm4_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    guard		0 \
	    res_type		rm4 \
	    end_type 		m4 \
	    end_surround	0.0 \
	    end_spacing		0.0 \
	    end_to_end_space	0.28 \
	    res_to_endcont	0.2 \
	    res_spacing		$mmetal_spacing \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::rm5_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    guard		0 \
	    res_type		rm5 \
	    end_type 		m5 \
	    end_surround	0.0 \
	    end_spacing		0.0 \
	    end_to_end_space	0.28 \
	    res_to_endcont	0.2 \
	    res_spacing		$mmetal_spacing \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::rm6_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    guard		0 \
	    res_type		rm6 \
	    end_type 		m6 \
	    end_surround	0.0 \
	    end_spacing		0.0 \
	    end_to_end_space	0.28 \
	    res_to_endcont	0.2 \
	    res_spacing		$mmetal_spacing \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::rm7_draw {parameters} {
    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    guard		0 \
	    res_type		rm7 \
	    end_type 		m7 \
	    end_surround	0.0 \
	    end_spacing		0.0 \
	    end_to_end_space	1.6 \
	    res_to_endcont	0.2 \
	    res_spacing		$mmetal_spacing \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

#----------------------------------------------------------------
# Resistor total length computation
#----------------------------------------------------------------

proc sg13g2::compute_ltot {parameters} {
    # In case snake not defined
    set snake 0
    set caplen 0

    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    set l [magic::spice2float $l]
    set l [magic::3digitpastdecimal $l]

    # Compute total length.  Use catch to prevent error in batch/scripted mode.
    if {$snake == 1} {
	catch {set magic::ltot_val [expr ($caplen * ($nx - 1)) + ($l * $nx) + ($nx - 1)]}
    } else {
	catch {set magic::ltot_val $l}
    }
}

#----------------------------------------------------------------
# resistor: Check device parameters for out-of-bounds values
#----------------------------------------------------------------

proc sg13g2::res_check {device parameters} {

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    set snake 0
    set guard 0
    set sterm 0.0
    set caplen 0
    set wmax 0

    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Normalize distance units to microns
    set w [magic::spice2float $w]
    set w [magic::3digitpastdecimal $w]
    set l [magic::spice2float $l]
    set l [magic::3digitpastdecimal $l]

    set val  [magic::spice2float $val]
    set rho  [magic::spice2float $rho]

    # nf, m must be integer
    if {![string is int $nx]} {
	puts stderr "X repeat must be an integer!"
        dict set parameters nx 1
    }
    if {![string is int $m]} {
	puts stderr "Y repeat must be an integer!"
        dict set parameters m 1
    }

    # Width always needs to be specified
    if {$w < $wmin} {
	puts stderr "Resistor width must be >= $wmin um"
	dict set parameters w $wmin
    } 
    if {$wmax > 0 && $w > $wmax} {
	puts stderr "Resistor width must be <= $wmax um"
	dict set parameters w $wmax
    }
    
    # Val and W specified - no L
    if {$l == 0}  {
   	set l [expr ($w - $dw) * $val / $rho]
        set l [magic::3digitpastdecimal $l]
        set stringval [magic::float2spice $val]
	dict set parameters l [magic::float2spice [expr $l * 1e-6]]
	# L and W specified - ignore Val if specified
    } else {
	if {$snake == 0} {
	    set val [expr (2 * $term + $l * $rho) / ($w - $dw)]
	} else {
	    set val [expr $rho * ($nx - 1) + ((2 * ($term + $sterm)) \
			+ ($rho * $l * $nx) + ($rho * $caplen * ($nx - 1))) \
			/ ($w - $dw)]
	}
	set val [magic::float2spice $val]
        dict set parameters val $val
    }
    if {$l < $lmin} {
	puts stderr "Resistor length must be >= $lmin um"
	dict set parameters l $lmin
    } 
    if {$nx < 1} {
	puts stderr "X repeat must be >= 1"
	dict set parameters nx 1
    } 
    if {$m < 1} {
	puts stderr "Y repeat must be >= 1"
	dict set parameters m 1
    } 

    # Snake resistors cannot have width greater than length
    if {$snake == 1} {
	if {$w > $l} {
	    puts stderr "Snake resistor width must be < length"
	    dict set parameters w $l
	}
    }

    # Check via coverage for syntax
    if {$guard == 1} {
    	if {[catch {expr abs($viagb)}]} {
	    puts stderr "Guard ring bottom via coverage must be numeric!"
            dict set parameters viagb 0
    	} elseif {[expr abs($viagb)] > 100} {
	    puts stderr "Guard ring bottom via coverage can't be more than 100%"
            dict set parameters viagb 100
    	}
    	if {[catch {expr abs($viagt)}]} {
	    puts stderr "Guard ring top via coverage must be numeric!"
            dict set parameters viagt 0
	} elseif {[expr abs($viagt)] > 100} {
	    puts stderr "Guard ring top via coverage can't be more than 100%"
            dict set parameters viagt 100
	}
	if {[catch {expr abs($viagr)}]} {
	    puts stderr "Guard ring right via coverage must be numeric!"
            dict set parameters viagr 0
	} elseif {[expr abs($viagr)] > 100} {
	    puts stderr "Guard ring right via coverage can't be more than 100%"
            dict set parameters viagr 100
   	} 
        if {[catch {expr abs($viagl)}]} {
	    puts stderr "Guard ring left via coverage must be numeric!"
            dict set parameters viagl 0
	} elseif {[expr abs($viagl)] > 100} {
	   puts stderr "Guard ring left via coverage can't be more than 100%"
           dict set parameters viagl 100
	}
    }

    sg13g2::compute_ltot $parameters
    return $parameters
}

#----------------------------------------------------------------

proc sg13g2::rsil_check {parameters} {
    return [sg13g2::res_check rsil $parameters]
}

proc sg13g2::rppd_check {parameters} {
    return [sg13g2::res_check rppd $parameters]
}

proc sg13g2::rhigh_check {parameters} {
    return [sg13g2::res_check rhigh $parameters]
}

proc sg13g2::rm1_check {parameters} {
    return [sg13g2::res_check rm1 $parameters]
}

proc sg13g2::rm2_check {parameters} {
    return [sg13g2::res_check rm2 $parameters]
}

proc sg13g2::rm3_check {parameters} {
    return [sg13g2::res_check rm3 $parameters]
}

proc sg13g2::rm4_check {parameters} {
    return [sg13g2::res_check rm4 $parameters]
}
proc sg13g2::rm5_check {parameters} {
    return [sg13g2::res_check rm5 $parameters]
}

#----------------------------------------------------------------
