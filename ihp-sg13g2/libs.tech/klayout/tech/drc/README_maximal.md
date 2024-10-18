## Current status -- *Preliminary*

List of available DRC rules:

| Name                     | Description                                                                             |
| ------------------------ | --------------------------------------------------------------------------------------- |
| NW.a                     | Min. NWell width                                                                        |
| NW.d1                    | Min. NWell space to external N+Activ inside ThickGateOx                                 |
| NW.f                     | Min. NWell space to substrate tie in P+Activ not inside ThickGateOx                     |
| NW.f1                    | Min. NWell space to substrate tie in P+Activ inside ThickGateOx                         |
| PWB.a                    | Min. PWell:block width                                                                  |
| PWB.b                    | Min. PWell:block space or notch                                                         |
| PWB.c                    | Min. PWell:block space to unrelated NWell                                               |
| NBL.a                    | Min. nBuLay width                                                                       |
| NBLB.a                   | Min. nBuLay:block width                                                                 |
| NBLB.b                   | Min. nBuLay:block space or notch                                                        |
| NBLB.c                   | Min. nBuLay enclosure of nBuLay:block                                                   |
| NBLB.d                   | Min. nBuLay:block space to unrelated nBuLay                                             |
| Act.a                    | Min. Activ width                                                                        |
| Act.b                    | Min. Activ space or notch                                                               |
| Act.d                    | Min. Activ area (µm²)                                                                   |
| Act.e                    | Min. Activ enclosed area (µm²)                                                          |
| AFil.a                   | Max. Activ:filler width                                                                 |
| AFil.a1                  | Min. Activ:filler width                                                                 |
| AFil.b                   | Min. Activ:filler space                                                                 |
| AFil.g                   | Min. global Activ density [%]                                                           |
| AFil.g1                  | Max. global Activ density [%]                                                           |
| AFil.g2                  | Min. Activ coverage ratio for any 800 x 800 µm² chip area [%]                           |
| AFil.g3                  | Max. Activ coverage ratio for any 800 x 800 µm² chip area [%]                           |
| TGO.a                    | Min. ThickGateOx extension over Activ                                                   |
| TGO.b                    | Min. space between ThickGateOx and Activ outside thick gate oxide region                |
| TGO.c                    | Min. ThickGateOx extension over GatPoly over Activ                                      |
| TGO.d                    | Min. space between ThickGateOx and GatPoly over Activ outside thick gate oxide region   |
| TGO.e                    | Min. ThickGateOx space (merge if less than this value)                                  |
| TGO.f                    | Min. ThickGateOx width                                                                  |
| Gat.a                    | Min. GatPoly width                                                                      |
| Gat.a3                   | Min. GatPoly width for channel length of 3.3 V NFET                                     |
| Gat.a4                   | Min. GatPoly width for channel length of 3.3 V PFET                                     |
| Gat.b                    | Min. GatPoly space or notch                                                             |
| Gat.b1                   | Min. space between unrelated 3.3 V GatPoly over Activ regions                           |
| Gat.c                    | Min. GatPoly extension over Activ (end cap)                                             |
| Gat.d                    | Min. GatPoly space to Activ                                                             |
| Gat.e                    | Min. GatPoly area (µm²)                                                                 |
| Gat.f                    | 45-degree and 90-degree angles for GatPoly on Activ area are not allowed                |
| GFil.a                   | Max. GatPoly:filler width                                                               |
| GFil.b                   | Min. GatPoly:filler width                                                               |
| GFil.c                   | Min. GatPoly:filler space                                                               |
| GFil.d.Activ             | Min. GatPoly:filler space to Activ                                                      |
| GFil.d.GatPoly           | Min. GatPoly:filler space to GatPoly                                                    |
| GFil.d.Cont              | Min. GatPoly:filler space to Cont                                                       |
| GFil.d.pSD               | Min. GatPoly:filler space to pSD                                                        |
| GFil.d.nSD_block         | Min. GatPoly:filler space to nSD:block                                                  |
| GFil.d.SalBlock          | Min. GatPoly:filler space to SalBlock                                                   |
| GFil.f                   | Min. GatPoly:filler space to TRANS                                                      |
| GFil.g                   | Min. global GatPoly density [%]                                                         |
| GFil.j                   | Min. GatPoly:filler extension over Activ:filler (end cap)                               |
| pSD.a                    | Min. pSD width                                                                          |
| pSD.b                    | Min. pSD space or notch (Note 1)                                                        |
| pSD.c                    | Min. pSD enclosure of P+Activ in NWell                                                  |
| pSD.d                    | Min. pSD space to unrelated N+Activ in PWell                                            |
| pSD.d1                   | Min. pSD space to N+Activ in NWell                                                      |
| pSD.e                    | Min. pSD overlap of Activ at one position when forming abutted substrate tie (Note 2)   |
| pSD.f                    | Min. Activ extension over pSD at one position when forming abutted NWell tie (Note 2)   |
| pSD.g                    | Min. N+Activ or P+Activ area (µm²) when forming abutted tie (Note 2)                    |
| pSD.i                    | Min. pSD enclosure of PFET gate not inside ThickGateOx                                  |
| pSD.i1                   | Min. pSD enclosure of PFET gate inside ThickGateOx                                      |
| pSD.j                    | Min. pSD space to NFET gate not inside ThickGateOx                                      |
| pSD.j1                   | Min. pSD space to NFET gate inside ThickGateOx                                          |
| pSD.k                    | Min. pSD area (µm²)                                                                     |
| pSD.l                    | Min. pSD enclosed area (µm²)                                                            |
| pSD.m                    | Min. pSD space to n-type poly resistors                                                 |
| pSD.n                    | Min. pSD enclosure of p-type poly resistors                                             |
| nSDB.a                   | Min. nSD:block width                                                                    |
| nSDB.b                   | Min. nSD:block space or notch                                                           |
| nSDB.c                   | Min. nSD:block space to unrelated pSD                                                   |
| nSDB.e                   | Min. nSD:block space to Cont (Note 2)                                                   |
| EXT.a                    | Min. EXTBlock width                                                                     |
| EXT.b                    | Min. EXTBlock space or notch                                                            |
| EXT.c                    | Min. EXTBlock space to pSD                                                              |
| Sal.a                    | Min. SalBlock width                                                                     |
| Sal.b                    | Min. SalBlock space or notch                                                            |
| Sal.c                    | Min. SalBlock extension over Activ or GatPoly                                           |
| Sal.d                    | Min. SalBlock space to unrelated Activ or GatPoly                                       |
| Sal.e                    | Min. SalBlock space to Cont                                                             |
| Cnt.a                    | Min. and max. Cont width                                                                |
| Cnt.b                    | Min. Cont space                                                                         |
| Cnt.b1                   | Min. Cont space in a contact array of more than 4 rows and more then 4 columns (Note 1) |
| Cnt.f                    | Min. Cont on Activ space to GatPoly                                                     |
| Cnt.g                    | Cont must be within Activ or GatPoly                                                    |
| Cnt.h                    | Cont must be covered with Metal1                                                        |
| Cnt.j                    | Cont on GatPoly over Activ is not allowed                                               |
| CntB.a                   | Min. and max. ContBar width                                                             |
| CntB.a1                  | Min. ContBar length                                                                     |
| CntB.b                   | Min. ContBar space                                                                      |
| CntB.b2                  | Min. ContBar space to Cont                                                              |
| CntB.e                   | Min. ContBar on GatPoly space to Activ                                                  |
| CntB.f                   | Min. ContBar on Activ space to GatPoly                                                  |
| CntB.g                   | ContBar must be within Activ or GatPoly                                                 |
| CntB.g1                  | Min. pSD space to ContBar on nSD-Activ                                                  |
| CntB.g2                  | Min. pSD overlap of ContBar on pSD-Activ                                                |
| CntB.h                   | ContBar must be covered with Metal1                                                     |
| CntB.j                   | ContBar on GatPoly over Activ is not allowed                                            |
| M1.a                     | Min. Metal1 width                                                                       |
| M1.b                     | Min. Metal1 space or notch                                                              |
| M1.c                     | Min. Metal1 enclosure of Cont                                                           |
| M1.c1                    | Min. Metal1 endcap enclosure of Cont (Note 1)                                           |
| M1.d                     | Min. Metal1 area (µm²)                                                                  |
| M1.j                     | Min. global Metal1 density [%]                                                          |
| M1.k                     | Max. global Metal1 density [%]                                                          |
| M2.a                     | Min. Metal2 width                                                                       |
| M2.b                     | Min. Metal2 space or notch                                                              |
| M2.c                     | Min. Metal2 enclosure of Via1                                                           |
| M2.c1                    | Min. Metal2 endcap enclosure of Via1 (Note 1)                                           |
| M2.d                     | Min. Metal2 area (µm²)                                                                  |
| M2.j                     | Min. global Metal2 density [%]                                                          |
| M2.k                     | Max. global Metal2 density [%]                                                          |
| M3.a                     | Min. Metal3 width                                                                       |
| M3.b                     | Min. Metal3 space or notch                                                              |
| M3.c                     | Min. Metal3 enclosure of Via2                                                           |
| M3.c1                    | Min. Metal3 endcap enclosure of Via2 (Note 1)                                           |
| M3.d                     | Min. Metal3 area (µm²)                                                                  |
| M3.j                     | Min. global Metal3 density [%]                                                          |
| M3.k                     | Max. global Metal3 density [%]                                                          |
| M4.a                     | Min. Metal4 width                                                                       |
| M4.b                     | Min. Metal4 space or notch                                                              |
| M4.c                     | Min. Metal4 enclosure of Via3                                                           |
| M4.c1                    | Min. Metal4 endcap enclosure of Via3 (Note 1)                                           |
| M4.d                     | Min. Metal4 area (µm²)                                                                  |
| M4.j                     | Min. global Metal4 density [%]                                                          |
| M4.k                     | Max. global Metal4 density [%]                                                          |
| M5.a                     | Min. Metal5 width                                                                       |
| M5.b                     | Min. Metal5 space or notch                                                              |
| M5.c                     | Min. Metal5 enclosure of Via4                                                           |
| M5.c1                    | Min. Metal5 endcap enclosure of Via4 (Note 1)                                           |
| M5.d                     | Min. Metal5 area (µm²)                                                                  |
| M5.j                     | Min. global Metal5 density [%]                                                          |
| M5.k                     | Max. global Metal5 density [%]                                                          |
| M1Fil.a1                 | Min. Metal1:filler width                                                                |
| M1Fil.b                  | Min. Metal1:filler space                                                                |
| M1Fil.c                  | Min. Metal1:filler space to Metal1                                                      |
| M1Fil.d                  | Min. Metal1:filler space to TRANS                                                       |
| M1Fil.h                  | Min. Metal1 and Metal1:filler coverage ratio for any 800 x 800 µm² chip area [%]        |
| M1Fil.k                  | Max. Metal1 and Metal1:filler coverage ratio for any 800 x 800 µm² chip area [%]        |
| M2Fil.a1                 | Min. Metal2:filler width                                                                |
| M2Fil.b                  | Min. Metal2:filler space                                                                |
| M2Fil.c                  | Min. Metal2:filler space to Metal2                                                      |
| M2Fil.d                  | Min. Metal2:filler space to TRANS                                                       |
| M2Fil.h                  | Min. Metal2 and Metal2:filler coverage ratio for any 800 x 800 µm² chip area [%]        |
| M2Fil.k                  | Max. Metal2 and Metal2:filler coverage ratio for any 800 x 800 µm² chip area [%]        |
| M3Fil.a1                 | Min. Metal3:filler width                                                                |
| M3Fil.b                  | Min. Metal3:filler space                                                                |
| M3Fil.c                  | Min. Metal3:filler space to Metal3                                                      |
| M3Fil.d                  | Min. Metal3:filler space to TRANS                                                       |
| M3Fil.h                  | Min. Metal3 and Metal3:filler coverage ratio for any 800 x 800 µm² chip area [%]        |
| M3Fil.k                  | Max. Metal3 and Metal3:filler coverage ratio for any 800 x 800 µm² chip area [%]        |
| M4Fil.a1                 | Min. Metal4:filler width                                                                |
| M4Fil.b                  | Min. Metal4:filler space                                                                |
| M4Fil.c                  | Min. Metal4:filler space to Metal4                                                      |
| M4Fil.d                  | Min. Metal4:filler space to TRANS                                                       |
| M4Fil.h                  | Min. Metal4 and Metal4:filler coverage ratio for any 800 x 800 µm² chip area [%]        |
| M4Fil.k                  | Max. Metal4 and Metal4:filler coverage ratio for any 800 x 800 µm² chip area [%]        |
| M5Fil.a1                 | Min. Metal5:filler width                                                                |
| M5Fil.b                  | Min. Metal5:filler space                                                                |
| M5Fil.c                  | Min. Metal5:filler space to Metal5                                                      |
| M5Fil.d                  | Min. Metal5:filler space to TRANS                                                       |
| M5Fil.h                  | Min. Metal5 and Metal5:filler coverage ratio for any 800 x 800 µm² chip area [%]        |
| M5Fil.k                  | Max. Metal5 and Metal5:filler coverage ratio for any 800 x 800 µm² chip area [%]        |
| V1.a                     | Min. and max. Via1 width                                                                |
| V1.b                     | Min. Via1 space                                                                         |
| V1.b1                    | Min. Via1 space in an array of more than 3 rows and more then 3 columns (Note 1)        |
| V1.c1                    | Min. Metal1 endcap enclosure of Via1 (Note 2)                                           |
| V2.a                     | Min. and max. Via2 width                                                                |
| V2.b                     | Min. Via2 space                                                                         |
| V2.b1                    | Min. Via2 space in an array of more than 3 rows and more then 3 columns (Note 1)        |
| V2.c1                    | Min. Metal2 endcap enclosure of Via2 (Note 2)                                           |
| V3.a                     | Min. and max. Via3 width                                                                |
| V3.b                     | Min. Via3 space                                                                         |
| V3.b1                    | Min. Via3 space in an array of more than 3 rows and more then 3 columns (Note 1)        |
| V3.c1                    | Min. Metal3 endcap enclosure of Via3 (Note 2)                                           |
| V4.a                     | Min. and max. Via4 width                                                                |
| V4.b                     | Min. Via4 space                                                                         |
| V4.b1                    | Min. Via4 space in an array of more than 3 rows and more then 3 columns (Note 1)        |
| V4.c1                    | Min. Metal4 endcap enclosure of Via4 (Note 2)                                           |
| TV1.a                    | Min. and max. TopVia1 width                                                             |
| TV1.b                    | Min. TopVia1 space                                                                      |
| TM1.a                    | Min. TopMetal1 width                                                                    |
| TM1.b                    | Min. TopMetal1 space or notch                                                           |
| TM1.c                    | Min. global TopMetal1 density [%]                                                       |
| TM1.d                    | Max. global TopMetal1 density [%]                                                       |
| TM1Fil.a                 | Min. TopMetal1:filler width                                                             |
| TM1Fil.b                 | Min. TopMetal1:filler space                                                             |
| TM1Fil.c                 | Min. TopMetal1:filler space to TopMetal1                                                |
| TM1Fil.d                 | Min. TopMetal1:filler space to TRANS                                                    |
| TV2.a                    | Min. and max. TopVia2 width                                                             |
| TV2.b                    | Min. TopVia2 space                                                                      |
| TM2.a                    | Min. TopMetal2 width                                                                    |
| TM2.b                    | Min. TopMetal2 space or notch                                                           |
| TM2.c                    | Min. global TopMetal2 density [%]                                                       |
| TM2.d                    | Max. global TopMetal2 density [%]                                                       |
| TM2Fil.a                 | Min. TopMetal2:filler width                                                             |
| TM2Fil.b                 | Min. TopMetal2:filler space                                                             |
| TM2Fil.c                 | Min. TopMetal2:filler space to TopMetal2                                                |
| TM2Fil.d                 | Min. TopMetal2:filler space to TRANS                                                    |
| Pas.a                    | Min. Passiv width                                                                       |
| Pas.b                    | Min. Passiv space or notch                                                              |
| npn13G2.a                | Min. and max. npn13G2 emitter length                                                    |
| npn13G2L.a               | Min. npn13G2L emitter length                                                            |
| npn13G2L.b               | Max. npn13G2L emitter length                                                            |
| npn13G2V.a               | Min. npn13G2V emitter length                                                            |
| npn13G2V.b               | Max. npn13G2V emitter length                                                            |
| Rsil.a                   | Min. GatPoly width                                                                      |
| Rsil.b                   | Min. RES space to Cont                                                                  |
| Rsil.c                   | Min. RES extension over GatPoly                                                         |
| Rsil.d                   | Min. pSD space to GatPoly                                                               |
| Rsil.e                   | Min. EXTBlock enclosure of GatPoly                                                      |
| Rsil.f                   | Min. RES length                                                                         |
| Rppd.a                   | Min. GatPoly width                                                                      |
| Rppd.b                   | Min. pSD enclosure of GatPoly                                                           |
| Rppd.c                   | Min. and max. SalBlock space to Cont                                                    |
| Rppd.e                   | Min. SalBlock length                                                                    |
| Rhi.a                    | Min. GatPoly width                                                                      |
| Rhi.b                    | pSD and nSD are identical (Note 1)                                                      |
| Rhi.c                    | Min. pSD and nSD enclosure of GatPoly                                                   |
| Rhi.d                    | Min. and max. SalBlock space to Cont                                                    |
| Rhi.f                    | Min. SalBlock length                                                                    |
| nmosi.b                  | Min. nBuLay enclosure of Iso-PWell-Activ (Note 1)                                       |
| nmosi.c                  | Min. NWell space to Iso-PWell-Activ                                                     |
| nmosi.d                  | Min. NWell-nBuLay width forming an unbroken ring around any Iso-PWell-Activ (Note 2)    |
| nmosi.f                  | Min. nSD:block width to separate ptap in nmosi                                          |
| nmosi.g                  | Min. SalBlock overlap of nSD:block over Activ                                           |
| Sdiod.a                  | Min. and max. PWell:block enclosure of ContBar                                          |
| Sdiod.b                  | Min. and max. nSD:block enclosure of ContBar                                            |
| Sdiod.c                  | Min. and max. SalBlock enclosure of ContBar                                             |
| Pad.aR                   | Min. recommended Pad width                                                              |
| Pad.a1                   | Max. Pad width                                                                          |
| Pad.bR                   | Min. recommended Pad space                                                              |
| Pad.d                    | Min. Pad space to EdgeSeal                                                              |
| Pad.dR                   | Min. recommended Pad to EdgeSeal space (Note 1)                                         |
| Pad.d1R                  | Min. recommended Pad to Activ (inside chip area) space                                  |
| Pad.gR                   | TopMetal1 (within dfpad) enclosure of TopVia2                                           |
| Pad.jR                   | No devices under Pad allowed (Note 2)                                                   |
| Pad.kR                   | TopVia2 under Pad not allowed (Note 3)                                                  |
| Padc.b                   | Min. CuPillarPad space                                                                  |
| Padc.d                   | Min. CuPillarPad space to EdgeSeal                                                      |
| Seal.a_Activ             | Min. EdgeSeal-Activ width                                                               |
| Seal.a_pSD               | Min. EdgeSeal-pSD width                                                                 |
| Seal.a_Metal1            | Min. EdgeSeal-Metal1 width                                                              |
| Seal.a_Metal2            | Min. EdgeSeal-Metal2 width                                                              |
| Seal.a_Metal3            | Min. EdgeSeal-Metal3 width                                                              |
| Seal.a_Metal4            | Min. EdgeSeal-Metal4 width                                                              |
| Seal.a_Metal5            | Min. EdgeSeal-Metal5 width                                                              |
| Seal.a_TopMetal1         | Min. EdgeSeal-TopMetal1 width                                                           |
| Seal.a_TopMetal2         | Min. EdgeSeal-TopMetal2 width                                                           |
| Seal.c                   | EdgeSeal-Cont ring width                                                                |
| Seal.c1.Via1             | EdgeSeal-Via1 ring width                                                                |
| Seal.c1.Via2             | EdgeSeal-Via2 ring width                                                                |
| Seal.c1.Via3             | EdgeSeal-Via3 ring width                                                                |
| Seal.c1.Via4             | EdgeSeal-Via4 ring width                                                                |
| Seal.c2                  | EdgeSeal-TopVia1 ring width                                                             |
| Seal.c3                  | EdgeSeal-TopVia2 ring width                                                             |
| Seal.e                   | Min. Passiv ring width outside of sealring                                              |
| MIM.a                    | Min. MIM width                                                                          |
| MIM.b                    | Min. MIM space                                                                          |
| MIM.e                    | Min. TopMetal1 space to MIM                                                             |
| MIM.f                    | Min. MIM area per MIM device (µm²)                                                      |
| MIM.g                    | Max. MIM area per MIM device (µm²)                                                      |
| MIM.h                    | TopVia1 must be over MIM                                                                |
| LU.a                     | Max. space from any portion of P+Activ inside NWell to an nSD-NWell tie                 |
| LU.c                     | Max. extension of an abutted NWell tie beyond Cont                                      |
| LU.c1                    | Max. extension of an abutted substrate tie beyond Cont                                  |
| LU.d                     | Max. extension of NWell tie Activ tie beyond Cont                                       |
| LU.d1                    | Max. extension of an substrate tie Activ beyond Cont                                    |
| Slt.a.M1                 | Min. Metal1:slit width                                                                  |
| Slt.b.M1                 | Max. Metal1:slit width                                                                  |
| Slt.c.M1                 | Max. Metal1 width without requiring a slit                                              |
| Slt.e.M1                 | No slits required on bond pads                                                          |
| Slt.f.M1                 | Min. Metal1 enclosure of Metal1:slit                                                    |
| Slt.h1                   | Min. Metal1:slit space to Cont and Via1                                                 |
| Slt.a.M2                 | Min. Metal2:slit width                                                                  |
| Slt.b.M2                 | Max. Metal2:slit width                                                                  |
| Slt.c.M2                 | Max. Metal2 width without requiring a slit                                              |
| Slt.e.M2                 | No slits required on bond pads                                                          |
| Slt.f.M2                 | Min. Metal2 enclosure of Metal2:slit                                                    |
| Slt.h2.M2                | Min. Metal2:slit space to Via1 and Via2                                                 |
| Slt.a.M3                 | Min. Metal3:slit width                                                                  |
| Slt.b.M3                 | Max. Metal3:slit width                                                                  |
| Slt.c.M3                 | Max. Metal3 width without requiring a slit                                              |
| Slt.e.M3                 | No slits required on bond pads                                                          |
| Slt.f.M3                 | Min. Metal3 enclosure of Metal2:slit                                                    |
| Slt.h2.M3                | Min. Metal3:slit space to Via2 and Via3                                                 |
| Slt.a.M4                 | Min. Metal4:slit width                                                                  |
| Slt.b.M4                 | Max. Metal4:slit width                                                                  |
| Slt.c.M4                 | Max. Metal4 width without requiring a slit                                              |
| Slt.e.M4                 | No slits required on bond pads                                                          |
| Slt.f.M4                 | Min. Metal4 enclosure of Metal4:slit                                                    |
| Slt.h2.M4                | Min. Metal4:slit space to Via3 and Via4                                                 |
| Slt.a.M5                 | Min. Metal5:slit width                                                                  |
| Slt.b.M5                 | Max. Metal5:slit width                                                                  |
| Slt.c.M5                 | Max. Metal5 width without requiring a slit                                              |
| Slt.e.M5                 | No slits required on bond pads                                                          |
| Slt.f.M5                 | Min. Metal5 enclosure of Metal5:slit                                                    |
| Slt.g.M5                 | Min. Metal5:slit and TopMetal1:slit space to MIM                                        |
| Slt.h2.M5                | Min. Metal5:slit space to Via4 and Via5                                                 |
| Slt.a.TM1                | Min. TopMetal1:slit width                                                               |
| Slt.b.TM1                | Max. TopMetal1:slit width                                                               |
| Slt.c.TM1                | Max. TopMetal1 width without requiring a slit                                           |
| Slt.e.TM1                | No slits required on bond pads                                                          |
| Slt.f.TM1                | Min. TopMetal1 enclosure of TopMetal1:slit                                              |
| Slt.g.TM1                | Min. Metal5:slit and TopMetal1:slit space to MIM                                        |
| Slt.h3                   | Min. TopMetal1:slit space to TopVia1 and TopVia2                                        |
| Slt.a.TM2                | Min. TopMetal2:slit width                                                               |
| Slt.b.TM2                | Max. TopMetal2:slit width                                                               |
| Slt.c.TM2                | Max. TopMetal2 width without requiring a slit                                           |
| Slt.e.TM2                | No slits required on bond pads                                                          |
| Slt.f.TM2                | Min. TopMetal2 enclosure of TopMetal2:slit                                              |
| Slt.h4                   | Min. TopMetal2:slit space to TopVia2                                                    |
| Pin.a                    | Min. Activ enclosure of Activ:pin                                                       |
| Pin.b                    | Min. GatPoly enclosure of GatPoly:pin                                                   |
| Pin.e                    | Min. Metal1 enclosure of Metal1:pin                                                     |
| Pin.f.M2                 | Min. Metal2 enclosure of Metal2:pin                                                     |
| Pin.f.M3                 | Min. Metal3 enclosure of Metal3:pin                                                     |
| Pin.f.M4                 | Min. Metal4 enclosure of Metal4:pin                                                     |
| Pin.f.M5                 | Min. Metal5 enclosure of Metal5:pin                                                     |
| Pin.g                    | Min. TopMetal1 enclosure of TopMetal1:pin                                               |
| Pin.h                    | Min. TopMetal2 enclosure of TopMetal2:pin                                               |
| NW.d1.dig                | Min. NWell space to external N+Activ inside ThickGateOx                                 |
| NW.f1.dig                | Min. NWell space to substrate tie in P+Activ inside ThickGateOx                         |
| Gat.a.SRAM               | Min. GatPoly width                                                                      |
| Gat.b.SRAM               | Min. GatPoly space or notch                                                             |
| Gat.c.SRAM               | Min. GatPoly extension over Activ (end cap)                                             |
| Gat.d.SRAM               | Min. GatPoly space to Activ                                                             |
| pSD.e.SRAM               | Min. pSD overlap of Activ when forming abutted substrate tie                            |
| pSD.g.SRAM               | Min. N+Activ or P+Activ width when forming abutted tie                                  |
| pSD.i.SRAM               | Min. pSD enclosure of PFET gate not inside ThickGateOx                                  |
| pSD.j.SRAM               | Min. pSD space to NFET gate not inside ThickGateOx                                      |
| Cnt.f.SRAM               | Min. Cont on Activ space to GatPoly                                                     |
| M1.b.SRAM                | Min. Metal1 space or notch                                                              |
| M1.c1.SRAM               | Min. Metal1 endcap enclosure of Cont                                                    |
| M2.b.SRAM                | Min. Metal2 space or notch                                                              |
| M2.c1.SRAM               | Min. Metal2 endcap enclosure of Via1                                                    |
| M3.b.SRAM                | Min. Metal3 space or notch                                                              |
| M3.c1.SRAM               | Min. Metal3 endcap enclosure of Via2                                                    |
| M4.b.SRAM                | Min. Metal4 space or notch                                                              |
| M4.c1.SRAM               | Min. Metal4 endcap enclosure of Via3                                                    |
| M5.b.SRAM                | Min. Metal5 space or notch                                                              |
| M5.c1.SRAM               | Min. Metal5 endcap enclosure of Via4                                                    |
| LBE.a                    | Min. LBE width                                                                          |
| LBE.b                    | Max. LBE width                                                                          |
| LBE.b1                   | Max. LBE area (µm²)                                                                     |
| LBE.b2                   | Min. LBE area (µm²)                                                                     |
| LBE.c                    | Min. LBE space or notch                                                                 |
| LBE.d                    | Min. LBE space to inner edge of EdgeSeal                                                |
| LBE.e.dfPad              | Min. LBE space to dfpad and Passiv                                                      |
| LBE.e.Passiv             | Min. LBE space to dfpad and Passiv                                                      |
| LBE.f                    | Min. LBE space to Activ                                                                 |
| LBE.h                    | No LBE ring allowed                                                                     |
| LBE.i                    | Max. global LBE density [%]                                                             |
| TSV_G.a                  | DeepVia has to be a ring structure                                                      |
| TSV_G.d                  | Min. DeepVia space                                                                      |
| TSV_G.f                  | Min. PWell:block enclosure of DeepVia                                                   |
| TSV_G.g                  | Min. Metal1 enclosure of DeepVia ring structure                                         |
| TSV_G.i                  | Max. global DeepVia density [%]                                                         |
| TSV_G.j                  | Max. DeepVia coverage ratio for any 500.0 x 500.0 µm² chip area [%]                     |
| forbidden.BiWind         | Forbidden drawn layer BiWind on GDS layer 3/0                                           |
| forbidden.PEmWind        | Forbidden drawn layer PEmWind on GDS layer 11/0                                         |
| forbidden.BasPoly        | Forbidden drawn layer BasPoly on GDS layer 13/0                                         |
| forbidden.DeepCo         | Forbidden drawn layer DeepCo on GDS layer 35/0                                          |
| forbidden.PEmPoly        | Forbidden drawn layer PEmPoly on GDS layer 53/0                                         |
| forbidden.EmPoly         | Forbidden gen./drawn layer EmPoly on GDS layer 53/0                                     |
| forbidden.LDMOS          | Forbidden drawn layer LDMOS on GDS layer 57/0                                           |
| forbidden.PBiWind        | Forbidden drawn layer PBiWind on GDS layer 58/0                                         |
| forbidden.Flash          | Forbidden drawn layer Flash on GDS layer 71/0                                           |
| forbidden.ColWind        | Forbidden drawn layer ColWind on GDS layer 139/0                                        |
| OffGrid.NWell            | NWell is off-grid                                                                       |
| OffGrid.PWell            | PWell is off-grid                                                                       |
| OffGrid.PWell_block      | PWell_block is off-grid                                                                 |
| OffGrid.nBuLay           | nBuLay is off-grid                                                                      |
| OffGrid.nBuLay_block     | nBuLay_block is off-grid                                                                |
| OffGrid.Activ            | Activ is off-grid                                                                       |
| OffGrid.ThickGateOx      | ThickGateOx is off-grid                                                                 |
| OffGrid.Activ_filler     | Activ_filler is off-grid                                                                |
| OffGrid.GatPoly_filler   | GatPoly_filler is off-grid                                                              |
| OffGrid.GatPoly          | GatPoly is off-grid                                                                     |
| OffGrid.pSD              | pSD is off-grid                                                                         |
| OffGrid.nSD              | nSD is off-grid                                                                         |
| OffGrid.nSD_block        | nSD_block is off-grid                                                                   |
| OffGrid.EXTBlock         | EXTBlock is off-grid                                                                    |
| OffGrid.SalBlock         | SalBlock is off-grid                                                                    |
| OffGrid.Cont             | Cont is off-grid                                                                        |
| OffGrid.Activ_nofill     | Activ_nofill is off-grid                                                                |
| OffGrid.GatPoly_nofill   | GatPoly_nofill is off-grid                                                              |
| OffGrid.Metal1           | Metal1 is off-grid                                                                      |
| OffGrid.Via1             | Via1 is off-grid                                                                        |
| OffGrid.Metal2           | Metal2 is off-grid                                                                      |
| OffGrid.Via2             | Via2 is off-grid                                                                        |
| OffGrid.Metal3           | Metal3 is off-grid                                                                      |
| OffGrid.Via3             | Via3 is off-grid                                                                        |
| OffGrid.Metal4           | Metal4 is off-grid                                                                      |
| OffGrid.Via4             | Via4 is off-grid                                                                        |
| OffGrid.Metal5           | Metal5 is off-grid                                                                      |
| OffGrid.MIM              | MIM is off-grid                                                                         |
| OffGrid.Vmim             | Vmim is off-grid                                                                        |
| OffGrid.TopVia1          | TopVia1 is off-grid                                                                     |
| OffGrid.TopMetal1        | TopMetal1 is off-grid                                                                   |
| OffGrid.TopVia2          | TopVia2 is off-grid                                                                     |
| OffGrid.TopMetal2        | TopMetal2 is off-grid                                                                   |
| OffGrid.Passiv           | Passiv is off-grid                                                                      |
| OffGrid.Metal1_filler    | Metal1_filler is off-grid                                                               |
| OffGrid.Metal2_filler    | Metal2_filler is off-grid                                                               |
| OffGrid.Metal3_filler    | Metal3_filler is off-grid                                                               |
| OffGrid.Metal4_filler    | Metal4_filler is off-grid                                                               |
| OffGrid.Metal5_filler    | Metal5_filler is off-grid                                                               |
| OffGrid.TopMetal1_filler | TopMetal1_filler is off-grid                                                            |
| OffGrid.TopMetal2_filler | TopMetal2_filler is off-grid                                                            |
| OffGrid.Metal1_nofill    | Metal1_nofill is off-grid                                                               |
| OffGrid.Metal2_nofill    | Metal2_nofill is off-grid                                                               |
| OffGrid.Metal3_nofill    | Metal3_nofill is off-grid                                                               |
| OffGrid.Metal4_nofill    | Metal4_nofill is off-grid                                                               |
| OffGrid.Metal5_nofill    | Metal5_nofill is off-grid                                                               |
| OffGrid.TopMetal1_nofill | TopMetal1_nofill is off-grid                                                            |
| OffGrid.TopMetal2_nofill | TopMetal2_nofill is off-grid                                                            |
| OffGrid.NoMetFiller      | NoMetFiller is off-grid                                                                 |
| OffGrid.Metal1_slit      | Metal1_slit is off-grid                                                                 |
| OffGrid.Metal2_slit      | Metal2_slit is off-grid                                                                 |
| OffGrid.Metal3_slit      | Metal3_slit is off-grid                                                                 |
| OffGrid.Metal4_slit      | Metal4_slit is off-grid                                                                 |
| OffGrid.Metal5_slit      | Metal5_slit is off-grid                                                                 |
| OffGrid.TopMetal1_slit   | TopMetal1_slit is off-grid                                                              |
| OffGrid.TopMetal2_slit   | TopMetal2_slit is off-grid                                                              |
| OffGrid.EdgeSeal         | EdgeSeal is off-grid                                                                    |
| OffGrid.EmWind           | EmWind is off-grid                                                                      |
| OffGrid.dfpad            | dfpad is off-grid                                                                       |
| OffGrid.Polimide         | Polimide is off-grid                                                                    |
| OffGrid.TRANS            | TRANS is off-grid                                                                       |
| OffGrid.IND              | IND is off-grid                                                                         |
| OffGrid.RES              | RES is off-grid                                                                         |
| OffGrid.RFMEM            | RFMEM is off-grid                                                                       |
| OffGrid.Recog_diode      | Recog_diode is off-grid                                                                 |
| OffGrid.Recog_esd        | Recog_esd is off-grid                                                                   |
| OffGrid.DigiBnd          | DigiBnd is off-grid                                                                     |
| OffGrid.DigiSub          | DigiSub is off-grid                                                                     |
| OffGrid.SRAM             | SRAM is off-grid                                                                        |
| OffGrid.dfpad_pillar     | dfpad_pillar is off-grid                                                                |
| OffGrid.dfpad_sbump      | dfpad_sbump is off-grid                                                                 |
| OffGrid.DeepVia          | DeepVia is off-grid                                                                     |
| OffGrid.LBE              | LBE is off-grid                                                                         |
| OffGrid.PolyRes          | PolyRes is off-grid                                                                     |
