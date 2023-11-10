
import pya
import os
import sys

from cni.dlo import Tech
from cni.dlo import PCellWrapper

# Creates the SG13_dev technology
from .sg13_tech import *

# Defines the IHP PCells
from .ihp import nmos_code
from .ihp import cmim_code
from .ihp import rsil_code

class PyCellLib(pya.Library):
    def __init__(self):
        self.description = "IHP PyCells"

        tech = Tech.get('SG13_dev')

        # TODO: instead of explicitly creating the PCells here we could
        # use introspection to collect the classes defined
        self.layout().register_pcell("nmos", PCellWrapper(nmos_code.nmos(), tech))
        #self.layout().register_pcell("cmim", PCellWrapper(cmim_code.cmim(), tech))
        #self.layout().register_pcell("rsil", PCellWrapper(rsil_code.rsil(), tech))

        self.register("IHP PyCells")

# instantiate and register the library
PyCellLib()

