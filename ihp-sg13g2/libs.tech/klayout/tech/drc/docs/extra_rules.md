|Rule                      |Description                                                                              |Value (um)    |
|--------------------------|-----------------------------------------------------------------------------------------|--------------|
| NW.a                     | Min. NWell width                                                                        | 0.62         |
| NW.d1                    | Min. NWell space to external N+Activ inside ThickGateOx                                 | 0.62         |
| NW.f                     | Min. NWell space to substrate tie in P+Activ not inside ThickGateOx                     | 0.24         |
| NW.f1                    | Min. NWell space to substrate tie in P+Activ inside ThickGateOx                         | 0.62         |
| PWB.a                    | Min. PWell:block width                                                                  | 0.62         |
| PWB.b                    | Min. PWell:block space or notch                                                         | 0.62         |
| PWB.c                    | Min. PWell:block space to unrelated NWell                                               | 0.62         |
| NBL.a                    | Min. nBuLay width                                                                       | 1            |
| NBLB.a                   | Min. nBuLay:block width                                                                 | 1.5          |
| NBLB.b                   | Min. nBuLay:block space or notch                                                        | 1            |
| NBLB.c                   | Min. nBuLay enclosure of nBuLay:block                                                   | 1            |
| NBLB.d                   | Min. nBuLay:block space to unrelated nBuLay                                             | 1.5          |
| Act.d                    | Min. Activ area (um2)                                                                   | 0.122        |
| Act.e                    | Min. Activ enclosed area (um2)                                                          | 0.15         |
| AFil.a                   | Max. Activ:filler width                                                                 | 5            |
| AFil.a1                  | Min. Activ:filler width                                                                 | 1            |
| AFil.b                   | Min. Activ:filler space                                                                 | 0.42         |
| TGO.a                    | Min. ThickGateOx extension over Activ                                                   | 0.27         |
| TGO.b                    | Min. space between ThickGateOx and Activ outside thick gate oxide region                | 0.27         |
| TGO.c                    | Min. ThickGateOx extension over GatPoly over Activ                                      | 0.34         |
| TGO.d                    | Min. space between ThickGateOx and GatPoly over Activ outside thick gate oxide region   | 0.34         |
| TGO.e                    | Min. ThickGateOx space (merge if less than this value)                                  | 0.86         |
| Gat.a3                   | Min. GatPoly width for channel length of 3.3 V NFET                                     | 0.45         |
| Gat.a4                   | Min. GatPoly width for channel length of 3.3 V PFET                                     | 0.4          |
| Gat.b1                   | Min. space between unrelated 3.3 V GatPoly over Activ regions                           | 0.25         |
| Gat.c                    | Min. GatPoly extension over Activ (end cap)                                             | 0.18         |
| Gat.e                    | Min. GatPoly area (um2)                                                                 | 0.09         |
| Gat.f                    | 45-degree and 90-degree angles for GatPoly on Activ area are not allowed                | 0            |
| GFil.a                   | Max. GatPoly:filler width                                                               | 5            |
| GFil.b                   | Min. GatPoly:filler width                                                               | 0.7          |
| GFil.c                   | Min. GatPoly:filler space                                                               | 0.8          |
| GFil.f                   | Min. GatPoly:filler space to TRANS                                                      | 1.1          |
| GFil.j                   | Min. GatPoly:filler extension over Activ:filler (end cap)                               | 0.18         |
| pSD.a                    | Min. pSD width                                                                          | 0.31         |
| pSD.b                    | Min. pSD space or notch (Note 1)                                                        | 0.31         |
| pSD.c                    | Min. pSD enclosure of P+Activ in NWell                                                  | 0.18         |
| pSD.d                    | Min. pSD space to unrelated N+Activ in PWell                                            | 0.18         |
| pSD.d1                   | Min. pSD space to N+Activ in NWell                                                      | 0.03         |
| pSD.e                    | Min. pSD overlap of Activ at one position when forming abutted substrate tie (Note 2)   | 0.3          |
| pSD.f                    | Min. Activ extension over pSD at one position when forming abutted NWell tie (Note 2)   | 0.3          |
| pSD.g                    | Min. N+Activ or P+Activ area (um2) when forming abutted tie (Note 2)                    | 0.09         |
| pSD.i                    | Min. pSD enclosure of PFET gate not inside ThickGateOx                                  | 0.3          |
| pSD.i1                   | Min. pSD enclosure of PFET gate inside ThickGateOx                                      | 0.4          |
| pSD.j                    | Min. pSD space to NFET gate not inside ThickGateOx                                      | 0.3          |
| pSD.j1                   | Min. pSD space to NFET gate inside ThickGateOx                                          | 0.4          |
| pSD.k                    | Min. pSD area (um2)                                                                     | 0.25         |
| pSD.l                    | Min. pSD enclosed area (um2)                                                            | 0.25         |
| pSD.m                    | Min. pSD space to n-type poly resistors                                                 | 0.18         |
| pSD.n                    | Min. pSD enclosure of p-type poly resistors                                             | 0.18         |
| nSDB.a                   | Min. nSD:block width                                                                    | 0.31         |
| nSDB.b                   | Min. nSD:block space or notch                                                           | 0.31         |
| nSDB.c                   | Min. nSD:block space to unrelated pSD                                                   | 0.31         |
| nSDB.e                   | Min. nSD:block space to Cont (Note 2)                                                   | 0            |
| EXT.a                    | Min. EXTBlock width                                                                     | 0.31         |
| EXT.b                    | Min. EXTBlock space or notch                                                            | 0.31         |
| EXT.c                    | Min. EXTBlock space to pSD                                                              | 0.31         |
| Sal.a                    | Min. SalBlock width                                                                     | 0.42         |
| Sal.b                    | Min. SalBlock space or notch                                                            | 0.42         |
| Sal.c                    | Min. SalBlock extension over Activ or GatPoly                                           | 0.2          |
| Sal.d                    | Min. SalBlock space to unrelated Activ or GatPoly                                       | 0.2          |
| Sal.e                    | Min. SalBlock space to Cont                                                             | 0.2          |
| Cnt.b1                   | Min. Cont space in a contact array of more than 4 rows and more then 4 columns (Note 1) | 0.2          |
| Cnt.f                    | Min. Cont on Activ space to GatPoly                                                     | 0.11         |
| Cnt.g                    | Cont must be within Activ or GatPoly                                                    | -            |
| Cnt.h                    | Cont must be covered with Metal1                                                        | -            |
| Cnt.j                    | Cont on GatPoly over Activ is not allowed                                               | -            |
| CntB.a                   | Min. and max. ContBar width                                                             | 0.16         |
| CntB.a1                  | Min. ContBar length                                                                     | 0.34         |
| CntB.b                   | Min. ContBar space                                                                      | 0.28         |
| CntB.b2                  | Min. ContBar space to Cont                                                              | 0.22         |
| CntB.e                   | Min. ContBar on GatPoly space to Activ                                                  | 0.14         |
| CntB.f                   | Min. ContBar on Activ space to GatPoly                                                  | 0.11         |
| CntB.g                   | ContBar must be within Activ or GatPoly                                                 | -            |
| CntB.g1                  | Min. pSD space to ContBar on nSD-Activ                                                  | 0.09         |
| CntB.g2                  | Min. pSD overlap of ContBar on pSD-Activ                                                | 0.09         |
| CntB.h                   | ContBar must be covered with Metal1                                                     | -            |
| CntB.j                   | ContBar on GatPoly over Activ is not allowed                                            | -            |
| M1.c                     | Min. Metal1 enclosure of Cont                                                           | 0            |
| M1.c1                    | Min. Metal1 endcap enclosure of Cont (Note 1)                                           | 0.05         |
| M1.d                     | Min. Metal1 area (um2)                                                                  | 0.09         |
| M2.c                     | Min. Metal2 enclosure of Via1                                                           | 0.005        |
| M2.c1                    | Min. Metal2 endcap enclosure of Via1 (Note 1)                                           | 0.05         |
| M2.d                     | Min. Metal2 area (um2)                                                                  | 0.144        |
| M3.c                     | Min. Metal3 enclosure of Via2                                                           | 0.005        |
| M3.c1                    | Min. Metal3 endcap enclosure of Via2 (Note 1)                                           | 0.05         |
| M3.d                     | Min. Metal3 area (um2)                                                                  | 0.144        |
| M4.c                     | Min. Metal4 enclosure of Via3                                                           | 0.005        |
| M4.c1                    | Min. Metal4 endcap enclosure of Via3 (Note 1)                                           | 0.05         |
| M4.d                     | Min. Metal4 area (um2)                                                                  | 0.144        |
| M5.c                     | Min. Metal5 enclosure of Via4                                                           | 0.005        |
| M5.c1                    | Min. Metal5 endcap enclosure of Via4 (Note 1)                                           | 0.05         |
| M5.d                     | Min. Metal5 area (um2)                                                                  | 0.144        |
| M1Fil.a1                 | Min. Metal1:filler width                                                                | 1            |
| M1Fil.b                  | Min. Metal1:filler space                                                                | 0.42         |
| M1Fil.d                  | Min. Metal1:filler space to TRANS                                                       | 1            |
| M2Fil.a1                 | Min. Metal2:filler width                                                                | 1            |
| M2Fil.b                  | Min. Metal2:filler space                                                                | 0.42         |
| M2Fil.d                  | Min. Metal2:filler space to TRANS                                                       | 1            |
| M3Fil.a1                 | Min. Metal3:filler width                                                                | 1            |
| M3Fil.b                  | Min. Metal3:filler space                                                                | 0.42         |
| M3Fil.d                  | Min. Metal3:filler space to TRANS                                                       | 1            |
| M4Fil.a1                 | Min. Metal4:filler width                                                                | 1            |
| M4Fil.b                  | Min. Metal4:filler space                                                                | 0.42         |
| M4Fil.d                  | Min. Metal4:filler space to TRANS                                                       | 1            |
| M5Fil.a1                 | Min. Metal5:filler width                                                                | 1            |
| M5Fil.b                  | Min. Metal5:filler space                                                                | 0.42         |
| M5Fil.d                  | Min. Metal5:filler space to TRANS                                                       | 1            |
| V1.b1                    | Min. Via1 space in an array of more than 3 rows and more then 3 columns (Note 1)        | 0.29         |
| V1.c1                    | Min. Metal1 endcap enclosure of Via1 (Note 2)                                           | 0.05         |
| V2.b1                    | Min. Via2 space in an array of more than 3 rows and more then 3 columns (Note 1)        | 0.29         |
| V2.c1                    | Min. Metal2 endcap enclosure of Via2 (Note 2)                                           | 0.05         |
| V3.b1                    | Min. Via3 space in an array of more than 3 rows and more then 3 columns (Note 1)        | 0.29         |
| V3.c1                    | Min. Metal3 endcap enclosure of Via3 (Note 2)                                           | 0.05         |
| V4.b1                    | Min. Via4 space in an array of more than 3 rows and more then 3 columns (Note 1)        | 0.29         |
| V4.c1                    | Min. Metal4 endcap enclosure of Via4 (Note 2)                                           | 0.05         |
| TM1Fil.a                 | Min. TopMetal1:filler width                                                             | 5            |
| TM1Fil.b                 | Min. TopMetal1:filler space                                                             | 3            |
| TM1Fil.d                 | Min. TopMetal1:filler space to TRANS                                                    | 4.9          |
| TM2Fil.a                 | Min. TopMetal2:filler width                                                             | 5            |
| TM2Fil.b                 | Min. TopMetal2:filler space                                                             | 3            |
| TM2Fil.d                 | Min. TopMetal2:filler space to TRANS                                                    | 4.9          |
| npn13G2.a                | Min. and max. npn13G2 emitter length                                                    | 0.9          |
| npn13G2L.a               | Min. npn13G2L emitter length                                                            | 1            |
| npn13G2L.b               | Max. npn13G2L emitter length                                                            | 2.5          |
| npn13G2V.a               | Min. npn13G2V emitter length                                                            | 1            |
| npn13G2V.b               | Max. npn13G2V emitter length                                                            | 5            |
| Rsil.a                   | Min. GatPoly width                                                                      | 0.5          |
| Rsil.b                   | Min. RES space to Cont                                                                  | 0.12         |
| Rsil.c                   | Min. RES extension over GatPoly                                                         | 0            |
| Rsil.d                   | Min. pSD space to GatPoly                                                               | 0.18         |
| Rsil.e                   | Min. EXTBlock enclosure of GatPoly                                                      | 0.18         |
| Rsil.f                   | Min. RES length                                                                         | 0.5          |
| Rppd.a                   | Min. GatPoly width                                                                      | 0.5          |
| Rppd.b                   | Min. pSD enclosure of GatPoly                                                           | 0.18         |
| Rppd.c                   | Min. and max. SalBlock space to Cont                                                    | 0.2          |
| Rppd.e                   | Min. SalBlock length                                                                    | 0.5          |
| Rhi.a                    | Min. GatPoly width                                                                      | 0.5          |
| Rhi.b                    | pSD and nSD are identical (Note 1)                                                      | -            |
| Rhi.c                    | Min. pSD and nSD enclosure of GatPoly                                                   | 0.18         |
| Rhi.d                    | Min. and max. SalBlock space to Cont                                                    | 0.2          |
| Rhi.f                    | Min. SalBlock length                                                                    | 0.5          |
| nmosi.b                  | Min. nBuLay enclosure of Iso-PWell-Activ (Note 1)                                       | 1.24         |
| nmosi.c                  | Min. NWell space to Iso-PWell-Activ                                                     | 0.39         |
| nmosi.d                  | Min. NWell-nBuLay width forming an unbroken ring around any Iso-PWell-Activ (Note 2)    | 0.62         |
| nmosi.f                  | Min. nSD:block width to separate ptap in nmosi                                          | 0.62         |
| nmosi.g                  | Min. SalBlock overlap of nSD:block over Activ                                           | 0.15         |
| Sdiod.a                  | Min. and max. PWell:block enclosure of ContBar                                          | 0.25         |
| Sdiod.b                  | Min. and max. nSD:block enclosure of ContBar                                            | 0.4          |
| Sdiod.c                  | Min. and max. SalBlock enclosure of ContBar                                             | 0.45         |
| Pad.aR                   | Min. recommended Pad width                                                              | 30           |
| Pad.a1                   | Max. Pad width                                                                          | 150          |
| Pad.bR                   | Min. recommended Pad space                                                              | 8.4          |
| Pad.d                    | Min. Pad space to EdgeSeal                                                              | 7.5          |
| Pad.dR                   | Min. recommended Pad to EdgeSeal space (Note 1)                                         | 25           |
| Pad.d1R                  | Min. recommended Pad to Activ (inside chip area) space                                  | 11.2         |
| Pad.gR                   | TopMetal1 (within dfpad) enclosure of TopVia2                                           | 1.4          |
| Pad.jR                   | No devices under Pad allowed (Note 2)                                                   | -            |
| Pad.kR                   | TopVia2 under Pad not allowed (Note 3)                                                  | -            |
| Padc.d                   | Min. CuPillarPad space to EdgeSeal                                                      | 30           |
| Seal.a_Activ             | Min. EdgeSeal-Activ width                                                               | 3.5          |
| Seal.a_pSD               | Min. EdgeSeal-pSD width                                                                 | 3.5          |
| Seal.a_Metal1            | Min. EdgeSeal-Metal1 width                                                              | 3.5          |
| Seal.a_Metal2            | Min. EdgeSeal-Metal2 width                                                              | 3.5          |
| Seal.a_Metal3            | Min. EdgeSeal-Metal3 width                                                              | 3.5          |
| Seal.a_Metal4            | Min. EdgeSeal-Metal4 width                                                              | 3.5          |
| Seal.a_Metal5            | Min. EdgeSeal-Metal5 width                                                              | 3.5          |
| Seal.a_TopMetal1         | Min. EdgeSeal-TopMetal1 width                                                           | 3.5          |
| Seal.a_TopMetal2         | Min. EdgeSeal-TopMetal2 width                                                           | 3.5          |
| Seal.c                   | EdgeSeal-Cont ring width                                                                | 0.16         |
| Seal.c1.Via1             | EdgeSeal-Via1 ring width                                                                | 0.19         |
| Seal.c1.Via2             | EdgeSeal-Via2 ring width                                                                | 0.19         |
| Seal.c1.Via3             | EdgeSeal-Via3 ring width                                                                | 0.19         |
| Seal.c1.Via4             | EdgeSeal-Via4 ring width                                                                | 0.19         |
| Seal.c2                  | EdgeSeal-TopVia1 ring width                                                             | 0.42         |
| Seal.c3                  | EdgeSeal-TopVia2 ring width                                                             | 0.9          |
| Seal.e                   | Min. Passiv ring width outside of sealring                                              | 4.2          |
| MIM.a                    | Min. MIM width                                                                          | 1.14         |
| MIM.b                    | Min. MIM space                                                                          | 0.6          |
| MIM.e                    | Min. TopMetal1 space to MIM                                                             | 0.6          |
| MIM.f                    | Min. MIM area per MIM device (um2)                                                      | 1.3          |
| MIM.g                    | Max. MIM area per MIM device (um2)                                                      | 5625         |
| MIM.h                    | TopVia1 must be over MIM                                                                | -            |
| LU.a                     | Max. space from any portion of P+Activ inside NWell to an nSD-NWell tie                 | 20           |
| LU.c                     | Max. extension of an abutted NWell tie beyond Cont                                      | 6            |
| LU.c1                    | Max. extension of an abutted substrate tie beyond Cont                                  | 6            |
| LU.d                     | Max. extension of NWell tie Activ tie beyond Cont                                       | 6            |
| LU.d1                    | Max. extension of an substrate tie Activ beyond Cont                                    | 6            |
| Slt.a.M1                 | Min. Metal1:slit width                                                                  | 2.8          |
| Slt.b.M1                 | Max. Metal1:slit width                                                                  | 20           |
| Slt.c.M1                 | Max. Metal1 width without requiring a slit                                              | 30           |
| Slt.e.M1                 | No slits required on bond pads                                                          | -            |
| Slt.f.M1                 | Min. Metal1 enclosure of Metal1:slit                                                    | 1            |
| Slt.h1                   | Min. Metal1:slit space to Cont and Via1                                                 | 0.3          |
| Slt.a.M2                 | Min. Metal2:slit width                                                                  | 2.8          |
| Slt.b.M2                 | Max. Metal2:slit width                                                                  | 20           |
| Slt.c.M2                 | Max. Metal2 width without requiring a slit                                              | 30           |
| Slt.e.M2                 | No slits required on bond pads                                                          | -            |
| Slt.f.M2                 | Min. Metal2 enclosure of Metal2:slit                                                    | 1            |
| Slt.h2.M2                | Min. Metal2:slit space to Via1 and Via2                                                 | 0.3          |
| Slt.a.M3                 | Min. Metal3:slit width                                                                  | 2.8          |
| Slt.b.M3                 | Max. Metal3:slit width                                                                  | 20           |
| Slt.c.M3                 | Max. Metal3 width without requiring a slit                                              | 30           |
| Slt.e.M3                 | No slits required on bond pads                                                          | -            |
| Slt.f.M3                 | Min. Metal3 enclosure of Metal2:slit                                                    | 1            |
| Slt.h2.M3                | Min. Metal3:slit space to Via2 and Via3                                                 | 0.3          |
| Slt.a.M4                 | Min. Metal4:slit width                                                                  | 2.8          |
| Slt.b.M4                 | Max. Metal4:slit width                                                                  | 20           |
| Slt.c.M4                 | Max. Metal4 width without requiring a slit                                              | 30           |
| Slt.e.M4                 | No slits required on bond pads                                                          | -            |
| Slt.f.M4                 | Min. Metal4 enclosure of Metal4:slit                                                    | 1            |
| Slt.h2.M4                | Min. Metal4:slit space to Via3 and Via4                                                 | 0.3          |
| Slt.a.M5                 | Min. Metal5:slit width                                                                  | 2.8          |
| Slt.b.M5                 | Max. Metal5:slit width                                                                  | 20           |
| Slt.c.M5                 | Max. Metal5 width without requiring a slit                                              | 30           |
| Slt.e.M5                 | No slits required on bond pads                                                          | -            |
| Slt.f.M5                 | Min. Metal5 enclosure of Metal5:slit                                                    | 1            |
| Slt.g.M5                 | Min. Metal5:slit and TopMetal1:slit space to MIM                                        | 0.6          |
| Slt.h2.M5                | Min. Metal5:slit space to Via4 and Via5                                                 | 0.3          |
| Slt.a.TM1                | Min. TopMetal1:slit width                                                               | 2.8          |
| Slt.b.TM1                | Max. TopMetal1:slit width                                                               | 20           |
| Slt.c.TM1                | Max. TopMetal1 width without requiring a slit                                           | 30           |
| Slt.e.TM1                | No slits required on bond pads                                                          | -            |
| Slt.f.TM1                | Min. TopMetal1 enclosure of TopMetal1:slit                                              | 1            |
| Slt.g.TM1                | Min. Metal5:slit and TopMetal1:slit space to MIM                                        | 0.6          |
| Slt.h3                   | Min. TopMetal1:slit space to TopVia1 and TopVia2                                        | 1            |
| Slt.a.TM2                | Min. TopMetal2:slit width                                                               | 2.8          |
| Slt.b.TM2                | Max. TopMetal2:slit width                                                               | 20           |
| Slt.c.TM2                | Max. TopMetal2 width without requiring a slit                                           | 30           |
| Slt.e.TM2                | No slits required on bond pads                                                          | -            |
| Slt.f.TM2                | Min. TopMetal2 enclosure of TopMetal2:slit                                              | 1            |
| Slt.h4                   | Min. TopMetal2:slit space to TopVia2                                                    | 1            |
| NW.d1.dig                | Min. NWell space to external N+Activ inside ThickGateOx                                 | 0.31         |
| NW.f1.dig                | Min. NWell space to substrate tie in P+Activ inside ThickGateOx                         | 0.24         |
| LBE.b2                   | Min. LBE area (um2)                                                                     | 30000        |
| LBE.e.dfPad              | Min. LBE space to dfpad and Passiv                                                      | 50           |
| LBE.e.Passiv             | Min. LBE space to dfpad and Passiv                                                      | 50           |
| LBE.f                    | Min. LBE space to Activ                                                                 | 30           |
| TSV_G.a                  | DeepVia has to be a ring structure                                                      | -            |
| TSV_G.d                  | Min. DeepVia space                                                                      | 25           |
| TSV_G.f                  | Min. PWell:block enclosure of DeepVia                                                   | 2.5          |
| TSV_G.g                  | Min. Metal1 enclosure of DeepVia ring structure                                         | 1.5          |
| TSV_G.i                  | Max. global DeepVia density [%]                                                         | 1            |
| TSV_G.j                  | Max. DeepVia coverage ratio for any 500.0 x 500.0 um2 chip area [%]                     | 10           |
| OffGrid.NWell            | NWell is off-grid                                                                       | -            |
| OffGrid.PWell            | PWell is off-grid                                                                       | -            |
| OffGrid.PWell_block      | PWell_block is off-grid                                                                 | -            |
| OffGrid.nBuLay           | nBuLay is off-grid                                                                      | -            |
| OffGrid.nBuLay_block     | nBuLay_block is off-grid                                                                | -            |
| OffGrid.Activ            | Activ is off-grid                                                                       | -            |
| OffGrid.ThickGateOx      | ThickGateOx is off-grid                                                                 | -            |
| OffGrid.Activ_filler     | Activ_filler is off-grid                                                                | -            |
| OffGrid.GatPoly_filler   | GatPoly_filler is off-grid                                                              | -            |
| OffGrid.GatPoly          | GatPoly is off-grid                                                                     | -            |
| OffGrid.pSD              | pSD is off-grid                                                                         | -            |
| OffGrid.nSD              | nSD is off-grid                                                                         | -            |
| OffGrid.nSD_block        | nSD_block is off-grid                                                                   | -            |
| OffGrid.EXTBlock         | EXTBlock is off-grid                                                                    | -            |
| OffGrid.SalBlock         | SalBlock is off-grid                                                                    | -            |
| OffGrid.Cont             | Cont is off-grid                                                                        | -            |
| OffGrid.Activ_nofill     | Activ_nofill is off-grid                                                                | -            |
| OffGrid.GatPoly_nofill   | GatPoly_nofill is off-grid                                                              | -            |
| OffGrid.Metal1           | Metal1 is off-grid                                                                      | -            |
| OffGrid.Via1             | Via1 is off-grid                                                                        | -            |
| OffGrid.Metal2           | Metal2 is off-grid                                                                      | -            |
| OffGrid.Via2             | Via2 is off-grid                                                                        | -            |
| OffGrid.Metal3           | Metal3 is off-grid                                                                      | -            |
| OffGrid.Via3             | Via3 is off-grid                                                                        | -            |
| OffGrid.Metal4           | Metal4 is off-grid                                                                      | -            |
| OffGrid.Via4             | Via4 is off-grid                                                                        | -            |
| OffGrid.Metal5           | Metal5 is off-grid                                                                      | -            |
| OffGrid.MIM              | MIM is off-grid                                                                         | -            |
| OffGrid.TopVia1          | TopVia1 is off-grid                                                                     | -            |
| OffGrid.TopMetal1        | TopMetal1 is off-grid                                                                   | -            |
| OffGrid.TopVia2          | TopVia2 is off-grid                                                                     | -            |
| OffGrid.TopMetal2        | TopMetal2 is off-grid                                                                   | -            |
| OffGrid.Passiv           | Passiv is off-grid                                                                      | -            |
| OffGrid.Metal1_filler    | Metal1_filler is off-grid                                                               | -            |
| OffGrid.Metal2_filler    | Metal2_filler is off-grid                                                               | -            |
| OffGrid.Metal3_filler    | Metal3_filler is off-grid                                                               | -            |
| OffGrid.Metal4_filler    | Metal4_filler is off-grid                                                               | -            |
| OffGrid.Metal5_filler    | Metal5_filler is off-grid                                                               | -            |
| OffGrid.TopMetal1_filler | TopMetal1_filler is off-grid                                                            | -            |
| OffGrid.TopMetal2_filler | TopMetal2_filler is off-grid                                                            | -            |
| OffGrid.Metal1_nofill    | Metal1_nofill is off-grid                                                               | -            |
| OffGrid.Metal2_nofill    | Metal2_nofill is off-grid                                                               | -            |
| OffGrid.Metal3_nofill    | Metal3_nofill is off-grid                                                               | -            |
| OffGrid.Metal4_nofill    | Metal4_nofill is off-grid                                                               | -            |
| OffGrid.Metal5_nofill    | Metal5_nofill is off-grid                                                               | -            |
| OffGrid.TopMetal1_nofill | TopMetal1_nofill is off-grid                                                            | -            |
| OffGrid.TopMetal2_nofill | TopMetal2_nofill is off-grid                                                            | -            |
| OffGrid.NoMetFiller      | NoMetFiller is off-grid                                                                 | -            |
| OffGrid.Metal1_slit      | Metal1_slit is off-grid                                                                 | -            |
| OffGrid.Metal2_slit      | Metal2_slit is off-grid                                                                 | -            |
| OffGrid.Metal3_slit      | Metal3_slit is off-grid                                                                 | -            |
| OffGrid.Metal4_slit      | Metal4_slit is off-grid                                                                 | -            |
| OffGrid.Metal5_slit      | Metal5_slit is off-grid                                                                 | -            |
| OffGrid.TopMetal1_slit   | TopMetal1_slit is off-grid                                                              | -            |
| OffGrid.TopMetal2_slit   | TopMetal2_slit is off-grid                                                              | -            |
| OffGrid.EdgeSeal         | EdgeSeal is off-grid                                                                    | -            |
| OffGrid.dfpad            | dfpad is off-grid                                                                       | -            |
| OffGrid.LBE              | LBE is off-grid                                                                         | -            |
