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

# Command script for generating cell diodevdd_2kv

suspendall
tech unlock *
snap internal
load diodevdd_2kv -silent
box values 0 0 0 0
box values 312 312 1638 7098
paint nwell
box values 58 7198 1886 7346
paint pwell
box values 58 212 206 7198
paint pwell
box values 1738 212 1886 7198
paint pwell
box values 58 64 1886 212
paint pwell
box values 846 6482 1098 6502
paint pdiff
box values 846 978 888 6482
paint pdiff
box values 1064 978 1098 6482
paint pdiff
box values 846 946 1098 978
paint pdiff
box values 888 978 1064 6482
paint pdiffc
box values 84 7288 1860 7320
paint psubdiff
box values 84 7256 128 7288
paint psubdiff
box values 1816 7256 1860 7288
paint psubdiff
box values 84 7224 1860 7256
paint psubdiff
box values 84 7173 180 7224
paint psubdiff
box values 84 229 116 7173
paint psubdiff
box values 148 229 180 7173
paint psubdiff
box values 1764 7173 1860 7224
paint psubdiff
box values 84 186 180 229
paint psubdiff
box values 1764 229 1796 7173
paint psubdiff
box values 1828 229 1860 7173
paint psubdiff
box values 1764 186 1860 229
paint psubdiff
box values 84 154 1860 186
paint psubdiff
box values 84 122 128 154
paint psubdiff
box values 1816 122 1860 154
paint psubdiff
box values 84 90 1860 122
paint psubdiff
box values 396 6980 1554 7014
paint nsubdiff
box values 396 6804 411 6980
paint nsubdiff
box values 1523 6804 1554 6980
paint nsubdiff
box values 396 6762 1554 6804
paint nsubdiff
box values 396 6761 648 6762
paint nsubdiff
box values 396 681 433 6761
paint nsubdiff
box values 609 681 648 6761
paint nsubdiff
box values 1302 6761 1554 6762
paint nsubdiff
box values 396 648 648 681
paint nsubdiff
box values 1302 681 1339 6761
paint nsubdiff
box values 1515 681 1554 6761
paint nsubdiff
box values 1302 648 1554 681
paint nsubdiff
box values 396 614 1554 648
paint nsubdiff
box values 396 438 411 614
paint nsubdiff
box values 1523 438 1554 614
paint nsubdiff
box values 396 396 1554 438
paint nsubdiff
box values 128 7256 1816 7288
paint psubdiffcont
box values 116 229 148 7173
paint psubdiffcont
box values 1796 229 1828 7173
paint psubdiffcont
box values 128 122 1816 154
paint psubdiffcont
box values 411 6804 1523 6980
paint nsubdiffcont
box values 433 681 609 6761
paint nsubdiffcont
box values 1339 681 1515 6761
paint nsubdiffcont
box values 411 438 1523 614
paint nsubdiffcont
box values 0 7288 1944 7410
paint metal1
box values 0 7256 128 7288
paint metal1
box values 1816 7256 1944 7288
paint metal1
box values 0 7173 1944 7256
paint metal1
box values 0 229 116 7173
paint metal1
box values 148 7140 1796 7173
paint metal1
box values 148 270 270 7140
paint metal1
box values 366 6980 1584 7032
paint metal1
box values 366 6804 411 6980
paint metal1
box values 1523 6804 1584 6980
paint metal1
box values 366 6761 1584 6804
paint metal1
box values 366 6667 433 6761
paint metal1
box values 609 6750 1339 6761
paint metal1
box values 609 6667 672 6750
paint metal1
box values 366 6147 397 6667
paint metal1
box values 629 6147 672 6667
paint metal1
box values 1272 6667 1339 6750
paint metal1
box values 1515 6667 1584 6761
paint metal1
box values 366 4867 433 6147
paint metal1
box values 609 4867 672 6147
paint metal1
box values 366 4347 397 4867
paint metal1
box values 629 4347 672 4867
paint metal1
box values 366 3067 433 4347
paint metal1
box values 609 3067 672 4347
paint metal1
box values 366 2547 397 3067
paint metal1
box values 629 2547 672 3067
paint metal1
box values 366 1267 433 2547
paint metal1
box values 609 1267 672 2547
paint metal1
box values 366 747 397 1267
paint metal1
box values 629 747 672 1267
paint metal1
box values 792 6482 1152 6556
paint metal1
box values 792 5863 888 6482
paint metal1
box values 1064 5863 1152 6482
paint metal1
box values 792 5151 860 5863
paint metal1
box values 1092 5151 1152 5863
paint metal1
box values 792 4063 888 5151
paint metal1
box values 1064 4063 1152 5151
paint metal1
box values 792 3351 860 4063
paint metal1
box values 1092 3351 1152 4063
paint metal1
box values 792 2263 888 3351
paint metal1
box values 1064 2263 1152 3351
paint metal1
box values 792 1551 860 2263
paint metal1
box values 1092 1551 1152 2263
paint metal1
box values 792 978 888 1551
paint metal1
box values 1064 978 1152 1551
paint metal1
box values 792 886 1152 978
paint metal1
box values 1272 6147 1309 6667
paint metal1
box values 1541 6147 1584 6667
paint metal1
box values 1272 4867 1339 6147
paint metal1
box values 1515 4867 1584 6147
paint metal1
box values 1272 4347 1309 4867
paint metal1
box values 1541 4347 1584 4867
paint metal1
box values 1272 3067 1339 4347
paint metal1
box values 1515 3067 1584 4347
paint metal1
box values 1272 2547 1309 3067
paint metal1
box values 1541 2547 1584 3067
paint metal1
box values 1272 1267 1339 2547
paint metal1
box values 1515 1267 1584 2547
paint metal1
box values 366 681 433 747
paint metal1
box values 609 681 672 747
paint metal1
box values 366 660 672 681
paint metal1
box values 1272 747 1309 1267
paint metal1
box values 1541 747 1584 1267
paint metal1
box values 1272 681 1339 747
paint metal1
box values 1515 681 1584 747
paint metal1
box values 1272 660 1584 681
paint metal1
box values 366 614 1584 660
paint metal1
box values 366 438 411 614
paint metal1
box values 1523 438 1584 614
paint metal1
box values 366 378 1584 438
paint metal1
box values 1680 270 1796 7140
paint metal1
box values 148 229 1796 270
paint metal1
box values 1828 229 1944 7173
paint metal1
box values 0 154 1944 229
paint metal1
box values 0 122 128 154
paint metal1
box values 1816 122 1944 154
paint metal1
box values 0 0 1944 122
paint metal1
box values 397 6147 433 6667
paint via1
box values 433 6147 609 6667
paint nsc+v
box values 609 6147 629 6667
paint via1
box values 397 4347 433 4867
paint via1
box values 433 4347 609 4867
paint nsc+v
box values 609 4347 629 4867
paint via1
box values 397 2547 433 3067
paint via1
box values 433 2547 609 3067
paint nsc+v
box values 609 2547 629 3067
paint via1
box values 397 747 433 1267
paint via1
box values 433 747 609 1267
paint nsc+v
box values 609 747 629 1267
paint via1
box values 860 5151 888 5863
paint via1
box values 888 5151 1064 5863
paint pdc+v
box values 1064 5151 1092 5863
paint via1
box values 860 3351 888 4063
paint via1
box values 888 3351 1064 4063
paint pdc+v
box values 1064 3351 1092 4063
paint via1
box values 860 1551 888 2263
paint via1
box values 888 1551 1064 2263
paint pdc+v
box values 1064 1551 1092 2263
paint via1
box values 1309 6147 1339 6667
paint via1
box values 1339 6147 1515 6667
paint nsc+v
box values 1515 6147 1541 6667
paint via1
box values 1309 4347 1339 4867
paint via1
box values 1339 4347 1515 4867
paint nsc+v
box values 1515 4347 1541 4867
paint via1
box values 1309 2547 1339 3067
paint via1
box values 1339 2547 1515 3067
paint nsc+v
box values 1515 2547 1541 3067
paint via1
box values 1309 747 1339 1267
paint via1
box values 1339 747 1515 1267
paint nsc+v
box values 1515 747 1541 1267
paint via1
box values 388 6147 397 6667
paint metal2
box values 629 6147 1309 6667
paint metal2
box values 1541 6147 2188 6667
paint metal2
box values -424 5151 860 5863
paint metal2
box values 1092 5151 1101 5863
paint metal2
box values -424 4063 296 5151
paint metal2
box values 1468 4867 2188 6147
paint metal2
box values 388 4347 397 4867
paint metal2
box values 629 4347 1309 4867
paint metal2
box values 1541 4347 2188 4867
paint metal2
box values -424 3351 860 4063
paint metal2
box values 1092 3351 1101 4063
paint metal2
box values -424 2263 296 3351
paint metal2
box values 1468 3067 2188 4347
paint metal2
box values 388 2547 397 3067
paint metal2
box values 629 2547 1309 3067
paint metal2
box values 1541 2547 2188 3067
paint metal2
box values -424 1551 860 2263
paint metal2
box values 1092 1551 1101 2263
paint metal2
box values 1468 1267 2188 2547
paint metal2
box values 388 747 397 1267
paint metal2
box values 629 747 1309 1267
paint metal2
box values 1541 747 2188 1267
paint metal2
box values 1830 3798 1830 3798
label VDD FreeSans 500 90 0 0 c comment
select area label
setlabel sticky true
box values -64 3707 -64 3707
label PAD FreeSans 500 90 0 0 c comment
select area label
setlabel sticky true
box values 972 135 972 135
label VSS FreeSans 200 0 0 0 c comment
select area label
setlabel sticky true
box values 1666 125 1666 125
label sub! FreeSans 200 0 0 0 c comment
select area label
setlabel sticky true
box values 1260 3686 1260 3686
label diodevdd_2kv FreeSans 600 90 0 0 c comment
select area label
setlabel sticky true
select clear
view
tech revert
resumeall
