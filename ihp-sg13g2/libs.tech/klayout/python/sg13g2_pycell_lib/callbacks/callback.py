########################################################################
#
# Copyright 2026 IHP PDK Authors
#
# Licensed under the GNU General Public License, Version 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.gnu.org/licenses/gpl-3.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
########################################################################

from __future__ import with_statement

from numeric import *

import os

def engToSci(value):
    numDigits = 0
    for char in value:
        if char.isdigit():
            numDigits += 1
        elif char == '.':
            pass
        elif char == '-' and numDigits == 0:
            pass
        else:
            break
    if numDigits == 0:
        return value
    precision = numDigits - 1
    return Numeric(value).sciFormat(int(precision))

def sciToEng(value, precision = 8):
    numDigits = 0
    for char in value:
        if char.isdigit():
            numDigits += 1
        elif char == '.':
            pass
        elif char == '-' and numDigits == 0:
            pass
        else:
            break
    if numDigits == 0:
        return value
    if numDigits <= precision:
        precision = numDigits
    if precision < 3:
        precision = 3
    return Numeric(value).engFormat(int(precision))

def cni_engToSci(value):
    return engToSci(value)

