# =========================================================================================
# Copyright 2026 IHP PDK Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========================================================================================

"""Regression for issue #1266: HV gate-poly end caps outside Activ.

Run from the repository root:
    python3 ihp-common/libs.tech/klayout/tech/drc/testing/test_gat_b1_endcaps.py

The expected errors are defined independently of the DRC output. Minimal
fixtures omit substrate taps; only Gat.b1 is asserted. --run-dir preserves
GDS fixtures, expected end-cap markers, actual reports and tool logs.
"""
from pathlib import Path
import argparse
import tempfile
import subprocess
import unittest
import xml.etree.ElementTree as ET
import klayout.db as kdb
import klayout.rdb as rdb

ROOT = Path(__file__).resolve().parents[6]
PDKS = ('sg13g2', 'sg13cmos5l')
OUT = None


def generate(name, gap, hv=True, active=True, side=False):
    """Write an end-cap or same-Activ spacing fixture; dimensions are in nm."""
    layout = kdb.Layout()
    layout.dbu = 0.001
    cell = layout.create_cell(name)
    second_y = 1360 + gap
    shapes = [
        (44, (-1000, -1500, 3000, 4000)),
        (1, (0, 0, 2000, 1000)),
        (5, (750, -180, 1250, 1180)),
        (1, (0, second_y, 2000, second_y + 1000)),
        (5, (750, second_y - 180, 1250, second_y + 1180)),
    ]
    if side:
        shapes = [(44, (-1000, -1500, 4000, 4000)),
                  (1, (0, 0, 3000, 1000)),
                  (5, (500, -180, 1000, 1180)),
                  (5, (1000 + gap, -180, 1500 + gap, 1180))]
    for layer, coords in shapes:
        if (layer == 44 and not hv) or (layer == 1 and not active):
            continue
        cell.shapes(layout.layer(layer, 0)).insert(kdb.Box(*coords))
    path = OUT / f'{name}.gds'
    layout.write(str(path))
    # Independent expected marker, defined directly from the known poly gap.
    expected = rdb.ReportDatabase('Expected Gat.b1 (rule-book reference, not deck output)')
    category = expected.create_category('Gat.b1')
    report_cell = expected.create_cell(name)
    if gap < 250 and hv and active:
        item = expected.create_item(report_cell.rdb_id(), category.rdb_id())
        if side:
            item.add_value(kdb.DBox(1.0, -0.18, (1000 + gap) * 0.001, 1.18))
        else:
            item.add_value(kdb.DBox(0.75, 1.18, 1.25, (1180 + gap) * 0.001))
    expected.save(str(OUT / f'{name}_expected.lyrdb'))
    return path


def check(pdk, layout, mode="flat"):
    """Run the checkout's maximal deck and return its Gat.b1 marker count."""
    deck = ROOT / f'ihp-{pdk}/libs.tech/klayout/tech/drc/rule_decks/{pdk}_maximal.drc'
    tag = f'{pdk}_{layout.stem}_{mode}_actual'
    report = OUT / f'{tag}.lyrdb'
    command = ['klayout', '-b', '-r', str(deck)]
    for key, value in dict(input=layout, topcell=layout.stem, report=report,
                           log=OUT / f'{tag}.log', threads=1, run_mode=mode,
                           fillerRules='false', no_recommended='true').items():
        command += ['-rd', f'{key}={value}']
    completed = subprocess.run(command, capture_output=True, text=True, timeout=90)
    (OUT / f'{tag}.stdout').write_text(completed.stdout + completed.stderr)
    if completed.returncode or not report.exists():
        raise RuntimeError(completed.stdout + completed.stderr)
    return sum(item.findtext('category', '').strip("'") == 'Gat.b1'
               for item in ET.parse(report).findall('./items/item'))


class TestGatB1Endcaps(unittest.TestCase):
    """Exercise complete maximal decks with rule-book-based expectations."""

    def assert_case(self, name, gap, expected, **options):
        """Check both PDKs independently so a failure does not hide the other."""
        layout = generate(name, gap, **options)
        for pdk in PDKS:
            with self.subTest(pdk=pdk, case=name):
                self.assertEqual(check(pdk, layout), expected,
                                 f'{name}: expected {expected} Gat.b1 marker(s)')

    def test_endcaps_below_minimum(self):
        """Facing ends below 0.25 um fail even when gate regions are farther apart."""
        for gap in (180, 249):
            self.assert_case(f'endcaps_{gap}nm', gap, 1)

    def test_endcaps_at_and_above_minimum(self):
        """The 0.25 um boundary and larger gaps pass."""
        for gap in (250, 251):
            self.assert_case(f'endcaps_{gap}nm', gap, 0)

    def test_non_hv_and_non_gate_poly(self):
        """LV gates and standalone poly inside ThickGateOx do not trigger Gat.b1."""
        self.assert_case('lv_poly', 180, 0, hv=False)
        self.assert_case('non_gate_poly', 180, 0, active=False)

    def test_same_activ_gate_spacing(self):
        """Existing gate-region violations remain, without duplicate markers."""
        self.assert_case('same_activ_fail', 180, 1, side=True)
        self.assert_case('same_activ_pass', 250, 0, side=True)

    def assert_layout(self, name, shapes, expected):
        """Write a flat fixture from (layer, box in nm) pairs and check both PDKs."""
        layout = kdb.Layout()
        layout.dbu = 0.001
        cell = layout.create_cell(name)
        for layer, coords in shapes:
            cell.shapes(layout.layer(layer, 0)).insert(kdb.Box(*coords))
        path = OUT / f'{name}.gds'
        layout.write(str(path))
        for pdk in PDKS:
            with self.subTest(pdk=pdk, case=name):
                self.assertEqual(check(pdk, path), expected,
                                 f'{name}: expected {expected} Gat.b1 marker(s)')

    def test_routing_outside_thickgateox(self):
        """HV gate poly routed 0.20 um apart outside ThickGateOx is left to Gat.b."""
        self.assert_layout('route_outside_tgo', [
            (44, (-1000, -1500, 3500, 4000)),
            (1, (0, 0, 3000, 1000)),
            (5, (500, -180, 1000, 1180)), (5, (2000, -180, 2500, 1180)),
            (5, (500, 1180, 1000, 8000)), (5, (1000, 7500, 1200, 8000)),
            (5, (1200, 6000, 1700, 8000)),
            (5, (2000, 1180, 2500, 6000)), (5, (1900, 6000, 2400, 8000))], 0)

    def test_connected_endcaps(self):
        """End caps of one connected poly are related, so Gat.b1 does not apply."""
        self.assert_layout('endcaps_connected', [
            (44, (-1000, -1500, 3000, 4000)),
            (1, (0, 0, 2000, 1000)), (5, (750, -180, 1250, 1180)),
            (1, (0, 1540, 2000, 2540)), (5, (750, 1360, 1250, 2720)),
            (5, (1250, 800, 2600, 1000)), (5, (2400, 800, 2600, 2000)),
            (5, (1250, 1800, 2600, 2000))], 0)

    def test_hierarchical_endcaps(self):
        """Check spacing across separate device instances with parent-level oxide."""
        for gap, expected in ((180, 1), (250, 0)):
            layout = kdb.Layout()
            layout.dbu = 0.001
            device = layout.create_cell('device')
            for layer, coords in [(1, (0, 0, 2000, 1000)), (5, (750, -180, 1250, 1180))]:
                device.shapes(layout.layer(layer, 0)).insert(kdb.Box(*coords))
            name = f'hierarchical_{gap}nm'
            top = layout.create_cell(name)
            top.shapes(layout.layer(44, 0)).insert(kdb.Box(-1000, -1500, 3000, 4000))
            for y in (0, 1360 + gap):
                top.insert(kdb.CellInstArray(device.cell_index(), kdb.Trans(0, y)))
            path = OUT / f'{name}.gds'
            layout.write(str(path))
            for pdk in PDKS:
                with self.subTest(pdk=pdk, gap=gap):
                    self.assertEqual(check(pdk, path, 'deep'), expected)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdk', choices=('ihp-sg13g2', 'ihp-sg13cmos5l'))
    parser.add_argument('--run-dir', type=Path, help='Keep generated layouts, expected markers and actual reports here')
    options, unittest_args = parser.parse_known_args()
    if options.pdk:
        PDKS = (options.pdk.removeprefix('ihp-'),)
    with tempfile.TemporaryDirectory(prefix='gat-b1-') as temporary:
        OUT = options.run_dir.resolve() if options.run_dir else Path(temporary)
        OUT.mkdir(parents=True, exist_ok=True)
        unittest.main(argv=[__file__, *unittest_args], verbosity=2)
