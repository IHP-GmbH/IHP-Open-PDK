<Qucs Schematic 24.2.0>
<Properties>
  <View=-98,-4,1595,976,0.926531,0,0>
  <Grid=10,10,1>
  <DataSet=dc_hv_pmos.dat>
  <DataDisplay=dc_hv_pmos.dpl>
  <OpenDisplay=0>
  <Script=dc_hv_pmos.m>
  <RunScript=0>
  <showFrame=3>
  <FrameText0=Title DC simulation of a High Voltage P type MOS>
  <FrameText1=Drawn By: IHP PDK Authors>
  <FrameText2=Date:2024>
  <FrameText3=Revision:1>
</Properties>
<Symbol>
</Symbol>
<Components>
  <.DC DC1 1 90 190 0 41 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "no" 0 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
  <.SW SW2 1 240 280 0 68 0 0 "SW1" 1 "lin" 1 "V1" 1 "0" 1 "0.9" 1 "10" 1 "false" 0>
  <.SW SW1 1 90 280 0 68 0 0 "DC1" 1 "lin" 1 "V2" 1 "0" 1 "3" 1 "301" 1 "false" 0>
  <GND * 1 190 910 0 0 0 0>
  <GND * 1 250 910 0 0 0 0>
  <GND * 1 370 910 0 0 0 0>
  <GND * 1 80 910 0 0 0 0>
  <Vdc V2 1 370 820 -61 -26 0 3 "1 V" 1>
  <Vdc V1 1 80 870 -61 -26 0 3 "1 V" 1>
  <IProbe Pr1 1 190 710 16 -26 0 1>
  <INCLSCR INCLSCR1 1 130 50 -60 16 0 0 "\n.LIB cornerMOShv.lib mos_tt\n" 1 "" 0 "" 0>
  <Lib sg13_hv_pmos1 1 190 820 45 -101 0 0 "<userhome>/<qucs_workspace>/user_lib/IHP_PDK_nonlinear_components" 0 "sg13_hv_pmos" 0 "1.0u" 1 "0.45u" 1 "1" 0 "1" 1 "0" 0 "0" 0 "0" 0 "0" 0 "0" 0 "0.346e-6" 0 "0.38e-6" 0 "0.15e-6" 0 "0" 0 "1" 0>
</Components>
<Wires>
  <190 880 190 910 "" 0 0 0 "">
  <200 820 250 820 "" 0 0 0 "">
  <250 820 250 910 "" 0 0 0 "">
  <190 740 190 770 "" 0 0 0 "">
  <190 660 190 680 "" 0 0 0 "">
  <190 660 370 660 "" 0 0 0 "">
  <370 660 370 790 "" 0 0 0 "">
  <370 850 370 910 "" 0 0 0 "">
  <80 820 140 820 "" 0 0 0 "">
  <80 820 80 840 "" 0 0 0 "">
  <80 900 80 910 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 492 870 986 577 3 #c0c0c0 1 00 1 0 0.2 3 1 -5e-07 5e-07 4.34555e-06 1 -1 0.2 1 315 0 225 1 0 0 "" "" "">
	<"ngspice/sw1.i(pr1)" #ff0000 0 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
