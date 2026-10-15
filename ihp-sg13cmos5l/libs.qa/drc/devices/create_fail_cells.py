#!/usr/bin/env python3
"""
Create _fail QA cells for CMOS5L DRC testing.
Each cell contains intentional violations of specific rules.
"""

import klayout.db as pya

# Rule values from sg13cmos5l_tech_default.json
TV1_a = 0.42   # TopVia1 size (min and max)
TV1_b = 0.42   # TopVia1 spacing
TV1_c = 0.10   # M4 enclosure of TV1
TV1_d = 0.42   # TM1 enclosure of TV1
TM1_a = 1.64   # TM1 width
TM1_b = 1.64   # TM1 spacing
Pas_a = 2.1    # Passiv width
Pas_b = 3.5    # Passiv spacing
Pas_c = 2.1    # TM1 enclosure of Passiv

# Layer definitions
METAL4 = (50, 0)
TOPVIA1 = (125, 0)
TOPMETAL1 = (126, 0)
PASSIV = (9, 0)
POLYRES = (128, 0)
GATPOLY = (5, 0)
ACTIV = (1, 0)
PSD = (14, 0)
CONT = (6, 0)
METAL1 = (8, 0)
SALBLOCK = (28, 0)

def um(val):
    """Convert um to database units (nm)"""
    return int(val * 1000)

def create_sealring_fail(layout, cell):
    """Create sealring_complete_fail with TopVia1 and TopMetal1 violations."""

    # Get layers
    m4 = layout.layer(*METAL4)
    tv1 = layout.layer(*TOPVIA1)
    tm1 = layout.layer(*TOPMETAL1)
    pas = layout.layer(*PASSIV)

    x_offset = 0
    y_offset = 0

    # Violation 1: TV1.a - TopVia1 wrong size (0.50um instead of 0.42um)
    # Metal4 pad
    cell.shapes(m4).insert(pya.Box(um(x_offset), um(y_offset), um(x_offset + 2), um(y_offset + 2)))
    # TopMetal1 pad
    cell.shapes(tm1).insert(pya.Box(um(x_offset), um(y_offset), um(x_offset + 2), um(y_offset + 2)))
    # Wrong size TopVia1 (0.50 instead of 0.42)
    cell.shapes(tv1).insert(pya.Box(um(x_offset + 0.75), um(y_offset + 0.75),
                                     um(x_offset + 1.25), um(y_offset + 1.25)))  # 0.50um

    x_offset += 5

    # Violation 2: TV1.b - TopVia1 spacing too small (0.30um instead of 0.42um)
    cell.shapes(m4).insert(pya.Box(um(x_offset), um(y_offset), um(x_offset + 3), um(y_offset + 2)))
    cell.shapes(tm1).insert(pya.Box(um(x_offset), um(y_offset), um(x_offset + 3), um(y_offset + 2)))
    # Two vias too close (0.30um spacing)
    cell.shapes(tv1).insert(pya.Box(um(x_offset + 0.5), um(y_offset + 0.79),
                                     um(x_offset + 0.92), um(y_offset + 1.21)))  # 0.42um
    cell.shapes(tv1).insert(pya.Box(um(x_offset + 1.22), um(y_offset + 0.79),   # 0.30um gap
                                     um(x_offset + 1.64), um(y_offset + 1.21)))  # 0.42um

    x_offset += 5

    # Violation 3: TV1.d - TM1 enclosure of TopVia1 too small (0.20um instead of 0.42um)
    cell.shapes(m4).insert(pya.Box(um(x_offset), um(y_offset), um(x_offset + 2), um(y_offset + 2)))
    # TM1 with insufficient enclosure
    cell.shapes(tm1).insert(pya.Box(um(x_offset + 0.59), um(y_offset + 0.59),
                                     um(x_offset + 1.41), um(y_offset + 1.41)))  # Only 0.20um enclosure
    cell.shapes(tv1).insert(pya.Box(um(x_offset + 0.79), um(y_offset + 0.79),
                                     um(x_offset + 1.21), um(y_offset + 1.21)))  # 0.42um via

    x_offset += 5

    # Violation 4: TM1.a - TopMetal1 width too small (1.0um instead of 1.64um)
    cell.shapes(m4).insert(pya.Box(um(x_offset), um(y_offset), um(x_offset + 1), um(y_offset + 3)))
    cell.shapes(tm1).insert(pya.Box(um(x_offset), um(y_offset), um(x_offset + 1), um(y_offset + 3)))  # 1.0um width

    x_offset += 4

    # Violation 5: TM1.b - TopMetal1 spacing too small (1.0um instead of 1.64um)
    cell.shapes(m4).insert(pya.Box(um(x_offset), um(y_offset), um(x_offset + 2), um(y_offset + 3)))
    cell.shapes(m4).insert(pya.Box(um(x_offset + 3), um(y_offset), um(x_offset + 5), um(y_offset + 3)))  # 1.0um gap
    cell.shapes(tm1).insert(pya.Box(um(x_offset), um(y_offset), um(x_offset + 2), um(y_offset + 3)))
    cell.shapes(tm1).insert(pya.Box(um(x_offset + 3), um(y_offset), um(x_offset + 5), um(y_offset + 3)))

    print(f"  Created sealring_complete_fail with 5 violations: TV1.a, TV1.b, TV1.d, TM1.a, TM1.b")

def create_rsil_fail(layout, cell):
    """Create rsil_fail with silicide resistor violations."""

    # Rsil rules (from tech JSON):
    # Rsil_a: 0.5 (min width)
    # Rsil_b: 0.12 (min length)
    # Rsil_d: 0.18 (SalBlock enclosure)
    # Rsil_e: 0.18 (SalBlock to Cont)

    activ = layout.layer(*ACTIV)
    psd = layout.layer(*PSD)
    salblock = layout.layer(*SALBLOCK)
    cont = layout.layer(*CONT)
    m1 = layout.layer(*METAL1)

    x_offset = 0
    y_offset = 0

    # Create a basic rsil structure with violations
    # Violation: SalBlock width too small (0.3um instead of 0.5um)
    cell.shapes(activ).insert(pya.Box(um(x_offset), um(y_offset), um(x_offset + 3), um(y_offset + 1)))
    cell.shapes(psd).insert(pya.Box(um(x_offset), um(y_offset), um(x_offset + 3), um(y_offset + 1)))
    cell.shapes(salblock).insert(pya.Box(um(x_offset + 1), um(y_offset + 0.1),
                                          um(x_offset + 1.3), um(y_offset + 0.9)))  # 0.3um width

    # Contacts at ends
    cell.shapes(cont).insert(pya.Box(um(x_offset + 0.2), um(y_offset + 0.42),
                                      um(x_offset + 0.36), um(y_offset + 0.58)))
    cell.shapes(cont).insert(pya.Box(um(x_offset + 2.64), um(y_offset + 0.42),
                                      um(x_offset + 2.8), um(y_offset + 0.58)))
    cell.shapes(m1).insert(pya.Box(um(x_offset), um(y_offset + 0.3), um(x_offset + 0.5), um(y_offset + 0.7)))
    cell.shapes(m1).insert(pya.Box(um(x_offset + 2.5), um(y_offset + 0.3), um(x_offset + 3), um(y_offset + 0.7)))

    print(f"  Created rsil_fail with SalBlock width violation")

def create_rppd_fail(layout, cell):
    """Create rppd_fail with poly resistor violations."""

    # Use Gat.a (min GatPoly width 0.13um) and Gat.b (min space 0.18um)

    gatpoly = layout.layer(*GATPOLY)
    polyres = layout.layer(*POLYRES)
    cont = layout.layer(*CONT)
    m1 = layout.layer(*METAL1)

    x_offset = 0
    y_offset = 0

    # Violation 1: Gat.a - GatPoly width too small (0.10um instead of 0.13um)
    cell.shapes(gatpoly).insert(pya.Box(um(x_offset), um(y_offset), um(x_offset + 3), um(y_offset + 0.10)))
    cell.shapes(polyres).insert(pya.Box(um(x_offset + 0.5), um(y_offset - 0.1),
                                         um(x_offset + 2.5), um(y_offset + 0.2)))
    cell.shapes(m1).insert(pya.Box(um(x_offset), um(y_offset - 0.1), um(x_offset + 0.4), um(y_offset + 0.2)))
    cell.shapes(m1).insert(pya.Box(um(x_offset + 2.6), um(y_offset - 0.1), um(x_offset + 3), um(y_offset + 0.2)))

    y_offset += 1

    # Violation 2: Gat.b - GatPoly spacing too small (0.10um instead of 0.18um)
    cell.shapes(gatpoly).insert(pya.Box(um(x_offset), um(y_offset), um(x_offset + 1), um(y_offset + 0.5)))
    cell.shapes(gatpoly).insert(pya.Box(um(x_offset + 1.10), um(y_offset), um(x_offset + 2.1), um(y_offset + 0.5)))  # 0.10um gap
    cell.shapes(m1).insert(pya.Box(um(x_offset), um(y_offset + 0.1), um(x_offset + 1), um(y_offset + 0.4)))
    cell.shapes(m1).insert(pya.Box(um(x_offset + 1.10), um(y_offset + 0.1), um(x_offset + 2.1), um(y_offset + 0.4)))

    print(f"  Created rppd_fail with Gat.a and Gat.b violations")

def create_rhigh_fail(layout, cell):
    """Create rhigh_fail with high-res poly resistor violations."""

    # Use Gat.a (min GatPoly width 0.13um) and M1 rules

    gatpoly = layout.layer(*GATPOLY)
    polyres = layout.layer(*POLYRES)
    m1 = layout.layer(*METAL1)

    x_offset = 0
    y_offset = 0

    # Violation 1: Gat.a - GatPoly width too small (0.08um instead of 0.13um)
    cell.shapes(gatpoly).insert(pya.Box(um(x_offset), um(y_offset), um(x_offset + 4), um(y_offset + 0.08)))
    cell.shapes(polyres).insert(pya.Box(um(x_offset + 0.5), um(y_offset - 0.1),
                                         um(x_offset + 3.5), um(y_offset + 0.2)))
    cell.shapes(m1).insert(pya.Box(um(x_offset), um(y_offset - 0.1), um(x_offset + 0.4), um(y_offset + 0.2)))
    cell.shapes(m1).insert(pya.Box(um(x_offset + 3.6), um(y_offset - 0.1), um(x_offset + 4), um(y_offset + 0.2)))

    y_offset += 1

    # Violation 2: M1.a - Metal1 width too small (0.10um instead of 0.16um)
    cell.shapes(gatpoly).insert(pya.Box(um(x_offset), um(y_offset), um(x_offset + 2), um(y_offset + 0.5)))
    cell.shapes(polyres).insert(pya.Box(um(x_offset + 0.3), um(y_offset - 0.1),
                                         um(x_offset + 1.7), um(y_offset + 0.6)))
    cell.shapes(m1).insert(pya.Box(um(x_offset), um(y_offset + 0.2), um(x_offset + 0.1), um(y_offset + 0.7)))  # 0.10um width

    print(f"  Created rhigh_fail with Gat.a and M1.a violations")

def main():
    qa_gds = "/home/montanares/git/slim-pdk/IHP-Open-PDK/ihp-sg13cmos5l/libs.qa/drc/devices/gds/sg13cmos5l_qacells.gds"

    # Load QA layout
    layout = pya.Layout()
    layout.read(qa_gds)

    print("Updating _fail cells for CMOS5L DRC...")

    # Find and update each _fail cell
    for i in range(layout.cells()):
        cell = layout.cell(i)

        if cell.name == "sealring_complete_fail":
            cell.clear()
            create_sealring_fail(layout, cell)

        elif cell.name == "rsil_fail":
            cell.clear()
            create_rsil_fail(layout, cell)

        elif cell.name == "rppd_fail":
            cell.clear()
            create_rppd_fail(layout, cell)

        elif cell.name == "rhigh_fail":
            cell.clear()
            create_rhigh_fail(layout, cell)

    # Save
    layout.write(qa_gds)
    print(f"\nSaved to {qa_gds}")

if __name__ == "__main__":
    main()
