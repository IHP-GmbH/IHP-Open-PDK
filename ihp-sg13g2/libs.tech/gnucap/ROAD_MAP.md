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
    - [x] mos_cap (psp)
    - [ ] mos_var (psp)

- [x] diode (sp_diode)
   - [x] antina   
   - [x] esd 
   - [x] dschottky_nb1 
   - [x] isobox 

- [ ] mosfets
  - [X] moslv (psp103)
  - [X] moshv (psp103)
  - [x] hbt (vbic)
  - [x] esd clamp (psp) (don't expose parameters)
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
