<Qucs Schematic 25.1.2>
<Properties>
  <View=-259,31,1305,797,0.585621,0,1>
  <Grid=10,10,1>
  <DataSet=dc_schottkydiode.dat>
  <DataDisplay=dc_schottkydiode.dpl>
  <OpenDisplay=0>
  <Script=dc_schottkydiode.m>
  <RunScript=0>
  <showFrame=1>
  <FrameText0=Schottky diode example>
  <FrameText1=Drawn By: IHP-Open-PDK Authors 2025>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
</Symbol>
<Components>
  <GND * 1 320 690 0 0 0 0>
  <Idc I1 1 80 600 18 -26 0 1 "1 mA" 1>
  <Lib schottky_nbl2 1 320 570 -37 45 0 0 "$HOME/<qucs_workspace>/user_lib/IHP_PDK_nonlinear_components" 0 "schottky_nbl1" 0 "{Nx}" 1 "1" 1>
  <Vdc V1 1 160 690 -26 18 0 0 "0 V" 1>
  <GND * 1 80 700 0 0 0 0>
  <.SW SW1 1 100 300 0 70 0 0 "DC1" 1 "lin" 1 "I1" 1 "-1m" 1 "1m" 1 "2001" 1>
  <.SW SW2 1 270 300 0 70 0 0 "SW1" 1 "lin" 1 "Nx" 1 "1" 0 "10" 0 "10" 0>
  <.DC DC1 1 100 220 0 41 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <SpiceLib SpiceLib1 1 120 120 -13 18 0 0 "cornerDIO.lib" 1 "dio_tt" 1>
  <SpicePar SpicePar1 1 330 120 -28 16 0 0 "Nx=1" 1>
</Components>
<Wires>
  <320 600 320 690 "" 0 0 0 "">
  <350 580 450 580 "" 0 0 0 "">
  <450 580 450 690 "" 0 0 0 "">
  <80 630 80 690 "" 0 0 0 "">
  <80 530 80 570 "" 0 0 0 "">
  <80 530 320 530 "vd" 270 500 157 "">
  <320 530 320 540 "" 0 0 0 "">
  <190 690 240 690 "" 0 0 0 "">
  <240 690 240 710 "" 0 0 0 "">
  <80 690 130 690 "" 0 0 0 "">
  <80 690 80 700 "" 0 0 0 "">
  <450 690 450 690 "sub!" 480 660 0 "">
  <240 710 240 710 "sub!" 240 730 0 "">
</Wires>
<Diagrams>
  <Rect 486 558 490 487 3 #c0c0c0 1 00 1 -1 0.1 1 1 -1 0.2 1 1 -1 0.2 1 315 0 225 1 0 0 "" "" "">
	<"ngspice/sw1.v(vd)" #ff0000 1 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
