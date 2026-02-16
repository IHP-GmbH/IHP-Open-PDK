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
# Rings the bell in the keyboard or terminal

proc hiGetAttention {} {
    puts -nonewline "\a" 
    flush stdout
}

proc Stof {value} {

    return [iPDK_engToSci $value]
}

proc Stoi {value} {

    return [expr int([iPDK_engToSci $value])]
}

proc GridFix {value} {
    
    global SG13_IGRID
    global SG13_EPSILON
    global SG13_GRID
    
    #fix(x*SG13_IGRID+SG13_EPSILON)*SG13_GRID ; always use "nice" numbers, as 1/grid may be irrational
    return [expr int($value*$SG13_IGRID+$SG13_EPSILON)*$SG13_GRID]
}

proc Snap {value} {
    
    return [GridFix $value]
}

proc even {x} {
    
    return [expr ($x%2)==0]
}

proc odd {x} {
    
    return [expr ($x%2)!=0]
}

#******************************************************************************************************
# print error message in CIW

proc CbError {s} {
    
    global IHP_iPDK_CbMsg
    
    #hiGetAttention() hiGetAttention()
    #hiRaiseWindow(window(1))

    puts $s      ;# automatically set CbMsg variable
    set IHP_iPDK_CbMsg $s ;# return error message
} ;# CbError

#******************************************************************************************************
# float to string. f = float, n=number of digits after comma

proc Ftos {f {n 3}} {
    
    set newf    $f
    set iso     0
    set suffix  "" 
    set absnew  [expr abs($newf)]
    
    # block for capturing 0.0
    if {$absnew == 0.0} {
        set iso 0
    } else {
        if {$absnew >= 1.0} {
            while {$absnew > 1.0e3} {
               set newf   [expr $newf / 1000.0]
               set absnew [expr abs($newf)]
               incr iso
            }
         } else {
            while {$absnew < 0.09} {
               set newf   [expr $newf * 1000.0]
               set absnew [expr abs($newf)]
               incr iso -1
            }
        } ;# if absnew >= 1.0
    }     ;# if absnew == 0.0

    switch $iso {
        1 {
            set suffix k
        }
        2 {
            set suffix M
        }
        3 {
            set suffix G
        }
        4 {
            set suffix P
        }
        5 {
            set suffix E
        }
        -1 {
            set suffix m
        }
        -2 {
            set suffix u
        }
        -3 {
            set suffix n
        }
        -4 {
            set suffix p
        }
        -5 {
            set suffix f
        }
        -6 {
            set suffix a
        }
    } ;# case iso

    set result [format %0.${n}f $newf]
    
    # remove trailng zeroes
    while {[string range $result end end] == 0 && [string range $result end-1 end-1] != "."} {
        set result [string range $result 0 end-1]
    }
    
    if {$suffix != ""} {
        set result ${result}${suffix}
    }
     
    return $result
}

#******************************************************************************************************
# round size (in m) to grid (in um), return [m]
proc CbRoundm {x rgrid} {
    
    global SG13_EPSILON

   # Give Waring, if Value is too big
   if {$x >= 2.1} {
       CbMessage [format "Given Value of %f is too big. Gave me um istead of m?" $x]
   }
   
   return [expr int($x*1.0e6/$rgrid+0.5+$SG13_EPSILON)*$rgrid/1.0e6]
   ;)
}
   
#******************************************************************************************************
# round size (in um) to grid (in um), return [um]
proc CbRoundum {x rgrid} {

    global SG13_EPSILON
    return [expr int($x/$rgrid+0.5+$SG13_EPSILON)*$rgrid]

}

#*****************************************************************************************************
#with Function "Less (a b)" is a< b (1 - eps) compared or,when "Less(a b c)" is a>b-(c*eps) compared

proc Less {var1 var2} {
    
    global SG13_EPSILON
    set eps $SG13_EPSILON

    if { $var1 < [expr $var2*(1-$eps)]} {
        return 1
    } else {
        return 0
    }
}

proc Less {var1 var2 var3} {
    
    global SG13_EPSILON
    set eps $SG13_EPSILON
    
    set var3 [Stof $var3]
    
    if { $var1 < [expr $var2-($var3*$eps)]} {
        return 1
    } else {
        return 0
    }
}

#*****************************************************************************************************
# Function "Greater(a b)" is compared a> b*(1 + eps) or,when "Greater(a b c)" is a>b+(c*eps) compared

proc Greater {var1 var2} {

    global SG13_EPSILON
    set eps $SG13_EPSILON

    if { $var1 > [expr $var2*(1+$eps)]} {
        return 1
    } else {
        return 0
    }
}

proc Greater {var1 var2 var3} {

    global SG13_EPSILON
    set eps $SG13_EPSILON
    
    set var3 [Stof $var3]

    if {$var1 > [expr $var2+$var3*$eps]} {
        return 1
    } else {
        return 0
    }
}

#******************************************************************************************************
# Check if a CDF string contains a pure number or if it contains variables/expressions. If not, return the number
# as a float

proc IsNumberString {str} {

    set x 0
    set str1 $str
    set str_end [string range $str1 end end]

    if {[string is alpha $str_end]} {
        set str1 [string range $str1 0 end-1]
    }
    
    if {$str != ""} {
        if {[string is integer $str1]} {
            set x [Stof $str]
        } else {
            if {[string is double $str1]} {
                set x [Stof $str]
            } 
        }
    } 
    
    return $x
}

proc CbRange {name minval maxval grid args}  {   ;#{info long} {allowzero 0} {beep t}
    
    set info long
    set beep t
    set allowzero 0
    
    if {$args != ""} {
        set arglen [llength $args]
        set i 0
        while {$i < $arglen} {
            set n [lindex $args $i]
            set v [lindex $args [incr i]]
            incr i
            
            if {$n == "?info"} {
                set info $v
            }
            if {$n == "?beep"} {
                set beep $v
            }
            if {$n == "?allowzero"} {
                set allowzero $v
            }
        }
    }
    
    set cellId [iPDK_getCurrentInst]

    set val [Stof [iPDK_getParamValue $name $cellId]]
    
    set minval [Stof $minval]
    set maxval [Stof $maxval]
    #set grid   [expr $grid]
    
    if {$allowzero != 0 && $val == 0.} {
        return t
    }
    
    if {$val < $minval} {
        if {$info == "short"} {
            set var [Ftos $minval 6]
            CbMessage "value below lower limit, set to ${var}"
        }
        if {$info == "long"} {
            set par_name [iPDK_getParamValue name $cellId]
            set var [Ftos $minval 6]
            CbMessage "${par_name}: ${name} parameter value below lower limit, set to ${var}"
        }
        if {$beep == t} {
            hiGetAttention
        }
        set val $minval
    }
    
    if {$val > $maxval} {
        if {$info == "short"} {
            set var [Ftos $maxval 6]
            CbMessage "value above upper limit, set to ${var}"
        }
        if {$info == "long"} {
            set par_name [iPDK_getParamValue name $cellId]
            set var [Ftos $maxval 6]
            CbMessage "${par_name}: ${name} parameter value above upper limit, set to ${var}"
        }
        if {$beep == t} {
            hiGetAttention
        }
        set val $maxval
    }
    
    if {$grid == 0} {
        set val [Ftos $val 6]
    } else {
        set val [Ftos [expr [GridFix [expr ($val*5e5)]]/5e5] 6]
    }
    
    iPDK_setParamValue $name $val $cellId
}

proc CbMessage {mess} {
    
    global IHP_iPDK_CbMsg
    
    puts $mess
    set IHP_iPDK_CbMsg $mess
}
