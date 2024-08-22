#!/bin/bash

########################################################################
#
# Copyright 2024 IHP PDK Authors
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

# checking CDL and SPICE netlists
# the only allowed multiplier is m=1

cellset="sg13g2_stdcell"
for view in cdl spice; do
  grep -nHE 'm=[^1]' ../../libs.ref/${cellset}/${view}/${cellset}.*
done
