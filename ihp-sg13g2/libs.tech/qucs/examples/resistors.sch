<Qucs Schematic 24.2.0>
<Properties>
  <View=-288,-4,1765,1119,1.04363,0,0>
  <Grid=10,10,1>
  <DataSet=resistors.dat>
  <DataDisplay=resistors.dpl>
  <OpenDisplay=0>
  <Script=resistors.m>
  <RunScript=0>
  <showFrame=3>
  <FrameText0=DC simulation resistors>
  <FrameText1=Drawn By:IHP PDK Authors>
  <FrameText2=Date:2024>
  <FrameText3=Revision:1>
</Properties>
<Symbol>
  <.ID -20 -16 SUB>
  <Line -20 20 40 0 #000080 2 1>
  <Line 20 20 0 -40 #000080 2 1>
  <Line -20 -20 40 0 #000080 2 1>
  <Line -20 20 0 -40 #000080 2 1>
</Symbol>
<Components>
  <.SW SW1 1 90 280 0 68 0 0 "DC1" 1 "lin" 1 "V2" 1 "0" 1 "10" 1 "301" 1 "false" 0>
  <INCLSCR INCLSCR1 1 130 50 -60 16 0 0 ".LIB ~/.qucs/IHP-Open-PDK-main/ihp-sg13g2/libs.tech/ngspice/models/cornerRES.lib res_wcs\n.control\nop\n.endc" 1 "" 0 "" 0>
  <Vdc V2 1 110 800 18 -26 0 1 "1 V" 1>
  <GND * 1 250 950 0 0 0 0>
  <GND * 1 110 950 0 0 0 0>
  <IProbe Pr1 1 180 690 -26 16 0 0>
  <GND * 1 420 950 0 0 0 0>
  <Lib rppd2 1 580 1060 -110 -196 0 0 "/home/herman/.qucs/user_lib/IHP_PDK_basic_components" 0 "rppd" 0 "10u" 1 "25u" 1 "2" 1>
  <Lib rsil3 1 250 750 50 -26 0 0 "/home/herman/.qucs/user_lib/IHP_PDK_basic_components" 0 "rsil" 0 "10u" 1 "40u" 1 "1" 1>
  <Lib rppd1 1 580 920 -110 -196 0 0 "/home/herman/.qucs/user_lib/IHP_PDK_basic_components" 0 "rppd" 0 "10u" 1 "25u" 1 "1" 1>
  <Lib rsil2 1 250 890 50 -26 0 0 "/home/herman/.qucs/user_lib/IHP_PDK_basic_components" 0 "rsil" 0 "10u" 1 "40u" 1 "1" 1>
  <GND * 1 610 950 0 0 0 0>
  <Lib rhigh1 1 610 760 50 -26 0 0 "/home/herman/.qucs/user_lib/IHP_PDK_basic_components" 0 "rhigh" 0 "10u" 1 "30u" 1 "1" 1>
  <Lib rhigh2 1 610 890 50 -26 0 0 "/home/herman/.qucs/user_lib/IHP_PDK_basic_components" 0 "rhigh" 0 "10u" 1 "50u" 1 "1" 1>
  <Lib ntap1 1 890 880 50 -26 0 0 "/home/herman/.qucs/user_lib/IHP_PDK_basic_components" 0 "ntap1" 0>
  <GND * 1 890 920 0 0 0 0>
  <GND * 1 790 920 0 0 0 0>
  <Lib ptap1 1 1120 880 50 -26 0 0 "/home/herman/.qucs/user_lib/IHP_PDK_basic_components" 0 "ptap1" 0>
  <GND * 1 1120 920 0 0 0 0>
  <GND * 1 1040 920 0 0 0 0>
  <Idc I1 1 790 890 18 -26 0 1 "1 mA" 1>
  <Idc I2 1 1040 890 18 -26 0 1 "1 mA" 1>
  <.DC DC1 1 90 180 0 41 0 0 "26.85" 0 "0.001" 0 "1 pA" 0 "1 uV" 0 "yes" 1 "150" 0 "no" 0 "none" 0 "CroutLU" 0>
</Components>
<Wires>
  <110 830 110 950 "" 0 0 0 "">
  <210 690 250 690 "" 0 0 0 "">
  <110 690 150 690 "" 0 0 0 "">
  <110 690 110 770 "" 0 0 0 "">
  <420 930 420 950 "" 0 0 0 "">
  <250 690 250 710 "" 0 0 0 "">
  <420 790 420 850 "div2" 440 810 21 "">
  <250 690 420 690 "" 0 0 0 "">
  <420 690 420 710 "" 0 0 0 "">
  <250 930 250 950 "" 0 0 0 "">
  <250 790 250 850 "div1" 270 810 35 "">
  <420 690 610 690 "" 0 0 0 "">
  <610 690 610 720 "" 0 0 0 "">
  <610 800 610 850 "div3" 650 810 24 "">
  <610 930 610 950 "" 0 0 0 "">
  <790 820 790 860 "" 0 0 0 "">
  <790 820 890 820 "ntap" 880 790 56 "">
  <890 820 890 840 "" 0 0 0 "">
  <1040 820 1040 860 "" 0 0 0 "">
  <1040 820 1120 820 "ptap" 1100 790 28 "">
  <1120 820 1120 840 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 553 615 857 473 3 #c0c0c0 1 00 1 0 0.5 10 1 -0.622632 1 7 1 0 0.1 0.525694 315 0 225 1 0 0 "" "" "">
	<"ngspice/v(div2)" #ff0000 2 3 0 0 0>
	  <Mkr 5.01661 503 -225 3 0 0>
	<"ngspice/i(pr1)" #ff0000 2 3 0 0 0>
	<"ngspice/v(div1)" #ff00ff 2 3 0 0 0>
	<"ngspice/v(div3)" #00ff00 2 3 0 0 0>
	<"ngspice/v(ntap)" #00ffff 3 3 0 0 1>
	<"ngspice/v(ptap)" #ffff00 2 3 0 0 1>
  </Rect>
</Diagrams>
<Paintings>
</Paintings>
