|Rule             |Description                                                                                                                 |Value     |Class   |
|-----------------|----------------------------------------------------------------------------------------------------------------------------|----------|--------|
|NW.b             |5.1.  NW.b Min. NWell space or notch (same net). NWell regions separated by less  than this value will be merged.           |0.62      |Missing |
|NW.b1            |5.1.  NW.b1 Min. PWell width between NWell regions (different net)                                                          |1.8       |Missing |
|PWB.d            |5.2.  PWB.d Min. PWell:block overlap of NWell                                                                               |0         |Missing |
|PWB.e            |5.2.  PWB.e Min. PWell:block space to (N+Activ not inside ThickGateOx) in PWell                                             |0.31      |Missing |
|PWB.e1           |5.2.  PWB.e1 Min. PWell:block space to (N+Activ inside ThickGateOx) in PWell                                                |0.62      |Missing |
|PWB.f            |5.2.  PWB.f Min. PWell:block space to (P+Activ not inside ThickGateOx) in PWell                                             |0.24      |Missing |
|PWB.f1           |5.2.  PWB.f1 Min. PWell:block space to (P+Activ inside ThickGateOx) in PWell                                                |0.62      |Missing |
|NBL.b            |5.3.  NBL.b Min. nBuLay space or notch (same net)                                                                           |1.5       |Missing |
|NBL.c            |5.3.  NBL.c Min. PWell width between nBuLay regions (different net)                                                         |3.2       |Missing |
|NBL.d            |5.3.  NBL.d Min. PWell width between nBuLay and NWell (different net)                                                       |2.2       |Missing |
|NBL.e            |5.3.  NBL.e Min. nBuLay space to unrelated N+Activ                                                                          |1         |Missing |
|NBL.f            |5.3.  NBL.f Min. nBuLay space to unrelated P+Activ                                                                          |0.5       |Missing |
|AFil.c           |5.6.  AFil.c Min. Activ:filler space to Cont, GatPoly                                                                       |1.1       |Missing |
|AFil.c1          |5.6.  AFil.c1 Min. Activ:filler space to Activ                                                                              |0.42      |Missing |
|AFil.d           |5.6.  AFil.d Min. Activ:filler space to NWell, nBuLay                                                                       |1         |Missing |
|AFil.e           |5.6.  AFil.e Min. Activ:filler space to TRANS                                                                               |1         |Missing |
|AFil.j           |5.6.  AFil.j Min. nSD:block and SalBlock enclosure of Activ:filler inside PWell:block                                       |0.25      |Missing |
|Gat.a1           |5.8.  Gat.a1 Min. GatPoly width for channel length of 1.2V NFET                                                             |0.13      |Missing |
|Gat.a2           |5.8.  Gat.a2 Min. GatPoly width for channel length of 1.2V PFET                                                             |0.13      |Missing |
|Gat.g            |5.8.  Gat.g Min. GatPoly width for 45-degree bent shapes if the bend GatPoly,length is > 0.39 µm                            |0.16      |Missing |
|GFil.e           |5.9.  GFil.e Min. GatPoly:filler space to NWell, nBuLay                                                                     |1.1       |Missing |
|GFil.i           |5.9.  GFil.i Max. GatPoly:nofill area (µm²)                                                                                 |400 x 400 |Missing |
|pSD.c1           |5.10.  pSD.c1 Min. pSD enclosure of P+Activ in PWell                                                                        |0.03      |Missing |
|Cnt.c            |5.14.  Cnt.c Min. Activ enclosure of Cont                                                                                   |0.07      |Missing |
|Cnt.d            |5.14.  Cnt.d Min. GatPoly enclosure of Cont                                                                                 |0.07      |Missing |
|Cnt.e            |5.14.  Cnt.e Min. Cont on GatPoly space to Activ                                                                            |0.14      |Missing |
|Cnt.g1           |5.14.  Cnt.g1 Min. pSD space to Cont on nSD-Activ                                                                           |0.09      |Missing |
|Cnt.g2           |5.14.  Cnt.g2 Min. pSD overlap of Cont on pSD-Activ                                                                         |0.09      |Missing |
|CntB.b1          |5.15.  CntB.b1 Min. ContBar space with common run > 5 µm                                                                    |0.36      |Missing |
|CntB.h1          |5.15.  CntB.h1 Min. Metal1 enclosure of ContBar                                                                             |0.05      |Missing |
|M1.e             |5.16.  M1.e Min. space of Metal1 lines if, at least one line is wider than 0.3 µm  and the parallel run is more than 1.0µm  |0.22      |Missing |
|M1.f             |5.16.  M1.f Min. space of Metal1 lines if, at least one line is wider than 10.0µm  and the parallel run is more than 10.0µm |0.6       |Missing |
|M1.g             |5.16.  M1.g Min. 45-degree bent Metal1 width if the bent metal length is > 0.5µm                                            |0.2       |Missing |
|M1.i             |5.16.  M1.i Min. space of Metal1 lines of which at least one is bent by 45-degree                                           |0.22      |Missing |
|M2.e             |5.17. M2.e Min. space of Metal2 lines if, at least one line is wider than 0.39µm and the parallel run is more than 1.0 µm   |0.24      |Missing |
|M2.f             |5.17. M2.f Min. space of Metal2 lines if, at least one line is wider than 10.0µm and the parallel run is more than 10.0µm   |0.6       |Missing |
|M2.g             |5.17. M2.g Min. 45-degree bent Metal2 width if the bent metal length is > 0.5µm                                             |0.24      |Missing |
|M2.i             |5.17. M2.i Min. space of Metal2 lines of which at least one is bent by 45-degree                                            |0.24      |Missing |
|M3.e             |5.17. M3.e Min. space of Metal3 lines if, at least one line is wider than 0.39µm and the parallel run is more than 1.0 µm   |0.24      |Missing |
|M3.f             |5.17. M3.f Min. space of Metal3 lines if, at least one line is wider than 10.0µm and the parallel run is more than 10.0µm   |0.6       |Missing |
|M3.g             |5.17. M3.g Min. 45-degree bent Metal3 width if the bent metal length is > 0.5µm                                             |0.24      |Missing |
|M3.i             |5.17. M3.i Min. space of Metal3 lines of which at least one is bent by 45-degree                                            |0.24      |Missing |
|M4.e             |5.17. M4.e Min. space of Metal4 lines if, at least one line is wider than 0.39µm and the parallel run is more than 1.0 µm   |0.24      |Missing |
|M4.f             |5.17. M4.f Min. space of Metal4 lines if, at least one line is wider than 10.0µm and the parallel run is more than 10.0µm   |0.6       |Missing |
|M4.g             |5.17. M4.g Min. 45-degree bent Metal4 width if the bent metal length is > 0.5µm                                             |0.24      |Missing |
|M4.i             |5.17. M4.i Min. space of Metal4 lines of which at least one is bent by 45-degree                                            |0.24      |Missing |
|M5.e             |5.17. M5.e Min. space of Metal5 lines if, at least one line is wider than 0.39µm and the parallel run is more than 1.0 µm   |0.24      |Missing |
|M5.f             |5.17. M5.f Min. space of Metal5 lines if, at least one line is wider than 10.0µm and the parallel run is more than 10.0µm   |0.6       |Missing |
|M5.g             |5.17. M5.g Min. 45-degree bent Metal5 width if the bent metal length is > 0.5µm                                             |0.24      |Missing |
|M5.i             |5.17. M5.i Min. space of Metal5 lines of which at least one is bent by 45-degree                                            |0.24      |Missing |
|M1Fil.a2         |5.18. M1Fil.a2 Max. Metal1:filler width                                                                                     |5         |Missing |
|M2Fil.a2         |5.18. M2Fil.a2 Max. Metal2:filler width                                                                                     |5         |Missing |
|M3Fil.a2         |5.18. M3Fil.a2 Max. Metal3:filler width                                                                                     |5         |Missing |
|M4Fil.a2         |5.18. M4Fil.a2 Max. Metal4:filler width                                                                                     |5         |Missing |
|M5Fil.a2         |5.18. M5Fil.a2 Max. Metal5:filler width                                                                                     |5         |Missing |
|V1.c             |5.19.  V1.c Min. Metal1 enclosure of Via1                                                                                   |0.01      |Missing |
|V2.c             |5.20. V2.c Min. Metal2 enclosure of Via2                                                                                    |0.005     |Missing |
|V3.c             |5.20. V3.c Min. Metal3 enclosure of Via3                                                                                    |0.005     |Missing |
|V4.c             |5.20. V4.c Min. Metal4 enclosure of Via4                                                                                    |0.005     |Missing |
|TV1.c            |5.21.  TV1.c Min. Metal5 enclosure of TopVia1                                                                               |0.1       |Missing |
|TV1.d            |5.21.  TV1.d Min. TopMetal1 enclosure of TopVia1                                                                            |0.42      |Missing |
|TM1Fil.a1        |5.23.  TM1Fil.a1 Max. TopMetal1:filler width                                                                                |10        |Missing |
|TV2.c            |5.24.  TV2.c Min. TopMetal1 enclosure of TopVia2                                                                            |0.5       |Missing |
|TV2.d            |5.24.  TV2.d Min. TopMetal2 enclosure of TopVia2                                                                            |0.5       |Missing |
|TM2.bR           |5.25.  TM2.bR Min. space of TopMetal2 lines if, at least one line is wider than 5.0µm  and the parallel run is more than 50.0 µm (Not checked within IND regions)|5     |Missing |
|TM2Fil.a1        |5.26.  TM2Fil.a1 Max. TopMetal2:filler width                                                                                |1         |Missing |
|Pas.c            |5.27.  Pas.c Min. TopMetal2 enclosure of Passiv [Not checked outside of sealring (edge-seal-passive)]                       |2.1       |Missing |
|npn13G2.bR       |6.1.3.  npn13G2.bR Max. recommended total number of npn13G2 emitters per chip                                               |4000      |Missing |
|npn13G2L.cR      |6.1.3.  npn13G2L.cR Max. recommended total number of npn13G2L emitters per chip                                             |800       |Missing |
|npn13G2V.cR      |6.1.3.  npn13G2V.cR Max. recommended total number of npn13G2V emitters per chip                                             |800       |Missing |
|Sdiod.d          |6.7.  Sdiod.d Min. and max. ContBar width inside nBuLay                                                                     |0.3       |Missing |
|Sdiod.e          |6.7.  Sdiod.e Min. and max. ContBar length inside nBuLay                                                                    |1         |Missing |
|Pad.fR_M1        |6.9.  Pad.fR_M1 Min. recommended Metal1 exit length                                                                         |7         |Missing |
|Pad.fR_M2        |6.9.  Pad.fR_M2 Min. recommended Metal2 exit length                                                                         |7         |Missing |
|Pad.fR_M3        |6.9.  Pad.fR_M3 Min. recommended Metal3 exit length                                                                         |7         |Missing |
|Pad.fR_M4        |6.9.  Pad.fR_M4 Min. recommended Metal4 exit length                                                                         |7         |Missing |
|Pad.fR_M5        |6.9.  Pad.fR_M5 Min. recommended Metal5 exit length                                                                         |7         |Missing |
|Pad.fR_TM1       |6.9.  Pad.fR_TM1 Min. recommended TopMetal1 exit length                                                                     |7         |Missing |
|Pad.fR_TM2       |6.9.  Pad.fR_TM2 Min. recommended TopMetal2 exit length                                                                     |7         |Missing |
|Pad.i            |6.9.  Pad.i dfpad without TopMetal2 not allowed                                                                             |-         |Missing |
|Padb.d           |6.9.  Padb.d Min. SBumpPad space to EdgeSeal                                                                                |50        |Missing |
|Seal.b_Activ     |6.10. Seal.b_Activ Min. Activ space to EdgeSeal-Activ                                                                       |4.9       |Missing |
|Seal.b_Metal1    |6.10. Seal.b_Metal1 Min. Activ space to EdgeSeal-Metal1                                                                     |4.9       |Missing |
|Seal.b_Metal2    |6.10. Seal.b_Metal2 Min. Activ space to EdgeSeal-Metal2                                                                     |4.9       |Missing |
|Seal.b_Metal3    |6.10. Seal.b_Metal3 Min. Activ space to EdgeSeal-Metal3                                                                     |4.9       |Missing |
|Seal.b_Metal4    |6.10. Seal.b_Metal4 Min. Activ space to EdgeSeal-Metal4                                                                     |4.9       |Missing |
|Seal.b_Metal5    |6.10. Seal.b_Metal5 Min. Activ space to EdgeSeal-Metal5                                                                     |4.9       |Missing |
|Seal.b_TopMetal1 |6.10. Seal.b_TopMetal1 Min. Activ space to EdgeSeal-TopMetal1                                                               |4.9       |Missing |
|Seal.b_TopMetal2 |6.10. Seal.b_TopMetal2 Min. Activ space to EdgeSeal-TopMetal2                                                               |4.9       |Missing |
|Seal.b_pSD       |6.10. Seal.b_pSD Min. Activ space to EdgeSeal-pSD                                                                           |4.9       |Missing |
|Seal.k           |6.10.  Seal.k Min. EdgeSeal 45-degree corner length                                                                         |21        |Missing |
|Seal.m           |6.10.  Seal.m Only one sealring per chip allowed                                                                            |-         |Missing |
|MIM.c            |6.11.  MIM.c Min. Metal5 enclosure of MIM                                                                                   |0.6       |Missing |
|MIM.d            |6.11.  MIM.d Min. MIM enclosure of TopVia1                                                                                  |0.36      |Missing |
|MIM.gR           |6.11.  MIM.gR Max. recommended total MIM area per chip (µm²)                                                                |174800    |Missing |
|Ant.a            |7.1.  Ant.a Max. ratio of GatPoly over field oxide area to connected Gate area                                              |200       |Missing |
|Ant.b_Metal1     |7.1.  Ant.b_Metal1 Max. ratio of cumulative Metal1 area  to connected Gate area (without protection diode)                  |200       |Missing |
|Ant.b_Metal2     |7.1.  Ant.b_Metal2 Max. ratio of cumulative Metal2 area  to connected Gate area (without protection diode)                  |200       |Missing |
|Ant.b_Metal3     |7.1.  Ant.b_Metal3 Max. ratio of cumulative Metal3 area  to connected Gate area (without protection diode)                  |200       |Missing |
|Ant.b_Metal4     |7.1.  Ant.b_Metal4 Max. ratio of cumulative Metal4 area  to connected Gate area (without protection diode)                  |200       |Missing |
|Ant.b_Metal5     |7.1.  Ant.b_Metal5 Max. ratio of cumulative Metal5 area  to connected Gate area (without protection diode)                  |200       |Missing |
|Ant.b_TopMetal1  |7.1.  Ant.b_TopMetal1  Max. ratio of cumulative TopMetal1 area  to connected Gate area (without protection diode)           |200       |Missing |
|Ant.b_TopMetal2  |7.1.  Ant.b_TopMetal2  Max. ratio of cumulative TopMetal2 area  to connected Gate area (without protection diode)           |200       |Missing |
|Ant.c            |7.1.  Ant.c Max. ratio of Cont area to connected Gate area                                                                  |20        |Missing |
|Ant.d_Via1       |7.1.  Ant.d_Via1 Max. ratio of cumulative Via1 area to connected Gate area (without protection diode)                       |20        |Missing |
|Ant.d_Via2       |7.1.  Ant.d_Via2 Max. ratio of cumulative Via2 area to connected Gate area (without protection diode)                       |20        |Missing |
|Ant.d_Via3       |7.1.  Ant.d_Via3 Max. ratio of cumulative Via3 area to connected Gate area (without protection diode)                       |20        |Missing |
|Ant.d_Via4       |7.1.  Ant.d_Via4 Max. ratio of cumulative Via4 area to connected Gate area (without protection diode)                       |20        |Missing |
|Ant.d_TopVia1    |7.1.  Ant.d_TopVia1 Max. ratio of cumulative TopVia1 area to connected Gate area (without protection diode)                 |20        |Missing |
|Ant.d_TopVia2    |7.1.  Ant.d_TopVia2 Max. ratio of cumulative TopVia2 area to connected Gate area (without protection diode)                 |20        |Missing |
|Ant.e_Metal1     |7.1.  Ant.e_Metal1 Max. ratio of cumulative Metal1 area to connected Gate area (with protection diode)                      |20000     |Missing |
|Ant.e_Metal2     |7.1.  Ant.e_Metal2 Max. ratio of cumulative Metal2 area to connected Gate area (with protection diode)                      |20000     |Missing |
|Ant.e_Metal3     |7.1.  Ant.e_Metal3 Max. ratio of cumulative Metal3 area to connected Gate area (with protection diode)                      |20000     |Missing |
|Ant.e_Metal4     |7.1.  Ant.e_Metal4 Max. ratio of cumulative Metal4 area to connected Gate area (with protection diode)                      |20000     |Missing |
|Ant.e_Metal5     |7.1.  Ant.e_Metal5 Max. ratio of cumulative Metal5 area to connected Gate area (with protection diode)                      |20000     |Missing |
|Ant.e_TopMetal1  |7.1.  Ant.e_TopMetal1 Max. ratio of cumulative TopMetal1 area to connected Gate area (with protection diode)                |20000     |Missing |
|Ant.e_TopMetal2  |7.1.  Ant.e_TopMetal2 Max. ratio of cumulative TopMetal2 area to connected Gate area (with protection diode)                |20000     |Missing |
|Ant.f_Via1       |7.1. Ant.f_Via1 Max. ratio of cumulative Via1 area to connected Gate area (with protection diode)                           |500       |Missing |
|Ant.f_Via2       |7.1. Ant.f_Via2 Max. ratio of cumulative Via2 area to connected Gate area (with protection diode)                           |500       |Missing |
|Ant.f_Via3       |7.1. Ant.f_Via3 Max. ratio of cumulative Via3 area to connected Gate area (with protection diode)                           |500       |Missing |
|Ant.f_Via4       |7.1. Ant.f_Via4 Max. ratio of cumulative Via4 area to connected Gate area (with protection diode)                           |500       |Missing |
|Ant.f_TopVia1    |7.1. Ant.f_TopVia1 Max. ratio of cumulative TopVia1 area to connected Gate area (with protection diode)                     |500       |Missing |
|Ant.f_TopVia2    |7.1. Ant.f_TopVia2 Max. ratio of cumulative TopVia2 area to connected Gate area (with protection diode)                     |500       |Missing |
|Ant.g            |7.1.  Ant.g Size of protection diode (µm²)                                                                                  |0.16      |Missing |
|LU.b             |7.2.  LU.b Max. space from any portion of N+Activ inside PWell to an pSD-PWell tie                                          |20        |Missing |
|Slt.e1_M1        |7.3. Slt.e1_M1 No Metal1:slit required on MIM                                                                               |-         |Missing |
|Slt.e1_M2        |7.3. Slt.e1_M2 No Metal2:slit required on MIM                                                                               |-         |Missing |
|Slt.e1_M3        |7.3. Slt.e1_M3 No Metal3:slit required on MIM                                                                               |-         |Missing |
|Slt.e1_M4        |7.3. Slt.e1_M4 No Metal4:slit required on MIM                                                                               |-         |Missing |
|Slt.e1_M5        |7.3. Slt.e1_M5 No Metal5:slit required on MIM                                                                               |-         |Missing |
|Slt.e1_TM1       |7.3. Slt.e1_TM1 No TopMetal1:slit required on MIM                                                                           |-         |Missing |
|Slt.e1_TM2       |7.3. Slt.e1_TM2 No TopMetal1:slit required on MIM                                                                           |-         |Missing |
|Slt.i_M1         |7.3. Slt.i_M1 Min. Metal1:slit density for any Metal plate bigger than 35 µm x 35µm [%]                                     |6         |Missing |
|Slt.i_M2         |7.3. Slt.i_M2 Min. Metal2:slit density for any Metal plate bigger than 35 µm x 35µm [%]                                     |6         |Missing |
|Slt.i_M3         |7.3. Slt.i_M3 Min. Metal3:slit density for any Metal plate bigger than 35 µm x 35µm [%]                                     |6         |Missing |
|Slt.i_M4         |7.3. Slt.i_M4 Min. Metal4:slit density for any Metal plate bigger than 35 µm x 35µm [%]                                     |6         |Missing |
|Slt.i_M5         |7.3. Slt.i_M5 Min. Metal5:slit density for any Metal plate bigger than 35 µm x 35µm [%]                                     |6         |Missing |
|Slt.i_TM1        |7.3. Slt.i_TM1 Min. TopMetal1:slit density for any Metal plate bigger than 35 µm x 35µm [%]                                 |6         |Missing |
|Slt.i_TM2        |7.3. Slt.i_TM2 Min. TopMetal2:slit density for any Metal plate bigger than 35 µm x 35µm [%]                                 |6         |Missing |
