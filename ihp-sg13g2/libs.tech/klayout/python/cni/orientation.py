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

class Orientation(object):
    # TODO: this better should match KLayout's transformation code for
    # easy porting
    R0 = 0
    R90 = 1
    R180 = 2
    R270 = 3
    MY = 4
    MYR90 = 5
    MX = 6
    MXR90 = 7

    def concat(self, other):
        raise Exception("Not implemented yet!")

    def getRelativeOrient(self, other):
        raise Exception("Not implemented yet!")


