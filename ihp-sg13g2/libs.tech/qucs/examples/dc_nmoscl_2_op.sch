<Qucs Schematic 24.3.0>
<Properties>
  <View=-7,24,1560,931,1.0011,0,0>
  <Grid=10,10,1>
  <DataSet=dc_nmoscl_2_op.dat>
  <DataDisplay=dc_nmoscl_2_op.dpl>
  <OpenDisplay=0>
  <Script=dc_nmoscl_2_op.m>
  <RunScript=0>
  <showFrame=3>
  <FrameText0=DC simulation of  ESD diodes>
  <FrameText1=Drawn By:IHP PDK Authors>
  <FrameText2=Date:2024>
  <FrameText3=Revision:1>
</Properties>
<Symbol>
</Symbol>
<Components>
  <.SW SW1 1 90 280 0 71 0 0 "DC1" 1 "lin" 1 "V2" 1 "-20" 1 "1" 1 "301" 1>
  <GND * 1 270 840 0 0 0 0>
  <IProbe Pr1 1 270 640 -37 -26 0 3>
  <GND * 1 120 840 0 0 0 0>
  <Vdc V2 1 120 750 18 -26 0 1 "1 V" 1>
  <GND * 1 470 840 0 0 0 0>
  <IProbe Pr2 1 470 640 -37 -26 0 3>
  <SpiceLib SpiceLib1 1 100 80 -13 18 0 0 "cornerMOSlv.lib" 1 "mos_tt" 1>
  <Lib nmoscl_1 1 270 760 16 -20 0 3 "$HOME/.qucs/user_lib/IHP_PDK_nonlinear_components" 0 "nmoscl_2" 0 "1" 1>
  <Lib nmoscl_2 1 470 750 16 -20 0 3 "$HOME/.qucs/user_lib/IHP_PDK_nonlinear_components" 0 "nmoscl_4" 0 "1" 1>
</Components>
<Wires>
  <270 590 270 610 "" 0 0 0 "">
  <120 590 270 590 "" 0 0 0 "">
  <120 780 120 840 "" 0 0 0 "">
  <120 590 120 720 "" 0 0 0 "">
  <270 670 270 730 "" 0 0 0 "">
  <270 790 270 840 "" 0 0 0 "">
  <470 590 470 610 "" 0 0 0 "">
  <270 590 470 590 "" 0 0 0 "">
  <470 780 470 840 "" 0 0 0 "">
  <470 670 470 720 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 639 890 831 618 3 #c0c0c0 1 00 1 0 0.2 2 1 0 2e-06 2e-05 1 -1 0.2 1 315 0 225 1 0 0 "" "" "">
	<"ngspice/i(pr1)" #0000ff 2 3 0 0 0>
	<"ngspice/i(pr2)" #ff0000 2 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
