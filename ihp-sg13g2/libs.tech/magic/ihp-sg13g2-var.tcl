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
# Drawn varactor (SVaricap) routines
#----------------------------------------------------------------

proc sg13g2::SVaricap_defaults {} {
    return {w 3.74 l 0.30 class varactor \
		nx 1 ny 1 lmin 0.30 wmin 3.74 lmax 0.80 wmax 9.74 \
		nxmax 10 nymax 1 doports 1}
}

#----------------------------------------------------------------
# Varactor defaults:
#----------------------------------------------------------------
#  w      Width of varactor finger
#  l      Length of varactor finger
#  nx     Number of devices in X
#  ny     Number of devices in Y
#
#  wmin   Minimum allowed width (3.74um)
#  wmax   Maximum allowed width (9.74um)
#  lmin   Minimum allowed length (0.3um)
#  lmax   Maximum allowed length (0.8um)
#  nxmax  Maximum number of devices in X (10)
#  nymax  Maximum number of devices in Y (1)
#----------------------------------------------------------------

#----------------------------------------------------------------
# varactor: Conversion from SPICE netlist parameters to toolkit
#----------------------------------------------------------------

proc sg13g2::var_convert {parameters} {
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

proc sg13g2::SVaricap_convert {parameters} {
    return [var_convert $parameters]
}

#----------------------------------------------------------------
# varactor: Interactively specifies the fixed layout parameters
#----------------------------------------------------------------

proc sg13g2::var_dialog {device parameters} {
    # Editable fields:      w, l, nx, ny

    magic::add_entry l "Length (um)" $parameters
    magic::add_entry w "Width (um)" $parameters
    magic::add_entry nx "X Repeat" $parameters
    magic::add_entry ny "Y Repeat" $parameters

    if {[dict exists $parameters compatible]} {
	set sellist [dict get $parameters compatible]
	magic::add_selectlist gencell "Device type" $sellist $parameters $device
    }

    if {[dict exists $parameters doports]} {
	magic::add_checkbox doports "Add ports" $parameters
    }
}

proc sg13g2::SVaricap_dialog {parameters} {
    sg13g2::var_dialog SVaricap $parameters
}

#----------------------------------------------------------------
# varactor: Draw a single device (single SVaricap finger pair)
#----------------------------------------------------------------

proc sg13g2::var_device {parameters} {
    # Set local default values if they are not in parameters
    set var_spacing 0.25
    set doports 0	;# no port labels by default
    set ext_top 1	;# extend the top for abutting next varactor
    set ext_bot 0	;# don't extend the bottom for abutting last varactor
    set add_sub 1	;# add substrate connections

    set term_g1 ""
    set term_g2 ""

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Draw the device
    pushbox
    box size 0 0

    pushbox
    set devwid [+ $w 0.55]
    set devend 0.33
    set devlen [+ $l $l [* 2.0 $devend] $var_spacing]

    set hdevlen [/ $devlen 2.0]
    set hdevwid [/ $devwid 2.0]

    box grow e ${hdevlen}um
    box grow w ${hdevlen}um
    box grow n ${hdevwid}um
    box grow s ${hdevwid}um
    paint nsd
    set cext [sg13g2::getbox]

    box grow c 0.24um
    paint nwell
    popbox

    # Paint entire region with poly, then erase areas to make
    # the two fingers
    pushbox
    set fdist [+ [/ $var_spacing 2.0] $l]
    set gheight [+ $hdevwid 0.35]
    box grow e ${fdist}um
    box grow w ${fdist}um
    box grow n ${gheight}um
    box grow s ${gheight}um
    paint poly
    popbox

    # Center cut-out
    pushbox
    set fdist [/ $var_spacing 2.0]
    set gheight [- $hdevwid 0.15]
    box grow e ${fdist}um
    box grow w ${fdist}um
    box grow n ${gheight}um
    box grow s ${gheight}um
    erase poly
    popbox

    # Top cut-out
    pushbox
    box grow w ${fdist}um
    box grow e ${hdevlen}um
    box move n ${hdevwid}um
    box move s 0.4um
    box height 0.25um
    erase poly
    popbox
    
    # Bottom cut-out
    pushbox
    box grow e ${fdist}um
    box grow w ${var_spacing}um
    box grow w ${l}um
    box move s ${hdevwid}um
    box move n 0.15um
    box height 0.25um
    erase poly
    popbox
    
    # Paint the tabs under the gate contact
    if {$add_sub} {
	pushbox
	box grow e 0.12um
	box grow w 0.12um

	# Top tab
    
	pushbox
	box move n ${hdevwid}um
	box grow n 0.24um
	paint var
	box move n 0.24um
	box height 0.52um
	paint psd
	box grow c 0.13um
	box grow s -0.13um
	paint pwell
	popbox

	# Bottom tab

	pushbox
	box move s ${hdevwid}um
	box move s 0.24um
	box height 0.24um
	paint var
	box move s 0.52um
	box height 0.52um
	paint psd
	box grow c 0.13um
	box grow n -0.13um
	paint pwell
	popbox
	popbox
    }

    # Paint top poly contacts
    pushbox
    box move n ${hdevwid}um
    box move n 0.175um
    pushbox
    box grow n 0.13um
    box grow s 0.13um
    box grow e ${l}um
    box grow e 0.105um
    box grow w ${l}um
    box grow w 0.105um
    if {$ext_top} {
	pushbox
	box grow e 0.29um
	pushbox
	box grow n 0.045um
	box grow s 0.195um
	paint poly
	popbox
	paint m1
	popbox
    }
    paint m1
    pushbox
    box width 0.26um
    box grow c -0.05um
    paint pc
    popbox
    pushbox
    box move e [box width]
    box move w 0.26um
    box width 0.26um
    box grow c -0.05um
    paint pc
    popbox
    # Metal strap over gate
    box width ${l}um
    box grow e -0.04um
    box grow s ${w}um
    box grow s -0.12um
    box move s 0.26um
    paint m1
    box grow n -0.13um
    box grow c -0.05um
    paint varc

    popbox
    if {$doports && ($term_g2 != "")} {
        label $term_g2 c m1
	select area label
	port make
    }
    popbox

    # Paint bottom poly contacts
    pushbox
    box move s ${hdevwid}um
    box move s 0.175um
    pushbox
    box grow n 0.13um
    box grow s 0.13um
    box grow e ${l}um
    box grow e 0.105um
    box grow w ${l}um
    box grow w 0.105um
    if {$ext_bot} {
	pushbox
	box grow w 0.29um
	pushbox
	box grow n 0.195um
	box grow s 0.045um
	paint poly
	popbox
	paint m1
	popbox
    }
    paint m1
    pushbox
    box width 0.26um
    box grow c -0.05um
    paint pc
    popbox
    pushbox
    box move e [box width]
    box move w 0.26um
    box width 0.26um
    box grow c -0.05um
    paint pc
    popbox
    # Metal strap over gate
    box move e [box width]
    box move w ${l}um
    box width ${l}um
    box grow w -0.04um
    box move n 0.26um
    box grow n ${w}um
    box grow n -0.12um
    paint m1
    box grow s -0.13um
    box grow c -0.05um
    paint varc

    popbox
    if {$doports && ($term_g1 != "")} {
        label $term_g1 c m1
	select area label
	port make
    }
    popbox

    popbox

    return $cext
}

#----------------------------------------------------------------
# SVaricap: Draw the complete SVaricap device (all fingers)
#----------------------------------------------------------------

proc sg13g2::var_draw {parameters} {
    tech unlock *
    set savesnap [snap]
    snap internal

    # Set defaults if they are not in parameters
    set var_spacing 0.25
    set doports 0
    set term_w W

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
    set bbox [sg13g2::var_device $parameters]
    tech unlock *

    set fw [- [lindex $bbox 2] [lindex $bbox 0]]
    set fh [- [lindex $bbox 3] [lindex $bbox 1]]

    # Determine tile width (there is only one device allowed in Y)
    set dx [* [+ $l $var_spacing] 2.0]
    set dy $fh

    # Determine core width and height
    set corex [+ [* [- $nx 1] $dx] $fw]
    set corey [+ [* [- $ny 1] $dy] $fh]

    set hcorex [/ $corex 2.0]
    set hcorey [/ $corey 2.0]

    pushbox
    box move w ${hcorex}um

    # Draw the bottom/well ("W") contact
    # Shouldn't there be an option to connect from both sides?

    # Add 0.16 diffusion and well to the left side
    box grow n ${hcorey}um
    box grow s ${hcorey}um
    box width 0.16um
    box move w 0.16um
    paint nsd
    box grow c 0.24um
    paint nwell
    popbox

    pushbox
    box move w ${hcorex}um
    box move e 0.01um
    box grow w 0.1um
    box grow e 0.1um
    box grow n 0.48um
    box grow s 0.48um
    paint m1
    box grow n -0.05um
    box grow s -0.05um
    paint nsc

    if {$doports} {
        label W c nsc
	select area label
	port make
    }
    popbox

    dict set parameters add_sub 0 

    pushbox
    box move w ${hcorex}um
    box move e [/ $fw 2.0]um

    for {set xp 0} {$xp < $nx} {incr xp} {
        if {$xp > 0} {dict set parameters ext_bot 1}
        if {$xp == [- $nx 1]} {dict set parameters ext_top 0}
	if {$xp == [/ $nx 2]} {
	    dict set parameters add_sub 1
	    dict set parameters term_g1 G1 
	    dict set parameters term_g2 G2 
	} else {
	    dict set parameters add_sub 0
	    dict set parameters term_g1 ""
	    dict set parameters term_g2 ""
	}
	pushbox
	sg13g2::var_device $parameters
	popbox
        box move e ${dx}um
    }
    popbox
    popbox

    snap $savesnap
    tech revert
}

#----------------------------------------------------------------

proc sg13g2::SVaricap_draw {parameters} {
    set newdict [dict create \
	    metal_surround	0.32 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::var_draw $drawdict]
}

#----------------------------------------------------------------
# varactor: Check device parameters for out-of-bounds values
#----------------------------------------------------------------

proc sg13g2::var_check {parameters} {
    # In case any of the maximums are undefined
    set lmax 0
    set wmax 0
    set nxmax 1
    set nymax 1

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Normalize distance units to microns
    set l [magic::spice2float $l]
    set l [magic::3digitpastdecimal $l] 
    set w [magic::spice2float $w]
    set w [magic::3digitpastdecimal $w] 

    if {$w < $wmin} {
	puts stderr "SVaricap width must be >= $wmin"
	dict set parameters w $wmin
	set w $wmin
    } 
    if {$l < $lmin} {
	puts stderr "SVaricap length must be >= $lmin"
	dict set parameters l $lmin
	set l $lmin
    } 
    if {($wmax > 0) && ($w > $wmax)} {
	puts stderr "SVaricap width must be <= $wmax"
	dict set parameters w $wmax
	set w $wmax
    } 
    if {($lmax > 0) && ($l > $lmax)} {
	puts stderr "SVaricap length must be <= $lmax"
	dict set parameters l $lmax
	set l $lmax
    } 

    if {$nx > $nxmax} {
	puts stderr "SVaricap number of finger pairs must be <= $nxmax"
        dict set parameters nx $nxmax
    }

    if {$ny > $nymax} {
	puts stderr "SVaricap number of devices must be <= $nymax"
        dict set parameters ny $nymax
    }

    return $parameters
}

proc sg13g2::SVaricap_check {parameters} {
    return [sg13g2::var_check $parameters]
}

#----------------------------------------------------------------
