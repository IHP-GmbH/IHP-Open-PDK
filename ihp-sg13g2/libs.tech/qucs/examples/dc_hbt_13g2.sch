<Qucs Schematic 24.2.0>
<Properties>
  <View=26,-124,1281,548,1.18486,0,0>
  <Grid=10,10,1>
  <DataSet=dc_hbt_13g2.dat>
  <DataDisplay=dc_hbt_13g2.dpl>
  <OpenDisplay=0>
  <Script=dc_hbt_13g2.m>
  <RunScript=0>
  <showFrame=0>
  <FrameText0=Title>
  <FrameText1=Drawn By:>
  <FrameText2=Date:>
  <FrameText3=Revision:>
</Properties>
<Symbol>
</Symbol>
<Components>
  <GND * 1 730 310 0 0 0 0>
  <GND * 1 440 310 0 0 0 0>
  <.DC DC1 1 90 190 0 41 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <INCLSCR INCLSCR2 1 130 -40 -60 16 0 0 ".LIB ../../.qucs/IHP-Open-PDK-main/ihp-sg13g2/libs.tech/ngspice/models/cornerHBT.lib hbt_typ\n.control\n\n.endc" 1 "" 0 "" 0>
  <Vdc V2 1 730 220 18 -26 0 1 "1 V" 1>
  <Idc I1 1 440 270 18 -26 0 1 "1 mA" 1>
  <.SW SW2 1 240 280 0 68 0 0 "SW1" 1 "lin" 1 "I1" 1 "0" 1 "5u" 1 "50" 1 "false" 0>
  <IProbe Pr1 1 550 110 -37 -26 0 3>
  <GND * 1 550 270 0 0 0 0>
  <GND * 1 610 270 0 0 0 0>
  <Lib npn13G1 1 560 170 10 64 0 0 "/home/herman/.qucs/user_lib/IHP_PDK_nonlinear_components" 0 "npn13G2" 0 "1" 1>
  <.SW SW1 1 90 280 0 68 0 0 "DC1" 1 "lin" 1 "V2" 1 "0" 1 "1.5" 1 "301" 1 "false" 0>
</Components>
<Wires>
  <550 60 550 80 "" 0 0 0 "">
  <550 60 730 60 "" 0 0 0 "">
  <730 60 730 190 "" 0 0 0 "">
  <730 250 730 310 "" 0 0 0 "">
  <440 300 440 310 "" 0 0 0 "">
  <550 140 550 170 "" 0 0 0 "">
  <550 250 550 270 "" 0 0 0 "">
  <570 210 610 210 "" 0 0 0 "">
  <610 210 610 270 "" 0 0 0 "">
  <440 210 530 210 "" 0 0 0 "">
  <440 210 440 240 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 859 335 381 285 3 #c0c0c0 1 00 1 0 0.2 1 1 -0.1 0.2 1.1 1 -0.1 0.2 1.1 315 0 225 1 0 0 "" "" "">
	<"ngspice/i(pr1)" #0000ff 0 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
