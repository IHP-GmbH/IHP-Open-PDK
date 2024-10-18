#set terminal postscript eps color
#set output "hv_nmos_id_vd_vg.eps"

set title "Id=f(Vds) Vg=0...3V Temp: 27degC"

set grid
set key left top
set format x "%.1s%c"
set format y "%.1s%c"
set xlabel "Vds [V]"
set ylabel "Id [A]"
plot 'hv_nmos_id_vd_vg.cir.prn' using 2:($3) t "Id" w lp
