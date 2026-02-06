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
# Bipolar transistors:
# Starting by copying "fixed device" routines and picking the
# example file from sg13g2_pr.  To be done:  Create callback
# routines for the bipolar devices.  Given the difference in
# layout, each one will likely have its own set of drawing
# routines, although they may share the other callbacks.
#
# npn13g2
# npn13g2l
# npn13g2v
# pnpMPA
#----------------------------------------------------------------

proc sg13g2::npn13g2_defaults {} {
    return {w 0.07 l 0.9 area 0.063 peri 1.94 class bjt \
	lmin 0.9 lmax 0.9 nx 1 nxmax 10 \
	compatible {npn13g2 npn13g2l npn13g2v} \
	elc 1 erc 1 etc 1 ebc 1 doports 1}
}
proc sg13g2::npn13g2l_defaults {} {
    return {w 0.07 l 1.0 area 0.07 peri 2.14 class bjt \
	lmin 1.0 lmax 2.5 nx 1 nxmax 4 \
	compatible {npn13g2 npn13g2l npn13g2v} \
	elc 1 erc 1 etc 1 ebc 1 doports 1}
}

proc sg13g2::npn13g2v_defaults {} {
    return {w 0.12 l 1.0 area 0.12 peri 2.24 class bjt \
	lmin 1.0 lmax 5.0 nx 1 nxmax 8 \
	compatible {npn13g2 npn13g2l npn13g2v} \
	elc 1 erc 1 etc 1 ebc 1 doports 1}
}

proc sg13g2::pnpMPA_defaults {} {
    return {w 2.0 l 0.7 area 1.4 peri 5.4 \
	nx 1 ny 1 dummy 0 lmin 0.7 wmin 2.0 class bjt \
	elc 1 erc 1 etc 1 ebc 1 doverlap 0 doports 1 \
	full_metal 1 vias 1 viagb 0 viagt 0 viagl 0 viagr 0}
}

#----------------------------------------------------------------
# Bipolar device: Conversion from SPICE netlist parameters to toolkit
#----------------------------------------------------------------

proc sg13g2::bipolar_convert {parameters} {
    set pdkparams [dict create]
    dict for {key value} $parameters {
	switch -nocase $key {
	    m {
		 dict set pdkparams nx $value
	    }
	    we {
		 dict set pdkparams w $value
	    }
	    le {
		 dict set pdkparams l $value
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

proc sg13g2::npn13g2_convert {parameters} {
    return [sg13g2::bipolar_convert $parameters]
}

proc sg13g2::npn13g2l_convert {parameters} {
    return [sg13g2::bipolar_convert $parameters]
}

proc sg13g2::npn13g2v_convert {parameters} {
    return [sg13g2::bipolar_convert $parameters]
}

proc sg13g2::pnpMPA_convert {parameters} {
    return [sg13g2::bipolar_convert $parameters]
}

#----------------------------------------------------------------
# Bipolar device: Interactively specifies the fixed layout parameters
#----------------------------------------------------------------

proc sg13g2::bipolar_dialog {device parameters} {
    # Editable fields:      l, area, perim, nx

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    magic::add_entry area "Area (um^2)" $parameters
    magic::add_entry peri "Perimeter (um)" $parameters
    sg13g2::compute_aptot $parameters
    magic::add_message atot "Total area (um^2)" $parameters
    magic::add_message ptot "Total perimeter (um)" $parameters
    magic::add_entry l "Emitter length (um)" $parameters
    magic::add_message w "Emitter width (um)" $parameters
    magic::add_entry nx "Number of emitters" $parameters

    if {[dict exists $parameters compatible]} {
       set sellist [dict get $parameters compatible]
       magic::add_selectlist gencell "Device type" $sellist $parameters $device
    }

    if {[dict exists $parameters guard]} {
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
    if {[dict exists $parameters viagb]} {
	magic::add_entry viagb  "Bottom guard ring via coverage \[+/-\](%)" $parameters
    }
    if {[dict exists $parameters viagt]} {
	magic::add_entry viagt  "Top guard ring via coverage \[+/-\](%)" $parameters
    }
    if {[dict exists $parameters viagr]} {
	magic::add_entry viagr  "Right guard ring via coverage \[+/-\](%)" $parameters
    }
    if {[dict exists $parameters viagl]} {
	magic::add_entry viagl  "Left guard ring via coverage \[+/-\](%)" $parameters
    }

    magic::add_dependency sg13g2::diode_recalc $device sg13g2 l w area peri

    if {[dict exists $parameters doports]} {
	magic::add_checkbox doports "Add ports" $parameters
    }
}

proc sg13g2::npn13g2_dialog {parameters} {
    sg13g2::bipolar_dialog npn13g2 $parameters
}

proc sg13g2::npn13g2l_dialog {parameters} {
    sg13g2::bipolar_dialog npn13g2l $parameters
}

proc sg13g2::npn13g2v_dialog {parameters} {
    sg13g2::bipolar_dialog npn13g2v $parameters
}

proc sg13g2::pnpMPA_dialog {parameters} {
    sg13g2::diode_dialog pnpMPA $parameters
}

#----------------------------------------------------------------
# SiGe bipolar base device:  This layout is fixed and cannot be
# modified.  If it exists already, then do not regenerate.
#----------------------------------------------------------------

proc sg13g2::npn13g2_base_generate {} {
    if {[cellname list exists npn13g2_base] != 0} {return}
    suspendall

    # Save critical values before creating and editing a new cell 
    set curcell [cellname list self]
    set curbox [box values]
    # Stop the tag method from messing with this procedure
    set ltag [tag load]
    tag load {}
    load npn13g2_base -silent
    tech unlock *
    set savesnap [snap]
    snap internal

    # Everything here is fixed geometry
    box values -0.975um 1.02um 0.975um 1.26um
    paint m1
    box values -0.35um -0.77um 0.35um 0.785um
    paint m1
    box values -0.925um -1.25um 0.925um -1.01um
    paint m1
    
    box values -0.925um -0.77um 0.925um 0.785um
    paint m2

    box values -0.305um -0.705um 0.305um 0.725um
    paint via

    box values -1.055um -1.41um 1.055um -0.85um
    paint pwell

    box values -0.925um -1.28um 0.925um -0.98um
    paint ndiff

    box values -0.825um -1.21um 0.825um -1.05um
    paint ndc

    box values -0.76um 1.06um 0.76um 1.22um
    paint pbasec

    polygon nemitter -0.925um -0.98um 0.925um -0.98um 0.925um 0.62um \
		0.445um 0.62um 0.235um 0.83um -0.235um 0.83um \
		-0.445um 0.62um -0.925um 0.62um

    polygon pbase -1.015um 2.47um -1.015um 0.86um -0.595um 0.44um \
		-0.595um -0.73um -0.345um -0.98um 0.345um -0.98um \
		0.595um -0.73um 0.595um 0.44um 1.015um 0.86um \
		1.015um 2.47um

    box values -0.035um -0.45um 0.035um 0.45um
    paint gemitterc

    # Cell has a text label at the bottom;  force it to attach to "comment"
    box position 0 -2.3um
    box size 0 0
    label npn13G2 c space
    select area label
    setlabel sticky 1
    setlabel layer comment
    
    # Return to our regularly scheduled program
    load $curcell
    snap $savesnap
    tag load $ltag
    tech revert
    box values {*}$curbox
    resumeall
}

#----------------------------------------------------------------
# Bipolar devices: Draw the device.  Each bipolar type has its
# own unique drawing routine.
#----------------------------------------------------------------

proc sg13g2::npn13g2_draw {parameters} {

    # To be done:  Loop over number of emitters

    tech unlock *
    set savesnap [snap]
    snap internal

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Emitter width is exactly 0.07um and cannot be changed
    set w 0.07

    # Spacing of multiple emitters is exactly 1.85um and cannot be changed
    set s 1.85

    box values 0 0 0 0
    pushbox

    # The guard ring is not centered on the device
    box move s 0.185um

    # Draw the guard ring first, then remove any pwell from inside
    set xoffset [* $s [- $nx 1]]
    set hxoffset [/ $xoffset 2.0]
    set gx [+ 5.73 $w $xoffset]
    set gy [+ 5.31 $l]
    dict set parameters contact_size ${contact_size}
    dict set parameters metal_surround ${metal_surround}
    dict set parameters metal_spacing ${metal_spacing}
    dict set parameters diff_surround ${diff_surround}
    dict set parameters sub_surround 0.2
    dict set parameters plus_diff_type    psd
    dict set parameters plus_contact_type psc
    dict set parameters diff_width 0.5
    # 
    set cext [sg13g2::guard_ring $gx $gy $parameters]
    # Remove pwell from center area
    select top cell
    box grow c -0.7um
    erase pwell

    popbox
    pushbox
    if {[cellname list exists npn13G2_base] == 0} {sg13g2::npn13g2_base_generate}
    box move w ${hxoffset}um
    for {set i 0} {$i < $nx} {incr i} {
	pushbox
	getcell npn13g2_base child 0 0
	popbox
	box move e ${s}um
    }
    popbox
    pushbox

    box grow c 0.745um
    box grow n 0.03um
    box grow s 0.03um
    box grow e ${hxoffset}um
    box grow w ${hxoffset}um
    paint m2
    if {$doports} {
	label E c m2
	port make
    }

    popbox
    pushbox

    box move n 1.135um
    box grow n 0.12um
    box grow s 0.12um
    box grow e 0.92um
    box grow w 0.92um
    box grow e ${hxoffset}um
    box grow w ${hxoffset}um
    paint m1
    if {$doports} {
	label C c m1
	port make
    }

    popbox
    pushbox

    box move s 1.135um
    box grow n 0.12um
    box grow s 0.12um
    box grow e 0.97um
    box grow w 0.97um
    box grow e ${hxoffset}um
    box grow w ${hxoffset}um
    paint m1
    if {$doports} {
	label B c m1
	port make
    }
    popbox

    snap $savesnap
    tech revert
}

#----------------------------------------------------------------

proc sg13g2::npn13g2l_draw {parameters} {

    # To be done:  Loop over number of emitters

    tech unlock *
    set savesnap [snap]
    snap internal

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Emitter width is exactly 0.07um and cannot be changed
    set w 0.07

    # Device spacing for multiple emitters is 2.8um and cannot be changed
    set s 2.80

    box values 0 0 0 0
    pushbox

    # Draw the guard ring first, otherwise it overwrites pbase
    set xoffset [* $s [- $nx 1]]
    set hxoffset [/ $xoffset 2.0]
    set gx [+ 6.82 $w $xoffset]
    set gy [+ 5.31 $l]
    dict set parameters contact_size ${contact_size}
    dict set parameters metal_surround ${metal_surround}
    dict set parameters metal_spacing ${metal_spacing}
    dict set parameters diff_surround ${diff_surround}
    dict set parameters sub_surround 0.05
    dict set parameters plus_diff_type    psd
    dict set parameters plus_contact_type psc
    dict set parameters diff_width 0.5
    set cext [sg13g2::guard_ring $gx $gy $parameters]
 
    # Length and width of the device are the length and width of
    # the emitter window/contact.  All other dimensions are
    # derived from this.

    set hl [/ $l 2.0]
    set hw [/ $w 2.0]

    box move w ${hxoffset}um

    # Loop through number of emitters
    for {set i 0} {$i < $nx} {incr i} {
	pushbox

	box grow w ${hw}um
	box grow e ${hw}um
	box grow n ${hl}um
	box grow s ${hl}um
	pushbox

	# Draw the substrate underneath
	pushbox
	box grow n 0.41um
	box grow s 0.41um
	box grow e 1.495um
	box grow w 1.495um
	paint pwell
	popbox

	# Draw the via over the emitter
	box grow e 0.065um
	box grow w 0.065um
	box grow n 0.105um
	box grow s 0.105um
	pushbox

	# Draw the full emitter diffusion area
	box grow e 0.03um
	box grow w 0.03um
	box grow n 0.175um
	box grow s 0.175um
	pushbox

	# Draw the base area
	box grow e 0.61um
	box grow w 0.61um
	pushbox

	# Draw the collector right side
	box move e [box width]
	box width 0.66um
	paint ndiff

	popbox
	pushbox

	# Draw the collector left side
	box move w 0.66um
	box width 0.66um
	paint ndiff

	popbox
	paint pbase

	popbox
	paint nemitter

	popbox
	paint via

	popbox
	pushbox

	# Draw the emitter metal1 area
	box grow n 0.2um
	box grow s 0.2um
	box grow e 0.095um
	box grow w 0.095um
	paint m1

	# Draw the emitter metal2 area (extends over the whole device)
	box grow e 1.27um
	box grow w 1.27um
	paint m2
	if {$i == 0} {
	    set ebox [sg13g2::getbox]
	} else {
	    set ebox [sg13g2::unionbox $ebox [sg13g2::getbox]]
	}
	popbox
	pushbox

	# Draw the right side base contact
	box move e [box width]
	box move e 0.32um
	box width 0.16um
	box grow n 0.2um
	box grow s 0.2um
	paint pbasec
	box grow n 0.08um
	box grow s 1.45um
	paint m1

	popbox
	pushbox

	# Draw the left side base contact
	box move w 0.48um
	box width 0.16um
	box grow n 0.2um
	box grow s 0.2um
	paint pbasec
	box grow n 0.08um
	box grow s 1.45um
	paint m1

	# Connect the two base sides across the bottom
	box height 0.65um
	box width 0.96um
	box grow e ${w}um
	paint m1
	if {$i == 0} {
	    set bbox [sg13g2::getbox]
	} else {
	    set bbox [sg13g2::unionbox $bbox [sg13g2::getbox]]
	}
	popbox
	pushbox

	# Paint the right side collector contact
	box move e [box width]
	box move e 1.025um
	box width 0.16um
	box grow s 0.15um
	box grow n 0.15um
	paint ndiffc
	box grow c 0.05um
	box grow s 0.08um
	box grow n 1.45um
	box grow e 0.13um
	paint m1

	popbox
	pushbox

	# Paint the left side collector contact
	box move w 1.185um
	box width 0.16um
	box grow s 0.15um
	box grow n 0.15um
	paint ndiffc
	box grow c 0.05um
	box grow s 0.08um
	box grow n 1.45um
	box grow w 0.13um
	paint m1

	# Connect the two collector sides across the top
	box move n 1.28um
	box move n ${l}um
	box height 0.65um
	box width 2.73um
	box grow e ${w}um
	paint m1
	if {$i == 0} {
	    set cbox [sg13g2::getbox]
	} else {
	    set cbox [sg13g2::unionbox $cbox [sg13g2::getbox]]
	}
	popbox
	paint nemitterc

	popbox
	box move e ${s}um
	# Repeat for next emitter
    }

    # Add labels for C, E, and B
    if {$doports} {
	sg13g2::setbox $cbox
	label C c m1
	port make

	sg13g2::setbox $bbox
	paint m1
	label B c m1
	port make

	sg13g2::setbox $ebox
	label E c m2
	port make
	# This port crosses vias, so make it sticky and make sure it
	# is on metal 2.
	select area label
	setlabel sticky 1
	setlabel layer m2
    }

    popbox
    snap $savesnap
    tech revert
}

#----------------------------------------------------------------
# Draw the high-voltage NPN
#----------------------------------------------------------------

proc sg13g2::npn13g2v_draw {parameters} {

    # To be done:  Loop over number of emitters

    tech unlock *
    set savesnap [snap]
    snap internal

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Emitter width is exactly 0.12um and cannot be changed
    set w 0.12

    # Device spacing for multiple emitters is 2.34um and cannot be changed
    set s 2.34

    box values 0 0 0 0
    pushbox

    # Draw the guard ring first, otherwise it overwrites pbase
    set xoffset [* $s [- $nx 1]]
    set hxoffset [/ $xoffset 2.0]
    set gx [+ 6.72 $w $xoffset]
    set gy [+ 5.3 $l]
    dict set parameters contact_size ${contact_size}
    dict set parameters metal_surround ${metal_surround}
    dict set parameters metal_spacing ${metal_spacing}
    dict set parameters diff_surround ${diff_surround}
    dict set parameters sub_surround 0.05
    dict set parameters plus_diff_type    psd
    dict set parameters plus_contact_type psc
    dict set parameters diff_width 0.5
    set cext [sg13g2::guard_ring $gx $gy $parameters]
 
    # Length and width of the device are the length and width of
    # the emitter window/contact.  All other dimensions are
    # derived from this.

    set hl [/ $l 2.0]
    set hw [/ $w 2.0]

    box move w ${hxoffset}um

    # Loop over all emitters

    for {set i 0} {$i < $nx} {incr i} {
	pushbox

	box grow w ${hw}um
	box grow e ${hw}um
	box grow n ${hl}um
	box grow s ${hl}um
	pushbox

	# Draw the substrate
	pushbox
	box grow n 0.41um
	box grow s 0.41um
	box grow e 1.24um
	box grow w 1.24um
	paint pwell
	popbox

	# Draw the via over the emitter
	box grow e 0.04um
	box grow w 0.04um
	box grow n 0.235um
	box grow s 0.235um
	pushbox

	# Draw the full emitter diffusion area
	box grow e 0.03um
	box grow w 0.03um
	box grow n 0.045um
	box grow s 0.045um
	pushbox

	# Draw the base area
	box grow e 0.635um
	box grow w 0.635um
	pushbox

	# Draw the collector right side
	box move e [box width]
	box width 0.405um
	paint ndiff

	popbox
	pushbox

	# Draw the collector left side
	box move w 0.405um
	box width 0.405um
	paint ndiff

	popbox
	paint pbase

	popbox
	paint hvnemitter

	popbox
	paint via

	popbox
	pushbox

	# Draw the emitter metal1 area
	box grow n 0.28um
	box grow s 0.28um
	box grow e 0.07um
	box grow w 0.07um
	paint m1

	# Draw the emitter metal2 area (extends over the whole device)
	box grow e 1.04um
	box grow w 1.04um
	paint m2
	if {$i == 0} {
	    set ebox [sg13g2::getbox]
	} else {
	    set ebox [sg13g2::unionbox $ebox [sg13g2::getbox]]
	}
	popbox
	pushbox

	# Draw the right side base contact
	box move e [box width]
	box move e 0.295um
	box width 0.17um
	box grow n 0.28um
	box grow s 0.28um
	paint pbasec
	box grow s 1.37um
	paint m1

	popbox
	pushbox

	# Draw the left side base contact
	box move w 0.465um
	box width 0.17um
	box grow n 0.28um
	box grow s 0.28um
	paint pbasec
	box grow s 1.37um
	paint m1

	# Connect the two base sides across the bottom
	box height 0.65um
	box width 0.93um
	box grow e ${w}um
	paint m1
	if {$i == 0} {
	    set bbox [sg13g2::getbox]
	} else {
	    set bbox [sg13g2::unionbox $bbox [sg13g2::getbox]]
	}
	popbox
	pushbox

	# Paint the right side collector contact
	box move e [box width]
	box move e 0.85um
	box width 0.16um
	box grow s 0.21um
	box grow n 0.21um
	paint ndiffc
	box grow c 0.06um
	box grow s 0.01um
	box grow n 1.38um
	box grow e 0.04um
	paint m1

	popbox
	pushbox

	# Paint the left side collector contact
	box move w 1.01um
	box width 0.16um
	box grow s 0.21um
	box grow n 0.21um
	paint ndiffc
	box grow c 0.06um
	box grow s 0.01um
	box grow n 1.38um
	box grow w 0.04um
	paint m1

	# Connect the two collector sides across the top
	box move n 1.28um
	box move n ${l}um
	box height 0.65um
	box width 2.22um
	box grow e ${w}um
	paint m1
	if {$i == 0} {
	    set cbox [sg13g2::getbox]
	} else {
	    set cbox [sg13g2::unionbox $cbox [sg13g2::getbox]]
	}
	popbox
	paint hvnemitterc

	popbox
	box move e ${s}um
	# Repeat for the next emitter
    }

    # Label all of the ports
    if {$doports} {
	# Collector
	sg13g2::setbox $cbox
	label C c m1
	port make

	# Base
	sg13g2::setbox $bbox
	paint m1
	label B c m1
	port make

	# Emitter
	sg13g2::setbox $ebox
	label E c m2
	port make
	# This port crosses vias, so make it sticky and make sure it
	# is on metal 2.
	select area label
	setlabel sticky 1
	setlabel layer m2
    }

    popbox
    snap $savesnap
    tech revert
}

#----------------------------------------------------------------
# The PNP is drawn like a diode (base, emitter)
# with a guard ring (collector)
#----------------------------------------------------------------

proc sg13g2::pnpMPA_draw {parameters} {
    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    guard		1 \
	    dev_type		pdiff \
	    dev_contact_type	pdc \
	    end_type		nsd \
	    end_contact_type	nsc \
	    end_sub_type	nbase \
	    dev_spacing		${diff_spacing} \
	    dev_surround	${diff_surround} \
	    end_spacing		${diff_spacing} \
	    end_surround	${diff_surround} \
	    diff_spacing	0.725 \
	    plus_contact_size	0.21 \
	    term_d		"E" \
	    term_s		"B" \
	    bulk		"C" \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::diode_draw $drawdict]
}

#----------------------------------------------------------------
# Bipolar device: Check device parameters for out-of-bounds values
#----------------------------------------------------------------

proc sg13g2::bipolar_check {parameters} {

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # nx must be integer and less that maximum
    if {![string is int $nx]} {
	puts stderr "Number of emitters must be an integer!"
        dict set parameters nx 1
    }
    if {$nxmax > 0 && $nx > $nxmax} {
	puts stderr "Number of emitters must be <= $nxmax"
	dict set parameters nx $nxmax
    }

    # Length muxt be within limits
    if {$l < $lmin} {
	puts stderr "Emitter length must be >= $lmin um"
	dict set parameters l $lmin
    } 
    if {$lmax > 0 && $l > $lmax} {
	puts stderr "Emitter length must be <= $lmax um"
	dict set parameters l $lmax
    }
    

    return $parameters
}

#----------------------------------------------------------------

proc sg13g2::npn13g2_check {parameters} {
    return [sg13g2::bipolar_check $parameters]
}

proc sg13g2::npn13g2l_check {parameters} {
    return [sg13g2::bipolar_check $parameters]
}

proc sg13g2::npn13g2v_check {parameters} {
    return [sg13g2::bipolar_check $parameters]
}

proc sg13g2::pnpMPA_check {parameters} {
    return [sg13g2::diode_check $parameters]
}

#----------------------------------------------------------------
