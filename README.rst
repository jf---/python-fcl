
This fork has been superceded by `BerkeleyAutomation
<https://github.com/BerkeleyAutomation/python-fcl/>`_ branch.



python-fcl
=========

About
-----
This library is a Python binding for the FCL library (0.5.0 atm).

Build
-----
Building python-fcl requires **FCL headers and libraries** and a recent version of **Cython**.
After installing both, you can specify their location with the --include-dirs
and --library-dirs command line options if they are not found automatically:

    $ python setup.py build_ext --include-dirs /path/to/includes --library-dirs /path/to/libraries

If you use ubuntu (>= 16.10) and install libfcl-dev, you can simply use the following command:

    $ python setup.py build_ext 

Install
-------
You can install python-fcl using the normal distutils install command:

    $ python setup.py install
