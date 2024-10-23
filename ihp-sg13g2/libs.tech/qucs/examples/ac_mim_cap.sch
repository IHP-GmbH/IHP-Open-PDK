<Qucs Schematic 24.2.0>
<Properties>
  <View=52,-2,1670,973,1.22451,269,33>
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
  <INCLSCR INCLSCR1 1 120 50 -60 16 0 0 "\n.LIB cornerRES.lib res_typ\n.LIB cornerCAP.lib cap_typ\n" 1 "" 0 "" 0>
  <.AC AC1 1 70 190 0 40 0 0 "log" 1 "100k" 1 "300 GHz" 1 "101" 1 "no" 0>
  <GND * 1 360 650 0 0 0 0>
  <Vac V1 1 70 570 18 -26 0 1 "1 V" 1 "1 kHz" 0 "0" 0 "0" 0 "0" 0 "0" 0>
  <GND * 1 70 650 0 0 0 0>
  <GND * 1 360 930 0 0 0 0>
  <GND * 1 330 930 0 0 0 0>
  <Lib cap_rfcmim1 1 370 860 50 -16 0 0 "<userhome>/<qucs_workspace>/user_lib/IHP_PDK_basic_components" 0 "cap_rfcmim" 0 "70u" 1 "70u" 1>
  <Lib rhigh1 1 240 500 -26 -122 0 1 "<userhome>/<qucs_workspace>/user_lib/IHP_PDK_basic_components" 0 "rhigh" 0 "1.0u" 1 "10u" 1 "1" 1>
  <Lib rhigh2 1 240 780 -26 -122 0 1 "<userhome>/<qucs_workspace>/user_lib/IHP_PDK_basic_components" 0 "rhigh" 0 "1.0u" 1 "10u" 1 "1" 1>
  <Lib cap_cmim1 1 360 590 -120 -49 0 0 "<userhome>/<qucs_workspace>/user_lib/IHP_PDK_basic_components" 0 "cap_cmim" 0 "70u" 1 "70u" 1>
</Components>
<Wires>
  <360 610 360 650 "" 0 0 0 "">
  <360 500 360 570 "" 0 0 0 "">
  <280 500 360 500 "" 0 0 0 "">
  <70 600 70 650 "" 0 0 0 "">
  <70 500 70 540 "" 0 0 0 "">
  <70 500 150 500 "" 0 0 0 "">
  <150 500 200 500 "" 0 0 0 "">
  <150 500 150 780 "" 0 0 0 "">
  <150 780 200 780 "" 0 0 0 "">
  <360 780 360 850 "" 0 0 0 "">
  <280 780 360 780 "" 0 0 0 "">
  <330 880 330 930 "" 0 0 0 "">
  <360 880 360 930 "" 0 0 0 "">
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
