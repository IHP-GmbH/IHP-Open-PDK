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

proc sg13g2::subconn_draw {} {
   set curunits [units]
   units microns
   set w [box width]
   set h [box height]
   if {$w < 0.16} {
      puts stderr "Substrate tap width must be at least 0.16um"
      return
   }
   if {$h < 0.16} {
      puts stderr "Substrate tap height must be at least 0.16um"
      return
   }
   suspendall
   paint psc
   pushbox
   pushbox
   box grow c 0.07
   paint psd
   popbox
   if {$w > $h} {
      box grow e 0.05
      box grow w 0.05
   } else {
      box grow n 0.05
      box grow s 0.05
   }
   paint m1
   popbox
   resumeall
   units {*}$curunits
}

#----------------------------------------------------------------

proc sg13g2::hvsubconn_draw {} {
   set curunits [units]
   units microns
   set w [box width]
   set h [box height]
   if {$w < 0.16} {
      puts stderr "Substrate tap width must be at least 0.16um"
      return
   }
   if {$h < 0.16} {
      puts stderr "Substrate tap height must be at least 0.16um"
      return
   }
   suspendall
   paint hvpsc
   pushbox
   box grow c 0.07
   paint hvpsd
   pushbox
   popbox
   if {$w > $h} {
      box grow e 0.05
      box grow w 0.05
   } else {
      box grow n 0.05
      box grow s 0.05
   }
   paint m1
   popbox
   resumeall
   units {*}$curunits
}

#----------------------------------------------------------------
# Helper function for drawing guard rings.
# Assumes that a box exists and defines the centerlines of the
# guard ring contacts.
# ctype = type to paint for contact
# dtype = type to paint for diffusion
#----------------------------------------------------------------

proc sg13g2::guard_ring_draw {ctype dtype} {
   set curunits [units]
   units microns
   pushbox
   box width 0
   box grow c 0.08
   paint m1
   pushbox
   box grow n -0.3
   box grow s -0.3
   paint $ctype
   popbox
   box grow c 0.07
   paint $dtype
   popbox

   pushbox
   box height 0
   box grow c 0.08
   paint m1
   pushbox
   box grow e -0.3
   box grow w -0.3
   paint $ctype
   popbox
   box grow c 0.07
   paint $dtype
   popbox

   pushbox
   box move n [box height]
   box height 0
   box grow c 0.08
   paint m1
   pushbox
   box grow e -0.3
   box grow w -0.3
   paint $ctype
   popbox
   box grow c 0.07
   paint $dtype
   popbox

   pushbox
   box move e [box width]
   box width 0
   box grow c 0.08
   paint m1
   pushbox
   box grow n -0.3
   box grow s -0.3
   paint $ctype
   popbox
   box grow c 0.07
   paint $dtype
   popbox
   units {*}$curunits
}

#----------------------------------------------------------------

proc sg13g2::subconn_guard_draw {} {
   set curunits [units]
   units microns
   set w [box width]
   set h [box height]
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
   units {*}$curunits
}

#----------------------------------------------------------------

proc sg13g2::hvsubconn_guard_draw {} {
   set curunits [units]
   units microns
   set w [box width]
   set h [box height]
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

   sg13g2::guard_ring_draw hvpsc hvpsd

   popbox
   tech revert
   resumeall
   units {*}$curunits
}

#----------------------------------------------------------------

proc sg13g2::nwell_draw {} {
   set curunits [units]
   units microns
   set w [box width]
   set h [box height]
   # NOTE:  Width and height are determined by the requirement for
   # a contact on each side.  There is not much that can be done
   # with an guarded nwell smaller than that, anyway.
   if {$w < 0.62} {
      puts stderr "N-well region width must be at least 0.62um"
      return
   }
   if {$h < 0.62} {
      puts stderr "N-well region height must be at least 0.62um"
      return
   }
   suspendall
   tech unlock *
   pushbox
   pushbox
   box grow c 0.390
   paint nwell
   popbox

   sg13g2::guard_ring_draw nsc nsd

   popbox
   tech revert
   resumeall
   units {*}$curunits
}

#----------------------------------------------------------------

proc sg13g2::hvnwell_draw {} {
   set curunits [units]
   units microns
   set w [box width]
   set h [box height]
   # NOTE:  Width and height are determined by the requirement for
   # a contact on each side.  There is not much that can be done
   # with an guarded nwell smaller than that, anyway.
   if {$w < 0.62} {
      puts stderr "MV N-well region width must be at least 0.62um"
      return
   }
   if {$h < 0.62} {
      puts stderr "MV N-well region height must be at least 0.26um"
      return
   }
   suspendall
   tech unlock *
   pushbox
   pushbox
   box grow c 0.770
   paint nwell
   popbox

   sg13g2::guard_ring_draw hvnsc hvnsd

   popbox
   tech revert
   resumeall
   units {*}$curunits
}

#----------------------------------------------------------------

proc sg13g2::deep_nwell_draw {} {
   set curunits [units]
   units microns
   set w [box width]
   set h [box height]
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
   box grow c 0.425
   pushbox
   box width 0.79
   paint nwell
   popbox
   pushbox
   box height 0.79
   paint nwell
   popbox
   pushbox
   box move n $h
   box move n 0.85
   box move s 0.79
   box height 0.79
   paint nwell
   popbox
   pushbox
   box move e $w
   box move e 0.85
   box move w 0.79
   box width 0.79
   paint nwell
   popbox

   popbox
   box grow c 0.03

   pushbox
   box width 0
   box grow c 0.085
   paint m1
   pushbox
   box grow n -0.3
   box grow s -0.3
   paint nsc
   popbox
   box grow c 0.07
   paint nsd
   popbox

   pushbox
   box height 0
   box grow c 0.085
   paint m1
   pushbox
   box grow e -0.3
   box grow w -0.3
   paint nsc
   popbox
   box grow c 0.07
   paint nsd
   popbox

   pushbox
   box move n [box height]
   box height 0
   box grow c 0.085
   paint m1
   pushbox
   box grow e -0.3
   box grow w -0.3
   paint nsc
   popbox
   box grow c 0.07
   paint nsd
   popbox

   pushbox
   box move e [box width]
   box width 0
   box grow c 0.085
   paint m1
   pushbox
   box grow n -0.3
   box grow s -0.3
   paint nsc
   box grow c 0.07
   paint nsd
   popbox

   popbox
   tech revert
   resumeall
   units {*}$curunits
}

#----------------------------------------------------------------

proc sg13g2::hvdeep_nwell_draw {} {
   set curunits [units]
   units microns
   set w [box width]
   set h [box height]
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
   box grow c 0.805
   pushbox
   box width 1.55
   paint nwell
   popbox
   pushbox
   box height 1.55
   paint nwell
   popbox
   pushbox
   box move n $h
   box move n 1.61
   box move s 1.55
   box height 1.55
   paint nwell
   popbox
   pushbox
   box move e $w
   box move e 1.61
   box move w 1.55
   box width 1.55
   paint nwell
   popbox

   popbox
   box grow c 0.03

   pushbox
   box width 0
   box grow c 0.085
   paint m1
   pushbox
   box grow n -0.3
   box grow s -0.3
   paint hvnsc
   popbox
   box grow c 0.07
   paint hvnsd
   popbox

   pushbox
   box height 0
   box grow c 0.085
   paint m1
   pushbox
   box grow e -0.3
   box grow w -0.3
   paint hvnsc
   popbox
   box grow c 0.07
   paint hvnsd
   popbox

   pushbox
   box move n [box height]
   box height 0
   box grow c 0.085
   paint m1
   pushbox
   box grow e -0.3
   box grow w -0.3
   paint hvnsc
   popbox
   box grow c 0.07
   paint hvnsd
   popbox

   pushbox
   box move e [box width]
   box width 0
   box grow c 0.085
   paint m1
   pushbox
   box grow n -0.3
   box grow s -0.3
   paint hvnsc
   box grow c 0.07
   paint hvnsd
   popbox

   popbox
   tech revert
   resumeall
   units {*}$curunits
}

#----------------------------------------------------------------
