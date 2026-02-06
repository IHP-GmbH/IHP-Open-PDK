########################################################################
#
# Copyright 2025 IHP PDK Authors
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

# Command script for generating cell scr1

suspendall
tech unlock *
snap internal
load scr1 -silent
box values 0 0 0 0
box values -1524 -466 1524 5466
paint dnwell
box values -1532 5174 1532 5474
paint nwell
box values -1532 -174 -1232 5174
paint nwell
box values -110 -174 110 5174
paint nwell
box values 1232 -174 1532 5174
paint nwell
box values -1532 -474 1532 -174
paint nwell
box values -1084 -26 -110 5026
paint pwell
box values 110 -26 1084 5026
paint pwell
box values -276 0 -210 5000
paint hvnmosesd
box values 210 0 276 5000
paint hvnmosesd
box values -686 4942 -476 5000
paint hvndiff
box values -686 58 -640 4942
paint hvndiff
box values -540 58 -476 4942
paint hvndiff
box values -686 0 -476 58
paint hvndiff
box values 476 4942 686 5000
paint hvndiff
box values 476 58 540 4942
paint hvndiff
box values 640 58 686 4942
paint hvndiff
box values 476 0 686 58
paint hvndiff
box values -640 58 -540 4942
paint hvndiffc
box values 540 58 640 4942
paint hvndiffc
box values -1058 4942 -876 5000
paint hvpsubdiff
box values -1058 58 -1024 4942
paint hvpsubdiff
box values -924 58 -876 4942
paint hvpsubdiff
box values -1058 0 -876 58
paint hvpsubdiff
box values 876 4942 1058 5000
paint hvpsubdiff
box values 876 58 924 4942
paint hvpsubdiff
box values 1024 58 1058 4942
paint hvpsubdiff
box values 876 0 1058 58
paint hvpsubdiff
box values -110 0 110 5000
paint hvnsubdiff
box values -1024 58 -924 4942
paint hvpsubdiffcont
box values 924 58 1024 4942
paint hvpsubdiffcont
box values -370 5210 -124 5224
paint poly
box values -370 5110 -354 5210
paint poly
box values -140 5110 -124 5210
paint poly
box values -370 5096 -124 5110
paint poly
box values 124 5210 370 5224
paint poly
box values 124 5110 140 5210
paint poly
box values 354 5110 370 5210
paint poly
box values 124 5096 370 5110
paint poly
box values -276 5000 -210 5096
paint poly
box values 210 5000 276 5096
paint poly
box values -276 -96 -210 0
paint poly
box values 210 -96 276 0
paint poly
box values -370 -110 -124 -96
paint poly
box values -370 -210 -354 -110
paint poly
box values -140 -210 -124 -110
paint poly
box values -370 -224 -124 -210
paint poly
box values 124 -110 370 -96
paint poly
box values 124 -210 140 -110
paint poly
box values 354 -210 370 -110
paint poly
box values 124 -224 370 -210
paint poly
box values -354 5110 -140 5210
paint polycont
box values 140 5110 354 5210
paint polycont
box values -354 -210 -140 -110
paint polycont
box values 140 -210 354 -110
paint polycont
box values -476 0 -276 5000
paint hvndiffres
box values -210 0 -110 5000
paint hvndiffres
box values 110 0 210 5000
paint hvndiffres
box values 276 0 476 5000
paint hvndiffres
box values -876 0 -686 5000
paint hvisodiffres
box values 686 0 876 5000
paint hvisodiffres
box values -660 5110 -354 5210
paint metal1
box values -140 5110 -130 5210
paint metal1
box values 130 5110 140 5210
paint metal1
box values 354 5110 660 5210
paint metal1
box values -660 4962 -520 5110
paint metal1
box values -1532 4943 -520 4962
paint metal1
box values -1532 3989 -1513 4943
paint metal1
box values -559 4942 -520 4943
paint metal1
box values -1532 58 -1024 3989
paint metal1
box values -924 58 -640 3989
paint metal1
box values -540 58 -520 4942
paint metal1
box values -1532 38 -520 58
paint metal1
box values -660 -110 -520 38
paint metal1
box values 520 4962 660 5110
paint metal1
box values 520 4942 1532 4962
paint metal1
box values 520 58 540 4942
paint metal1
box values 640 1011 924 4942
paint metal1
box values 1024 1011 1532 4942
paint metal1
box values 520 57 559 58
paint metal1
box values 1513 57 1532 1011
paint metal1
box values 520 38 1532 57
paint metal1
box values 520 -110 660 38
paint metal1
box values -660 -210 -354 -110
paint metal1
box values -140 -210 -130 -110
paint metal1
box values 130 -210 140 -110
paint metal1
box values 354 -210 660 -110
paint metal1
box values -1513 4942 -559 4943
paint via1
box values -1513 3989 -1024 4942
paint via1
box values -1024 3989 -924 4942
paint hvpsc+v
box values -924 3989 -640 4942
paint via1
box values -640 3989 -559 4942
paint hvndc+v
box values 559 58 640 1011
paint hvndc+v
box values 640 58 924 1011
paint via1
box values 924 58 1024 1011
paint hvpsc+v
box values 1024 58 1513 1011
paint via1
box values 559 57 1513 58
paint via1
box values -1532 4943 -540 4962
paint metal2
box values -1532 3989 -1513 4943
paint metal2
box values -559 3989 -540 4943
paint metal2
box values -1532 3970 -540 3989
paint metal2
box values 540 1011 1532 1030
paint metal2
box values 540 57 559 1011
paint metal2
box values 1513 57 1532 1011
paint metal2
box values 540 38 1532 57
paint metal2
box values -1513 3989 -559 4943
paint v+v2
box values 559 57 1513 1011
paint v+v2
box values -1532 4943 -540 4962
paint metal3
box values -1532 3989 -1513 4943
paint metal3
box values -559 3989 -540 4943
paint metal3
box values -1532 3970 -540 3989
paint metal3
box values 540 1011 1532 1030
paint metal3
box values 540 57 559 1011
paint metal3
box values 1513 57 1532 1011
paint metal3
box values 540 38 1532 57
paint metal3
box values 1036 534 1036 534
label B FreeSans 1000 0 0 0 c space
select area label
setlabel sticky true
box values -1036 4466 -1036 4466
label A FreeSans 1000 0 0 0 c space
select area label
setlabel sticky true
box values -1470 -418 -1470 -418
label scr1 FreeSans 500 0 0 0 ne space
select area label
setlabel sticky true
select clear
view
tech revert
resumeall
