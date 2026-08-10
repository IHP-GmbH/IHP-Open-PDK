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

proc vias_cb {var} {
    
    set cellId [iPDK_getCurrentInst]
    
    switch $var {
        l {
            set l [Stof [iPDK_getParamValue l $cellId]]
            if {$l > 1e-3} {
                set l 1m
                CbMessage "l set to maximum value 1m"
            }
            set l [expr [GridFix [expr l*5e5]]*2/1e6]
            iPDK_setParamValue l [Ftos $l 4] $cellId
        }
        w {
            set w [Stof [iPDK_getParamValue w $cellId]]
            if {$w > 1e-3} {
                set w 1m
                CbMessage "w set to maximum value 1m"
            }
            set w [expr [GridFix [expr w*5e5]]*2/1e6]
            iPDK_setParamValue w [Ftos $w 4] $cellId
        }
        Rows {
            set rows [iPDK_getParamValue Rows $cellId]
            if {$rows < 1 || $rows > 50} {
                hiGetAttention
            }
            if {$rows < 1} {
                CbMessage "Rows set to its min. value 1"
                iPDK_setParamValue Rows 1 $cellId
            }
            if {$rows < 1 || $rows > 50} {
                CbMessage "Rows set to its max. value 50"
                iPDK_setParamValue Rows 50 $cellId
            }
        }
        Cols {
            set cols [iPDK_getParamValue Cols $cellId]
            if {$cols < 1 || $cols > 50} {
                hiGetAttention
            }
            if {$cols < 1} {
                CbMessage "Colums set to its min. value 1"
                iPDK_setParamValue Cols 1 $cellId
            }
            if {$cols < 1 || $cols > 50} {
                CbMessage "Colums set to its max. value 50"
                iPDK_setParamValue Cols 50 $cellId
            }
        }
    }
}


