<Qucs Schematic 25.2.0>
<Properties>
  <View=16,32,1512,1067,1.52847,139,648>
  <Grid=10,10,1>
  <DataSet=tran_moscap_p.dat>
  <DataDisplay=tran_moscap_p.dpl>
  <OpenDisplay=0>
  <Script=tran_moscap_p.m>
  <RunScript=0>
  <showFrame=3>
  <FrameText0=DC simulation of a Low Voltage  N type MOS>
  <FrameText1=Drawn By:IHP PDK Authors>
  <FrameText2=Date:2024>
  <FrameText3=Revision:1>
</Properties>
<Symbol>
</Symbol>
<Components>
  <IProbe Pr1 1 380 560 -37 -26 0 3>
  <GND * 1 170 760 0 0 0 0>
  <GND * 1 380 830 0 0 0 0>
  <INCLSCR INCLSCR1 1 120 90 -60 16 0 0 ".LIB cornerMOSCAP.lib moscap_tt\n" 1 "" 0 "" 0>
  <S4Q_V V1 1 170 600 18 -26 0 1 "pwl(0 -1.2 400ns 1.2)" 1 "" 0 "" 0 "" 0 "" 0>
  <.CUSTOMSIM CUSTOM1 1 110 210 0 32 0 0 "     save all\n     tran 0.1n 400n\n     let Cn_abs = abs(i(vpr1)) / deriv(v(p))\n     meas tran C_max MAX Cn_abs\n     meas tran C_min MIN Cn_abs from=5n to=400n\n     meas tran t_c_min MIN_AT Cn_abs from=5n to=400n\n     meas tran V_th FIND v(p) AT=t_c_min\n     let Cn_norm = Cn_abs / C_max\n     write tran_moscap_n.raw" 1 "V(P);VPr1#branch;Cn_abs;Cn_norm" 0 "tran_moscap_n.raw" 0>
  <MC_P C1 1 380 640 -118 -12 0 3 "X" 0 "sg13_moscap_p" 0 "1.0" 1 "1.0" 1 "1" 1 "1" 0>
</Components>
<Wires>
  <380 590 380 640 "P" 410 590 25 "">
  <380 700 380 830 "" 0 0 0 "">
  <170 630 170 760 "" 0 0 0 "">
  <380 490 380 530 "" 0 0 0 "">
  <170 490 380 490 "" 0 0 0 "">
  <170 490 170 570 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 602 852 868 643 3 #c0c0c0 1 00 1 -1.2 0.2 1.2 1 -1.38788e-12 1e-12 1.26414e-11 1 -1 0.2 1 315 0 225 1 0 0 "" "" "">
	<"ngspice/tran.cn_abs@tran.v(p)" #0000ff 0 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
