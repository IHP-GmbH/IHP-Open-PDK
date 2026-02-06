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

#-----------------------------------------------------------------
# Command script for generating cell sealring_side
# Sealring is bottom side as drawn.  Rotate for other sides.
# Default width is 21600, value in magic internal units.
# Set sealring_width before sourcing this file to resize.
# Default name is sealring_side;  set sealring_suffix to add a
# suffix (e.g., "_short" or "_long" if the frame is not square).
#-----------------------------------------------------------------

if {[catch {set testwidth $sealring_width}]} {
    set sealring_width 21600
}
if {[catch {set testname $sealring_suffix}]} {
    set sealring_suffix ""
}

suspendall
tech unlock *
snap internal
load sealring_side${sealring_suffix} -silent
box values -26 -26 [expr $sealring_width + 26] 726
paint pwell
box values 0 260 $sealring_width 292
paint sealcont
box values 0 292 $sealring_width 700
paint psubdiff
box values 0 0 $sealring_width 260
paint psubdiff
box values 0 298 $sealring_width 700
paint metal1
box values 0 0 $sealring_width 260
paint metal1
box values 0 260 $sealring_width 298
paint sealvia1
box values 0 298 $sealring_width 700
paint metal2
box values 0 0 $sealring_width 260
paint metal2
box values 0 260 $sealring_width 298
paint sealvia2
box values 0 298 $sealring_width 700
paint metal3
box values 0 0 $sealring_width 260
paint metal3
box values 0 260 $sealring_width 298
paint sealvia3
box values 0 298 $sealring_width 700
paint metal4
box values 0 0 $sealring_width 260
paint metal4
box values 0 260 $sealring_width 298
paint sealvia4
box values 0 344 $sealring_width 700
paint metal5
box values 0 0 $sealring_width 260
paint metal5
box values 0 260 $sealring_width 344
paint sealvia5
box values 0 440 $sealring_width 700
paint metal6
box values 0 0 $sealring_width 260
paint metal6
box values 0 260 $sealring_width 440
paint sealvia6
box values 0 0 $sealring_width 700
paint metal7
box values 0 -1440 $sealring_width -600
paint seal
property FIXED_BBOX "0 -1440 $sealring_width 700"
select clear
view
tech revert
resumeall
