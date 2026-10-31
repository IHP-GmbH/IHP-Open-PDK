<Qucs Schematic 25.2.0>
<Properties>
  <View=392,247,1126,793,0.849817,0,0>
  <Grid=5,5,1>
  <DataSet=sg13g2_hv_tielo.dat>
  <DataDisplay=sg13g2_hv_tielo.dpl>
  <OpenDisplay=0>
  <Script=sg13g2_hv_tielo.m>
  <RunScript=0>
  <showFrame=3>
  <FrameText0=Title: sg13g2_hv_tielo>
  <FrameText1=Drawn By: ChipDesign B.V.>
  <FrameText2=Date: August 2026>
  <FrameText3=Revision: 1.0>
</Properties>
<Symbol>
  <.PortSym 0 0 1 0 L_LO>
  <Text 5 -3 10 #800000 0 "L-LO">
  <Line -10 10 20 0 #000080 2 1>
  <Line 0 0 0 10 #000080 2 1>
  <Line -6 13 13 0 #000080 2 1>
  <Line -2 16 5 0 #000080 2 1>
  <.ID -5 25 TIELO>
  <.PortSym -20 -35 2 0 VDD>
  <.PortSym -20 45 3 0 VSS>
</Symbol>
<Components>
  <Port L_LO 1 845 500 -23 12 0 2 "1" 1 "out" 0>
  <Port VDD 1 679 250 -23 12 0 0 "2" 1 "inout" 0>
  <Port VSS 1 679 750 -23 12 0 0 "3" 1 "inout" 0>
  <pmos M2 1 805 300 -26 34 0 0 "sg13_hv_pmos" 0 "X" 0 "pmos" 0 "2.690u" 1 "450.00n" 1 "1" 1 "1" 1>
  <nmos M1 1 805 700 -26 34 0 0 "sg13_hv_nmos" 0 "X" 0 "nmos" 0 "740.00n" 1 "450.00n" 1 "1" 1 "1" 1>
</Components>
<Wires>
  <805 730 805 750 "" 0 0 0 "">
  <805 500 845 500 "" 0 0 0 "">
  <805 500 805 670 "" 0 0 0 "">
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
  <775 250 775 300 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
