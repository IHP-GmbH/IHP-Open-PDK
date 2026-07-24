<Qucs Schematic 24.4.1>
<Properties>
  <View=-60,-60,960,560,1,0,0>
  <Grid=10,10,1>
  <DataSet=ac_mom_cap.dat>
  <DataDisplay=ac_mom_cap.dpl>
  <OpenDisplay=0>
  <Script=ac_mom_cap.m>
  <RunScript=0>
  <showFrame=3>
  <FrameText0=AC MoM capacitor (cap_cmom) -3dB extraction>
  <FrameText1=Drawn By: IHP PDK Authors>
  <FrameText2=Date:2026>
  <FrameText3=Revision:1>
</Properties>
<Symbol>
</Symbol>
<Components>
  <Vac V1 1 100 200 18 -26 0 0 "1 V" 1 "1 kHz" 0 "0" 0 "0" 0 "0" 0 "0" 0>
  <cmom C1 1 300 200 20 -40 0 0 "cap_cmom" 0 "X" 0 "10.0" 1 "70.0" 1 "1" 1 "5" 1 "double" 1 "0" 0 "1" 1 "m*((mmax-mmin+1<=2)?0.55:((mmax-mmin+1==3)?0.82:((mmax-mmin+1==4)?1.09:1.36)))*(max(1,rint(l*1e6/0.84+1e-6-0.5))*0.84)*(max(1,rint(w*1e6/0.89+1e-6-0.5)-1)*0.89)*1e-15" 1 "1" 0 "cap_cmom" 0>
  <R R1 1 500 200 -26 15 0 0 "100k" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <GND * 1 70 270 0 0 0 0>
  <GND * 1 530 270 0 0 0 0>
  <SpiceLib SpiceLib1 1 120 60 -13 18 0 0 "cornerCAP.lib" 1 "cap_typ" 1>
  <.CUSTOMSIM CUSTOM1 1 360 60 0 27 0 0 "ac dec 1000 1e6 1e9\nlet mag=abs(out)\nmeas ac freq_at when mag = 0.707\nlet C = 1/(2*PI*freq_at*1e+5)\nprint C\n" 1 "out;C" 0 "" 0>
</Components>
<Wires>
  <130 200 270 200 "in" 180 170 0 "">
  <330 200 470 200 "out" 380 170 0 "">
  <70 200 70 270 "" 0 0 0 "">
  <530 200 530 270 "" 0 0 0 "">
</Wires>
<Diagrams>
</Diagrams>
<Paintings>
  <Text 60 330 12 #000000 0 "High-pass RC. C is extracted from the -3dB corner: C = 1/(2*pi*f_3dB*R), R = 100k.\ncap_cmom 10x70 (M1..M5, feed=double) -> C ~ 818.5 fF.\nSame method and result as the xschem testcase sg13g2_tests/ac_cap_cmom.">
</Paintings>
