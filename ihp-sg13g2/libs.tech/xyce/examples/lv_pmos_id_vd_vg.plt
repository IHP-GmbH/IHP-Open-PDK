#set terminal postscript eps color
#set output "lv_pmos_id_vd_vg.eps"

set title "Id=f(Vds) Vg=-1.5...0V Temp: 27degC"

set grid
set key left top
set format x "%.1s%c"
set format y "%.1s%c"
set xlabel "Vds [V]"
set ylabel "Id [A]"
plot 'lv_pmos_id_vd_vg.cir.prn' using 2:($3) t "Id" w lp
