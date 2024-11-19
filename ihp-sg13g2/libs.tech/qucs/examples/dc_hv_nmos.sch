<Qucs Schematic 24.2.0>
<Properties>
  <View=-39,-4,1577,932,0.971123,0,1>
  <Grid=10,10,1>
  <DataSet=dc_hv_nmos.dat>
  <DataDisplay=dc_hv_nmos.dpl>
  <OpenDisplay=0>
  <Script=dc_hv_nmos.m>
  <RunScript=0>
  <showFrame=3>
  <FrameText0=DC simulation of a High Voltage  N type MOS>
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
  <INCLSCR INCLSCR1 1 130 50 -60 16 0 0 "\n.LIB cornerMOShv.lib mos_tt\n" 1 "" 0 "" 0>
  <.DC DC1 1 90 180 0 41 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <.SW SW2 1 260 280 0 68 0 0 "SW1" 1 "lin" 1 "V1" 1 "0" 1 "0.9" 1 "10" 1 "false" 0>
  <Lib sg13_hv_nmos1 1 270 750 55 -121 0 0 "<userhome>/<qucs_workspace>/user_lib/IHP_PDK_nonlinear_components" 0 "sg13_hv_nmos" 0 "1.0u" 1 "0.45u" 1 "1" 1 "1" 1 "0" 0 "0" 0 "0" 0 "0" 0 "0" 0 "0.346e-6" 0 "0.38e-6" 0 "0.15e-6" 0 "0" 0 "1" 0>
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
  <Rect 639 890 831 618 3 #c0c0c0 1 00 1 -1 0.2 1 1 -1 0.2 1 1 -1 0.2 1 315 0 225 1 0 0 "" "" "">
	<"ngspice/sw1.i(pr1)" #ff0000 0 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
