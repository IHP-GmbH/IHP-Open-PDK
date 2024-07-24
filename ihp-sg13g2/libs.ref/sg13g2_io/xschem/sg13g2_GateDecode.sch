v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N -360 -210 -260 -210 {
lab=#net1}
N -80 -200 60 -200 {
lab=#net2}
N -320 20 -130 20 {
lab=#net3}
N 170 20 460 20 {
lab=xxx}
N 360 -200 450 -200 {
lab=ngate}
N -670 -210 -600 -210 {
lab=en}
N -670 -210 -670 0 {
lab=en}
N -720 -210 -670 -210 {
lab=en}
N -670 0 -560 -0 {
lab=en}
N -610 40 -560 40 {
lab=core}
N -610 -100 -610 40 {
lab=core}
N -740 40 -610 40 {
lab=core}
N -610 -100 -260 -100 {
lab=core}
N -260 -190 -260 -100 {
lab=core}
N -490 -170 -490 -120 {
lab=vss}
N -170 -120 200 -120 {
lab=vss}
N 200 -140 200 -120 {
lab=vss}
N -210 -140 -210 -120 {
lab=vss}
N -490 -120 -210 -120 {
lab=vss}
N -460 100 -460 140 {
lab=vss}
N -170 140 10 140 {
lab=vss}
N 10 80 10 140 {
lab=vss}
N -170 -120 -170 140 {
lab=vss}
N -210 -120 -170 -120 {
lab=vss}
N -220 140 -170 140 {
lab=vss}
N -490 -340 -490 -260 {
lab=vdd}
N -30 -340 200 -340 {
lab=vdd}
N 200 -340 200 -260 {
lab=vdd}
N -210 -340 -210 -260 {
lab=vdd}
N -490 -340 -210 -340 {
lab=vdd}
N -460 -80 -460 -60 {
lab=vdd}
N -30 -80 10 -80 {
lab=vdd}
N 10 -80 10 -40 {
lab=vdd}
N -30 -340 -30 -80 {
lab=vdd}
N -120 -340 -30 -340 {
lab=vdd}
N -460 -80 -30 -80 {
lab=vdd}
N 70 -280 70 -40 {
lab=iovdd}
N 70 -280 260 -280 {
lab=iovdd}
N 260 -280 260 -260 {
lab=iovdd}
N -220 140 -220 200 {
lab=vss}
N -460 140 -220 140 {
lab=vss}
N -120 -390 -120 -340 {
lab=vdd}
N -210 -340 -120 -340 {
lab=vdd}
N 260 -350 260 -280 {
lab=iovdd}
C {/home/prabhat.dubey/OPEN_Source_IHP_PDK/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_io/xschem/sg13g2_io_inv_x1.sym} -450 -210 0 0 {name=x1}
C {/home/prabhat.dubey/OPEN_Source_IHP_PDK/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_io/xschem/sg13g2_io_nor2_x1.sym} -120 -200 0 0 {name=x2}
C {/home/prabhat.dubey/OPEN_Source_IHP_PDK/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_io/xschem/sg13g2_LevelUp.sym} 20 20 0 0 {name=x3}
C {/home/prabhat.dubey/OPEN_Source_IHP_PDK/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_io/xschem/sg13g2_io_nand2_x1.sym} -410 20 0 0 {name=x4}
C {/home/prabhat.dubey/OPEN_Source_IHP_PDK/IHP-Open-PDK/ihp-sg13g2/libs.ref/sg13g2_io/xschem/sg13g2_LevelUp.sym} 210 -200 0 0 {name=x5}
C {devices/ipin.sym} -720 -210 0 0 {name=en lab=en}
C {devices/ipin.sym} -740 40 0 0 {name=core lab=core}
C {devices/iopin.sym} -220 200 0 0 {name=vss lab=vss}
C {devices/iopin.sym} -120 -390 0 0 {name=vdd lab=vdd}
C {devices/iopin.sym} 260 -350 0 0 {name=iovdd lab=iovdd}
C {devices/opin.sym} 450 -200 0 0 {name=ngate lab=ngate}
C {devices/opin.sym} 460 20 0 0 {name=pgate lab=pgate}
