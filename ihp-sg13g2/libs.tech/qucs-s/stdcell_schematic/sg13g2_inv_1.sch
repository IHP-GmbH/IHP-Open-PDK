<Qucs Schematic 25.2.0>
<Properties>
  <View=-612,-270,3298,2004,0.563928,0,4>
  <Grid=5,5,1>
  <DataSet=sg13g2_inv_1.dat>
  <DataDisplay=sg13g2_inv_1.dpl>
  <OpenDisplay=0>
  <Script=sg13g2_inv_1.m>
  <RunScript=0>
  <showFrame=3>
  <FrameText0=Title: sg13g2_inv_1>
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
  <Port Y 1 845 500 -23 12 0 2 "1" 1 "out" 0>
  <Port A 1 715 500 -23 12 0 0 "2" 1 "in" 0>
  <Port VDD 1 679 250 -23 12 0 0 "3" 1 "inout" 0>
  <Port VSS 1 679 750 -23 12 0 0 "4" 1 "inout" 0>
  <pmos M2 1 805 300 -26 34 0 0 "sg13_lv_pmos" 0 "X" 0 "pmos" 0 "1.12u" 1 "130.00n" 1 "1" 1 "1" 1>
  <nmos M1 1 805 700 -26 34 0 0 "sg13_lv_nmos" 0 "X" 0 "nmos" 0 "740.00n" 1 "130.00n" 1 "1" 1 "1" 1>
</Components>
<Wires>
  <805 730 805 750 "" 0 0 0 "">
  <805 500 845 500 "" 0 0 0 "">
  <805 500 805 670 "" 0 0 0 "">
  <715 500 775 500 "" 0 0 0 "">
  <775 500 775 700 "" 0 0 0 "">
  <805 295 825 295 "" 0 0 0 "">
  <805 250 805 270 "" 0 0 0 "">
  <775 300 775 500 "" 0 0 0 "">
  <805 330 805 500 "" 0 0 0 "">
  <805 250 825 250 "" 0 0 0 "">
  <825 250 825 295 "" 0 0 0 "">
  <805 705 825 705 "" 0 0 0 "">
  <679 250 805 250 "" 0 0 0 "">
  <825 705 825 750 "" 0 0 0 "">
  <679 750 805 750 "" 0 0 0 "">
  <805 750 825 750 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
