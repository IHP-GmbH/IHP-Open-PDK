v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
B 2 2100 650 2860 1170 {flags=graph,unlocked
y1=6.3e-11
y2=6.2e-10
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=-1.2
x2=1.2
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
dataset=-1
unitx=1
logx=0
logy=0
sweep=p
color=4
node=cn_abs}
N 1990 880 1990 960 {lab=P}
N 1670 880 1990 880 {lab=P}
N 1670 880 1670 1040 {lab=P}
N 1670 1100 1670 1150 {lab=GND}
N 1670 1150 1990 1150 {lab=GND}
N 1990 1020 1990 1150 {lab=GND}
C {code_shown.sym} 1250 860 0 0 {name=MODEL only_toplevel=false value="
.lib cornerMOSCAP.lib moscap_tt
"}
C {code_shown.sym} 1240 970 0 0 {name=SIMULATION only_toplevel=false value="
.param  TEMP = 27
  .control
     save all
     tran 0.1n 400n
     let Cn_abs = abs(i(v1)) / deriv(v(p))
     meas tran C_max MAX Cn_abs
     meas tran C_min MIN Cn_abs from=5n to=400n
     meas tran t_c_min MIN_AT Cn_abs from=5n to=400n
     meas tran V_th FIND v(p) AT=t_c_min
     let Cn_norm = Cn_abs / C_max
     plot Cn_abs vs v(p)
     write tran_moscap_n.raw
  .endc
"}
C {vsource.sym} 1670 1070 0 0 {name=V1 value="pwl 0 -1.2 400n 1.2" savecurrent=false}
C {gnd.sym} 1990 1150 0 0 {name=l1 lab=GND}
C {lab_wire.sym} 1990 880 0 0 {name=p1 sig_type=std_logic lab=P}
C {launcher.sym} 2170 1210 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/tran_moscap_n.raw tran"
}
C {sg13g2_pr/moscap_n.sym} 1990 960 0 0 {name=C1
l=1.0u
w=1.0u
m=1
model=sg13_moscap_n
spiceprefix=X
}
