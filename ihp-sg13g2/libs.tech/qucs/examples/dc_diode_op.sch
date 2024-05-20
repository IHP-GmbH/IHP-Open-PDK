<Qucs Schematic 24.2.0>
<Properties>
  <View=-86,-4,1624,1075,1.25348,0,181>
  <Grid=10,10,1>
  <DataSet=dc_diode_op.dat>
  <DataDisplay=dc_diode_op.dpl>
  <OpenDisplay=0>
  <Script=diode.m>
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
  <.SW SW1 1 90 280 0 68 0 0 "DC1" 1 "lin" 1 "V2" 1 "0" 1 "1" 1 "301" 1 "false" 0>
  <GND * 1 270 840 0 0 0 0>
  <IProbe Pr1 1 270 640 -37 -26 0 3>
  <INCLSCR INCLSCR1 1 130 50 -60 16 0 0 ".INCLUDE ~/.qucs/IHP-Open-PDK-main/ihp-sg13g2/libs.tech/ngspice/models/diodes.lib\n.control\npre_osdi ~/.qucs/psp103_nqs.osdi\n.endc" 1 "" 0 "" 0>
  <.DC DC1 1 90 180 0 41 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <GND * 1 120 840 0 0 0 0>
  <Vdc V2 1 120 750 18 -26 0 1 "1 V" 1>
  <Lib dantenna1 1 270 750 40 -16 0 0 "/home/herman/.qucs/user_lib/IHP_PDK_nonlinear_components" 0 "dantenna" 0 "8u" 1 "8u" 1>
  <GND * 1 470 840 0 0 0 0>
  <IProbe Pr2 1 470 640 -37 -26 0 3>
  <Lib dpantenna1 1 470 750 40 -16 0 0 "/home/herman/.qucs/user_lib/IHP_PDK_nonlinear_components" 0 "dpantenna" 0 "16u" 1 "16u" 1>
</Components>
<Wires>
  <270 590 270 610 "" 0 0 0 "">
  <120 590 270 590 "" 0 0 0 "">
  <120 780 120 840 "" 0 0 0 "">
  <120 590 120 720 "" 0 0 0 "">
  <270 670 270 730 "" 0 0 0 "">
  <270 790 270 840 "" 0 0 0 "">
  <470 590 470 610 "" 0 0 0 "">
  <470 670 470 730 "" 0 0 0 "">
  <470 790 470 840 "" 0 0 0 "">
  <270 590 470 590 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 639 890 831 618 3 #c0c0c0 1 00 1 0 0.1 1 0 0 2e-06 2e-05 1 -1 0.2 1 315 0 225 1 0 0 "" "" "">
	<"ngspice/i(pr1)" #0000ff 2 3 0 0 0>
	<"ngspice/i(pr2)" #ff0000 2 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
