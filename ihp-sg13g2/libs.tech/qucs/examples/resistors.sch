<Qucs Schematic 24.4.1>
<Properties>
  <View=-255,-70,2012,1279,0.723747,0,0>
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
  <INCLSCR INCLSCR1 1 130 50 -60 16 0 0 "\n.LIB cornerRES.lib res_wcs\n" 1 "" 0 "" 0>
  <.SW SW1 1 320 70 0 71 0 0 "DC1" 1 "lin" 1 "V2" 1 "0" 1 "10" 1 "301" 1>
  <Vdc V2 1 100 470 18 -26 0 1 "1 V" 1>
  <GND * 1 240 620 0 0 0 0>
  <GND * 1 100 620 0 0 0 0>
  <IProbe Pr1 1 170 360 -26 16 0 0>
  <GND * 1 410 620 0 0 0 0>
  <GND * 1 600 620 0 0 0 0>
  <Lib rsil2 1 240 550 25 -16 0 0 "$HOME/.qucs/user_lib/IHP_PDK_basic_components" 0 "rsil" 0 "10u" 1 "40u" 1 "1" 1>
  <Lib rppd1 1 410 410 25 -1 0 0 "$HOME/.qucs/user_lib/IHP_PDK_basic_components" 0 "rppd" 0 "10u" 1 "25u" 1 "1" 1>
  <Lib rhigh1 1 600 410 25 -16 0 0 "$HOME/.qucs/user_lib/IHP_PDK_basic_components" 0 "rhigh" 0 "10u" 1 "30u" 1 "1" 1>
  <Lib rppd2 1 410 550 25 -1 0 0 "$HOME/.qucs/user_lib/IHP_PDK_basic_components" 0 "rppd" 0 "10u" 1 "25u" 1 "1" 1>
  <GND * 1 970 750 0 0 0 0>
  <GND * 1 870 750 0 0 0 0>
  <GND * 1 1200 750 0 0 0 0>
  <GND * 1 1120 750 0 0 0 0>
  <Idc I1 1 870 720 18 -26 0 1 "1 mA" 1>
  <Idc I2 1 1120 720 18 -26 0 1 "1 mA" 1>
  <Lib ptap1 1 970 700 25 -16 0 0 "$HOME/.qucs/user_lib/IHP_PDK_basic_components" 0 "ptap1" 0 "0.78u" 1 "0.78u" 1>
  <Lib ntap1 1 1200 700 25 -16 0 0 "$HOME/.qucs/user_lib/IHP_PDK_basic_components" 0 "ntap1" 0 "0.78u" 1 "0.78u" 1>
  <Lib ptap4 1 180 730 25 -16 0 0 "$HOME/.qucs/user_lib/IHP_PDK_basic_components" 0 "ptap1" 0 "0.78u" 1 "0.78u" 1>
  <Lib ptap3 1 330 730 25 -16 0 0 "$HOME/.qucs/user_lib/IHP_PDK_basic_components" 0 "ptap1" 0 "0.78u" 1 "0.78u" 1>
  <Lib ptap2 1 510 730 25 -16 0 0 "$HOME/.qucs/user_lib/IHP_PDK_basic_components" 0 "ptap1" 0 "0.78u" 1 "0.78u" 1>
  <GND * 1 180 760 0 0 0 0>
  <GND * 1 510 760 0 0 0 0>
  <GND * 1 330 760 0 0 0 0>
  <Lib rhigh2 1 600 550 25 -16 0 0 "$HOME/.qucs/user_lib/IHP_PDK_basic_components" 0 "rhigh" 0 "10u" 1 "20u" 1 "1" 1>
  <Lib rsil1 1 240 410 25 -16 0 0 "$HOME/.qucs/user_lib/IHP_PDK_basic_components" 0 "rsil" 0 "10u" 1 "30u" 1 "1" 1>
</Components>
<Wires>
  <100 500 100 620 "" 0 0 0 "">
  <100 360 140 360 "" 0 0 0 "">
  <100 360 100 440 "" 0 0 0 "">
  <200 360 240 360 "" 0 0 0 "">
  <240 580 240 620 "" 0 0 0 "">
  <410 360 410 380 "" 0 0 0 "">
  <410 360 600 360 "" 0 0 0 "">
  <600 360 600 380 "" 0 0 0 "">
  <410 580 410 620 "" 0 0 0 "">
  <410 440 410 520 "div2" 430 480 80 "">
  <600 580 600 620 "" 0 0 0 "">
  <600 440 600 520 "div3" 640 480 80 "">
  <240 440 240 520 "div1" 260 480 80 "">
  <240 360 410 360 "" 0 0 0 "">
  <240 360 240 380 "" 0 0 0 "">
  <870 650 870 690 "" 0 0 0 "">
  <1120 650 1120 690 "" 0 0 0 "">
  <970 730 970 750 "" 0 0 0 "">
  <870 650 970 650 "ntap" 960 620 46 "">
  <970 650 970 670 "" 0 0 0 "">
  <1200 730 1200 750 "" 0 0 0 "">
  <1120 650 1200 650 "ptap" 1180 620 18 "">
  <1200 650 1200 670 "" 0 0 0 "">
  <180 410 210 410 "" 0 0 0 "">
  <180 410 180 550 "" 0 0 0 "">
  <180 550 180 700 "" 0 0 0 "">
  <180 550 210 550 "" 0 0 0 "">
  <330 410 380 410 "" 0 0 0 "">
  <330 410 330 550 "" 0 0 0 "">
  <330 550 330 700 "" 0 0 0 "">
  <330 550 380 550 "" 0 0 0 "">
  <510 410 570 410 "" 0 0 0 "">
  <510 410 510 550 "" 0 0 0 "">
  <510 550 510 700 "" 0 0 0 "">
  <510 550 570 550 "" 0 0 0 "">
</Wires>
<Diagrams>
  <Rect 679 431 791 379 3 #c0c0c0 1 00 1 0 1 10 1 -0.499996 1 5.49995 1 0 0.1 0.5256 315 0 225 1 0 0 "" "" "">
	<"ngspice/v(div2)" #ff0000 2 3 0 0 0>
	  <Mkr 5 437 -131 3 0 0>
	<"ngspice/v(div1)" #ff00ff 0 3 0 0 0>
	<"ngspice/v(div3)" #00ff00 2 3 0 0 0>
	<"ngspice/v(ntap)" #00ffff 3 3 0 0 1>
	<"ngspice/v(ptap)" #ffff00 2 3 0 0 1>
	<"ngspice/v(div2)" #ff00ff 0 3 0 0 0>
  </Rect>
</Diagrams>
<Paintings>
  <Text 60 810 12 #000000 0 "Bulk connections of the third terminal of the resistors are made with ptap1 devices\nUsually it should be connected to the lowest system potential (VSS)">
</Paintings>
