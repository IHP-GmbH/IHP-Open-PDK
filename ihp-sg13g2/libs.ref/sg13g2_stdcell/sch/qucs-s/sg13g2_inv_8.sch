<Qucs Schematic 25.2.0>
<Properties>
  <View=-677,-635,3248,1648,0.679709,337,353>
  <Grid=5,5,1>
  <DataSet=sg13g2_inv_8.dat>
  <DataDisplay=sg13g2_inv_8.dpl>
  <OpenDisplay=0>
  <Script=sg13g2_inv_8.m>
  <RunScript=0>
  <showFrame=3>
  <FrameText0=Title: sg13g2_inv_8>
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
  <Port Y 1 850 505 -23 12 0 2 "1" 1 "out" 0>
  <Port A 1 740 505 -23 12 0 0 "2" 1 "in" 0>
  <Port VDD 1 644 155 -23 12 0 0 "3" 1 "inout" 0>
  <Port VSS 1 644 845 -23 12 0 0 "4" 1 "inout" 0>
  <pmos M2 1 810 235 -26 34 0 0 "sg13_lv_pmos" 0 "X" 0 "pmos" 0 "8.96u" 1 "130.00n" 1 "8" 1 "1" 1>
  <nmos M1 1 810 765 -26 34 0 0 "sg13_lv_nmos" 0 "X" 0 "nmos" 0 "5.92u" 1 "130.00n" 1 "8" 1 "1" 1>
</Components>
<Wires>
  <780 235 780 505 "" 0 0 0 "">
  <810 230 880 230 "" 0 0 0 "">
  <644 155 810 155 "" 0 0 0 "">
  <810 155 880 155 "" 0 0 0 "">
  <644 845 810 845 "" 0 0 0 "">
  <880 155 880 230 "" 0 0 0 "">
  <810 155 810 205 "" 0 0 0 "">
  <810 505 810 735 "" 0 0 0 "">
  <740 505 780 505 "" 0 0 0 "">
  <780 505 780 765 "" 0 0 0 "">
  <810 265 810 505 "" 0 0 0 "">
  <810 770 880 770 "" 0 0 0 "">
  <810 505 850 505 "" 0 0 0 "">
  <810 845 880 845 "" 0 0 0 "">
  <880 770 880 845 "" 0 0 0 "">
  <810 795 810 845 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
