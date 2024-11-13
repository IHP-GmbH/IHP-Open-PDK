# Compilation and installation of the psp_103 model for XYCE


Each model should be placed in a separate directory like `psp103`

If you would like to compile the models just run the script:

```
./adms-compile-va.sh

```
If you are going to add a model place it in a separate directory and edit the build script.

The binaries are placed in the default location `$PDK_ROOT/$PDK/libs.tech/xyce/plugins`


You can use the adms models using `-plugin` options in Xyce as follows:
```
Xyce -plugin  $PDK_ROOT/$PDK/libs.tech/xyce/plugins/Xyce_Plugin_PSP103_VA.so your_netlist.spice


```

