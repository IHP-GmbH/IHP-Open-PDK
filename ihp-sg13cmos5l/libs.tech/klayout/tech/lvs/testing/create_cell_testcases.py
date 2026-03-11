#! /usr/bin/env python3

"""
create_cell_testcases.py - SG13CMOS5L version

Extract individual cell testcases from the SG13CMOS5L standard cell library.

1. Use klayout to create "testcases/sg13cmos5l_cells/<cell>/layout/<cell>.gds" files
   from "libs.ref/sg13cmos5l_stdcell/gds/sg13cmos5l_stdcell.gds"
2. Create "testcases/sg13cmos5l_cells/<cell>/netlist/<cell>.cdl" files
   from "libs.ref/sg13cmos5l_stdcell/cdl/sg13cmos5l_stdcell.cdl"

CMOS5L differences from G2:
- No _iso or _digisub variants (nBuLay and DigiSub layers are forbidden)
- No frame layer insertion needed
- Only base cell names are extracted
"""

from sys import stderr
import os
import re
from datetime import datetime, timezone
import argparse
import pya
from pathlib import Path
import shutil
import logging
import inspect

BOUNDARY_LAYER = (189, 4)


class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        if datefmt:
            return datetime.fromtimestamp(record.created).strftime(datefmt)
        else:
            return datetime.fromtimestamp(record.created).strftime('%d-%b-%Y %H:%M:%S')


def die(message):
    print(f"ERROR: {message}", file=stderr)
    raise SystemExit(1)


def error(message, *, verbose=True):
    logger.error(message)
    if verbose:
        print(f"ERROR: {message}", file=stderr)


def warn(message, *, verbose=False):
    logger.warning(message)
    if verbose:
        print(f"WARNING: {message}", file=stderr)


def info(message, *, verbose=False):
    logger.info(message)
    if verbose:
        print(f"INFO: {message}")


def debug(message, *, verbose=False):
    logger.debug(message)
    if verbose:
        print(f"DEBUG: {message}")


def find_files_by_extension(directory, extension):
    search_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                search_files.append(os.path.join(root, file))
    return search_files


def sort_layers(layers):
    return sorted(layers, key=lambda lay: (lay))


def get_cell_layers(layout, cell):
    used_layers = set()
    for layer_index in layout.layer_indices():
        shapes = cell.shapes(layer_index)
        if not shapes.is_empty():
            layer_info = layout.get_info(layer_index)
            used_layers.add((layer_info.layer, layer_info.datatype))
    return used_layers


# ~~~~~~~~~~~~~~~~~~~~~~~ Main Procedure ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Clone cdl PDK -> LVS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def clone_cdl_files(cdl_in: str, cell_list: list, ref_dir: str, out_dir: str,
                    *, verbose=False):

    cdl_path = Path(cdl_in)
    if not cdl_path.exists():
        die(f'Input cdl file does not exist: {cdl_in}')

    # Create subckt dict from the reference CDL
    subckt_ref = {}
    with open(cdl_in, 'rt') as f_in:
        input_line_number = 1
        for input_line in f_in:

            if input_line_number == 1:
                line_buf = [input_line]
                next_line = next(f_in)
                input_line_number += 1
                while next_line.strip() != "":
                    line_buf.append(next_line)
                    next_line = next(f_in)
                    input_line_number += 1
                subckt_ref['HEADER'] = line_buf
                continue

            elif input_line.startswith('*****'):
                line_buf = [input_line]
                next_line = next(f_in)
                input_line_number += 1
                while next_line.strip() != ".ENDS":
                    if re.match(r'\.SUBCKT', next_line):
                        cell_name = next_line.split()[1]
                    line_buf.append(next_line)
                    next_line = next(f_in)
                    input_line_number += 1
                line_buf.append(next_line)
                subckt_ref[cell_name] = line_buf

    out_dir_by_cell = {}
    for cell_ref in cell_list:

        search_cdl = find_files_by_extension(ref_dir, f'{cell_ref}.cdl')
        src_path = search_cdl[0] if search_cdl else None
        dest_path = os.path.join(out_dir, f'{cell_ref}/netlist/{cell_ref}.cdl')

        if not os.path.exists(os.path.dirname(dest_path)):
            out_path = Path(os.path.dirname(dest_path))
            out_path.mkdir(parents=True, exist_ok=True)

        if cell_ref not in subckt_ref:
            if src_path and os.path.exists(src_path):
                if os.path.exists(dest_path):
                    warn(f'Already exists {dest_path} => Skipped copy', verbose=True)
                else:
                    warn(f'Copy {src_path} -> {dest_path}', verbose=True)
                    shutil.copy2(src_path, dest_path)
            warn('Manual update may be needed', verbose=True)
        else:
            # CMOS5L: only write the base cell (no _iso, _digisub variants)
            info(f'Clone subckt_ref[{cell_ref}] -> {dest_path}', verbose=True)
            with open(dest_path, 'wt') as f_out:
                for line in subckt_ref['HEADER']:
                    f_out.write(line)
                f_out.write('\n')

                for line in subckt_ref[cell_ref]:
                    f_out.write(line)

        out_dir_by_cell[cell_ref] = os.path.dirname(dest_path)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Clone GDS PDK -> LVS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def insert_stdcell_frames(gds_in: str, cell_list: list, ref_dir: str, out_dir: str,
                          *, verbose=False):

    gds_path = Path(gds_in)
    if not gds_path.exists():
        die(f'Input gds does not exist: {gds_in}')

    # Read input GDS
    layout = pya.Layout()
    info(f'Reading input GDS file {gds_in} ..', verbose=True)
    layout.read(gds_in)

    out_dir_by_cell = {}

    for cell_ref in cell_list:

        cell = layout.cell(cell_ref)

        search_gds = find_files_by_extension(ref_dir, f'{cell_ref}.gds')
        if len(search_gds) == 0:
            warn(f'Reference gds of {cell_ref} does not exist => Skipped', verbose=True)
            continue

        src_path = search_gds[0]
        dest_path = os.path.join(out_dir, f'{cell_ref}/layout/{cell_ref}.gds')

        if not os.path.exists(os.path.dirname(dest_path)):
            out_path = Path(os.path.dirname(dest_path))
            out_path.mkdir(parents=True, exist_ok=True)

        if not cell:
            if not os.path.exists(dest_path):
                info(f'Copy {src_path} -> {dest_path}', verbose=verbose)
                shutil.copy(src_path, dest_path)
            out_dir_by_cell[cell_ref] = os.path.dirname(dest_path)
            warn(f'Copying non library cell {src_path} -> {dest_path}', verbose=verbose)
            warn('Manual update may be needed', verbose=True)
            continue

        info(f'Extracting cell => {cell.name}', verbose=True)

        # CMOS5L: extract only the base cell (no _iso, _digisub clones)
        layout_gds = pya.Layout()
        layout_gds.dbu = layout.dbu
        layout_gds_cell = layout_gds.create_cell(cell.name)
        layout_gds_cell.copy_tree(cell)

        layout_gds.write(os.path.join(dest_path))
        out_dir_by_cell[cell.name] = os.path.dirname(dest_path)

    return out_dir_by_cell


def copy_yaml_files(ref_dir: str, out_dir: str, *, verbose=False):

    src_path = find_files_by_extension(ref_dir, '.yaml')

    for each_path in src_path:
        base_name = os.path.basename(each_path)
        cell_name = re.sub(r'\.yaml', '', base_name)
        dest_path = os.path.join(out_dir, f'{cell_name}/layout/{base_name}')

        if not os.path.exists(os.path.dirname(dest_path)):
            Path(os.path.dirname(dest_path)).mkdir(parents=True, exist_ok=True)

        if not os.path.exists(dest_path):
            info(f'Copy {each_path} -> {dest_path}', verbose=True)
            shutil.copy2(each_path, dest_path)


if __name__ == "__main__":

    SCRIPT_DIR = os.path.realpath(__file__)

    default_gds_ref = re.sub(r'libs\.tech.*',
                             'libs.ref/sg13cmos5l_stdcell/gds/sg13cmos5l_stdcell.gds',
                             SCRIPT_DIR)
    default_cdl_ref = re.sub(r'libs\.tech.*',
                             'libs.ref/sg13cmos5l_stdcell/cdl/sg13cmos5l_stdcell.cdl',
                             SCRIPT_DIR)

    default_input_dir = './testcases/sg13cmos5l_cells'
    default_output_dir = './testcases/sg13cmos5l_cells'

    parser = argparse.ArgumentParser(description='Extract SG13CMOS5L cell testcases from stdcell library')
    parser.add_argument('--gds_ref', '-gds', action='store', default=default_gds_ref,
                        help=f'Reference GDS file (default={default_gds_ref})')
    parser.add_argument('--cdl_ref', '-cdl', action='store', default=default_cdl_ref,
                        help=f'Reference CDL file (default={default_cdl_ref})')
    parser.add_argument('--testcase_dir', '-i', action='store', default=default_input_dir,
                        help=f'Reference testcase directory (default={default_input_dir})')
    parser.add_argument('--out_dir', '-o', action='store', default=default_output_dir,
                        help=f'Output result files directory (default={default_output_dir})')
    parser.add_argument('--cell_name', '-s', action='store',
                        help='Select executing cell name (default=all)')
    parser.add_argument('--clean', '-c', action='store_true',
                        help='Clean previous gds files in the output directory')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose mode on')
    args = parser.parse_args()

    gds_ref = args.gds_ref
    cdl_ref = args.cdl_ref
    ref_dir = args.testcase_dir
    out_dir = args.out_dir

    chk_path = Path(ref_dir)
    if not chk_path.exists():
        # Create if it does not exist (first run)
        chk_path.mkdir(parents=True, exist_ok=True)

    CELL_LIST = [os.path.basename(cdl_file).replace('.cdl', '') for cdl_file
                 in find_files_by_extension(ref_dir, '.cdl')]
    print(f'CELL_LIST={CELL_LIST}')

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Replace GDS & CDL in testcases/sg13cmos5l_cells with libs.ref/sg13cmos5l_stdcell
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    run_name = datetime.now(timezone.utc).strftime('create_cells_%Y_%m_%d_%H_%M_%S')
    output_path = '.'
    log_file = os.path.join(output_path, f'{run_name}.log')

    # Create a logger
    logger = logging.getLogger('mon_logger')
    logger.setLevel(logging.DEBUG)

    # Create a console handler and set its log level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    # Create a file handler and set its log level
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter and add it to the handlers
    formatter = CustomFormatter('%(asctime)s | %(levelname)-7s | %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Create result output directory if not exist
    out_path = Path(out_dir)
    if args.clean:
        if Path(ref_dir) == out_path:
            warn(f"Can not clean output directory {out_path} because it is also the reference directory.")
        else:
            shutil.rmtree(out_path)
    out_path.mkdir(parents=True, exist_ok=True)

    # ~~~~~~~~~~~~~~~~~~~
    # Replace cdl
    # ~~~~~~~~~~~~~~~~~~~
    clone_cdl_files(cdl_ref, CELL_LIST, ref_dir, out_dir, verbose=args.verbose)

    # ~~~~~~~~~~~~~~~~~~~
    # Replace GDS
    # ~~~~~~~~~~~~~~~~~~~
    saved_dir = insert_stdcell_frames(gds_ref, CELL_LIST, ref_dir, out_dir, verbose=args.verbose)

    # ~~~~~~~~~~~~~~~~~~~
    # Copy yaml
    # ~~~~~~~~~~~~~~~~~~~
    copy_yaml_files(ref_dir, out_dir, verbose=True)

    # ~~~~~~~~~~~~~~~~~~~
    # Check ERROR
    # ~~~~~~~~~~~~~~~~~~~
    os.system(f'grep --color ERROR {log_file}')
