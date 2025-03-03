<Qucs Schematic 24.2.0>
<Properties>
  <View=12,36,1515,906,1.04368,0,0>
  <Grid=10,10,1>
  <DataSet=dc_lv_nmos.dat>
  <DataDisplay=dc_lv_nmos.dpl>
  <OpenDisplay=0>
  <Script=dc_lv_nmos.m>
  <RunScript=0>
  <showFrame=3>
  <FrameText0=DC simulation of a Low Voltage  N type MOS>
  <FrameText1=Drawn By:IHP PDK Authors>
  <FrameText2=Date:2024>
  <FrameText3=Revision:1>
</Properties>
<Symbol>
</Symbol>
<Components>
  <.SW SW1 1 90 280 0 68 0 0 "DC1" 1 "lin" 1 "V2" 1 "0" 1 "3" 1 "301" 1 "false" 0>
  <GND * 1 270 840 0 0 0 0>
  <GND * 1 330 840 0 0 0 0>
  <IProbe Pr1 1 270 640 -37 -26 0 3>
  <Vdc V2 1 450 750 18 -26 0 1 "1 V" 1>
  <GND * 1 450 840 0 0 0 0>
  <Vdc V1 1 160 800 18 -26 0 1 "1 V" 1>
  <GND * 1 160 840 0 0 0 0>
  <.SW SW2 1 260 280 0 68 0 0 "SW1" 1 "lin" 1 "V1" 1 "0" 1 "0.9" 1 "10" 1 "false" 0>
  <Lib sg13_lv_nmos1 1 270 750 55 -121 0 0 "<userhome>/<qucs_workspace>/user_lib/IHP_PDK_nonlinear_components" 0 "sg13_lv_nmos" 0 "0.35u" 1 "0.34u" 1 "1" 1 "1" 1 "0" 0 "0" 0 "0" 0 "0" 0 "0" 0 "0.346e-6" 0 "0.38e-6" 0 "0.15e-6" 0 "0" 0 "1" 0>
  <INCLSCR INCLSCR1 1 120 90 -60 16 0 0 ".LIB cornerMOSlv.lib mos_tt\n" 1 "" 0 "" 0>
</Components>
<Wires>
  <270 810 270 840 "" 0 0 0 "">
  <280 750 330 750 "" 0 0 0 "">
  <330 750 330 840 "" 0 0 0 "">
  <270 670 270 700 "" 0 0 0 "">
  <270 590 270 610 "" 0 0 0 "">
  <270 590 450 590 "" 0 0 0 "">
  <450 590 450 720 "" 0 0 0 "">
  <450 780 450 840 "" 0 0 0 "">
  <160 750 220 750 "" 0 0 0 "">
  <160 750 160 770 "" 0 0 0 "">
  <160 830 160 840 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 602 852 868 643 3 #c0c0c0 1 00 1 0 0.5 10 1 -0.1 0.1 1 1 -1 0.2 1 315 0 225 1 0 0 "" "" "">
	<"ngspice/i(pr1)" #ff00ff 0 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
