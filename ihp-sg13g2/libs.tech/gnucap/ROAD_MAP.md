# Port Device library to Verilog-A 

- [x] resistors
    - [x] parasitic
    - [x] rsil
    - [x] rhigh
    - [x] rppd

- [x] capacitors
    - [x] cparasitic
    - [x] cap_cmim
    - [x] cap_rfcmim

- [ ] diode

- [ ] mosfets
  - [X] moslv
  - [X] moshv
  - [ ] hbt
  - [ ] esd
  - [ ] dschottky_nb1
  - [ ] bondpad
 
## TODOs

- test setting multiplicity via $mfactor during device instantiation
- decide which resistor, capacitor, inductor primitives to use for parasitics 
- improve performance of ngspice mc tests  
- built pipline that compiles devices to osdi 

- Clean up test harness
  - `make check` should write stdout and stderr to an intermediate log file
  - test cases should write regression data explicitly to an output file
  - delete the log file if the test passes
