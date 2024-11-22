// sch_path: /home/prabhat.dubey/OPEN_Source_IHP_PDK/IHP-Open-PDK/ihp-sg13g2/libs.tech/xschem/sg13g2_tests/tran_logic_not.sch
module tran_logic_not
(

);
wire out ;
wire in ;
wire net1 ;
wire GND ;

vsource
#(
.value ( "dc )
)
Vin ( 
 .p( in ),
 .m( GND )
);


vsource
#(
.value ( 1.2 )
)
Vdd ( 
 .p( net1 ),
 .m( GND )
);


sg13_lv_nmos
#(
.l ( 4.5e-07 ) ,
.w ( 1e-06 ) ,
.ng ( 1 ) ,
.m ( 1 ) ,
.model ( sg13_lv_nmos ) ,
.spiceprefix ( X )
)
M1 ( 
 .D( out ),
 .G( in ),
 .S( GND ),
 .B( GND )
);


sg13_lv_pmos
#(
.l ( 4.5e-07 ) ,
.w ( 1e-06 ) ,
.ng ( 1 ) ,
.m ( 1 ) ,
.model ( sg13_lv_pmos ) ,
.spiceprefix ( X )
)
M2 ( 
 .D( out ),
 .G( in ),
 .S( net1 ),
 .B( net1 )
);


.lib cornerMOSlv.lib mos_tt


.param temp=27
.control
save all 
tran 50p 20n
meas tran tdelay TRIG v(in) VAl=0.9 FALl=1 TARG v(out) VAl=0.9 RISE=1
write tran_logic_not.raw
.endc

endmodule
