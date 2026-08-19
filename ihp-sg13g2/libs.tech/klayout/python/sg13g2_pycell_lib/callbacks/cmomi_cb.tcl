########################################################################
#
# Copyright 2026 IHP PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
########################################################################
#
# cap_cmomi live capacitance callback (g2 device name: cmomi).
#
# Forward only: recompute the read-back C parameter from w, l, mmin, mmax and
# feed on any edit, the way cmim/rfcmim keep their C field live. There is no
# reverse solve (C -> w/l): the array is quantised to the unit cell, so C is a
# staircase in w and l and the inverse is ill-posed.
#
# CbCmomiCalc MUST return the same value as _model_C_fF in the PCell
# (cmomi_code.py / cap_cmomi_code.py) and as cap_cmomi.va. The constants below
# are copied from those two; if the model changes, change all three together.

# l, w in metres. Returns C in Farads.
proc CbCmomiCalc {l w mmin mmax feed cell} {
    set UC_X 0.84
    set UC_Y 0.89
    set T_BAR 0.21
    set CFEED_SLOPE  0.1625
    set CFEED_END    0.0916
    set CFEED2_SLOPE 0.152

    # cmos5l tops out at Metal4, g2 goes to Metal5.
    if {$cell eq "cap_cmomi"} {
        set METAL_MAX 4
    } else {
        set METAL_MAX 5
    }

    set lu [expr {$l * 1.0e6}]
    set wu [expr {$w * 1.0e6}]

    # unit-cell tiling, same floors as the PCell and the Verilog-A
    set nx [expr {int($lu / $UC_X + 1.0e-6)}]
    if {$nx < 1} { set nx 1 }
    set ny [expr {int($wu / $UC_Y + 1.0e-6) - 1}]
    if {$ny < 1} { set ny 1 }
    set ny [expr {$ny + 1}]

    # metal-band density AREACAP[n], n = clamp(mmax-mmin+1, 2, METAL_MAX)
    set n [expr {int($mmax) - int($mmin) + 1}]
    if {$n < 2} { set n 2 }
    if {$n > $METAL_MAX} { set n $METAL_MAX }
    switch $n {
        2       { set dens 0.55 }
        3       { set dens 0.82 }
        4       { set dens 1.09 }
        5       { set dens 1.36 }
        default { set dens 0.55 }
    }

    set c_active [expr {$dens * ($nx * $UC_X) * ($ny * $UC_Y)}]
    set pad_len  [expr {$ny * $UC_Y + 2.0 * $T_BAR}]

    set cfeed 0.0
    switch $feed {
        same   { set cfeed [expr {$CFEED_SLOPE * $pad_len + $CFEED_END}] }
        double { set cfeed [expr {$CFEED2_SLOPE * $pad_len}] }
    }

    # Returns {C [F]  Lx [um]  Wy [um]}: the modelled capacitance and the
    # effective drawn extents (the read-only Lx/Wy dialog fields).
    set c_F  [expr {($c_active + $cfeed) * 1.0e-15}]
    set lx_um [expr {$nx * $UC_X}]
    set wy_um [expr {$ny * $UC_Y}]
    return [list $c_F $lx_um $wy_um]
}

proc CbCmomi {param} {
    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId]

    # The coerce writeback applies bool() to the string form of a bool
    # parameter, so "False" comes back as True (any non-empty string is
    # truthy). Normalise the subblock checkbox so a false value round-trips as
    # false (empty string -> bool("") = False); a true value is left as is.
    # Without this every coerced cmomi would draw a spurious PWell.block.
    set sb [iPDK_getParamValue subblock $cellId]
    if {$sb ne "True" && $sb ne "1"} {
        iPDK_setParamValue subblock "" $cellId
    }

    set wraw [iPDK_getParamValue w    $cellId]
    set lraw [iPDK_getParamValue l    $cellId]
    set mmin [iPDK_getParamValue mmin $cellId]
    set mmax [iPDK_getParamValue mmax $cellId]
    set feed [iPDK_getParamValue feed $cellId]

    if {$wraw eq "" || $lraw eq "" || $mmin eq "" || $mmax eq "" || $feed eq ""} {
        return
    }

    set res [CbCmomiCalc [Stof $lraw] [Stof $wraw] $mmin $mmax $feed $cell]
    iPDK_setParamValue C  [Ftos [lindex $res 0] 3] $cellId
    iPDK_setParamValue Lx [Ftos [expr {[lindex $res 1] * 1.0e-6}] 3] $cellId
    iPDK_setParamValue Wy [Ftos [expr {[lindex $res 2] * 1.0e-6}] 3] $cellId
}
