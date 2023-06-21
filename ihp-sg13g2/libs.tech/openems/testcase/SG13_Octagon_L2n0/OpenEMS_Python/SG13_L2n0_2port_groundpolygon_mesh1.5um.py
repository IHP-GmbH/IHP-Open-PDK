# This model represents an RFIC inductor in SG13G2 technology, simulated using two ports
# with a common ground node. That ground node is connected to bulk substrate, so that 
# simulation results include both series effects (in coil)  and shunt effects (coil to substrate).
#
# In openEMS (FDTD) that requires excitation at both ports, one after another. In the code below
# function createSimulation() is called twice, once for each port, to run these two excitations.
# Only with both results we get the full 2x2 element [S] matrix.
#
# If only the series L and series R are required, we can use a simpler and faster simulation setup
# where one port is required, connected between the two inductor terminals. Limitation: that 1-port 
# model cannot be evaluated for shunt capacitance to the substrate.
#
# For comparison to 1-port results, the code below also extracts series L and series R 
# by converting the 2-port data into differential 1-port data. That calculated 1-port data is 
# the same as directly simulating the 1-port model in openEMS (which is also available as an example). 
#
# If you just want to preview the model, set preview_only = True. This will skip simulation.
# If you just want to plot results that already exist from previous simulation, you can set 
# postprocess_only = True

import os
from pylab import *

from CSXCAD  import ContinuousStructure
from openEMS import openEMS
from openEMS.physical_constants import *

# preview model/mesh only?
# postprocess existing data without re-running simulation?
preview_only = False
postprocess_only = False

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
# os.chdir(sim_path)

############ simulation settings ############
 
unit = 1e-6 # specify everything in um
Z0=50 # reference impedance for ports

refined_cellsize = 1.5  # mesh resolution in area with polygons from GDSII

fstart = 0
fstop  = 30e9
numfreq = 401  # number of frequency points (has no effect on simulation time!)

energy_limit = -50    # end criteria for residual energy
Boundaries   = ['PEC', 'PEC', 'PEC', 'PEC', 'PEC', 'PEC']  # xmin xmax ymin ymax zmin zmax

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
    Sub_thick = 280
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
    Air_thick = 300
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

    # Cell ('L_2n0_simplify", 10 polygons, 0 paths, 2 labels, 0 references)

    pts_x = np.array([])
    pts_y = np.array([])
    pts_x = r_[pts_x, 22.200]
    pts_y = r_[pts_y, 0.000]
    pts_x = r_[pts_x, 34.200]
    pts_y = r_[pts_y, 0.000]
    pts_x = r_[pts_x, 34.200]
    pts_y = r_[pts_y, 57.000]
    pts_x = r_[pts_x, 22.200]
    pts_y = r_[pts_y, 57.000]
    pts = np.array([pts_x, pts_y])
    TopMetal1.AddLinPoly(priority=200, points=pts, norm_dir ='z', elevation=TopMetal1_zmin, length=TopMetal1_thick)

    pts_x = np.array([])
    pts_y = np.array([])
    pts_x = r_[pts_x, -34.200]
    pts_y = r_[pts_y, 0.000]
    pts_x = r_[pts_x, -22.200]
    pts_y = r_[pts_y, 0.000]
    pts_x = r_[pts_x, -22.200]
    pts_y = r_[pts_y, 57.000]
    pts_x = r_[pts_x, -34.200]
    pts_y = r_[pts_y, 57.000]
    pts = np.array([pts_x, pts_y])
    TopMetal1.AddLinPoly(priority=200, points=pts, norm_dir ='z', elevation=TopMetal1_zmin, length=TopMetal1_thick)

    pts_x = np.array([])
    pts_y = np.array([])
    pts_x = r_[pts_x, -23.230]
    pts_y = r_[pts_y, 272.000]
    pts_x = r_[pts_x, -9.985]
    pts_y = r_[pts_y, 272.000]
    pts_x = r_[pts_x, 5.015]
    pts_y = r_[pts_y, 257.000]
    pts_x = r_[pts_x, 23.230]
    pts_y = r_[pts_y, 257.000]
    pts_x = r_[pts_x, 23.230]
    pts_y = r_[pts_y, 269.000]
    pts_x = r_[pts_x, 9.985]
    pts_y = r_[pts_y, 269.000]
    pts_x = r_[pts_x, -5.015]
    pts_y = r_[pts_y, 284.000]
    pts_x = r_[pts_x, -23.230]
    pts_y = r_[pts_y, 284.000]
    pts = np.array([pts_x, pts_y])
    TopMetal1.AddLinPoly(priority=200, points=pts, norm_dir ='z', elevation=TopMetal1_zmin, length=TopMetal1_thick)

    pts_x = np.array([])
    pts_y = np.array([])
    pts_x = r_[pts_x, 11.230]
    pts_y = r_[pts_y, 257.000]
    pts_x = r_[pts_x, 41.425]
    pts_y = r_[pts_y, 257.000]
    pts_x = r_[pts_x, 100.000]
    pts_y = r_[pts_y, 198.425]
    pts_x = r_[pts_x, 100.000]
    pts_y = r_[pts_y, 115.575]
    pts_x = r_[pts_x, 41.425]
    pts_y = r_[pts_y, 57.000]
    pts_x = r_[pts_x, 22.200]
    pts_y = r_[pts_y, 57.000]
    pts_x = r_[pts_x, 22.200]
    pts_y = r_[pts_y, 45.000]
    pts_x = r_[pts_x, 46.395]
    pts_y = r_[pts_y, 45.000]
    pts_x = r_[pts_x, 112.000]
    pts_y = r_[pts_y, 110.605]
    pts_x = r_[pts_x, 112.000]
    pts_y = r_[pts_y, 203.395]
    pts_x = r_[pts_x, 46.395]
    pts_y = r_[pts_y, 269.000]
    pts_x = r_[pts_x, 11.230]
    pts_y = r_[pts_y, 269.000]
    pts = np.array([pts_x, pts_y])
    TopMetal2.AddLinPoly(priority=200, points=pts, norm_dir ='z', elevation=TopMetal2_zmin, length=TopMetal2_thick)

    pts_x = np.array([])
    pts_y = np.array([])
    pts_x = r_[pts_x, -100.000]
    pts_y = r_[pts_y, 115.575]
    pts_x = r_[pts_x, -100.000]
    pts_y = r_[pts_y, 198.425]
    pts_x = r_[pts_x, -41.425]
    pts_y = r_[pts_y, 257.000]
    pts_x = r_[pts_x, -5.015]
    pts_y = r_[pts_y, 257.000]
    pts_x = r_[pts_x, 9.985]
    pts_y = r_[pts_y, 272.000]
    pts_x = r_[pts_x, 47.635]
    pts_y = r_[pts_y, 272.000]
    pts_x = r_[pts_x, 115.000]
    pts_y = r_[pts_y, 204.635]
    pts_x = r_[pts_x, 115.000]
    pts_y = r_[pts_y, 109.365]
    pts_x = r_[pts_x, 47.635]
    pts_y = r_[pts_y, 42.000]
    pts_x = r_[pts_x, -47.635]
    pts_y = r_[pts_y, 42.000]
    pts_x = r_[pts_x, -115.000]
    pts_y = r_[pts_y, 109.365]
    pts_x = r_[pts_x, -115.000]
    pts_y = r_[pts_y, 204.635]
    pts_x = r_[pts_x, -47.635]
    pts_y = r_[pts_y, 272.000]
    pts_x = r_[pts_x, -11.230]
    pts_y = r_[pts_y, 272.000]
    pts_x = r_[pts_x, -11.230]
    pts_y = r_[pts_y, 284.000]
    pts_x = r_[pts_x, -52.605]
    pts_y = r_[pts_y, 284.000]
    pts_x = r_[pts_x, -127.000]
    pts_y = r_[pts_y, 209.605]
    pts_x = r_[pts_x, -127.000]
    pts_y = r_[pts_y, 104.395]
    pts_x = r_[pts_x, -52.605]
    pts_y = r_[pts_y, 30.000]
    pts_x = r_[pts_x, 52.605]
    pts_y = r_[pts_y, 30.000]
    pts_x = r_[pts_x, 127.000]
    pts_y = r_[pts_y, 104.395]
    pts_x = r_[pts_x, 127.000]
    pts_y = r_[pts_y, 209.605]
    pts_x = r_[pts_x, 52.605]
    pts_y = r_[pts_y, 284.000]
    pts_x = r_[pts_x, 5.015]
    pts_y = r_[pts_y, 284.000]
    pts_x = r_[pts_x, -9.985]
    pts_y = r_[pts_y, 269.000]
    pts_x = r_[pts_x, -46.395]
    pts_y = r_[pts_y, 269.000]
    pts_x = r_[pts_x, -112.000]
    pts_y = r_[pts_y, 203.395]
    pts_x = r_[pts_x, -112.000]
    pts_y = r_[pts_y, 110.605]
    pts_x = r_[pts_x, -46.395]
    pts_y = r_[pts_y, 45.000]
    pts_x = r_[pts_x, -22.200]
    pts_y = r_[pts_y, 45.000]
    pts_x = r_[pts_x, -22.200]
    pts_y = r_[pts_y, 57.000]
    pts_x = r_[pts_x, -41.425]
    pts_y = r_[pts_y, 57.000]
    pts = np.array([pts_x, pts_y])
    TopMetal2.AddLinPoly(priority=200, points=pts, norm_dir ='z', elevation=TopMetal2_zmin, length=TopMetal2_thick)

    pts_x = np.array([])
    pts_y = np.array([])
    pts_x = r_[pts_x, -22.610]
    pts_y = r_[pts_y, 272.620]
    pts_x = r_[pts_x, -11.860]
    pts_y = r_[pts_y, 272.620]
    pts_x = r_[pts_x, -11.860]
    pts_y = r_[pts_y, 283.370]
    pts_x = r_[pts_x, -22.610]
    pts_y = r_[pts_y, 283.370]
    pts = np.array([pts_x, pts_y])
    TopVia2.AddLinPoly(priority=200, points=pts, norm_dir ='z', elevation=TopVia2_zmin, length=TopVia2_thick)

    pts_x = np.array([])
    pts_y = np.array([])
    pts_x = r_[pts_x, 11.850]
    pts_y = r_[pts_y, 257.620]
    pts_x = r_[pts_x, 22.600]
    pts_y = r_[pts_y, 257.620]
    pts_x = r_[pts_x, 22.600]
    pts_y = r_[pts_y, 268.370]
    pts_x = r_[pts_x, 11.850]
    pts_y = r_[pts_y, 268.370]
    pts = np.array([pts_x, pts_y])
    TopVia2.AddLinPoly(priority=200, points=pts, norm_dir ='z', elevation=TopVia2_zmin, length=TopVia2_thick)

    pts_x = np.array([])
    pts_y = np.array([])
    pts_x = r_[pts_x, -33.580]
    pts_y = r_[pts_y, 45.620]
    pts_x = r_[pts_x, -22.830]
    pts_y = r_[pts_y, 45.620]
    pts_x = r_[pts_x, -22.830]
    pts_y = r_[pts_y, 56.370]
    pts_x = r_[pts_x, -33.580]
    pts_y = r_[pts_y, 56.370]
    pts = np.array([pts_x, pts_y])
    TopVia2.AddLinPoly(priority=200, points=pts, norm_dir ='z', elevation=TopVia2_zmin, length=TopVia2_thick)

    pts_x = np.array([])
    pts_y = np.array([])
    pts_x = r_[pts_x, 22.820]
    pts_y = r_[pts_y, 45.620]
    pts_x = r_[pts_x, 33.570]
    pts_y = r_[pts_y, 45.620]
    pts_x = r_[pts_x, 33.570]
    pts_y = r_[pts_y, 56.370]
    pts_x = r_[pts_x, 22.820]
    pts_y = r_[pts_y, 56.370]
    pts = np.array([pts_x, pts_y])
    TopVia2.AddLinPoly(priority=200, points=pts, norm_dir ='z', elevation=TopVia2_zmin, length=TopVia2_thick)

    # Bounding box of INDUCTOR geometry
    geometry_xmin= -127.000
    geometry_xmax= 127.000
    geometry_ymin= 0.000
    geometry_ymax= 284.000


    # ground shape on Metal1 connected to Sub, this will have an effect on single ended S-params
    Metal1.AddBox(priority=200, start=[-240, -140, Metal1_zmin], stop=[240, 10, Metal1_zmax])
    Cont.AddBox(priority=170, start=[-240, -100, Cont_zmin], stop=[-170, -30, Cont_zmax])
    Cont.AddBox(priority=170, start=[ -35, -100, Cont_zmin], stop=[  35, -30, Cont_zmax])
    Cont.AddBox(priority=170, start=[ 240, -100, Cont_zmin], stop=[ 170, -30, Cont_zmax])



    ############# end layout geometries ##########

    ############ ports created manually ##########

    # port 1 in x direction, 50 Ohm reference impedance
    # port 2 with opposite direction
    
    if exciteport==1:
        port1 = FDTD.AddLumpedPort(1, Z0, [-22.2, 0, TopMetal1_zmin], [-10, 10, TopMetal1_zmax], 'x', excite=1.0, priority=150)
        port2 = FDTD.AddLumpedPort(2, Z0, [ 22.2, 0, TopMetal1_zmin], [ 10, 10, TopMetal1_zmax], 'x', excite=0,   priority=150)
    else:    
        port1 = FDTD.AddLumpedPort(1, Z0, [-22.2, 0, TopMetal1_zmin], [-10, 10, TopMetal1_zmax], 'x', excite=0,   priority=150)
        port2 = FDTD.AddLumpedPort(2, Z0, [ 22.2, 0, TopMetal1_zmin], [ 10, 10, TopMetal1_zmax], 'x', excite=1.0, priority=150)
    

    # create ground polygon in the middle, connect from TopMetal1 down to Metal1
    # This will be the common ground for both ports
    GND_REF = CSX.AddMetal( 'PEC' )
    GND_REF.AddBox(priority=210, start=[-10, -10, Metal1_zmax], stop=[10, 10, TopMetal1_zmax])


    #################  end ports  ################

    geometry_width = geometry_xmax - geometry_xmin
    geometry_height = geometry_ymax - geometry_ymin

    # for inductors, add margin of one inductor diameter on each side, so that metal walls have no effect
    box_xmin = geometry_xmin - 1.0 * geometry_width
    box_xmax = geometry_xmax + 1.0 * geometry_width
    box_ymin = geometry_ymin - 1.0 * geometry_height
    box_ymax = geometry_ymax + 1.0 * geometry_height

    # create boxes for substrate, oxide etc that are not drawn in GDSII layout
    Sub.AddBox(priority=10, start=[box_xmin, box_ymin, Sub_zmin], stop=[box_xmax, box_ymax, Sub_zmax])
    EPI.AddBox(priority=10, start=[box_xmin, box_ymin, EPI_zmin], stop=[box_xmax, box_ymax, EPI_zmax])
    SiO2.AddBox(priority=10, start=[box_xmin, box_ymin, SiO2_zmin], stop=[box_xmax, box_ymax, SiO2_zmax])

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

    # refine mesh in conductor regions
    lines = add_equal_meshlines(geometry_xmin, geometry_xmax, round(geometry_width/refined_cellsize))
    for line in lines:
        mesh.AddLine('x', line)
        
    lines = add_equal_meshlines(geometry_ymin, geometry_ymax, round(geometry_height/refined_cellsize))
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
sub2_port1, sub2_port2, sub2_excitation_path = createSimulation (2)  # excite port 2

if not preview_only:
    # evaluate port 1 excitation
    sub1_port1.CalcPort( sub1_excitation_path, f, ref_impedance = Z0)
    sub1_port2.CalcPort( sub1_excitation_path, f, ref_impedance = Z0)

    s11 = sub1_port1.uf_ref / sub1_port1.uf_inc
    s21 = sub1_port2.uf_ref / sub1_port1.uf_inc

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

    s22_dB = 20.0*np.log10(np.abs(s22))
    s22_phase = angle(s22, deg=True) 

    s12_dB = 20.0*np.log10(np.abs(s12))
    s12_phase = angle(s12, deg=True) 

       
    # S11,S22 dB
    figure()
    plot(f/1e9, s11_dB, 'k-', linewidth=2, label='$S_{11}$')
    plot(f/1e9, s22_dB, 'r--', linewidth=2, label='$S_{22}$')
    grid()
    legend()
    ylabel('S11,S22 (dB)')
    xlabel('Frequency (GHz)')    

    # S21, S12 dB
    figure()
    plot(f/1e9, s21_dB, 'k-', linewidth=2, label='$S_{21}$')
    plot(f/1e9, s12_dB, 'r--', linewidth=2, label='$S_{12}$')
    grid()
    legend()
    ylabel('S21,S12 (dB)')
    xlabel('Frequency (GHz)')    

    # optional conversion to differential parameters (symmetric inductor use)
    z11 = Z0 * (((1+s11)*(1-s22))+s12*s21) / (((1-s11)*(1-s22))-s12*s21)
    z12 = Z0 * (2*s12) / (((1-s11)*(1-s22))-s12*s21)
    z21 = Z0 * (2*s21) / (((1-s11)*(1-s22))-s12*s21)
    z22 = Z0 * (((1-s11)*(1+s22))+s12*s21) / (((1-s11)*(1-s22))-s12*s21)    

    zdiff = z11 - z12 - z21 +z22

    # Rseries for symmetric excitation
    Rseries = real(zdiff)
    figure()
    plot(f/1e9, Rseries, 'k-', linewidth=2, label='Rseries')
    ylim(0, 10)
    xlim(0, fstop/1e9)
    grid()
    legend()
    ylabel('Differential Rseries (Ohm)')
    xlabel('Frequency (GHz)')

    # ignore warning when dividing by zero frequency in L calculation
    import warnings
    warnings.filterwarnings('ignore')

    # Lseries for symmetric excitation
    omega = 2*pi*f
    Lseries = imag(zdiff)/omega
    figure()
    plot(f/1e9, Lseries*1e9, 'k-', linewidth=2, label='Lseries')
    ylim(0, 10)
    xlim(0, fstop/1e9)
    grid()
    legend()
    ylabel('Differential Lseries (nH)')
    xlabel('Frequency (GHz)')

    # Q factor for symmetric excitation
    Q = imag(zdiff)/real(zdiff)
    figure()
    plot(f/1e9, Q, 'k-', linewidth=2, label='Q')
    ylim(0, 30)
    xlim(0, fstop/1e9)
    grid()
    legend()
    ylabel('Differential Q factor')
    xlabel('Frequency (GHz)')

    # create Touchstone S2P output file in simulation data path
    s2p_name = os.path.join(sim_path, model_basename + '.s2p')
    s2p_file = open(s2p_name, 'w')
    s2p_file.write('#   Hz   S  RI   R   50\n')
    s2p_file.write('!\n')
    for index in range(0, numfreq):
        freq = f[index]
        s11re = real(s11[index])
        s11im = imag(s11[index])
        s12re = real(s12[index])
        s12im = imag(s12[index])
        s21re = real(s21[index])
        s21im = imag(s21[index])
        s22re = real(s22[index])
        s22im = imag(s22[index])
        s2p_file.write(str(freq) + ' ' + str(s11re) + ' ' + str(s11im) + ' ' + str(s21re) + ' ' + str(s21im) + ' ' + str(s12re) + ' ' + str(s12im) + ' ' + str(s22re) + ' ' + str(s22im) + '\n')
    s2p_file.close()

    # show plots
    show()


     