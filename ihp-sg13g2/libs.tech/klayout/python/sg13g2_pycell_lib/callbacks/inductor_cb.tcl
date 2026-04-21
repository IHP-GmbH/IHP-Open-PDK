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

#------------------------------------------------------------------------
#Inductor
#------------------------------------------------------------------------

proc inductor_minD {w s nr} {

    global SG13_GRID

    set sqrt2 [expr sqrt(2)]  ;# 1.41421356
    if {$nr == 1} {
        set dmin [expr [GridFix [expr (($s+$w+$w)*(1+$sqrt2)/2+$SG13_GRID*2)]]*2]
    }
    if {$nr == 2} {
        set dmin [GridFix [expr ([GridFix [expr $w/$sqrt2+$s/2]]+[GridFix [expr $s*0.4143]]+0.02+$w)*2*(1+$sqrt2)+0.01]]
    }
    if {$nr > 2} {
        set dmin [GridFix [expr (([GridFix [expr $w/$sqrt2+$s/2]]+[GridFix [expr $s*0.4143]])*2+2*$s+4*$w)*(1+$sqrt2)]]
    }

    return $dmin
}

proc inductor_w {} {

    set cellId [iPDK_getCurrentInst]

    set tmpw [Stof [iPDK_getParamValue w $cellId]]
    set w [GridFix [expr ($tmpw*5e5)*2]]
    iPDK_setParamValue w [Ftos $w 3]u $cellId
    set tmpw [Stof [iPDK_getParamValue w $cellId]]

    set tmpWmaxS 30u
    set tmpWmax  [Stof $tmpWmaxS]
    set tmpWminS [iPDK_getParamValue Wmin $cellId]
    set tmpWmin  [Stof $tmpWminS]

    if {$tmpw!="" && $tmpWmin!="" && $tmpWmin>$tmpw} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong width: using minimum width ${tmpWminS}%s!!"
        iPDK_setParamValue w $tmpWminS $cellId
        set tmpw $tmpWminS
    }

    if {$tmpw!="" && $tmpWmax!="" && $tmpWmax<$tmpw} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong width: using maximum width ${tmpWmaxS}!!"
        iPDK_setParamValue w $tmpWmaxS $cellId
        set tmpw $tmpWmaxS
    }

    set tmps  [Stof [iPDK_getParamValue s $cellId]]
    set tmpnr [expr int([iPDK_getParamValue nr_r $cellId])]
    set tmps  [expr $tmps*1000000.0]
    set tmpw  [expr $tmpw*1000000.0]

    set var [inductor_minD $tmpw $tmps $tmpnr]

    iPDK_setParamValue Dmin [Ftos $var 3]u $cellId

    inductor_d
    inductor_L
}

proc inductor_s {} {

    set cellId [iPDK_getCurrentInst]

    set tmps [Stof [iPDK_getParamValue s $cellId]]
    set s [GridFix [expr $tmps*1e6]]
    iPDK_setParamValue s [Ftos $s 3]u $cellId
    set tmps [Stof [iPDK_getParamValue s $cellId]]

    set tmpSmaxS 30u
    set tmpSmax  [Stof $tmpSmaxS]
    set tmpSminS [iPDK_getParamValue Smin $cellId]
    set tmpSmin  [Stof $tmpSminS]

    if {$tmps!="" && $tmpSmin!="" && $tmpSmin>$tmps} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong space distance: using minimum space ${tmpSminS}!!"
        iPDK_setParamValue s $tmpSminS $cellId
        set tmps $tmpSmin
    }

    if {$tmps!="" && $tmpSmax!="" && $tmpSmax<$tmps} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong space distance: using maximum space ${tmpSmaxS}!!"
        iPDK_setParamValue s $tmpSmaxS $cellId
        set tmps $tmpSmax
    }

    set tmpw  [Stof [iPDK_getParamValue w $cellId]]
    set tmpnr [expr int([iPDK_getParamValue nr_r $cellId])]
    set tmps  [expr $tmps*1000000.0]
    set tmpw  [expr $tmpw*1000000.0]

    set var [inductor_minD $tmpw $tmps $tmpnr]

    iPDK_setParamValue Dmin [Ftos $var 3]u $cellId

    inductor_d
    inductor_L
}

proc inductor_nr {} {

    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]

    set tmpnr [expr int([iPDK_getParamValue nr_r $cellId])]

    set cell [string range $cell 0 [string first "_" $cell]-1]
    set tmpNrmax 10
    set tmpNrmin [iPDK_getParamValue minNr_t $cellId]

    if {$tmpnr!="" && $tmpNrmin!="" && $tmpNrmin>$tmpnr} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong number of turns: using minimum number ${tmpNrmin}!!"

        iPDK_setParamValue nr_r $tmpNrmin $cellId
        set tmpnr $tmpNrmin
    }

    if { [odd $tmpnr] && $cell=="inductor3"} {
        hiGetAttention
        hiGetAttention
        incr tmpnr -1
        CbMessage "WARNING: Wrong number of turns: Only even numbers are accepted! Using minimum number ${tmpnr}!!"
        iPDK_setParamValue nr_r $tmpnr $cellId
    }

    if {$tmpnr != "" && $tmpNrmax!="" && $tmpNrmax<$tmpnr} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong number of turns: using maximum number ${tmpNrmax}%L!!"
        iPDK_setParamValue nr_r $tmpNrmax $cellId
        set tmpnr $tmpNrmax
    }

    set tmps  [Stof [iPDK_getParamValue s $cellId]]
    set tmpw  [Stof [iPDK_getParamValue w $cellId]]
    set tmps  [expr $tmps*1000000.0]
    set tmpw  [expr $tmpw*1000000.0]

    set var [inductor_minD $tmpw $tmps $tmpnr]

    iPDK_setParamValue Dmin [Ftos $var 3]u $cellId

    inductor_d
    inductor_L
}


# Inductance formula from
# IEEE Journal of Solid_state Circuits, Vol 34, No 10, Oct 1999
# Simple Accurate Expressions for Planar Spiral Inductances
proc inductor_L {} {

    set cellId [iPDK_getCurrentInst]

    set nr   [iPDK_getParamValue nr_r $cellId]
    set tmps [Stof [iPDK_getParamValue s $cellId]]
    set tmpw [Stof [iPDK_getParamValue w $cellId]]
    set tmpd [Stof [iPDK_getParamValue d $cellId]]

    set ro  [expr ($nr*($tmpw+$tmps)-$tmps)/($tmpd+$nr*($tmpw+$tmps)-$tmps)]  ;# fill ratio
    set mu  [expr 3.1416*4*1e-7] ;# permeability constant
    set tmp [expr $mu*0.5*1.07*$nr*$nr*($tmpd+$nr*($tmpw+$tmps)-$tmps)*(log(2.29/$ro)+0.19*$ro*$ro)]
    iPDK_setParamValue lEstim [Ftos $tmp 3] $cellId
    set tmp [expr ($nr*($tmpd+$tmpw+($nr-1)*($tmps+$tmpw))*3.314+60e-6)/$tmpw*0.01]
    iPDK_setParamValue rEstim [Ftos $tmp 3] $cellId
}

proc inductor_d {} {

    set cellId [iPDK_getCurrentInst]

    set tmpd [Stof [iPDK_getParamValue d $cellId]]
    set d [GridFix [expr ($tmpd*5e5)*2]]
    iPDK_setParamValue d [Ftos $d 3]u $cellId

    set tmps [Stof [iPDK_getParamValue s $cellId]]
    set tmpw [Stof [iPDK_getParamValue w $cellId]]
    set tmpd [Stof [iPDK_getParamValue d $cellId]]

    set tmpDmaxS 1000u
    set tmpDmax  [Stof $tmpDmaxS]
    set tmpDminS [iPDK_getParamValue Dmin $cellId]
    set tmpDmin  [Stof $tmpDminS]

    if {$tmpd!="" && $tmpDmin!="" && $tmpDmin>$tmpd} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong distance in the center of inductor: using the minimum distance ${tmpDminS}!!"
        iPDK_setParamValue d $tmpDminS $cellId
        set tmpd $tmpDminS
    }

    if {$tmpd!="" && $tmpDmax!="" && $tmpDmax<$tmpd} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong distance in the center of inductor: using the maximum distance ${tmpDmaxS}!!"
        iPDK_setParamValue d $tmpDmaxS $cellId
        set tmpd $tmpDmaxS
    }

    inductor_L
}

proc l2_ind_lvs_cb {} {

    set cellId [iPDK_getCurrentInst]

    set m 0
    set i [iPDK_getParamValue useM1  $cellId]
    if {$i!=""} {
        set m [expr $m|1]
    }
    set i [iPDK_getParamValue useM2  $cellId]
    if {$i!=""} {
        set m [expr $m|2]
    }
    set i [iPDK_getParamValue useM3  $cellId]
    if {$i!=""} {
        set m [expr $m|4]
    }
    set i [iPDK_getParamValue useM4  $cellId]
    if {$i!=""} {
        set m [expr $m|8]
    }
    set i [iPDK_getParamValue useM5  $cellId]
    if {$i!=""} {
        set m [expr $m|16]
    }
    set i [iPDK_getParamValue useTM1 $cellId]
    if {$i!=""} {
        set m [expr $m|32]
    }
    set i [iPDK_getParamValue useTM2 $cellId]
    if {$i!=""} {
        set m [expr $m|64]
    }

    iPDK_setParamValue mergeStat $m $cellId
}



