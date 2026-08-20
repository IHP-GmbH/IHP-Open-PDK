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
import math


class cap_cmomi(DloGen):
    """Interdigitated MoM (metal-oxide-metal) capacitor PCell.

    APPROXIMATE, pending cmos5l silicon: the area density AREACAP is TRANSFERRED
    from the sg13g2 characterisation (thin metals M1..M5) and re-used on the
    cmos5l M1..M4 stack by LAYER COUNT
    N = mmax-mmin+1; N=2 is additionally extrapolated. None are measured on
    cmos5l silicon. The single-side feed term is the exception: that
    characterisation's feed section is a different structure from the one drawn
    here, so CFEED_SLOPE
    and CFEED_END are fitted to this cell's own geometry. The C-label and the
    Verilog-A/OSDI model share this same formula, so they always agree, but
    treat the absolute value as an engineering estimate (re-fit ~3-6 months).

    Built on the four thin metals Metal1..Metal4 of this PDK; the metal stack
    is selected by mmin/mmax (any contiguous subset of Metal1..Metal4).

    Topology (brick-staggered interdigitated teeth):
      * Unit cell 0.840 x 0.890 um, tiled nx (X, finger length = l) by
        ny (Y, row stacking = w).
      * Every metal layer mmin..mmax carries the same pattern:
          - Continuous horizontal bars at y = j*UC_Y, j = 0..ny.
            Bar polarity alternates per row (j even -> PLUS, j odd -> MINUS).
          - Two teeth per (i, j) unit cell, staggered at X = 0 and 0.42, each
            attached to a bar of matching polarity.
      * Via stacks at every tooth/bar overlap, linking all layers of the same
        polarity column.

    Feed variants (the two characterised versions are 'double' and 'same'):
      * 'double' : opposite-side feed. PLUS pad left (even rows), MINUS pad right
                   (odd rows). Adds a feed capacitance Cfeed = CFEED2_SLOPE *
                   pad_len, measured on the drawn cell (see cap_cmomi.va). This
                   is the default configuration.
      * 'same'   : single-side feed. Two STACKED left pads on the same footprint:
                   PLUS on the mmax metal, MINUS on the (mmax-1) metal directly
                   below it, overlapping in x,y but with no via between them
                   (separate nets). That plate overlap is the feed capacitance
                   Cfeed, measured on this drawn overlap rather than taken from
                   the g2 characterisation, whose feed section is a different
                   structure (see cap_cmomi.va).
                   Requires mmax > mmin (>=2 metals) for the two stacked plates;
                   a single-metal stack has no second layer, so use 'double'
                   when mmin == mmax.
      * 'none'   : LAYOUT-ONLY bare array, no feed routing. The interdigitated
                   rows are NOT tied into two terminals (each finger pair is its
                   own net), so this is NOT a standalone 2-terminal device: it
                   extracts as a partial cap and is meant only for a user that
                   supplies external feed routing. Use 'double' or 'same' for a
                   complete, LVS-clean capacitor.
    """

    # ---------------------------------------------------------------
    # Layer tables: the four thin metals of this PDK.
    # ---------------------------------------------------------------
    METAL_NAMES = {1: 'Metal1', 2: 'Metal2', 3: 'Metal3', 4: 'Metal4'}
    VIA_NAMES   = {1: 'Via1', 2: 'Via2', 3: 'Via3'}
    METAL_MAX   = 4

    # ---------------------------------------------------------------
    # Geometry constants (um)
    # ---------------------------------------------------------------
    UC_X        = 0.840
    UC_Y        = 0.890
    FINGER_W    = 0.21
    T_BAR       = 0.21
    VIA_CUT     = 0.19
    ENDCAP_EXT  = 0.0
    # 0.575 leaves (UC_Y - T_BAR/2) - TOOTH_EXT = 0.21 um from the tooth tip to
    # the opposite-polarity bar = Mn.b (Metal2..4 min space). 0.58 would give
    # 0.205 um and fail Mn.b on Metal2/3/4.
    TOOTH_EXT   = 0.575
    # Along-tooth via offset. The foundry reference (MOM_92u_92u) vias each finger
    # on a 0.41 um pitch: one via at the bar/tooth base and one 0.41 um out along
    # the tooth toward the tip. We had drawn only the
    # base via, under-viaing the teeth by ~half. A full-wave (gds2palace) + electro-
    # static Palace campaign measured the missing tip vias at ~+13% (full-wave) /
    # ~+14% (electrostatic) capacitance, the same in our cell and the reference (the
    # earlier "~5%" estimate was wrong). TOOTH_VIA_OFF = 0.41 reproduces the reference
    # lattice exactly: 0.41 - VIA_CUT = 0.22 um to the base via = V1.b/Vn.b min via
    # space (the reference sits at this same limit), and TOOTH_EXT - TOOTH_VIA_OFF
    # - VIA_CUT/2 = 0.07 um of metal past the tip via = clears the 0.05 um endcap
    # enclosure (V1.c1/Mn.c1). Larger offsets shrink the tip endcap; smaller ones
    # break V1.b, so 0.41 is the only on-grid value that satisfies both.
    TOOTH_VIA_OFF = 0.41
    X_UP        = 0.0
    X_DOWN      = 0.42
    BAR_OVERHANG = 0.05

    # Origin offset (per-instance in genLayout): shifts every drawn coordinate so
    # (0,0) lands at the device centre. Class defaults keep _paint safe if it were
    # ever called before genLayout sets them.
    ox = 0.0
    oy = 0.0

    # Double feed (opposite side)
    FEED_GAP    = 0.30
    FEED_PAD_W  = 0.60
    FEED_EXT    = FEED_GAP + FEED_PAD_W     # 0.90
    LANDING_PAD = 0.31

    # Same-side (single-side) feed: two STACKED left pads.
    #   PLUS pad on the top metal (mmax) and MINUS pad on the metal below it
    #   (mmax-1), painted on the SAME footprint so they overlap in x,y but are
    #   NOT connected (no via) -> that plate overlap is the single-side feed
    #   capacitance. Even-row top-metal bars reach the PLUS pad; odd-row
    #   sub-metal bars reach the MINUS pad. The PLUS/MINUS pins sit stacked at
    #   the pad centre. LVS keeps them on separate nets by connecting each
    #   metal's pins ONLY to its own metal (per-layer, cap_cmomi_connections.lvs).
    SAME_PAD_GAP  = 0.30                        # gap from the core to the pad
    SAME_PAD_W    = 0.90                        # pad width (X)
    FEED_EXT_SAME = SAME_PAD_GAP + SAME_PAD_W   # 1.20  left extent of same feed

    # ---------------------------------------------------------------
    # Capacitance densities, indexed by LAYER COUNT N = mmax-mmin+1.
    # Characterised values: N=3 -> 0.82, N=4 -> 1.09 fF/um^2.
    # N=2 is extrapolated (~+0.27 fF/um^2 per thin layer); unmeasured.
    # ---------------------------------------------------------------
    AREACAP      = {2: 0.55, 3: 0.82, 4: 1.09}
    # Single-side feed, measured on the cell as drawn rather than transferred:
    # Cfeed = CFEED_SLOPE * pad_len + CFEED_END, with pad_len the drawn height of
    # the two stacked pads. No layer keying: those pads sit on the top two metals
    # whatever the stack is, and the measurement is flat for N>=3 (a two-metal
    # window reads ~3% lower, inside the term's own error bar). See cap_cmomi.va
    # for the provenance.
    CFEED_SLOPE  = 0.1625
    CFEED_END    = 0.0916
    # Opposite-side (double) feed, fitted on the via-fixed cell against the same
    # pad_len as the single-side term: Cfeed_dbl = CFEED2_SLOPE * pad_len.
    CFEED2_SLOPE = 0.152

    # ---------------------------------------------------------------
    # Parameter specs
    # ---------------------------------------------------------------
    @classmethod
    def defineParamSpecs(cls, specs):
        mchoice = list(range(1, cls.METAL_MAX + 1))
        # Default capacitance shown as a parameter (ref. cmim/rfcmim). Computed
        # from the shipped model on the default device; recomputed per geometry
        # in setupParams and for the label.
        #
        # On cmos5l this C field is a STATIC default: it does NOT track w/l/mmin/
        # mmax/feed live in the parameter dialog. The g2 twin (cmomi) updates C on
        # edit through a coerce callback (callbacks/cmomi_cb.tcl), but that
        # subsystem is not available here: cmos5l does not vendor its own PCell
        # framework, it symlinks pycell4klayout-api from the g2 tree, and that
        # shared copy ships the older dlo.py without coerce_parameters / callbacks
        # loading. Making C live on cmos5l is a shared-framework upgrade (it also
        # changes the in-tree g2), out of scope for this device. The live value is
        # always on the cell label instead (see _model_C_fF / genLayout). For the
        # same reason the effective-size fields Lx/Wy that g2 shows live are not
        # added here; the drawn size is on the cell label.
        c_def = eng_string(cls._model_C_fF(5.0, 5.0, 1, cls.METAL_MAX,
                                           'double') * 1e-15)

        def _ro():
            # Mark the just-added parameter read-only (KLayout only; the guard
            # keeps the non-KLayout branch harmless).
            try:
                decls = getattr(specs, '_paramDecls', None)
                if decls is None:
                    decls = specs.param_decls
                decls[-1].readonly = True
            except Exception:
                pass
#ifdef KLAYOUT
        # Editable inputs (write) first, then read-only derived/info fields, so
        # the dialog reads top-to-bottom as "what you set" then "what you get".
        specs('w', '5.0u', 'Width (Y), requested [um]',
              RangeConstraint(2e-6, 100e-6, USE_DEFAULT))
        specs('l', '5.0u', 'Length (X), requested [um]',
              RangeConstraint(2e-6, 100e-6, USE_DEFAULT))
        specs('mmin', 1, 'Bottom metal (1=M1 .. 4=M4)',
              ChoiceConstraint(mchoice))
        specs('mmax', 4, 'Top metal (1=M1 .. 4=M4)',
              ChoiceConstraint(mchoice))
        specs('feed', 'double',
              "Feed: double/same = 2-term cap; none = bare array",
              ChoiceConstraint(['none', 'same', 'double']))
        specs('subblock', False, 'Add substrate isolation block')
        # A read-only string acts as a visible divider before the derived
        # fields, since the dialog has no native section separator.
        specs('sep', '', '──────  read only  ──────'); _ro()
        specs('C', c_def, 'C [F], static default (live value on label)'); _ro()
        specs('model', 'cap_cmomi', 'Model name'); _ro()
#else
        # Editable inputs (write) first, then read-only derived/info fields, so
        # the dialog reads top-to-bottom as "what you set" then "what you get".
        specs('w', '5.0u', 'Width (Y), requested [um]',
              RangeConstraint(2e-6, 100e-6, USE_DEFAULT))
        specs('l', '5.0u', 'Length (X), requested [um]',
              RangeConstraint(2e-6, 100e-6, USE_DEFAULT))
        specs('mmin', 1, 'Bottom metal (1=M1 .. 4=M4)',
              ChoiceConstraint(mchoice))
        specs('mmax', 4, 'Top metal (1=M1 .. 4=M4)',
              ChoiceConstraint(mchoice))
        specs('feed', 'double',
              "Feed: double/same = 2-term cap; none = bare array",
              ChoiceConstraint(['none', 'same', 'double']))
        specs('subblock', False, 'Add substrate isolation block')
        # A read-only string acts as a visible divider before the derived
        # fields, since the dialog has no native section separator.
        specs('sep', '', '──────  read only  ──────'); _ro()
        specs('C', c_def, 'C [F], static default (live value on label)'); _ro()
        specs('model', 'cap_cmomi', 'Model name'); _ro()
#endif

    @classmethod
    def _model_C_fF(cls, l_um, w_um, mmin, mmax, feed):
        """Model capacitance (fF) for the 'C' parameter and the label.

        Must stay identical to cap_cmomi.va. The active area bills the ny rows
        this cell DRAWS (each has a counter electrode); the feed term is fitted
        against pad_len, the drawn pad height. The earlier billing subtracted a
        row because the characterised structure ends in single fingers that
        couple to nothing; nothing here is drawn that way.
        """
        if mmax < mmin:
            mmax = mmin
        nx = max(1, int(l_um / cls.UC_X + 1e-6))
        ny = max(1, int(w_um / cls.UC_Y + 1e-6) - 1) + 1
        n_clamped = min(cls.METAL_MAX, max(2, mmax - mmin + 1))
        c_active = cls.AREACAP[n_clamped] * (nx * cls.UC_X) * (ny * cls.UC_Y)
        pad_len = ny * cls.UC_Y + 2 * cls.T_BAR
        if feed == 'same':
            return c_active + cls.CFEED_SLOPE * pad_len + cls.CFEED_END
        if feed == 'double':
            return c_active + cls.CFEED2_SLOPE * pad_len
        return c_active

    def setupParams(self, params):
        self.params = params
        # PDF axis convention: length -> X (finger length), width -> Y (rows).
        self.w_um = Numeric(params['w']) * 1e6      # width  -> Y
        self.l_um = Numeric(params['l']) * 1e6      # length -> X
        self.mmin = int(params['mmin'])
        self.mmax = int(params['mmax'])
        self.feed = str(params['feed'])
        self.subblock = bool(params['subblock'])
        if self.mmax < self.mmin:
            self.mmax = self.mmin

    # ---------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------
    def _paint(self, layer, x0, y0, x1, y1):
        # self.ox/self.oy centre the cell on (0,0); set in genLayout before use.
        dbCreateRect(self, layer,
                     Box(GridFix(x0 + self.ox), GridFix(y0 + self.oy),
                         GridFix(x1 + self.ox), GridFix(y1 + self.oy)))

    def _bar_x_range(self, m, j, m_top, dev_w):
        """Return (xL, xR) for the horizontal bar at row j on layer m."""
        if self.feed == 'double':
            if j % 2 == 0:                      # PLUS -> LEFT pad
                return (-self.FEED_EXT, dev_w + self.BAR_OVERHANG)
            else:                               # MINUS -> RIGHT pad
                return (-self.BAR_OVERHANG, dev_w + self.FEED_EXT)
        if self.feed == 'same':
            # PLUS (even rows) reach the top-metal pad; MINUS (odd rows) reach
            # the sub-metal pad stacked directly below it. Only the carrying
            # metal extends out to the pad; the rest of the row stack stays in
            # the core (still one net through the core via stacks).
            sub = m_top - 1 if m_top > self.mmin else m_top
            if (j % 2 == 0) and m == m_top:                 # PLUS -> top pad
                return (-self.FEED_EXT_SAME, dev_w + self.BAR_OVERHANG)
            if (j % 2 == 1) and m == sub:                   # MINUS -> sub pad
                return (-self.FEED_EXT_SAME, dev_w + self.BAR_OVERHANG)
            return (-self.BAR_OVERHANG, dev_w + self.BAR_OVERHANG)
        # feed == 'none'
        return (-self.BAR_OVERHANG, dev_w + self.BAR_OVERHANG)

    def _draw_bars_and_teeth(self, mlayer, m, m_top, nx, ny, dev_w):
        half_bar = self.T_BAR / 2.0
        for j in range(0, ny + 1):
            yc = j * self.UC_Y
            xL, xR = self._bar_x_range(m, j, m_top, dev_w)
            self._paint(mlayer, xL, yc - half_bar, xR, yc + half_bar)
        for i in range(nx):
            for j in range(ny):
                # UP-tooth attached to bar at j*UC_Y
                x_l = i * self.UC_X + self.X_UP
                x_r = x_l + self.FINGER_W
                y_b = j * self.UC_Y - self.ENDCAP_EXT
                y_t = j * self.UC_Y + self.TOOTH_EXT
                self._paint(mlayer, x_l, y_b, x_r, y_t)
                # DOWN-tooth attached to bar at (j+1)*UC_Y
                x_l = i * self.UC_X + self.X_DOWN
                x_r = x_l + self.FINGER_W
                y_b = (j + 1) * self.UC_Y - self.TOOTH_EXT
                y_t = (j + 1) * self.UC_Y + self.ENDCAP_EXT
                self._paint(mlayer, x_l, y_b, x_r, y_t)

    def _draw_core_vias(self, vlayer, nx, ny):
        half_fw = self.FINGER_W / 2.0
        half_via = self.VIA_CUT / 2.0
        off = self.TOOTH_VIA_OFF

        def via(xc, yc):
            self._paint(vlayer, xc - half_via, yc - half_via,
                        xc + half_via, yc + half_via)

        for i in range(nx):
            for j in range(ny):
                # UP-tooth (rooted at bar j, extends up): base via at the bar,
                # tooth via 0.41 um out toward the tip (reference finger pitch).
                xc = i * self.UC_X + self.X_UP + half_fw
                y_base = j * self.UC_Y
                via(xc, y_base)
                via(xc, y_base + off)
                # DOWN-tooth (rooted at bar j+1, extends down): base via at the
                # bar, tooth via 0.41 um out toward the tip.
                xc = i * self.UC_X + self.X_DOWN + half_fw
                y_base = (j + 1) * self.UC_Y
                via(xc, y_base)
                via(xc, y_base - off)

    def _draw_feed_double(self, m_bot, m_top, ny, dev_w,
                          metal_layers, via_layers):
        top_metal = metal_layers[m_top]
        feed_width = ny * self.UC_Y + 0.64
        all_bars_mid = (ny * self.UC_Y) / 2.0
        pad_y_lo = all_bars_mid - feed_width / 2.0
        pad_y_hi = all_bars_mid + feed_width / 2.0
        # PLUS pad (LEFT)
        self._paint(top_metal, -self.FEED_EXT, pad_y_lo,
                    -self.FEED_GAP, pad_y_hi)
        # MINUS pad (RIGHT)
        self._paint(top_metal, dev_w + self.FEED_GAP, pad_y_lo,
                    dev_w + self.FEED_EXT, pad_y_hi)

        half_via = self.VIA_CUT / 2.0
        half_lp = self.LANDING_PAD / 2.0
        plus_pad_cx = (-self.FEED_EXT + -self.FEED_GAP) / 2.0
        minus_pad_cx = dev_w + (self.FEED_GAP + self.FEED_EXT) / 2.0
        for j in range(0, ny + 1):
            xc = plus_pad_cx if (j % 2 == 0) else minus_pad_cx
            yc = j * self.UC_Y
            for v in range(m_bot, m_top):
                self._paint(via_layers[v], xc - half_via, yc - half_via,
                            xc + half_via, yc + half_via)
            for m in range(m_bot, m_top):
                self._paint(metal_layers[m], xc - half_lp, yc - half_lp,
                            xc + half_lp, yc + half_lp)
        return pad_y_lo, pad_y_hi

    def _draw_feed_same(self, m_bot, m_top, ny, dev_w,
                        metal_layers, via_layers):
        # Two STACKED vertical left pads on the SAME footprint:
        #   PLUS pad on the top metal, MINUS pad on the metal below it. They
        # overlap fully in x,y but carry no via between them (separate nets); the
        # plate overlap is the single-side feed capacitance. Each pad contacts
        # only the bars of its polarity on its own metal (even-row top-metal bars
        # reach the PLUS pad, odd-row sub-metal bars reach the MINUS pad); the
        # rest of each row's stack stays in the core. The pads extend past the
        # array in Y so the stacked pins sit fully on pad metal.
        sub = m_top - 1 if m_top > m_bot else m_top
        y0 = -self.T_BAR
        y1 = ny * self.UC_Y + self.T_BAR
        x_lo = -self.FEED_EXT_SAME
        x_hi = -self.SAME_PAD_GAP
        self._paint(metal_layers[m_top], x_lo, y0, x_hi, y1)    # PLUS  (top metal)
        self._paint(metal_layers[sub],   x_lo, y0, x_hi, y1)    # MINUS (sub metal)
        return y0, y1

    def _place_pins(self, m_top, dev_w, ny, feed_pad_yrange, metal_layers):
        top_metal_name = self.METAL_NAMES[m_top]
        sub_idx = m_top - 1 if m_top > self.mmin else m_top
        sub_metal_name = self.METAL_NAMES[sub_idx]
        half_bar = self.T_BAR / 2.0
        pin_h = self.T_BAR
        pin_w = self.techparams['Mn_a']    # min metal width, was 0.20

        def B(x0, y0, x1, y1):
            # Same centring offset as _paint, so pins sit on their drawn pads.
            return Box(GridFix(x0 + self.ox), GridFix(y0 + self.oy),
                       GridFix(x1 + self.ox), GridFix(y1 + self.oy))

        if self.feed == 'double':
            pad_y_lo, pad_y_hi = feed_pad_yrange
            pad_cy = (pad_y_lo + pad_y_hi) / 2.0
            plus_cx = (-self.FEED_EXT + -self.FEED_GAP) / 2.0
            plus_box = B(plus_cx - pin_w / 2.0, pad_cy - pin_h / 2.0,
                         plus_cx + pin_w / 2.0, pad_cy + pin_h / 2.0)
            MkPin(self, 'PLUS', 1, plus_box, top_metal_name)
            minus_cx = dev_w + (self.FEED_GAP + self.FEED_EXT) / 2.0
            minus_box = B(minus_cx - pin_w / 2.0, pad_cy - pin_h / 2.0,
                          minus_cx + pin_w / 2.0, pad_cy + pin_h / 2.0)
            MkPin(self, 'MINUS', 2, minus_box, top_metal_name)
            return

        if self.feed == 'same':
            # PLUS pin on the top-metal pad and MINUS pin on the sub-metal pad,
            # STACKED at the same pad centre (they overlap in x,y on adjacent
            # metals). LVS keeps them on separate nets because each metal's pins
            # connect only to that metal (per-layer, cap_cmomi_connections.lvs); a
            # symmetric cap is orientation/terminal-swap invariant, so the two
            # terminals need not be told apart by position.
            pad_cx = (-self.FEED_EXT_SAME + -self.SAME_PAD_GAP) / 2.0
            pad_cy = (ny * self.UC_Y) / 2.0
            pin_box = B(pad_cx - pin_w / 2.0, pad_cy - pin_h / 2.0,
                        pad_cx + pin_w / 2.0, pad_cy + pin_h / 2.0)
            MkPin(self, 'PLUS', 1, pin_box, top_metal_name)
            MkPin(self, 'MINUS', 2, pin_box, sub_metal_name)
            return

        # feed == 'none': pins inside the outer top-metal bars.
        plus_x0 = 0.0
        plus_box = B(plus_x0, 0 - half_bar, plus_x0 + pin_w, 0 + half_bar)
        MkPin(self, 'PLUS', 1, plus_box, top_metal_name)
        minus_x0 = dev_w - pin_w
        minus_box = B(minus_x0, ny * self.UC_Y - half_bar,
                      minus_x0 + pin_w, ny * self.UC_Y + half_bar)
        MkPin(self, 'MINUS', 2, minus_box, top_metal_name)

    # ---------------------------------------------------------------
    # Main
    # ---------------------------------------------------------------
    def genLayout(self):
        self.techparams = self.tech.getTechParams()
        # Geometry that is a DRC minimum is read from the tech file rather than
        # hardcoded (Via1..Via3 share the thin-via rules). The class literals
        # above stay as documented fallbacks; these overrides are authoritative:
        #   via cut         = V1_a                 (0.19)
        #   tooth via pitch = V1_a + V1_b          (cut + min via space -> the
        #                                           foundry finger lattice, 0.41)
        #   tooth extension = UC_Y - T_BAR/2 - Mn_b (leaves Mn_b from the tip to
        #                                            the opposite bar, 0.575)
        # pin width (Mn_a) is applied in _place_pins.
        tp = self.techparams
        self.VIA_CUT = tp['V1_a']
        self.TOOTH_VIA_OFF = self.VIA_CUT + tp['V1_b']
        self.TOOTH_EXT = self.UC_Y - self.T_BAR / 2.0 - tp['Mn_b']

        # Active unit-cell counts (PDF: length -> X, width -> Y).
        # A drawn dimension that is a non-integer exact multiple of the pitch
        # (e.g. l=8.4um = 10*UC_X) can round-trip through *1e6 to one ULP below
        # the integer, where a bare floor/`//` lands on k or k-1 depending on the
        # toolchain. Snap to the pitch grid with a sub-grid epsilon before the
        # floor so the layout, this C-label, and the simulation model agree on
        # the geometric count k for every geometry. Keep this identical to the
        # ngspice/Verilog-A model (floor(x/pitch + 1e-6)).
        nx_active = max(1, int(self.l_um / self.UC_X + 1e-6))
        ny_active = max(1, int(self.w_um / self.UC_Y + 1e-6) - 1)
        nx = nx_active
        ny = ny_active + 1
        dev_w = GridFix(nx * self.UC_X)     # X extent (finger length)
        dev_l = GridFix(ny * self.UC_Y)     # Y extent (row stacking)

        # Centre the cell on its own origin: shift every drawn coordinate so
        # (0,0) is the device centre. Y is symmetric about the core mid-row for
        # every feed; X is symmetric except single-side 'same', whose feed sits
        # only on the left, so use its real bbox centre there. All offsets land
        # on the 5 nm grid, so GridFix after the shift stays exact.
        self.oy = -(ny * self.UC_Y) / 2.0
        if self.feed == 'same':
            self.ox = -((-self.FEED_EXT_SAME) + (dev_w + self.BAR_OVERHANG)) / 2.0
        else:
            self.ox = -dev_w / 2.0

        m_top = self.mmax
        m_bot = self.mmin

        metal_layers = {m: Layer(self.METAL_NAMES[m], 'drawing')
                        for m in range(m_bot, m_top + 1)}
        via_layers = {v: Layer(self.VIA_NAMES[v], 'drawing')
                      for v in range(m_bot, m_top)}
        recog_layer = Layer('Recog', 'mom')            # GDS 99/39
        text_layer = Layer('TEXT', 'drawing')

        # 1) Bars + teeth on every layer
        for m in range(m_bot, m_top + 1):
            self._draw_bars_and_teeth(metal_layers[m], m, m_top,
                                      nx, ny, dev_w)

        # 2) Core via stacks
        for v in range(m_bot, m_top):
            self._draw_core_vias(via_layers[v], nx, ny)

        # 3) Feed structures
        feed_pad_yrange = None
        if self.feed == 'double':
            feed_pad_yrange = self._draw_feed_double(
                m_bot, m_top, ny, dev_w, metal_layers, via_layers)
        elif self.feed == 'same':
            feed_pad_yrange = self._draw_feed_same(
                m_bot, m_top, ny, dev_w, metal_layers, via_layers)

        # 4) Recognition marker bbox (full extent including feed)
        y_lo = -self.ENDCAP_EXT
        y_hi = dev_l + self.ENDCAP_EXT
        if self.feed == 'double':
            x_lo = -self.FEED_EXT
            x_hi = dev_w + self.FEED_EXT
        elif self.feed == 'same':
            x_lo = -self.FEED_EXT_SAME
            x_hi = dev_w + self.BAR_OVERHANG
        else:
            x_lo = -self.BAR_OVERHANG
            x_hi = dev_w + self.BAR_OVERHANG
        # The feed pads (and the PLUS/MINUS pins placed on them) can extend
        # beyond the active rows in Y. The marker must enclose those pins:
        # the LVS extractor keys ports on (metal_pin AND marker), so a pin
        # sitting outside the marker yields <2 ports and the device is dropped.
        if feed_pad_yrange is not None:
            pad_y_lo, pad_y_hi = feed_pad_yrange
            y_lo = min(y_lo, pad_y_lo)
            y_hi = max(y_hi, pad_y_hi)
        self._paint(recog_layer, x_lo, y_lo, x_hi, y_hi)

        # 5) Filler keep-out over the full device.
        # The cap_cmomi value is defined by the metal geometry. Automatic dummy
        # metal fill (density fill) landing on or beside the fingers, or over the
        # device on the upper metals the cap does not draw, perturbs the real
        # capacitance. LVS matches this device topologically and does not compare
        # its value, and DRC leaves rule-compliant fill untouched, so neither
        # catches the perturbation. NoMetFiller (160/0) over the device bbox is
        # honoured by every metal and topmetal filler and excludes all metal
        # fill in one marker.
        nofiller_layer = Layer('NoMetFiller', 'drawing')
        self._paint(nofiller_layer, x_lo, y_lo, x_hi, y_hi)

        # 6) Substrate isolation block
        if self.subblock:
            pwb_layer = Layer('PWell', 'block')
            self._paint(pwb_layer, x_lo, y_lo, x_hi, y_hi)

        # 7) Pins
        self._place_pins(m_top, dev_w, ny, feed_pad_yrange, metal_layers)

        # 8) Device name + capacitance label, two lines centred inside the cell
        # (ref. cmim/rfcmim). The value must match the simulation model; the
        # billing lives in _model_C_fF, kept identical to cap_cmomi.va.
        c_total = self._model_C_fF(self.l_um, self.w_um,
                                   self.mmin, self.mmax, self.feed)
        labelpos = Point(GridFix(dev_w / 2.0 + self.ox),
                         GridFix(ny * self.UC_Y / 2.0 + self.oy))
        label_h = min(self.l_um, self.w_um) / 10.0
        dbCreateLabel(self, text_layer, labelpos,
                      'C={:.3f}fF'.format(c_total), 'lowerCenter', 'R0',
                      Font.EURO_STYLE, label_h)
        dbCreateLabel(self, text_layer, labelpos, 'cap_cmomi',
                      'upperCenter', 'R0', Font.EURO_STYLE, label_h)
