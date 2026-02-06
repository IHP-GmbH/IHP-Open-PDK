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
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
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
   box grow c 0.07um
   paint psd
   popbox
   if {$w > $h} {
      box grow e 0.05um
      box grow w 0.05um
   } else {
      box grow n 0.05um
      box grow s 0.05um
   }
   paint m1
   popbox
   resumeall
}

#----------------------------------------------------------------

proc sg13g2::hvsubconn_draw {} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
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
   box grow c 0.07um
   paint hvpsd
   pushbox
   popbox
   if {$w > $h} {
      box grow e 0.05um
      box grow w 0.05um
   } else {
      box grow n 0.05um
      box grow s 0.05um
   }
   paint m1
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
   box grow c 0.08um
   paint m1
   pushbox
   box grow n -0.3um
   box grow s -0.3um
   paint $ctype
   popbox
   box grow c 0.07um
   paint $dtype
   popbox

   pushbox
   box height 0
   box grow c 0.08um
   paint m1
   pushbox
   box grow e -0.3um
   box grow w -0.3um
   paint $ctype
   popbox
   box grow c 0.07um
   paint $dtype
   popbox

   pushbox
   box move n [box height]i
   box height 0
   box grow c 0.08um
   paint m1
   pushbox
   box grow e -0.3um
   box grow w -0.3um
   paint $ctype
   popbox
   box grow c 0.07um
   paint $dtype
   popbox

   pushbox
   box move e [box width]i
   box width 0
   box grow c 0.08um
   paint m1
   pushbox
   box grow n -0.3um
   box grow s -0.3um
   paint $ctype
   popbox
   box grow c 0.07um
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

proc sg13g2::hvsubconn_guard_draw {} {
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

   sg13g2::guard_ring_draw hvpsc hvpsd

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
   box grow c 0.390um
   paint nwell
   popbox

   sg13g2::guard_ring_draw nsc nsd

   popbox
   tech revert
   resumeall
}

#----------------------------------------------------------------

proc sg13g2::hvnwell_draw {} {
   set w [magic::i2u [box width]]
   set h [magic::i2u [box height]]
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
   box grow c 0.770um
   paint nwell
   popbox

   sg13g2::guard_ring_draw hvnsc hvnsd

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
   box grow c 0.425um
   pushbox
   box width 0.79um
   paint nwell
   popbox
   pushbox
   box height 0.79um
   paint nwell
   popbox
   pushbox
   box move n ${h}um
   box move n 0.85um
   box move s 0.79um
   box height 0.79um
   paint nwell
   popbox
   pushbox
   box move e ${w}um
   box move e 0.85um
   box move w 0.79um
   box width 0.79um
   paint nwell
   popbox

   popbox
   box grow c 0.03um

   pushbox
   box width 0
   box grow c 0.085um
   paint m1
   pushbox
   box grow n -0.3um
   box grow s -0.3um
   paint nsc
   popbox
   box grow c 0.07um
   paint nsd
   popbox

   pushbox
   box height 0
   box grow c 0.085um
   paint m1
   pushbox
   box grow e -0.3um
   box grow w -0.3um
   paint nsc
   popbox
   box grow c 0.07um
   paint nsd
   popbox

   pushbox
   box move n [box height]i
   box height 0
   box grow c 0.085um
   paint m1
   pushbox
   box grow e -0.3um
   box grow w -0.3um
   paint nsc
   popbox
   box grow c 0.07um
   paint nsd
   popbox

   pushbox
   box move e [box width]i
   box width 0
   box grow c 0.085um
   paint m1
   pushbox
   box grow n -0.3um
   box grow s -0.3um
   paint nsc
   box grow c 0.07um
   paint nsd
   popbox

   popbox
   tech revert
   resumeall
}

#----------------------------------------------------------------

proc sg13g2::hvdeep_nwell_draw {} {
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
   box grow c 0.805um
   pushbox
   box width 1.55um
   paint nwell
   popbox
   pushbox
   box height 1.55um
   paint nwell
   popbox
   pushbox
   box move n ${h}um
   box move n 1.61um
   box move s 1.55um
   box height 1.55um
   paint nwell
   popbox
   pushbox
   box move e ${w}um
   box move e 1.61um
   box move w 1.55um
   box width 1.55um
   paint nwell
   popbox

   popbox
   box grow c 0.03um

   pushbox
   box width 0
   box grow c 0.085um
   paint m1
   pushbox
   box grow n -0.3um
   box grow s -0.3um
   paint hvnsc
   popbox
   box grow c 0.07um
   paint hvnsd
   popbox

   pushbox
   box height 0
   box grow c 0.085um
   paint m1
   pushbox
   box grow e -0.3um
   box grow w -0.3um
   paint hvnsc
   popbox
   box grow c 0.07um
   paint hvnsd
   popbox

   pushbox
   box move n [box height]i
   box height 0
   box grow c 0.085um
   paint m1
   pushbox
   box grow e -0.3um
   box grow w -0.3um
   paint hvnsc
   popbox
   box grow c 0.07um
   paint hvnsd
   popbox

   pushbox
   box move e [box width]i
   box width 0
   box grow c 0.085um
   paint m1
   pushbox
   box grow n -0.3um
   box grow s -0.3um
   paint hvnsc
   box grow c 0.07um
   paint hvnsd
   popbox

   popbox
   tech revert
   resumeall
}

#----------------------------------------------------------------
