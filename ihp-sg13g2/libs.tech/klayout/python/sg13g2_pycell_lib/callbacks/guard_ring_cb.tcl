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

#*******************************************************************************
#* Callback functions for guard rings
#*******************************************************************************

# NOTE: keep in sync with MIN_GUARD_RING_DISTANCE_UM in device_base_code.py
set IHP_minGuardRingDistance 0.6 ;# um

#*******************************************************************************
#* Guard ring distance of devices with a guard ring option (DeviceBase)
#*******************************************************************************
proc CbGuardRingDistance {} {

    global IHP_minGuardRingDistance
    global SG13_EPSILON

    set cellId [iPDK_getCurrentInst]

    set tmpDistanceS [iPDK_getParamValue guardRingDistance $cellId]
    if {$tmpDistanceS == ""} {
        return
    }
    set tmpDistance [expr [Stof $tmpDistanceS]*1e6]

    if {$tmpDistance < $IHP_minGuardRingDistance-$SG13_EPSILON} {
        set minDistanceS [Ftos [expr $IHP_minGuardRingDistance*1e-6]]
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: guard ring distance too small: using minimum distance ${minDistanceS}!!"
        iPDK_setParamValue guardRingDistance $minDistanceS $cellId
    }
}

#*******************************************************************************
#* Width/height of the standalone guard ring
#*******************************************************************************
proc CbGuardRingSize {} {

    global SG13_EPSILON

    set cellId [iPDK_getCurrentInst]

    # NOTE: keep in sync with min_guard_ring_span() in guard_ring_code.py,
    #       the smallest ring that still gets a contact on each side
    set cont_size         [techGetParam Cnt_a]
    set cont_space        [techGetParam Cnt_b]
    set cont_min_act_encl [techGetParam Cnt_c]
    set wguard_active     [expr $cont_size + 2*$cont_min_act_encl]
    set minSpan  [GridFix [expr 2*($wguard_active - $cont_min_act_encl + $cont_space) + $cont_size]] ;# um
    set minSpanS [Ftos [expr $minSpan*1e-6]]

    foreach param {w h} {
        set tmpS [iPDK_getParamValue $param $cellId]
        if {$tmpS == ""} {
            continue
        }

        if {[expr [Stof $tmpS]*1e6] < $minSpan-$SG13_EPSILON} {
            hiGetAttention
            hiGetAttention
            CbMessage "WARNING: guard ring $param too small: using minimum ${minSpanS}!!"
            iPDK_setParamValue $param $minSpanS $cellId
        }
    }
}
