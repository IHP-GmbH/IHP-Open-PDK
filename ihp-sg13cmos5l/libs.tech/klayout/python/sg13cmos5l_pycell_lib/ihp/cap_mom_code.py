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


class cap_mom(DloGen):
    """Interdigitated MoM (metal-oxide-metal) capacitor PCell.

    Source model: V. Muhlhaus, "MOM model development notes" (IHP, Nov 2022).
    Built on the four thin metals Metal1..Metal4 of this PDK; the metal stack
    is selected by mmin/mmax (any contiguous subset of Metal1..Metal4). Model
    coefficients (AREACAP / CFEED_PER_UM) are reused by LAYER COUNT
    N = mmax-mmin+1: Metal1..Metal4 are the physical thin-metal layers the
    model was characterised on, so the per-count densities apply directly.

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
                   (odd rows). Cfeed ~ 0. This is the reference configuration.
      * 'same'   : single-side feed. Two non-overlapping left rails: PLUS on the
                   mmax metal (far), MINUS on the (mmax-1) metal (near). Even-row
                   top-metal bars cross OVER the near rail on a different layer
                   (no via) -> that controlled overlap is the feed capacitance
                   Cfeed ~ (active_y*UC_Y + 0.64) * cfeed_per_um.
                   Requires mmax > mmin (>=2 metals) for the near/far rails; a
                   single-metal stack has no second layer for the crossover, so
                   use 'double' when mmin == mmax.
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
    X_UP        = 0.0
    X_DOWN      = 0.42
    BAR_OVERHANG = 0.05

    # Double feed (opposite side)
    FEED_GAP    = 0.30
    FEED_PAD_W  = 0.60
    FEED_EXT    = FEED_GAP + FEED_PAD_W     # 0.90
    LANDING_PAD = 0.31

    # Same-side (single-side) feed: two NON-overlapping left rails.
    #   PLUS rail on the top metal (far left), MINUS rail on the metal below it
    #   (near left). Both terminals exit on the same side. The even-row (PLUS)
    #   top-metal bars cross OVER the MINUS rail on a different layer with no via
    #   -> that controlled overlap is exactly the single-side feed capacitance.
    #   Pins are placed in single-metal zones so the LVS 'ports connect to all
    #   metals' scheme cannot bridge the two nets (see cap_mom_extractor.lvs).
    SAME_RAIL_W    = 0.60
    SAME_MINUS_XHI = -0.30
    SAME_MINUS_XLO = SAME_MINUS_XHI - SAME_RAIL_W    # -0.90  MINUS rail (sub metal)
    SAME_RAIL_GAP  = 0.30
    SAME_PLUS_XHI  = SAME_MINUS_XLO - SAME_RAIL_GAP  # -1.20
    SAME_PLUS_XLO  = SAME_PLUS_XHI - SAME_RAIL_W     # -1.80  PLUS rail (top metal)
    FEED_EXT_SAME  = -SAME_PLUS_XLO                  # 1.80   left extent of same feed

    # ---------------------------------------------------------------
    # Capacitance densities, indexed by LAYER COUNT N = mmax-mmin+1.
    # Characterised values: N=3 -> 0.82, N=4 -> 1.09 fF/um^2.
    # N=2 is extrapolated (~+0.27 fF/um^2 per thin layer); unmeasured.
    # ---------------------------------------------------------------
    AREACAP      = {2: 0.55, 3: 0.82, 4: 1.09}
    CFEED_PER_UM = {2: 0.70, 3: 0.97, 4: 1.28}

    # ---------------------------------------------------------------
    # Parameter specs
    # ---------------------------------------------------------------
    @classmethod
    def defineParamSpecs(cls, specs):
        mchoice = list(range(1, cls.METAL_MAX + 1))
#ifdef KLAYOUT
        specs('model', 'cap_mom', 'Model name')
        specs('w', '5.0u', 'Width (Y, row stacking)',
              RangeConstraint(2e-6, 100e-6, USE_DEFAULT))
        specs('l', '5.0u', 'Length (X, finger length)',
              RangeConstraint(2e-6, 100e-6, USE_DEFAULT))
        specs('mmin', 1, 'Bottom metal (1=M1 .. 4=M4)',
              ChoiceConstraint(mchoice))
        specs('mmax', 4, 'Top metal (1=M1 .. 4=M4)',
              ChoiceConstraint(mchoice))
        specs('feed', 'double',
              "Feed topology: 'double'/'same' = complete 2-terminal cap, "
              "'none' = bare array (layout only)",
              ChoiceConstraint(['none', 'same', 'double']))
        specs('subblock', 0, 'Add substrate isolation block',
              ChoiceConstraint([0, 1]))
#else
        specs('model', 'cap_mom', 'Model name')
        specs('w', '5.0u', 'Width (Y, row stacking)',
              RangeConstraint(2e-6, 100e-6, USE_DEFAULT))
        specs('l', '5.0u', 'Length (X, finger length)',
              RangeConstraint(2e-6, 100e-6, USE_DEFAULT))
        specs('mmin', 1, 'Bottom metal (1=M1 .. 4=M4)',
              ChoiceConstraint(mchoice))
        specs('mmax', 4, 'Top metal (1=M1 .. 4=M4)',
              ChoiceConstraint(mchoice))
        specs('feed', 'double',
              "Feed topology: 'double'/'same' = complete 2-terminal cap, "
              "'none' = bare array (layout only)",
              ChoiceConstraint(['none', 'same', 'double']))
        specs('subblock', 0, 'Add substrate isolation block',
              ChoiceConstraint([0, 1]))
#endif

    def setupParams(self, params):
        self.params = params
        # PDF axis convention: length -> X (finger length), width -> Y (rows).
        self.w_um = Numeric(params['w']) * 1e6      # width  -> Y
        self.l_um = Numeric(params['l']) * 1e6      # length -> X
        self.mmin = int(params['mmin'])
        self.mmax = int(params['mmax'])
        self.feed = str(params['feed'])
        self.subblock = int(params['subblock'])
        if self.mmax < self.mmin:
            self.mmax = self.mmin

    # ---------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------
    def _paint(self, layer, x0, y0, x1, y1):
        dbCreateRect(self, layer,
                     Box(GridFix(x0), GridFix(y0),
                         GridFix(x1), GridFix(y1)))

    def _bar_x_range(self, m, j, m_top, dev_w):
        """Return (xL, xR) for the horizontal bar at row j on layer m."""
        if self.feed == 'double':
            if j % 2 == 0:                      # PLUS -> LEFT pad
                return (-self.FEED_EXT, dev_w + self.BAR_OVERHANG)
            else:                               # MINUS -> RIGHT pad
                return (-self.BAR_OVERHANG, dev_w + self.FEED_EXT)
        if self.feed == 'same':
            # PLUS (even rows) reach the far top-metal rail; MINUS (odd rows)
            # reach the near sub-metal rail. Only the carrying metal extends out;
            # the rest of the row stack stays in the core (still one net through
            # the core via stacks).
            sub = m_top - 1 if m_top > self.mmin else m_top
            if (j % 2 == 0) and m == m_top:                 # PLUS -> far rail
                return (self.SAME_PLUS_XLO, dev_w + self.BAR_OVERHANG)
            if (j % 2 == 1) and m == sub:                   # MINUS -> near rail
                return (self.SAME_MINUS_XLO, dev_w + self.BAR_OVERHANG)
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
        for i in range(nx):
            for j in range(ny):
                xc = i * self.UC_X + self.X_UP + half_fw
                yc = j * self.UC_Y
                self._paint(vlayer, xc - half_via, yc - half_via,
                            xc + half_via, yc + half_via)
                xc = i * self.UC_X + self.X_DOWN + half_fw
                yc = (j + 1) * self.UC_Y
                self._paint(vlayer, xc - half_via, yc - half_via,
                            xc + half_via, yc + half_via)

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
        # Two non-overlapping vertical left rails, each on its own metal:
        #   PLUS rail on the top metal (far left), MINUS rail on the metal below.
        # A rail contacts every bar of its polarity on the same metal (no vias
        # needed): even-row top-metal bars reach the PLUS rail, odd-row sub-metal
        # bars reach the MINUS rail. The rails extend past the array in Y so the
        # PLUS/MINUS pins have room to sit fully on rail metal.
        sub = m_top - 1 if m_top > m_bot else m_top
        y0 = -self.T_BAR
        y1 = ny * self.UC_Y + self.T_BAR
        self._paint(metal_layers[m_top],
                    self.SAME_PLUS_XLO, y0, self.SAME_PLUS_XHI, y1)
        self._paint(metal_layers[sub],
                    self.SAME_MINUS_XLO, y0, self.SAME_MINUS_XHI, y1)
        return y0, y1

    def _place_pins(self, m_top, dev_w, ny, feed_pad_yrange, metal_layers):
        top_metal_name = self.METAL_NAMES[m_top]
        sub_idx = m_top - 1 if m_top > self.mmin else m_top
        sub_metal_name = self.METAL_NAMES[sub_idx]
        half_bar = self.T_BAR / 2.0
        pin_h = self.T_BAR
        pin_w = 0.20

        if self.feed == 'double':
            pad_y_lo, pad_y_hi = feed_pad_yrange
            pad_cy = (pad_y_lo + pad_y_hi) / 2.0
            plus_cx = (-self.FEED_EXT + -self.FEED_GAP) / 2.0
            plus_box = Box(GridFix(plus_cx - pin_w / 2.0),
                           GridFix(pad_cy - pin_h / 2.0),
                           GridFix(plus_cx + pin_w / 2.0),
                           GridFix(pad_cy + pin_h / 2.0))
            MkPin(self, 'PLUS', 1, plus_box, top_metal_name)
            minus_cx = dev_w + (self.FEED_GAP + self.FEED_EXT) / 2.0
            minus_box = Box(GridFix(minus_cx - pin_w / 2.0),
                            GridFix(pad_cy - pin_h / 2.0),
                            GridFix(minus_cx + pin_w / 2.0),
                            GridFix(pad_cy + pin_h / 2.0))
            MkPin(self, 'MINUS', 2, minus_box, top_metal_name)
            return

        if self.feed == 'same':
            # PLUS pin on the top-metal rail at an even row (row 0); MINUS pin on
            # the sub-metal rail at an odd row (row 1). Distinct metals AND
            # distinct rails (non-overlapping X) put each pin in a single-metal
            # zone, so the LVS 'ports connect to all metals' scheme keeps the two
            # terminals on separate nets.
            plus_cx = (self.SAME_PLUS_XLO + self.SAME_PLUS_XHI) / 2.0
            minus_cx = (self.SAME_MINUS_XLO + self.SAME_MINUS_XHI) / 2.0
            plus_cy = 0.0                       # row 0 (even -> PLUS)
            minus_cy = self.UC_Y                # row 1 (odd  -> MINUS)
            plus_box = Box(GridFix(plus_cx - pin_w / 2.0),
                           GridFix(plus_cy - pin_h / 2.0),
                           GridFix(plus_cx + pin_w / 2.0),
                           GridFix(plus_cy + pin_h / 2.0))
            MkPin(self, 'PLUS', 1, plus_box, top_metal_name)
            minus_box = Box(GridFix(minus_cx - pin_w / 2.0),
                            GridFix(minus_cy - pin_h / 2.0),
                            GridFix(minus_cx + pin_w / 2.0),
                            GridFix(minus_cy + pin_h / 2.0))
            MkPin(self, 'MINUS', 2, minus_box, sub_metal_name)
            return

        # feed == 'none': pins inside the outer top-metal bars.
        plus_x0 = 0.0
        plus_box = Box(GridFix(plus_x0), GridFix(0 - half_bar),
                       GridFix(plus_x0 + pin_w), GridFix(0 + half_bar))
        MkPin(self, 'PLUS', 1, plus_box, top_metal_name)
        minus_x0 = dev_w - pin_w
        minus_box = Box(GridFix(minus_x0), GridFix(ny * self.UC_Y - half_bar),
                        GridFix(minus_x0 + pin_w),
                        GridFix(ny * self.UC_Y + half_bar))
        MkPin(self, 'MINUS', 2, minus_box, top_metal_name)

    # ---------------------------------------------------------------
    # Main
    # ---------------------------------------------------------------
    def genLayout(self):
        # Active unit-cell counts (PDF: length -> X, width -> Y).
        nx_active = max(1, int(self.l_um // self.UC_X))
        ny_active = max(1, int(self.w_um // self.UC_Y) - 1)
        nx = nx_active
        ny = ny_active + 1
        dev_w = GridFix(nx * self.UC_X)     # X extent (finger length)
        dev_l = GridFix(ny * self.UC_Y)     # Y extent (row stacking)

        m_top = self.mmax
        m_bot = self.mmin
        n_layers = m_top - m_bot + 1

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

        # 5) Substrate isolation block
        if self.subblock:
            pwb_layer = Layer('PWell', 'block')
            self._paint(pwb_layer, x_lo, y_lo, x_hi, y_hi)

        # 6) Pins
        self._place_pins(m_top, dev_w, ny, feed_pad_yrange, metal_layers)

        # 7) Capacitance label (must match the simulation model, contract).
        n_clamped = min(self.METAL_MAX, max(2, n_layers))
        areacap = self.AREACAP[n_clamped]
        active_area = nx_active * self.UC_X * ny_active * self.UC_Y
        c_active = areacap * active_area
        if self.feed == 'same':
            cfeed = self.CFEED_PER_UM[n_clamped]
            feed_width = ny_active * self.UC_Y + 0.64
            c_total = c_active + cfeed * feed_width
        else:
            c_total = c_active
        label_text = 'cap_mom C={:.3f}fF'.format(c_total)
        dbCreateLabel(self, text_layer,
                      Point(GridFix(x_lo), GridFix(y_lo - 0.5)),
                      label_text, 'centerLeft', 'R0',
                      Font.EURO_STYLE, 0.25)
