v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
T {Ctrl-Click to execute launcher} 90 -510 0 0 0.3 0.3 {layer=11}
T {possible parameter sweep types:
Auto:Begin:TotalPoints:End
Lin:Begin:StepSize:End
Dec:Begin:PointsPerDecade:End
Log:Begin:TotalPoints:End} 1340 -360 0 0 0.3 0.3 {layer=11}
T {sort .csv file by given index} 1340 -450 0 0 0.3 0.3 {layer=11}
T {number of parallel workers} 1340 -470 0 0 0.3 0.3 {layer=11}
N 110 -180 110 -160 {
lab=GND}
N 270 -180 270 -160 {
lab=GND}
N 110 -320 110 -240 {
lab=isosub_net}
N 110 -320 270 -320 {
lab=isosub_net}
N 270 -320 270 -300 {
lab=isosub_net}
N 270 -240 350 -240 {
lab=nwell_net}
N 270 -320 350 -320 {
lab=isosub_net}
N 350 -240 350 -220 {
lab=nwell_net}
C {devices/title.sym} 245 -55 0 0 {name=l5 author="IHP Open PDK Authors 2025"}
C {launcher.sym} 150 -465 0 0 {name=h3
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
file mkdir $netlist_dir
write_data [save_params] $netlist_dir/[file rootname [file tail [xschem get current_name]]].save

# run netlist and simulation
xschem netlist
simulate
"}
C {simulator_commands_shown.sym} 485 -465 0 0 {name=SWEEP_SIM
simulator=ngspice
only_toplevel=false 
value="
.param temp=27
.param iso_w=3u
.param iso_l=3u


.control
set num_threads 1

dc I0 -1m 1m 1u
meas dc vbk_pos find v(isosub_net) at=1u
meas dc vbk_neg find v(isosub_net) at=-1u
echo results_sweep_begin
print vbk_pos
print vbk_neg
echo results_sweep_end

.endc
"
}
C {code_shown.sym} 1000 -480 0 0 {name=SWEEP_SETTINGS
only_toplevel=false
value="
**nr_workers=50
**sort_results_index=3
**results_plot_contour_index=0,1
**results_plot_logx_index=3
**results_plot_logy_index=3

**parameter_sweep_begin
**iso_w=Auto:3u:10:300u
**iso_l=Auto:3u:10:500u
**parameter_sweep_end

**results_plot_begin
**vbk_pos
**vbk_neg
**results_plot_end
"
}
C {launcher.sym} 1050 -135 0 0 {name=h2
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
file mkdir $netlist_dir
write_data [save_params] $netlist_dir/[file rootname [file tail [xschem get current_name]]].save

# run netlist and simulation
xschem netlist
python3 $\{PDK_ROOT\}/$\{PDK\}/libs.tech/xschem/sg13g2_tests/ngspice_parallel_sweep.py [file tail [xschem get current_name]]
"}
C {devices/gnd.sym} 110 -160 0 0 {name=l6 lab=GND}
C {devices/code_shown.sym} 90 -400 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.include diodes.lib
"}
C {isource.sym} 110 -210 2 0 {name=I0 value=1m}
C {devices/gnd.sym} 270 -160 0 0 {name=l7 lab=GND}
C {lab_pin.sym} 350 -320 2 0 {name=p6 sig_type=std_logic lab=isosub_net}
C {lab_pin.sym} 350 -240 2 0 {name=p7 sig_type=std_logic lab=nwell_net}
C {sg13g2_pr/isolbox.sym} 270 -240 0 0 {name=D1
model=isolbox
l=\{iso_l\}
w=\{iso_w\}
spiceprefix=X
}
C {noconn.sym} 350 -220 3 0 {name=l8}
