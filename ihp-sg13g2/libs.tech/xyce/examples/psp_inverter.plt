#set terminal postscript eps color
#set output "psp_inverter.eps"

set title "psp inverter"

set grid
set key left top
set format x "%.1s%c"
set format y "%.1s%c"
set xlabel "time"
set ylabel "Voltage"
plot 'psp_inverter.cir.prn' using 2:($3) t "in" w lines,\
     'psp_inverter.cir.prn' using 2:($4) t "out" w lines
