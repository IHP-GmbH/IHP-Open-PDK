#set terminal postscript eps color
#set output "psp_ro.eps"

set title "ringosc 5 stages"

set grid
set key left top
set format x "%.1s%c"
set format y "%.1s%c"
set xlabel "time"
set ylabel "Voltage"
plot 'psp_ro.cir.prn' using 2:($3) t "in" w lines
