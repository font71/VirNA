# from distutils.core import setup
from setuptools import setup
from Cython.Build import cythonize


# setup(ext_modules=cythonize('libdist.pyx', gdb_debug=True), compiler_directives={'language_level' : "3"})
setup(ext_modules=cythonize('libdist.pyx', gdb_debug=True))