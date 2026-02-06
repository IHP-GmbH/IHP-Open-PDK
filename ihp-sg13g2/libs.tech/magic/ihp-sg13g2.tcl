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

#-----------------------------------------------------
# Magic/TCL design kit for IHP ihp-sg13g2
#-----------------------------------------------------
# Tim Edwards
# Revision 1.0	November 3, 2025
#-----------------------------------------------------
#
# Devices in the model files, with notes about
# implementation as generated devices in magic:
#
# Capacitors:
#
# cap_cmim	(basic MiM cap, L and W, contact options)
# cap_rfcmim	(cmim with RF option; draws guard ring under the device, feed width)
#
# Diodes:
#
# dantenna	(basic n-diode, L and W)
# dpantenna	(basic p-diode, L and W)
#
# Resistors:
#
# rsil		(low-R silicided poly resistor, L and W)
# rppd		(medium-R P+ unsalicided poly resistor, L and W)
# rhigh		(high-R N- unsalicided poly resistor, L and W)
#
# Bipolars:
#
# npn13g2	(bipolar, emitter L and W)
# npn13g2l	(bipolar, emitter L and W)
# npn13g2v	(bipolar, emitter L and W)
# pnpMPA	(bipolar, emitter L and W)
#
# MOSFETs:
#
# sg13_hv_nmos	(mosfet, channel L and W, NF, M, RF option)
# sg13_hv_pmos	(mosfet, channel L and W, NF, M, RF option)
# sg13_lv_nmos	(mosfet, channel L and W, NF, M, RF option)
# sg13_lv_pmos	(mosfet, channel L and W, NF, M, RF option)
#
# Varactors:
#
# SVaricap	(macro with two sg13_hv_svaricap devices)
# sg13_hv_svaricap (varactor, L and W, M)
#
# Fixed-layout devices:
#
# diodevdd_2kv	(fixed layout, array options only)
# diodevdd_4kv	(fixed layout, array options only)
# diodevss_2kv	(fixed layout, array options only)
# diodevss_4kv	(fixed layout, array options only)
# nmoscl_2	(clamp mosfet, fixed layout)
# nmoscl_4	(clamp mosfet, fixed layout)
# scr1		(silicon rectifier, fixed layout)
#
# Miscellaneous:
#
# bondpad	(octagon or square, bond or probe, diameter)
# isolbox	(deep nwell area, length and width)
# inductor	(2-terminal, width, spacing, diameter, windings)
# balun		(3-terminal, width, spacing, diameter, windings)
# seal ring	(length and width)

# Devices not part of the device generator:
# cparasitic	(device model for parasitic capacitance)
# Rparasitic	(device model for parasitic resistance)
# npn13g2_5t	(bipolar, emitter L and W, nonphysical 5th terminal)
# npn13g2l_5t	(bipolar, emitter L and W, nonphysical 5th terminal)
# npn13g2v_5t	(bipolar, emitter L and W, nonphysical 5th terminal)
# ptap1		(p-tap contact, treated as resistor device, L and W)
# ntap1		(n-tap contact, treated as resistor device, L and W)

if {[catch {set TECHPATH $env(PDK_ROOT)}]} {
    set TECHPATH /usr/share/pdk
}
if [catch {set PDKPATH}] {set PDKPATH ${TECHPATH}/ihp-sg13g2}
set PDKNAME ihp-sg13g2
# "sg13g2" is the namespace used for all devices
set PDKNAMESPACE sg13g2
puts stdout "Loading ihp-sg13g2 Device Generator Menu ..."

# Initialize toolkit menus to the wrapper window

global Opts
namespace eval sg13g2 {}

# Set the window callback
if [catch {set Opts(callback)}] {set Opts(callback) ""}
set Opts(callback) [subst {sg13g2::addtechmenu \$framename; $Opts(callback)}]

# if {![info exists Opts(cmdentry)]} {set Opts(cmdentry) 1}

# Set options specific to this PDK
set Opts(hidelocked) 1
set Opts(hidespecial) 0

# Wrap the closewrapper procedure so that closing the last
# window is equivalent to quitting.
if {[info commands closewrapper] == "closewrapper"} {
   rename closewrapper closewrapperonly
   proc closewrapper { framename } {
      if {[llength [windownames all]] <= 1} {
         magic::quit
      } else {
         closewrapperonly $framename
      }
   }
}

# Remove maze router layers from the toolbar by locking them
catch {tech lock fence,magnet,rotate}

namespace eval sg13g2 {
    namespace path {::tcl::mathop ::tcl::mathfunc}

    set ruleset [dict create]

    # Process DRC rules (magic style)

    dict set ruleset poly_surround    0.07      ;# Poly surrounds contact
    dict set ruleset diff_surround    0.07      ;# Diffusion surrounds contact
    dict set ruleset gate_to_diffcont 0.19      ;# Gate to diffusion contact center
    dict set ruleset gate_to_polycont 0.22      ;# Gate to poly contact center
    dict set ruleset gate_extension   0.18      ;# Poly extension beyond gate
    dict set ruleset diff_extension   0.18      ;# Diffusion extension beyond gate
    dict set ruleset contact_size     0.16      ;# Minimum contact size
    dict set ruleset via_size         0.20      ;# Minimum via size
    dict set ruleset metal_surround   0.05      ;# Metal 1 exension over contact
    dict set ruleset sub_surround     0.31      ;# Sub/well surrounds diffusion
    dict set ruleset diff_spacing     0.21      ;# Diffusion spacing rule
    dict set ruleset poly_spacing     0.18      ;# Poly spacing rule
    dict set ruleset diff_poly_space  0.07      ;# Diffusion to poly spacing rule
    dict set ruleset diff_gate_space  0.07      ;# Diffusion to gate poly spacing rule
    dict set ruleset metal_spacing    0.18      ;# Metal 1 spacing rule
    dict set ruleset mmetal_spacing   0.21      ;# Metal spacing rule (metal 2 to 5)
    dict set ruleset res_to_cont      0.20      ;# resistor to contact center
    dict set ruleset res_diff_spacing 0.18      ;# resistor to guard ring
}

#-----------------------------------------------------
# magic::addtechmenu
#-----------------------------------------------------

proc sg13g2::addtechmenu {framename} {
   global Winopts Opts
   
   # Check for difference between magic 8.1.125 and earlier, and 8.1.126 and later
   if {[catch {${framename}.titlebar cget -height}]} {
      set layoutframe ${framename}.pane.top
   } else {
      set layoutframe ${framename}
   }

   # List of devices is long.  Divide into two sections for active and passive deivces
   magic::add_toolkit_menu $layoutframe "Devices" pdk1

   magic::add_toolkit_command $layoutframe "nmos (MOSFET)" \
	    "magic::gencell sg13g2::sg13_lv_nmos" pdk1
   magic::add_toolkit_command $layoutframe "pmos (MOSFET)" \
	    "magic::gencell sg13g2::sg13_lv_pmos" pdk1
   magic::add_toolkit_command $layoutframe "RF nmos (MOSFET)" \
	    "magic::gencell sg13g2::sg13_lv_rfnmos" pdk1
   magic::add_toolkit_command $layoutframe "RF pmos (MOSFET)" \
	    "magic::gencell sg13g2::sg13_lv_rfpmos" pdk1

   magic::add_toolkit_separator	$layoutframe pdk1
   magic::add_toolkit_command $layoutframe "n-diode" \
	    "magic::gencell sg13g2::dantenna" pdk1
   magic::add_toolkit_command $layoutframe "p-diode" \
	    "magic::gencell sg13g2::dpantenna" pdk1
   magic::add_toolkit_command $layoutframe "schottky" \
	    "magic::gencell sg13g2::schottky_nbl1" pdk1
   magic::add_toolkit_separator	$layoutframe pdk1

   magic::add_toolkit_command $layoutframe "NPN" \
	    "magic::gencell sg13g2::npn13g2" pdk1
   magic::add_toolkit_command $layoutframe "PNP" \
	    "magic::gencell sg13g2::pnpMPA" pdk1
   magic::add_toolkit_separator	$layoutframe pdk1

   magic::add_toolkit_command $layoutframe "poly resistor - 7 Ohm/sq" \
	    "magic::gencell sg13g2::rsil" pdk1
   magic::add_toolkit_command $layoutframe "poly resistor - 260 Ohm/sq" \
	    "magic::gencell sg13g2::rppd" pdk1
   magic::add_toolkit_command $layoutframe "poly resistor - 1360 Ohm/sq" \
	    "magic::gencell sg13g2::rhigh" pdk1
   magic::add_toolkit_command $layoutframe "metal resistor" \
	    "magic::gencell sg13g2::rm1" pdk1
   magic::add_toolkit_separator	$layoutframe pdk1

   magic::add_toolkit_command $layoutframe "MiM cap - 1.5fF/um^2" \
	    "magic::gencell sg13g2::cap_cmim" pdk1
   magic::add_toolkit_separator	$layoutframe pdk1

   magic::add_toolkit_command $layoutframe "substrate contact (1.8V)" \
	    "sg13g2::subconn_draw" pdk1
   magic::add_toolkit_command $layoutframe "substrate guard ring (1.8V)" \
	    "sg13g2::subconn_guard_draw" pdk1
   magic::add_toolkit_command $layoutframe "substrate contact (5.0V)" \
	    "sg13g2::hvsubconn_draw" pdk1
   magic::add_toolkit_command $layoutframe "substrate guard ring (5.0V)" \
	    "sg13g2::hvsubconn_guard_draw" pdk1
   magic::add_toolkit_command $layoutframe "n-well region with guard ring (1.8V)" \
	    "sg13g2::nwell_draw" pdk1
   magic::add_toolkit_command $layoutframe "n-well region with guard ring (5.0V)" \
	    "sg13g2::hvnwell_draw" pdk1
   magic::add_toolkit_command $layoutframe "deep n-well region (1.8V)" \
	    "sg13g2::deep_nwell_draw" pdk1
   magic::add_toolkit_command $layoutframe "deep n-well region (5.0V)" \
	    "sg13g2::hvdeep_nwell_draw" pdk1
   # magic::add_toolkit_command $layoutframe "via1" \
   #	    "sg13g2::via1_draw" pdk1
   # magic::add_toolkit_command $layoutframe "via2" \
   #	    "sg13g2::via2_draw" pdk1
   # magic::add_toolkit_command $layoutframe "via3" \
   #	    "sg13g2::via3_draw" pdk1
   # magic::add_toolkit_command $layoutframe "via4" \
   #	    "sg13g2::via4_draw" pdk1
   # magic::add_toolkit_command $layoutframe "via5" \
   #	    "sg13g2::via5_draw" pdk1
   # magic::add_toolkit_command $layoutframe "via6" \
   #	    "sg13g2::via6_draw" pdk1
   magic::add_toolkit_command $layoutframe "via stack" \
	    "magic::gencell sg13g2::via" pdk1
   magic::add_toolkit_separator	$layoutframe pdk1

   magic::add_toolkit_command $layoutframe "ESD diode" \
	    "magic::gencell sg13g2::diodevdd_2kv" pdk1
   magic::add_toolkit_command $layoutframe "nMOS clamp" \
	    "magic::gencell sg13g2::nmoscl_2" pdk1
   magic::add_toolkit_command $layoutframe "silicon-controlled rectifier" \
	    "magic::gencell sg13g2::scr1" pdk1
   magic::add_toolkit_separator	$layoutframe pdk1

   magic::add_toolkit_command $layoutframe "Varactor" \
	    "magic::gencell sg13g2::SVaricap" pdk1
   magic::add_toolkit_separator	$layoutframe pdk1

   magic::add_toolkit_command $layoutframe "Inductor" \
	    "magic::gencell sg13g2::inductor2" pdk1
   magic::add_toolkit_separator	$layoutframe pdk1

   magic::add_toolkit_command $layoutframe "Bond pad" \
	    "magic::gencell sg13g2::bondpad" pdk1

   # Additional DRC style for routing only---add this to the DRC menu
   ${layoutframe}.titlebar.mbuttons.drc.toolmenu add command -label "DRC Routing" -command {drc style drc(routing)}

   # Add SPICE import function to File menu
   ${layoutframe}.titlebar.mbuttons.file.toolmenu insert 4 command -label "Import SPICE" -command {sg13g2::importspice}
   ${layoutframe}.titlebar.mbuttons.file.toolmenu insert 4 separator

   # Add command entry window by default if enabled
   if {[info exists Opts(cmdentry)]} {
      set Winopts(${framename},cmdentry) $Opts(cmdentry)
   } else {
      set Winopts(${framename},cmdentry) 0
   }
   if {$Winopts(${framename},cmdentry) == 1} {
      addcommandentry $framename
   }
}

#----------------------------------------------------------------
# Source the various files for the device generator
#----------------------------------------------------------------

set script_file [info script]
set script_path [file dirname $script_file]
source ${script_path}/ihp-sg13g2-util.tcl	;# basic utility functions
source ${script_path}/ihp-sg13g2-misc.tcl	;# isolbox and tap rings
source ${script_path}/ihp-sg13g2-via.tcl	;# via stacks
source ${script_path}/ihp-sg13g2-fet.tcl	;# MOSFETs
source ${script_path}/ihp-sg13g2-cap.tcl	;# Capacitors
source ${script_path}/ihp-sg13g2-res.tcl	;# Resistors
source ${script_path}/ihp-sg13g2-bjt.tcl	;# Bipolar transistors
source ${script_path}/ihp-sg13g2-dio.tcl	;# Diodes
source ${script_path}/ihp-sg13g2-fix.tcl	;# ESD, clamps, SCR
source ${script_path}/ihp-sg13g2-var.tcl	;# Varactor
source ${script_path}/ihp-sg13g2-ind.tcl	;# Inductors
source ${script_path}/ihp-sg13g2-pad.tcl	;# Bond pad

# Make the script path available to procedures
set sg13g2::script_path ${script_path}

#----------------------------------------------------------------
