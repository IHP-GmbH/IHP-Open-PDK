# cap_cmomi symbol C() helper (cmos5l).
#
# Reproduces the low-frequency capacitance of the shipped model so the xschem
# symbol label can show a value that tracks feed as well as w/l/mmin/mmax/m.
# Source of truth: libs.tech/verilog-a/cap_cmomi/cap_cmomi.va
#   Cmain = density(N) * active_area + Cfeed,   N = mmax-mmin+1
#   active_x = max(1, floor(l_um/0.84)),  active_y = max(2, floor(w_um/0.89))
#   active_area = active_x*0.84 * active_y*0.89
#   pad_len = active_y*0.89 + 0.42
#   Cfeed = same:0.1625*pad_len+0.0916 ; double:0.152*pad_len ; none:0
# Density table is the cmos5l one (M1..M4 stack): N>=4 -> 1.09 (no N>=5 branch).
# This is display only; the simulated value comes from the .va through format=.
proc cap_cmomi_C {m l w mmin mmax feed} {
    set N [expr {$mmax - $mmin + 1}]
    if {$N < 1} {set N 1}
    set density [expr {$N <= 2 ? 0.55 : ($N == 3 ? 0.82 : 1.09)}]
    set ax [expr {floor($l * 1e6 / 0.84 + 1e-6)}]
    set ay [expr {floor($w * 1e6 / 0.89 + 1e-6)}]
    set active_x [expr {$ax < 1 ? 1 : $ax}]
    set active_y [expr {$ay < 2 ? 2 : $ay}]
    set active_area [expr {$active_x * $active_y * 0.84 * 0.89}]
    set pad_len [expr {$active_y * 0.89 + 0.42}]
    set cfeed [expr {[string equal $feed same] ? (0.1625 * $pad_len + 0.0916) : \
                    ([string equal $feed double] ? (0.152 * $pad_len) : 0.0)}]
    set cmain [expr {$density * $active_area + $cfeed}]
    return [format %.4g [expr {$m * $cmain * 1e-15}]]
}
