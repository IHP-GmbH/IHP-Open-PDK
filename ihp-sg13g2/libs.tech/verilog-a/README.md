# Compilation and installation of verilog-a models for ngspice and Xyce


Each model should be placed in a separate directory like `psp103`
If you are going to add a new model place it in a separate directory and edit the build script.

In order to compile the Verilog-A models for ngspice use the following command:

```
./openvaf-compile-va.sh

```
The binaries will be generated in the following direcotry
`$PDK_ROOT/$PDK/libs.tech/ngspice/osdi/` and referenced in `.spiceinit`

If you would like to compile the models for xyce just run the script:

```
./adms-compile-va.sh

```

The binaries are placed in the default location `$PDK_ROOT/$PDK/libs.tech/xyce/plugins`


You can use the adms models using `-plugin` options in Xyce as follows:
```
Xyce -plugin  $PDK_ROOT/$PDK/libs.tech/xyce/plugins/Xyce_Plugin_PSP103_VA.so your_netlist.spice

```

