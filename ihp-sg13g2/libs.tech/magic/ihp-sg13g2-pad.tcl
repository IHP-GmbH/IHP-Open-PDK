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
# Bond pad device (special drawing routine)
#----------------------------------------------------------------

proc sg13g2::bondpad_defaults {} {
    return {height 80 width 80 depth 5 class special shape octagon}
}

proc sg13g2::bondpad_convert {parameters} {
    set pdkparams [dict create]
    dict for {key value} $parameters {
	switch -nocase $key {
	    size {
		dict set pdkparams width $value
		dict set pdkparams height $value
	    }
	    default {
		# Allow unrecognized parameters to be passed unmodified
		dict set pdkparams $key $value
	    }
	}
    }
    return $pdkparams
}

proc sg13g2::bondpad_dialog {parameters} {
    # Instance fields:	    width, height, depth, shape
    # Editable fields:	    width, height, depth, shape
    # Non-editable fields:  

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    magic::add_entry width "W" $parameters
    magic::add_entry height "H" $parameters
    magic::add_entry depth "Number metals" $parameters
    set sellist {octagon square circle}
    magic::add_selectlist shape "Shape" $sellist $parameters octagon
}

# Note:  In some cases, round-off errors are violating the 45 degree angles?

proc sg13g2::bondpad_draw {parameters} {
    tech unlock *
    set savesnap [snap]
    snap internal

    # Set defaults if they are not in parameters
    set shape	octagon	;# Draw an octagon shape
    set depth	3	;# Use three metal layers for the pad

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    pushbox
    box values 0 0 0 0

    # Calculate pad polygons by drawing a circle of N points, where
    # N is 4 for a square, 8 for an octagon, and we will arbitrarily
    # set N to 24 for a circle.  The polygon will assume that W = L,
    # and points will be adjusted to make up the difference.

    if {$shape == "octagon"} {
	set npoints 8
    } elseif {$shape == "circle"} {
	# Note that this will violate DRC rules.
	set npoints 24
    } else {
	set npoints 4
    }

    set pwidth [- $width 4.2]		;# passivation cut layer width
    set pheight [- $height 4.2]		;# passivation cut layer width
    set mwidth [- $width 4.0]		;# metal (< 7) centerline
    set mheight [- $height 4.0]		;# metal (< 7) centerline

    set metal_edge [sg13g2::create_polygon $npoints $width $height]
    set glass_edge [sg13g2::create_polygon $npoints $pwidth $pheight]
    set metal_center [sg13g2::create_wire $npoints $mwidth $mheight]

    # Diagnostic
    # puts stdout "metal_edge = $metal_edge"
    # puts stdout "glass_edge = $glass_edge"
    # puts stdout "metal_center = $metal_center"

    # Create polygons
    polygon metal7 {*}$metal_edge
    polygon glass {*}$glass_edge

    # Create lower metals as wires 4um wide, matching the outer
    # edge of the pad metal.
    if {$depth > 1} {wire segment metal6 4um {*}$metal_center}
    if {$depth > 2} {wire segment metal5 4um {*}$metal_center}
    if {$depth > 3} {wire segment metal4 4um {*}$metal_center}
    if {$depth > 4} {wire segment metal3 4um {*}$metal_center}
    if {$depth > 5} {wire segment metal2 4um {*}$metal_center}
    if {$depth > 6} {wire segment metal1 4um {*}$metal_center}

    # Add contacts (note that currently all contacts violate DRC
    # rules because they cross the passivation boundary).

    set hmwidth [/ $mwidth 2.0]
    set hmheight [/ $mheight 2.0]

    if {$shape == "octagon"} {
	for {set i 1} {$i < $depth} {incr i} {
	    if {$i == 1} {set delta 3} else {set delta 1}
            set vn [- 7 $i]
	    # Draw the four sides
	    foreach {x1 y1 x2 y2} $metal_center {
		wire segment via${vn} 3um ${x1} ${y1} ${x2} ${y2} -noendcap
	    }
	    # Then fill in angled edges
	    foreach {x1 y1 x2 y2} [lrange $metal_center 2 end-2] {
		# Remove the "um" suffix from each value
		set x1 [string range $x1 0 end-2]
		set y1 [string range $y1 0 end-2]
		set x2 [string range $x2 0 end-2]
		set y2 [string range $y2 0 end-2]
		set x $x1
		set y $y1
		if {$y1 < $y2} {set yd $delta} else {set yd -$delta}

		if {$x1 < $x2} {
		    set xd $delta
		    for {set x [+ $x1 $xd] ; set y [+ $y1 $yd]} {$x <= [- $x2 $xd]} \
				{set x [+ $x $xd]; set y [+ $y $yd]} {
			box position ${x}um ${y}um
			box size 0 0
			box grow c 1um
			paint via${vn}
		    }
		} elseif {$x1 > $x2} {
		    set xd -$delta
		    for {set x [+ $x1 $xd] ; set y [+ $y1 $yd]} {$x > [- $x2 $xd]} \
				{set x [+ $x $xd]; set y [+ $y $yd]} {
			box position ${x}um ${y}um
			box size 0 0
			box grow c 1um
			paint via${vn}
		    }
		}
	    }
	}
    } elseif {$shape == "circle"} {
	set npoints [int [min $width $height]]
	set contact_points [sg13g2::create_wire $npoints $mwidth $mheight]
	for {set i 1} {$i < $depth} {incr i} {
            set vn [- 7 $i]
	    foreach {x y} [lrange $contact_points 2 end-2] {
		box position ${x} ${y}
		box size 0 0
		box grow c 1um
		paint via${vn}
	    }
	    # For oval pads, add contacts along the straight edges
	    if {$width > $height} {
		set wdelta [- [/ [- $width $height] 2.0] 3.0]
		wire segment via${vn} 3um \
			-${wdelta}um -${hmheight}um ${wdelta}um -${hmheight}um
		wire segment via${vn} 3um \
			-${wdelta}um ${hmheight}um ${wdelta}um ${hmheight}um
	    } elseif {$width < $height} {
		set hdelta [- [/ [- $height $width] 2.0] 3.0]
		wire segment via${vn} 3um \
			-${hmwidth}um -${hdelta}um -${hmwidth}um ${hdelta}um
		wire segment via${vn} 3um \
			${hmwidth}um -${hdelta}um ${hmwidth}um ${hdelta}um
	    }
	}
    } else {	;# "square"
	for {set i 1} {$i < $depth} {incr i} {
            set vn [- 7 $i]
	    wire segment via${vn} 3um \
			${hmwidth}um -${hmheight}um ${hmwidth}um ${hmheight}um
	    wire segment via${vn} 3um \
			-${hmwidth}um -${hmheight}um -${hmwidth}um ${hmheight}um
	    wire segment via${vn} 3um \
			-${hmwidth}um -${hmheight}um ${hmwidth}um -${hmheight}um
	    wire segment via${vn} 3um \
			-${hmwidth}um ${hmheight}um ${hmwidth}um ${hmheight}um
	}
    }

    popbox

    snap $savesnap
    tech revert
}

#----------------------------------------------------------------
# Bondpad device: Check device parameters for out-of-bounds values
#----------------------------------------------------------------

proc sg13g2::bondpad_check {parameters} {

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Metal depth must be 1 to 7
    if {$depth < 1} {
	puts stderr "depth must be >= 1"
        dict set parameters depth 1
    }
    if {$depth > 7} {
	puts stderr "depth must be <= 7"
        dict set parameters depth 7
    }

    # Min/Max passivation layer recommended dimensions are 30 and 150.
    # The pad is measured according to the metal layer dimension, where
    # the metal overlaps passivation cut by 2.1um, so add 4.2 to these.
    if {$width < 34.2} {
	puts stderr "width must be >= 34.2"
        dict set parameters width 34.2
    }
    if {$width > 154.2} {
	puts stderr "width must be <= 154.2"
        dict set parameters width 154.2
    }
    if {$height < 34.2} {
	puts stderr "height must be >= 34.2"
        dict set parameters height 34.2
    }
    if {$height > 154.2} {
	puts stderr "height must be <= 154.2"
        dict set parameters height 154.2
    }

    return $parameters
}

#----------------------------------------------------------------
