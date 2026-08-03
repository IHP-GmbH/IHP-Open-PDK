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

set currentInst "dummy"
set currentInstName ""
set currentCellParameters [dict create]
set currentParamName ""
set techParameters [dict create]
set isAbutment 0
set cniPythonPath ""

proc setCniPythonPath {path} {
    global cniPythonPath
    set cniPythonPath $path
}

proc setCurrentInstancedName {name} {
    global currentInstName
    set currentInstName $name
}

proc setCurrentCellParameters {parameters} {
    global currentCellParameters

    set currentCellParameters [dict create]
    set zeroLengthPattern [format "'?%c'?,?" 0x2717]

    dict for {key value} $parameters {
        # remove decoration from key
        regexp {'?([^',]+)'?:?} $key match undecoratedKey

        if {[regexp $zeroLengthPattern $value match]} {
            set undecoratedValue {}
        } else {
            # map space pattern to space
            set value [string map {"\u2709" " "} $value]
            # map square brackets pattern to square brackets
            set value [string map {"\u2772" "\["} $value]
            set value [string map {"\u2773" "\]"} $value]

            # remove decoration from value
            regexp {'?([^',]+)'?,?} $value match undecoratedValue
        }

        dict append currentCellParameters $undecoratedKey $undecoratedValue
    }
}

proc getCurrentCellParameters {} {
    global currentCellParameters

    set coercedCellParameters [dict create]

    dict for {key value} $currentCellParameters {
        if {$value eq ""} {
            set value "\u2717"
        } else {
            set value [string map {" " "\u2709"} $value]
            set value [string map {"\[" "\u2772"} $value]
            set value [string map {"\]" "\u2773"} $value]
        }
        dict append coercedCellParameters $key $value
    }

    return $coercedCellParameters
}

proc setTechParameters {techParams} {
    global techParameters

    set techParameters [dict create]

    # techParams arrives as a Python dict repr, e.g.
    #   'key': 'value', 'key': 0.001, 'key': 'value with spaces', ...
    # A plain "dict for" over this string breaks whenever a value contains a
    # space (e.g. 'No value'), because the whitespace split then yields an odd
    # number of tokens and Tcl raises "missing value to go with key". Parse
    # with a regex that respects the quoting so that space-containing values
    # keep their key/value pairing intact.
    set pattern {'([^']+)'\s*:\s*(?:'([^']*)'|([^,]+))}
    foreach {match key quotedValue bareValue} [regexp -all -inline $pattern $techParams] {
        if {$match eq ""} {
            continue
        }
        if {$bareValue ne ""} {
            set value [string trim $bareValue]
        } else {
            set value $quotedValue
        }
        dict set techParameters $key $value
    }
}

proc cni_setAbutment { value } {
    global isAbutment
    set isAbutment $value
}

proc techGetParam {name} {
    global techParameters

    if {[dict exists $techParameters $name]} {
        set value [dict get $techParameters $name]
        return $value
    } else {
        return ""
    }
}

proc cni_getParamValue {param inst} {
    global currentCellParameters

    if {[dict exists $currentCellParameters $param]} {
        set value [dict get $currentCellParameters $param]
        return $value
    } else {
        return ""
    }
}

proc cni_setParamValue {param value inst {evalCB true} } {
    global currentCellParameters

    dict set currentCellParameters $param $value
}

global SG13_GRID
set SG13_GRID [techGetParam grid]

if {$SG13_GRID == ""} {
    set SG13_GRID 0.01
}

set SG13_IGRID [expr {1.0/$SG13_GRID}]

global SG13_EPSILON
global SG13_EPSILON2

set SG13_EPSILON  [techGetParam epsilon1]
if {$SG13_EPSILON == ""} {
    set SG13_EPSILON 0.001
}
set SG13_EPSILON2 [techGetParam epsilon2]
if {$SG13_EPSILON2 == ""} {
    set SG13_EPSILON2 1e-9
}

proc iPDK_getCurrentInst {  } {
    global currentInst
    if {$currentInst == ""} {
        error "No current instance"
    }
    return $currentInst
}

proc iPDK_setParamValue { param value inst {evalCB true} } {
    global currentInst
    global isAbutment
    if { $isAbutment == 1 } {
        set instName [oa::getName $inst]
        return [cni_setAbutParamValue $param $value $instName $evalCB]
    } else {
        if {$inst != $currentInst} {
            error "iPDK_setParamValue: given inst does not match current inst"
        }
        return [cni_setParamValue $param $value $inst $evalCB]
    }
}

proc iPDK_getParamValue { param inst } {
    global currentInst
    global isAbutment
    if { $isAbutment == 1 } {
        set instName [oa::getName $inst]
        return [cni_getAbutParamValue $param $instName ]

    } else {
        if {$inst != $currentInst} {
            error "iPDK_getParamValue: given inst does not match current inst"
        }
        return [cni_getParamValue $param $inst]
    }
}

proc iPDK_getInstCellName { inst } {
    global currentInstName
    if {$currentInstName == ""} {
        error "No current instance name"
    }
    return $currentInstName
}

set sciCache [dict create]

variable dispScriptFile [file normalize [info script]]

proc iPDK_engToSci { value } {
    global sciCache
    global cniPythonPath

    if {[dict exists $sciCache $value]} {
        set res [dict get $sciCache $value]
    } else {
        variable dispScriptFile
        set path [file dirname $dispScriptFile]
        set path "$path:$cniPythonPath"
        set ::env(PYTHONPATH) $path

        set pythonPath [auto_execok python3]
        if {$pythonPath eq ""} {
            set pythonPath [auto_execok python]
        }
        if {$pythonPath eq ""} {
            puts "Err: No python executable found!"
            return ""
        }

        set res [exec $pythonPath -c "import callback; print(f'{callback.cni_engToSci(\"$value\")}')"]
        dict append sciCache $value $res
    }
    return $res
}
