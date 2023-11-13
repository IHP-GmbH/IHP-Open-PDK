########################################################################
#
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
#
########################################################################

__version__ = "$Revision: #3 $"

from cni.dlo import *
from .geometry import *

def ihpAddThermalLayer(self, heatLayer, bbox, addThermalText, label):
    lw = bbox.lowerLeft()
    ur = bbox.upperRight();
    
    x1 = lw.getX();
    x2 = ur.getX();        
    y1 = lw.getY();
    y2 = ur.getY();
        
    pcInst = dbCreateRect(self, heatLayer, Box(x1, y1, x2, y2))
    
    if addThermalText:
        dbCreateLabel(self, heatLayer, Point((x1+x2)/2, (y1+y2)/2), label, 'centerCenter', 'R0', Font.EURO_STYLE, 0.001);
        
    return(pcInst)

def ihpAddThermalResLayer(self, bbox, addThermalText, label):
    return(ihpAddThermalLayer(self, Layer('HeatTrans'), bbox, addThermalText, label));

def ihpAddThermalMosLayer(self, bbox, addThermalText, label):
    return(ihpAddThermalLayer(self, Layer('HeatTrans'), bbox, addThermalText, label));


def ihpAddThermalBjtLayer(self, bbox, addThermalText, label):
    return(ihpAddThermalLayer(self, Layer('HeatTrans'), bbox, addThermalText, label));

