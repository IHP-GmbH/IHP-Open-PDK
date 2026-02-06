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

# Command script for generating cell sealring_corner

suspendall
tech unlock *
snap internal
load sealring_corner -silent
box values -26 3351 1601 4226
paint pwell
box values -26 3299 2476 3351
paint pwell
box values 849 2476 2476 3299
paint pwell
box values 849 2424 3351 2476
paint pwell
box values 1724 1601 3351 2424
paint pwell
box values 1724 1549 4226 1601
paint pwell
box values 2599 674 4226 1549
paint pwell
box values 3474 -26 4226 674
paint pwell
box values 260 3617 292 4200
paint sealcont
box values 260 3585 1167 3617
paint sealcont
box values 1135 2742 1167 3585
paint sealcont
box values 1135 2710 2042 2742
paint sealcont
box values 2010 1867 2042 2710
paint sealcont
box values 2010 1835 2917 1867
paint sealcont
box values 2885 992 2917 1835
paint sealcont
box values 2885 960 3792 992
paint sealcont
box values 3760 292 3792 960
paint sealcont
box values 3760 260 4200 292
paint sealcont
box values 0 3585 260 4200
paint psubdiff
box values 292 3617 1575 4200
paint psubdiff
box values 0 3325 1135 3585
paint psubdiff
box values 875 2710 1135 3325
paint psubdiff
box values 1167 3325 1575 3617
paint psubdiff
box values 1167 2742 2450 3325
paint psubdiff
box values 875 2450 2010 2710
paint psubdiff
box values 1750 1835 2010 2450
paint psubdiff
box values 2042 2450 2450 2742
paint psubdiff
box values 2042 1867 3325 2450
paint psubdiff
box values 1750 1575 2885 1835
paint psubdiff
box values 2625 960 2885 1575
paint psubdiff
box values 2917 1575 3325 1867
paint psubdiff
box values 2917 992 4200 1575
paint psubdiff
box values 2625 700 3760 960
paint psubdiff
box values 3500 260 3760 700
paint psubdiff
box values 3792 292 4200 992
paint psubdiff
box values 3500 0 4200 260
paint psubdiff
box values 0 3585 260 4200
paint metal1
box values 298 3623 1575 4200
paint metal1
box values 0 3325 1135 3585
paint metal1
box values 875 2710 1135 3325
paint metal1
box values 1173 3325 1575 3623
paint metal1
box values 1173 2748 2450 3325
paint metal1
box values 875 2450 2010 2710
paint metal1
box values 1750 1835 2010 2450
paint metal1
box values 2048 2450 2450 2748
paint metal1
box values 2048 1873 3325 2450
paint metal1
box values 1750 1575 2885 1835
paint metal1
box values 2625 960 2885 1575
paint metal1
box values 2923 1575 3325 1873
paint metal1
box values 2923 998 4200 1575
paint metal1
box values 2625 700 3760 960
paint metal1
box values 3500 260 3760 700
paint metal1
box values 3798 298 4200 998
paint metal1
box values 3500 0 4200 260
paint metal1
box values 260 3623 298 4200
paint sealvia1
box values 260 3585 1173 3623
paint sealvia1
box values 1135 2748 1173 3585
paint sealvia1
box values 1135 2710 2048 2748
paint sealvia1
box values 2010 1873 2048 2710
paint sealvia1
box values 2010 1835 2923 1873
paint sealvia1
box values 2885 998 2923 1835
paint sealvia1
box values 2885 960 3798 998
paint sealvia1
box values 3760 298 3798 960
paint sealvia1
box values 3760 260 4200 298
paint sealvia1
box values 0 3585 260 4200
paint metal2
box values 298 3623 1575 4200
paint metal2
box values 0 3325 1135 3585
paint metal2
box values 875 2710 1135 3325
paint metal2
box values 1173 3325 1575 3623
paint metal2
box values 1173 2748 2450 3325
paint metal2
box values 875 2450 2010 2710
paint metal2
box values 1750 1835 2010 2450
paint metal2
box values 2048 2450 2450 2748
paint metal2
box values 2048 1873 3325 2450
paint metal2
box values 1750 1575 2885 1835
paint metal2
box values 2625 960 2885 1575
paint metal2
box values 2923 1575 3325 1873
paint metal2
box values 2923 998 4200 1575
paint metal2
box values 2625 700 3760 960
paint metal2
box values 3500 260 3760 700
paint metal2
box values 3798 298 4200 998
paint metal2
box values 3500 0 4200 260
paint metal2
box values 260 3623 298 4200
paint sealvia2
box values 260 3585 1173 3623
paint sealvia2
box values 1135 2748 1173 3585
paint sealvia2
box values 1135 2710 2048 2748
paint sealvia2
box values 2010 1873 2048 2710
paint sealvia2
box values 2010 1835 2923 1873
paint sealvia2
box values 2885 998 2923 1835
paint sealvia2
box values 2885 960 3798 998
paint sealvia2
box values 3760 298 3798 960
paint sealvia2
box values 3760 260 4200 298
paint sealvia2
box values 0 3585 260 4200
paint metal3
box values 298 3623 1575 4200
paint metal3
box values 0 3325 1135 3585
paint metal3
box values 875 2710 1135 3325
paint metal3
box values 1173 3325 1575 3623
paint metal3
box values 1173 2748 2450 3325
paint metal3
box values 875 2450 2010 2710
paint metal3
box values 1750 1835 2010 2450
paint metal3
box values 2048 2450 2450 2748
paint metal3
box values 2048 1873 3325 2450
paint metal3
box values 1750 1575 2885 1835
paint metal3
box values 2625 960 2885 1575
paint metal3
box values 2923 1575 3325 1873
paint metal3
box values 2923 998 4200 1575
paint metal3
box values 2625 700 3760 960
paint metal3
box values 3500 260 3760 700
paint metal3
box values 3798 298 4200 998
paint metal3
box values 3500 0 4200 260
paint metal3
box values 260 3623 298 4200
paint sealvia3
box values 260 3585 1173 3623
paint sealvia3
box values 1135 2748 1173 3585
paint sealvia3
box values 1135 2710 2048 2748
paint sealvia3
box values 2010 1873 2048 2710
paint sealvia3
box values 2010 1835 2923 1873
paint sealvia3
box values 2885 998 2923 1835
paint sealvia3
box values 2885 960 3798 998
paint sealvia3
box values 3760 298 3798 960
paint sealvia3
box values 3760 260 4200 298
paint sealvia3
box values 0 3585 260 4200
paint metal4
box values 298 3623 1575 4200
paint metal4
box values 0 3325 1135 3585
paint metal4
box values 875 2710 1135 3325
paint metal4
box values 1173 3325 1575 3623
paint metal4
box values 1173 2748 2450 3325
paint metal4
box values 875 2450 2010 2710
paint metal4
box values 1750 1835 2010 2450
paint metal4
box values 2048 2450 2450 2748
paint metal4
box values 2048 1873 3325 2450
paint metal4
box values 1750 1575 2885 1835
paint metal4
box values 2625 960 2885 1575
paint metal4
box values 2923 1575 3325 1873
paint metal4
box values 2923 998 4200 1575
paint metal4
box values 2625 700 3760 960
paint metal4
box values 3500 260 3760 700
paint metal4
box values 3798 298 4200 998
paint metal4
box values 3500 0 4200 260
paint metal4
box values 260 3623 298 4200
paint sealvia4
box values 260 3585 1173 3623
paint sealvia4
box values 1135 2748 1173 3585
paint sealvia4
box values 1135 2710 2048 2748
paint sealvia4
box values 2010 1873 2048 2710
paint sealvia4
box values 2010 1835 2923 1873
paint sealvia4
box values 2885 998 2923 1835
paint sealvia4
box values 2885 960 3798 998
paint sealvia4
box values 3760 298 3798 960
paint sealvia4
box values 3760 260 4200 298
paint sealvia4
box values 0 3585 260 4200
paint metal5
box values 344 3669 1575 4200
paint metal5
box values 0 3325 1135 3585
paint metal5
box values 875 2710 1135 3325
paint metal5
box values 1219 3325 1575 3669
paint metal5
box values 1219 2794 2450 3325
paint metal5
box values 875 2450 2010 2710
paint metal5
box values 1750 1835 2010 2450
paint metal5
box values 2094 2450 2450 2794
paint metal5
box values 2094 1919 3325 2450
paint metal5
box values 1750 1575 2885 1835
paint metal5
box values 2625 960 2885 1575
paint metal5
box values 2969 1575 3325 1919
paint metal5
box values 2969 1044 4200 1575
paint metal5
box values 2625 700 3760 960
paint metal5
box values 3500 260 3760 700
paint metal5
box values 3844 344 4200 1044
paint metal5
box values 3500 0 4200 260
paint metal5
box values 260 3669 344 4200
paint sealvia5
box values 260 3585 1219 3669
paint sealvia5
box values 1135 2794 1219 3585
paint sealvia5
box values 1135 2710 2094 2794
paint sealvia5
box values 2010 1919 2094 2710
paint sealvia5
box values 2010 1835 2969 1919
paint sealvia5
box values 2885 1044 2969 1835
paint sealvia5
box values 2885 960 3844 1044
paint sealvia5
box values 3760 344 3844 960
paint sealvia5
box values 3760 260 4200 344
paint sealvia5
box values 0 3585 260 4200
paint metal6
box values 440 3765 1575 4200
paint metal6
box values 0 3325 1135 3585
paint metal6
box values 875 2710 1135 3325
paint metal6
box values 1315 3325 1575 3765
paint metal6
box values 1315 2890 2450 3325
paint metal6
box values 875 2450 2010 2710
paint metal6
box values 1750 1835 2010 2450
paint metal6
box values 2190 2450 2450 2890
paint metal6
box values 2190 2015 3325 2450
paint metal6
box values 1750 1575 2885 1835
paint metal6
box values 2625 960 2885 1575
paint metal6
box values 3065 1575 3325 2015
paint metal6
box values 3065 1140 4200 1575
paint metal6
box values 2625 700 3760 960
paint metal6
box values 3500 260 3760 700
paint metal6
box values 3940 440 4200 1140
paint metal6
box values 3500 0 4200 260
paint metal6
box values 260 3765 440 4200
paint sealvia6
box values 260 3585 1315 3765
paint sealvia6
box values 1135 2890 1315 3585
paint sealvia6
box values 1135 2710 2190 2890
paint sealvia6
box values 2010 2015 2190 2710
paint sealvia6
box values 2010 1835 3065 2015
paint sealvia6
box values 2885 1140 3065 1835
paint sealvia6
box values 2885 960 3940 1140
paint sealvia6
box values 3760 440 3940 960
paint sealvia6
box values 3760 260 4200 440
paint sealvia6
box values 0 3325 1575 4200
paint metal7
box values 875 2450 2450 3325
paint metal7
box values 1750 1575 3325 2450
paint metal7
box values 2625 700 4200 1575
paint metal7
box values 3500 0 4200 700
paint metal7
box values -1440 2725 -600 4200
paint seal
box values -1440 1885 275 2725
paint seal
box values -565 1850 275 1885
paint seal
box values -565 1010 1150 1850
paint seal
box values 310 975 1150 1010
paint seal
box values 310 135 2025 975
paint seal
box values 1185 100 2025 135
paint seal
box values 1185 -600 2900 100
paint seal
box values 1185 -740 4200 -600
paint seal
box values 2060 -1440 4200 -740
paint seal
property FIXED_BBOX "-1440 -1440 4200 4200"
select clear
view
tech revert
resumeall
