<Qucs Schematic 24.4.1>
<Properties>
  <View=-143,-6,1617,996,0.893214,0,0>
  <Grid=10,10,1>
  <DataSet=ac_mim_cap.dat>
  <DataDisplay=ac_mim_cap.dpl>
  <OpenDisplay=0>
  <Script=cmim_AC.m>
  <RunScript=0>
  <showFrame=3>
  <FrameText0=AC Mim capacitor simulation>
  <FrameText1=Drawn By: IHP PDK Authors>
  <FrameText2=Date:2024>
  <FrameText3=Revision:1>
</Properties>
<Symbol>
</Symbol>
<Components>
  <.AC AC1 1 70 190 0 42 0 0 "log" 1 "100k" 1 "300 GHz" 1 "101" 1 "no" 0>
  <GND * 1 360 650 0 0 0 0>
  <Vac V1 1 70 570 18 -26 0 1 "1 V" 1 "1 kHz" 0 "0" 0 "0" 0 "0" 0 "0" 0>
  <GND * 1 70 650 0 0 0 0>
  <GND * 1 360 930 0 0 0 0>
  <Lib cap_cmim1 1 360 610 30 -26 0 0 "$HOME/.qucs/user_lib/IHP_PDK_basic_components" 0 "cap_cmim" 0 "70u" 1 "70u" 1>
  <Lib rhigh4 1 250 780 -16 -113 0 1 "$HOME/.qucs/user_lib/IHP_PDK_basic_components" 0 "rhigh" 0 "1.0u" 1 "1.0u" 1 "1" 1>
  <GND * 1 280 930 0 0 0 0>
  <Lib cap_rfcmim1 1 360 870 30 -26 0 0 "$HOME/.qucs/user_lib/IHP_PDK_basic_components" 0 "cap_rfcmim" 0 "70u" 1 "70u" 1>
  <GND * 1 250 530 0 0 0 0>
  <GND * 1 250 810 0 0 0 0>
  <Lib rhigh3 1 250 500 -16 -113 0 1 "$HOME/.qucs/user_lib/IHP_PDK_basic_components" 0 "rhigh" 0 "1.0u" 1 "2.0u" 1 "1" 1>
  <SpiceLib SpiceLib1 1 90 60 -13 18 0 0 "cornerRES.lib" 1 "res_typ" 1>
  <SpiceLib SpiceLib2 1 280 60 -13 18 0 0 "cornerCAP.lib" 1 "cap_typ" 1>
</Components>
<Wires>
  <70 600 70 650 "" 0 0 0 "">
  <70 500 70 540 "" 0 0 0 "">
  <70 500 150 500 "" 0 0 0 "">
  <360 640 360 650 "" 0 0 0 "">
  <360 500 360 580 "" 0 0 0 "">
  <280 500 360 500 "" 0 0 0 "">
  <150 500 220 500 "" 0 0 0 "">
  <150 500 150 780 "" 0 0 0 "">
  <150 780 220 780 "" 0 0 0 "">
  <360 900 360 930 "" 0 0 0 "">
  <280 780 360 780 "" 0 0 0 "">
  <360 780 360 840 "" 0 0 0 "">
  <280 870 330 870 "" 0 0 0 "">
  <280 870 280 930 "" 0 0 0 "">
  <360 500 360 500 "Vout" 390 470 0 "">
  <360 780 360 780 "Vout2" 390 750 0 "">
</Wires>
<Diagrams>
  <Rect 550 872 871 717 3 #c0c0c0 1 11 0 100000 1 3e+11 1 0.0001 1 1 1 -1 0.2 1 315 0 225 1 0 0 "" "" "">
	<"ngspice/ac.v(vout)" #0000ff 2 3 0 0 0>
	<"ngspice/ac.v(vout2)" #ff0000 2 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
