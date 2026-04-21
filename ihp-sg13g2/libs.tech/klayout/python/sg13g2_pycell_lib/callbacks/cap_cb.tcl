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

#* Callback functions for capacitors ******************************************************************
# cap general calculation function
# CbCapCalc takes geometric values in [m]
# parameters: calc-mode capacitance length width cellname (e.g. "cmim")
# calc-mode is one of ('C 'l 'w 'lw)

proc CbCapCalc {calc c l w cell} {

    set caspec [expr [Stof [techGetParam ${cell}_caspec]] * 1e-12] ;# specific cap per sq. [um] (float)
    set cpspec [expr [Stof [techGetParam ${cell}_cpspec]] * 1e-6 ] ;# specific cap. per [um] perimeter (float)
    set lwd          [Stof [techGetParam ${cell}_lwd   ]]          ;# line width delta [m]

    set c [Stof $c]
    set l [Stof $l]
    set w [Stof $w]

    set w   [expr {$w   * 1.0e6}] ;# um (needed for contact calculation)
    set l   [expr {$l   * 1.0e6}]
    set lwd [expr {$lwd * 1.0e6}]

    set result 0
    switch $calc {
      C {
          set leff   [expr $l+$lwd]
          set weff   [expr $w+$lwd]
          set result [expr $leff*$weff*$caspec + 2.0*($leff+$weff)*$cpspec]
      }  ;# C
      l {
          set weff   [expr $w+$lwd]
          set result [expr (($c-2.0*$weff*$cpspec)/($caspec*$weff+2.0*$cpspec) - $lwd) * 1.0e-6] ;# in [m]
      }  ;# l
      w {
          set leff   [expr $l+$lwd]
          set result [expr (($c-2.0*$leff*$cpspec)/($caspec*$leff+2.0*$cpspec) - $lwd) * 1.0e-6] ;# in [m]
      }  ;# w
      lw {
          set result [expr (-2.0*$cpspec/$caspec + sqrt(4.0*$cpspec*$cpspec/($caspec*$caspec) + $c/$caspec) - $lwd) * 1.0e-6] ;# in [m]
      }  ;# lw
    }  ;# switch

    return $result
}


#******************************************************************************************************
# cap callback function
proc CbCap {param} {

    global SG13_GRID

    set RC 1

    # get cell name to make procedure sharing with different parameter sets possible
    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]

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

    set minC [Stof [techGetParam ${cell}_minC]]
    set maxC [Stof [techGetParam ${cell}_maxC]]

    # read component parameters and convert info floats
    set w [Stof [iPDK_getParamValue w  $cellId]]
    set l [Stof [iPDK_getParamValue l  $cellId]]
    set c [Stof [iPDK_getParamValue C  $cellId]]

    set wold $w
    set lold $l
    set cold $c

    # check the entered parameters
    switch $param {
        w {
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
        } ;# 'w
        l {
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
        }  ;# 'l
        C {
            if {[Less $c $minC 1f]} {
                CbMessage "c too small"
                set c $minC
            }
            if {[Greater $c $maxC 1f]} {
                CbMessage "c too large"
                set c $maxC
            }
            iPDK_setParamValue C [Ftos $c 3] $cellId
        }  ;# 'C
    }  ;# switch

    # now recalculate other params

    set calc [iPDK_getParamValue Calculate $cellId]
    switch $calc {
        C {
            if {$w!="" && $l!=""} {
                set c [CbCapCalc C 0 $l $w $cell]
                iPDK_setParamValue C [Ftos $c 3] $cellId
            }
        } ;# "c"
        w {
            if {$l!="" && $c!=""} {
                set w [CbCapCalc w $c $l 0 $cell]
                set w [CbRoundm $w $SG13_GRID]
                iPDK_setParamValue w [Ftos $w 3] $cellId
            }
        } ;# "w"
        l {
            if {$w!="" && $c!=""} {
                set l [CbCapCalc l $c 0 $w $cell]
                set l [CbRoundm $l $SG13_GRID]
                iPDK_setParamValue l [Ftos $l 3] $cellId
            }
        } ;# "l"
        w&l {
            if {$c!=""} {
                set w [CbCapCalc lw $c 0 0 $cell]
                set w [CbRoundm $w $SG13_GRID]
                if {[Greater [CbCapCalc C 0 $w $w $cell] $maxC 1f]} {
                    set w [expr $w-$SG13_GRID*1e-6] ;# ! SG13_GRID in um
                }
                set l $w
                iPDK_setParamValue w [Ftos $w 3] $cellId
                iPDK_setParamValue l [Ftos $l 3] $cellId
            }
        }  ;# "w&l"
    }  ;# switch

    # recalculate c value (may have changed due to grid rounding)
    set c [CbCapCalc C 0 $l $w $cell]

    iPDK_setParamValue C [Ftos $c 3] $cellId

    # check for error condition, restore old data in that case
    if {[Less $l $minL 1u] || [Greater $l $maxL 1u] || [Less $w $minW 1u] || [Greater $w $maxW 1u] || [Less $c $minC 1f] || [Greater $c $maxC 1f]} {
        if {[Less $l $minL 1u] || [Greater $l $maxL 1u] } {
            CbMessage [format "%s < l = %s < %s" $minL $l $maxL]
        }
        if {[Less $w $minW 1u] || [Greater $w $maxW 1u] } {
            CbMessage [format "%s < w = %s < %s" $minW $w $maxW]
        }
        if {[Less $c $minC 1f] || [Greater $c $maxC 1f] } {
            CbMessage [format "%s < c = %s < %s" $minC $c $maxC]
        }

        set RC 0
        CbMessage "parameter value out of range - restoring last value"

        set c $cold
        set l $lold
        set w $wold

        switch $param {
            C {
                if {$wold!="" && $lold!=""} {
                    set c [CbCapCalc C 0 $lold $wold $cell]
                }
            } ;# c
            w {
                if {$lold!="" && $cold!=""} {
                    set w [CbCapCalc w $cold $lold 0 $cell]
                    set w [CbRoundm $w $SG13_GRID]
                }
            } ;# w
            l {
                if {$wold!="" && $cold!=""} {
                    set l [CbCapCalc l $cold 0 $wold $cell]
                    set l [CbRoundm $l $SG13_GRID]
                }
            } ;# l
            lw {
                if {$cold!=""} {
                    set l [CbCapCalc lw $cold 0 0 $cell]
                    set l [CbRoundm $l $SG13_GRID]
                    set w $l
                }
            } ;# lw
        } ;# caseq

        iPDK_setParamValue C [Ftos $c 3] $cellId
        iPDK_setParamValue w [Ftos $w 3] $cellId
        iPDK_setParamValue l [Ftos $l 3] $cellId
    }

    return $RC
}

#*******************************************************************************
#* Callback functions for MOS varicap
#*******************************************************************************

# limit Nx and Ny multipliers
proc CbVaricap {param} {

    # get cell name to make procedure sharing with different parameter sets possible
    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]

    set minN [expr int([techGetParam ${cell}_min${param}])]
    set maxN [expr int([techGetParam ${cell}_max${param}])]


    switch $param {
        Nx {
            set oldN [expr round([Stof [iPDK_getParamValue Nx $cellId]])]   ;# no epsilon needed. Nx should be it. Round ist just be be secure
        }
        Ny {
            set oldN [expr round([Stof [iPDK_getParamValue Ny $cellId]])]   ;# no epsilon needed. Ny should be it. Round ist just be be secure
        }
    }

    if {$oldN < $minN} {
        CbMessage "${param} too small"
        set oldN $minN
    }

    if {$oldN > $maxN} {
        CbMessage "${param}  too large"
        set oldN $maxN
    }

    switch $param {
        Nx {
            iPDK_setParamValue Nx $oldN $cellId
        }
        Ny {
            iPDK_setParamValue Ny $oldN $cellId
        }
    }
}

#*******************************************************************************
#* Callback functions for SVaricap
#*******************************************************************************

# limit Nx and Ny multipliers
proc CbSVaricap {param} {

    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]

    switch $param {
        w {
            # get actual w
            set actw [iPDK_getParamValue w $cellId]
            # get min and max w and l
            set minw [techGetParam ${cell}_minw]
            set maxw [techGetParam ${cell}_maxw]
            set minl [techGetParam ${cell}_minl]
            set maxl [techGetParam ${cell}_maxl]

            # check which w and l have to be used
            set wdiff1 [expr abs([Stof $actw]-[Stof $minw])]
            set wdiff2 [expr abs([Stof $actw]-[Stof $maxw])]
            if {$wdiff1!=0 && $wdiff2!=0} {
                if {$wdiff1 < $wdiff2} {
                    set neww $minw
                    CbMessage "${param} too small\nAllowed values are ${minw} and ${maxw}. Setting to value ${neww}!"
                } else {
                    set neww $maxw
                    CbMessage "${param} too large\nAllowed values are ${minw} and ${maxw}. Setting to value ${neww}!"
                }

                # set l to the right value
                iPDK_setParamValue w $neww $cellId
            }

            set actw [iPDK_getParamValue w $cellId]

            # calculate cap / finger
            # first way: use the 2 fixed values until a formular is found
            if {$actw == $minw} {
                set newcap "14fF"
                set newl $minl
            } else {
                set newcap "97fF"
                set newl $maxl
            }

            # set cap to the right value
            iPDK_setParamValue Cap $newcap $cellId
            iPDK_setParamValue l $newl $cellId
        }
        Nx {
            set minNx [techGetParam ${cell}_minNx]
            set maxNx [techGetParam ${cell}_maxNx]
            set Nx [expr round([Stof [iPDK_getParamValue Nx $cellId]])] ;# no epsilon needed. Nx should be it. Round ist just be be secure
            if {$Nx < $minNx} {
                set Nx $minNx
                CbMessage "Setting Nx to min Value $minNx"
                iPDK_setParamValue Nx [expr int($Nx)] $cellId
            }

            if {$Nx > $maxNx} {
                set Nx $maxNx
                CbMessage "Setting Nx to max Value $minNx"
                iPDK_setParamValue Nx [expr int($Nx)] $cellId
            }
        }

        default {
            set minN [expr int([techGetParam ${cell}_min${param}])]
            set maxN [expr int([techGetParam ${cell}_max${param}])]

            switch $param {
                Nx {
                    set Nx [expr round([Stof [iPDK_getParamValue Nx $cellId]])] ;# no epsilon needed. Ny should be it. Round ist just be be secure
                }
                Ny {
                    set Nx [expr round([Stof [iPDK_getParamValue Ny $cellId]])] ;# no epsilon needed. Nx should be it. Round ist just be be secure
                }
            }

            if {$oldN < $minN} {
                CbMessage "${param} too small"
                set oldN $minN
            }
            if {$oldN > $maxN} {
                CbMessage "${param} too large"
                set oldN $maxN
            }

            switch $param {
                Nx {
                    iPDK_setParamValue Nx $oldN $cellId
                }
                Ny {
                    iPDK_setParamValue Ny $oldN $cellId
                }
            }
        }
    }

    # calculate effective area
    set l  [Stof [iPDK_getParamValue l  $cellId]]
    set w  [Stof [iPDK_getParamValue w  $cellId]]
    set Nx [Stof [iPDK_getParamValue Nx $cellId]]

    set a [expr $l*$w*$Nx]
    iPDK_setParamValue a $a $cellId
}

#***********************************************************************************************************************
# CbSVaricap_wl
#***********************************************************************************************************************
proc CbSVaricap_wl {var} {

    set cellId [iPDK_getCurrentInst]

    switch $var {
        w {
            if {[iPDK_getParamValue w $cellId] == "3.74u"} {
                iPDK_setParamValue l "0.3u" $cellId
            } else {
                iPDK_setParamValue l "0.8u" $cellId
            }
        }
        l {
            if {[iPDK_getParamValue l $cellId] == "0.3u"} {
                iPDK_setParamValue w "3.74u" $cellId
            } else {
                iPDK_setParamValue w "9.74u" $cellId
            }
        }
    }
}

#***********************************************************************************************************************
# CbSVaricap_thickO
#***********************************************************************************************************************
proc CbSVaricap_thickO {} {

    set cellId [iPDK_getCurrentInst]

    iPDK_setParamValue thickO t $cellId
    set thickOx [iPDK_getParamValue thickO $cellId]
    if {$thickOx == t} {
        set model "sg13_hv_svaricap"
    } else {
        set model "sg13_lv_svaricap"
    }

    iPDK_setParamValue model $model $cellId
}

