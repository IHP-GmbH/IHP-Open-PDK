## Current status -- *Minimum Rule Set*

These are layout rules necessary for all layouts in standard MPW runs. The minimum required rules are
tested with the MinimumDRC script during the tape-in procedure.
For special mask sets, like for BEOL runs, some rules are not important. This is mentioned in the header of
a section.

### 1.1 Activ (not in BEOL)
| Rule              | Description                                          |
|-------------------|------------------------------------------------------|
| Act.a             | Minimum **Activ** width                              |
| Act.b             | Minimum **Activ** space                              |
### 1.2 Thick Gate Oxide (not in BEOL)
| Rule              | Description                                          |
|-------------------|------------------------------------------------------|
| TGO.f             | Minimum **ThickGateOx** width                        |
### 1.3 GatPoly (not in BEOL)
| Rule              | Description                                          |
|-------------------|------------------------------------------------------|
| Gat.a             | Minimum **GatPoly** width                            |
| Gat.b             | Minimum **GatPoly** space                            |
| Gat.d             | Minimum **GatPoly** to **Active** space              |
### 1.4 Cont (not in BEOL)
| Rule              | Description                                          |
|-------------------|------------------------------------------------------|
| Cnt.a             | Min. and max. size of **Cont**                       |
| Cnt.b             | Min. **Cont** space                                  |
### 1.5 Metal1
| Rule              | Description                                          |
|-------------------|------------------------------------------------------|
| M1.a              | Min. width of **Metal1**                             |
| M1.b              | Min. **Metal1** space                                |
### 1.6 Metal(n=2-5)
| Rule              | Description                                          |
|-------------------|------------------------------------------------------|
| M2.a              | Min. width of **Metal2**                             |
| M2.b              | Min. **Metal2** space                                |
| M3.a              | Min. width of **Metal3**                             |
| M3.b              | Min. **Metal3** space                                |
| M4.a              | Min. width of **Metal4**                             |
| M4.b              | Min. **Metal4** space                                |
| M5.a              | Min. width of **Metal5**                             |
| M5.b              | Min. **Metal5** space                                |
### 1.7 Via(n=1-4)
| Rule              | Description                                          |
|-------------------|------------------------------------------------------|
| V1.a              | Minimum and maximum **Via1** area                    |
| V1.b              | Minimum **Via1** space                               |
| V2.a              | Minimum and maximum **Via2** area                    |
| V2.b              | Minimum **Via2** space                               |
| V3.a              | Minimum and maximum **Via3** area                    |
| V3.b              | Minimum **Via3** space                               |
| V4.a              | Minimum and maximum **Via4** area                    |
| V4.b              | Minimum **Via4** space                               |
### 1.8 TopVia1
| Rule              | Description                                          |
|-------------------|------------------------------------------------------|
| TV1.a             | Minimum and maximum **TopVia1** area                 |
| TV1.b             | Minimum **TopVia1** space                            |
### 1.9 TopMetal1
| Rule              | Description                                          |
|-------------------|------------------------------------------------------|
| TM1.a             | Min. width of **TopMetal1**                          |
| TM1.b             | Min. **TopMetal1** space                             |
### 1.10 TopVia2
| Rule              | Description                                          |
|-------------------|------------------------------------------------------|
| TV2.a             | Minimum and maximum **TopVia2** area                 |
| TV2.b             | Minimum **TopVia2** space                            |
### 1.11 TopMetal2
| Rule              | Description                                          |
|-------------------|------------------------------------------------------|
| TM2.a             | Min. width of **TopMetal2**                          |
| TM2.b             | Min. **TopMetal2** space                             |
### 1.12 Passiv
| Rule              | Description                                          |
|-------------------|------------------------------------------------------|
| Pas.a             | Minimum **Passiv** width                             |
| Pas.b             | Minimum **Passiv** space                             |
### 1.13 Density rules
This section is a summary of all minimum required density rules.
### 1.13.1 Front-end density rules
| Rule              | Description                                          |
|-------------------|------------------------------------------------------|
| GFil.g            | Min. global **GatPoly** density                      |
| AFil.g            | Minimum global **Activ** coverage                    |
| AFil.g1           | Maximum global **Activ** coverage                    |
| AFil.g2           | Minimum **Activ** coverage ratio                     |
| AFil.g3           | Maximum **Activ** coverage ratio                     |
### 1.13.2 Back-end density rules
| Rule              | Description                                          |
|-------------------|------------------------------------------------------|
| M1.j              | Min. global **Metal1** density                       |
| M1.k              | Max. global **Metal1** density                       |
| M2.j              | Min. global **Metal2** density                       |
| M2.k              | Max. global **Metal2** density                       |
| M3.j              | Min. global **Metal3** density                       |
| M3.k              | Max. global **Metal3** density                       |
| M4.j              | Min. global **Metal4** density                       |
| M4.k              | Max. global **Metal4** density                       |
| M5.j              | Min. global **Metal5** density                       |
| M5.k              | Max. global **Metal5** density                       |
| M1Fil.h           | Minimum **Metal1** coverage ratio                    |
| M1Fil.k           | Maximum **Metal1** coverage ratio                    |
| M2Fil.h           | Minimum **Metal2** coverage ratio                    |
| M2Fil.k           | Maximum **Metal2** coverage ratio                    |
| M3Fil.h           | Minimum **Metal3** coverage ratio                    |
| M3Fil.k           | Maximum **Metal3** coverage ratio                    |
| M4Fil.h           | Minimum **Metal4** coverage ratio                    |
| M4Fil.k           | Maximum **Metal4** coverage ratio                    |
| M5Fil.h           | Minimum **Metal5** coverage ratio                    |
| M5Fil.k           | Maximum **Metal5** coverage ratio                    |
| TM1.c             | Min. global **TopMetal1** density                    |
| TM1.~~c1~~d       | Max. global **TopMetal1** density                    |
| TM2.c             | Min. global **TopMetal2** density                    |
| TM2.c1            | Max. global **TopMetal2** density                    |
### 1.14 LBE
| Rule              | Description                                          |
|-------------------|------------------------------------------------------|
| LBE.a             | Min. width of **LBE**                                |
| LBE.b             | Max. width of **LBE**                                |
| LBE.b1            | Max. allowed **LBE** area                            |
| LBE.c             | **LBE** space or notch                               |
| LBE.d             | Min. space of **LBE** to inner edge of **Edge Seal** |
| LBE.h             | No **LBE** ring allowed                              |
| LBE.i             | Max. global **LBE** density                          |
### 1.15 Pin layer rules
| Rule              | Description                                          |
|-------------------|------------------------------------------------------|
| Pin.a             | Minimum **Activ** enclosure of **Active_pin**        |
| Pin.b             | Minimum **GatPoly** enclosure of **GatPoly_pin**     |
| Pin.c             | Minimum **NWell** enclosure of **NWell_pin**         |
| Pin.e             | Minimum **Metal1** enclosure of **Metal1_pin**       |
| Pin.f2            | Minimum **Metal2** enclosure of **Metal2_pin**       |
| Pin.f3            | Minimum **Metal3** enclosure of **Metal3_pin**       |
| Pin.f4            | Minimum **Metal4** enclosure of **Metal4_pin**       |
| Pin.f5            | Minimum **Metal5** enclosure of **Metal5_pin**       |
| Pin.g             | Minimum **TopMetal1** enclosure of **TopMetal1_pin** |
| Pin.h             | Minimum **TopMetal2** enclosure of **TopMetal2_pin** |
### 1.16 Forbidden layers
Following layers are forbidden in designs submitted for sg13g2 technology.
| Rule              | Description                                          |
|-------------------|------------------------------------------------------|
| forbidden.BiWind  | Forbidden layer **BiWind**                           |
| forbidden.PEmWind | Forbidden layer **PEmWind**                          |
| forbidden.BasPoly | Forbidden layer **BasPoly**                          |
| forbidden.DeepCo  | Forbidden layer **DeepCo**                           |
| forbidden.PEmPoly | Forbidden layer **PEmPoly**                          |
| forbidden.EmPoly  | Forbidden layer **EmPoly**                           |
| forbidden.LDMOS   | Forbidden layer **LDMOS**                            |
| forbidden.PBiWind | Forbidden layer **PBiWind**                          |
| forbidden.Flash   | Forbidden layer **Flash**                            |
| forbidden.ColWind | Forbidden layer **ColWind**                          |

