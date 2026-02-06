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

# Command script for generating cell diodevss_4kv

suspendall
tech unlock *
snap internal
load diodevss_4kv -silent
box values 0 0 0 0
box values 0 7140 2864 7410
paint nwell
box values 0 270 270 7140
paint nwell
box values 2600 270 2864 7140
paint nwell
box values 0 0 2864 270
paint nwell
box values 370 6736 2488 7040
paint pwell
box values 370 6512 674 6736
paint pwell
box values 1276 6512 1580 6736
paint pwell
box values 2184 6512 2488 6736
paint pwell
box values 370 904 2488 6512
paint pwell
box values 370 674 674 904
paint pwell
box values 1276 674 1580 904
paint pwell
box values 2184 674 2488 904
paint pwell
box values 370 370 2488 674
paint pwell
box values 846 6466 1098 6486
paint ndiff
box values 846 962 888 6466
paint ndiff
box values 1064 962 1098 6466
paint ndiff
box values 846 930 1098 962
paint ndiff
box values 1752 6466 2004 6486
paint ndiff
box values 1752 962 1794 6466
paint ndiff
box values 1970 962 2004 6466
paint ndiff
box values 1752 930 2004 962
paint ndiff
box values 888 962 1064 6466
paint ndiffc
box values 1794 962 1970 6466
paint ndiffc
box values 396 6980 2462 7014
paint psubdiff
box values 396 6804 447 6980
paint psubdiff
box values 2423 6804 2462 6980
paint psubdiff
box values 396 6762 2462 6804
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
box values 1302 681 1345 6761
paint psubdiff
box values 1521 681 1554 6761
paint psubdiff
box values 2210 6761 2462 6762
paint psubdiff
box values 1302 648 1554 681
paint psubdiff
box values 2210 681 2257 6761
paint psubdiff
box values 2433 681 2462 6761
paint psubdiff
box values 2210 648 2462 681
paint psubdiff
box values 396 614 2462 648
paint psubdiff
box values 396 438 447 614
paint psubdiff
box values 2423 438 2462 614
paint psubdiff
box values 396 396 2462 438
paint psubdiff
box values 84 7288 2780 7320
paint nsubdiff
box values 84 7256 124 7288
paint nsubdiff
box values 2748 7256 2780 7288
paint nsubdiff
box values 84 7224 2780 7256
paint nsubdiff
box values 84 7165 180 7224
paint nsubdiff
box values 84 221 116 7165
paint nsubdiff
box values 148 221 180 7165
paint nsubdiff
box values 2684 7165 2780 7224
paint nsubdiff
box values 84 186 180 221
paint nsubdiff
box values 2684 221 2708 7165
paint nsubdiff
box values 2740 221 2780 7165
paint nsubdiff
box values 2684 186 2780 221
paint nsubdiff
box values 84 154 2780 186
paint nsubdiff
box values 84 122 124 154
paint nsubdiff
box values 2748 122 2780 154
paint nsubdiff
box values 84 90 2780 122
paint nsubdiff
box values 447 6804 2423 6980
paint psubdiffcont
box values 433 681 609 6761
paint psubdiffcont
box values 1345 681 1521 6761
paint psubdiffcont
box values 2257 681 2433 6761
paint psubdiffcont
box values 447 438 2423 614
paint psubdiffcont
box values 124 7256 2748 7288
paint nsubdiffcont
box values 116 221 148 7165
paint nsubdiffcont
box values 2708 221 2740 7165
paint nsubdiffcont
box values 124 122 2748 154
paint nsubdiffcont
box values 0 7288 2864 7410
paint metal1
box values 0 7256 124 7288
paint metal1
box values 2748 7256 2864 7288
paint metal1
box values 0 7165 2864 7256
paint metal1
box values 0 221 116 7165
paint metal1
box values 148 7140 2708 7165
paint metal1
box values 148 270 270 7140
paint metal1
box values 366 6980 2492 7032
paint metal1
box values 366 6804 447 6980
paint metal1
box values 2423 6804 2492 6980
paint metal1
box values 366 6761 2492 6804
paint metal1
box values 366 6665 433 6761
paint metal1
box values 609 6750 1345 6761
paint metal1
box values 609 6665 672 6750
paint metal1
box values 366 6145 401 6665
paint metal1
box values 633 6145 672 6665
paint metal1
box values 1272 6665 1345 6750
paint metal1
box values 1521 6750 2257 6761
paint metal1
box values 1521 6665 1584 6750
paint metal1
box values 366 4865 433 6145
paint metal1
box values 609 4865 672 6145
paint metal1
box values 366 4345 401 4865
paint metal1
box values 633 4345 672 4865
paint metal1
box values 366 3065 433 4345
paint metal1
box values 609 3065 672 4345
paint metal1
box values 366 2545 401 3065
paint metal1
box values 633 2545 672 3065
paint metal1
box values 366 1265 433 2545
paint metal1
box values 609 1265 672 2545
paint metal1
box values 366 745 401 1265
paint metal1
box values 633 745 672 1265
paint metal1
box values 822 6466 1128 6540
paint metal1
box values 822 5844 888 6466
paint metal1
box values 1064 5844 1128 6466
paint metal1
box values 822 5132 856 5844
paint metal1
box values 1088 5132 1128 5844
paint metal1
box values 822 4044 888 5132
paint metal1
box values 1064 4044 1128 5132
paint metal1
box values 822 3332 856 4044
paint metal1
box values 1088 3332 1128 4044
paint metal1
box values 822 2244 888 3332
paint metal1
box values 1064 2244 1128 3332
paint metal1
box values 822 1532 856 2244
paint metal1
box values 1088 1532 1128 2244
paint metal1
box values 822 962 888 1532
paint metal1
box values 1064 962 1128 1532
paint metal1
box values 822 870 1128 962
paint metal1
box values 1272 6145 1313 6665
paint metal1
box values 1545 6145 1584 6665
paint metal1
box values 2180 6665 2257 6750
paint metal1
box values 2433 6665 2492 6761
paint metal1
box values 1272 4865 1345 6145
paint metal1
box values 1521 4865 1584 6145
paint metal1
box values 1272 4345 1313 4865
paint metal1
box values 1545 4345 1584 4865
paint metal1
box values 1272 3065 1345 4345
paint metal1
box values 1521 3065 1584 4345
paint metal1
box values 1272 2545 1313 3065
paint metal1
box values 1545 2545 1584 3065
paint metal1
box values 1272 1265 1345 2545
paint metal1
box values 1521 1265 1584 2545
paint metal1
box values 366 681 433 745
paint metal1
box values 609 681 672 745
paint metal1
box values 366 660 672 681
paint metal1
box values 1272 745 1313 1265
paint metal1
box values 1545 745 1584 1265
paint metal1
box values 1728 6466 2034 6540
paint metal1
box values 1728 5844 1794 6466
paint metal1
box values 1970 5844 2034 6466
paint metal1
box values 1728 5132 1762 5844
paint metal1
box values 1994 5132 2034 5844
paint metal1
box values 1728 4044 1794 5132
paint metal1
box values 1970 4044 2034 5132
paint metal1
box values 1728 3332 1762 4044
paint metal1
box values 1994 3332 2034 4044
paint metal1
box values 1728 2244 1794 3332
paint metal1
box values 1970 2244 2034 3332
paint metal1
box values 1728 1532 1762 2244
paint metal1
box values 1994 1532 2034 2244
paint metal1
box values 1728 962 1794 1532
paint metal1
box values 1970 962 2034 1532
paint metal1
box values 1728 870 2034 962
paint metal1
box values 2180 6145 2225 6665
paint metal1
box values 2457 6145 2492 6665
paint metal1
box values 2180 4865 2257 6145
paint metal1
box values 2433 4865 2492 6145
paint metal1
box values 2180 4345 2225 4865
paint metal1
box values 2457 4345 2492 4865
paint metal1
box values 2180 3065 2257 4345
paint metal1
box values 2433 3065 2492 4345
paint metal1
box values 2180 2545 2225 3065
paint metal1
box values 2457 2545 2492 3065
paint metal1
box values 2180 1265 2257 2545
paint metal1
box values 2433 1265 2492 2545
paint metal1
box values 1272 681 1345 745
paint metal1
box values 1521 681 1584 745
paint metal1
box values 1272 660 1584 681
paint metal1
box values 2180 745 2225 1265
paint metal1
box values 2457 745 2492 1265
paint metal1
box values 2180 681 2257 745
paint metal1
box values 2433 681 2492 745
paint metal1
box values 2180 660 2492 681
paint metal1
box values 366 614 2492 660
paint metal1
box values 366 438 447 614
paint metal1
box values 2423 438 2492 614
paint metal1
box values 366 378 2492 438
paint metal1
box values 2600 270 2708 7140
paint metal1
box values 148 221 2708 270
paint metal1
box values 2740 221 2864 7165
paint metal1
box values 0 154 2864 221
paint metal1
box values 0 122 124 154
paint metal1
box values 2748 122 2864 154
paint metal1
box values 0 0 2864 122
paint metal1
box values 401 6145 433 6665
paint via1
box values 433 6145 609 6665
paint psc+v
box values 609 6145 633 6665
paint via1
box values 401 4345 433 4865
paint via1
box values 433 4345 609 4865
paint psc+v
box values 609 4345 633 4865
paint via1
box values 401 2545 433 3065
paint via1
box values 433 2545 609 3065
paint psc+v
box values 609 2545 633 3065
paint via1
box values 401 745 433 1265
paint via1
box values 433 745 609 1265
paint psc+v
box values 609 745 633 1265
paint via1
box values 856 5132 888 5844
paint via1
box values 888 5132 1064 5844
paint ndc+v
box values 1064 5132 1088 5844
paint via1
box values 856 3332 888 4044
paint via1
box values 888 3332 1064 4044
paint ndc+v
box values 1064 3332 1088 4044
paint via1
box values 856 1532 888 2244
paint via1
box values 888 1532 1064 2244
paint ndc+v
box values 1064 1532 1088 2244
paint via1
box values 1313 6145 1345 6665
paint via1
box values 1345 6145 1521 6665
paint psc+v
box values 1521 6145 1545 6665
paint via1
box values 1313 4345 1345 4865
paint via1
box values 1345 4345 1521 4865
paint psc+v
box values 1521 4345 1545 4865
paint via1
box values 1313 2545 1345 3065
paint via1
box values 1345 2545 1521 3065
paint psc+v
box values 1521 2545 1545 3065
paint via1
box values 1313 745 1345 1265
paint via1
box values 1345 745 1521 1265
paint psc+v
box values 1521 745 1545 1265
paint via1
box values 1762 5132 1794 5844
paint via1
box values 1794 5132 1970 5844
paint ndc+v
box values 1970 5132 1994 5844
paint via1
box values 1762 3332 1794 4044
paint via1
box values 1794 3332 1970 4044
paint ndc+v
box values 1970 3332 1994 4044
paint via1
box values 1762 1532 1794 2244
paint via1
box values 1794 1532 1970 2244
paint ndc+v
box values 1970 1532 1994 2244
paint via1
box values 2225 6145 2257 6665
paint via1
box values 2257 6145 2433 6665
paint psc+v
box values 2433 6145 2457 6665
paint via1
box values 2225 4345 2257 4865
paint via1
box values 2257 4345 2433 4865
paint psc+v
box values 2433 4345 2457 4865
paint via1
box values 2225 2545 2257 3065
paint via1
box values 2257 2545 2433 3065
paint psc+v
box values 2433 2545 2457 3065
paint via1
box values 2225 745 2257 1265
paint via1
box values 2257 745 2433 1265
paint psc+v
box values 2433 745 2457 1265
paint via1
box values 492 6665 3092 6666
paint metal2
box values 392 6145 401 6665
paint metal2
box values 633 6145 1313 6665
paint metal2
box values 1545 6145 2225 6665
paint metal2
box values 2457 6145 3092 6665
paint metal2
box values 492 6144 3092 6145
paint metal2
box values -462 5132 856 5844
paint metal2
box values 1088 5132 1762 5844
paint metal2
box values 1994 5132 2003 5844
paint metal2
box values -462 4044 259 5132
paint metal2
box values 2364 4866 3092 6144
paint metal2
box values 492 4865 3092 4866
paint metal2
box values 392 4345 401 4865
paint metal2
box values 633 4345 1313 4865
paint metal2
box values 1545 4345 2225 4865
paint metal2
box values 2457 4345 3092 4865
paint metal2
box values 492 4344 3092 4345
paint metal2
box values -462 3332 856 4044
paint metal2
box values 1088 3332 1762 4044
paint metal2
box values 1994 3332 2003 4044
paint metal2
box values -462 2244 259 3332
paint metal2
box values 2364 3066 3092 4344
paint metal2
box values 492 3065 3092 3066
paint metal2
box values 392 2545 401 3065
paint metal2
box values 633 2545 1313 3065
paint metal2
box values 1545 2545 2225 3065
paint metal2
box values 2457 2545 3092 3065
paint metal2
box values 492 2544 3092 2545
paint metal2
box values -462 1532 856 2244
paint metal2
box values 1088 1532 1762 2244
paint metal2
box values 1994 1532 2003 2244
paint metal2
box values 2364 1266 3092 2544
paint metal2
box values 492 1265 3092 1266
paint metal2
box values 392 745 401 1265
paint metal2
box values 633 745 1313 1265
paint metal2
box values 1545 745 2225 1265
paint metal2
box values 2457 745 3092 1265
paint metal2
box values 492 744 3092 745
paint metal2
box values 1432 7275 1432 7275
label VDD FreeSans 200 0 0 0 c comment
select area label
setlabel sticky true
box values 2728 3705 2728 3705
label VSS FreeSans 500 90 0 0 c comment
select area label
setlabel sticky true
box values -102 3688 -102 3688
label PAD FreeSans 500 90 0 0 c comment
select area label
setlabel sticky true
box values 689 499 689 499
label sub! FreeSans 200 0 0 0 c comment
select area label
setlabel sticky true
box values 2124 3650 2124 3650
label diodevss_4kv FreeSans 600 90 0 0 c comment
select area label
setlabel sticky true
select clear
view
tech revert
resumeall
