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

__version__ = '$Revision: #3 $'

import pya

import cni.rect
import cni.text
from cni.dlo import *
from .geometry import *
from .guard_ring_code import generate_guard_ring, GuardRingType
from .utility_functions import *


class DeviceBase(DloGen):
    @classmethod
    def defineParamSpecs(cls, specs):
        choices = [c.value for c in cls.validGuardRingTypes()]
        specs('guardRingType', 'none', 'Guard Ring Type', ChoiceConstraint(choices))
        specs('guardRingDistance', '1u', 'Guard Ring Distance')

    def setupParams(self, params):
        # process parameter values entered by user
        self.guardRingType     = GuardRingType(params['guardRingType'])
        self.guardRingDistance = Numeric(params['guardRingDistance'])*1e6

    @abstractmethod
    def genDeviceLayout(self):
        """
        Template method for subclasses to overwrite
        """
        raise NotImplementedError()

    @classmethod
    def validGuardRingTypes(cls) -> List[GuardRingType]:
        """
        Template method for subclasses to restrict the guard ring types
        """
        return GuardRingType.cases()

    def genLayout(self):
        self.genDeviceLayout()
        if self.guardRingType != GuardRingType.NONE:
            min_left = INT_MAX
            min_bottom = INT_MAX
            max_right = INT_MIN
            max_top = INT_MIN

            for s in self.getShapes():
                if isinstance(s, cni.text.Text):
                    continue

                bbox = s.bbox
                if isinstance(bbox, bool):
                    # FIXME: in dpantenna/inductor2/inductor3 cells,
                    #        strangely Polygon shapes
                    #        had s.bbox being a boolean!
                    #        skip those for now
                    #
                    # remove this as soon as this PR is merged:
                    # https://github.com/IHP-GmbH/pycell4klayout-api/pull/3
                    continue

                min_left = min(min_left, bbox.left)
                min_bottom = min(min_bottom, bbox.bottom)
                max_right = max(max_right, bbox.right)
                max_top = max(max_top, bbox.top)

            w = max_right - min_left + self.guardRingDistance * 2.0
            h = max_top - min_bottom + self.guardRingDistance * 2.0

            x_center = min_left + (max_right - min_left) / 2.0
            y_center = min_bottom + (max_top - min_bottom) / 2.0

            generate_guard_ring(dlo_gen=self,
                                guard_ring_type=self.guardRingType,
                                w=w,
                                h=h,
                                x_center=x_center,
                                y_center=y_center)