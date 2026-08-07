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
#* Callback functions for MOS transistors
#*******************************************************************************

#******************************************************************************************************
proc NLCB_mos_w {} {
    
    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]
    
    set tmpw     [Stof [iPDK_getParamValue w $cellId]]
    set tmpng    [expr int([iPDK_getParamValue ng $cellId])]
    set tmpWminS [iPDK_getParamValue Wmin $cellId]
    set tmpWmax  [Stof [techGetParam ${cell}_maxW]]
    
    if {$tmpWminS == ""} {
        set tmpWminS [techGetParam ${cell}_minW]
    }
    set tmpWmin [Stof $tmpWminS]
    
    if {$tmpw != "" && $tmpw>$tmpWmax*$tmpng} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong width: using minimum width ${tmpWminS}!!"
        iPDK_setParamValue w $tmpWminS $cellId
        set tmpw $tmpWmin
    }
    
    if {$tmpw != "" && $tmpWmin!="" && $tmpWmin>$tmpw} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong width: using minimum width ${tmpWminS}!!"
        iPDK_setParamValue w $tmpWminS $cellId
        set tmpw $tmpWmin
    }
    
    if {$tmpw != "" && $tmpWmin!="" && $tmpng!="" && $tmpWmin*$tmpng>$tmpw} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong width: using ng times minimum width ${tmpWminS}!!"
        iPDK_setParamValue w [Ftos [expr $tmpWmin*$tmpng*1e6] 3]u $cellId 
        set tmpw  [Stof [iPDK_getParamValue w $cellId]]
    }
    
    set tmpw [Stof [iPDK_getParamValue w $cellId]]
    set tmpw [GridFix [expr ($tmpw/$tmpng*1.0e6)*$tmpng]]
    
    iPDK_setParamValue w  [Ftos $tmpw 3]u $cellId
    iPDK_setParamValue ws [Ftos [expr $tmpw/$tmpng] 3]u $cellId
}

#******************************************************************************************************
proc NLCB_mos_ng {} {

    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]

    set tmpng    [expr round([Stof [iPDK_getParamValue ng $cellId]])]
    set tmpMaxNg [expr round([Stof [techGetParam ${cell}_maxNG]])]
    
    if {$tmpng < 1} {
        set tmpng 1
    }
    if {$tmpng > $tmpMaxNg} {
        set tmpng $tmpMaxNg 
    }

    iPDK_setParamValue ng [expr int($tmpng)] $cellId

    set tmpw [Stof [iPDK_getParamValue w $cellId]]
    iPDK_setParamValue ws [Ftos [expr 1e6*$tmpw/$tmpng] 3]u $cellId

    NLCB_mos_w
}
   
#******************************************************************************************************
proc NLCB_mos_l {} {
    
    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]
    
    set tmpl    [Stof [iPDK_getParamValue l $cellId]]
    set tmpLmax [Stof [techGetParam ${cell}_maxL]] 
    
    if {$tmpl != "" && $tmpl>$tmpLmax} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong length: using maximum length 10u!!"
        iPDK_setParamValue l [Ftos [expr $tmpLmax*1e6] 3]u $cellId
        #set tmpl [Stof [iPDK_getParamValue l $cellId]]
    }
    
    NLCB_l
}

#******************************************************************************************************
proc NLCB_l {} {
    # Callback function for a "l"-parameter.
    
    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]
    
    set tmpl     [Stof [iPDK_getParamValue l $cellId]]
    set tmpLminS [iPDK_getParamValue Lmin $cellId]
    
    if {$tmpLminS == ""} {
        set tmpLminS [techGetParam ${cell}_minL]
    }
    set tmpLmin [Stof $tmpLminS]
    
    if {$tmpl != "" && $tmpl>15e-3} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong length: using minimum length ${tmpLminS}!!"
        iPDK_setParamValue l $tmpLminS $cellId
    }
    
    if { $tmpl != "" && $tmpLmin!="" && $tmpLmin>$tmpl} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong length: using minimum length ${tmpLminS}!!"
        iPDK_setParamValue l $tmpLminS $cellId
    }
    
    set tmpl [Stof [iPDK_getParamValue l $cellId]]
    set tmpl [GridFix [expr $tmpl*1.0e6]]
    iPDK_setParamValue l [format %.3f $tmpl]u $cellId
}

#******************************************************************************************************
proc NLCB_w {} {
    # Callback function for a "w"-parameter.
    
    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]
    
    set tmpw     [Stof [iPDK_getParamValue w $cellId]]
    set tmpWminS [iPDK_getParamValue Wmin $cellId]
    
    if {$tmpWminS == ""} {
        set tmpWminS [techGetParam ${cell}_minW]
    }
    set tmpWmin [Stof $tmpWminS]
    
    if {$tmpw > 15e-3} {
        hiGetAttention
        hiGetAttention
        CbMessage "Warning: wrong width: using minimum width ${tmpWminS}!!"
        iPDK_setParamValue w $tmpWminS $cellId
    }

    if {$tmpWmin > $tmpw} {
        hiGetAttention
        hiGetAttention
        CbMessage "Warning: wrong width: using minimum width ${tmpWminS}!!"
        iPDK_setParamValue w $tmpWminS $cellId
    }
    
    set tmpw [Stof [iPDK_getParamValue w $cellId]]
    set tmpw [GridFix [expr $tmpw*1.0e6]]
    iPDK_setParamValue w [format %.3f $tmpw]u $cellId
}

