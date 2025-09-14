"""IHP PDK Technology definitions.

- LayerMap with IHP PDK layers
- LayerStack for 3D representation
- Cross-sections for routing
- Technology parameters
"""

import sys
from functools import partial

import gdsfactory as gf
from doroutes.bundles import add_bundle_astar
from gdsfactory.add_pins import add_pin_path
from gdsfactory.component import Component
from gdsfactory.cross_section import get_cross_sections
from gdsfactory.technology import LayerLevel, LayerMap, LayerStack
from gdsfactory.typings import Callable, Layer, LayerSpec
from pydantic import BaseModel

from ihp.config import PATH

nm = 1e-3
pin_length = 10 * nm
heater_width = 4


class LayerMapIHP(LayerMap):
    """IHP PDK Layer Map based on SG13G2 technology."""

    # Substrate and Wells
    SUBSTRATE: Layer = (40, 0)
    NWELL: Layer = (31, 0)
    PWELL: Layer = (29, 0)

    # Active and Poly
    ACTIV: Layer = (1, 0)
    GATPOLY: Layer = (5, 0)
    POLYRES: Layer = (128, 0)  # Poly resistor marker

    # Implants
    PSD: Layer = (14, 0)  # P+ implant
    NSD: Layer = (16, 0)  # N+ implant
    NBULAY: Layer = (32, 0)  # N-buried layer
    SALBLOCK: Layer = (28, 0)  # Salicide block

    # Gate oxide
    THICKGATEOX: Layer = (44, 0)  # Thick gate oxide for HV devices

    # Contacts and Vias
    CONT: Layer = (6, 0)
    VIA1: Layer = (19, 0)
    VIA2: Layer = (29, 0)
    VIA3: Layer = (49, 0)
    VIA4: Layer = (66, 0)
    TOPVIA1: Layer = (125, 5)
    TOPVIA2: Layer = (133, 5)

    # Metal layers
    METAL1: Layer = (8, 0)
    METAL2: Layer = (10, 0)
    METAL3: Layer = (30, 0)
    METAL4: Layer = (50, 0)
    METAL5: Layer = (67, 0)
    TOPMETAL1: Layer = (126, 5)
    TOPMETAL2: Layer = (134, 5)

    # MIM Capacitor
    MIM: Layer = (36, 0)
    VMIM: Layer = (129, 0)  # Via for MIM

    # Special layers for markers and devices
    NPN: Layer = (82, 0)  # NPN marker
    PNP: Layer = (83, 0)  # PNP marker
    TRANS: Layer = (84, 0)  # Transistor marker
    VARICAP: Layer = (87, 0)  # Varicap marker
    ESD: Layer = (88, 0)  # ESD marker

    # Resistor markers
    RSIL: Layer = (6, 10)  # Silicide resistor marker
    RPPD: Layer = (31, 10)  # P+ poly resistor marker
    RHIGH: Layer = (85, 0)  # High resistance marker

    # Tap markers
    PTAP: Layer = (13, 0)  # P-tap marker
    NTAP: Layer = (26, 0)  # N-tap marker

    # Inductor and RF
    IND: Layer = (8, 5)  # Inductor marker
    RFPAD: Layer = (81, 0)  # RF pad marker

    # Passivation and protection
    PASSIV: Layer = (6, 0)  # Passivation
    PASSIV_OPEN: Layer = (33, 0)  # Passivation opening
    SIPROTECTION: Layer = (2, 6)  # Silicon protection

    # Seal ring and die protection
    SEALRING: Layer = (167, 5)  # Seal ring marker

    # Substrate etch
    LBE: Layer = (24, 0)  # Local back etch (substrate etch)

    # Filler and fill exclusion layers
    METAL1_FILLER: Layer = (8, 22)
    METAL1_NOFILL: Layer = (8, 23)
    METAL2_FILLER: Layer = (10, 22)
    METAL2_NOFILL: Layer = (10, 23)
    METAL3_FILLER: Layer = (30, 22)
    METAL3_NOFILL: Layer = (30, 23)
    METAL4_FILLER: Layer = (50, 22)
    METAL4_NOFILL: Layer = (50, 23)
    ACTIV_FILLER: Layer = (1, 22)
    ACTIV_NOFILL: Layer = (1, 23)
    GATPOLY_FILLER: Layer = (5, 22)
    GATPOLY_NOFILL: Layer = (5, 23)

    # QRC and extraction control
    NOQRC: Layer = (15, 5)  # No QRC extraction
    METAL1_NOQRC: Layer = (8, 28)
    METAL2_NOQRC: Layer = (10, 28)
    METAL3_NOQRC: Layer = (30, 28)
    METAL4_NOQRC: Layer = (50, 28)
    GATPOLY_NOQRC: Layer = (5, 28)
    ACTIV_NOQRC: Layer = (1, 28)

    # Text and labels
    TEXT: Layer = (63, 63)
    METAL1_TEXT: Layer = (8, 25)
    METAL2_TEXT: Layer = (10, 25)
    METAL3_TEXT: Layer = (30, 25)
    METAL4_TEXT: Layer = (50, 25)


    # Device recognition and boundary
    DEVREC: Layer = (68, 0)
    FLOORPLAN: Layer = (99, 0)
    SHOW_PORTS: Layer = (1, 13)

    # Probe layers
    METAL1_IPROBE: Layer = (8, 33)
    METAL1_DIFFPRB: Layer = (8, 34)
    METAL2_IPROBE: Layer = (10, 33)
    METAL2_DIFFPRB: Layer = (10, 34)
    METAL3_IPROBE: Layer = (30, 33)
    METAL3_DIFFPRB: Layer = (30, 34)
    METAL4_IPROBE: Layer = (50, 33)
    METAL4_DIFFPRB: Layer = (50, 34)

    # Legacy compatibility layers
    WAFER: Layer = (40, 0)  # Same as SUBSTRATE


LAYER = LayerMapIHP


def add_labels_to_ports_optical(
    component: Component,
    label_layer: LayerSpec = LAYER.TEXT,
    port_type: str | None = "optical",
    **kwargs,
) -> Component:
    """Add labels to component ports.

    Args:
        component: to add labels.
        label_layer: layer spec for the label.
        port_type: to select ports.

    keyword Args:
        layer: select ports with GDS layer.
        prefix: select ports with prefix in port name.
        orientation: select ports with orientation in degrees.
        width: select ports with port width.
        layers_excluded: List of layers to exclude.
        port_type: select ports with port_type (optical, electrical, vertical_te).
        clockwise: if True, sort ports clockwise, False: counter-clockwise.
    """
    suffix = "o3_0" if len(component.ports) == 4 else "o2_0"
    ports = component.ports.filter(port_type=port_type, suffix=suffix, **kwargs)
    for port in ports:
        component.add_label(text=port.name, position=port.center, layer=label_layer)

    return component


margin = 0.5


def get_layer_stack(
    thickness_si: float = 10.0,  # Silicon substrate
    thickness_metal: float = 0.5,  # Metal thickness
    thickness_via: float = 0.3,  # Via thickness
    substrate_thickness: float = 300.0,  # Full substrate
) -> LayerStack:
    """Returns IHP PDK LayerStack for 3D visualization and simulation.

    Args:
        thickness_si: Silicon layer thickness in um.
        thickness_metal: Metal layer thickness in um.
        thickness_via: Via layer thickness in um.
        substrate_thickness: Substrate thickness in um.

    Returns:
        LayerStack for IHP PDK.
    """

    return LayerStack(
        layers=dict(
            # Substrate
            substrate=LayerLevel(
                layer=LAYER.SUBSTRATE,
                thickness=substrate_thickness,
                zmin=-substrate_thickness,
                material="si",
                info={"mesh_order": 99},
            ),
            # Active silicon
            active=LayerLevel(
                layer=LAYER.ACTIV,
                thickness=0.2,
                zmin=0.0,
                material="si",
                info={"mesh_order": 1},
            ),
            # Poly gate
            poly=LayerLevel(
                layer=LAYER.GATPOLY,
                thickness=0.18,
                zmin=0.0,
                material="poly_si",
                info={"mesh_order": 2},
            ),
            # Metal 1
            metal1=LayerLevel(
                layer=LAYER.METAL1,
                thickness=thickness_metal,
                zmin=1.0,
                material="aluminum",
                info={"mesh_order": 3},
            ),
            # Via 1
            via1=LayerLevel(
                layer=LAYER.VIA1,
                thickness=thickness_via,
                zmin=1.0 + thickness_metal,
                material="tungsten",
                info={"mesh_order": 4},
            ),
            # Metal 2
            metal2=LayerLevel(
                layer=LAYER.METAL2,
                thickness=thickness_metal,
                zmin=1.0 + thickness_metal + thickness_via,
                material="aluminum",
                info={"mesh_order": 5},
            ),
            # Via 2
            via2=LayerLevel(
                layer=LAYER.VIA2,
                thickness=thickness_via,
                zmin=1.0 + 2 * (thickness_metal + thickness_via),
                material="tungsten",
                info={"mesh_order": 6},
            ),
            # Metal 3
            metal3=LayerLevel(
                layer=LAYER.METAL3,
                thickness=thickness_metal,
                zmin=1.0 + 2 * (thickness_metal + thickness_via),
                material="aluminum",
                info={"mesh_order": 7},
            ),
            # Via 3
            via3=LayerLevel(
                layer=LAYER.VIA3,
                thickness=thickness_via,
                zmin=1.0 + 3 * (thickness_metal + thickness_via),
                material="tungsten",
                info={"mesh_order": 8},
            ),
            # Metal 4
            metal4=LayerLevel(
                layer=LAYER.METAL4,
                thickness=thickness_metal,
                zmin=1.0 + 3 * (thickness_metal + thickness_via),
                material="aluminum",
                info={"mesh_order": 9},
            ),
            # Via 4
            via4=LayerLevel(
                layer=LAYER.VIA4,
                thickness=thickness_via,
                zmin=1.0 + 4 * (thickness_metal + thickness_via),
                material="tungsten",
                info={"mesh_order": 10},
            ),
            # Metal 5
            metal5=LayerLevel(
                layer=LAYER.METAL5,
                thickness=thickness_metal,
                zmin=1.0 + 4 * (thickness_metal + thickness_via),
                material="aluminum",
                info={"mesh_order": 11},
            ),
            # Top Via 1
            topvia1=LayerLevel(
                layer=LAYER.TOPVIA1,
                thickness=thickness_via * 2,
                zmin=1.0 + 5 * (thickness_metal + thickness_via),
                material="tungsten",
                info={"mesh_order": 12},
            ),
            # Top Metal 1
            topmetal1=LayerLevel(
                layer=LAYER.TOPMETAL1,
                thickness=thickness_metal * 2,
                zmin=1.0 + 5 * (thickness_metal + thickness_via) + thickness_via,
                material="aluminum",
                info={"mesh_order": 13},
            ),
            # Top Via 2
            topvia2=LayerLevel(
                layer=LAYER.TOPVIA2,
                thickness=thickness_via * 3,
                zmin=1.0 + 6 * (thickness_metal + thickness_via),
                material="tungsten",
                info={"mesh_order": 14},
            ),
            # Top Metal 2
            topmetal2=LayerLevel(
                layer=LAYER.TOPMETAL2,
                thickness=thickness_metal * 3,
                zmin=1.0 + 6 * (thickness_metal + thickness_via) + thickness_via,
                material="aluminum",
                info={"mesh_order": 15},
            ),
        )
    )


class TechIHP(BaseModel):
    """IHP PDK Technology parameters."""

    # Grid and precision
    grid: float = 0.005  # 5nm grid
    precision: float = 1e-9

    # Design rules - transistors
    nmos_min_width: float = 0.15
    nmos_min_length: float = 0.13
    pmos_min_width: float = 0.15
    pmos_min_length: float = 0.13

    # Design rules - contacts and vias
    cont_size: float = 0.16
    cont_spacing: float = 0.18
    cont_enc_active: float = 0.07
    cont_enc_poly: float = 0.07
    cont_enc_metal: float = 0.06

    via1_size: float = 0.26
    via1_spacing: float = 0.36
    via1_enc_metal: float = 0.06

    # Design rules - metal
    metal1_width: float = 0.14
    metal1_spacing: float = 0.14
    metal2_width: float = 0.16
    metal2_spacing: float = 0.16
    metal3_width: float = 0.20
    metal3_spacing: float = 0.20
    metal4_width: float = 0.20
    metal4_spacing: float = 0.20
    metal5_width: float = 0.20
    metal5_spacing: float = 0.20
    topmetal1_width: float = 1.0
    topmetal1_spacing: float = 1.0
    topmetal2_width: float = 2.0
    topmetal2_spacing: float = 2.0

    # Design rules - resistors
    rsil_min_width: float = 0.4
    rsil_min_length: float = 0.8
    rsil_sheet_res: float = 7.0  # ohms/square

    rppd_min_width: float = 0.4
    rppd_min_length: float = 0.8
    rppd_sheet_res: float = 300.0  # ohms/square

    rhigh_min_width: float = 1.4
    rhigh_min_length: float = 5.0
    rhigh_sheet_res: float = 1350.0  # ohms/square

    # Design rules - capacitors
    mim_min_size: float = 0.5
    mim_cap_density: float = 1.5  # fF/um^2

    # Design rules - inductors
    inductor_min_width: float = 2.0
    inductor_min_spacing: float = 2.1
    inductor_min_diameter: float = 15.0


TECH = TechIHP()
LAYER_STACK = get_layer_stack()
LAYER_VIEWS = gf.technology.LayerViews(PATH.lyp)



############################
# Cross-sections functions
############################
cross_section = gf.cross_section.cross_section


# Metal routing cross-sections
metal1_routing = partial(
    cross_section,
    layer=LAYER.METAL1,
    width=TECH.metal1_width * 2,
    port_names=gf.cross_section.port_names_electrical,
    port_types=gf.cross_section.port_types_electrical,
    radius=None,
)

metal2_routing = partial(
    cross_section,
    layer=LAYER.METAL2,
    width=TECH.metal2_width * 2,
    port_names=gf.cross_section.port_names_electrical,
    port_types=gf.cross_section.port_types_electrical,
    radius=None,
)

metal3_routing = partial(
    cross_section,
    layer=LAYER.METAL3,
    width=TECH.metal3_width * 2,
    port_names=gf.cross_section.port_names_electrical,
    port_types=gf.cross_section.port_types_electrical,
    radius=None,
)

topmetal1_routing = partial(
    cross_section,
    layer=LAYER.TOPMETAL1,
    width=TECH.topmetal1_width,
    port_names=gf.cross_section.port_names_electrical,
    port_types=gf.cross_section.port_types_electrical,
    radius=None,
)

topmetal2_routing = partial(
    cross_section,
    layer=LAYER.TOPMETAL2,
    width=TECH.topmetal2_width,
    port_names=gf.cross_section.port_names_electrical,
    port_types=gf.cross_section.port_types_electrical,
    radius=None,
)

strip = topmetal2_routing
metal_routing = topmetal2_routing

cross_sections = get_cross_sections(sys.modules[__name__])

############################
# Routing functions
############################

route_bundle = partial(gf.routing.route_bundle, cross_section="strip")
route_bundle_rib = partial(
    route_bundle,
    cross_section="rib",
)
route_bundle_metal = partial(
    route_bundle,
    straight="straight_metal",
    bend="bend_metal",
    taper=None,
    cross_section="metal_routing",
    port_type="electrical",
)
route_bundle_metal_corner = partial(
    route_bundle,
    straight="straight_metal",
    bend="wire_corner",
    taper=None,
    cross_section="metal_routing",
    port_type="electrical",
)

route_astar = partial(
    add_bundle_astar,
    layers=["WG"],
    bend="bend_euler",
    straight="straight",
    grid_unit=500,
    spacing=3,
)

route_astar_metal = partial(
    add_bundle_astar,
    layers=["M2_ROUTER"],
    bend="wire_corner",
    straight="straight_metal",
    grid_unit=500,
    spacing=15,
)


routing_strategies = dict(
    route_bundle=route_bundle,
    route_bundle_rib=route_bundle_rib,
    route_bundle_metal=route_bundle_metal,
    route_bundle_metal_corner=route_bundle_metal_corner,
    route_astar=route_astar,
    route_astar_metal=route_astar_metal,
)
