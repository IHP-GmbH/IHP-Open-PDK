"""Bipolar transistor components for IHP PDK."""

from typing import Literal, Optional
from toolz import compose

import gdsfactory as gf
from gdsfactory import Component


from pathlib import Path
from functools import partial
import gdsfactory as gf
from ihp.config import PATH

add_ports_metal1 = partial(
    gf.add_ports.add_ports_from_markers_inside, pin_layer=(8, 2), port_layer=(8, 0)
)
add_ports_metal2 = partial(
    gf.add_ports.add_ports_from_markers_inside, pin_layer=(10, 2), port_layer=(10, 0)
)
add_ports = (add_ports_metal1, add_ports_metal2)


gdsdir = PATH.gds

import_gds = partial(gf.import_gds, post_process=add_ports)


@gf.cell
def CuPillarPad() -> gf.Component:
    """Returns CuPillarPad fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.CuPillarPad()
      c.plot()
    """
    return import_gds(gdsdir / "CuPillarPad.gds")


@gf.cell
def L2_IND_LVS() -> gf.Component:
    """Returns L2_IND_LVS fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.L2_IND_LVS()
      c.plot()
    """
    return import_gds(gdsdir / "L2_IND_LVS.gds")


@gf.cell
def M1_GatPoly_CDNS_675179387644() -> gf.Component:
    """Returns M1_GatPoly_CDNS_675179387644 fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.M1_GatPoly_CDNS_675179387644()
      c.plot()
    """
    return import_gds(gdsdir / "M1_GatPoly_CDNS_675179387644.gds")


@gf.cell
def M2_M1_CDNS_675179387643() -> gf.Component:
    """Returns M2_M1_CDNS_675179387643 fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.M2_M1_CDNS_675179387643()
      c.plot()
    """
    return import_gds(gdsdir / "M2_M1_CDNS_675179387643.gds")


@gf.cell
def M3_M2_CDNS_675179387642() -> gf.Component:
    """Returns M3_M2_CDNS_675179387642 fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.M3_M2_CDNS_675179387642()
      c.plot()
    """
    return import_gds(gdsdir / "M3_M2_CDNS_675179387642.gds")


@gf.cell
def M4_M3_CDNS_675179387641() -> gf.Component:
    """Returns M4_M3_CDNS_675179387641 fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.M4_M3_CDNS_675179387641()
      c.plot()
    """
    return import_gds(gdsdir / "M4_M3_CDNS_675179387641.gds")


@gf.cell
def M5_M4_CDNS_675179387640() -> gf.Component:
    """Returns M5_M4_CDNS_675179387640 fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.M5_M4_CDNS_675179387640()
      c.plot()
    """
    return import_gds(gdsdir / "M5_M4_CDNS_675179387640.gds")


@gf.cell
def NoFillerStack() -> gf.Component:
    """Returns NoFillerStack fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.NoFillerStack()
      c.plot()
    """
    return import_gds(gdsdir / "NoFillerStack.gds")


@gf.cell
def SVaricap() -> gf.Component:
    """Returns SVaricap fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.SVaricap()
      c.plot()
    """
    return import_gds(gdsdir / "SVaricap.gds")


@gf.cell
def TM1_M5_CDNS_675179387645() -> gf.Component:
    """Returns TM1_M5_CDNS_675179387645 fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.TM1_M5_CDNS_675179387645()
      c.plot()
    """
    return import_gds(gdsdir / "TM1_M5_CDNS_675179387645.gds")


@gf.cell
def TM2_TM1_CDNS_675179387646() -> gf.Component:
    """Returns TM2_TM1_CDNS_675179387646 fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.TM2_TM1_CDNS_675179387646()
      c.plot()
    """
    return import_gds(gdsdir / "TM2_TM1_CDNS_675179387646.gds")


@gf.cell
def TSV() -> gf.Component:
    """Returns TSV fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.TSV()
      c.plot()
    """
    return import_gds(gdsdir / "TSV.gds")


@gf.cell
def ViaStack() -> gf.Component:
    """Returns ViaStack fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.ViaStack()
      c.plot()
    """
    return import_gds(gdsdir / "ViaStack.gds")


@gf.cell
def bondpad() -> gf.Component:
    """Returns bondpad fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.bondpad()
      c.plot()
    """
    return import_gds(gdsdir / "bondpad.gds")


@gf.cell
def chipText() -> gf.Component:
    """Returns chipText fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.chipText()
      c.plot()
    """
    return import_gds(gdsdir / "chipText.gds")


@gf.cell
def cmim() -> gf.Component:
    """Returns cmim fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.cmim()
      c.plot()
    """
    return import_gds(gdsdir / "cmim.gds")


@gf.cell
def colors_and_stipples() -> gf.Component:
    """Returns colors_and_stipples fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.colors_and_stipples()
      c.plot()
    """
    return import_gds(gdsdir / "colors_and_stipples.gds")


@gf.cell
def dantenna() -> gf.Component:
    """Returns dantenna fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.dantenna()
      c.plot()
    """
    return import_gds(gdsdir / "dantenna.gds")


@gf.cell
def diffstbprobe() -> gf.Component:
    """Returns diffstbprobe fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.diffstbprobe()
      c.plot()
    """
    return import_gds(gdsdir / "diffstbprobe.gds")


@gf.cell
def diodevdd_2kv() -> gf.Component:
    """Returns diodevdd_2kv fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.diodevdd_2kv()
      c.plot()
    """
    return import_gds(gdsdir / "diodevdd_2kv.gds")


@gf.cell
def diodevdd_4kv() -> gf.Component:
    """Returns diodevdd_4kv fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.diodevdd_4kv()
      c.plot()
    """
    return import_gds(gdsdir / "diodevdd_4kv.gds")


@gf.cell
def diodevss_2kv() -> gf.Component:
    """Returns diodevss_2kv fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.diodevss_2kv()
      c.plot()
    """
    return import_gds(gdsdir / "diodevss_2kv.gds")


@gf.cell
def diodevss_4kv() -> gf.Component:
    """Returns diodevss_4kv fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.diodevss_4kv()
      c.plot()
    """
    return import_gds(gdsdir / "diodevss_4kv.gds")


@gf.cell
def dpantenna() -> gf.Component:
    """Returns dpantenna fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.dpantenna()
      c.plot()
    """
    return import_gds(gdsdir / "dpantenna.gds")


@gf.cell
def dummy1() -> gf.Component:
    """Returns dummy1 fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.dummy1()
      c.plot()
    """
    return import_gds(gdsdir / "dummy1.gds")


@gf.cell
def inductor2() -> gf.Component:
    """Returns inductor2 fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.inductor2()
      c.plot()
    """
    return import_gds(gdsdir / "inductor2.gds")


@gf.cell
def inductor3() -> gf.Component:
    """Returns inductor3 fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.inductor3()
      c.plot()
    """
    return import_gds(gdsdir / "inductor3.gds")


@gf.cell
def iprobe() -> gf.Component:
    """Returns iprobe fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.iprobe()
      c.plot()
    """
    return import_gds(gdsdir / "iprobe.gds")


@gf.cell
def isolbox() -> gf.Component:
    """Returns isolbox fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.isolbox()
      c.plot()
    """
    return import_gds(gdsdir / "isolbox.gds")


@gf.cell
def lvsres() -> gf.Component:
    """Returns lvsres fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.lvsres()
      c.plot()
    """
    return import_gds(gdsdir / "lvsres.gds")


@gf.cell
def nmos() -> gf.Component:
    """Returns nmos fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.nmos()
      c.plot()
    """
    return import_gds(gdsdir / "nmos.gds")


@gf.cell
def nmosHV() -> gf.Component:
    """Returns nmosHV fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.nmosHV()
      c.plot()
    """
    return import_gds(gdsdir / "nmosHV.gds")


@gf.cell
def nmoscl_2() -> gf.Component:
    """Returns nmoscl_2 fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.nmoscl_2()
      c.plot()
    """
    return import_gds(gdsdir / "nmoscl_2.gds")


@gf.cell
def nmoscl_4() -> gf.Component:
    """Returns nmoscl_4 fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.nmoscl_4()
      c.plot()
    """
    return import_gds(gdsdir / "nmoscl_4.gds")


@gf.cell
def npn13G2() -> gf.Component:
    """Returns npn13G2 fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.npn13G2()
      c.plot()
    """
    return import_gds(gdsdir / "npn13G2.gds")


@gf.cell
def npn13G2L() -> gf.Component:
    """Returns npn13G2L fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.npn13G2L()
      c.plot()
    """
    return import_gds(gdsdir / "npn13G2L.gds")


@gf.cell
def npn13G2V() -> gf.Component:
    """Returns npn13G2V fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.npn13G2V()
      c.plot()
    """
    return import_gds(gdsdir / "npn13G2V.gds")


@gf.cell
def npn13G2_base_CDNS_675179387640() -> gf.Component:
    """Returns npn13G2_base_CDNS_675179387640 fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.npn13G2_base_CDNS_675179387640()
      c.plot()
    """
    return import_gds(gdsdir / "npn13G2_base_CDNS_675179387640.gds")


@gf.cell
def ntap() -> gf.Component:
    """Returns ntap fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.ntap()
      c.plot()
    """
    return import_gds(gdsdir / "ntap.gds")


@gf.cell
def ntap1() -> gf.Component:
    """Returns ntap1 fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.ntap1()
      c.plot()
    """
    return import_gds(gdsdir / "ntap1.gds")


@gf.cell
def pmos() -> gf.Component:
    """Returns pmos fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.pmos()
      c.plot()
    """
    return import_gds(gdsdir / "pmos.gds")


@gf.cell
def pmosHV() -> gf.Component:
    """Returns pmosHV fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.pmosHV()
      c.plot()
    """
    return import_gds(gdsdir / "pmosHV.gds")


@gf.cell
def pnpMPA() -> gf.Component:
    """Returns pnpMPA fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.pnpMPA()
      c.plot()
    """
    return import_gds(gdsdir / "pnpMPA.gds")


@gf.cell
def ptap() -> gf.Component:
    """Returns ptap fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.ptap()
      c.plot()
    """
    return import_gds(gdsdir / "ptap.gds")


@gf.cell
def ptap1() -> gf.Component:
    """Returns ptap1 fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.ptap1()
      c.plot()
    """
    return import_gds(gdsdir / "ptap1.gds")


@gf.cell
def rfcmim() -> gf.Component:
    """Returns rfcmim fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.rfcmim()
      c.plot()
    """
    return import_gds(gdsdir / "rfcmim.gds")


@gf.cell
def rfnmos() -> gf.Component:
    """Returns rfnmos fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.rfnmos()
      c.plot()
    """
    return import_gds(gdsdir / "rfnmos.gds")


@gf.cell
def rfnmosHV() -> gf.Component:
    """Returns rfnmosHV fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.rfnmosHV()
      c.plot()
    """
    return import_gds(gdsdir / "rfnmosHV.gds")


@gf.cell
def rfpmos() -> gf.Component:
    """Returns rfpmos fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.rfpmos()
      c.plot()
    """
    return import_gds(gdsdir / "rfpmos.gds")


@gf.cell
def rfpmosHV() -> gf.Component:
    """Returns rfpmosHV fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.rfpmosHV()
      c.plot()
    """
    return import_gds(gdsdir / "rfpmosHV.gds")


@gf.cell
def rhigh() -> gf.Component:
    """Returns rhigh fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.rhigh()
      c.plot()
    """
    return import_gds(gdsdir / "rhigh.gds")


@gf.cell
def rppd() -> gf.Component:
    """Returns rppd fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.rppd()
      c.plot()
    """
    return import_gds(gdsdir / "rppd.gds")


@gf.cell
def rsil() -> gf.Component:
    """Returns rsil fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.rsil()
      c.plot()
    """
    return import_gds(gdsdir / "rsil.gds")


@gf.cell
def schottky_nbl1() -> gf.Component:
    """Returns schottky_nbl1 fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.schottky_nbl1()
      c.plot()
    """
    return import_gds(gdsdir / "schottky_nbl1.gds")


@gf.cell
def scr1() -> gf.Component:
    """Returns scr1 fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.scr1()
      c.plot()
    """
    return import_gds(gdsdir / "scr1.gds")


@gf.cell
def sealring_CDNS_675179387642() -> gf.Component:
    """Returns sealring_CDNS_675179387642 fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.sealring_CDNS_675179387642()
      c.plot()
    """
    return import_gds(gdsdir / "sealring_CDNS_675179387642.gds")


@gf.cell
def sealring_complete() -> gf.Component:
    """Returns sealring_complete fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.sealring_complete()
      c.plot()
    """
    return import_gds(gdsdir / "sealring_complete.gds")


@gf.cell
def sealring_corner_CDNS_675179387641() -> gf.Component:
    """Returns sealring_corner_CDNS_675179387641 fixed cell.

    .. plot::
      :include-source:

      import ihp

      c = ihp.cells.sealring_corner_CDNS_675179387641()
      c.plot()
    """
    return import_gds(gdsdir / "sealring_corner_CDNS_675179387641.gds")


if __name__ == "__main__":
    # c = sealring_corner_CDNS_675179387641()
    c=  schottky_nbl1()
    c.show()
