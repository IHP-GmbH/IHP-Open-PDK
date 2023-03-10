# IHP Open Source PDK
130nm BiCMOS Open Source PDK, dedicated for Analog, Mixed Signal and RF Design

IHP Open Source PDK project goal is to provide a fully open source Process
Design Kit and related data, which can be used to create manufacturable
designs at IHP’s facility.

As of March 2023, this repository is targeting the SG13G2 process node.

[<p align="center"><img src="docs/images/ihp_logo.png" alt="IHP Logo Image" width="50%"/></p>](https://github.com/IHP-GmbH/IHP-Open-PDK)

# Current status -- Preview

> **Warning**
>
> IHP is currently treating the current content as a **preview only**.

While the SG13G2 process node and the PDK from which this open source
release was derived have been used to create many designs that have been
successfully manufactured in significant quantities, the open source PDK
is not intended to be used for production at this moment.

# SG13G2 Process Node

SG13G2 is a high performance BiCMOS technology with a 0.13 μm CMOS process. It contains bipolar
devices based on SiGe:C npn-HBT's with up to 300 GHz transient frequency and 500 GHz oscillation
frequency. This process provides 2 gate oxides: A thin gate oxide for the 1.2 V digital logic and a thick
oxide for a 3.3 V supply voltage. For both modules NMOS, PMOS and isolated NMOS transistors are
offered. Further passive components like poly silicon resistors and MIM capacitors are available. The
backend option offers 5 thin metal layers, two thick metal layers (2 and 3 μm thick) and a MIM layer.

# PDK Contents

* GDSII view of primitive devices
* KLayout layer property file
* HSPICE Models of HBT devices
* SG13G2 Process specification
* MOS/HBT Measurements in MDM format
* Project Roadmap Gantt chart

# About IHP

**The IHP is a non-university research establishment institutionally funded by the German federal and state governments and a member of the Leibniz Association.**

The IHP is one of the world's leading research institutions in the field of silicon/germanium electronics. In this field, it has extensive, closely coordinated expertise in semiconductor technology, materials research, high-frequency circuit design and system solutions. Its electronic and photonic-electronic technologies and circuits are among the most powerful in the world. In the speed of silicon-based transistors, IHP holds the world record with 720 GHz maximum oscillation frequency. The institute has a pilot line that manufactures circuits using its high-performance SiGe BiCMOS technologies. Through its research and manufacturing services, IHP contributes significantly to the innovative strength of Germany and Europe, especially in the field of ultrahigh-frequency electronics. The institute's research results are applied in socially important areas such as semiconductor manufacturing, wireless and power broadband communications, health, space, Industry 4.0 or Agriculture 4.0 and mobility.

## Contacting IHP

Requests for more information about SG13G2 and other standard and
custom foundry technologies can be emailed to \<TBD\>.

# License

The IHP Open Source PDK is released under the [Apache 2.0 license](LICENSE).

The copyright details are:
    
    Copyright 2023 IHP PDK Authors

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       https://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
