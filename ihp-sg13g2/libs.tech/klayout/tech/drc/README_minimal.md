## Current status -- *Preliminary*

List of available DRC rules:

| Name              | Description                                                                 |
| ----------------- | --------------------------------------------------------------------------- |
| Act.a             | Min. Activ width                                                            |
| Act.b             | Min. Activ space or notch                                                   |
| AFil.g/g1         | Global Activ density [%]                                                    |
| AFil.g2/g3        | Activ coverage ratio for any 800 x 800 µm² chip area [%]                    |
| TGO.f             | Min. ThickGateOx width                                                      |
| Gat.a             | Min. GatPoly width                                                          |
| Gat.b             | Min. GatPoly space or notch                                                 |
| Gat.d             | Min. GatPoly space to Activ                                                 |
| GFil.g            | Min. global GatPoly density [%]                                             |
| Cnt.a             | Min. and max. Cont width                                                    |
| Cnt.b             | Min. Cont space                                                             |
| M1.a              | Min. Metal1 width                                                           |
| M1.b              | Min. Metal1 space or notch                                                  |
| M1.j/k            | Global Metal1 density [%]                                                   |
| M2.a              | Min. Metal2 width                                                           |
| M2.b              | Min. Metal2 space or notch                                                  |
| M2.j/k            | Global Metal2 density [%]                                                   |
| M3.a              | Min. Metal3 width                                                           |
| M3.b              | Min. Metal3 space or notch                                                  |
| M3.j/k            | Global Metal3 density [%]                                                   |
| M4.a              | Min. Metal4 width                                                           |
| M4.b              | Min. Metal4 space or notch                                                  |
| M4.j/k            | Global Metal4 density [%]                                                   |
| M5.a              | Min. Metal5 width                                                           |
| M5.b              | Min. Metal5 space or notch                                                  |
| M5.j/k            | Global Metal5 density [%]                                                   |
| M1Fil.h/k         | Metal1 and Metal1:filler coverage ratio for any 800 x 800 µm² chip area [%] |
| M2Fil.h/k         | Metal2 and Metal2:filler coverage ratio for any 800 x 800 µm² chip area [%] |
| M3Fil.h/k         | Metal3 and Metal3:filler coverage ratio for any 800 x 800 µm² chip area [%] |
| M4Fil.h/k         | Metal4 and Metal4:filler coverage ratio for any 800 x 800 µm² chip area [%] |
| M5Fil.h/k         | Metal5 and Metal5:filler coverage ratio for any 800 x 800 µm² chip area [%] |
| V1.a              | Min. and max. Via1 width                                                    |
| V1.b              | Min. Via1 space                                                             |
| V2.a              | Min. and max. Via2 width                                                    |
| V2.b              | Min. Via2 space                                                             |
| V3.a              | Min. and max. Via3 width                                                    |
| V3.b              | Min. Via3 space                                                             |
| V4.a              | Min. and max. Via4 width                                                    |
| V4.b              | Min. Via4 space                                                             |
| TV1.a             | Min. and max. TopVia1 width                                                 |
| TV1.b             | Min. TopVia1 space                                                          |
| TM1.a             | Min. TopMetal1 width                                                        |
| TM1.b             | Min. TopMetal1 space or notch                                               |
| TM1.c/d           | Global TopMetal1 density [%]                                                |
| TV2.a             | Min. and max. TopVia2 width                                                 |
| TV2.b             | Min. TopVia2 space                                                          |
| TM2.a             | Min. TopMetal2 width                                                        |
| TM2.b             | Min. TopMetal2 space or notch                                               |
| TM2.c/d           | Global TopMetal2 density [%]                                                |
| Pas.a             | Min. Passiv width                                                           |
| Pas.b             | Min. Passiv space or notch                                                  |
| Pin.a             | Min. Activ enclosure of Activ:pin                                           |
| Pin.b             | Min. GatPoly enclosure of GatPoly:pin                                       |
| Pin.e             | Min. Metal1 enclosure of Metal1:pin                                         |
| Pin.f.M2          | Min. Metal2 enclosure of Metal2:pin                                         |
| Pin.f.M3          | Min. Metal3 enclosure of Metal3:pin                                         |
| Pin.f.M4          | Min. Metal4 enclosure of Metal4:pin                                         |
| Pin.f.M5          | Min. Metal5 enclosure of Metal5:pin                                         |
| Pin.g             | Min. TopMetal1 enclosure of TopMetal1:pin                                   |
| Pin.h             | Min. TopMetal2 enclosure of TopMetal2:pin                                   |
| LBE.a             | Min. LBE width                                                              |
| LBE.b             | Max. LBE width                                                              |
| LBE.b1            | Max. LBE area (µm²)                                                         |
| LBE.c             | Min. LBE space or notch                                                     |
| LBE.d             | Min. LBE space to inner edge of EdgeSeal                                    |
| LBE.h             | No LBE ring allowed                                                         |
| LBE.i             | Max. global LBE density [%]                                                 |
| forbidden.BiWind  | Forbidden drawn layer BiWind on GDS layer 3/0                               |
| forbidden.PEmWind | Forbidden drawn layer PEmWind on GDS layer 11/0                             |
| forbidden.BasPoly | Forbidden drawn layer BasPoly on GDS layer 13/0                             |
| forbidden.DeepCo  | Forbidden drawn layer DeepCo on GDS layer 35/0                              |
| forbidden.PEmPoly | Forbidden drawn layer PEmPoly on GDS layer 53/0                             |
| forbidden.EmPoly  | Forbidden gen./drawn layer EmPoly on GDS layer 53/0                         |
| forbidden.LDMOS   | Forbidden drawn layer LDMOS on GDS layer 57/0                               |
| forbidden.PBiWind | Forbidden drawn layer PBiWind on GDS layer 58/0                             |
| forbidden.Flash   | Forbidden drawn layer Flash on GDS layer 71/0                               |
| forbidden.ColWind | Forbidden drawn layer ColWind on GDS layer 139/0                            |
