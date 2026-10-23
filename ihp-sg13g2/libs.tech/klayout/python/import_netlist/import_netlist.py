# Copyright 2024 Efabless Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Original file changed by IHP PDK Authors 2025
# Adopting the Skywater PDK import_netlist.py file to IHP SG13G2 technology


import os
import re
import sys
import pya

from .ihp130_pcell_templates import templates


SI_MULTIPLIERS = {
    "t": 1e12,
    "g": 1e9,
    "meg": 1e6,
    "k": 1e3,
    "m": 1e-3,
    "u": 1e-6,
    "µ": 1e-6,
    "n": 1e-9,
    "p": 1e-12,
    "f": 1e-15,
}

# Pin declarations written by xschem
PIN_DIRECTIVES = ('*.iopin', '*.ipin', '*.opin')

# Keys of the user properties stored on device cell instances and pins.
# They are integers because GDS drops properties with string keys on save.
PROP_NAME = 1
PROP_NETS = 2
PROP_DIRECTION = 3

# Metal1 layers for pins; LVS reads the pin labels from 8/25
METAL1_DRAWING = pya.LayerInfo(8, 0)
METAL1_PIN = pya.LayerInfo(8, 2)
METAL1_TEXT = pya.LayerInfo(8, 25)
PIN_SIZE_UM = 1.0
PIN_SPACING_UM = 4.0
PIN_ROW_Y_UM = -10.0


def parse_si_value(value):
    if not isinstance(value, str):
        return value

    cleaned = value.strip()
    match = re.fullmatch(r"([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*([a-zA-Zµ]+)?", cleaned)
    if not match:
        return value

    number = float(match.group(1))
    suffix = match.group(2)
    if not suffix:
        return number

    suffix = suffix.lower()
    if suffix in SI_MULTIPLIERS:
        return number * SI_MULTIPLIERS[suffix]

    if suffix.endswith("m") and len(suffix) == 2:
        prefix = suffix[0]
        if prefix in SI_MULTIPLIERS:
            return number * SI_MULTIPLIERS[prefix]

    return value


def normalize_params(params):
    normalized = {}
    for key, value in params.items():
        normalized[key] = parse_si_value(value)
    return normalized


def create_pcell_instance(pcell_name='CIRCLE', lib_name='Basic', params={}, pos=pya.Trans.R0,
                          name_spice=None, nets=None):
    """
    Create a new instance of a PCell
    and return its width and height

    With name_spice the PCell is wrapped in a cell of that name and
    the instance carries the SPICE name and nets as user properties.
    """

    print(f"Creating PCell '{pcell_name}' with parameters:")
    
    for key, value in params.items():
        print(f' - {key}: {value}')

    # Get the active layout
    cellview = pya.CellView().active()
    layout = cellview.layout()
    if layout is None:
        print('Error: Couldn\'t get active layout.')
        return (0, 0)

    # Get PCell Library of the layout's technology
    lib = pya.Library.library_by_name(lib_name, layout.technology_name)

    if not lib:
        print(f'Error: Library not found {lib_name} (technology "{layout.technology_name}")')
        return (0, 0)

    # The PCell Declaration. This one will create PCell variants.
    pcell_decl = lib.layout().pcell_declaration(pcell_name)

    if not pcell_decl:
        print(f'Error: Pcell not found {pcell_name}')
        return (0, 0)

    # Get the top cell. Assuming only one top cell exists
    top_cell = layout.top_cell()

    # Add a PCell variant
    pcell_var = layout.add_pcell_variant(lib, pcell_decl.id(), params)
    
    bbox = layout.cell(pcell_var).bbox()
    
    # Add an offset to the position to account for the origin
    offset = pya.Trans(pos, x=-bbox.left, y=-bbox.bottom)

    width = bbox.width()
    height = bbox.height()
    
    # Insert instance
    if name_spice:
        # The PCell sits at the origin of a cell named after the SPICE
        # instance, so it stays editable one level down
        device_cell = layout.create_cell(name_spice)
        device_cell.insert(pya.CellInstArray(pcell_var, pya.Trans(-bbox.left, -bbox.bottom)))
        # Set the properties on insert: set_property() needs editable mode
        props = [(PROP_NAME, name_spice)]
        if nets:
            props.append((PROP_NETS, ' '.join(nets)))
        top_cell.insert(pya.CellInstArray(device_cell.cell_index(), pos), layout.properties_id(props))
    else:
        top_cell.insert(pya.CellInstArray(pcell_var, offset))
    
    return (width, height)

current_x = 0
spacing = 100

def create_subckt_instance(name, subckt_definitions):
    global current_x
    global spacing

    for pcell_inst in subckt_definitions[name]['pcells']:
        (width, height) = create_pcell_instance(
            pcell_inst['pcell_name'],
            pcell_inst['pcell_library'],
            pcell_inst['params'],
            pya.Trans(current_x, 0),
            name_spice=pcell_inst['name_spice'],
            nets=pcell_inst['nets'],
        )
        current_x += width + spacing

    for subckt_inst in subckt_definitions[name]['subckts']:
        if not subckt_inst in subckt_definitions:
            print(f'Error: Unknown subckt {subckt_inst}')
        else:
            create_subckt_instance(subckt_inst, subckt_definitions)


def create_pin_instance(name, direction, x):
    """
    Draw a Metal1 pin with its label in the top cell, below the devices,
    and return how far (in dbu) to advance x for the next pin
    """
    layout = pya.CellView().active().layout()
    top_cell = layout.top_cell()

    y = int(round(PIN_ROW_Y_UM / layout.dbu))
    size = int(round(PIN_SIZE_UM / layout.dbu))
    box = pya.Box(x, y, x + size, y + size)

    prop_id = layout.properties_id([(PROP_NAME, name), (PROP_DIRECTION, direction)])
    top_cell.shapes(layout.layer(METAL1_DRAWING)).insert(box)
    top_cell.shapes(layout.layer(METAL1_PIN)).insert(box, prop_id)
    top_cell.shapes(layout.layer(METAL1_TEXT)).insert(pya.Text(name, pya.Trans(box.center().x, box.center().y)))

    print(f'Creating pin {name} ({direction})')
    return size + int(round(PIN_SPACING_UM / layout.dbu))


def ihp130_import_netlist():

    # The PCell library is looked up by the layout's technology
    layout = pya.CellView().active().layout()
    if layout is None:
        print('Error: Couldn\'t get active layout.')
        return
    if not layout.technology_name:
        print('Error: The active layout has no technology. Set it in File > Layout Properties.')
        return

    # Get the schematic netlist
    netlist_path = pya.FileDialog.ask_open_file_name("Choose the schematic netlist", '.', "SPICE (*.spice)")

    print(f'Info: The netlist importer is still experimental.')
    
    # Check whether file exists
    if not netlist_path or not os.path.isfile(netlist_path):
        print(f'Error: {netlist_path} is not a file!')
        sys.exit(0)

    print(f'Reading Spice netlist: {netlist_path}')

    # Parse the spice netlist
    with open(netlist_path, 'r') as netlist_file:
        netlist_content = netlist_file.read()

    # Continue lines starting with '+'
    netlist_content = netlist_content.replace('\n+', '')
    
    # Split lines
    netlist_lines = netlist_content.split('\n')

    # Subckt data
    subckt_definitions = {'root': {'subckts': [], 'pcells': [], 'pins': [], 'references': 0}}
    active_subckt = 'root'

    # Parameter data
    global_parameters = {}

    # Handle ".include" statements
    found = True
    while found:
        found = False
        for i, line in enumerate(netlist_lines):
            # Ignore comments
            if line.startswith('*'):
                continue

            # Find start of include statement
            if line.startswith('.include') or line.startswith('.INCLUDE'):
                found = True
                include_path = line.split(' ')[1]
                
                # Relative path
                if not os.path.isabs(include_path):
                    include_path = os.path.join(os.path.dirname(netlist_path), include_path)

                # Get the content
                with open(include_path, 'r') as include_file:
                    include_content = include_file.read()
                
                # Continue lines starting with '+'
                include_content = include_content.replace('\n+', '')
                
                # Split lines
                include_lines = include_content.split('\n')

                # Replace ".include" with the lines
                netlist_lines[i:i+1] = include_lines
                
                break

    # Scan for parameters
    for line in netlist_lines:
        # Ignore comments
        if line.startswith('*'):
            continue

        # Find start of subckt definitions
        if line.startswith('.param') or line.startswith('.PARAM'):
            parameter = line.split(' ')[1]
            name, value = parameter.split('=')
            global_parameters[name] = value
    
    # Apply parameters
    for i, line in enumerate(netlist_lines):
        # Ignore comments
        if line.startswith('*'):
            continue

        # Find start of subckt definitions
        def replace_parameters(matchobj):
            if matchobj.group(1) in global_parameters:
                return global_parameters[matchobj.group(1)]
            print(f'Error: Unknown parameter "{matchobj.group(1)}"')
            return matchobj.group(1)

        netlist_lines[i] = re.sub(r'{(.*?)}', replace_parameters, line)

    # Scan for subckts
    for line in netlist_lines:
        # Collect pins, e.g. "*.ipin A"; xschem may list a pin twice
        if line.lower().startswith(PIN_DIRECTIVES):
            direction, pin = line.split()[:2]
            pins = subckt_definitions[active_subckt]['pins']
            if pin not in [p['name'] for p in pins]:
                pins.append({'name': pin, 'direction': direction.lower().lstrip('*.')})
            continue

        # Ignore comments
        if line.startswith('*'):
            continue

        # Find start of subckt definitions
        if line.startswith('.subckt') or line.startswith('.SUBCKT'):
            active_subckt = line.split(' ')[1]
            subckt_definitions[active_subckt] = {'subckts': [], 'pcells': [], 'pins': [], 'references': 0}

        # Find end of subckt definitions
        if line.startswith('.ends') or line.startswith('.ENDS'):
            active_subckt = 'root'

    # Devices outside of .subckt blocks belong to 'root'
    active_subckt = 'root'
    for line in netlist_lines:
        # Ignore comments
        if line.startswith('*'):
            continue

        # Find start of subckt definitions
        if line.startswith('.subckt') or line.startswith('.SUBCKT'):
            active_subckt = line.split(' ')[1]
            
            if not active_subckt in subckt_definitions:
                print(f'Error: Unknown subckt "{active_subckt}"')

        # Find end of subckt definitions
        if line.startswith('.ends') or line.startswith('.ENDS'):
            active_subckt = 'root'

        #print(f"Searching for match with '{line}'!")
        any_match = False
        for template in templates:
      
            match = template['regex'].match(line)
            if match:
                any_match = True
                params = normalize_params(template['default_params'])
              
                # Parse parameters
                for param in template['params']:
                    #print(f"Parsing parameter {param['name']}")
                    if param["type"] == "raw_string":
                        params[param['name']] = match.group(param['name'])
                    if param["type"] == "string":
                        parsed_value = parse_si_value(match.group(param['name']))
                        params[param['name']] = parsed_value
                    if param["type"] == "int":
                        if match.group(param['name']) == None:
                            params[param['name']] = 1
                        else:
                            parsed_value = parse_si_value(match.group(param['name']))
                            params[param['name']] = int(parsed_value)
                    if param["type"] == "float":
                        parsed_value = parse_si_value(match.group(param['name']))
                        params[param['name']] = float(parsed_value)
              
                # Multiplicity 'm'
                m = 1
                if 'm' in params:
                    m = params.pop('m')
              
                # Divide 'w' by 'nf' to get individual finger width
                if 'nf' in params and params['nf'] > 1:
                    if 'w' in params:
                        params['w'] /= params['nf']
              
                #print(f'Instantiating Pcell with: {params}')
              
                # Nets are the tokens between the instance name and the model,
                # which is the token right before the first "key=value"
                tokens = line.split()
                first_kv = next((k for k, t in enumerate(tokens) if '=' in t), len(tokens))
                nets = tokens[1:first_kv - 1]

                for i in range(m):
                    subckt_definitions[active_subckt]['pcells'].append({
                        'name_spice':       tokens[0] if m == 1 else f'{tokens[0]}_{i + 1}',
                        'pcell_name':       template['pcell_name'],
                        'pcell_library':    template['pcell_library'],
                        'params':           params.copy(),
                        'nets':             nets,
                    })

        # Line was handled by template
        # no need to parse subcircuit
        if any_match:
            continue

        # Subckt instantiation
        # TODO: handle parameters
        if line.startswith('x') or line.startswith('X'):
            subckt = line.split(' ')[-1]
            subckt_definitions[active_subckt]['subckts'].append(subckt)
            
            if not subckt in subckt_definitions:
                print(f'Error: Unknown subckt "{subckt}"')
            else:
                subckt_definitions[subckt]['references'] += 1

    # Instanciate all top-level subckts and their pins
    pin_x = 0
    for name in subckt_definitions.keys():
        if subckt_definitions[name]['references'] == 0:
            create_subckt_instance(name, subckt_definitions)
            for pin in subckt_definitions[name]['pins']:
                pin_x += create_pin_instance(pin['name'], pin['direction'], pin_x)
