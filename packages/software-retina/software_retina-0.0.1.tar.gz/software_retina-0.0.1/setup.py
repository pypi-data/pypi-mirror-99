from Cython.Build import cythonize
from setuptools import setup
from distutils.core import setup, Extension
import numpy

ext_modules = [
    Extension(
        "software_retina.utils", 
        ["src/software_retina/utils.pyx"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
        include_dirs=[numpy.get_include()],
    ),
    Extension(
        "software_retina.retina",
        ["src/software_retina/retina.pyx"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
        include_dirs=['pxd', numpy.get_include()],

    ),
    Extension(
        "software_retina.rf_generation",
        ["src/software_retina/rf_generation.pyx"],
        include_dirs=[numpy.get_include()],
    ),
]

setup(
    name="software_retina",
    ext_modules=cythonize(ext_modules),
)

# python setup.py build_ext --inplace