#set terminal postscript eps color
#set output "hv_pmos_id_vg_vb.eps"

set title "Id=f(Vgs) Vb=-3...0V Temp: 27degC"

set grid
set key left top
set format x "%.1s%c"
set format y "%.1s%c"
set xlabel "Vgs [V]"
set ylabel "Id [A]"
plot 'hv_pmos_id_vg_vb.cir.prn' using 2:($3) t "Id" w lp
