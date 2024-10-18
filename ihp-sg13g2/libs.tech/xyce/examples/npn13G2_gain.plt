#set terminal postscript eps color
#set output "npn13G2_gain.eps"

set title "vbic gain stage Ic=50u...5m"

set grid
set key left top
set format x "%.1s%c"
set format y "%.1s%c"
set xlabel "frequency [Hz]"
set ylabel "Gain [dB]"
set yrange [0:]
set log x
plot 'npn13G2_gain.cir.FD.prn' using 2:($3) t "C" w lines
