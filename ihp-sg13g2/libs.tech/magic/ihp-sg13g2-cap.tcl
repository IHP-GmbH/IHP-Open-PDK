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
# Drawn capacitor routines
# NOTE:  Work in progress.  These values need to be corrected.
#----------------------------------------------------------------

proc sg13g2::cap_cmim_defaults {} {
    return {w 2.00 l 2.00 val 6.0 carea 1.50 cperi 0.19 class capacitor \
		compatible {cap_cmim cap_rfcmim} \
		nx 1 ny 1 dummy 0 square 0 lmin 2.00 wmin 2.00 \
		lmax 30.0 wmax 30.0 dc 0 tabwidth 1.0 \
		upcontact 0 bconnect 1 tconnect 1 \
		ccov 100 doports 1}
}

proc sg13g2::cap_rfcmim_defaults {} {
    return {w 7.00 l 7.00 val 73.5 carea 1.50 cperi 0.19 class capacitor \
		compatible {cap_cmim cap_rfcmim} \
		nx 1 ny 1 dummy 0 square 0 lmin 7.00 wmin 7.00 \
		lmax 75.0 wmax 75.0 dc 0 tabwidth 3.0 \
		upcontact 0 bconnect 1 tconnect 1 \
		ccov 100 doports 1}
}

#----------------------------------------------------------------
# Recalculate capacitor values from GUI entries.
# Recomputes W/L and Value as long as 2 of them are present
# (To be completed)
#----------------------------------------------------------------

proc sg13g2::cap_recalc {field parameters} {
    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }
    switch  $field {
	val { puts stdout "value changed" }
	w   { puts stdout "width changed" }
	l   { puts stdout "length changed" }
    }
    dict set parameters val $val
    dict set parameters w $w
    dict set parameters l $l
}

#----------------------------------------------------------------
# Capacitor defaults:
#----------------------------------------------------------------
#  w      Width of drawn cap
#  l      Length of drawn cap
#  nx     Number of devices in X
#  ny     Number of devices in Y
#  val    Default cap value
#  carea  Area
#  cperi  Perimeter
#  dummy  Add dummy cap
#  square Make square capacitor
#  tabwidth  Width of tabs on bottom plate
#
#  (not user-editable)
#
#  wmin   Minimum allowed width
#  lmin   Minimum allowed length
#  dc     Area to remove to calculated area 
#----------------------------------------------------------------

#----------------------------------------------------------------
# capacitor: Conversion from SPICE netlist parameters to toolkit
#----------------------------------------------------------------

proc sg13g2::cap_convert {parameters} {
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

proc sg13g2::cap_cmim_convert {parameters} {
    return [cap_convert $parameters]
}

proc sg13g2::cap_rfcmim_convert {parameters} {
    return [cap_convert $parameters]
}

#----------------------------------------------------------------
# capacitor: Interactively specifies the fixed layout parameters
#----------------------------------------------------------------

proc sg13g2::cap_dialog {device parameters} {
    # Editable fields:      w, l, nx, ny, val
    # Checked fields:  	    square, dummy

    magic::add_entry val "Value (fF)" $parameters
    sg13g2::compute_ctot $parameters
    magic::add_message ctot "Total capacitance (pF)" $parameters
    magic::add_entry l "Length (um)" $parameters
    magic::add_entry w "Width (um)" $parameters
    magic::add_entry nx "X Repeat" $parameters
    magic::add_entry ny "Y Repeat" $parameters

    if {[dict exists $parameters compatible]} {
	set sellist [dict get $parameters compatible]
	magic::add_selectlist gencell "Device type" $sellist $parameters $device
    }

    if {[dict exists $parameters square]} {
	magic::add_checkbox square "Square capacitor" $parameters
    }
    if {[dict exists $parameters upcontact]} {
	magic::add_checkbox upcontact "Create bottom plate contact" $parameters
    }
    if {[dict exists $parameters tabwidth]} {
	magic::add_entry tabwidth "Width of bottom plate tab" $parameters
    }
    if {[dict exists $parameters bconnect]} {
	magic::add_checkbox bconnect "Connect bottom plates in array" $parameters
    }
    if {[dict exists $parameters tconnect]} {
	magic::add_checkbox tconnect "Connect top plates in array" $parameters
    }
    if {[dict exists $parameters ccov]} {
    	magic::add_entry ccov "Capacitor contact coverage \[+/-\](%)" $parameters
    }
    if {[dict exists $parameters guard]} {
	magic::add_checkbox guard "Add guard ring" $parameters
    }

    magic::add_dependency sg13g2::cap_recalc $device sg13g2 l w val

    if {[dict exists $parameters doports]} {
	magic::add_checkbox doports "Add ports" $parameters
    }

    # magic::add_checkbox dummy "Add dummy" $parameters
}

proc sg13g2::cap_cmim_dialog {parameters} {
    sg13g2::cap_dialog cap_cmim $parameters
}

proc sg13g2::cap_rfcmim_dialog {parameters} {
    sg13g2::cap_dialog cap_rfcmim $parameters
}

#----------------------------------------------------------------
# Capacitor total capacitance computation
#----------------------------------------------------------------

proc sg13g2::compute_ctot {parameters} {
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }
    set val [magic::spice2float $val]
    set val [magic::3digitpastdecimal $val]

    # Compute total capacitance (and convert fF to pF)
    catch {set magic::ctot_val [expr (0.001 * $val * $nx * $ny)]}
}

#----------------------------------------------------------------
# Capacitor: Draw a single device
#----------------------------------------------------------------

proc sg13g2::cap_device {parameters} {
    # Epsilon for avoiding round-off errors
    set eps  0.0005

    # Set local default values if they are not in parameters
    set doports 0	;# no port labels by default
    set cap_surround 0
    set bot_surround 0
    set top_surround 0
    set top_spacing 0
    set upcontact 0	;# create bottom plate contact (disabled)
    set bconnect 0	;# bottom plates are connected in array (disabled)
    set cap_spacing 0	;# cap spacing in array
    set top_space 0   	;# top metal spacing (if larger than cap spacing)
    set top_width 0   	;# top metal minimum width
    set top_contact_size 0  ;# cap contact minimum size
    set ccov 100	    ;# amount of contact coverage

    set term_t ""
    set term_b ""

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    if {![dict exists $parameters top_space]} {
	set top_space $metal_spacing
    }

    # Draw the device
    pushbox
    box size 0 0

    pushbox
    set hw [/ $w 2.0]
    set hl [/ $l 2.0]
    box grow e ${hw}um
    box grow w ${hw}um
    box grow n ${hl}um
    box grow s ${hl}um
    paint ${cap_type}
    pushbox

    # Find contact width if ccov is other than 100
    set cmaxw [- $w [* $cap_surround 2]]
    set cw [* $cmaxw [/ [expr abs($ccov)] 100.0]]
    # Contact width must meet minimum
    if {$cw < $top_contact_size} {set cw $top_contact_size}
    # Max contact width must also meet minimum
    if {$cmaxw < $top_contact_size} {set cmaxw $top_contact_size}

    # Difference between maximum contact width and actual contact width
    set cdif [- $cmaxw $cw]

    # Reduce the box to the maximum contact area
    box grow n -${cap_surround}um
    box grow s -${cap_surround}um
    box grow e -${cap_surround}um
    box grow w -${cap_surround}um

    set anchor [string index $ccov 0]
    if {$anchor == "+"} {
	box grow e -${cdif}um
    } elseif {$anchor == "-"} {
	box grow w -${cdif}um
    } else {
        set cdif [/ ${cdif} 2.0]
	box grow w -${cdif}um
	box grow e -${cdif}um
    }
    paint ${cap_contact_type}

    pushbox
    box grow n ${top_surround}um
    box grow s ${top_surround}um
    box grow e ${top_surround}um
    box grow w ${top_surround}um

    # If the contact size does not meet the minimum top metal
    # width requirement, then add more top metal.
    set cext [sg13g2::getbox]
    set cwid [- [lindex $cext 2] [lindex $cext 0]]
    set chgt [- [lindex $cext 3] [lindex $cext 1]]
    set hcwid 0
    if {$cwid < $top_width} {
	set cdif [- $top_width $cwid]
	set hcwid [/ $cdif 2.0]
	box grow e ${hcwid}um
	box grow w ${hcwid}um
    }
    if {$chgt < $top_width} {
	set cdif [- $top_width $chgt]
	set hchgt [/ $cdif 2.0]
	box grow n ${hchgt}um
	box grow s ${hchgt}um
    }

    paint ${top_type}
    set cext [sg13g2::getbox]
    # Save the area of the top metal
    set topmetbox $cext
    # puts stdout "Diagnostic:  cext is $cext"
    popbox
    popbox
    pushbox
    box grow n ${bot_surround}um
    box grow s ${bot_surround}um
    box grow e ${bot_surround}um
    box grow w ${bot_surround}um

    paint ${bot_type}
    # Create boundary using properties
    property FIXED_BBOX [box values]
    set botmetbox [sg13g2::getbox]
    set cext [sg13g2::unionbox $cext $botmetbox]

    popbox
    popbox

    if {$upcontact == 1} {
	# Extend bottom metal under contact to right
	pushbox
	box values [lindex $botmetbox 0]um [lindex $botmetbox 1]um \
		[lindex $topmetbox 2]um [lindex $botmetbox 3]um
	box grow e ${top_spacing}um
	box grow e ${metal_surround}um
	box grow e ${top_contact_size}um
	paint ${bot_type}
	popbox

	# Draw contact to right.  Reduce contact extent if devices are not
	# wired together and the top metal spacing rule limits the distance
	set lcont $l
	if {($bconnect == 0) && ($ny > 1)} {
	    set cspace [- [+ [* [- $bot_surround $cap_surround] 2.0] $cap_spacing] \
			[* $metal_surround 2.0]]
	    set cdiff [- $top_spacing $cspace]
	    if {$cdiff > 0} {
		set lcont [- $l $cdiff]
	    }
	}

	pushbox
        # Measure from top metal edge 
	set tmw [/ [- [lindex $topmetbox 2] [lindex $topmetbox 0]] 2.0]
	box move e ${tmw}um
	box move e ${top_spacing}um
	box move e ${metal_surround}um
	box move e [/ $top_contact_size 2.0]um

	# cl shrinks top and bottom to accomodate larger bottom metal
	# surround rule for contacts near a MiM cap.  This should be its
	# own variable, but metal_surround is sufficient.
	# set cl [- [+ ${lcont} [* ${bot_surround} 2.0]] [* ${end_surround} 2.0]]
	# set cl [- ${cl} ${metal_surround}]
	# if {$bconnect == 0} {set cl [- ${cl} ${top_spacing}]}
	
	set cext [sg13g2::unionbox $cext [sg13g2::draw_contact 0 ${lcont} \
		${end_surround} ${metal_surround} \
		${top_contact_size} ${bot_type} ${top_contact_type} \
		${top_type} full]]
	pushbox
	# A top contact + top metal surround doesn't meet minimum top metal
	# width, so extend the top metal over the contact to the right to
	# meet minimum width.
	set hcl [/ $lcont 2.0]
	box grow n ${hcl}um
	box grow n ${metal_surround}um
	box grow s ${hcl}um
	box grow s ${metal_surround}um
	box move w [/ $top_contact_size 2.0]um
	box move w ${metal_surround}um
	box width ${top_width}um
	paint ${top_type}
	set cext [sg13g2::unionbox $cext [sg13g2::getbox]]
	popbox
	# Bottom plate port label
	if {$term_b != ""} {
	    label $term_b c $bot_type
	    select area label
	    port make
	}
	popbox
    }
    popbox

    # Top plate port label
    if {$term_t != ""} {
	label $term_t c $top_type
	select area label
	port make
    }

    # Bottom plate port label (in absence of bottom plate contact)
    if {($term_b != "") && ($upcontact == 0)} {
	pushbox
	box move e ${hw}um
	box move e 0.1um
	label $term_b c $bot_type
	select area label
	port make
	popbox
    } 

    return [list {*}$cext $hcwid]
}

#----------------------------------------------------------------
# Capacitor: Draw the tiled device
#----------------------------------------------------------------

proc sg13g2::cap_draw {parameters} {
    tech unlock *
    set savesnap [snap]
    snap internal

    # Set defaults if they are not in parameters
    set coverlap 0	;# overlap capacitors at contacts
    set guard 0		;# draw a guard ring
    set sandwich 0	;# this is not a plate sandwich capacitor
    set cap_spacing 0	;# abutted caps if spacing is zero
    set cap_diff_spacing 0
    set top_spacing 0
    set end_surround 0
    set bot_surround 0
    set top_width 0
    set end_spacing 0
    set bconnect 0	;# connect bottom plates in array
    set tconnect 0	;# connect top plates in array
    set top_type ""
    set doports 0
    set tabwidth 0

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
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
    if {$sandwich == 1} {
	set bbox [sg13g2::sandwich_cap_device $parameters]
    } else {
	set bbox [sg13g2::cap_device $parameters]
    }
    # puts stdout "Diagnostic: Device bounding box + x adjustment is $bbox (um)"
    tech unlock *

    set fw [+ [- [lindex $bbox 2] [lindex $bbox 0]] [lindex $bbox 4]]
    set fh [- [lindex $bbox 3] [lindex $bbox 1]]
    set lw [+ [lindex $bbox 2] [lindex $bbox 0]]
    set lh [+ [lindex $bbox 3] [lindex $bbox 1]]
    set rp [lindex $bbox 2]	;# right edge of device

    # Determine tile width and height (depends on overlap)
    if {$coverlap == 0} {
        set dy [+ $fh $cap_spacing]
    } else {
        # overlap at end contact
        set dy [- $fh [+ $end_surround $end_surround $contact_size]]
    }
    # Contact is placed on right so spacing is determined by top_spacing.
    if {$upcontact == 1} {
	set dx [+ $fw $top_spacing -$cap_surround -$bot_surround]
    } else {
	set dx [+ $fw $cap_spacing]
    }

    # Determine core width and height
    set corex [+ [* [- $nx 1] $dx] $fw]
    set corey [+ [* [- $ny 1] $dy] $fh]
    set corellx [/ [+ [- $corex $fw] $lw] 2.0]
    set corelly [/ [+ [- $corey $fh] $lh] 2.0]

    if {$guard != 0} {
	# Calculate guard ring size (measured to contact center)
	set gx [+ $corex [* 2.0 [+ $cap_diff_spacing $diff_surround]] $contact_size]
	set gy [+ $corey [* 2.0 [+ $cap_diff_spacing $diff_surround]] $contact_size]

	# Draw the guard ring first.
	if {$doports} {dict set parameters bulk B}
	sg13g2::guard_ring $gx $gy $parameters

	# NOTE: A guard ring under a MiM cap implies an RF device.
	# The RF MiM cap uses PWELLBLK (pblock) inside the guard ring area.
	# Put 0.6um space between block and the ring.
	set gedgex [+ $corex [* 2.0 [+ $cap_diff_spacing]]]
	set gedgey [+ $corey [* 2.0 [+ $cap_diff_spacing]]]
	set hgx [- [/ $gedgex 2.0] 0.6]
	set hgy [- [/ $gedgey 2.0] 0.6]
	# Paint pblock this area (this also erases pwell)
	pushbox
	box values -${hgx}um -${hgy}um ${hgx}um ${hgy}um
	paint pblock
	popbox
    }

    set twidth [+ ${contact_size} ${end_surround} ${end_surround}]
    if {${twidth} < ${top_width}} {
	set twidth ${top_width}
    }
    set hmw [/ $twidth 2.0]
    set hdy [/ $dy 2.0]
    set cdx [+ [/ ${w} 2.0] ${bot_surround} ${end_spacing}]

    pushbox
    box move w ${corellx}um
    box move s ${corelly}um
    for {set xp 0} {$xp < $nx} {incr xp} {
	pushbox
	for {set yp 0} {$yp < $ny} {incr yp} {
	    if {$doports} {
		if {($ny == 1) && ($nx == 1)} {
		    dict set parameters term_t C1
		    dict set parameters term_b C2
		} elseif {$ny == 1} {
		    dict set parameters term_t C1_$xp
		    dict set parameters term_b C2_$xp
		} elseif {$nx == 1} {
		    if {$tconnect} {
			dict set parameters term_t C1
		    } else {
			dict set parameters term_t C1_$yp
		    }
		    if {$bconnect} {
			dict set parameters term_b C2
		    } else {
			dict set parameters term_b C2_$yp
		    }
		} else {
		    if {$tconnect} {
			dict set parameters term_t C1_$xp
		    } else {
			dict set parameters term_t C1_${xp}_$yp
		    }
		    if {$bconnect} {
			dict set parameters term_b C2_$xp
		    } else {
			dict set parameters term_b C2_${xp}_$yp
		    }
		}
		if {$yp > 0} {
		    if {$tconnect} {dict set parameters term_t ""}
		    if {$bconnect} {dict set parameters term_b ""}
		}
	    }

	    sg13g2::cap_device $parameters
	    if {$ny > 1} {
		pushbox
		box grow n ${hdy}um
		box grow s ${hdy}um
		pushbox
		box grow e ${hmw}um
		box grow w ${hmw}um
		if {($top_type != "") && ($tconnect == 1)} {
		    paint ${top_type}
		}
		if {($bot_type != "") && ($bconnect == 1) && ($upcontact == 1)} {
		    # When connecting up from the bottom plate end, use the top
		    # metal connection to strap multiple capacitors together
		    box move e ${rp}um
		    box move w ${hmw}um
		    paint ${top_type}
		}
		popbox
		if {($bot_type != "") && ($bconnect == 1) && ($upcontact != 1)} {
		    set halftab [/ $tabwidth 2.0]
		    box grow e ${halftab}um
		    box grow w ${halftab}um
		    paint ${bot_type}
		} 
		popbox
	    }
            box move n ${dy}um
        }
	# If there is a guard ring, then draw the connecting tabs
	# to the edge of the guard ring.
	if {$guard == 1} {
	    pushbox
	    set xpos [lindex [sg13g2::getbox] 0]
	    box position ${xpos}um 0um
	    set hgy [+ [/ $gedgey 2.0] 2.0]
	    box grow n ${hgy}um
	    box grow s ${hgy}um
	    if {($top_type != "") && ($tconnect == 1) && ($upcontact != 1)} {
		pushbox
		box grow e ${hmw}um
		box grow w ${hmw}um
		paint ${top_type}
		popbox
	    }
	    if {($bot_type != "") && ($bconnect == 1)} {
		set halftab [/ $tabwidth 2.0]
		pushbox
		box grow e ${halftab}um
		box grow w ${halftab}um
		paint ${bot_type}
		popbox
	    }
	    popbox
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
# Note:  cap_spacing is set to 0.6 which is the metal5 spacing
# for width and run > 10um.  It could be lower for small caps.
# Currently there is no override for this value.
#----------------------------------------------------------------

proc sg13g2::cap_cmim_draw {parameters} {
    set newdict [dict create \
	    top_type 		m6 \
	    top_contact_type	via5 \
	    cap_type 		mimcap \
	    cap_contact_type	mimcc \
	    bot_type 		m5 \
	    bot_surround	0.6 \
	    cap_spacing		0.6 \
	    cap_surround	0.2 \
	    top_surround	0.0 \
	    end_surround	0.0 \
	    metal_surround	0.32 \
	    top_contact_size    0.62 \
	    bot_width           0.20 \
	    bot_spacing         0.21 \
	    top_width           1.64 \
	    top_spacing         1.64 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::cap_draw $drawdict]
}

proc sg13g2::cap_rfcmim_draw {parameters} {
    set newdict [dict create \
	    guard		1 \
	    top_type 		m6 \
	    top_contact_type	via5 \
	    cap_type 		mimcap \
	    cap_contact_type	mimcc \
	    bot_type 		m5 \
	    bot_surround	0.6 \
	    cap_spacing		0.6 \
	    cap_surround	0.2 \
	    top_surround	0.0 \
	    end_surround	0.0 \
	    metal_surround	0.32 \
	    top_contact_size    0.62 \
	    bot_width           0.20 \
	    bot_spacing         0.21 \
	    top_width           1.64 \
	    top_spacing         1.64 \
	    cap_diff_spacing	3.00 \
	    contact_size	1.86 \
	    diff_width		2.00 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::cap_draw $drawdict]
}

#----------------------------------------------------------------
# capacitor: Check device parameters for out-of-bounds values
#----------------------------------------------------------------

proc sg13g2::cap_check {devname parameters} {
    # In case wmax and/or lmax are undefined
    set lmax 0
    set wmax 0
    set ccov 100
    set tabwidth 1.0
    set bconnect 0

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Normalize distance units to microns
    set l [magic::spice2float $l]
    set l [magic::3digitpastdecimal $l] 
    set w [magic::spice2float $w]
    set w [magic::3digitpastdecimal $w] 

    set val   [magic::spice2float $val]
    set carea [magic::spice2float $carea]
    set cperi [magic::spice2float $cperi]
    set dc    [magic::spice2float $dc]

    if {$square == 1} {
        # Calculate L and W from value
	set a $carea
	set b [expr $cperi * 4]
	set c [expr -4 * $dc - $val]
	set l [expr ((-$b + sqrt($b * $b - (4 * $a * $c))) / (2 * $a))]
	dict set parameters l [magic::float2spice $l]
	set w $l
	dict set parameters w [magic::float2spice $w]
    } elseif {$l == 0} {
        # Calculate L from W and value
	set l [expr (($val + 4 * $dc - 2 * $w * $cperi) / ($w * $carea + 2 * $cperi))]
	dict set parameters l [magic::float2spice $l]
    } elseif {$w == 0} {
        # Calculate W from L and value
	set w [expr (($val + 4 * $dc - 2 * $l * $cperi) / ($l * $carea + 2 * $cperi))]
	dict set parameters w [magic::float2spice $w]
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
    if {[catch {expr abs($ccov)}]} {
	puts stderr "Capacitor contact coverage must be numeric!"
        dict set parameters ccov 100
    } elseif {[expr abs($ccov)] > 100} {
	puts stderr "Capaitor contact coverage can't be more than 100%"
        dict set parameters ccov 100
    }

    if {$bconnect == 1} {
	# The rfcmim device requires the tab width to be at least 1um and
	# less than the width.  The regular cmim device has no such
	# restrictions, so set limits to 0.2um (metal minimum width) and
	# the width of the capacitor.

        if {$devname == "cap_rfcmim"} {
	    if {$tabwidth < 1.0} {
		puts stderr "Bottom plate tab must be at least 1um!"
		dict set parameters tabwidth 1.0
	    } elseif {$tabwidth > [- $w 1.2]} {
		puts stderr "Bottom plate tab must be no larger than the capacitor width (less 1.2um)!"
		dict set parameters tabwidth [- $w 1.2]
	    }
	} else {
	    if {$tabwidth < 0.2} {
		puts stderr "Bottom plate tab must be at least minimum metal width!"
		dict set parameters tabwidth 0.2
	    } elseif {$tabwidth > $w} {
		puts stderr "Bottom plate tab must be no larger than the capacitor width!"
		dict set parameters tabwidth $w
	    }
	}
    }

    # Calculate value from L and W
    set cval [expr ($l * $w * $carea + 2 * ($l + $w) * $cperi - 4 * $dc)]
    dict set parameters val [magic::float2spice $cval]
    sg13g2::compute_ctot $parameters

    return $parameters
}

proc sg13g2::cap_cmim_check {parameters} {
    return [sg13g2::cap_check cap_cmim $parameters]
}

proc sg13g2::cap_rfcmim_check {parameters} {
    return [sg13g2::cap_check cap_rfcmim $parameters]
}

#----------------------------------------------------------------
