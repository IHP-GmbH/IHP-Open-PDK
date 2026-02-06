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
# Fixed device: Specify all user-editable default values
#
# deltax --- Additional horizontal space between devices
# deltay --- Additional vertical space between devices
# nx     --- Number of arrayed devices in X
# ny     --- Number of arrayed devices in Y
#
# Note that these values, specifically nx, ny, deltax,
# and deltay, are properties of the instance, not the cell.
# They translate to the instance array x and y counts;  while
# deltax is the x pitch less the cell width, and deltay is the
# y pitch less the cell height.
#
# non-user-editable
#
# nocell --- Indicates that this cell has a predefined layout
#	     and therefore there is no cell to draw.
# xstep  --- Width of the cell (nominal array pitch in X)
# ystep  --- Height of the cell (nominal array pitch in Y)
#----------------------------------------------------------------

# Fixed-layout devices (from sg13g2_fd_pr library)
#
# diodevdd_2kv
# diodevdd_4kv
# diodevss_2kv
# diodevss_4kv
# nmoscl_2
# nmoscl_4
# scr1
# schottky_nbl1

proc sg13g2::diodevdd_2kv_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 nocell 1 \
    compatible {diodevdd_2kv diodevdd_4kv diodevss_2kv diodevss_4kv} \
    xstep 13.3 ystep 35.67 class diode}
}
proc sg13g2::diodevdd_4kv_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 nocell 1 \
    compatible {diodevdd_2kv diodevdd_4kv diodevss_2kv diodevss_4kv} \
    xstep 18.1 ystep 35.67 class diode}
}

proc sg13g2::diodevss_2kv_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 nocell 1 \
    compatible {diodevdd_2kv diodevdd_4kv diodevss_2kv diodevss_4kv} \
    xstep 13.3 ystep 35.67 class diode}
}

proc sg13g2::diodevss_4kv_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 nocell 1 \
    compatible {diodevdd_2kv diodevdd_4kv diodevss_2kv diodevss_4kv} \
    xstep 18.1 ystep 35.67 class diode}
}

proc sg13g2::nmoscl_2_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 nocell 1 \
    compatible {nmoscl_2 nmoscl_4} \
    xstep 35.76 ystep 24 class mosfet}
}

proc sg13g2::nmoscl_4_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 nocell 1 \
    compatible {nmoscl_2 nmoscl_4} \
    xstep 67.68 ystep 24 class mosfet}
}

proc sg13g2::scr1_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 nocell 1 \
    xstep 16.8 ystep 31.2 class diode}
}

proc sg13g2::schottky_nbl1_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 nocell 1 \
    xstep 5.5 ystep 6.0 class diode}
}

#----------------------------------------------------------------
# Bipolar device: Conversion from SPICE netlist parameters to toolkit
#----------------------------------------------------------------

proc sg13g2::fixed_convert {parameters} {
    set pdkparams [dict create]
    dict for {key value} $parameters {
	switch -nocase $key {
	    m {
		 dict set pdkparams nx $value
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
# To be reworked:  Bipolars are not fixed devices.  Each has
# a unique layout and needs its own drawing routine.
#----------------------------------------------------------------

proc sg13g2::diodevdd_2kv_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}

proc sg13g2::diodevdd_4kv_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}

proc sg13g2::diodevss_2kv_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}

proc sg13g2::diodevss_4kv_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}

proc sg13g2::nmoscl_2_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}

proc sg13g2::nmoscl_4_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}

proc sg13g2::scr1_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}

proc sg13g2::schottky_nbl1_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}

#----------------------------------------------------------------
# Fixed device: Interactively specifies the fixed layout parameters
#----------------------------------------------------------------

proc sg13g2::fixed_dialog {device parameters} {
    # Instance fields:	    nx, ny, pitchx, pitchy
    # Editable fields:	    nx, ny, deltax, deltay
    # Non-editable fields:  nocell, xstep, ystep

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # "nocell" field causes nx and ny to be dropped in from
    # "array count".  Also "pitchx" and "pitchy" are passed
    # in internal units.  Convert these to microns and generate
    # If there is no pitchx and pitchy, then the device has not
    # yet been created, so keep the deltax and deltay defaults.

    if [dict exists $parameters pitchx] {
	set pitchux [magic::i2u $pitchx]
	set stepux [magic::spice2float $xstep]
        set deltax [magic::3digitpastdecimal [expr $pitchux - $stepux]] 
        # An array size 1 should not cause deltax to go negative
	if {$deltax < 0.0} {set deltax 0.0}
	dict set parameters deltax $deltax
    }
    if [dict exists $parameters pitchy] {
	set pitchuy [magic::i2u $pitchy]
	set stepuy [magic::spice2float $ystep]
        set deltay [magic::3digitpastdecimal [expr $pitchuy - $stepuy]] 
        # An array size 1 should not cause deltay to go negative
	if {$deltay < 0.0} {set deltay 0.0}
	dict set parameters deltay $deltay
    }

    magic::add_entry nx "NX" $parameters
    magic::add_entry ny "NY" $parameters
    magic::add_entry deltax "X step (um)" $parameters
    magic::add_entry deltay "Y step (um)" $parameters

    if {[dict exists $parameters compatible]} {
	set sellist [dict get $parameters compatible]
	magic::add_selectlist gencell "Device type" $sellist $parameters $device
    }
}

proc sg13g2::diodevdd_2kv_dialog {parameters} {
    sg13g2::fixed_dialog diodevdd_2kv $parameters
}

proc sg13g2::diodevdd_4kv_dialog {parameters} {
    sg13g2::fixed_dialog diodevdd_4kv $parameters
}

proc sg13g2::diodevss_2kv_dialog {parameters} {
    sg13g2::fixed_dialog diodevss_2kv $parameters
}

proc sg13g2::diodevss_4kv_dialog {parameters} {
    sg13g2::fixed_dialog diodevss_4kv $parameters
}

proc sg13g2::nmoscl_2_dialog {parameters} {
    sg13g2::fixed_dialog nmoscl_2 $parameters
}

proc sg13g2::nmoscl_4_dialog {parameters} {
    sg13g2::fixed_dialog nmoscl_4 $parameters
}

proc sg13g2::scr1_dialog {parameters} {
    sg13g2::fixed_dialog scr1 $parameters
}

proc sg13g2::schottky_nbl1_dialog {parameters} {
    sg13g2::fixed_dialog schottky_nbl1 $parameters
}

#----------------------------------------------------------------
# Fixed devices:  Generate the devices
#----------------------------------------------------------------

proc sg13g2::diodevdd_2kv_generate {} {
    if {[cellname list exists diodevdd_2kv]} {return}
    suspendall

    # Save critical values before creating and editing a new cell 
    set curcell [cellname list window]
    set curbox [box values]
    # Stop the tag method from messing with this procedure
    set ltag [tag load]
    tag load {}
    load diodevdd_2kv -silent
    tech unlock *
    set savesnap [snap]
    snap internal

    source ${sg13g2::script_path}/diodevdd_2kv.tcl

    # Return to our regularly scheduled program
    load $curcell
    snap $savesnap
    tag load $ltag
    tech revert
    box values {*}$curbox
    resumeall
}

#----------------------------------------------------------------
#----------------------------------------------------------------

proc sg13g2::diodevdd_4kv_generate {} {
    if {[cellname list exists diodevdd_4kv]} {return}
    suspendall

    # Save critical values before creating and editing a new cell 
    set curcell [cellname list window]
    set curbox [box values]
    # Stop the tag method from messing with this procedure
    set ltag [tag load]
    tag load {}
    load diodevdd_4kv -silent
    tech unlock *
    set savesnap [snap]
    snap internal

    source ${sg13g2::script_path}/diodevdd_4kv.tcl

    # Return to our regularly scheduled program
    load $curcell
    snap $savesnap
    tag load $ltag
    tech revert
    box values {*}$curbox
    resumeall
}

#----------------------------------------------------------------
#----------------------------------------------------------------

proc sg13g2::diodevss_2kv_generate {} {
    if {[cellname list exists diodevss_2kv]} {return}
    suspendall

    # Save critical values before creating and editing a new cell 
    set curcell [cellname list window]
    set curbox [box values]
    # Stop the tag method from messing with this procedure
    set ltag [tag load]
    tag load {}
    load diodevss_2kv -silent
    tech unlock *
    set savesnap [snap]
    snap internal

    source ${sg13g2::script_path}/diodevss_2kv.tcl

    # Return to our regularly scheduled program
    load $curcell
    snap $savesnap
    tag load $ltag
    tech revert
    box values {*}$curbox
    resumeall
}

#----------------------------------------------------------------
#----------------------------------------------------------------

proc sg13g2::diodevss_4kv_generate {} {
    if {[cellname list exists diodevss_4kv]} {return}
    suspendall

    # Save critical values before creating and editing a new cell 
    set curcell [cellname list window]
    set curbox [box values]
    # Stop the tag method from messing with this procedure
    set ltag [tag load]
    tag load {}
    load diodevss_4kv -silent
    tech unlock *
    set savesnap [snap]
    snap internal

    source ${sg13g2::script_path}/diodevss_4kv.tcl

    # Return to our regularly scheduled program
    load $curcell
    snap $savesnap
    tag load $ltag
    tech revert
    box values {*}$curbox
    resumeall
}

#----------------------------------------------------------------
#----------------------------------------------------------------

proc sg13g2::nmoscl_2_generate {} {
    if {[cellname list exists nmoscl_2]} {return}
    suspendall

    # Save critical values before creating and editing a new cell 
    set curcell [cellname list window]
    set curbox [box values]
    # Stop the tag method from messing with this procedure
    set ltag [tag load]
    tag load {}
    load nmoscl_2 -silent
    tech unlock *
    set savesnap [snap]
    snap internal

    source ${sg13g2::script_path}/nmoscl_2.tcl

    # Return to our regularly scheduled program
    load $curcell
    snap $savesnap
    tag load $ltag
    tech revert
    box values {*}$curbox
    resumeall
}

#----------------------------------------------------------------
#----------------------------------------------------------------

proc sg13g2::nmoscl_4_generate {} {
    if {[cellname list exists nmoscl_4]} {return}
    suspendall

    # Save critical values before creating and editing a new cell 
    set curcell [cellname list window]
    set curbox [box values]
    # Stop the tag method from messing with this procedure
    set ltag [tag load]
    tag load {}
    load nmoscl_4 -silent
    tech unlock *
    set savesnap [snap]
    snap internal

    source ${sg13g2::script_path}/nmoscl_4.tcl

    # Return to our regularly scheduled program
    load $curcell
    snap $savesnap
    tag load $ltag
    tech revert
    box values {*}$curbox
    resumeall
}

#----------------------------------------------------------------
#----------------------------------------------------------------

proc sg13g2::scr1_generate {} {
    if {[cellname list exists scr1]} {return}
    suspendall

    # Save critical values before creating and editing a new cell 
    set curcell [cellname list window]
    set curbox [box values]
    # Stop the tag method from messing with this procedure
    set ltag [tag load]
    tag load {}
    load scr1 -silent
    tech unlock *
    set savesnap [snap]
    snap internal

    source ${sg13g2::script_path}/scr1.tcl

    # Return to our regularly scheduled program
    load $curcell
    snap $savesnap
    tag load $ltag
    tech revert
    box values {*}$curbox
    resumeall
}

#----------------------------------------------------------------
#----------------------------------------------------------------

proc sg13g2::schottky_nbl1_generate {} {
    if {[cellname list exists schottky_nbl1]} {return}
    suspendall

    # Save critical values before creating and editing a new cell 
    set curcell [cellname list window]
    set curbox [box values]
    # Stop the tag method from messing with this procedure
    set ltag [tag load]
    tag load {}
    load schottky_nbl1 -silent
    tech unlock *
    set savesnap [snap]
    snap internal

    source ${sg13g2::script_path}/schottky_nbl1.tcl

    # Return to our regularly scheduled program
    load $curcell
    snap $savesnap
    tag load $ltag
    tech revert
    box values {*}$curbox
    resumeall
}

#----------------------------------------------------------------
# Fixed device: Draw the device
#----------------------------------------------------------------

proc sg13g2::fixed_draw {devname parameters} {

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # This cell declares "nocell" in parameters, so it needs to
    # instance the cell and set properties.

    # Instantiate the cell.  The name corresponds to the cell in the sg13g2_fd_pr_* directory.
    set instname [getcell ${devname}]

    set deltax [magic::spice2float $deltax] 
    set deltay [magic::spice2float $deltay] 
    set xstep [magic::spice2float $xstep] 
    set ystep [magic::spice2float $ystep] 

    # Array stepping
    if {$nx > 1 || $ny > 1} {
        set xstep [expr $xstep + $deltax]
        set ystep [expr $ystep + $deltay]
        box size ${xstep}um ${ystep}um
	array $nx $ny
    }
    select cell $instname
    expand
    return $instname
}

#----------------------------------------------------------------
# No additional parameters declared for drawing
#----------------------------------------------------------------

proc sg13g2::diodevdd_2kv_draw {parameters} {
    if {[cellname list exists diodevdd_2kv] == 0} {sg13g2::diodevdd_2kv_generate}
    return [sg13g2::fixed_draw diodevdd_2kv $parameters]
}

proc sg13g2::diodevdd_4kv_draw {parameters} {
    if {[cellname list exists diodevdd_4kv] == 0} {sg13g2::diodevdd_4kv_generate}
    return [sg13g2::fixed_draw diodevdd_4kv $parameters]
}

proc sg13g2::diodevss_2kv_draw {parameters} {
    if {[cellname list exists diodevss_2kv] == 0} {sg13g2::diodevss_2kv_generate}
    return [sg13g2::fixed_draw diodevss_2kv $parameters]
}

proc sg13g2::diodevss_4kv_draw {parameters} {
    if {[cellname list exists diodevss_4kv] == 0} {sg13g2::diodevss_4kv_generate}
    return [sg13g2::fixed_draw diodevss_4kv $parameters]
}

proc sg13g2::nmoscl_2_draw {parameters} {
    if {[cellname list exists nmoscl_2] == 0} {sg13g2::nmoscl_2_generate}
    return [sg13g2::fixed_draw nmoscl_2 $parameters]
}

proc sg13g2::nmoscl_4_draw {parameters} {
    if {[cellname list exists nmoscl_4] == 0} {sg13g2::nmoscl_4_generate}
    return [sg13g2::fixed_draw nmoscl_4 $parameters]
}

proc sg13g2::scr1_draw {parameters} {
    if {[cellname list exists scr1] == 0} {sg13g2::scr1_generate}
    return [sg13g2::fixed_draw scr1 $parameters]
}

proc sg13g2::schottky_nbl1_draw {parameters} {
    if {[cellname list exists schottky_nbl1] == 0} {sg13g2::schottky_nbl1_generate}
    return [sg13g2::fixed_draw schottky_nbl1 $parameters]
}

#----------------------------------------------------------------
# Fixed device: Check device parameters for out-of-bounds values
#----------------------------------------------------------------

proc sg13g2::fixed_check {parameters} {

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Normalize distance units to microns
    set deltax [magic::spice2float $deltax -1] 
    set deltax [magic::3digitpastdecimal $deltax]
    set deltay [magic::spice2float $deltay -1] 
    set deltay [magic::3digitpastdecimal $deltay]

    # nx, ny must be integer
    if {![string is int $nx]} {
	puts stderr "NX must be an integer!"
        dict set parameters nx 1
    }
    if {![string is int $ny]} {
	puts stderr "NY must be an integer!"
        dict set parameters nx 1
    }

    # Number of devices in X and Y must be at least 1
    if {$nx < 1} {
	puts stderr "NX must be >= 1"
        dict set parameters nx 1
    }
    if {$ny < 1} {
	puts stderr "NY must be >= 1"
        dict set parameters nx 1
    }
    # Step less than zero violates DRC
    if {$deltax < 0} {
	puts stderr "X step must be >= 0"
        dict set parameters deltax 0
    }
    if {$deltay < 0} {
	puts stderr "Y step must be >= 0"
        dict set parameters deltay 0
    }
    return $parameters
}

#----------------------------------------------------------------

proc sg13g2::diodevdd_2kv_check {parameters} {
    return [sg13g2::fixed_check $parameters]
}

proc sg13g2::diodevdd_4kv_check {parameters} {
    return [sg13g2::fixed_check $parameters]
}

proc sg13g2::diodevss_2kv_check {parameters} {
    return [sg13g2::fixed_check $parameters]
}

proc sg13g2::diodevss_4kv_check {parameters} {
    return [sg13g2::fixed_check $parameters]
}

proc sg13g2::nmoscl_2_check {parameters} {
    return [sg13g2::fixed_check $parameters]
}

proc sg13g2::nmoscl_4_check {parameters} {
    return [sg13g2::fixed_check $parameters]
}

proc sg13g2::scr1_check {parameters} {
    return [sg13g2::fixed_check $parameters]
}

proc sg13g2::schottky_nbl1_check {parameters} {
    return [sg13g2::fixed_check $parameters]
}

#----------------------------------------------------------------
