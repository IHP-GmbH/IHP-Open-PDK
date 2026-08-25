<Qucs Schematic 25.2.0>
<Properties>
  <View=-936,-648,3468,1750,0.73295,534,464>
  <Grid=5,5,1>
  <DataSet=sg13g2_inv_2.dat>
  <DataDisplay=sg13g2_inv_2.dpl>
  <OpenDisplay=0>
  <Script=sg13g2_inv_2.m>
  <RunScript=0>
  <showFrame=3>
  <FrameText0=Title: sg13g2_inv_2>
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
  <Port Y 1 855 475 -23 12 0 2 "1" 1 "out" 0>
  <Port A 1 705 475 -23 12 0 0 "2" 1 "in" 0>
  <Port VDD 1 665 185 -23 12 0 0 "3" 1 "inout" 0>
  <Port VSS 1 665 815 -23 12 0 0 "4" 1 "inout" 0>
  <pmos M2 1 785 235 -26 34 0 0 "sg13_lv_pmos" 0 "X" 0 "pmos" 0 "2.24u" 1 "130.00n" 1 "2" 1 "1" 1>
  <nmos M1 1 785 735 -26 34 0 0 "sg13_lv_nmos" 0 "X" 0 "nmos" 0 "1.48u" 1 "130.00n" 1 "2" 1 "1" 1>
</Components>
<Wires>
  <785 475 855 475 "" 0 0 0 "">
  <785 185 785 205 "" 0 0 0 "">
  <705 475 755 475 "" 0 0 0 "">
  <785 765 785 815 "" 0 0 0 "">
  <785 230 805 230 "" 0 0 0 "">
  <665 815 785 815 "" 0 0 0 "">
  <785 740 805 740 "" 0 0 0 "">
  <755 475 755 735 "" 0 0 0 "">
  <805 185 805 230 "" 0 0 0 "">
  <805 740 805 815 "" 0 0 0 "">
  <785 185 805 185 "" 0 0 0 "">
  <785 475 785 705 "" 0 0 0 "">
  <665 185 785 185 "" 0 0 0 "">
  <785 265 785 475 "" 0 0 0 "">
  <755 235 755 475 "" 0 0 0 "">
  <785 815 805 815 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
