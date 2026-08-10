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
#* Callback functions for rf{np}mos[HV]
#*******************************************************************************

#******************************************************************************************************
proc rfmos_cb_ng {} {
    
    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]
    
    set ng [iPDK_getParamValue ng $cellId]

    set ng [expr int($ng)]
    if {$ng < 1} {
        set ng 1
        CbMessage "ng out of range, set to 1"
        hiGetAttention
    }
    
    if { $ng > 10} {
        set ng 10
        CbMessage "ng out of range, set to 10"
        hiGetAttention
    }
    
    iPDK_setParamValue ng $ng $cellId
    
    rfmos_cb_w
    
    return t
}

#******************************************************************************************************
proc rfmos_cb_cnt_rows {} {

    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]
    
    set n [iPDK_getParamValue cnt_rows $cellId]

    if {$n < 1} {
        iPDK_setParamValue cnt_rows 1 $cellId
        CbMessage "S/D contact rows out of range, set to 1"
        hiGetAttention
    }

    if {$n > 10} {
        iPDK_setParamValue cnt_rows 10 $cellId
        CbMessage "S/D contact rows out of range, set to 10"
        hiGetAttention
    }
   
    rfmos_cb_sd
    
    return t
}

#******************************************************************************************************
proc rfmos_cb_l {} {
    
    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]
    
    set l [Stof [iPDK_getParamValue l $cellId]]

    if {$l == 0.0} {
        set defL [iPDK_getParamDef defValue $cellId l]
        iPDK_setParamValue l $defL $cellId
        CbMessage "l invalid, set to default"
        return nil
    }
    
    set str  [techGetParam ${cell}_minL]
    set minl [Stof $str]

    if {$l < $minl} {
        iPDK_setParamValue l $str $cellId
        CbMessage "l below minimum, set to minimum"
        hiGetAttention
        return t
    }
    
    set str  [techGetParam ${cell}_maxL]
    set maxl [Stof $str]
    
    if {$l > $maxl} {
        iPDK_setParamValue l $str $cellId
        CbMessage "l above maximum, set to maximum"
        hiGetAttention
        return t
    }
    
    set l [GridFix [expr $l*1e6]]
    iPDK_setParamValue l [Ftos [expr $l/1e6] 3] $cellId
}

#******************************************************************************************************
proc rfmos_cb_w {} {
    
    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]

    set w [Stof [iPDK_getParamValue w $cellId]]
    if {$w == 0.0} {
        hiGetAttention
        CbMessage "w invalid"
        return nil
    }
    
    set ng [Stof [iPDK_getParamValue ng $cellId]]
    set w  [expr $w/$ng]
    
    set str  [techGetParam ${cell}_minW]
    set minw [Stof $str]
    if {$w < $minw} {
        hiGetAttention
        iPDK_setParamValue w  [Ftos [expr $minw*$ng] 3] $cellId
        iPDK_setParamValue ws $str $cellId
        rfmos_cb_sd
        return t
    }
    
    set str  [techGetParam ${cell}_maxW]
    set maxw [Stof $str]
    if {$w > $maxw} {
        hiGetAttention
        iPDK_setParamValue w  [Ftos [expr $maxw*$ng] 3] $cellId
        iPDK_setParamValue ws $str $cellId
        rfmos_cb_sd
        return t
    }
    
    set w [expr {[GridFix [expr ($w*1e6)] ] / 1e6}]
    iPDK_setParamValue w  [Ftos [expr $w*$ng] 3] $cellId
    iPDK_setParamValue ws [Ftos $w 3] $cellId
    
    rfmos_cb_sd
}

#******************************************************************************************************
# as, ad, ps, pd (done procedure)
proc rfmos_cb_sd {} {
    
    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]

    if {[iPDK_getParamValue calculate $cellId] == ""} {
        return t
    }
    
    set ng [Stof [iPDK_getParamValue ng $cellId]]
    set ng [expr int($ng)]
    set nr [expr int([iPDK_getParamValue ng $cellId])]
    set w  [Stof [iPDK_getParamValue w $cellId]] 
    set ws [expr $w/$ng]
    set z1 [expr 0.345e-6+0.41e-6*($nr-1)]
    set z2 [expr  0.38e-6+0.41e-6*($nr-1)]
    
    if {[odd $ng]} {
        set as [expr $ws*($z1+(($ng-1)/2)*$z2)]
        set ad $as
        set ps [expr ($ws*($ng+1)+$z1*2+$z2*($ng-1))]
        set pd $ps
    } else {
        set as [expr $ws*(2*$z1+(($ng-2)/2)*$z2)]
        set ad [expr $ws*$z2*$ng/2]
        set ps [expr ($ws*($ng+2)+4*$z1+($ng-2)*$z2)]
        set pd [expr ($ws+$z2)*$ng]
    }
    
    iPDK_setParamValue as [Ftos $as 4] $cellId
    iPDK_setParamValue ad [Ftos $ad 4] $cellId
    iPDK_setParamValue ps [Ftos $ps 4] $cellId
    iPDK_setParamValue pd [Ftos $pd 4] $cellId
}
