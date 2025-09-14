"""Bondpad components for IHP PDK."""

import math
from typing import Literal

import gdsfactory as gf
from gdsfactory import Component


@gf.cell
def bondpad(
    shape: Literal["octagon", "square", "circle"] = "octagon",
    stack_metals: bool = True,
    fill_metals: bool = False,
    flip_chip: bool = False,
    diameter: float = 68.0,
    top_metal: str = "TopMetal2",
    bottom_metal: str = "Metal1",
) -> Component:
    """Create a bondpad for wire bonding or flip-chip connection.

    Args:
        shape: Shape of the bondpad ("octagon", "square", or "circle").
        stack_metals: Stack all metal layers from bottom to top.
        fill_metals: Add metal fill patterns.
        flip_chip: Enable flip-chip configuration.
        diameter: Diameter or size of the bondpad in micrometers.
        top_metal: Top metal layer name.
        bottom_metal: Bottom metal layer name.

    Returns:
        Component with bondpad layout.
    """
    c = Component()

    # Define metal layers
    layers = {
        "Metal1": (8, 0),
        "Metal2": (10, 0),
        "Metal3": (30, 0),
        "Metal4": (50, 0),
        "Metal5": (67, 0),
        "TopMetal1": (126, 5),
        "TopMetal2": (134, 5),
    }

    # Define via layers
    via_layers = {
        "Via1": (19, 0),
        "Via2": (29, 0),
        "Via3": (49, 0),
        "Via4": (66, 0),
        "Via5": (125, 5),
    }

    # Passivation and other layers
    passivation_open = (33, 0)

    # Grid alignment
    grid = 0.01
    d = round(diameter / grid) * grid

    # Create the main pad shape
    if shape == "square":
        # Square bondpad
        pad = gf.components.rectangle(
            size=(d, d),
            layer=layers[top_metal],
            centered=True,
        )
        c.add_ref(pad)

    elif shape == "octagon":
        # Octagonal bondpad
        # Calculate octagon vertices
        side_length = d / (1 + math.sqrt(2))
        half_side = side_length / 2

        vertices = [
            (half_side, d / 2),
            (d / 2 - half_side, d / 2),
            (d / 2, d / 2 - half_side),
            (d / 2, -d / 2 + half_side),
            (d / 2 - half_side, -d / 2),
            (-d / 2 + half_side, -d / 2),
            (-d / 2, -d / 2 + half_side),
            (-d / 2, d / 2 - half_side),
        ]

        pad = gf.Component()
        pad.add_polygon(vertices, layer=layers[top_metal])
        c.add_ref(pad)

    elif shape == "circle":
        # Circular bondpad (approximated with polygon)
        pad = gf.components.circle(
            radius=d / 2,
            layer=layers[top_metal],
        )
        c.add_ref(pad)

    else:
        raise ValueError(f"Unknown shape: {shape}")

    # Stack metal layers if requested
    if stack_metals:
        # Create stack from bottom_metal to top_metal
        metal_stack = [
            "Metal1",
            "Metal2",
            "Metal3",
            "Metal4",
            "Metal5",
            "TopMetal1",
            "TopMetal2",
        ]

        # Find indices for start and end
        start_idx = metal_stack.index(bottom_metal)
        end_idx = metal_stack.index(top_metal)

        # Add metal layers
        for i in range(start_idx, end_idx):
            metal_name = metal_stack[i]
            metal_layer = layers[metal_name]

            if shape == "square":
                metal = gf.components.rectangle(
                    size=(d * 0.95, d * 0.95),  # Slightly smaller for via clearance
                    layer=metal_layer,
                    centered=True,
                )
                c.add_ref(metal)

            elif shape == "octagon":
                # Scale down octagon for lower metals
                scale = 0.95
                scaled_vertices = [(x * scale, y * scale) for x, y in vertices]
                metal = gf.Component()
                metal.add_polygon(scaled_vertices, layer=metal_layer)
                c.add_ref(metal)

            elif shape == "circle":
                metal = gf.components.circle(
                    radius=d / 2 * 0.95,
                    layer=metal_layer,
                )
                c.add_ref(metal)

        # Add vias between metal layers
        via_mapping = {
            ("Metal1", "Metal2"): "Via1",
            ("Metal2", "Metal3"): "Via2",
            ("Metal3", "Metal4"): "Via3",
            ("Metal4", "Metal5"): "Via4",
            ("Metal5", "TopMetal1"): "Via5",
            ("TopMetal1", "TopMetal2"): "TopVia2",
        }

        # Via parameters
        via_size = 0.26
        via_spacing = 0.36
        via_enclosure = 0.06

        # Calculate via array dimensions
        n_vias_x = int((d - 2 * via_enclosure) / via_spacing)
        n_vias_y = int((d - 2 * via_enclosure) / via_spacing)

        # Add via arrays between consecutive metal layers
        for i in range(start_idx, end_idx):
            if i < len(metal_stack) - 1:
                metal1 = metal_stack[i]
                metal2 = metal_stack[i + 1]
                via_key = (metal1, metal2)

                if via_key in via_mapping:
                    via_name = via_mapping[via_key]
                    if via_name in via_layers:
                        via_layer = via_layers[via_name]
                    elif via_name == "TopVia2":
                        via_layer = (125, 5)
                    else:
                        continue

                    # Create via array
                    for ix in range(n_vias_x):
                        for iy in range(n_vias_y):
                            x = -d / 2 + via_enclosure + via_size / 2 + ix * via_spacing
                            y = -d / 2 + via_enclosure + via_size / 2 + iy * via_spacing

                            # Check if via is within the pad shape
                            if shape == "circle":
                                if math.sqrt(x**2 + y**2) > d / 2 * 0.9:
                                    continue

                            via = gf.components.rectangle(
                                size=(via_size, via_size),
                                layer=via_layer,
                                centered=True,
                            )
                            via_ref = c.add_ref(via)
                            via_ref.move((x, y))

    # Add passivation opening
    if shape == "square":
        opening = gf.components.rectangle(
            size=(d * 0.85, d * 0.85),
            layer=passivation_open,
            centered=True,
        )
        c.add_ref(opening)
    elif shape == "octagon":
        scale = 0.85
        opening_vertices = [(x * scale, y * scale) for x, y in vertices]
        opening = gf.Component()
        opening.add_polygon(opening_vertices, layer=passivation_open)
        c.add_ref(opening)
    elif shape == "circle":
        opening = gf.components.circle(
            radius=d / 2 * 0.85,
            layer=passivation_open,
        )
        c.add_ref(opening)

    # Add flip-chip bumps if requested
    if flip_chip:
        # Add under-bump metallization (UBM)
        ubm_layer = (155, 0)  # Example UBM layer
        if shape == "circle":
            ubm = gf.components.circle(
                radius=d / 2 * 0.7,
                layer=ubm_layer,
            )
            c.add_ref(ubm)
        else:
            ubm = gf.components.rectangle(
                size=(d * 0.7, d * 0.7),
                layer=ubm_layer,
                centered=True,
            )
            c.add_ref(ubm)

    # Add port at the center
    c.add_port(
        name="pad",
        center=(0, 0),
        width=d,
        orientation=0,
        layer=layers[top_metal],
        port_type="electrical",
    )

    # Add metadata
    c.info["shape"] = shape
    c.info["diameter"] = diameter
    c.info["stack_metals"] = stack_metals
    c.info["flip_chip"] = flip_chip
    c.info["top_metal"] = top_metal
    c.info["bottom_metal"] = bottom_metal

    return c


@gf.cell
def bondpad_array(
    n_pads: int = 4,
    pad_pitch: float = 100.0,
    pad_diameter: float = 68.0,
    shape: Literal["octagon", "square", "circle"] = "octagon",
    stack_metals: bool = True,
) -> Component:
    """Create an array of bondpads.

    Args:
        n_pads: Number of bondpads.
        pad_pitch: Pitch between bondpad centers in micrometers.
        pad_diameter: Diameter of each bondpad in micrometers.
        shape: Shape of the bondpads.
        stack_metals: Stack all metal layers.

    Returns:
        Component with bondpad array.
    """
    c = Component()

    for i in range(n_pads):
        pad = bondpad(
            shape=shape,
            stack_metals=stack_metals,
            diameter=pad_diameter,
        )
        pad_ref = c.add_ref(pad)
        pad_ref.movex(i * pad_pitch)

        # Add port for each pad
        c.add_port(
            name=f"pad_{i + 1}",
            center=(i * pad_pitch, 0),
            width=pad_diameter,
            orientation=0,
            layer=pad.ports["pad"].layer,
            port_type="electrical",
        )

    c.info["n_pads"] = n_pads
    c.info["pad_pitch"] = pad_pitch
    c.info["pad_diameter"] = pad_diameter

    return c


if __name__ == "__main__":
    # Test the components
    c1 = bondpad(shape="octagon")
    c1.show()

    c2 = bondpad(shape="square", flip_chip=True)
    c2.show()

    c3 = bondpad_array(n_pads=6)
    c3.show()
