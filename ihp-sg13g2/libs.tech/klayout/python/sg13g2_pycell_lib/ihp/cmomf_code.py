########################################################################
#
# Copyright 2026 IHP PDK Authors
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

__version__ = '$Revision: #1 $'

from cni.dlo import *
from .geometry import *
from .utility_functions import *


class cmomf(DloGen):
    """Metal fringe (finger) MoM capacitor PCell.

    The fringe-style sibling of cmomi. Both are metal-oxide-metal capacitors
    on the Metal1..Metal5 thin-metal stack, and they are complementary rather
    than redundant: cap_cmomi is IHP's characterised interdigitated device
    with a defined feed topology, while this one is the classic cross-fingered
    fringe cap, with every metal layer carrying a comb of fingers whose
    orientation alternates from layer to layer (vertical on the first layer,
    horizontal on the next, and so on).

    Origin. The geometry is a port of the Magic device generator contributed
    by R. Timothy Edwards in ihp-sg13cmos5l PR #31, and reaches g2 through
    ihp-sg13cmos5l PR #78, where it was first released as cap_cmomf on the
    Metal1..Metal4 stack of that PDK. TopMetal1 and TopMetal2 are deliberately
    excluded, as they are for cap_cmomi: the thick top metals are practically
    useless as fringe capacitor plates.

    Capacitance. AREACAP_M1 / AREACAP_MN below come from that same generator
    after its recalibration in ihp-sg13cmos5l PR #69, where the Magic
    wire-edge parasitic extraction was compared against a full 3D OpenEMS
    analysis and corrected for the roughly constant 11% difference between
    them. They are therefore a simulation-derived fit, not foundry-provided
    silicon data, and no corner or mismatch spread is modelled. The C label
    painted here, the Verilog-A/OSDI model and the xschem symbol all evaluate
    the same expression, so layout and simulation agree by construction. With
    one caveat on the area rather than the density: the label below multiplies
    the extents AFTER they are snapped to the 5 nm grid, while the model and
    the symbols use the parameters as given, so a w or l that is not a multiple
    of 5 nm puts the label a fraction of a percent under the simulated value.

    Metal5, specifically, is EXTRAPOLATED. That calibration was run on the
    ihp-sg13cmos5l stack, which stops at Metal4, so the Metal4 to Metal5 step
    reuses AREACAP_MN like every other step and has no measurement behind it.
    cap_cmomi is in the same position at the other end of its range, where its
    own N=2 entry is extrapolated at a constant 0.27 fF/um2 per layer, so the
    two devices are consistent in how far they reach beyond what was measured.
    Anyone with an EM run to spare should start here.

    Axis convention. l is the X extent and w the Y extent, the same mapping
    cap_cmomi uses, because both devices are extracted by the shared
    CapMomExtractor, which reads l from the marker bbox width and w from its
    height. Note that unlike cap_cmomi neither axis is "the finger length"
    here: the finger direction alternates per layer by construction.

    Terminals. PLUS on the left edge, MINUS on the top edge, both on the mmax
    metal, painted as MkPin shapes inside the Recog.momf marker so the LVS
    extractor finds exactly two ports.
    """

    # ---------------------------------------------------------------
    # Layer tables: the five thin metals of the g2 stack (Metal1..Metal5).
    # ---------------------------------------------------------------
    METAL_NAMES = {1: 'Metal1', 2: 'Metal2', 3: 'Metal3', 4: 'Metal4', 5: 'Metal5'}
    VIA_NAMES   = {1: 'Via1', 2: 'Via2', 3: 'Via3', 4: 'Via4'}
    METAL_MAX   = 5

    # ---------------------------------------------------------------
    # Metal rules per layer (um), from the DRM:
    #   mw     minimum width          M1.a = 0.16, Mn.a = 0.20
    #   ms     minimum space          M1.b = 0.18, Mn.b = 0.21
    #   widem  wide-metal threshold, above which the run-length space applies
    #   extras extra space required past that threshold
    #
    # Metal5 takes the Mn row unchanged: 5_17_metaln.drc applies Mn.a, Mn.b
    # and Mn.e to Metal2 through Metal5 alike, and 5_20_vian.drc does the same
    # for Via2 through Via4.
    # ---------------------------------------------------------------
    METAL_RULES = {
        1: {'mw': 0.16, 'ms': 0.18, 'widem': 0.30, 'extras': 0.04},
        2: {'mw': 0.20, 'ms': 0.21, 'widem': 0.39, 'extras': 0.03},
        3: {'mw': 0.20, 'ms': 0.21, 'widem': 0.39, 'extras': 0.03},
        4: {'mw': 0.20, 'ms': 0.21, 'widem': 0.39, 'extras': 0.03},
        5: {'mw': 0.20, 'ms': 0.21, 'widem': 0.39, 'extras': 0.03},
    }

    # V1.a and Vn.a constrain the cut both ways, so vias are square and tiled
    # in arrays rather than drawn as bars.
    VIA_CUT      = 0.19    # V1.a = Vn.a (min AND max)
    VIA_SPACING  = 0.22    # V1.b = Vn.b
    VIA_WIDTH    = 0.20    # VIA_CUT + 2 * Mn.c
    VIA1_BOT_ENC = 0.005   # V1.c - Mn.c
    PIN_SIZE     = 0.20    # nominal pin square, clipped to the bar it sits on

    # ---------------------------------------------------------------
    # Capacitance density (fF/um^2), recalibrated against OpenEMS in PR #69.
    # See the class docstring for provenance and for what is NOT modelled.
    # ---------------------------------------------------------------
    AREACAP_M1 = 0.372     # base when Metal1 is the bottom plate
    AREACAP_MN = 0.305     # base otherwise, and per additional metal layer

    # ---------------------------------------------------------------
    # Parameter specs
    # ---------------------------------------------------------------
    @classmethod
    def defineParamSpecs(cls, specs):
        mchoice = list(range(1, cls.METAL_MAX + 1))
#ifdef KLAYOUT
        specs('model', 'cap_cmomf', 'Model name')
        specs('w', '5.0u', 'Width (Y extent)',
              RangeConstraint(2e-6, 100e-6, USE_DEFAULT))
        specs('l', '5.0u', 'Length (X extent)',
              RangeConstraint(2e-6, 100e-6, USE_DEFAULT))
        specs('mmin', 1, 'Bottom metal (1=M1 .. 5=M5)',
              ChoiceConstraint(mchoice))
        specs('mmax', 5, 'Top metal (1=M1 .. 5=M5)',
              ChoiceConstraint(mchoice))
        specs('subblock', 0, 'Add substrate isolation block',
              ChoiceConstraint([0, 1]))
#else
        specs('model', 'cap_cmomf', 'Model name')
        specs('w', '5.0u', 'Width (Y extent)',
              RangeConstraint(2e-6, 100e-6, USE_DEFAULT))
        specs('l', '5.0u', 'Length (X extent)',
              RangeConstraint(2e-6, 100e-6, USE_DEFAULT))
        specs('mmin', 1, 'Bottom metal (1=M1 .. 5=M5)',
              ChoiceConstraint(mchoice))
        specs('mmax', 5, 'Top metal (1=M1 .. 5=M5)',
              ChoiceConstraint(mchoice))
        specs('subblock', 0, 'Add substrate isolation block',
              ChoiceConstraint([0, 1]))
#endif

    def setupParams(self, params):
        self.params = params
        # Axis convention shared with cap_cmomi: length -> X, width -> Y.
        # Snap here, once: every derived coordinate is GridFix'd on its way to
        # dbCreateRect, so leaving the outer extents unsnapped is what puts the
        # right and top edges of the metal off grid while the marker, built
        # from the same numbers, lands on it.
        self.w_um = GridFix(Numeric(params['w']) * 1e6)      # width  -> Y
        self.l_um = GridFix(Numeric(params['l']) * 1e6)      # length -> X
        self.mmin = int(params['mmin'])
        self.mmax = int(params['mmax'])
        self.subblock = int(params['subblock'])

        # Enforce mmax >= mmin
        if self.mmax < self.mmin:
            self.mmax = self.mmin

    # ---------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------
    @classmethod
    def areacap(cls, mmin, mmax):
        """Capacitance density in fF/um^2 for a given metal stack.

        Kept as a classmethod so the sweep and any external checker can call
        the exact expression the label uses. The Verilog-A model, the ngspice
        wrapper and the xschem symbol duplicate this formula deliberately;
        they must be changed together.
        """
        base = cls.AREACAP_M1 if mmin == 1 else cls.AREACAP_MN
        return base + (mmax - mmin) * cls.AREACAP_MN

    @classmethod
    def _pin_box(cls, rect, side):
        """A pin box fully enclosed by `rect`, hugging the given side.

        Pin.e requires the pin to be inside the metal it labels, and the bar
        it lands on is only as thick as that layer's minimum metal width. Clip
        to what is drawn instead of assuming PIN_SIZE fits.
        """
        llx, lly, urx, ury = rect
        w = min(cls.PIN_SIZE, urx - llx)
        h = min(cls.PIN_SIZE, ury - lly)
        if side == 'left':
            x0, y0 = llx, (lly + ury) / 2.0 - h / 2.0
        else:                                   # 'top'
            x0, y0 = (llx + urx) / 2.0 - w / 2.0, ury - h
        # GridFix truncates, so clamp both corners back into the bar.
        x0 = max(llx, GridFix(x0))
        y0 = max(lly, GridFix(y0))
        return Box(x0, y0,
                   min(urx, GridFix(x0 + w)), min(ury, GridFix(y0 + h)))

    def _paint_via_array(self, via_layer, llx, lly, urx, ury):
        """Paint an array of square vias within the given bounding box.

        Vias are VIA_CUT x VIA_CUT squares at VIA_SPACING edge-to-edge. The
        array is centered within the region. V1.a/Vn.a constrain the cut as
        both a minimum and a maximum, so a single via bar is not legal.
        """
        via_cut = self.VIA_CUT
        via_pitch = via_cut + self.VIA_SPACING
        region_w = urx - llx
        region_h = ury - lly
        if region_w < via_cut or region_h < via_cut:
            return
        nx = max(1, int((region_w - via_cut) / via_pitch) + 1)
        ny = max(1, int((region_h - via_cut) / via_pitch) + 1)
        array_w = (nx - 1) * via_pitch + via_cut
        array_h = (ny - 1) * via_pitch + via_cut
        x0 = llx + (region_w - array_w) / 2.0
        y0 = lly + (region_h - array_h) / 2.0
        for i in range(nx):
            for j in range(ny):
                vx = GridFix(x0 + i * via_pitch)
                vy = GridFix(y0 + j * via_pitch)
                dbCreateRect(self, via_layer,
                             Box(vx, vy, GridFix(vx + via_cut),
                                 GridFix(vy + via_cut)))

    def genLayout(self):
        # dx / dy are the drawn extents. The parameter names follow the
        # cap_cmomi axis convention (l -> X, w -> Y); see the class docstring.
        dx = self.l_um
        dy = self.w_um
        mmin = self.mmin
        mmax = self.mmax

        # Layer objects
        metal_layers = {}
        for m in range(mmin, mmax + 1):
            metal_layers[m] = Layer(self.METAL_NAMES[m], 'drawing')

        via_layers = {}
        for v in range(mmin, mmax):
            via_layers[v] = Layer(self.VIA_NAMES[v], 'drawing')

        recog_layer = Layer('Recog', 'momf')    # GDS 99/40
        text_layer = Layer('TEXT', 'drawing')

        # Track edge sizes from previous layer for via placement
        last_edge = {'l': 0, 'r': 0, 't': 0, 'b': 0}

        orient = 0  # 0 = fingers along Y, 1 = fingers along X
        for m in range(mmin, mmax + 1):
            rules = self.METAL_RULES[m]
            mw = rules['mw']
            ms = rules['ms']
            widem = rules['widem']
            extras = rules['extras']

            viabe = self.VIA1_BOT_ENC if m == 1 else 0.0

            # Extra spacing adjustments for run-length rules
            msxl = msxr = msxt = msxb = 0.0

            # Via parameters for the layer below
            viaw1 = self.VIA_WIDTH
            viabe1 = self.VIA1_BOT_ENC if m == 2 else 0.0
            viate1 = 0.0

            pitch = mw + ms
            viaw = self.VIA_WIDTH

            # -- Determine edge widths --
            if m == 1:
                edge_base = mw
                if mmax >= 2:
                    edge_base = viaw + 2 * viabe
                edgel = edger = edget = edgeb = edge_base
            elif m == 2:
                edge_base = viaw
                if mmin == 1:
                    edge_base = mw + viabe1
                edgel = edger = edget = edgeb = edge_base
            else:
                edgel = edger = edget = edgeb = viaw

            # -- Compute finger count and distribute remainder --
            if orient == 0:     # Fingers along Y, pitched along X
                wbase = edgel + edger
                nfxi = max(0, int((dx - (wbase + ms)) / pitch))
                xdelta = (dx - (nfxi * pitch + ms + wbase)) / 2.0
                edgel += xdelta
                edger += xdelta

                if edgel > widem:
                    msxl = extras
                    edgel -= msxl
                if edger > widem:
                    msxr = extras
                    edger -= msxr
            else:               # Fingers along X, pitched along Y
                lbase = edget + edgeb
                nfyi = max(0, int((dy - (lbase + ms)) / pitch))
                ydelta = (dy - (nfyi * pitch + ms + lbase)) / 2.0
                edget += ydelta
                edgeb += ydelta

                if edget > widem:
                    msxt = extras
                    edget -= msxt
                if edgeb > widem:
                    msxb = extras
                    edgeb -= msxb

            # -- Paint vias to layer below --
            if m > mmin:
                maxel = max(edgel, last_edge['l'])
                maxer = max(edger, last_edge['r'])
                maxeb = max(edgeb, last_edge['b'])
                maxet = max(edget, last_edge['t'])
                via_lyr = via_layers[m - 1]

                # Bottom via region
                vb_llx = GridFix(maxel + pitch)
                vb_urx = GridFix(dx - (maxer + pitch))
                vb_lly = GridFix(viabe1)
                vb_ury = GridFix(vb_lly + viaw1)
                if vb_urx > vb_llx:
                    self._paint_via_array(via_lyr,
                                          vb_llx, vb_lly, vb_urx, vb_ury)

                # Left via region
                vl_lly = GridFix(maxeb + ms)
                vl_ury = GridFix(dy - (maxet + pitch))
                vl_llx = GridFix(viabe1 + viate1)
                vl_urx = GridFix(vl_llx + viaw1)
                if vl_ury - vl_lly < viaw1:
                    vl_ury = GridFix(vl_lly + viaw1)
                if vl_ury > vl_lly:
                    self._paint_via_array(via_lyr,
                                          vl_llx, vl_lly, vl_urx, vl_ury)

                # Right via region
                vr_lly = GridFix(maxeb + pitch)
                vr_ury = GridFix(dy - (maxet + ms))
                vr_urx = GridFix(dx - viabe1)
                vr_llx = GridFix(vr_urx - viaw1)
                if vr_ury > vr_lly:
                    self._paint_via_array(via_lyr,
                                          vr_llx, vr_lly, vr_urx, vr_ury)

                # Top via region
                vt_ury = GridFix(dy - (viabe1 + viate1))
                vt_lly = GridFix(vt_ury - viaw1)
                vt_llx = GridFix(maxel + pitch)
                vt_urx = GridFix(dx - (maxer + ms))
                if vt_urx - vt_llx < viaw1:
                    vt_urx = GridFix(vt_llx + viaw1)
                if vt_urx > vt_llx:
                    self._paint_via_array(via_lyr,
                                          vt_llx, vt_lly, vt_urx, vt_ury)

            # -- Paint metal fingers --
            met = metal_layers[m]

            if orient == 0:     # Fingers along Y
                # Left edge (full height), PLUS side
                dbCreateRect(self, met, Box(0, 0, GridFix(edgel), dy))

                # Interior fingers
                for x in range(int(nfxi)):
                    f_llx = GridFix(x * pitch + edgel + msxl + ms)
                    f_urx = GridFix(f_llx + mw)
                    f_lly = 0.0
                    f_ury = dy

                    if x % 2 == 0:
                        # Shorten from top: joins the bottom bar (PLUS)
                        inset = edget + ms + msxt + viabe1
                        f_ury = GridFix(dy - inset)
                    else:
                        # Shorten from bottom: joins the top bar (MINUS)
                        inset = edgeb + ms + msxb + viabe1
                        f_lly = GridFix(inset)

                    dbCreateRect(self, met,
                                 Box(f_llx, f_lly, f_urx, f_ury))

                # Right edge (full height), MINUS side
                re_llx = GridFix(nfxi * pitch + edgel + msxl + msxr + ms)
                dbCreateRect(self, met, Box(re_llx, 0, GridFix(dx), dy))

                # Bottom connecting bar (PLUS side)
                bb_urx = GridFix(dx - (edger + ms + msxr))
                dbCreateRect(self, met,
                             Box(0, 0, bb_urx, GridFix(edgeb)))

                # Top connecting bar (MINUS side)
                tb_llx = GridFix(edgel + ms + msxl)
                dbCreateRect(self, met,
                             Box(tb_llx, GridFix(dy - edget), GridFix(dx), dy))

                # The two bars a pin may sit on for this orientation.
                plus_rect = (0.0, 0.0, GridFix(edgel), dy)
                minus_rect = (tb_llx, GridFix(dy - edget), GridFix(dx), dy)

            else:               # Fingers along X
                # Bottom edge (full width)
                dbCreateRect(self, met,
                             Box(0, 0, dx, GridFix(edgeb)))

                # Interior fingers
                for y in range(int(nfyi)):
                    f_llx = 0.0
                    f_urx = dx
                    f_lly = GridFix(y * pitch + edgeb + ms + msxb)
                    f_ury = GridFix(f_lly + mw)

                    if y % 2 == 0:
                        # Shorten from left: joins the right bar (MINUS)
                        inset = edgel + ms + msxl + viabe1
                        f_llx = GridFix(inset)
                    else:
                        # Shorten from right: joins the left bar (PLUS)
                        inset = edger + ms + msxr + viabe1
                        f_urx = GridFix(dx - inset)

                    dbCreateRect(self, met,
                                 Box(f_llx, f_lly, f_urx, f_ury))

                # Top edge (full width)
                te_lly = GridFix(nfyi * pitch + edgeb + ms + msxb + msxt)
                dbCreateRect(self, met, Box(0, te_lly, dx, dy))

                # Left connecting bar (PLUS side)
                lb_ury = GridFix(dy - (edget + ms + msxt))
                dbCreateRect(self, met,
                             Box(0, 0, GridFix(edgel), lb_ury))

                # Right connecting bar (MINUS side)
                rb_lly = GridFix(edgeb + ms + msxb)
                dbCreateRect(self, met,
                             Box(GridFix(dx - edger), rb_lly, dx, dy))

                # The two bars a pin may sit on for this orientation.
                plus_rect = (0.0, 0.0, GridFix(edgel), lb_ury)
                minus_rect = (0.0, te_lly, GridFix(dx), dy)

            # Remember where the pins may go on the layer that carries them.
            # The bars are only as thick as that layer's minimum metal width,
            # 0.16 on Metal1 against 0.20 above it, so a fixed-size pin box
            # hangs off the Metal1 bar and Pin.e fires on a single-layer stack.
            if m == mmax:
                top_plus_rect = plus_rect
                top_minus_rect = minus_rect

            # Save edge sizes for next layer's via placement
            last_edge = {'l': edgel, 'r': edger, 't': edget, 'b': edgeb}

            # Alternate orientation for next layer
            orient = 1 - orient

        # -- Recognition marker --
        # Recog.momf (99/40), one rectangle over the whole device. cap_cmomi
        # owns Recog.mom (99/39) by design, so this device carries its own
        # datatype: sharing one would make a single geometry extract twice.
        dbCreateRect(self, recog_layer, Box(0, 0, GridFix(dx), GridFix(dy)))

        # -- Filler keep-out --
        # The value of this device is defined by its metal geometry, and the
        # automatic density filler is free to drop dummy metal beside the
        # fingers or over the device on the metals it does not draw. LVS
        # matches topologically and does not compare the value, and DRC leaves
        # rule-compliant fill in place, so neither would flag the perturbation.
        # A fringe cap is more sensitive to this than an interdigitated one,
        # because dummy metal couples straight into the fringe field.
        nofiller_layer = Layer('NoMetFiller', 'drawing')
        dbCreateRect(self, nofiller_layer, Box(0, 0, GridFix(dx), GridFix(dy)))

        # -- Substrate isolation block --
        if self.subblock:
            pwb_layer = Layer('PWell', 'block')
            dbCreateRect(self, pwb_layer, Box(0, 0, GridFix(dx), GridFix(dy)))

        # -- Pins on top metal --
        # Both sit inside the marker: the LVS extractor keys ports on
        # (metal_pin AND marker), so a pin outside it yields fewer than two
        # ports and the device is dropped. CapMomExtractor sorts the two ports
        # by x, so PLUS (left) maps to mim_top and MINUS (top) to mim_btm,
        # the same order cap_cmomi produces.
        top_metal_name = self.METAL_NAMES[mmax]
        MkPin(self, 'PLUS', 1, self._pin_box(top_plus_rect, 'left'),
              top_metal_name)
        MkPin(self, 'MINUS', 2, self._pin_box(top_minus_rect, 'top'),
              top_metal_name)

        # -- Capacitance label (must match the simulation model, contract) --
        cval = self.areacap(mmin, mmax) * dx * dy
        label_text = 'cap_cmomf C={:.3f}fF'.format(cval)
        dbCreateLabel(self, text_layer, Point(0, GridFix(-0.5)),
                      label_text, 'centerLeft', 'R0',
                      Font.EURO_STYLE, 0.25)
