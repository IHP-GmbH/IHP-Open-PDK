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

#******************************************************************************************************
proc CbBondpad {param} { ;# check topMetal or bottom Metal

    set rc 1

    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]

    set metallization [techGetParam "metalName"]
    set actTopMet [iPDK_getParamValue topMetal    $cellId]
    set actBotMet [iPDK_getParamValue bottomMetal $cellId]
    set writeTM1 ""
    #set botMetText $actBotMet
    #set topMetText $actTopMet

    if {$actBotMet == "TM1"} {
        set writeTM1 1
        # Check Metallization for BotMetNumber and set to number
        if {$metallization=="M4" || $metallization=="M4M5"} {
            set actBotMet 4
        } else {
            set actBotMet 6
        }
    } else {
        set writeTC2 0
        set actBotMet [expr $actBotMet]
    }

    #*************************************
    #chek by metallistaion which number ist topMetal
    switch $param {
        topMetal {
            iPDK_setParamValue topMetal $actTopMet $cellId
        }  ;# topMetal

        bottomMetal {
            # get the number of topest Metal(4,5, 7,8 )
            set tmpTopMetNr [iPDK_getParamValue topMetal $cellId]

            if { [string length $tmpTopMetNr] == 1} {
                set topMetalNumber [expr $tmpTopMetNr]
            } else {
                set topMetalNumber [string range [iPDK_getParamValue topMetal $cellId] 2 2]       ;# hat to be 1 or 2
                set topMetalNumber [expr ${topMetalNumber}+[expr [string range $metallization 1 1]]-1 ]  ;# add 4 or 7
            }

            set newBotMet $actBotMet

            # is bottom under top?
            if {$newBotMet >= $topMetalNumber} {
                hiGetAttention
                CbMessage "WARNING: bottomMetal has to be under TopMetal!!\n topMetal:${topMetalNumber}, bottomMetal:${actBotMet}"
                iPDK_setParamValue bottomMetal 1 $cellId
                set newBotMet [expr $topMetalNumber-1]
                set writeTM1 0
                set rc 0
            }

            # Set botMetValue in every Case to fix CDF Update
            set actBotMet $newBotMet
            if {$writeTM1 != ""} {
                iPDK_setParamValue bottomMetal "TM1" $cellId
            } else {
                iPDK_setParamValue bottomMetal $actBotMet $cellId
            }
        }

        t {
            CbMessage "You must'n be here\nI think You found a bug. Congratulation."
            set rc 0
        }
    }

    return $rc
}

#******************************************************************************************************
proc bondpad_cb {param} {

    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]

    set diam [Stof [iPDK_getParamValue diameter $cellId]]
    set hwq  [Stof [iPDK_getParamValue hwquota  $cellId]]

    if {$hwq > 8.} {
        set hwq 8
        iPDK_setParamValue hwquota [Ftos $hwq] $cellId
    }

    if {[expr $hwq] < 0.125} {
        set hwq 0.125
        iPDK_setParamValue hwquota [Ftos $hwq] $cellId
    }

    set typ  [iPDK_getParamValue padType  $cellId]
    set flip [iPDK_getParamValue FlipChip $cellId]
    set diamsmall [expr min($diam*$hwq, $diam/$hwq)]

    if {$typ == "probepad"} {
        set minsize [Stof 40u]
    } else {
        set minsize [Stof 60u]
    }
    if {$flip == "yes"} {
        set minsize [Stof 80u]
    }

    switch $param {
        hwquota {
            if {$hwq == 1} {
                return t
            }
            if {$diamsmall >= $minsize} {
                return t
            }
            if {$hwq > 1} {
                set hwq [expr max($hwq*$diamsmall/$minsize,1.)]
            } else {
                set hwq [expr min($hwq*$minsize/$diamsmall,1.)]
            }
            iPDK_setParamValue hwquota [Ftos $hwq 4] $cellId
        }
        diameter {
            if {$diam > 500e-6} {
                iPDK_setParamValue diameter "500u" $cellId
                return t
            }
            if {$diamsmall < $minsize} {
                set diam [expr $diam*($minsize/$diamsmall)]
                set diam [expr [GridFix [expr $diam*5e5]]/5e5]
                iPDK_setParamValue diameter [Ftos $diam 3] $cellId
                return t
            }
            set diam [expr [GridFix [expr $diam*5e5]]/5e5]
            iPDK_setParamValue diameter [Ftos $diam 3] $cellId
            set v [Stof [iPDK_getParamValue passEncl $cellId]]
            if {$v+$v > $diam-20e-6} {
                iPDK_setParamValue passEncl [Ftos [expr $diam*0.5-10e-6] 3] $cellId
            }
            return t
        }
        padType {
            if {$diamsmall < $minsize} {
                set diam [expr $diam*($minsize/$diamsmall)]
                set diam [expr [GridFix [expr ($diam*5e5)]]/5e5]
                iPDK_setParamValue diameter [Ftos $diam 3] $cellId
                return t
            }
        }
        passEncl {
            if {$flip == yes} {
                set minEncl 10.0
            } else {
                set minEncl [techGetParam "Pas_c"]
            }
            set v [GridFix [expr [Stof [iPDK_getParamValue passEncl $cellId]*1e6]]]
            if {$v < $minEncl} {
                set v $minEncl
            }
            if {$v > [expr $diam*5e5-10]} {
                set v [expr $diam*5e5-10]
            }
            iPDK_setParamValue passEncl [Ftos [expr $v/1e6] 3] $cellId
            return t
        }
        FlipChip {
            if {$diamsmall < $minsize} {
                set diam [expr $diam*($minsize/$diamsmall)]
                iPDK_setParamValue diameter [Ftos $diam 3] $cellId
            }
            if {$flip == "yes"} {
                set v [GridFix [expr [Stof [iPDK_getParamValue passEncl $cellId]*1e6]]]
                if {$v < 10.0} {
                    iPDK_setParamValue passEncl "10u" $cellId
                }
            }
            return t
        }
    }
}

#******************************************************************************************************
proc CbSealring {} {  ;# check topMetal of sealring

    set rc t
    set cellId [iPDK_getCurrentInst]

    set metallization [techGetParam metalName]
    set actTopMet [iPDK_getParamValue topMetal $cellId]

    #*************************************
    # check, if clicked TopMetal is in metallisation
    switch $actTopMet {
        TkAl {
            if {$metallization=="M4"||$metallization=="M6"||$metallization=="M7"} {
                hiGetAttention
                CbMessage "WARNING: TkAl is not allowed in ${metallization}!!"
                iPDK_setParamValue topMetal "TC2" $cellId
                set rc nil
            } else {
                 iPDK_setParamValue topMetal actTopMet $cellId
             }
        }
    }

    return rc
}

