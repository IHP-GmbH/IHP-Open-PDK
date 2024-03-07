<Qucs Schematic 24.2.0>
<Properties>
  <View=-2465,-794,3507,1139,0.809276,1872,768>
  <Grid=10,10,1>
  <DataSet=dc_hbt_13g2.dat>
  <DataDisplay=dc_hbt_13g2.dpl>
  <OpenDisplay=0>
  <Script=dc_hbt_13g2.m>
  <RunScript=0>
  <showFrame=3>
  <FrameText0=HBT npn13G2 DC simulation>
  <FrameText1=Drawn By: IHP-PDK Authors>
  <FrameText2=Date: 2024>
  <FrameText3=Revision:1>
</Properties>
<Symbol>
</Symbol>
<Components>
  <INCLSCR INCLSCR1 1 160 70 -60 16 0 0 ".LIB ../../.qucs/IHP-Open-PDK-main/ihp-sg13g2/libs.tech/ngspice/models/cornerHBT.lib hbt_typ\n" 1 "" 0 "" 0>
  <.DC DC1 1 100 170 0 46 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <.SW SW1 1 110 260 0 77 0 0 "DC1" 1 "lin" 1 "V2" 1 "0" 1 "1.5" 1 "301" 1 "false" 0>
  <.SW SW2 1 110 480 0 77 0 0 "SW1" 1 "lin" 1 "I1" 1 "0" 1 "5u" 1 "10" 1 "false" 0>
  <IProbe Pr1 1 400 600 -37 -26 0 3>
  <GND * 1 400 760 0 0 0 0>
  <GND * 1 460 760 0 0 0 0>
  <Lib npn13G1 1 410 660 10 64 0 0 "/home/herman/.qucs/user_lib/IHP_PDK_nonlinear_components" 0 "npn13G2" 0 "1" 1>
  <Vdc V2 1 520 630 18 -26 0 1 "1 V" 1>
  <GND * 1 520 760 0 0 0 0>
  <Idc I1 1 330 730 18 -26 0 1 "0" 1>
  <GND * 1 330 760 0 0 0 0>
</Components>
<Wires>
  <400 630 400 660 "" 0 0 0 "">
  <400 740 400 760 "" 0 0 0 "">
  <420 700 460 700 "" 0 0 0 "">
  <460 700 460 760 "" 0 0 0 "">
  <400 550 400 570 "" 0 0 0 "">
  <400 550 520 550 "" 0 0 0 "">
  <520 550 520 600 "" 0 0 0 "">
  <520 660 520 760 "" 0 0 0 "">
  <330 700 380 700 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 669 860 810 550 3 #c0c0c0 1 00 1 0 0.1 1.5 1 -0.000277029 0.0002 0.00246701 1 -1 0.2 1 315 0 225 1 0 0 "" "" "">
	<"ngspice/i(pr1)" #0000ff 2 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
