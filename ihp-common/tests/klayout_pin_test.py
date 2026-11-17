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

"""PCell pin regression. Run from the repository root with make test-pycell-pins."""

import argparse
import importlib
import itertools
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


def run_tests(pdk_dir):
    import pya
    from cni.dlo import Box, DloGen, Layer, PyCellContext, Tech
    from cni.constants import PROPERTY_KEY__PIN_INFO__PIN_NAME as pin_name_key

    technology = pdk_dir.name.removeprefix('ihp-')
    python_dir = pdk_dir / 'libs.tech/klayout/python'
    package = technology + '_pycell_lib'
    geometry = importlib.import_module(package + '.ihp.geometry')
    library_module = importlib.import_module(package)
    if Path(library_module.__file__).resolve().parent != (python_dir / package).resolve():
        raise RuntimeError('PCell library was loaded from outside the selected PDK')

    class PCellPinTest(unittest.TestCase):
        def setUp(self):
            self.layout = pya.Layout()
            self.layout.technology_name = technology

        def create_cell(self, device, params):
            cell = self.layout.create_cell(device, 'SG13_dev', params)
            self.assertIsNotNone(cell, device)
            self.assertFalse(cell.is_empty(), device)
            return cell

        def check_pins(self, cell, expected_names):
            found = {}
            for layer in self.layout.layer_indexes():
                for shape in cell.shapes(layer).each():
                    name = shape.property(pin_name_key)
                    if name is None:
                        continue
                    self.assertNotIn(name, found, 'Duplicate metadata for ' + name)
                    found[name] = shape
                    properties = shape.properties()
                    self.assertEqual(properties['PIN_INFO__VERSION'], '0.1')
                    self.assertEqual(properties['PIN_INFO__LIB_NAME'], 'SG13_dev')
                    self.assertEqual(properties['PIN_INFO__TERM_NAME'], name)
                    self.assertTrue(properties['PIN_INFO__CELL_NAME'])
                    layer_info = self.layout.get_info(layer)
                    drawing = self.layout.find_layer(layer_info.layer, 0)
                    self.assertIsNotNone(drawing, str(layer_info))
                    uncovered = pya.Region(shape.polygon) - pya.Region(cell.shapes(drawing))
                    self.assertTrue(uncovered.is_empty(), name + ' extends outside drawing geometry')
            self.assertEqual(set(found), expected_names)
            return found

        def test_mkpin_creates_one_rectangle_and_keeps_label(self):
            cell = self.layout.create_cell('mkpin_test')
            impl = DloGen()
            impl.addCellContext(cell)
            with PyCellContext(Tech.get('SG13_dev'), cell, impl):
                geometry.MkPin(impl, 'S', 0, Box(1, 2, 3, 4), 'Metal1', label=True)
                pins = list(cell.shapes(Layer('Metal1', 'pin').number).each())
                self.assertEqual(len(pins), 1)
                self.assertEqual(pins[0].property(pin_name_key), 'S')
                self.assertEqual(pins[0].dbox, pya.DBox(1, 2, 3, 4))
                labels = [s.text.string for s in cell.shapes(Layer('TEXT', 'drawing').number).each()
                          if s.is_text()]
                self.assertEqual(labels, ['S'])

        def test_rfmos_pins(self):
            devices = ('rfnmos', 'rfnmosHV', 'rfpmos', 'rfpmosHV')
            configurations = [{}]
            for guard, rows, metal2, gate_ring in itertools.product(
                    ('Yes', 'No', 'U', 'Top+Bottom'), (1, 3), ('Yes', 'No'), ('Yes', 'No')):
                configurations.append({'guard_ring': guard, 'cnt_rows': rows, 'Met2Cont': metal2,
                                       'gat_ring': gate_ring, 'ng': '4', 'w': '8u'})
            for device, params in itertools.product(devices, configurations):
                with self.subTest(device=device, params=params):
                    cell = self.create_cell(device, params)
                    names = {'S', 'D', 'G'}
                    if params.get('guard_ring', 'Yes') != 'No':
                        names.add('TIE')
                    self.check_pins(cell, names)
                    pin_layer = self.layout.find_layer(8, 2)
                    self.assertIsNotNone(pin_layer)
                    self.assertEqual(cell.shapes(pin_layer).size(), len(names))
                    self.assertEqual(cell.dbbox().left, 0)
                    self.assertEqual(cell.dbbox().bottom, 0)

        def test_unshifted_mos_pins(self):
            for device in ('nmos', 'nmosHV', 'pmos', 'pmosHV'):
                with self.subTest(device=device):
                    self.check_pins(self.create_cell(device, {}), {'S', 'D', 'G'})

        @unittest.skipUnless(technology == 'sg13g2', 'CMIM is only available in SG13G2')
        def test_direct_addpin_cmim(self):
            self.check_pins(self.create_cell('cmim', {}), {'PLUS', 'MINUS'})

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PCellPinTest)
    api_tests = python_dir / 'pycell4klayout-api/tests'
    suite.addTests(unittest.defaultTestLoader.discover(str(api_tests)))
    print('Testing pin geometry for {} with KLayout {}'.format(pdk_dir.name, pya.__version__), flush=True)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdk_dir', type=Path)
    parser.add_argument('--klayout', default='klayout')
    args = parser.parse_args()
    pdk_dir = args.pdk_dir.resolve()
    with tempfile.TemporaryDirectory(prefix='ihp-pin-test-') as config_dir:
        env = os.environ.copy()
        env['KLAYOUT_HOME'] = config_dir
        env['KLAYOUT_PATH'] = str(pdk_dir / 'libs.tech/klayout')
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        return subprocess.run([
            args.klayout, '-zz', '-r', str(Path(__file__).resolve()),
            '-rd', 'pin_test_pdk_dir=' + str(pdk_dir),
        ], env=env).returncode


if __name__ == '__main__':
    if 'pin_test_pdk_dir' in globals():
        import pya
        pya.Application.instance().exit(run_tests(Path(globals()['pin_test_pdk_dir'])))
    else:
        sys.exit(main())
