<Qucs Schematic 25.2.0>
<Properties>
  <View=-178,-139,2028,1144,0.683013,1,0>
  <Grid=5,5,1>
  <DataSet=sg13g2_inv_16.dat>
  <DataDisplay=sg13g2_inv_16.dpl>
  <OpenDisplay=0>
  <Script=sg13g2_inv_16.m>
  <RunScript=0>
  <showFrame=3>
  <FrameText0=Title: sg13g2_inv_16>
  <FrameText1=Drawn By: IHP PDK AUTHORS>
  <FrameText2=Date: April 2026>
  <FrameText3=Revision: 1.0>
</Properties>
<Symbol>
  <.PortSym 30 0 1 180 Y>
  <Text 28 3 10 #800000 0 "Y">
  <.PortSym -30 0 2 0 A>
  <Text -30 3 10 #800000 0 "A">
  <Line -15 0 -15 0 #000080 2 1>
  <Line -15 -15 25 15 #000080 2 1>
  <Line 10 0 -25 15 #000080 2 1>
  <Line -15 15 0 -30 #000080 2 1>
  <Line 30 0 -9 0 #000080 2 1>
  <EArc 10 5 10 -10 0 5760 #000080 2 1>
  <.ID 0 25 INV>
  <.PortSym -10 -40 3 0 VDD>
  <.PortSym -10 45 4 0 VSS>
</Symbol>
<Components>
  <Port Y 1 830 500 -23 12 0 2 "1" 1 "out" 0>
  <Port A 1 750 500 -23 12 0 0 "2" 1 "in" 0>
  <Port VDD 1 650 190 -23 12 0 0 "3" 1 "inout" 0>
  <Port VSS 1 664 810 -23 12 0 0 "4" 1 "inout" 0>
  <nmos M1 1 800 730 -26 34 0 0 "sg13_lv_nmos" 0 "X" 0 "nmos" 0 "11.84u" 1 "130.00n" 1 "16" 1 "1" 1>
  <pmos M2 1 800 260 -26 34 0 0 "sg13_lv_pmos" 0 "X" 0 "pmos" 0 "17.92u" 1 "130.00n" 1 "16" 1 "1" 1>
</Components>
<Wires>
  <750 500 770 500 "" 0 0 0 "">
  <800 500 800 700 "" 0 0 0 "">
  <770 500 770 730 "" 0 0 0 "">
  <800 500 830 500 "" 0 0 0 "">
  <800 760 800 810 "" 0 0 0 "">
  <664 810 800 810 "" 0 0 0 "">
  <800 290 800 500 "" 0 0 0 "">
  <870 735 870 810 "" 0 0 0 "">
  <800 190 870 190 "" 0 0 0 "">
  <800 190 800 230 "" 0 0 0 "">
  <770 260 770 500 "" 0 0 0 "">
  <800 735 870 735 "" 0 0 0 "">
  <650 190 800 190 "" 0 0 0 "">
  <870 190 870 255 "" 0 0 0 "">
  <800 810 870 810 "" 0 0 0 "">
  <800 255 870 255 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
