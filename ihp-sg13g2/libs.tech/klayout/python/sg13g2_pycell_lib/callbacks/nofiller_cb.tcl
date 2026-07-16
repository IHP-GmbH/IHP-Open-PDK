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

proc noFiller_cb {var} {
    
    global SG13_GRID
    
    set cellId [iPDK_getCurrentInst]

    #minLW = Stof(cdfgData->minLW->value)
    set minLW   10e-9
    set maxLW   600e-6
    set maxLWs  600u

    switch $var {
        m {
            set m 0
            set i [iPDK_getParamValue noAct $cellId]
            if {$i==t} {
                set m [expr $m|1]
            }
            set i [iPDK_getParamValue noGP $cellId]
            if {$i==t} {
                set m [expr $m|2]
            }
            set i [iPDK_getParamValue noM1 $cellId]
            if {$i==t} {
                set m [expr $m|4]
            }
            set i [iPDK_getParamValue noM2 $cellId]
            if {$i==t} {
                set m [expr $m|8]
            }
            set i [iPDK_getParamValue noM3 $cellId]
            if {$i==t} {
                set m [expr $m|16]
            }
            set i [iPDK_getParamValue noM4 $cellId]
            if {$i==t} {
                set m [expr $m|32]
            }
            set i [iPDK_getParamValue noM5 $cellId]
            if {$i==t} {
                set m [expr $m|64]
            }
            set i [iPDK_getParamValue noTM1 $cellId]
            if {$i==t} {
                set m [expr $m|128]
            }
            set i [iPDK_getParamValue noTM2 $cellId]
            if {$i==t} {
                set m [expr $m|256]
            }
            
            iPDK_setParamValue noMask $m $cellId
        }
        w {
            set w [Stof [iPDK_getParamValue w $cellId]]
            set w [CbRoundm $w $SG13_GRID]
            if {$w < $minLW} {
                CbMessage "w < min. w"
                set w $minLW
            }
            if {$w > $maxLW} {
                CbMessage "w > max. w (${maxLWs})" 
                set w $maxLW
            }
            iPDK_setParamValue w [Ftos $w 6] $cellId
        }
        l {
            set l [Stof [iPDK_getParamValue l $cellId]]
            set l [CbRoundm $l $SG13_GRID]
            if {$l < $minLW} {
                CbMessage "l < min. l"
                set l $minLW
            }
            if {$l > $maxLW} {
                CbMessage "l > max. l (${maxLWs})" 
                set l $maxLW
            }
            iPDK_setParamValue l [Ftos $l 6] $cellId
        }
        setall {
            iPDK_setParamValue noAct t $cellId
            iPDK_setParamValue noGP t $cellId
            iPDK_setParamValue noM1 t $cellId
            iPDK_setParamValue noM2 t $cellId
            iPDK_setParamValue noM3 t $cellId
            iPDK_setParamValue noM4 t $cellId
            iPDK_setParamValue noM5 t $cellId
            iPDK_setParamValue noTM1 t $cellId
            iPDK_setParamValue noTM2 t $cellId
            iPDK_setParamValue noMask 511 $cellId
        }
        setnone {
            iPDK_setParamValue noAct nil $cellId
            iPDK_setParamValue noGP nil $cellId
            iPDK_setParamValue noM1 nil $cellId
            iPDK_setParamValue noM2 nil $cellId
            iPDK_setParamValue noM3 nil $cellId
            iPDK_setParamValue noM4 nil $cellId
            iPDK_setParamValue noM5 nil $cellId
            iPDK_setParamValue noTM1 nil $cellId
            iPDK_setParamValue noTM2 nil $cellId
            iPDK_setParamValue noMask 0 $cellId
        }
        done {
            CbMessage "No layer selected"
        }
    }
}

proc noFiller_apply {cellId} {

   set val [iPDK_getParamValue noMask $cellId]
   if {$val == 0} {
        CbMessage "No layer selected"
        return nil
    } else {
        return t
    }
}

