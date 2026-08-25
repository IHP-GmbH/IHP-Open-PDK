<Qucs Schematic 25.2.0>
<Properties>
  <View=262,332,1055,793,1.90022,0,0>
  <Grid=5,5,1>
  <DataSet=sg13g2_antennanp.dat>
  <DataDisplay=sg13g2_antennanp.dpl>
  <OpenDisplay=0>
  <Script=sg13g2_antennanp.m>
  <RunScript=0>
  <showFrame=3>
  <FrameText0=Title: sg13g2_antennanp>
  <FrameText1=Drawn By: IHP PDK AUTHORS>
  <FrameText2=Date: April 2026>
  <FrameText3=Revision: 1.0>
</Properties>
<Symbol>
  <.PortSym -30 -10 1 0 A>
  <Text -30 -7 10 #800000 0 "A">
  <Line -30 -10 25 0 #000080 2 1>
  <Line 40 5 -45 0 #000080 2 1>
  <Line 40 -25 -45 0 #000080 2 1>
  <Line 40 -25 0 30 #000080 2 1>
  <Line -5 5 0 -30 #000080 2 1>
  <Line 30 -10 -10 0 #000080 2 1>
  <Line 5 -10 -10 0 #000080 2 1>
  <Line 20 -17 0 14 #000080 2 1>
  <Line 20 -10 -15 -7 #000080 2 1>
  <Line 20 -10 -15 7 #000080 2 1>
  <Line 5 -3 0 -14 #000080 2 1>
  <.ID 5 15 ANTENNA>
  <.PortSym -5 -45 2 0 VDD>
  <.PortSym -5 25 3 0 VSS>
</Symbol>
<Components>
  <Port A 1 655 500 -23 12 0 0 "1" 1 "in" 0>
  <Port VDD 1 575 380 -23 12 0 0 "2" 1 "inout" 0>
  <Port VSS 1 695 710 -60 7 1 1 "3" 1 "inout" 0>
  <D_IHP D3 1 695 440 13 -26 0 1 "dpantenna" 0 "X" 0 "1.05" 1 "1.34" 1 "1" 0>
  <D_IHP D2 1 695 590 13 -26 0 1 "dantenna" 0 "X" 0 ".780" 1 ".780" 1 "1" 0>
</Components>
<Wires>
  <655 500 695 500 "" 0 0 0 "">
  <695 500 695 560 "" 0 0 0 "">
  <695 380 695 410 "" 0 0 0 "">
  <695 470 695 500 "" 0 0 0 "">
  <575 380 695 380 "" 0 0 0 "">
  <695 620 695 710 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
</Paintings>
