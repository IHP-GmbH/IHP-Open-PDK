"""Capacitor components for IHP PDK."""

import gdsfactory as gf
from gdsfactory import Component

# Define layers for capacitors
LAYERS = {
    "Metal1": (8, 0),
    "Metal2": (10, 0),
    "Metal3": (30, 0),
    "Metal4": (50, 0),
    "Metal5": (67, 0),
    "TopMetal1": (126, 5),
    "TopMetal2": (134, 5),
    "Via1": (19, 0),
    "Via2": (29, 0),
    "Via3": (49, 0),
    "Via4": (66, 0),
    "TopVia1": (125, 5),
    "TopVia2": (133, 5),
    "MIM": (36, 0),
    "RFPad": (81, 0),
    "CapMark": (34, 0),
    "NoMetFiller": (34, 10),
    "TEXT": (63, 63),
}


@gf.cell
def cmim(
    width: float = 5.0,
    length: float = 5.0,
    capacitance: float | None = None,
    model: str = "cmim",
) -> Component:
    """Create a MIM (Metal-Insulator-Metal) capacitor.

    Args:
        width: Width of the capacitor in micrometers.
        length: Length of the capacitor in micrometers.
        capacitance: Target capacitance in fF (optional).
        model: Device model name.

    Returns:
        Component with MIM capacitor layout.
    """
    c = Component()

    # Design rules
    mim_min_size = 0.5
    plate_enclosure = 0.2
    via_enclosure = 0.1
    cont_size = 0.26
    cont_spacing = 0.36
    cap_density = 1.5  # fF/um^2 (example value)

    # Validate dimensions
    width = max(width, mim_min_size)
    length = max(length, mim_min_size)

    # Grid snap
    grid = 0.005
    width = round(width / grid) * grid
    length = round(length / grid) * grid

    # Calculate capacitance if not provided
    if capacitance is None:
        capacitance = width * length * cap_density

    # Bottom plate (Metal4)
    bottom_plate_width = width + 2 * plate_enclosure
    bottom_plate_length = length + 2 * plate_enclosure

    bottom_plate = gf.components.rectangle(
        size=(bottom_plate_length, bottom_plate_width),
        layer=LAYERS["Metal4"],
        centered=True,
    )
    c.add_ref(bottom_plate)

    # MIM dielectric layer
    mim_layer = gf.components.rectangle(
        size=(length, width),
        layer=LAYERS["MIM"],
        centered=True,
    )
    c.add_ref(mim_layer)

    # Top plate (Metal5)
    top_plate = gf.components.rectangle(
        size=(length, width),
        layer=LAYERS["Metal5"],
        centered=True,
    )
    c.add_ref(top_plate)

    # Via array for top plate connection
    n_vias_x = int((length - 2 * via_enclosure - cont_size) / cont_spacing) + 1
    n_vias_y = int((width - 2 * via_enclosure - cont_size) / cont_spacing) + 1

    for i in range(n_vias_x):
        for j in range(n_vias_y):
            x = -length / 2 + via_enclosure + cont_size / 2 + i * cont_spacing
            y = -width / 2 + via_enclosure + cont_size / 2 + j * cont_spacing

            via = gf.components.rectangle(
                size=(cont_size, cont_size),
                layer=LAYERS["Via4"],
                centered=True,
            )
            via_ref = c.add_ref(via)
            via_ref.move((x, y))

    # Connection extensions for bottom plate
    # Left extension
    bottom_ext_left = gf.components.rectangle(
        size=(plate_enclosure + 1.0, 1.0),
        layer=LAYERS["Metal4"],
    )
    bottom_ext_left_ref = c.add_ref(bottom_ext_left)
    bottom_ext_left_ref.move((-(bottom_plate_length / 2), -0.5))

    # Right extension for top plate
    top_ext_right = gf.components.rectangle(
        size=(1.0, 1.0),
        layer=LAYERS["Metal5"],
    )
    top_ext_right_ref = c.add_ref(top_ext_right)
    top_ext_right_ref.move((length / 2, -0.5))

    # Via to connect top plate extension to TopMetal1
    top_via = gf.components.rectangle(
        size=(0.9, 0.9),
        layer=LAYERS["TopVia1"],
        centered=True,
    )
    top_via_ref = c.add_ref(top_via)
    top_via_ref.move((length / 2 + 0.5, 0))

    top_metal = gf.components.rectangle(
        size=(1.2, 1.2),
        layer=LAYERS["TopMetal1"],
        centered=True,
    )
    top_metal_ref = c.add_ref(top_metal)
    top_metal_ref.move((length / 2 + 0.5, 0))

    # Capacitor marker
    cap_mark = gf.components.rectangle(
        size=(bottom_plate_length + 0.5, bottom_plate_width + 0.5),
        layer=LAYERS["CapMark"],
        centered=True,
    )
    c.add_ref(cap_mark)

    # No metal filler region
    no_fill = gf.components.rectangle(
        size=(bottom_plate_length + 1.0, bottom_plate_width + 1.0),
        layer=LAYERS["NoMetFiller"],
        centered=True,
    )
    c.add_ref(no_fill)

    # Add ports
    c.add_port(
        name="P1",
        center=(-(bottom_plate_length / 2 + 0.5), 0),
        width=1.0,
        orientation=180,
        layer=LAYERS["Metal4"],
        port_type="electrical",
    )

    c.add_port(
        name="P2",
        center=(length / 2 + 0.5, 0),
        width=1.0,
        orientation=0,
        layer=LAYERS["TopMetal1"],
        port_type="electrical",
    )

    # Add metadata
    c.info["model"] = model
    c.info["width"] = width
    c.info["length"] = length
    c.info["capacitance_fF"] = capacitance
    c.info["area_um2"] = width * length

    return c


@gf.cell
def rfcmim(
    width: float = 10.0,
    length: float = 10.0,
    capacitance: float | None = None,
    model: str = "rfcmim",
) -> Component:
    """Create an RF MIM capacitor with optimized layout.

    Args:
        width: Width of the capacitor in micrometers.
        length: Length of the capacitor in micrometers.
        capacitance: Target capacitance in fF (optional).
        model: Device model name.

    Returns:
        Component with RF MIM capacitor layout.
    """
    c = Component()

    # Design rules for RF capacitor
    mim_min_size = 5.0  # Larger minimum for RF
    plate_enclosure = 0.3
    via_enclosure = 0.15
    cont_size = 0.26
    cont_spacing = 0.36
    cap_density = 1.5  # fF/um^2
    shield_enclosure = 2.0

    # Validate dimensions
    width = max(width, mim_min_size)
    length = max(length, mim_min_size)

    # Grid snap
    grid = 0.005
    width = round(width / grid) * grid
    length = round(length / grid) * grid

    # Calculate capacitance if not provided
    if capacitance is None:
        capacitance = width * length * cap_density

    # Ground shield (Metal3)
    shield_width = width + 2 * shield_enclosure
    shield_length = length + 2 * shield_enclosure

    ground_shield = gf.components.rectangle(
        size=(shield_length, shield_width),
        layer=LAYERS["Metal3"],
        centered=True,
    )
    c.add_ref(ground_shield)

    # Bottom plate (Metal4)
    bottom_plate_width = width + 2 * plate_enclosure
    bottom_plate_length = length + 2 * plate_enclosure

    bottom_plate = gf.components.rectangle(
        size=(bottom_plate_length, bottom_plate_width),
        layer=LAYERS["Metal4"],
        centered=True,
    )
    c.add_ref(bottom_plate)

    # MIM dielectric layer
    mim_layer = gf.components.rectangle(
        size=(length, width),
        layer=LAYERS["MIM"],
        centered=True,
    )
    c.add_ref(mim_layer)

    # Top plate (Metal5)
    top_plate = gf.components.rectangle(
        size=(length, width),
        layer=LAYERS["Metal5"],
        centered=True,
    )
    c.add_ref(top_plate)

    # Via array for top plate connection (denser for RF)
    n_vias_x = int((length - 2 * via_enclosure - cont_size) / cont_spacing) + 1
    n_vias_y = int((width - 2 * via_enclosure - cont_size) / cont_spacing) + 1

    for i in range(n_vias_x):
        for j in range(n_vias_y):
            x = -length / 2 + via_enclosure + cont_size / 2 + i * cont_spacing
            y = -width / 2 + via_enclosure + cont_size / 2 + j * cont_spacing

            via = gf.components.rectangle(
                size=(cont_size, cont_size),
                layer=LAYERS["Via4"],
                centered=True,
            )
            via_ref = c.add_ref(via)
            via_ref.move((x, y))

    # RF pad connections
    # Bottom plate pad
    bottom_pad = gf.components.rectangle(
        size=(2.0, 2.0),
        layer=LAYERS["Metal4"],
    )
    bottom_pad_ref = c.add_ref(bottom_pad)
    bottom_pad_ref.move((-(bottom_plate_length / 2 + 1.0), -1.0))

    # Top plate pad
    top_pad = gf.components.rectangle(
        size=(2.0, 2.0),
        layer=LAYERS["TopMetal1"],
    )
    top_pad_ref = c.add_ref(top_pad)
    top_pad_ref.move((length / 2 + 1.0, -1.0))

    # Connect top plate to TopMetal1
    # Via stack from Metal5 to TopMetal1
    via5_array = gf.components.rectangle(
        size=(0.9, 0.9),
        layer=LAYERS["TopVia1"],
        centered=True,
    )
    via5_ref = c.add_ref(via5_array)
    via5_ref.move((length / 2 + 2.0, 0))

    tm1_connect = gf.components.rectangle(
        size=(2.0, 1.0),
        layer=LAYERS["TopMetal1"],
    )
    tm1_ref = c.add_ref(tm1_connect)
    tm1_ref.move((length / 2 + 1.0, -0.5))

    # RF pad marker
    rf_pad1 = gf.components.rectangle(
        size=(3.0, 3.0),
        layer=LAYERS["RFPad"],
        centered=True,
    )
    rf_pad1_ref = c.add_ref(rf_pad1)
    rf_pad1_ref.move((-(bottom_plate_length / 2 + 1.0), 0))

    rf_pad2 = gf.components.rectangle(
        size=(3.0, 3.0),
        layer=LAYERS["RFPad"],
        centered=True,
    )
    rf_pad2_ref = c.add_ref(rf_pad2)
    rf_pad2_ref.move((length / 2 + 2.0, 0))

    # Capacitor marker
    cap_mark = gf.components.rectangle(
        size=(shield_length, shield_width),
        layer=LAYERS["CapMark"],
        centered=True,
    )
    c.add_ref(cap_mark)

    # Add ports
    c.add_port(
        name="P1",
        center=(-(bottom_plate_length / 2 + 1.0), 0),
        width=2.0,
        orientation=180,
        layer=LAYERS["Metal4"],
        port_type="electrical",
    )

    c.add_port(
        name="P2",
        center=(length / 2 + 2.0, 0),
        width=2.0,
        orientation=0,
        layer=LAYERS["TopMetal1"],
        port_type="electrical",
    )

    c.add_port(
        name="GND",
        center=(0, -shield_width / 2),
        width=shield_length,
        orientation=270,
        layer=LAYERS["Metal3"],
        port_type="electrical",
    )

    # Add metadata
    c.info["model"] = model
    c.info["width"] = width
    c.info["length"] = length
    c.info["capacitance_fF"] = capacitance
    c.info["area_um2"] = width * length
    c.info["type"] = "rf_capacitor"

    return c


if __name__ == "__main__":
    # Test the components
    c1 = cmim(width=10, length=10)
    c1.show()

    c2 = rfcmim(width=20, length=20)
    c2.show()
