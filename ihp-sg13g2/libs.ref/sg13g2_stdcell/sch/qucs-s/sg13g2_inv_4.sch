<Qucs Schematic 25.2.0>
<Properties>
  <View=-74,-144,3003,1510,0.640913,1,0>
  <Grid=5,5,1>
  <DataSet=sg13g2_inv_4.dat>
  <DataDisplay=sg13g2_inv_4.dpl>
  <OpenDisplay=0>
  <Script=sg13g2_inv_4.m>
  <RunScript=0>
  <showFrame=3>
  <FrameText0=Title: sg13g2_inv_4>
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
  <Port Y 1 840 470 -23 12 0 2 "1" 1 "out" 0>
  <Port A 1 750 470 -23 12 0 0 "2" 1 "in" 0>
  <Port VDD 1 644 130 -23 12 0 0 "3" 1 "inout" 0>
  <Port VSS 1 644 870 -23 12 0 0 "4" 1 "inout" 0>
  <pmos M1 1 810 240 -26 34 0 0 "sg13_lv_pmos" 0 "X" 0 "pmos" 0 "4.48u" 1 "130.00n" 1 "4" 1 "1" 1>
  <nmos M2 1 810 730 -26 34 0 0 "sg13_lv_nmos" 0 "X" 0 "nmos" 0 "2.96u" 1 "130.00n" 1 "4" 1 "1" 1>
</Components>
<Wires>
  <780 470 780 730 "" 0 0 0 "">
  <810 130 810 210 "" 0 0 0 "">
  <810 735 880 735 "" 0 0 0 "">
  <750 470 780 470 "" 0 0 0 "">
  <810 470 810 700 "" 0 0 0 "">
  <810 760 810 870 "" 0 0 0 "">
  <810 470 840 470 "" 0 0 0 "">
  <810 270 810 470 "" 0 0 0 "">
  <810 235 880 235 "" 0 0 0 "">
  <644 130 810 130 "" 0 0 0 "">
  <644 870 810 870 "" 0 0 0 "">
  <880 735 880 870 "" 0 0 0 "">
  <780 240 780 470 "" 0 0 0 "">
  <810 870 880 870 "" 0 0 0 "">
  <880 130 880 235 "" 0 0 0 "">
  <810 130 880 130 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
