<Qucs Schematic 25.1.2>
<Properties>
  <View=-150,-264,3002,1198,0.898321,25,221>
  <Grid=10,10,1>
  <DataSet=dc_isolbox.dat>
  <DataDisplay=dc_isolbox.dpl>
  <OpenDisplay=0>
  <Script=diode.m>
  <RunScript=0>
  <showFrame=3>
  <FrameText0=DC simulation of  ESD diodes>
  <FrameText1=Drawn By:IHP PDK Authors>
  <FrameText2=Date:2024>
  <FrameText3=Revision:1>
</Properties>
<Symbol>
</Symbol>
<Components>
  <INCLSCR INCLSCR1 1 130 50 -60 16 0 0 "\n.INCLUDE diodes.lib\n" 1 "" 0 "" 0>
  <Idc I1 1 120 750 18 -26 0 1 "1 mA" 1>
  <GND * 1 300 850 0 0 0 0>
  <.SW SW1 1 90 280 0 70 0 0 "DC1" 1 "lin" 1 "I1" 1 "-1m" 1 "1m" 1 "2001" 1>
  <.DC DC1 1 90 170 0 41 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <GND * 1 120 850 0 0 0 0>
  <Lib isolbox1 1 300 750 20 -60 0 0 "$HOME/<qucs_workspace>/user_lib/IHP_PDK_nonlinear_components" 0 "isolbox" 0 "{size}" 1 "{size}" 1>
  <SpicePar SpicePar1 1 310 170 -28 18 0 0 "size=3u" 1>
  <.SW SW2 1 270 280 0 70 0 0 "SW1" 1 "list" 1 "size" 1 "3u" 0 "300u" 0 "[3u;10u;100u;300u]" 0>
</Components>
<Wires>
  <120 600 120 720 "" 0 0 0 "">
  <120 600 300 600 "" 0 0 0 "">
  <300 600 300 660 "" 0 0 0 "">
  <300 780 300 850 "" 0 0 0 "">
  <240 720 300 720 "nwell_net" 200 790 13 "">
  <120 780 120 850 "" 0 0 0 "">
  <300 600 300 600 "isosub_net" 330 580 0 "">
</Wires>
<Diagrams>
  <Rect 517 686 906 484 3 #c0c0c0 1 00 1 -0.001 0.0001 0.001 1 -20 5 20 1 -1 0.2 1 315 0 225 1 0 0 "" "" "">
	<"ngspice/sw1.v(isosub_net)" #0000ff 2 3 0 0 0>
	<"ngspice/sw1.v(nwell_net)" #ff0000 0 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
