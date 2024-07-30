__version__ = '$Revision: #3 $'

from cni.dlo import *
from .geometry import *
from .utility_functions import *

import math


class dpantenna(DloGen):

    @classmethod
    def defineParamSpecs(self, specs):
        techparams = specs.tech.getTechParams()

        CDFVersion = techparams['CDFVersion']
        model = techparams['dpantenna_model']
        defL = techparams['dpantenna_defL']
        defW = techparams['dpantenna_defW']

        specs('cdf_version', CDFVersion, 'CDF Version')
        specs('Display', 'Selected', 'Display', ChoiceConstraint(['All', 'Selected']))
        specs('model', model, 'Model name')
        specs('Calculate', 'a', 'Calculate', ChoiceConstraint(['a', 'w', 'l', 'w&l']))

        specs('w', defW, 'Width')
        specs('l', defL, 'Length')
        specs('a', eng_string(CbDiodeCalc('a', 0, Numeric(defL), Numeric(defW), 'dantenna'), 3), 'Device area')
        specs('p', eng_string(CbDiodeCalc('p', 0, Numeric(defL), Numeric(defW), 'dantenna'), 3), 'Device perimeter')

        specs('addRecLayer', 't', 'Add Recognition Layer', ChoiceConstraint(['t', 'f']))
        specs('off', False, 'Device initially off')
        specs('Vd', '', 'Initial diode voltage')
        specs('perim', '', 'Junction perimeter factor')
        specs('m', '1', 'Multiplier')
        specs('trise', '', 'Temp rise from ambient')
        specs('region', ' ', 'Estimated operating region', ChoiceConstraint([' ', 'off', 'on']))
        specs('dtemp', '', 'Temperature difference')
        specs('mode', 'No', 'Linearized Region', ChoiceConstraint(['Yes', 'No']))

    def setupParams(self, params):
        # process parameter values entered by user
        self.w = Numeric(params['w']) * 1e6
        self.l = Numeric(params['l']) * 1e6
        self.addRecLayer = params['addRecLayer']

    def genLayout(self):
        w = self.w
        l = self.l
        addRecLayer = self.addRecLayer

        self.techparams = self.tech.getTechParams()
        self.epsilon = self.techparams['epsilon1']

        metall_layer = Layer('Metal1')
        pdiff_layer = Layer('Activ')
        pdiffx_layer = Layer('pSD')
        cont_layer = Layer('Cont')
        diods_layer = Layer('Recog', 'diode')
        text_layer = Layer('TEXT')
        nwell_layer = Layer('NWell')
        cont_size = self.techparams['Cnt_a']
        cont_dist = self.techparams['Cnt_b']
        cont_diff_over = self.techparams['Cnt_c']
        pdiffx_over = self.techparams['pSD_c']
        wmin = Numeric(self.techparams['dpantenna_minW']) * 1e6
        lmin = Numeric(self.techparams['dpantenna_minL']) * 1e6
        diods_over = Numeric(self.techparams['dpantenna_dov']) * 1e6
        NW_c = self.techparams['NW_c']

        dbReplaceProp(self, 'pin#', 2)

        if w < wmin - self.epsilon:
            w = wmin
            hiGetAttention()
            print('W < ' + str(wmin))

        if l < lmin - self.epsilon:
            l = lmin
            hiGetAttention()
            print('L < ' + str(lmin))

        dbCreateLabel(self, text_layer, Point(w / 2, l / 2), 'dpant', 'centerCenter', 'R0', Font.EURO_STYLE, 0.2)

        bBox = DrawContArray(self, cont_layer, Box(0, 0, w, l), cont_size, cont_dist, cont_diff_over)

        dbCreateRect(self, metall_layer, bBox)

        MkPin(self, 'MINUS', 1, bBox, metall_layer)

        pdiffRect = dbCreateRect(self, pdiff_layer, Box(0, 0, w, l))
        dbCreateRect(self, pdiffx_layer, Box(-pdiffx_over, -pdiffx_over, w + pdiffx_over, l + pdiffx_over))

        if addRecLayer == 't':
            dbCreateRect(self, diods_layer, Box(-diods_over, -diods_over, w + diods_over, l + diods_over))

        dbLayerSize(nwell_layer, [pdiffRect], NW_c)
