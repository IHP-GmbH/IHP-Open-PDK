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

# Command script for generating cell diodevss_2kv

suspendall
tech unlock *
snap internal
load diodevss_2kv -silent
box values 0 0 0 0
box values 0 7140 1944 7410
paint nwell
box values 0 270 270 7140
paint nwell
box values 1680 270 1944 7140
paint nwell
box values 0 0 1944 270
paint nwell
box values 370 6736 1580 7040
paint pwell
box values 370 6528 674 6736
paint pwell
box values 1276 6528 1580 6736
paint pwell
box values 370 920 1580 6528
paint pwell
box values 370 674 674 920
paint pwell
box values 1276 674 1580 920
paint pwell
box values 370 370 1580 674
paint pwell
box values 846 6482 1098 6502
paint ndiff
box values 846 978 888 6482
paint ndiff
box values 1064 978 1098 6482
paint ndiff
box values 846 946 1098 978
paint ndiff
box values 888 978 1064 6482
paint ndiffc
box values 396 6980 1554 7014
paint psubdiff
box values 396 6804 411 6980
paint psubdiff
box values 1523 6804 1554 6980
paint psubdiff
box values 396 6762 1554 6804
paint psubdiff
box values 396 6761 648 6762
paint psubdiff
box values 396 681 433 6761
paint psubdiff
box values 609 681 648 6761
paint psubdiff
box values 1302 6761 1554 6762
paint psubdiff
box values 396 648 648 681
paint psubdiff
box values 1302 681 1339 6761
paint psubdiff
box values 1515 681 1554 6761
paint psubdiff
box values 1302 648 1554 681
paint psubdiff
box values 396 614 1554 648
paint psubdiff
box values 396 438 411 614
paint psubdiff
box values 1523 438 1554 614
paint psubdiff
box values 396 396 1554 438
paint psubdiff
box values 84 7288 1860 7320
paint nsubdiff
box values 84 7256 128 7288
paint nsubdiff
box values 1816 7256 1860 7288
paint nsubdiff
box values 84 7224 1860 7256
paint nsubdiff
box values 84 7173 180 7224
paint nsubdiff
box values 84 229 116 7173
paint nsubdiff
box values 148 229 180 7173
paint nsubdiff
box values 1764 7173 1860 7224
paint nsubdiff
box values 84 186 180 229
paint nsubdiff
box values 1764 229 1796 7173
paint nsubdiff
box values 1828 229 1860 7173
paint nsubdiff
box values 1764 186 1860 229
paint nsubdiff
box values 84 154 1860 186
paint nsubdiff
box values 84 122 128 154
paint nsubdiff
box values 1816 122 1860 154
paint nsubdiff
box values 84 90 1860 122
paint nsubdiff
box values 411 6804 1523 6980
paint psubdiffcont
box values 433 681 609 6761
paint psubdiffcont
box values 1339 681 1515 6761
paint psubdiffcont
box values 411 438 1523 614
paint psubdiffcont
box values 128 7256 1816 7288
paint nsubdiffcont
box values 116 229 148 7173
paint nsubdiffcont
box values 1796 229 1828 7173
paint nsubdiffcont
box values 128 122 1816 154
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
box values 366 6665 433 6761
paint metal1
box values 609 6750 1339 6761
paint metal1
box values 609 6665 672 6750
paint metal1
box values 366 6145 405 6665
paint metal1
box values 637 6145 672 6665
paint metal1
box values 1272 6665 1339 6750
paint metal1
box values 1515 6665 1584 6761
paint metal1
box values 366 4865 433 6145
paint metal1
box values 609 4865 672 6145
paint metal1
box values 366 4345 405 4865
paint metal1
box values 637 4345 672 4865
paint metal1
box values 366 3065 433 4345
paint metal1
box values 609 3065 672 4345
paint metal1
box values 366 2545 405 3065
paint metal1
box values 637 2545 672 3065
paint metal1
box values 366 1265 433 2545
paint metal1
box values 609 1265 672 2545
paint metal1
box values 366 745 405 1265
paint metal1
box values 637 745 672 1265
paint metal1
box values 822 6482 1128 6556
paint metal1
box values 822 5860 888 6482
paint metal1
box values 1064 5860 1128 6482
paint metal1
box values 822 5148 856 5860
paint metal1
box values 1088 5148 1128 5860
paint metal1
box values 822 4060 888 5148
paint metal1
box values 1064 4060 1128 5148
paint metal1
box values 822 3348 856 4060
paint metal1
box values 1088 3348 1128 4060
paint metal1
box values 822 2260 888 3348
paint metal1
box values 1064 2260 1128 3348
paint metal1
box values 822 1548 856 2260
paint metal1
box values 1088 1548 1128 2260
paint metal1
box values 822 978 888 1548
paint metal1
box values 1064 978 1128 1548
paint metal1
box values 822 886 1128 978
paint metal1
box values 1272 6145 1317 6665
paint metal1
box values 1549 6145 1584 6665
paint metal1
box values 1272 4865 1339 6145
paint metal1
box values 1515 4865 1584 6145
paint metal1
box values 1272 4345 1316 4865
paint metal1
box values 1549 4825 1584 4865
paint metal1
box values 1548 4769 1584 4825
paint metal1
box values 1549 4729 1584 4769
paint metal1
box values 1548 4673 1584 4729
paint metal1
box values 1549 4633 1584 4673
paint metal1
box values 1548 4577 1584 4633
paint metal1
box values 1549 4537 1584 4577
paint metal1
box values 1548 4481 1584 4537
paint metal1
box values 1549 4441 1584 4481
paint metal1
box values 1548 4385 1584 4441
paint metal1
box values 1549 4345 1584 4385
paint metal1
box values 1272 3065 1339 4345
paint metal1
box values 1515 3065 1584 4345
paint metal1
box values 1272 2545 1317 3065
paint metal1
box values 1549 2545 1584 3065
paint metal1
box values 1272 1265 1339 2545
paint metal1
box values 1515 1265 1584 2545
paint metal1
box values 366 681 433 745
paint metal1
box values 609 681 672 745
paint metal1
box values 366 660 672 681
paint metal1
box values 1272 745 1317 1265
paint metal1
box values 1549 745 1584 1265
paint metal1
box values 1272 681 1339 745
paint metal1
box values 1515 681 1584 745
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
box values 405 6145 433 6665
paint via1
box values 433 6145 609 6665
paint psc+v
box values 609 6145 637 6665
paint via1
box values 405 4345 433 4865
paint via1
box values 433 4345 609 4865
paint psc+v
box values 609 4345 637 4865
paint via1
box values 405 2545 433 3065
paint via1
box values 433 2545 609 3065
paint psc+v
box values 609 2545 637 3065
paint via1
box values 405 745 433 1265
paint via1
box values 433 745 609 1265
paint psc+v
box values 609 745 637 1265
paint via1
box values 856 5148 888 5860
paint via1
box values 888 5148 1064 5860
paint ndc+v
box values 1064 5148 1088 5860
paint via1
box values 856 3348 888 4060
paint via1
box values 888 3348 1064 4060
paint ndc+v
box values 1064 3348 1088 4060
paint via1
box values 856 1548 888 2260
paint via1
box values 888 1548 1064 2260
paint ndc+v
box values 1064 1548 1088 2260
paint via1
box values 1317 6145 1339 6665
paint via1
box values 1339 6145 1515 6665
paint psc+v
box values 1515 6145 1549 6665
paint via1
box values 1316 4345 1339 4865
paint via1
box values 1339 4345 1515 4865
paint psc+v
box values 1515 4825 1549 4865
paint via1
box values 1515 4769 1548 4825
paint via1
box values 1515 4729 1549 4769
paint via1
box values 1515 4673 1548 4729
paint via1
box values 1515 4633 1549 4673
paint via1
box values 1515 4577 1548 4633
paint via1
box values 1515 4537 1549 4577
paint via1
box values 1515 4481 1548 4537
paint via1
box values 1515 4441 1549 4481
paint via1
box values 1515 4385 1548 4441
paint via1
box values 1515 4345 1549 4385
paint via1
box values 1317 2545 1339 3065
paint via1
box values 1339 2545 1515 3065
paint psc+v
box values 1515 2545 1549 3065
paint via1
box values 1317 745 1339 1265
paint via1
box values 1339 745 1515 1265
paint psc+v
box values 1515 745 1549 1265
paint via1
box values 396 6145 405 6665
paint metal2
box values 637 6145 1317 6665
paint metal2
box values 1549 6145 2196 6665
paint metal2
box values -416 5860 1097 5861
paint metal2
box values -416 5149 856 5860
paint metal2
box values -416 4061 304 5149
paint metal2
box values 847 5148 856 5149
paint metal2
box values 1088 5148 1097 5860
paint metal2
box values 1476 4865 2196 6145
paint metal2
box values 396 4345 405 4865
paint metal2
box values 637 4345 1316 4865
paint metal2
box values 1549 4825 2196 4865
paint metal2
box values 1548 4769 2196 4825
paint metal2
box values 1549 4729 2196 4769
paint metal2
box values 1548 4673 2196 4729
paint metal2
box values 1549 4633 2196 4673
paint metal2
box values 1548 4577 2196 4633
paint metal2
box values 1549 4537 2196 4577
paint metal2
box values 1548 4481 2196 4537
paint metal2
box values 1549 4441 2196 4481
paint metal2
box values 1548 4385 2196 4441
paint metal2
box values 1549 4345 2196 4385
paint metal2
box values -416 4060 1097 4061
paint metal2
box values -416 3349 856 4060
paint metal2
box values -416 2261 304 3349
paint metal2
box values 847 3348 856 3349
paint metal2
box values 1088 3348 1097 4060
paint metal2
box values 1476 3065 2196 4345
paint metal2
box values 396 2545 405 3065
paint metal2
box values 637 2545 1317 3065
paint metal2
box values 1549 2545 2196 3065
paint metal2
box values -416 2260 1097 2261
paint metal2
box values -416 1549 856 2260
paint metal2
box values 847 1548 856 1549
paint metal2
box values 1088 1548 1097 2260
paint metal2
box values 1476 1265 2196 2545
paint metal2
box values 396 745 405 1265
paint metal2
box values 637 745 1317 1265
paint metal2
box values 1549 745 2196 1265
paint metal2
box values -56 3705 -56 3705
label PAD FreeSans 500 90 0 0 c comment
select area label
setlabel sticky true
box values 1836 3705 1836 3705
label VSS FreeSans 500 90 0 0 c comment
select area label
setlabel sticky true
box values 972 7275 972 7275
label VDD FreeSans 200 0 0 0 c comment
select area label
setlabel sticky true
box values 657 477 657 477
label sub! FreeSans 200 0 0 0 c comment
select area label
setlabel sticky true
box values 1260 3686 1260 3686
label diodevss_2kv FreeSans 600 90 0 0 c comment
select area label
setlabel sticky true
select clear
view
tech revert
resumeall
