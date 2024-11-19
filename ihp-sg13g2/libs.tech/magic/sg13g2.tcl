#-----------------------------------------------------
# Magic/TCL design kit for IHP sg13g2
#-----------------------------------------------------
# Tim Edwards
# Revision 0.1	ALPHA   8/27/2024
# Currently a work in progress, migrating from sky130.
#-----------------------------------------------------

if {[catch {set TECHPATH $env(PDK_ROOT)}]} {
    set TECHPATH /usr/share/pdk
}
if [catch {set PDKPATH}] {set PDKPATH ${TECHPATH}/sg13g2A}
set PDKNAME sg13g2
# "sg13g2" is the namespace used for all devices
set PDKNAMESPACE sg13g2
puts stdout "Loading sg13g2 Device Generator Menu ..."

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

    dict set ruleset poly_surround    0.08      ;# Poly surrounds contact
    dict set ruleset diff_surround    0.06      ;# Diffusion surrounds contact
    dict set ruleset gate_to_diffcont 0.145     ;# Gate to diffusion contact center
    dict set ruleset gate_to_polycont 0.275     ;# Gate to poly contact center
    dict set ruleset gate_extension   0.13      ;# Poly extension beyond gate
    dict set ruleset diff_extension   0.29      ;# Diffusion extension beyond gate
    dict set ruleset contact_size     0.17      ;# Minimum contact size
    dict set ruleset via_size         0.17      ;# Minimum via size
    dict set ruleset metal_surround   0.08      ;# Local interconnect overlaps contact
    dict set ruleset sub_surround     0.18      ;# Sub/well surrounds diffusion
    dict set ruleset diff_spacing     0.28      ;# Diffusion spacing rule
    dict set ruleset poly_spacing     0.21      ;# Poly spacing rule
    dict set ruleset diff_poly_space  0.075     ;# Diffusion to poly spacing rule
    dict set ruleset diff_gate_space  0.20      ;# Diffusion to gate poly spacing rule
    dict set ruleset metal_spacing    0.23      ;# Local interconnect spacing rule
    dict set ruleset mmetal_spacing   0.14      ;# Metal spacing rule (above local interconnect)
    dict set ruleset res_to_cont      0.20      ;# resistor to contact center
    dict set ruleset res_diff_spacing 0.20      ;# resistor to guard ring
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
   magic::add_toolkit_menu $layoutframe "Devices 1" pdk1

   magic::add_toolkit_command $layoutframe "nmos (MOSFET)" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__nfet_01v8" pdk1
   magic::add_toolkit_command $layoutframe "pmos (MOSFET)" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__pfet_01v8" pdk1

   magic::add_toolkit_separator	$layoutframe pdk1
   magic::add_toolkit_command $layoutframe "LDNMOS (extended drain)" \
   	    "magic::gencell sg13g2::sg13g2_fd_pr__nfet_g5v0d16v0" pdk1
   magic::add_toolkit_command $layoutframe "LDPMOS (extended drain)" \
   	    "magic::gencell sg13g2::sg13g2_fd_pr__pfet_g5v0d16v0" pdk1

   magic::add_toolkit_separator	$layoutframe pdk1
   magic::add_toolkit_command $layoutframe "n-diode" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__diode_pw2nd_05v5" pdk1
   magic::add_toolkit_command $layoutframe "p-diode" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__diode_pd2nw_05v5" pdk1
   magic::add_toolkit_command $layoutframe "photodiode" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__photodiode" pdk1

   magic::add_toolkit_separator	$layoutframe pdk1
   magic::add_toolkit_command $layoutframe "MOS varactor" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__cap_var_lvt" pdk1
   magic::add_toolkit_separator	$layoutframe pdk1

   magic::add_toolkit_command $layoutframe "NPN 1.0 x 1.0" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__npn_05v5_W1p00L1p00" pdk1
   magic::add_toolkit_command $layoutframe "NPN 1.0 x 2.0" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__npn_05v5_W1p00L2p00" pdk1
   magic::add_toolkit_command $layoutframe "PNP 0.68 x 0.68" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__pnp_05v5_W0p68L0p68" pdk1
   magic::add_toolkit_command $layoutframe "PNP 3.4 x 3.4" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__pnp_05v5_W3p40L3p40" pdk1
   magic::add_toolkit_command $layoutframe "NPN 11V 1.0 x 1.0" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__npn_11v0_W1p00L1p00" pdk1

   magic::add_toolkit_separator	$layoutframe pdk1

   magic::add_toolkit_command $layoutframe "inductor 1" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__rf_test_coil1" pdk1
   magic::add_toolkit_command $layoutframe "inductor 2" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__rf_test_coil2" pdk1
   magic::add_toolkit_command $layoutframe "inductor 3" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__rf_test_coil3" pdk1

   magic::add_toolkit_separator	$layoutframe pdk1

   magic::add_toolkit_command $layoutframe "substrate contact (1.8V)" \
	    "sg13g2::subconn_draw" pdk1
   magic::add_toolkit_command $layoutframe "substrate guard ring (1.8V)" \
	    "sg13g2::subconn_guard_draw" pdk1
   magic::add_toolkit_command $layoutframe "substrate contact (5.0V)" \
	    "sg13g2::mvsubconn_draw" pdk1
   magic::add_toolkit_command $layoutframe "substrate guard ring (5.0V)" \
	    "sg13g2::mvsubconn_guard_draw" pdk1
   magic::add_toolkit_command $layoutframe "deep n-well region (1.8V)" \
	    "sg13g2::deep_nwell_draw" pdk1
   magic::add_toolkit_command $layoutframe "deep n-well region (5.0V)" \
	    "sg13g2::mvdeep_nwell_draw" pdk1
   magic::add_toolkit_command $layoutframe "n-well region with guard ring (1.8V)" \
	    "sg13g2::nwell_draw" pdk1
   magic::add_toolkit_command $layoutframe "n-well region with guard ring (5.0V)" \
	    "sg13g2::mvnwell_draw" pdk1
   magic::add_toolkit_command $layoutframe "mcon" \
	    "sg13g2::mcon_draw" pdk1
   magic::add_toolkit_command $layoutframe "via1" \
	    "sg13g2::via1_draw" pdk1
   magic::add_toolkit_command $layoutframe "via2" \
	    "sg13g2::via2_draw" pdk1
   magic::add_toolkit_command $layoutframe "via3" \
	    "sg13g2::via3_draw" pdk1
   magic::add_toolkit_command $layoutframe "via4" \
	    "sg13g2::via4_draw" pdk1
   

   magic::add_toolkit_menu $layoutframe "Devices 2" pdk2

   magic::add_toolkit_command $layoutframe "n-diff resistor (1.8V) - 120 Ohm/sq" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__res_generic_nd" pdk2
   magic::add_toolkit_command $layoutframe "p-diff resistor (1.8V) - 197 Ohm/sq" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__res_generic_pd" pdk2
   magic::add_toolkit_command $layoutframe "n-diff resistor (5.0V) - 114 Ohm/sq" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__res_generic_nd__hv" pdk2
   magic::add_toolkit_command $layoutframe "p-diff resistor (5.0V) - 191 Ohm/sq" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__res_generic_pd__hv" pdk2

   magic::add_toolkit_command $layoutframe "poly resistor - 48.2 Ohm/sq" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__res_generic_po" pdk2
   magic::add_toolkit_command $layoutframe "poly resistor - 319.8 Ohm/sq" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__res_high_po_0p35" pdk2
   magic::add_toolkit_command $layoutframe "poly resistor - 2000 Ohm/sq" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__res_xhigh_po_0p35" pdk2
   magic::add_toolkit_command $layoutframe "p-well resistor - 3050 Ohm/sq" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__res_iso_pw" pdk2
   magic::add_toolkit_separator	$layoutframe pdk2

   magic::add_toolkit_command $layoutframe "l1 metal resistor - 12.2 Ohm/sq" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__res_generic_l1" pdk2
   magic::add_toolkit_command $layoutframe "m1 metal resistor - 125 mOhm/sq" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__res_generic_m1" pdk2
   magic::add_toolkit_command $layoutframe "m2 metal resistor - 125 mOhm/sq" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__res_generic_m2" pdk2
   magic::add_toolkit_command $layoutframe "m3 metal resistor - 47 mOhm/sq" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__res_generic_m3" pdk2
   magic::add_toolkit_command $layoutframe "m4 metal resistor - 47 mOhm/sq" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__res_generic_m4" pdk2
   magic::add_toolkit_command $layoutframe "m5 metal resistor - 29 mOhm/sq" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__res_generic_m5" pdk2

   magic::add_toolkit_command $layoutframe "MiM cap - 2fF/um^2 (metal3)" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__cap_mim_m3_1" pdk2
   magic::add_toolkit_command $layoutframe "MiM cap - 2fF/um^2 (metal4)" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__cap_mim_m3_2" pdk2
   magic::add_toolkit_separator	$layoutframe pdk2

   magic::add_toolkit_command $layoutframe "vpp 11.5x11.7 m1-m4, li/m5 shield" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__cap_vpp_11p5x11p7_m1m2m3m4_shieldl1m5" pdk2
   magic::add_toolkit_command $layoutframe "vpp 11.5x11.7 m1-m2" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__cap_vpp_11p5x11p7_m1m2_noshield" pdk2
   magic::add_toolkit_command $layoutframe "vpp 8.6x7.8 m1-m2 l1 shield" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__cap_vpp_08p6x07p8_m1m2_shieldl1" pdk2
   magic::add_toolkit_command $layoutframe "vpp 4.4x4.6 m1-m2 l1 shield" \
	    "magic::gencell sg13g2::sg13g2_fd_pr__cap_vpp_04p4x04p6_m1m2_shieldl1" pdk2

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
# Menu callback function to read a SPICE netlist and generate an
# initial layout using the SKYWATER sg13g2A gencells.
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

proc sg13g2::mcon_draw {{dir default}} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
   if {$w < 0.17} {
      puts stderr "Mcon width must be at least 0.17um"
      return
   }
   if {$h < 0.17} {
      puts stderr "Mcon height must be at least 0.17um"
      return
   }
   suspendall
   paint mcon
   pushbox
   if {($w < $h) || ($dir == "vert")} {
       box grow e 0.03um
       box grow w 0.03um
       box grow n 0.06um
       box grow s 0.06um
       paint m1
   } else {
       box grow n 0.03um
       box grow s 0.03um
       box grow e 0.06um
       box grow w 0.06um
       paint m1
   }
   popbox
   resumeall
}

proc sg13g2::via1_draw {} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
   if {$w < 0.26} {
      puts stderr "Via1 width must be at least 0.26um"
      return
   }
   if {$h < 0.26} {
      puts stderr "Via1 height must be at least 0.26um"
      return
   }
   suspendall
   paint via1
   box grow n 0.05um
   box grow s 0.05um
   paint m2
   box grow n -0.05um
   box grow s -0.05um
   box grow e 0.05um
   box grow w 0.05um
   paint m1
   box grow e -0.05um
   box grow w -0.05um
   resumeall
}

proc sg13g2::via2_draw {} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
   if {$w < 0.28} {
      puts stderr "Via2 width must be at least 0.28um"
      return
   }
   if {$h < 0.28} {
      puts stderr "Via2 height must be at least 0.28um"
      return
   }
   suspendall
   pushbox
   paint via2
   box grow n 0.05um
   box grow s 0.05um
   paint m2
   popbox
   pushbox
   box grow n 0.025um
   box grow s 0.025um
   box grow e 0.05um
   box grow w 0.05um
   paint m3
   popbox
   resumeall
}

proc sg13g2::via3_draw {} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
   if {$w < 0.32} {
      puts stderr "Via3 width must be at least 0.32um"
      return
   }
   if {$h < 0.32} {
      puts stderr "Via3 height must be at least 0.32um"
      return
   }
   suspendall
   pushbox
   paint via3
   box grow n 0.005um
   box grow s 0.005um
   box grow e 0.005um
   box grow w 0.005um
   paint m4
   popbox
   pushbox
   box grow e 0.05um
   box grow w 0.05um
   paint m3
   popbox
   resumeall
}

proc sg13g2::via4_draw {} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
   if {$w < 1.18} {
      puts stderr "Via3 width must be at least 1.18um"
      return
   }
   if {$h < 1.18} {
      puts stderr "Via3 height must be at least 1.18um"
      return
   }
   suspendall
   paint via4
   pushbox
   box grow n 0.12um
   box grow s 0.12um
   box grow e 0.12um
   box grow w 0.12um
   paint m5
   popbox
   resumeall
}

proc sg13g2::subconn_draw {} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
   if {$w < 0.17} {
      puts stderr "Substrate tap width must be at least 0.17um"
      return
   }
   if {$h < 0.17} {
      puts stderr "Substrate tap height must be at least 0.17um"
      return
   }
   suspendall
   paint psc
   pushbox
   if {$w > $h} {
      box grow e 0.08um
      box grow w 0.08um
      paint li
      box grow e 0.04um
      box grow w 0.04um
   } else {
      box grow n 0.08um
      box grow s 0.08um
      paint li
      box grow n 0.04um
      box grow s 0.04um
   }
   paint psd
   popbox
   resumeall
}

#----------------------------------------------------------------

proc sg13g2::mvsubconn_draw {} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
   if {$w < 0.17} {
      puts stderr "Substrate tap width must be at least 0.17um"
      return
   }
   if {$h < 0.17} {
      puts stderr "Substrate tap height must be at least 0.17um"
      return
   }
   suspendall
   paint mvpsc
   pushbox
   if {$w > $h} {
      box grow e 0.08um
      box grow w 0.08um
      paint li
      box grow e 0.04um
      box grow w 0.04um
   } else {
      box grow n 0.08um
      box grow s 0.08um
      paint li
      box grow n 0.04um
      box grow s 0.04um
   }
   paint mvpsd
   popbox
   resumeall
}

#----------------------------------------------------------------
# Helper function for drawing guard rings.
# Assumes that a box exists and defines the centerlines of the
# guard ring contacts.
# ctype = type to paint for contact
# dtype = type to paint for diffusion
#----------------------------------------------------------------

proc sg13g2::guard_ring_draw {ctype dtype} {
   pushbox
   box width 0
   box grow c 0.085um
   paint li
   pushbox
   box grow n -0.3um
   box grow s -0.3um
   paint $ctype
   popbox
   paint $dtype
   popbox

   pushbox
   box height 0
   box grow c 0.085um
   paint li
   pushbox
   box grow e -0.3um
   box grow w -0.3um
   paint $ctype
   popbox
   paint $dtype
   popbox

   pushbox
   box move n [box height]i
   box height 0
   box grow c 0.085um
   paint li
   pushbox
   box grow e -0.3um
   box grow w -0.3um
   paint $ctype
   popbox
   paint $dtype
   popbox

   pushbox
   box move e [box width]i
   box width 0
   box grow c 0.085um
   paint li
   pushbox
   box grow n -0.3um
   box grow s -0.3um
   paint $ctype
   popbox
   paint $dtype
   popbox
}

#----------------------------------------------------------------

proc sg13g2::subconn_guard_draw {} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
   # NOTE:  Width and height are determined by the requirement for
   # a contact on each side.  There is not much that can be done
   # with an guarded nwell smaller than that, anyway.
   if {$w < 0.6} {
      puts stderr "Substrate guard ring width must be at least 0.6um"
      return
   }
   if {$h < 0.6} {
      puts stderr "Substrate guard ring height must be at least 0.6um"
      return
   }
   suspendall
   tech unlock *
   pushbox

   sg13g2::guard_ring_draw psc psd

   popbox
   tech revert
   resumeall
}

#----------------------------------------------------------------

proc sg13g2::mvsubconn_guard_draw {} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
   # NOTE:  Width and height are determined by the requirement for
   # a contact on each side.  There is not much that can be done
   # with an guarded nwell smaller than that, anyway.
   if {$w < 0.6} {
      puts stderr "Substrate guard ring width must be at least 0.6um"
      return
   }
   if {$h < 0.6} {
      puts stderr "Substrate guard ring height must be at least 0.6um"
      return
   }
   suspendall
   tech unlock *
   pushbox

   sg13g2::guard_ring_draw mvpsc mvpsd

   popbox
   tech revert
   resumeall
}

#----------------------------------------------------------------

proc sg13g2::nwell_draw {} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
   # NOTE:  Width and height are determined by the requirement for
   # a contact on each side.  There is not much that can be done
   # with an guarded nwell smaller than that, anyway.
   if {$w < 0.6} {
      puts stderr "N-well region width must be at least 0.6um"
      return
   }
   if {$h < 0.6} {
      puts stderr "N-well region height must be at least 0.6um"
      return
   }
   suspendall
   tech unlock *
   pushbox
   pushbox
   box grow c 0.265um
   paint nwell
   popbox

   sg13g2::guard_ring_draw nsc nsd

   popbox
   tech revert
   resumeall
}

#----------------------------------------------------------------

proc sg13g2::mvnwell_draw {} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
   # NOTE:  Width and height are determined by the requirement for
   # a contact on each side.  There is not much that can be done
   # with an guarded nwell smaller than that, anyway.
   if {$w < 0.6} {
      puts stderr "MV N-well region width must be at least 0.6um"
      return
   }
   if {$h < 0.6} {
      puts stderr "MV N-well region height must be at least 0.6um"
      return
   }
   suspendall
   tech unlock *
   pushbox
   pushbox
   box grow c 0.415um
   paint nwell
   popbox

   sg13g2::guard_ring_draw mvnsc mvnsd

   popbox
   tech revert
   resumeall
}

#----------------------------------------------------------------

proc sg13g2::deep_nwell_draw {} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
   if {$w < 3.0} {
      puts stderr "Deep-nwell region width must be at least 3.0um"
      return
   }
   if {$h < 3.0} {
      puts stderr "Deep-nwell region height must be at least 3.0um"
      return
   }
   suspendall
   tech unlock *
   paint dnwell
   pushbox
   pushbox
   box grow c 0.4um
   # Note:  Previous implementation was to draw nwell over the whole
   # area and then erase it from the center.  That can interact with
   # any layout already drawn in the center area.  Instead, draw four
   # separate rectangles.
   # -----------------
   # paint nwell
   # box grow c -1.43um
   # erase nwell
   # -----------------
   pushbox
   box width 1.43um
   paint nwell
   popbox
   pushbox
   box height 1.43um
   paint nwell
   popbox
   pushbox
   box move n ${h}um
   box move n 0.8um
   box move s 1.43um
   box height 1.43um
   paint nwell
   popbox
   pushbox
   box move e ${w}um
   box move e 0.8um
   box move w 1.43um
   box width 1.43um
   paint nwell
   popbox

   popbox
   box grow c 0.03um

   pushbox
   box width 0
   box grow c 0.085um
   paint li
   pushbox
   box grow n -0.3um
   box grow s -0.3um
   paint nsc
   popbox
   box grow c 0.1um
   paint nsd
   popbox

   pushbox
   box height 0
   box grow c 0.085um
   paint li
   pushbox
   box grow e -0.3um
   box grow w -0.3um
   paint nsc
   popbox
   box grow c 0.1um
   paint nsd
   popbox

   pushbox
   box move n [box height]i
   box height 0
   box grow c 0.085um
   paint li
   pushbox
   box grow e -0.3um
   box grow w -0.3um
   paint nsc
   popbox
   box grow c 0.1um
   paint nsd
   popbox

   pushbox
   box move e [box width]i
   box width 0
   box grow c 0.085um
   paint li
   pushbox
   box grow n -0.3um
   box grow s -0.3um
   paint nsc
   box grow c 0.1um
   paint nsd
   popbox

   popbox
   tech revert
   resumeall
}

#----------------------------------------------------------------

proc sg13g2::mvdeep_nwell_draw {} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
   if {$w < 3.0} {
      puts stderr "MV Deep-nwell region width must be at least 3.0um"
      return
   }
   if {$h < 3.0} {
      puts stderr "MV Deep-nwell region height must be at least 3.0um"
      return
   }
   suspendall
   tech unlock *
   paint dnwell
   pushbox
   pushbox
   box grow c 0.55um
   pushbox
   box width 1.58um
   paint nwell
   popbox
   pushbox
   box height 1.58um
   paint nwell
   popbox
   pushbox
   box move n ${h}um
   box move n 1.1um
   box move s 1.58um
   box height 1.58um
   paint nwell
   popbox
   pushbox
   box move e ${w}um
   box move e 1.1um
   box move w 1.58um
   box width 1.58um
   paint nwell
   popbox

   popbox
   box grow c 0.03um

   pushbox
   box width 0
   box grow c 0.085um
   paint li
   pushbox
   box grow n -0.3um
   box grow s -0.3um
   paint mvnsc
   popbox
   box grow c 0.1um
   paint mvnsd
   popbox

   pushbox
   box height 0
   box grow c 0.085um
   paint li
   pushbox
   box grow e -0.3um
   box grow w -0.3um
   paint mvnsc
   popbox
   box grow c 0.1um
   paint mvnsd
   popbox

   pushbox
   box move n [box height]i
   box height 0
   box grow c 0.085um
   paint li
   pushbox
   box grow e -0.3um
   box grow w -0.3um
   paint mvnsc
   popbox
   box grow c 0.1um
   paint mvnsd
   popbox

   pushbox
   box move e [box width]i
   box width 0
   box grow c 0.085um
   paint li
   pushbox
   box grow n -0.3um
   box grow s -0.3um
   paint mvnsc
   box grow c 0.1um
   paint mvnsd
   popbox

   popbox
   tech revert
   resumeall
}

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
# Drawn diode routines
#----------------------------------------------------------------

proc sg13g2::diode_recalc {field parameters} {
    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }
    switch  $field {
	area { puts stdout "area changed" }
	peri { puts stdout "perimeter changed" }
	w   { puts stdout "width changed" }
	l   { puts stdout "length changed" }
    }
    dict set parameters area $area
    dict set parameters peri $peri
    dict set parameters w $w
    dict set parameters l $l
}

#----------------------------------------------------------------
# diode: Conversion from SPICE netlist parameters to toolkit
#----------------------------------------------------------------

proc sg13g2::diode_convert {parameters} {
    set pdkparams [dict create]
    dict for {key value} $parameters {
	switch -nocase $key {
	    l -
	    w -
	    peri {
		# Length, width, and perimeter are converted to units of microns
		set value [magic::spice2float $value]
		# set value [expr $value * 1e6]
		set value [magic::3digitpastdecimal $value]
		dict set pdkparams [string tolower $key] $value
	    }
	    area {
		# area also converted to units of microns
		set value [magic::spice2float $value]
		# set value [expr $value * 1e12]
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

#----------------------------------------------------------------
# diode: Interactively specifies the fixed layout parameters
#----------------------------------------------------------------

proc sg13g2::diode_dialog {device parameters} {
    # Editable fields:      w, l, area, perim, nx, ny

    magic::add_entry area "Area (um^2)" $parameters
    magic::add_entry peri "Perimeter (um)" $parameters
    sg13g2::compute_aptot $parameters
    magic::add_message atot "Total area (um^2)" $parameters
    magic::add_message ptot "Total perimeter (um)" $parameters
    magic::add_entry l "Length (um)" $parameters
    magic::add_entry w "Width (um)" $parameters
    magic::add_entry nx "X Repeat" $parameters
    magic::add_entry ny "Y Repeat" $parameters

    if {[dict exists $parameters compatible]} {
       set sellist [dict get $parameters compatible]
       magic::add_selectlist gencell "Device type" $sellist $parameters $device
    }

    if {[dict exists $parameters doverlap]} {
	magic::add_checkbox doverlap "Overlap at end contact" $parameters
    }
    if {[dict exists $parameters elc]} {
        magic::add_checkbox elc "Add left end contact" $parameters
    }
    if {[dict exists $parameters erc]} {
        magic::add_checkbox erc "Add right end contact" $parameters
    }
    if {[dict exists $parameters etc]} {
        magic::add_checkbox etc "Add top end contact" $parameters
    }
    if {[dict exists $parameters ebc]} {
        magic::add_checkbox ebc "Add bottom end contact" $parameters
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

    if {[dict exists $parameters vias]} {
	magic::add_checkbox vias "Add vias over contacts" $parameters
    }

    magic::add_dependency sg13g2::diode_recalc $device sg13g2 l w area peri

    # magic::add_checkbox dummy "Add dummy" $parameters
}

#----------------------------------------------------------------
# Diode total area and perimeter computation
#----------------------------------------------------------------

proc sg13g2::compute_aptot {parameters} {
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }
    set area [magic::spice2float $area]
    set area [magic::3digitpastdecimal $area]
    set peri [magic::spice2float $peri]
    set peri [magic::3digitpastdecimal $peri]

    # Compute total area
    catch {set magic::atot_val [expr ($area * $nx * $ny)]}
    # Compute total perimeter
    catch {set magic::ptot_val [expr ($peri * $nx * $ny)]}
}

#----------------------------------------------------------------
# diode: Check device parameters for out-of-bounds values
#----------------------------------------------------------------

proc sg13g2::diode_check {parameters} {

    set guard 0
    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Normalize distance units to microns
    set l [magic::spice2float $l]
    set l [magic::3digitpastdecimal $l] 
    set w [magic::spice2float $w]
    set w [magic::3digitpastdecimal $w] 

    set area [magic::spice2float $area]
    set area [magic::3digitpastdecimal $area] 
    set peri [magic::spice2float $peri]
    set peri [magic::3digitpastdecimal $peri] 

    if {$l == 0} {
        # Calculate L from W and area
	set l [expr ($area / $w)]
	dict set parameters l [magic::float2spice $l]
    } elseif {$w == 0} {
        # Calculate W from L and area
	set w [expr ($area / $l)]
	dict set parameters w [magic::float2spice $w]
    }
    if {$w < $wmin} {
	puts stderr "Diode width must be >= $wmin"
	dict set parameters w $wmin
    } 
    if {$l < $lmin} {
	puts stderr "Diode length must be >= $lmin"
	dict set parameters l $lmin
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

    # Calculate area and perimeter from L and W
    set area [expr ($l * $w)]
    dict set parameters area [magic::float2spice $area]
    set peri [expr (2 * ($l + $w))]
    dict set parameters peri [magic::float2spice $peri]
    sg13g2::compute_aptot $parameters

    return $parameters
}

#------------------------------------------------------------------
# NOTE:  sg13g2_fd_pr__diode_pw2nd_05v5_lvt,
# sg13g2_fd_pr__diode_pw2nd_05v5_nvt, sg13g2_fd_pr__diode_pd2nw_05v5_lvt,
# and sg13g2_fd_pr__diode_pd2nw_11v0 are all considered parasitic diodes.
# They may be generated by invoking the build procedure on the
# command line.  To enable them in the PDK, add them to the
# appropriate compatible {} list.
#------------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__diode_pw2nd_05v5_defaults {} {
    return {w 0.45 l 0.45 area 0.2025 peri 1.8 \
	nx 1 ny 1 dummy 0 lmin 0.45 wmin 0.45 class diode \
	elc 1 erc 1 etc 1 ebc 1 doverlap 0 \
	compatible {sg13g2_fd_pr__diode_pw2nd_05v5 sg13g2_fd_pr__diode_pw2nd_05v5_lvt \
	sg13g2_fd_pr__diode_pw2nd_05v5_nvt sg13g2_fd_pr__diode_pw2nd_11v0} \
	full_metal 1 vias 1 viagb 0 viagt 0 viagl 0 viagr 0}
}

proc sg13g2::sg13g2_fd_pr__diode_pw2nd_05v5_lvt_defaults {} {
    return {w 0.45 l 0.45 area 0.2025 peri 1.8 \
	nx 1 ny 1 dummy 0 lmin 0.45 wmin 0.45 class diode \
	elc 1 erc 1 etc 1 ebc 1 doverlap 0 \
	compatible {sg13g2_fd_pr__diode_pw2nd_05v5 sg13g2_fd_pr__diode_pw2nd_05v5_lvt \
	sg13g2_fd_pr__diode_pw2nd_05v5_nvt sg13g2_fd_pr__diode_pw2nd_11v0} \
	full_metal 1 vias 1 viagb 0 viagt 0 viagl 0 viagr 0}
}

proc sg13g2::sg13g2_fd_pr__diode_pw2nd_05v5_nvt_defaults {} {
    return {w 0.45 l 0.45 area 0.2024 peri 1.8 \
	nx 1 ny 1 dummy 0 lmin 0.45 wmin 0.45 class diode \
	elc 1 erc 1 etc 1 ebc 1 doverlap 0 \
	compatible {sg13g2_fd_pr__diode_pw2nd_05v5 sg13g2_fd_pr__diode_pw2nd_05v5_lvt \
	sg13g2_fd_pr__diode_pw2nd_05v5_nvt sg13g2_fd_pr__diode_pw2nd_11v0} \
	full_metal 1 vias 1 viagb 0 viagt 0 viagl 0 viagr 0}
}

proc sg13g2::sg13g2_fd_pr__diode_pw2nd_11v0_defaults {} {
    return {w 0.45 l 0.45 area 0.2024 peri 1.8 \
	nx 1 ny 1 dummy 0 lmin 0.45 wmin 0.45 class diode \
	elc 1 erc 1 etc 1 ebc 1 doverlap 0 \
	compatible {sg13g2_fd_pr__diode_pw2nd_05v5 sg13g2_fd_pr__diode_pw2nd_05v5_lvt \
	sg13g2_fd_pr__diode_pw2nd_05v5_nvt sg13g2_fd_pr__diode_pw2nd_11v0} \
	full_metal 1 vias 1 viagb 0 viagt 0 viagl 0 viagr 0}
}

proc sg13g2::sg13g2_fd_pr__photodiode_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 xstep 8.0 ystep 8.0 class diode}
}

proc sg13g2::sg13g2_fd_pr__diode_pd2nw_05v5_defaults {} {
    return {w 0.45 l 0.45 area 0.2025 peri 1.8 \
	nx 1 ny 1 dummy 0 lmin 0.45 wmin 0.45 class diode \
	elc 1 erc 1 etc 1 ebc 1 \
	glc 1 grc 1 gtc 1 gbc 1 doverlap 0 \
	compatible {sg13g2_fd_pr__diode_pd2nw_05v5 sg13g2_fd_pr__diode_pd2nw_05v5_lvt \
	sg13g2_fd_pr__diode_pd2nw_05v5_hvt sg13g2_fd_pr__diode_pd2nw_11v0} \
	full_metal 1 vias 1 viagb 0 viagt 0 viagl 0 viagr 0}
}

proc sg13g2::sg13g2_fd_pr__diode_pd2nw_05v5_lvt_defaults {} {
    return {w 0.45 l 0.45 area 0.2025 peri 1.8 \
	nx 1 ny 1 dummy 0 lmin 0.45 wmin 0.45 class diode \
	elc 1 erc 1 etc 1 ebc 1 \
	glc 1 grc 1 gtc 1 gbc 1 doverlap 0 \
	compatible {sg13g2_fd_pr__diode_pd2nw_05v5 sg13g2_fd_pr__diode_pd2nw_05v5_lvt \
	sg13g2_fd_pr__diode_pd2nw_05v5_hvt sg13g2_fd_pr__diode_pd2nw_11v0} \
	full_metal 1 vias 1 viagb 0 viagt 0 viagl 0 viagr 0}
}

proc sg13g2::sg13g2_fd_pr__diode_pd2nw_05v5_hvt_defaults {} {
    return {w 0.45 l 0.45 area 0.2025 peri 1.8 \
	nx 1 ny 1 dummy 0 lmin 0.45 wmin 0.45 class diode \
	elc 1 erc 1 etc 1 ebc 1 \
	glc 1 grc 1 gtc 1 gbc 1 doverlap 0 \
	compatible {sg13g2_fd_pr__diode_pd2nw_05v5 sg13g2_fd_pr__diode_pd2nw_05v5_lvt \
	sg13g2_fd_pr__diode_pd2nw_05v5_hvt sg13g2_fd_pr__diode_pd2nw_11v0} \
	full_metal 1 vias 1 viagb 0 viagt 0 viagl 0 viagr 0}
}


proc sg13g2::sg13g2_fd_pr__diode_pd2nw_11v0_defaults {} {
    return {w 0.45 l 0.45 area 0.2024 peri 1.8 \
	nx 1 ny 1 dummy 0 lmin 0.45 wmin 0.45 class diode \
	elc 1 erc 1 etc 1 ebc 1 \
	glc 1 grc 1 gtc 1 gbc 1 doverlap 0 \
	compatible {sg13g2_fd_pr__diode_pd2nw_05v5 sg13g2_fd_pr__diode_pd2nw_05v5_lvt \
	sg13g2_fd_pr__diode_pd2nw_05v5_hvt sg13g2_fd_pr__diode_pd2nw_11v0} \
	full_metal 1 vias 1 viagb 0 viagt 0 viagl 0 viagr 0}
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__diode_pw2nd_05v5_convert {parameters} {
    return [sg13g2::diode_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__diode_pw2nd_05v5_lvt_convert {parameters} {
    return [sg13g2::diode_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__diode_pw2nd_05v5_nvt_convert {parameters} {
    return [sg13g2::diode_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__diode_pw2nd_11v0_convert {parameters} {
    return [sg13g2::diode_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__photodiode_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__diode_pd2nw_05v5_convert {parameters} {
    return [sg13g2::diode_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__diode_pd2nw_05v5_lvt_convert {parameters} {
    return [sg13g2::diode_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__diode_pd2nw_05v5_hvt_convert {parameters} {
    return [sg13g2::diode_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__diode_pd2nw_11v0_convert {parameters} {
    return [sg13g2::diode_convert $parameters]
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__diode_pw2nd_05v5_dialog {parameters} {
    sg13g2::diode_dialog sg13g2_fd_pr__diode_pw2nd_05v5 $parameters
}

proc sg13g2::sg13g2_fd_pr__diode_pw2nd_05v5_lvt_dialog {parameters} {
    sg13g2::diode_dialog sg13g2_fd_pr__diode_pw2nd_05v5_lvt $parameters
}

proc sg13g2::sg13g2_fd_pr__diode_pw2nd_05v5_nvt_dialog {parameters} {
    sg13g2::diode_dialog sg13g2_fd_pr__diode_pw2nd_05v5_nvt $parameters
}

proc sg13g2::sg13g2_fd_pr__diode_pw2nd_11v0_dialog {parameters} {
    sg13g2::diode_dialog sg13g2_fd_pr__diode_pw2nd_11v0 $parameters
}

proc sg13g2::sg13g2_fd_pr__photodiode_dialog {parameters} {
    sg13g2::fixed_dialog $parameters
}

proc sg13g2::sg13g2_fd_pr__diode_pd2nw_05v5_dialog {parameters} {
    sg13g2::diode_dialog sg13g2_fd_pr__diode_pd2nw_05v5 $parameters
}

proc sg13g2::sg13g2_fd_pr__diode_pd2nw_05v5_lvt_dialog {parameters} {
    sg13g2::diode_dialog sg13g2_fd_pr__diode_pd2nw_05v5_lvt $parameters
}

proc sg13g2::sg13g2_fd_pr__diode_pd2nw_05v5_hvt_dialog {parameters} {
    sg13g2::diode_dialog sg13g2_fd_pr__diode_pd2nw_05v5_hvt $parameters
}

proc sg13g2::sg13g2_fd_pr__diode_pd2nw_11v0_dialog {parameters} {
    sg13g2::diode_dialog sg13g2_fd_pr__diode_pd2nw_11v0 $parameters
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__diode_pw2nd_05v5_check {parameters} {
    sg13g2::diode_check $parameters
}

proc sg13g2::sg13g2_fd_pr__diode_pw2nd_05v5_lvt_check {parameters} {
    sg13g2::diode_check $parameters
}

proc sg13g2::sg13g2_fd_pr__diode_pw2nd_05v5_nvt_check {parameters} {
    sg13g2::diode_check $parameters
}

proc sg13g2::sg13g2_fd_pr__diode_pw2nd_11v0_check {parameters} {
    sg13g2::diode_check $parameters
}

proc sg13g2::sg13g2_fd_pr__photodiode_check {parameters} {
    sg13g2::fixed_check $parameters
}

proc sg13g2::sg13g2_fd_pr__diode_pd2nw_05v5_check {parameters} {
    sg13g2::diode_check $parameters
}

proc sg13g2::sg13g2_fd_pr__diode_pd2nw_05v5_lvt_check {parameters} {
    sg13g2::diode_check $parameters
}

proc sg13g2::sg13g2_fd_pr__diode_pd2nw_05v5_hvt_check {parameters} {
    sg13g2::diode_check $parameters
}

proc sg13g2::sg13g2_fd_pr__diode_pd2nw_11v0_check {parameters} {
    sg13g2::diode_check $parameters
}

#----------------------------------------------------------------
# Diode: Draw a single device
#----------------------------------------------------------------

proc sg13g2::diode_device {parameters} {
    # Epsilon for avoiding round-off errors
    set eps  0.0005

    # Set local default values if they are not in parameters
    set dev_surround 0
    set dev_sub_type ""

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # If there is no end_sub_surround, set it to sub_surround
    if {![dict exists $parameters end_sub_surround]} {
	set end_sub_surround $sub_surround
    }

    # Draw the device
    pushbox
    box size 0 0

    set hw [/ $w 2.0]
    set hl [/ $l 2.0]

    # Calculate ring size (measured to contact center)
    set gx [+ $w [* 2.0 [+ $dev_spacing $dev_surround]] $contact_size]
    set gy [+ $l [* 2.0 [+ $dev_spacing $dev_surround]] $contact_size]

    # Draw the ring first, because diode may occupy well/substrate plane
    set guardparams $parameters
    dict set guardparams plus_diff_type $end_type
    dict set guardparams plus_contact_type $end_contact_type
    dict set guardparams diff_surround $end_surround
    dict set guardparams sub_type $end_sub_type
    dict set guardparams sub_surround $sub_surround
    dict set guardparams guard_sub_surround $end_sub_surround
    dict set guardparams glc $elc
    dict set guardparams grc $erc
    dict set guardparams gtc $etc
    dict set guardparams gbc $ebc
    set cext [sg13g2::guard_ring $gx $gy $guardparams]

    pushbox
    box grow n ${hl}um
    box grow s ${hl}um
    box grow e ${hw}um
    box grow w ${hw}um
    paint ${dev_type}
    set cext [sg13g2::unionbox $cext [sg13g2::getbox]]

    if {$dev_sub_type != ""} {
	box grow n ${sub_surround}um
	box grow s ${sub_surround}um
	box grow e ${sub_surround}um
	box grow w ${sub_surround}um
	paint ${dev_sub_type}
    }
    popbox

    if {${w} < ${l}} {
	set orient vert
    } else {
	set orient horz
    }

    # Reduce width by surround amount
    set w [- $w [* ${dev_surround} 2.0]]
    set l [- $l [* ${dev_surround} 2.0]]

    # Draw via over contact first
    if {$vias != 0} {
        pushbox
        set ch $l
    	if {$ch < $via_size} {set ch $via_size}
    	set cw $w
    	if {$cw < $via_size} {set cw $via_size}
	box grow n [/ $ch 2]um
	box grow s [/ $ch 2]um
	box grow w [/ $cw 2]um
	box grow e [/ $cw 2]um
        sg13g2::mcon_draw
        popbox
    }
    set cext [sg13g2::unionbox $cext [sg13g2::draw_contact ${w} ${l} \
		${dev_surround} ${metal_surround} ${contact_size} \
		${dev_type} ${dev_contact_type} li ${orient}]]

    popbox
    return $cext
}

#----------------------------------------------------------------
# Diode: Draw the tiled device
#----------------------------------------------------------------

proc sg13g2::diode_draw {parameters} {
    tech unlock *

    # Set defaults if they are not in parameters
    set doverlap 0	;# overlap diodes at contacts
    set guard 0		;# draw a guard ring
    set prohibit_overlap false  ;# don't prohibit overlaps

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
    set bbox [sg13g2::diode_device $parameters]
    # puts stdout "Diagnostic: Device bounding box e $bbox (um)"
    tech unlock *

    set fw [- [lindex $bbox 2] [lindex $bbox 0]]
    set fh [- [lindex $bbox 3] [lindex $bbox 1]]
    set lw [+ [lindex $bbox 2] [lindex $bbox 0]]
    set lh [+ [lindex $bbox 3] [lindex $bbox 1]]

    # If prohibit_overlap is true, then end overlapping is prohibited when
    # nx or ny is > 1 to prevent DRC errors (typically from well spacing rule)
    if {$prohibit_overlap == true} {
        if {($nx > 1) || ($ny > 1)} {
	    set doverlap 0
	}
    }

    # Determine tile width and height (depends on overlap)

    if {$doverlap == 0} {
	set dx [+ $fw $end_spacing]
        set dy [+ $fh $end_spacing]
    } else {
        # overlap contact
        set dx [- $fw [+ [* 2.0 $sub_surround] [* 2.0 $end_surround] $contact_size]]
        set dy [- $fh [+ [* 2.0 $sub_surround] [* 2.0 $end_surround] $contact_size]]
    }

    # Determine core width and height
    set corex [+ [* [- $nx 1] $dx] $fw]
    set corey [+ [* [- $ny 1] $dy] $fh]
    set corellx [/ [+ [- $corex $fw] $lw] 2.0]
    set corelly [/ [+ [- $corey $fh] $lh] 2.0]

    if {$guard != 0} {
	# Calculate guard ring size (measured to contact center)
	set gx [+ $corex [* 2.0 [+ $diff_spacing $diff_surround]] $contact_size]
	set gy [+ $corey [* 2.0 [+ $diff_spacing $diff_surround]] $contact_size]

	# Draw the guard ring first, because diode may occupy well/substrate plane
	sg13g2::guard_ring $gx $gy $parameters
    }

    pushbox
    box move w ${corellx}um
    box move s ${corelly}um
    if {($nx > 1) || ($ny > 1)} {
	pushbox
	set hfw [/ $fw 2.0]
	set hfh [/ $fh 2.0]
	box move w ${hfw}um
	box move s ${hfh}um
	box size ${corex}um ${corey}um
	paint $end_sub_type
	popbox
    }
    for {set xp 0} {$xp < $nx} {incr xp} {
	pushbox
	for {set yp 0} {$yp < $ny} {incr yp} {
	    sg13g2::diode_device $parameters
            box move n ${dy}um
        }
	popbox
        box move e ${dx}um
    }
    popbox
    popbox

    tech revert
}

#----------------------------------------------------------------
# Photodiode: Draw a single device
#----------------------------------------------------------------

proc sg13g2::photodiode_device {parameters} {

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Draw the device
    pushbox
    box size 0 0

    # Device has ntap fixed width of 0.41 x 0.41
    # Surrounded by nwell 0.84 x 0.84
    # Surrounded by deep nwell 3.0 x 3.0

    pushbox
    box grow c 0.205um
    paint nsd
    popbox
    pushbox
    box grow c 0.42um
    paint nwell
    popbox
    pushbox
    box grow c 1.5um
    paint photo

    set cext [sg13g2::getbox]

    popbox

    # Only enough space for one contact
    set w ${contact_size}
    set l ${contact_size}

    set cext [sg13g2::unionbox $cext [sg13g2::draw_contact ${w} ${l} \
		0 ${metal_surround} ${contact_size} \
		nsd nsc li horz]]

    popbox
    return $cext
}

#----------------------------------------------------------------

proc sg13g2::photodiode_draw {parameters} {

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    pushbox
    box values 0 0 0 0

    # Determine the base device dimensions by drawing one device
    # while all layers are locked (nothing drawn).  This allows the
    # base drawing routine to do complicated geometry without having
    # to duplicate it here with calculations.

    tech lock *
    set bbox [sg13g2::photodiode_device $parameters]
    # puts stdout "Diagnostic: Device bounding box e $bbox (um)"
    tech unlock *

    set fw [- [lindex $bbox 2] [lindex $bbox 0]]
    set fh [- [lindex $bbox 3] [lindex $bbox 1]]
    set lw [+ [lindex $bbox 2] [lindex $bbox 0]]
    set lh [+ [lindex $bbox 3] [lindex $bbox 1]]

    # Determine tile width and height

    set dx [+ $fw $end_spacing]
    set dy [+ $fh $end_spacing]

    # Determine core width and height
    set corex [+ [* [- $nx 1] $dx] $fw]
    set corey [+ [* [- $ny 1] $dy] $fh]
    set corellx [/ [+ [- $corex $fw] $lw] 2.0]
    set corelly [/ [+ [- $corey $fh] $lh] 2.0]

    # Calculate guard ring size (measured to contact center)
    # Spacing between photodiode (deep nwell) and deep nwell (other) is 5.3um
    set gx [+ $corex 15.965]
    set gy [+ $corey 15.965]

    pushbox

    # The deep nwell is offset 0.315 from the nwell ring center to get the
    # right overlap.  The deep nwell ring has a minimum width of 3um.
    set hgx [/ $gx 2.0]
    set hgy [/ $gy 2.0]
    set dwx [+ $hgx 0.315]
    set dwy [+ $hgy 0.315]
    box grow e ${dwx}um
    box grow w ${dwx}um
    box grow n ${dwy}um
    box grow s ${dwy}um
    paint dnwell
    box grow e -3.0um
    box grow w -3.0um
    box grow n -3.0um
    box grow s -3.0um
    erase dnwell

    popbox

    # Draw the guard ring first.  0.63 is the amount nwell surrounds contact;
    # 0.63 * 2 + 0.17 = total nwell width 1.43um, needed to cover dnwell edge.
    set newdict [dict create	 \
	sub_type    space	 \
	guard_sub_type	 nwell	 \
	guard_sub_surround  0.63 \
	plus_diff_type   nsd	 \
	plus_contact_type nsc	 \
    ]
    set guarddict [dict merge $parameters $newdict]
    sg13g2::guard_ring $gx $gy $guarddict

    # Draw outside P-ring and generated the 2nd ring
    set gx [+ $gx [* 2.0 [+ 0.56 $diff_spacing $diff_surround]] $contact_size]
    set gy [+ $gy [* 2.0 [+ 0.56 $diff_spacing $diff_surround]] $contact_size]
    sg13g2::guard_ring $gx $gy $parameters

    pushbox
    box move w ${corellx}um
    box move s ${corelly}um

    for {set xp 0} {$xp < $nx} {incr xp} {
	pushbox
	for {set yp 0} {$yp < $ny} {incr yp} {
	    sg13g2::photodiode_device $parameters
            box move n ${dy}um
        }
	popbox
        box move e ${dx}um
    }
    popbox
    popbox

    tech revert
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__diode_pw2nd_05v5_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    dev_type		ndiode \
	    dev_contact_type	ndic \
	    end_type		psd \
	    end_contact_type	psc \
	    end_sub_type	psub \
	    dev_spacing		${diff_spacing} \
	    dev_surround	${diff_surround} \
	    end_spacing		${diff_spacing} \
	    end_surround	0 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::diode_draw $drawdict]
} 

#----------------------------------------------------------------
# NOTE:  Use ppd instead of psd so that there is additional
# diffusion around the contact, allowing more space for the
# implant (likewise sg13g2_fd_pr__diode_pd2nw_05v5_lvt and
# sg13g2_fd_pr__diode_pd2nw_11v0).

proc sg13g2::sg13g2_fd_pr__diode_pw2nd_05v5_lvt_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    dev_type		ndiodelvt \
	    dev_contact_type	ndilvtc \
	    end_type		ppd \
	    end_contact_type	psc \
	    end_sub_type	psub \
	    dev_spacing		${diff_spacing} \
	    dev_surround	${diff_surround} \
	    end_spacing		${diff_spacing} \
	    end_surround	${diff_surround} \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::diode_draw $drawdict]
} 

proc sg13g2::sg13g2_fd_pr__diode_pw2nd_05v5_nvt_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    dev_type		nndiode \
	    dev_contact_type	nndic \
	    end_type		mvpsd \
	    end_contact_type	mvpsc \
	    end_sub_type	psub \
	    dev_spacing		0.37 \
	    dev_surround	${diff_surround} \
	    end_spacing		0.30 \
	    end_surround	${diff_surround} \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::diode_draw $drawdict]
} 

proc sg13g2::sg13g2_fd_pr__diode_pw2nd_11v0_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    dev_type		mvndiode \
	    dev_contact_type	mvndic \
	    end_type		mvpsd \
	    end_contact_type	mvpsc \
	    end_sub_type	psub \
	    diff_spacing	0.37 \
	    dev_spacing		0.39 \
	    dev_surround	${diff_surround} \
	    end_spacing		0.36 \
	    end_surround	${diff_surround} \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::diode_draw $drawdict]
}


#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__diode_pd2nw_05v5_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    dev_type		pdiode \
	    guard		1 \
	    dev_contact_type	pdic \
	    end_type		nsd \
	    end_contact_type	nsc \
	    end_sub_type	nwell \
	    plus_diff_type	psd \
	    plus_contact_type	psc \
	    sub_type		psub \
	    dev_spacing		${diff_spacing} \
	    dev_surround	${diff_surround} \
	    end_spacing		${diff_spacing} \
	    end_surround	0 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::diode_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__diode_pd2nw_05v5_lvt_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    dev_type		pdiodelvt \
	    guard		1 \
	    dev_contact_type	pdilvtc \
	    end_type		nnd \
	    end_contact_type	nsc \
	    end_sub_type	nwell \
	    plus_diff_type	psd \
	    plus_contact_type	psc \
	    sub_type		psub \
	    dev_spacing		${diff_spacing} \
	    dev_surround	${diff_surround} \
	    end_spacing		${diff_spacing} \
	    end_surround	${diff_surround} \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::diode_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__diode_pd2nw_05v5_hvt_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    dev_type		pdiodehvt \
	    guard		1 \
	    dev_contact_type	pdihvtc \
	    end_type		nnd \
	    end_contact_type	nsc \
	    end_sub_type	nwell \
	    plus_diff_type	psd \
	    plus_contact_type	psc \
	    sub_type		psub \
	    dev_spacing		${diff_spacing} \
	    dev_surround	${diff_surround} \
	    end_spacing		${diff_spacing} \
	    end_surround	${diff_surround} \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::diode_draw $drawdict]
}


#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__diode_pd2nw_11v0_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    guard		1 \
	    dev_type 		mvpdiode \
	    dev_contact_type	mvpdic \
	    end_type		mvnsd \
	    end_contact_type	mvnsc \
	    end_sub_type	nwell \
	    plus_diff_type	mvpsd \
	    plus_contact_type	mvpsc \
	    sub_type		psub \
	    diff_spacing	0.58 \
	    dev_spacing		0.37 \
	    dev_surround	${diff_surround} \
	    end_spacing		0.30 \
	    end_sub_surround	0.33 \
	    end_surround	${diff_surround} \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::diode_draw $drawdict]
}

#----------------------------------------------------------------
# The photodiode has its own drawing routine, so
#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__photodiode_draw {parameters} {
    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    guard		1	\
	    sub_type		space	\
	    end_spacing		5.0	\
	    end_surround	1.0	\
	    sub_spacing		5.3	\
	    guard_sub_type	pwell	\
	    guard_sub_surround  0.18	\
	    plus_diff_type	psd	\
	    plus_contact_type	psc	\
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::photodiode_draw $drawdict]
}

#----------------------------------------------------------------
# Drawn capacitor routines
# NOTE:  Work in progress.  These values need to be corrected.
#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__cap_mim_m3_1_defaults {} {
    return {w 2.00 l 2.00 val 8.0 carea 2.00 cperi 0.19 class capacitor \
		nx 1 ny 1 dummy 0 square 0 lmin 2.00 wmin 2.00 \
		lmax 30.0 wmax 30.0 dc 0 bconnect 1 tconnect 1 \
		ccov 100}
}
proc sg13g2::sg13g2_fd_pr__cap_mim_m3_2_defaults {} {
    return {w 2.00 l 2.00 val 8.0 carea 2.00 cperi 0.19 class capacitor \
		nx 1 ny 1 dummy 0 square 0 lmin 2.00 wmin 2.00 \
		lmax 30.0 wmax 30.0 dc 0 bconnect 1 tconnect 1 \
		ccov 100}
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

proc sg13g2::sg13g2_fd_pr__cap_mim_m3_1_convert {parameters} {
    return [cap_convert $parameters]
}
proc sg13g2::sg13g2_fd_pr__cap_mim_m3_2_convert {parameters} {
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

    if {[dict exists $parameters square]} {
	magic::add_checkbox square "Square capacitor" $parameters
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

    # magic::add_checkbox dummy "Add dummy" $parameters
}

proc sg13g2::sg13g2_fd_pr__cap_mim_m3_1_dialog {parameters} {
    sg13g2::cap_dialog sg13g2_fd_pr__cap_mim_m3_1 $parameters
}
proc sg13g2::sg13g2_fd_pr__cap_mim_m3_2_dialog {parameters} {
    sg13g2::cap_dialog sg13g2_fd_pr__cap_mim_m3_2 $parameters
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
    set cap_surround 0
    set bot_surround 0
    set top_surround 0
    set end_spacing 0
    set bconnect 0	    ;# bottom plates are connected in array
    set cap_spacing 0	    ;# cap spacing in array
    set top_metal_space 0   ;# top metal spacing (if larger than cap spacing)
    set top_metal_width 0   ;# top metal minimum width
    set contact_size 0	    ;# cap contact minimum size
    set ccov 100	    ;# amount of contact coverage

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    if {![dict exists $parameters top_metal_space]} {
	set top_metal_space $metal_spacing
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
    if {$cw < $contact_size} {set cw $contact_size}
    if {$cw < $top_metal_width} {set cw $top_metal_width}
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
        set cdif [/ ${cdif} 2]
	box grow w -${cdif}um
	box grow e -${cdif}um
    }
    paint ${cap_contact_type}

    pushbox
    box grow n ${top_surround}um
    box grow s ${top_surround}um
    box grow e ${top_surround}um
    box grow w ${top_surround}um
    paint ${top_type}
    set cext [sg13g2::getbox]
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
    set cext [sg13g2::unionbox $cext [sg13g2::getbox]]

    # Calculate the distance from the top metal on the cap contact
    # to the top metal on the end contact.
    set top_met_sep [+ $end_spacing [- $cdif $top_surround]]

    # Diagnostic!
    # puts stdout "cdif = $cdif"
    # puts stdout "top_met_sep = $top_met_sep"

    # Increase end spacing if top metal spacing rule is not met
    set loc_end_spacing $end_spacing
    if {$top_met_sep < $top_metal_space} {
	set loc_end_spacing [+ $loc_end_spacing [- $top_metal_space $top_met_sep]]
    }
    # Diagnostic!
    # puts stdout "loc_end_spacing = $loc_end_spacing"

    # Extend bottom metal under contact to right
    box grow e ${loc_end_spacing}um
    set chw [/ ${contact_size} 2.0]
    box grow e ${chw}um
    box grow e ${end_surround}um
    paint ${bot_type}

    popbox
    popbox

    # Draw contact to right.  Reduce contact extent if devices are not
    # wired together and the top metal spacing rule limits the distance
    set lcont $l
    if {($bconnect == 0) && ($ny > 1)} {
	if {$cap_spacing < $top_metal_space} {
	    set cspace [- $top_metal_space $cap_spacing]
	    set lcont [- $l $cspace]
	}
    }

    pushbox
    box move e ${hw}um
    box move e ${bot_surround}um
    box move e ${loc_end_spacing}um
    set cl [- [+ ${lcont} [* ${bot_surround} 2.0]] [* ${end_surround} 2.0]]
    set cl [- ${cl} ${metal_surround}]  ;# see below
    set cext [sg13g2::unionbox $cext [sg13g2::draw_contact 0 ${cl} \
		${end_surround} ${metal_surround} ${contact_size} \
		${bot_type} ${top_contact_type} ${top_type} full]]
    popbox
    popbox

    return $cext

    # cl shrinks top and bottom to accomodate larger bottom metal
    # surround rule for contacts near a MiM cap.  This should be its
    # own variable, but metal_surround is sufficient.
}

#----------------------------------------------------------------
# Metal plate sandwich capacitor:  Draw a single device
#----------------------------------------------------------------

proc sg13g2::sandwich_cap_device {parameters} {

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    pushbox
    box size 0 0

    set hw [/ $w 2.0]
    set hl [/ $l 2.0]

    set cw [- [* $hw [/ 2.0 3]] [* $cont_surround 2.0]]
    set cl [- [* $hl [/ 2.0 3]] [* $cont_surround 2.0]]

    # plate capacitor defines layers p0, p1, etc.
    for {set i 0} {$i < 20} {incr i} {
        if {[catch {set layer [subst \$p${i}_type]}]} {break}  ;# no more layers defined
	pushbox
	box grow e ${hw}um
	box grow w ${hw}um
	box grow n ${hl}um
	box grow s ${hl}um
        if {![catch {set shrink [subst \$p${i}_shrink]}]} {
	    box grow e -${shrink}um
	    box grow w -${shrink}um
	    box grow n -${shrink}um
	    box grow s -${shrink}um
	    set cutout_spacing [+ [* ${shrink} 2.0] [/ $via_size 2.0] $cont_surround]
	} else {
	    set cutout_spacing 0
	}

	paint ${layer}

	if {$i == 1} {
	    # Note that cap_type geometry is coincident with p1_type.
	    # Typically, this will define a layer that outputs as both
	    # poly and a capacitor definition layer.
	    if {[dict exists $parameters cap_type]} {
		paint $cap_type
	    }
	}
	popbox

	# Even layers connect at corners, odd layers connect at sides.
	# Even layers cut out the sides, odd layers cut out the corners.
	# Layer zero has no side contacts or cutout.

	if {[% $i 2] == 0} {
	    set cornercmd  paint
	    set cornersize $cutout_spacing
	    set sidecmd    erase
	    set nssidelong   [+ $cutout_spacing [/ $hw 3.0]]
	    set ewsidelong   [+ $cutout_spacing [/ $hl 3.0]]
	    set sideshort    $cutout_spacing
	} else {
	    set cornercmd  erase
	    set cornersize $cutout_spacing
	    set sidecmd    paint
	    set nssidelong   [/ $hw 3.0]
	    set ewsidelong   [/ $hl 3.0]
	    set sideshort    $cutout_spacing
	}

	if {$i > 0} {
	    pushbox
	    box move e ${hw}um
	    box grow n ${ewsidelong}um
	    box grow s ${ewsidelong}um
	    box grow w ${sideshort}um
	    ${sidecmd} ${layer}
	    popbox
	    pushbox
	    box move n ${hl}um
	    box grow e ${nssidelong}um
	    box grow w ${nssidelong}um
	    box grow s ${sideshort}um
	    ${sidecmd} ${layer}
	    popbox
	    pushbox
	    box move w ${hw}um
	    box grow n ${ewsidelong}um
	    box grow s ${ewsidelong}um
	    box grow e ${sideshort}um
	    ${sidecmd} ${layer}
	    popbox
	    pushbox
	    box move s ${hl}um
	    box grow e ${nssidelong}um
	    box grow w ${nssidelong}um
	    box grow n ${sideshort}um
	    ${sidecmd} ${layer}
	    popbox

	    pushbox
	    box move n ${hl}um
	    box move e ${hw}um
	    box grow s ${cornersize}um
	    box grow w ${cornersize}um
	    ${cornercmd} ${layer}
	    popbox
	    pushbox
	    box move n ${hl}um
	    box move w ${hw}um
	    box grow s ${cornersize}um
	    box grow e ${cornersize}um
	    ${cornercmd} ${layer}
	    popbox
	    pushbox
	    box move s ${hl}um
	    box move e ${hw}um
	    box grow n ${cornersize}um
	    box grow w ${cornersize}um
	    ${cornercmd} ${layer}
	    popbox
	    pushbox
	    box move s ${hl}um
	    box move w ${hw}um
	    box grow n ${cornersize}um
	    box grow e ${cornersize}um
	    ${cornercmd} ${layer}
	    popbox
	}
    }

    # Draw contacts after all layers have been drawn, so that erasing
    # layers does not affect the contacts.

    for {set i 0} {$i < 20} {incr i} {
        if {![catch {set contact [subst \$p${i}_contact_type]}]} {
	    set layer [subst \$p${i}_type]
	    set j [+ $i 1]
	    set toplayer [subst \$p${j}_type]

	    # Draw corner contacts
	    pushbox
	    box move e ${hw}um
	    box move n ${hl}um
	    sg13g2::draw_contact 0 0 \
			${cont_surround} ${cont_surround} ${via_size} \
			${layer} ${contact} ${toplayer} full
	    popbox
	    pushbox
	    box move w ${hw}um
	    box move n ${hl}um
	    sg13g2::draw_contact 0 0 \
			${cont_surround} ${cont_surround} ${via_size} \
			${layer} ${contact} ${toplayer} full
	    popbox
	    pushbox
	    box move e ${hw}um
	    box move s ${hl}um
	    sg13g2::draw_contact 0 0 \
			${cont_surround} ${cont_surround} ${via_size} \
			${layer} ${contact} ${toplayer} full
	    popbox
	    pushbox
	    box move w ${hw}um
	    box move s ${hl}um
	    sg13g2::draw_contact 0 0 \
			${cont_surround} ${cont_surround} ${via_size} \
			${layer} ${contact} ${toplayer} full
	    popbox

	    # Draw side contacts (except on poly)
	    if {$i > 0} {
		pushbox
		box move w ${hw}um
		sg13g2::draw_contact 0 ${cl} \
			${cont_surround} ${cont_surround} ${via_size} \
			${layer} ${contact} ${toplayer} full
		popbox
		pushbox
		box move e ${hw}um
		sg13g2::draw_contact 0 ${cl} \
			${cont_surround} ${cont_surround} ${via_size} \
			${layer} ${contact} ${toplayer} full
		popbox
		pushbox
		box move n ${hl}um
		sg13g2::draw_contact ${cw} 0 \
			${cont_surround} ${cont_surround} ${via_size} \
			${layer} ${contact} ${toplayer} full
		popbox
		pushbox
		box move s ${hl}um
		sg13g2::draw_contact ${cw} 0 \
			${cont_surround} ${cont_surround} ${via_size} \
			${layer} ${contact} ${toplayer} full
		popbox
	    }
	} else {
	    break
	}
    }

    popbox
    # Bounding box is the same as the device length and width
    set cext [list -$hw -$hl $hw $hl]
    return $cext
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
    set wide_cap_spacing 0  ;# additional spacing for wide metal rule
    set wide_cap_width 0
    set end_spacing 0
    set end_surround 0
    set bot_surround 0
    set top_metal_width 0
    set bconnect 0	;# connect bottom plates in array
    set tconnect 0	;# connect top plates in array
    set top_type ""

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
    # puts stdout "Diagnostic: Device bounding box e $bbox (um)"
    tech unlock *

    set fw [- [lindex $bbox 2] [lindex $bbox 0]]
    set fh [- [lindex $bbox 3] [lindex $bbox 1]]
    set lw [+ [lindex $bbox 2] [lindex $bbox 0]]
    set lh [+ [lindex $bbox 3] [lindex $bbox 1]]

    set dwide 0
    if {($fw >= $wide_cap_width) && ($fh >= $wide_cap_width)} {
	set dwide $wide_cap_spacing
    }

    # Determine tile width and height (depends on overlap)
    if {$coverlap == 0} {
        set dy [+ $fh $cap_spacing $dwide]
    } else {
        # overlap at end contact
        set dy [- $fh [+ $end_surround $end_surround $contact_size]]
    }
    # Contact is placed on right so spacing is determined by end_spacing.
    set dx [+ $fw $end_spacing $dwide]

    # Determine core width and height
    set corex [+ [* [- $nx 1] $dx] $fw]
    set corey [+ [* [- $ny 1] $dy] $fh]
    set corellx [/ [+ [- $corex $fw] $lw] 2.0]
    set corelly [/ [+ [- $corey $fh] $lh] 2.0]

    if {$guard != 0} {
	# Calculate guard ring size (measured to contact center)
	set gx [+ $corex [* 2.0 [+ $cap_diff_spacing $diff_surround]] $contact_size]
	set gy [+ $corey [* 2.0 [+ $end_spacing $diff_surround]] $contact_size]

	# Draw the guard ring first.
	sg13g2::guard_ring $gx $gy $parameters
    }

    set twidth [+ ${contact_size} ${end_surround} ${end_surround}]
    if {${twidth} < ${top_metal_width}} {
	set twidth ${top_metal_width}
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
	    if {$sandwich == 1} {
		sg13g2::sandwich_cap_device $parameters
	    } else {
		sg13g2::cap_device $parameters
	    }
	    if {$ny > 1} {
		pushbox
		box grow e ${hmw}um
		box grow w ${hmw}um
		box grow n ${hdy}um
		box grow s ${hdy}um
		if {($top_type != "") && ($tconnect == 1)} {
		    paint ${top_type}
		}
		if {($top_type != "") && ($bconnect == 1)} {
		    box move e ${cdx}um
		    paint ${top_type}
		}
		popbox
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

proc sg13g2::sg13g2_fd_pr__cap_mim_m3_1_draw {parameters} {
    set newdict [dict create \
	    top_type 		m4 \
	    top_contact_type	via3 \
	    cap_type 		mimcap \
	    cap_contact_type	mimcc \
	    bot_type 		m3 \
	    bot_surround	0.2 \
	    cap_spacing		1.2 \
	    cap_surround	0.2 \
	    top_surround	0.005 \
	    end_surround	0.1 \
	    end_spacing		1.2 \
	    contact_size	0.32 \
	    metal_surround	0.08 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::cap_draw $drawdict]
}

proc sg13g2::sg13g2_fd_pr__cap_mim_m3_2_draw {parameters} {
    set newdict [dict create \
	    top_type 		m5 \
	    top_contact_type	via4 \
	    cap_type 		mimcap2 \
	    cap_contact_type	mim2cc \
	    bot_type 		m4 \
	    bot_surround	0.4 \
	    cap_spacing		1.2 \
	    cap_surround	0.2 \
	    top_surround	0.12 \
	    end_surround	0.1 \
	    end_spacing		2.0 \
	    contact_size	1.18 \
	    metal_surround	0.21 \
	    top_metal_width	1.6 \
	    top_metal_space	0.7 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::cap_draw $drawdict]
}


#----------------------------------------------------------------
# capacitor: Check device parameters for out-of-bounds values
#----------------------------------------------------------------

proc sg13g2::cap_check {parameters} {
    # In case wmax and/or lmax are undefined
    set lmax 0
    set wmax 0
    set ccov 100

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

    # Calculate value from L and W
    set cval [expr ($l * $w * $carea + 2 * ($l + $w) * $cperi - 4 * $dc)]
    dict set parameters val [magic::float2spice $cval]
    sg13g2::compute_ctot $parameters

    return $parameters
}

proc sg13g2::sg13g2_fd_pr__cap_mim_m3_1_check {parameters} {
    return [sg13g2::cap_check $parameters]
}
proc sg13g2::sg13g2_fd_pr__cap_mim_m3_2_check {parameters} {
    return [sg13g2::cap_check $parameters]
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
# sg13g2_fd_pr__res_iso_pw: Specify all user-editable default values
# and those needed by sg13g2_fd_pr__res_iso_pw_check
# NOTE:  Work in progress.  Some values need to be corrected.
# Discrepancy between sheet rho value in documentation vs. model.
#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_iso_pw_defaults {} {
    return {w 2.650 l 26.50 m 1 nx 1 wmin 2.650 lmin 26.50 class resistor \
	 	rho 3050 val 30502 dummy 0 dw 0.25 term 1.0 \
		guard 1 endcov 100 full_metal 1 vias 1 \
		viagb 0 viagt 0 viagl 0 viagr 0}
}

#----------------------------------------------------------------
# rpp1: Specify all user-editable default values and those
# needed by rp1_check
#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_generic_po_defaults {} {
    return {w 0.330 l 1.650 m 1 nx 1 wmin 0.330 lmin 1.650 class resistor \
		rho 48.2 val 241 dummy 0 dw 0.0 term 0.0 \
		sterm 0.0 caplen 0.4 snake 0 guard 1 \
		glc 1 grc 1 gtc 1 gbc 1 roverlap 0 endcov 100 \
		full_metal 1 hv_guard 0 n_guard 0 vias 1 \
		viagb 0 viagt 0 viagl 0 viagr 0}
}

# "term" is rho * 0.06, the distance between xpc edge and CONT.
proc sg13g2::sg13g2_fd_pr__res_high_po_0p35_defaults {} {
    return {w 0.350 l 0.50 m 1 nx 1 wmin 0.350 lmin 0.50 class resistor \
		rho 319.8 val 456.857 dummy 0 dw 0.0 term 194.82 \
		sterm 0.0 caplen 0 guard 1 glc 1 grc 1 gtc 1 gbc 1 \
		compatible {sg13g2_fd_pr__res_high_po_0p35 \
		sg13g2_fd_pr__res_high_po_0p69 sg13g2_fd_pr__res_high_po_1p41 \
		sg13g2_fd_pr__res_high_po_2p85 sg13g2_fd_pr__res_high_po_5p73} \
		snake 0 full_metal 1 wmax 0.350 vias 1 n_guard 0 hv_guard 0 \
		viagb 0 viagt 0 viagl 0 viagr 0}
}
proc sg13g2::sg13g2_fd_pr__res_high_po_0p69_defaults {} {
    return {w 0.690 l 1.00 m 1 nx 1 wmin 0.690 lmin 0.50 class resistor \
		rho 319.8 val 463.480 dummy 0 dw 0.0 term 194.82 \
		sterm 0.0 caplen 0 guard 1 glc 1 grc 1 gtc 1 gbc 1 \
		compatible {sg13g2_fd_pr__res_high_po_0p35 \
		sg13g2_fd_pr__res_high_po_0p69 sg13g2_fd_pr__res_high_po_1p41 \
		sg13g2_fd_pr__res_high_po_2p85 sg13g2_fd_pr__res_high_po_5p73} \
		snake 0 full_metal 1 wmax 0.690 n_guard 0 hv_guard 0 vias 1 \
		viagb 0 viagt 0 viagl 0 viagr 0}
}
proc sg13g2::sg13g2_fd_pr__res_high_po_1p41_defaults {} {
    return {w 1.410 l 2.00 m 1 nx 1 wmin 1.410 lmin 0.50 class resistor \
		rho 319.8 val 453.620 dummy 0 dw 0.0 term 194.82 \
		sterm 0.0 caplen 0 guard 1 glc 1 grc 1 gtc 1 gbc 1 \
		compatible {sg13g2_fd_pr__res_high_po_0p35 \
		sg13g2_fd_pr__res_high_po_0p69 sg13g2_fd_pr__res_high_po_1p41 \
		sg13g2_fd_pr__res_high_po_2p85 sg13g2_fd_pr__res_high_po_5p73} \
		snake 0 full_metal 1 wmax 1.410 n_guard 0 hv_guard 0 vias 1 \
		viagb 0 viagt 0 viagl 0 viagr 0}
}
proc sg13g2::sg13g2_fd_pr__res_high_po_2p85_defaults {} {
    return {w 2.850 l 3.00 m 1 nx 1 wmin 2.850 lmin 0.50 class resistor \
		rho 319.8 val 336.630 dummy 0 dw 0.0 term 194.82 \
		sterm 0.0 caplen 0 guard 1 glc 1 grc 1 gtc 1 gbc 1 \
		compatible {sg13g2_fd_pr__res_high_po_0p35 \
		sg13g2_fd_pr__res_high_po_0p69 sg13g2_fd_pr__res_high_po_1p41 \
		sg13g2_fd_pr__res_high_po_2p85 sg13g2_fd_pr__res_high_po_5p73} \
		snake 0 full_metal 1 wmax 2.850 n_guard 0 hv_guard 0 vias 1 \
		viagb 0 viagt 0 viagl 0 viagr 0}
}
proc sg13g2::sg13g2_fd_pr__res_high_po_5p73_defaults {} {
    return {w 5.730 l 6.00 m 1 nx 1 wmin 5.730 lmin 0.50 class resistor \
		rho 319.8 val 334.870 dummy 0 dw 0.0 term 194.82 \
		sterm 0.0 caplen 0 guard 1 glc 1 grc 1 gtc 1 gbc 1 \
		compatible {sg13g2_fd_pr__res_high_po_0p35 \
		sg13g2_fd_pr__res_high_po_0p69 sg13g2_fd_pr__res_high_po_1p41 \
		sg13g2_fd_pr__res_high_po_2p85 sg13g2_fd_pr__res_high_po_5p73} \
		snake 0 full_metal 1 wmax 5.730 n_guard 0 hv_guard 0 vias 1 \
		viagb 0 viagt 0 viagl 0 viagr 0}
}

# "term" is rho * 0.06, the distance between xpc edge and CONT.
proc sg13g2::sg13g2_fd_pr__res_xhigh_po_0p35_defaults {} {
    return {w 0.350 l 0.50 m 1 nx 1 wmin 0.350 lmin 0.50 class resistor \
		rho 2000 val 2875.143 dummy 0 dw 0.0 term 188.2 \
		sterm 0.0 caplen 0 wmax 0.350 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 \
		compatible {sg13g2_fd_pr__res_xhigh_po_0p35 \
		sg13g2_fd_pr__res_xhigh_po_0p69 sg13g2_fd_pr__res_xhigh_po_1p41 \
		sg13g2_fd_pr__res_xhigh_po_2p85 sg13g2_fd_pr__res_xhigh_po_5p73} \
		snake 0 full_metal 1 n_guard 0 hv_guard 0 vias 1 \
		viagb 0 viagt 0 viagl 0 viagr 0}
}
proc sg13g2::sg13g2_fd_pr__res_xhigh_po_0p69_defaults {} {
    return {w 0.690 l 1.00 m 1 nx 1 wmin 0.690 lmin 0.50 class resistor \
		rho 2000 val 2898.600 dummy 0 dw 0.0 term 188.2 \
		sterm 0.0 caplen 0 wmax 0.690 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 \
		compatible {sg13g2_fd_pr__res_xhigh_po_0p35 \
		sg13g2_fd_pr__res_xhigh_po_0p69 sg13g2_fd_pr__res_xhigh_po_1p41 \
		sg13g2_fd_pr__res_xhigh_po_2p85 sg13g2_fd_pr__res_xhigh_po_5p73} \
		snake 0 full_metal 1 n_guard 0 hv_guard 0 vias 1 \
		viagb 0 viagt 0 viagl 0 viagr 0}
}
proc sg13g2::sg13g2_fd_pr__res_xhigh_po_1p41_defaults {} {
    return {w 1.410 l 2.00 m 1 nx 1 wmin 1.410 lmin 0.50 class resistor \
		rho 2000 val 2836.900 dummy 0 dw 0.0 term 188.2 \
		sterm 0.0 caplen 0 wmax 1.410 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 \
		compatible {sg13g2_fd_pr__res_xhigh_po_0p35 \
		sg13g2_fd_pr__res_xhigh_po_0p69 sg13g2_fd_pr__res_xhigh_po_1p41 \
		sg13g2_fd_pr__res_xhigh_po_2p85 sg13g2_fd_pr__res_xhigh_po_5p73} \
		snake 0 full_metal 1 n_guard 0 hv_guard 0 vias 1 \
		viagb 0 viagt 0 viagl 0 viagr 0}
}
proc sg13g2::sg13g2_fd_pr__res_xhigh_po_2p85_defaults {} {
    return {w 2.850 l 3.00 m 1 nx 1 wmin 2.850 lmin 0.50 class resistor \
		rho 2000 val 2105.300 dummy 0 dw 0.0 term 188.2 \
		sterm 0.0 caplen 0 wmax 2.850 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 \
		compatible {sg13g2_fd_pr__res_xhigh_po_0p35 \
		sg13g2_fd_pr__res_xhigh_po_0p69 sg13g2_fd_pr__res_xhigh_po_1p41 \
		sg13g2_fd_pr__res_xhigh_po_2p85 sg13g2_fd_pr__res_xhigh_po_5p73} \
		snake 0 full_metal 1 n_guard 0 hv_guard 0 vias 1 \
		viagb 0 viagt 0 viagl 0 viagr 0}
}
proc sg13g2::sg13g2_fd_pr__res_xhigh_po_5p73_defaults {} {
    return {w 5.730 l 6.00 m 1 nx 1 wmin 5.730 lmin 0.50 class resistor \
		rho 2000 val 2094.200 dummy 0 dw 0.0 term 188.2 \
		sterm 0.0 caplen 0 wmax 5.730 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 \
		compatible {sg13g2_fd_pr__res_xhigh_po_0p35 \
		sg13g2_fd_pr__res_xhigh_po_0p69 sg13g2_fd_pr__res_xhigh_po_1p41 \
		sg13g2_fd_pr__res_xhigh_po_2p85 sg13g2_fd_pr__res_xhigh_po_5p73} \
		snake 0 full_metal 1 n_guard 0 hv_guard 0 vias 1 \
		viagb 0 viagt 0 viagl 0 viagr 0}
}

#----------------------------------------------------------------
# sg13g2_fd_pr__res_generic_nd: Specify all user-editable default values and those
# needed by rdn_check
#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_generic_nd_defaults {} {
    return {w 0.420 l 2.100 m 1 nx 1 wmin 0.42 lmin 2.10 class resistor \
		rho 120 val 600.0 dummy 0 dw 0.05 term 0.0 \
		sterm 0.0 caplen 0.4 snake 0 guard 1 \
		glc 1 grc 1 gtc 1 gbc 1 roverlap 0 endcov 100 \
		full_metal 1 vias 1 \
		viagb 0 viagt 0 viagl 0 viagr 0}
}

proc sg13g2::sg13g2_fd_pr__res_generic_nd__hv_defaults {} {
    return {w 0.420 l 2.100 m 1 nx 1 wmin 0.42 lmin 2.10 class resistor \
		rho 120 val 600.0 dummy 0 dw 0.02 term 0.0 \
		sterm 0.0 caplen 0.4 snake 0 guard 1 \
		glc 1 grc 1 gtc 1 gbc 1 roverlap 0 endcov 100 \
		full_metal 1 vias 1 \
		viagb 0 viagt 0 viagl 0 viagr 0}
}

#----------------------------------------------------------------
# sg13g2_fd_pr__res_generic_pd: Specify all user-editable default values and those
# needed by rdp_check
#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_generic_pd_defaults {} {
    return {w 0.420 l 2.100 m 1 nx 1 wmin 0.42 lmin 2.10 class resistor \
		rho 197 val 985.0 dummy 0 dw 0.02 term 0.0 \
		sterm 0.0 caplen 0.60 snake 0 guard 1 \
		glc 1 grc 1 gtc 1 gbc 1 roverlap 0 endcov 100 \
		full_metal 1 vias 1 \
		viagb 0 viagt 0 viagl 0 viagr 0}
}

proc sg13g2::sg13g2_fd_pr__res_generic_pd__hv_defaults {} {
    return {w 0.420 l 2.100 m 1 nx 1 wmin 0.42 lmin 2.10 class resistor \
		rho 197 val 985.0 dummy 0 dw 0.02 term 0.0 \
		sterm 0.0 caplen 0.60 snake 0 guard 1 \
		glc 1 grc 1 gtc 1 gbc 1 roverlap 0 endcov 100 \
		full_metal 1 vias 1 \
		viagb 0 viagt 0 viagl 0 viagr 0}
}

#----------------------------------------------------------------
# sg13g2_fd_pr__res_generic_l1: Specify all user-editable default values and those needed
# by sg13g2_fd_pr__res_generic_l1_check
#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_generic_l1_defaults {} {
    return {w 0.170 l 0.170 m 1 nx 1 wmin 0.17 lmin 0.17 class resistor \
		rho 12.8 val 12.8 dummy 0 dw 0.0 term 0.0 snake 0 \
		roverlap 0}
}

#----------------------------------------------------------------
# sg13g2_fd_pr__res_generic_m1: Specify all user-editable default values and those needed
# by sg13g2_fd_pr__res_generic_m1_check
#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_generic_m1_defaults {} {
    return {w 0.140 l 0.140 m 1 nx 1 wmin 0.14 lmin 0.14 class resistor \
		rho 0.125 val 0.125 dummy 0 dw 0.0 term 0.0 \
		roverlap 0}
}

#----------------------------------------------------------------
# sg13g2_fd_pr__res_generic_m2: Specify all user-editable default values and those needed
# by sg13g2_fd_pr__res_generic_m2_check
#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_generic_m2_defaults {} {
    return {w 0.140 l 0.140 m 1 nx 1 wmin 0.14 lmin 0.14 class resistor \
		rho 0.125 val 0.125 dummy 0 dw 0.0 term 0.0 \
		roverlap 0}
}

#----------------------------------------------------------------
# sg13g2_fd_pr__res_generic_m3: Specify all user-editable default values and those needed
# by sg13g2_fd_pr__res_generic_m3_check
#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_generic_m3_defaults {} {
    return {w 0.300 l 0.300 m 1 nx 1 wmin 0.30 lmin 0.30 class resistor \
		rho 0.047 val 0.047 dummy 0 dw 0.0 term 0.0 \
		roverlap 0}
}

#----------------------------------------------------------------
# Additional entries for sg13g2_fd_pr__res_generic_m4 and sg13g2_fd_pr__res_generic_m5, depending on the
# back-end metal stack.
#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_generic_m4_defaults {} {
    return {w 0.300 l 0.300 m 1 nx 1 wmin 0.30 lmin 0.30 class resistor \
		rho 0.047 val 0.047 dummy 0 dw 0.0 term 0.0 \
		roverlap 0}
}
proc sg13g2::sg13g2_fd_pr__res_generic_m5_defaults {} {
    return {w 1.600 l 1.600 m 1 nx 1 wmin 1.60 lmin 1.60 class resistor \
		rho 0.029 val 0.029 dummy 0 dw 0.0 term 0.0 \
		roverlap 0}
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

proc sg13g2::sg13g2_fd_pr__res_iso_pw_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_generic_po_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_high_po_0p35_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}
proc sg13g2::sg13g2_fd_pr__res_high_po_0p69_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}
proc sg13g2::sg13g2_fd_pr__res_high_po_1p41_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}
proc sg13g2::sg13g2_fd_pr__res_high_po_2p85_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}
proc sg13g2::sg13g2_fd_pr__res_high_po_5p73_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_xhigh_po_0p35_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}
proc sg13g2::sg13g2_fd_pr__res_xhigh_po_0p69_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}
proc sg13g2::sg13g2_fd_pr__res_xhigh_po_1p41_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}
proc sg13g2::sg13g2_fd_pr__res_xhigh_po_2p85_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}
proc sg13g2::sg13g2_fd_pr__res_xhigh_po_5p73_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_generic_nd_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_generic_pd_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_generic_nd__hv_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_generic_pd__hv_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_generic_l1_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_generic_m1_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_generic_m2_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_generic_m3_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_generic_m4_convert {parameters} {
    return [sg13g2::res_convert $parameters]
}
proc sg13g2::sg13g2_fd_pr__res_generic_m5_convert {parameters} {
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
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_iso_pw_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_iso_pw $parameters
}

proc sg13g2::sg13g2_fd_pr__res_generic_po_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_generic_po $parameters
}

proc sg13g2::sg13g2_fd_pr__res_high_po_0p35_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_high_po_0p35 $parameters
}
proc sg13g2::sg13g2_fd_pr__res_high_po_0p69_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_high_po_0p69 $parameters
}
proc sg13g2::sg13g2_fd_pr__res_high_po_1p41_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_high_po_1p41 $parameters
}
proc sg13g2::sg13g2_fd_pr__res_high_po_2p85_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_high_po_2p85 $parameters
}
proc sg13g2::sg13g2_fd_pr__res_high_po_5p73_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_high_po_5p73 $parameters
}

proc sg13g2::sg13g2_fd_pr__res_xhigh_po_0p35_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_xhigh_po_0p35 $parameters
}
proc sg13g2::sg13g2_fd_pr__res_xhigh_po_0p69_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_xhigh_po_0p69 $parameters
}
proc sg13g2::sg13g2_fd_pr__res_xhigh_po_1p41_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_xhigh_po_1p41 $parameters
}
proc sg13g2::sg13g2_fd_pr__res_xhigh_po_2p85_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_xhigh_po_2p85 $parameters
}
proc sg13g2::sg13g2_fd_pr__res_xhigh_po_5p73_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_xhigh_po_5p73 $parameters
}

proc sg13g2::sg13g2_fd_pr__res_generic_nd_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_generic_nd $parameters
}

proc sg13g2::sg13g2_fd_pr__res_generic_pd_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_generic_pd $parameters
}

proc sg13g2::sg13g2_fd_pr__res_generic_nd__hv_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_generic_nd__hv $parameters
}

proc sg13g2::sg13g2_fd_pr__res_generic_pd__hv_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_generic_pd__hv $parameters
}

proc sg13g2::sg13g2_fd_pr__res_generic_l1_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_generic_l1 $parameters
}

proc sg13g2::sg13g2_fd_pr__res_generic_m1_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_generic_m1 $parameters
}

proc sg13g2::sg13g2_fd_pr__res_generic_m2_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_generic_m2 $parameters
}

proc sg13g2::sg13g2_fd_pr__res_generic_m3_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_generic_m3 $parameters
}

proc sg13g2::sg13g2_fd_pr__res_generic_m4_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_generic_m4 $parameters
}
proc sg13g2::sg13g2_fd_pr__res_generic_m5_dialog {parameters} {
    sg13g2::res_dialog sg13g2_fd_pr__res_generic_m5 $parameters
}

#----------------------------------------------------------------
# Resistor: Draw a single device in straight geometry
#----------------------------------------------------------------

proc sg13g2::res_device {parameters} {
    # Epsilon for avoiding round-off errors
    set eps  0.0005

    # Set local default values if they are not in parameters
    set endcov 0	 	;# percent coverage of end contacts
    set roverlap 0		;# overlap resistors at end contacts
    set well_res_overlap 0 	;# not a well resistor
    set end_contact_type ""	;# no contacts for metal resistors
    set end_overlap_cont 0	;# additional end overlap on sides
    set vias 0			;# add vias over contacts
    set l_delta 0		;# delta between measured and drawn length
    set res_idtype none

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

    if {${end_contact_type} != ""} {
	# Draw via over contact first
	if {$vias != 0} {
            pushbox
            set ch $res_to_endcont
    	    if {$ch < $via_size} {set ch $via_size}
    	    set cw $epl
    	    if {$cw < $via_size} {set cw $via_size}
	    box grow n [/ $via_size 2]um
	    box grow s [- $ch [/ $via_size 2]]um
	    box grow w [/ $cw 2]um
	    box grow e [/ $cw 2]um
            sg13g2::mcon_draw
            popbox
    	}
	set cext [sg13g2::unionbox $cext [sg13g2::draw_contact ${cpl} 0 \
		${end_surround} ${metal_surround} ${end_contact_size} \
		${end_type} ${end_contact_type} li horz]]
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

    if {${end_contact_type} != ""} {
	# Draw via over contact first
	if {$vias != 0} {
            pushbox
            set ch $res_to_endcont
    	    if {$ch < $via_size} {set ch $via_size}
    	    set cw $epl
    	    if {$cw < $via_size} {set cw $via_size}
	    box grow n [- $ch [/ $via_size 2]]um
	    box grow s [/ $via_size 2]um
	    box grow w [/ $cw 2]um
	    box grow e [/ $cw 2]um
            sg13g2::mcon_draw
            popbox
    	}
	set cext [sg13g2::unionbox $cext [sg13g2::draw_contact ${cpl} 0 \
		${end_surround} ${metal_surround} ${end_contact_size} \
		${end_type} ${end_contact_type} li horz]]
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
    set endcov 100	 	;# percent coverage of end contacts
    set well_res_overlap 0 	;# not a well resistor
    set end_contact_type ""	;# no contacts for metal resistors
    set mask_clearance 0	;# additional length to clear mask

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

    if {${end_contact_type} != ""} {
	set cext [sg13g2::draw_contact ${cpl} 0 \
		${end_surround} ${metal_surround} ${end_contact_size} \
		${end_type} ${end_contact_type} li horz]
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

    if {${end_contact_type} != ""} {
	set cext [sg13g2::unionbox $cext [sg13g2::draw_contact ${cpl} 0 \
		${end_surround} ${metal_surround} ${end_contact_size} \
		${end_type} ${end_contact_type} li horz]]
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
	sg13g2::guard_ring $gx $gy $parameters
    }

    pushbox
    box move w ${corellx}um
    box move s ${corelly}um
    # puts "Device position at = [sg13g2::getbox]"
    for {set xp 0} {$xp < $nx} {incr xp} {
	pushbox
	for {set yp 0} {$yp < $m} {incr yp} {
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

proc sg13g2::sg13g2_fd_pr__res_generic_po_draw {parameters} {

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
	    set gdifftype mvnsd
	    set gdiffcont mvnsc
	} else {
	    set gdifftype mvpsd
	    set gdiffcont mvpsc
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
	    res_type		npres \
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
	    res_to_endcont	1.985 \
	    res_spacing		$poly_spacing \
	    res_diff_spacing	0.48 \
	    mask_clearance	0.52 \
	    overlap_compress	0.36 \
    ]

    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_high_po_0p35_draw {parameters} {

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
	    set gdifftype mvnsd
	    set gdiffcont mvnsc
	} else {
	    set gdifftype mvpsd
	    set gdiffcont mvpsc
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
	    res_type		ppres \
	    end_type 		xpc \
	    end_contact_type	xpc \
	    end_contact_size	0 \
	    plus_diff_type	$gdifftype \
	    plus_contact_type	$gdiffcont \
	    sub_type		$gsubtype \
	    guard_sub_surround	$gsurround \
	    end_surround	$poly_surround \
	    end_spacing		$gresdiff_end \
	    end_to_end_space	0.52 \
	    end_contact_size	0.19 \
	    res_to_cont		0.575 \
	    res_to_endcont	1.985 \
	    res_spacing		0.48 \
	    res_diff_spacing	$gresdiff_spacing \
	    mask_clearance	-2.16 \
	    overlap_compress	0.36 \
	    l_delta		-0.08 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

proc sg13g2::sg13g2_fd_pr__res_high_po_0p69_draw {parameters} {

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
	    set gdifftype mvnsd
	    set gdiffcont mvnsc
	} else {
	    set gdifftype mvpsd
	    set gdiffcont mvpsc
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
	set gresdiff_spacing 0.615
	set gresdiff_end 0.525
    } else {
	set gsubtype psub
	set gresdiff_spacing 0.48
	set gresdiff_end 0.48
    }

    set newdict [dict create \
	    res_type		ppres \
	    end_type 		xpc \
	    end_contact_type	xpc \
	    end_contact_size	0 \
	    plus_diff_type	$gdifftype \
	    plus_contact_type	$gdiffcont \
	    sub_type		$gsubtype \
	    guard_sub_surround	$gsurround \
	    end_surround	$poly_surround \
	    end_spacing		$gresdiff_end \
	    end_to_end_space	0.52 \
	    end_contact_size	0.19 \
	    res_to_cont		0.575 \
	    res_to_endcont	1.985 \
	    res_spacing		0.48 \
	    res_diff_spacing	$gresdiff_spacing \
	    mask_clearance	0.52 \
	    overlap_compress	0.36 \
	    l_delta		-0.08 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

proc sg13g2::sg13g2_fd_pr__res_high_po_1p41_draw {parameters} {

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
	    set gdifftype mvnsd
	    set gdiffcont mvnsc
	} else {
	    set gdifftype mvpsd
	    set gdiffcont mvpsc
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
	set gresdiff_spacing 0.525
	set gresdiff_end 0.525
    } else {
	set gsubtype psub
	set gresdiff_spacing 0.48
	set gresdiff_end 0.48
    }

    set newdict [dict create \
	    res_type		ppres \
	    end_type 		xpc \
	    end_contact_type	xpc \
	    end_contact_size	0 \
	    plus_diff_type	$gdifftype \
	    plus_contact_type	$gdiffcont \
	    sub_type		$gsubtype \
	    guard_sub_surround	$gsurround \
	    end_surround	$poly_surround \
	    end_spacing		$gresdiff_end \
	    end_to_end_space	0.52 \
	    end_contact_size	0.19 \
	    res_to_cont		0.575 \
	    res_to_endcont	1.985 \
	    res_spacing		0.48 \
	    res_diff_spacing	$gresdiff_spacing \
	    mask_clearance	0.52 \
	    overlap_compress	0.36 \
	    l_delta		-0.08 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

proc sg13g2::sg13g2_fd_pr__res_high_po_2p85_draw {parameters} {

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
	    set gdifftype mvnsd
	    set gdiffcont mvnsc
	} else {
	    set gdifftype mvpsd
	    set gdiffcont mvpsc
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
	set gresdiff_spacing 0.525
	set gresdiff_end 0.525
    } else {
	set gsubtype psub
	set gresdiff_spacing 0.48
	set gresdiff_end 0.48
    }

    set newdict [dict create \
	    res_type		ppres \
	    end_type 		xpc \
	    end_contact_type	xpc \
	    end_contact_size	0 \
	    plus_diff_type	$gdifftype \
	    plus_contact_type	$gdiffcont \
	    sub_type		$gsubtype \
	    guard_sub_surround	$gsurround \
	    end_surround	$poly_surround \
	    end_spacing		$gresdiff_end \
	    end_to_end_space	0.52 \
	    end_contact_size	0.19 \
	    res_to_cont		0.575 \
	    res_to_endcont	1.985 \
	    res_spacing		0.48 \
	    res_diff_spacing	$gresdiff_spacing \
	    mask_clearance	0.52 \
	    overlap_compress	0.36 \
	    l_delta		-0.08 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

proc sg13g2::sg13g2_fd_pr__res_high_po_5p73_draw {parameters} {

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
	    set gdifftype mvnsd
	    set gdiffcont mvnsc
	} else {
	    set gdifftype mvpsd
	    set gdiffcont mvpsc
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
	set gresdiff_spacing 0.525
	set gresdiff_end 0.525
    } else {
	set gsubtype psub
	set gresdiff_spacing 0.48
	set gresdiff_end 0.48
    }

    set newdict [dict create \
	    res_type		ppres \
	    end_type 		xpc \
	    end_contact_type	xpc \
	    end_contact_size	0 \
	    plus_diff_type	$gdifftype \
	    plus_contact_type	$gdiffcont \
	    sub_type		$gsubtype \
	    guard_sub_surround	$gsurround \
	    end_surround	$poly_surround \
	    end_spacing		$gresdiff_end \
	    end_to_end_space	0.52 \
	    end_contact_size	0.19 \
	    res_to_cont		0.575 \
	    res_to_endcont	1.985 \
	    res_spacing		0.48 \
	    res_diff_spacing	$gresdiff_spacing \
	    mask_clearance	0.52 \
	    overlap_compress	0.36 \
	    l_delta		-0.08 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_xhigh_po_0p35_draw {parameters} {

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
	    set gdifftype mvnsd
	    set gdiffcont mvnsc
	} else {
	    set gdifftype mvpsd
	    set gdiffcont mvpsc
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
	    res_type		xpres \
	    end_type 		xpc \
	    end_contact_type	xpc \
	    end_contact_size	0 \
	    plus_diff_type	$gdifftype \
	    plus_contact_type	$gdiffcont \
	    sub_type		$gsubtype \
	    guard_sub_surround	$gsurround \
	    end_surround	$poly_surround \
	    end_spacing		$gresdiff_end \
	    end_to_end_space	0.52 \
	    end_contact_size	0.19 \
	    res_to_cont		0.575 \
	    res_to_endcont	1.985 \
	    res_spacing		0.48 \
	    res_diff_spacing	$gresdiff_spacing \
	    mask_clearance	0.52 \
	    overlap_compress	0.36 \
	    l_delta		-0.08 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_xhigh_po_0p35_draw {parameters} {

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
	    set gdifftype mvnsd
	    set gdiffcont mvnsc
	} else {
	    set gdifftype mvpsd
	    set gdiffcont mvpsc
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
	    res_type		xpres \
	    end_type 		xpc \
	    end_contact_type	xpc \
	    end_contact_size	0 \
	    plus_diff_type	$gdifftype \
	    plus_contact_type	$gdiffcont \
	    sub_type		$gsubtype \
	    guard_sub_surround	$gsurround \
	    end_surround	$poly_surround \
	    end_spacing		$gresdiff_end \
	    end_to_end_space	0.52 \
	    end_contact_size	0.19 \
	    res_to_cont		0.575 \
	    res_to_endcont	1.985 \
	    res_spacing		0.48 \
	    res_diff_spacing	$gresdiff_spacing \
	    mask_clearance	0.52 \
	    overlap_compress	0.36 \
	    l_delta		-0.08 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

proc sg13g2::sg13g2_fd_pr__res_xhigh_po_0p69_draw {parameters} {

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
	    set gdifftype mvnsd
	    set gdiffcont mvnsc
	} else {
	    set gdifftype mvpsd
	    set gdiffcont mvpsc
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
	set gresdiff_spacing 0.615
	set gresdiff_end 0.525
    } else {
	set gsubtype psub
	set gresdiff_spacing 0.48
	set gresdiff_end 0.48
    }

    set newdict [dict create \
	    res_type		xpres \
	    end_type 		xpc \
	    end_contact_type	xpc \
	    end_contact_size	0 \
	    plus_diff_type	$gdifftype \
	    plus_contact_type	$gdiffcont \
	    sub_type		$gsubtype \
	    guard_sub_surround	$gsurround \
	    end_surround	$poly_surround \
	    end_spacing		$gresdiff_end \
	    end_to_end_space	0.52 \
	    end_contact_size	0.19 \
	    res_to_cont		0.575 \
	    res_to_endcont	1.985 \
	    res_spacing		0.48 \
	    res_diff_spacing	$gresdiff_spacing \
	    mask_clearance	0.52 \
	    overlap_compress	0.36 \
	    l_delta		-0.08 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

proc sg13g2::sg13g2_fd_pr__res_xhigh_po_1p41_draw {parameters} {

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
	    set gdifftype mvnsd
	    set gdiffcont mvnsc
	} else {
	    set gdifftype mvpsd
	    set gdiffcont mvpsc
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
	set gresdiff_spacing 0.525
	set gresdiff_end 0.525
    } else {
	set gsubtype psub
	set gresdiff_spacing 0.48
	set gresdiff_end 0.48
    }

    set newdict [dict create \
	    res_type		xpres \
	    end_type 		xpc \
	    end_contact_type	xpc \
	    end_contact_size	0 \
	    plus_diff_type	$gdifftype \
	    plus_contact_type	$gdiffcont \
	    sub_type		$gsubtype \
	    guard_sub_surround	$gsurround \
	    end_surround	$poly_surround \
	    end_spacing		$gresdiff_end \
	    end_to_end_space	0.52 \
	    end_contact_size	0.19 \
	    res_to_cont		0.575 \
	    res_to_endcont	1.985 \
	    res_spacing		0.48 \
	    res_diff_spacing	$gresdiff_spacing \
	    mask_clearance	0.52 \
	    overlap_compress	0.36 \
	    l_delta		-0.08 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

proc sg13g2::sg13g2_fd_pr__res_xhigh_po_2p85_draw {parameters} {

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
	    set gdifftype mvnsd
	    set gdiffcont mvnsc
	} else {
	    set gdifftype mvpsd
	    set gdiffcont mvpsc
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
	set gresdiff_spacing 0.525
	set gresdiff_end 0.525
    } else {
	set gsubtype psub
	set gresdiff_spacing 0.48
	set gresdiff_end 0.48
    }

    set newdict [dict create \
	    res_type		xpres \
	    end_type 		xpc \
	    end_contact_type	xpc \
	    end_contact_size	0 \
	    plus_diff_type	$gdifftype \
	    plus_contact_type	$gdiffcont \
	    sub_type		$gsubtype \
	    guard_sub_surround	$gsurround \
	    end_surround	$poly_surround \
	    end_spacing		$gresdiff_end \
	    end_to_end_space	0.52 \
	    end_contact_size	0.19 \
	    res_to_cont		0.575 \
	    res_to_endcont	1.985 \
	    res_spacing		0.48 \
	    res_diff_spacing	$gresdiff_spacing \
	    mask_clearance	0.52 \
	    overlap_compress	0.36 \
	    l_delta		-0.08 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

proc sg13g2::sg13g2_fd_pr__res_xhigh_po_5p73_draw {parameters} {

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
	    set gdifftype mvnsd
	    set gdiffcont mvnsc
	} else {
	    set gdifftype mvpsd
	    set gdiffcont mvpsc
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
	set gresdiff_spacing 0.525
	set gresdiff_end 0.525
    } else {
	set gsubtype psub
	set gresdiff_spacing 0.48
	set gresdiff_end 0.48
    }

    set newdict [dict create \
	    res_type		xpres \
	    end_type 		xpc \
	    end_contact_type	xpc \
	    end_contact_size	0 \
	    plus_diff_type	$gdifftype \
	    plus_contact_type	$gdiffcont \
	    sub_type		$gsubtype \
	    guard_sub_surround	$gsurround \
	    end_surround	$poly_surround \
	    end_spacing		$gresdiff_end \
	    end_to_end_space	0.52 \
	    end_contact_size	0.19 \
	    res_to_cont		0.575 \
	    res_to_endcont	1.985 \
	    res_spacing		0.48 \
	    res_diff_spacing	$gresdiff_spacing \
	    mask_clearance	0.52 \
	    overlap_compress	0.36 \
	    l_delta		-0.08 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_generic_nd_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    res_type		rdn \
	    end_type 		ndiff \
	    end_contact_type	ndc \
	    plus_diff_type	psd \
	    plus_contact_type	psc \
	    sub_type		psub \
	    end_surround	$diff_surround \
	    end_spacing		0.44 \
	    res_to_endcont	0.37 \
	    res_spacing		0.30 \
	    res_diff_spacing	0.44 \
	    mask_clearance	0.22 \
	    overlap_compress	0.36 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_generic_nd__hv_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    res_type		mvrdn \
	    end_type 		mvndiff \
	    end_contact_type	mvndc \
	    plus_diff_type	mvpsd \
	    plus_contact_type	mvpsc \
	    sub_type		psub \
	    end_surround	$diff_surround \
	    end_spacing		0.44 \
	    res_to_endcont	0.37 \
	    res_spacing		0.30 \
	    res_diff_spacing	0.44 \
	    mask_clearance	0.22 \
	    overlap_compress	0.36 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_generic_pd_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    res_type		rdp \
	    end_type 		pdiff \
	    end_contact_type	pdc \
	    plus_diff_type	nsd \
	    plus_contact_type	nsc \
	    sub_type		nwell \
	    end_surround	$diff_surround \
	    end_spacing		0.44 \
	    res_to_endcont	0.37 \
	    res_spacing		$diff_spacing \
	    res_diff_spacing	0.44 \
	    mask_clearance	0.22 \
	    overlap_compress	0.36 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_generic_pd__hv_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    res_type		mvrdp \
	    end_type 		mvpdiff \
	    end_contact_type	mvpdc \
	    plus_diff_type	mvnsd \
	    plus_contact_type	mvnsc \
	    sub_type		nwell \
	    end_surround	$diff_surround \
	    guard_sub_surround	0.33 \
	    end_spacing		0.44 \
	    res_to_endcont	0.37 \
	    res_spacing		0.30 \
	    res_diff_spacing	0.44 \
	    mask_clearance	0.22 \
	    overlap_compress	0.36 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_iso_pw_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    well_res_type	pwell \
	    res_type		rpw \
	    end_type 		psd \
	    end_contact_type	psc \
	    plus_diff_type	nsd \
	    plus_contact_type	nsc \
	    sub_type		dnwell \
	    sub_surround	0.23 \
	    guard_sub_type	nwell \
	    guard_sub_surround	0.63 \
	    end_surround	$diff_surround \
	    end_spacing		0.63 \
	    end_to_end_space	1.15 \
	    end_overlap_cont	0.06 \
	    end_contact_size	0.53 \
	    overlap_compress	-0.17 \
	    res_to_endcont	0.265 \
	    res_spacing		1.4 \
	    res_diff_spacing	0.63 \
	    well_res_overlap	0.2 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_generic_l1_draw {parameters} {

    # Set a local variable for each rule in ruleset
    foreach key [dict keys $sg13g2::ruleset] {
        set $key [dict get $sg13g2::ruleset $key]
    }

    set newdict [dict create \
	    guard		0 \
	    res_type		rli \
	    end_type 		li \
	    end_surround	0.0 \
	    end_spacing		0.0 \
	    res_to_endcont	0.2 \
	    end_to_end_space	0.23 \
	    res_spacing		$metal_spacing \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::res_draw $drawdict]
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_generic_m1_draw {parameters} {

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

proc sg13g2::sg13g2_fd_pr__res_generic_m2_draw {parameters} {

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

proc sg13g2::sg13g2_fd_pr__res_generic_m3_draw {parameters} {

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

proc sg13g2::sg13g2_fd_pr__res_generic_m4_draw {parameters} {

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

proc sg13g2::sg13g2_fd_pr__res_generic_m5_draw {parameters} {
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

    # Diffusion resistors must satisfy diffusion-to-tap spacing of 15um.
    # Therefore the maximum of guard ring width or height cannot exceed 30um.
    # If in violation, reduce counts first, as these are easiest to recover
    # by duplicating the device and overlapping the wells.
    if {$device == "rdn" || $device == "rdp"} {
       set origm $m
       set orignx $nx
       while true {
	  set xext [expr ($w + 0.8) * $nx + 1.0]
	  set yext [expr ($l + 1.7) * $m + 1.7]
          if {[expr min($xext, $yext)] > 40.0} {
              if {$yext > 40.0 && $m > 1} {
		 incr m -1
	      } elseif {$xext > 30.0 && $nx > 1} {
		 incr nx -1
	      } elseif {$yext > 30.0} {
		 set l 29
		 puts -nonewline stderr "Diffusion resistor length must be < 29 um"
		 puts stderr " to avoid tap spacing violation."
		 dict set parameters l $l
	      } elseif {$xext > 30.0} {
		 set w 29
		 puts -nonewline stderr "Diffusion resistor width must be < 29 um"
		 puts stderr " to avoid tap spacing violation."
		 dict set parameters w $w
	      }
          } else {
	      break
	  }
       }
       if {$m != $origm} {
	  puts stderr "Warning:  Fingers may need to be reduced to prevent tap distance violation"
	  # dict set parameters m $m
       }
       if {$nx != $orignx} {
	  puts stderr "Warning:  M may need to be reduced to prevent tap distance violation"
	  # dict set parameters nx $nx
       }
    }
    sg13g2::compute_ltot $parameters
    return $parameters
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__res_iso_pw_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_iso_pw $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_generic_po_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_generic_po $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_high_po_0p35_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_high_po_0p35 $parameters]
}
proc sg13g2::sg13g2_fd_pr__res_high_po_0p69_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_high_po_0p69 $parameters]
}
proc sg13g2::sg13g2_fd_pr__res_high_po_1p41_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_high_po_1p41 $parameters]
}
proc sg13g2::sg13g2_fd_pr__res_high_po_2p85_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_high_po_2p85 $parameters]
}
proc sg13g2::sg13g2_fd_pr__res_high_po_5p73_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_high_po_5p73 $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_xhigh_po_0p35_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_xhigh_po_0p35 $parameters]
}
proc sg13g2::sg13g2_fd_pr__res_xhigh_po_0p69_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_xhigh_po_0p69 $parameters]
}
proc sg13g2::sg13g2_fd_pr__res_xhigh_po_1p41_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_xhigh_po_1p41 $parameters]
}
proc sg13g2::sg13g2_fd_pr__res_xhigh_po_2p85_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_xhigh_po_2p85 $parameters]
}
proc sg13g2::sg13g2_fd_pr__res_xhigh_po_5p73_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_xhigh_po_5p73 $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_generic_nd_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_generic_nd $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_generic_pd_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_generic_pd $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_generic_nd__hv_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_generic_nd__hv $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_generic_pd__hv_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_generic_pd__hv $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_generic_l1_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_generic_l1 $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_generic_m1_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_generic_m1 $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_generic_m2_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_generic_m2 $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_generic_m3_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_generic_m3 $parameters]
}

proc sg13g2::sg13g2_fd_pr__res_generic_m4_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_generic_m4 $parameters]
}
proc sg13g2::sg13g2_fd_pr__res_generic_m5_check {parameters} {
    return [sg13g2::res_check sg13g2_fd_pr__res_generic_m5 $parameters]
}

#----------------------------------------------------------------
# MOS defaults:
#----------------------------------------------------------------
#    w       = Gate width
#    l       = Gate length
#    m	     = Multiplier
#    nf	     = Number of fingers
#    diffcov = Diffusion contact coverage
#    polycov = Poly contact coverage
#    topc    = Top gate contact
#    botc    = Bottom gate contact
#    guard   = Guard ring
#
# (not user-editable)
#
#    lmin    = Gate minimum length
#    wmin    = Gate minimum width
#----------------------------------------------------------------

#----------------------------------------------------------------
# pmos: Specify all user-editable default values and those
# needed by mos_check
#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__pfet_01v8_defaults {} {
    return {w 0.42 l 0.15 m 1 nf 1 diffcov 100 polycov 100 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 tbcov 100 rlcov 100 \
		topc 1 botc 1 poverlap 0 doverlap 1 lmin 0.15 wmin 0.42 \
		class mosfet compatible {sg13g2_fd_pr__pfet_01v8 \
		sg13g2_fd_pr__pfet_01v8_lvt sg13g2_fd_pr__pfet_01v8_hvt \
		sg13g2_fd_pr__pfet_g5v0d10v5} full_metal 1 \
		viasrc 100 viadrn 100 viagate 100 \
		viagb 0 viagr 0 viagl 0 viagt 0}
}

proc sg13g2::sg13g2_fd_pr__pfet_01v8_lvt_defaults {} {
    return {w 0.42 l 0.35 m 1 nf 1 diffcov 100 polycov 100 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 tbcov 100 rlcov 100 \
		topc 1 botc 1 poverlap 0 doverlap 1 lmin 0.35 wmin 0.42 \
		class mosfet compatible {sg13g2_fd_pr__pfet_01v8 \
		sg13g2_fd_pr__pfet_01v8_lvt sg13g2_fd_pr__pfet_01v8_hvt \
		sg13g2_fd_pr__pfet_g5v0d10v5} full_metal 1 \
		viasrc 100 viadrn 100 viagate 100 \
		viagb 0 viagr 0 viagl 0 viagt 0}
}

proc sg13g2::sg13g2_fd_pr__pfet_01v8_hvt_defaults {} {
    return {w 0.42 l 0.15 m 1 nf 1 diffcov 100 polycov 100 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 tbcov 100 rlcov 100 \
		topc 1 botc 1 poverlap 0 doverlap 1 lmin 0.15 wmin 0.42 \
		class mosfet compatible {sg13g2_fd_pr__pfet_01v8 \
		sg13g2_fd_pr__pfet_01v8_lvt sg13g2_fd_pr__pfet_01v8_hvt \
		sg13g2_fd_pr__pfet_g5v0d10v5} full_metal 1 \
		viasrc 100 viadrn 100 viagate 100 \
		viagb 0 viagr 0 viagl 0 viagt 0}
}

proc sg13g2::sg13g2_fd_pr__pfet_g5v0d10v5_defaults {} {
    return {w 0.42 l 0.50 m 1 nf 1 diffcov 100 polycov 100 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 tbcov 100 rlcov 100 \
		topc 1 botc 1 poverlap 0 doverlap 1 lmin 0.50 wmin 0.42 \
		class mosfet compatible {sg13g2_fd_pr__pfet_01v8 \
		sg13g2_fd_pr__pfet_01v8_lvt sg13g2_fd_pr__pfet_01v8_hvt \
		sg13g2_fd_pr__pfet_g5v0d10v5} full_metal 1 \
		viasrc 100 viadrn 100 viagate 100 \
		viagb 0 viagr 0 viagl 0 viagt 0}
}

proc sg13g2::sg13g2_fd_pr__pfet_g5v0d16v0_defaults {} {
    return {w 5.00 l 1.050 m 1 nf 1 diffcov 100 polycov 100 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 tbcov 100 rlcov 100 \
		topc 1 botc 1 poverlap 0 doverlap 0 lmin 1.050 wmin 5.00 \
		class mosfet full_metal 1 viasrc 100 viadrn 100 viagate 100 \
		viagb 0 viagr 0 viagl 0 viagt 0}
}

#----------------------------------------------------------------
# nmos: Specify all user-editable default values and those
# needed by mos_check
#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__nfet_01v8_defaults {} {
    return {w 0.420 l 0.150 m 1 nf 1 diffcov 100 polycov 100 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 tbcov 100 rlcov 100 \
		topc 1 botc 1 poverlap 0 doverlap 1 lmin 0.15 wmin 0.42 \
		class mosfet \
		compatible {sg13g2_fd_pr__nfet_01v8 sg13g2_fd_pr__nfet_01v8_lvt \
		sg13g2_fd_bs_flash__special_sonosfet_star \
		sg13g2_fd_pr__nfet_g5v0d10v5 sg13g2_fd_pr__nfet_05v0_nvt \
		sg13g2_fd_pr__nfet_03v3_nvt} \
		full_metal 1 viasrc 100 viadrn 100 viagate 100 \
		viagb 0 viagr 0 viagl 0 viagt 0}
}

proc sg13g2::sg13g2_fd_pr__nfet_01v8_lvt_defaults {} {
    return {w 0.420 l 0.150 m 1 nf 1 diffcov 100 polycov 100 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 tbcov 100 rlcov 100 \
		topc 1 botc 1 poverlap 0 doverlap 1 lmin 0.15 wmin 0.42 \
		class mosfet \
		compatible {sg13g2_fd_pr__nfet_01v8 sg13g2_fd_pr__nfet_01v8_lvt \
		sg13g2_fd_bs_flash__special_sonosfet_star \
		sg13g2_fd_pr__nfet_g5v0d10v5 sg13g2_fd_pr__nfet_05v0_nvt \
		sg13g2_fd_pr__nfet_03v3_nvt} \
		full_metal 1 viasrc 100 viadrn 100 viagate 100 \
		viagb 0 viagr 0 viagl 0 viagt 0}
}

proc sg13g2::sg13g2_fd_bs_flash__special_sonosfet_star_defaults {} {
    return {w 0.420 l 0.150 m 1 nf 1 diffcov 100 polycov 100 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 tbcov 100 rlcov 100 \
		topc 1 botc 1 poverlap 0 doverlap 1 lmin 0.15 wmin 0.42 \
		class mosfet \
		compatible {sg13g2_fd_pr__nfet_01v8 sg13g2_fd_pr__nfet_01v8_lvt \
		sg13g2_fd_bs_flash__special_sonosfet_star \
		sg13g2_fd_pr__nfet_g5v0d10v5 sg13g2_fd_pr__nfet_05v0_nvt \
		sg13g2_fd_pr__nfet_03v3_nvt} \
		full_metal 1 viasrc 100 viadrn 100 viagate 100 \
		viagb 0 viagr 0 viagl 0 viagt 0}
}

proc sg13g2::sg13g2_fd_pr__nfet_g5v0d10v5_defaults {} {
    return {w 0.42 l 0.50 m 1 nf 1 diffcov 100 polycov 100 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 tbcov 100 rlcov 100 \
		topc 1 botc 1 poverlap 0 doverlap 1 lmin 0.50 wmin 0.42 \
		class mosfet \
		compatible {sg13g2_fd_pr__nfet_01v8 sg13g2_fd_pr__nfet_01v8_lvt \
		sg13g2_fd_bs_flash__special_sonosfet_star \
		sg13g2_fd_pr__nfet_g5v0d10v5 sg13g2_fd_pr__nfet_05v0_nvt \
		sg13g2_fd_pr__nfet_03v3_nvt} \
		full_metal 1 viasrc 100 viadrn 100 viagate 100 \
		viagb 0 viagr 0 viagl 0 viagt 0}
}

proc sg13g2::sg13g2_fd_pr__nfet_05v0_nvt_defaults {} {
    return {w 0.42 l 0.90 m 1 nf 1 diffcov 100 polycov 100 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 tbcov 100 rlcov 100 \
		topc 1 botc 1 poverlap 0 doverlap 1 lmin 0.90 wmin 0.42 \
		class mosfet \
		compatible {sg13g2_fd_pr__nfet_01v8 sg13g2_fd_pr__nfet_01v8_lvt \
		sg13g2_fd_bs_flash__special_sonosfet_star \
		sg13g2_fd_pr__nfet_g5v0d10v5 sg13g2_fd_pr__nfet_05v0_nvt \
		sg13g2_fd_pr__nfet_03v3_nvt} \
		full_metal 1 viasrc 100 viadrn 100 viagate 100 \
		viagb 0 viagr 0 viagl 0 viagt 0}
}

proc sg13g2::sg13g2_fd_pr__nfet_03v3_nvt_defaults {} {
    return {w 0.42 l 0.50 m 1 nf 1 diffcov 100 polycov 100 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 tbcov 100 rlcov 100 \
		topc 1 botc 1 poverlap 0 doverlap 1 lmin 0.50 wmin 0.42 \
		class mosfet \
		compatible {sg13g2_fd_pr__nfet_01v8 sg13g2_fd_pr__nfet_01v8_lvt \
		sg13g2_fd_bs_flash__special_sonosfet_star \
		sg13g2_fd_pr__nfet_g5v0d10v5 sg13g2_fd_pr__nfet_05v0_nvt \
		sg13g2_fd_pr__nfet_03v3_nvt} \
		full_metal 1 viasrc 100 viadrn 100 viagate 100 \
		viagb 0 viagr 0 viagl 0 viagt 0}
}

proc sg13g2::sg13g2_fd_pr__nfet_g5v0d16v0_defaults {} {
    return {w 5.00 l 1.055 m 1 nf 1 diffcov 100 polycov 100 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 tbcov 100 rlcov 100 \
		topc 1 botc 1 poverlap 0 doverlap 0 lmin 1.050 wmin 5.00 \
		full_metal 1 viasrc 100 viadrn 100 viagate 100 \
		viagb 0 viagr 0 viagl 0 viagt 0}
}

#----------------------------------------------------------------
# mos varactor: Specify all user-editable default values and those
# needed by mosvc_check
#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__cap_var_lvt_defaults {} {
    return {w 1.0 l 0.18 m 1 nf 1 diffcov 100 polycov 100 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 tbcov 100 rlcov 100 \
		topc 1 botc 1 poverlap 0 doverlap 1 lmin 0.18 wmin 1.0 \
		class mosfet compatible {sg13g2_fd_pr__cap_var_lvt \
		sg13g2_fd_pr__cap_var_hvt sg13g2_fd_pr__cap_var} \
		full_metal 1 viasrc 100 viadrn 100 viagate 100 \
		viagb 0 viagr 0 viagl 0 viagt 0 gshield 1}
}

proc sg13g2::sg13g2_fd_pr__cap_var_hvt_defaults {} {
    return {w 1.0 l 0.18 m 1 nf 1 diffcov 100 polycov 100 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 tbcov 100 rlcov 100 \
		topc 1 botc 1 poverlap 0 doverlap 1 lmin 0.18 wmin 1.0 \
		class mosfet compatible {sg13g2_fd_pr__cap_var_lvt \
		sg13g2_fd_pr__cap_var_hvt sg13g2_fd_pr__cap_var} \
		full_metal 1 viasrc 100 viadrn 100 viagate 100 \
		viagb 0 viagr 0 viagl 0 viagt 0 gshield 1}
}

proc sg13g2::sg13g2_fd_pr__cap_var_defaults {} {
    return {w 1.0 l 0.50 m 1 nf 1 diffcov 100 polycov 100 \
		guard 1 glc 1 grc 1 gtc 1 gbc 1 tbcov 100 rlcov 100 \
		topc 1 botc 1 poverlap 0 doverlap 1 lmin 0.50 wmin 1.0 \
		class mosfet compatible {sg13g2_fd_pr__cap_var_lvt \
		sg13g2_fd_pr__cap_var_hvt sg13g2_fd_pr__cap_var} \
		full_metal 1 viasrc 100 viadrn 100 viagate 100 \
		viagb 0 viagr 0 viagl 0 viagt 0 gshield 1}
}

#----------------------------------------------------------------
# mos: Conversion from SPICE netlist parameters to toolkit
#----------------------------------------------------------------

proc sg13g2::mos_convert {parameters} {
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
		dict set pdkparams [string tolower $key] $value
	    }
	    nf {
		# Adjustment ot W will be handled below
		dict set pdkparams [string tolower $key] $value
	    }
	    default {
		# Allow unrecognized parameters to be passed unmodified
		dict set pdkparams $key $value
	    }
	}
    }

    # Magic does not understand "nf" as a parameter, but expands to
    # "nf" number of devices connected horizontally.  The "w" value
    # must be divided down accordingly, as the "nf" parameter implies
    # that the total width "w" is divided into "nf" fingers.

    catch {
	set w [dict get $pdkparams w]
	set nf [dict get $pdkparams nf]
	if {$nf > 1} {
	    dict set pdkparams w [expr $w / $nf]
	}
    }

    return $pdkparams
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__nfet_01v8_convert {parameters} {
    return [sg13g2::mos_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__nfet_01v8_lvt_convert {parameters} {
    return [sg13g2::mos_convert $parameters]
}

proc sg13g2::sg13g2_fd_bs_flash__special_sonosfet_star_convert {parameters} {
    return [sg13g2::mos_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__nfet_g5v0d10v5_convert {parameters} {
    return [sg13g2::mos_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__nfet_g5v0d16v0_convert {parameters} {
    return [sg13g2::mos_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__nfet_05v0_nvt_convert {parameters} {
    return [sg13g2::mos_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__nfet_03v3_nvt_convert {parameters} {
    return [sg13g2::mos_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__pfet_01v8_convert {parameters} {
    return [sg13g2::mos_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__pfet_01v8_lvt_convert {parameters} {
    return [sg13g2::mos_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__pfet_01v8_hvt_convert {parameters} {
    return [sg13g2::mos_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__pfet_g5v0d10v5_convert {parameters} {
    return [sg13g2::mos_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__pfet_g5v0d16v0_convert {parameters} {
    return [sg13g2::mos_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__cap_var_lvt_convert {parameters} {
    return [sg13g2::mos_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__cap_var_hvt_convert {parameters} {
    return [sg13g2::mos_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__cap_var_convert {parameters} {
    return [sg13g2::mos_convert $parameters]
}

#----------------------------------------------------------------
# mos: Interactively specifies the fixed layout parameters
#----------------------------------------------------------------

proc sg13g2::mos_dialog {device parameters} {
    # Editable fields:      w, l, nf, m, diffcov, polycov
    # Checked fields:  topc, botc
    # For specific devices, gate type is a selection list

    magic::add_entry w "Width (um)" $parameters
    magic::add_entry l "Length (um)" $parameters
    magic::add_entry nf "Fingers" $parameters
    magic::add_entry m "M" $parameters

    if {[dict exists $parameters compatible]} {
       set sellist [dict get $parameters compatible]
       magic::add_selectlist gencell "Device type" $sellist $parameters $device
    }

    # Default-empty message area, used by the varactor dialog.
    magic::add_message minfo "" $parameters brown

    magic::add_entry diffcov "Diffusion contact coverage (%)" $parameters
    magic::add_entry polycov "Poly contact coverage (%)" $parameters
    magic::add_entry rlcov "Guard ring contact coverage (%)" $parameters
    if {[dict exists $parameters gbc]} {
	magic::add_entry tbcov "Guard ring top/bottom contact coverage (%)" $parameters
    }

    magic::add_checkbox poverlap "Overlap at poly contact" $parameters
    magic::add_checkbox doverlap "Overlap at diffusion contact" $parameters
    magic::add_checkbox topc "Add top gate contact" $parameters
    magic::add_checkbox botc "Add bottom gate contact" $parameters

    magic::add_checkbox guard "Add guard ring" $parameters
    magic::add_checkbox full_metal "Full metal guard ring" $parameters
    magic::add_checkbox glc "Add left guard ring contact" $parameters
    magic::add_checkbox grc "Add right guard ring contact" $parameters
    if {[dict exists $parameters gbc]} {
	magic::add_checkbox gbc "Add bottom guard ring contact" $parameters
    }
    if {[dict exists $parameters gtc]} {
	magic::add_checkbox gtc "Add top guard ring contact" $parameters
    }

    if {[string first "cap_var" $device] != -1} {
	magic::add_checkbox gshield "Metal shield over gate" $parameters
    }

    magic::add_entry viasrc "Source via coverage \[+/-\](%)" $parameters
    magic::add_entry viadrn "Drain via coverage \[+/-\](%)" $parameters
    magic::add_entry viagate "Gate via coverage \[+/-\](%)" $parameters
    magic::add_entry viagb "Bottom guard ring via coverage \[+/-\](%)" $parameters
    magic::add_entry viagt "Top guard ring via coverage \[+/-\](%)" $parameters
    magic::add_entry viagr "Right guard ring via coverage \[+/-\](%)" $parameters
    magic::add_entry viagl "Left guard ring via coverage \[+/-\](%)" $parameters
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__nfet_01v8_dialog {parameters} {
    sg13g2::mos_dialog sg13g2_fd_pr__nfet_01v8 $parameters
}

proc sg13g2::sg13g2_fd_pr__nfet_01v8_lvt_dialog {parameters} {
    sg13g2::mos_dialog sg13g2_fd_pr__nfet_01v8_lvt $parameters
}

proc sg13g2::sg13g2_fd_bs_flash__special_sonosfet_star_dialog {parameters} {
    sg13g2::mos_dialog sg13g2_fd_bs_flash__special_sonosfet_star $parameters
}

proc sg13g2::sg13g2_fd_pr__nfet_g5v0d10v5_dialog {parameters} {
    sg13g2::mos_dialog sg13g2_fd_pr__nfet_g5v0d10v5 $parameters
}

proc sg13g2::sg13g2_fd_pr__nfet_g5v0d16v0_dialog {parameters} {
    sg13g2::mos_dialog sg13g2_fd_pr__nfet_g5v0d16v0 $parameters
}

proc sg13g2::sg13g2_fd_pr__nfet_05v0_nvt_dialog {parameters} {
    sg13g2::mos_dialog sg13g2_fd_pr__nfet_05v0_nvt $parameters
}

proc sg13g2::sg13g2_fd_pr__nfet_03v3_nvt_dialog {parameters} {
    sg13g2::mos_dialog sg13g2_fd_pr__nfet_03v3_nvt $parameters
}

proc sg13g2::sg13g2_fd_pr__pfet_01v8_dialog {parameters} {
    sg13g2::mos_dialog sg13g2_fd_pr__pfet_01v8 $parameters
}

proc sg13g2::sg13g2_fd_pr__pfet_01v8_lvt_dialog {parameters} {
    sg13g2::mos_dialog sg13g2_fd_pr__pfet_01v8_lvt $parameters
}

proc sg13g2::sg13g2_fd_pr__pfet_01v8_hvt_dialog {parameters} {
    sg13g2::mos_dialog sg13g2_fd_pr__pfet_01v8_hvt $parameters
}

proc sg13g2::sg13g2_fd_pr__pfet_g5v0d10v5_dialog {parameters} {
    sg13g2::mos_dialog sg13g2_fd_pr__pfet_g5v0d10v5 $parameters
}

proc sg13g2::sg13g2_fd_pr__pfet_g5v0d16v0_dialog {parameters} {
    sg13g2::mos_dialog sg13g2_fd_pr__pfet_g5v0d16v0 $parameters
}

proc sg13g2::sg13g2_fd_pr__cap_var_lvt_dialog {parameters} {
    sg13g2::mos_dialog sg13g2_fd_pr__cap_var_lvt $parameters
}

proc sg13g2::sg13g2_fd_pr__cap_var_hvt_dialog {parameters} {
    sg13g2::mos_dialog sg13g2_fd_pr__cap_var_hvt $parameters
}

proc sg13g2::sg13g2_fd_pr__cap_var_dialog {parameters} {
    sg13g2::mos_dialog sg13g2_fd_pr__cap_var $parameters
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
    # orient is the orientation of the contact

    # Set orientations for the bottom material based on material type.
    # Substrate diffusions (tap) need not overlap the contact in all
    # directions, but other (diff) types do.  The metal (local
    # interconnect) layer always overlaps in two directions only.

    set lv_sub_types {"psd" "nsd"}
    if {[lsearch $lv_sub_types $atype] >= 0} {
	set aorient $orient
    } else {
	set aorient "full"
    }

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
    set sub_type	 pwell	;# substrate type

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Set guard_sub_type to sub_type if it is not defined
    if {![dict exists $parameters guard_sub_type]} {
	set guard_sub_type $sub_type
    }

    set hx [/ $contact_size 2.0]
    set hw [/ $gw 2.0]
    set hh [/ $gh 2.0]

    # Watch for (LV) substrate diffusion types, which have a different
    # contact surround amount depending on the direction

    set lv_sub_types {"psd" "nsd"}
    if {[lsearch $lv_sub_types $plus_diff_type] >= 0} {
	set diff_surround 0
    }

    # Compute diffusion width
    set difft [+ $contact_size $diff_surround $diff_surround]
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
	set hmetw [/ [+ $gw $contact_size] 2.0]
	set hmeth [/ [+ $gh $contact_size] 2.0]
	pushbox
	box move n ${hh}um
	box grow n ${hx}um
	box grow s ${hx}um
	box grow e ${hmetw}um
	box grow w ${hmetw}um
	paint li
	popbox
	pushbox
	box move s ${hh}um
	box grow n ${hx}um
	box grow s ${hx}um
	box grow e ${hmetw}um
	box grow w ${hmetw}um
	paint li
	popbox
	pushbox
	box move e ${hw}um
	box grow e ${hx}um
	box grow w ${hx}um
	box grow n ${hmeth}um
	box grow s ${hmeth}um
	paint li
	popbox
	pushbox
	box move w ${hw}um
	box grow e ${hx}um
	box grow w ${hx}um
	box grow n ${hmeth}um
	box grow s ${hmeth}um
	paint li
	popbox
    }

    # Set guard ring height so that contact metal reaches to end, scale by $per
    # set ch [* [+ $gh $contact_size [* $metal_surround -2.0]] [/ $rlcov 100.0]]
    set ch [* [- $gh $contact_size [* [+ $metal_surround $metal_spacing] \
		2.0]] [/ $rlcov 100.0]]
    if {$ch < $contact_size} {set ch $contact_size}

    # Set guard ring width so that contact metal reaches to side contacts
    set cw [* [- $gw $contact_size [* [+ $metal_surround $metal_spacing] \
		2.0]] [/ $tbcov 100.0]]
    if {$cw < $contact_size} {set cw $contact_size}

    if {$tbcov > 0.0} {
        if {$gtc == 1} {
            pushbox
            box move n ${hh}um
            sg13g2::draw_contact $cw 0 $diff_surround $metal_surround \
		$contact_size $plus_diff_type $plus_contact_type li horz
            popbox
	}
	if {$gbc == 1} {
	    pushbox
	    box move s ${hh}um
	    sg13g2::draw_contact $cw 0 $diff_surround $metal_surround \
		$contact_size $plus_diff_type $plus_contact_type li horz
	    popbox
	}
    }
    if {$rlcov > 0.0} {
        if {$grc == 1} {
            pushbox
            box move e ${hw}um
            sg13g2::draw_contact 0 $ch $diff_surround $metal_surround \
		$contact_size $plus_diff_type $plus_contact_type li vert
            popbox
        }
        if {$glc == 1} {
            pushbox
            box move w ${hw}um
            sg13g2::draw_contact 0 $ch $diff_surround $metal_surround \
		$contact_size $plus_diff_type $plus_contact_type li vert
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
	box grow n [/ $ch 2]um
	box grow s [/ $ch 2]um
        set anchor [string index $viagb 0]
	if {$anchor == "+"} {
            box move w [/ [- $gw $via_size] 2]um
	    box grow e ${cw}um
	} elseif {$anchor == "-"} {
            box move e [/ [- $gw $via_size] 2]um
	    box grow w ${cw}um
	} else {
	    box grow e [/ $cw 2]um
	    box grow w [/ $cw 2]um
	}
        sg13g2::mcon_draw horz
        popbox
    }
    if {$viagt != 0} {
        pushbox
    	set ch $via_size
    	set cw [* [- $gw $via_size] [/ [expr abs($viagt)] 100.0]]
    	if {$cw < $via_size} {set cw $via_size}
        box move n ${hh}um
	box grow n [/ $ch 2]um
	box grow s [/ $ch 2]um
        set anchor [string index $viagt 0]
	if {$anchor == "+"} {
            box move w [/ [- $gw $via_size] 2]um
	    box grow e ${cw}um
	} elseif {$anchor == "-"} {
            box move e [/ [- $gw $via_size] 2]um
	    box grow w ${cw}um
	} else {
	    box grow e [/ $cw 2]um
	    box grow w [/ $cw 2]um
	}
        sg13g2::mcon_draw horz
        popbox
    }
    if {$viagr != 0} {
        pushbox
    	set ch [* [- $gh $via_size] [/ [expr abs($viagr)] 100.0]]
    	if {$ch < $via_size} {set ch $via_size}
    	set cw $via_size
        box move e ${hw}um
	box grow e [/ $cw 2]um
	box grow w [/ $cw 2]um
        set anchor [string index $viagr 0]
	if {$anchor == "+"} {
            box move s [/ [- $gh $via_size] 2]um
	    box grow n ${ch}um
	} elseif {$anchor == "-"} {
            box move n [/ [- $gh $via_size] 2]um
	    box grow s ${ch}um
	} else {
	    box grow n [/ $ch 2]um
	    box grow s [/ $ch 2]um
	}
        sg13g2::mcon_draw vert
        popbox
    }
    if {$viagl != 0} {
        pushbox
    	set ch [* [- $gh $via_size] [/ [expr abs($viagl)] 100.0]]
    	if {$ch < $via_size} {set ch $via_size}
    	set cw $via_size
        box move w ${hw}um
	box grow e [/ $cw 2]um
	box grow w [/ $cw 2]um
        set anchor [string index $viagl 0]
	if {$anchor == "+"} {
            box move s [/ [- $gh $via_size] 2]um
	    box grow n ${ch}um
	} elseif {$anchor == "-"} {
            box move n [/ [- $gh $via_size] 2]um
	    box grow s ${ch}um
	} else {
	    box grow n [/ $ch 2]um
	    box grow s [/ $ch 2]um
	}
        sg13g2::mcon_draw vert
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

#----------------------------------------------------------------
# LDNMOS:  Sub-procedure to draw the extended drain
#----------------------------------------------------------------

proc sg13g2::draw_ldnmos_drain {parameters} {

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Need to regenerate some values from mos_device
    set hl [/ $l 2.0]
    set hw [/ $w 2.0]

    # Extension is fixed at 1.585um and we assume a fixed
    # underlap of the gate of 0.13um, which is not in the
    # drawn device, so subtracted from the extension distance.
    set extension 1.455

    pushbox
    # Starts with point at the device center
    box grow n ${hw}um
    box grow s ${hw}um
    box move $dside ${hl}um
    pushbox
    box grow $dside ${extension}um
    paint ed
    set cext [sg13g2::getbox]
    popbox
    box move $dside ${extension}um
    box move $dside 0.13um
    box grow e 0.13um
    box grow w 0.13um
    paint mvnsd
    # Test:  Do not include nwell in bounding box
    set cext [sg13g2::unionbox $cext [sg13g2::getbox]]
    pushbox
    box grow c 0.66um
    paint nwell
    popbox
    popbox
    # Back to the center point
    pushbox
    box move $dside ${hl}um
    box move $dside ${extension}um
    box move $dside 0.13um

    # Drain via on top of contact
    set viatype $viadrn
    if {$viatype != 0} {
        pushbox
        set cw $via_size
    	set ch [* $cdwfull [/ [expr abs($viatype)] 100.0]]
    	if {$ch < $via_size} {set ch $via_size}
	box grow $dside [/ $cw 2]um
	box grow $sside [/ $cw 2]um
        set anchor [string index $viatype 0]
	if {$anchor == "+"} {
            box move s [/ [- $cdwfull $via_size] 2]um
	    box grow n ${ch}um
	} elseif {$anchor == "-"} {
            box move n [/ [- $cdwfull $via_size] 2]um
	    box grow s ${ch}um
	} else {
	    box grow n [/ $ch 2]um
	    box grow s [/ $ch 2]um
	}
	sg13g2::mcon_draw vert
	popbox
    }
    # cdwfull was calculated for the source side and is too long for
    # the drain side by 0.06um on top and bottom.
    set cdwfull [- $cdwfull 0.12]
    if {$cdw > $cdwfull} [set cdw $cdwfull]

    set cext [sg13g2::unionbox $cext [sg13g2::draw_contact 0 ${cdw} \
		${drain_diff_surround} ${metal_surround} ${contact_size}\
		mvnsd mvnsc li vert]]
    popbox
    return $cext
}

#----------------------------------------------------------------
# LDPMOS:  Sub-procedure to draw the extended drain
#----------------------------------------------------------------

proc sg13g2::draw_ldpmos_drain {parameters} {

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Need to regenerate some values from mos_device
    set hl [/ $l 2.0]
    set hw [/ $w 2.0]

    # Extension is fixed at 1.19um and we assume a fixed
    # underlap of the gate of 0.13um, which is not in the
    # drawn device, so subtracted from the extension distance.
    set extension 1.06

    pushbox
    # Starts with point at the device center
    box grow n ${hw}um
    box grow s ${hw}um
    box move $dside ${hl}um
    pushbox
    box grow $dside ${extension}um
    paint ed
    set cext [sg13g2::getbox]
    popbox
    box move $dside ${extension}um
    box move $dside 0.13um
    box grow e 0.13um
    box grow w 0.13um
    paint mvpsd
    pushbox
    box grow c 0.86um
    # Shorter than necessary to avoid DRC error;  actual
    # nwell is erased under gate by GDS generation rules.
    box grow e -0.15um
    box grow w -0.15um
    paint pwell
    popbox
    popbox
    # Back to the center point
    pushbox
    box move $dside ${hl}um
    box move $dside ${extension}um
    box move $dside 0.13um

    # Drain via on top of contact
    set viatype $viadrn
    if {$viatype != 0} {
        pushbox
        set cw $via_size
    	set ch [* $cdwfull [/ [expr abs($viatype)] 100.0]]
    	if {$ch < $via_size} {set ch $via_size}
	box grow $dside [/ $cw 2]um
	box grow $sside [/ $cw 2]um
        set anchor [string index $viatype 0]
	if {$anchor == "+"} {
            box move s [/ [- $cdwfull $via_size] 2]um
	    box grow n ${ch}um
	} elseif {$anchor == "-"} {
            box move n [/ [- $cdwfull $via_size] 2]um
	    box grow s ${ch}um
	} else {
	    box grow n [/ $ch 2]um
	    box grow s [/ $ch 2]um
	}
	sg13g2::mcon_draw vert
	popbox
    }
    # cdwfull was calculated for the source side and is too long for
    # the drain side by 0.06um on top and bottom.
    set cdwfull [- $cdwfull 0.12]
    if {$cdw > $cdwfull} [set cdw $cdwfull]

    set cext [sg13g2::unionbox $cext [sg13g2::draw_contact 0 ${cdw} \
		${drain_diff_surround} ${metal_surround} ${contact_size}\
		mvpsd mvpsc li vert]]
    popbox
    return $cext
}

#----------------------------------------------------------------
# MOSFET: Draw a single device
#----------------------------------------------------------------

proc sg13g2::mos_device {parameters} {

    # Epsilon for avoiding round-off errors
    set eps  0.0005

    # Set local default values if they are not in parameters
    set diffcov 100	;# percent coverage of diffusion contact
    set polycov 100	;# percent coverage of poly contact
    set topc 1		;# draw top poly contact
    set botc 1		;# draw bottom poly contact
    set viasrc 100	;# draw source vias
    set viadrn 100	;# draw drain vias
    set viagate 100	;# draw gate vias
    set evens 1		;# even or odd (evens = 1 means drain is on the left)
    set dev_sub_type ""	;# device substrate type (if different from guard ring)
    set dev_sub_dist 0	;# device substrate distance (if nondefault dev_sub_type)
    set min_effl 0	;# gate length below which finger pitch must be stretched
    set diff_overlap_cont 0	;# extra overlap of end contact by diffusion
    set gshield 0	;# no metal shield over gate (used for varactors)
    set drain_proc {}	;# no special procedure to draw the drain

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Draw the diffusion and poly
    pushbox
    box size 0 0
    pushbox
    set hw [/ $w 2.0]
    set hl [/ $l 2.0]
    set he [/ $min_effl 2.0]
    if {$nf == 1 || $he < $hl} {set he $hl}
    box grow n ${hw}um
    box grow s ${hw}um
    box grow e ${hl}um
    box grow w ${hl}um

    # Set drain and source sides based on "evens".
    if {$evens == 0} {
	set dside e
	set sside w
    } else {
	set dside w
	set sside e
    }

    pushbox
    if {${diff_extension} > ${gate_to_diffcont}} {
        box grow $dside ${diff_extension}um
        box grow $sside ${diff_extension}um
    } else {
        box grow $dside ${gate_to_diffcont}um
        box grow $sside ${gate_to_diffcont}um
    }
    paint ${diff_type}
    popbox
    pushbox
    if {${gate_extension} > ${gate_to_polycont}} {
	box grow n ${gate_extension}um
	box grow s ${gate_extension}um
    } else {
	if {$topc} {
	    box grow n ${gate_to_polycont}um
	} else {
	    box grow n ${gate_extension}um
	}
	if {$botc} {
	    box grow s ${gate_to_polycont}um
	} else {
	    box grow s ${gate_extension}um
	}
    }
    paint ${poly_type}
    set cext [sg13g2::getbox]
    popbox
    # save gate area now and paint later, so that diffusion surrounding the
    # contact does not paint over the gate area, in case the gate type is
    # not part of a "compose" entry in the techfile.
    set gaterect [box values]
    popbox

    # Adjust position of contacts for dogbone geometry
    # Rule 1: Minimize diffusion length.  Contacts only move out
    # if width <  contact diffusion height.  They move out enough
    # that the diffusion-to-poly spacing is satisfied.

    set ddover 0
    set cdwmin [+ ${contact_size} [* ${diff_surround} 2]]
    set cstem [- ${gate_to_diffcont} [/ ${cdwmin} 2.0]]
    set cgrow [- ${diff_poly_space} ${cstem}]
    if {[+ ${w} ${eps}] < ${cdwmin}} {
        if {${cgrow} > 0} {
            set gate_to_diffcont [+ ${gate_to_diffcont} ${cgrow}]
        }
	set ddover [/ [- ${cdwmin} ${w}] 2.0]
    }

    # Rule 2: Minimum poly width.  Poly contacts only move out
    # if length < contact poly width.  They move out enough
    # that the diffusion-to-poly spacing is satisfied.

    set gporig ${gate_to_polycont}
    set cplmin [+ ${contact_size} [* ${poly_surround} 2]]
    set cstem [- ${gate_to_polycont} [/ ${cplmin} 2.0]]
    set cgrow [- ${diff_poly_space} ${cstem}]
    if {[+ ${l} ${eps}] < ${cplmin}} {
        if {${cgrow} > 0} {
            set gate_to_polycont [+ ${gate_to_polycont} ${cgrow}]
        }
    }

    # Rule 3: If both poly and diffusion are dogboned, then move
    # poly out further to clear spacing to the diffusion contact

    if {[+ ${w} ${eps}] < ${cdwmin}} {
        if {[+ ${l} ${eps}] < ${cplmin}} {
            set cgrow [/ [- ${cplmin} ${w}] 2.0]
            set gate_to_polycont [+ ${gate_to_polycont} ${cgrow}]
        }
    }

    # Rule 4: If M > 1 and poly contacts overlap, then increase the
    # transistor-to-poly-contact distance by the amount of any
    # diffusion dogbone overhang.

    if {($poverlap == 1) && ($m > 1)} {
	if {${gate_to_polycont} - $gporig < $ddover} {
	    set gate_to_polycont [+ ${gporig} ${ddover}]
	}
    }

    # Reduce contact sizes by poly or diffusion surround so that
    # the contact area edges match the device diffusion or poly.
    # (Minimum dimensions will be enforced by the contact drawing routine)
    set tsurround [+ ${diff_surround} ${diff_overlap_cont}]
    set cdw [- ${w} [* ${tsurround} 2]]		;# diff contact height
    set cpl [- ${l} [* ${poly_surround} 2]]     ;# poly contact width

    # Save the full diffusion (source/drain) and poly (gate) lengths
    set cdwfull $cdw
    set cplfull $cpl

    # Reduce by coverage percentage.  NOTE:  If overlapping multiple devices,
    # keep maximum poly contact coverage.

    set cdw [* ${cdw} [/ ${diffcov} 100.0]]
    if {($poverlap == 0) || ($m == 1)} {
	set cpl [* ${cpl} [/ ${polycov} 100.0]]
    }

    if {$drain_proc != {}} {
	# Add variables to the parameters dictionary that we'll need
	dict set parameters cdw $cdw
	dict set parameters cdwfull $cdwfull
	dict set parameters dside $dside
	dict set parameters sside $sside
	set cext [sg13g2::unionbox $cext [eval $drain_proc {$parameters}]]
    } else {
	# Drain diffusion contact
	pushbox
	box move $dside ${he}um
	box move $dside ${gate_to_diffcont}um

	# Drain via on top of contact
	set viatype $viadrn
	if {$viatype != 0} {
            pushbox
            set cw $via_size
    	    set ch [* $cdwfull [/ [expr abs($viatype)] 100.0]]
    	    if {$ch < $via_size} {set ch $via_size}
	    box grow $dside [/ $cw 2]um
	    box grow $sside [/ $cw 2]um
            set anchor [string index $viatype 0]
	    if {$anchor == "+"} {
        	box move s [/ [- $cdwfull $via_size] 2]um
		box grow n ${ch}um
	    } elseif {$anchor == "-"} {
        	box move n [/ [- $cdwfull $via_size] 2]um
		box grow s ${ch}um
	    } else {
		box grow n [/ $ch 2]um
		box grow s [/ $ch 2]um
	    }
	    sg13g2::mcon_draw vert
	    popbox
	}
	set cext [sg13g2::unionbox $cext [sg13g2::draw_contact 0 ${cdw} \
		${diff_surround} ${metal_surround} ${contact_size}\
		${diff_type} ${diff_contact_type} li vert]]
	popbox
    }

    # Source diffusion contact
    pushbox
    box move $sside ${he}um
    box move $sside ${gate_to_diffcont}um

    # Source via on top of contact
    set viatype $viasrc
    if {$viatype != 0} {
        pushbox
        set cw $via_size
    	set ch [* $cdwfull [/ [expr abs($viatype)] 100.0]]
    	if {$ch < $via_size} {set ch $via_size}
	box grow $sside [/ $cw 2]um
	box grow $dside [/ $cw 2]um
        set anchor [string index $viatype 0]
	if {$anchor == "+"} {
            box move s [/ [- $cdwfull $via_size] 2]um
	    box grow n ${ch}um
	} elseif {$anchor == "-"} {
            box move n [/ [- $cdwfull $via_size] 2]um
	    box grow s ${ch}um
	} else {
	    box grow n [/ $ch 2]um
	    box grow s [/ $ch 2]um
	}
        sg13g2::mcon_draw vert
        popbox
    }
    set cext [sg13g2::unionbox $cext [sg13g2::draw_contact 0 ${cdw} \
		${diff_surround} ${metal_surround} ${contact_size} \
		${diff_type} ${diff_contact_type} li vert]]
    set diffarea $cext
    popbox
    # Gate shield (only on varactors)
    if {$gshield == 1} {
 	pushbox
	box move w ${he}um
	box move w ${gate_to_diffcont}um
	box width [* 2 [+ ${he} ${gate_to_diffcont}]]um
	box grow n [/ $cdwfull 2]um
	box grow s [/ $cdwfull 2]um
	paint m1
	# Enforce slotting of large metal
	set gsh [magic::i2u [box height]]
	if {$gsh > 25} {
	   box move n [/ $gsh 2]um
	   box move s 1.15um
	   box height 2.3um	;# Minimum m1 slot width
	   box grow w -${via_size}um
	   box grow e -${via_size}um
	   erase m1
	}
	popbox
    }
    # Top poly contact
    if {$topc} {
       pushbox
       box move n ${hw}um
       box move n ${gate_to_polycont}um

       # Gate via on top of contact
       if {$viagate != 0} {
           pushbox
    	   set ch $via_size
    	   set cw [* $cplfull [/ [expr abs($viagate)] 100.0]]
    	   if {$cw < $via_size} {set cw $via_size}
	   box grow n [/ $ch 2]um
	   box grow s [/ $ch 2]um
           set anchor [string index $viagate 0]
	   if {$anchor == "+"} {
               box move w [/ [- $cplfull $via_size] 2]um
	       box grow e ${cw}um
	   } elseif {$anchor == "-"} {
               box move e [/ [- $cplfull $via_size] 2]um
	       box grow w ${cw}um
	   } else {
	       box grow e [/ $cw 2]um
	       box grow w [/ $cw 2]um
	   }
           sg13g2::mcon_draw horz
           popbox
       }
       set cext [sg13g2::unionbox $cext [sg13g2::draw_contact ${cpl} 0 \
		${poly_surround} ${metal_surround} ${contact_size} \
		${poly_type} ${poly_contact_type} li horz]]
       popbox
    }
    # Bottom poly contact
    if {$botc} {
       pushbox
       box move s ${hw}um
       box move s ${gate_to_polycont}um

       # Gate via on top of contact
       if {$viagate != 0} {
           pushbox
    	   set ch $via_size
    	   set cw [* $cplfull [/ [expr abs($viagate)] 100.0]]
    	   if {$cw < $via_size} {set cw $via_size}
	   box grow n [/ $ch 2]um
	   box grow s [/ $ch 2]um
           set anchor [string index $viagate 0]
	   if {$anchor == "+"} {
               box move w [/ [- $cplfull $via_size] 2]um
	       box grow e ${cw}um
	   } elseif {$anchor == "-"} {
               box move e [/ [- $cplfull $via_size] 2]um
	       box grow w ${cw}um
	   } else {
	       box grow e [/ $cw 2]um
	       box grow w [/ $cw 2]um
	   }
           sg13g2::mcon_draw horz
           popbox
       }
       set cext [sg13g2::unionbox $cext [sg13g2::draw_contact ${cpl} 0 \
		${poly_surround} ${metal_surround} ${contact_size} \
		${poly_type} ${poly_contact_type} li horz]]
       popbox
    }

    # Now draw the gate, after contacts have been drawn
    pushbox
    box values {*}${gaterect}
    # gate_type need not be defined if poly over diff paints the right type.
    catch {paint ${gate_type}}
    # sub_surround_dev, if defined, may create a larger area around the gate
    # than sub_surround creates around the diffusion/poly area.
    if [dict exists $parameters sub_surround_dev] {
	box grow n ${sub_surround_dev}um
	box grow s ${sub_surround_dev}um
	box grow e ${sub_surround_dev}um
	box grow w ${sub_surround_dev}um
	paint ${dev_sub_type}
	set cext [sg13g2::unionbox $cext [sg13g2::getbox]]
    }
    popbox

    if {$dev_sub_type != ""} {
	box values [lindex $diffarea 0]um [lindex $diffarea 1]um \
	    [lindex $diffarea 2]um [lindex $diffarea 3]um
	box grow n ${sub_surround}um
	box grow s ${sub_surround}um
	box grow e ${sub_surround}um
	box grow w ${sub_surround}um
	paint ${dev_sub_type}
	if {$dev_sub_dist > 0} {
	    set cext [sg13g2::unionbox $cext [sg13g2::getbox]]
	}
        # puts stdout "Diagnostic:  bounding box is $cext"
    }

    popbox
    return $cext
}

#----------------------------------------------------------------
# MOSFET: Draw the tiled device
#----------------------------------------------------------------

proc sg13g2::mos_draw {parameters} {
    tech unlock *
    set savesnap [snap]
    snap internal

    # Set defaults if they are not in parameters
    set poverlap 0	;# overlap poly contacts when tiling
    set doverlap 1	;# overlap diffusion contacts when tiling
    set dev_sub_dist 0	;# substrate to guard ring, if dev_sub_type defined
    set dev_sub_space 0	;# distance between substrate areas for arrayed devices
    set min_allc 0	;# gate length below which poly contacts must be interleaved
    set id_type ""	;# additional type covering everything
    set id_surround 0	;# amount of surround on above type
    set id2_type ""	;# additional type covering everything
    set id2_surround 0	;# amount of surround on above type

    set set_x_to_guard ""	;# override x distance to guard ring
    set set_y_to_guard ""	;# override y distance to guard ring

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Diff surround on drain is by default the same as diff surround
    if {![dict exist $parameters drain_diff_surround]} {
	set drain_diff_surround $diff_surround
    }

    # Diff-to-tap spacing is by default the same as diff spacing
    if {![dict exist $parameters diff_tap_space]} {
	set diff_tap_space $diff_spacing
    }

    # If poverlap is 1 then both poly contacts must be present
    if {$poverlap == 1} {
	set topc 1
	set botc 1
	dict set parameters topc 1
	dict set parameters botc 1
    }

    # Normalize distance units to microns
    set w [magic::spice2float $w]
    set l [magic::spice2float $l]

    pushbox
    box values 0 0 0 0

    # If dx < (poly contact space + poly contact width), then there is not
    # enough room for a row of contacts, so force alternating contacts

    set evens 1
    if {$nf > 1 && $l < $min_allc} {
	set intc 1
	set evenodd 1
	set topc 1
	set botc 1
	dict set parameters topc 1
	dict set parameters botc 1
	set poverlap 0
    } else {
	set intc 0
    }

    # Determine the base device dimensions by drawing one device
    # while all layers are locked (nothing drawn).  This allows the
    # base drawing routine to do complicated geometry without having
    # to duplicate it here with calculations.

    tech lock *
    set bbox [sg13g2::mos_device $parameters]
    puts stdout "Diagnostic: Device bounding box e $bbox (um)"
    tech unlock *

    set fw [- [lindex $bbox 2] [lindex $bbox 0]]
    set fh [- [lindex $bbox 3] [lindex $bbox 1]]
    set lw [+ [lindex $bbox 2] [lindex $bbox 0]]
    set lh [+ [lindex $bbox 3] [lindex $bbox 1]]

    # If the bounding box is not symmetric about x=0, then find the
    # offset.  Assumed to be needed only for X (asymmetric drain)
    set xoffset [+ [lindex $bbox 0] [lindex $bbox 2]]
    
    # If dev_sub_dist > 0 then each device must be in its own substrate
    # (well) area, and overlaps are disallowed.  dev_sub_space determines
    # the distance between individual devices in an array.

    if {$dev_sub_dist > 0} {
        set poverlap 0
        set doverlap 0

	if {$dev_sub_space > $poly_spacing} {
	    set dx [+ $fw $dev_sub_space]
	    set dy [+ $fh $dev_sub_space]
	} else {
	    set dx [+ $fw $poly_spacing]
	    set dy [+ $fh $poly_spacing]
	}

    } else {

	# Determine tile width and height (depends on overlap)
	if {$poverlap == 0} {
	    set dy [+ $fh $poly_spacing]
	} else {
	    # overlap poly
	    set dy [- $fh [+ $poly_surround $poly_surround $contact_size]]
	}

	if {$doverlap == 0} {
	    set dx [+ $fw $diff_spacing]
	} else {
	    # overlap diffusions
	    set dx [- $fw [+ $drain_diff_surround $drain_diff_surround $contact_size]]
	}
    }

    # Determine core width and height
    set corex [+ [* [- $nf 1] $dx] $fw]
    set corey [+ [* [- $m 1] $dy] $fh]
    set corellx [/ [+ [- $corex $fw] $lw] 2.0]
    set corelly [/ [+ [- $corey $fh] $lh] 2.0]

    # If there is a diffusion dogbone, and no top poly contact, then
    # increase the core height by the amount of the dogbone overhang.

    if {$topc == 0} {
	set cdwmin [+ ${contact_size} [* ${diff_surround} 2]]
	if {${w} < ${cdwmin}} {
	    set corey [+ $corey [/ [- ${cdwmin} ${w}] 2.0]]
	}
    }

    # Calculate guard ring size (measured to contact center)
    if {($guard != 0) || (${id_type} != "")} {
	if {($dev_sub_dist > 0) && ([+ $dev_sub_dist $sub_surround] > $diff_tap_space)} {
	    set gx [+ $corex [* 2.0 [+ $dev_sub_dist $diff_surround]] $contact_size]
	} else {
	    set gx [+ $corex [* 2.0 [+ $diff_tap_space $diff_surround]] $contact_size]
	}
	if {($dev_sub_dist > 0) && ([+ $dev_sub_dist $sub_surround] > $diff_gate_space)} {
	    set gy [+ $corey [* 2.0 [+ $dev_sub_dist $diff_surround]] $contact_size]
	} else {
	    set gy [+ $corey [* 2.0 [+ $diff_gate_space $diff_surround]] $contact_size]
	}

	# Somewhat tricky. . . if the width is small and the diffusion is 
	# a dogbone, and the top or bottom poly contact is missing, then
	# the spacing to the guard ring may be limited by diffusion spacing, not
	# poly to diffusion.

	set inset [/ [+ $contact_size [* 2.0 $diff_surround] -$w] 2.0]
	set sdiff [- [+ $inset $diff_tap_space] [+ $gate_extension $diff_gate_space]]

	if {$sdiff > 0} {
	    if {$topc == 0} {
		set gy [+ $gy $sdiff]
		set corelly [+ $corelly [/ $sdiff 2.0]]
	    }
	    if {$botc == 0} {
		set gy [+ $gy $sdiff]
		set corelly [- $corelly [/ $sdiff 2.0]]
	    }
	}

	# set_x|y_to_guard overrides the above calculations if present.
	if {$set_x_to_guard != ""} {
	    set gx [+ $corex [* 2.0 $set_x_to_guard]]
	}
	if {$set_y_to_guard != ""} {
	    set gy [+ $corey [* 2.0 $set_y_to_guard]]
	}
    }
    if {$guard != 0} {
	# Draw the guard ring first, as MOS well may interact with guard ring substrate
	sg13g2::guard_ring $gx $gy $parameters
    }

    pushbox
    # If any surrounding identifier type is defined, draw it
    if {${id_type} != ""} {
	set hw [/ $gx 2]
	set hh [/ $gy 2]
	box grow e ${hw}um
	box grow w ${hw}um
	box grow n ${hh}um
	box grow s ${hh}um
	box grow c ${id_surround}um
	paint ${id_type}
    }
    popbox
    pushbox
    box move w ${corellx}um
    box move s ${corelly}um
    for {set xp 0} {$xp < $nf} {incr xp} {
	dict set parameters evens $evens
	set evens [- 1 $evens]
        pushbox
	if {$intc == 1} {
	    set evenodd [- 1 $evenodd]
	    if {$evenodd == 1} {
		dict set parameters topc 1
		dict set parameters botc 0
	    } else {
		dict set parameters topc 0
		dict set parameters botc 1
	    }
	    set saveeo $evenodd
	}
        for {set yp 0} {$yp < $m} {incr yp} {
            if {$evens != 0} {box move e ${xoffset}um}
            sg13g2::mos_device $parameters
            if {$evens != 0} {box move w ${xoffset}um}
            box move n ${dy}um
	    if {$intc == 1} {
		set evenodd [- 1 $evenodd]
		if {$evenodd == 1} {
		    dict set parameters topc 1
		    dict set parameters botc 0
		} else {
		    dict set parameters topc 0
		    dict set parameters botc 1
		}
	    }
        }
	if {$intc == 1} {
	    set evenodd $saveeo
	}
        popbox
        box move e ${dx}um
    }
    popbox
    popbox

    snap $savesnap
    tech revert
}

#-------------------
# nMOS 1.8V
#-------------------

proc sg13g2::sg13g2_fd_pr__nfet_01v8_draw {parameters} {
    set newdict [dict create \
	    gate_type		nfet \
	    diff_type 		ndiff \
	    diff_contact_type	ndc \
	    plus_diff_type	psd \
	    plus_contact_type	psc \
	    poly_type		poly \
	    poly_contact_type	pc \
	    sub_type		psub \
	    min_effl		0.185 \
	    min_allc		0.26 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::mos_draw $drawdict]
}

proc sg13g2::sg13g2_fd_pr__nfet_01v8_lvt_draw {parameters} {
    set newdict [dict create \
	    gate_type		nfetlvt \
	    diff_type 		ndiff \
	    diff_contact_type	ndc \
	    plus_diff_type	psd \
	    plus_contact_type	psc \
	    poly_type		poly \
	    poly_contact_type	pc \
	    sub_type		psub \
	    min_effl		0.185 \
	    min_allc		0.26 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::mos_draw $drawdict]
}

proc sg13g2::sg13g2_fd_bs_flash__special_sonosfet_star_draw {parameters} {
    set newdict [dict create \
	    gate_type		nsonos \
	    diff_type 		ndiff \
	    diff_contact_type	ndc \
	    plus_diff_type	psd \
	    plus_contact_type	psc \
	    poly_type		poly \
	    poly_contact_type	pc \
	    sub_type		psub \
	    id_type		dnwell \
	    id_surround		1.355 \
	    min_effl		0.185 \
	    min_allc		0.26 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::mos_draw $drawdict]
}

#-------------------
# pMOS 1.8V
#-------------------

proc sg13g2::sg13g2_fd_pr__pfet_01v8_draw {parameters} {
    set newdict [dict create \
	    gate_type		pfet \
	    diff_type 		pdiff \
	    diff_contact_type	pdc \
	    plus_diff_type	nsd \
	    plus_contact_type	nsc \
	    poly_type		poly \
	    poly_contact_type	pc \
	    sub_type		nwell \
	    dev_sub_type	nwell \
	    gate_to_polycont	0.32 \
	    min_effl		0.185 \
	    min_allc		0.26 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::mos_draw $drawdict]
}

proc sg13g2::sg13g2_fd_pr__pfet_01v8_lvt_draw {parameters} {
    set newdict [dict create \
	    gate_type		pfetlvt \
	    diff_type 		pdiff \
	    diff_contact_type	pdc \
	    plus_diff_type	nsd \
	    plus_contact_type	nsc \
	    poly_type		poly \
	    poly_contact_type	pc \
	    sub_type		nwell \
	    dev_sub_type	nwell \
	    gate_to_polycont	0.32 \
	    min_effl		0.185 \
	    min_allc		0.26 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::mos_draw $drawdict]
}

proc sg13g2::sg13g2_fd_pr__pfet_01v8_hvt_draw {parameters} {
    set newdict [dict create \
	    gate_type		pfethvt \
	    diff_type 		pdiff \
	    diff_contact_type	pdc \
	    plus_diff_type	nsd \
	    plus_contact_type	nsc \
	    poly_type		poly \
	    poly_contact_type	pc \
	    sub_type		nwell \
	    dev_sub_type	nwell \
	    gate_to_polycont	0.32 \
	    min_effl		0.185 \
	    min_allc		0.26 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::mos_draw $drawdict]
}

#-------------------
# pMOS 5.0V
#-------------------

proc sg13g2::sg13g2_fd_pr__pfet_g5v0d10v5_draw {parameters} {
    set newdict [dict create \
	    gate_type		mvpfet \
	    diff_type 		mvpdiff \
	    diff_contact_type	mvpdc \
	    plus_diff_type	mvnsd \
	    plus_contact_type	mvnsc \
	    poly_type		poly \
	    poly_contact_type	pc \
	    sub_type		nwell \
	    dev_sub_type	nwell \
	    guard_sub_surround	0.33 \
	    gate_to_polycont	0.32 \
	    diff_spacing	0.31 \
	    diff_tap_space	0.38 \
	    diff_gate_space	0.38 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::mos_draw $drawdict]
}

#-------------------
# nMOS 5.0V
#-------------------

proc sg13g2::sg13g2_fd_pr__nfet_g5v0d10v5_draw {parameters} {
    set newdict [dict create \
	    gate_type		mvnfet \
	    diff_type 		mvndiff \
	    diff_contact_type	mvndc \
	    plus_diff_type	mvpsd \
	    plus_contact_type	mvpsc \
	    poly_type		poly \
	    poly_contact_type	pc \
	    sub_type		psub \
	    diff_spacing	0.31 \
	    diff_tap_space	0.38 \
	    diff_gate_space	0.38 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::mos_draw $drawdict]
}

proc sg13g2::sg13g2_fd_pr__nfet_05v0_nvt_draw {parameters} {
    set newdict [dict create \
	    gate_type		mvnnfet \
	    diff_type 		mvndiff \
	    diff_contact_type	mvndc \
	    plus_diff_type	mvpsd \
	    plus_contact_type	mvpsc \
	    poly_type		poly \
	    poly_contact_type	pc \
	    sub_type		psub \
	    diff_spacing	0.30 \
	    diff_tap_space	0.38 \
	    diff_gate_space	0.38 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::mos_draw $drawdict]
}

proc sg13g2::sg13g2_fd_pr__nfet_03v3_nvt_draw {parameters} {
    set newdict [dict create \
	    gate_type		nnfet \
	    diff_type 		mvndiff \
	    diff_contact_type	mvndc \
	    plus_diff_type	mvpsd \
	    plus_contact_type	mvpsc \
	    poly_type		poly \
	    poly_contact_type	pc \
	    sub_type		psub \
	    diff_spacing	0.30 \
	    diff_tap_space	0.38 \
	    diff_gate_space	0.38 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::mos_draw $drawdict]
}

#------------------------
# MOS varactor (1.8V)
#------------------------

proc sg13g2::sg13g2_fd_pr__cap_var_lvt_draw {parameters} {
    set newdict [dict create \
	    gate_type		var \
	    diff_type 		nnd \
	    diff_contact_type	nsc \
	    plus_diff_type	psd \
	    plus_contact_type	psc \
	    poly_type		poly \
	    poly_contact_type	pc \
	    sub_type		psub \
	    dev_sub_type	nwell \
	    diff_overlap_cont	0.06 \
	    dev_sub_dist	0.14 \
	    dev_sub_space	1.27 \
	    gate_to_diffcont	0.34 \
	    diff_extension	0.485 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::mos_draw $drawdict]
}

proc sg13g2::sg13g2_fd_pr__cap_var_hvt_draw {parameters} {
    set newdict [dict create \
	    gate_type		varhvt \
	    diff_type 		nnd \
	    diff_contact_type	nsc \
	    plus_diff_type	psd \
	    plus_contact_type	psc \
	    poly_type		poly \
	    poly_contact_type	pc \
	    sub_type		psub \
	    dev_sub_type	nwell \
	    diff_overlap_cont	0.06 \
	    dev_sub_dist	0.14 \
	    dev_sub_space	1.27 \
	    gate_to_diffcont	0.34 \
	    diff_extension	0.485 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::mos_draw $drawdict]
}

#---------------------------------------------------------
# MOS varactor (5.0V)
# NOTE:  dev_sub_space set to 2.0 assuming different nets.
# Should have option for same-net with merged wells.
#---------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__cap_var_draw {parameters} {
    set newdict [dict create \
	    gate_type		mvvar \
	    diff_type 		mvnsd \
	    diff_contact_type	mvnsc \
	    plus_diff_type	mvpsd \
	    plus_contact_type	mvpsc \
	    poly_type		poly \
	    poly_contact_type	pc \
	    sub_type		psub \
	    dev_sub_type	nwell \
	    sub_surround	0.38 \
	    sub_surround_dev	0.56 \
	    guard_sub_surround	0.18 \
	    diff_overlap_cont	0.06 \
	    dev_sub_dist	0.785 \
	    dev_sub_space	2.0 \
	    gate_to_diffcont	0.34 \
	    diff_extension	0.485 \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::mos_draw $drawdict]
}

#----------------------------------------------------------------
# 16V extended-drain devices LDNMOS and LDPMOS
#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__nfet_g5v0d16v0_draw {parameters} {
    set newdict [dict create \
	    gate_type		mvnfet \
	    diff_type 		mvndiff \
	    diff_contact_type	mvndc \
	    plus_diff_type	mvpsd \
	    plus_contact_type	mvpsc \
	    poly_type		poly \
	    poly_contact_type	pc \
	    sub_type		psub \
	    diff_spacing	0.31 \
	    diff_tap_space	0.38 \
	    diff_gate_space	0.38 \
	    drain_diff_surround 0.045 \
	    set_x_to_guard	1.665 \
	    set_y_to_guard	1.225 \
	    drain_proc		sg13g2::draw_ldnmos_drain \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::mos_draw $drawdict]
}

proc sg13g2::sg13g2_fd_pr__pfet_g5v0d16v0_draw {parameters} {
    set newdict [dict create \
	    gate_type		mvpfet \
	    diff_type 		mvpdiff \
	    diff_contact_type	mvpdc \
	    plus_diff_type	mvnsd \
	    plus_contact_type	mvnsc \
	    poly_type		poly \
	    poly_contact_type	pc \
	    sub_type		nwell \
	    id_type		nwell \
	    id_surround		0.035 \
	    guard_sub_surround	0.33 \
	    gate_to_polycont	0.32 \
	    diff_spacing	0.31 \
	    diff_tap_space	0.38 \
	    diff_gate_space	0.38 \
	    drain_diff_surround 0.045 \
	    set_x_to_guard	1.665 \
	    set_y_to_guard	1.180 \
	    drain_proc		sg13g2::draw_ldpmos_drain \
    ]
    set drawdict [dict merge $sg13g2::ruleset $newdict $parameters]
    return [sg13g2::mos_draw $drawdict]
}

#----------------------------------------------------------------
# MOSFET: Check device parameters for out-of-bounds values
#----------------------------------------------------------------

proc sg13g2::mos_check {device parameters} {

    # Set a local variable for each parameter (e.g., $l, $w, etc.)
    foreach key [dict keys $parameters] {
        set $key [dict get $parameters $key]
    }

    # Normalize distance units to microns
    set l [magic::spice2float $l] 
    set l [magic::3digitpastdecimal $l]
    set w [magic::spice2float $w] 
    set w [magic::3digitpastdecimal $w]

    # nf, m must be integer
    if {![string is int $nf]} {
	puts stderr "NF must be an integer!"
        dict set parameters nf 1
    }
    if {![string is int $m]} {
	puts stderr "M must be an integer!"
        dict set parameters m 1
    }
    # diffcov, polycov must be numeric
    if {[catch {expr abs($diffcov)}]} {
	puts stderr "diffcov must be numeric!"
	set diffcov 100
	dict set parameters diffcov $diffcov
    }
    if {[catch {expr abs($polycov)}]} {
	puts stderr "polycov must be numeric!"
	set polycov 100
	dict set parameters polycov $polycov
    }

    if {$l < $lmin} {
	puts stderr "Mos length must be >= $lmin um"
        dict set parameters l $lmin
    } 
    if {$w < $wmin} {
	puts stderr "Mos width must be >= $wmin um"
        dict set parameters w $wmin
    } 
    if {$nf < 1} {
	puts stderr "NF must be >= 1"
        dict set parameters nf 1
    } 
    if {$m < 1} {
	puts stderr "M must be >= 1"
        dict set parameters m 1
    } 
    if {$diffcov < 20 } {
	puts stderr "Diffusion contact coverage must be at least 20%"
        dict set parameters diffcov 20
    } elseif {$diffcov > 100 } {
	puts stderr "Diffusion contact coverage can't be more than 100%"
        dict set parameters diffcov 100
    }
    if {$polycov < 20 } {
	puts stderr "Poly contact coverage must be at least 20%"
        dict set parameters polycov 20
    } elseif {$polycov > 100 } {
	puts stderr "Poly contact coverage can't be more than 100%"
        dict set parameters polycov 100
    }

    if {[catch {expr abs($viasrc)}]} {
	puts stderr "Source via coverage must be numeric!"
        dict set parameters viasrc 100
    } elseif {[expr abs($viasrc)] > 100} {
	puts stderr "Source via coverage can't be more than 100%"
        dict set parameters viasrc 100
    }
    if {[catch {expr abs($viadrn)}]} {
	puts stderr "Drain via coverage must be numeric!"
        dict set parameters viadrn 100
    } elseif {[expr abs($viadrn)] > 100} {
	puts stderr "Drain via coverage can't be more than 100%"
        dict set parameters viadrn 100
    }
    if {[catch {expr abs($viagate)}]} {
	puts stderr "Gate via coverage must be numeric!"
        dict set parameters viagate 100
    } elseif {[expr abs($viagate)] > 100} {
	puts stderr "Gate via coverage can't be more than 100%"
        dict set parameters viagate 100
    }
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

    # Values must satisfy diffusion-to-tap spacing of 15um.
    # Therefore the maximum of guard ring width or height cannot exceed 30um.
    # This requires detailed knowledge of the layout, so can only be estimated
    # here.  Since the estimate may be off, do not enforce the rule but just
    # generate a warning.

    # "clearance" is an estimation of the amount of space taken up by the
    # gate or source/drain contacts.
    set clearance 1.0

    set origm $m
    set orignf $nf
    while true {
       set yext [expr ($w + $clearance) * $m + $clearance]
       set xext [expr ($l + $clearance) * $nf + $clearance]
       if {[expr min($xext, $yext)] > 30.0} {
          if {$yext > 30.0 && $m > 1} {
	     incr m -1
	  } elseif {$xext > 30.0 && $nf > 1} {
	     incr nf -1
	  } elseif {$yext > 30.0} {
	     set w 29
	     puts -nonewline stderr "Transistor width must be < 29 um"
	     puts stderr " to avoid tap spacing violation."
	     dict set parameters w $w
	  } elseif {$xext > 30.0} {
	     set l 29
	     puts -nonewline stderr "Transistor length must be < 29 um"
	     puts stderr " to avoid tap spacing violation."
	     dict set parameters l $l
	  }
       } else {
	  break
       }
    }
    if {$m != $origm} {
       puts stderr "Warning: M may need to be reduced to prevent tap distance violation"
       # dict set parameters m $m
    }
    if {$nf != $orignf} {
       puts stderr "Warning: Fingers may need to be reduced to prevent tap distance violation"
       # dict set parameters nf $nf
    }

    # Used by varactor only
    if {$device == "sg13g2_fd_pr__cap_var"} {
        catch {set magic::minfo_val "Warning:  No model exists for this device!"}
    } else {
        catch {set magic::minfo_val ""}
    }

    return $parameters
}

#----------------------------------------------------------------

proc sg13g2::sg13g2_fd_pr__nfet_01v8_check {parameters} {
   return [sg13g2::mos_check sg13g2_fd_pr__nfet_01v8 $parameters]
}

proc sg13g2::sg13g2_fd_pr__nfet_01v8_lvt_check {parameters} {
   return [sg13g2::mos_check sg13g2_fd_pr__nfet_01v8_lvt $parameters]
}

proc sg13g2::sg13g2_fd_bs_flash__special_sonosfet_star_check {parameters} {
   return [sg13g2::mos_check sg13g2_fd_bs_flash__special_sonosfet_star $parameters]
}

proc sg13g2::sg13g2_fd_pr__nfet_g5v0d10v5_check {parameters} {
   return [sg13g2::mos_check sg13g2_fd_pr__nfet_g5v0d10v5 $parameters]
}

proc sg13g2::sg13g2_fd_pr__nfet_g5v0d16v0_check {parameters} {
   return [sg13g2::mos_check sg13g2_fd_pr__nfet_g5v0d16v0 $parameters]
}

proc sg13g2::sg13g2_fd_pr__nfet_05v0_nvt_check {parameters} {
   return [sg13g2::mos_check sg13g2_fd_pr__nfet_05v0_nvt $parameters]
}

proc sg13g2::sg13g2_fd_pr__nfet_03v3_nvt_check {parameters} {
   return [sg13g2::mos_check sg13g2_fd_pr__nfet_03v3_nvt $parameters]
}

proc sg13g2::sg13g2_fd_pr__pfet_01v8_check {parameters} {
   return [sg13g2::mos_check sg13g2_fd_pr__pfet_01v8 $parameters]
}

proc sg13g2::sg13g2_fd_pr__pfet_01v8_lvt_check {parameters} {
   return [sg13g2::mos_check sg13g2_fd_pr__pfet_01v8_lvt $parameters]
}

proc sg13g2::sg13g2_fd_pr__pfet_01v8_hvt_check {parameters} {
   return [sg13g2::mos_check sg13g2_fd_pr__pfet_01v8_hvt $parameters]
}

proc sg13g2::sg13g2_fd_pr__pfet_g5v0d10v5_check {parameters} {
   return [sg13g2::mos_check sg13g2_fd_pr__pfet_g5v0d10v5 $parameters]
}

proc sg13g2::sg13g2_fd_pr__pfet_g5v0d16v0_check {parameters} {
   return [sg13g2::mos_check sg13g2_fd_pr__pfet_g5v0d16v0 $parameters]
}

proc sg13g2::sg13g2_fd_pr__cap_var_lvt_check {parameters} {
   return [sg13g2::mos_check sg13g2_fd_pr__cap_var_lvt $parameters]
}

proc sg13g2::sg13g2_fd_pr__cap_var_hvt_check {parameters} {
   return [sg13g2::mos_check sg13g2_fd_pr__cap_var_hvt $parameters]
}

proc sg13g2::sg13g2_fd_pr__cap_var_check {parameters} {
   return [sg13g2::mos_check sg13g2_fd_pr__cap_var $parameters]
}

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

# Fixed-layout devices (from sg13g2_fd_pr_base, _rf, and _rf2 libraries)
#
# Bipolar transistors:
#
# sg13g2_fd_pr__npn_05v5_W1p00L1p00
# sg13g2_fd_pr__npn_05v5_W1p00L2p00
# sg13g2_fd_pr__pnp_05v5_W3p40L3p40
# sg13g2_fd_pr__pnp_05v5_W0p68L0p68
# sg13g2_fd_pr__npn_11v0_W1p00L1p00
#
# Parallel Plate Capacitors:
#
# sg13g2_fd_pr__cap_vpp_11p5x11p7_m1m2m3m4_shieldlim5
# sg13g2_fd_pr__cap_vpp_11p5x11p7_m1m2_noshield
# sg13g2_fd_pr__cap_vpp_08p6x07p8_m1m2_shieldl1
# sg13g2_fd_pr__cap_vpp_04p4x04p6_m1m2_shieldl1
#
# Inductors:
#
# sg13g2_fd_pr__rf_test_coil1
# sg13g2_fd_pr__rf_test_coil2
# sg13g2_fd_pr__rf_test_coil3

proc sg13g2::sg13g2_fd_pr__npn_05v5_W1p00L1p00_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 nocell 1 xstep 7.03 ystep 7.03 class bjt}
}
proc sg13g2::sg13g2_fd_pr__npn_05v5_W1p00L2p00_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 nocell 1 xstep 7.03 ystep 8.03 class bjt}
}

proc sg13g2::sg13g2_fd_pr__pnp_05v5_W0p68L0p68_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 nocell 1 xstep 3.72 ystep 3.72 class bjt}
}

proc sg13g2::sg13g2_fd_pr__pnp_05v5_W3p40L3p40_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 nocell 1 xstep 6.44 ystep 6.44 class bjt}
}
proc sg13g2::sg13g2_fd_pr__npn_11v0_W1p00L1p00_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 nocell 1 xstep 7.03 ystep 7.03 class bjt}
}

proc sg13g2::sg13g2_fd_pr__rf_test_coil1_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 nocell 1 xstep 258 ystep 258 class inductor}
}
proc sg13g2::sg13g2_fd_pr__rf_test_coil2_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 nocell 1 xstep 290 ystep 404 class inductor}
}
proc sg13g2::sg13g2_fd_pr__rf_test_coil3_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 nocell 1 xstep 290 ystep 404 class inductor}
}

proc sg13g2::sg13g2_fd_pr__cap_vpp_11p5x11p7_m1m2m3m4_shieldl1m5_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 nocell 1 xstep 11.08 ystep 11.36 class capacitor}
}
proc sg13g2::sg13g2_fd_pr__cap_vpp_11p5x11p7_m1m2_noshield_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 nocell 1 xstep 11.08 ystep 11.36 class capacitor}
}
proc sg13g2::sg13g2_fd_pr__cap_vpp_08p6x07p8_m1m2_shieldl1_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 nocell 1 xstep 11.08 ystep 11.36 class capacitor}
}
proc sg13g2::sg13g2_fd_pr__cap_vpp_04p4x04p6_m1m2_shieldl1_defaults {} {
    return {nx 1 ny 1 deltax 0 deltay 0 nocell 1 xstep 11.08 ystep 11.36 class capacitor}
}

#----------------------------------------------------------------
# Fixed device: Conversion from SPICE netlist parameters to toolkit
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

proc sg13g2::sg13g2_fd_pr__npn_05v5_W1p00L1p00_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__npn_05v5_W1p00L2p00_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__pnp_05v5_W0p68L0p68_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__pnp_05v5_W3p40L3p40_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__npn_11v0_W1p00L1p00_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__rf_test_coil1_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__rf_test_coil2_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__rf_test_coil3_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}

proc sg13g2::sg13g2_fd_pr__cap_vpp_11p5x11p7_m1m2m3m4_shieldl1m5_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}
proc sg13g2::sg13g2_fd_pr__cap_vpp_11p5x11p7_m1m2_noshield_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}
proc sg13g2::sg13g2_fd_pr__cap_vpp_08p6x07p8_m1m2_shieldl1_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}
proc sg13g2::sg13g2_fd_pr__cap_vpp_04p4x04p6_m1m2_shieldl1_convert {parameters} {
    return [sg13g2::fixed_convert $parameters]
}

#----------------------------------------------------------------
# Fixed device: Interactively specifies the fixed layout parameters
#----------------------------------------------------------------

proc sg13g2::fixed_dialog {parameters} {
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
}

proc sg13g2::sg13g2_fd_pr__npn_05v5_W1p00L1p00_dialog {parameters} {
    sg13g2::fixed_dialog $parameters
}

proc sg13g2::sg13g2_fd_pr__npn_05v5_W1p00L2p00_dialog {parameters} {
    sg13g2::fixed_dialog $parameters
}

proc sg13g2::sg13g2_fd_pr__pnp_05v5_W0p68L0p68_dialog {parameters} {
    sg13g2::fixed_dialog $parameters
}

proc sg13g2::sg13g2_fd_pr__pnp_05v5_W3p40L3p40_dialog {parameters} {
    sg13g2::fixed_dialog $parameters
}

proc sg13g2::sg13g2_fd_pr__npn_11v0_W1p00L1p00_dialog {parameters} {
    sg13g2::fixed_dialog $parameters
}

proc sg13g2::sg13g2_fd_pr__rf_test_coil1_dialog {parameters} {
    sg13g2::fixed_dialog $parameters
}

proc sg13g2::sg13g2_fd_pr__rf_test_coil2_dialog {parameters} {
    sg13g2::fixed_dialog $parameters
}

proc sg13g2::sg13g2_fd_pr__rf_test_coil3_dialog {parameters} {
    sg13g2::fixed_dialog $parameters
}

proc sg13g2::sg13g2_fd_pr__cap_vpp_11p5x11p7_m1m2m3m4_shieldl1m5_dialog {parameters} {
    sg13g2::fixed_dialog $parameters
}
proc sg13g2::sg13g2_fd_pr__cap_vpp_11p5x11p7_m1m2_noshield_dialog {parameters} {
    sg13g2::fixed_dialog $parameters
}
proc sg13g2::sg13g2_fd_pr__cap_vpp_08p6x07p8_m1m2_shieldl1_dialog {parameters} {
    sg13g2::fixed_dialog $parameters
}
proc sg13g2::sg13g2_fd_pr__cap_vpp_04p4x04p6_m1m2_shieldl1_dialog {parameters} {
    sg13g2::fixed_dialog $parameters
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

proc sg13g2::sg13g2_fd_pr__npn_05v5_W1p00L1p00_draw {parameters} {
    return [sg13g2::fixed_draw sg13g2_fd_pr__rf_npn_05v5_W1p00L1p00 $parameters]
}

proc sg13g2::sg13g2_fd_pr__npn_05v5_W1p00L2p00_draw {parameters} {
    return [sg13g2::fixed_draw sg13g2_fd_pr__rf_npn_05v5_W1p00L2p00 $parameters]
}

proc sg13g2::sg13g2_fd_pr__pnp_05v5_W0p68L0p68_draw {parameters} {
    return [sg13g2::fixed_draw sg13g2_fd_pr__rf_pnp_05v5_W0p68L0p68 $parameters]
}

proc sg13g2::sg13g2_fd_pr__pnp_05v5_W3p40L3p40_draw {parameters} {
    return [sg13g2::fixed_draw sg13g2_fd_pr__rf_pnp_05v5_W3p40L3p40 $parameters]
}

proc sg13g2::sg13g2_fd_pr__npn_11v0_W1p00L1p00_draw {parameters} {
    return [sg13g2::fixed_draw sg13g2_fd_pr__rf_npn_11v0_W1p00L1p00 $parameters]
}

proc sg13g2::sg13g2_fd_pr__rf_test_coil1_draw {parameters} {
    return [sg13g2::fixed_draw sg13g2_fd_pr__rf_test_coil1 $parameters]
}

proc sg13g2::sg13g2_fd_pr__rf_test_coil2_draw {parameters} {
    return [sg13g2::fixed_draw sg13g2_fd_pr__rf_test_coil2 $parameters]
}

proc sg13g2::sg13g2_fd_pr__rf_test_coil3_draw {parameters} {
    return [sg13g2::fixed_draw sg13g2_fd_pr__rf_test_coil3 $parameters]
}

proc sg13g2::sg13g2_fd_pr__cap_vpp_11p5x11p7_m1m2m3m4_shieldl1m5_draw {parameters} {
    return [sg13g2::fixed_draw sg13g2_fd_pr__cap_vpp_11p5x11p7_m1m2m3m4_shieldl1m5 $parameters]
}
proc sg13g2::sg13g2_fd_pr__cap_vpp_11p5x11p7_m1m2_noshield_draw {parameters} {
    return [sg13g2::fixed_draw sg13g2_fd_pr__cap_vpp_11p5x11p7_m1m2_noshield $parameters]
}
proc sg13g2::sg13g2_fd_pr__cap_vpp_08p6x07p8_m1m2_shieldl1_draw {parameters} {
    return [sg13g2::fixed_draw sg13g2_fd_pr__cap_vpp_08p6x07p8_m1m2_shieldl1 $parameters]
}
proc sg13g2::sg13g2_fd_pr__cap_vpp_04p4x04p6_m1m2_shieldl1_draw {parameters} {
    return [sg13g2::fixed_draw sg13g2_fd_pr__cap_vpp_04p4x04p6_m1m2_shieldl1 $parameters]
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

proc sg13g2::sg13g2_fd_pr__npn_05v5_W1p00L1p00_check {parameters} {
    return [sg13g2::fixed_check $parameters]
}

proc sg13g2::sg13g2_fd_pr__npn_05v5_W1p00L2p00_check {parameters} {
    return [sg13g2::fixed_check $parameters]
}

proc sg13g2::sg13g2_fd_pr__pnp_05v5_W0p68L0p68_check {parameters} {
    return [sg13g2::fixed_check $parameters]
}

proc sg13g2::sg13g2_fd_pr__pnp_05v5_W3p40L3p40_check {parameters} {
    return [sg13g2::fixed_check $parameters]
}

proc sg13g2::sg13g2_fd_pr__npn_11v0_W1p00L1p00_check {parameters} {
    return [sg13g2::fixed_check $parameters]
}

proc sg13g2::sg13g2_fd_pr__rf_test_coil1_check {parameters} {
    return [sg13g2::fixed_check $parameters]
}

proc sg13g2::sg13g2_fd_pr__rf_test_coil2_check {parameters} {
    return [sg13g2::fixed_check $parameters]
}

proc sg13g2::sg13g2_fd_pr__rf_test_coil3_check {parameters} {
    return [sg13g2::fixed_check $parameters]
}

proc sg13g2::sg13g2_fd_pr__cap_vpp_11p5x11p7_m1m2m3m4_shieldl1m5_check {parameters} {
    return [sg13g2::fixed_check $parameters]
}
proc sg13g2::sg13g2_fd_pr__cap_vpp_11p5x11p7_m1m2_noshield_check {parameters} {
    return [sg13g2::fixed_check $parameters]
}
proc sg13g2::sg13g2_fd_pr__cap_vpp_08p6x07p8_m1m2_shieldl1_check {parameters} {
    return [sg13g2::fixed_check $parameters]
}
proc sg13g2::sg13g2_fd_pr__cap_vpp_04p4x04p6_m1m2_shieldl1_check {parameters} {
    return [sg13g2::fixed_check $parameters]
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
    return [expr {((round([magic::cif scale output] * 10000)) / 10000.0) * $value}]
}

#---------------------
# Microns to Internal
#---------------------
proc magic::u2i {value} {
    return [expr {$value / ((round([magic::cif scale output] * 10000)) / 10000.0)}]
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
