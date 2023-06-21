# This model represents an RFIC microstrip line in SG13G2 technology, simulated using two ports.
# The line is on TopMetal2 over Metal1 ground, line width w=15um for 50 Ohm
# Dimensions are set in the geometry section below.
#
# FDTD method excites one port at a time: excite port 1 to get S11 and S21, 
# excite port 2 to get S22 and S12
# In the code below function createSimulation() is called twice, once for each port, 
# to run these two excitations. Only with both results we get the full 2x2 element [S] matrix
# so that we can create an S2P output file.
#
# If you want to save time, and don't need the reverse direction S-params, 
# you can set variable full_2port = False which only calculates port 1 excitation.
# This gives S11 and S21 only, and the S2P file will not be created.
#
# If you just want to preview the model, set preview_only = True. This will skip simulation.
# If you just want to plot results that already exist from previous simulation, you can set 
# postprocess_only = True
#
# For this transmission line, simulation results are compared to measurements.
# Measurement data for the line is obtained by de-embedding the pad sections from raw measurement.

import os
from pylab import *

from CSXCAD  import ContinuousStructure
from openEMS import openEMS
from openEMS.physical_constants import *
from s2p_utils import *

# preview model/mesh only?
# postprocess existing data without re-running simulation?
preview_only = False
postprocess_only = False

# Simulate reverse path (S22 and S12) also?
full_2port = True

# get *.py model path and put simulation files in data directory below
model_path = os.path.normcase(os.path.dirname(__file__))
model_basename = os.path.basename(__file__).replace('.py','')
common_data_path = os.path.join(model_path, 'data')
sim_path = os.path.join(common_data_path,  model_basename)

print('Model path:', model_path)
print('Model basename:', model_basename)
print('Simulation data path:', sim_path, '\n')

# create data directory if it does not exist
if not os.path.exists(sim_path):
    os.makedirs(sim_path)

# change to data directory
os.chdir(sim_path)

############ simulation settings ############
 
unit = 1e-6 # specify everything in um
Z0=50 # reference impedance for ports

refined_cellsize = 0.5  # mesh resolution in line area 

fstart = 0
fstop  = 110e9
numfreq = 501  # number of frequency points (has no effect on simulation time!)

energy_limit = -50    # end criteria for residual energy
Boundaries   = ['PML_8', 'PML_8', 'PML_8', 'PML_8', 'PEC', 'PML_8']  # xmin xmax ymin ymax zmin zmax

eps_max = 11.9 # maximum permittivity in model, used for calculating max cellsize

lim = exp(energy_limit/10 * log(10))
FDTD = openEMS(EndCriteria=lim)
FDTD.SetGaussExcite( (fstart+fstop)/2, (fstop-fstart)/2 )
FDTD.SetBoundaryCond( Boundaries )

wavelength_air = (3e8/unit)/fstop
max_cellsize = wavelength_air/(sqrt(eps_max)*20) # max cellsize is lambda/20 in medium


def createSimulation (exciteport):
# Define function for model creation because we need to create and run separate CSX
# for each excitation. For S11,S21 we only need to excite port 1, but for S22,S12
# we need to excite port 2. This requires separate CSX with different port settings.


    ############ Geometry setup ############
    CSX = ContinuousStructure()
    FDTD.SetCSX(CSX)
    mesh = CSX.GetGrid()
    mesh.SetDeltaUnit(unit)


    # silicon substrate
    Sub = CSX.AddMaterial('Sub', epsilon=11.9, kappa=2)
    Sub_thick = 750
    Sub_zmin = 0
    Sub_zmax = Sub_zmin + Sub_thick

    # EPI
    EPI = CSX.AddMaterial('EPI', epsilon=11.9, kappa=5)
    EPI_thick = 3.75
    EPI_zmin = Sub_zmax
    EPI_zmax = EPI_zmin + EPI_thick

    # SiO2
    SiO2 = CSX.AddMaterial('SiO2', epsilon=4.1)
    SiO2_thick = 17.73
    SiO2_zmin = EPI_zmax
    SiO2_zmax = SiO2_zmin + SiO2_thick

    # Passivation
    # this stackup version does NOT include passivation, it has little effect and slows down simulation
    # because it enforces a small timestep (thin and high epsilon)

    # Air above is background material, no need to place box, just add mesh line
    Air_thick = 200
    Air_zmin = SiO2_zmax;
    Air_zmax = SiO2_zmax + Air_thick

    # Boxes for substrate, oxide etc that are not part of GDSII layout
    # must be created in main model file
    # That bounding box is NOT known upfront when materials are defined!


    # TopMetal2
    TopMetal2_sigma = 3.0300E7
    TopMetal2_thick = 3
    TopMetal2_zmin  = SiO2_zmin + 11.23
    TopMetal2_zmax  = TopMetal2_zmin + TopMetal2_thick
    TopMetal2 = CSX.AddMaterial('TopMetal2', kappa=TopMetal2_sigma)

    # TopMetal1
    TopMetal1_sigma = 2.7800E7
    TopMetal1_thick = 2
    TopMetal1_zmin  = SiO2_zmin + 6.43
    TopMetal1_zmax  = TopMetal1_zmin + TopMetal1_thick
    TopMetal1 = CSX.AddMaterial('TopMetal1', kappa=TopMetal1_sigma)

    # Metal5
    Metal5_sigma = 2.3190E7
    Metal5_thick = 0.49
    Metal5_zmin  = SiO2_zmin + 5.09
    Metal5_zmax  = Metal5_zmin + Metal5_thick
    Metal5 = CSX.AddMaterial('Metal5', kappa=Metal5_sigma)

    # Metal4
    Metal4_sigma = 2.3190E7
    Metal4_thick = 0.49
    Metal4_zmin  = SiO2_zmin + 4.06
    Metal4_zmax  = Metal4_zmin + Metal4_thick
    Metal4 = CSX.AddMaterial('Metal4', kappa=Metal4_sigma)

    # Metal3
    Metal3_sigma = 2.3190E7
    Metal3_thick = 0.49
    Metal3_zmin  = SiO2_zmin + 3.03
    Metal3_zmax  = Metal3_zmin + Metal3_thick
    Metal3 = CSX.AddMaterial('Metal3', kappa=Metal3_sigma)

    # Metal2
    Metal2_sigma = 2.3190E7
    Metal2_thick = 0.49
    Metal2_zmin  = SiO2_zmin + 2.0
    Metal2_zmax  = Metal2_zmin + Metal2_thick
    Metal2 = CSX.AddMaterial('Metal2', kappa=Metal2_sigma)

    # Metal1
    Metal1_sigma = 2.1640E7
    Metal1_thick = 0.42
    Metal1_zmin  = SiO2_zmin + 1.04
    Metal1_zmax  = Metal1_zmin + Metal1_thick
    Metal1 = CSX.AddMaterial('Metal1', kappa=Metal1_sigma)

    # TopVia2
    TopVia2_sigma = 3.1430E6
    TopVia2_zmin  = TopMetal1_zmax
    TopVia2_zmax  = TopMetal2_zmin
    TopVia2_thick = TopVia2_zmax-TopVia2_zmin
    TopVia2 = CSX.AddMaterial('TopVia2', kappa=TopVia2_sigma)

    # TopVia1
    TopVia1_sigma = 2.1910E6
    TopVia1_zmin  = Metal5_zmax
    TopVia1_zmax  = TopMetal1_zmin
    TopVia1_thick = TopVia1_zmax-TopVia1_zmin
    TopVia1 = CSX.AddMaterial('TopVia1', kappa=TopVia1_sigma)

    # Via4
    Via4_sigma = 1.6600E6
    Via4_zmin  = Metal4_zmax
    Via4_zmax  = Metal5_zmin
    Via4_thick = Via4_zmax-Via4_zmin
    Via4 = CSX.AddMaterial('Via4', kappa=Via4_sigma)

    # Via3
    Via3_sigma = 1.6600E6
    Via3_zmin  = Metal3_zmax
    Via3_zmax  = Metal4_zmin
    Via3_thick = Via3_zmax-Via3_zmin
    Via3 = CSX.AddMaterial('Via3', kappa=Via3_sigma)

    # Via2
    Via2_sigma = 1.6600E6
    Via2_zmin  = Metal2_zmax
    Via2_zmax  = Metal3_zmin
    Via2_thick = Via2_zmax-Via2_zmin
    Via2 = CSX.AddMaterial('Via2', kappa=Via2_sigma)

    # Via1
    Via1_sigma = 1.6600E6
    Via1_zmin  = Metal1_zmax
    Via1_zmax  = Metal2_zmin
    Via1_thick = Via1_zmax-Via1_zmin
    Via1 = CSX.AddMaterial('Via1', kappa=Via1_sigma)

    # Cont
    Cont_sigma = 2.3900E6
    Cont_zmin  = EPI_zmax
    Cont_zmax  = Metal1_zmin
    Cont_thick = Cont_zmax-Cont_zmin
    Cont = CSX.AddMaterial('Cont', kappa=Cont_sigma)



    ############# begin layout geometries ###########

    # TopMetal2 line over Metal1, w=15um for 50 Ohm
    wline = 15
    lline = 880
    wgnd  = 90
    lgnd  = lline+50


    TopMetal2.AddBox(priority=200, start=[-lline/2, -wline/2, TopMetal2_zmin], stop=[lline/2, wline/2, TopMetal2_zmax])

    # Metal1 ground plane w=90um 
    Metal1.AddBox(priority=200, start=[-lgnd/2, -wgnd/2, Metal1_zmin], stop=[lgnd/2, wgnd/2, Metal1_zmax])

    ############# end layout geometries ##########

    ############ ports created manually ##########
   
    if exciteport==1:
        port1 = FDTD.AddLumpedPort(1, Z0, [-lline/2, -wline/2, Metal1_zmax], [-lline/2, wline/2, TopMetal2_zmin], 'z', excite=1.0, priority=150)
        port2 = FDTD.AddLumpedPort(2, Z0, [ lline/2, -wline/2, Metal1_zmax], [ lline/2, wline/2, TopMetal2_zmin], 'z', excite=0,   priority=150)        
    else:    
        port1 = FDTD.AddLumpedPort(1, Z0, [-lline/2, -wline/2, Metal1_zmax], [-lline/2, wline/2, TopMetal2_zmin], 'z', excite=0,   priority=150)
        port2 = FDTD.AddLumpedPort(2, Z0, [ lline/2, -wline/2, Metal1_zmax], [ lline/2, wline/2, TopMetal2_zmin], 'z', excite=1.0, priority=150)        
    


    #################  end ports  ################

    # Simulation box with some margin to line
    box_xmin = -(lgnd/2+100)
    box_xmax =  (lgnd/2+100)
    box_ymin = -(wgnd/2+150)
    box_ymax =  (wgnd/2+150)

    # create boxes for substrate, oxide etc that are not drawn in GDSII layout
    Sub.AddBox(priority=10, start=[box_xmin+50, box_ymin+50, Sub_zmin], stop=[box_xmax-50, box_ymax-50, Sub_zmax])
    EPI.AddBox(priority=10, start=[box_xmin+50, box_ymin+50, EPI_zmin], stop=[box_xmax-50, box_ymax-50, EPI_zmax])
    SiO2.AddBox(priority=10, start=[box_xmin+50, box_ymin+50, SiO2_zmin], stop=[box_xmax-50, box_ymax-50, SiO2_zmax])

    ############# create vertical mesh  #############


    def add_equal_meshlines ( start, stop, number):
        return list(linspace(start,stop,number))

    def add_graded_meshlines (start, stop, stepstart, factor, maxstep):
        lines = [start]
        value = start
        step = stepstart
        finished = False

        while not finished:
            value = value + step
            lines.append(value)
            step = step * factor

            if (step/maxstep > 1):
                step = maxstep

            if  start<stop:
                finished = (value+step) > stop
            else:
                finished = (value+step) < stop

        if (value!=stop):
            lines.append(stop)
        return lines



    # Sub: fill DOWNWARDS with increasing mesh size
    lines = add_graded_meshlines (Sub_zmax, Sub_zmin, -1.5*refined_cellsize, 1.3, -max_cellsize)
    for line in lines:
        mesh.AddLine('z', line)
        
    # EPI: fill equal mesh size
    lines = add_equal_meshlines(EPI_zmin,EPI_zmax, int(ceil(EPI_thick/refined_cellsize)+1))
    for line in lines:
        mesh.AddLine('z', line)

    # SiO2: Fill down to TopMetal2 only because metals inside SiO2 have their own mesh lines
    lines = add_equal_meshlines(TopMetal2_zmax,SiO2_zmax, int(ceil((SiO2_zmax-TopMetal2_zmax)/refined_cellsize)+1))
    for line in lines:
        mesh.AddLine('z', line)
        
    # Passivation: not included in this stackup version

    # Air above: fill UPWARDS with increasing mesh size
    lines = add_graded_meshlines (Air_zmin, Air_zmax, 1.5, 1.3, max_cellsize)
    for line in lines:
        mesh.AddLine('z', line)

    # Metals
    # For thick top metal, place multiple few mesh lines based on refined_cellsize
    # For thin metal layers, create top AND bottom mesh line only if metal is actually used, otherwise only top
    lines = add_equal_meshlines(TopMetal2_zmin, TopMetal2_zmax, int(ceil(TopMetal2_thick/refined_cellsize)+1))
    for line in lines:
        mesh.AddLine('z', line)
        
    lines = add_equal_meshlines(TopMetal1_zmin, TopMetal1_zmax, int(ceil(TopMetal1_thick/refined_cellsize)+1))
    for line in lines:
        mesh.AddLine('z', line)

    mesh.AddLine('z',Metal5_zmax)
    if (Metal5.GetQtyPrimitives() > 0): mesh.AddLine('z',Metal5_zmin)
        
    mesh.AddLine('z',Metal4_zmax)
    if (Metal4.GetQtyPrimitives() > 0): mesh.AddLine('z',Metal4_zmin)

    mesh.AddLine('z',Metal3_zmax)
    if (Metal3.GetQtyPrimitives() > 0): mesh.AddLine('z',Metal3_zmin)

    mesh.AddLine('z',Metal2_zmax)
    if (Metal2.GetQtyPrimitives() > 0): mesh.AddLine('z',Metal2_zmin)

    mesh.AddLine('z',Metal1_zmax)
    if (Metal1.GetQtyPrimitives() > 0): mesh.AddLine('z',Metal1_zmin)


    # Vias, except for short vias between thin metals
    lines = add_equal_meshlines(TopVia2_zmin, TopVia2_zmax, int(ceil(TopVia2_thick/refined_cellsize)+1))
    for line in lines:
        mesh.AddLine('z', line)
        
    if (TopVia1.GetQtyPrimitives() > 0):
        lines = add_equal_meshlines(TopVia1_zmin,TopVia1_zmax, int(ceil(TopVia1_thick/refined_cellsize)+1))
        for line in lines:
            mesh.AddLine('z', line)
        
    if (Cont.GetQtyPrimitives() > 0):
        lines = add_equal_meshlines(Cont_zmin,Cont_zmax, int(ceil(Cont_thick/refined_cellsize)+1))
        for line in lines:
            mesh.AddLine('z', line)


    ############ build final mesh ##########
    mesh.AddLine('x', box_xmin)
    mesh.AddLine('x', box_xmax)

    mesh.AddLine('y', box_ymin)
    mesh.AddLine('y', box_ymax)

    mesh.AddLine('x', -lgnd/2)
    mesh.AddLine('x',  lgnd/2)


    # refine mesh in conductor regions 
    # fine mesh near port 1
    lines = add_equal_meshlines(-lline/2-10, -lline/2+10, 11)
    for line in lines:
        mesh.AddLine('x', line)

    #finer mesh near port 2
    lines = add_equal_meshlines(lline/2-10, lline/2+10, 11)
    for line in lines:
        mesh.AddLine('x', line)

    # fine mesh across line width
    lines = add_equal_meshlines(-wline/2, wline/2, round(wline/refined_cellsize))
    for line in lines:
        mesh.AddLine('y', line)
  
    
    mesh.SmoothMeshLines('x', max_cellsize, 1.3)
    mesh.SmoothMeshLines('y', max_cellsize, 1.3)
    # don't smooth mesh in z-direction, that is already final!


    #################### write model file and view in AppCSXCAD ################


    
    # create subdirectory to hold data for this excitation
    excitation_path = os.path.join(sim_path, 'sub-' + str(exciteport))
    if not os.path.exists(excitation_path):
        os.makedirs(excitation_path)

    # write CSX file 
    CSX_file = os.path.join(excitation_path, model_basename + '.xml')
    CSX.Write2XML(CSX_file)

    if not postprocess_only: # preview model, but only for first port excitation
        if (exciteport==1): 
            from CSXCAD import AppCSXCAD_BIN
            os.system(AppCSXCAD_BIN + ' "{}"'.format(CSX_file))

    if not preview_only:  # start simulation 
        if not postprocess_only:
            print("Running FDTD simulation, excitation port " + str(exciteport))
            starttime=time.time()
            FDTD.Run(excitation_path, verbose=1)
            finishtime=time.time()
            print(" done! Simulation time " + str(int(finishtime-starttime)) + " seconds \n")


    # return ports, so that we can postprocess them
    return port1, port2, excitation_path
  
######### end of function createSimulation (exciteport) ##########



########### create model, run and post-process ###########

f = np.linspace(fstart,fstop,numfreq)

# call createSimulation function defined above 
sub1_port1, sub1_port2, sub1_excitation_path = createSimulation (1)  # excite port 1 
if full_2port:
    sub2_port1, sub2_port2, sub2_excitation_path = createSimulation (2)  # excite port 2

if not preview_only:
    # evaluate port 1 excitation
    sub1_port1.CalcPort( sub1_excitation_path, f, ref_impedance = Z0)
    sub1_port2.CalcPort( sub1_excitation_path, f, ref_impedance = Z0)

    s11 = sub1_port1.uf_ref / sub1_port1.uf_inc
    s21 = sub1_port2.uf_ref / sub1_port1.uf_inc

    if full_2port:
        # evaluate port 2 excitation
        sub2_port1.CalcPort( sub2_excitation_path, f, ref_impedance = Z0)
        sub2_port2.CalcPort( sub2_excitation_path, f, ref_impedance = Z0)

        s22 = sub2_port2.uf_ref / sub2_port2.uf_inc
        s12 = sub2_port1.uf_ref / sub2_port2.uf_inc

    ### Plot results

    s11_dB = 20.0*np.log10(np.abs(s11))
    s11_phase = angle(s11, deg=True) 

    s21_dB = 20.0*np.log10(np.abs(s21))
    s21_phase = angle(s21, deg=True) 

    if full_2port:
        s22_dB = 20.0*np.log10(np.abs(s22))
        s22_phase = angle(s22, deg=True) 

        s12_dB = 20.0*np.log10(np.abs(s12))
        s12_phase = angle(s12, deg=True) 

    # get measured data
    measured_filename = os.path.join(model_path, 'measured/LINE_880_corrected.S2P')
    fmeas, Smeas = readS2P(measured_filename)   
    s11meas,s12meas,s21meas,s22meas = S_to_sxx (Smeas) 

    s11meas_dB = 20.0*np.log10(np.abs(s11meas))
    s11meas_phase = angle(s11meas, deg=True) 

    s21meas_dB = 20.0*np.log10(np.abs(s21meas))
    s21meas_phase = angle(s21meas, deg=True) 


    # compare simulated and measured
    plot_compare (f, s11_dB, 'S11 simulation', fmeas, s11meas_dB, 'S11 measured', '[dB]')
    plot_compare (f, s21_dB, 'S21 simulation', fmeas, s21meas_dB, 'S21 measured', '[dB] ')
      
      
    if full_2port:
        # create Touchstone S2P output file in simulation data path
        # this required full S-matrix with forward and reverse path
        s2p_name = os.path.join(sim_path, model_basename + '.s2p')
        
        S = sxx_to_S (s11, s12, s21, s22)
        writeS2P (f, S, s2p_name)


    # show plots
    show()


     