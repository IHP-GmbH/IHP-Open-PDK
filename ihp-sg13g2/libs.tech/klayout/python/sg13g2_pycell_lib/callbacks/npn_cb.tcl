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

#***********************************************************************************************************************
# NLCB_npn_we
#***********************************************************************************************************************
proc NLCB_npn_we {} {
    
    global SG13_EPSILON2

    set tmpwe [Stof [iPDK_getParamValue we $cellId]]
    set tmple [Stof [iPDK_getParamValue le $cellId]]
    set tmpNx [expr int([iPDK_getParamValue Nx $cellId])]
    set tmpNy [expr int([iPDK_getParamValue Ny $cellId])]
    set Iarea [Stof [iPDK_getParamValue Iarea $cellId]]
    
    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]

    set wemin [Stof [techGetParam ${cell}_minWE]]
    if {$wemin == 0.0} {
        set wemin 0.42e-6
    }
    set wemax [Stof [techGetParam ${cell}_maxWE]]
    if {$wemax == 0.0} {
        set wemax 0.42e-6
    }
    
    set tmpwe [GridFix $tmpwe]
    set tmple [GridFix $tmple] 

    if {$tmpwe != "" && $tmpwe<$wemin-$SG13_EPSILON2} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong width: using minimum width ${wemin}!!"
        iPDK_setParamValue we [Ftos $wemin 3] $cellId
        set tmpwe [Stof [iPDK_getParamValue we $cellId]]
    }

    if {$tmpwe != "" && $tmpwe>$wemax+$SG13_EPSILON2} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong width: using maximum width ${wemax}!!"
        iPDK_setParamValue we [Ftos $wemax 3] $cellId
        set tmpwe [Stof [iPDK_getParamValue we $cellId]]
    }

    iPDK_setParamValue we [Ftos [GridFix [expr $tmpwe*1.0e6]] 3]u $cellId
    set tmpwe [Stof [iPDK_getParamValue we $cellId]]
    iPDK_setParamValue Icmax [Ftos [expr $Iarea*$tmpwe*$tmple*$tmpNx*$tmpNy*1e12] 3] $cellId
}

#***********************************************************************************************************************
# NLCB_npn_le
#***********************************************************************************************************************
proc NLCB_npn_le {} {
    
    global SG13_EPSILON2

    set tmpwe [Stof [iPDK_getParamValue we $cellId]]
    set tmple [Stof [iPDK_getParamValue le $cellId]]
    set tmpNx [expr int([iPDK_getParamValue Nx $cellId])]
    set tmpNy [expr int([iPDK_getParamValue Ny $cellId])]
    set Iarea [Stof [iPDK_getParamValue Iarea $cellId]]
    
    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]

    set lemin [Stof [techGetParam ${cell}_minLE]]
    if {$lemin == 0.0} {
        set lemin 0.84e-6
    }
    set lemax [Stof [techGetParam ${cell}_maxLE]]
    if {$lemax == 0.0} {
        set lemax 3.36e-6
    }

    if {$tmple != "" && $tmple<$lemin-$SG13_EPSILON2} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong length: using minimum length ${lemin}!!"
        iPDK_setParamValue le [Ftos $lemin 3] $cellId
        set tmple [Stof [iPDK_getParamValue le $cellId]]
    }

    if {$tmple != "" && $tmple>$lemax+$SG13_EPSILON2} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong length: using maximum length ${lemax}!!"
        iPDK_setParamValue le [Ftos $lemax 3] $cellId
        set tmple [Stof [iPDK_getParamValue le $cellId]]
    }

    iPDK_setParamValue le [Ftos [GridFix [expr $tmple*1.0e6]] 3]u $cellId
    iPDK_setParamValue Icmax [Ftos [expr $Iarea*$tmpwe*$tmple*$tmpNx*$tmpNy*1e12] 3] $cellId
}

#***********************************************************************************************************************
# NLCB_npn_Ny
#***********************************************************************************************************************
proc NLCB_npn_Ny {} {
    
    global SG13_EPSILON2

    set cellId [iPDK_getCurrentInst]

    set tmpwe [Stof [iPDK_getParamValue we $cellId]]
    set tmple [Stof [iPDK_getParamValue le $cellId]]
    set tmpNx [expr int(int([iPDK_getParamValue Nx $cellId])+$SG13_EPSILON2)]
    set tmpNy [expr int(int([iPDK_getParamValue Ny $cellId])+$SG13_EPSILON2)]
    set Iarea [Stof [iPDK_getParamValue Iarea $cellId]]
    
    set cell   [iPDK_getInstCellName $cellId]

    set Nymin [expr int([techGetParam ${cell}_minNY])]
    if {$Nymin == 0} {
        set Nymin 1
    }
    set Nymax [expr int([techGetParam ${cell}_maxNY])]
    if {$Nymax == 0} {
        set Nymax 2
    }

    if {$tmpNy != "" && $tmpNy<$Nymin-$SG13_EPSILON2} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong y emitter count: using minimum ${Nymin}!!"
        iPDK_setParamValue Ny $Nymin $cellId
    }

    if {$tmpNy != "" && $tmpNy>$Nymax+$SG13_EPSILON2} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong y emitter count: using maximum ${Nymax}!!"
        iPDK_setParamValue Ny $Nymax $cellId
    }

    iPDK_setParamValue Icmax [Ftos [expr $Iarea*$tmpwe*$tmple*$tmpNx*$tmpNy*1e12] 3] $cellId
}

#***********************************************************************************************************************
# NLCB_npn_Nx
#***********************************************************************************************************************
proc NLCB_npn_Nx {{change nil}} {
    
    global SG13_EPSILON2

    set tmpwe [Stof [iPDK_getParamValue we $cellId]]
    set tmple [Stof [iPDK_getParamValue le $cellId]]
    set tmpNx [expr int(int([iPDK_getParamValue Nx $cellId])+$SG13_EPSILON2)]
    set tmpNy [expr int(int([iPDK_getParamValue Ny $cellId])+$SG13_EPSILON2)]
    set Iarea [Stof [iPDK_getParamValue Iarea $cellId]]
    
    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]

    set Nxmin [expr int([techGetParam ${cell}_minNX])]
    if {$Nxmin == 0} {
        set Nxmin 1
    }
    set Nxmax [expr int([techGetParam ${cell}_maxNX])]
    if {$Nxmax == 0} {
        set Nxmax 8
    }
    set defNX [techGetParam ${cell}_defNX]

    if {$tmpNx != "" && $tmpNx<$Nxmin-$SG13_EPSILON2} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong x emitter count: using minimum ${Nxmin}!!"
        iPDK_setParamValue Nx $Nxmin $cellId
        set tmpNx [expr int($Nxmin+$SG13_EPSILON2)]
    }

    if {$tmpNx != "" && $tmpNx>$Nxmax+$SG13_EPSILON2} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong x emitter count: using maximum ${Nxmax}!!"
        iPDK_setParamValue Nx $Nxmax $cellId
        set tmpNx [expr int($Nxmax+$SG13_EPSILON2)]
    }

    iPDK_setParamValue Icmax [Ftos [expr $Iarea*$tmpwe*$tmple*$tmpNx*$tmpNy*1e12] 3] $cellId
    
    #unless( ((boundp('GLOBAL_EDITABLE) && GLOBAL_EDITABLE  == t) || change=="t")
    if {$change == t} {
        set nx [iPDK_getParamValue Nx $cellId]
        if {$nx != $defNX} {
            CbMessage "Error: Don't change x-Multiplier!\nUsing default value"
            iPDK_setParamValue Nx $defNX $cellId
        }
    }
}

#***********************************************************************************************************************
# NLCB_npnG2_Nx
#***********************************************************************************************************************
proc NLCB_npnG2_Nx {{change nil}} {
    
    global SG13_EPSILON2

    set cellId [iPDK_getCurrentInst]

    set tmpwe [Stof [iPDK_getParamValue we $cellId]]
    set tmple [Stof [iPDK_getParamValue le $cellId]]
    set tmpNx [expr int(int([iPDK_getParamValue Nx $cellId])+$SG13_EPSILON2)]
    set tmpNy [expr int(int([iPDK_getParamValue Ny $cellId])+$SG13_EPSILON2)]
    set Iarea [Stof [iPDK_getParamValue Iarea $cellId]]
    
    set cell   [iPDK_getInstCellName $cellId]

    set Nxmin [expr int([techGetParam ${cell}_minNX])]
    if {$Nxmin == 0} {
        set Nxmin 1
    }
    set Nxmax [expr int([techGetParam ${cell}_maxNX])]
    if {$Nxmax == 0} {
        set Nxmax 8
    }
    set defNX [techGetParam ${cell}_defNX]

    if {$tmpNx != "" && $tmpNx<$Nxmin-$SG13_EPSILON2} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong x emitter count: using minimum ${Nxmin}!!"
        iPDK_setParamValue Nx $Nxmin $cellId
        set tmpNx [expr int($Nxmin+$SG13_EPSILON2)]
    }

    if {$tmpNx != "" && $tmpNx>$Nxmax+$SG13_EPSILON2} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong x emitter count: using maximum ${Nxmax}!!"
        iPDK_setParamValue Nx $Nxmax $cellId
        set tmpNx [expr int($Nxmax+$SG13_EPSILON2)]
    }

    iPDK_setParamValue Icmax [Ftos [expr $Iarea*$tmpNx*1e3] 3]m $cellId
    
    #unless( ((boundp('GLOBAL_EDITABLE) && GLOBAL_EDITABLE  == t) || change=="t")
    if {$change == t} {
        set nx [iPDK_getParamValue Nx $cellId]
        if {$nx != $defNX} {
            CbMessage "Error: Don't change x-Multiplier!\nUsing default value"
            iPDK_setParamValue Nx $defNX $cellId
        }
    }
}

#***********************************************************************************************************************
# NLCB_npnG2L_Nx
#***********************************************************************************************************************
proc NLCB_npnG2L_Nx {{change nil}} {
    
    global SG13_EPSILON2

    set cellId [iPDK_getCurrentInst]

    set tmpwe [Stof [iPDK_getParamValue we $cellId]]
    set tmple [Stof [iPDK_getParamValue le $cellId]]
    set tmpNx [expr int(int([iPDK_getParamValue Nx $cellId])+$SG13_EPSILON2)]
    #set tmpNy [expr int(int([iPDK_getParamValue Ny $cellId])+$SG13_EPSILON2)]
    set Iarea [Stof [iPDK_getParamValue Iarea $cellId]]
    
    set cell   [iPDK_getInstCellName $cellId]

    set Nxmin [expr int([techGetParam ${cell}_minNX])]
    if {$Nxmin == 0} {
        set Nxmin 1
    }
    set Nxmax [expr int([techGetParam ${cell}_maxNX])]
    if {$Nxmax == 0} {
        set Nxmax 8
    }
    set defNX [techGetParam ${cell}_defNX]

    if {$tmpNx != "" && $tmpNx<$Nxmin-$SG13_EPSILON2} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong x emitter count: using minimum ${Nxmin}!!"
        iPDK_setParamValue Nx $Nxmin $cellId
        set tmpNx [expr int($Nxmin+$SG13_EPSILON2)]
    }

    if {$tmpNx != "" && $tmpNx>$Nxmax+$SG13_EPSILON2} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong x emitter count: using maximum ${Nxmax}!!"
        iPDK_setParamValue Nx $Nxmax $cellId
        set tmpNx [expr int($Nxmax+$SG13_EPSILON2)]
    }

    iPDK_setParamValue Icmax [Ftos [expr $Iarea*$tmple*$tmpNx*1e6] 3] $cellId
    
    #unless( ((boundp('GLOBAL_EDITABLE) && GLOBAL_EDITABLE  == t) || change=="t")
    if {$change == t} {
        set nx [iPDK_getParamValue Nx $cellId]
        if {$nx != $defNX} {
            CbMessage "Error: Don't change x-Multiplier!\nUsing default value"
            iPDK_setParamValue Nx $defNX $cellId
        }
    }
}

#***********************************************************************************************************************
# NLCB_npnG2L_le
#***********************************************************************************************************************
proc NLCB_npnG2L_le {} {
    
    global SG13_EPSILON2

    set cellId [iPDK_getCurrentInst]

    set tmpwe [Stof [iPDK_getParamValue we $cellId]]
    set tmple [Stof [iPDK_getParamValue le $cellId]]
    set tmpNx [expr int([iPDK_getParamValue Nx $cellId])]
    #set tmpNy [expr int([iPDK_getParamValue Ny $cellId])]
    set Iarea [Stof [iPDK_getParamValue Iarea $cellId]]
    
    set lemin [Stof 1.0e-6]
    set lemax [Stof 2.5e-6]

    if {$tmple != "" && $tmple<$lemin-$SG13_EPSILON2} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong length: using minimum length ${lemin}!!"
        iPDK_setParamValue le [Ftos $lemin 3] $cellId
        set tmple [Stof [iPDK_getParamValue le $cellId]]
    }

    if {$tmple != "" && $tmple>$lemax+$SG13_EPSILON2} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong length: using maximum length ${lemax}!!"
        iPDK_setParamValue le [Ftos $lemax 3] $cellId
        set tmple [Stof [iPDK_getParamValue le $cellId]]
    }

    iPDK_setParamValue Icmax [Ftos [expr $Iarea*$tmple*$tmpNx*1e6] 3] $cellId
}

#***********************************************************************************************************************
# NLCB_npnG2V_le
#***********************************************************************************************************************
proc NLCB_npnG2V_le {} {
    
    global SG13_EPSILON2

    set cellId [iPDK_getCurrentInst]

    set tmpwe [Stof [iPDK_getParamValue we $cellId]]
    set tmple [Stof [iPDK_getParamValue le $cellId]]
    set tmpNx [expr int([iPDK_getParamValue Nx $cellId])]
    #set tmpNy [expr int([iPDK_getParamValue Ny $cellId])]
    set Iarea [Stof [iPDK_getParamValue Iarea $cellId]]
    
    set lemin [Stof 1.0e-6]
    set lemax [Stof 5e-6]

    if {$tmple != "" && $tmple<$lemin-$SG13_EPSILON2} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong length: using minimum length ${lemin}!!"
        iPDK_setParamValue le [Ftos $lemin 3] $cellId
        set tmple [Stof [iPDK_getParamValue le $cellId]]
    }

    if {$tmple != "" && $tmple>$lemax+$SG13_EPSILON2} {
        hiGetAttention
        hiGetAttention
        CbMessage "WARNING: wrong length: using maximum length ${lemax}!!"
        iPDK_setParamValue le [Ftos $lemax 3] $cellId
        set tmple [Stof [iPDK_getParamValue le $cellId]]
    }

    iPDK_setParamValue Icmax [Ftos [expr $Iarea*$tmple*$tmpNx*1e6] 3] $cellId
}

#******************************************************************************************************
# Scalable NPN callback function
proc CbNpn {param} {
    
    global SG13_GRID

    # get cell name to make procedure sharing with different parameter sets possible
    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId] 
    
    set minLE [Stof [techGetParam ${cell}_minLE]]
    set maxLE [Stof [techGetParam ${cell}_maxLE]]
    set minWE [Stof [techGetParam ${cell}_minWE]]
    set maxWE [Stof [techGetParam ${cell}_maxWE]]
    
    # read component parameters and convert info floats
    set we [Stof [iPDK_getParamValue we $cellId]]
    set le [Stof [iPDK_getParamValue le $cellId]]

    # check the entered parameters
    switch $param {
        we {
            set we [CbRoundm $we $SG13_GRID]
            if {[Less $we $minWE 1u]} {
                CbMessage "w too small"
                set we $minWE
            }
            if {[Greater $we $maxWE 1u]} {
                CbMessage "w too large"
                set we $maxWE
            }
            iPDK_setParamValue we [Ftos $we 3] $cellId
        }
        
        le {
            set le [CbRoundm $le $SG13_GRID]
            if {[Less $le $minLE 1u]} {
                CbMessage "l too small"
                set le $minLE
            }
            if {[Greater $le $maxLE 1u]} {
                CbMessage "l too large"
                set le $maxLE
            }
            iPDK_setParamValue we [Ftos $le 3] $cellId
        }
    }
}
