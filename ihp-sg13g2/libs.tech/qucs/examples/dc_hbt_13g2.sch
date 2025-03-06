<Qucs Schematic 24.3.0>
<Properties>
  <View=-82,44,1615,1026,0.924644,0,0>
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
  <.SW SW1 1 50 250 0 71 0 0 "DC1" 1 "lin" 1 "V2" 1 "0" 1 "1.5" 1 "301" 1>
  <.SW SW2 1 50 470 0 71 0 0 "SW1" 1 "lin" 1 "I1" 1 "0" 1 "5u" 1 "10" 1>
  <IProbe Pr1 1 170 740 -37 -26 0 3>
  <Vdc V2 1 290 770 18 -26 0 1 "1 V" 1>
  <GND * 1 170 960 0 0 0 0>
  <GND * 1 230 960 0 0 0 0>
  <GND * 1 290 960 0 0 0 0>
  <GND * 1 70 960 0 0 0 0>
  <Idc I1 1 70 910 18 -26 0 1 "0" 1>
  <INCLSCR INCLSCR1 1 100 100 -60 16 0 0 ".LIB cornerHBT.lib hbt_typ\n" 1 "" 0 "" 0>
  <Vdc V3 1 170 920 18 -26 0 1 "0" 1>
  <Lib npn13G1 1 170 850 10 15 0 0 "$HOME/.qucs/user_lib/IHP_PDK_nonlinear_components" 0 "npn13G2" 0 "1" 1>
</Components>
<Wires>
  <170 690 170 710 "" 0 0 0 "">
  <170 690 290 690 "" 0 0 0 "">
  <290 690 290 740 "" 0 0 0 "">
  <290 800 290 960 "" 0 0 0 "">
  <70 940 70 960 "" 0 0 0 "">
  <70 850 70 880 "" 0 0 0 "">
  <70 850 140 850 "base" 130 820 32 "">
  <230 850 230 960 "" 0 0 0 "">
  <170 770 170 820 "col" 200 770 33 "">
  <180 850 230 850 "" 0 0 0 "">
  <170 950 170 960 "" 0 0 0 "">
  <170 880 170 890 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 437 899 1062 769 3 #c0c0c0 1 00 1 0 0.1 1.5 1 -0.000277029 0.0002 0.00246701 1 -1 0.2 1 315 0 225 1 0 0 "" "" "">
	<"ngspice/i(pr1)" #ff0000 0 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
