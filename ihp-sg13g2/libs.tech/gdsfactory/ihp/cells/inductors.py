"""Inductor components for IHP PDK."""

import math
from typing import Optional

import gdsfactory as gf
from gdsfactory import Component
from gdsfactory.typings import Layer


def inductor_min_diameter(width: float, space: float, turns: int, grid: float) -> float:
    """Calculate minimum diameter for inductor.

    Args:
        width: Width of the inductor trace in micrometers.
        space: Space between turns in micrometers.
        turns: Number of turns.
        grid: Grid resolution.

    Returns:
        Minimum diameter in micrometers.
    """
    var = 1 + math.sqrt(2)
    min_d = 2 * turns * (width + space) + 4 * width
    return round(min_d / grid) * grid


@gf.cell
def inductor2(
    width: float = 2.0,
    space: float = 2.1,
    diameter: float = 15.48,
    resistance: float = 0.5777,
    inductance: float = 33.303e-12,
    turns: int = 1,
    block_qrc: bool = True,
    substrate_etch: bool = False,
) -> Component:
    """Create a 2-turn inductor.

    Args:
        width: Width of the inductor trace in micrometers.
        space: Space between turns in micrometers.
        diameter: Inner diameter in micrometers.
        resistance: Resistance in ohms.
        inductance: Inductance in henries.
        turns: Number of turns (default 1 for inductor2).
        block_qrc: Block QRC layer.
        substrate_etch: Enable substrate etching.

    Returns:
        Component with inductor layout.
    """
    c = Component()

    # Define layers
    TM2 = (134, 5)  # TopMetal2
    TM1 = (126, 5)  # TopMetal1
    TV2 = (125, 5)  # TopVia2
    IND = (8, 5)    # IND layer
    NoRCX = (15, 5) # NoRCX layer
    LBE = (24, 0)   # Substrate etch layer

    # Grid fixing for manufacturing constraints
    grid = 0.01
    w = round(width / (2 * grid)) * 2 * grid
    s = round(space / grid) * grid
    d = round(diameter / (2 * grid)) * 2 * grid

    # Check minimum diameter
    min_d = inductor_min_diameter(w, s, turns, grid)
    if d < min_d:
        d = min_d

    # Calculate geometry parameters
    var = 1 + math.sqrt(2)
    lat_sm = round(d / (2 * var * grid)) * 2 * grid
    lat_big = round((d + 2 * w) / (var * grid)) * grid
    cateta_sm = (d - lat_sm) / 2
    cateta_big = round((d + 2 * w) / (var * math.sqrt(2) * grid)) * grid

    # Create octagonal spiral inductor
    # Center opening
    octagon_points = []
    angle_step = 45
    for i in range(8):
        angle = i * angle_step * math.pi / 180
        if i % 2 == 0:  # Cardinal points
            r = d / 2
        else:  # Diagonal points
            r = d / (2 * math.cos(math.pi / 8))
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        octagon_points.append((x, y))

    # Create spiral turns
    for turn in range(turns):
        turn_offset = turn * (w + s)

        # Create path for this turn
        path_points = []
        for i in range(8):
            angle = (i * 45 + 22.5) * math.pi / 180  # Offset by 22.5 degrees
            if i % 2 == 0:
                r = d/2 + turn_offset + w/2
            else:
                r = (d/2 + turn_offset + w/2) / math.cos(math.pi/8)

            x = r * math.cos(angle)
            y = r * math.sin(angle)
            path_points.append((x, y))

        # Add opening for connection
        if turn == 0:
            # Create opening in first turn for connection
            path_points = path_points[:-1]  # Remove last point to create opening

        # Create the path
        path = gf.Path(path_points)
        inductor_path = c << gf.path.extrude(path, layer=TM2, width=w)

    # Add connection traces and ports
    # Port 1 - Inner connection
    port1_trace = c << gf.components.rectangle(
        size=(w, d/2 + w),
        layer=TM2
    )
    port1_trace.move((-(d/2 + w), -w/2))
    c.add_port(
        name="P1",
        center=(-(d/2 + w), .0),
        width=w,
        orientation=180,
        layer=TM2
    )

    # Port 2 - Outer connection
    outer_radius = d/2 + turns * (w + s)
    port2_trace = c << gf.components.rectangle(
        size=(w, outer_radius + w),
        layer=TM2
    )
    port2_trace.move((outer_radius, -w/2))
    c.add_port(
        name="P2",
        center=(outer_radius + w, 0),
        width=w,
        orientation=0,
        layer=TM2
    )

    # Add IND marker layer
    ind_box = c << gf.components.rectangle(
        size=(2 * outer_radius + 2 * w, 2 * outer_radius + 2 * w),
        layer=IND,
        centered=True
    )

    # Add blocking layers if requested
    if block_qrc:
        qrc_box = c << gf.components.rectangle(
            size=(2 * outer_radius + 3 * w, 2 * outer_radius + 3 * w),
            layer=NoRCX,
            centered=True
        )

    # Add substrate etch if requested
    if substrate_etch:
        etch_box = c << gf.components.rectangle(
            size=(2 * outer_radius + 4 * w, 2 * outer_radius + 4 * w),
            layer=LBE,
            centered=True
        )

    # Add metadata
    c.info["resistance"] = resistance
    c.info["inductance"] = inductance
    c.info["model"] = "inductor2"
    c.info["turns"] = turns
    c.info["width"] = width
    c.info["space"] = space
    c.info["diameter"] = diameter

    return c


@gf.cell
def inductor3(
    width: float = 2.0,
    space: float = 2.1,
    diameter: float = 24.68,
    resistance: float = 1.386,
    inductance: float = 221.5e-12,
    turns: int = 2,
    block_qrc: bool = True,
    substrate_etch: bool = False,
) -> Component:
    """Create a 3-turn inductor.

    Args:
        width: Width of the inductor trace in micrometers.
        space: Space between turns in micrometers.
        diameter: Inner diameter in micrometers.
        resistance: Resistance in ohms.
        inductance: Inductance in henries.
        turns: Number of turns (default 2 for inductor3).
        block_qrc: Block QRC layer.
        substrate_etch: Enable substrate etching.

    Returns:
        Component with inductor layout.
    """
    # Use inductor2 as base with different default parameters
    return inductor2(
        width=width,
        space=space,
        diameter=diameter,
        resistance=resistance,
        inductance=inductance,
        turns=turns,
        block_qrc=block_qrc,
        substrate_etch=substrate_etch,
    )


if __name__ == "__main__":
    # Test the components
    c1 = inductor2()
    c1.show()

    c2 = inductor3()
    c2.show()