#!/usr/bin/env python
from setuptools import setup, find_packages
 
setup(
    name = "tofimaging",
    version = "0.0.4",
    author = "Matteo Busi",
    author_email = "mbusi2691@gmail.com",
    packages = find_packages('PythonModules'),
    include_package_data = True,
    test_suite = 'Tests',
    install_requires = [
        'numpy',
        'pyfits',
        'pillow',
        'lmfit',
        'tqdm',
        'scipy',
        'scikit-image',
        'matplotlib',
        'astropy',
    ],
    dependency_links = [
    ],
    description = "Library for neutron ToF imaging",
    license = 'BSD',
    keywords = "edge fitting",
    url = "https://github.com/neutronimaging/ToFImaging",
    classifiers = ['Development Status :: 3 - Alpha',
                   'Topic :: Scientific/Engineering :: Physics',
                   'Intended Audience :: Developers',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.5'],
)