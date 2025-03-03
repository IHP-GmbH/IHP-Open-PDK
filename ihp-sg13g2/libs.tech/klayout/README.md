Note on running PyCells:
Location of the Python-generated pre-compiled cached files (*.pyc) can be controlled via environment variable `PYTHONPYCACHEPREFIX`.
```bash
export PYTHONPYCACHEPREFIX=/tmp
```

Support for 'conditional compilation' in a C-style manner of PyCell code (preprocessing directives should start on the beginning of the line):

```
#ifdef name (|| name)*
    ...some code...
#else
    ...some other code...
#endif
```

The #ifdef-block is executed (name is considered as defined) if
  1. An environment variable name can be found case-insentive, or
  2. The name can be found case-insentive as part of a process name of the process chain beginnig at
     the current process upwards through all parent processes.
otherwise the #else-block is executed

The current process chain will be dumped if the environment variable 'IHP\_PYCELL\_LIB\_PRINT\_PROCESS_TREE'
is set.

The list of names which are used in an #ifdef-statement and are considered as 'defined' will be dumped
if the environment variable 'IHP\_PYCELL\_LIB\_PRINT\_DEFINES\_SET' is set.

On non-windows platforms using the 'conditional PyCell compilation' feature, the Python library `psutil` must be installed.
