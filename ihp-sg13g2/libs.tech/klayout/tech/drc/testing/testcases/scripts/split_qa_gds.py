#!/usr/bin/env python3
"""
Split the monolithic QA GDS into individual per-table GDS files.

The QA GDS contains 60 cells, each representing a DRC test table.
Each cell has PASS structures (left/negative x) and FAIL structures (right/positive x).

This script splits each cell into its own GDS file, applying the naming
conventions expected by run_regression.py:
  - Filename: {table_name}.gds (or {table}_{cell}.gds for multi-cell tables)
  - The first token of the filename (before '_') becomes the table_name
  - Table name must match the DRC rule deck file suffix (e.g., 'psd' matches '5_10_psd.drc')

Usage:
    python split_qa_gds.py --input <qa_gds_path> --output_dir <output_directory>
"""

import argparse
import sys
from pathlib import Path

import klayout.db as db


# Mapping: QA cell name -> (output_filename_without_gds, new_cell_name_or_None)
# If new_cell_name is None, keep original cell name.
# The first token of the filename (split by '_') determines the table_name in regression.
QA_CELL_MAP = {
    # === Direct matches (already in test suite, same cell name) ===
    "activ":         ("activ",               None),
    "antenna":       ("antenna",             None),
    "cont":          ("cont",                None),
    "contb":         ("contbar",             None),  # table=contbar, cell stays 'contb'
    "gatpoly":       ("gatpoly",             None),
    "lbe":           ("lbe",                 None),
    "lu":            ("latchup",             None),  # table=latchup, cell stays 'lu'
    "metal1":        ("metal1",              None),
    "mim":           ("mim",                 None),
    "nBuLay":        ("nbulay",              None),  # table=nbulay, cell stays 'nBuLay'
    "nwell":         ("nwell",               None),
    "pSD":           ("psd",                 None),  # table=psd, cell stays 'pSD'
    "pad":           ("pad",                 None),
    "passiv":        ("passiv",              None),
    "pwellblock":    ("pwellblock",          None),
    "rhigh":         ("rhigh",               None),
    "rppd":          ("rppd",                None),
    "rsil":          ("rsil",                None),
    "salblock":      ("salblock",            None),
    "sealring_pt1":  ("sealring",            None),  # table=sealring
    "thickgateox":   ("thickgateox",         None),
    "via1":          ("via1",                None),
    "nmosi":         ("nmosi",               None),

    # === Cells needing cell name change (camelCase -> lowercase) ===
    "activFiller":   ("activfiller",         "activfiller"),
    "extBlock":      ("extblock",            "extblock"),
    "forbidden_layer": ("forbidden",         "forbidden"),
    "gatFiller":     ("gatpolyfiller",       "gatpolyfiller"),
    "metalFiller":   ("metalnfiller",        "metalnfiller"),
    "metalSlits":    ("metalslits",          "metalslits"),
    "npnSubTie":     ("npnsubstratetie",     "npnsubstratetie"),
    "pin_layer":     ("pin",                 "pin"),
    "schottky_diode": ("schottkydiode",      "schottkydiode"),
    "topMet1Filler": ("topmetal1filler",     "topmetal1filler"),
    "topMet2Filler": ("topmetal2filler",     "topmetal2filler"),
    "topMetal1":     ("topmetal1",           "topmetal1"),
    "topMetal2":     ("topmetal2",           "topmetal2"),
    "topVia1":       ("topvia1",             "topvia1"),
    "topVia2":       ("topvia2",             "topvia2"),

    # === Consolidated cells (one QA cell -> multiple table files) ===
    # metaln covers metal2-metal5 -> we keep as single file, table=metaln
    "metaln":        ("metaln",              "metaln"),
    # vian covers via2-via4 -> we keep as single file, table=vian
    "vian":          ("vian",                "vian"),

    # === Multi-cell tables (additional cells for existing tables) ===
    "nBuLaBlock":    ("nbulay_nBuLaBlock",   None),  # table=nbulay
    "nSDBlock":      ("nsdblock",            None),   # separate table for nSD:block rules
    "nwell_digi":    ("nwell_digi",          None),   # table=nwell
    "cont_digi":     ("cont_digi",           None),   # table=cont
    "sealring_pt2":  ("sealring_pt2",        None),   # table=sealring

    # === Offgrid cells (3 cells -> 1 combined file) ===
    # Handled specially below - merged into single offgrid.gds with 3 top cells
    "offGrid_fe":    ("__offgrid__",         None),
    "offGrid_be":    ("__offgrid__",         None),
    "offGrid_misc":  ("__offgrid__",         None),

    # === New cells not in current suite ===
    "tsv_g":         ("tsv",                 "tsv_g"),
    "pad_pillars":   ("copperpillar",        "copperpillar"),
    "pad_sbump":     ("solderbump",          "solderbump"),
    "angles_acute":  ("angles_acute",        None),
    "angles_non45":  ("angles_non45",        None),
    "angles_non90":  ("angles_non90",        None),

    # === Density cells (handled by density/ subdir, skip for unit/) ===
    "densityMax_pass":    None,  # Skip
    "densityMax_fail":    None,  # Skip
    "densityMin_pass":    None,  # Skip
    "densityMin_fail":    None,  # Skip
    "densityMinSlt_pass": None,  # Skip
    "densityMinSlt_fail": None,  # Skip
}


def split_qa_gds(input_path: str, output_dir: str):
    """Split the monolithic QA GDS into individual per-table GDS files."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    qa = db.Layout()
    qa.read(input_path)

    # Collect offgrid cells for merging
    offgrid_cells = []
    written_files = []
    skipped_cells = []

    for cell in qa.each_cell():
        cname = cell.name

        if cname not in QA_CELL_MAP:
            print(f"WARNING: Unknown QA cell '{cname}', skipping")
            skipped_cells.append(cname)
            continue

        mapping = QA_CELL_MAP[cname]
        if mapping is None:
            print(f"SKIP: {cname} (density cell, not for unit/)")
            skipped_cells.append(cname)
            continue

        out_name, new_cell_name = mapping

        # Offgrid cells are merged into a single file
        if out_name == "__offgrid__":
            offgrid_cells.append(cname)
            continue

        # Create new layout with just this cell
        new_layout = db.Layout()
        new_layout.dbu = qa.dbu

        # Create target cell
        target_name = new_cell_name if new_cell_name else cname
        new_cell = new_layout.create_cell(target_name)

        # Copy all layers and shapes
        for li in qa.layer_indices():
            info = qa.get_info(li)
            new_li = new_layout.layer(info.layer, info.datatype)
            for shape in cell.shapes(li).each():
                new_cell.shapes(new_li).insert(shape)

        out_file = output_path / f"{out_name}.gds"
        new_layout.write(str(out_file))
        written_files.append((out_file.name, cname, target_name))
        print(f"WRITE: {out_file.name} (cell: {target_name}, from QA cell: {cname})")

    # Handle offgrid: merge 3 cells into 1 file
    if offgrid_cells:
        new_layout = db.Layout()
        new_layout.dbu = qa.dbu

        for cname in offgrid_cells:
            ci = qa.cell_by_name(cname)
            src_cell = qa.cell(ci)
            new_cell = new_layout.create_cell(cname)

            for li in qa.layer_indices():
                info = qa.get_info(li)
                new_li = new_layout.layer(info.layer, info.datatype)
                for shape in src_cell.shapes(li).each():
                    new_cell.shapes(new_li).insert(shape)

        out_file = output_path / "offgrid.gds"
        new_layout.write(str(out_file))
        written_files.append((out_file.name, "offGrid_*", "offGrid_fe/be/misc"))
        print(f"WRITE: {out_file.name} (merged 3 offgrid cells)")

    print(f"\nSummary: {len(written_files)} files written, {len(skipped_cells)} cells skipped")
    return written_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split QA GDS into individual test files")
    parser.add_argument("--input", required=True, help="Path to monolithic QA GDS")
    parser.add_argument("--output_dir", required=True, help="Output directory for split GDS files")
    args = parser.parse_args()

    split_qa_gds(args.input, args.output_dir)
