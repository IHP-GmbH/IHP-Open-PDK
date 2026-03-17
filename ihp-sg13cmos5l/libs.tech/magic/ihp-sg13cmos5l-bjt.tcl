########################################################################
#
# Copyright 2026 IHP PDK Authors
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
# The CMOS5L does not define any NPN devices.  The lateral PNP
# device is missing the deep nwell underneath that it has in the
# SG13G2 process, so its characteristics will be slightly different;
# however, it is still expected to behave similarly to the SG13G2
# pnpMPA model.
#
# pnpMPA
#----------------------------------------------------------------

proc sg13cmos5l::pnpMPA_defaults {} {
    return {w 2.0 l 0.7 area 1.4 peri 5.4 \
	nx 1 ny 1 dummy 0 lmin 0.7 wmin 2.0 class bjt \
	elc 1 erc 1 etc 1 ebc 1 doverlap 0 doports 1 \
	full_metal 1 vias 1 viagb 0 viagt 0 viagl 0 viagr 0}
}

#----------------------------------------------------------------
# Bipolar device: Conversion from SPICE netlist parameters to toolkit
#----------------------------------------------------------------

proc sg13cmos5l::bipolar_convert {parameters} {
    set pdkparams [dict create]
    dict for {key value} $parameters {
	switch -nocase $key {
	    m {
		 dict set pdkparams nx $value
	    }
	    we {
		# Convert value to microns
		set value [magic::spice2float $value]
		set value [expr $value * 1e6]
		dict set pdkparams w $value
	    }
	    le {
		# Convert value to microns
		set value [magic::spice2float $value]
		set value [expr $value * 1e6]
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

proc sg13cmos5l::pnpMPA_convert {parameters} {
    return [sg13cmos5l::bipolar_convert $parameters]
}

#----------------------------------------------------------------
# Bipolar device: Interactively specifies the fixed layout parameters
#----------------------------------------------------------------

proc sg13cmos5l::bipolar_dialog {device parameters} {
    # Editable fields:      l, area, perim, nx

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    magic::add_entry area "Area (um^2)" $parameters
    magic::add_entry peri "Perimeter (um)" $parameters
    sg13cmos5l::compute_aptot $parameters
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

    magic::add_dependency sg13cmos5l::diode_recalc $device sg13cmos5l l w area peri

    if {[dict exists $parameters doports]} {
	magic::add_checkbox doports "Add ports" $parameters
    }
}

proc sg13cmos5l::pnpMPA_dialog {parameters} {
    sg13cmos5l::diode_dialog pnpMPA $parameters
}

#----------------------------------------------------------------
# The PNP is drawn like a diode (base, emitter)
# with a guard ring (collector)
#----------------------------------------------------------------

proc sg13cmos5l::pnpMPA_draw {parameters} {
    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13cmos5l::ruleset] {
        set $key [dict get $sg13cmos5l::ruleset $key]
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
    set drawdict [dict merge $sg13cmos5l::ruleset $newdict $parameters]
    return [sg13cmos5l::diode_draw $drawdict]
}

#----------------------------------------------------------------
# Bipolar device: Check device parameters for out-of-bounds values
#----------------------------------------------------------------

proc sg13cmos5l::bipolar_check {parameters} {

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

proc sg13cmos5l::pnpMPA_check {parameters} {
    return [sg13cmos5l::diode_check $parameters]
}

#----------------------------------------------------------------
