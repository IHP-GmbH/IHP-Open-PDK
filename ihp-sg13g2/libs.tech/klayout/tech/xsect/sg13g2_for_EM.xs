# Copyright 2024 IHP PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Cross section file for KLayout xsection tool
# Version 7-August-2024: updated to support MIM
#
# Limitations:
# - No support for active devices (layers below ACTIV)


# Prepare input layers
mask_ACTIV = layer("1/0")
mask_METAL1    = layer("8/0")
mask_METAL2    = layer("10/0")
mask_METAL3    = layer("30/0")
mask_METAL4    = layer("50/0")
mask_METAL5    = layer("67/0")
mask_MIM   = layer("36/0")
mask_TM1   = layer("126/0")
mask_TM2   = layer("134/0")

mask_CONT  = layer("6/0")
mask_VIA1  = layer("19/0")
mask_VIA2  = layer("29/0")
mask_VIA3  = layer("49/0")
mask_VIA4  = layer("66/0")
mask_VMIM  = layer("129/0")
mask_TOPVIA1  = layer("125/0")
mask_TOPVIA2  = layer("133/0")

# height of processing windows above substrate
height(20)

# Process steps:
# Now we move to cross section view: from the layout geometry we create
# a material stack by simulating the process step by step.
# The basic idea is that all activity happens at the surface. We can
# deposit material (over existing or at a mask), etch material and
# planarize.

# Start with the bulk material and assign that to material "substrate"
# "bulk" delivers the wafer's cross section.

substrate = bulk
z = 0

# TO DO: add EPI
# t_epi = 3.75
# epi = deposit(t_epi)
# z = z + t_epi


# ACTIV and CONT
t_activ = 0.4
t_cont  = 0.64
activ  = mask(mask_ACTIV).grow(t_activ)
cont  = mask(mask_CONT).grow(t_cont)
imd0 = deposit(t_activ+t_cont)
z = z + t_activ + t_cont
planarize(:to => z, :into => imd0)

# METAL1 and VIA1
t_metal1 = 0.42
t_via1   = 0.54
metal1   = mask(mask_METAL1).grow(t_metal1)
via1     = mask(mask_VIA1).grow(t_via1)
imd1 = deposit(t_metal1+t_via1)
z = z + t_metal1 + t_via1
planarize(:to => z, :into => imd1)

# METAL2 and VIA2
t_metal2 = 0.49
t_via2   = 0.54
metal2   = mask(mask_METAL2).grow(t_metal2)
via2     = mask(mask_VIA2).grow(t_via2)
imd2 = deposit(t_metal2+t_via2)
z = z + t_metal2 + t_via2
planarize(:to => z, :into => imd2)

# METAL3 and VIA3
t_metal3 = 0.49
t_via3   = 0.54
metal3   = mask(mask_METAL3).grow(t_metal3)
via3     = mask(mask_VIA3).grow(t_via3)
imd3 = deposit(t_metal3+t_via3)
z = z + t_metal3 + t_via3
planarize(:to => z, :into => imd3)

# METAL4 and VIA4
t_metal4 = 0.49
t_via4   = 0.54
metal4   = mask(mask_METAL4).grow(t_metal4)
via4     = mask(mask_VIA4).grow(t_via4)
imd4 = deposit(t_metal4+t_via4)
z = z + t_metal4 + t_via4
planarize(:to => z, :into => imd4)

# Metal5 and TopVia1
t_metal5  = 0.49
t_topvia1 = 0.85
metal5    = mask(mask_METAL5).grow(t_metal5)
topvia1   = mask(mask_TOPVIA1).grow(t_topvia1)

t_mimdiel = 0.04
mimdiel   = mask(mask_MIM).grow(t_mimdiel)
t_mim     = 0.15
mim       = mask(mask_MIM).grow(t_mim)

t_vmim    = t_topvia1-t_mim-t_mimdiel
vmim 	  = mask(mask_VMIM).grow(t_vmim)

imd5     = deposit(t_metal5+t_topvia1)
z = z + t_metal5 + t_topvia1
planarize(:to => z, :into => imd5)

# TopMetal1 and TopVia2
t_tm1     = 2.0
t_topvia2 = 2.8
tm1       = mask(mask_TM1).grow(t_tm1)
topvia2   = mask(mask_TOPVIA2).grow(t_topvia2)
imd6 = deposit(t_tm1+t_topvia2)
z = z + t_tm1 + t_topvia2
planarize(:to => z, :into => imd6)


# TopMetal2
t_tm2 = 3
tm2   = mask(mask_TM2).grow(t_tm2)

# Passivation
t_passi1 = 1.5
t_passi2 = 0.4
passi1 = deposit(t_passi1, 0.6)
passi2 = deposit(t_passi2, 0.4)



output("300/0", substrate)
# output("301/0", epi)
output("302/0", imd0)
output("303/0", imd1)
output("304/0", imd2)
output("305/0", imd3)
output("306/0", imd4)
output("307/0", imd5)
output("308/0", imd6)
output("309/0", passi1)
output("310/0", passi2)
output("311/0", mimdiel)


output("400/0", activ)
output("401/0", metal1)
output("402/0", metal2)
output("403/0", metal3)
output("404/0", metal4)
output("405/0", metal5)
output("406/0", tm1)
output("407/0", tm2)
output("408/0", mim)

output("500/0", cont)
output("501/0", via1)
output("502/0", via2)
output("503/0", via3)
output("504/0", via4)
output("505/0", topvia1)
output("506/0", topvia2)
output("507/0", vmim)



