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

#******************************************** Callback functions for taps *************************************************
# callback parameters are either l,w,td of a stripe and sides = number of stripes (1..4),
# or for sides = 0 area a and perimeter p
# allowed calculation mode is 'r only
proc CbTapCalc {calc r l w cell} {
    
    set raspec [expr [Stof [techGetParam ${cell}_raspec]]*1.0e12] ;# specific res per sq. [um] (float)
    set rpspec [expr [Stof [techGetParam ${cell}_rpspec]]*1.0e6 ] ;# specific res. per [um] perimeter (float)

    set w [expr $w*1.0e6] ;# um (needed for contact calculation)
    set l [expr $l*1.0e6]
    set a [expr $l*$w]
    set p [expr 2.0*($l+$w)]

    switch $calc {
        R {
            set result [expr 1.0/(1.0/($raspec/$a) + 1.0/($rpspec/$p))]
        }  ;# R
        l {
            set result [expr ($raspec*$rpspec- $r*$raspec*2.0*$w)/($r*$raspec*2.0+$r*$rpspec*$w)*1.0e-6] ;# in [m]
        }  ;# l
        w {
            set result [expr ($raspec*$rpspec- $r*$raspec*2.0*$l)/($r*$raspec*2.0+$r*$rpspec*$l)*1.0e-6] ;# in [m]
        }  ;# w
        wl {
            set result [expr ((-4.0*$r*$raspec + sqrt(16.0*$r*$r*$raspec*$raspec + 4.0*$r*$rpspec*$rpspec*$raspec))/(2.0*$r*$rpspec))*1.0e-6]  ;# in [m]
        }  ;# w&l
    }
    
    return $result
}

#******************************************************************************************************
# Tap callback function
proc CbTap {param} {
    
    global SG13_GRID

    # get cell name to make procedure sharing with different parameter sets possible
    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]
    if {$cell == "ptapSB"} {
        set cell ptap1
    }

    
    ## parameter limits
    # try to read minLW
    set minLW [techGetParam ${cell}_minLW]
    if {$minLW != ""} {
        set minLW [Stof $minLW]
    }
    # try to read maxLW
    set maxLW [techGetParam ${cell}_maxLW]
    if {$maxLW != ""} {
        set maxLW [Stof $maxLW]
    }

    # try to read minL/maxL
    set minL [techGetParam ${cell}_minL]
    set maxL [techGetParam ${cell}_maxL]
    set minW [techGetParam ${cell}_minW]
    set maxW [techGetParam ${cell}_maxW]

    # test, if data read, when not read: use minLW maxLW values
    if {$minL != ""} {
        set minL [Stof $minL]
    } else {
        set minL $minLW
    }
    if {$maxL != ""} {
        set maxL [Stof $maxL]
    } else {
        set maxL $maxLW
    }
    if {$minW != ""} {
        set minW [Stof $minW]
    } else {
        set minW $minLW
    }
    if {$maxW != ""} {
        set maxW [Stof $maxW]
    } else {
        set maxW $maxLW
    }
    
    set minA [expr $minW*$minL]
    set maxA [expr $maxW*$maxL]
    set minPerim [expr 2*$minW+2*$minL]
    set maxPerim [expr 2*$maxW+2*$maxL]
    
    set minR [CbTapCalc R 0.0 $maxL $maxW $cell]
    set maxR [CbTapCalc R 0.0 $minL $minW $cell]

    ## read component parameters and convert info floats
    set w [iPDK_getParamValue w $cellId]
    if {$w==""} {
        set w $minW
    } else {
        set w [Stof $w]
    }
    set l [iPDK_getParamValue l $cellId]
    if {$l==""} {
        set l $minL
    } else {
        set l [Stof $l]
    }
    set r [iPDK_getParamValue R $cellId]
    if {$r==""} {
        set r $maxR
    } else {
        set r [Stof $r]
    }
    set A [iPDK_getParamValue A $cellId]
    if {$A==""} {
        set A $minA
    } else {
        set A [Stof $A]
    }
    set Perim [iPDK_getParamValue Perim $cellId]
    if {$Perim==""} {
        set Perim $minPerim
    } else {
        set Perim [Stof $Perim]
    }
    
    set wold $w
    set lold $l
    set rold $r
    set Aold $A
    set Pold $Perim
    
    ## check the entered parameters
    switch $param {
        w {
            set w [CbRoundm $w $SG13_GRID]
            if {[Less $w $minW 0.1u]} {
                CbMessage "w set to its min. value $minW"
                set w $minW
            }
            if {[Greater $w $maxW 1u]} {
                CbMessage "w set to its max. value $maxW"
                set w $maxW
                iPDK_setParamValue w [Ftos $w 3] $cellId
            }
        }  ;# 'w
        l {
            set l [CbRoundm $l $SG13_GRID]
            if {[Less $l $minL 0.1u]} {
                CbMessage "l set to its min. value $minL"
                set l $minL
            }
            if {[Greater $l $maxL 1u]} {
                CbMessage "l set to its max. value $maxL"
                set l $maxL
                iPDK_setParamValue l [Ftos $l 3] $cellId
            }
        }  ;# l
        R {
            if {[Less $r $minR 1]} {
                CbMessage "r set to its min. value $minR"
                set r $minR
            }
            if {[Greater $r $maxR 1]} {
                CbMessage "r set to its max. value $maxR"
                set r $maxR
                iPDK_setParamValue R [Ftos $r 3] $cellId
            }
        }  ;# R
        A {
            if {[Less $A $minA 1p]} {
                CbMessage "A set to its min. value $minA"
                set A $minA
            }
            if {[Greater $A $maxA 1p]} {
                CbMessage "A set to its max. value $maxA"
                set A $maxA
                PDK_setParamValue A [Ftos $A 3] $cellId
            }
        }  ;# A
    }  ;#  switch

    ## now recalculate other params
    set calc [iPDK_getParamValue Calculate $cellId]
    switch $calc {
        "R,A" {
            if {[Less $l $minL 1u]} {
                set l $minL
            }
            if {[Greater $l $maxL 1u]} {
                set l $maxL
            }
            if {[Less $w $minW 1u]} {
                set w $minW
            }
            if {[Greater $w $maxW 1u]} {
                set w $maxW
            }
        }  ;# "R"
        "w,A" {
            if {[Less $r $minR 1]} {
                set r $minR
            }
            if {[Greater $r $maxR 1]} {
                set r $maxR
            }
            if {[Less $l $minL 1u]} {
                set l $minL
            }
            if {[Greater $l $maxL 1u]} {
                set l $maxL
            }
            set w [CbTapCalc w $r $l 0.0 $cell]
            set w [CbRoundm $w $SG13_GRID]
        }  ;# "w"
        "l,A" {
            if {[Less $r $minR 1]} {
                set r $minR
            }
            if {[Greater $r $maxR 1]} {
                set r $maxR
            }
            if {[Less $w $minW 1u]} {
                set w $minW
            }
            if {[Greater $w $maxW 1u]} {
                set w $maxW
            }
            set l [CbTapCalc l $r 0.0 $w $cell]
            set l [CbRoundm $l $SG13_GRID]
        }  ;# "l"
        "w,l,A" {
            if {[Less $r $minR 1]} {
                set r $minR
            }
            if {[Greater $r $maxR 1]} {
                set r $maxR
            }
            set w [CbTapCalc wl $r 0.0 0.0 $cell]
            set w [CbRoundm $w $SG13_GRID]
            set l $w
        }  ;# "w,l,A"
        "w,l,R" {
            set w [expr sqrt($A)]
            set w [CbRoundm $w $SG13_GRID]
            set l $w
        }   ;# "w,l,R"
        "w,R" {
            set w [CbRoundm [expr $A/$l] $SG13_GRID]
            if {$w > $maxW} {
                set w $maxW
                if {$param == A} {
                    set l [CbRoundm [expr $A/$w] $SG13_GRID]
                    CbMessage "l >= ${l} required for given area"
                    return 0
                }
            }
            if {$w < $minW} {
                set w $minW
                if {$param == A} {
                    set l [CbRoundm [expr $A/$w] $SG13_GRID]
                }
                if{$param == A} {
                    set l [CbRoundm [expr $A/$w] $SG13_GRID]
                    CbMessage "l <= ${l} required for given area"
                    return 0
                }
            }
        }  ;# "w,R"
        "l,R" {
            set l [CbRoundm [expr $A/$w] $SG13_GRID]
            if {$l > $maxL} {
                set l $maxL
                if {$param == A} {
                    set w [CbRoundm [expr[$A/$l] $SG13_GRID]
                }
            }
            if {$l < $minL} {
                set l $minL
                if {$param == A} {
                    set w [CbRoundm [expr $A/$l] $SG13_GRID]
                }
            }
        }  ;# "l,R"
    }  ;# switch
    
    set A [expr $l*$w]
    set Perim [expr 2*$l+2*$w]
    set r [CbTapCalc R 0.0 $l $w $cell]
      
    iPDK_setParamValue w [Ftos $w 3] $cellId
    iPDK_setParamValue l [Ftos $l 3] $cellId
    iPDK_setParamValue A [Ftos $A 3] $cellId
    iPDK_setParamValue Perim [Ftos $Perim 3] $cellId
    iPDK_setParamValue R [Ftos $r 3] $cellId
}
