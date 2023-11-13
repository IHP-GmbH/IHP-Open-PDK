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

from cni.location import *
from cni.orientation import *

class Font(object):
    EURO_STYLE = 1
    FIXED = 2
    GOTHIC = 3
    MATH = 4
    MIL_SPEC = 5
    ROMAN = 6
    SCRIPT = 7
    STICK = 8
    SWEDISH = 9

    @classmethod
    def getMembers(cls):
        return [cls.EURO_STYLE, cls.FIXED, cls.GOTHIC, cls.MATH, cls.MIL_SPEC, cls.ROMAN, cls.SCRIPT, cls.STICK, sls.SWEDISH]

    def calcBBox(self, text, origin, height, location=Location.UPPER_LEFT, orient=Orientation.R0, overbar=False):
        raise Exception("Not implemented yet!")

