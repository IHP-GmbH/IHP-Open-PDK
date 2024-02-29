# Copyright 2023 IHP PDK Authors
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Extract objects on *all* IHP layers in GDSII file
# Write result to polygon list for OpenEMS in Python syntax
# Usage: gds2pythonpoly <input.gds> 

# File history: 
# Initial version 14 April 2022 Volker Muehlhaus 

import gdspy
import sys
from pathlib import Path

# ============= utilities ==========

def float2string (value):
  return "{:.3f}".format(value)    # fixed 3 decimal digits


# ============= technology specific stuff ===============
# list of layers to evaluate
layerlist = [
8,
10,
30,
50,
67,
126,
134,
19,
29,
49,
66,
125,
133
]

# list of purpose to evaluate
purposelist = [
0
]

# list of materialnames for each GDSII layer number
layermapping = {
"8":"Metal1",
"10":"Metal2",
"30":"Metal3",
"50":"Metal4",
"67":"Metal5",
"126":"TopMetal1",
"134":"TopMetal2",
"19":"Via1",
"29":"Via2",
"49":"Via3",
"66":"Via4",
"125":"TopVia1",
"133":"TopVia2"
}

# get layername/materialname from GDSII layer number 
def layernum2layername (num):
  layername = layermapping.get(str(num),"unknown")
  return layername

# ============= main ===============

if len(sys.argv) >= 2:
  input_name = sys.argv[1]
  print ("Input file: ", input_name)

    # get basename of input file, append suffix to identify output polygons
  output_name = Path(input_name).stem + "_polygons.py"
  output_file = open(output_name, 'w')
    
  input_library = gdspy.GdsLibrary(infile=input_name)


  # evaluate only first top level cell
  toplevel_cell_list = input_library.top_level()
  cell = toplevel_cell_list[0]
  
  #  write top level cell information into comment 
  output_file.write("# " + str(cell) + '\n\n')
  
  # initialize values for bounding box calculation
  xmin=10000
  ymin=10000
  xmax=-10000
  ymax=-10000
    
  # iterate over IHP technology layers
  for layer_to_extract in layerlist:
    
    print ("Evaluating layer ", str(layer_to_extract))
    # flatten hierarchy below this cell
    cell.flatten(single_layer=None, single_datatype=None, single_texttype=None)
    
    # get layers used in cell
    used_layers = cell.get_layers()
    
    # check if layer-to-extract is used in cell 
    if (layer_to_extract in used_layers):
            
      # iterate over layer-purpose pairs (by_spec=true)
      # do not descend into cell references (depth=0)
      LPPpolylist = cell.get_polygons(by_spec=True, depth=0)
      for LPP in LPPpolylist:
        layer = LPP[0]
        purpose = LPP[1]
        
        # now get polygons for this one layer-purpose-pair
        if (layer==layer_to_extract) and (purpose in purposelist):
          layername = layernum2layername(layer)
          layerpolygons = LPPpolylist[(layer, purpose)]
          
          # iterate over layer polygons
          for polypoints in layerpolygons:

            # write to output
            numvertices = int(polypoints.size/polypoints.ndim)
            print('  Number of polygon points: ' + str(numvertices))

            output_file.write('pts_x = np.array([])\n')
            output_file.write('pts_y = np.array([])\n')
            
            # define vertices
            for vertex in range(numvertices):
              x = polypoints[vertex,0]
              y = polypoints[vertex,1]
              
              print('  x= ' + float2string(x) + ' y= ' + float2string(y))
              
              output_file.write('pts_x = r_[pts_x, ' + float2string(x)+ ']\n')
              output_file.write('pts_y = r_[pts_y, ' + float2string(y)+ ']\n')
              
              # update bounding box information
              if x<xmin: xmin=x
              if x>xmax: xmax=x
              if y<ymin: ymin=y
              if y>ymax: ymax=y
            
            # create polygon with vertics written before
            output_file.write('pts = np.array([pts_x, pts_y])\n')
            txt = "{layername}.AddLinPoly(priority=200, points=pts, norm_dir ='z', elevation={layername}_zmin, length={layername}_thick)\n\n"
            output_file.write(txt.format(layername=layername))

  # write bounding box information
  output_file.write('# Bounding box of geometry\n')
  output_file.write('geometry_xmin= ' + float2string(xmin) + '\n')
  output_file.write('geometry_xmax= ' + float2string(xmax) + '\n')
  output_file.write('geometry_ymin= ' + float2string(ymin) + '\n')
  output_file.write('geometry_ymax= ' + float2string(ymax) + '\n\n')

      
  # done writing output  
  output_file.close()

else:
  print ("Usage: gds2pythonpoly <input.gds> ")

  
  
