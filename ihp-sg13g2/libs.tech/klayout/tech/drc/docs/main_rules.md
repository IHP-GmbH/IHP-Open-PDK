|Rule             |Description                                                                                                                 |Value     
|-----------------|----------------------------------------------------------------------------------------------------------------------------|----------
|NW.b             |5.1.  NW.b Min. NWell space or notch (same net). NWell regions separated by less  than this value will be merged.           |0.62      
|NW.b1            |5.1.  NW.b1 Min. PWell width between NWell regions (different net)                                                          |1.8       
|PWB.d            |5.2.  PWB.d Min. PWell:block overlap of NWell                                                                               |0         
|PWB.e            |5.2.  PWB.e Min. PWell:block space to (N+Activ not inside ThickGateOx) in PWell                                             |0.31      
|PWB.e1           |5.2.  PWB.e1 Min. PWell:block space to (N+Activ inside ThickGateOx) in PWell                                                |0.62      
|PWB.f            |5.2.  PWB.f Min. PWell:block space to (P+Activ not inside ThickGateOx) in PWell                                             |0.24      
|PWB.f1           |5.2.  PWB.f1 Min. PWell:block space to (P+Activ inside ThickGateOx) in PWell                                                |0.62      
|NBL.b            |5.3.  NBL.b Min. nBuLay space or notch (same net)                                                                           |1.5       
|NBL.c            |5.3.  NBL.c Min. PWell width between nBuLay regions (different net)                                                         |3.2       
|NBL.d            |5.3.  NBL.d Min. PWell width between nBuLay and NWell (different net)                                                       |2.2       
|NBL.e            |5.3.  NBL.e Min. nBuLay space to unrelated N+Activ                                                                          |1         
|NBL.f            |5.3.  NBL.f Min. nBuLay space to unrelated P+Activ                                                                          |0.5
|Act.a            |5.5.  Act.a Min. Activ width                                                                                                |0.15      
|Act.b            |5.5.  Act.b Min. Activ space or notch                                                                                       |0.21      
|AFil.c           |5.6.  AFil.c Min. Activ:filler space to Cont, GatPoly                                                                       |1.1  
|AFil.c1          |5.6.  AFil.c1 Min. Activ:filler space to Activ                                                                              |0.42      
|AFil.d           |5.6.  AFil.d Min. Activ:filler space to NWell, nBuLay                                                                       |1         
|AFil.e           |5.6.  AFil.e Min. Activ:filler space to TRANS                                                                               |1         
|AFil.g           |5.6.  AFil.g Min. global Activ density [%]                                                                                  |35        
|AFil.g1          |5.6.  AFil.g1 Max. global Activ density [%]                                                                                 |55        
|AFil.g2          |5.6.  AFil.g2 Min. Activ coverage ratio for any 800 x 800 µm² chip area [%]                                                 |25        
|AFil.g3          |5.6.  AFil.g3 Max. Activ coverage ratio for any 800 x 800 µm² chip area [%]                                                 |65        
|AFil.j           |5.6.  AFil.j Min. nSD:block and SalBlock enclosure of Activ:filler inside PWell:block                                       |0.25      
|TGO.f            |5.7.  TGO.f Min. ThickGateOx width                                                                                          |0.86      
|Gat.a            |5.8.  Gat.a Min. GatPoly width                                                                                              |0.13      
|Gat.a1           |5.8.  Gat.a1 Min. GatPoly width for channel length of 1.2V NFET                                                             |0.13      
|Gat.a2           |5.8.  Gat.a2 Min. GatPoly width for channel length of 1.2V PFET                                                             |0.13      
|Gat.b            |5.8.  Gat.b Min. GatPoly space or notch                                                                                     |0.18      
|Gat.d            |5.8.  Gat.d Min. GatPoly space to Activ                                                                                     |0.07      
|Gat.g            |5.8.  Gat.g Min. GatPoly width for 45-degree bent shapes if the bend GatPoly,length is > 0.39 µm                            |0.16      
|GFil.d           |5.9.  GFil.d Min. GatPoly:filler space to Activ, GatPoly, Cont, pSD, nSD:block, SalBlock                                    |1.1       
|GFil.e           |5.9.  GFil.e Min. GatPoly:filler space to NWell, nBuLay                                                                     |1.1       
|GFil.g           |5.9.  GFil.g Min. global GatPoly density [%]                                                                                |15        
|GFil.i           |5.9.  GFil.i Max. GatPoly:nofill area (µm²)                                                                                 |400 x 400 
|pSD.c1           |5.10.  pSD.c1 Min. pSD enclosure of P+Activ in PWell                                                                        |0.03      
|Cnt.a            |5.14.  Cnt.a Min. and max. Cont width                                                                                       |0.16      
|Cnt.b            |5.14.  Cnt.b Min. Cont space                                                                                                |0.18      
|Cnt.c            |5.14.  Cnt.c Min. Activ enclosure of Cont                                                                                   |0.07      
|Cnt.d            |5.14.  Cnt.d Min. GatPoly enclosure of Cont                                                                                 |0.07      
|Cnt.e            |5.14.  Cnt.e Min. Cont on GatPoly space to Activ                                                                            |0.14      
|Cnt.g1           |5.14.  Cnt.g1 Min. pSD space to Cont on nSD-Activ                                                                           |0.09      
|Cnt.g2           |5.14.  Cnt.g2 Min. pSD overlap of Cont on pSD-Activ                                                                         |0.09      
|CntB.b1          |5.15.  CntB.b1 Min. ContBar space with common run > 5 µm                                                                    |0.36      
|CntB.h1          |5.15.  CntB.h1 Min. Metal1 enclosure of ContBar                                                                             |0.05      
|M1.a             |5.16.  M1.a Min. Metal1 width                                                                                               |0.16      
|M1.b             |5.16.  M1.b Min. Metal1 space or notch                                                                                      |0.18      
|M1.e             |5.16.  M1.e Min. space of Metal1 lines if, at least one line is wider than 0.3 µm  and the parallel run is more than 1.0µm  |0.22      
|M1.f             |5.16.  M1.f Min. space of Metal1 lines if, at least one line is wider than 10.0µm  and the parallel run is more than 10.0µm |0.6       
|M1.g             |5.16.  M1.g Min. 45-degree bent Metal1 width if the bent metal length is > 0.5µm                                            |0.2       
|M1.i             |5.16.  M1.i Min. space of Metal1 lines of which at least one is bent by 45-degree                                           |0.22      
|M1.j             |5.16.  M1.j Min. global Metal1 density [%]                                                                                  |35        
|M1.k             |5.16.  M1.k Max. global Metal1 density [%]                                                                                  |60        
|M2.a             |5.17. M2.a Min. Metal2 width                                                                                                |0.2       
|M2.b             |5.17. M2.b Min. Metal2 space or notch                                                                                       |0.21      
|M2.e             |5.17. M2.e Min. space of Metal2 lines if, at least one line is wider than 0.39µm and the parallel run is more than 1.0 µm   |0.24      
|M2.f             |5.17. M2.f Min. space of Metal2 lines if, at least one line is wider than 10.0µm and the parallel run is more than 10.0µm   |0.6       
|M2.g             |5.17. M2.g Min. 45-degree bent Metal2 width if the bent metal length is > 0.5µm                                             |0.24      
|M2.i             |5.17. M2.i Min. space of Metal2 lines of which at least one is bent by 45-degree                                            |0.24      
|M2.j             |5.17. M2.j Min. global Metal2 density [%]                                                                                   |35        
|M2.k             |5.17. M2.k Max. global Metal2 density [%]                                                                                   |60        
|M3.a             |5.17. M3.a Min. Metal3 width                                                                                                |0.2       
|M3.b             |5.17. M3.b Min. Metal3 space or notch                                                                                       |0.21      
|M3.e             |5.17. M3.e Min. space of Metal3 lines if, at least one line is wider than 0.39µm and the parallel run is more than 1.0 µm   |0.24      
|M3.f             |5.17. M3.f Min. space of Metal3 lines if, at least one line is wider than 10.0µm and the parallel run is more than 10.0µm   |0.6       
|M3.g             |5.17. M3.g Min. 45-degree bent Metal3 width if the bent metal length is > 0.5µm                                             |0.24      
|M3.i             |5.17. M3.i Min. space of Metal3 lines of which at least one is bent by 45-degree                                            |0.24      
|M3.j             |5.17. M3.j Min. global Metal3 density [%]                                                                                   |35        
|M3.k             |5.17. M3.k Max. global Metal3 density [%]                                                                                   |60        
|M4.a             |5.17. M4.a Min. Metal4 width                                                                                                |0.2       
|M4.b             |5.17. M4.b Min. Metal4 space or notch                                                                                       |0.21      
|M4.e             |5.17. M4.e Min. space of Metal4 lines if, at least one line is wider than 0.39µm and the parallel run is more than 1.0 µm   |0.24      
|M4.f             |5.17. M4.f Min. space of Metal4 lines if, at least one line is wider than 10.0µm and the parallel run is more than 10.0µm   |0.6       
|M4.g             |5.17. M4.g Min. 45-degree bent Metal4 width if the bent metal length is > 0.5µm                                             |0.24      
|M4.i             |5.17. M4.i Min. space of Metal4 lines of which at least one is bent by 45-degree                                            |0.24      
|M4.j             |5.17. M4.j Min. global Metal4 density [%]                                                                                   |35        
|M4.k             |5.17. M4.k Max. global Metal4 density [%]                                                                                   |60        
|M5.a             |5.17. M5.a Min. Metal5 width                                                                                                |0.2       
|M5.b             |5.17. M5.b Min. Metal5 space or notch                                                                                       |0.21      
|M5.e             |5.17. M5.e Min. space of Metal5 lines if, at least one line is wider than 0.39µm and the parallel run is more than 1.0 µm   |0.24      
|M5.f             |5.17. M5.f Min. space of Metal5 lines if, at least one line is wider than 10.0µm and the parallel run is more than 10.0µm   |0.6       
|M5.g             |5.17. M5.g Min. 45-degree bent Metal5 width if the bent metal length is > 0.5µm                                             |0.24      
|M5.i             |5.17. M5.i Min. space of Metal5 lines of which at least one is bent by 45-degree                                            |0.24      
|M5.j             |5.17. M5.j Min. global Metal5 density [%]                                                                                   |35        
|M5.k             |5.17. M5.k Max. global Metal5 density [%]                                                                                   |60        
|M1Fil.a2         |5.18. M1Fil.a2 Max. Metal1:filler width                                                                                     |5         
|M1Fil.c          |5.18. M1Fil.c Min. Metal1:filler space to Metal1                                                                            |0.42      
|M1Fil.h          |5.18. M1Fil.h Min. Metal1 and Metal1:filler coverage ratio for any 800 x 800 µm² chip area [%]                              |25        
|M1Fil.k          |5.18. M1Fil.k Max. Metal1 and Metal1:filler coverage ratio for any 800 x 800 µm² chip area [%]                              |75        
|M2Fil.a2         |5.18. M2Fil.a2 Max. Metal2:filler width                                                                                     |5         
|M2Fil.c          |5.18. M2Fil.c Min. Metal2:filler space to Metal2                                                                            |0.42      
|M2Fil.h          |5.18. M2Fil.h Min. Metal2 and Metal2:filler coverage ratio for any 800 x 800 µm² chip area [%]                              |25        
|M2Fil.k          |5.18. M2Fil.k Max. Metal2 and Metal2:filler coverage ratio for any 800 x 800 µm² chip area [%]                              |75        
|M3Fil.a2         |5.18. M3Fil.a2 Max. Metal3:filler width                                                                                     |5         
|M3Fil.c          |5.18. M3Fil.c Min. Metal3:filler space to Metal3                                                                            |0.42      
|M3Fil.h          |5.18. M3Fil.h Min. Metal3 and Metal3:filler coverage ratio for any 800 x 800 µm² chip area [%]                              |25        
|M3Fil.k          |5.18. M3Fil.k Max. Metal3 and Metal3:filler coverage ratio for any 800 x 800 µm² chip area [%]                              |75        
|M4Fil.a2         |5.18. M4Fil.a2 Max. Metal4:filler width                                                                                     |5         
|M4Fil.c          |5.18. M4Fil.c Min. Metal4:filler space to Metal4                                                                            |0.42      
|M4Fil.h          |5.18. M4Fil.h Min. Metal4 and Metal4:filler coverage ratio for any 800 x 800 µm² chip area [%]                              |25        
|M4Fil.k          |5.18. M4Fil.k Max. Metal4 and Metal4:filler coverage ratio for any 800 x 800 µm² chip area [%]                              |75        
|M5Fil.a2         |5.18. M5Fil.a2 Max. Metal5:filler width                                                                                     |5         
|M5Fil.c          |5.18. M5Fil.c Min. Metal5:filler space to Metal5                                                                            |0.42      
|M5Fil.h          |5.18. M5Fil.h Min. Metal5 and Metal5:filler coverage ratio for any 800 x 800 µm² chip area [%]                              |25        
|M5Fil.k          |5.18. M5Fil.k Max. Metal5 and Metal5:filler coverage ratio for any 800 x 800 µm² chip area [%]                              |75        
|V1.a             |5.19.  V1.a Min. and max. Via1 width                                                                                        |0.19      
|V1.b             |5.19.  V1.b Min. Via1 space                                                                                                 |0.22      
|V1.c             |5.19.  V1.c Min. Metal1 enclosure of Via1                                                                                   |0.01      
|V2.a             |5.20. V2.a Min. and max. Via2 width                                                                                         |0.19      
|V2.b             |5.20. V2.b Min. Via2 space                                                                                                  |0.22      
|V2.c             |5.20. V2.c Min. Metal2 enclosure of Via2                                                                                    |0.005     
|V3.a             |5.20. V3.a Min. and max. Via3 width                                                                                         |0.19      
|V3.b             |5.20. V3.b Min. Via3 space                                                                                                  |0.22      
|V3.c             |5.20. V3.c Min. Metal3 enclosure of Via3                                                                                    |0.005     
|V4.a             |5.20. V4.a Min. and max. Via4 width                                                                                         |0.19      
|V4.b             |5.20. V4.b Min. Via4 space                                                                                                  |0.22      
|V4.c             |5.20. V4.c Min. Metal4 enclosure of Via4                                                                                    |0.005     
|TV1.a            |5.21.  TV1.a Min. and max. TopVia1 width                                                                                    |0.42      
|TV1.b            |5.21.  TV1.b Min. TopVia1 space                                                                                             |0.42      
|TV1.c            |5.21.  TV1.c Min. Metal5 enclosure of TopVia1                                                                               |0.1       
|TV1.d            |5.21.  TV1.d Min. TopMetal1 enclosure of TopVia1                                                                            |0.42      
|TM1.a            |5.22.  TM1.a Min. TopMetal1 width                                                                                           |1.64      
|TM1.b            |5.22.  TM1.b Min. TopMetal1 space or notch                                                                                  |1.64      
|TM1.c            |5.22.  TM1.c Min. global TopMetal1 density [%]                                                                              |25        
|TM1.d            |5.22.  TM1.d Max. global TopMetal1 density [%]                                                                              |70        
|TM1Fil.a1        |5.23.  TM1Fil.a1 Max. TopMetal1:filler width                                                                                |10        
|TM1Fil.c         |5.23.  TM1Fil.c Min. TopMetal1:filler space to TopMetal1                                                                    |3         
|TV2.a            |5.24.  TV2.a Min. and max. TopVia2 width                                                                                    |0.9       
|TV2.b            |5.24.  TV2.b Min. TopVia2 space                                                                                             |1.06      
|TV2.c            |5.24.  TV2.c Min. TopMetal1 enclosure of TopVia2                                                                            |0.5       
|TV2.d            |5.24.  TV2.d Min. TopMetal2 enclosure of TopVia2                                                                            |0.5       
|TM2.a            |5.25.  TM2.a Min. TopMetal2 width                                                                                           |2         
|TM2.b            |5.25.  TM2.b Min. TopMetal2 space or notch                                                                                  |2         
|TM2.bR           |5.25.  TM2.bR Min. space of TopMetal2 lines if, at least one line is wider than 5.0µm  and the parallel run is more than 50.0 µm (Not checked within IND regions)|5     
|TM2.c            |5.25.  TM2.c Min. global TopMetal2 density [%]                                                                              |25        
|TM2.d            |5.25.  TM2.d Max. global TopMetal2 density [%]                                                                              |70        
|TM2Fil.a1        |5.26.  TM2Fil.a1 Max. TopMetal2:filler width                                                                                |1         
|TM2Fil.c         |5.26.  TM2Fil.c Min. TopMetal2:filler space to TopMetal2                                                                    |3         
|Pas.a            |5.27.  Pas.a Min. Passiv width                                                                                              |2.1       
|Pas.b            |5.27.  Pas.b Min. Passiv space or notch                                                                                     |3.5       
|Pas.c            |5.27.  Pas.c Min. TopMetal2 enclosure of Passiv [Not checked outside of sealring (edge-seal-passive)]                       |2.1       
|npn13G2.bR       |6.1.3.  npn13G2.bR Max. recommended total number of npn13G2 emitters per chip                                               |4000      
|npn13G2L.cR      |6.1.3.  npn13G2L.cR Max. recommended total number of npn13G2L emitters per chip                                             |800       
|npn13G2V.cR      |6.1.3.  npn13G2V.cR Max. recommended total number of npn13G2V emitters per chip                                             |800       
|Sdiod.d          |6.7.  Sdiod.d Min. and max. ContBar width inside nBuLay                                                                     |0.3       
|Sdiod.e          |6.7.  Sdiod.e Min. and max. ContBar length inside nBuLay                                                                    |1         
|Pad.fR_M1        |6.9.  Pad.fR_M1 Min. recommended Metal1 exit length                                                                         |7         
|Pad.fR_M2        |6.9.  Pad.fR_M2 Min. recommended Metal2 exit length                                                                         |7         
|Pad.fR_M3        |6.9.  Pad.fR_M3 Min. recommended Metal3 exit length                                                                         |7         
|Pad.fR_M4        |6.9.  Pad.fR_M4 Min. recommended Metal4 exit length                                                                         |7         
|Pad.fR_M5        |6.9.  Pad.fR_M5 Min. recommended Metal5 exit length                                                                         |7         
|Pad.fR_TM1       |6.9.  Pad.fR_TM1 Min. recommended TopMetal1 exit length                                                                     |7         
|Pad.fR_TM2       |6.9.  Pad.fR_TM2 Min. recommended TopMetal2 exit length                                                                     |7         
|Pad.i            |6.9.  Pad.i dfpad without TopMetal2 not allowed                                                                             |-         
|Padb.a           |6.9.  Padb.a SBumpPad size                                                                                                  |60        
|Padb.b           |6.9.  Padb.b Min. SBumpPad space                                                                                            |70        
|Padb.c           |6.9.  Padb.c Min. TopMetal2 (within dfpad) enclosure of SBumpPad                                                            |10        
|Padb.d           |6.9.  Padb.d Min. SBumpPad space to EdgeSeal                                                                                |50        
|Padc.a           |6.9.  Padc.a CuPillarPad size                                                                                               |35        
|Padc.b           |6.9.  Padc.b Min. CuPillarPad space                                                                                         |40        
|Padc.c           |6.9.  Padc.c Min. TopMetal2 (within dfpad) enclosure of CuPillarPad                                                         |7.5       
|Seal.b_Activ     |6.10. Seal.b_Activ Min. Activ space to EdgeSeal-Activ                                                                       |4.9       
|Seal.b_Metal1    |6.10. Seal.b_Metal1 Min. Activ space to EdgeSeal-Metal1                                                                     |4.9       
|Seal.b_Metal2    |6.10. Seal.b_Metal2 Min. Activ space to EdgeSeal-Metal2                                                                     |4.9       
|Seal.b_Metal3    |6.10. Seal.b_Metal3 Min. Activ space to EdgeSeal-Metal3                                                                     |4.9       
|Seal.b_Metal4    |6.10. Seal.b_Metal4 Min. Activ space to EdgeSeal-Metal4                                                                     |4.9       
|Seal.b_Metal5    |6.10. Seal.b_Metal5 Min. Activ space to EdgeSeal-Metal5                                                                     |4.9       
|Seal.b_TopMetal1 |6.10. Seal.b_TopMetal1 Min. Activ space to EdgeSeal-TopMetal1                                                               |4.9       
|Seal.b_TopMetal2 |6.10. Seal.b_TopMetal2 Min. Activ space to EdgeSeal-TopMetal2                                                               |4.9       
|Seal.b_pSD       |6.10. Seal.b_pSD Min. Activ space to EdgeSeal-pSD                                                                           |4.9       
|Seal.k           |6.10.  Seal.k Min. EdgeSeal 45-degree corner length                                                                         |21        
|Seal.l           |6.10.  Seal.l No structures outside sealring boundary allowed                                                               |-         
|Seal.m           |6.10.  Seal.m Only one sealring per chip allowed                                                                            |-         
|Seal.n           |6.10.  seal.n Sealring must be enclosed by an unbroken Passiv ring                                                          |-         
|MIM.c            |6.11.  MIM.c Min. Metal5 enclosure of MIM                                                                                   |0.6       
|MIM.d            |6.11.  MIM.d Min. MIM enclosure of TopVia1                                                                                  |0.36      
|MIM.gR           |6.11.  MIM.gR Max. recommended total MIM area per chip (µm²)                                                                |174800    
|Ant.a            |7.1.  Ant.a Max. ratio of GatPoly over field oxide area to connected Gate area                                              |200       
|Ant.b_Metal1     |7.1.  Ant.b_Metal1 Max. ratio of cumulative Metal1 area  to connected Gate area (without protection diode)                  |200       
|Ant.b_Metal2     |7.1.  Ant.b_Metal2 Max. ratio of cumulative Metal2 area  to connected Gate area (without protection diode)                  |200       
|Ant.b_Metal3     |7.1.  Ant.b_Metal3 Max. ratio of cumulative Metal3 area  to connected Gate area (without protection diode)                  |200       
|Ant.b_Metal4     |7.1.  Ant.b_Metal4 Max. ratio of cumulative Metal4 area  to connected Gate area (without protection diode)                  |200       
|Ant.b_Metal5     |7.1.  Ant.b_Metal5 Max. ratio of cumulative Metal5 area  to connected Gate area (without protection diode)                  |200       
|Ant.b_TopMetal1  |7.1.  Ant.b_TopMetal1  Max. ratio of cumulative TopMetal1 area  to connected Gate area (without protection diode)           |200       
|Ant.b_TopMetal2  |7.1.  Ant.b_TopMetal2  Max. ratio of cumulative TopMetal2 area  to connected Gate area (without protection diode)           |200       
|Ant.c            |7.1.  Ant.c Max. ratio of Cont area to connected Gate area                                                                  |20        
|Ant.d_Via1       |7.1.  Ant.d_Via1 Max. ratio of cumulative Via1 area to connected Gate area (without protection diode)                       |20        
|Ant.d_Via2       |7.1.  Ant.d_Via2 Max. ratio of cumulative Via2 area to connected Gate area (without protection diode)                       |20        
|Ant.d_Via3       |7.1.  Ant.d_Via3 Max. ratio of cumulative Via3 area to connected Gate area (without protection diode)                       |20        
|Ant.d_Via4       |7.1.  Ant.d_Via4 Max. ratio of cumulative Via4 area to connected Gate area (without protection diode)                       |20        
|Ant.d_TopVia1    |7.1.  Ant.d_TopVia1 Max. ratio of cumulative TopVia1 area to connected Gate area (without protection diode)                 |20        
|Ant.d_TopVia2    |7.1.  Ant.d_TopVia2 Max. ratio of cumulative TopVia2 area to connected Gate area (without protection diode)                 |20        
|Ant.e_Metal1     |7.1.  Ant.e_Metal1 Max. ratio of cumulative Metal1 area to connected Gate area (with protection diode)                      |20000     
|Ant.e_Metal2     |7.1.  Ant.e_Metal2 Max. ratio of cumulative Metal2 area to connected Gate area (with protection diode)                      |20000     
|Ant.e_Metal3     |7.1.  Ant.e_Metal3 Max. ratio of cumulative Metal3 area to connected Gate area (with protection diode)                      |20000     
|Ant.e_Metal4     |7.1.  Ant.e_Metal4 Max. ratio of cumulative Metal4 area to connected Gate area (with protection diode)                      |20000     
|Ant.e_Metal5     |7.1.  Ant.e_Metal5 Max. ratio of cumulative Metal5 area to connected Gate area (with protection diode)                      |20000     
|Ant.e_TopMetal1  |7.1.  Ant.e_TopMetal1 Max. ratio of cumulative TopMetal1 area to connected Gate area (with protection diode)                |20000     
|Ant.e_TopMetal2  |7.1.  Ant.e_TopMetal2 Max. ratio of cumulative TopMetal2 area to connected Gate area (with protection diode)                |20000     
|Ant.f_Via1       |7.1. Ant.f_Via1 Max. ratio of cumulative Via1 area to connected Gate area (with protection diode)                           |500       
|Ant.f_Via2       |7.1. Ant.f_Via2 Max. ratio of cumulative Via2 area to connected Gate area (with protection diode)                           |500       
|Ant.f_Via3       |7.1. Ant.f_Via3 Max. ratio of cumulative Via3 area to connected Gate area (with protection diode)                           |500       
|Ant.f_Via4       |7.1. Ant.f_Via4 Max. ratio of cumulative Via4 area to connected Gate area (with protection diode)                           |500       
|Ant.f_TopVia1    |7.1. Ant.f_TopVia1 Max. ratio of cumulative TopVia1 area to connected Gate area (with protection diode)                     |500       
|Ant.f_TopVia2    |7.1. Ant.f_TopVia2 Max. ratio of cumulative TopVia2 area to connected Gate area (with protection diode)                     |500       
|Ant.g            |7.1.  Ant.g Size of protection diode (µm²)                                                                                  |0.16      
|LU.b             |7.2.  LU.b Max. space from any portion of N+Activ inside PWell to an pSD-PWell tie                                          |20        
|Slt.e1_M1        |7.3. Slt.e1_M1 No Metal1:slit required on MIM                                                                               |-         
|Slt.e1_M2        |7.3. Slt.e1_M2 No Metal2:slit required on MIM                                                                               |-         
|Slt.e1_M3        |7.3. Slt.e1_M3 No Metal3:slit required on MIM                                                                               |-         
|Slt.e1_M4        |7.3. Slt.e1_M4 No Metal4:slit required on MIM                                                                               |-         
|Slt.e1_M5        |7.3. Slt.e1_M5 No Metal5:slit required on MIM                                                                               |-         
|Slt.e1_TM1       |7.3. Slt.e1_TM1 No TopMetal1:slit required on MIM                                                                           |-         
|Slt.e1_TM2       |7.3. Slt.e1_TM2 No TopMetal1:slit required on MIM                                                                           |-         
|Slt.i_M1         |7.3. Slt.i_M1 Min. Metal1:slit density for any Metal plate bigger than 35 µm x 35µm [%]                                     |6         
|Slt.i_M2         |7.3. Slt.i_M2 Min. Metal2:slit density for any Metal plate bigger than 35 µm x 35µm [%]                                     |6         
|Slt.i_M3         |7.3. Slt.i_M3 Min. Metal3:slit density for any Metal plate bigger than 35 µm x 35µm [%]                                     |6         
|Slt.i_M4         |7.3. Slt.i_M4 Min. Metal4:slit density for any Metal plate bigger than 35 µm x 35µm [%]                                     |6         
|Slt.i_M5         |7.3. Slt.i_M5 Min. Metal5:slit density for any Metal plate bigger than 35 µm x 35µm [%]                                     |6         
|Slt.i_TM1        |7.3. Slt.i_TM1 Min. TopMetal1:slit density for any Metal plate bigger than 35 µm x 35µm [%]                                 |6         
|Slt.i_TM2        |7.3. Slt.i_TM2 Min. TopMetal2:slit density for any Metal plate bigger than 35 µm x 35µm [%]                                 |6         
|Pin.a            |7.4.  Pin.a Min. Activ enclosure of Activ:pin                                                                               |0         
|Pin.b            |7.4.  Pin.b Min. GatPoly enclosure of GatPoly:pin                                                                           |0         
|Pin.e            |7.4.  Pin.e Min. Metal1 enclosure of Metal1:pin                                                                             |0         
|Pin.f_M2         |7.4.  Pin.f Min. Metal2 enclosure of Metal2:pin                                                                             |0         
|Pin.f_M3         |7.4.  Pin.f Min. Metal3 enclosure of Metal3:pin                                                                             |0         
|Pin.f_M4         |7.4.  Pin.f Min. Metal4 enclosure of Metal4:pin                                                                             |0         
|Pin.f_M5         |7.4.  Pin.f Min. Metal5 enclosure of Metal5:pin                                                                             |0         
|Pin.g            |7.4.  Pin.g Min. TopMetal1 enclosure of TopMetal1:pin                                                                       |0         
|Pin.h            |7.4.  Pin.h Min. TopMetal2 enclosure of TopMetal2:pin                                                                       |0         
|LBE.a            |9.1.  LBE.a Min. LBE width                                                                                                  |100       
|LBE.b            |9.1.  LBE.b Max. LBE width                                                                                                  |1500      
|LBE.b1           |9.1.  LBE.b1 Max. LBE area (µm²)                                                                                            |250000    
|LBE.c            |9.1.  LBE.c Min. LBE space or notch                                                                                         |100       
|LBE.d            |9.1.  LBE.d Min. LBE space to inner edge of EdgeSeal                                                                        |150       
|LBE.h            |9.1.  LBE.h No LBE ring allowed                                                                                             |-         
|LBE.i            |9.1.  LBE.i Max. global LBE density [%]                                                                                     |20        
|forbidden.BiWind |3.2. forbidden.BiWind BiWind is forbidden in designs submitted for all 0.13 µm technologies.                                |-         
|forbidden.PEmWind|3.2. forbidden.PEmWind PEmWind is forbidden in designs submitted for all 0.13 µm technologies.                              |-         
|forbidden.BasPoly|3.2. forbidden.BasPoly BasPoly is forbidden in designs submitted for all 0.13 µm technologies.                              |-         
|forbidden.DeepCo |3.2. forbidden.DeepCo DeepCo is forbidden in designs submitted for all 0.13 µm technologies.                                |-         
|forbidden.PEmPoly|3.2. forbidden.PEmPoly PEmPoly is forbidden in designs submitted for all 0.13 µm technologies.                              |-         
|forbidden.EmPoly |3.2. forbidden.EmPoly EmPoly is forbidden in designs submitted for all 0.13 µm technologies.                                |-         
|forbidden.LDMOS  |3.2. forbidden.LDMOS LDMOS is forbidden in designs submitted for all 0.13 µm technologies.                                  |-         
|forbidden.PBiWind|3.2. forbidden.PBiWind PBiWind is forbidden in designs submitted for all 0.13 µm technologies.                              |-         
|forbidden.NoDRC  |3.2. forbidden.NoDRC NoDRC is forbidden in designs submitted for all 0.13 µm technologies.                                  |-         
|forbidden.Flash  |3.2. forbidden.Flash Flash is forbidden in designs submitted for all 0.13 µm technologies.                                  |-         
|forbidden.ColWind|3.2. forbidden.ColWind ColWind is forbidden in designs submitted for all 0.13 µm technologies.                              |-         
