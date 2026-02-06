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

__version__ = '$Revision: #3 $'

from cni.dlo import *
from .geometry import *
from .utility_functions import *

from dataclasses import dataclass


@dataclass
class ResistorInfo:
    plus_pin_box: Box
    minus_pin_box: Box


class ResistorBase(DloGen):
    @classmethod
    def defineParamSpecs(cls, specs):
        specs('NumberOfSegments', 1, 'Number of Segments')
        specs('SegmentConnection', 'Serial', 'Segment Connection', ChoiceConstraint(['None', 'Serial', 'Parallel']))
        specs('SegmentSpacing', '2u', 'Segment Spacing')

    def setupParams(self, params):
        # process parameter values entered by user
        self.params = params
        self.number_of_segments = int(params['NumberOfSegments'])
        self.segment_connection = params['SegmentConnection']
        self.segment_spacing = Numeric(params['SegmentSpacing'])*1e6

    @abstractmethod
    def genSingleResistorLayout(self, index: int, x_offset: float) -> ResistorInfo:
        raise NotImplementedError('subclasses must overwrite the method genSingleResistorLayout()')

    def genLayout(self):
        met1_drw = Layer('Metal1', 'drawing')

        x_offset = 0.0
        previous_res_info = None
        for i in range(0, self.number_of_segments):
            res_info = self.genSingleResistorLayout(index=i, x_offset=x_offset)

            if previous_res_info is not None:
                match self.segment_connection:
                    case 'Serial':
                        box1: Box
                        box2: Box
                        if i % 2 == 0:
                            # horizontal connection near top, PLUS
                            box1 = previous_res_info.plus_pin_box
                            box2 = res_info.plus_pin_box
                        else:
                            # horizontal connection near bottom, MINUS
                            box1 = previous_res_info.minus_pin_box
                            box2 = res_info.minus_pin_box
                        dbCreateRect(self, met1_drw, Box(box1.left, box1.bottom, box2.right, box2.top))
                    case 'Parallel':
                        box1 = previous_res_info.plus_pin_box
                        box2 = res_info.plus_pin_box
                        dbCreateRect(self, met1_drw, Box(box1.left, box1.bottom, box2.right, box2.top))
                        box1 = previous_res_info.minus_pin_box
                        box2 = res_info.minus_pin_box
                        dbCreateRect(self, met1_drw, Box(box1.left, box1.bottom, box2.right, box2.top))
            x_offset += self.segment_spacing
            previous_res_info = res_info

