#set terminal postscript eps color
#set output "c7552_ann_psp.eps"

set title "c7552 ann psp"

set grid
set key left top
set format x "%.1s%c"
set format y "%.1s%c"
set xlabel "time"
set ylabel "Voltage"
plot 'c7552_ann_psp.cir.prn' using 2:($3) t "g7529_1" w lines,\
     'c7552_ann_psp.cir.prn' using 2:($4) t "g7509_0" w lines
