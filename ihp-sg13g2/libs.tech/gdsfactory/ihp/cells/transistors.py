"""Transistor components for IHP PDK."""

import gdsfactory as gf
from gdsfactory import Component

# Define layers for transistors
LAYERS = {
    "NWell": (31, 0),
    "PWell": (29, 0),
    "ThickGateOx": (44, 0),
    "GatPoly": (5, 0),
    "Activ": (1, 0),
    "pSD": (14, 0),
    "nSD": (16, 0),
    "SiProtection": (2, 6),
    "Cont": (6, 0),
    "Metal1": (8, 0),
    "Metal2": (10, 0),
    "Via1": (19, 0),
    "Ptap": (13, 0),
    "Ntap": (26, 0),
    "TEXT": (63, 63),
}


@gf.cell
def nmos(
    width: float = 1.0,
    length: float = 0.13,
    nf: int = 1,
    m: int = 1,
    model: str = "sg13_lv_nmos",
) -> Component:
    """Create an NMOS transistor.

    Args:
        width: Total width of the transistor in micrometers.
        length: Gate length in micrometers.
        nf: Number of fingers.
        m: Multiplier (number of parallel devices).
        model: Device model name.

    Returns:
        Component with NMOS transistor layout.
    """
    c = Component()

    # Design rules
    gate_min_width = 0.15
    gate_min_length = 0.13
    cont_size = 0.16
    cont_spacing = 0.18
    cont_gate_spacing = 0.14
    cont_enc_active = 0.07
    cont_enc_metal = 0.06
    poly_extension = 0.18
    active_extension = 0.23
    psd_enclosure = 0.12

    # Calculate dimensions
    gate_width = max(width / nf, gate_min_width)
    gate_length = max(length, gate_min_length)

    # Grid snap
    grid = 0.005
    gate_width = round(gate_width / grid) * grid
    gate_length = round(gate_length / grid) * grid

    # Create transistor fingers
    finger_pitch = gate_width + 2 * cont_gate_spacing + cont_size

    for i in range(nf):
        x_offset = i * finger_pitch

        # Gate poly
        gate = gf.components.rectangle(
            size=(gate_length, gate_width + 2 * poly_extension),
            layer=LAYERS["GatPoly"],
        )
        gate_ref = c.add_ref(gate)
        gate_ref.movex(x_offset)

        # Active region
        active_width = gate_width
        active_length = gate_length + 2 * active_extension
        active = gf.components.rectangle(
            size=(active_length, active_width),
            layer=LAYERS["Activ"],
        )
        active_ref = c.add_ref(active)
        active_ref.move((x_offset - active_extension, poly_extension))

        # Source/Drain contacts
        # Calculate number of contacts
        n_cont_y = int((active_width - cont_size) / cont_spacing) + 1

        # Source contacts (left)
        for j in range(n_cont_y):
            y_pos = poly_extension + j * cont_spacing

            cont = gf.components.rectangle(
                size=(cont_size, cont_size),
                layer=LAYERS["Cont"],
            )
            cont_ref = c.add_ref(cont)
            cont_ref.move((x_offset - active_extension + cont_enc_active, y_pos))

            # Metal1 for source
            m1 = gf.components.rectangle(
                size=(cont_size + 2 * cont_enc_metal, cont_size + 2 * cont_enc_metal),
                layer=LAYERS["Metal1"],
            )
            m1_ref = c.add_ref(m1)
            m1_ref.move(
                (
                    x_offset - active_extension + cont_enc_active - cont_enc_metal,
                    y_pos - cont_enc_metal,
                )
            )

        # Drain contacts (right)
        for j in range(n_cont_y):
            y_pos = poly_extension + j * cont_spacing

            cont = gf.components.rectangle(
                size=(cont_size, cont_size),
                layer=LAYERS["Cont"],
            )
            cont_ref = c.add_ref(cont)
            cont_ref.move((x_offset + gate_length + cont_gate_spacing, y_pos))

            # Metal1 for drain
            m1 = gf.components.rectangle(
                size=(cont_size + 2 * cont_enc_metal, cont_size + 2 * cont_enc_metal),
                layer=LAYERS["Metal1"],
            )
            m1_ref = c.add_ref(m1)
            m1_ref.move(
                (
                    x_offset + gate_length + cont_gate_spacing - cont_enc_metal,
                    y_pos - cont_enc_metal,
                )
            )

    # N+ implant
    nsd = gf.components.rectangle(
        size=(nf * finger_pitch + active_extension, gate_width + 2 * psd_enclosure),
        layer=LAYERS["nSD"],
    )
    nsd_ref = c.add_ref(nsd)
    nsd_ref.move((-active_extension - psd_enclosure, poly_extension - psd_enclosure))

    # Add ports
    c.add_port(
        name="G",
        center=(nf * finger_pitch / 2, -poly_extension),
        width=gate_length,
        orientation=270,
        layer=LAYERS["GatPoly"],
        port_type="electrical",
    )

    c.add_port(
        name="S",
        center=(-active_extension, gate_width / 2 + poly_extension),
        width=gate_width,
        orientation=180,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    c.add_port(
        name="D",
        center=(gate_length + active_extension, gate_width / 2 + poly_extension),
        width=gate_width,
        orientation=0,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    # Add metadata
    c.info["model"] = model
    c.info["width"] = width
    c.info["length"] = length
    c.info["nf"] = nf
    c.info["m"] = m
    c.info["type"] = "nmos"

    return c


@gf.cell
def pmos(
    width: float = 1.0,
    length: float = 0.13,
    nf: int = 1,
    m: int = 1,
    model: str = "sg13_lv_pmos",
) -> Component:
    """Create a PMOS transistor.

    Args:
        width: Total width of the transistor in micrometers.
        length: Gate length in micrometers.
        nf: Number of fingers.
        m: Multiplier (number of parallel devices).
        model: Device model name.

    Returns:
        Component with PMOS transistor layout.
    """
    c = Component()

    # Design rules
    gate_min_width = 0.15
    gate_min_length = 0.13
    cont_size = 0.16
    cont_spacing = 0.18
    cont_gate_spacing = 0.14
    cont_enc_active = 0.07
    cont_enc_metal = 0.06
    poly_extension = 0.18
    active_extension = 0.23
    nwell_enclosure = 0.31
    psd_enclosure = 0.12

    # Calculate dimensions
    gate_width = max(width / nf, gate_min_width)
    gate_length = max(length, gate_min_length)

    # Grid snap
    grid = 0.005
    gate_width = round(gate_width / grid) * grid
    gate_length = round(gate_length / grid) * grid

    # N-Well
    nwell_width = gate_width + 2 * nwell_enclosure
    nwell_length = gate_length + 2 * active_extension + 2 * nwell_enclosure
    nwell = gf.components.rectangle(
        size=(nwell_length * nf, nwell_width),
        layer=LAYERS["NWell"],
    )
    nwell_ref = c.add_ref(nwell)
    nwell_ref.move(
        (-active_extension - nwell_enclosure, poly_extension - nwell_enclosure)
    )

    # Create transistor fingers
    finger_pitch = gate_width + 2 * cont_gate_spacing + cont_size

    for i in range(nf):
        x_offset = i * finger_pitch

        # Gate poly
        gate = gf.components.rectangle(
            size=(gate_length, gate_width + 2 * poly_extension),
            layer=LAYERS["GatPoly"],
        )
        gate_ref = c.add_ref(gate)
        gate_ref.movex(x_offset)

        # Active region
        active_width = gate_width
        active_length = gate_length + 2 * active_extension
        active = gf.components.rectangle(
            size=(active_length, active_width),
            layer=LAYERS["Activ"],
        )
        active_ref = c.add_ref(active)
        active_ref.move((x_offset - active_extension, poly_extension))

        # Source/Drain contacts
        n_cont_y = int((active_width - cont_size) / cont_spacing) + 1

        # Source contacts (left)
        for j in range(n_cont_y):
            y_pos = poly_extension + j * cont_spacing

            cont = gf.components.rectangle(
                size=(cont_size, cont_size),
                layer=LAYERS["Cont"],
            )
            cont_ref = c.add_ref(cont)
            cont_ref.move((x_offset - active_extension + cont_enc_active, y_pos))

            # Metal1 for source
            m1 = gf.components.rectangle(
                size=(cont_size + 2 * cont_enc_metal, cont_size + 2 * cont_enc_metal),
                layer=LAYERS["Metal1"],
            )
            m1_ref = c.add_ref(m1)
            m1_ref.move(
                (
                    x_offset - active_extension + cont_enc_active - cont_enc_metal,
                    y_pos - cont_enc_metal,
                )
            )

        # Drain contacts (right)
        for j in range(n_cont_y):
            y_pos = poly_extension + j * cont_spacing

            cont = gf.components.rectangle(
                size=(cont_size, cont_size),
                layer=LAYERS["Cont"],
            )
            cont_ref = c.add_ref(cont)
            cont_ref.move((x_offset + gate_length + cont_gate_spacing, y_pos))

            # Metal1 for drain
            m1 = gf.components.rectangle(
                size=(cont_size + 2 * cont_enc_metal, cont_size + 2 * cont_enc_metal),
                layer=LAYERS["Metal1"],
            )
            m1_ref = c.add_ref(m1)
            m1_ref.move(
                (
                    x_offset + gate_length + cont_gate_spacing - cont_enc_metal,
                    y_pos - cont_enc_metal,
                )
            )

    # P+ implant
    psd = gf.components.rectangle(
        size=(nf * finger_pitch + active_extension, gate_width + 2 * psd_enclosure),
        layer=LAYERS["pSD"],
    )
    psd_ref = c.add_ref(psd)
    psd_ref.move((-active_extension - psd_enclosure, poly_extension - psd_enclosure))

    # Add ports
    c.add_port(
        name="G",
        center=(nf * finger_pitch / 2, -poly_extension),
        width=gate_length,
        orientation=270,
        layer=LAYERS["GatPoly"],
        port_type="electrical",
    )

    c.add_port(
        name="S",
        center=(-active_extension, gate_width / 2 + poly_extension),
        width=gate_width,
        orientation=180,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    c.add_port(
        name="D",
        center=(gate_length + active_extension, gate_width / 2 + poly_extension),
        width=gate_width,
        orientation=0,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    # Add metadata
    c.info["model"] = model
    c.info["width"] = width
    c.info["length"] = length
    c.info["nf"] = nf
    c.info["m"] = m
    c.info["type"] = "pmos"

    return c


@gf.cell
def nmos_hv(
    width: float = 1.0,
    length: float = 0.45,
    nf: int = 1,
    m: int = 1,
    model: str = "sg13_hv_nmos",
) -> Component:
    """Create a high-voltage NMOS transistor.

    Args:
        width: Total width of the transistor in micrometers.
        length: Gate length in micrometers.
        nf: Number of fingers.
        m: Multiplier (number of parallel devices).
        model: Device model name.

    Returns:
        Component with HV NMOS transistor layout.
    """
    c = nmos(width=width, length=length, nf=nf, m=m, model=model)

    # Add thick gate oxide layer
    thick_ox = gf.components.rectangle(
        size=(length + 0.5, width + 0.5),
        layer=LAYERS["ThickGateOx"],
        centered=True,
    )
    c.add_ref(thick_ox)

    c.info["type"] = "nmos_hv"
    return c


@gf.cell
def pmos_hv(
    width: float = 1.0,
    length: float = 0.45,
    nf: int = 1,
    m: int = 1,
    model: str = "sg13_hv_pmos",
) -> Component:
    """Create a high-voltage PMOS transistor.

    Args:
        width: Total width of the transistor in micrometers.
        length: Gate length in micrometers.
        nf: Number of fingers.
        m: Multiplier (number of parallel devices).
        model: Device model name.

    Returns:
        Component with HV PMOS transistor layout.
    """
    c = pmos(width=width, length=length, nf=nf, m=m, model=model)

    # Add thick gate oxide layer
    thick_ox = gf.components.rectangle(
        size=(length + 0.5, width + 0.5),
        layer=LAYERS["ThickGateOx"],
        centered=True,
    )
    c.add_ref(thick_ox)

    c.info["type"] = "pmos_hv"
    return c


@gf.cell
def rfnmos(
    width: float = 2.0,
    length: float = 0.13,
    nf: int = 2,
    m: int = 1,
    model: str = "sg13_lv_rfnmos",
) -> Component:
    """Create an RF NMOS transistor with optimized layout.

    Args:
        width: Total width of the transistor in micrometers.
        length: Gate length in micrometers.
        nf: Number of fingers (should be even for RF).
        m: Multiplier (number of parallel devices).
        model: Device model name.

    Returns:
        Component with RF NMOS transistor layout.
    """
    # Ensure even number of fingers for RF layout
    if nf % 2 != 0:
        nf = nf + 1

    c = nmos(width=width, length=length, nf=nf, m=m, model=model)

    # Add substrate shielding for RF
    shield_layer = (37, 0)  # Example shield layer
    shield = gf.components.rectangle(
        size=(length * nf * 1.5, width * 1.2),
        layer=shield_layer,
        centered=True,
    )
    c.add_ref(shield)

    c.info["type"] = "rfnmos"
    return c


@gf.cell
def rfpmos(
    width: float = 2.0,
    length: float = 0.13,
    nf: int = 2,
    m: int = 1,
    model: str = "sg13_lv_rfpmos",
) -> Component:
    """Create an RF PMOS transistor with optimized layout.

    Args:
        width: Total width of the transistor in micrometers.
        length: Gate length in micrometers.
        nf: Number of fingers (should be even for RF).
        m: Multiplier (number of parallel devices).
        model: Device model name.

    Returns:
        Component with RF PMOS transistor layout.
    """
    # Ensure even number of fingers for RF layout
    if nf % 2 != 0:
        nf = nf + 1

    c = pmos(width=width, length=length, nf=nf, m=m, model=model)

    # Add substrate shielding for RF
    shield_layer = (37, 0)  # Example shield layer
    shield = gf.components.rectangle(
        size=(length * nf * 1.5, width * 1.2),
        layer=shield_layer,
        centered=True,
    )
    c.add_ref(shield)

    c.info["type"] = "rfpmos"
    return c


if __name__ == "__main__":
    # Test the components
    c1 = nmos(width=2.0, length=0.13, nf=4)
    c1.show()

    c2 = pmos(width=3.0, length=0.13, nf=2)
    c2.show()

    c3 = rfnmos(width=5.0, length=0.13, nf=8)
    c3.show()
