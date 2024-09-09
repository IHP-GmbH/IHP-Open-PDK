#set terminal postscript eps color
#set output "npn13G2_ic_vc_ib.eps"

set title "Ic=f(Vce,Ib) Ve,Vs=0V Temp: 27degC"

set grid
set key left top
set format x "%.1s%c"
set format y "%.1s%c"
set xlabel "Vce [V]"
set ylabel "Ic [A]"
plot 'npn13G2_ic_vc_ib.cir.prn' using 2:(-$3) t "Ic" w l
