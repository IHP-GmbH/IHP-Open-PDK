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

import pya
import sys

class TechImpl(object):
    pass

class Tech(object):

    techsByName = {}

    def register(tech):
        Tech.techsByName[tech.name()] = tech

    def get(name):
        return Tech.techsByName[name]


def ChoiceConstraint(choices, action = ACCEPT):
    return choices


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

        self.param_decls = []

        # NOTE: the PCellWrapper acts as the "specs" object
        type(impl).defineParamSpecs(self)

    def __call__(self, name, value, description = None, choices = None):
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

        if choices is not None:
            for v in choices:
                param_decl.add_choice(repr(v), v)

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


