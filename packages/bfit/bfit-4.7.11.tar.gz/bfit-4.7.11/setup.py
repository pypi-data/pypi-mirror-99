import setuptools
from distutils.core import Extension
from Cython.Build import cythonize
import numpy, os

with open("README.md", "r") as fh:
    long_description = fh.read()

# module extension
ext = Extension("bfit.fitting.integrator",
                sources=["./bfit/fitting/integrator.pyx",
                        "./bfit/fitting/FastNumericalIntegration_src/integration_fns.cpp"],
                language="c++",             # generate C++ code                        
                include_dirs=["./bfit/fitting/FastNumericalIntegration_src",numpy.get_include()],
                libraries=["m"],
                extra_compile_args=["-ffast-math"]
                )

setuptools.setup(
    name="bfit",
    version="4.7.11",
    author="Derek Fujimoto",
    author_email="fujimoto@phas.ubc.ca",
    description="β-NMR and β-NQR Data Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dfujim/bfit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",     
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Cython",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Development Status :: 5 - Production/Stable",
    ],
    install_requires=['cython>=0.28', 'numpy>=1.14', 'tqdm>=4.25.0',
                      'bdata>=6.4.2', 'matplotlib>=2.2.4', 'pandas>=0.23.0',
                      'pyyaml>=5.1', 'scipy>=1.2.0', 'iminuit>=2.3.0', 
                      'requests>=2.25.0', 'argparse>=1.4.0'],
    package_data={'': ['./data']},
    entry_points={'console_scripts':['bfit = bfit:main']},
    include_package_data=True,
    ext_modules = cythonize([ext], include_path=[numpy.get_include()]),
)
