v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
B 2 1990 780 2790 1180 {flags=graph,unlocked
y1=3.2e-10
y2=6.2e-10
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=-2.4
x2=1.2
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
dataset=-1
unitx=1
logx=0
logy=0
sweep=vcap
color=4
node=cp_abs}
N 1700 860 1700 900 {lab=M}
N 1700 860 1860 860 {lab=M}
N 1860 860 1860 900 {lab=M}
N 1700 960 1700 1000 {lab=GND}
N 1860 960 1860 990 {lab=VDD}
N 1860 1050 1860 1070 {lab=GND}
C {code_shown.sym} 1251.25 786.25 0 0 {name=MODEL only_toplevel=false value="
.lib cornerMOSCAP.lib moscap_tt
"}
C {code_shown.sym} 1253.75 906.25 0 0 {name=SIMULATION only_toplevel=false value="

.control
save all
  tran 0.1n 400n
  let vcap = v(m)-v(vdd)
  let Cp_abs = abs(i(v1)) / deriv(vcap)
   meas tran C_max MAX Cp_abs 
   meas tran C_min MIN Cp_abs from=5n to=400n
   meas tran t_c_min MIN_AT Cp_abs from=5n to=400n
   meas tran V_th FIND vcap AT=t_c_min
   plot Cp_abs vs vcap
  write tran_moscap_p.raw
.endc
  
"}
C {launcher.sym} 2140 1220 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/tran_moscap_p.raw tran"
}
C {gnd.sym} 1700 1000 0 0 {name=l1 lab=GND}
C {vsource.sym} 1700 930 0 0 {name=V1 value="pwl 0 0 400n 2.4 " savecurrent=false}
C {sg13g2_pr/moscap_p.sym} 1860 900 0 0 {name=C1
l=1u
w=1u
m=1
model=sg13_moscap_p
spiceprefix=X
}
C {gnd.sym} 1860 1070 0 0 {name=l2 lab=GND}
C {lab_wire.sym} 1860 860 0 0 {name=p1 sig_type=std_logic lab=M}
C {vsource.sym} 1860 1020 0 0 {name=V2 value="DC 1.2" savecurrent=false}
C {lab_wire.sym} 1860 980 0 0 {name=p2 sig_type=std_logic lab=VDD}
