// sch_path: /home/prabhat.dubey/OPEN_Source_IHP_PDK/IHP-Open-PDK/ihp-sg13g2/libs.tech/xschem/sg13g2_tests/tran_mim_cap.sch
module tran_mim_cap
(

);
wire REF ;
wire G2 ;
wire 0 ;
wire G ;

isource
#(
.value ( "pwl )
)
I1 ( 
 .p( 0 ),
 .m( G )
);

tran  R1 ( G ,  REF );

isource
#(
.value ( "pwl )
)
I3 ( 
 .p( 0 ),
 .m( G2 )
);

tran  R3 ( G2 ,  REF );

vsource
#(
.value ( -2 )
)
V1 ( 
 .p( REF ),
 .m( 0 )
);


cap_cmim
#(
.model ( cap_cmim ) ,
.w ( 7e-06 ) ,
.l ( 7e-06 ) ,
.m ( 1 ) ,
.spiceprefix ( X )
)
C2 ( 
 .c0( G ),
 .c1( 0 )
);


.control
save all
tran 10n 6u
write test_mim_cap.raw
.endc


.lib $::SG13G2_MODELS/cornerCAP.lib cap_typ

endmodule
