from Cython.Build import cythonize
from setuptools import setup, Extension, find_packages
# from distutils.core import setup, Extension
import numpy

ext_modules = [
    # Extension(
    #     "software_retina.utils", 
    #     ["src/software_retina/utils.pyx"],
    #     extra_compile_args=['-fopenmp'],
    #     extra_link_args=['-fopenmp'],
    #     include_dirs=[numpy.get_include()],
    # ),
    Extension(
        "src.software_retina.retina",
        ["src/software_retina/retina.pyx"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
        include_dirs=[numpy.get_include()],

    ),
    Extension(
        "src.software_retina.rf_generation",
        ["src/software_retina/rf_generation.pyx"],
        include_dirs=[numpy.get_include()],
    ),
]

setup(
    name='software-retina',
    version='0.0.5',
    author='Han M. Loo',
    author_email='nloo33755@gmail.com',
    packages=['src', 'src.software_retina', 'src.software_retina_generation'],
    package_data={'src.software_retina': ['*.pyx', '*.pxd']},
    url='https://github.com/hanl00/software-retina',
    description='A software retina inspired by the biological vision system',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    ext_modules=cythonize(ext_modules),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Cython",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    zip_safe=False,
)

# python setup.py build_ext --inplace