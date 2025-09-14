"""Bipolar transistor components for IHP PDK."""

from typing import Literal, Optional

import gdsfactory as gf
from gdsfactory import Component


# Define layers for bipolar transistors
LAYERS = {
    "NWell": (31, 0),
    "PWell": (29, 0),
    "PWellBlock": (28, 0),
    "DeepNWell": (30, 0),
    "DeepPWell": (31, 1),
    "Activ": (1, 0),
    "ActiveDummy": (1, 22),
    "pSD": (14, 0),
    "nSD": (16, 0),
    "nBuLay": (32, 0),
    "pBuLay": (33, 0),
    "SiProtection": (2, 6),
    "Cont": (6, 0),
    "Metal1": (8, 0),
    "Metal2": (10, 0),
    "Via1": (19, 0),
    "NPN": (82, 0),
    "PNP": (83, 0),
    "TRANS": (84, 0),
    "TEXT": (63, 63),
}


@gf.cell
def npn13G2(
    emitter_width: float = 0.07,
    emitter_length: float = 0.9,
    model: str = "npn13G2",
    m: int = 1,
) -> Component:
    """Create an NPN13G2 bipolar transistor.

    Args:
        emitter_width: Emitter width in micrometers.
        emitter_length: Emitter length in micrometers.
        model: Device model name.
        m: Multiplier (number of parallel devices).

    Returns:
        Component with NPN bipolar transistor layout.
    """
    c = Component()

    # Design rules
    emitter_min_width = 0.07
    emitter_min_length = 0.84
    base_enclosure = 0.1
    collector_enclosure = 0.6
    cont_size = 0.16
    cont_spacing = 0.18
    cont_enc_active = 0.07
    cont_enc_metal = 0.06
    nwell_enclosure = 0.31

    # Validate and adjust dimensions
    em_width = max(emitter_width, emitter_min_width)
    em_length = max(emitter_length, emitter_min_length)

    # Grid snap
    grid = 0.005
    em_width = round(em_width / grid) * grid
    em_length = round(em_length / grid) * grid

    # Calculate component dimensions
    base_width = em_width + 2 * base_enclosure
    base_length = em_length + 2 * base_enclosure
    collector_width = base_width + 2 * collector_enclosure
    collector_length = base_length + 2 * collector_enclosure

    # Collector N-Well (outermost)
    nwell = gf.components.rectangle(
        size=(collector_length + 2 * nwell_enclosure, collector_width + 2 * nwell_enclosure),
        layer=LAYERS["NWell"],
        centered=True,
    )
    c.add_ref(nwell)

    # Deep N-Well for collector
    deep_nwell = gf.components.rectangle(
        size=(collector_length, collector_width),
        layer=LAYERS["DeepNWell"],
        centered=True,
    )
    c.add_ref(deep_nwell)

    # Collector active region (N+ ring)
    collector_ring_outer = gf.components.rectangle(
        size=(collector_length, collector_width),
        layer=LAYERS["Activ"],
        centered=True,
    )
    collector_ring_inner = gf.components.rectangle(
        size=(base_length, base_width),
        layer=LAYERS["Activ"],
        centered=True,
    )
    collector = gf.boolean(collector_ring_outer, collector_ring_inner, "A-B", layer=LAYERS["Activ"])
    c.add_ref(collector)

    # N+ implant for collector
    nsd_collector = gf.boolean(
        collector_ring_outer, collector_ring_inner, "A-B",
        layer=LAYERS["nSD"]
    )
    c.add_ref(nsd_collector)

    # Base P-Well
    pwell = gf.components.rectangle(
        size=(base_length, base_width),
        layer=LAYERS["PWell"],
        centered=True,
    )
    c.add_ref(pwell)

    # Base active region (P+ ring)
    base_ring_outer = gf.components.rectangle(
        size=(base_length, base_width),
        layer=LAYERS["Activ"],
        centered=True,
    )
    base_ring_inner = gf.components.rectangle(
        size=(em_length, em_width),
        layer=LAYERS["Activ"],
        centered=True,
    )
    base = gf.boolean(base_ring_outer, base_ring_inner, "A-B", layer=LAYERS["Activ"])
    c.add_ref(base)

    # P+ implant for base
    psd_base = gf.boolean(
        base_ring_outer, base_ring_inner, "A-B",
        layer=LAYERS["pSD"]
    )
    c.add_ref(psd_base)

    # Emitter active region (N+)
    emitter = gf.components.rectangle(
        size=(em_length, em_width),
        layer=LAYERS["Activ"],
        centered=True,
    )
    c.add_ref(emitter)

    # N+ implant for emitter
    nsd_emitter = gf.components.rectangle(
        size=(em_length, em_width),
        layer=LAYERS["nSD"],
        centered=True,
    )
    c.add_ref(nsd_emitter)

    # Add contacts for emitter
    n_cont_x = int((em_length - cont_size) / cont_spacing) + 1
    n_cont_y = int((em_width - cont_size) / cont_spacing) + 1

    for i in range(n_cont_x):
        for j in range(n_cont_y):
            x = -em_length/2 + cont_enc_active + i * cont_spacing
            y = -em_width/2 + cont_enc_active + j * cont_spacing

            cont = gf.components.rectangle(
                size=(cont_size, cont_size),
                layer=LAYERS["Cont"],
            )
            cont_ref = c.add_ref(cont)
            cont_ref.move((x, y))

    # Emitter metal
    emitter_metal = gf.components.rectangle(
        size=(em_length - 2 * cont_enc_active + 2 * cont_enc_metal,
               em_width - 2 * cont_enc_active + 2 * cont_enc_metal),
        layer=LAYERS["Metal1"],
        centered=True,
    )
    c.add_ref(emitter_metal)

    # Add base contacts (ring around emitter)
    base_cont_y = base_width / 2 - base_enclosure / 2
    for i in range(4):  # Simplified: 4 contacts on each side
        angle = i * 90
        if i % 2 == 0:  # Top and bottom
            x = 0
            y = base_cont_y if i == 0 else -base_cont_y
        else:  # Left and right
            x = base_cont_y if i == 1 else -base_cont_y
            y = 0

        cont = gf.components.rectangle(
            size=(cont_size, cont_size),
            layer=LAYERS["Cont"],
            centered=True,
        )
        cont_ref = c.add_ref(cont)
        cont_ref.move((x, y))

        # Base metal contact
        m1 = gf.components.rectangle(
            size=(cont_size + 2 * cont_enc_metal, cont_size + 2 * cont_enc_metal),
            layer=LAYERS["Metal1"],
            centered=True,
        )
        m1_ref = c.add_ref(m1)
        m1_ref.move((x, y))

    # Add collector contacts (outer ring)
    coll_cont_y = collector_width / 2 - collector_enclosure / 2
    for i in range(4):  # Simplified: 4 contacts on each side
        angle = i * 90
        if i % 2 == 0:  # Top and bottom
            x = 0
            y = coll_cont_y if i == 0 else -coll_cont_y
        else:  # Left and right
            x = coll_cont_y if i == 1 else -coll_cont_y
            y = 0

        cont = gf.components.rectangle(
            size=(cont_size, cont_size),
            layer=LAYERS["Cont"],
            centered=True,
        )
        cont_ref = c.add_ref(cont)
        cont_ref.move((x, y))

        # Collector metal contact
        m1 = gf.components.rectangle(
            size=(cont_size + 2 * cont_enc_metal, cont_size + 2 * cont_enc_metal),
            layer=LAYERS["Metal1"],
            centered=True,
        )
        m1_ref = c.add_ref(m1)
        m1_ref.move((x, y))

    # NPN marker layer
    npn_marker = gf.components.rectangle(
        size=(collector_length, collector_width),
        layer=LAYERS["NPN"],
        centered=True,
    )
    c.add_ref(npn_marker)

    # Add ports
    c.add_port(
        name="E",
        center=(0, 0),
        width=em_width,
        orientation=0,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    c.add_port(
        name="B",
        center=(0, base_width/2),
        width=cont_size,
        orientation=90,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    c.add_port(
        name="C",
        center=(collector_length/2, 0),
        width=cont_size,
        orientation=0,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    # Add metadata
    c.info["model"] = model
    c.info["emitter_width"] = emitter_width
    c.info["emitter_length"] = emitter_length
    c.info["m"] = m
    c.info["type"] = "npn"

    return c


@gf.cell
def npn13G2L(
    emitter_width: float = 0.07,
    emitter_length: float = 1.26,
    model: str = "npn13G2L",
    m: int = 1,
) -> Component:
    """Create an NPN13G2L (low-current) bipolar transistor.

    Args:
        emitter_width: Emitter width in micrometers.
        emitter_length: Emitter length in micrometers.
        model: Device model name.
        m: Multiplier (number of parallel devices).

    Returns:
        Component with NPN bipolar transistor layout.
    """
    return npn13G2(
        emitter_width=emitter_width,
        emitter_length=emitter_length,
        model=model,
        m=m,
    )


@gf.cell
def npn13G2V(
    emitter_width: float = 0.12,
    emitter_length: float = 0.9,
    model: str = "npn13G2V",
    m: int = 1,
) -> Component:
    """Create an NPN13G2V (varactor) bipolar transistor.

    Args:
        emitter_width: Emitter width in micrometers.
        emitter_length: Emitter length in micrometers.
        model: Device model name.
        m: Multiplier (number of parallel devices).

    Returns:
        Component with NPN bipolar transistor layout.
    """
    return npn13G2(
        emitter_width=emitter_width,
        emitter_length=emitter_length,
        model=model,
        m=m,
    )


@gf.cell
def pnpMPA(
    emitter_width: float = 0.4,
    emitter_length: float = 0.4,
    model: str = "pnpMPA",
    m: int = 1,
) -> Component:
    """Create a PNP MPA bipolar transistor.

    Args:
        emitter_width: Emitter width in micrometers.
        emitter_length: Emitter length in micrometers.
        model: Device model name.
        m: Multiplier (number of parallel devices).

    Returns:
        Component with PNP bipolar transistor layout.
    """
    c = Component()

    # Design rules
    emitter_min_size = 0.4
    base_enclosure = 0.15
    collector_enclosure = 0.8
    cont_size = 0.16
    cont_spacing = 0.18
    cont_enc_active = 0.07
    cont_enc_metal = 0.06
    pwell_enclosure = 0.31

    # Validate and adjust dimensions
    em_width = max(emitter_width, emitter_min_size)
    em_length = max(emitter_length, emitter_min_size)

    # Grid snap
    grid = 0.005
    em_width = round(em_width / grid) * grid
    em_length = round(em_length / grid) * grid

    # Calculate component dimensions
    base_width = em_width + 2 * base_enclosure
    base_length = em_length + 2 * base_enclosure
    collector_width = base_width + 2 * collector_enclosure
    collector_length = base_length + 2 * collector_enclosure

    # Collector P-Well (outermost)
    pwell = gf.components.rectangle(
        size=(collector_length + 2 * pwell_enclosure, collector_width + 2 * pwell_enclosure),
        layer=LAYERS["PWell"],
        centered=True,
    )
    c.add_ref(pwell)

    # Deep P-Well for collector
    deep_pwell = gf.components.rectangle(
        size=(collector_length, collector_width),
        layer=LAYERS["DeepPWell"],
        centered=True,
    )
    c.add_ref(deep_pwell)

    # Collector active region (P+ ring)
    collector_ring_outer = gf.components.rectangle(
        size=(collector_length, collector_width),
        layer=LAYERS["Activ"],
        centered=True,
    )
    collector_ring_inner = gf.components.rectangle(
        size=(base_length, base_width),
        layer=LAYERS["Activ"],
        centered=True,
    )
    collector = gf.boolean(collector_ring_outer, collector_ring_inner, "A-B", layer=LAYERS["Activ"])
    c.add_ref(collector)

    # P+ implant for collector
    psd_collector = gf.boolean(
        collector_ring_outer, collector_ring_inner, "A-B",
        layer=LAYERS["pSD"]
    )
    c.add_ref(psd_collector)

    # Base N-Well
    nwell = gf.components.rectangle(
        size=(base_length, base_width),
        layer=LAYERS["NWell"],
        centered=True,
    )
    c.add_ref(nwell)

    # Base active region (N+ ring)
    base_ring_outer = gf.components.rectangle(
        size=(base_length, base_width),
        layer=LAYERS["Activ"],
        centered=True,
    )
    base_ring_inner = gf.components.rectangle(
        size=(em_length, em_width),
        layer=LAYERS["Activ"],
        centered=True,
    )
    base = gf.boolean(base_ring_outer, base_ring_inner, "A-B", layer=LAYERS["Activ"])
    c.add_ref(base)

    # N+ implant for base
    nsd_base = gf.boolean(
        base_ring_outer, base_ring_inner, "A-B",
        layer=LAYERS["nSD"]
    )
    c.add_ref(nsd_base)

    # Emitter active region (P+)
    emitter = gf.components.rectangle(
        size=(em_length, em_width),
        layer=LAYERS["Activ"],
        centered=True,
    )
    c.add_ref(emitter)

    # P+ implant for emitter
    psd_emitter = gf.components.rectangle(
        size=(em_length, em_width),
        layer=LAYERS["pSD"],
        centered=True,
    )
    c.add_ref(psd_emitter)

    # Add contacts for emitter
    n_cont_x = int((em_length - cont_size) / cont_spacing) + 1
    n_cont_y = int((em_width - cont_size) / cont_spacing) + 1

    for i in range(n_cont_x):
        for j in range(n_cont_y):
            x = -em_length/2 + cont_enc_active + i * cont_spacing
            y = -em_width/2 + cont_enc_active + j * cont_spacing

            cont = gf.components.rectangle(
                size=(cont_size, cont_size),
                layer=LAYERS["Cont"],
            )
            cont_ref = c.add_ref(cont)
            cont_ref.move((x, y))

    # Emitter metal
    emitter_metal = gf.components.rectangle(
        size=(em_length - 2 * cont_enc_active + 2 * cont_enc_metal,
               em_width - 2 * cont_enc_active + 2 * cont_enc_metal),
        layer=LAYERS["Metal1"],
        centered=True,
    )
    c.add_ref(emitter_metal)

    # PNP marker layer
    pnp_marker = gf.components.rectangle(
        size=(collector_length, collector_width),
        layer=LAYERS["PNP"],
        centered=True,
    )
    c.add_ref(pnp_marker)

    # Add ports
    c.add_port(
        name="E",
        center=(0, 0),
        width=em_width,
        orientation=0,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    c.add_port(
        name="B",
        center=(0, base_width/2),
        width=cont_size,
        orientation=90,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    c.add_port(
        name="C",
        center=(collector_length/2, 0),
        width=cont_size,
        orientation=0,
        layer=LAYERS["Metal1"],
        port_type="electrical",
    )

    # Add metadata
    c.info["model"] = model
    c.info["emitter_width"] = emitter_width
    c.info["emitter_length"] = emitter_length
    c.info["m"] = m
    c.info["type"] = "pnp"

    return c


if __name__ == "__main__":
    # Test the components
    c1 = npn13G2(emitter_width=0.07, emitter_length=0.9)
    c1.show()

    c2 = pnpMPA(emitter_width=0.4, emitter_length=0.4)
    c2.show()