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

#******************************************** Callback functions for diodes****************************
#******************************************************************************************************
# callback parameters are l,w,a

proc CbDiodeCalc {calc a l w cell} {
    
    set cellId [iPDK_getCurrentInst]
    
    set minL [Stof [techGetParam ${cell}_minL]]
    set minW [Stof [techGetParam ${cell}_minW]]

    if {$w < $minW} {
        CbMessage "w too small"
    }
    if {$l < $minL} {
        CbMessage "l too small"
    }

    set w [expr $w*1.0e6] ;# um (needed for contact calculation)
    set l [expr $l*1.0e6]

    switch $calc {
        a {
            set result [expr $w*$l*1.0e-12]
        }
        p {
            set result [expr ($w+$l)*2.0e-6]
        }
        l {
            set result [expr ($a/$w)*1.0e6]
        }
        w {
            set result [expr ($a/$l)*1.0e6]
        }
        wl {
            set result [expr sqrt($a)]
        }
    }
    
    return $result
}

#******************************************************************************************************
# Diode callback function

proc CbDiode {param} {
    
    global SG13_GRID
    
    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]
    
    set minL [Stof [techGetParam ${cell}_minL]]
    set minW [Stof [techGetParam ${cell}_minW]]
    set maxL [Stof [techGetParam ${cell}_maxL]]
    set maxW [Stof [techGetParam ${cell}_maxW]]
    set amin [expr $minL*$minW]
    set amax [expr $maxL*$maxW]

    # read component parameters and convert info floats
    set w [Stof [iPDK_getParamValue w $cellId]]
    set l [Stof [iPDK_getParamValue l $cellId]]
    set a [Stof [iPDK_getParamValue a $cellId]]

    if {$w > 30e-6} {
        iPDK_setParamValue w 30u $cellId
        set w 30e-6
    }
    set wold $w 
    set lold $l 
    set aold $a

    # check the entered parameters
    switch $param {
        w {
            set w [CbRoundm $w $SG13_GRID]
            if {[Less $w $minW 1e-6]} {
                CbMessage "w too small"
                set w $minW
            }
            if {[Greater $w $maxW 1e-6]} {
                CbMessage "w too large"
                set w $maxW
            }
            iPDK_setParamValue w [Ftos $w 3] $cellId
        }
        l {
            set l [CbRoundm $l $SG13_GRID]
            if {[Less $l $minL 1e-6]} {
                CbMessage "l too small"
                set l $minL
            }
            if {[Greater $l $maxL 1e-6]} {
                CbMessage "l too large"
                set l $maxL
            }
            iPDK_setParamValue l [Ftos $l 3] $cellId
        }
        a {
            if {[Less $a $amin 1e-12]} {
                CbMessage "a too small"
                set a $amin
            }
            if {[Greater $a $amax 1e-12]} {
                CbMessage "a too large"
                set a $amax
            }
            iPDK_setParamValue a [Ftos $a 3] $cellId
        }
    }

    # now recalculate other params
    set calc [iPDK_getParamValue Calculate $cellId]
    switch $calc {
        a {
            if {$w!="" && $l!=""} {
                if {[Less $l $minL 1e-6]} {
                    set l $minL
                }
                if {[Greater $l $maxL 1e-6]} {
                    set l $maxL
                }
                if {[Less $w $minW 1e-6]} {
                    set w $minW
                }
                if {[Greater $w $maxW 1e-6]} {
                    set w $maxW
                }
                set a [CbDiodeCalc a 0.0 $l $w $cell]
                iPDK_setParamValue a [Ftos $a 3] $cellId
            }
        }
        w {
            if {$a!="" && $l!=""} {
                if {[Less $l $minL 1e-6]} {
                    set l $minL
                }
                if {[Greater $l $maxL 1e-6]} {
                    set l $maxL
                }
                if {[Less $a $amin 1e-12]} {
                    set a $amin
                }
                if {[Greater $a $amax 1e-12]} {
                    set a $amax
                }

                set w [CbDiodeCalc w $a $l 0.0 $cell]
                set w [CbRoundm $w $SG13_GRID]
                iPDK_setParamValue w [Ftos $w 3] $cellId
            }
        }
        l {
            if {$a!="" && $w!=""} {
                if {[Less $w $minW 1e-6]} {
                    set w $minW
                }
                if {[Greater $w $maxW 1e-6]} {
                    set w $maxW
                }
                if {[Less $a $amin 1e-12]} {
                    set a $amin
                }
                if {[Greater $a $amax 1e-12]} {
                    set a $amax
                }

                set w [CbDiodeCalc l $a 0.0 $w $cell]
                set w [CbRoundm $l $SG13_GRID]
                iPDK_setParamValue l [Ftos $l 3] $cellId
            }
        }
        w&l {
            if {$a!=""} {
                if {[Less $a $amin 1e-12]} {
                    set a $amin
                }
                if {[Greater $a $amax 1e-12]} {
                    set a $amax
                }
                set w [CbDiodeCalc wl $a 0.0 0.0 $cell]
                set w [CbRoundm $w $SG13_GRID]
                set l $w
                iPDK_setParamValue w [Ftos $w 3] $cellId
                iPDK_setParamValue l [Ftos $l 3] $cellId
            }
        }
    }

    iPDK_setParamValue p [Ftos [CbDiodeCalc p $a $l $w $cell] 3] $cellId

    # check for error condition, restore old data in that case

    if {[Less $l $minL 1u] || [Greater $l $maxL 1u] || [Less $w $minW 1u] || [Greater $w $maxW 1u] || [Less $a $amin 1u] || [Greater $a $amax 1u]} {
        if {[Less $l $minL 1u] || [Greater $l $maxL 1u]} {
            CbMessage "${minL} < l = ${l} < ${maxL}\n"
            if {[Less $l $minL 1u]} {
                set l $minL
            }
            if {[Greater $l $maxL 1u]} {
                set l $maxL
            }
        }
        
        if {[Less $w $minW 1u] || [Greater $w $maxW 1u]} {
            CbMessage "${minW} < w = ${w} < ${maxW}\n"
            if {[Less $w $minW 1u]} {
                set w $minW
            }
            if {[Greater $w $maxW 1u]} {
                set w $maxW
            }
        }
        
        if {[Less $a $amin 1u] || [Greater $a $amax 1u]} {
            CbMessage "${amin} < a = ${a} < ${amax}\n"
            if {[Less $a $amin 1u]} {
                set a $amin
            }
            if {[Greater $a $amax 1u]} {
                set a $amax
            }
        }
        
        CbMessage "parameter value out of range - restoring last value"
        
        set a $aold
        set l $lold
        set w $wold
        
        switch $param {
            a {
                if {$w!="" && $l!=""} {
                    if {[Less $l $minL 1e-6]} {
                        set l $minL
                    }
                    if {[Greater $l $maxL 1e-6]} {
                        set l $maxL
                    }
                    if {[Less $w $minW 1e-6]} {
                        set w $minW
                    }
                    if {[Greater $w $maxW 1e-6]} {
                        set w $maxW
                    }
                    set a [CbDiodeCalc a 0.0 $l $w $cell]
                }
            }

            w {
                if {$a!="" && $l!=""} {
                    if {[Less $l $minL 1e-6]} {
                        set l $minL
                    }
                    if {[Greater $l $maxL 1e-6]} {
                        set l $maxL
                    }
                    if {[Less $a $amin 1e-12]} {
                        set a $amin
                    }
                    if {[Greater $a $amax 1e-12]} {
                        set a $amax
                    }

                    set w [CbDiodeCalc w $a $l 0.0 $cell]
                    set w [CbRoundm $w $SG13_GRID]
                }
            }

            l {
                if {$a!="" && $w!=""} {
                    if {[Less $w $minW 1e-6]} {
                        set w $minW
                    }
                    if {[Greater $w $maxW 1e-6]} {
                        set w $maxW
                    }
                    if {[Less $a $amin 1e-12]} {
                        set a $amin
                    }
                    if {[Greater $a $amax 1e-12]} {
                        set a $amax
                    }

                    set w [CbDiodeCalc l $a 0.0 $w $cell]
                    set w [CbRoundm $l $SG13_GRID]
                }
            }

            wl {
                if {$a!=""} {
                    if {[Less $a $amin 1e-12]} {
                        set a $amin
                    }
                    if {[Greater $a $amax 1e-12]} {
                        set a $amax
                    }
                    set w [CbDiodeCalc wl $a 0.0 0.0 $cell]
                    set w [CbRoundm $w $SG13_GRID]
                    set l $w
                }
            }
        }
     
        iPDK_setParamValue a [Ftos $a 3] $cellId
        iPDK_setParamValue w [Ftos $w 6] $cellId
        iPDK_setParamValue l [Ftos $l 6] $cellId
        iPDK_setParamValue p [Ftos [CbDiodeCalc p $a $l $w $cell] 3] $cellId
    }
    
    if {$cell == "pnpMPA"} {
        iPDK_setParamValue ac [Ftos [expr ($w+1.58e6)*($l+1.3e6)] 3] $cellId
        iPDK_setParamValue pc [Ftos [expr ($w+$l+2.88e6)*2] 6] $cellId
    }
}

#***********************************************************************************************************************
# CbDiodeCalc
# This callback routine is used to calculate the dnw2 (parasitic Nwell-
# Substrate diodes) Area and Perimeter for possibility of pre layout simulations.
#***********************************************************************************************************************
proc dnw_cb {} {
    
    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]

    #********************************************************************************
    # 1st step
    # get the symbols correct  values
    #********************************************************************************

    set rev2_Calculate     [string tolower [iPDK_getParamValue Calculate $cellId]]
    set rev2_p_singleWidth [expr [Stof [iPDK_getParamValue p_singleWidth $cellId]]*1e06]
    set rev2_p_Length      [expr [Stof [iPDK_getParamValue p_Length $cellId]]*1e06]
    set rev2_p_ng          [Stof [iPDK_getParamValue p_ng $cellId]]
    set rev2_p_Multiplier  [Stof [iPDK_getParamValue p_Multiplier $cellId]]
    set rev2_p_WidthMin    [expr [Stof [iPDK_getParamValue p_WidthMin $cellId]]*1e06]
    set rev2_p_LengthMin   [expr [Stof [iPDK_getParamValue p_LengthMin $cellId]]*1e06]
    
    #the below calculations should be only done when pmos mode is on!
    if {$rev2_Calculate =="pmos_w&l"} {
        
        #*******************************************************************************
        #2nd step
        # check the correct values:
        #*******************************************************************************
        
        # Check Wmin
        if {$rev2_p_singleWidth < $rev2_p_WidthMin} {
            iPDK_setParamValue p_singleWidth [Ftos [expr $rev2_p_WidthMin*1e-06] 3] $cellId
            CbMessage "\n WARNING: rev2_dnw: minimum width is 330.0n !!!"
        }
        
        # Check Lmin
        if {$rev2_p_Length < $rev2_p_LengthMin} {
            iPDK_setParamValue p_Length [Ftos [expr $rev2_p_LengthMin*1e-06] 3] $cellId
            CbMessage "\n WARNING rev2_dnw: minimum width is  240.0n !!!"
        }
        
        # Check ng
        if {$rev2_p_ng < 1} {
            set rev2_p_ng 1
            iPDK_setParamValue p_ng "1" $cellId
            CbMessage "\n WARNING rev2_dnw: minimum number of gates is 1 !!!"
        }
        
        #check m-factor
        if {$rev2_p_Multiplier < 1} {
            set rev2_p_Multiplier 1
            iPDK_setParamValue p_Multiplier "1" $cellId
            CbMessage "\n WARNING rev2_dnw: minimum m-factor is 1 !!!"
        }
        
        #*******************************************************************************
        #3rd step
        # recalculate the complete pmos Width:
        #;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
        
        set rev2_p_Width [expr [Stof [iPDK_getParamValue p_singleWidth $cellId]] * rev2_p_ng * rev2_p_Multiplier]
        iPDK_setParamValue p_Width $rev2_p_Width $cellId
        
        #;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
        #4th step
        #calculate the correct Nwell area and perimeter
        #;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
        
        #a) calculate the common rev2_dn_Width:
        
        if {$rev2_p_singleWidth < 0.72} { ;#note: small pmos could be put closer together the larger ones
            set rev2_dnw_Width = [expr (0.61 + (($rev2_p_Multiplier - 1) * 0.42) + ($rev2_p_Multiplier * 0.72))]
        } else {  ;#larger pmos devices
            set rev2_dnw_Width = [expr ((2 * 0.3) + (($rev2_p_Multiplier - 1) * 0.66) + ($rev2_p_Multiplier * $rev2_p_singleWidth))]
        }
        
        if {$rev2_dnw_Width < 1.5} {  ;# note: minimum Nwell-Width is 1.5um!!!
            set rev2_dnw_Width 1.5
        } else {
            return nil
        }
        
        #b) calculate the common rev2_dnw_Length:
        
        if {$rev2_p_singleWidth < 0.72} { ;# note: small pmos could be put closer together the larger ones
            set rev2_dnw_Length [expr ( 1.92 + 1.14 + (( $rev2_p_ng - 1) * 0.96) + ($rev2_p_ng  *  $rev2_p_Length ))]
        } else {
            set rev2_dnw_Length [expr ( 1.86 + 1.08 + (( rev2_p_ng - 1) * 0.84) + (rev2_p_ng  *  rev2_p_Length ))]
        }
        
        #c) calculate the common rev2_dnw_Area
        set rev2_dnw_Area [expr $rev2_dnw_Width * $rev2_dnw_Length]
        
        #d) calculate the common rev2_dnw_Perimeter
        set rev2_dnw_Perimeter [expr 2*($rev2_dnw_Width + $rev2_dnw_Length)]
        
        #write back Area and Perimeter into the Symbol
        iPDK_setParamValue a [Ftos [expr $rev2_dnw_Area      * 1e-12] 3] $cellId
        iPDK_setParamValue p [Ftos [expr $rev2_dnw_Perimeter * 1e-06] 3] $cellId
        
    } else {
        return nil
    }
}
