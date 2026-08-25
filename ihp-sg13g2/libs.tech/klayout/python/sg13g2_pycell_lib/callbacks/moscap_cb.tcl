########################################################################
#
# Copyright 2026 IHP PDK Authors
#
# Licensed under the GNU General Public License, Version 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.gnu.org/licenses/gpl-3.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
########################################################################

proc CbMoscap_wl {param} {

    global SG13_GRID

    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]

    set minW [Stof [techGetParam ${cell}_minW]]
    set minL [Stof [techGetParam ${cell}_minL]]
    set maxW [Stof [techGetParam ${cell}_maxW]]
    set maxL [Stof [techGetParam ${cell}_maxL]]

    set w [Stof [iPDK_getParamValue w $cellId]]
    set l [Stof [iPDK_getParamValue l $cellId]]

    set w [CbRoundm $w $SG13_GRID]
    if {[Less $w $minW 1u]} {
        CbMessage "w too small"
        set w $minW
    }
    if {[Greater $w $maxW 1u]} {
        CbMessage "w too large"
        set w $maxW
    }
    iPDK_setParamValue w [Ftos $w 3] $cellId

    set l [CbRoundm $l $SG13_GRID]
    if {[Less $l $minL 1u]} {
        CbMessage "l too small"
        set l $minL
    }
    if {[Greater $l $maxL 1u]} {
        CbMessage "l too large"
        set l $maxL
    }
    iPDK_setParamValue l [Ftos $l 3] $cellId
}
