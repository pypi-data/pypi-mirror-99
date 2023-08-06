# -*- coding: utf-8 -*-
import setuptools
from setuptools import dist
dist.Distribution().fetch_build_eggs(['Cython>=0.20', 'numpy>=1.15'])
import os
import glob
import io
import numpy.distutils.core
from numpy.distutils.fcompiler import get_default_fcompiler
from Cython.Build import cythonize
from numpy.distutils.extension import Extension

# this is to get the __version__ from version.py
with open('src/jscatter/version.py', 'r') as f:  exec(f.read())

with io.open('README.rst', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

# find fortran files
fs = glob.glob(os.path.join('src', 'jscatter', 'source', '*.f9[05]'))
fs.sort()
EXTENSIONS = []
if get_default_fcompiler(requiref90=True):
    EXTENSIONS.append(Extension(name='jscatter.fscatter',
                             sources=fs,
                             extra_f90_compile_args=['-fopenmp'],
                             libraries=['gomp'],
                             # extra_f90_compile_args=['--debug','-fbounds-check'],
                             # f2py_options=['--debug-capi']
                             ))

# cython and c compilation
c_extensions = [Extension(name='jscatter.libs.cubature._cubature',
                    sources = [
                        'src/jscatter/libs/cubature/cpackage/hcubature.c',
                        'src/jscatter/libs/cubature/cpackage/pcubature.c',
                        'src/jscatter/libs/cubature/get_ptr.c',
                        'src/jscatter/libs/cubature/_cubature.pyx',
                        ],
                    include_dirs = [numpy.get_include()],
                    language='c'),
                Extension('jscatter.libs.cubature._test_integrands',
                    sources = ['src/jscatter/libs/cubature/_test_integrands.pyx'],
                    include_dirs = [numpy.get_include()],
                    language='c'),
                ]
EXTENSIONS.extend(cythonize(c_extensions, compiler_directives={'linetrace': True,
                                                               'language_level' : "3"}))




description=("Combines dataArrays with attributes for fitting, plotting" 
             "and analysis including models for Xray and neutron scattering")

fileext=['*.txt', '*.rst', '*.dat', '*.html',  '*.ipynb', '*.md', '*.f95', '*.f90',
         '*.tiff', '*.png', '*.jpg', '*.agr', '*.gif',
         '*.Dq', '*.pdb', '*.pdh', '*.cif']

numpy.distutils.core.setup(name='jscatter',
                           version=__version__,
                           description=description,
                           long_description=long_description,
                           author='Ralf Biehl',
                           author_email='ra.biehl@fz-juelich.de',
                           url='https://gitlab.com/biehl/jscatter',
                           project_urls={"Documentation": "http://jscatter.readthedocs.io/",
                                         "Source Code": "https://gitlab.com/biehl/jscatter",
                                         "Live Demo": "https://mybinder.org/v2/gl/biehl%2Fjscatter/master?filepath="
                                                      "src%2Fjscatter%2Fexamples%2Fnotebooks"},
                           platforms=["linux", "osx", "windows"],
                           classifiers=[
                               'Development Status :: 5 - Production/Stable',
                               'Intended Audience :: Science/Research',
                               'Operating System :: POSIX :: Linux',
                               'Operating System :: MacOS :: MacOS X',
                               'Operating System :: Microsoft :: Windows :: Windows 10',
                               'Programming Language :: Python :: 3.5',
                               'Programming Language :: Python :: 3.6',
                               'Programming Language :: Python :: 3.7',
                               'Programming Language :: Python :: 3.8',
                               'Programming Language :: Python :: 3.9',
                               'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                               'Programming Language :: Python',
                               'Topic :: Scientific/Engineering :: Physics'],
                           include_package_data=True,
                           package_dir={'': 'src'},
                           py_modules=[],
                           packages=setuptools.find_packages('src'),
                           package_data={'': fileext},
                           # data_files=datafiles,
                           dependency_links=[''],
                           install_requires=["numpy >= 1.15 ",
                                             "scipy >= 1.4",
                                             "matplotlib >= 2",
                                             "Pillow >= 7.0",
                                             "cython"],
                           ext_modules=EXTENSIONS,
                           test_suite='jscatter.test.suite'
                           )
