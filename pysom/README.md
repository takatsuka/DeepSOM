# PySOM

The most powerful, extensible Self-Organizing Map library for Python.

- High performance compute engine optimized with LLVM based toolchain.
- Customizable to support variety of cutting edge SOM models.

## Message to the Maintainer

Use `pysom/components` for SOM components, like the SOM class itself and the
SOM layer, containers etc.

Use `pysom/utils` for any non-SOM specific functionality, like activation
functions, transition functions, learning growth/decay functions, etc.

Use the base directory `pysom` to store public methods that should be
imported by other libraries.
