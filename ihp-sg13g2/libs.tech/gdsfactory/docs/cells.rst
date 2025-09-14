

Here are the components available in the PDK


Cells
=============================


CuPillarPad
----------------------------------------------------

.. autofunction:: ihp.cells.CuPillarPad

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.CuPillarPad()
  c.plot()



L2_IND_LVS
----------------------------------------------------

.. autofunction:: ihp.cells.L2_IND_LVS

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.L2_IND_LVS()
  c.plot()



M1_GatPoly_CDNS_675179387644
----------------------------------------------------

.. autofunction:: ihp.cells.M1_GatPoly_CDNS_675179387644

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.M1_GatPoly_CDNS_675179387644()
  c.plot()



M2_M1_CDNS_675179387643
----------------------------------------------------

.. autofunction:: ihp.cells.M2_M1_CDNS_675179387643

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.M2_M1_CDNS_675179387643()
  c.plot()



M3_M2_CDNS_675179387642
----------------------------------------------------

.. autofunction:: ihp.cells.M3_M2_CDNS_675179387642

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.M3_M2_CDNS_675179387642()
  c.plot()



M4_M3_CDNS_675179387641
----------------------------------------------------

.. autofunction:: ihp.cells.M4_M3_CDNS_675179387641

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.M4_M3_CDNS_675179387641()
  c.plot()



M5_M4_CDNS_675179387640
----------------------------------------------------

.. autofunction:: ihp.cells.M5_M4_CDNS_675179387640

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.M5_M4_CDNS_675179387640()
  c.plot()



NoFillerStack
----------------------------------------------------

.. autofunction:: ihp.cells.NoFillerStack

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.NoFillerStack()
  c.plot()



SVaricap
----------------------------------------------------

.. autofunction:: ihp.cells.SVaricap

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.SVaricap()
  c.plot()



TM1_M5_CDNS_675179387645
----------------------------------------------------

.. autofunction:: ihp.cells.TM1_M5_CDNS_675179387645

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.TM1_M5_CDNS_675179387645()
  c.plot()



TM2_TM1_CDNS_675179387646
----------------------------------------------------

.. autofunction:: ihp.cells.TM2_TM1_CDNS_675179387646

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.TM2_TM1_CDNS_675179387646()
  c.plot()



TSV
----------------------------------------------------

.. autofunction:: ihp.cells.TSV

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.TSV()
  c.plot()



ViaStack
----------------------------------------------------

.. autofunction:: ihp.cells.ViaStack

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.ViaStack()
  c.plot()



add_pads_top
----------------------------------------------------

.. autofunction:: ihp.cells.add_pads_top

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.add_pads_top(component='straight', cross_section='metal_routing', pad_port_name='e1', pad='CuPillarPad', bend='wire_corner', straight_separation=15.0, pad_pitch=100.0, port_type='electrical', allow_width_mismatch=True, fanout_length=80, route_width=0)
  c.plot()



bend_euler
----------------------------------------------------

.. autofunction:: ihp.cells.bend_euler

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.bend_euler(angle=90, p=0.5, cross_section='strip', allow_min_radius_violation=False)
  c.plot()



bend_metal
----------------------------------------------------

.. autofunction:: ihp.cells.bend_metal

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.bend_metal(angle=90, cross_section='metal_routing')
  c.plot()



bend_s
----------------------------------------------------

.. autofunction:: ihp.cells.bend_s

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.bend_s(size=(11, 1.8), cross_section='strip', allow_min_radius_violation=False)
  c.plot()



bend_s_metal
----------------------------------------------------

.. autofunction:: ihp.cells.bend_s_metal

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.bend_s_metal(size=(11, 1.8), cross_section='metal_routing', allow_min_radius_violation=True)
  c.plot()



bondpad
----------------------------------------------------

.. autofunction:: ihp.cells.bondpad

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.bondpad()
  c.plot()



bondpad_array
----------------------------------------------------

.. autofunction:: ihp.cells.bondpad_array

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.bondpad_array(n_pads=4, pad_pitch=100.0, pad_diameter=68.0, shape='octagon', stack_metals=True)
  c.plot()



chipText
----------------------------------------------------

.. autofunction:: ihp.cells.chipText

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.chipText()
  c.plot()



cmim
----------------------------------------------------

.. autofunction:: ihp.cells.cmim

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.cmim()
  c.plot()



colors_and_stipples
----------------------------------------------------

.. autofunction:: ihp.cells.colors_and_stipples

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.colors_and_stipples()
  c.plot()



dantenna
----------------------------------------------------

.. autofunction:: ihp.cells.dantenna

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.dantenna()
  c.plot()



diffstbprobe
----------------------------------------------------

.. autofunction:: ihp.cells.diffstbprobe

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.diffstbprobe()
  c.plot()



diodevdd_2kv
----------------------------------------------------

.. autofunction:: ihp.cells.diodevdd_2kv

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.diodevdd_2kv()
  c.plot()



diodevdd_4kv
----------------------------------------------------

.. autofunction:: ihp.cells.diodevdd_4kv

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.diodevdd_4kv()
  c.plot()



diodevss_2kv
----------------------------------------------------

.. autofunction:: ihp.cells.diodevss_2kv

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.diodevss_2kv()
  c.plot()



diodevss_4kv
----------------------------------------------------

.. autofunction:: ihp.cells.diodevss_4kv

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.diodevss_4kv()
  c.plot()



dpantenna
----------------------------------------------------

.. autofunction:: ihp.cells.dpantenna

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.dpantenna()
  c.plot()



dummy1
----------------------------------------------------

.. autofunction:: ihp.cells.dummy1

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.dummy1()
  c.plot()



esd_nmos
----------------------------------------------------

.. autofunction:: ihp.cells.esd_nmos

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.esd_nmos(width=50.0, length=0.5, nf=10, model='esd_nmos')
  c.plot()



import_gds
----------------------------------------------------

.. autofunction:: ihp.cells.import_gds

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.import_gds(post_process=(functools.partial(<function add_ports_from_markers_center at 0x1212a00e0>, inside=True, pin_layer=(8, 2), port_layer=(8, 0)), functools.partial(<function add_ports_from_markers_center at 0x1212a00e0>, inside=True, pin_layer=(10, 2), port_layer=(10, 0))), rename_duplicated_cells=False)
  c.plot()



inductor2
----------------------------------------------------

.. autofunction:: ihp.cells.inductor2

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.inductor2(width=2.0, space=2.1, diameter=15.48, resistance=0.5777, inductance=3.3303e-11, turns=1, block_qrc=True, substrate_etch=False)
  c.plot()



inductor3
----------------------------------------------------

.. autofunction:: ihp.cells.inductor3

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.inductor3(width=2.0, space=2.1, diameter=24.68, resistance=1.386, inductance=2.215e-10, turns=2, block_qrc=True, substrate_etch=False)
  c.plot()



iprobe
----------------------------------------------------

.. autofunction:: ihp.cells.iprobe

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.iprobe()
  c.plot()



isolbox
----------------------------------------------------

.. autofunction:: ihp.cells.isolbox

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.isolbox()
  c.plot()



lvsres
----------------------------------------------------

.. autofunction:: ihp.cells.lvsres

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.lvsres()
  c.plot()



nmos
----------------------------------------------------

.. autofunction:: ihp.cells.nmos

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.nmos(width=1.0, length=0.13, nf=1, m=1, model='sg13_lv_nmos')
  c.plot()



nmosHV
----------------------------------------------------

.. autofunction:: ihp.cells.nmosHV

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.nmosHV()
  c.plot()



nmos_hv
----------------------------------------------------

.. autofunction:: ihp.cells.nmos_hv

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.nmos_hv(width=1.0, length=0.45, nf=1, m=1, model='sg13_hv_nmos')
  c.plot()



nmoscl_2
----------------------------------------------------

.. autofunction:: ihp.cells.nmoscl_2

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.nmoscl_2()
  c.plot()



nmoscl_4
----------------------------------------------------

.. autofunction:: ihp.cells.nmoscl_4

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.nmoscl_4()
  c.plot()



npn13G2
----------------------------------------------------

.. autofunction:: ihp.cells.npn13G2

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.npn13G2()
  c.plot()



npn13G2L
----------------------------------------------------

.. autofunction:: ihp.cells.npn13G2L

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.npn13G2L()
  c.plot()



npn13G2V
----------------------------------------------------

.. autofunction:: ihp.cells.npn13G2V

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.npn13G2V()
  c.plot()



npn13G2_base_CDNS_675179387640
----------------------------------------------------

.. autofunction:: ihp.cells.npn13G2_base_CDNS_675179387640

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.npn13G2_base_CDNS_675179387640()
  c.plot()



ntap
----------------------------------------------------

.. autofunction:: ihp.cells.ntap

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.ntap()
  c.plot()



ntap1
----------------------------------------------------

.. autofunction:: ihp.cells.ntap1

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.ntap1(width=1.0, length=1.0, rows=1, cols=1)
  c.plot()



pack_doe
----------------------------------------------------

.. autofunction:: ihp.cells.pack_doe

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.pack_doe(do_permutations=False)
  c.plot()



pack_doe_grid
----------------------------------------------------

.. autofunction:: ihp.cells.pack_doe_grid

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.pack_doe_grid(do_permutations=False, with_text=False)
  c.plot()



pmos
----------------------------------------------------

.. autofunction:: ihp.cells.pmos

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.pmos(width=1.0, length=0.13, nf=1, m=1, model='sg13_lv_pmos')
  c.plot()



pmosHV
----------------------------------------------------

.. autofunction:: ihp.cells.pmosHV

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.pmosHV()
  c.plot()



pmos_hv
----------------------------------------------------

.. autofunction:: ihp.cells.pmos_hv

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.pmos_hv(width=1.0, length=0.45, nf=1, m=1, model='sg13_hv_pmos')
  c.plot()



pnpMPA
----------------------------------------------------

.. autofunction:: ihp.cells.pnpMPA

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.pnpMPA()
  c.plot()



ptap
----------------------------------------------------

.. autofunction:: ihp.cells.ptap

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.ptap()
  c.plot()



ptap1
----------------------------------------------------

.. autofunction:: ihp.cells.ptap1

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.ptap1(width=1.0, length=1.0, rows=1, cols=1)
  c.plot()



rfcmim
----------------------------------------------------

.. autofunction:: ihp.cells.rfcmim

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.rfcmim()
  c.plot()



rfnmos
----------------------------------------------------

.. autofunction:: ihp.cells.rfnmos

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.rfnmos(width=2.0, length=0.13, nf=2, m=1, model='sg13_lv_rfnmos')
  c.plot()



rfnmosHV
----------------------------------------------------

.. autofunction:: ihp.cells.rfnmosHV

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.rfnmosHV()
  c.plot()



rfpmos
----------------------------------------------------

.. autofunction:: ihp.cells.rfpmos

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.rfpmos(width=2.0, length=0.13, nf=2, m=1, model='sg13_lv_rfpmos')
  c.plot()



rfpmosHV
----------------------------------------------------

.. autofunction:: ihp.cells.rfpmosHV

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.rfpmosHV()
  c.plot()



rhigh
----------------------------------------------------

.. autofunction:: ihp.cells.rhigh

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.rhigh(width=1.4, length=20.0, model='rhigh')
  c.plot()



rppd
----------------------------------------------------

.. autofunction:: ihp.cells.rppd

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.rppd(width=0.8, length=10.0, model='rppd')
  c.plot()



rsil
----------------------------------------------------

.. autofunction:: ihp.cells.rsil

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.rsil(width=0.8, length=10.0, model='rsil')
  c.plot()



schottky_nbl1
----------------------------------------------------

.. autofunction:: ihp.cells.schottky_nbl1

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.schottky_nbl1()
  c.plot()



scr1
----------------------------------------------------

.. autofunction:: ihp.cells.scr1

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.scr1()
  c.plot()



sealring
----------------------------------------------------

.. autofunction:: ihp.cells.sealring

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.sealring(width=200.0, height=200.0, ring_width=5.0)
  c.plot()



sealring_CDNS_675179387642
----------------------------------------------------

.. autofunction:: ihp.cells.sealring_CDNS_675179387642

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.sealring_CDNS_675179387642()
  c.plot()



sealring_complete
----------------------------------------------------

.. autofunction:: ihp.cells.sealring_complete

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.sealring_complete()
  c.plot()



sealring_corner_CDNS_675179387641
----------------------------------------------------

.. autofunction:: ihp.cells.sealring_corner_CDNS_675179387641

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.sealring_corner_CDNS_675179387641()
  c.plot()



straight
----------------------------------------------------

.. autofunction:: ihp.cells.straight

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.straight(length=10, cross_section='strip', npoints=2)
  c.plot()



straight_metal
----------------------------------------------------

.. autofunction:: ihp.cells.straight_metal

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.straight_metal(length=10, cross_section='metal_routing')
  c.plot()



svaricap
----------------------------------------------------

.. autofunction:: ihp.cells.svaricap

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.svaricap(width=1.0, length=1.0, nf=1, model='svaricap')
  c.plot()



text_rectangular
----------------------------------------------------

.. autofunction:: ihp.cells.text_rectangular

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.text_rectangular(text='abc', size=3, justify='left', layer='TOPMETAL2')
  c.plot()



text_rectangular_multi_layer
----------------------------------------------------

.. autofunction:: ihp.cells.text_rectangular_multi_layer

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.text_rectangular_multi_layer(text='abc', layers=('TOPMETAL2',), text_factory='text_rectangular')
  c.plot()



via_array
----------------------------------------------------

.. autofunction:: ihp.cells.via_array

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.via_array(via_type='Via1', columns=2, rows=2)
  c.plot()



via_stack
----------------------------------------------------

.. autofunction:: ihp.cells.via_stack

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.via_stack(bottom_layer='Metal1', top_layer='Metal2', size=(10.0, 10.0), vn_columns=2, vn_rows=2, vt1_columns=1, vt1_rows=1, vt2_columns=1, vt2_rows=1)
  c.plot()



via_stack_with_pads
----------------------------------------------------

.. autofunction:: ihp.cells.via_stack_with_pads

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.via_stack_with_pads(bottom_layer='Metal1', top_layer='TopMetal2', size=(10.0, 10.0), pad_size=(20.0, 20.0), pad_spacing=50.0)
  c.plot()



wire_corner
----------------------------------------------------

.. autofunction:: ihp.cells.wire_corner

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.wire_corner(cross_section='metal_routing')
  c.plot()



wire_corner45
----------------------------------------------------

.. autofunction:: ihp.cells.wire_corner45

.. plot::
  :include-source:

  from ihp import PDK, cells

  PDK.activate()

  c = cells.wire_corner45(cross_section='metal_routing', radius=10, with_corner90_ports=True)
  c.plot()

