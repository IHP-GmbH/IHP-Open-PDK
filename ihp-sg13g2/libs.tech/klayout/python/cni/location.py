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

class Location(object):

    LOWER_LEFT = 1
    CENTER_LEFT = 2
    UPPER_LEFT = 3
    LOWER_CENTER = 4
    CENTER_CENTER = 5
    UPPER_CENTER = 6
    LOWER_RIGHT = 7
    CENTER_RIGHT = 8
    UPPER_RIGHT = 9

    def mirrorX(self):
        raise Exception("Not implemented yet!")

    def mirrorY(self):
        raise Exception("Not implemented yet!")

    def rotate90(self):
        raise Exception("Not implemented yet!")

    def rotate180(self):
        raise Exception("Not implemented yet!")

    def rotate270(self):
        raise Exception("Not implemented yet!")

    def transform(self, transform):
        raise Exception("Not implemented yet!")



