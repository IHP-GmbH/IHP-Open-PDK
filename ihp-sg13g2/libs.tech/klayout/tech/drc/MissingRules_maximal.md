# Missing Rules

| Name        | Description                                                                                                                    |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------ |
| NW.b        | Min. NWell space or notch (same net). NWell regions separated by less than this value will be merged.                          |
| NW.b1       | Min. PWell width between NWell regions (different net) (Note 3)                                                                |
| NW.c        | Min. NWell enclosure of P+Activ not inside ThickGateOx                                                                         |
| NW.c1       | Min. NWell enclosure of P+Activ inside ThickGateOx                                                                             |
| NW.d        | Min. NWell space to external N+Activ not inside ThickGateOx                                                                    |
| NW.e        | Min. NWell enclosure of NWell tie surrounded entirely by NWell in N+Activ not inside ThickGateOx                               |
| NW.e1       | Min. NWell enclosure of NWell tie surrounded entirely by NWell in N+Activ inside ThickGateOx                                   |
| PWB.d       | Min. PWell:block overlap of NWell                                                                                              |
| PWB.e       | Min. PWell:block space to (N+Activ not inside ThickGateOx) in PWell                                                            |
| PWB.e1      | Min. PWell:block space to (N+Activ inside ThickGateOx) in PWell                                                                |
| PWB.f       | Min. PWell:block space to (P+Activ not inside ThickGateOx) in PWell                                                            |
| PWB.f1      | Min. PWell:block space to (P+Activ inside ThickGateOx) in PWell                                                                |
| NBL.b       | Min. nBuLay space or notch (same net)                                                                                          |
| NBL.c       | Min. PWell width between nBuLay regions (different net) (Note 1)                                                               |
| NBL.d       | Min. PWell width between nBuLay and NWell (different net) (Note 1)                                                             |
| NBL.e       | Min. nBuLay space to unrelated N+Activ                                                                                         |
| NBL.f       | Min. nBuLay space to unrelated P+Activ                                                                                         |
| Act.c       | Min. Activ drain/source extension                                                                                              |
| AFil.c      | Min. Activ:filler space to Cont, GatPoly                                                                                       |
| AFil.c1     | Min. Activ:filler space to Activ                                                                                               |
| AFil.d      | Min. Activ:filler space to NWell, nBuLay                                                                                       |
| AFil.e      | Min. Activ:filler space to TRANS                                                                                               |
| AFil.i      | Min. Activ:filler space to edges of PWell:block                                                                                |
| AFil.j      | Min. nSD:block and SalBlock enclosure of Activ:filler inside PWell:block                                                       |
| Gat.a1      | Min. GatPoly width for channel length of 1.2 V NFET                                                                            |
| Gat.a2      | Min. GatPoly width for channel length of 1.2 V PFET                                                                            |
| Gat.g       | Min. GatPoly width for 45-degree bent shapes if the bend GatPoly length is > 0.39 µm                                           |
| GFil.e      | Min. GatPoly:filler space to NWell, nBuLay                                                                                     |
| GFil.i      | Max. GatPoly:nofill area (µm²)                                                                                                 |
| pSD.c1      | Min. pSD enclosure of P+Activ in PWell                                                                                         |
| nSDB.d      | Min. nSD:block overlap of pSD (Note 1)                                                                                         |
| Cnt.c       | Min. Activ enclosure of Cont                                                                                                   |
| Cnt.d       | Min. GatPoly enclosure of Cont                                                                                                 |
| Cnt.e       | Min. Cont on GatPoly space to Activ                                                                                            |
| Cnt.g1      | Min. pSD space to Cont on nSD-Activ                                                                                            |
| Cnt.g2      | Min. pSD overlap of Cont on pSD-Activ                                                                                          |
| CntB.b1     | Min. ContBar space with common run > 5 µm                                                                                      |
| CntB.c      | Min. Activ enclosure of ContBar                                                                                                |
| CntB.d      | Min. GatPoly enclosure of ContBar                                                                                              |
| CntB.h1     | Min. Metal1 enclosure of ContBar                                                                                               |
| M1.e        | Min. space of Metal1 lines if, at least one line is wider than 0.3 µm and the parallel run is more than 1.0 µm                 |
| M1.f        | Min. space of Metal1 lines if, at least one line is wider than 10.0 µm and the parallel run is more than 10.0 µm               |
| M1.g        | Min. 45-degree bent Metal1 width if the bent metal length is > 0.5 µm                                                          |
| M1.i        | Min. space of Metal1 lines of which at least one is bent by 45-degree                                                          |
| M2.e        | Min. space of Metal2 lines if, at least one line is wider than 0.39 µm and the parallel run is more than 1.0 µm                |
| M2.f        | Min. space of Metal2 lines if, at least one line is wider than 10.0 µm and the parallel run is more than 10.0 µm               |
| M2.g        | Min. 45-degree bent Metal2 width if the bent metal length is > 0.5 µm                                                          |
| M2.i        | Min. space of Metal2 lines of which at least one is bent by 45-degree                                                          |
| M3.e        | Min. space of Metal3 lines if, at least one line is wider than 0.39 µm and the parallel run is more than 1.0 µm                |
| M3.f        | Min. space of Metal3 lines if, at least one line is wider than 10.0 µm and the parallel run is more than 10.0 µm               |
| M3.g        | Min. 45-degree bent Metal3 width if the bent metal length is > 0.5 µm                                                          |
| M3.i        | Min. space of Metal3 lines of which at least one is bent by 45-degree                                                          |
| M4.e        | Min. space of Metal4 lines if, at least one line is wider than 0.39 µm and the parallel run is more than 1.0 µm                |
| M4.f        | Min. space of Metal4 lines if, at least one line is wider than 10.0 µm and the parallel run is more than 10.0 µm               |
| M4.g        | Min. 45-degree bent Metal4 width if the bent metal length is > 0.5 µm                                                          |
| M4.i        | Min. space of Metal4 lines of which at least one is bent by 45-degree                                                          |
| M5.e        | Min. space of Metal5 lines if, at least one line is wider than 0.39 µm and the parallel run is more than 1.0 µm                |
| M5.f        | Min. space of Metal5 lines if, at least one line is wider than 10.0 µm and the parallel run is more than 10.0 µm               |
| M5.g        | Min. 45-degree bent Metal5 width if the bent metal length is > 0.5 µm                                                          |
| M5.i        | Min. space of Metal5 lines of which at least one is bent by 45-degree                                                          |
| M1Fil.a2    | Max. Metal1:filler width                                                                                                       |
| M2Fil.a2    | Max. Metal2:filler width                                                                                                       |
| M3Fil.a2    | Max. Metal3:filler width                                                                                                       |
| M4Fil.a2    | Max. Metal4:filler width                                                                                                       |
| M5Fil.a2    | Max. Metal5:filler width                                                                                                       |
| V1.c        | Min. Metal1 enclosure of Via1                                                                                                  |
| V2.c        | Min. Metal2 enclosure of Via2                                                                                                  |
| V3.c        | Min. Metal3 enclosure of Via3                                                                                                  |
| V4.c        | Min. Metal4 enclosure of Via4                                                                                                  |
| TV1.c       | Min. Metal5 enclosure of TopVia1                                                                                               |
| TV1.d       | Min. TopMetal1 enclosure of TopVia1                                                                                            |
| TM1Fil.a1   | Max. TopMetal1:filler width                                                                                                    |
| TV2.c       | Min. TopMetal1 enclosure of TopVia2                                                                                            |
| TV2.d       | Min. TopMetal2 enclosure of TopVia2                                                                                            |
| TM2.bR      | Min. space of TopMetal2 lines if, at least one line is wider than 5.0 µm and the parallel run is more than 50.0 µm (Note 1, 2) |
| TM2Fil.a1   | Max. TopMetal2:filler width                                                                                                    |
| Pas.c       | Min. TopMetal2 enclosure of Passiv (Note 1)                                                                                    |
| npnG2.a     | NPN Substrate-Tie = Activ AND pSD                                                                                              |
| npnG2.b     | NPN Substrate-Tie must enclose TRANS                                                                                           |
| npnG2.c     | pSD enclosure of Activ inside NPN Substrate-Tie                                                                                |
| npnG2.d     | Min. unrelated N+Activ, NWell, PWell:block, nBuLay, nSD:block space to TRANS                                                   |
| npnG2.d1    | Min. unrelated GatPoly space to TRANS                                                                                          |
| npnG2.d2    | Min. unrelated SalBlock space to TRANS                                                                                         |
| npnG2.e     | Min. unrelated Cont space to TRANS                                                                                             |
| npnG2.f     | NPN Substrate-Ties are allowed to overlap each other                                                                           |
| npn13G2.bR  | Max. recommended total number of npn13G2 emitters per chip                                                                     |
| npn13G2L.cR | Max. recommended total number of npn13G2L emitters per chip                                                                    |
| npn13G2V.cR | Max. recommended total number of npn13G2V emitters per chip                                                                    |
| Rppd.d      | Min. EXTBlock enclosure of GatPoly                                                                                             |
| Rhi.e       | Min. EXTBlock enclosure of GatPoly                                                                                             |
| nmosi.e1    | A separate Iso-PWell contact unabutted to a nmosi device is not allowed                                                        |
| nmosi.e2    | nmosi unabutted to an Iso-PWell-Activ tie is not allowed                                                                       |
| Sdiod.d     | Min. and max. ContBar width inside nBuLay                                                                                      |
| Sdiod.e     | Min. and max. ContBar length inside nBuLay                                                                                     |
| Pad.eR      | Min. recommended Metal(n), TopMetal1, TopMetal2 exit width                                                                     |
| Pad.fR      | Min. recommended Metal(n), TopMetal1, TopMetal2 exit length                                                                    |
| Pad.i       | dfpad without TopMetal2 not allowed                                                                                            |
| Padb.a      | SBumpPad size                                                                                                                  |
| Padb.b      | Min. SBumpPad space                                                                                                            |
| Padb.c      | Min. TopMetal2 (within dfpad) enclosure of SBumpPad                                                                            |
| Padb.d      | Min. SBumpPad space to EdgeSeal                                                                                                |
| Padb.e      | Min. SBumpPad pitch (Note 1)                                                                                                   |
| Padb.f      | Allowed passivation opening shape (Note 1)                                                                                     |
| Padc.a      | CuPillarPad size                                                                                                               |
| Padc.c      | Min. TopMetal2 (within dfpad) enclosure of CuPillarPad                                                                         |
| Padc.e      | Min. CuPillarPad pitch (Note 1)                                                                                                |
| Padc.f      | Allowed passivation opening shape (Note 1)                                                                                     |
| Seal.b      | Min. Activ space to EdgeSeal-Activ, EdgeSeal-pSD, EdgeSeal-Metal(n=1-5), EdgeSeal-TopMetal1, EdgeSeal-TopMetal2                |
| Seal.d      | Min. EdgeSeal-Activ enclosure of EdgeSeal-Cont, EdgeSeal-Metal(n=1-5), EdgeSeal-TopMetal1, EdgeSeal-TopMetal2 ring             |
| Seal.f      | Min. Passiv ring outside of sealring space to EdgeSeal-Activ, EdgeSeal-Metal(n=1-5), EdgeSeal-TopMetal1, EdgeSeal-TopMetal2    |
| Seal.k      | Min. EdgeSeal 45-degree corner length (Note 1)                                                                                 |
| Seal.l      | No structures outside sealring boundary allowed                                                                                |
| Seal.m      | Only one sealring per chip allowed (Note 1)                                                                                    |
| MIM.c       | Min. Metal5 enclosure of MIM                                                                                                   |
| MIM.d       | Min. MIM enclosure of TopVia1                                                                                                  |
| MIM.gR      | Max. recommended total MIM area per chip (µm²)                                                                                 |
| Ant.a       | Max. ratio of GatPoly over field oxide area to connected Gate area                                                             |
| Ant.b       | Max. ratio of cumulative metal area (from Metal1 to TopMetal2) to connected Gate area (without protection diode)               |
| Ant.c       | Max. ratio of Cont area to connected Gate area                                                                                 |
| Ant.d       | Max. ratio of cumulative via area (from Via1 to TopVia2) to connected Gate area (without protection diode)                     |
| Ant.e       | Max. ratio of cumulative metal area (from Metal1 to TopMetal2) to connected Gate area (with protection diode)                  |
| Ant.f       | Max. ratio of cumulative via area (from Via1 to TopVia2) to connected Gate area (with protection diode)                        |
| Ant.g       | Size of protection diode (µm²) (Note 4)                                                                                        |
| LU.b        | Max. space from any portion of N+Activ inside PWell to an pSD-PWell tie                                                        |
| Slt.e1      | No slits required on MIM                                                                                                       |
| Slt.i.M1    | Min. Metal1:slit density for any Metal1 plate bigger than 35 µm x 35 µm [%]                                                    |
| Slt.i.M2    | Min. Metal2:slit density for any Metal2 plate bigger than 35 µm x 35 µm [%]                                                    |
| Slt.i.M3    | Min. Metal3:slit density for any Metal3 plate bigger than 35 µm x 35 µm [%]                                                    |
| Slt.i.M4    | Min. Metal4:slit density for any Metal4 plate bigger than 35 µm x 35 µm [%]                                                    |
| Slt.i.M5    | Min. Metal5:slit density for any Metal5 plate bigger than 35 µm x 35 µm [%]                                                    |
| Slt.i.TM1   | Min. TopMetal1:slit density for any TopMetal1 plate bigger than 35 µm x 35 µm [%]                                              |
| Slt.i.TM2   | Min. TopMetal2:slit density for any TopMetal2 plate bigger than 35 µm x 35 µm [%]                                              |
| NW.c1.dig   | Min. NWell enclosure of P+Activ inside ThickGateOx                                                                             |
| NW.e1.dig   | Min. NWell enclosure of NWell tie surrounded entirely by NWell in N+Activ inside ThickGateOx                                   |
| Cnt.c.Digi  | Min. Activ enclosure of Cont                                                                                                   |
| NW.c.SRAM   | Min. NWell enclosure of P+Activ not inside ThickGateOx                                                                         |
| NW.d.SRAM   | Min. NWell space to external N+Activ not inside ThickGateOx                                                                    |
| Act.c.SRAM  | Min. Activ drain/source extension                                                                                              |
| Cnt.c.SRAM  | Min. Activ enclosure of Cont                                                                                                   |
| Cnt.d.SRAM  | Min. GatPoly enclosure of Cont                                                                                                 |
| Cnt.g2.SRAM | Min. pSD overlap of Cont on pSD-Activ                                                                                          |
| M1.i.SRAM   | Min. space of Metal1 lines of which at least one is bent by 45-degree                                                          |
| V1.c1.SRAM  | Min. Metal1 endcap enclosure of Via1                                                                                           |
| V2.c1.SRAM  | Min. Metal2 endcap enclosure of Via2                                                                                           |
| V3.c1.SRAM  | Min. Metal3 endcap enclosure of Via3                                                                                           |
| V4.c1.SRAM  | Min. Metal4 endcap enclosure of Via4                                                                                           |
| TSV_G.b     | Min. and max. DeepVia width                                                                                                    |
| TSV_G.c     | DeepVia ring diameter                                                                                                          |
| TSV_G.e     | Min. DeepVia space to Activ, Activ:filler, GatPoly, GatPoly:filler and Cont                                                    |
