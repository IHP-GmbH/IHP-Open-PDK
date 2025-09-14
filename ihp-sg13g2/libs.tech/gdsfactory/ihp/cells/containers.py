"""This module contains cells that contain other cells."""

from typing import Any

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import (
    CellSpec,
    ComponentSpec,
    CrossSectionSpec,
    Strs,
)


@gf.cell
def add_pads_top(
    component: ComponentSpec = "straight",
    port_names: Strs | None = None,
    component_name: str | None = None,
    cross_section: CrossSectionSpec = "metal_routing",
    pad_port_name: str = "e1",
    pad: ComponentSpec = "CuPillarPad",
    bend: ComponentSpec = "wire_corner",
    straight_separation: float = 15.0,
    pad_pitch: float = 100.0,
    taper: ComponentSpec | None = None,
    port_type: str = "electrical",
    allow_width_mismatch: bool = True,
    fanout_length: float | None = 80,
    route_width: float | list[float] | None = 0,
    **kwargs,
) -> Component:
    """Returns new component with ports connected top pads.

    Args:
        component: component spec to connect to.
        port_names: list of port names to connect to pads.
        component_name: optional for the label.
        cross_section: cross_section function.
        pad_port_name: pad port name.
        pad: pad function.
        bend: bend function.
        straight_separation: from edge to edge.
        pad_pitch: spacing between pads.
        taper: taper function.
        port_type: port type.
        allow_width_mismatch: if True, allows width mismatch.
        fanout_length: length of the fanout.
        route_width: width of the route.
        kwargs: additional arguments.

    .. plot::
        :include-source:

        import gdsfactory as gf
        c = gf.c.nxn(
            xsize=600,
            ysize=200,
            north=2,
            south=3,
            wg_width=10,
            layer="M3",
            port_type="electrical",
        )
        cc = gf.routing.add_pads_top(component=c, port_names=("e1", "e4"), fanout_length=50)
        cc.plot()

    """
    return gf.routing.add_pads_top(
        component=component,
        port_names=port_names,
        component_name=component_name,
        cross_section=cross_section,
        pad_port_name=pad_port_name,
        pad=pad,
        bend=bend,
        straight_separation=straight_separation,
        pad_pitch=pad_pitch,
        taper=taper,
        port_type=port_type,
        allow_width_mismatch=allow_width_mismatch,
        fanout_length=fanout_length,
        route_width=route_width,
        **kwargs,
    )


@gf.cell
def pack_doe(
    doe: ComponentSpec,
    settings: dict[str, tuple[Any, ...]],
    do_permutations: bool = False,
    function: CellSpec | None = None,
    **kwargs,
) -> Component:
    """Packs a component DOE (Design of Experiment) using pack.

    Args:
        doe: function to return Components.
        settings: component settings.
        do_permutations: for each setting.
        function: to apply (add padding, grating couplers).
        kwargs: for pack.

    Keyword Args:
        spacing: Minimum distance between adjacent shapes.
        aspect_ratio: (width, height) ratio of the rectangular bin.
        max_size: Limits the size into which the shapes will be packed.
        sort_by_area: Pre-sorts the shapes by area.
        density: Values closer to 1 pack tighter but require more computation.
        precision: Desired precision for rounding vertex coordinates.
        text: Optional function to add text labels.
        text_prefix: for labels. For example. 'A' for 'A1', 'A2'...
        text_offsets: relative to component size info anchor. Defaults to center.
        text_anchors: relative to component (ce cw nc ne nw sc se sw center cc).
        name_prefix: for each packed component (avoids the Unnamed cells warning).
            Note that the suffix contains a uuid so the name will not be deterministic.
        rotation: for each component in degrees.
        h_mirror: horizontal mirror in y axis (x, 1) (1, 0). This is the most common.
        v_mirror: vertical mirror using x axis (1, y) (0, y).
    """
    return gf.components.pack_doe(
        doe=doe,
        settings=settings,
        do_permutations=do_permutations,
        function=function,
        **kwargs,
    )


@gf.cell
def pack_doe_grid(
    doe: ComponentSpec,
    settings: dict[str, tuple[Any, ...]],
    do_permutations: bool = False,
    function: CellSpec | None = None,
    with_text: bool = False,
    **kwargs,
) -> Component:
    """Packs a component DOE (Design of Experiment) using grid.

    Args:
        doe: function to return Components.
        settings: component settings.
        do_permutations: for each setting.
        function: to apply to component (add padding, grating couplers).
        with_text: includes text label.
        kwargs: for grid.

    Keyword Args:
        spacing: between adjacent elements on the grid, can be a tuple for
            different distances in height and width.
        separation: If True, guarantees elements are separated with fixed spacing
            if False, elements are spaced evenly along a grid.
        shape: x, y shape of the grid (see np.reshape).
            If no shape and the list is 1D, if np.reshape were run with (1, -1).
        align_x: {'x', 'xmin', 'xmax'} for x (column) alignment along.
        align_y: {'y', 'ymin', 'ymax'} for y (row) alignment along.
        edge_x: {'x', 'xmin', 'xmax'} for x (column) (ignored if separation = True).
        edge_y: {'y', 'ymin', 'ymax'} for y (row) (ignored if separation = True).
        rotation: for each component in degrees.
        h_mirror: horizontal mirror y axis (x, 1) (1, 0). most common mirror.
        v_mirror: vertical mirror using x axis (1, y) (0, y).
    """
    return gf.components.pack_doe_grid(
        doe=doe,
        settings=settings,
        do_permutations=do_permutations,
        function=function,
        with_text=with_text,
        **kwargs,
    )


if __name__ == "__main__":
    from ihp import PDK

    PDK.activate()
    c = add_pads_top()
    c.show()
