|Rule       |Description                                                                                                                     |Value (um) |Class   |
|-----------|--------------------------------------------------------------------------------------------------------------------------------|-----------|--------|
|NW.a       |5.1.  NW.a Min. NWell width                                                                                                     |0.62       |Max     |
|NW.c       |5.1.  NW.c Min. NWell enclosure of P+Activ not inside ThickGateOx                                                               |0.31       |Max     |
|NW.c1      |5.1.  NW.c1 Min. NWell enclosure of P+Activ inside ThickGateOx                                                                  |0.62       |Max     |
|NW.d       |5.1.  NW.d Min. NWell space to external N+Activ not inside ThickGateOx                                                          |0.31       |Max     |
|NW.d1      |5.1.  NW.d1 Min. NWell space to external N+Activ inside ThickGateOx                                                             |0.62       |Max     |
|NW.e       |5.1.  NW.e Min. NWell enclosure of NWell tie surrounded entirely by  NWell in N+Activ not inside ThickGateOx                    |0.24       |Max     |
|NW.e1      |5.1.  NW.e1 Min. NWell enclosure of NWell tie surrounded entirely by  NWell in N+Activ inside ThickGateOx                       |0.62       |Max     |
|NW.f       |5.1.  NW.f Min. NWell space to substrate tie in P+Activ not inside ThickGateOx                                                  |0.24       |Max     |
|NW.f1      |5.1.  NW.f1 Min. NWell space to substrate tie in P+Activ inside ThickGateOx                                                     |0.62       |Max     |
|PWB.a      |5.2.  PWB.a Min. PWell:block width                                                                                              |0.62       |Max     |
|PWB.b      |5.2.  PWB.b Min. PWell:block space or notch                                                                                     |0.62       |Max     |
|PWB.c      |5.2.  PWB.c Min. PWell:block space to unrelated NWell                                                                           |0.62       |Max     |
|NBL.a      |5.3.  NBL.a Min. nBuLay width                                                                                                   |1          |Max     |
|NBLB.a     |5.4.  NBL.a Min. nBuLay:block width                                                                                             |1.5        |Max     |
|NBLB.b     |5.4.  NBL.b Min. nBuLay:block space or notch                                                                                    |1          |Max     |
|NBLB.c     |5.4.  NBL.c Min. nBuLay enclosure of nBuLay:block                                                                               |1          |Max     |
|NBLB.d     |5.4.  NBL.d Min. nBuLay:block space to unrelated nBuLay                                                                         |1.5        |Max     |
|Act.c      |5.5.  Act.c Min. Activ drain/source extension                                                                                   |0.23       |Max     |
|Act.d      |5.5.  Act.d Min. Activ area (µm²)                                                                                               |0.122      |Max     |
|Act.e      |5.5.  Act.e Min. Activ enclosed area (µm²)                                                                                      |0.15       |Max     |
|AFil.a     |5.6.  AFil.a Max. Activ:filler width                                                                                            |5          |Max     |
|AFil.a1    |5.6.  AFil.a1 Min. Activ:filler width                                                                                           |1          |Max     |
|AFil.b     |5.6.  AFil.b Min. Activ:filler space                                                                                            |0.42       |Max     |
|AFil.i     |5.6.  AFil.i Min. Activ:filler space to edges of PWell:block                                                                    |1.5        |Max     |
|TGO.a      |5.7.  TGO.a Min. ThickGateOx extension over Activ                                                                               |0.27       |Max     |
|TGO.b      |5.7.  TGO.b Min. space between ThickGateOx and Activ outside thick gate oxide region                                            |0.27       |Max     |
|TGO.c      |5.7.  TGO.c Min. ThickGateOx extension over GatPoly over Activ                                                                  |0.34       |Max     |
|TGO.d      |5.7.  TGO.d Min. space between ThickGateOx and GatPoly over Activ outside thick gate oxide region                               |0.34       |Max     |
|TGO.e      |5.7.  TGO.e Min. ThickGateOx space (merge if less than this value)                                                              |0.86       |Max     |
|Gat.a3     |5.8.  Gat.a3 Min. GatPoly width for channel length of 3.3V NFET                                                                 |0.45       |Max     |
|Gat.a4     |5.8.  Gat.a4 Min. GatPoly width for channel length of 3.3V PFET                                                                 |0.4        |Max     |
|Gat.b1     |5.8.  Gat.b1 Min. space between unrelated 3.3 V GatPoly over Activ regions                                                      |0.25       |Max     |
|Gat.c      |5.8.  Gat.c Min. GatPoly extension over Activ (end cap)                                                                         |0.18       |Max     |
|Gat.e      |5.8.  Gat.e Min. GatPoly area (µm²)                                                                                             |0.09       |Max     |
|Gat.f      |5.8.  Gat.f 45-degree and 90-degree angles for GatPoly on Activ area are not allowed.                                           |0          |Max     |
|GFil.a     |5.9.  GFil.a Max. GatPoly:filler width                                                                                          |5          |Max     |
|GFil.b     |5.9.  GFil.b Min. GatPoly:filler width                                                                                          |0.7        |Max     |
|GFil.c     |5.9.  GFil.c Min. GatPoly:filler space                                                                                          |0.8        |Max     |
|GFil.f     |5.9.  GFil.f Min. GatPoly:filler space to TRANS                                                                                 |1.1        |Max     |
|GFil.j     |5.9.  GFil.j Min. GatPoly:filler extension over Activ:filler (end cap)                                                          |0.18       |Max     |
|pSD.a      |5.10.  pSD.a Min. pSD width                                                                                                     |0.31       |Max     |
|pSD.b      |5.10.  pSD.b Min. pSD space or notch. (pSD regions separated by less than this value will be merged)                            |0.31       |Max     |
|pSD.c      |5.10.  pSD.c Min. pSD enclosure of P+Activ in NWell                                                                             |0.18       |Max     |
|pSD.d      |5.10.  pSD.d Min. pSD space to unrelated N+Activ in PWell                                                                       |0.18       |Max     |
|pSD.d1     |5.10.  pSD.d1 Min. pSD space to N+Activ in NWell                                                                                |0.03       |Max     |
|pSD.e      |5.10.  pSD.e Min. pSD overlap of Activ at one position when forming abutted substrate tie                                       |0.3        |Max     |
|pSD.f      |5.10.  pSD.f Min. Activ extension over pSD at one position when forming abutted NWell tie                                       |0.3        |Max     |
|pSD.g      |5.10.  pSD.g Min. N+Activ or P+Activ area (µm²) when forming abutted tie                                                        |0.09       |Max     |
|pSD.i      |5.10.  pSD.i Min. pSD enclosure of PFET gate not inside ThickGateOx                                                             |0.3        |Max     |
|pSD.i1     |5.10.  pSD.i1 Min. pSD enclosure of PFET gate inside ThickGateOx                                                                |0.4        |Max     |
|pSD.j      |5.10.  pSD.j Min. pSD space to NFET gate not inside ThickGateOx                                                                 |0.3        |Max     |
|pSD.j1     |5.10.  pSD.j1 Min. pSD space to NFET gate inside ThickGateOx                                                                    |0.4        |Max     |
|pSD.k      |5.10.  pSD.k Min. pSD area (µm²)                                                                                                |0.25       |Max     |
|pSD.l      |5.10.  pSD.l Min. pSD enclosed area (µm²)                                                                                       |0.25       |Max     |
|pSD.m      |5.10.  pSD.m Min. pSD space to n-type poly resistors                                                                            |0.18       |Max     |
|pSD.n      |5.10.  pSD.n Min. pSD enclosure of p-type poly resistors                                                                        |0.18       |Max     |
|nSDB.a     |5.11.  nSDB.a Min. nSD:block width                                                                                              |0.31       |Max     |
|nSDB.b     |5.11.  nSDB.b Min. nSD:block space or notch                                                                                     |0.31       |Max     |
|nSDB.c     |5.11.  nSDB.c Min. nSD:block space to unrelated pSD                                                                             |0.31       |Max     |
|nSDB.e     |5.11.  nSDB.e Min. nSD:block space to Cont (nSD:block and Cont do not overlap.)                                                 |0          |Max     |
|EXTB.a     |5.12.  EXT.a Min. EXTBlock width                                                                                                |0.31       |Max     |
|EXTB.b     |5.12.  EXT.b Min. EXTBlock space or notch                                                                                       |0.31       |Max     |
|EXTB.c     |5.12.  EXT.c Min. EXTBlock space to pSD                                                                                         |0.31       |Max     |
|Sal.a      |5.13.  Sal.a Min. SalBlock width                                                                                                |0.42       |Max     |
|Sal.b      |5.13.  Sal.b Min. SalBlock space or notch                                                                                       |0.42       |Max     |
|Sal.c      |5.13.  Sal.c Min. SalBlock extension over Activ or GatPoly                                                                      |0.2        |Max     |
|Sal.d      |5.13.  Sal.d Min. SalBlock space to unrelated Activ or GatPoly                                                                  |0.2        |Max     |
|Sal.e      |5.13.  Sal.e Min. SalBlock space to Cont                                                                                        |0.2        |Max     |
|Cnt.b1     |5.14.  Cnt.b1 Min. Cont space in a contact array of more than 4 rows and more,then 4 columns (Cnt.b1 is only required in one direction. The distance of the other direction must be at least Cnt.b.)|0.2        |Max     |
|Cnt.f     |5.14.  Cnt.f Min. Cont on Activ space to GatPoly                                                                                 |0.11       |Max     |
|Cnt.g     |5.14.  Cnt.g Cont must be within Activ or GatPoly                                                                                |-          |Max     |
|Cnt.h     |5.14.  Cnt.h Cont must be covered with Metal1                                                                                    |-          |Max     |
|Cnt.j     |5.14.  Cnt.j Cont on GatPoly over Activ is not allowed                                                                           |-          |Max     |
|CntB.a    |5.15.  CntB.a Min. and max. ContBar width                                                                                        |0.16       |Max     |
|CntB.a1   |5.15.  CntB.a1 Min. ContBar length                                                                                               |0.34       |Max     |
|CntB.b    |5.15.  CntB.b Min. ContBar space                                                                                                 |0.28       |Max     |
|CntB.b2   |5.15.  CntB.b2 Min. ContBar space to Cont                                                                                        |0.22       |Max     |
|CntB.c    |5.15.  CntB.c Min. Activ enclosure of ContBar                                                                                    |0.07       |Max     |
|CntB.d    |5.15.  CntB.d Min. GatPoly enclosure of ContBar                                                                                  |0.07       |Max     |
|CntB.e    |5.15.  CntB.e Min. ContBar on GatPoly space to Activ                                                                             |0.14       |Max     |
|CntB.f    |5.15.  CntB.f Min. ContBar on Activ space to GatPoly                                                                             |0.11       |Max     |
|CntB.g    |5.15.  CntB.g ContBar must be within Activ or GatPoly                                                                            |-          |Max     |
|CntB.g1   |5.15.  CntB.g1 Min. pSD space to ContBar on nSD-Activ                                                                            |0.09       |Max     |
|CntB.g2   |5.15.  CntB.g2 Min. pSD overlap of ContBar on pSD-Activ                                                                          |0.09       |Max     |
|CntB.h    |5.15.  CntB.h ContBar must be covered with Metal1                                                                                |-          |Max     |
|CntB.j    |5.15.  CntB.j ContBar on GatPoly over Activ is not allowed                                                                       |-          |Max     |
|M1.c      |5.16.  M1.c Min. Metal1 enclosure of Cont                                                                                        |0          |Max     |
|M1.c1     |5.16.  M1.c1 Min. Metal1 endcap enclosure of Cont (For contacts at Metal1 corners at least one side must be treated as an endcap and for the other sides rule M1.c can be applied.)                                                                                                                                    |0.05       |Max     |
|M1.d      |5.16.  M1.d Min. Metal1 area (µm²)                                                                                               |0.09       |Max     |
|M2.c      |5.17. M2.c Min. Metal2 enclosure of Via1                                                                                         |0.005      |Max     |
|M2.c1     |5.17. M2.c1 Min. Metal2 endcap enclosure of Via1 (For vias at Metal2 corners at least one side must be treated as an endcap and for the other sides rule M2.c can be applied.)                                                                                                                                    |0.05       |Max     |
|M2.d      |5.17. M2.d Min. Metal2 area (µm²)                                                                                                |0.144      |Max     |
|M3.c      |5.17. M3.c Min. Metal3 enclosure of Via2                                                                                         |0.005      |Max     |
|M3.c1     |5.17. M3.c1 Min. Metal3 endcap enclosure of Via2 (For vias at Metal3 corners at least one side must be treated as an endcap and for the other sides rule M3.c can be applied.)                                                                                                                                    |0.05       |Max     |
|M3.d      |5.17. M3.d Min. Metal3 area (µm²)                                                                                                |0.144      |Max     |
|M4.c      |5.17. M4.c Min. Metal4 enclosure of Via3                                                                                         |0.005      |Max     |
|M4.c1     |5.17. M4.c1 Min. Metal4 endcap enclosure of Via3 (For vias at Metal4 corners at least one side must be treated as an endcap and for the other sides rule M4.c can be applied.)                                                                                                                                    |0.05       |Max     |
|M4.d      |5.17. M4.d Min. Metal4 area (µm²)                                                                                                |0.144      |Max     |
|M5.c      |5.17. M5.c Min. Metal5 enclosure of Via4                                                                                         |0.005      |Max     |
|M5.c1     |5.17. M5.c1 Min. Metal5 endcap enclosure of Via4 (For vias at Metal5 corners at least one side must be treated as an endcap and for the other sides rule M5.c can be applied.)                                                                                                                                    |0.05       |Max     |
|M5.d      |5.17. M5.d Min. Metal5 area (µm²)                                                                                                |0.144      |Max     |
|M1Fil.a1  |5.18. M1Fil.a1 Min. Metal1:filler width                                                                                          |1          |Max     |
|M1Fil.b   |5.18. M1Fil.b Min. Metal1:filler space                                                                                           |0.42       |Max     |
|M1Fil.c   |5.18. M1Fil.c Min. Metal1:filler space to Metal1                                                                                 |0.42       |Max     |
|M1Fil.d   |5.18. M1Fil.d Min. Metal1:filler space to TRANS                                                                                  |1          |Max     |
|M2Fil.a1  |5.18. M2Fil.a1 Min. Metal2:filler width                                                                                          |1          |Max     |
|M2Fil.b   |5.18. M2Fil.b Min. Metal2:filler space                                                                                           |0.42       |Max     |
|M2Fil.c   |5.18. M2Fil.c Min. Metal2:filler space to Metal2                                                                                 |0.42       |Max     |
|M2Fil.d   |5.18. M2Fil.d Min. Metal2:filler space to TRANS                                                                                  |1          |Max     |
|M3Fil.a1  |5.18. M3Fil.a1 Min. Metal3:filler width                                                                                          |1          |Max     |
|M3Fil.b   |5.18. M3Fil.b Min. Metal3:filler space                                                                                           |0.42       |Max     |
|M3Fil.c   |5.18. M3Fil.c Min. Metal3:filler space to Metal3                                                                                 |0.42       |Max     |
|M3Fil.d   |5.18. M3Fil.d Min. Metal3:filler space to TRANS                                                                                  |1          |Max     |
|M4Fil.a1  |5.18. M4Fil.a1 Min. Metal4:filler width                                                                                          |1          |Max     |
|M4Fil.b   |5.18. M4Fil.b Min. Metal4:filler space                                                                                           |0.42       |Max     |
|M4Fil.c   |5.18. M4Fil.c Min. Metal4:filler space to Metal4                                                                                 |0.42       |Max     |
|M4Fil.d   |5.18. M4Fil.d Min. Metal4:filler space to TRANS                                                                                  |1          |Max     |
|M5Fil.a1  |5.18. M5Fil.a1 Min. Metal5:filler width                                                                                          |1          |Max     |
|M5Fil.b   |5.18. M5Fil.b Min. Metal5:filler space                                                                                           |0.42       |Max     |
|M5Fil.c   |5.18. M5Fil.c Min. Metal5:filler space to Metal5                                                                                 |0.42       |Max     |
|M5Fil.d   |5.18. M5Fil.d Min. Metal5:filler space to TRANS                                                                                  |1          |Max     |
|V1.b1     |5.19.  V1.b1 Min. Via1 space in an array of more than 3 rows and more then 3 columns  (V1.b1 is only required in one direction. The distance of the other direction must be at least V1.b.)                                                                                                                                 |0.29       |Max     |
|V1.c1     |5.19.  V1.c1 Min. Metal1 endcap enclosure of Via1 (For Via1 at Metal1 corners at  least one side must be treated as an endcap and for the other sides rule V1.c can be applied.)                                                                                                                                    |0.05       |Max     |
|V2.b1     |5.20. V2.b1 Min. Via2 space in an array of more than 3 rows and more then 3,columns (V2.b1 is only required in one direction. The distance of the other direction must be at least V2.b.)                                                                                                                                 |0.29       |Max     |
|V2.c1     |5.20. V2.c1 Min. Metal2 endcap enclosure of Via2 (For Via2 at Metal2 corners at least one side must be treated as an endcap and for the other sides rule V2.c can be applied.)                                                                                                                                    |0.05       |Max     |
|V3.b1     |5.20. V3.b1 Min. Via3 space in an array of more than 3 rows and more then 3,columns (V3.b1 is only required in one direction. The distance of the other direction must be at least V3.b.)                                                                                                                                 |0.29       |Max     |
|V3.c1     |5.20. V3.c1 Min. Metal3 endcap enclosure of Via3 (For Via3 at Metal3 corners at least one side must be treated as an endcap and for the other sides rule V3.c can be applied.)                                                                                                                                    |0.05       |Max     |
|V4.b1     |5.20. V4.b1 Min. Via4 space in an array of more than 3 rows and more then 3,columns (V4.b1 is only required in one direction. The distance of the other direction must be at least V4.b.)                                                                                                                                 |0.29       |Max     |
|V4.c1     |5.20. V4.c1 Min. Metal4 endcap enclosure of Via4 (For Via4 at Metal4 corners at least one side must be treated as an endcap and for the other sides rule V4.c can be applied.)                                                                                                                                    |0.05       |Max     |
|TM1Fil.a                |5.23.  TM1Fil.a Min. TopMetal1:filler width                                                                        |5          |Max     |
|TM1Fil.b                |5.23.  TM1Fil.b Min. TopMetal1:filler space                                                                        |3          |Max     |
|TM1Fil.c                |5.23.  TM1Fil.c Min. TopMetal1:filler space to TopMetal1                                                           |3          |Max     |
|TM1Fil.d                |5.23. TM1Fil.d Min. TopMetal1:filler space to TRANS                                                                |4.9        |Max     |
|TM2Fil.a                |5.26.  TM2Fil.a Min. TopMetal2:filler width                                                                        |5          |Max     |
|TM2Fil.b                |5.26.  TM2Fil.b Min. TopMetal2:filler space                                                                        |3          |Max     |
|TM2Fil.c                |5.26.  TM2Fil.c Min. TopMetal2:filler space to TopMetal2                                                           |3          |Max     |
|TM2Fil.d                |5.26.  TM2Fil.d Min. TopMetal2:filler space to TRANS                                                               |4.9        |Max     |
|npnG2.b                 |6.1.3.  npnG2.b NPN Substrate-Tie must enclose TRANS                                                               |-          |Max     |
|npnG2.c                 |6.1.3.  npnG2.c Min. pSD enclosure of Activ inside NPN Substrate-Tie                                               |0.2        |Max     |
|npnG2.d                 |6.1.3.  npnG2.d Min. unrelated N+Activ, NWell, PWell:block, nBuLay, nSD:block space to TRANS                       |1.21       |Max     |
|npnG2.d1                |6.1.3.  npnG2.d1 Min. unrelated GatPoly space to TRANS                                                             |0.9        |Max     |
|npnG2.d2                |6.1.3.  npnG2.d2 Min. unrelated SalBlock space to TRANS                                                            |0.9        |Max     |
|npnG2.e                 |6.1.3.  npnG2.e Min. unrelated Cont space to TRANS                                                                 |0.27       |Max     |
|npn13G2.a               |6.1.3.  npn13G2.a Min. and max. npn13G2 emitter length                                                             |0.9        |Max     |
|npn13G2L.a              |6.1.3.  npn13G2L.a Min. npn13G2L emitter length                                                                    |1          |Max     |
|npn13G2L.b              |6.1.3.  npn13G2L.b Max. npn13G2L emitter length                                                                    |2.5        |Max     |
|npn13G2V.a              |6.1.3.  npn13G2V.a Min. npn13G2V emitter length                                                                    |1          |Max     |
|npn13G2V.b              |6.1.3.  npn13G2V.b Max. npn13G2V emitter length                                                                    |5          |Max     |
|Rsil.a                  |6.2.  Rsil.a Min. GatPoly width                                                                                    |0.5        |Max     |
|Rsil.b                  |6.2.  Rsil.b Min. RES space to Cont                                                                                |0.12       |Max     |
|Rsil.c                  |6.2.  Rsil.c Min. RES extension over GatPoly                                                                       |0          |Max     |
|Rsil.d                  |6.2.  Rsil.d Min. pSD space to GatPoly                                                                             |0.18       |Max     |
|Rsil.e                  |6.2.  Rsil.e Min. EXTBlock enclosure of GatPoly                                                                    |0.18       |Max     |
|Rsil.f                  |6.2.  Rsil.f Min. RES length                                                                                       |0.5        |Max     |
|Rppd.a                  |6.3.  Rppd.a Min. GatPoly width                                                                                    |0.5        |Max     |
|Rppd.b                  |6.3.  Rppd.b Min. pSD enclosure of GatPoly                                                                         |0.18       |Max     |
|Rppd.c                  |6.3.  Rppd.c Min. and max. SalBlock space to Cont                                                                  |0.2        |Max     |
|Rppd.d                  |6.3.  Rppd.d Min. EXTBlock enclosure of GatPoly                                                                    |0.18       |Max     |
|Rppd.e                  |6.3.  Rppd.e Min. SalBlock length                                                                                  |0.5        |Max     |
|Rhi.a                   |6.4. Rhi.a Min. GatPoly width                                                                                      |0.5        |Max     |
|Rhi.b                   |6.4. Rhi.b pSD and nSD are identical (nSD:drawing is only permitted within Rhigh resistors)                        |-          |Max     |
|Rhi.c                   |6.4. Rhi.c Min. pSD and nSD enclosure of GatPoly                                                                   |0.18       |Max     |
|Rhi.d                   |6.4. Rhi.d Min. and max. SalBlock space to Cont                                                                    |0.2        |Max     |
|Rhi.e                   |6.4. Rhi.e Min. EXTBlock enclosure of GatPoly                                                                      |0.18       |Max     |
|Rhi.f                   |6.4. Rhi.f Min. Salblock length                                                                                    |0.5        |Max     |
|nmosi.b                 |6.5.  nmosi.b Min. nBuLay enclosure of Iso-PWell-Activ (Note 1)                                                    |1.24       |Max     |
|nmosi.c                 |6.5.  nmosi.c Min. NWell space to Iso-PWell-Activ                                                                  |0.39       |Max     |
|nmosi.d                 |6.5.  nmosi.d Min. NWell-nBuLay width forming an unbroken ring around any,Iso-PWell-Activ (Note 2)                 |0.62       |Max     |
|nmosi.f                 |6.5.  nmosi.f Min. nSD:block width to separate ptap in nmosi                                                       |0.62       |Max     |
|nmosi.g                 |6.5.  nmosi.g Min. SalBlock overlap of nSD:block over Activ                                                        |0.15       |Max     |
|Sdiod.a                 |6.7.  Sdiod.a Min. and max. PWell:block enclosure of ContBar                                                       |0.25       |Max     |
|Sdiod.b                 |6.7.  Sdiod.b Min. and max. nSD:block enclosure of ContBar                                                         |0.4        |Max     |
|Sdiod.c                 |6.7.  Sdiod.c Min. and max. SalBlock enclosure of ContBar                                                          |0.45       |Max     |
|Pad.aR                  |6.9.  Pad.aR Min. recommended Pad width                                                                            |30         |Max     |
|Pad.a1                  |6.9.  Pad.a1 Max. Pad width                                                                                        |150        |Max     |
|Pad.bR                  |6.9.  Pad.bR Min. recommended Pad space                                                                            |8.4        |Max     |
|Pad.d                   |6.9.  Pad.d Min. Pad space to EdgeSeal                                                                             |7.5        |Max     |
|Pad.dR                  |6.9.  Pad.dR Min. recommended Pad to EdgeSeal space                                                                |25         |Max     |
|Pad.d1R                 |6.9.  Pad.d1R Min. recommended Pad to Activ (inside chip area) space                                               |11.2       |Max     |
|Pad.eR_M1               |6.9.  Pad.eR_M1 Min. recommended Metal1 exit width                                                                 |7          |Max     |
|Pad.eR_M2               |6.9.  Pad.eR_M2 Min. recommended Metal2 exit width                                                                 |7          |Max     |
|Pad.eR_M3               |6.9.  Pad.eR_M3 Min. recommended Metal3 exit width                                                                 |7          |Max     |
|Pad.eR_M4               |6.9.  Pad.eR_M4 Min. recommended Metal4 exit width                                                                 |7          |Max     |
|Pad.eR_M5               |6.9.  Pad.eR_M5 Min. recommended Metal5 exit width                                                                 |7          |Max     |
|Pad.eR_TM1              |6.9.  Pad.eR_TM1 Min. recommended TopMetal1 exit width                                                             |7          |Max     |
|Pad.eR_TM2              |6.9.  Pad.eR_TM2 Min. recommended TopMetal2 exit width                                                             |7          |Max     |
|Pad.gR                  |6.9.  Pad.gR TopMetal1 (within dfpad) enclosure of TopVia2                                                         |1.4        |Max     |
|Pad.jR                  |6.9.  Pad.jR No devices under Pad allowed                                                                          |-          |Max     |
|Pad.kR                  |6.9.  Pad.kR TopVia2 under Pad not allowed                                                                         |-          |Max     |
|Padc.d                  |6.9.  Padc.d Min. CuPillarPad space to EdgeSeal                                                                    |30         |Max     |
|Seal.a_Activ            |6.10. Seal.a_Activ Min. EdgeSeal-Activ width                                                                       |3.5        |Max     |
|Seal.a_Metal1           |6.10. Seal.a_Metal1 Min. EdgeSeal-Metal1 width                                                                     |3.5        |Max     |
|Seal.a_Metal2           |6.10. Seal.a_Metal2 Min. EdgeSeal-Metal2 width                                                                     |3.5        |Max     |
|Seal.a_Metal3           |6.10. Seal.a_Metal3 Min. EdgeSeal-Metal3 width                                                                     |3.5        |Max     |
|Seal.a_Metal4           |6.10. Seal.a_Metal4 Min. EdgeSeal-Metal4 width                                                                     |3.5        |Max     |
|Seal.a_Metal5           |6.10. Seal.a_Metal5 Min. EdgeSeal-Metal5 width                                                                     |3.5        |Max     |
|Seal.a_TopMetal1        |6.10. Seal.a_TopMetal1 Min. EdgeSeal-TopMetal1  width                                                              |3.5        |Max     |
|Seal.a_TopMetal2        |6.10. Seal.a_TopMetal2 Min. EdgeSeal-TopMetal2 width                                                               |3.5        |Max     |
|Seal.a_pSD              |6.10. Seal.a_pSD Min. EdgeSeal-psD width                                                                           |3.5        |Max     |
|Seal.c                  |6.10.  Seal.c EdgeSeal-Cont ring width                                                                             |0.16       |Max     |
|Seal.c1_Via1            |6.10 Seal.c1_Via1 EdgeSeal-Via1 ring width                                                                         |0.19       |Max     |
|Seal.c1_Via2            |6.10 Seal.c1_Via2 EdgeSeal-Via2 ring width                                                                         |0.19       |Max     |
|Seal.c1_Via3            |6.10 Seal.c1_Via3 EdgeSeal-Via3 ring width                                                                         |0.19       |Max     |
|Seal.c1_Via4            |6.10 Seal.c1_Via4 EdgeSeal-Via4 ring width                                                                         |0.19       |Max     |
|Seal.c2                 |6.10.  Seal.c2 EdgeSeal-TopVia1 ring width                                                                         |0.42       |Max     |
|Seal.c3                 |6.10.  Seal.c3 EdgeSeal-TopVia2 ring width                                                                         |0.9        |Max     |
|Seal.d_Cont             |6.10. Seal.d_Cont Min. EdgeSeal-Activ enclosure of EdgeSeal-Cont                                                   |1.3        |Max     |
|Seal.d_Via1             |6.10. Seal.d_Metal1 Min. EdgeSeal-Activ enclosure of EdgeSeal-Via1                                                 |1.3        |Max     |
|Seal.d_Via2             |6.10. Seal.d_Metal2 Min. EdgeSeal-Activ enclosure of EdgeSeal-Via2                                                 |1.3        |Max     |
|Seal.d_Via3             |6.10. Seal.d_Metal3 Min. EdgeSeal-Activ enclosure of EdgeSeal-Via3                                                 |1.3        |Max     |
|Seal.d_Via4             |6.10. Seal.d_Metal3 Min. EdgeSeal-Activ enclosure of EdgeSeal-Via4                                                 |1.3        |Max     |
|Seal.d_TopVia1          |6.10. Seal.d_Metal1 Min. EdgeSeal-Activ enclosure of EdgeSeal-TopVia1                                              |1.3        |Max     |
|Seal.d_TopVia2          |6.10. Seal.d_Metal1 Min. EdgeSeal-Activ enclosure of EdgeSeal-TopVia2                                              |1.3        |Max     |
|Seal.e                  |6.10.  Seal.e Min. Passiv ring width outside of sealring                                                           |4.2        |Max     |
|Seal.f_Activ            |6.10. Seal.f_Activ Min. Passiv ring outside of sealring space to EdgeSeal-Activ                                    |1          |Max     |
|Seal.f_Metal1           |6.10. Seal.f_Metal1 Min. Passiv ring outside of sealring space to EdgeSeal-Metal1                                  |1          |Max     |
|Seal.f_Metal2           |6.10. Seal.f_Metal2 Min. Passiv ring outside of sealring space to EdgeSeal-Metal2                                  |1          |Max     |
|Seal.f_Metal3           |6.10. Seal.f_Metal3 Min. Passiv ring outside of sealring space to EdgeSeal-Metal3                                  |1          |Max     |
|Seal.f_Metal4           |6.10. Seal.f_Metal4 Min. Passiv ring outside of sealring space to EdgeSeal-Metal4                                  |1          |Max     |
|Seal.f_Metal5           |6.10. Seal.f_Metal5 Min. Passiv ring outside of sealring space to EdgeSeal-Metal5                                  |1          |Max     |
|Seal.f_TopMetal1        |6.10. Seal.f_TopMetal1 Min. Passiv ring outside of sealring space to EdgeSeal-TopMetal1                            |1          |Max     |
|Seal.f_TopMetal2        |6.10. Seal.f_TopMetal2 Min. Passiv ring outside of sealring space to EdgeSeal-TopMetal2                            |1          |Max     |
|MIM.a                   |6.11.  MIM.a Min. MIM width                                                                                        |1.14       |Max     |
|MIM.b                   |6.11.  MIM.b Min. MIM space                                                                                        |0.6        |Max     |
|MIM.e                   |6.11.  MIM.e Min. TopMetal1 space to MIM                                                                           |0.6        |Max     |
|MIM.f                   |6.11.  MIM.f Min. MIM area per MIM device (µm²)                                                                    |1.3        |Max     |
|MIM.g                   |6.11.  MIM.g Max. MIM area per MIM device (µm²)                                                                    |5625       |Max     |
|MIM.h                   |6.11.  MIM.h TopVia1 must be over MIM                                                                              |-          |Max     |
|LU.a                    |7.2.  LU.a Max. space from any portion of P+Activ inside NWell to an nSD-NWell tie                                 |20         |Max     |
|LU.c                    |7.2.  LU.c Max. extension of an abutted NWell tie beyond Cont                                                      |6          |Max     |
|LU.c1                   |7.2.  LU.c1 Max. extension of an abutted substrate tie beyond Cont                                                 |6          |Max     |
|LU.d                    |7.2.  LU.d Max. extension of NWell tie Activ tie beyond Cont                                                       |6          |Max     |
|LU.d1                   |7.2.  LU.d1 Max. extension of an substrate tie Activ beyond Cont                                                   |6          |Max     |
|Slt.a_M1                |7.3. Slt.a_M1 Min. Metal1:slit width                                                                               |2.8        |Max     |
|Slt.a_M2                |7.3. Slt.a_M2 Min. Metal2:slit width                                                                               |2.8        |Max     |
|Slt.a_M3                |7.3. Slt.a_M3 Min. Metal3:slit width                                                                               |2.8        |Max     |
|Slt.a_M4                |7.3. Slt.a_M4 Min. Metal4:slit width                                                                               |2.8        |Max     |
|Slt.a_M5                |7.3. Slt.a_M5 Min. Metal5:slit width                                                                               |2.8        |Max     |
|Slt.a_TM1               |7.3. Slt.a_TM1 Min. TopMetal1:slit width                                                                           |2.8        |Max     |
|Slt.a_TM2               |7.3. Slt.a_TM2 Min. TopMetal2:slit width                                                                           |2.8        |Max     |
|Slt.b_M1                |7.3. Slt.b_M1 Max. Metal1:slit width                                                                               |20         |Max     |
|Slt.b_M2                |7.3. Slt.b_M2 Max. Metal2:slit width                                                                               |20         |Max     |
|Slt.b_M3                |7.3. Slt.b_M3 Max. Metal3:slit width                                                                               |20         |Max     |
|Slt.b_M4                |7.3. Slt.b_M4 Max. Metal4:slit width                                                                               |20         |Max     |
|Slt.b_M5                |7.3. Slt.b_M5 Max. Metal5:slit width                                                                               |20         |Max     |
|Slt.b_TM1               |7.3. Slt.b_TM1 Max. TopMetal1:slit width                                                                           |20         |Max     |
|Slt.b_TM2               |7.3. Slt.b_TM2 Max. TopMetal2:slit width                                                                           |20         |Max     |
|Slt.c_M1                |7.3. Slt.c_M1 Max. Metal1 width without requiring a slit                                                           |30         |Max     |
|Slt.c_M2                |7.3. Slt.c_M2 Max. Metal2 width without requiring a slit                                                           |30         |Max     |
|Slt.c_M3                |7.3. Slt.c_M3 Max. Metal3 width without requiring a slit                                                           |30         |Max     |
|Slt.c_M4                |7.3. Slt.c_M4 Max. Metal4 width without requiring a slit                                                           |30         |Max     |
|Slt.c_M5                |7.3. Slt.c_M5 Max. Metal5 width without requiring a slit                                                           |30         |Max     |
|Slt.c_TM1               |7.3. Slt.c_TM1 Max. TopMetal1 width without requiring a slit                                                       |30         |Max     |
|Slt.c_TM2               |7.3. Slt.c_TM2 Max. TopMetal2 width without requiring a slit                                                       |30         |Max     |
|Slt.e_M1                |7.3. Slt.e_M1 No Metal1:slit required on bond pads                                                                 |-          |Max     |
|Slt.e_M2                |7.3. Slt.e_M2 No Metal2:slit required on bond pads                                                                 |-          |Max     |
|Slt.e_M3                |7.3. Slt.e_M3 No Metal3:slit required on bond pads                                                                 |-          |Max     |
|Slt.e_M4                |7.3. Slt.e_M4 No Metal4:slit required on bond pads                                                                 |-          |Max     |
|Slt.e_M5                |7.3. Slt.e_M5 No Metal5:slit required on bond pads                                                                 |-          |Max     |
|Slt.e_TM1               |7.3. Slt.e_TM1 No TopMetal1:slit required on bond pads                                                             |-          |Max     |
|Slt.e_TM2               |7.3. Slt.e_TM2 No TopMetal1:slit required on bond pads                                                             |-          |Max     |
|Slt.f_M1                |7.3. Slt.f_M1 Min. Metal1 enclosure of Metal1:slit                                                                 |1          |Max     |
|Slt.f_M2                |7.3. Slt.f_M2 Min. Metal2 enclosure of Metal2:slit                                                                 |1          |Max     |
|Slt.f_M3                |7.3. Slt.f_M3 Min. Metal3 enclosure of Metal3:slit                                                                 |1          |Max     |
|Slt.f_M4                |7.3. Slt.f_M4 Min. Metal4 enclosure of Metal4:slit                                                                 |1          |Max     |
|Slt.f_M5                |7.3. Slt.f_M5 Min. Metal5 enclosure of Metal5:slit                                                                 |1          |Max     |
|Slt.f_TM1               |7.3. Slt.f_TM1 Min. TopMetal1 enclosure of TopMetal1:slit                                                          |1          |Max     |
|Slt.f_TM2               |7.3. Slt.f_TM2 Min. TopMetal2 enclosure of TopMetal2:slit                                                          |1          |Max     |
|Slt.g_M5                |7.3.  Slt.g Min. Metal5:slit space to MIM                                                                          |0.6        |Max     |
|Slt.g_TM1               |7.3.  Slt.g Min. TopMetal1:slit space to MIM                                                                       |0.6        |Max     |
|Slt.h1                  |7.3.  Slt.h1 Min. Metal1:slit space to Cont and Via1                                                               |0.3        |Max     |
|Slt.h2_M2               |7.3. Slt.h2_M2 Min. Metal2:slit space to Via1 and Via2                                                             |0.3        |Max     |
|Slt.h2_M3               |7.3. Slt.h2_M3 Min. Metal3:slit space to Via2 and Via3                                                             |0.3        |Max     |
|Slt.h2_M4               |7.3. Slt.h2_M4 Min. Metal4:slit space to Via3 and Via4                                                             |0.3        |Max     |
|Slt.h2_M5               |7.3. Slt.h2_M5 Min. Metal5:slit space to Via4 and Via5                                                             |0.3        |Max     |
|Slt.h3                  |7.3.  Slt.h3 Min. TopMetal1:slit space to TopVia1 and TopVia2                                                      |1          |Max     |
|Slt.h4                  |7.3.  Slt.h4 Min. TopMetal2:slit space to TopVia2                                                                  |1          |Max     |
|NW.c1.DigiBnd           |8.1.1. NW.c1.DigiBnd Min. NWell enclosure of P+Activ inside ThickGateOx                                            |0.31       |Max     |
|NW.d1.DigiBnd           |8.1.1. NW.d1.DigiBnd Min. NWell space to external N+Activ inside ThickGateOx                                       |0.31       |Max     |
|NW.e1.DigiBnd           |8.1.1. NW.e1.DigiBnd Min. NWell enclosure of NWell tie surrounded  entirely by NWell in N+Activ inside ThickGateOx |0.24       |Max     |
|NW.f1.DigiBnd           |8.1.1. NW.f1.DigiBnd Min. NWell space to substrate tie in P+Activ inside ThickGateOx                               |0.24       |Max     |
|Cnt.c.DigiBnd           |8.1.2.  Cnt.c.DigiBnd Min. Activ enclosure of Cont                                                                 |0.05       |Max     |
|LBE.b2                  |9.1.  LBE.b2 Min. LBE area (µm²)                                                                                   |30000      |Max     |
|LBE.e                   |9.1.  LBE.e Min. LBE space to dfpad and Passiv                                                                     |50         |Max     |
|LBE.f                   |9.1.  LBE.f Min. LBE space to Activ                                                                                |30         |Max     |
|TSV_G.a                 |10.1.  TSV_G.a DeepVia has to be a ring structure                                                                  |-          |Max     |
|TSV_G.b                 |10.1.  TSV_G.b Min. and max. DeepVia width                                                                         |3          |Max     |
|TSV_G.c                 |10.1.  TSV_G.c DeepVia ring diameter                                                                               |25         |Max     |
|TSV_G.d                 |10.1.  TSV_G.d Min. DeepVia space                                                                                  |25         |Max     |
|TSV_G.e                 |10.1.  TSV_G.e Min. DeepVia space to Activ, Activ:filler, GatPoly, GatPoly:filler and Cont                         |5          |Max     |
|TSV_G.f                 |10.1.  TSV_G.f Min. PWell:block enclosure of DeepVia                                                               |2.5        |Max     |
|TSV_G.g                 |10.1.  TSV_G.g Min. Metal1 enclosure of DeepVia ring structure                                                     |1.5        |Max     |
|TSV_G.i                 |10.1.  TSV_G.i Max. global DeepVia density [%]                                                                     |1          |Max     |
|TSV_G.j                 |10.1.  TSV_G.j Max. DeepVia coverage ratio for any 500.0 x 500.0 µm² chip area[%]                                  |10         |Max     |
|OffGrid.NWell           |3.1. OffGrid.NWell NWell layer is offgrid. (All features are on a drawing grid of 5 nm)                            |-          |Max     |
|OffGrid.PWell           |3.1. OffGrid.PWell PWell layer is offgrid. (All features are on a drawing grid of 5 nm)                            |-          |Max     |
|OffGrid.PWell_block     |3.1. OffGrid.PWell_block PWell_block layer is offgrid. (All features are on a drawing grid of 5 nm)                |-          |Max     |
|OffGrid.nBuLay          |3.1. OffGrid.nBuLay nBuLay layer is offgrid. (All features are on a drawing grid of 5 nm)                          |-          |Max     |
|OffGrid.nBuLay_block    |3.1. OffGrid.nBuLay_block nBuLay_block layer is offgrid. (All features are on a drawing grid of 5 nm)              |-          |Max     |
|OffGrid.Activ           |3.1. OffGrid.Activ Activ layer is offgrid. (All features are on a drawing grid of 5 nm)                            |-          |Max     |
|OffGrid.ThickGateOx     |3.1. OffGrid.ThickGateOx ThickGateOx layer is offgrid. (All features are on a drawing grid of 5 nm)                |-          |Max     |
|OffGrid.Activ_filler    |3.1. OffGrid.Activ_filler Activ_filler layer is offgrid. (All features are on a drawing grid of 5 nm)              |-          |Max     |
|OffGrid.GatPoly_filler  |3.1. OffGrid.GatPoly_filler GatPoly_filler layer is offgrid. (All features are on a drawing grid of 5 nm)          |-          |Max     |
|OffGrid.GatPoly         |3.1. OffGrid.GatPoly GatPoly layer is offgrid. (All features are on a drawing grid of 5 nm)                        |-          |Max     |
|OffGrid.pSD             |3.1. OffGrid.pSD pSD layer is offgrid. (All features are on a drawing grid of 5 nm)                                |-          |Max     |
|OffGrid.nSD             |3.1. OffGrid.nSD nSD layer is offgrid. (All features are on a drawing grid of 5 nm)                                |-          |Max     |
|OffGrid.nSD_block       |3.1. OffGrid.nSD_block nSD_block layer is offgrid. (All features are on a drawing grid of 5 nm)                    |-          |Max     |
|OffGrid.EXTBlock        |3.1. OffGrid.EXTBlock EXTBlock layer is offgrid. (All features are on a drawing grid of 5 nm)                      |-          |Max     |
|OffGrid.SalBlock        |3.1. OffGrid.SalBlock SalBlock layer is offgrid. (All features are on a drawing grid of 5 nm)                      |-          |Max     |
|OffGrid.Cont            |3.1. OffGrid.Cont Cont layer is offgrid. (All features are on a drawing grid of 5 nm)                              |-          |Max     |
|OffGrid.Activ_nofill    |3.1. OffGrid.Activ_nofill Activ_nofill layer is offgrid. (All features are on a drawing grid of 5 nm)              |-          |Max     |
|OffGrid.GatPoly_nofill  |3.1. OffGrid.GatPoly_nofill GatPoly_nofill layer is offgrid. (All features are on a drawing grid of 5 nm)          |-          |Max     |
|OffGrid.Metal1          |3.1. OffGrid.Metal1 Metal1 layer is offgrid. (All features are on a drawing grid of 5 nm)                          |-          |Max     |
|OffGrid.Via1            |3.1. OffGrid.Via1 Via1 layer is offgrid. (All features are on a drawing grid of 5 nm)                              |-          |Max     |
|OffGrid.Metal2          |3.1. OffGrid.Metal2 Metal2 layer is offgrid. (All features are on a drawing grid of 5 nm)                          |-          |Max     |
|OffGrid.Via2            |3.1. OffGrid.Via2 Via2 layer is offgrid. (All features are on a drawing grid of 5 nm)                              |-          |Max     |
|OffGrid.Metal3          |3.1. OffGrid.Metal3 Metal3 layer is offgrid. (All features are on a drawing grid of 5 nm)                          |-          |Max     |
|OffGrid.Via3            |3.1. OffGrid.Via3 Via3 layer is offgrid. (All features are on a drawing grid of 5 nm)                              |-          |Max     |
|OffGrid.Metal4          |3.1. OffGrid.Metal4 Metal4 layer is offgrid. (All features are on a drawing grid of 5 nm)                          |-          |Max     |
|OffGrid.Via4            |3.1. OffGrid.Via4 Via4 layer is offgrid. (All features are on a drawing grid of 5 nm)                              |-          |Max     |
|OffGrid.Metal5          |3.1. OffGrid.Metal5 Metal5 layer is offgrid. (All features are on a drawing grid of 5 nm)                          |-          |Max     |
|OffGrid.MIM             |3.1. OffGrid.MIM MIM layer is offgrid. (All features are on a drawing grid of 5 nm)                                |-          |Max     |
|OffGrid.Vmim            |3.1. OffGrid.Vmim Vmim layer is offgrid. (All features are on a drawing grid of 5 nm)                              |-          |Max     |
|OffGrid.TopVia1         |3.1. OffGrid.TopVia1 TopVia1 layer is offgrid. (All features are on a drawing grid of 5 nm)                        |-          |Max     |
|OffGrid.TopMetal1       |3.1. OffGrid.TopMetal1 TopMetal1 layer is offgrid. (All features are on a drawing grid of 5 nm)                    |-          |Max     |
|OffGrid.TopVia2         |3.1. OffGrid.TopVia2 TopVia2 layer is offgrid. (All features are on a drawing grid of 5 nm)                        |-          |Max     |
|OffGrid.TopMetal2       |3.1. OffGrid.TopMetal2 TopMetal2 layer is offgrid. (All features are on a drawing grid of 5 nm)                    |-          |Max     |
|OffGrid.Passiv          |3.1. OffGrid.Passiv Passiv layer is offgrid. (All features are on a drawing grid of 5 nm)                          |-          |Max     |
|OffGrid.Metal1_filler   |3.1. OffGrid.Metal1_filler Metal1_filler layer is offgrid. (All features are on a drawing grid of 5 nm)            |-          |Max     |
|OffGrid.Metal2_filler   |3.1. OffGrid.Metal2_filler Metal2_filler layer is offgrid. (All features are on a drawing grid of 5 nm)            |-          |Max     |
|OffGrid.Metal3_filler   |3.1. OffGrid.Metal3_filler Metal3_filler layer is offgrid. (All features are on a drawing grid of 5 nm)            |-          |Max     |
|OffGrid.Metal4_filler   |3.1. OffGrid.Metal4_filler Metal4_filler layer is offgrid. (All features are on a drawing grid of 5 nm)            |-          |Max     |
|OffGrid.Metal5_filler   |3.1. OffGrid.Metal5_filler Metal5_filler layer is offgrid. (All features are on a drawing grid of 5 nm)            |-          |Max     |
|OffGrid.TopMetal1_filler|3.1. OffGrid.TopMetal1_filler TopMetal1_filler layer is offgrid. (All features are on a drawing grid of 5 nm)      |-          |Max     |
|OffGrid.TopMetal2_filler|3.1. OffGrid.TopMetal2_filler TopMetal2_filler layer is offgrid. (All features are on a drawing grid of 5 nm)      |-          |Max     |
|OffGrid.Metal1_nofill   |3.1. OffGrid.Metal1_nofill Metal1_nofill layer is offgrid. (All features are on a drawing grid of 5 nm)            |-          |Max     |
|OffGrid.Metal2_nofill   |3.1. OffGrid.Metal2_nofill Metal2_nofill layer is offgrid. (All features are on a drawing grid of 5 nm)            |-          |Max     |
|OffGrid.Metal3_nofill   |3.1. OffGrid.Metal3_nofill Metal3_nofill layer is offgrid. (All features are on a drawing grid of 5 nm)            |-          |Max     |
|OffGrid.Metal4_nofill   |3.1. OffGrid.Metal4_nofill Metal4_nofill layer is offgrid. (All features are on a drawing grid of 5 nm)            |-          |Max     |
|OffGrid.Metal5_nofill   |3.1. OffGrid.Metal5_nofill Metal5_nofill layer is offgrid. (All features are on a drawing grid of 5 nm)            |-          |Max     |
|OffGrid.TopMetal1_nofill|3.1. OffGrid.TopMetal1_nofill TopMetal1_nofill layer is offgrid. (All features are on a drawing grid of 5 nm)      |-          |Max     |
|OffGrid.TopMetal2_nofill|3.1. OffGrid.TopMetal2_nofill TopMetal2_nofill layer is offgrid. (All features are on a drawing grid of 5 nm)      |-          |Max     |
|OffGrid.NoMetFiller     |3.1. OffGrid.NoMetFiller NoMetFiller layer is offgrid. (All features are on a drawing grid of 5 nm)                |-          |Max     |
|OffGrid.Metal1_slit     |3.1. OffGrid.Metal1_slit Metal1_slit layer is offgrid. (All features are on a drawing grid of 5 nm)                |-          |Max     |
|OffGrid.Metal2_slit     |3.1. OffGrid.Metal2_slit Metal2_slit layer is offgrid. (All features are on a drawing grid of 5 nm)                |-          |Max     |
|OffGrid.Metal3_slit     |3.1. OffGrid.Metal3_slit Metal3_slit layer is offgrid. (All features are on a drawing grid of 5 nm)                |-          |Max     |
|OffGrid.Metal4_slit     |3.1. OffGrid.Metal4_slit Metal4_slit layer is offgrid. (All features are on a drawing grid of 5 nm)                |-          |Max     |
|OffGrid.Metal5_slit     |3.1. OffGrid.Metal5_slit Metal5_slit layer is offgrid. (All features are on a drawing grid of 5 nm)                |-          |Max     |
|OffGrid.TopMetal1_slit  |3.1. OffGrid.TopMetal1_slit TopMetal1_slit layer is offgrid. (All features are on a drawing grid of 5 nm)          |-          |Max     |
|OffGrid.TopMetal2_slit  |3.1. OffGrid.TopMetal2_slit TopMetal2_slit layer is offgrid. (All features are on a drawing grid of 5 nm)          |-          |Max     |
|OffGrid.EdgeSeal        |3.1. OffGrid.EdgeSeal EdgeSeal layer is offgrid. (All features are on a drawing grid of 5 nm)                      |-          |Max     |
|OffGrid.EmWind          |3.1. OffGrid.EmWind EmWind layer is offgrid. (All features are on a drawing grid of 5 nm)                          |-          |Max     |
|OffGrid.dfpad           |3.1. OffGrid.dfpad dfpad layer is offgrid. (All features are on a drawing grid of 5 nm)                            |-          |Max     |
|OffGrid.Polimide        |3.1. OffGrid.Polimide Polimide layer is offgrid. (All features are on a drawing grid of 5 nm)                      |-          |Max     |
|OffGrid.TRANS           |3.1. OffGrid.TRANS TRANS layer is offgrid. (All features are on a drawing grid of 5 nm)                            |-          |Max     |
|OffGrid.IND             |3.1. OffGrid.IND IND layer is offgrid. (All features are on a drawing grid of 5 nm)                                |-          |Max     |
|OffGrid.RES             |3.1. OffGrid.RES RES layer is offgrid. (All features are on a drawing grid of 5 nm)                                |-          |Max     |
|OffGrid.Recog_diode     |3.1. OffGrid.Recog_diode Recog_diode layer is offgrid. (All features are on a drawing grid of 5 nm)                |-          |Max     |
|OffGrid.Recog_esd       |3.1. OffGrid.Recog_esd Recog_esd layer is offgrid. (All features are on a drawing grid of 5 nm)                    |-          |Max     |
|OffGrid.DigiBnd         |3.1. OffGrid.DigiBnd DigiBnd layer is offgrid. (All features are on a drawing grid of 5 nm)                        |-          |Max     |
|OffGrid.DigiSub         |3.1. OffGrid.DigiSub DigiSub layer is offgrid. (All features are on a drawing grid of 5 nm)                        |-          |Max     |
|OffGrid.dfpad_pillar    |3.1. OffGrid.dfpad_pillar dfpad_pillar layer is offgrid. (All features are on a drawing grid of 5 nm)              |-          |Max     |
|OffGrid.dfpad_sbump     |3.1. OffGrid.dfpad_sbump dfpad_sbump layer is offgrid. (All features are on a drawing grid of 5 nm)                |-          |Max     |
|OffGrid.DeepVia         |3.1. OffGrid.DeepVia DeepVia layer is offgrid. (All features are on a drawing grid of 5 nm)                        |-          |Max     |
|OffGrid.LBE             |3.1. OffGrid.LBE LBE layer is offgrid. (All features are on a drawing grid of 5 nm)                                |-          |Max     |
|OffGrid.recog_tsv       |3.1. OffGrid.recog_tsv recog_tsv layer is offgrid. (All features are on a drawing grid of 5 nm)                    |-          |Max     |
|OffGrid.PolyRes         |3.1. OffGrid.PolyRes PolyRes layer is offgrid. (All features are on a drawing grid of 5 nm)                        |-          |Max     |
|Non90_Cont              |3.1. Non90_Cont Cont layer only allowed angles are 90, 180 degrees.                                                |-          |Max     |
|Non90_Via1              |3.1 Non90_Via1 Via1 layer only allowed angles are 90, 180 degrees.                                                 |-          |Max     |
|Non90_Via2              |3.1 Non90_Via2 Via2 layer only allowed angles are 90, 180 degrees.                                                 |-          |Max     |
|Non90_Via3              |3.1 Non90_Via3 Via3 layer only allowed angles are 90, 180 degrees.                                                 |-          |Max     |
|Non90_Via4              |3.1 Non90_Via4 Via4 layer only allowed angles are 90, 180 degrees.                                                 |-          |Max     |
|Non90_Vmim              |3.1 Non90_Vmim Vmim layer only allowed angles are 90, 180 degrees.                                                 |-          |Max     |
|Non90_TopVia1           |3.1 Non90_TopVia1 TopVia1 layer only allowed angles are 90, 180 degrees.                                           |-          |Max     |
|Non90_TopVia2           |3.1 Non90_TopVia2 TopVia2 layer only allowed angles are 90, 180 degrees.                                           |-          |Max     |
|non45R_GatPoly          |3.1. non45R_GatPoly GatPoly layer is only allowed on 90, 135, 180, 225, and 270 degree angles.                     |-          |Max     |
|non45R_Activ            |3.1. non45R_Activ Activ layer is only allowed on 90, 135, 180, 225, and 270 degree angles.                         |-          |Max     |
|non45R_Metal1           |3.1. non45R_Metal1 Metal1 layer is only allowed on 90, 135, 180, 225, and 270 degree angles.                       |-          |Max     |
|non45R_Metal2           |3.1. non45R_Metal2 Metal2 layer is only allowed on 90, 135, 180, 225, and 270 degree angles.                       |-          |Max     |
|non45R_Metal3           |3.1. non45R_Metal3 Metal3 layer is only allowed on 90, 135, 180, 225, and 270 degree angles.                       |-          |Max     |
|non45R_Metal4           |3.1. non45R_Metal4 Metal4 layer is only allowed on 90, 135, 180, 225, and 270 degree angles.                       |-          |Max     |
|non45R_Metal5           |3.1. non45R_Metal5 Metal5 layer is only allowed on 90, 135, 180, 225, and 270 degree angles.                       |-          |Max     |
|non45R_TopMetal1        |3.1. non45R_TopMetal1 TopMetal1 layer is only allowed on 90, 135, 180, 225, and 270 degree angles.                 |-          |Max     |
|non45R_TopMetal2        |3.1. non45R_TopMetal2 TopMetal2 layer is only allowed on 90, 135, 180, 225, and 270 degree angles.                 |-          |Max     |
|acutAngle_NWell         |3.1. acutAngle_NWell NWell layer with acute angle < 87 is not allowed.                                             |-          |Max     |
|acutAngle_PWell         |3.1. acutAngle_PWell PWell layer with acute angle < 87 is not allowed.                                             |-          |Max     |
|acutAngle_PWell_block   |3.1. acutAngle_PWell_block PWell_block layer with acute angle < 87 is not allowed.                                 |-          |Max     |
|acutAngle_nBuLay        |3.1. acutAngle_nBuLay nBuLay layer with acute angle < 87 is not allowed.                                           |-          |Max     |
|acutAngle_nBuLay_block  |3.1. acutAngle_nBuLay_block nBuLay_block layer with acute angle < 87 is not allowed.                               |-          |Max     |
|acutAngle_Activ         |3.1. acutAngle_Activ Activ layer with acute angle < 87 is not allowed.                                             |-          |Max     |
|acutAngle_ThickGateOx   |3.1. acutAngle_ThickGateOx ThickGateOx layer with acute angle < 87 is not allowed.                                 |-          |Max     |
|acutAngle_GatPoly       |3.1. acutAngle_GatPoly GatPoly layer with acute angle < 87 is not allowed.                                         |-          |Max     |
|acutAngle_pSD           |3.1. acutAngle_pSD pSD layer with acute angle < 87 is not allowed.                                                 |-          |Max     |
|acutAngle_nSD           |3.1. acutAngle_nSD nSD layer with acute angle < 87 is not allowed.                                                 |-          |Max     |
|acutAngle_nSD_block     |3.1. acutAngle_nSD_block nSD_block layer with acute angle < 87 is not allowed.                                     |-          |Max     |
|acutAngle_EXTBlock      |3.1. acutAngle_EXTBlock EXTBlock layer with acute angle < 87 is not allowed.                                       |-          |Max     |
|acutAngle_SalBlock      |3.1. acutAngle_SalBlock SalBlock layer with acute angle < 87 is not allowed.                                       |-          |Max     |
|acutAngle_Cont          |3.1. acutAngle_Cont Cont layer with acute angle < 87 is not allowed.                                               |-          |Max     |
|acutAngle_Metal1        |3.1. acutAngle_Metal1 Metal1 layer with acute angle < 87 is not allowed.                                           |-          |Max     |
|acutAngle_Via1          |3.1. acutAngle_Via1 Via1 layer with acute angle < 87 is not allowed.                                               |-          |Max     |
|acutAngle_Metal2        |3.1. acutAngle_Metal2 Metal2 layer with acute angle < 87 is not allowed.                                           |-          |Max     |
|acutAngle_Via2          |3.1. acutAngle_Via2 Via2 layer with acute angle < 87 is not allowed.                                               |-          |Max     |
|acutAngle_Metal3        |3.1. acutAngle_Metal3 Metal3 layer with acute angle < 87 is not allowed.                                           |-          |Max     |
|acutAngle_Via3          |3.1. acutAngle_Via3 Via3 layer with acute angle < 87 is not allowed.                                               |-          |Max     |
|acutAngle_Metal4        |3.1. acutAngle_Metal4 Metal4 layer with acute angle < 87 is not allowed.                                           |-          |Max     |
|acutAngle_Via4          |3.1. acutAngle_Via4 Via4 layer with acute angle < 87 is not allowed.                                               |-          |Max     |
|acutAngle_Metal5        |3.1. acutAngle_Metal5 Metal5 layer with acute angle < 87 is not allowed.                                           |-          |Max     |
|acutAngle_TopVia1       |3.1. acutAngle_TopVia1 TopVia1 layer with acute angle < 87 is not allowed.                                         |-          |Max     |
|acutAngle_TopMetal1     |3.1. acutAngle_TopMetal1 TopMetal1 layer with acute angle < 87 is not allowed.                                     |-          |Max     |
|acutAngle_TopVia2       |3.1. acutAngle_TopVia2 TopVia2 layer with acute angle < 87 is not allowed.                                         |-          |Max     |
|acutAngle_Vmim          |3.1. acutAngle_Vmim Vmim layer with acute angle < 87 is not allowed.                                               |-          |Max     |
|acutAngle_TopMetal2     |3.1. acutAngle_TopMetal2 TopMetal2 layer with acute angle < 87 is not allowed.                                     |-          |Max     |
|acutAngle_Passiv        |3.1. acutAngle_Passiv Passiv layer with acute angle < 87 is not allowed.                                           |-          |Max     |
|acutAngle_MIM           |3.1. acutAngle_MIM MIM layer with acute angle < 87 is not allowed.                                                 |-          |Max     |
|acutAngle_PolyRes       |3.1. acutAngle_PolyRes PolyRes layer with acute angle < 87 is not allowed.                                         |-          |Max     |
|acutAngle_EdgeSeal      |3.1. acutAngle_EdgeSeal EdgeSeal layer with acute angle < 87 is not allowed.                                       |-          |Max     |
|acutAngle_EmWind        |3.1. acutAngle_EmWind EmWind layer with acute angle < 87 is not allowed.                                           |-          |Max     |
|acutAngle_dfpad         |3.1. acutAngle_dfpad dfpad layer with acute angle < 87 is not allowed.                                             |-          |Max     |
|acutAngle_dfpad_pillar  |3.1. acutAngle_dfpad_pillar dfpad_pillar layer with acute angle < 87 is not allowed.                               |-          |Max     |
|acutAngle_dfpad_sbump   |3.1. acutAngle_dfpad_sbump dfpad_sbump layer with acute angle < 87 is not allowed.                                 |-          |Max     |
|acutAngle_Polimide      |3.1. acutAngle_Polimide Polimide layer with acute angle < 87 is not allowed.                                       |-          |Max     |
|acutAngle_TRANS         |3.1. acutAngle_TRANS TRANS layer with acute angle < 87 is not allowed.                                             |-          |Max     |
|acutAngle_IND           |3.1. acutAngle_IND IND layer with acute angle < 87 is not allowed.                                                 |-          |Max     |
|acutAngle_RES           |3.1. acutAngle_RES RES layer with acute angle < 87 is not allowed.                                                 |-          |Max     |
|acutAngle_DeepVia       |3.1. acutAngle_DeepVia DeepVia layer with acute angle < 87 is not allowed.                                         |-          |Max     |
|acutAngle_LBE           |3.1. acutAngle_LBE LBE layer with acute angle < 87 is not allowed.                                                 |-          |Max     |
|acutAngle_Recog_diode   |3.1. acutAngle_Recog_diode Recog_diode layer with acute angle < 87 is not allowed.                                 |-          |Max     |
|acutAngle_Recog_esd     |3.1. acutAngle_Recog_esd Recog_esd layer with acute angle < 87 is not allowed.                                     |-          |Max     |
|acutAngle_Recog_tsv     |3.1. acutAngle_Recog_tsv Recog_tsv layer with acute angle < 87 is not allowed.                                     |-          |Max     |
|acutAngle_DigiBnd       |3.1. acutAngle_DigiBnd DigiBnd layer with acute angle < 87 is not allowed.                                         |-          |Max     |
|acutAngle_DigiSub       |3.1. acutAngle_DigiSub DigiSub layer with acute angle < 87 is not allowed.                                         |-          |Max     |
|acutAngle_Substrate     |3.1. acutAngle_Substrate Substrate layer with acute angle < 87 is not allowed.                                     |-          |Max     |
