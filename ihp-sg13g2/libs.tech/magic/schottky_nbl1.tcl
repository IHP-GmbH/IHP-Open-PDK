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

# Command script for generating cell schottky_nbl1

suspendall
tech unlock *
snap internal
load schottky_nbl1 -silent
box values 0 0 0 0
box values -110 -84 350 464
paint dnwell
box values -234 -204 474 584
paint nwell
box values -486 698 726 810
paint pwell
box values -486 -390 -374 698
paint pwell
box values 614 -390 726 698
paint pwell
box values -486 -502 726 -390
paint pwell
box values -460 724 700 784
paint hvpsubdiff
box values -460 706 -400 724
paint hvpsubdiff
box values -460 -398 -446 706
paint hvpsubdiff
box values -414 -398 -400 706
paint hvpsubdiff
box values 640 706 700 724
paint hvpsubdiff
box values -460 -416 -400 -398
paint hvpsubdiff
box values 640 -398 654 706
paint hvpsubdiff
box values 686 -398 700 706
paint hvpsubdiff
box values 640 -416 700 -398
paint hvpsubdiff
box values -460 -476 700 -416
paint hvpsubdiff
box values -110 442 350 460
paint hvnsubdiff
box values -110 -62 -90 442
paint hvnsubdiff
box values -58 380 298 442
paint hvnsubdiff
box values -58 0 0 380
paint hvnsubdiff
box values 240 0 298 380
paint hvnsubdiff
box values -58 -62 298 0
paint hvnsubdiff
box values 330 -62 350 442
paint hvnsubdiff
box values -110 -80 350 -62
paint hvnsubdiff
box values -446 -398 -414 706
paint hvpsubdiffcont
box values 654 -398 686 706
paint hvpsubdiffcont
box values -90 -62 -58 442
paint hvnsubdiffcont
box values 298 -62 330 442
paint hvnsubdiffcont
box values 0 290 240 380
paint schottky
box values 0 90 90 290
paint schottky
box values 150 90 240 290
paint schottky
box values 0 0 240 90
paint schottky
box values 90 90 150 290
paint schottkycont
box values -460 706 -400 724
paint metal1
box values -460 -398 -446 706
paint metal1
box values -414 -398 -400 706
paint metal1
box values 640 706 700 724
paint metal1
box values -110 460 350 671
paint metal1
box values -110 442 -46 460
paint metal1
box values -110 -62 -90 442
paint metal1
box values -58 -62 -46 442
paint metal1
box values 286 442 350 460
paint metal1
box values 50 295 190 304
paint metal1
box values 50 255 59 295
paint metal1
box values 181 255 190 295
paint metal1
box values 50 210 90 255
paint metal1
box values 150 210 190 255
paint metal1
box values 50 170 59 210
paint metal1
box values 181 170 190 210
paint metal1
box values 50 125 90 170
paint metal1
box values 150 125 190 170
paint metal1
box values 50 85 59 125
paint metal1
box values 181 85 190 125
paint metal1
box values 50 76 190 85
paint metal1
box values -110 -80 -46 -62
paint metal1
box values 286 -62 298 442
paint metal1
box values 330 -62 350 442
paint metal1
box values 286 -80 350 -62
paint metal1
box values -460 -416 -400 -398
paint metal1
box values 640 -398 654 706
paint metal1
box values 686 -398 700 706
paint metal1
box values 640 -416 700 -398
paint metal1
box values 59 290 181 295
paint via1
box values 59 255 90 290
paint via1
box values 90 255 150 290
paint sdic+v
box values 150 255 181 290
paint via1
box values 59 170 90 210
paint via1
box values 90 170 150 210
paint sdic+v
box values 150 170 181 210
paint via1
box values 59 90 90 125
paint via1
box values 90 90 150 125
paint sdic+v
box values 150 90 181 125
paint via1
box values 59 85 181 90
paint via1
box values 59 295 181 401
paint metal2
box values 59 210 181 255
paint metal2
box values 59 125 181 170
paint metal2
box values 59 -139 181 85
paint metal2
box values -116 -363 356 -139
paint metal2
box values 3 -118 3 -118
label schottky_nbl1 FreeSans 70 0 0 0 c comment
select area label
setlabel sticky true
box values 120 -251 120 -251
label PLUS FreeSans 140 0 0 0 c metal2
select area label
setlabel sticky true
box values 670 154 670 154
label TIE FreeSans 37 0 0 0 c hvpsubdiffcont
select area label
setlabel sticky true
box values -430 154 -430 154
label TIE FreeSans 37 0 0 0 c hvpsubdiffcont
select area label
setlabel sticky true
box values 120 565 120 565
label MINUS FreeSans 131 0 0 0 c metal1
select area label
setlabel sticky true
# Note: Use mask hint for pblock to avoid DRC errors.
# PWELLBLK will be generated automatically.
property MASKHINTS_PWELLBLK "-326 -368 566 -130 -326 -130 -160 510 400 -130 566 510 -326 510 566 670"
select clear
view
tech revert
resumeall
