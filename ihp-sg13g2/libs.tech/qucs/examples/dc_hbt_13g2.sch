<Qucs Schematic 24.2.1>
<Properties>
  <View=-147,16,1678,1026,0.852475,0,0>
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
  <INCLSCR INCLSCR1 1 160 70 -60 16 0 0 ".LIB ~/.qucs/IHP-Open-PDK-main/ihp-sg13g2/libs.tech/ngspice/models/cornerHBT.lib hbt_typ\n" 1 "" 0 "" 0>
  <.DC DC1 1 40 160 0 46 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <.SW SW1 1 50 250 0 77 0 0 "DC1" 1 "lin" 1 "V2" 1 "0" 1 "1.5" 1 "301" 1 "false" 0>
  <.SW SW2 1 50 470 0 77 0 0 "SW1" 1 "lin" 1 "I1" 1 "0" 1 "5u" 1 "10" 1 "false" 0>
  <IProbe Pr1 1 170 740 -37 -26 0 3>
  <Vdc V2 1 290 770 18 -26 0 1 "1 V" 1>
  <GND * 1 170 960 0 0 0 0>
  <GND * 1 230 960 0 0 0 0>
  <GND * 1 290 960 0 0 0 0>
  <GND * 1 70 960 0 0 0 0>
  <Idc I1 1 70 910 18 -26 0 1 "0" 1>
  <Lib npn13G1 1 170 850 10 64 0 0 "/home/herman/.qucs/user_lib/IHP_PDK_nonlinear_components" 0 "npn13G2" 0 "1" 1>
</Components>
<Wires>
  <170 770 170 800 "" 0 0 0 "">
  <170 690 170 710 "" 0 0 0 "">
  <170 690 290 690 "" 0 0 0 "">
  <290 690 290 740 "" 0 0 0 "">
  <290 800 290 960 "" 0 0 0 "">
  <70 940 70 960 "" 0 0 0 "">
  <70 850 70 880 "" 0 0 0 "">
  <70 850 140 850 "" 0 0 0 "">
  <180 850 230 850 "" 0 0 0 "">
  <230 850 230 960 "" 0 0 0 "">
  <170 900 170 960 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 437 899 1062 769 3 #c0c0c0 1 00 1 -1 0.1 1 1 -1 0.2 1 1 -1 0.2 1 315 0 225 1 0 0 "" "" "">
	<"ngspice/sw1.i(pr1)" #ff0000 0 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
