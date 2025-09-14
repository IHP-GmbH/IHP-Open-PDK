"""Resistor components for IHP PDK."""

from typing import Literal, Optional

import gdsfactory as gf
from gdsfactory import Component


# Define layers for resistors
LAYERS = {
    "Rsil": (6, 10),
    "Rppd": (31, 10),
    "Rhigh": (85, 0),
    "PolyRes": (86, 0),
    "Activ": (1, 0),
    "GatPoly": (5, 0),
    "pSD": (14, 0),
    "nSD": (16, 0),
    "NWell": (31, 0),
    "SiProtection": (2, 6),
    "Cont": (6, 0),
    "Metal1": (8, 0),
    "Metal2": (10, 0),
    "Via1": (19, 0),
    "ResistorMark": (110, 5),
    "TEXT": (63, 63),
}


@gf.cell
def rsil(
    width: float = 0.8,
    length: float = 10.0,
    resistance: Optional[float] = None,
    model: str = "rsil",
) -> Component:
    """Create a silicided polysilicon resistor.

    Args:
        width: Width of the resistor in micrometers.
        length: Length of the resistor in micrometers.
        resistance: Target resistance in ohms (optional).
        model: Device model name.

    Returns:
        Component with silicided poly resistor layout.
    """
    c = Component()

    # Design rules
    rsil_min_width = 0.4
    rsil_min_length = 0.8
    sheet_resistance = 7.0  # ohms/square (example)
    cont_size = 0.16
    cont_enc = 0.07
    metal_enc = 0.06
    end_extension = 0.4

    # Validate dimensions
    width = max(width, rsil_min_width)
    length = max(length, rsil_min_length)

    # Grid snap
    grid = 0.005
    width = round(width / grid) * grid
    length = round(length / grid) * grid

    # Calculate resistance if not provided
    if resistance is None:
        n_squares = length / width
        resistance = n_squares * sheet_resistance

    # Create resistor body (polysilicon)
    res_body = gf.components.rectangle(
        size=(length, width),
        layer=LAYERS["GatPoly"],
        centered=True,
    )
    c.add_ref(res_body)

    # Silicide blocking layer
    sil_block = gf.components.rectangle(
        size=(length + 0.2, width + 0.2),
        layer=LAYERS["Rsil"],
        centered=True,
    )
    c.add_ref(sil_block)

    # End contact regions (polysilicon extensions)
    # Left contact region
    left_contact = gf.components.rectangle(
        size=(end_extension, width),
        layer=LAYERS["GatPoly"],
    )
    left_ref = c.add_ref(left_contact)
    left_ref.move((-(length/2 + end_extension), -width/2))

    # Right contact region
    right_contact = gf.components.rectangle(
        size=(end_extension, width),
        layer=LAYERS["GatPoly"],
    )
    right_ref = c.add_ref(right_contact)
    right_ref.move((length/2, -width/2))

    # Contacts at ends
    n_cont_y = int((width - cont_size) / (cont_size + 0.18)) + 1

    for i in range(n_cont_y):
        y_pos = -width/2 + cont_enc + i * (cont_size + 0.18)

        # Left contact
        cont_left = gf.components.rectangle(
            size=(cont_size, cont_size),
            layer=LAYERS["Cont"],
        )
        cont_left_ref = c.add_ref(cont_left)
        cont_left_ref.move((-(length/2 + end_extension/2) - cont_size/2, y_pos))

        # Right contact
        cont_right = gf.components.rectangle(
            size=(cont_size, cont_size),
            layer=LAYERS["Cont"],
        )
        cont_right_ref = c.add_ref(cont_right)
        cont_right_ref.move(((length/2 + end_extension/2) - cont_size/2, y_pos))

    # Metal1 connections
    # Left metal
    m1_left = gf.components.rectangle(
        size=(end_extension + 2 * metal_enc, width + 2 * metal_enc),
        layer=LAYERS["Metal1"],
    )
    m1_left_ref = c.add_ref(m1_left)
    m1_left_ref.move((-(length/2 + end_extension + metal_enc), -width/2 - metal_enc))

    # Right metal
    m1_right = gf.components.rectangle(
        size=(end_extension + 2 * metal_enc, width + 2 * metal_enc),
        layer=LAYERS["Metal1"],
    )
    m1_right_ref = c.add_ref(m1_right)
    m1_right_ref.move((length/2 - metal_enc, -width/2 - metal_enc))

    # Resistor marker
    res_mark = gf.components.rectangle(
        size=(length + 2 * end_extension + 0.5, width + 0.5),
        layer=LAYERS["ResistorMark"],
        centered=True,
    )
    c.add_ref(res_mark)

    # Add ports
    c.add_port(
        name="P1",
        center=(-(length/2 + end_extension), 0),
        width=width,
        orientation=180,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    c.add_port(
        name="P2",
        center=(length/2 + end_extension, 0),
        width=width,
        orientation=0,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    # Add metadata
    c.info["model"] = model
    c.info["width"] = width
    c.info["length"] = length
    c.info["resistance"] = resistance
    c.info["sheet_resistance"] = sheet_resistance
    c.info["n_squares"] = length / width

    return c


@gf.cell
def rppd(
    width: float = 0.8,
    length: float = 10.0,
    resistance: Optional[float] = None,
    model: str = "rppd",
) -> Component:
    """Create a P+ polysilicon resistor.

    Args:
        width: Width of the resistor in micrometers.
        length: Length of the resistor in micrometers.
        resistance: Target resistance in ohms (optional).
        model: Device model name.

    Returns:
        Component with P+ poly resistor layout.
    """
    c = Component()

    # Design rules
    rppd_min_width = 0.4
    rppd_min_length = 0.8
    sheet_resistance = 300.0  # ohms/square (high resistance)
    cont_size = 0.16
    cont_enc = 0.07
    metal_enc = 0.06
    end_extension = 0.4

    # Validate dimensions
    width = max(width, rppd_min_width)
    length = max(length, rppd_min_length)

    # Grid snap
    grid = 0.005
    width = round(width / grid) * grid
    length = round(length / grid) * grid

    # Calculate resistance if not provided
    if resistance is None:
        n_squares = length / width
        resistance = n_squares * sheet_resistance

    # Create resistor body (polysilicon)
    res_body = gf.components.rectangle(
        size=(length, width),
        layer=LAYERS["GatPoly"],
        centered=True,
    )
    c.add_ref(res_body)

    # P+ doping layer
    p_doping = gf.components.rectangle(
        size=(length + 2 * end_extension, width + 0.2),
        layer=LAYERS["pSD"],
        centered=True,
    )
    c.add_ref(p_doping)

    # RPPD marker layer
    rppd_mark = gf.components.rectangle(
        size=(length, width),
        layer=LAYERS["Rppd"],
        centered=True,
    )
    c.add_ref(rppd_mark)

    # End contact regions
    # Left contact region
    left_contact = gf.components.rectangle(
        size=(end_extension, width),
        layer=LAYERS["GatPoly"],
    )
    left_ref = c.add_ref(left_contact)
    left_ref.move((-(length/2 + end_extension), -width/2))

    # Right contact region
    right_contact = gf.components.rectangle(
        size=(end_extension, width),
        layer=LAYERS["GatPoly"],
    )
    right_ref = c.add_ref(right_contact)
    right_ref.move((length/2, -width/2))

    # Contacts at ends
    n_cont_y = int((width - cont_size) / (cont_size + 0.18)) + 1

    for i in range(n_cont_y):
        y_pos = -width/2 + cont_enc + i * (cont_size + 0.18)

        # Left contact
        cont_left = gf.components.rectangle(
            size=(cont_size, cont_size),
            layer=LAYERS["Cont"],
        )
        cont_left_ref = c.add_ref(cont_left)
        cont_left_ref.move((-(length/2 + end_extension/2) - cont_size/2, y_pos))

        # Right contact
        cont_right = gf.components.rectangle(
            size=(cont_size, cont_size),
            layer=LAYERS["Cont"],
        )
        cont_right_ref = c.add_ref(cont_right)
        cont_right_ref.move(((length/2 + end_extension/2) - cont_size/2, y_pos))

    # Metal1 connections
    # Left metal
    m1_left = gf.components.rectangle(
        size=(end_extension + 2 * metal_enc, width + 2 * metal_enc),
        layer=LAYERS["Metal1"],
    )
    m1_left_ref = c.add_ref(m1_left)
    m1_left_ref.move((-(length/2 + end_extension + metal_enc), -width/2 - metal_enc))

    # Right metal
    m1_right = gf.components.rectangle(
        size=(end_extension + 2 * metal_enc, width + 2 * metal_enc),
        layer=LAYERS["Metal1"],
    )
    m1_right_ref = c.add_ref(m1_right)
    m1_right_ref.move((length/2 - metal_enc, -width/2 - metal_enc))

    # Resistor marker
    res_mark = gf.components.rectangle(
        size=(length + 2 * end_extension + 0.5, width + 0.5),
        layer=LAYERS["ResistorMark"],
        centered=True,
    )
    c.add_ref(res_mark)

    # Add ports
    c.add_port(
        name="P1",
        center=(-(length/2 + end_extension), 0),
        width=width,
        orientation=180,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    c.add_port(
        name="P2",
        center=(length/2 + end_extension, 0),
        width=width,
        orientation=0,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    # Add metadata
    c.info["model"] = model
    c.info["width"] = width
    c.info["length"] = length
    c.info["resistance"] = resistance
    c.info["sheet_resistance"] = sheet_resistance
    c.info["n_squares"] = length / width

    return c


@gf.cell
def rhigh(
    width: float = 1.4,
    length: float = 20.0,
    resistance: Optional[float] = None,
    model: str = "rhigh",
) -> Component:
    """Create a high-resistance polysilicon resistor.

    Args:
        width: Width of the resistor in micrometers.
        length: Length of the resistor in micrometers.
        resistance: Target resistance in ohms (optional).
        model: Device model name.

    Returns:
        Component with high-resistance poly resistor layout.
    """
    c = Component()

    # Design rules
    rhigh_min_width = 1.4
    rhigh_min_length = 5.0
    sheet_resistance = 1350.0  # ohms/square (very high resistance)
    cont_size = 0.16
    cont_enc = 0.07
    metal_enc = 0.06
    end_extension = 0.8
    isolation_enc = 0.5

    # Validate dimensions
    width = max(width, rhigh_min_width)
    length = max(length, rhigh_min_length)

    # Grid snap
    grid = 0.005
    width = round(width / grid) * grid
    length = round(length / grid) * grid

    # Calculate resistance if not provided
    if resistance is None:
        n_squares = length / width
        resistance = n_squares * sheet_resistance

    # N-Well for isolation
    nwell = gf.components.rectangle(
        size=(length + 2 * end_extension + 2 * isolation_enc,
               width + 2 * isolation_enc),
        layer=LAYERS["NWell"],
        centered=True,
    )
    c.add_ref(nwell)

    # Create resistor body (polysilicon)
    res_body = gf.components.rectangle(
        size=(length, width),
        layer=LAYERS["GatPoly"],
        centered=True,
    )
    c.add_ref(res_body)

    # High resistance marker
    rhigh_mark = gf.components.rectangle(
        size=(length + 0.2, width + 0.2),
        layer=LAYERS["Rhigh"],
        centered=True,
    )
    c.add_ref(rhigh_mark)

    # End contact regions
    # Left contact region
    left_contact = gf.components.rectangle(
        size=(end_extension, width),
        layer=LAYERS["GatPoly"],
    )
    left_ref = c.add_ref(left_contact)
    left_ref.move((-(length/2 + end_extension), -width/2))

    # Right contact region
    right_contact = gf.components.rectangle(
        size=(end_extension, width),
        layer=LAYERS["GatPoly"],
    )
    right_ref = c.add_ref(right_contact)
    right_ref.move((length/2, -width/2))

    # Contacts at ends (larger contacts for high resistance)
    n_cont_x = 2  # Multiple contacts in X for better connection
    n_cont_y = int((width - cont_size) / (cont_size + 0.18)) + 1

    for i in range(n_cont_x):
        for j in range(n_cont_y):
            x_offset = i * (cont_size + 0.18)
            y_pos = -width/2 + cont_enc + j * (cont_size + 0.18)

            # Left contacts
            cont_left = gf.components.rectangle(
                size=(cont_size, cont_size),
                layer=LAYERS["Cont"],
            )
            cont_left_ref = c.add_ref(cont_left)
            cont_left_ref.move((
                -(length/2 + end_extension - cont_enc - x_offset),
                y_pos
            ))

            # Right contacts
            cont_right = gf.components.rectangle(
                size=(cont_size, cont_size),
                layer=LAYERS["Cont"],
            )
            cont_right_ref = c.add_ref(cont_right)
            cont_right_ref.move((
                length/2 + end_extension - cont_enc - cont_size - x_offset,
                y_pos
            ))

    # Metal1 connections (wider for lower contact resistance)
    # Left metal
    m1_left = gf.components.rectangle(
        size=(end_extension + 2 * metal_enc, width + 2 * metal_enc),
        layer=LAYERS["Metal1"],
    )
    m1_left_ref = c.add_ref(m1_left)
    m1_left_ref.move((-(length/2 + end_extension + metal_enc), -width/2 - metal_enc))

    # Right metal
    m1_right = gf.components.rectangle(
        size=(end_extension + 2 * metal_enc, width + 2 * metal_enc),
        layer=LAYERS["Metal1"],
    )
    m1_right_ref = c.add_ref(m1_right)
    m1_right_ref.move((length/2 - metal_enc, -width/2 - metal_enc))

    # Resistor marker
    res_mark = gf.components.rectangle(
        size=(length + 2 * end_extension + 1.0, width + 1.0),
        layer=LAYERS["ResistorMark"],
        centered=True,
    )
    c.add_ref(res_mark)

    # Add ports
    c.add_port(
        name="P1",
        center=(-(length/2 + end_extension), 0),
        width=width,
        orientation=180,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    c.add_port(
        name="P2",
        center=(length/2 + end_extension, 0),
        width=width,
        orientation=0,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    # Add metadata
    c.info["model"] = model
    c.info["width"] = width
    c.info["length"] = length
    c.info["resistance"] = resistance
    c.info["sheet_resistance"] = sheet_resistance
    c.info["n_squares"] = length / width

    return c


if __name__ == "__main__":
    # Test the components
    c1 = rsil(width=1.0, length=10.0)
    c1.show()

    c2 = rppd(width=0.8, length=20.0)
    c2.show()

    c3 = rhigh(width=1.4, length=50.0)
    c3.show()