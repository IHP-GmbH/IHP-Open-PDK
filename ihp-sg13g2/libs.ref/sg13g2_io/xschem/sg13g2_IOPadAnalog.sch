v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N 2660 -380 2660 -330 {
lab=iovss}
N 2810 -530 2860 -530 {
lab=pad}
N 2860 -310 2860 -280 {
lab=pad}
N 2810 -280 2860 -280 {
lab=pad}
N 2660 -600 2660 -580 {
lab=iovdd}
N 2490 -600 2660 -600 {
lab=iovdd}
N 2490 -600 2490 -190 {
lab=iovdd}
N 2490 -190 2660 -190 {
lab=iovdd}
N 2660 -230 2660 -190 {
lab=iovdd}
N 2660 -430 2940 -430 {
lab=iovss}
N 2660 -480 2660 -430 {
lab=iovss}
N 3240 -480 3240 -450 {
lab=pad}
N 2860 -500 3240 -500 {
lab=pad}
N 2860 -530 2860 -500 {
lab=pad}
N 3240 -410 3280 -410 {
lab=iovdd}
N 3280 -600 3280 -410 {
lab=iovdd}
N 3090 -600 3280 -600 {
lab=iovdd}
N 2860 -310 2940 -310 {
lab=pad}
N 2860 -500 2860 -310 {
lab=pad}
N 3240 -330 3280 -330 {
lab=iovdd}
N 3280 -410 3280 -330 {
lab=iovdd}
N 3540 -600 3540 -450 {
lab=iovdd}
N 3280 -600 3540 -600 {
lab=iovdd}
N 3540 -330 3540 -290 {
lab=iovss}
N 3390 -290 3540 -290 {
lab=iovss}
N 2660 -380 2900 -380 {
lab=iovss}
N 2660 -430 2660 -380 {
lab=iovss}
N 2900 -380 2900 -250 {
lab=iovss}
N 3230 -250 3390 -250 {
lab=iovss}
N 3390 -290 3390 -250 {
lab=iovss}
N 3240 -290 3390 -290 {
lab=iovss}
N 3230 -250 3230 -170 {
lab=iovss}
N 2900 -250 3230 -250 {
lab=iovss}
N 3090 -670 3090 -600 {
lab=iovdd}
N 2660 -600 3090 -600 {
lab=iovdd}
N 3350 -480 3380 -480 {
lab=pad}
N 3240 -500 3240 -480 {
lab=pad}
N 3380 -480 3380 -390 {
lab=pad}
N 3680 -380 3740 -380 {
lab=padres}
N 3350 -530 3350 -480 {
lab=pad}
N 3240 -480 3350 -480 {
lab=pad}
N 3220 -670 3220 -630 {
lab=vdd}
N 3340 -200 3340 -170 {
lab=iovss}
C {/home/prabhat.dubey/OPEN_Source_IHP_PDK/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_io/xschem/sg13g2_DCNDiode.sym} 3090 -430 0 0 {name=x3}
C {/home/prabhat.dubey/OPEN_Source_IHP_PDK/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_io/xschem/sg13g2_DCPDiode.sym} 3090 -310 0 0 {name=x4}
C {/home/prabhat.dubey/OPEN_Source_IHP_PDK/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_io/xschem/sg13g2_SecondaryProtection.sym} 3530 -390 0 0 {}
C {/home/prabhat.dubey/OPEN_Source_IHP_PDK/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_io/xschem/sg13g2_Clamp_N20N0D.sym} 2660 -530 0 0 {name=x1}
C {/home/prabhat.dubey/OPEN_Source_IHP_PDK/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_io/xschem/sg13g2_Clamp_P20N0D.sym} 2660 -280 2 1 {name=x2}
C {devices/iopin.sym} 3740 -380 0 0 {name=padres lab=padres}
C {devices/iopin.sym} 3230 -170 1 0 {name=iovss lab=iovss}
C {devices/iopin.sym} 3090 -670 3 0 {name=iovdd lab=iovdd}
C {devices/iopin.sym} 3350 -530 3 0 {name=pad lab=pad}
C {devices/iopin.sym} 3220 -670 3 0 {name=vdd lab=vdd}
C {devices/iopin.sym} 3340 -170 1 0 {name=vss lab=vss}
