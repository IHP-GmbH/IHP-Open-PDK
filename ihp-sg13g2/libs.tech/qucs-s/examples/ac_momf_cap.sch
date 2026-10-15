<Qucs Schematic 25.2.0>
<Properties>
  <View=-114,-61,2753,920,1.34875,0,12>
  <Grid=10,10,1>
  <DataSet=ac_momf_cap.dat>
  <DataDisplay=ac_momf_cap.dpl>
  <OpenDisplay=0>
  <Script=ac_momf_cap.m>
  <RunScript=0>
  <showFrame=3>
  <FrameText0=AC MoM fringe capacitor (cap_cmomf) -3dB extraction>
  <FrameText1=Drawn By: IHP PDK Authors>
  <FrameText2=Date:2026>
  <FrameText3=Revision:1>
</Properties>
<Symbol>
</Symbol>
<Components>
  <Vac V1 1 90 250 -57 33 0 1 "1 V" 1 "1 kHz" 0 "0" 0 "0" 0 "0" 0 "0" 0>
  <R R1 1 360 210 -26 15 0 0 "100k" 1 "26.85" 0 "0.0" 0 "0.0" 0 "26.85" 0 "US" 0>
  <GND * 1 90 320 0 0 0 0>
  <GND * 1 460 320 0 0 0 0>
  <SpiceLib SpiceLib1 1 90 70 -13 18 0 0 "cornerCAP.lib" 1 "cap_typ" 1>
  <.AC AC1 1 290 50 0 32 0 0 "log" 1 "1e4" 1 "1e10" 1 "1001" 1 "no" 0>
  <cmomf C1 1 220 210 -27 23 0 0 "cap_cmomf" 0 "X" 0 "10.0" 1 "70.0" 1 "1" 0 "5" 0 "0" 0 "1" 0 "m*(((mmin==1)?0.372:0.305)+max(0,mmax-mmin)*0.305)*(l*1e6)*(w*1e6)*1e-15" 1 "1" 0>
</Components>
<Wires>
  <460 210 460 320 "" 0 0 0 "">
  <90 280 90 320 "" 0 0 0 "">
  <90 210 90 220 "" 0 0 0 "">
  <90 210 190 210 "" 0 0 0 "">
  <390 210 460 210 "" 0 0 0 "">
  <250 210 330 210 "out" 280 180 0 "">
</Wires>
<Diagrams>
  <Rect 600 390 540 340 1 #c0c0c0 1 10 0 10000 1 1e+10 1 -0.093109 0.2 1.08783 1 -1 0.5 1 315 0 225 1 0 0 "" "" "">
	<"ngspice/ac.v(out)" #0000ff 2 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
  <Text 580 470 12 #000000 0 "High-pass RC: |v(out)| rises through the -3dB corner at f_3dB = 1/(2*pi*R*C), R = 100k.\ncap_cmomf 10x70 (M1..M5): f_3dB ~ 1.428 MHz -> C ~ 1114.7 fF.\nSame method and device as the xschem test sg13g2_tests/ac_cap_cmomf.">
</Paintings>
