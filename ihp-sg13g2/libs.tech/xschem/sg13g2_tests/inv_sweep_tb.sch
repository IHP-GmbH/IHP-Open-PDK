v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {used to run ngspice sweep in parallel} 1440 -1000 0 0 0.3 0.3 {layer=11}
T {used to check OP, AC and TRAN} 920 -1000 0 0 0.3 0.3 {layer=11}
T {Ctrl-Click to execute launcher} 170 -910 0 0 0.3 0.3 {layer=11}
T {.save file can be created with IHP->"Create FET and BIP .save file"} 170 -810 0 0 0.3 0.3 {layer=11}
T {each printed value will be saved in csv file} 1710 -510 0 0 0.3 0.3 {layer=11}
T {possible parameter sweep types:
Auto:Begin:TotalPoints:End
Lin:Begin:StepSize:End
Dec:Begin:PointsPerDecade:End
Log:Begin:TotalPoints:End} 1790 -240 0 0 0.3 0.3 {layer=11}
T {set num_threads to 1 for small circuits} 1710 -760 0 0 0.3 0.3 {layer=11}
T {which results should be ploted using a contourplot} 1790 -310 0 0 0.3 0.3 {layer=11}
T {which results should be ploted using a log x-axis} 1790 -290 0 0 0.3 0.3 {layer=11}
T {which results should be ploted using a log y-axis} 1790 -270 0 0 0.3 0.3 {layer=11}
T {sort .csv file by given index} 1790 -330 0 0 0.3 0.3 {layer=11}
T {number of parallel workers} 1790 -350 0 0 0.3 0.3 {layer=11}
N 180 -270 180 -250 {lab=vdd}
N 180 -190 180 -170 {lab=GND}
N 550 -400 610 -400 {lab=vdd}
N 610 -460 610 -400 {lab=vdd}
N 550 -460 610 -460 {lab=vdd}
N 550 -300 610 -300 {lab=GND}
N 610 -300 610 -230 {lab=GND}
N 550 -230 610 -230 {lab=GND}
N 550 -270 550 -230 {lab=GND}
N 550 -460 550 -430 {lab=vdd}
N 550 -350 550 -330 {lab=inv_out}
N 450 -350 450 -300 {lab=inv_in}
N 750 -350 750 -320 {lab=inv_out}
N 550 -350 750 -350 {lab=inv_out}
N 550 -370 550 -350 {lab=inv_out}
N 720 -230 750 -230 {lab=GND}
N 750 -230 780 -230 {lab=GND}
N 720 -280 720 -230 {lab=GND}
N 750 -280 750 -230 {lab=GND}
N 780 -280 780 -230 {lab=GND}
N 310 -190 310 -170 {lab=GND}
N 310 -350 310 -250 {lab=in}
N 450 -350 470 -350 {lab=inv_in}
N 450 -400 450 -350 {lab=inv_in}
N 530 -350 550 -350 {lab=inv_out}
N 450 -300 510 -300 {lab=inv_in}
N 450 -400 510 -400 {lab=inv_in}
N 400 -350 450 -350 {lab=inv_in}
N 310 -350 340 -350 {lab=in}
C {devices/title.sym} 245 -55 0 0 {name=l5 author="Patrick Fath"}
C {launcher.sym} 230 -865 0 0 {name=h3
descr=SimulateNGSPICE
tclcommand="
# Setup the default simulation commands if not already set up
# for example by already launched simulations.
set_sim_defaults
puts $sim(spice,1,cmd) 

# Change the Xyce command. In the spice category there are currently
# 5 commands (0, 1, 2, 3, 4). Command 3 is the Xyce batch
# you can get the number by querying $sim(spice,n)
set sim(spice,1,cmd) \{ngspice  \\"$N\\" -a\}

# change the simulator to be used (Xyce)
set sim(spice,default) 0

# Create FET and BIP .save file
mkdir -p $netlist_dir
write_data [save_params] $netlist_dir/[file rootname [file tail [xschem get current_name]]].save

# run netlist and simulation
xschem netlist
simulate
"}
C {devices/vsource.sym} 180 -220 0 0 {name=VDD1 value=1.5}
C {lab_wire.sym} 180 -270 0 1 {name=p1 sig_type=std_logic lab=vdd}
C {code_shown.sym} 155 -695 0 0 {
name=TT_MODELS
only_toplevel=true
value="
** IHP models
.lib cornerMOSlv.lib mos_tt
.lib cornerMOShv.lib mos_tt
.lib cornerHBT.lib hbt_typ
.lib cornerRES.lib res_typ
.lib cornerCAP.lib cap_typ
"
spice_ignore=false
      }
C {simulator_commands_shown.sym} 915 -915 0 0 {name=OP_AC_TRAN
simulator=ngspice
only_toplevel=false 
value="
.param temp=27
.param c1_val=1p
.param r1_val=100Meg
.param m1_w_val=0.15u
.param m2_w_val=0.15u
.param l_val=0.13u
.include inv_sweep_tb.save
.options warn=1

.control
set num_threads=1
save all
op
write inv_sweep_tb.raw
set appendwrite
ac dec 1001 1 100G
write inv_sweep_tb.raw
let gain_lin = abs(inv_out)
let gain_dB = vdb(inv_out)
meas ac gain_passband_dB max gain_dB
let gain_fc_dB = gain_passband_dB-3
meas ac fc_l when gain_dB = gain_fc_dB
meas ac fc_u when gain_dB = gain_fc_dB cross=last
let GBW = gain_lin[0] * (fc_u-fc_l)
print gain_passband_dB
print fc_l
print fc_u
print GBW
plot gain_dB xlimit 1 100G ylabel 'small signal gain'
tran 10p 30n
write inv_sweep_tb.raw
plot inv_in inv_out
.endc
"
spice_ignore=true}
C {simulator_commands_shown.sym} 1435 -915 0 0 {name=SWEEP_SIM
simulator=ngspice
only_toplevel=false 
value="
.param temp=27
.param c1_val=1p
.param r1_val=100Meg
.param m1_w_val=0.15u
.param m2_w_val=0.15u
.param l_val=0.13u

.control
set num_threads 1

ac dec 1001 1 100G
let gain_lin = abs(inv_out)
let gain_dB = vdb(inv_out)
meas ac gain_passband_dB max gain_dB
let gain_fc_dB = gain_passband_dB-3
meas ac fc_l when gain_dB = gain_fc_dB
meas ac fc_u when gain_dB = gain_fc_dB cross=last
let GBW = gain_lin[0] * (fc_u-fc_l)

echo results_sweep_begin
print gain_passband_dB
print fc_l
print fc_u
print GBW
echo results_sweep_end

.endc
"
}
C {gnd.sym} 180 -170 0 0 {name=l1 lab=GND}
C {sg13g2_pr/sg13_lv_nmos.sym} 530 -300 0 0 {name=M1
l=\{l_val\}
w=\{m1_w_val\}
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 530 -400 0 0 {name=M2
l=\{l_val\}
w=\{m2_w_val\}
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {gnd.sym} 550 -230 0 0 {name=l2 lab=GND}
C {lab_wire.sym} 550 -460 0 1 {name=p2 sig_type=std_logic lab=vdd}
C {sg13g2_pr/sg13_lv_nmos.sym} 750 -300 1 0 {name=M3
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {gnd.sym} 720 -230 0 0 {name=l3 lab=GND}
C {lab_wire.sym} 450 -350 0 0 {name=p3 sig_type=std_logic lab=inv_in}
C {lab_wire.sym} 750 -350 0 1 {name=p4 sig_type=std_logic lab=inv_out}
C {devices/vsource.sym} 310 -220 0 0 {name=VIN1 value="dc 0.75 ac 1 sin(0.75 1m 100Meg)"}
C {gnd.sym} 310 -170 0 0 {name=l4 lab=GND}
C {res.sym} 500 -350 1 0 {name=R1
value=\{r1_val\}
footprint=1206
device=resistor
m=1}
C {capa.sym} 370 -350 1 0 {name=C1
m=1
value=\{c1_val\}
footprint=1206
device="ceramic capacitor"}
C {lab_wire.sym} 310 -350 0 0 {name=p5 sig_type=std_logic lab=in}
C {devices/launcher.sym} 230 -830 0 0 {name=h1
descr="OP annotate" 
tclcommand="xschem annotate_op"
}
C {sg13g2_pr/annotate_fet_params.sym} 630 -570 0 0 {name=annot1 ref=M2}
C {sg13g2_pr/annotate_fet_params.sym} 640 -200 0 0 {name=annot2 ref=M1}
C {code_shown.sym} 1450 -360 0 0 {name=SWEEP_SETTINGS
only_toplevel=false
value="
**nr_workers=50
**sort_results_index=0
**results_plot_contour_index=3
**results_plot_logx_index=1,2
**results_plot_logy_index=2

**parameter_sweep_begin
**m1_w_val=Auto:0.1u:20:10u
**m2_w_val=Auto:1u:5:5u
**parameter_sweep_end

**results_plot_begin
**gain_passband_dB
**fc_l
**fc_u
**GBW
**results_plot_end
"
}
C {launcher.sym} 1500 -15 0 0 {name=h2
descr=SimulatePARALLEL
tclcommand="
# Setup the default simulation commands if not already set up
# for example by already launched simulations.
set_sim_defaults
puts $sim(spice,1,cmd) 

# Change the Xyce command. In the spice category there are currently
# 5 commands (0, 1, 2, 3, 4). Command 3 is the Xyce batch
# you can get the number by querying $sim(spice,n)
set sim(spice,1,cmd) \{ngspice  \\"$N\\" -a\}

# change the simulator to be used (Xyce)
set sim(spice,default) 0

# Create FET and BIP .save file
mkdir -p $netlist_dir
write_data [save_params] $netlist_dir/[file rootname [file tail [xschem get current_name]]].save

# run netlist and simulation
xschem netlist
python3 ngspice_parallel_sweep.py [file tail [xschem get current_name]]
"}
