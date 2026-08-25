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
# cap_cmomi live parameter callback (g2 device name: cmomi).
#
# Two directions, selected by the Calculate parameter (ref. cmim/CbCap):
#   Calculate = C : forward. C, Lx, Wy, Fx, Fy are recomputed from w, l,
#                   mmin, mmax, feed on any edit (C is a read-out).
#   Calculate = w : solve W from a target C, keeping L fixed.
#   Calculate = l : solve L from a target C, keeping W fixed.
# C is a staircase in the integer cell counts, so a solved dimension lands on
# the unit-cell grid and C snaps to the nearest achievable value. The solved
# dimension is clamped to the allowed 2..100 um range.
#
# The C model MUST stay identical to _model_C_fF in the PCell (cmomi_code.py /
# cap_cmomi_code.py) and to cap_cmomi.va; the footprint to _footprint_um and the
# genLayout Recog box. Change all together.

set CMOMI_UC_X 0.84
set CMOMI_UC_Y 0.89
set CMOMI_T_BAR 0.21
set CMOMI_CFEED_SLOPE  0.1625
set CMOMI_CFEED_END    0.0916
set CMOMI_CFEED2_SLOPE 0.152
# Footprint (Recog box) constants, copied from the PCell genLayout.
set CMOMI_FEED_EXT        0.90
set CMOMI_FEED_EXT_SAME   1.20
set CMOMI_BAR_OVERHANG    0.05
set CMOMI_FEED_Y_OVERHANG 0.64
# Allowed requested l/w range (mirrors the PCell RangeConstraint), um.
set CMOMI_MIN_UM 2.0
set CMOMI_MAX_UM 100.0

# Area density AREACAP[n], n = clamp(mmax-mmin+1, 2, METAL_MAX).
proc CbCmomiDensity {mmin mmax cell} {
    if {$cell eq "cap_cmomi"} { set MM 4 } else { set MM 5 }
    set n [expr {int($mmax) - int($mmin) + 1}]
    if {$n < 2}   { set n 2 }
    if {$n > $MM} { set n $MM }
    switch $n {
        2 { return 0.55 }
        3 { return 0.82 }
        4 { return 1.09 }
        default { return 1.36 }
    }
}

# Feed capacitance as Cfeed = slope*Wy + intercept [fF], Wy = ny*UC_Y [um].
proc CbCmomiFeed {feed} {
    global CMOMI_CFEED_SLOPE CMOMI_CFEED_END CMOMI_CFEED2_SLOPE CMOMI_T_BAR
    set two_tbar [expr {2.0 * $CMOMI_T_BAR}]
    switch $feed {
        same   { return [list $CMOMI_CFEED_SLOPE \
                              [expr {$CMOMI_CFEED_SLOPE * $two_tbar + $CMOMI_CFEED_END}]] }
        double { return [list $CMOMI_CFEED2_SLOPE \
                              [expr {$CMOMI_CFEED2_SLOPE * $two_tbar}]] }
        default { return [list 0.0 0.0] }
    }
}

# Integer cell counts for a given l/w (metres), same floors as the model.
proc CbCmomiNx {l} {
    global CMOMI_UC_X
    set nx [expr {int($l * 1.0e6 / $CMOMI_UC_X + 1.0e-6)}]
    if {$nx < 1} { set nx 1 }
    return $nx
}
proc CbCmomiNy {w} {
    global CMOMI_UC_Y
    set ny [expr {int($w * 1.0e6 / $CMOMI_UC_Y + 1.0e-6) - 1}]
    if {$ny < 1} { set ny 1 }
    return [expr {$ny + 1}]
}

# Forward: l, w in metres. Returns {C[F] Lx[um] Wy[um] Fx[um] Fy[um]}.
proc CbCmomiCalc {l w mmin mmax feed cell} {
    global CMOMI_UC_X CMOMI_UC_Y CMOMI_T_BAR
    global CMOMI_FEED_EXT CMOMI_FEED_EXT_SAME CMOMI_BAR_OVERHANG CMOMI_FEED_Y_OVERHANG

    set lu [expr {$l * 1.0e6}]
    set wu [expr {$w * 1.0e6}]

    # unit-cell tiling, same floors as the PCell and the Verilog-A
    set nx [expr {int($lu / $CMOMI_UC_X + 1.0e-6)}]
    if {$nx < 1} { set nx 1 }
    set ny [expr {int($wu / $CMOMI_UC_Y + 1.0e-6) - 1}]
    if {$ny < 1} { set ny 1 }
    set ny [expr {$ny + 1}]

    set dens [CbCmomiDensity $mmin $mmax $cell]
    set c_active [expr {$dens * ($nx * $CMOMI_UC_X) * ($ny * $CMOMI_UC_Y)}]

    set fs    [CbCmomiFeed $feed]
    set Wy    [expr {$ny * $CMOMI_UC_Y}]
    set cfeed [expr {[lindex $fs 0] * $Wy + [lindex $fs 1]}]

    # Outer footprint (Recog box), feed pads included. Mirrors _footprint_um.
    set dev_w [expr {$nx * $CMOMI_UC_X}]
    set dev_l [expr {$ny * $CMOMI_UC_Y}]
    switch $feed {
        double {
            set fx_um [expr {$dev_w + 2.0 * $CMOMI_FEED_EXT}]
            set fy_um [expr {$dev_l + $CMOMI_FEED_Y_OVERHANG}]
        }
        same {
            set fx_um [expr {$dev_w + $CMOMI_BAR_OVERHANG + $CMOMI_FEED_EXT_SAME}]
            set fy_um [expr {$dev_l + 2.0 * $CMOMI_T_BAR}]
        }
        default {
            set fx_um [expr {$dev_w + 2.0 * $CMOMI_BAR_OVERHANG}]
            set fy_um $dev_l
        }
    }

    set c_F  [expr {($c_active + $cfeed) * 1.0e-15}]
    return [list $c_F [expr {$nx * $CMOMI_UC_X}] $Wy $fx_um $fy_um]
}

# Solve W (metres) from a target C [F] with L fixed.
proc CbCmomiSolveW {c l mmin mmax feed cell} {
    global CMOMI_UC_X CMOMI_UC_Y CMOMI_MIN_UM CMOMI_MAX_UM
    set c_fF [expr {$c * 1.0e15}]
    set lu   [expr {$l * 1.0e6}]
    set nx   [expr {int($lu / $CMOMI_UC_X + 1.0e-6)}]
    if {$nx < 1} { set nx 1 }
    set dens [CbCmomiDensity $mmin $mmax $cell]
    set fs   [CbCmomiFeed $feed]
    # c_fF = Wy*(dens*nx*UC_X + slope) + intercept,  Wy = ny*UC_Y
    set denom [expr {$dens * $nx * $CMOMI_UC_X + [lindex $fs 0]}]
    if {$denom <= 0.0} { return $l }
    set Wy [expr {($c_fF - [lindex $fs 1]) / $denom}]
    set ny [expr {round($Wy / $CMOMI_UC_Y)}]
    if {$ny < 2} { set ny 2 }
    set wum [expr {$ny * $CMOMI_UC_Y}]
    if {$wum < $CMOMI_MIN_UM} { set wum $CMOMI_MIN_UM }
    if {$wum > $CMOMI_MAX_UM} { set wum $CMOMI_MAX_UM }
    return [expr {$wum * 1.0e-6}]
}

# Solve L (metres) from a target C [F] with W fixed.
proc CbCmomiSolveL {c w mmin mmax feed cell} {
    global CMOMI_UC_X CMOMI_UC_Y CMOMI_MIN_UM CMOMI_MAX_UM
    set c_fF [expr {$c * 1.0e15}]
    set wu   [expr {$w * 1.0e6}]
    set ny   [expr {int($wu / $CMOMI_UC_Y + 1.0e-6) - 1}]
    if {$ny < 1} { set ny 1 }
    set ny   [expr {$ny + 1}]
    set Wy   [expr {$ny * $CMOMI_UC_Y}]
    set dens [CbCmomiDensity $mmin $mmax $cell]
    set fs   [CbCmomiFeed $feed]
    set cfeed [expr {[lindex $fs 0] * $Wy + [lindex $fs 1]}]
    set denom [expr {$dens * $CMOMI_UC_X * $Wy}]
    if {$denom <= 0.0} { return $w }
    set nx [expr {round(($c_fF - $cfeed) / $denom)}]
    if {$nx < 1} { set nx 1 }
    set lum [expr {$nx * $CMOMI_UC_X}]
    if {$lum < $CMOMI_MIN_UM} { set lum $CMOMI_MIN_UM }
    if {$lum > $CMOMI_MAX_UM} { set lum $CMOMI_MAX_UM }
    return [expr {$lum * 1.0e-6}]
}

proc CbCmomi {param} {
    global CMOMI_MIN_UM CMOMI_MAX_UM
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
    set craw [iPDK_getParamValue C    $cellId]
    set mmin [iPDK_getParamValue mmin $cellId]
    set mmax [iPDK_getParamValue mmax $cellId]
    set feed [iPDK_getParamValue feed $cellId]
    set calc [iPDK_getParamValue Calculate $cellId]
    if {$calc eq ""} { set calc "C" }

    if {$wraw eq "" || $lraw eq "" || $mmin eq "" || $mmax eq "" || $feed eq ""} {
        return
    }

    set w [Stof $wraw]
    set l [Stof $lraw]
    set c [expr {$craw eq "" ? 0.0 : [Stof $craw]}]

    # Clamp a directly-edited geometry field to the allowed range.
    set lo [expr {$CMOMI_MIN_UM * 1.0e-6}]
    set hi [expr {$CMOMI_MAX_UM * 1.0e-6}]
    # Only write back when the value was actually clamped: the framework types
    # a parameter by the incoming value, so rewriting an in-range float field
    # with an engineering string ('5.0u') would break its re-cast on the
    # scripted (float-input) path. In the GUI the fields are strings, so a
    # clamp write is harmless there.
    switch $param {
        w {
            set nw $w
            if {$nw < $lo} { set nw $lo }
            if {$nw > $hi} { set nw $hi }
            if {$nw != $w} { set w $nw; iPDK_setParamValue w [Ftos $w 3] $cellId }
        }
        l {
            set nl $l
            if {$nl < $lo} { set nl $lo }
            if {$nl > $hi} { set nl $hi }
            if {$nl != $l} { set l $nl; iPDK_setParamValue l [Ftos $l 3] $cellId }
        }
    }

    # Solve the dependent dimension from a target C (staircase inverse). Skip on
    # a bare Calculate mode-switch: picking the mode must not move geometry by
    # itself. Only an actual edit of C (or L/W/mmin/mmax/feed) re-solves. Without
    # this, switching to "solve W" would immediately snap W to the grid width for
    # the current C (e.g. 5.0 -> 4.45), which reads as a spurious change.
    # Idempotent solve: only move W/L when the target C needs a DIFFERENT integer
    # cell count. Switching mode (or any edit that leaves the row/column count
    # unchanged) then does not disturb the current value, even though KLayout
    # fires the callback for every listed parameter rather than only the one the
    # user touched. The param!=Calculate guard is a further short-circuit for the
    # toolchains that do report the single changed parameter.
    if {$param ne "Calculate"} {
        switch $calc {
            w {
                if {$c > 0.0} {
                    set wnew [CbCmomiSolveW $c $l $mmin $mmax $feed $cell]
                    if {[CbCmomiNy $wnew] != [CbCmomiNy $w]} {
                        set w $wnew
                        iPDK_setParamValue w [Ftos $w 3] $cellId
                    }
                }
            }
            l {
                if {$c > 0.0} {
                    set lnew [CbCmomiSolveL $c $w $mmin $mmax $feed $cell]
                    if {[CbCmomiNx $lnew] != [CbCmomiNx $l]} {
                        set l $lnew
                        iPDK_setParamValue l [Ftos $l 3] $cellId
                    }
                }
            }
        }
    }

    # Forward-recompute the read-out fields from the final geometry. This also
    # snaps C to the achievable staircase value when a target was solved.
    set res [CbCmomiCalc $l $w $mmin $mmax $feed $cell]
    iPDK_setParamValue C  [Ftos [lindex $res 0] 3] $cellId
    iPDK_setParamValue Fx [Ftos [expr {[lindex $res 3] * 1.0e-6}] 3] $cellId
    iPDK_setParamValue Fy [Ftos [expr {[lindex $res 4] * 1.0e-6}] 3] $cellId
}
