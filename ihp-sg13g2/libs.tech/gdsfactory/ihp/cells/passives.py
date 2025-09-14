"""Passive components (varicaps, ESD, taps, seal rings) for IHP PDK."""

import gdsfactory as gf
from gdsfactory import Component

# Define layers
LAYERS = {
    "NWell": (31, 0),
    "PWell": (29, 0),
    "Activ": (1, 0),
    "GatPoly": (5, 0),
    "pSD": (14, 0),
    "nSD": (16, 0),
    "Ptap": (13, 0),
    "Ntap": (26, 0),
    "Cont": (6, 0),
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
    "Varicap": (87, 0),
    "ESD": (88, 0),
    "SealRing": (167, 5),
    "TEXT": (63, 63),
}


@gf.cell
def svaricap(
    width: float = 1.0,
    length: float = 1.0,
    nf: int = 1,
    model: str = "svaricap",
) -> Component:
    """Create a MOS varicap (variable capacitor).

    Args:
        width: Width of the varicap in micrometers.
        length: Length of the varicap in micrometers.
        nf: Number of fingers.
        model: Device model name.

    Returns:
        Component with varicap layout.
    """
    c = Component()

    # Design rules
    var_min_width = 0.5
    var_min_length = 0.5
    gate_ext = 0.18
    active_ext = 0.23
    cont_size = 0.16
    cont_enc = 0.07
    nwell_enc = 0.31

    # Validate dimensions
    width = max(width, var_min_width)
    length = max(length, var_min_length)

    # Grid snap
    grid = 0.005
    width = round(width / grid) * grid
    length = round(length / grid) * grid

    # Calculate finger dimensions
    finger_width = width / nf
    finger_pitch = finger_width + 0.5

    # N-Well
    nwell = gf.components.rectangle(
        size=(
            length + 2 * active_ext + 2 * nwell_enc,
            nf * finger_pitch + 2 * nwell_enc,
        ),
        layer=LAYERS["NWell"],
        centered=True,
    )
    c.add_ref(nwell)

    # Create varicap fingers
    for i in range(nf):
        y_offset = (i - nf / 2 + 0.5) * finger_pitch

        # Gate poly (acts as one terminal)
        gate = gf.components.rectangle(
            size=(length, finger_width + 2 * gate_ext),
            layer=LAYERS["GatPoly"],
        )
        gate_ref = c.add_ref(gate)
        gate_ref.move((-length / 2, y_offset - finger_width / 2 - gate_ext))

        # Active region (acts as other terminal)
        active = gf.components.rectangle(
            size=(length + 2 * active_ext, finger_width),
            layer=LAYERS["Activ"],
        )
        active_ref = c.add_ref(active)
        active_ref.move((-length / 2 - active_ext, y_offset - finger_width / 2))

        # N+ implant for active region
        nsd = gf.components.rectangle(
            size=(length + 2 * active_ext, finger_width),
            layer=LAYERS["nSD"],
        )
        nsd_ref = c.add_ref(nsd)
        nsd_ref.move((-length / 2 - active_ext, y_offset - finger_width / 2))

        # Contacts on active regions (source/drain)
        # Left side contacts
        cont_left = gf.components.rectangle(
            size=(cont_size, cont_size),
            layer=LAYERS["Cont"],
        )
        cont_left_ref = c.add_ref(cont_left)
        cont_left_ref.move(
            (-length / 2 - active_ext + cont_enc, y_offset - cont_size / 2)
        )

        # Right side contacts
        cont_right = gf.components.rectangle(
            size=(cont_size, cont_size),
            layer=LAYERS["Cont"],
        )
        cont_right_ref = c.add_ref(cont_right)
        cont_right_ref.move(
            (length / 2 + active_ext - cont_enc - cont_size, y_offset - cont_size / 2)
        )

    # Metal connections
    # Gate connection (Metal1)
    gate_metal = gf.components.rectangle(
        size=(1.0, nf * finger_pitch),
        layer=LAYERS["Metal1"],
    )
    gate_metal_ref = c.add_ref(gate_metal)
    gate_metal_ref.move((-length / 2 - 1.5, -nf * finger_pitch / 2))

    # Active connection (Metal1)
    active_metal = gf.components.rectangle(
        size=(1.0, nf * finger_pitch),
        layer=LAYERS["Metal1"],
    )
    active_metal_ref = c.add_ref(active_metal)
    active_metal_ref.move((length / 2 + 0.5, -nf * finger_pitch / 2))

    # Varicap marker
    var_mark = gf.components.rectangle(
        size=(length + 2 * active_ext + 0.5, nf * finger_pitch + 0.5),
        layer=LAYERS["Varicap"],
        centered=True,
    )
    c.add_ref(var_mark)

    # Add ports
    c.add_port(
        name="G",
        center=(-length / 2 - 1.0, 0),
        width=nf * finger_pitch,
        orientation=180,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    c.add_port(
        name="B",
        center=(length / 2 + 1.0, 0),
        width=nf * finger_pitch,
        orientation=0,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    # Add metadata
    c.info["model"] = model
    c.info["width"] = width
    c.info["length"] = length
    c.info["nf"] = nf
    c.info["type"] = "varicap"

    return c


@gf.cell
def esd_nmos(
    width: float = 50.0,
    length: float = 0.5,
    nf: int = 10,
    model: str = "esd_nmos",
) -> Component:
    """Create an ESD protection NMOS device.

    Args:
        width: Total width of the ESD device in micrometers.
        length: Gate length in micrometers.
        nf: Number of fingers.
        model: Device model name.

    Returns:
        Component with ESD NMOS layout.
    """
    c = Component()

    # Design rules for ESD devices
    gate_width = width / nf
    gate_length = length
    gate_ext = 0.18
    active_ext = 0.3  # Larger for ESD
    cont_size = 0.16
    cont_spacing = 0.18
    cont_enc = 0.07
    metal_enc = 0.06
    pwell_enc = 0.5

    # Grid snap
    grid = 0.005
    gate_width = round(gate_width / grid) * grid
    gate_length = round(gate_length / grid) * grid

    # P-Well for ESD NMOS
    pwell = gf.components.rectangle(
        size=(
            (gate_length + 2 * active_ext) * nf + pwell_enc * 2,
            gate_width + 2 * gate_ext + pwell_enc * 2,
        ),
        layer=LAYERS["PWell"],
        centered=True,
    )
    c.add_ref(pwell)

    # Create multi-finger ESD structure
    finger_pitch = gate_length + 2 * active_ext + 0.5

    for i in range(nf):
        x_offset = (i - nf / 2 + 0.5) * finger_pitch

        # Gate poly
        gate = gf.components.rectangle(
            size=(gate_length, gate_width + 2 * gate_ext),
            layer=LAYERS["GatPoly"],
        )
        gate_ref = c.add_ref(gate)
        gate_ref.move((x_offset - gate_length / 2, -gate_width / 2 - gate_ext))

        # Active region
        active = gf.components.rectangle(
            size=(gate_length + 2 * active_ext, gate_width),
            layer=LAYERS["Activ"],
        )
        active_ref = c.add_ref(active)
        active_ref.move((x_offset - gate_length / 2 - active_ext, -gate_width / 2))

        # N+ implant
        nsd = gf.components.rectangle(
            size=(gate_length + 2 * active_ext, gate_width),
            layer=LAYERS["nSD"],
        )
        nsd_ref = c.add_ref(nsd)
        nsd_ref.move((x_offset - gate_length / 2 - active_ext, -gate_width / 2))

        # Source/Drain contacts
        n_cont_y = int((gate_width - cont_size) / cont_spacing) + 1

        for j in range(n_cont_y):
            y_pos = -gate_width / 2 + cont_enc + j * cont_spacing

            # Source contact
            cont_s = gf.components.rectangle(
                size=(cont_size, cont_size),
                layer=LAYERS["Cont"],
            )
            cont_s_ref = c.add_ref(cont_s)
            cont_s_ref.move((x_offset - gate_length / 2 - active_ext + cont_enc, y_pos))

            # Drain contact
            cont_d = gf.components.rectangle(
                size=(cont_size, cont_size),
                layer=LAYERS["Cont"],
            )
            cont_d_ref = c.add_ref(cont_d)
            cont_d_ref.move((x_offset + gate_length / 2 + cont_enc, y_pos))

    # Metal bus connections
    # Source bus (connected to ground)
    source_bus = gf.components.rectangle(
        size=(nf * finger_pitch, gate_width + 2 * metal_enc),
        layer=LAYERS["Metal1"],
    )
    source_bus_ref = c.add_ref(source_bus)
    source_bus_ref.move((-nf * finger_pitch / 2, -gate_width / 2 - metal_enc))

    # Drain bus (connected to I/O pad)
    drain_bus = gf.components.rectangle(
        size=(nf * finger_pitch, 1.0),
        layer=LAYERS["Metal2"],
    )
    drain_bus_ref = c.add_ref(drain_bus)
    drain_bus_ref.move((-nf * finger_pitch / 2, gate_width / 2 + 1.0))

    # Gate bus (can be tied to source or left floating)
    gate_bus = gf.components.rectangle(
        size=(nf * finger_pitch, 0.5),
        layer=LAYERS["GatPoly"],
    )
    gate_bus_ref = c.add_ref(gate_bus)
    gate_bus_ref.move((-nf * finger_pitch / 2, -gate_width / 2 - gate_ext - 0.5))

    # ESD marker
    esd_mark = gf.components.rectangle(
        size=(nf * finger_pitch + 1.0, gate_width + 3.0),
        layer=LAYERS["ESD"],
        centered=True,
    )
    c.add_ref(esd_mark)

    # Add ports
    c.add_port(
        name="PAD",
        center=(0, gate_width / 2 + 1.5),
        width=nf * finger_pitch,
        orientation=90,
        layer=LAYERS["Metal2"],
        port_type="electrical",
    )

    c.add_port(
        name="GND",
        center=(0, -gate_width / 2),
        width=nf * finger_pitch,
        orientation=270,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    # Add metadata
    c.info["model"] = model
    c.info["width"] = width
    c.info["length"] = length
    c.info["nf"] = nf
    c.info["type"] = "esd_nmos"

    return c


@gf.cell
def ptap1(
    width: float = 1.0,
    length: float = 1.0,
    rows: int = 1,
    cols: int = 1,
) -> Component:
    """Create a P+ substrate tap.

    Args:
        width: Width of the tap in micrometers.
        length: Length of the tap in micrometers.
        rows: Number of contact rows.
        cols: Number of contact columns.

    Returns:
        Component with P+ tap layout.
    """
    c = Component()

    # Design rules
    cont_size = 0.16
    cont_spacing = 0.18
    metal_enc = 0.06
    tap_enc = 0.1

    # Grid snap
    grid = 0.005
    width = round(width / grid) * grid
    length = round(length / grid) * grid

    # P+ active region
    active = gf.components.rectangle(
        size=(length, width),
        layer=LAYERS["Activ"],
        centered=True,
    )
    c.add_ref(active)

    # P+ implant
    psd = gf.components.rectangle(
        size=(length + 2 * tap_enc, width + 2 * tap_enc),
        layer=LAYERS["pSD"],
        centered=True,
    )
    c.add_ref(psd)

    # P-tap marker
    ptap = gf.components.rectangle(
        size=(length, width),
        layer=LAYERS["Ptap"],
        centered=True,
    )
    c.add_ref(ptap)

    # Contact array
    cont_array_width = cont_size * cols + cont_spacing * (cols - 1)
    cont_array_height = cont_size * rows + cont_spacing * (rows - 1)

    for i in range(cols):
        for j in range(rows):
            x = -cont_array_width / 2 + cont_size / 2 + i * (cont_size + cont_spacing)
            y = -cont_array_height / 2 + cont_size / 2 + j * (cont_size + cont_spacing)

            cont = gf.components.rectangle(
                size=(cont_size, cont_size),
                layer=LAYERS["Cont"],
                centered=True,
            )
            cont_ref = c.add_ref(cont)
            cont_ref.move((x, y))

    # Metal1 connection
    metal = gf.components.rectangle(
        size=(cont_array_width + 2 * metal_enc, cont_array_height + 2 * metal_enc),
        layer=LAYERS["Metal1"],
        centered=True,
    )
    c.add_ref(metal)

    # Add port
    c.add_port(
        name="TAP",
        center=(0, 0),
        width=width,
        orientation=0,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    # Add metadata
    c.info["type"] = "ptap"
    c.info["width"] = width
    c.info["length"] = length
    c.info["rows"] = rows
    c.info["cols"] = cols

    return c


@gf.cell
def ntap1(
    width: float = 1.0,
    length: float = 1.0,
    rows: int = 1,
    cols: int = 1,
) -> Component:
    """Create an N+ substrate tap.

    Args:
        width: Width of the tap in micrometers.
        length: Length of the tap in micrometers.
        rows: Number of contact rows.
        cols: Number of contact columns.

    Returns:
        Component with N+ tap layout.
    """
    c = Component()

    # Design rules
    cont_size = 0.16
    cont_spacing = 0.18
    metal_enc = 0.06
    tap_enc = 0.1
    nwell_enc = 0.31

    # Grid snap
    grid = 0.005
    width = round(width / grid) * grid
    length = round(length / grid) * grid

    # N-Well
    nwell = gf.components.rectangle(
        size=(length + 2 * nwell_enc, width + 2 * nwell_enc),
        layer=LAYERS["NWell"],
        centered=True,
    )
    c.add_ref(nwell)

    # N+ active region
    active = gf.components.rectangle(
        size=(length, width),
        layer=LAYERS["Activ"],
        centered=True,
    )
    c.add_ref(active)

    # N+ implant
    nsd = gf.components.rectangle(
        size=(length + 2 * tap_enc, width + 2 * tap_enc),
        layer=LAYERS["nSD"],
        centered=True,
    )
    c.add_ref(nsd)

    # N-tap marker
    ntap = gf.components.rectangle(
        size=(length, width),
        layer=LAYERS["Ntap"],
        centered=True,
    )
    c.add_ref(ntap)

    # Contact array
    cont_array_width = cont_size * cols + cont_spacing * (cols - 1)
    cont_array_height = cont_size * rows + cont_spacing * (rows - 1)

    for i in range(cols):
        for j in range(rows):
            x = -cont_array_width / 2 + cont_size / 2 + i * (cont_size + cont_spacing)
            y = -cont_array_height / 2 + cont_size / 2 + j * (cont_size + cont_spacing)

            cont = gf.components.rectangle(
                size=(cont_size, cont_size),
                layer=LAYERS["Cont"],
                centered=True,
            )
            cont_ref = c.add_ref(cont)
            cont_ref.move((x, y))

    # Metal1 connection
    metal = gf.components.rectangle(
        size=(cont_array_width + 2 * metal_enc, cont_array_height + 2 * metal_enc),
        layer=LAYERS["Metal1"],
        centered=True,
    )
    c.add_ref(metal)

    # Add port
    c.add_port(
        name="TAP",
        center=(0, 0),
        width=width,
        orientation=0,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    # Add metadata
    c.info["type"] = "ntap"
    c.info["width"] = width
    c.info["length"] = length
    c.info["rows"] = rows
    c.info["cols"] = cols

    return c


@gf.cell
def sealring(
    width: float = 200.0,
    height: float = 200.0,
    ring_width: float = 5.0,
) -> Component:
    """Create a seal ring for die protection.

    Args:
        width: Inner width of the seal ring in micrometers.
        height: Inner height of the seal ring in micrometers.
        ring_width: Width of the seal ring metal in micrometers.

    Returns:
        Component with seal ring layout.
    """
    c = Component()

    # Create seal ring on all metal layers
    metal_layers = [
        LAYERS["Metal1"],
        LAYERS["Metal2"],
        LAYERS["Metal3"],
        LAYERS["Metal4"],
        LAYERS["Metal5"],
        LAYERS["TopMetal1"],
        LAYERS["TopMetal2"],
    ]

    # Create ring on each metal layer
    for metal_layer in metal_layers:
        # Outer rectangle
        outer = gf.components.rectangle(
            size=(width + 2 * ring_width, height + 2 * ring_width),
            layer=metal_layer,
            centered=True,
        )

        # Inner rectangle (to create ring)
        inner = gf.components.rectangle(
            size=(width, height),
            layer=metal_layer,
            centered=True,
        )

        # Create ring by boolean subtraction
        ring = gf.boolean(outer, inner, "A-B", layer=metal_layer)
        c.add_ref(ring)

    # Add vias between metal layers
    via_layers = [
        LAYERS["Via1"],
        LAYERS["Via2"],
        LAYERS["Via3"],
        LAYERS["Via4"],
        LAYERS["TopVia1"],
        LAYERS["TopVia2"],
    ]

    # Via arrays in the ring
    via_size = 0.26
    via_spacing = 0.36

    for via_layer in via_layers:
        # Calculate number of vias along each edge
        n_vias_x = int((width + ring_width - via_size) / via_spacing)
        n_vias_y = int((height + ring_width - via_size) / via_spacing)

        # Top edge vias
        for i in range(n_vias_x):
            x = -width / 2 - ring_width / 2 + via_size / 2 + i * via_spacing
            y = height / 2 + ring_width / 2

            via = gf.components.rectangle(
                size=(via_size, via_size),
                layer=via_layer,
                centered=True,
            )
            via_ref = c.add_ref(via)
            via_ref.move((x, y))

        # Bottom edge vias
        for i in range(n_vias_x):
            x = -width / 2 - ring_width / 2 + via_size / 2 + i * via_spacing
            y = -height / 2 - ring_width / 2

            via = gf.components.rectangle(
                size=(via_size, via_size),
                layer=via_layer,
                centered=True,
            )
            via_ref = c.add_ref(via)
            via_ref.move((x, y))

        # Left edge vias
        for i in range(n_vias_y):
            x = -width / 2 - ring_width / 2
            y = -height / 2 - ring_width / 2 + via_size / 2 + i * via_spacing

            via = gf.components.rectangle(
                size=(via_size, via_size),
                layer=via_layer,
                centered=True,
            )
            via_ref = c.add_ref(via)
            via_ref.move((x, y))

        # Right edge vias
        for i in range(n_vias_y):
            x = width / 2 + ring_width / 2
            y = -height / 2 - ring_width / 2 + via_size / 2 + i * via_spacing

            via = gf.components.rectangle(
                size=(via_size, via_size),
                layer=via_layer,
                centered=True,
            )
            via_ref = c.add_ref(via)
            via_ref.move((x, y))

    # Seal ring marker
    seal_mark = gf.components.rectangle(
        size=(width + 2 * ring_width + 1.0, height + 2 * ring_width + 1.0),
        layer=LAYERS["SealRing"],
        centered=True,
    )
    seal_inner = gf.components.rectangle(
        size=(width - 1.0, height - 1.0),
        layer=LAYERS["SealRing"],
        centered=True,
    )
    seal_ring_mark = gf.boolean(seal_mark, seal_inner, "A-B", layer=LAYERS["SealRing"])
    c.add_ref(seal_ring_mark)

    # Add metadata
    c.info["type"] = "sealring"
    c.info["width"] = width
    c.info["height"] = height
    c.info["ring_width"] = ring_width

    return c


if __name__ == "__main__":
    # Test the components
    c1 = svaricap(width=2.0, length=1.0, nf=4)
    c1.show()

    c2 = esd_nmos(width=100.0, length=0.5, nf=20)
    c2.show()

    c3 = ptap1(width=2.0, length=2.0, rows=2, cols=2)
    c3.show()

    c4 = sealring(width=500, height=500, ring_width=10)
    c4.show()
