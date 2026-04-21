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
#*
#* Callback functions for isolbox
#*
#*******************************************************************************
#-------------------------------------------------------------------------------
proc isol_w {} {
#-------------------------------------------------------------------------------
#   Callback function for a "w"-parameter.
#
    set cellId [iPDK_getCurrentInst]

    set tmpw [Stof [iPDK_getParamValue w $cellId]]

    set tmpWminS [iPDK_getParamValue Wmin $cellId]
    set tmpWmin  [Stof $tmpWminS]

    if {$tmpw != "" && $tmpw>15e-3} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong width: using minimum width ${tmpWminS}!!"
        iPDK_setParamValue w $tmpWminS $cellId
    }

    if {$tmpw != "" && $tmpWmin!="" && $tmpWmin>$tmpw} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong width: using minimum width ${tmpWminS}!!"
        iPDK_setParamValue w $tmpWminS $cellId
    }

    set tmpw [Stof [iPDK_getParamValue w $cellId]]
    set tmpl [Stof [iPDK_getParamValue l $cellId]]

    set area  [expr $tmpw*$tmpl]
    set perim [expr 2*($tmpw+$tmpl)]
    set tmpw  [GridFix [expr ($tmpw*1.0e6)]]

    iPDK_setParamValue w [Ftos $tmpw 3]u $cellId
    iPDK_setParamValue a [Ftos [GridFix [expr ($area*1.0e12)]] 6]p $cellId
    iPDK_setParamValue p [Ftos [GridFix [expr ($perim*1.0e6)]] 6]u $cellId
}

#************************************************************************************************************************
#-------------------------------------------------------------------------------
proc isol_l {} {
#-------------------------------------------------------------------------------
#   Callback function for a "l"-parameter.
#
    set cellId [iPDK_getCurrentInst]

    set tmpl [Stof [iPDK_getParamValue l $cellId]]

    set tmpLminS [iPDK_getParamValue Lmin $cellId]
    set tmpLmin  [Stof $tmpLminS]

    if {$tmpl != "" && $tmpl>15e-3} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong length: using minimum length ${tmpLminS}!!"
        iPDK_setParamValue l $tmpLminS $cellId
    }

    if {$tmpl != "" && $tmpLmin!="" && $tmpLmin>$tmpl} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong length: using minimum length ${tmpLminS}!!"
        iPDK_setParamValue l $tmpLminS $cellId
    }

    set tmpw [Stof [iPDK_getParamValue w $cellId]]
    set tmpl [Stof [iPDK_getParamValue l $cellId]]

    set area  [expr $tmpw*$tmpl]
    set perim [expr 2*($tmpw+$tmpl)]
    set tmpl  [GridFix [expr ($tmpl*1.0e6)]]

    iPDK_setParamValue l [Ftos $tmpl 3]u $cellId
    iPDK_setParamValue a [Ftos [GridFix [expr ($area*1.0e12)]] 6]p $cellId
    iPDK_setParamValue p [Ftos [GridFix [expr ($perim*1.0e6)]] 6]u $cellId
}

#************************************************************************************************************************
#-------------------------------------------------------------------------------
proc isol_well {} {
#-------------------------------------------------------------------------------
#   Callback function for a "w"-parameter.
#
    set cellId [iPDK_getCurrentInst]

    set tmpw [expr [Stof [iPDK_getParamValue w $cellId]]*1.0e6]
    set tmpl [expr [Stof [iPDK_getParamValue l $cellId]]*1.0e6]
    set well [iPDK_getParamValue wellwidth $cellId]

    if {$well == "1.05u"} {
        set tmpminw 3.6u
        set tmpminl 3.6u
        iPDK_setParamValue pwell_w 0 $cellId
        iPDK_setParamValue Bv 10.8 $cellId
    } else {
        set tmpminw 4.5u
        set tmpminl 4.5u
    }

    set tmpwellwidth [expr [Stof [iPDK_getParamValue wellwidth $cellId]]*1.0e6]
    if {$tmpwellwidth < 0.85} {
        iPDK_setParamValue wellwidth 0.85u $cellId
        CbMessage "WARNING: wellwidth reset according to minimum Isolbox NWell width 0.85u"
    }

    iPDK_setParamValue Wmin $tmpminw $cellId
    iPDK_setParamValue Lmin $tmpminl $cellId
    iPDK_setParamValue a [Ftos [expr   ($tmpw*$tmpl)] 3]p $cellId
    iPDK_setParamValue p [Ftos [expr 2*($tmpw+$tmpl)] 3]u $cellId

    isol_w
    isol_l
}

#************************************************************************************************************************
proc isolbox_cb {arg} {

    set cellId [iPDK_getCurrentInst]

    set a 64.24
    set b 68.59
    set c 0.56491

    switch arg {
        Bv {
            set bv [Stof [iPDK_getParamValue Bv $cellId]]
            if {$bv <= 10.8} {
                set bv 10.8
                iPDK_setParamValue Bv $bv $cellId
                set w 0
            } else {
                if {$bv < $a} {
                    set w [expr log(($a-$bv)/$b)/log($c)]
                } else {
                    set w 10
                }

                if {$w < 0.62} {
                    set w 0.62
                    set bv [expr $a-$b*pow($c,$w)]
                    CbMessage "WARNING: Bv reset according to minimum PWellBlock width 1.5u"
                    hiGetAttention
                    hiGetAttention
                    iPDK_setParamValue Bv [Ftos $bv 2] $cellId
                }
                if {$w >= 10} {
                    set w 10
                    set bv [expr $a-$b*pow($c,$w)]
                    CbMessage "WARNING: Bv reset according to maximum PWellBlock width 10u"
                    hiGetAttention(
                    hiGetAttention
                    iPDK_setParamValue Bv [Ftos $bv 2] $cellId
                }
            }
            set w [GridFix $w]
            iPDK_setParamValue pwell_w ${w}u $cellId
        }
        calculate {
            set comp [iPDK_getParamValue compute $cellId]
            if {$comp == "Bv"} {
                isolbox_cb pwell_w
            } else {
                isolbox_cb Bv
            }
        }
        pwell_w {
            set w [Stof [iPDK_getParamValue pwell_w $cellId]]
            set w [expr $w*1e6]
            set w [GridFix $w]
            iPDK_setParamValue pwell_w ${w}u $cellId

            if {$w > 0 && $w < 0.62} {
                 hiGetAttention
                 hiGetAttention
                 CbMessage "WARNING: PWellBlock width < 0.62u, set to 0"
                 iPDK_setParamValue pwell_w 0 $cellId
                 set w 0
            }

            if {$w > 10} {
                hiGetAttention
                hiGetAttention
                CbMessage "WARNING: PWellBlock width > 10u, set to 10u"
                iPDK_setParamValue pwell_w 10u $cellId
                set w 10
            }

            if {$w >= 0.5} {
                set bv [expr $a-$b*pow($c,$w)]
            } else {
                set bv 10.8
            }

            iPDK_setParamValue Bv [Ftos $bv 2] $cellId
        }
    }
}

#***********************************************************************************
proc isolbox_done {cellId} {

    set width [Stof [iPDK_getParamValue w $cellId]]
    set length [Stof [iPDK_getParamValue l $cellId]]
    set wellwidth [Stof [iPDK_getParamValue wellwidth $cellId]]

    set aw [expr ($width-$wellwidth)*($length-$wellwidth)]
    set pw [expr ($width+$length)*2-$wellwidth*8]
    iPDK_setParamValue aw [Ftos $aw 6] $cellId
    iPDK_setParamValue pw [Ftos $pw 6] $cellId
}

