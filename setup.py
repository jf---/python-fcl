import os
import sys
from distutils.core import Extension, setup
from Cython.Distutils import build_ext

platform_supported = False
for prefix in ['darwin', 'linux', 'bsd']:
    if prefix in sys.platform:
        platform_supported = True
        include_dirs = [
            '/usr/include',
            '/usr/local/include',
        ]
        lib_dirs = [
            '/usr/lib',
            '/usr/local/lib',
        ]
        if 'CPATH' in os.environ:
            include_dirs += os.environ['CPATH'].split(':')
        if 'LD_LIBRARY_PATH' in os.environ:
            lib_dirs += os.environ['LD_LIBRARY_PATH'].split(':')
        break

if sys.platform == "win32":
    platform_supported = False

if not platform_supported:
    raise NotImplementedError(sys.platform)

setup(
    name="fcl",
    version="0.1",
    license = "BSD",
    packages=["fcl"],
    ext_modules=[Extension(
        "fcl.fcl",
        ["fcl/fcl.pyx"],
        include_dirs = include_dirs,
        library_dirs = lib_dirs,
        libraries=[
                "fcl"
                ],
        language="c++",
        #for clang, add: , "-Xclang", "-fcolor-diagnostics"
        extra_compile_args = ["-std=c++11"]
    )],
    cmdclass={'build_ext': build_ext},
    )
