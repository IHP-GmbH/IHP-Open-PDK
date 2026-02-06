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
# Routines for generated vias
#----------------------------------------------------------------

proc sg13g2::via_defaults {} {
   return {metalbot metal1 metaltop metal2 nxcuts 1 nycuts 1 \
	orient default pattern none}
}

proc sg13g2::via_dialog {parameters} {
    # Editable fields:     all of them
    # Special handling:
    #	cuts can be lists if metaltop - metalbot > 1
    #	orientation can be a list if non-default

    set sellist {metal1 metal2 metal3 metal4 metal5 metal6}
    magic::add_selectlist metalbot "Bottom metal" $sellist $parameters metal1
    set sellist {metal2 metal3 metal4 metal5 metal6 metal7}
    magic::add_selectlist metaltop "Top metal" $sellist $parameters metal2

    # NOTE: Need to implement custom per-layer orientation
    set sellist {default inverse horizontal vertical}
    magic::add_selectlist orient "Orientation" $sellist $parameters default

    # NOTE: "none" just uses a square via area, filled by the algorithm.
    # To do:  Implement a "checker" pattern
    set sellist {none offset}
    magic::add_selectlist pattern "Pattern" $sellist $parameters none

    magic::add_entry nxcuts "Number cuts in X" $parameters
    magic::add_entry nycuts "Number cuts in Y" $parameters
}

proc sg13g2::via_convert {parameters} {
    # Vias do not import from SPICE;  nothing to do.
}

proc sg13g2::via_check {parameters} {
    # Numerical sanity checks

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # nxcuts and nycuts can be arrays of values.  If they are arrays,
    # then check that each entry in the array is integer, and that
    # the number of entries matches or exceeds the number of metal
    # layers selected.  If less, then pad out the list.

    for {set i 0} {$i < [llength $nxcuts]} {incr i} {
	set nxcut [lindex $nxcuts $i]
	if {[catch {expr abs($nxcut)}]} {
	    puts stderr "Number of cuts in X must be numeric!"
	    set nxcuts [lreplace $nxcuts $i $i 1]
            dict set parameters nxcuts $nxcuts
	} elseif {$nxcut < 1} {
	    puts stderr "Number of cuts in X must be at least 1!"
	    set nxcuts [lreplace $nxcuts $i $i 1]
            dict set parameters nxcuts $nxcuts
	} elseif {[floor $nxcut] != $nxcut} {
	    puts stderr "Number of cuts in X must be an integer!"
	    set nxcuts [lreplace $nxcuts $i $i [floor $nxcut]]
            dict set parameters nxcuts $nxcuts
	}
    }
    for {set i 0} {$i < [llength $nycuts]} {incr i} {
	set nycut [lindex $nycuts $i]
	if {[catch {expr abs($nycut)}]} {
	    puts stderr "Number of cuts in Y must be numeric!"
	    set nycuts [lreplace $nycuts $i $i 1]
            dict set parameters nycuts $nycuts
	} elseif {$nycut < 1} {
	    puts stderr "Number of cuts in Y must be at least 1!"
	    set nycuts [lreplace $nycuts $i $i 1]
            dict set parameters nycuts $nycuts
	} elseif {[floor $nycut] != $nycut} {
	    puts stderr "Number of cuts in Y must be an integer!"
	    set nycuts [lreplace $nycuts $i $i [floor $nycut]]
            dict set parameters nycuts $nycuts
	}
    }

    set metallist {metal1 metal2 metal3 metal4 metal5 metal6 metal7}
    set mbotidx [lsearch $metallist $metalbot]
    set mtopidx [lsearch $metallist $metaltop]

    if {$mbotidx < 0} {
	puts stderr "Invalid bottom metal selection!"
	set mbotidx 0
        dict set parameters metalbot metal1
    }
    if {$mtopidx < 0} {
	puts stderr "Invalid top metal selection!"
	if {$mtopidx == 6} {
	    set mbotidx 5
	} else {
	    set mtopidx [+ $mbotidx 1]
	}
        dict set parameters metaltop [lindex $metallist $mtopidx]
        dict set parameters metalbot [lindex $metallist $mbotidx]
    }
    if {$mtopidx <= $mbotidx} {
	puts stderr "Top metal must be higher than the bottom metal!"
	if {$mtopidx == 6} {
	    set mbotidx [- $mtopidx 1]
	} else {
	    set mtopidx [+ $mbotidx 1]
	}
        dict set parameters metaltop [lindex $metallist $mtopidx]
        dict set parameters metalbot [lindex $metallist $mbotidx]
    }

    set numvias [- $mtopidx $mbotidx]
    set numxcuts [llength $nxcuts]
    set numycuts [llength $nycuts]
    if {($numxcuts != 1) && ($numxcuts < $numvias)} {
	puts stderr "List of cuts in X padded to match metal layer stack."
	for {set i $numxcuts} {$i < $numvias} {incr i} {
	    lappend nxcuts [lindex $nxcuts end]
	}
	dict set parameters nxcuts $nxcuts
    }
    if {($numycuts != 1) && ($numycuts < $numvias)} {
	puts stderr "List of cuts in Y padded to match metal layer stack."
	for {set i $numycuts} {$i < $numvias} {incr i} {
	    lappend nycuts [lindex $nycuts end]
	}
	dict set parameters nycuts $nycuts
    }
    return $parameters
}

proc sg13g2::via_draw {parameters} {

    # suspendall

    # Set defaults if they are not in parameters
    set nxcuts 1
    set nycuts 2
    set pattern none
    set orient default

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Local to this routine:  width, spacing, and overlap rules
    # for each via layer, starting with via1.  Note that via rules
    # are magic's rules for via areas, not IHP rules for cut layers.

    set metalwidthrule {0.16  0.20  0.20  0.20  0.20  1.64 2.00}
    set metalarearule  {0.09  0.144 0.144 0.144 0.144 0.0  0.0}
    set viawidthrule   {0.20  0.20  0.20  0.20  0.62  1.90}
    set spacingrule    {0.21  0.21  0.21  0.21  0.22  0.06}
    set b0overlaprule  {0.005 0.0   0.0   0.0   0.0   0.0}
    set b1overlaprule  {0.045 0.045 0.045 0.045 0.0   0.0}
    set t0overlaprule  {0.0   0.0   0.0   0.0   0.32  0.0}
    set t1overlaprule  {0.045 0.045 0.045 0.045 0.32  0.0}

    # These are IHP cut rules and are needed to determine what area
    # is required for a specific number of cuts.
    set cutsizerule    {0.19  0.19  0.19  0.19  0.42  0.90}
    set cutspacerule   {0.22  0.22  0.22  0.22  0.42  1.06}
    set cutspace2rule  {0.29  0.29  0.29  0.29  0.42  1.06}
    set cutborderrule  {0.005 0.005 0.005 0.005 0.10  0.50}

    # Convert metalbot and metaltop to array indexes
    set metallist {metal1 metal2 metal3 metal4 metal5 metal6 metal7}
    set metalbot [lsearch $metallist $metalbot]
    set metaltop [lsearch $metallist $metaltop]

    # Expand cuts to cover all layers
    set numvias [- $metaltop $metalbot]
    set numlayers [+ $numvias 1]
    if {[llength $nxcuts] == 1} {
	set nxcuts [lrepeat 6 $nxcuts]
    } elseif {[llength $nxcuts] == $numvias} {
	set allnxcuts {}
	for {set i 0} {$i < $metalbot} {incr i} {
	    lappend allnxcuts 1
	}
	lappend allnxcuts {*}$nxcuts
	for {set i $metaltop} {$i < 7} {incr i} {
	    lappend allnxcuts 1
	}
	set nxcuts $allnxcuts
    }

    if {[llength $nycuts] == 1} {
	set nycuts [lrepeat 6 $nycuts]
    } elseif {[llength $nycuts] == $numvias} {
	set allnycuts {}
	for {set i 0} {$i < $metalbot} {incr i} {
	    lappend allnycuts 1
	}
	lappend allnycuts {*}$nycuts
	for {set i $metaltop} {$i < 7} {incr i} {
	    lappend allnycuts 1
	}
	set nycuts $allnycuts
    }

    if {[llength $orient] == 1} {
	if {$orient == "default"} {
	    set orient [lrepeat 4 horizontal vertical]
	} elseif {$orient == "inverse"} {
	    set orient [lrepeat 4 vertical horizontal]
	} else {
	    set orient [lrepeat 7 $orient]
	}
    } elseif {[llength $orient] == $numlayers} {
	# NOTE:  Custom per-layer orientation is not yet implemented in
	# the via dialog.
	set allorient {}
	for {set i 0} {$i < $metalbot} {incr i} {
	    lappend allorient default
	}
	lappend allorient {*}$orient
	for {set i $metaltop} {$i < 7} {incr i} {
	    lappend allorient default
	}
	set orient $allorient
    }

    # For offset patterns, reduce the counts of every other layer by 1
    # unless the count is only 1.
    if {$pattern == "offset"} {
	for {set i [+ $metalbot 1]} {$i <= $metaltop} {incr i 2} {
	    set lnxcuts [lindex $nxcuts $i]
	    set lnycuts [lindex $nycuts $i]
	    if {$lnxcuts > 1} {
		incr lnxcuts -1
		set nxcuts [lreplace $nxcuts $i $i $lnxcuts]
	    }
	    if {$lnycuts > 1} {
		incr lnycuts -1
		set nycuts [lreplace $nycuts $i $i $lnycuts]
	    }
	}
    }
    
    # Make sure all layers are represented so that indexing works.
    set metalwidth [lrepeat 7 0]
    set metalheight [lrepeat 7 0]
    set viawidth [lrepeat 6 0]
    set viaheight [lrepeat 6 0]

    # Compute the via layer area from the border/size/space rules
    for {set i $metalbot} {$i < $metaltop} {incr i} {
	set cutsize [lindex $cutsizerule $i]
	set cutborder [* [lindex $cutborderrule $i] 2]
	set lnxcuts [lindex $nxcuts $i]
	set lnycuts [lindex $nycuts $i]
	if {$lnxcuts > 3} {
	    set cutspacex [lindex $cutspace2rule $i]
	} else {
	    set cutspacex [lindex $cutspacerule $i]
	}
	if {$lnycuts > 3} {
	    set cutspacey [lindex $cutspace2rule $i]
	} else {
	    set cutspacey [lindex $cutspacerule $i]
	}

	set lviawidth [+ [* $lnxcuts $cutsize] [* [- $lnxcuts 1] $cutspacex] $cutborder]
	set lviaheight [+ [* $lnycuts $cutsize] [* [- $lnycuts 1] $cutspacey] $cutborder]

	set viawidth [lreplace $viawidth $i $i $lviawidth]
	set viaheight [lreplace $viaheight $i $i $lviaheight]
    }

    # Determine the surrounding metal area needed on each layer
    # Do this both for the metal as the bottom layer of the via on top, and
    # the metal as the top layer of the via underneath.

    for {set i $metalbot} {$i <= $metaltop} {incr i} {
	set lorient [lindex $orient $i]
	set twidth 0
	set theight 0
	set bwidth 0
	set bheight 0
	if {$i > $metalbot} {
	    # Calculate minimum dimensions of metal surrounding the via below
	    set narrowoverlap [lindex $t0overlaprule [- $i 1]]
	    set wideoverlap [lindex $t1overlaprule [- $i 1]]
	    if {$lorient == "horizontal"} {
		set toverlapx $wideoverlap
		set toverlapy $narrowoverlap
	    } else {
		set toverlapx $narrowoverlap
		set toverlapy $wideoverlap
	    }
	    # Find the total minimum X and Y extents of metal
	    set lviawidth [lindex $viawidth [- $i 1]]
	    set lviaheight [lindex $viaheight [- $i 1]]
	    set twidth [+ $lviawidth [* 2 $toverlapx]]
	    set theight [+ $lviaheight [* 2 $toverlapy]]
	}
	if {$i < $metaltop} {
	    # Calculate minimum dimensions of metal surrounding the via above
	    set narrowoverlap [lindex $b0overlaprule $i]
	    set wideoverlap [lindex $b1overlaprule $i]
	    if {$lorient == "horizontal"} {
		set boverlapx $wideoverlap
		set boverlapy $narrowoverlap
	    } else {
		set boverlapx $narrowoverlap
		set boverlapy $wideoverlap
	    }
	    # Find the total minimum X and Y extents of metal
	    set lviawidth [lindex $viawidth $i]
	    set lviaheight [lindex $viaheight $i]
	    set bwidth [+ $lviawidth [* 2 $boverlapx]]
	    set bheight [+ $lviaheight [* 2 $boverlapy]]
	}
	# Actual width and height are the greater of the two measurements
	if {$twidth > $bwidth} {set lmetalwidth $twidth} {set lmetalwidth $bwidth}
	if {$theight > $bheight} {set lmetalheight $theight} {set lmetalheight $bheight}
	
	# Ensure that minimum metal width rule is satisfied in both directions
	set minmetalwidth [lindex $metalwidthrule $i]
	if {$lmetalwidth < $minmetalwidth} {set lmetalwidth $minmetalwidth}
	if {$lmetalheight < $minmetalwidth} {set lmetalheight $minmetalwidth}

	set metalwidth [lreplace $metalwidth $i $i $lmetalwidth]
	set metalheight [lreplace $metalheight $i $i $lmetalheight]
    }

    # puts stdout "Diagnostic 1:  metalwidth = $metalwidth   metalheight = $metalheight" 

    # For each internal metal, make sure that minimum metal area
    # rule is satisfied.  It is assumed that the top and bottom layers
    # of a stack will be routed to, and so do not need to meet the
    # minimum area requirement within this cell.

    for {set i [+ $metalbot 1]} {$i < $metaltop} {incr i} {
	set lmetalwidth [lindex $metalwidth $i]
	set lmetalheight [lindex $metalheight $i]
	set metalarea [* $lmetalwidth $lmetalheight]
	set minmetalarea [lindex $metalarearule $i]
	if {$metalarea < $minmetalarea} {
	    set lorient [lindex $orient $i]
	    if {$lorient == "horizontal"} {
		set lmetalwidth [/ $minmetalarea $lmetalheight]
		set metalwidth [lreplace $metalwidth $i $i $lmetalwidth]
	    } else {
		set lmetalheight [/ $minmetalarea $lmetalwidth]
		set metalheight [lreplace $metalheight $i $i $lmetalheight]
	    }
	}
    }

    # puts stdout "Diagnostic 2:  metalwidth = $metalwidth   metalheight = $metalheight" 

    # For each metal layer, paint the metal and contact
    snap internal
    for {set i $metalbot} {$i <= $metaltop} {incr i} {
	set lmetalwidth [lindex $metalwidth $i]
	set lmetalheight [lindex $metalheight $i]
	set hmetalwidth [/ $lmetalwidth 2.0]
	set hmetalheight [/ $lmetalheight 2.0]
	box values -${hmetalwidth}um -${hmetalheight}um ${hmetalwidth}um ${hmetalheight}um
	paint metal[+ $i 1]

	if {$i < $metaltop} {
	    set lviawidth [lindex $viawidth $i]
	    set lviaheight [lindex $viaheight $i]
	    set hviawidth [/ $lviawidth 2.0]
	    set hviaheight [/ $lviaheight 2.0]
	    box values -${hviawidth}um -${hviaheight}um ${hviawidth}um ${hviaheight}um
	    paint via[+ $i 1]
	}
    }
    # resumeall
}

#-----------------------------------------------------------------
# The specific via-drawing routines below are deprecated in favor
# of the via stack method above.  However, they are still useful
# for drawing a via directly into a layout rather than creating a
# subcell, and are used by most of the device generators.  Note
# that "dir" is the orientation of the via bottom layer, which is
# the opposite sense used by "draw_contact".
#
# If "layers" is set to 1, then draw only the via and top metal.
# This is useful when drawing vias on top of contacts at device
# terminals.
#
# If "minarea" is non-zero, then ensure that the lower metal
# layer meets the specified minimum area.  This is done only on
# the lower metal on the assumption that the top metal will be
# wired to in the design, so the top metal does not need to meet
# minimum metal area in the device.
#-----------------------------------------------------------------

proc sg13g2::via1_draw {{dir default} {layers 2} {minarea 0}} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
   if {$w < 0.2} {
      puts stderr "Via1 width must be at least 0.2um"
      return
   }
   if {$h < 0.2} {
      puts stderr "Via1 height must be at least 0.2um"
      return
   }
   # Use width vs. height to define the "natural" orientation
   # This is probably not particularly useful.
   if {$dir == "default"} {
      if {$w < $h} {
	 set dir "vert"
      } else {
	 set dir "horz"
      }
   }
   suspendall
   paint via1
   if {$dir == "vert"} {
      pushbox
      box grow e 0.045um
      box grow w 0.045um
      paint m2
      popbox
      if {$layers > 1} {
         pushbox
         box grow c 0.005um
         box grow n 0.045um
         box grow s 0.045um
	 sg13g2::minareabox $minarea $dir
         paint m1
         popbox
      }
   } else {
      pushbox
      box grow n 0.045um
      box grow s 0.045um
      paint m2
      popbox
      if {$layers > 1} {
         pushbox
         box grow c 0.005um
         box grow e 0.045um
         box grow w 0.045um
	 sg13g2::minareabox $minarea $dir
         paint m1
         popbox
      }
   }
   resumeall
}

proc sg13g2::via2_draw {} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
   if {$w < 0.2} {
      puts stderr "Via2 width must be at least 0.2um"
      return
   }
   if {$h < 0.2} {
      puts stderr "Via2 height must be at least 0.2um"
      return
   }
   suspendall
   pushbox
   paint via2
   box grow n 0.045um
   box grow s 0.045um
   paint m2
   popbox
   pushbox
   box grow e 0.045um
   box grow w 0.045um
   paint m3
   popbox
   resumeall
}

proc sg13g2::via3_draw {} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
   if {$w < 0.2} {
      puts stderr "Via3 width must be at least 0.2um"
      return
   }
   if {$h < 0.2} {
      puts stderr "Via3 height must be at least 0.2um"
      return
   }
   suspendall
   pushbox
   paint via3
   box grow n 0.045um
   box grow s 0.045um
   paint m4
   popbox
   pushbox
   box grow e 0.045um
   box grow w 0.045um
   paint m3
   popbox
   resumeall
}

proc sg13g2::via4_draw {} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
   if {$w < 0.2} {
      puts stderr "Via4 width must be at least 0.2um"
      return
   }
   if {$h < 0.2} {
      puts stderr "Via4 height must be at least 0.2um"
      return
   }
   suspendall
   pushbox
   paint via4
   box grow n 0.045um
   box grow s 0.045um
   paint m5
   popbox
   pushbox
   box grow e 0.045um
   box grow w 0.045um
   paint m4
   popbox
   resumeall
}

proc sg13g2::via5_draw {} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
   if {$w < 0.62} {
      puts stderr "Via5 width must be at least 0.62um"
      return
   }
   if {$h < 0.62} {
      puts stderr "Via5 height must be at least 0.62um"
      return
   }
   suspendall
   paint via5
   pushbox
   box grow c 0.32um
   paint m6
   popbox
   resumeall
}

proc sg13g2::via6_draw {} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
   if {$w < 1.90} {
      puts stderr "Via6 width must be at least 1.90um"
      return
   }
   if {$h < 1.90} {
      puts stderr "Via6 height must be at least 1.90um"
      return
   }
   suspendall
   paint via6
   paint m7
   resumeall
}

#----------------------------------------------------------------
