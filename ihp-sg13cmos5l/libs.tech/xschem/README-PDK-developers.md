# Symbolic link generation

Each directory contains a `*.txt` file, which denominates 
files which should be linked with the orginal SG13G2 file. 
These files are used by `$PDK_ROOT` install script to generate 
the symbolic links.

The files, which are specific to the PDK are maintained separately. 


# Naming conventions

Since the schematic contains `sg13g2_pr/` string in the instance reference 
we use symbolic links to ensure schematic portability between G2 and CMOS5L.

In the `xschemrc` file the global variable were change for the same reason. 

SG13G2_MODELS -> MODELS_NGSPICE
SG13G2_MODELS_XYCE -> MODELS_XYCE

same for SG13CMOS5L




