v {xschem version=3.4.5 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
N -150 -110 -150 -80 {
lab=GND}
N -180 -110 -180 -80 {
lab=GND}
N 10 -60 10 -50 {
lab=GND}
N 110 -160 150 -160 {
lab=#net1}
N 10 -160 50 -160 {
lab=#net2}
N 10 -160 10 -120 {
lab=#net2}
N -20 -160 10 -160 {
lab=#net2}
N -130 -160 -80 -160 {
lab=#net3}
N 170 -110 170 -80 {
lab=GND}
N 200 -110 200 -80 {
lab=GND}
N -180 200 -180 230 {
lab=GND}
N -150 200 -150 230 {
lab=GND}
N 170 190 170 230 {
lab=GND}
N 200 190 200 230 {
lab=GND}
N -590 -120 -590 -100 {
lab=GND}
N -500 -120 -500 -100 {
lab=GND}
N -500 -200 -500 -180 {
lab=Vbb}
N -500 -200 -470 -200 {
lab=Vbb}
N -260 -160 -240 -160 {
lab=Vbb}
N -260 150 -240 150 {
lab=Vbb}
N 260 140 280 140 {
lab=Vbb}
N 260 -160 280 -160 {
lab=Vbb}
N 200 10 200 30 {
lab=Vc}
N -180 20 -180 40 {
lab=Vc}
N -180 -290 -180 -270 {
lab=Vc}
N 200 -290 200 -270 {
lab=Vc}
N -590 -200 -590 -180 {
lab=Vc}
N -590 -200 -570 -200 {
lab=Vc}
C {sg13g2_pr/npn13G2_5t.sym} -200 -160 0 0 {name=Q1
model=npn13G2_5t
spiceprefix=X
Nx=1
le=900e-9}
C {gnd.sym} -180 -80 0 0 {name=l1 lab=GND}
C {gnd.sym} -150 -80 0 0 {name=l2 lab=GND}
C {res.sym} 10 -90 0 0 {name=R1
value=50
footprint=1206
device=resistor
m=1}
C {gnd.sym} 10 -50 0 0 {name=l3 lab=GND}
C {sg13g2_pr/npn13G2_5t.sym} 220 -160 0 1 {name=Q2
model=npn13G2_5t
spiceprefix=X
Nx=1
le=900e-9}
C {res.sym} -50 -160 1 0 {name=R2
value=10
footprint=1206
device=resistor
m=1}
C {res.sym} 80 -160 1 0 {name=R3
value=10
footprint=1206
device=resistor
m=1}
C {gnd.sym} 170 -80 0 0 {name=l4 lab=GND}
C {gnd.sym} 200 -80 0 0 {name=l5 lab=GND}
C {sg13g2_pr/npn13G2_5t.sym} -200 150 0 0 {name=Q3
model=npn13G2_5t
spiceprefix=X
Nx=1
le=900e-9}
C {sg13g2_pr/npn13G2_5t.sym} 220 140 0 1 {name=Q4
model=npn13G2_5t
spiceprefix=X
Nx=1
le=900e-9}
C {gnd.sym} -180 230 0 0 {name=l6 lab=GND}
C {gnd.sym} -150 230 0 0 {name=l7 lab=GND}
C {gnd.sym} 170 230 0 0 {name=l8 lab=GND}
C {gnd.sym} 200 230 0 0 {name=l9 lab=GND}
C {vsource.sym} -590 -150 0 0 {name=V_C value=1 savecurrent=false}
C {vsource.sym} -500 -150 0 0 {name=V_B value=\{Vb\} savecurrent=false}
C {gnd.sym} -590 -100 0 0 {name=l10 lab=GND}
C {gnd.sym} -500 -100 0 0 {name=l11 lab=GND}
C {ammeter.sym} -180 70 0 0 {name=Vq3 savecurrent=true spice_ignore=0}
C {ammeter.sym} 200 60 0 0 {name=Vq4 savecurrent=true spice_ignore=0}
C {ammeter.sym} -180 -240 0 0 {name=Vq1 savecurrent=true spice_ignore=0}
C {ammeter.sym} 200 -240 0 0 {name=Vq2 savecurrent=true spice_ignore=0}
C {lab_pin.sym} -570 -200 2 0 {name=p1 sig_type=std_logic lab=Vc}
C {lab_pin.sym} -180 -290 2 0 {name=p2 sig_type=std_logic lab=Vc}
C {lab_pin.sym} 200 -290 2 0 {name=p3 sig_type=std_logic lab=Vc}
C {lab_pin.sym} -180 20 2 0 {name=p4 sig_type=std_logic lab=Vc}
C {lab_pin.sym} 200 10 2 0 {name=p5 sig_type=std_logic lab=Vc}
C {lab_pin.sym} -470 -200 2 0 {name=p6 sig_type=std_logic lab=Vbb}
C {lab_pin.sym} -260 150 0 0 {name=p7 sig_type=std_logic lab=Vbb}
C {lab_pin.sym} -260 -160 0 0 {name=p8 sig_type=std_logic lab=Vbb}
C {lab_pin.sym} 280 140 2 0 {name=p9 sig_type=std_logic lab=Vbb}
C {lab_pin.sym} 280 -160 2 0 {name=p10 sig_type=std_logic lab=Vbb}
C {devices/code_shown.sym} 370 -270 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerHBT.lib hbt_typ
"}
C {devices/code_shown.sym} 360 -160 0 0 {name=NGSPICE only_toplevel=true 
value="
.param temp=27
.control 
save all
op
print all

.endc
"}
