# openEMS for IHP SG13G2 technology

openEMS is a free and open electromagnetic field solver using the FDTD method. 
https://www.openems.de/

The files provided here are examples how to use openEMS for simulation of 
on-chip structures in IHP SG13G2 technology. All models for openEMS are code-based, 
using either Matlab or Python environment. Instead of using Matlab, you can also 
use the free Octave environment, which is compatible with the Matlab code provided here.

The model code includes geometry setup (here an inductor with one differential port) 
and technology stackup definition for SG13G2, plus some model setup. 

Please refer to the PDF documents in the Matlab and Python model directories for detailed instructions.

# GDSII import
When creating your own models, you need to replace the example 
geometry code with your own geometries. To simplify that, we provide python translators 
that convert GDSII layout to openEMS code for Matlab/Octave or Python syntax. The code 
can then be included in the model using copy&paste.
Note that these translators are specifically designed for IHP SG13G2 technology, the 
resulting code only works with the stackup definition and material names in the model code 
provided here.

These scripts are run from the command line, the only parameter is the GDSII filename. 
For example in openEMS Matlab syntax,
python3 gds2matlabpoly.py L2n0.gds
will create an output file L2n0_polygons.m which can then be inserted into the model template. 
The layer table inside the script defines what GDSII layer numbers and purposes are evaluated, 
and map the corresponding material names for the output file.

All example models provided here are complete and ready to run, they already include the 
geometry code. Translators are only required when you create your own models from GDSII data.

# Matlab inductor example
The Matlab example SG13_L2n0_30GHz_mesh1um_50dB.m models a 2nH inductor over frequency 
range 0 to 30 GHz. One single port is defined between the terminals, so that we get 1-port 
S-parameters. In the model code, that results is converted into the equivalent series 
elements and L,R, Q are plotted over frequency. 
The example code references two external files: SG13G2 technology setup and a utility 
to write Touchstone S1P files. 

# Python inductor example
The Python examples SG13_L2n0_mesh1.5um_v2.py and SG13_L2n0_mesh1um_v2.py model
a 2nH inductor over frequency range 0 to 30 GHz. One single port is defined between the 
terminals, so that we get 1-port S-parameters. In the model code, that results is 
converted into the equivalent series elements and L,R, Q are plotted over frequency.
The difference between both models is mesh density, 1.5um and 1um. 

Model SG13_L2n0_2port_groundpolygon_mesh1.5um.py shows how to create a 2-port simulation 
with a common ground node. That ground node is connected to bulk substrate, so that 
simulation results include both series effects (in coil)  and shunt effects (coil to substrate).
In openEMS (FDTD) that requires excitation at both ports, one after another. In the code,
function createSimulation() is called twice, once for each port, to run these two excitations.
Only with both results we get the full 2x2 element S-matrix for Touchstone *.s2p export.

For the Python inductor models, all code (including technology setup and S1P export) is included in a single file.

# Python transmission line example
Model SG13_line_2port_TM2overM1_880um_PML.py represents an RFIC microstrip line simulated 
using two ports. The line is on TopMetal2 over Metal1 ground, line width w=15um for 50 Ohm. 

FDTD method excites one port at a time: excite port 1 to get S11 and S21, 
excite port 2 to get S22 and S12. In this model, function createSimulation() is called
twice, once for each port, to run these two excitations. Only with both results we get the 
full 2x2 element [S] matrix so that we can create an S2P output file.
For this transmission line, simulation results are compared to measurements. 
Measurement data for the line is obtained by de-embedding the pad sections from raw measurement.

# Metal model
Typical openEMS examples for PCB use flat conductors that are infinitely small for the 
actual field solver calculation. Losses are included by mapping a sheet resistance 
onto the thin conductor sheets, and skin effect loss is included there behind the scenes,

However, for SG13G2 we might have metal thickness on the order of trace width or 
gap width, so that simulation using flat conductors is not recommended. Instead, we use 
a general material model, which enables thick conductor materials in EM solution, The downside 
of doing so: these materials have no built-in skin effect loss correction, and we 
can only capture skin effect by sufficiently fine mesh resolution!

# Meshing
One important aspect of EM simulation is meshing: how to divide the analysis volume 
into small 3D boxes for the field solver. Reality is continuous, but in simulation we 
need to reduce complexity and use only a limited number of 3D boxes for solving the 
actual EM field equations. The finer the mesh, the closer we get to reality, but the 
price to pay is simulation time and memory requirement.

In this initial version, meshing in the layout region is homogeneous with a fixed 
mesh size defined by the user. This mesh size must be small enough to resolve relevant 
details such as line width and gap size, and it must also be small enough to capture 
skin effect inside conductors.

Meshing in vertical direction is preset and does not depend on the actual geometry 
defined by the user, so you should leave this unchanged, unless you know exactly what you are doing.

IMPORTANT: FDTD simulation speed depends on mesh size. The smallest mesh cell in the model 
will determine the time step for FDTD calculation, so you can dramatically slow down 
simulation if there is any small mesh dimension anywhere. Make the mesh fine enough to 
capture geometry details and skin effect loss, but no finer than necessary!

# Boundaries

In many cases, the simulation model includes a margin (empty area) between layout 
and simulation model boundaries. The mesh in that empty region is created automatically 
in the example code (fixed oversize factor relative to drawn objects) 
with less mesh density than the active layout region.
