<Qucs Schematic 24.3.0>
<Properties>
  <View=-126,20,1510,1072,0.958817,0,2>
  <Grid=10,10,1>
  <DataSet=dc_esd_op.dat>
  <DataDisplay=dc_esd_op.dpl>
  <OpenDisplay=0>
  <Script=dc_esd_op.m>
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
  <.SW SW1 1 60 690 0 71 0 0 "DC1" 1 "lin" 1 "V2" 1 "-15" 1 "2" 1 "301" 1>
  <INCLSCR INCLSCR1 1 120 550 -60 16 0 0 "\n.INCLUDE sg13g2_esd.lib\n" 1 "" 0 "" 0>
  <GND * 1 400 310 0 0 0 0>
  <Vdc V2 1 400 220 18 -26 0 1 "1 V" 1>
  <GND * 1 690 310 0 0 0 0>
  <IProbe Pr2 1 690 110 -37 -26 0 3>
  <IProbe Pr1 1 570 110 -37 -26 0 3>
  <IProbe Pr4 1 910 250 -37 -26 0 3>
  <IProbe Pr3 1 1030 250 -37 -26 0 3>
  <GND * 1 1030 320 0 0 0 0>
  <GND * 1 910 320 0 0 0 0>
  <Lib diodevdd_2kv1 1 690 230 -169 -40 1 3 "$HOME/.qucs/user_lib/IHP_PDK_nonlinear_components" 0 "diodevdd_2kv" 0 "1" 1>
  <Lib diodevss_2kv1 1 1030 150 -165 -40 1 3 "$HOME/.qucs/user_lib/IHP_PDK_nonlinear_components" 0 "diodevss_2kv" 0 "1" 1>
</Components>
<Wires>
  <400 250 400 310 "" 0 0 0 "">
  <400 60 400 190 "" 0 0 0 "">
  <690 60 690 80 "" 0 0 0 "">
  <690 140 690 200 "" 0 0 0 "">
  <690 260 690 310 "" 0 0 0 "">
  <570 230 660 230 "" 0 0 0 "">
  <400 60 570 60 "" 0 0 0 "">
  <570 60 690 60 "" 0 0 0 "">
  <570 60 570 80 "" 0 0 0 "">
  <570 140 570 230 "" 0 0 0 "">
  <690 60 1030 60 "" 0 0 0 "">
  <1030 60 1030 120 "" 0 0 0 "">
  <1030 180 1030 220 "" 0 0 0 "">
  <1030 280 1030 320 "" 0 0 0 "">
  <910 280 910 320 "" 0 0 0 "">
  <910 150 1000 150 "" 0 0 0 "">
  <910 150 910 220 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 481 926 849 469 3 #c0c0c0 1 00 1 -15 1 2 1 -0.307323 0.05 0.167933 1 -1 0.2 1 315 0 225 1 0 0 "" "" "">
	<"ngspice/i(pr1)" #0000ff 0 3 0 0 0>
	<"ngspice/i(pr3)" #ff0000 1 3 0 0 0>
	<"ngspice/i(pr4)" #ff00ff 1 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
