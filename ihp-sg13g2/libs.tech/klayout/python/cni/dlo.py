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

from cni.constants import *
from cni.numeric import *
from cni.orientation import *
from cni.location import *
from cni.layer import *
from cni.pathstyle import *
from cni.signaltype import *
from cni.termtype import *
from cni.font import *
from cni.point import *
from cni.pointlist import *
from cni.box import *
from cni.shape import *
from cni.text import *
from cni.polygon import *
from cni.dlogen import *
from cni.transform import *

import pya
import sys

class ChoiceConstraint(list):

    def __init__(self, choices, action = REJECT):
        super().__init__(choices)


class RangeConstraint:

    def __init__(self, low, high, resolution = None, action = REJECT):
        self.low = low
        self.high = high
        self.resolution = resolution
        self.action = action

        if low is not None:
            if not isinstance(low, (int, float)):
                raise Exception(f"Invalid RangeConstraint: low type: '{type(low)})'")

        if high is not None:
            if not isinstance(high, (int, float)):
                raise Exception(f"Invalid RangeConstraint: high type: '{type(high)})'")

        if low is not None and high is not None and low > high:
            raise Exception(f"Invalid RangeConstraint: {low}(low) > {high}(high)")

        if action is not None and type(action) is not int:
            raise Exception(f"Invalid RangeConstraint: action type: '{type(action)})'")


class PyCellContext(object):

  def __init__(self, tech, cell):
    self.tech = tech
    self.cell = cell

  def __enter__(self):
    Layer.tech = self.tech
    Layer.layout = self.cell.layout()
    Shape.cell = self.cell

  def __exit__(self, *params):
    Layer.tech = None
    Layer.layout = None
    Shape.cell = None


class PCellWrapper(pya.PCellDeclaration):

    def __init__(self, impl, tech):
        super(PCellWrapper, self).__init__()

        self.impl = impl
        self.impl.set_tech(tech)
        self.tech = tech

        Tech.techInUse = tech.getTechParams()['libName']

        self.param_decls = []

        # NOTE: the PCellWrapper acts as the "specs" object
        type(impl).defineParamSpecs(self)

    def __call__(self, name, value, description = None, constraint = None):
        # NOTE: this is calles from inside defineParamSpecs as we
        # supply the "specs" object through self.

        if type(value) is float:
            value_type = pya.PCellParameterDeclaration.TypeDouble
        elif type(value) is int:
            value_type = pya.PCellParameterDeclaration.TypeInt
        elif type(value) is str:
            value_type = pya.PCellParameterDeclaration.TypeString
        else:
            print(f"Invalid parameter type for parameter {name} (value is {repr(value)})")
            assert(False)

        param_decl = pya.PCellParameterDeclaration(name, value_type, description, value)

        if type(constraint) is ChoiceConstraint:
            for v in constraint:
                param_decl.add_choice(repr(v), v)
        elif type(constraint) is RangeConstraint:
            if constraint.action is REJECT:
                if constraint.low is not None:
                    param_decl.min_value = constraint.low
                if constraint.high is not None:
                    param_decl.max_value = constraint.high

        self.param_decls.append(param_decl)

    def get_parameters(self):
        return self.param_decls

    def params_as_hash(self,parameters):
        params = {}
        for i in range(0, len(self.param_decls)):
            params[self.param_decls[i].name] = parameters[i]
        return params

    def display_text(self, parameters):
        params = self.params_as_hash(parameters)
        # TODO: form a display string from "important" parameters in a class-specific fashion
        return self.name() + " (...)"

    def produce(self, layout, layers, parameters, cell):
        params = self.params_as_hash(parameters)

        with (PyCellContext(self.tech, cell)):
            self.impl.setupParams(params)
            self.impl.genLayout()


